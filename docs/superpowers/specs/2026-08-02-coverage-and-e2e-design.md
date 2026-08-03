# v0.13.0 sub-project 1 — Coverage to 80% + real-transport e2e tests: Design

Date: 2026-08-02
Status: Approved (interactive session)

## v0.13.0 milestone map (context)

Four sub-projects, each with its own spec → plan → implementation cycle,
in order: **(1) this spec**, (2) health/metrics endpoints, (3) rate limiting +
graceful degradation + load testing, (4) documentation improvements (advanced
cross-source search, version filtering, ecosystem mapping). This spec covers
only (1).

## Problem

Product coverage sits at 67.7% (branch-inclusive) against a roadmap target of
80%. The gap is concentrated, not diffuse:

| Module | Line coverage | Uncovered lines |
|---|---|---|
| `docs_updater.py` | 64.4% | 687 of 1928 |
| `laravel_mcp_companion.py` | 69.2% | 235 of 764 |
| `mcp_tools.py` | 89.3% | 62 of 580 |
| everything else | 97–100% | 1 |

The uncovered code is the scraping/update machinery (fetchers, retry logic,
section discovery, HTML→markdown conversion, cache handling) and the server
wiring in `main()` (argument/env parsing, the HTTP branch that assembles auth,
CORS, host validation, and the well-known route together). Both are places
where regressions have actually shipped.

Separately, v1.0.0's criteria require "integration tests through a real MCP
client." Every existing test uses fastmcp's in-memory `Client` — real protocol
messages, but no transport. Nothing exercises stdio framing or the HTTP stack
end to end, which is exactly where the recent bug classes lived (auth, host
validation, transform surface).

## Decisions (made with the user)

- **Gate ratchets to achieved-minus-margin.** Land the tests, measure, then
  set `--cov-fail-under` just under the measured figure (e.g. measure 81%,
  gate at 80). No aspirational gate that fails every run; no gate left at 65
  after the work either. The existing guard test asserting the gate is
  configured continues to pass unchanged.
- **"Real MCP client" means a small subprocess smoke suite**, not a full
  matrix: ~10–15 tests spawning the actual server over stdio and over HTTP,
  running a representative flow. Everything else stays in-memory for speed.
- **Fixture-first strategy** (approach A): recorded payloads + mocked
  `urllib`, no live network in CI, no fixture-HTTP-server refactor of
  docs_updater's hardcoded upstream URLs.

## Design

### 1. Fixture corpus — `tests/fixtures/`

Recorded, checked-in payloads (the directory exists and is empty today):

- GitHub API: tags listing, branch commit response, rate-limit error body.
- One representative HTML page per external service (Forge, Vapor, Envoyer,
  Nova) captured from the live sites, plus one community-package page.
- Malformed variants: 404 body, truncated HTML, a page whose section
  structure moved (exercises auto-discovery's adaptation path), empty
  response.

Fixtures are static files; a `fixture(name)` helper in `tests/conftest.py`
loads them. Capture is a one-time manual step during implementation, not a
test-time network call — CI never touches the network (`network`/`external`
markers stay excluded).

### 2. docs_updater unit tests — the 687 lines

New modules split by responsibility (mirroring the class structure rather
than one giant file):

- `tests/unit/test_docs_fetching.py` — fetcher paths: success, HTTP error →
  retry with backoff (`time.sleep` mocked), exhaustion after `max_retries`,
  timeout, malformed JSON. Asserts behavior (returned/raised values, retry
  counts), not call sequences.
- `tests/unit/test_docs_discovery.py` — section discovery over the recorded
  service pages: sections found on the happy page, adaptation on the
  moved-structure page, sanitization of hostile section names (extending the
  v0.10.0 security tests' fixtures, not duplicating them).
- `tests/unit/test_docs_conversion.py` — HTML→markdown conversion and asset
  filtering over the recorded pages; golden-file comparison against expected
  markdown output.
- `tests/unit/test_docs_cache_handling.py` — cache TTL behavior,
  metadata read/write, the update-clears-both-caches contract.

Target: docs_updater ≥ 80% line coverage. The genuinely unreachable corners
(defensive except-blocks around interpreter-level failures) are left red, not
contorted around — that is what the margin in the ratchet is for.

### 3. Server-wiring tests — the 235 lines

In-process, no subprocess:

- `parse_arguments` edge cases via `sys.argv`/env monkeypatching: env
  fallbacks, CLI-replaces-env for the append-type flags, invalid
  `TRANSFORM_MODE` from env, auth flag surface.
- HTTP-branch assembly: extract the app-building block of `main()` (from
  transform-mode resolution through `attach`-ing CORS/well-known) into a
  testable `build_http_app(args, mcp)` helper — a mechanical extraction,
  behavior unchanged — then test the assembled app in-process: CORS headers
  present only when origins configured, wildcard origin exits, 421 on bad
  Host off-loopback, auth 401 + well-known coexisting. `main()` keeps only
  argument resolution, startup logging, and `uvicorn.run`.
- Resource handlers (`read_laravel_doc`, `read_external_laravel_doc`) through
  the in-memory client's resource reads — currently near-zero coverage.

### 4. e2e smoke suite — `tests/e2e/`, new `e2e` marker

Excluded from the default run and from coverage measurement; run explicitly
(`pytest -m e2e`) and in CI as a separate step so a hang can't mask the unit
suite. Spawns `python laravel_mcp_companion.py` as a subprocess against a
prepared temp docs tree:

- stdio: fastmcp `Client` over stdio transport — initialize (server version,
  capabilities incl. tasks), search → read-section flow, structured content
  present, transform surface (`search_tools`/`call_tool`) responds.
- HTTP: server on an ephemeral port — same flow over streamable HTTP, plus
  `/.well-known/mcp/server.json`, plus one auth case (401 without token,
  200 with `AUTH_STATIC_TOKENS` token).
- One `--transform-mode none` stdio case pinning representative tools of the
  raw surface (subset assertion by design: the surface grows with the product,
  and an exact count would break on every tool addition without adding signal).

Budget: ~10–15 tests, each with a hard timeout so a wedged subprocess fails
fast. These validate transports and packaging (the ENTRYPOINT path Docker
uses), not coverage.

### 5. Finish line

- Measure; set `--cov-fail-under` to measured-minus-1, minimum 80 if the
  measurement allows, in `pytest.ini` only.
- Update ROADMAP QA checkbox and the coverage figure in ROADMAP's completed
  list; CHANGELOG under Unreleased (tests don't ship user-facing behavior —
  one line suffices).
- CI: add the `pytest -m e2e` step to the Harness ci pipeline **in a
  follow-up PR after merge** — branch builds run main's pipeline YAML, so the
  step lands separately once the suite exists on main.

## Error handling & risks

- Recorded fixtures drift from live sites: acceptable — these tests pin the
  parser's contract, and the daily sync is the live-site canary. Refresh
  fixtures when a real structural change lands.
- Subprocess tests are the flake-prone kind: hard timeouts, ephemeral ports,
  no fixed sleeps (poll for readiness), and the separate CI step keep them
  from destabilizing the main suite.
- The `build_http_app` extraction touches `main()`: mechanical, covered
  immediately by the new wiring tests plus the existing auth/well-known
  tests, verified by the e2e HTTP cases.

## Success criteria

- Overall branch-inclusive coverage ≥ 80%; gate ratcheted to hold it.
- docs_updater.py ≥ 80% line coverage.
- e2e suite green over both transports, runnable locally with one command.
- Full unit+protocol suite stays under ~90 seconds locally.
