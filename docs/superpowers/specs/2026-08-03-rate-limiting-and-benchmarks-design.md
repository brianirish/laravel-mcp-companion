# v0.13.0 sub-project 3 — Rate limiting, degradation pins, benchmarks: Design

Date: 2026-08-03
Status: Approved (interactive session)

## Problem

Three Production Readiness items remain in this slot: rate limiting, "error
recovery and graceful degradation improvements", and load testing. Probing
found the middle one mostly *delivered but unpinned* — search survives a
corrupt corpus file, updates return partial results, discovery falls back to
manual sections, caches fail closed, token verification fails closed — so
this sub-project builds the first, pins the second, and adds the third as
report-only measurement.

## Decisions (made with the user)

- **Rate limiting is opt-in, off by default.** `--rate-limit RPS` (env:
  `RATE_LIMIT_RPS`); nothing changes for existing deployments. Default bind
  is loopback where limits only annoy; stdio is unaffected.
- **Benchmarks report, never gate.** Latency gates on shared CI runners are
  flake factories; the sub-100ms promise is v1.0.0's gate decision. The
  suite prints percentiles against the target and fails only on real
  breakage, not timing.

## Verified constraints (probed against FastMCP 3.4.5)

- `RateLimitingMiddleware(max_requests_per_second, burst_capacity, ...)`
  counts **every MCP request including the initialize handshake**: with a
  burst of 2, `initialize` + notifications drained the bucket before the
  first tool call. Burst must default generously.
- The default bucket is **global** — one budget for the whole server, not
  per client. That is the honest offering: without auth there is no reliable
  client identity to key on. Documented as a total-throughput cap.
- A limited request surfaces to clients as a clean MCP error
  ("Rate limit exceeded..."), not a connection failure.

## Design

### 1. Rate limiting

- Flags, mirroring the existing pattern (flag replaces env):
  `--rate-limit` (float RPS, env `RATE_LIMIT_RPS`) and `--rate-limit-burst`
  (int, env `RATE_LIMIT_BURST`, default `max(10, ceil(2 × rps))` so the
  handshake never self-throttles at low limits).
- `build_rate_limiter(args) -> RateLimitingMiddleware | None` beside
  `build_auth_provider`: None when unset; `rps <= 0` or `burst < 1` is a
  startup error (`sys.exit(1)`), matching the loud-config precedent; set on
  stdio → warn and ignore, exactly like auth.
- Wiring in `create_mcp_server(..., rate_limiter=None)`: registered **after**
  the metrics middleware so throttled requests still count in
  `laravel_mcp_requests_total` (verify effective order empirically in tests —
  outermost-first is assumed, not documented upstream).
- README: options table rows plus a paragraph in the HTTP section stating the
  global-bucket semantics ("a total throughput cap, not per-client
  fairness") and the handshake-counting caveat.

### 2. Graceful degradation — pin, don't build

No new machinery. Two new tests capture behavior that currently rests on
luck:

- Corrupt corpus resilience: a version directory containing a file of
  hostile bytes still serves search results from its healthy files
  (pins today's probe).
- Client-visible throttling: with a tiny bucket, a client sees a clean MCP
  error naming the rate limit, and succeeding calls resume once the bucket
  refills (use a burst sized so initialize passes and the tool call fails).

ROADMAP's "Error recovery and graceful degradation" item is checked off
citing the accumulated mechanisms (partial update results, discovery
fallback, fail-closed caches and token verification, corrupt-corpus search,
staleness advice) rather than pretending this PR built them.

### 3. Benchmarks — `tests/bench/`, `bench` marker, report-only

- Marker registered in `pytest.ini`; default addopts deselect becomes
  `-m "not e2e and not bench"`. Run via `pytest -m bench --no-cov -s`.
- Runs against the **real repo corpus** (`docs/12.x`, present in the working
  tree) through the in-memory `Client` — no subprocess, no network. Skips
  cleanly (`pytest.skip`) if the corpus is absent (fresh clone before a docs
  pull).
- Measures, over a fixed 10-query set spanning easy and hard lookups:
  `search_laravel_docs` (cold first call recorded separately — index build —
  then warm p50/p95 over ≥30 iterations), `read_laravel_doc_section`, and
  `laravel_docs_info`. Prints a table with p50/p95/max per operation against
  the 100 ms v1.0.0 target.
- Assertions cover setup only (results non-empty, section reads succeed);
  timing is printed, never asserted.
- CI: one informational Harness step after e2e running the bench suite; it
  fails only if the benchmarks themselves break. Lands with this PR's main
  merge (branch builds run main's YAML — same follow-up dance as the e2e
  step, noted for the plan).

## Out of scope (YAGNI)

Per-client rate limits and quota persistence, `Retry-After` metadata, locust
or other load-generator tooling, latency assertions in CI, and rate limiting
for stdio.

## Testing

- Unit: `build_rate_limiter` validation matrix (unset → None, bad values →
  SystemExit, stdio → warn+None, burst default arithmetic).
- Protocol/in-memory: throttle-and-recover flow; middleware ordering (a
  throttled request still increments `laravel_mcp_requests_total`).
- Corrupt-corpus search pin (unit).
- Bench suite as above; e2e untouched.
- Coverage gate stays ≥80.
