# v0.13.0 sub-project 2 — Health and metrics endpoints: Design

Date: 2026-08-03
Status: Approved (interactive session)

## Problem

An HTTP deployment of this server is a black box: nothing answers "is it up
and should traffic go to it" for a load balancer, and nothing answers "what is
it doing" for an operator. The roadmap's Production Readiness milestone calls
for health monitoring and metrics endpoints; this spec delivers both for HTTP
mode. stdio deployments have no endpoint surface and are explicitly out of
scope — the process boundary is their health check.

## Decisions (made with the user)

- **Prometheus text format, hand-rolled.** The metric set is small enough to
  emit with a ~40-line formatter we own; no `prometheus-client` dependency.
  Health is a separate, tiny JSON endpoint.
- **`/healthz` always public; `/metrics` follows auth.** Load balancers can't
  do OAuth, so health always answers. Metrics reveal usage patterns, so when
  a bearer-token provider is configured, `/metrics` requires a valid token;
  unauthenticated deployments (loopback-bound by default) serve it openly.
- **Collection via FastMCP middleware** (`on_call_tool` / `on_request`), not
  per-tool wrapping: zero changes to the 26 tool closures, identical behavior
  under both transports. Counters simply have no exposure surface in stdio.

## Design

### 1. `metrics.py` — registry and renderer

New module owning all metrics state:

- `MetricsRegistry`: thread-safe (single lock) holder of
  - counters: `tool_calls_total` keyed by `(tool, status)` where status is
    `ok` or `error`; `requests_total` keyed by MCP method.
  - one latency histogram for tool calls overall, fixed buckets
    `(0.005, 0.025, 0.1, 0.5, 1, 5, 30, +Inf)` seconds — per-tool histograms
    would be 26× the cardinality for little value; per-tool counts plus one
    duration distribution answer the real questions.
  - scrape-time gauges supplied by callables registered at wiring time:
    `docs_copy_age_days`, `uptime_seconds`.
  - `laravel_mcp_info{version="..."}` constant gauge.
- `render_prometheus(registry) -> str`: deterministic exposition-format
  output (`# TYPE` lines, stable label ordering) so tests can golden-match.
- A module-level `registry` singleton plus `reset()` for tests, following the
  existing cache-singleton pattern in `mcp_tools.py`.

Metric names, fixed here: `laravel_mcp_tool_calls_total`,
`laravel_mcp_tool_call_seconds` (histogram), `laravel_mcp_requests_total`,
`laravel_mcp_docs_copy_age_days`, `laravel_mcp_uptime_seconds`,
`laravel_mcp_info`.

### 2. `MetricsMiddleware`

A `fastmcp.server.middleware.Middleware` subclass in `metrics.py`:

- `on_call_tool`: time the downstream call; record `(tool, ok|error)` and the
  duration. Errors still re-raise unchanged.
- `on_request`: count by MCP method name.
- Registered unconditionally in `create_mcp_server` — negligible overhead, and
  keeping collection always-on means the HTTP endpoints never lie about
  "since when".

### 3. `GET /healthz` — liveness + readiness, always public

Registered via `mcp.custom_route` next to the `.well-known` route. JSON:

```json
{
  "status": "ok" | "degraded" | "unhealthy",
  "version": "<SERVER_VERSION>",
  "uptime_seconds": 123.4,
  "docs": {
    "versions_available": 8,
    "documentation_current_to": "2026-08-01",
    "copy_age_days": 2,
    "stale": false
  }
}
```

- `ok` (HTTP 200): at least one version directory readable, copy not stale.
- `degraded` (HTTP 200): serving, but `copy_is_stale()` says the corpus is
  behind — the existing >30-day rule from v0.11.0, same message intent:
  traffic is fine, pull a newer image.
- `unhealthy` (HTTP 503): no documentation readable at all — the
  "don't route traffic here" signal.

Reuses `get_documentation_date` / `copy_is_stale` from `mcp_tools`; no new
staleness logic.

### 4. `GET /metrics` — Prometheus text, follows auth

Registered via `mcp.custom_route`. Custom routes bypass FastMCP's auth
middleware (established with `.well-known`), so this route enforces its own
check: when `create_mcp_server` received an auth provider, the handler
requires `Authorization: Bearer <token>` and validates it with that same
`TokenVerifier` (`verify_token`); missing/invalid → 401 with
`WWW-Authenticate: Bearer`. No provider → public. Response is
`text/plain; version=0.0.4` exposition format.

### 5. Wiring

`create_mcp_server` grows no new parameters: it already has `docs_path` (for
the gauge callables) and `auth` (for the metrics guard). Start time is
captured at server construction. The two routes and the middleware are
registered where the `.well-known` route is today.

## Testing

- Unit (`tests/unit/test_metrics.py`): registry counting/threading basics,
  histogram bucketing edges, renderer golden output, `reset()` isolation.
- Wiring (`tests/unit/test_http_wiring.py` additions or a sibling module):
  `/healthz` public with and without auth; degraded state via a stale-dated
  corpus; 503 via an empty docs dir; `/metrics` 401 without token and 200
  with, on an auth-enabled app; tool-call counters visible in `/metrics`
  after in-process client calls; middleware records errors as `error`.
- e2e (`tests/e2e/test_http.py` addition): one test hitting `/healthz` and
  `/metrics` on the real server and asserting a counter incremented by the
  session's own initialize/tool calls.
- Coverage gate stays at 80; `metrics.py` should land near-fully covered.

## Out of scope (YAGNI)

Rate limiting (sub-project 3), per-version scrape gauges beyond copy age,
push gateways, OpenMetrics exemplars, stdio-mode metrics exposure, and
persistence of counters across restarts (scrape-and-restart is the Prometheus
model; counters reset with the process by design).

## Risks

- Middleware overhead on every tool call: one lock acquisition and a clock
  read — noise against tool bodies that do file I/O and BM25 scoring.
- Cardinality: tool names are a closed set (the registered surface), method
  names likewise; no user-supplied label values, so no cardinality explosion.
- The metrics auth check duplicates a small amount of bearer parsing; it uses
  the provider's own `verify_token`, so token semantics cannot drift from the
  MCP endpoint's.
