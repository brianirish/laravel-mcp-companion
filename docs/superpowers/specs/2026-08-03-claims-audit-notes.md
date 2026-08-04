# Documentation completeness audit — notes

Date: 2026-08-03. The roadmap QA item, run as a claims-vs-reality sweep of
README.md, ROADMAP.md, `TOOL_DESCRIPTIONS`, and the server instructions
against the running server and the shipped corpus.

## Verified true (no change)

- "Multi-version Laravel documentation (6.x through latest)" — 6.x–13.x
  directories present and searchable.
- "42,000+ lines from Spatie, Livewire, Inertia, Filament" — measured 46,236
  lines under `docs/packages/`.
- "117+ sections" of service docs — 147 files under `docs/external/`.
- "Auto-discovery" service claims, TOON example output, transform-mode copy,
  HTTP security copy, operational-endpoint copy — match behavior.
- Comparison-table capability rows — each maps to a real tool.

## Corrected

- **"50+ curated packages" → 22** (README ×2, ROADMAP ×1). `PACKAGE_CATALOG`
  has 22 entries; the inflated figure predates this audit trail. A guard now
  ties the README figure to the catalog length.
- **`search_laravel_docs` description** claimed "Returns file names and match
  counts" — the pre-v0.11.0 substring-search contract, false for two
  releases. Rewritten for ranked sections + unified sources.
- **"Unified search across core Laravel docs, services, and packages"** —
  false until this branch (packages and most nested service files were not
  indexed); now true and covered by retrieval-quality tests.
- Package catalog `documentation_link`s — 19 of 22 dead; repointed and
  guard-tested (see the unified-search spec).

## Left alone, deliberately

- TOON "30-60% fewer tokens" — upstream project's benchmark claim, presented
  with attribution and an example; not re-measured here.
- "Daily updates" — true via the docs-sync cron; the sync pipeline is its own
  canary.

## Guards added

- README's curated-package count must equal `len(PACKAGE_CATALOG)`.
- Corpus presence: the README's named ecosystems exist under
  `docs/packages/` in a shipped tree (skip-if-absent locally).
