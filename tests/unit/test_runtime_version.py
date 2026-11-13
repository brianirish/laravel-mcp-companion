"""Which Laravel version a call is answered from.

An explicit `version` wins, then a version named in the filename, then the
version the server was started with (`--version`), then the newest supported
one. The same order holds for every tool that takes a version.
"""

import sys
from unittest.mock import patch, MagicMock

import pytest

from laravel_mcp_companion.docs_updater import DEFAULT_VERSION
from laravel_mcp_companion.mcp_tools import get_version_from_path
from laravel_mcp_companion.tools.common import require_version
from laravel_mcp_companion.tools.docs import read_content
from laravel_mcp_companion.tools.learning import browse_docs
from laravel_mcp_companion.tools.search import search


@pytest.fixture
def docs(temp_dir):
    """10.x, 11.x and the newest supported version, each saying which it is."""
    root = temp_dir / "docs"
    for version in ("10.x", "11.x", DEFAULT_VERSION):
        (root / version).mkdir(parents=True)
        (root / version / "routing.md").write_text(f"# Routing\n\n## Basics\n\nRouting as documented for {version}.\n")
        (root / version / "blade.md").write_text(f"# Blade\n\n## Basics\n\nBlade as documented for {version}.\n")
    return root


class TestVersionFromPath:
    def test_a_bare_name_uses_the_default(self):
        assert get_version_from_path("blade.md") == (DEFAULT_VERSION, "blade.md")

    def test_a_bare_name_uses_the_runtime_version_when_there_is_one(self):
        assert get_version_from_path("blade.md", runtime_version="10.x") == ("10.x", "blade.md")

    def test_a_version_in_the_path_overrides_the_runtime_version(self):
        assert get_version_from_path("11.x/blade.md", runtime_version="10.x") == ("11.x", "blade.md")


class TestReads:
    def test_with_nothing_said_the_newest_version_answers(self, docs):
        assert f"documented for {DEFAULT_VERSION}" in read_content(docs, "routing.md").text

    def test_the_runtime_version_is_the_servers_default(self, docs):
        assert "documented for 10.x" in read_content(docs, "routing.md", runtime_version="10.x").text

    def test_an_explicit_version_overrides_the_runtime_version(self, docs):
        assert "documented for 11.x" in read_content(docs, "routing.md", version="11.x", runtime_version="10.x").text

    def test_a_version_in_the_filename_overrides_both(self, docs):
        reply = read_content(docs, "11.x/routing.md", version="10.x", runtime_version="10.x")

        assert "documented for 11.x" in reply.text
        assert reply.data["version"] == "11.x"


class TestBrowse:
    def test_the_runtime_version_is_the_default(self, docs):
        assert browse_docs(docs, category="frontend", runtime_version="10.x")["version"] == "10.x"

    def test_an_explicit_version_overrides_it(self, docs):
        result = browse_docs(docs, category="frontend", version="11.x", runtime_version="10.x")

        assert result["version"] == "11.x"
        assert [doc["file"] for doc in result["docs"]] == ["11.x/blade.md"]


class TestSearchScope:
    def test_with_nothing_said_the_newest_version_is_searched(self, docs):
        assert search(docs, None, "routing", sources=["core"])["scope"] == DEFAULT_VERSION

    def test_the_runtime_version_is_the_default_scope(self, docs):
        result = search(docs, None, "routing", runtime_version="10.x", sources=["core"])

        assert result["scope"] == "10.x"
        assert any("documented for 10.x" in hit["snippet"] for hit in result["results"])

    def test_an_explicit_version_overrides_it(self, docs):
        assert search(docs, None, "routing", version="11.x", runtime_version="10.x", sources=["core"])["scope"] == "11.x"

    def test_all_versions_searches_every_one(self, docs):
        result = search(docs, None, "routing", all_versions=True, runtime_version="10.x", sources=["core"], limit=10)

        assert {hit["file"].split("/")[0] for hit in result["results"]} == {"10.x", "11.x", DEFAULT_VERSION}


