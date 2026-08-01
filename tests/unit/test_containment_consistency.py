"""Every path that touches a documentation file must agree on containment.

`read_laravel_doc_content` refuses a file that resolves outside its version
directory. The enumeration paths -- listing and searching -- did not check at
all, so the same symlinked file was denied on read while being listed and
match-counted. That disagreement is a content oracle over material the read
path explicitly refuses to serve.
"""

import os

import pytest

from mcp_tools import (
    SUPPORTED_VERSIONS,
    list_laravel_docs_impl,
    read_laravel_doc_content_impl,
    search_laravel_docs_impl,
)

# The term searched for. It is echoed back in "no results" messages, so it
# cannot double as the leak canary.
QUERY = "OUTSIDE-CANARY-content"
# Text that only ever appears inside the out-of-tree file. Its presence in any
# response means real content escaped, not just the query being echoed.
PAYLOAD = "SENSITIVE-PAYLOAD-4417"
VERSION = SUPPORTED_VERSIONS[-1]


@pytest.fixture
def docs_with_escaping_symlink(tmp_path):
    """A version directory containing a symlink that points outside the tree."""
    docs = tmp_path / "docs"
    version_dir = docs / VERSION
    version_dir.mkdir(parents=True)
    (version_dir / "blade.md").write_text("# Blade\n\nLegitimate content.")

    outside = tmp_path / "outside.md"
    outside.write_text(f"# Secret\n\n{QUERY} {PAYLOAD}")
    os.symlink(outside, version_dir / "routing.md")

    return docs


def test_read_refuses_the_escaping_symlink(docs_with_escaping_symlink):
    """Baseline: this is the behavior the other paths must match."""
    result = read_laravel_doc_content_impl(docs_with_escaping_symlink, "routing.md", VERSION)

    assert PAYLOAD not in result
    assert "Access denied" in result


def test_list_does_not_advertise_the_escaping_symlink(docs_with_escaping_symlink):
    result = list_laravel_docs_impl(docs_with_escaping_symlink, version=VERSION)

    assert "routing.md" not in result, "listed a file that read refuses to serve"
    assert "blade.md" in result, "legitimate files must still be listed"


def test_search_does_not_match_inside_the_escaping_symlink(docs_with_escaping_symlink):
    result = search_laravel_docs_impl(
        docs_with_escaping_symlink, QUERY, version=VERSION, include_external=False
    )

    assert "routing.md" not in result, "match-counted a file that read refuses to serve"


def test_search_snippets_do_not_leak_the_escaping_symlink(docs_with_escaping_symlink):
    """Search now returns content in snippets, so a leak here is a direct one."""
    result = search_laravel_docs_impl(
        docs_with_escaping_symlink, QUERY, version=VERSION, include_external=False
    )

    assert PAYLOAD not in result, "leaked content that read refuses to serve"
    assert "routing.md" not in result


def test_legitimate_search_still_works(docs_with_escaping_symlink):
    """The containment filter must not break ordinary searching."""
    result = search_laravel_docs_impl(
        docs_with_escaping_symlink, "Legitimate", version=VERSION, include_external=False
    )

    assert "blade.md" in result


class TestAllowedHostWildcard:
    """`ALLOWED_HOSTS=*` must not silently disable the Host guard.

    FastMCP matches allowed hosts with fnmatchcase, so a wildcard entry matches
    every Host header — turning off DNS-rebinding protection while the operator
    sees a configured allowlist. Wildcard CORS origins are already rejected;
    hosts were not.
    """

    def _parse(self, monkeypatch, argv, env):
        import sys
        from laravel_mcp_companion import parse_arguments

        for var in ("CORS_ORIGINS", "ALLOWED_HOSTS"):
            monkeypatch.delenv(var, raising=False)
        for key, value in env.items():
            monkeypatch.setenv(key, value)
        monkeypatch.setattr(sys, "argv", ["prog"] + argv)
        return parse_arguments()

    @pytest.mark.parametrize("wildcard", ["*", "*.example.com", "foo*"])
    def test_wildcard_host_is_rejected_from_cli(self, monkeypatch, wildcard):
        with pytest.raises(SystemExit):
            self._parse(monkeypatch, ["--allowed-host", wildcard], {})

    def test_wildcard_host_is_rejected_from_env(self, monkeypatch):
        """The env path must be checked too; argparse does not validate defaults."""
        with pytest.raises(SystemExit):
            self._parse(monkeypatch, [], {"ALLOWED_HOSTS": "good.example,*"})

    def test_literal_hosts_are_accepted(self, monkeypatch):
        args = self._parse(
            monkeypatch, ["--allowed-host", "mcp.internal.example"], {}
        )
        assert args.allowed_host == ["mcp.internal.example"]


