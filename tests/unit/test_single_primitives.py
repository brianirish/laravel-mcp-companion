from laravel_mcp_companion import server as companion_server
from laravel_mcp_companion import mcp_tools
def test_one_file_cache_implementation():
    assert companion_server.get_file_content_cached is mcp_tools.get_file_content_cached


def test_one_version_parser():
    assert companion_server.get_version_from_path is mcp_tools.get_version_from_path


def test_cached_read_refuses_symlink_swap(tmp_path):
    """The TOCTOU regression: a symlink in the final component is refused."""
    secret = tmp_path / "outside.md"
    secret.write_text("SECRET")
    docs = tmp_path / "docs"
    docs.mkdir()
    link = docs / "blade.md"
    link.symlink_to(secret)
    content = companion_server.get_file_content_cached(str(link))
    assert "SECRET" not in content
