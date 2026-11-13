"""Regression tests for path traversal and input validation.

Each test here corresponds to a vulnerability that was exploitable before the
security hardening pass. They assert that untrusted tool arguments cannot be
used to read, enumerate, or write outside the documentation tree.
"""

import pytest

from laravel_mcp_companion.mcp_tools import is_safe_path
from laravel_mcp_companion.docs_updater import is_safe_section_name, is_within_directory, DocsUpdater
from laravel_mcp_companion.tools import ToolFailure
from laravel_mcp_companion.tools.common import require_version
from laravel_mcp_companion.tools.docs import compare_versions, docs_info, list_docs, read_content, read_section
from laravel_mcp_companion.tools.learning import browse_docs
from laravel_mcp_companion.tools.search import search

SECRET = "TOPSECRET-api-key-sk-live-1234"

BAD_VERSIONS = ["..", "../..", "/etc", "/", "12.x/../..", "\x00"]


@pytest.fixture
def docs_tree(tmp_path):
    """A docs tree with secrets planted outside it."""
    docs = tmp_path / "docs"
    (docs / "12.x").mkdir(parents=True)
    (docs / "12.x" / "blade.md").write_text("# Blade\n\nTemplating docs.")
    (docs / "learning_resources" / "tutorials").mkdir(parents=True)
    (docs / "learning_resources" / "tutorials" / "intro.md").write_text("# Intro")

    # Secrets living outside the docs root
    (tmp_path / "secret_notes.md").write_text(SECRET)
    (tmp_path / "private").mkdir()
    (tmp_path / "private" / "notes.md").write_text(SECRET)

    # A sibling directory sharing a name prefix with a valid version
    (docs / "12.x-backup").mkdir()
    (docs / "12.x-backup" / "leak.md").write_text(SECRET)

    return docs


def refused(call):
    """Run a tool function that must refuse; return the ToolFailure it raised."""
    with pytest.raises(ToolFailure) as raised:
        call()
    assert SECRET not in str(raised.value.payload())
    return raised.value


class TestVersionArgumentTraversal:
    """The `version` argument is joined onto docs_path and must be allowlisted.

    Every tool that takes one is listed here. A tool added later that takes a
    version belongs in this list."""

    VERSION_TAKING = {
        "read_content": lambda docs, v: read_content(docs, "secret_notes", version=v),
        "read_section": lambda docs, v: read_section(docs, "secret_notes", "intro", version=v),
        "outline": lambda docs, v: read_content(docs, "secret_notes", version=v, mode="outline"),
        "browse": lambda docs, v: browse_docs(docs, category="frontend", version=v),
        "search": lambda docs, v: search(docs, None, "TOPSECRET", version=v, sources=["core"]),
        "info": lambda docs, v: docs_info(docs, version=v),
        "compare_from": lambda docs, v: compare_versions(docs, v, "12.x"),
        "compare_to": lambda docs, v: compare_versions(docs, "12.x", v),
    }

    @pytest.mark.parametrize("tool", sorted(VERSION_TAKING))
    @pytest.mark.parametrize("bad_version", BAD_VERSIONS)
    def test_a_traversal_version_is_refused(self, docs_tree, tool, bad_version):
        failure = refused(lambda: self.VERSION_TAKING[tool](docs_tree, bad_version))

        assert failure.code == "unknown_version"

    def test_legitimate_version_still_works(self, docs_tree):
        assert "Templating docs." in read_content(docs_tree, "blade.md", version="12.x").text


class TestFilenameTraversal:
    """Traversal via the filename argument stays blocked."""

    @pytest.mark.parametrize("read", [
        lambda docs, name: read_content(docs, name, version="12.x"),
        lambda docs, name: read_content(docs, name, version="12.x", mode="outline"),
        lambda docs, name: read_section(docs, name, "intro", version="12.x"),
    ])
    def test_filename_traversal_denied(self, docs_tree, read):
        assert refused(lambda: read(docs_tree, "../../secret_notes")).code == "access_denied"

    def test_sibling_directory_prefix_not_treated_as_inside(self, docs_tree):
        """A string-prefix check would wrongly accept '12.x-backup' under '12.x'."""
        failure = refused(lambda: read_content(docs_tree, "../12.x-backup/leak", version="12.x"))

        assert failure.code == "access_denied"

    def test_a_corpus_prefix_cannot_climb_out_of_its_family(self, docs_tree):
        failure = refused(lambda: read_content(docs_tree, "tutorials/../../../private/notes"))

        assert failure.code in ("access_denied", "not_found")


