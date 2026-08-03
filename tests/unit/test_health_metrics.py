"""/healthz and /metrics wiring on the HTTP app.

Health is always public (load balancers can't do OAuth); metrics follow the
bearer-token provider when one is configured. Both are custom routes, which
bypass FastMCP's auth middleware, so /metrics enforces its own check via the
same TokenVerifier the MCP endpoint uses.
"""

import argparse

import httpx
import pytest

import laravel_mcp_companion
import metrics
from laravel_mcp_companion import build_auth_provider, build_http_app, create_mcp_server


@pytest.fixture(autouse=True)
def fresh_registry():
    metrics.registry.reset()
    yield
    metrics.registry.reset()


def make_args(**overrides):
    defaults = {
        "transport": "http", "host": None, "port": None,
        "cors_origin": [], "allowed_host": [],
        "auth_jwks_uri": None, "auth_issuer": None, "auth_audience": None,
        "auth_required_scope": [],
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def app_for(server):
    app, _, _ = build_http_app(make_args(), server)
    return app


def client_for(app):
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://localhost",
        follow_redirects=True,
    )


@pytest.fixture
def mcp_server(test_docs_dir):
    return create_mcp_server("TestServer", test_docs_dir, "12.x", transform_mode=None)


@pytest.fixture
def authed_server(test_docs_dir, monkeypatch):
    monkeypatch.setenv("AUTH_STATIC_TOKENS", "sekrit:client-a")
    provider = build_auth_provider(make_args())
    return create_mcp_server(
        "TestServer", test_docs_dir, "12.x", transform_mode=None, auth=provider
    )


class TestHealthz:
    async def test_healthy_corpus_reports_ok(self, mcp_server):
        async with client_for(app_for(mcp_server)) as client:
            res = await client.get("/healthz")
            assert res.status_code == 200
            data = res.json()
            assert data["status"] in ("ok", "degraded")  # staleness depends on fixture dates
            assert data["version"] == laravel_mcp_companion.SERVER_VERSION
            assert data["uptime_seconds"] > 0
            assert data["docs"]["versions_available"] >= 2
            assert isinstance(data["docs"]["stale"], bool)

    async def test_stale_corpus_reports_degraded_but_200(self, mcp_server, monkeypatch):
        monkeypatch.setattr(laravel_mcp_companion, "copy_is_stale", lambda p: True)
        async with client_for(app_for(mcp_server)) as client:
            res = await client.get("/healthz")
            assert res.status_code == 200
            data = res.json()
            assert data["status"] == "degraded"
            assert data["docs"]["stale"] is True

    async def test_empty_corpus_reports_unhealthy_503(self, temp_dir):
        server = create_mcp_server("TestServer", temp_dir, "12.x", transform_mode=None)
        async with client_for(app_for(server)) as client:
            res = await client.get("/healthz")
            assert res.status_code == 503
            data = res.json()
            assert data["status"] == "unhealthy"
            # numeric-or-null contract: monitors parse this as a number
            assert data["docs"]["copy_age_days"] is None

    async def test_copy_age_days_is_numeric_when_known(self, mcp_server):
        async with client_for(app_for(mcp_server)) as client:
            data = (await client.get("/healthz")).json()
            assert isinstance(data["docs"]["copy_age_days"], (int, float))

    async def test_healthz_public_even_with_auth(self, authed_server):
        async with client_for(app_for(authed_server)) as client:
            res = await client.get("/healthz")
            assert res.status_code == 200


class TestMetricsEndpoint:
    async def test_public_when_no_auth_configured(self, mcp_server):
        async with client_for(app_for(mcp_server)) as client:
            res = await client.get("/metrics")
            assert res.status_code == 200
            assert res.headers["content-type"].startswith("text/plain")
            assert "# TYPE laravel_mcp_tool_calls_total counter" in res.text
            version = laravel_mcp_companion.SERVER_VERSION
            assert f'laravel_mcp_info{{version="{version}"}} 1' in res.text
            assert "laravel_mcp_uptime_seconds" in res.text

    async def test_requires_token_when_auth_configured(self, authed_server):
        async with client_for(app_for(authed_server)) as client:
            bare = await client.get("/metrics")
            assert bare.status_code == 401
            assert bare.headers.get("www-authenticate", "").startswith("Bearer")

            wrong = await client.get(
                "/metrics", headers={"authorization": "Bearer nope"}
            )
            assert wrong.status_code == 401

            good = await client.get(
                "/metrics", headers={"authorization": "Bearer sekrit"}
            )
            assert good.status_code == 200
            assert "laravel_mcp_info" in good.text

    async def test_verifier_outage_fails_closed_not_500(self, test_docs_dir, monkeypatch):
        """A JWKS fetch failure raises out of JWTVerifier (network errors
        aren't in its catch list), and FastMCP's auth middleware eagerly
        verifies ANY request carrying an Authorization header — every route,
        custom ones included — so an unhandled raise is an app-wide 500.
        harden_verifier fails closed instead: token-bearing requests get 401
        during the outage, and the public routes keep answering."""
        monkeypatch.setenv("AUTH_STATIC_TOKENS", "sekrit:client-a")
        provider = build_auth_provider(make_args())

        async def explode(token):
            raise ValueError("JWKS failed to fetch")

        monkeypatch.setattr(provider, "verify_token", explode)
        laravel_mcp_companion.harden_verifier(provider)
        server = create_mcp_server(
            "TestServer", test_docs_dir, "12.x", transform_mode=None, auth=provider
        )
        async with client_for(app_for(server)) as client:
            res = await client.get("/metrics", headers={"authorization": "Bearer sekrit"})
            assert res.status_code == 401  # failed closed, not 500

            health = await client.get("/healthz")
            assert health.status_code == 200  # public routes unaffected

    async def test_tool_calls_flow_into_metrics(self, mcp_server):
        from fastmcp import Client

        async with Client(mcp_server) as mcp_client:
            await mcp_client.call_tool("laravel_docs_info", {"version": "12.x"})

        async with client_for(app_for(mcp_server)) as client:
            res = await client.get("/metrics")
            assert (
                'laravel_mcp_tool_calls_total{status="ok",tool="laravel_docs_info"} 1'
                in res.text
            )
            assert 'laravel_mcp_requests_total{method="tools/call"} 1' in res.text

    async def test_docs_age_gauge_present_for_dated_corpus(self, mcp_server):
        async with client_for(app_for(mcp_server)) as client:
            res = await client.get("/metrics")
            # fixture corpus carries commit dates, so the age gauge renders
            assert "laravel_mcp_docs_copy_age_days" in res.text
