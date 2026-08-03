# Coverage to 80% + real-transport e2e tests — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Raise branch-inclusive product coverage from 67.7% to ≥80%, add a subprocess e2e suite over real stdio/HTTP transports, ratchet the gate to hold it.

**Architecture:** Target the *enumerated* uncovered blocks in `docs_updater.py` (3,882 lines, 64.4%) and `laravel_mcp_companion.py` (69.2%) — do NOT duplicate the extensive happy-path coverage already in `tests/unit/test_docs_updater.py` (1,581 lines; see its per-class inventory in the design notes below). New unit tests use recorded fixtures + `docs_updater.urllib.request.urlopen` monkeypatching (the module-level import at `docs_updater.py:18` is the single canonical patch target; also patch `docs_updater.time.sleep` and `docs_updater.random.uniform` in every retry test). e2e lives in `tests/e2e/` behind a new marker.

**Tech Stack:** pytest (asyncio_mode=auto), fastmcp in-memory `Client` + stdio/HTTP transports, curl for one-time fixture capture.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-08-02-coverage-and-e2e-design.md`. Gate policy: ratchet to measured-minus-1 at the END (Task 9), not before.
- `pytest.ini` is the only pytest config (guard-tested). Coverage source config lives in pyproject only.
- No live network in tests: CI must never hit GitHub/laravel.com. Fixture capture is a one-time implementation step.
- New-test hygiene (from the module map): always pass temp paths to constructors (they `mkdir` in `__init__`); never call `get_supported_versions()` without `cache_file=` (default writes into the repo's `docs/`); reset `docs_updater._SUPPORTED_VERSIONS_CACHE = None` when touching version discovery; `test_external_docs_dir`'s `.cache_metadata.json` has hardcoded `cached_at: 1704110400.0` (always stale) — freeze or rewrite when asserting valid caches.
- Known-uncovered blocks being targeted (line refs): 3090–3574 (`LearningResourceFetcher`, no tests at all), 2755–3006 (`update_all`/`get_all_documentation_status`/`MultiSourceDocsUpdater.needs_update`), 1430–1467 + 1542–1570 (retry backoff branches), 2207–2279 (`_process_jsx_to_markdown`), 2703–2740 (`update_package_docs`/`update_learning_docs`), 3681–3697 + 3745–3880 (docs_updater CLI `update_version`/`main`), 956–970 (section sanitization/asset skip branches), 172–223 (versions-cache error paths).
- Commit after each task (plain `git commit` evenings/weekends; `git lc` weekday 9–5 Toronto).

---

### Task 1: Fixture corpus + loader

**Files:** Create `tests/fixtures/{github_branch_commit.json, github_branches.json, forge_index.html, blog_index.html, news_index.html, laracasts_index.html, inertia_page.jsx, truncated.html, moved_structure.html}`; Modify `tests/conftest.py` (add `fixture_path`/`load_fixture` helpers).

- [ ] Capture real payloads once (curl with a browser UA): GitHub `branches/12.x` API JSON + branches list, `https://forge.laravel.com/docs` index, `https://blog.laravel.com`, `https://laravel-news.com`, `https://laracasts.com/topics/laravel` (trim each to <100KB, keeping the nav/article structure the extractors parse), one Inertia `.jsx` doc page from raw.githubusercontent. Synthesize `truncated.html` (cut mid-tag) and `moved_structure.html` (valid HTML, none of the expected selectors).
- [ ] Add to `tests/conftest.py`:

```python
FIXTURES = Path(__file__).parent / "fixtures"

def load_fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")

def urlopen_returning(payload: bytes, url_map: dict[str, bytes] | None = None):
    """Context-manager mock for docs_updater.urllib.request.urlopen.
    With url_map, serve per-URL-substring payloads; else always `payload`."""
```

- [ ] Commit: "Add recorded fixtures for docs_updater tests"

### Task 2: LearningResourceFetcher suite (biggest block, zero existing tests)

**Files:** Create `tests/unit/test_learning_fetcher.py`. Interfaces consumed: `LearningResourceFetcher(target_dir, cache_duration=86400, max_retries=3)` (`docs_updater.py:3012`), sources registry `:3028` (laravel-bootcamp, laravel-blog, laravel-news, laracasts-index).