class TestCollectionNames:
    """`name` in list_laravel_docs names a directory and must not escape it."""

    @pytest.mark.parametrize("bad", ["../../private", "..", "/etc", "tutorials/..", ""])
    def test_listing_refuses_a_traversal_name(self, docs_tree, bad):
        failure = refused(lambda: list_docs(docs_tree, name=bad) if bad else list_docs(docs_tree, name="."))

        assert failure.code in ("invalid_argument", "not_found")
        assert "notes.md" not in str(failure.payload())

    def test_search_refuses_an_unknown_source(self, docs_tree):
        failure = refused(lambda: search(docs_tree, None, "TOPSECRET", sources=["../../private"]))

        assert failure.code == "invalid_argument"

    def test_legitimate_collection_still_lists(self, docs_tree):
        listing = list_docs(docs_tree, name="tutorials")

        assert listing["collections"][0]["files"] == ["tutorials/intro.md"]


class TestIsSafePath:
    def test_rejects_traversal(self, tmp_path):
        base = tmp_path / "docs" / "12.x"
        base.mkdir(parents=True)
        assert is_safe_path(base, base / ".." / ".." / "secret.md") is False

    def test_rejects_sibling_prefix_directory(self, tmp_path):
        base = tmp_path / "docs" / "12.x"
        base.mkdir(parents=True)
        sibling = tmp_path / "docs" / "12.x-backup" / "leak.md"
        assert is_safe_path(base, sibling) is False

    def test_accepts_contained_path(self, tmp_path):
        base = tmp_path / "docs" / "12.x"
        base.mkdir(parents=True)
        assert is_safe_path(base, base / "blade.md") is True

    def test_fails_closed_on_error(self):
        """Any resolution error denies access rather than raising."""
        assert is_safe_path(None, None) is False


class TestValidators:
    def test_a_supported_version_is_accepted(self):
        from laravel_mcp_companion.mcp_tools import SUPPORTED_VERSIONS
        require_version(SUPPORTED_VERSIONS[0])

    def test_no_version_is_accepted(self):
        require_version(None)

    @pytest.mark.parametrize("bad", ["..", "/etc", "99.x", "12.x/..", "'; DROP TABLE"])
    def test_anything_else_is_refused_with_the_supported_list(self, bad):
        with pytest.raises(ToolFailure) as raised:
            require_version(bad)

        assert raised.value.code == "unknown_version"
        assert raised.value.details["supported_versions"]


class TestSectionNameSanitization:
    """Section names are parsed from remote HTML and become file paths."""

    @pytest.mark.parametrize("bad", [
        "../../../../etc/passwd",
        "/absolute/path",
        "..",
        "a/../../b",
        "back\\slash",
        "nul\x00byte",
        "",
        # Dot components: `base / "."` collapses to `base` itself
        ".",
        "./x",
        "a/./b",
        "a//b",
    ])
    def test_rejects_unsafe_section_names(self, bad):
        assert is_safe_section_name(bad) is False

    @pytest.mark.parametrize("good", ["eloquent", "getting-started", "api/reference", "v2.0_notes"])
    def test_accepts_safe_section_names(self, good):
        assert is_safe_section_name(good) is True

    def test_is_within_directory(self, tmp_path):
        base = tmp_path / "external" / "forge"
        base.mkdir(parents=True)
        assert is_within_directory(base, base / "intro.md") is True
        assert is_within_directory(base, base / ".." / ".." / "evil.md") is False


