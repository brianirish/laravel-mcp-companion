import laravel_mcp_companion
import mcp_tools


def test_one_file_cache_implementation():
    assert laravel_mcp_companion.get_file_content_cached is mcp_tools.get_file_content_cached


def test_one_version_parser():
    assert laravel_mcp_companion.get_version_from_path is mcp_tools.get_version_from_path


def test_one_metadata_reader():
    assert laravel_mcp_companion.get_laravel_docs_metadata is mcp_tools.get_laravel_docs_metadata


def test_cached_read_refuses_symlink_swap(tmp_path):
    """The TOCTOU regression: a symlink in the final component is refused."""
    secret = tmp_path / "outside.md"
    secret.write_text("SECRET")
    docs = tmp_path / "docs"
    docs.mkdir()
    link = docs / "blade.md"
    link.symlink_to(secret)
    content = laravel_mcp_companion.get_file_content_cached(str(link))
    assert "SECRET" not in content
