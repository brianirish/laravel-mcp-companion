import path_security
import mcp_tools
import docs_updater


def test_single_containment_primitive():
    """Every module's containment check is literally the same function."""
    assert mcp_tools.resolve_contained_path is path_security.resolve_contained_path
    assert mcp_tools.is_safe_path is path_security.is_safe_path
    assert docs_updater.is_within_directory is path_security.is_within_directory


def test_containment_rejects_prefix_sibling(tmp_path):
    base = tmp_path / "docs" / "12.x"
    base.mkdir(parents=True)
    sibling = tmp_path / "docs" / "12.x-backup" / "secret.md"
    sibling.parent.mkdir()
    sibling.write_text("secret")
    assert path_security.resolve_contained_path(base, sibling) is None
    assert path_security.is_within_directory(base, sibling) is False


def test_containment_accepts_inside(tmp_path):
    base = tmp_path / "docs"
    inside = base / "12.x" / "blade.md"
    inside.parent.mkdir(parents=True)
    inside.write_text("x")
    assert path_security.resolve_contained_path(base, inside) == inside.resolve()


def test_no_follow_opener_refuses_symlink(tmp_path):
    target = tmp_path / "real.md"
    target.write_text("content")
    link = tmp_path / "link.md"
    link.symlink_to(target)
    import pytest
    with pytest.raises(OSError):
        open(link, "r", opener=path_security.no_follow_opener)
