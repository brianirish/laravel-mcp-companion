"""Regression tests for path traversal and input validation.

Each test here corresponds to a vulnerability that was exploitable before the
security hardening pass. They assert that untrusted tool arguments cannot be
used to read, enumerate, or write outside the documentation tree.
"""

import pytest

from mcp_tools import (
    is_safe_path,
    validate_version,
    validate_subdirectory,
    read_laravel_doc_content_impl,
    get_doc_structure_impl,
    list_laravel_docs_impl,
    verify_laravel_feature_impl,
    browse_docs_by_category_impl,
    search_laravel_docs_with_context_impl,
    list_laravel_learning_resources_impl,
    search_laravel_learning_resources_impl,
)
from docs_updater import is_safe_section_name, is_within_directory, DocsUpdater

SECRET = "TOPSECRET-api-key-sk-live-1234"


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


class TestVersionArgumentTraversal:
    """The `version` argument is joined onto docs_path and must be allowlisted."""

    @pytest.mark.parametrize("bad_version", ["..", "../..", "/etc", "/", "12.x/../..", "\x00"])
    def test_read_doc_rejects_traversal_version(self, docs_tree, bad_version):
        result = read_laravel_doc_content_impl(docs_tree, "secret_notes", version=bad_version)
        assert SECRET not in result
        assert "Invalid version" in result

    def test_get_doc_structure_rejects_traversal_version(self, docs_tree):
        result = get_doc_structure_impl(docs_tree, "secret_notes", version="..")
        assert SECRET not in result
        assert "Invalid version" in result

    def test_list_docs_rejects_traversal_version(self, docs_tree):
        result = list_laravel_docs_impl(docs_tree, version="..")
        assert "secret_notes" not in result
        assert "Invalid version" in result

    def test_verify_feature_rejects_traversal_version(self, docs_tree):
        result = verify_laravel_feature_impl(docs_tree, "secret_notes", version="..")
        assert "secret_notes" not in result
        assert "Invalid version" in result

    def test_browse_category_rejects_traversal_version(self, docs_tree):
        result = browse_docs_by_category_impl(docs_tree, "frontend", version="..")
        assert SECRET not in result
        assert "Invalid version" in result

    def test_search_with_context_rejects_traversal_version(self, docs_tree):
        result = search_laravel_docs_with_context_impl(
            docs_tree, "TOPSECRET", version="..", include_external=False
        )
        assert SECRET not in result
        assert "Invalid version" in result

    def test_legitimate_version_still_works(self, docs_tree):
        result = read_laravel_doc_content_impl(docs_tree, "blade.md", version="12.x")
        assert "Templating docs." in result


class TestFilenameTraversal:
    """Traversal via the filename argument stays blocked."""

    def test_filename_traversal_denied(self, docs_tree):
        result = read_laravel_doc_content_impl(docs_tree, "../../secret_notes", version="12.x")
        assert SECRET not in result
        assert "Access denied" in result

    def test_sibling_directory_prefix_not_treated_as_inside(self, docs_tree):
        """A string-prefix check would wrongly accept '12.x-backup' under '12.x'."""
        result = read_laravel_doc_content_impl(docs_tree, "../12.x-backup/leak", version="12.x")
        assert SECRET not in result
        assert "Access denied" in result


class TestLearningResourceSources:
    """`source`/`sources` name a subdirectory and must not escape it."""

    def test_list_rejects_traversal_source(self, docs_tree):
        result = list_laravel_learning_resources_impl(docs_tree, source="../../private")
        assert "notes.md" not in result
        assert "not found" in result

    def test_search_rejects_traversal_source(self, docs_tree):
        result = search_laravel_learning_resources_impl(
            docs_tree, "TOPSECRET", sources=["../../private"]
        )
        assert "notes.md" not in result
        assert "Invalid sources" in result

    def test_legitimate_source_still_works(self, docs_tree):
        result = list_laravel_learning_resources_impl(docs_tree, source="tutorials")
        assert "intro.md" in result


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
    def test_validate_version_accepts_supported(self):
        from mcp_tools import SUPPORTED_VERSIONS
        assert validate_version(SUPPORTED_VERSIONS[0]) is None

    def test_validate_version_allows_none(self):
        assert validate_version(None) is None

    @pytest.mark.parametrize("bad", ["..", "/etc", "99.x", "12.x/..", "'; DROP TABLE"])
    def test_validate_version_rejects_bad(self, bad):
        result = validate_version(bad)
        assert result is not None
        assert "Invalid version" in result

    def test_validate_subdirectory(self, tmp_path):
        (tmp_path / "real").mkdir()
        assert validate_subdirectory(tmp_path, "real") is True
        assert validate_subdirectory(tmp_path, "..") is False
        assert validate_subdirectory(tmp_path, "../etc") is False
        assert validate_subdirectory(tmp_path, "/etc") is False
        assert validate_subdirectory(tmp_path, "") is False
        assert validate_subdirectory(tmp_path, "nonexistent") is False


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
        from laravel_mcp_companion import parse_arguments

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
