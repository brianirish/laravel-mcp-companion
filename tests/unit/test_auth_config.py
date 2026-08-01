"""OAuth 2.1 resource-server configuration (HTTP transport).

The server validates bearer tokens; it never issues them. Misconfiguration
must fail at startup, not at request time: an auth setup that half-works is
worse than none because it presents as protection.
"""

import argparse

import httpx
import pytest

from laravel_mcp_companion import build_auth_provider, create_mcp_server


def make_args(**overrides):
    defaults = {
        "transport": "http",
        "auth_jwks_uri": None,
        "auth_issuer": None,
        "auth_audience": None,
        "auth_required_scope": [],
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


class TestBuildAuthProvider:
    def test_no_auth_config_returns_none(self):
        assert build_auth_provider(make_args()) is None

    def test_jwks_requires_issuer_and_audience(self):
        with pytest.raises(SystemExit):
            build_auth_provider(make_args(auth_jwks_uri="https://as.example/jwks"))

    def test_jwks_with_issuer_but_no_audience_refused(self):
        with pytest.raises(SystemExit):
            build_auth_provider(make_args(
                auth_jwks_uri="https://as.example/jwks",
                auth_issuer="https://as.example",
            ))

    def test_jwt_verifier_built_when_fully_configured(self):
        from fastmcp.server.auth.providers.jwt import JWTVerifier

        provider = build_auth_provider(make_args(
            auth_jwks_uri="https://as.example/jwks",
            auth_issuer="https://as.example",
            auth_audience="laravel-mcp-companion",
            auth_required_scope=["mcp:read"],
        ))
        assert isinstance(provider, JWTVerifier)
        assert provider.required_scopes == ["mcp:read"]

    def test_static_tokens_build_a_static_verifier(self, monkeypatch):
        from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

        monkeypatch.setenv("AUTH_STATIC_TOKENS", "sekrit:client-a,other:client-b")
        provider = build_auth_provider(make_args())
        assert isinstance(provider, StaticTokenVerifier)

    def test_static_and_jwks_are_mutually_exclusive(self, monkeypatch):
        monkeypatch.setenv("AUTH_STATIC_TOKENS", "sekrit:client-a")
        with pytest.raises(SystemExit):
            build_auth_provider(make_args(
                auth_jwks_uri="https://as.example/jwks",
                auth_issuer="https://as.example",
                auth_audience="laravel-mcp-companion",
            ))

    def test_malformed_static_tokens_refused(self, monkeypatch):
        monkeypatch.setenv("AUTH_STATIC_TOKENS", "token-without-client-id")
        with pytest.raises(SystemExit):
            build_auth_provider(make_args())

    def test_auth_on_stdio_warns_and_is_ignored(self, monkeypatch, caplog):
        monkeypatch.setenv("AUTH_STATIC_TOKENS", "sekrit:client-a")
        provider = build_auth_provider(make_args(transport="stdio"))
        assert provider is None
        assert any("stdio" in r.message for r in caplog.records)


class TestHTTPAuthBehavior:
    @pytest.fixture
    def authed_app(self, test_docs_dir, monkeypatch):
        monkeypatch.setenv("AUTH_STATIC_TOKENS", "sekrit:client-a")
        provider = build_auth_provider(make_args())
        server = create_mcp_server(
            "TestServer", test_docs_dir, "12.x", transform_mode=None, auth=provider
        )
        return server.http_app()

    async def test_request_without_token_gets_401_with_www_authenticate(self, authed_app):
        transport = httpx.ASGITransport(app=authed_app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://localhost", follow_redirects=True
        ) as client:
            res = await client.post(
                "/mcp/",
                json={"jsonrpc": "2.0", "id": 1, "method": "ping"},
                headers={"accept": "application/json, text/event-stream"},
            )
            assert res.status_code == 401
            assert "www-authenticate" in {k.lower() for k in res.headers}

    async def test_request_with_valid_token_is_not_rejected(self, authed_app):
        transport = httpx.ASGITransport(app=authed_app)
        # ASGITransport does not run the lifespan; the MCP session manager
        # needs it, so enter it explicitly.
        async with authed_app.router.lifespan_context(authed_app):
            async with httpx.AsyncClient(
                transport=transport, base_url="http://localhost", follow_redirects=True
            ) as client:
                res = await client.post(
                    "/mcp/",
                    json={"jsonrpc": "2.0", "id": 1, "method": "ping"},
                    headers={
                        "accept": "application/json, text/event-stream",
                        "authorization": "Bearer sekrit",
                    },
                )
                assert res.status_code != 401
