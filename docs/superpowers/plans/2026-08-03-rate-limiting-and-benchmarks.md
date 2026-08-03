# Rate Limiting, Degradation Pins, and Benchmarks Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Opt-in token-bucket rate limiting on the MCP surface, tests pinning the existing degradation behavior, and a report-only benchmark suite against the real corpus.

**Architecture:** Spec: `docs/superpowers/specs/2026-08-03-rate-limiting-and-benchmarks-design.md`. `build_rate_limiter(args)` beside `build_auth_provider` in `laravel_mcp_companion.py`, wiring FastMCP's `RateLimitingMiddleware(max_requests_per_second, burst_capacity)` through a new `create_mcp_server(..., rate_limiter=None)` parameter, registered after `MetricsMiddleware`. Benchmarks live in `tests/bench/` behind a `bench` marker mirroring the e2e pattern.

**Tech Stack:** `fastmcp.server.middleware.rate_limiting.RateLimitingMiddleware`; existing flag/env mirroring pattern; in-memory `Client` + `time.perf_counter()` for benchmarks.

## Global Constraints

- Rate limiting off unless `--rate-limit`/`RATE_LIMIT_RPS` given. Burst default `max(10, ceil(2*rps))` — the MCP handshake counts against the bucket (probed). Bad values exit loudly; stdio warns and ignores.
- Benchmarks never assert timing. Coverage gate stays ≥80. Weekday-daytime commits via `git lc`.

---

### Task 1: `build_rate_limiter` + flags

**Files:** Modify `laravel_mcp_companion.py` (parse_arguments + new function); Create `tests/unit/test_rate_limit_config.py`.

**Interfaces — Produces:** flags `--rate-limit` (float, env `RATE_LIMIT_RPS`), `--rate-limit-burst` (int, env `RATE_LIMIT_BURST`); `build_rate_limiter(args) -> RateLimitingMiddleware | None`.

- [ ] **Step 1: failing tests** — unset → None; `rps=0`/negative → SystemExit; explicit burst honored; default burst arithmetic (`rps=2 → 10`, `rps=20 → 40`); `burst<1` → SystemExit; stdio with rps set → warn + None (caplog); env fallback parses floats; invalid env value → parser error.
- [ ] **Step 2: verify failure.** **Step 3: implement** (flags follow the auth-flag pattern; float parse; `math.ceil`). **Step 4: pass.** **Step 5: commit** — "Add opt-in rate limit configuration"

### Task 2: wiring + degradation pins

**Files:** Modify `laravel_mcp_companion.py` (`create_mcp_server(..., rate_limiter=None)` registering after MetricsMiddleware; `main()` passes `build_rate_limiter(args)`); Create `tests/unit/test_rate_limiting.py`; extend `tests/unit/test_retrieval_quality.py` or new test for corrupt-corpus pin.

- [ ] **Step 1: failing tests** (in-memory `Client`):
  - throttle-and-recover: server with `rps=1, burst=3` — initialize passes, first tool call ok, immediate second call errors with "Rate limit" text, then after `await asyncio.sleep(1.1)` a call succeeds again.
  - metrics ordering: after a throttled call, `laravel_mcp_requests_total{method="tools/call"}` counts it (registry reset fixture; if ordering proves inverted, swap registration order — the test defines the contract).
  - no limiter → no throttling (existing suites already cover implicitly; one explicit high-frequency loop of 5 calls all ok).
  - corrupt-corpus pin: version dir with a hostile-bytes file + healthy file — `search_laravel_docs_data` returns the healthy hit, no raise.
- [ ] **Step 2: verify failure.** **Step 3: implement.** **Step 4: full suite ≥80.** **Step 5: commit** — "Wire opt-in rate limiting and pin degradation behavior"

### Task 3: benchmark suite

**Files:** Modify `pytest.ini` (marker `bench`, addopts deselect `-m "not e2e and not bench"`); Create `tests/bench/__init__.py`, `tests/bench/test_latency.py`.

- [ ] **Step 1: implement** (no TDD cycle — the suite IS the test): module-scoped fixture building `create_mcp_server` over the repo's real `docs/` (resolve from repo root; `pytest.skip` if `docs/12.x` absent); 10 fixed queries (mix: "routing", "queue retry failed jobs", "eloquent relationships", "middleware", "validation rules", "cache tags", "broadcasting", "sanctum api tokens", "blade components", "queue:retry"); helpers `timed(coro) -> seconds`; benchmarks: cold search (first call, index build) recorded once; warm search ≥30 iterations round-robin over queries; `read_laravel_doc_section` on a hit from search; `laravel_docs_info`. Print table: operation, n, p50, p95, max, vs 100ms target. Assertions: search returns hits, section read non-error — never timing.
- [ ] **Step 2:** `uv run pytest -m bench --no-cov -s -q` prints the table; bare `uv run pytest -q` deselects bench AND e2e; e2e still runs via `-m e2e`.
- [ ] **Step 3: commit** — "Add report-only latency benchmarks against the real corpus"

### Task 4: docs + verification + PR

**Files:** `README.md` (options table rows + HTTP-section paragraph on global-bucket semantics), `ROADMAP.md` (check rate limiting + load testing + error recovery items, the last citing accumulated mechanisms), `CHANGELOG.md` (Unreleased Added).

- [ ] **Step 1: docs.** **Step 2:** full suite, e2e, bench, ruff, mypy. **Step 3: commit, push, PR.** Post-merge follow-up (separate, on main): informational Harness bench step after the e2e step.

## Self-Review

- Spec coverage: flags→T1, wiring/pins→T2, bench→T3, docs→T4, Harness step deferred post-merge (same constraint as e2e's).
- Interface consistency: `build_rate_limiter`, `rate_limiter=` kwarg, marker names match across tasks.
- Risk noted in T2: middleware registration order vs FastMCP semantics is asserted by test, not assumed.
