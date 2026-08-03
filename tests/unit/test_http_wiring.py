"""build_http_app assembly (laravel_mcp_companion.py) and arg-parsing edges.

The HTTP branch of main() had ~zero coverage: the guard, CORS, auth, and
well-known plumbing were only proven individually. These tests exercise the
assembled app in-process — no sockets.
"""

import argparse

import httpx
import pytest

import laravel_mcp_companion
from laravel_mcp_companion import build_auth_provider, build_http_app, create_mcp_server, parse_arguments


def make_args(**overrides):
    defaults = {
        "transport": "http", "host": None, "port": None,
        "cors_origin": [], "allowed_host": [],
        "auth_jwks_uri": None, "auth_issuer": None, "auth_audience": None,
        "auth_required_scope": [],
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


@pytest.fixture
def mcp_server(test_docs_dir):
    return create_mcp_server("TestServer", test_docs_dir, "12.x", transform_mode=None)


def client_for(app, base="http://localhost"):
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=base, follow_redirects=True
    )


class TestBuildHttpApp:
    def test_defaults_are_loopback_8081(self, mcp_server):
        app, host, port = build_http_app(make_args(), mcp_server)
        assert (host, port) == ("127.0.0.1", 8081)

    def test_explicit_host_and_port_honored(self, mcp_server):
        _, host, port = build_http_app(make_args(host="0.0.0.0", port=9000), mcp_server)
        assert (host, port) == ("0.0.0.0", 9000)

    def test_wildcard_cors_exits(self, mcp_server):
        with pytest.raises(SystemExit):
            build_http_app(make_args(cors_origin=["*"]), mcp_server)

    async def test_no_cors_headers_without_origins(self, mcp_server):
        app, _, _ = build_http_app(make_args(), mcp_server)
        async with client_for(app) as client:
            res = await client.get("/.well-known/mcp/server.json")
            assert res.status_code == 200
            assert "access-control-allow-origin" not in res.headers

    async def test_unlisted_origin_is_rejected_outright(self, mcp_server):
        """With no configured origins, a browser-style request from any origin
        gets 403 from the origin guard — stronger than merely omitting CORS
        headers."""
        app, _, _ = build_http_app(make_args(), mcp_server)
        async with client_for(app) as client:
            res = await client.get("/.well-known/mcp/server.json",
                                   headers={"origin": "https://app.example"})
            assert res.status_code == 403

    async def test_configured_origin_gets_cors_without_credentials(self, mcp_server):
        app, _, _ = build_http_app(make_args(cors_origin=["https://app.example"]), mcp_server)
        async with client_for(app) as client:
            res = await client.options(
                "/.well-known/mcp/server.json",
                headers={
                    "origin": "https://app.example",
                    "access-control-request-method": "GET",
                },
            )
            assert res.headers.get("access-control-allow-origin") == "https://app.example"
            assert res.headers.get("access-control-allow-credentials") is None

    async def test_off_loopback_rejects_unknown_host_on_mcp_endpoint(self, mcp_server):
        """The Host guard protects the MCP endpoint; discovery routes are
        deliberately public and stay readable. Host is set via header (not
        base_url) so the redirect re-issue can't rewrite it."""
        app, _, _ = build_http_app(make_args(host="0.0.0.0"), mcp_server)
        async with client_for(app) as client:
            res = await client.post(
                "/mcp/",
                json={"jsonrpc": "2.0", "id": 1, "method": "ping"},
                headers={
                    "accept": "application/json, text/event-stream",
                    "host": "evil.example",
                },
                follow_redirects=False,
            )
            assert res.status_code == 421

    async def test_off_loopback_accepts_allowed_host(self, mcp_server):
        app, _, _ = build_http_app(
            make_args(host="0.0.0.0", allowed_host=["mcp.internal.example"]), mcp_server
        )
        async with client_for(app, base="http://mcp.internal.example") as client:
            res = await client.get("/.well-known/mcp/server.json")
            assert res.status_code == 200

    async def test_auth_and_well_known_coexist(self, test_docs_dir, monkeypatch):
        monkeypatch.setenv("AUTH_STATIC_TOKENS", "sekrit:client-a")
        provider = build_auth_provider(make_args())
        server = create_mcp_server(
            "TestServer", test_docs_dir, "12.x", transform_mode=None, auth=provider
        )
        app, _, _ = build_http_app(make_args(), server)
        async with client_for(app) as client:
            protected = await client.post(
                "/mcp/",
                json={"jsonrpc": "2.0", "id": 1, "method": "ping"},
                headers={"accept": "application/json, text/event-stream"},
            )
            assert protected.status_code == 401
            open_meta = await client.get("/.well-known/mcp/server.json")
            assert open_meta.status_code == 200


class TestParseArgumentEdges:
    def test_auth_scopes_env_csv_fallback(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["prog"])
        monkeypatch.setenv("AUTH_REQUIRED_SCOPES", "mcp:read, mcp:search")
        args = parse_arguments()
        assert args.auth_required_scope == ["mcp:read", "mcp:search"]

    def test_cli_scope_replaces_env(self, monkeypatch):
        monkeypatch.setenv("AUTH_REQUIRED_SCOPES", "mcp:read")
        monkeypatch.setattr("sys.argv", ["prog", "--auth-required-scope", "mcp:admin"])
        args = parse_arguments()
        assert args.auth_required_scope == ["mcp:admin"]

    def test_invalid_env_transform_mode_errors(self, monkeypatch):
        monkeypatch.setenv("TRANSFORM_MODE", "yolo")
        monkeypatch.setattr("sys.argv", ["prog"])
        with pytest.raises(SystemExit):
            parse_arguments()


class TestResourceHandlers:
    async def test_core_resource_read(self, mcp_server):
        from fastmcp import Client

        async with Client(mcp_server) as client:
            content = await client.read_resource("laravel://12.x/installation.md")
            assert "Installation" in content[0].text

    async def test_core_resource_traversal_yields_no_content(self, mcp_server):
        """URI normalization collapses the `..` before the handler runs, so
        the request degrades to a not-found inside 12.x — either way, no
        11.x file content crosses the version boundary."""
        from fastmcp import Client

        async with Client(mcp_server) as client:
            content = await client.read_resource("laravel://12.x/../11.x/installation.md")
            text = content[0].text
            assert "Access denied" in text or "not found" in text.lower()
            assert "# Installation" not in text

    async def test_missing_core_resource_reports_not_found(self, mcp_server):
        from fastmcp import Client

        async with Client(mcp_server) as client:
            content = await client.read_resource("laravel://12.x/no-such-file.md")
            assert "not found" in content[0].text.lower()

    async def test_external_resource_unknown_service(self, mcp_server):
        from fastmcp import Client

        async with Client(mcp_server) as client:
            content = await client.read_resource("laravel-external://nope/intro.md")
            assert "not found" in content[0].text.lower()
