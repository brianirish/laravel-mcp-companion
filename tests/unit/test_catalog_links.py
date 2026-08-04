"""Every documentation_link in the package catalog must resolve.

19 of the 22 catalog links pointed at paths that never existed
(laravel://packages/cashier.md, laravel://authentication/sanctum.md). This
guard resolves each link through the server's real resource handlers — the
same path production URIs take — so a resolver change that breaks them
breaks here too.
"""

from pathlib import Path
from urllib.parse import urlparse

import pytest

from fastmcp import Client

from laravel_mcp_companion import PACKAGE_CATALOG, create_mcp_server

REPO_DOCS = Path(__file__).resolve().parents[2] / "docs"

LINKED = {
    pkg_id: info["documentation_link"]
    for pkg_id, info in PACKAGE_CATALOG.items()
    if info.get("documentation_link")
}

RESOURCE_SCHEMES = ("laravel://", "laravel-package://", "laravel-external://")

pytestmark = pytest.mark.skipif(
    not (REPO_DOCS / "12.x").is_dir(), reason="real corpus absent"
)


@pytest.fixture(scope="module")
def link_guard_server():
    # Server construction is cheap; a fresh in-memory Client per test avoids
    # sharing one across event loops, which deadlocks under function-scoped
    # asyncio.
    return create_mcp_server("LinkGuard", REPO_DOCS, "12.x", transform_mode=None)


@pytest.mark.parametrize("pkg_id", sorted(LINKED))
async def test_documentation_link_resolves(pkg_id, link_guard_server):
    link = LINKED[pkg_id]

    if link.startswith("https://"):
        # External sites can't be resolved offline; hold the shape instead:
        # a real scheme AND a real host ("https://" and "https:///x" fail).
        parsed = urlparse(link)
        assert parsed.scheme == "https" and parsed.netloc, f"{pkg_id}: malformed {link}"
        return

    assert link.startswith(RESOURCE_SCHEMES), f"{pkg_id}: unsupported scheme {link}"
    async with Client(link_guard_server) as client:
        content = (await client.read_resource(link))[0].text
    assert "not found" not in content.lower(), f"{pkg_id}: dead link {link}"
    assert "access denied" not in content.lower(), f"{pkg_id}: {link}"
    assert len(content) > 200, f"{pkg_id}: {link} resolved to a stub"


def test_most_packages_keep_documentation_links():
    """Deleting links is not a fix. The catalog held 22 linked entries when
    this guard landed; a drop means links were removed instead of repaired."""
    assert len(LINKED) >= 20, f"only {len(LINKED)} linked entries remain"
