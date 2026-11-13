"""Metrics collection and Prometheus exposition for Laravel MCP Companion.

A deliberately small, dependency-free implementation: the metric set is fixed
(see docs/superpowers/specs/2026-08-03-health-metrics-endpoints-design.md),
label values come from closed sets (registered tool names, MCP method names),
and rendering is deterministic so tests can golden-match it.

Counters reset with the process; that is the Prometheus model
(scrape-and-restart), not a bug.
"""

import threading
import time
from typing import Any, Callable, Dict, Optional, Tuple

from fastmcp.server.middleware import Middleware

# Latency buckets in seconds. One histogram overall rather than per tool:
# per-tool histograms would be ~26x the cardinality for little added signal;
# per-tool counters plus one duration distribution answer the real questions.
BUCKETS = (0.005, 0.025, 0.1, 0.5, 1.0, 5.0, 30.0)


class MetricsRegistry:
    """Thread-safe holder of the server's metrics."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._tool_calls: Dict[Tuple[str, str], int] = {}
        self._requests: Dict[str, int] = {}
        self._bucket_counts: list[int] = [0] * (len(BUCKETS) + 1)
        self._duration_sum = 0.0
        self._duration_count = 0
        self._gauges: Dict[str, Callable[[], Optional[float]]] = {}
        self._info_version: Optional[str] = None

    def record_tool_call(self, tool: str, seconds: float, ok: bool) -> None:
        status = "ok" if ok else "error"
        with self._lock:
            key = (tool, status)
            self._tool_calls[key] = self._tool_calls.get(key, 0) + 1
            for i, bound in enumerate(BUCKETS):
                if seconds <= bound:
                    self._bucket_counts[i] += 1
                    break
            else:
                self._bucket_counts[-1] += 1
            self._duration_sum += seconds
            self._duration_count += 1

    def record_request(self, method: str) -> None:
        with self._lock:
            self._requests[method] = self._requests.get(method, 0) + 1

    def set_gauge_callable(self, name: str, fn: Callable[[], Optional[float]]) -> None:
        """Register a gauge evaluated at scrape time; returning None omits it."""
        with self._lock:
            self._gauges[name] = fn

    def set_info(self, version: str) -> None:
        with self._lock:
            self._info_version = version

    def reset(self) -> None:
        with self._lock:
            self._tool_calls.clear()
            self._requests.clear()
            self._bucket_counts = [0] * (len(BUCKETS) + 1)
            self._duration_sum = 0.0
            self._duration_count = 0
            self._gauges.clear()
            self._info_version = None

    def snapshot(self) -> Dict[str, Any]:
        """A consistent copy of the counting state for rendering."""
        with self._lock:
            return {
                "tool_calls": dict(self._tool_calls),
                "requests": dict(self._requests),
                "buckets": list(self._bucket_counts),
                "duration_sum": self._duration_sum,
                "duration_count": self._duration_count,
                "gauges": dict(self._gauges),
                "info_version": self._info_version,
            }


def _fmt(value: float) -> str:
    """Render a number the Prometheus way: integers without a decimal point."""
    as_int = int(value)
    return str(as_int) if value == as_int and "e" not in repr(value) else repr(value)


def render_prometheus(reg: MetricsRegistry) -> str:
    """Exposition-format output with stable ordering."""
    snap = reg.snapshot()
    lines: list[str] = []

    lines.append("# TYPE laravel_mcp_tool_calls_total counter")
    for (tool, status), count in sorted(snap["tool_calls"].items()):
        lines.append(
            f'laravel_mcp_tool_calls_total{{status="{status}",tool="{tool}"}} {count}'
        )

    lines.append("# TYPE laravel_mcp_requests_total counter")
    for method, count in sorted(snap["requests"].items()):
        lines.append(f'laravel_mcp_requests_total{{method="{method}"}} {count}')

    lines.append("# TYPE laravel_mcp_tool_call_seconds histogram")
    cumulative = 0
    for bound, bucket_count in zip(BUCKETS, snap["buckets"]):
        cumulative += bucket_count
        lines.append(
            f'laravel_mcp_tool_call_seconds_bucket{{le="{_fmt(bound)}"}} {cumulative}'
        )
    cumulative += snap["buckets"][-1]
    lines.append(f'laravel_mcp_tool_call_seconds_bucket{{le="+Inf"}} {cumulative}')
    lines.append(f"laravel_mcp_tool_call_seconds_sum {round(snap['duration_sum'], 6)}")
    lines.append(f"laravel_mcp_tool_call_seconds_count {snap['duration_count']}")

    for name, fn in sorted(snap["gauges"].items()):
        try:
            value = fn()
        except Exception:
            value = None
        if value is not None:
            lines.append(f"# TYPE {name} gauge")
            lines.append(f"{name} {value}")

    if snap["info_version"] is not None:
        lines.append("# TYPE laravel_mcp_info gauge")
        lines.append(f'laravel_mcp_info{{version="{snap["info_version"]}"}} 1')

    return "\n".join(lines) + "\n"


# Module singleton: one process, one registry, mirroring the cache singletons
# in mcp_tools. Tests isolate through reset().
registry = MetricsRegistry()


class MetricsMiddleware(Middleware):
    """Counts and times every tool call at the protocol layer."""

    async def on_request(self, context, call_next):
        registry.record_request(context.method)
        return await call_next(context)

    async def on_call_tool(self, context, call_next):
        started = time.perf_counter()
        try:
            result = await call_next(context)
        except Exception:
            registry.record_tool_call(
                context.message.name, time.perf_counter() - started, ok=False
            )
            raise
        registry.record_tool_call(
            context.message.name, time.perf_counter() - started, ok=True
        )
        return result
