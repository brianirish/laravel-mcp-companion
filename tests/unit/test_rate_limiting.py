"""Rate limiting through the live server, plus degradation pins.

The throttle tests use a burst sized so the MCP handshake passes and the
budget runs out mid-conversation — the realistic failure shape.
"""

import argparse
import asyncio
from pathlib import Path

import pytest

from fastmcp import Client

import metrics
from laravel_mcp_companion import build_rate_limiter, create_mcp_server
from mcp_tools import search_laravel_docs_data


@pytest.fixture(autouse=True)
def fresh_registry():
    metrics.registry.reset()
    yield
    metrics.registry.reset()


def limiter(rps, burst):
    args = argparse.Namespace(transport="http", rate_limit=rps, rate_limit_burst=burst)
    return build_rate_limiter(args)


class TestThrottleAndRecover:
    async def test_budget_exhausts_and_refills(self, test_docs_dir):
        # burst 8: the handshake (~4 requests) passes, a couple of tool
        # calls succeed, then the bucket runs dry at 1 rps.
        server = create_mcp_server(
            "TestServer", test_docs_dir, "12.x", transform_mode=None,
            rate_limiter=limiter(1.0, 8),
        )
        async with Client(server) as client:
            saw_limit = False
            for _ in range(8):
                result = await client.call_tool(
                    "list_laravel_docs", {"version": "12.x"}, raise_on_error=False
                )
                if result.is_error:
                    assert "Rate limit" in result.content[0].text
                    saw_limit = True
                    break
            assert saw_limit, "budget never ran out despite burst 8 at 1 rps"

            # ~1.2s at 1 rps refills a token; the client recovers.
            await asyncio.sleep(1.2)
            recovered = await client.call_tool(
                "list_laravel_docs", {"version": "12.x"}, raise_on_error=False
            )
            assert not recovered.is_error

    async def test_no_limiter_means_no_throttling(self, test_docs_dir):
        server = create_mcp_server(
            "TestServer", test_docs_dir, "12.x", transform_mode=None
        )
        async with Client(server) as client:
            for _ in range(5):
                result = await client.call_tool(
                    "list_laravel_docs", {"version": "12.x"}, raise_on_error=False
                )
                assert not result.is_error

    async def test_throttled_requests_still_counted_in_metrics(self, test_docs_dir):
        """Registration order contract: metrics sits outside the limiter, so
        a throttled request is still visible in laravel_mcp_requests_total."""
        server = create_mcp_server(
            "TestServer", test_docs_dir, "12.x", transform_mode=None,
            rate_limiter=limiter(1.0, 6),
        )
        async with Client(server) as client:
            attempts = 0
            for _ in range(8):
                attempts += 1
                result = await client.call_tool(
                    "list_laravel_docs", {"version": "12.x"}, raise_on_error=False
                )
                if result.is_error:
                    break

        from metrics import render_prometheus
        out = render_prometheus(metrics.registry)
        assert f'laravel_mcp_requests_total{{method="tools/call"}} {attempts}' in out


class TestCorruptCorpusDegradation:
    def test_search_survives_hostile_bytes_in_the_corpus(self, temp_dir):
        version_dir = Path(temp_dir) / "12.x"
        version_dir.mkdir(parents=True)
        (version_dir / "broken.md").write_bytes(b"\xff\xfe\x00broken\x00bytes\xff")
        (version_dir / "routing.md").write_text(
            "# Routing\n\n## Basics\n\nRoutes are registered in web.php with "
            "plenty of surrounding words so scoring has something to rank.\n"
        )
        result = search_laravel_docs_data(temp_dir, "routing", "12.x")
        assert "error" not in result
        assert result["results"]
        assert result["results"][0]["file"] == "12.x/routing.md"
