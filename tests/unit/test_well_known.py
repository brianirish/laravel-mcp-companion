"""Registry discovery endpoint: GET /.well-known/mcp/server.json (HTTP mode).

Serves the repo's server.json with the live SERVER_VERSION stamped in, so a
deployment is discoverable the way the registry documents for self-hosting.
stdio mode has nothing to serve and is untouched.
"""

import httpx
import pytest

import laravel_mcp_companion
from laravel_mcp_companion import create_mcp_server


@pytest.fixture
def http_app(test_docs_dir):
    server = create_mcp_server("TestServer", test_docs_dir, "12.x", transform_mode=None)
    return server.http_app()


async def test_well_known_serves_stamped_server_json(http_app):
    transport = httpx.ASGITransport(app=http_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://localhost") as client:
        res = await client.get("/.well-known/mcp/server.json")
        assert res.status_code == 200
        assert res.headers["content-type"].startswith("application/json")
        data = res.json()
        assert data["name"] == "io.github.brianirish/laravel-mcp-companion"
        assert data["version"] == laravel_mcp_companion.SERVER_VERSION
        assert data["packages"][0]["identifier"].endswith(
            f":v{laravel_mcp_companion.SERVER_VERSION}"
        )


async def test_well_known_is_readable_without_auth(test_docs_dir, monkeypatch):
    """Discovery metadata is public by design, even when the MCP endpoint isn't."""
    import argparse

    monkeypatch.setenv("AUTH_STATIC_TOKENS", "sekrit:client-a")
    args = argparse.Namespace(
        transport="http", auth_jwks_uri=None, auth_issuer=None,
        auth_audience=None, auth_required_scope=[],
    )
    provider = laravel_mcp_companion.build_auth_provider(args)
    server = create_mcp_server(
        "TestServer", test_docs_dir, "12.x", transform_mode=None, auth=provider
    )
    app = server.http_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://localhost") as client:
        res = await client.get("/.well-known/mcp/server.json")
        assert res.status_code == 200
