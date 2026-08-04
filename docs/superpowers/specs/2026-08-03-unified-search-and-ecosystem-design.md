# v0.13.0 sub-project 4 — Unified search, ecosystem mapping, upstream repairs: Design

Date: 2026-08-03
Status: Approved (interactive session; scope deliberately expanded at the
user's request to close out the milestone)

## Problem — the three roadmap bullets, grounded

Probing turned the vague "Documentation Improvements" bullets into verified
defects:

- **Search doesn't cover the advertised corpus.** `search_laravel_docs`
  indexes core versions and external services only. The 166 community-package
  files (Spatie, Livewire, Inertia, Filament — the "42,000+ lines" the README
  leads with) and the learning-resource indexes are invisible: "spatie
  permission roles" returns `12.x/filesystem.md`-grade noise. The README's
  "Unified search across core Laravel docs, services, and packages" is false.
- **The search→read flow is broken for non-core hits already.**
  `read_laravel_doc_section` resolves only under version directories, so a
  service hit ("forge/…") returned by search cannot be read back — latent
  since v0.11.0.
- **The package catalog's `documentation_link`s are dead.** All ~50 entries
  point at paths that have never existed (`laravel://packages/cashier.md`,
  `laravel://authentication/sanctum.md`); the real files are `billing.md`,
  `sanctum.md`, or fetched package docs with no resource scheme at all.

Expanded scope (user request): also repair the two upstream fetchers found
broken during sub-project 1, run the roadmap's open documentation
completeness audit, and prep the v0.13.0 release.

## Design

### 1. Unified search

- New corpus loaders mirroring the existing two (`load_version_sections`,
  `load_service_sections`): `load_package_sections(packages_dir, package)`
  and `load_learning_sections(learning_dir, source)`, chunking through the
  same `list_contained_markdown` + `chunk_markdown` path so containment and
  symlink refusal carry over. Per-corpus lazy indexes under the existing LRU
  (raise its cap if the corpus count now exceeds it — check at
  implementation).
- `search_laravel_docs` gains `sources: Optional[List[str]]` over
  `{"core", "services", "packages", "learning"}`; invalid entries are an
  error listing the valid set. Default `None` = all sources — the behavior
  the README already promises. `include_external` retained for
  back-compat: `False` → `["core"]`, exactly today's narrow behavior;
  explicit `sources` wins over it.
- `version`/`all_versions` scope the core corpus only; packages, services,
  and learning docs are not Laravel-versioned. This is the honest resolution
  of the "version-specific filtering improvements" bullet.
- Every hit gains `source`: `"core"`, `"service:<name>"`,
  `"package:<name>"`, `"learning:<name>"`. `file` stays
  `<corpus-key>/<path>` as today. Output schema updated; TOON text and
  structured content stay one dict.

### 2. Uniform read path

`read_laravel_doc_section_impl` and `read_laravel_doc_content_impl` resolve
corpus-prefixed filenames: when the first path segment names a known external
service, fetched package ecosystem, or learning source, resolve against that
corpus root (containment checked against that root, same helpers); otherwise
the existing version logic applies unchanged. Version validation applies only
to core paths. Fixes the broken service flow and makes every search hit
readable by the same rule that produced it.

New resource template `laravel-package://{package}/{path*}` mirroring
`laravel-external://`, so package docs are addressable as resources too.

### 3. Ecosystem mapping — catalog links

Repoint every `documentation_link` in `PACKAGE_CATALOG` at something that
resolves, in preference order: core doc file (`laravel://billing.md` for
cashier — version-less URIs already resolve against the runtime default),
fetched package docs (`laravel-package://spatie/...`), otherwise drop the
link rather than advertise a 404. Guard test: every catalog link resolves
through the real resource handlers (parametrized over the catalog, offline).

### 4. Upstream fetcher repairs (expanded scope)

- **Inertia**: the configured `resources/js/Pages` JSX path 404s — the
  upstream site repo restructured. Find the current location/format of the
  Inertia docs (likely markdown now), update the fetcher config and, if the
  format moved from JSX to markdown, route it through the existing markdown
  processing instead of `_process_jsx_to_markdown`. Refresh the fixture to
  match reality; the JSX processor and its tests stay (Filament-era JSX
  pages may still need it — remove only if nothing references it).
- **Laracasts**: `_extract_laracasts_topics` matches zero topics on the
  current page. Update the extractor's selectors against the recorded
  2026-08 fixture, unskew the sub-project-1 test that pins the zero-topic
  drift (it flips to asserting extraction works), and keep the
  moved-structure degradation case.
- Both verified against recorded fixtures only — the daily sync remains the
  live canary.

### 5. Documentation completeness audit (expanded scope)

The roadmap QA item, run as a claims-vs-reality sweep now that one false
claim is already confirmed: every capability claim in README (feature lists,
comparison table, TOON savings, counts like "117+ sections" and "42,000+
lines"), tool descriptions in `TOOL_DESCRIPTIONS`, and server instructions
gets checked against the running server. Deliverable: corrected copy in the
same PR, plus a short audit note in the spec directory listing what was
checked and what changed. Claims that can be guard-tested cheaply (tool
count, corpus presence) get tests; prose stays prose.

### 6. Release prep (expanded scope, lands only if 1–5 are green)

v0.13.0 ships once this merges: version bump across the guarded files,
CHANGELOG release section (Unreleased → 0.13.0, including the **Breaking**
callout for any tool-surface changes), ROADMAP flips v0.13.0 to completed.
Release commit follows the established flow (bump → merge → tag → registry
publish fires on the tag).

## Out of scope

Cross-corpus ranking tuning beyond BM25's existing behavior, search syntax,
fetching additional package ecosystems, per-corpus boosting, and the
`search_laravel_learning_resources` tool's future (folding it into unified
search is plausible but is a breaking removal that deserves its own
decision, not an 11pm one).

## Testing

- Retrieval quality: "spatie permission roles" → top hits carry
  `source: "package:spatie"`; "livewire wire:model" → livewire package hits;
  core queries unaffected (existing quality tests keep passing untouched).
- Read-back: for each source type, search → `read_laravel_doc_section` on
  the top hit succeeds — the flow contract, parametrized.
- Sources param: filtering, invalid values, `include_external=False`
  equivalence, version scoping applying to core only.
- Catalog link guard as §3. Fetcher repairs against fixtures as §4.
- e2e: one cross-source search + read flow over stdio. Bench: add one
  package-corpus query so latency claims cover the bigger index.
- Coverage gate ≥80 holds.

## Risks

- Default-on package/learning results change existing result mixes for core
  queries. BM25 scoring across corpora is approximate (per-corpus IDF); the
  quality tests assert core queries still surface core docs first.
- Index count grows from ~10 to ~20 lazy indexes; memory is bounded by the
  LRU cap, verified at implementation.
- Upstream page formats may have drifted further than the recorded
  fixtures; fixtures are refreshed once during implementation and the sync
  remains the canary.