class TestDocsUpdaterVersionValidation:
    """DocsUpdater creates directories from `version` before any network call."""

    @pytest.mark.parametrize("bad", ["../../pwned", "/tmp/pwned_abs", "..", "a/b", ".", "./"])
    def test_rejects_traversal_version(self, tmp_path, bad):
        with pytest.raises(ValueError, match="Invalid Laravel version|escapes target"):
            DocsUpdater(tmp_path / "docs", bad)

    def test_dot_version_cannot_target_the_docs_root(self, tmp_path):
        """`docs_root / "."` collapses to docs_root, whose contents update() clears."""
        docs = tmp_path / "docs"
        (docs / "12.x").mkdir(parents=True)
        (docs / "12.x" / "blade.md").write_text("important")

        with pytest.raises(ValueError):
            DocsUpdater(docs, ".")

        # Every existing version must survive the rejected call
        assert (docs / "12.x" / "blade.md").exists()

    def test_version_dir_must_be_strict_subdirectory(self, tmp_path):
        """A version resolving to the docs root itself is rejected."""
        docs = tmp_path / "docs"
        docs.mkdir(parents=True)
        updater = DocsUpdater(docs, "12.x")
        assert updater.version_dir.resolve() != docs.resolve()

    def test_creates_no_directories_when_rejected(self, tmp_path):
        target = tmp_path / "docs"
        with pytest.raises(ValueError):
            DocsUpdater(target, "../../pwned")
        assert not (tmp_path.parent / "pwned").exists()
        assert not (tmp_path / "pwned").exists()

    def test_accepts_valid_version(self, tmp_path):
        updater = DocsUpdater(tmp_path / "docs", "12.x")
        assert updater.version_dir == tmp_path / "docs" / "12.x"
        assert updater.version_dir.is_dir()


class TestAllowlistArgumentParsing:
    """CLI allowlists must replace the environment, not union with it.

    argparse's "append" action appends to the default, so a non-empty default
    would leave stale env entries trusted alongside the explicit CLI values.
    """

    def _parse(self, monkeypatch, argv, env):
        import sys
        from laravel_mcp_companion.server import parse_arguments

        for var in ("CORS_ORIGINS", "ALLOWED_HOSTS"):
            monkeypatch.delenv(var, raising=False)
        for key, value in env.items():
            monkeypatch.setenv(key, value)
        monkeypatch.setattr(sys, "argv", ["prog"] + argv)
        return parse_arguments()

    def test_cli_origin_replaces_env(self, monkeypatch):
        args = self._parse(
            monkeypatch,
            ["--cors-origin", "https://cli.example"],
            {"CORS_ORIGINS": "https://env.example"},
        )
        assert args.cors_origin == ["https://cli.example"]

    def test_cli_allowed_host_replaces_env(self, monkeypatch):
        args = self._parse(
            monkeypatch,
            ["--allowed-host", "cli.example"],
            {"ALLOWED_HOSTS": "env.example"},
        )
        assert args.allowed_host == ["cli.example"]

    def test_env_used_when_flag_absent(self, monkeypatch):
        args = self._parse(monkeypatch, [], {"CORS_ORIGINS": "https://env.example,https://two.example"})
        assert args.cors_origin == ["https://env.example", "https://two.example"]

    def test_repeated_flags_accumulate(self, monkeypatch):
        args = self._parse(
            monkeypatch,
            ["--cors-origin", "https://a.example", "--cors-origin", "https://b.example"],
            {},
        )
        assert args.cors_origin == ["https://a.example", "https://b.example"]

    def test_defaults_are_empty(self, monkeypatch):
        args = self._parse(monkeypatch, [], {})
        assert args.cors_origin == []
        assert args.allowed_host == []


