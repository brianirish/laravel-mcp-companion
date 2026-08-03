# Health and Metrics Endpoints Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `/healthz` (public JSON liveness/readiness) and `/metrics` (Prometheus text, auth-following) on the HTTP transport, fed by a FastMCP middleware that counts and times every tool call.

**Architecture:** New leaf module `metrics.py` (registry + renderer + middleware, no project imports except stdlib) wired in `create_mcp_server` alongside the existing `.well-known` custom route. Spec: `docs/superpowers/specs/2026-08-03-health-metrics-endpoints-design.md` — metric names, buckets, health semantics, and auth policy are fixed there.

**Tech Stack:** FastMCP middleware hooks (`on_call_tool` sees `context.message.name`; `on_request` sees `context.method`), `mcp.custom_route`, `TokenVerifier.verify_token(token) -> AccessToken|None` (async), `FastMCP(middleware=[...])`.

## Global Constraints

- No new dependencies. Coverage gate stays ≥80. Commit per task; weekday-daytime commits via `git lc`.
- Registry is a module singleton with `reset()`; tests must call `reset()` (autouse fixture in the new test modules, NOT in the global conftest).
- Buckets: `(0.005, 0.025, 0.1, 0.5, 1, 5, 30, inf)`. Status codes: ok/degraded=200, unhealthy=503.

---

### Task 1: `metrics.py` — registry, renderer, middleware

**Files:** Create `metrics.py`, `tests/unit/test_metrics.py`.

**Interfaces — Produces:**
- `registry: MetricsRegistry` singleton; `MetricsRegistry.reset()`; `record_tool_call(tool: str, seconds: float, ok: bool)`; `record_request(method: str)`; `set_gauge_callable(name: str, fn: Callable[[], float | None])` (a callable returning None omits the gauge from output); `set_info(version: str)`.
- `render_prometheus(registry) -> str` — deterministic: sorted label values, `# TYPE` lines, histogram `_bucket`/`_sum`/`_count` series.
- `MetricsMiddleware(Middleware)` — times `on_call_tool` with `time.perf_counter()`, records `(name, ok)` on success and `(name, error)` on exception before re-raising; `on_request` records `context.method`.

- [ ] **Step 1: failing tests** — counters accumulate and label by (tool,status); histogram buckets edge values correctly (a 0.5s observation lands in the 0.5 bucket, cumulative buckets are monotonic, `_count`/`_sum` consistent); renderer golden test against a small fixed registry state; gauge callables evaluated at render time and omitted when returning None; `reset()` empties everything; middleware records ok, error (exception re-raised to caller), and request methods through an in-memory `Client` on a throwaway `FastMCP` instance.
- [ ] **Step 2: run, verify failure** (module absent).
- [ ] **Step 3: implement** `metrics.py` (~150 lines: registry with one `threading.Lock`, plain dicts; renderer; middleware).
- [ ] **Step 4: tests pass.**
- [ ] **Step 5: commit** — "Add the metrics registry, renderer, and middleware"

### Task 2: wire endpoints into `create_mcp_server`

**Files:** Modify `laravel_mcp_companion.py` (imports, `create_mcp_server`); Create `tests/unit/test_health_metrics.py`.

**Interfaces — Consumes:** Task 1's registry/middleware; existing `get_documentation_date`, `copy_is_stale`, `SUPPORTED_VERSIONS`, `SERVER_VERSION`, `mcp.custom_route`, the `auth` parameter.

- [ ] **Step 1: failing tests** (in-process ASGI, `build_http_app`, patterns from `test_http_wiring.py` / `test_well_known.py`):
  - `/healthz` 200 with `status=ok`, `version=SERVER_VERSION`, `uptime_seconds > 0`, docs block populated (use `test_docs_dir`).
  - degraded: monkeypatch `laravel_mcp_companion.copy_is_stale` → True ⇒ 200, `status=degraded`, `docs.stale` true.
  - unhealthy: server built on an empty temp dir ⇒ 503, `status=unhealthy`.
  - `/healthz` stays 200 on an auth-enabled app with no token.
  - `/metrics` public without auth: 200, `text/plain` content type, contains `# TYPE laravel_mcp_tool_calls_total counter` and `laravel_mcp_info{version="..."} 1`.
  - `/metrics` on auth-enabled app: 401 + `WWW-Authenticate: Bearer` bare; 200 with the static token.
  - counters flow end to end: call `laravel_docs_info` through an in-memory `Client`, then `/metrics` shows `laravel_mcp_tool_calls_total{status="ok",tool="laravel_docs_info"} 1`.
  - autouse `reset()` fixture keeps tests order-independent.
- [ ] **Step 2: verify failures** (404s).
- [ ] **Step 3: implement** in `create_mcp_server`: capture `start_time = time.monotonic()`; `mcp.add_middleware(MetricsMiddleware())` (or constructor arg); `set_info(SERVER_VERSION)`; gauge callables for `uptime_seconds` and `docs_copy_age_days` (from `get_documentation_date(docs_path)` age, None when unknown); `/healthz` handler computing the JSON per spec (versions_available = count of readable version dirs among `SUPPORTED_VERSIONS`); `/metrics` handler: if `auth` provider given, parse `Authorization: Bearer` and `await auth.verify_token(token)`, 401 on missing/invalid, else render.
- [ ] **Step 4: new tests + full suite pass** (coverage ≥80 holds).
- [ ] **Step 5: commit** — "Serve /healthz and /metrics on the HTTP transport"

### Task 3: e2e + docs + verification

**Files:** Modify `tests/e2e/test_http.py`, `README.md`, `ROADMAP.md`, `CHANGELOG.md`.

- [ ] **Step 1: e2e test** — against the real HTTP server: `GET /healthz` is 200/ok; run one tool call through a real client; `GET /metrics` shows the counter and uptime gauge. One test, `@pytest.mark.e2e`, existing fixtures.
- [ ] **Step 2: docs** — README HTTP-security section gains a short "Operational endpoints" note (`/healthz` public by design, `/metrics` follows auth, Prometheus format); ROADMAP checks off "Health monitoring and metrics endpoints" under v0.13.0; CHANGELOG Unreleased Added entry.
- [ ] **Step 3: full verification** — `uv run pytest` (gate ≥80), `uv run pytest -m e2e --no-cov`, ruff, mypy.
- [ ] **Step 4: commit** — "Document and e2e-test the operational endpoints"

## Self-Review

- Spec coverage: module→T1, endpoints/auth/wiring→T2, e2e/docs→T3. Health semantics, buckets, names all pinned in the spec and restated in tests.
- Interfaces consistent: `record_tool_call/record_request/set_gauge_callable/set_info/reset/render_prometheus` used identically across tasks.
- Known risk: whether `mcp.custom_route` handlers can be registered before tools without ordering issues — `.well-known` already proves the pattern at the same spot.
