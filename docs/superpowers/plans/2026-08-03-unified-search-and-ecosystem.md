# Unified Search, Ecosystem Mapping, Upstream Repairs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the advertised corpus actually reachable — packages and learning resources join the flagship search, every hit is readable back, catalog links resolve — plus repair the two broken upstream fetchers, run the claims audit, and prep the v0.13.0 release.

**Architecture:** Spec: `docs/superpowers/specs/2026-08-03-unified-search-and-ecosystem-design.md`. Corpus loaders follow the `load_version_sections`/`load_service_sections` pattern in `mcp_tools.py` (list_contained_markdown + chunk_markdown; the Section `version` field carries the corpus key). Corpus roots derive from the filesystem (`docs/external/*`, `docs/packages/*`, `docs/learning_resources/*` subdirectories), not fetcher registries — a corpus exists iff its directory does.

**Tech Stack:** Existing BM25 machinery in `doc_search.py` (`get_index(docs_path, key, loader)`), FastMCP resources, recorded fixtures.

## Global Constraints

- Coverage ≥80; TOON text + structured content stay one dict; commits plain `git commit` (evening).
- `include_external=False` must reproduce today's core-only behavior byte-for-byte; explicit `sources` wins over it.
- `version`/`all_versions` scope core only. Valid sources: `{"core","services","packages","learning"}`; invalid → error dict listing them.
- Check `doc_search.py`'s index-cache cap before landing Task 1 (corpus count roughly doubles); raise it if it would evict mid-search.

---

### Task 1: corpus loaders + search fan-out + `source` labels

**Files:** Modify `mcp_tools.py` (loaders + `search_laravel_docs_data`), `tool_schemas.py` (source/sources in output schema), `laravel_mcp_companion.py` (tool signature gains `sources`); Test `tests/unit/test_unified_search.py`.

**Interfaces — Produces:** `load_package_sections(packages_dir: Path, package: str) -> List[Section]`; `load_learning_sections(learning_dir: Path, source: str) -> List[Section]`; `search_laravel_docs_data(..., sources: Optional[List[str]] = None)`; hit dict gains `"source"`.

- [ ] **Step 1: failing tests** — fixture tree with core + external/forge + packages/spatie + learning_resources/laravel-blog content: default search returns hits from all four with correct `source` labels (`core`/`service:forge`/`package:spatie`/`learning:laravel-blog`); `sources=["packages"]` returns only package hits; `sources=["core"]` ≡ `include_external=False` result set; invalid source value → error dict naming the valid set; explicit `sources` beats `include_external`; version scoping still core-only (package hits identical across `version=` values). Real-corpus quality (skip-if-absent, same guard as bench): "spatie permission roles" top-3 contains a `package:spatie` hit; "livewire wire:model" surfaces `package:livewire`; "how do I retry a failed queue job" still surfaces core `queues.md` first.
- [ ] **Step 2: run, verify failure.** **Step 3: implement** — loaders; fan-out loops over corpus dirs per requested source (index keys `package:<name>`, `learning:<name>`); source label derived from the corpus key at hit-build time; cache key includes sources. Check/raise the index cache cap. **Step 4: pass + full suite.** **Step 5: commit.**

### Task 2: uniform read path + `laravel-package://` resource

**Files:** Modify `mcp_tools.py` (`read_laravel_doc_section_impl`, `read_laravel_doc_content_impl` corpus-prefix resolution), `laravel_mcp_companion.py` (resource template); Test `tests/unit/test_cross_corpus_reads.py`.

- [ ] **Step 1: failing tests** — parametrized over source types: search top hit's `file` + `anchor` feeds `read_laravel_doc_section_impl` and succeeds (the flow contract); content reads for `forge/...`, `spatie/...`, `laravel-blog/...` resolve; traversal attempts against corpus roots denied; version validation still applies to core paths and NOT to corpus paths; unknown prefix falls through to today's version logic (so `12.x/routing.md` still works). Resource: `laravel-package://spatie/<real-file>.md` readable via in-memory client; unknown package lists available ones.
- [ ] **Step 2–5:** fail → implement (resolution: first path segment ∈ existing subdirs of external/packages/learning roots → resolve+contain there; else current logic) → pass → commit.

