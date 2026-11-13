# Laravel MCP Companion - Roadmap

What has been built, and what is left before 1.0.0.

## Mission

**Every Laravel version, the whole ecosystem, fully local.**

Laravel MCP Companion is a reference library for anyone looking something up in Laravel: any
version, any MCP client, no project required. It holds the documentation on the user's machine,
so it works offline and the same way every time.

It complements the official tools. [Laravel Boost](https://github.com/laravel/boost) is for writing
code inside one Laravel project and knows what that project uses. Companion is for reference:
several Laravel versions side by side, clients with no project open, and places where the
documentation has to stay local. The learning paths and topic browsing are kept, as supporting
features and not as the point of the project.

---

## Current Version: v0.15.0

### What it does today
- **Framework documentation** for Laravel 6.x through 13.x, with version comparison
- **First-party services:** Forge, Vapor, Envoyer, Nova, Cloud, Nightwatch and Herd
- **Package documentation:** Livewire, Filament, Inertia and Spatie, each on its current major
- **Ranked section search** across all of it, and section-level reads
- **A curated catalog** of 42 packages, with legacy ones flagged
- **Twelve tools** with declared output schemas, structured errors and a recorded contract
- **A nightly sync** with a health report for every source
- **An installable Python package** as well as the Docker image, both carrying the documentation

---

## ✅ v0.9.0 - Learning Resources & Discovery (COMPLETED)
**Released: Q1 2026**

### Learning Resource Infrastructure ✅
- ✅ Learning resource data model with difficulty levels (beginner/intermediate/advanced)
- ✅ 15 semantic categories for documentation organization
- ✅ Learning path generation based on topic and skill level
- ✅ "I need X" documentation finder for natural language queries
- ✅ Related content suggestions based on current context

### New MCP Tools ✅
- ✅ `list_learning_categories` - Browse all 15 documentation categories
- ✅ `get_learning_resources` - Retrieve resources by category and difficulty
- ✅ `find_documentation_for_need` - Natural language documentation discovery
- ✅ `get_learning_path` - Generate structured learning sequences
- ✅ `get_resources_by_difficulty` - Filter content by skill level
- ✅ `search_learning_resources` - Full-text search across learning materials
- ✅ `get_related_resources` - Find related documentation
- ✅ `get_quick_reference` - Condensed reference guides

### Infrastructure ✅
- ✅ Learning resource registry with category mappings
- ✅ Difficulty classification system
- ✅ Integration with existing documentation aggregation

---

## ✅ v0.10.0 - Security Hardening (COMPLETED)
**Released: Q3 2026**

Pulled forward from the Production Readiness milestone after an audit found
exploitable path traversal in tool arguments. Contains breaking changes — see the
release notes before upgrading.

### Path Traversal Fixes ✅
- ✅ Validate the `version` argument against supported versions in every tool
  (it was joined onto the docs path unchecked, allowing arbitrary `.md` reads)
- ✅ Single correct containment helper using `resolve()` + `is_relative_to()`,
  replacing two broken implementations
- ✅ Validate learning resource `source`/`sources` as real subdirectories
- ✅ Sanitize remotely-discovered section names before using them as file paths
- ✅ Validate `version` in `DocsUpdater` before creating directories

### HTTP Transport Hardening ✅
- ✅ Bind loopback by default instead of all interfaces
- ✅ Enable Host/Origin validation (blocks DNS rebinding and drive-by localhost)
- ✅ Require explicit `--cors-origin`; no wildcard reflection with credentials
- ✅ 47 regression tests covering every traversal

### Performance ✅
- ✅ Cache-first version lookup with TTL; timeouts on all network calls
- ✅ Fixed stale documentation served after updates (caches were not all cleared)
- ✅ Version-scoped search by default; right-sized file cache
- ✅ One GitHub API call per update instead of three

---

## ✅ v0.11.0 - Retrieval Quality & Currency (COMPLETED)
**Released: Q3 2026**

Not the MCP Modernization originally planned for this slot — that moved to
v0.12.0. An audit of whether the project actually delivers "the latest Laravel
documentation at the ready" found retrieval and currency both broken, and those
are the point of the project. Contains breaking changes; see the release notes.

### Retrieval ✅
- ✅ BM25 ranking over documentation *sections* instead of substring match counts
  on whole files — four of seven realistic developer questions previously
  returned nothing at all
- ✅ `read_laravel_doc_section` for section-level reads; a full answer costs
  ~3,200 tokens against ~34,000 for the whole-file path
- ✅ Lazy per-version index with an LRU cap; substring fallback preserved for
  exact-symbol queries like `queue:retry`

### Documentation Currency ✅
- ✅ Report the date Laravel last changed each version, not the date we fetched
  it — five of eight versions were being called stale while byte-identical to
  upstream, with a warning no tool could clear
- ✅ Staleness now judges the copy rather than a version, and says to pull a
  newer image rather than run a tool that cannot help
- ✅ `update_laravel_docs` accepts `version` like every other tool

### Security ✅
- ✅ Validate `version` in `laravel_docs_info`, which v0.10.0 missed despite
  claiming otherwise
- ✅ Filter the supported-versions cache on read; it is the trust root for every
  allowlist and was writable through a bind-mounted file
- ✅ One containment rule across reading, listing, and searching
- ✅ Close the check-to-open TOCTOU with `O_NOFOLLOW`
- ✅ Reject wildcard entries in `ALLOWED_HOSTS`

### Release & CI ✅
- ✅ Documentation syncs tagged `docs-YYYY-MM-DD` instead of consuming semver
- ✅ CI runs the Python version the project actually declares
- ✅ Coverage measured against product code only, so the reported figure is real
- ✅ Version-drift guards that compare against release tags, not just each other

---

## ✅ v0.12.0 - MCP Modernization (COMPLETED)
**Released: Q3 2026 — originally targeted Q1 2027**

### MCP 2025-11-25 Spec Compatibility
- [x] **Tasks primitive** for async documentation updates — both update tools
  declare optional task support; sync clients are unaffected
- [x] **Elicitation** for interactive learning path selection, with the old
  listing as the fallback for clients without the capability
- [x] **Structured tool outputs** alongside TOON text for the five tabular
  tools, with real output schemas
- [x] **OAuth 2.1** resource-server support for the HTTP transport (JWKS or
  static tokens; issuer+audience mandatory)

### MCP Registry Publishing
- [x] Publish workflow for the official MCP Registry (GitHub OIDC, fires on
  the next `v*` tag)
- [x] `.well-known/mcp/server.json` endpoint for server identity in HTTP mode
- [x] Self-publishing metadata (`server.json`, schema-validated) and
  version-guarded

The Documentation Improvements bullets originally sketched for this slot
(advanced search, version filtering, ecosystem mapping) moved to v0.13.0:
they are retrieval work, unrelated to the protocol modernization, and the
retrieval overhaul in v0.11.0 already delivered the highest-value part.

---

## ✅ v0.13.0 - Production Readiness (COMPLETED)
**Released: Q3 2026 — originally targeted Q2 2027**

### Documentation Improvements (moved from v0.12.0)
- [x] Advanced search across all aggregated sources *(unified fan-out with
  source labels and a `sources` filter; recursive enumeration surfaced the
  121 nested service files and all Spatie docs search had never seen)*
- [x] Version-specific documentation filtering improvements *(version scopes
  core only, stated honestly; non-core corpora are not Laravel-versioned)*
- [x] Package ecosystem documentation mapping *(all 22 catalog links resolve
  and are guard-tested; laravel-package:// resource scheme added)*

### Reliability & Monitoring
- [x] Health monitoring and metrics endpoints *(/healthz + Prometheus /metrics, HTTP mode)*
- [x] Rate limiting *(opt-in global token bucket via `--rate-limit`; quota
  management deliberately out of scope — no per-client identity without auth)*
- [x] Error recovery and graceful degradation *(accumulated and now pinned by
  tests: partial update results, discovery fallback, fail-closed caches and
  token verification, corrupt-corpus search resilience, staleness advice)*
- [x] Performance optimization and caching improvements *(delivered in v0.10.0)*

### Security & Stability
- [x] Security audit and hardening *(v0.10.0, extended in v0.11.0)*
- [x] Input validation improvements *(v0.10.0, completed in v0.11.0)*
- [x] Dependency security scanning *(CodeQL and Dependabot)*
- [x] Authentication for the HTTP transport *(v0.12.0: OAuth 2.1 resource
  server — JWKS or static tokens)*

### Quality Assurance
- [x] 80%+ coverage of product code *(81% as of the v0.13.0 coverage push; gate ratcheted to 80)*
- [x] Integration tests through a real MCP client *(e2e suite over stdio and HTTP; also a v1.0.0 criterion)*
- [x] Latency benchmarks *(report-only `pytest -m bench` against the real
  corpus; warm search p95 ~4ms against the v1.0.0 100ms target)*
- [x] Documentation completeness audit *(claims-vs-reality sweep; notes in
  docs/superpowers/specs/2026-08-03-claims-audit-notes.md)*

---

## ✅ v0.14.0 - Sync Reliability (COMPLETED)
**Released: Q4 2026 — unplanned; it came out of an audit of the nightly docs sync**

- [x] Laravel service docs (Forge, Vapor, Nova, Envoyer) read from each site's `llms.txt` index
- [x] Filament docs follow the current major from the site's index
- [x] Community package docs refresh again (cache age no longer read from file mtime)
- [x] Laravel Learn courses replace the retired Bootcamp site; Laracasts topic index restored
- [x] Per-source sync health report, gating the nightly pipeline
- [x] CI running again and required on `main`; failure notifications on the docs and release pipelines

---

## ✅ v0.15.0 - The surface for 1.0 (COMPLETED)
**Released: Q4 2026. The one deliberately breaking release before 1.0; see [MIGRATING.md](MIGRATING.md)**

- [x] 26 tools consolidated to 12, each with an output schema and structured content
- [x] Structured errors with codes; finding nothing is no longer an error
- [x] The surface recorded in `tests/protocol/contract.json` and enforced by a test
- [x] One ranking across corpora, so the framework's own page is not crowded out by package docs
- [x] Curated tables refreshed (catalog 22 to 42 entries, legacy flags) and audited in CI
- [x] Laravel Cloud, Nightwatch and Herd added; Spatie and Livewire follow their current majors
- [x] Installable as a Python package with the documentation in the wheel
- [x] `:latest` carries released code only; the image installs from the lockfile and runs unprivileged
- [x] API reference generated from the server; versioning policy and release checklist written

---

## v1.0.0 - First Stable Release
**Timing: when the conditions below hold, not on a date**

1.0.0 freezes the surface that 0.15 introduced. No features are planned between the two.

### Conditions
The full list is in [RELEASING.md](RELEASING.md#conditions-for-tagging-100). In short:

- [ ] 0.15 has been in use and nothing in the recorded contract needs to change
- [ ] The nightly sync has run green for 14 consecutive nights, every source healthy
- [ ] `docker run` works on amd64 and arm64, and `pip install` works from PyPI
- [ ] The failure email and the stale-sync alarm have each been seen to fire
- [ ] The support window in [VERSIONING.md](VERSIONING.md) is confirmed

### Not yet done
- [ ] Publish to PyPI (needs a one-time trusted-publisher setup) and list the PyPI package in the MCP Registry entry
- [ ] A release candidate, `v1.0.0-rc1`, while the fourteen nights run
- [ ] Pest's own documentation as a source (its site publishes an index; the fetcher reads a different index format)
- [ ] A persistent, user-writable location for documentation updates on a `pip` install
- [ ] An evaluation set for search ranking; today it is checked against a handful of queries

---

## What We're NOT Building

To maintain focus and deliver quality, we've explicitly decided against:

- **VS Code extension** - MCP clients handle this natively
- **Standalone CLI tool** - Use any MCP-compatible client
- **Web interface** - Not the MCP pattern
- **Mobile app** - Wrong direction for developer tooling
- **ML-based topic clustering** - Overkill for our use case
- **Real-time documentation change tracking** - Complex, low ROI
- **Code generation or project-aware context** - That's what [laravel/boost](https://github.com/laravel/boost) does
- **Embeddings or semantic search** - Ranked keyword search over sections answers the questions asked of it, with nothing to host
- **Original learning content** - The project organises other people's documentation; it does not write tutorials
- **Per-client rate limiting** - There is no client identity without authentication

---

## Version History

### ✅ v0.8.0 - Community Learning Resources (Phase 1)
**Released: Q4 2024 / Q1 2025**
- Use case → documentation mapping system
- Package combination integration guides
- Cross-package compatibility documentation
- 42,000+ lines of aggregated package documentation

### ✅ v0.7.0 - Community Package Documentation
**Released: Q4 2024**
- Spatie, Livewire, Inertia.js, Filament documentation
- CommunityPackageFetcher with modular architecture
- Markdownify integration for HTML conversion

### ✅ v0.6.0 - Test Coverage & Quality
**Released: Q3 2024**
- Test coverage from 34% to 84%
- Refactored testable architecture
- Asset filtering for documentation quality

### ✅ v0.5.0 - Laravel Ecosystem Documentation
**Released: Q2 2024**
- Auto-Discovery Engine for Laravel services
- Forge, Vapor, Envoyer, Nova documentation
- 117+ sections via intelligent discovery

---

## Contributing to the Roadmap

We welcome community input! If you have ideas, feature requests, or want to contribute:

1. **Open an Issue**: Propose new features or improvements
2. **Join Discussions**: Participate in roadmap planning
3. **Submit PRs**: Help implement features from this roadmap
4. **Share Feedback**: Let us know how you use the MCP server

## Versioning

[VERSIONING.md](VERSIONING.md) says what a version number promises: what is covered from 1.0.0,
what is not, and how deprecation works. Until 1.0.0, a minor release may contain breaking changes,
and the changelog says so.
