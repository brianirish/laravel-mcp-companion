"""metrics.py: registry counting, histogram bucketing, Prometheus rendering,
and the FastMCP middleware that feeds them."""

import pytest

from laravel_mcp_companion import metrics
from laravel_mcp_companion.metrics import MetricsMiddleware, MetricsRegistry, render_prometheus


@pytest.fixture(autouse=True)
def fresh_registry():
    metrics.registry.reset()
    yield
    metrics.registry.reset()


class TestRegistry:
    def test_tool_calls_count_by_tool_and_status(self):
        r = MetricsRegistry()
        r.record_tool_call("search_laravel_docs", 0.05, ok=True)
        r.record_tool_call("search_laravel_docs", 0.07, ok=True)
        r.record_tool_call("search_laravel_docs", 0.01, ok=False)
        out = render_prometheus(r)
        assert 'laravel_mcp_tool_calls_total{status="ok",tool="search_laravel_docs"} 2' in out
        assert 'laravel_mcp_tool_calls_total{status="error",tool="search_laravel_docs"} 1' in out

    def test_requests_count_by_method(self):
        r = MetricsRegistry()
        r.record_request("tools/call")
        r.record_request("tools/call")
        r.record_request("initialize")
        out = render_prometheus(r)
        assert 'laravel_mcp_requests_total{method="tools/call"} 2' in out
        assert 'laravel_mcp_requests_total{method="initialize"} 1' in out

    def test_histogram_buckets_are_cumulative_and_consistent(self):
        r = MetricsRegistry()
        r.record_tool_call("t", 0.004, ok=True)   # -> 0.005 bucket
        r.record_tool_call("t", 0.5, ok=True)     # boundary lands in le=0.5
        r.record_tool_call("t", 40.0, ok=True)    # only +Inf
        out = render_prometheus(r)
        assert 'laravel_mcp_tool_call_seconds_bucket{le="0.005"} 1' in out
        assert 'laravel_mcp_tool_call_seconds_bucket{le="0.5"} 2' in out
        assert 'laravel_mcp_tool_call_seconds_bucket{le="30"} 2' in out
        assert 'laravel_mcp_tool_call_seconds_bucket{le="+Inf"} 3' in out
        assert 'laravel_mcp_tool_call_seconds_count 3' in out
        assert "laravel_mcp_tool_call_seconds_sum 40.504" in out

    def test_gauge_callables_render_at_scrape_time(self):
        r = MetricsRegistry()
        value = {"v": 1.0}
        r.set_gauge_callable("laravel_mcp_uptime_seconds", lambda: value["v"])
        assert "laravel_mcp_uptime_seconds 1.0" in render_prometheus(r)
        value["v"] = 2.5
        assert "laravel_mcp_uptime_seconds 2.5" in render_prometheus(r)

    def test_none_gauge_is_omitted(self):
        r = MetricsRegistry()
        r.set_gauge_callable("laravel_mcp_docs_copy_age_days", lambda: None)
        assert "laravel_mcp_docs_copy_age_days" not in render_prometheus(r)

    def test_info_metric(self):
        r = MetricsRegistry()
        r.set_info("0.12.0")
        assert 'laravel_mcp_info{version="0.12.0"} 1' in render_prometheus(r)

    def test_type_lines_present(self):
        r = MetricsRegistry()
        r.record_tool_call("t", 0.1, ok=True)
        r.record_request("initialize")
        out = render_prometheus(r)
        assert "# TYPE laravel_mcp_tool_calls_total counter" in out
        assert "# TYPE laravel_mcp_requests_total counter" in out
        assert "# TYPE laravel_mcp_tool_call_seconds histogram" in out

    def test_reset_empties_everything(self):
        r = MetricsRegistry()
        r.record_tool_call("t", 0.1, ok=True)
        r.record_request("x")
        r.reset()
        out = render_prometheus(r)
        assert "tool_calls_total{" not in out
        assert "requests_total{" not in out

    def test_render_is_deterministic(self):
        r = MetricsRegistry()
        r.record_tool_call("b_tool", 0.1, ok=True)
        r.record_tool_call("a_tool", 0.1, ok=False)
        r.record_request("z")
        r.record_request("a")
        assert render_prometheus(r) == render_prometheus(r)
        # sorted label values: a_tool line appears before b_tool
        out = render_prometheus(r)
        assert out.index("a_tool") < out.index("b_tool")


class TestMiddleware:
    async def test_tool_calls_recorded_through_a_live_server(self):
        from fastmcp import Client, FastMCP

        server = FastMCP("t", middleware=[MetricsMiddleware()])

        @server.tool
        def works() -> str:
            return "ok"

        @server.tool
        def explodes() -> str:
            raise ValueError("boom")

        async with Client(server) as client:
            await client.call_tool("works", {})
            result = await client.call_tool("explodes", {}, raise_on_error=False)
            assert result.is_error

        out = render_prometheus(metrics.registry)
        assert 'laravel_mcp_tool_calls_total{status="ok",tool="works"} 1' in out
        assert 'laravel_mcp_tool_calls_total{status="error",tool="explodes"} 1' in out
        assert 'laravel_mcp_requests_total{method="tools/call"} 2' in out
        assert "laravel_mcp_tool_call_seconds_count 2" in out

    async def test_a_tool_that_does_not_exist_is_counted_under_one_label(self):
        """The name of a tool that does not exist is whatever the client sent.
        Counted under its own name, every invented name would stay in memory
        and in /metrics for the life of the process."""
        from fastmcp import Client, FastMCP

        server = FastMCP("t", middleware=[MetricsMiddleware()])

        async with Client(server) as client:
            for name in ("invented-1", "invented-2", 'x"} 1\nforged_metric{a="b'):
                result = await client.call_tool(name, {}, raise_on_error=False)
                assert result.is_error

        out = render_prometheus(metrics.registry)
        assert 'laravel_mcp_tool_calls_total{status="error",tool="unknown"} 3' in out
        assert "invented" not in out
        assert "forged_metric" not in out


class TestLabelEscaping:
    def test_a_label_value_cannot_end_its_own_line(self):
        reg = MetricsRegistry()
        reg.record_tool_call('a"b\\c\nd', 0.01, ok=True)

        out = render_prometheus(reg)

        assert 'tool="a\\"b\\\\c\\nd"' in out
        assert all(line.startswith(("#", "laravel_mcp_")) for line in out.splitlines())