- [ ] Write failing tests, then run, then (no impl needed — this is test-only) verify they pass against the real class; investigate any that fail as potential bugs:
  - `fetch_learning_source`: unknown source → False; cached+fresh (write metadata with `cached_at=time.time()`, `success_rate=1.0`) → True without network (urlopen mock that raises if called); `force=True` bypasses cache.
  - `_fetch_blog_index` / `_fetch_news_index` / `_fetch_laracasts_metadata` against the recorded pages: writes the expected `.md` files, metadata carries `success_rate` and `cached_at` (`:3112` stamps it — assert it, contrasting with the External bug in Task 5).
  - `_extract_blog_articles` / `_extract_news_articles` / `_extract_laracasts_topics` on recorded + `moved_structure.html` (→ empty list, no raise).
  - `_fetch_and_process_html`: recorded page → markdown >100 chars with nav/script gone; `moved_structure.html` body <100 chars → None.
  - `_retry_request` (`:3534`): 404 raises immediately; 5xx retries then succeeds (assert sleep called with uncapped `2**attempt` backoff, `random.uniform` patched to 0); exhaustion raises.
  - `is_cache_valid` threshold: `success_rate=0.69` → invalid, `0.7` → valid (freeze `time.time`).
- [ ] Run `uv run pytest tests/unit/test_learning_fetcher.py --no-cov -q` → all pass. Commit: "Cover LearningResourceFetcher end to end"

### Task 3: MultiSourceDocsUpdater orchestration suite