class TestNewVersionSimulation:
    """Simulate a new Laravel version (e.g. 14.x) appearing in the GitHub API.

    These tests verify that the entire stack handles a version bump gracefully
    without hardcoded version assumptions breaking things.
    """

    FUTURE_VERSION = "14.x"
    FUTURE_VERSIONS = ["6.x", "7.x", "8.x", "9.x", "10.x", "11.x", "12.x", "13.x", "14.x"]

    @pytest.fixture
    def future(self, docs):
        (docs / self.FUTURE_VERSION).mkdir()
        (docs / self.FUTURE_VERSION / "routing.md").write_text("# Routing\n\n## Basics\n\nRouting as documented for 14.x.\n")
        with patch('laravel_mcp_companion.mcp_tools.SUPPORTED_VERSIONS', self.FUTURE_VERSIONS), \
             patch('laravel_mcp_companion.mcp_tools.get_default_version', return_value=self.FUTURE_VERSION), \
             patch('laravel_mcp_companion.tools.common.get_default_version', return_value=self.FUTURE_VERSION):
            yield docs

    def test_version_parsing_accepts_future_version(self, future):
        assert get_version_from_path("blade.md") == (self.FUTURE_VERSION, "blade.md")

    def test_explicit_version_still_overrides(self, future):
        assert get_version_from_path("12.x/blade.md") == ("12.x", "blade.md")

    def test_read_doc_uses_future_default(self, future):
        assert "documented for 14.x" in read_content(future, "routing.md").text

    def test_browse_category_uses_future_default(self, future):
        assert browse_docs(future)["version"] == self.FUTURE_VERSION

    def test_search_uses_future_default(self, future):
        assert search(future, None, "routing", sources=["core"])["scope"] == self.FUTURE_VERSION

    def test_the_future_version_is_accepted_as_an_argument(self, future):
        require_version(self.FUTURE_VERSION)

    def test_main_uses_future_default(self):
        """Main function wires through the new default version."""
        # setup_server_environment's version check now runs through
        # mcp_tools.validate_version, which checks mcp_tools.SUPPORTED_VERSIONS
        # -- that must be patched too, or the future version is rejected.
        with patch('laravel_mcp_companion.server.GracefulShutdown'), \
             patch('laravel_mcp_companion.server.MultiSourceDocsUpdater') as mock_updater_class, \
             patch('laravel_mcp_companion.server.FastMCP') as mock_fastmcp_class, \
             patch('laravel_mcp_companion.server.setup_docs_path') as mock_setup_docs, \
             patch('laravel_mcp_companion.server.SUPPORTED_VERSIONS', self.FUTURE_VERSIONS), \
             patch('laravel_mcp_companion.server.get_default_version', return_value=self.FUTURE_VERSION), \
             patch('laravel_mcp_companion.mcp_tools.SUPPORTED_VERSIONS', self.FUTURE_VERSIONS), \
             patch.object(sys, 'argv', ['laravel-mcp-companion']):
            mock_setup_docs.return_value = "/tmp/test"
            mock_mcp = MagicMock()
            mock_fastmcp_class.return_value = mock_mcp

            from laravel_mcp_companion.server import main
            main()

            mock_updater_class.assert_called_once_with("/tmp/test", self.FUTURE_VERSION)

    def test_cache_file_contains_current_default(self):
        """Committed cache file includes the current DEFAULT_VERSION."""
        from laravel_mcp_companion.docs_updater import DEFAULT_VERSION, VERSIONS_CACHE_FILE
        import json
        assert VERSIONS_CACHE_FILE.exists(), f"Cache file missing: {VERSIONS_CACHE_FILE}"
        data = json.loads(VERSIONS_CACHE_FILE.read_text())
        assert DEFAULT_VERSION in data["versions"], (
            f"Cache file is stale: missing {DEFAULT_VERSION}"
        )

    def test_api_failure_with_cache_returns_cached_versions(self, tmp_path):
        """When API fails, the cache file provides the fallback."""
        import json
        from laravel_mcp_companion.docs_updater import get_supported_versions
        cache_file = tmp_path / ".versions_cache.json"
        cache_file.write_text(json.dumps({
            "versions": self.FUTURE_VERSIONS,
            "updated_at": "2026-04-05T00:00:00Z"
        }))

        with patch('laravel_mcp_companion.docs_updater.urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = Exception("API down")
            versions = get_supported_versions(cache_file=cache_file)

        assert versions == self.FUTURE_VERSIONS
        assert self.FUTURE_VERSION in versions