class TestLearningResourceSymlinkConsistency:
    """Scoped and unscoped learning-resource access must give the same answer.

    `validate_subdirectory` resolves through symlinks, so a symlinked source was
    reported "not found" while simultaneously appearing in the available-sources
    list, and an unscoped search read it anyway. Whichever answer is right, all
    three paths have to give it.
    """

    @pytest.fixture
    def learning_with_symlinked_source(self, tmp_path):
        docs = tmp_path / "docs"
        learning = docs / "learning_resources"
        learning.mkdir(parents=True)

        # A real source, and one relocated elsewhere via symlink
        (learning / "tutorials").mkdir()
        (learning / "tutorials" / "intro.md").write_text("# Intro\n\nreal source")

        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        (elsewhere / "guide.md").write_text(f"# Guide\n\n{PAYLOAD}")
        os.symlink(elsewhere, learning / "bootcamp")

        return docs

    def test_listing_a_source_agrees_with_listing_all(self, learning_with_symlinked_source):
        from mcp_tools import list_laravel_learning_resources_impl

        all_sources = list_laravel_learning_resources_impl(learning_with_symlinked_source)
        scoped = list_laravel_learning_resources_impl(
            learning_with_symlinked_source, source="bootcamp"
        )

        advertised = "bootcamp" in all_sources
        readable = "not found" not in scoped

        assert advertised == readable, (
            "a source listed as available must be readable, and vice versa; "
            f"advertised={advertised} readable={readable}"
        )

    def test_search_agrees_with_listing(self, learning_with_symlinked_source):
        from mcp_tools import (
            list_laravel_learning_resources_impl,
            search_laravel_learning_resources_impl,
        )

        all_sources = list_laravel_learning_resources_impl(learning_with_symlinked_source)
        unscoped_search = search_laravel_learning_resources_impl(
            learning_with_symlinked_source, PAYLOAD
        )

        advertised = "bootcamp" in all_sources
        searched = "bootcamp" in unscoped_search

        assert advertised == searched, (
            "unscoped search must cover exactly the sources that are listed; "
            f"advertised={advertised} searched={searched}"
        )

    def test_real_sources_are_unaffected(self, learning_with_symlinked_source):
        from mcp_tools import list_laravel_learning_resources_impl

        result = list_laravel_learning_resources_impl(
            learning_with_symlinked_source, source="tutorials"
        )
        assert "intro.md" in result


class TestOpensThePathItValidated:
    """The containment check must hand back the path the caller then opens.

    `is_safe_path` resolved the target, threw the resolved value away, and the
    caller opened the original. Between those two steps a symlink can be
    swapped, so the path that was checked and the path that was opened are not
    guaranteed to be the same file. Resolving once and opening that result
    closes the window.
    """

    def test_read_opens_the_resolved_target_not_the_link(self, tmp_path):
        from unittest.mock import patch

        from mcp_tools import read_laravel_doc_content_impl

        docs = tmp_path / "docs"
        version_dir = docs / VERSION
        version_dir.mkdir(parents=True)
        (version_dir / "real.md").write_text("# Real\n\ncontent")
        os.symlink(version_dir / "real.md", version_dir / "alias.md")

        with patch("mcp_tools.get_file_content_cached", return_value="# Real") as reader:
            read_laravel_doc_content_impl(docs, "alias.md", VERSION)

        opened = os.path.basename(reader.call_args[0][0])
        assert opened == "real.md", (
            f"opened {opened!r}; must open the resolved path that was validated, "
            "not the link that was validated through"
        )

    def test_resolved_contained_path_returns_the_resolution(self, tmp_path):
        from mcp_tools import resolve_contained_path

        base = tmp_path / "base"
        base.mkdir()
        (base / "real.md").write_text("x")
        os.symlink(base / "real.md", base / "alias.md")

        resolved = resolve_contained_path(base, base / "alias.md")

        assert resolved is not None
        assert resolved.name == "real.md", "must return what the path resolves to"

    def test_resolved_contained_path_rejects_escapes(self, tmp_path):
        from mcp_tools import resolve_contained_path

        base = tmp_path / "base"
        base.mkdir()
        outside = tmp_path / "outside.md"
        outside.write_text("secret")
        os.symlink(outside, base / "escape.md")

        assert resolve_contained_path(base, base / "escape.md") is None
        assert resolve_contained_path(base, base / ".." / "outside.md") is None

    def test_resolved_contained_path_fails_closed(self):
        from mcp_tools import resolve_contained_path

        assert resolve_contained_path(None, None) is None


class TestReaderRefusesToFollowLinks:
    """Resolving before opening is necessary but not sufficient.

    A path that is a regular file when checked can be replaced by a symlink
    before it is opened, and the open follows it. Resolving first does not help
    -- a regular file resolves to itself. Only refusing to follow a link at open
    time closes that window, because the refusal is part of the open itself.
    """

    def test_reader_refuses_a_symlink(self, tmp_path):
        from mcp_tools import clear_caches, get_file_content_cached

        secret = tmp_path / "secret.md"
        secret.write_text("TOCTOU-CANARY-7712")
        link = tmp_path / "link.md"
        os.symlink(secret, link)

        clear_caches()
        content = get_file_content_cached(str(link))

        assert "TOCTOU-CANARY-7712" not in content, "followed a symlink at open time"

    def test_reader_still_reads_regular_files(self, tmp_path):
        from mcp_tools import clear_caches, get_file_content_cached

        regular = tmp_path / "regular.md"
        regular.write_text("# Regular\n\nordinary content")

        clear_caches()
        content = get_file_content_cached(str(regular))

        assert "ordinary content" in content