**Files:** Create `tests/unit/test_multi_source_orchestration.py`. Consumes `MultiSourceDocsUpdater(temp_dir, "12.x")` (composes 4 fetchers, no injection point — patch the composed instances' methods directly, e.g. `updater.package_fetcher.fetch_package_docs = Mock(...)`).

- [ ] Failing tests for the uncovered orchestration paths (2703–2740, 2755–3006):
  - `update_package_docs` with named packages / all / a fetcher returning False.
  - `update_learning_docs` same shape.
  - `update_all`: partial failure — one sub-updater raises, result dict still carries the others (the `:2806` swallow); all-success shape; force flags forwarded (assert via mocks).
  - `MultiSourceDocsUpdater.needs_update` (`:2947`): each check_* flag toggles its section; core metadata missing → True.
  - `get_all_documentation_status` remaining variants: empty tree, populated tree (uses `test_docs_dir` + `test_external_docs_dir` fixtures).
- [ ] Run → pass. Commit: "Cover multi-source update orchestration"

### Task 4: Retry/backoff branch matrix

**Files:** Create `tests/unit/test_retry_behavior.py`. Targets: `ExternalDocsFetcher._retry_request` (`:1399`, uncovered 1430–1467), `DocsUpdater.get_latest_commit` (`:1508`, uncovered 1542–1570), `DocumentationAutoDiscovery._retry_request` exhaustion edges.

- [ ] Parametrized failing tests, `docs_updater.time.sleep` and `docs_updater.random.uniform` patched, capturing sleep args:
  - External `_retry_request`: 403+"rate limit" in reason → sleep `min(300, 2**attempt*5 + jitter)`; plain 403 → raises immediately; `URLError` branch retries with `min(30, ...)`; generic Exception branch; exhaustion re-raises last exception; `max_retries=0` override does one attempt.
  - `get_latest_commit`: rate-limit backoff `min(300, 2**attempt*30)` (no jitter — assert exact values); 5xx retry-then-succeed; exhaustion raises; malformed JSON (missing `commit` key) → `KeyError` propagates (and separately: `needs_update()` swallows it into `True`).
  - AutoDiscovery `_retry_request`: courtesy-delay pre-sleep on attempt>0 (`request_delay * 2**(attempt-1)`).
- [ ] Run → pass. Commit: "Cover the retry backoff branch matrix"

### Task 5: Cache handling + the cached_at bug fix

**Files:** Modify `docs_updater.py` (`ExternalDocsFetcher.save_cache_metadata:869`, `_fetch_service_documentation` metadata dict `:1002`, `_fetch_github_documentation` `:1123`); Create `tests/unit/test_cache_validity.py`.

**The bug:** External metadata never includes `cached_at` (`is_cache_valid:851` reads `.get('cached_at', 0)` → always stale → every request refetches, defeating `cache_duration`). `_fetch_github_documentation` also writes no `success_rate` (→ 0.0 → invalid).

- [ ] Failing test first: run `_fetch_service_documentation` against a mocked fetch for one section, then assert `is_cache_valid(service)` is True immediately after. Expect FAIL (cached_at absent).
- [ ] Fix: stamp `metadata.setdefault("cached_at", time.time())` inside `save_cache_metadata` (mirrors `LearningResourceFetcher:3112`), and add `success_rate` to `_fetch_github_documentation`'s metadata (1.0 on success path).
- [ ] More tests: `CommunityPackageFetcher.is_cache_valid` mtime-based path (fresh file valid, `os.utime` back-dated file invalid); versions-cache error paths (`_read_versions_cache`: corrupt JSON, non-list, invalid entry rejected by the `\d+\.x` fullmatch, missing `updated_at` with TTL, naive-timestamp coercion — lines 172–223).
- [ ] Full existing suite still green (`uv run pytest tests/unit/test_docs_updater.py tests/unit/test_package_fetchers.py --no-cov -q`). Commit: "Fix external docs cache never validating after a fetch"

### Task 6: Conversion + sanitization skip branches + docs_updater CLI

**Files:** Create `tests/unit/test_docs_conversion_extra.py`, `tests/unit/test_docs_updater_cli.py`.

- [ ] Conversion failing tests: `_process_jsx_to_markdown` (`:2142`) on the recorded Inertia page (headings/code preserved, JSX syntax gone) and on garbage (→ None); `_clean_jsx_text` cases; `ExternalDocsFetcher._extract_html_content` selector-fallback chain using `moved_structure.html` (falls to body) and the 50,000-char truncation.
- [ ] Sanitization skip branches (`:956–970`): `_fetch_service_documentation` with a discovered section list containing `../evil` and an asset (`logo.png`) — both skipped, counted in denominator, success_rate reflects it (document the "hostile input permanently drags success_rate" behavior in a test comment).
- [ ] Discovery arbitration: discovered < 75% of manual count → manual wins (`discovery_method: "manual configuration"` in metadata); ≥75% → discovery wins. (`:930–944`)
- [ ] CLI (`update_version:3674`, `main:3719`, uncovered 3745–3880): drive `docs_updater.main()` via monkeypatched `sys.argv` + mocked `MultiSourceDocsUpdater`/`DocsUpdater` for the command paths existing tests skip (check-only mode, update failure exit codes, the all-sources path).
- [ ] Run → pass. Commit: "Cover conversion edges, sanitization skips, and the updater CLI"

### Task 7: Server wiring — build_http_app extraction + tests

**Files:** Modify `laravel_mcp_companion.py` (extract from `main()`); Create `tests/unit/test_http_wiring.py`; extend `tests/unit/test_laravel_mcp_companion_main.py` for arg edges.

**Interfaces — Produces:** `build_http_app(args, mcp) -> tuple[Starlette, str, int]` (app, host, port): everything in today's HTTP branch from `port = args.port if args.port else 8081` through the CORS middleware block inclusive; `main()` keeps mode resolution, `create_mcp_server`, logging, shutdown handler, and calls `uvicorn.run(*build_http_app(args, mcp))`-style. Wildcard-CORS `sys.exit(1)` moves into `build_http_app`. Behavior unchanged.

- [ ] Failing tests first (in-process, `httpx.ASGITransport`):
  - wildcard CORS origin → `SystemExit`.
  - no origins → no CORS headers on response; explicit origin → `access-control-allow-origin` echoed on preflight, credentials disallowed.
  - loopback default host `127.0.0.1`, port default 8081, `args.port` honored.
  - off-loopback (`host="0.0.0.0"`) → request with bogus `Host:` header gets 421 (assemble app, don't bind a socket).
  - auth + well-known coexist: with `AUTH_STATIC_TOKENS`, `/mcp/` → 401 but `/.well-known/mcp/server.json` → 200 (reuses Task-independent existing helpers from test_well_known.py patterns).
  - `parse_arguments` edges not yet covered: env-fallback for `AUTH_REQUIRED_SCOPES` CSV, CLI append replaces env list, invalid env `TRANSFORM_MODE` → parser error.
  - Resource handlers: in-memory `Client.read_resource("laravel://12.x/routing.md")` and `laravel-external://forge/...` happy + traversal-denied + missing-file paths (near-zero coverage today).
- [ ] Extract `build_http_app`, wire `main()` to use it. Run the new tests + full suite. Commit: "Extract and test the HTTP app assembly"

### Task 8: e2e suite over real transports

**Files:** Create `tests/e2e/__init__.py`, `tests/e2e/conftest.py`, `tests/e2e/test_stdio.py`, `tests/e2e/test_http.py`; Modify `pytest.ini`.

- [ ] `pytest.ini`: add `e2e` marker line, and `-m "not e2e"` to addopts (CLI `-m e2e` overrides — the last `-m` wins). e2e runs use `--no-cov` so the gate doesn't fire on the subset.
- [ ] `tests/e2e/conftest.py`: session fixture building a temp docs tree (reuse `test_docs_dir`-style content builder); `stdio_client()` helper → `fastmcp.Client` with a `PythonStdioTransport` pointed at `laravel_mcp_companion.py` with `--docs-path <tmp> --transport stdio --transform-mode none`; `http_server()` helper → `subprocess.Popen([sys.executable, "laravel_mcp_companion.py", "--transport", "http", "--port", str(free_port), ...])`, poll the port for readiness (no fixed sleeps), yield base URL, terminate with `timeout=5` then kill. Every test carries `@pytest.mark.e2e` and `@pytest.mark.timeout(30)` — add `pytest-timeout` to dev deps.
- [ ] stdio tests (~6): initialize (serverInfo.version == SERVER_VERSION, `tasks` capability present); search → `read_laravel_doc_section` flow; structured content on `laravel_docs_info`; default transform surface (separate client run without `--transform-mode none`: `search_tools`/`call_tool` present, `call_tool` proxies with structuredContent); resource read.
- [ ] HTTP tests (~6): same initialize+flow over streamable HTTP; `/.well-known/mcp/server.json` 200 + name; auth pair (401 bare / 200 with `AUTH_STATIC_TOKENS` token via env on the subprocess); 421 on bad Host.
- [ ] Run `uv run pytest -m e2e --no-cov -q` → green; run bare `uv run pytest -q` → e2e deselected, suite time still ~previous. Commit: "Add end-to-end tests over real stdio and HTTP transports"

### Task 9: Ratchet, docs, verification

**Files:** Modify `pytest.ini` (gate), `ROADMAP.md`, `CHANGELOG.md`.

- [ ] Full run: `uv run pytest -q`; read the total. Expect ≥80; if short, check `coverage.xml` per-module and top up the largest remaining block (repeat once, don't chase decimals).
- [ ] Set `--cov-fail-under=<measured-1>` in pytest.ini; update its ratchet comment.
- [ ] ROADMAP: check off "80%+ coverage" and "integration tests through a real MCP client" (v1.0.0 list cross-ref); update the "67%" figure in the completed-features line. CHANGELOG `[Unreleased]`: one Added line (e2e suite), one Fixed line (external cache validity bug).
- [ ] `uv run ruff check .` and `uv run mypy --ignore-missing-imports .` clean; `uv run pytest -m e2e --no-cov -q` green.
- [ ] Commit: "Ratchet the coverage gate to the measured figure"

## Self-Review

- Spec coverage: fixtures→T1, docs_updater 687 lines→T2–T6, server wiring 235→T7, e2e→T8, ratchet/docs→T9. cached_at bug fix included (T5) — a behavior fix discovered during design, noted for changelog.
- No placeholders; line refs come from the module map dated 2026-08-02 (they drift if docs_updater changes first — re-grep before relying on exact numbers).
- Type consistency: `load_fixture`/`urlopen_returning` (T1) consumed by T2/T4/T6; `build_http_app(args, mcp)` produced T7, consumed by T8's understanding of main() but e2e drives the CLI, not the function.
