"""End-to-end over streamable HTTP: real uvicorn, real port, real headers."""

import httpx
import pytest

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

import laravel_mcp_companion

pytestmark = [pytest.mark.e2e, pytest.mark.timeout(60)]


class TestHttpTransport:
    async def test_initialize_and_search_flow(self, http_server):
        base = http_server("--transform-mode", "none")
        async with Client(StreamableHttpTransport(f"{base}/mcp/")) as client:
            info = client.initialize_result.serverInfo
            assert info.version == laravel_mcp_companion.SERVER_VERSION

            search = await client.call_tool(
                "search_laravel_docs",
                {"query": "basic routing", "include_external": False},
            )
            assert search.structured_content.get("results")

    async def test_well_known_discovery(self, http_server):
        base = http_server()
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{base}/.well-known/mcp/server.json")
            assert res.status_code == 200
            data = res.json()
            assert data["name"] == "io.github.brianirish/laravel-mcp-companion"
            assert data["version"] == laravel_mcp_companion.SERVER_VERSION

    async def test_bad_host_header_rejected(self, http_server):
        base = http_server()
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{base}/mcp/",
                json={"jsonrpc": "2.0", "id": 1, "method": "ping"},
                headers={
                    "accept": "application/json, text/event-stream",
                    "host": "evil.example",
                },
            )
            assert res.status_code == 421

    async def test_auth_enforced_end_to_end(self, http_server):
        base = http_server(env_extra={"AUTH_STATIC_TOKENS": "e2e-token:e2e-client"})
        async with httpx.AsyncClient() as bare:
            res = await bare.post(
                f"{base}/mcp/",
                json={"jsonrpc": "2.0", "id": 1, "method": "ping"},
                headers={"accept": "application/json, text/event-stream"},
                follow_redirects=True,
            )
            assert res.status_code == 401
            assert "www-authenticate" in {k.lower() for k in res.headers}

        transport = StreamableHttpTransport(
            f"{base}/mcp/", headers={"authorization": "Bearer e2e-token"}
        )
        async with Client(transport) as client:
            tools = await client.list_tools()
            assert tools  # authenticated initialize + list works
