# Laravel MCP Companion - Roadmap

This roadmap outlines the planned development path toward v1.0.0.

## Mission Statement

**Laravel MCP Companion** is a documentation aggregator and navigator designed specifically for **junior and intermediate Laravel developers**. We centralize and organize existing high-quality documentation from across the Laravel ecosystem, making it easily discoverable through MCP.

**We complement, not compete with, official Laravel tools.** Laravel's [Boost](https://github.com/laravel/boost) focuses on code generation context for active development. We focus on documentation navigation, learning paths, and reference material.

---

## Current Version: v0.11.0

### ✅ Completed Features
- **Multi-version Laravel documentation** support (6.x through latest)
- **Auto-Discovery System**: Automatically discovers Laravel service documentation (117+ sections)
- **Community Package Documentation**: Spatie, Livewire, Inertia.js, Filament integration (42,000+ lines)
- **Learning Resource Infrastructure**: Difficulty classification, 15 semantic categories
- **8 New MCP Tools**: Learning paths, "I need X" finder, category browsing, difficulty filtering
- **Package recommendation system** with 50+ curated packages
- **Ranked section search** with BM25 relevance, snippets, and section-level reads
- **Documentation currency reporting** so the assistant knows what date its corpus covers
- **Future-proof version detection** via GitHub API
- **Automated daily documentation updates** with auto-discovery metrics
- **Test suite** at 67% coverage of product code (branch coverage, tests excluded)

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

## v0.12.0 - MCP Modernization
**Target: Q1 2027 — implemented ahead of schedule, ships as the next release**

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

## v0.13.0 - Production Readiness
**Target: Q2 2027**

### Documentation Improvements (moved from v0.12.0)
- [ ] Advanced search across all aggregated sources
- [ ] Version-specific documentation filtering improvements
- [ ] Package ecosystem documentation mapping

### Reliability & Monitoring
- [ ] Health monitoring and metrics endpoints
- [ ] Rate limiting and quota management
- [ ] Error recovery and graceful degradation improvements
- [x] Performance optimization and caching improvements *(delivered in v0.10.0)*

### Security & Stability
- [x] Security audit and hardening *(v0.10.0, extended in v0.11.0)*
- [x] Input validation improvements *(v0.10.0, completed in v0.11.0)*
- [x] Dependency security scanning *(CodeQL and Dependabot)*
- [ ] Authentication for the HTTP transport

### Quality Assurance
- [ ] 80%+ coverage of product code, from 67% today
- [ ] Load testing and performance benchmarks
- [ ] Documentation completeness audit

---

## v1.0.0 - First Stable Release
**Target: Q3 2027**

### Stability Commitments
- [ ] Feature freeze and API stability
- [ ] Breaking change policy documentation
- [ ] LTS commitment (minimum 12 months support)
- [ ] Semantic versioning guarantee

### Documentation & Support
- [ ] Comprehensive user documentation
- [ ] API reference and examples
- [ ] Troubleshooting guides
- [ ] Migration guides for future versions

### Success Criteria
- Documentation coverage for 95% of common Laravel development scenarios
- Sub-100ms response times for documentation queries
- 80%+ coverage of product code, with integration tests through a real MCP client
- MCP Registry listing with verified status
- Active community of users and contributors

---

## What We're NOT Building

To maintain focus and deliver quality, we've explicitly decided against:

- **VS Code extension** - MCP clients handle this natively
- **Standalone CLI tool** - Use any MCP-compatible client
- **Web interface** - Not the MCP pattern
- **Mobile app** - Wrong direction for developer tooling
- **ML-based topic clustering** - Overkill for our use case
- **Real-time documentation change tracking** - Complex, low ROI
- **Code generation** - That's what [laravel/boost](https://github.com/laravel/boost) does

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

## Versioning Strategy

We follow [Semantic Versioning](https://semver.org). While the project is on
`0.x`, the public API is not yet stable and the **minor** version carries
breaking changes:

- **Patch releases (v0.x.y)**: Bug fixes, documentation updates
- **Minor releases (v0.x.0)**: New features, and breaking changes where needed,
  called out in the release notes
- **v1.0.0 onward**: Breaking changes only in major releases, with migration guides

Backward compatibility is guaranteed within a major version starting at v1.0.0.
