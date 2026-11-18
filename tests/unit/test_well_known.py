"""Registry discovery endpoint: GET /.well-known/mcp/server.json (HTTP mode).

Serves the repo's server.json with the live SERVER_VERSION stamped in, so a
deployment is discoverable the way the registry documents for self-hosting.
stdio mode has nothing to serve and is untouched.
"""

import httpx
import pytest

from laravel_mcp_companion import server as companion_server
from laravel_mcp_companion.server import create_mcp_server


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
        # Stamped from SERVER_VERSION. The form each field takes is checked
        # in the parametrized test at the end of this file.
        assert data["version"] == companion_server._semver(companion_server.SERVER_VERSION)
        assert data["packages"][0]["identifier"].endswith(f":v{data['version']}")


async def test_well_known_is_readable_without_auth(test_docs_dir, monkeypatch):
    """Discovery metadata is public by design, even when the MCP endpoint isn't."""
    import argparse

    monkeypatch.setenv("AUTH_STATIC_TOKENS", "sekrit:client-a")
    args = argparse.Namespace(
        transport="http", auth_jwks_uri=None, auth_issuer=None,
        auth_audience=None, auth_required_scope=[],
    )
    provider = companion_server.build_auth_provider(args)
    server = create_mcp_server(
        "TestServer", test_docs_dir, "12.x", transform_mode=None, auth=provider
    )
    app = server.http_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://localhost") as client:
        res = await client.get("/.well-known/mcp/server.json")
        assert res.status_code == 200


@pytest.mark.parametrize("version,registry,image_tag", [
    ("0.15.1", "0.15.1", "v0.15.1"),
    ("1.0.0", "1.0.0", "v1.0.0"),
    ("1.0.0rc1", "1.0.0-rc1", "v1.0.0-rc1"),
    ("1.0.0rc12", "1.0.0-rc12", "v1.0.0-rc12"),
])
def test_a_release_candidate_is_stamped_in_the_form_each_field_takes(
    monkeypatch, version, registry, image_tag
):
    """SERVER_VERSION is the PyPI form, 1.0.0rc1. The registry version is
    semver, 1.0.0-rc1, and the image is tagged with the git tag, v1.0.0-rc1."""
    monkeypatch.setattr(companion_server, "SERVER_VERSION", version)
    data = companion_server._registry_metadata()
    assert data["version"] == registry
    packages = {package["registryType"]: package for package in data["packages"]}
    assert packages["oci"]["identifier"] == f"ghcr.io/brianirish/laravel-mcp-companion:{image_tag}"
    assert packages["pypi"]["identifier"] == "laravel-mcp-companion"
    assert packages["pypi"]["version"] == version
