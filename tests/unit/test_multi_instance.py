"""Two servers in one process must not share configuration.

`create_mcp_server` used to stash `docs_path`/`version` in a module-level
`_server_config` dict. Creating a second server overwrote it, so the first
server's resource handler started serving the second server's docs -- the
two servers were never actually independent.
"""

from fastmcp import Client

from laravel_mcp_companion.server import create_mcp_server


def _make_docs(tmp_path, name, marker):
    docs = tmp_path / name
    (docs / "12.x").mkdir(parents=True)
    (docs / "12.x" / "blade.md").write_text(f"# Blade\n\n{marker}\n")
    return docs


async def test_two_servers_serve_their_own_docs(tmp_path):
    docs_a = _make_docs(tmp_path, "a", "MARKER-ALPHA")
    docs_b = _make_docs(tmp_path, "b", "MARKER-BETA")
    server_a = create_mcp_server("a", docs_a, "12.x", transform_mode=None)
    server_b = create_mcp_server("b", docs_b, "12.x", transform_mode=None)

    async with Client(server_a) as client_a:
        content_a = await client_a.read_resource("laravel://12.x/blade.md")
    async with Client(server_b) as client_b:
        content_b = await client_b.read_resource("laravel://12.x/blade.md")

    assert "MARKER-ALPHA" in content_a[0].text  # fails today: A serves B's docs
    assert "MARKER-BETA" in content_b[0].text
