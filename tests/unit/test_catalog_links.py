"""Every documentation_link in the package catalog must resolve.

All ~50 links pointed at paths that never existed (laravel://packages/
cashier.md, laravel://authentication/sanctum.md). This guard resolves each
through the real read implementations against the real corpus so they cannot
rot silently again.
"""

from pathlib import Path

import pytest

from laravel_mcp_companion import PACKAGE_CATALOG
from mcp_tools import read_laravel_doc_content_impl, resolve_contained_path

REPO_DOCS = Path(__file__).resolve().parents[2] / "docs"

LINKED = {
    pkg_id: info["documentation_link"]
    for pkg_id, info in PACKAGE_CATALOG.items()
    if info.get("documentation_link")
}

pytestmark = pytest.mark.skipif(
    not (REPO_DOCS / "12.x").is_dir(), reason="real corpus absent"
)


def resolve_link(link: str) -> str:
    if link.startswith("laravel://"):
        return read_laravel_doc_content_impl(
            REPO_DOCS, link[len("laravel://"):], runtime_version="12.x"
        )
    if link.startswith(("laravel-package://", "laravel-external://")):
        scheme, _, rest = link.partition("://")
        family = "packages" if scheme == "laravel-package" else "external"
        key, _, path = rest.partition("/")
        if not path.endswith(".md"):
            path = f"{path}.md"
        root = REPO_DOCS / family / key
        if not root.is_dir():
            return f"not found: no fetched corpus '{key}'"
        safe = resolve_contained_path(root, root / path)
        if safe is None or not safe.exists():
            return f"not found: {rest}"
        return safe.read_text(encoding="utf-8")
    if link.startswith("https://"):
        # External sites can't be resolved offline; the guard only holds the
        # shape. Prefer fetched docs where they exist.
        return "https-link " + "x" * 200
    return f"not found: unsupported scheme in {link}"


@pytest.mark.parametrize("pkg_id", sorted(LINKED))
def test_documentation_link_resolves(pkg_id):
    link = LINKED[pkg_id]
    content = resolve_link(link)
    assert "not found" not in content.lower(), f"{pkg_id}: dead link {link}"
    assert "access denied" not in content.lower()
    assert len(content) > 200, f"{pkg_id}: {link} resolved to a stub"


def test_most_packages_keep_documentation_links():
    """Deleting links is not a fix. The catalog held 22 linked entries when
    this guard landed (the README's "50+" was itself a false claim — see the
    claims audit); a drop means links were removed instead of repaired."""
    assert len(LINKED) >= 20, f"only {len(LINKED)} linked entries remain"
