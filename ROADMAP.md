# Laravel MCP Companion - Roadmap

This roadmap outlines the planned development path toward v1.0.0.

## Mission Statement

**Laravel MCP Companion** is a documentation aggregator and navigator designed specifically for **junior and intermediate Laravel developers**. We centralize and organize existing high-quality documentation from across the Laravel ecosystem, making it easily discoverable through MCP.

**We complement, not compete with, official Laravel tools.** Laravel's [Boost](https://github.com/laravel/boost) focuses on code generation context for active development. We focus on documentation navigation, learning paths, and reference material.

---

## Current Version: v0.10.0

### ✅ Completed Features
- **Multi-version Laravel documentation** support (6.x through latest)
- **Auto-Discovery System**: Automatically discovers Laravel service documentation (117+ sections)
- **Community Package Documentation**: Spatie, Livewire, Inertia.js, Filament integration (42,000+ lines)
- **Learning Resource Infrastructure**: Difficulty classification, 15 semantic categories
- **8 New MCP Tools**: Learning paths, "I need X" finder, category browsing, difficulty filtering
- **Package recommendation system** with 50+ curated packages
- **Context-aware search** with surrounding text snippets
- **Future-proof version detection** via GitHub API
- **Automated daily documentation updates** with auto-discovery metrics
- **Comprehensive test suite** with 85%+ code coverage

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

Pulled forward from v0.12.0 after an audit found exploitable path traversal in
tool arguments. Contains breaking changes — see the release notes before upgrading.

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

## v0.11.0 - MCP Modernization
**Target: Q4 2026**

### MCP 2025-11-25 Spec Compatibility
- [ ] **Tasks primitive** for async documentation updates and background indexing
- [ ] **Elicitation** for interactive learning path customization
- [ ] **Structured tool outputs** for better response formatting
- [ ] **OAuth 2.1** support for remote HTTP transport

### MCP Registry Publishing
- [ ] Publish to official MCP Registry for discoverability
- [ ] `.well-known` URL support for server identity
- [ ] Self-publishing metadata and versioning

### Documentation Improvements
- [ ] Advanced search across all aggregated sources
- [ ] Version-specific documentation filtering improvements
- [ ] Package ecosystem documentation mapping

---

## v0.12.0 - Production Readiness
**Target: Q1 2027**

### Reliability & Monitoring
- [ ] Health monitoring and metrics endpoints
- [ ] Rate limiting and quota management
- [ ] Error recovery and graceful degradation improvements
- [x] Performance optimization and caching improvements *(delivered in v0.10.0)*

### Security & Stability
- [x] Security audit and hardening *(delivered in v0.10.0)*
- [x] Input validation improvements *(delivered in v0.10.0)*
- [ ] Authentication for the HTTP transport
- [ ] Dependency security scanning

### Quality Assurance
- [ ] 90%+ test coverage target
- [ ] Load testing and performance benchmarks
- [ ] Documentation completeness audit

---

## v1.0.0 - First Stable Release
**Target: Q2 2027**

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
- 85%+ test coverage with comprehensive integration tests
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
