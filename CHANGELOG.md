# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
this project follows [Semantic Versioning](https://semver.org). While on `0.x` the
public API is not yet stable, so **breaking changes ship in minor releases** and are
always called out below.

Releases before v0.10.0 predate this file; see the
[GitHub releases page](https://github.com/brianirish/laravel-mcp-companion/releases)
for their notes. Documentation-sync snapshots are tagged `docs-YYYY-MM-DD` and are
not releases — they do not appear here.

`v0.10.1` is absent deliberately: it was cut by the documentation cron shortly
before that pipeline stopped consuming semantic versions. It points at a
docs-only commit and contains no code change.

## [Unreleased]

### Breaking
- `search_laravel_docs` returns ranked documentation *sections* with snippets and
  anchors, rather than files with match counts, and
  `search_laravel_docs_with_context` is removed. Both matched the query as a
  literal substring, so four of seven realistic developer questions returned
  nothing at all; ranking by raw match count also placed `queues.md` 13th of 24
  for "queues", behind a file with a single match. An exact-symbol query such as
  `queue:retry` still works, via a substring fallback.
- `update_laravel_docs` takes `version` rather than `version_param`. Every other
  tool takes `version`, so an assistant following the server's own advice
  guessed it and received a hard error; the name being broken is one that never
  worked.

### Added
- `read_laravel_doc_section` reads one section by anchor or heading, as returned
  by search. Answering "how do I retry a failed queue job" end to end now costs
  about 3,200 tokens against roughly 34,000 for the whole-file path — `queues.md`
  alone is 34,048 tokens, and a quarter of the files exceed 10,000.
- The server now reports the date Laravel last changed the documentation it
  serves. MCP server instructions carry that date for the version being served,
  so an assistant asked about a feature added after it says so rather than
  answering as if the documentation covered it. `laravel_docs_info` reports
  `documentation_date` per version, and `documentation_current_to` /
  `copy_age_days` for the copy as a whole.

  This reads `commit_date` rather than the time of the last fetch. The two
  diverge for a branch Laravel no longer changes: the fetch time recedes
  forever, so five of eight shipped versions were being called stale while
  byte-identical to upstream, with a warning no tool could clear. The staleness
  warning now fires only when *no* version has changed in over 30 days, which
  means the copy itself is behind rather than upstream being quiet, and it
  advises pulling a newer image instead of running a tool that cannot help.
- Tests asserting the project version matches the newest release tag, and stays
  consistent across `pyproject.toml`, `ROADMAP.md`, and `README.md`. The tag
  comparison is the one that matters: during the drift that motivated these
  guards, all three files agreed with each other and only the tags disagreed.
- Tests asserting pytest and coverage are each configured in exactly one place.

### Changed
- Documentation syncs are tagged `docs-YYYY-MM-DD` instead of incrementing the
  patch version, and no longer publish a GitHub Release. Version numbers now
  describe the software rather than counting days of content refreshes.
- Coverage is measured against the product modules only, with branch coverage
  enabled in one place, so a bare `pytest` and CI report the same figure. The
  previous CI invocation also measured the test suite, inflating the reported
  number well above actual product coverage.
- CI installs Python 3.12 rather than inheriting the runner image's 3.10. The
  project declares `requires-python = ">=3.12"`, so the only pipeline that runs
  had never validated a supported interpreter. The daily documentation job now
  does the same, and installs from `requirements.txt` instead of a hand-listed
  set that had drifted from it.

### Fixed
- Removed a Harness cache configuration that failed on every run — it supplied
  no cache key, which the plugin requires for custom paths — leaving the test
  stage permanently degraded and masking the status of the steps that matter.

## [0.10.0] - 2026-07-30

### Breaking
- `tools/list` now returns a search-first surface (`search_tools`, `call_tool`,
  plus a pinned `search_laravel_docs`) rather than all 26 tools. Use
  `--transform-mode none` to restore the previous listing.
- The HTTP transport binds `127.0.0.1` instead of `0.0.0.0`, validates `Host`
  and `Origin` headers, and sends no CORS headers unless `--cors-origin` is
  given. Docker is unaffected. Non-loopback binds now require `--allowed-host`.
- Documentation search covers the configured Laravel version rather than all
  supported versions; pass `all_versions: true` for the previous behavior.
- Unsupported `version` arguments are rejected with an explicit error instead of
  falling through to a filesystem lookup.

### Security
- Fixed arbitrary `.md` file read via an unvalidated `version` argument, which
  was joined onto the documentation path while the containment check derived its
  base from that same untrusted value.
- Replaced two independently broken path containment checks — one using
  `Path.absolute()`, which does not resolve `..`, and one using a string prefix
  comparison that treated `12.x-backup` as inside `12.x`.
- Fixed unauthenticated network exposure: wildcard CORS origins combined with
  credentials caused arbitrary origins to be reflected back as trusted.
- Fixed arbitrary `.md` overwrite from a hostile upstream, where section names
  scraped from remote HTML were used directly as file paths.
- Validated learning-resource `source` parameters and updater versions that
  previously allowed directory enumeration and out-of-tree directory creation.

### Added
- `--transform-mode {search,code,none}` selecting the tool exposure strategy,
  including experimental Code Mode with sandboxed Python execution.
- `--cors-origin` and `--allowed-host` for explicit HTTP allowlists.

### Fixed
- Documentation is no longer served stale after an update; the update tools
  cleared only one of two caches.
- Package recommendations now account for name and description matches, which a
  scoring expression had been discarding.

### Changed
- FastMCP floor raised to 3.4.5 and Starlette to 1.3.1.
- Startup reads the supported-version list from cache with a 24-hour TTL, and
  all network calls have timeouts.

[Unreleased]: https://github.com/brianirish/laravel-mcp-companion/compare/v0.10.0...HEAD
[0.10.0]: https://github.com/brianirish/laravel-mcp-companion/compare/v0.9.145...v0.10.0