### Task 3: catalog links repointed + guard

**Files:** Modify `laravel_mcp_companion.py` (`PACKAGE_CATALOG` links); Test `tests/unit/test_catalog_links.py`.

- [ ] **Step 1: guard test first** — parametrized over `PACKAGE_CATALOG`: every `documentation_link` resolves through the real handlers (`laravel://` → `read_laravel_doc`-equivalent impl, `laravel-package://` → the new impl); entries without links are exempt but counted (assert the with-link count stays ≥ some floor so links don't quietly vanish as a "fix").
- [ ] **Step 2:** run — expect ~50 failures enumerating every dead link. **Step 3:** repoint each: core file where the package is core-documented (cashier→`billing.md`, sanctum→`sanctum.md`, scout→`scout.md`, …), `laravel-package://` for fetched ecosystems, drop otherwise. **Step 4–5:** pass → commit.

### Task 4: Inertia fetcher repair

**Files:** Modify `docs_updater.py` (inertia config/fetch path), `tests/fixtures/` (refreshed fixture); Test updates in `tests/unit/test_package_fetchers.py` + conversion tests.

- [ ] **Step 1: research** — find where inertiajs.com docs live now (WebFetch the repo tree / site). Record the real format.
- [ ] **Step 2:** capture one real page as a fixture. **Step 3:** failing test: fetcher retrieves+converts the recorded page into non-trivial markdown. **Step 4:** update config/fetch route (markdown path if the format moved; `_process_jsx_to_markdown` stays while any caller remains). **Step 5:** pass, commit.

### Task 5: Laracasts extractor repair

**Files:** Modify `docs_updater.py` (`_extract_laracasts_topics`); Test `tests/unit/test_learning_fetcher.py` (flip the drift-pin test).

- [ ] **Step 1:** inspect the recorded `laracasts_index.html` structure; write the failing test asserting topics extract from it (flip `test_laracasts_extraction_finds_nothing_on_current_page` to assert success; keep moved-structure → `[]`). **Step 2–4:** update selectors → pass → commit.

### Task 6: claims audit

**Files:** Modify `README.md`, `TOOL_DESCRIPTIONS` / server instructions as findings dictate; Create `docs/superpowers/specs/2026-08-03-claims-audit-notes.md`; guard tests where cheap.

- [ ] **Step 1:** sweep README capability claims + comparison table + counts, every `TOOL_DESCRIPTIONS` entry, and `build_server_instructions` output against the running server (in-memory client). Log each claim → verified/corrected in the notes file.
- [ ] **Step 2:** correct false copy (the unified-search claim becomes true via Tasks 1–2 — verify wording); guard-test the cheap invariants (tool count in `none` mode, corpus dirs the README counts). **Step 3:** commit.

### Task 7: e2e + bench + docs + PR

- [ ] e2e stdio: one cross-source search→read flow. Bench: add a package-corpus query. README feature copy updated for sources/labels; ROADMAP checks off the three sub-project-4 bullets + documentation completeness audit; CHANGELOG Unreleased (Added: unified search/sources/labels/resource + fetcher repairs; Fixed: dead catalog links + service-hit read breakage). Full verify (suite, e2e, bench, ruff, mypy) → push → PR.

### Task 8: release prep (only if 1–7 green and merged)

- [ ] After PR merges: on main — bump 0.12.0→0.13.0 across pyproject/SERVER_VERSION/server.json/ROADMAP/README heading; CHANGELOG Unreleased → `[0.13.0]`; ROADMAP v0.13.0 → COMPLETED; guards green; push, tag `v0.13.0`, GitHub release, watch registry publish + Harness.

## Self-Review

- Spec §1→T1, §2→T2, §3→T3, §4→T4, §5→T6, §6→T8, testing section distributed + T7. Deliberate slip order if the evening runs out: T6, T8 (stated in spec).
- Interfaces consistent across tasks; corpus-root rule stated once (filesystem-derived) and reused.