class TestDocsInfoTraversal:
    """`laravel_docs_info` is implemented inline rather than via an *_impl.

    That is how it escaped the validation added to every other version-taking
    tool: it read `<docs>/<version>/.metadata/sync_info.json` with `version`
    unchecked, giving an arbitrary-directory read and existence oracle that was
    reachable through the default search transform's call_tool proxy.
    """

    @pytest.mark.parametrize("bad_version", [
        "../secretzone", "../secretzone/", "./../secretzone",
        "12.x/../../secretzone", "12.x/./../../secretzone", "..", "/etc",
    ])
    @pytest.mark.asyncio
    async def test_rejects_traversal_version(self, tmp_path, bad_version):
        import json
        from fastmcp import Client
        from laravel_mcp_companion.server import create_mcp_server

        docs = tmp_path / "docs"
        (docs / "12.x" / ".metadata").mkdir(parents=True)
        (docs / "12.x" / "blade.md").write_text("# Blade")
        (docs / "12.x" / ".metadata" / "sync_info.json").write_text(
            json.dumps({"version": "12.x", "sync_time": "2026-07-30T00:00:00Z"})
        )

        # A metadata file planted outside the documentation tree
        outside = tmp_path / "secretzone" / ".metadata"
        outside.mkdir(parents=True)
        (outside / "sync_info.json").write_text(json.dumps({
            "version": "x", "sync_time": "2026-07-01T00:00:00Z",
            "commit_sha": "PROXY-CANARY", "commit_message": "PROXY-CANARY",
        }))

        server = create_mcp_server("T", docs, "12.x", transform_mode=None)
        async with Client(server) as client:
            result = await client.call_tool("laravel_docs_info", {"version": bad_version}, raise_on_error=False)
            text = result.content[0].text if result.content else ""

        assert "PROXY-CANARY" not in text, f"leaked via version={bad_version!r}"
        assert result.is_error
        assert result.structured_content["error"]["code"] == "unknown_version"

    @pytest.mark.asyncio
    async def test_legitimate_version_still_works(self, tmp_path):
        import json
        from fastmcp import Client
        from laravel_mcp_companion.server import create_mcp_server
        from laravel_mcp_companion.mcp_tools import SUPPORTED_VERSIONS

        version = SUPPORTED_VERSIONS[-1]
        docs = tmp_path / "docs"
        (docs / version / ".metadata").mkdir(parents=True)
        (docs / version / ".metadata" / "sync_info.json").write_text(
            json.dumps({"version": version, "sync_time": "2026-07-30T00:00:00Z",
                        "commit_sha": "abc1234"})
        )

        server = create_mcp_server("T", docs, version, transform_mode=None)
        async with Client(server) as client:
            result = await client.call_tool("laravel_docs_info", {"version": version})
            text = result.content[0].text if result.content else ""

        assert "abc1234" in text


class TestVersionsCacheIsTrustworthy:
    """SUPPORTED_VERSIONS is the trust root for every version allowlist.

    It is read from a JSON file that ships in the image, is tracked in git, and
    lives in a directory users bind-mount. The GitHub API response was filtered
    to `\\d+\\.x`; the cache read was not, so one edited value disabled every check.
    """

    @pytest.mark.parametrize("poisoned", [
        "../secretzone", "..", ".", "/etc", "12.x/../..", "", 42, None, {"a": 1},
    ])
    def test_malformed_cache_entries_are_discarded(self, tmp_path, poisoned):
        import json
        from laravel_mcp_companion.docs_updater import get_supported_versions

        cache = tmp_path / "versions.json"
        cache.write_text(json.dumps({
            "versions": ["12.x", poisoned],
            "updated_at": "2099-01-01T00:00:00+00:00",
        }))

        versions = get_supported_versions(cache_file=cache)
        assert poisoned not in versions
        assert versions == ["12.x"]

    def test_cache_of_only_bad_entries_falls_through(self, tmp_path):
        """A wholly malformed cache must not become the allowlist."""
        import json
        from laravel_mcp_companion.docs_updater import get_supported_versions

        cache = tmp_path / "versions.json"
        cache.write_text(json.dumps({
            "versions": ["../etc", "."],
            "updated_at": "2099-01-01T00:00:00+00:00",
        }))

        versions = get_supported_versions(cache_file=cache)
        assert "../etc" not in versions and "." not in versions


class TestSymlinkedVersionDirectory:
    """Relocating a version directory via symlink is legitimate, not an attack."""

    def test_symlinked_version_dir_is_accepted(self, tmp_path):
        import os
        from laravel_mcp_companion.docs_updater import DocsUpdater

        docs = tmp_path / "docs"
        docs.mkdir()
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        os.symlink(elsewhere, docs / "12.x")

        updater = DocsUpdater(docs, "12.x")
        assert updater.version_dir == docs / "12.x"

    def test_server_starts_with_symlinked_version_dir(self, tmp_path):
        """This previously aborted startup, not merely the update path."""
        import os
        from laravel_mcp_companion.server import create_mcp_server

        docs = tmp_path / "docs"
        docs.mkdir()
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        (elsewhere / "blade.md").write_text("# Blade")
        os.symlink(elsewhere, docs / "12.x")

        assert create_mcp_server("T", docs, "12.x", transform_mode=None) is not None
