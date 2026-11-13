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

### Added
- Documentation for **Laravel Cloud, Nightwatch and Herd**. Each publishes an
  `llms.txt` index, so each is one entry in the service table. Herd's macOS
  and Windows guides are kept under separate paths. Cloud is read from the
  site's single-file export (`llms-full.txt`) in two requests: fetching its
  pages one at a time gets the client blocked by laravel.com, which also hosts
  Forge and Laravel Learn. Cloud's API reference, about 130 pages of OpenAPI
  YAML, is not included.
- **Spatie and Livewire follow the site's current major and page list.** Both
  were hand-kept lists against pinned or unversioned URLs. Laravel Permission
  was two majors behind (v6; the site is on v8) and Livewire had 36 of the 80
  pages Livewire 4 lists. The pinned lists remain as the fallback for a night
  when a site's navigation cannot be read.
- A scheduled GitHub workflow that opens an issue when the newest
  `docs-YYYY-MM-DD` tag is more than four days old. It catches a sync that has
  stopped starting, which no failure email can.
- The project is an installable Python package. `uvx --from
  git+https://github.com/brianirish/laravel-mcp-companion laravel-mcp-companion`
  and `pip install git+...` both work, with the documentation bundled in the
  wheel so no download is needed on first run. Two console scripts are
  installed: `laravel-mcp-companion` and `laravel-mcp-companion-docs`. A
  manual workflow for publishing to PyPI is included; publishing needs a
  one-time PyPI setup first.
- A container `HEALTHCHECK`. Over HTTP it asks the server's `/healthz`; over
  stdio it passes, since there is no port to ask.

### Changed
- **Breaking for anyone running from a clone:** the modules moved into a
  `laravel_mcp_companion/` package. `python laravel_mcp_companion.py` is now
  `python -m laravel_mcp_companion`, and `python docs_updater.py` is
  `python -m laravel_mcp_companion.docs_updater`. Docker users are unaffected.
- `toon-format` comes from PyPI (1.2.0) instead of a pinned git commit of its
  0.9 beta. Three details of the text output change with it: an empty list is
  written `key: []` rather than `key[0]:`, a whole float loses its `.0`
  (`score: 3`), and a string starting with `#` is quoted. Structured content
  is unchanged.
- The server version is written in one place, `pyproject.toml`. The
  `SERVER_VERSION` constant is read from it.
- **Breaking for Docker volumes:** the image runs as an unprivileged user (uid
  10001) instead of root. A named volume mounted at `/app/docs` that an earlier
  image created is owned by root, so `--update-docs` can no longer write to it.
  Remove the volume and let the next run recreate it.
- `:latest` no longer carries unreleased code. The nightly image was built from
  `main` as it stood at the documentation sync, so anything merged since the
  last release shipped to `latest` the same night. It is now the newest
  release's code with that night's documentation. Release candidates and
  patches to an older line no longer move `latest` either.
- The image installs the versions pinned in `uv.lock`. It installed from
  `requirements.txt`, six direct dependencies with open ranges, so two builds of
  one tag could differ in every transitive dependency. CI and the documentation
  pipeline install from the same lockfile. `requirements.txt` and
  `requirements-dev.txt` are removed; `uv sync` replaces them.
- The image is built in two stages, so the compiler toolchain and git are no
  longer in it.

### Internal
- Importing the server no longer contacts GitHub. Version discovery used to run
  at import whenever the versions cache had expired, and rewrote the checked-in
  cache file as a side effect. The import now reads the cache only; the server
  and `docs_updater.py` refresh the list once at startup, and keep the cached
  list if GitHub is unreachable.
- Path containment and the symlink-refusing file open live in one module,
  `path_security.py`, used by both the server and the updater. The server's
  duplicate cache, version parser and metadata reader are gone in favour of the
  ones in `mcp_tools`.
- The coverage gate measures every product module. It left out `doc_search`,
  `metrics`, `tool_schemas` and `path_security`; with them included coverage is
  85%.
- The Docker image no longer contains repository metadata, caches or test
  directories; `.dockerignore` now excludes them.

### Fixed
- `docs_updater --update` exits 0 when the framework docs were already
  current. It treated "nothing changed" as a failure. A framework update that
  does fail no longer stops the services and packages from being updated.
- A `429 Too Many Requests` from a documentation site is retried after the
  pause it asks for, or a growing backoff. It was raised at once, like a 404.
- Spatie, Livewire and Debugbar pages that a site has dropped are removed
  after a complete sync.
- The advertisement at the top of every Livewire docs page is no longer saved.
- `laravel://` resource reads go through the same symlink-refusing open as the
  tools. They used a second file cache that checked a path and then opened it
  in two steps.
- Two servers created in one process no longer share configuration. A module
  global held it, so creating a second server repointed the first one's
  resource handlers.

### Removed
- **The Laravel Blog and Laravel News sources.** Each was a list of a few
  article titles with links, refetched nightly. They held no documentation,
  and a changed headline was enough to publish a new image. Search and reads
  against `laravel-blog` and `laravel-news` return nothing now.
- The unused JSX-to-markdown converter in the updater.
- Dead server-side code: the unused search and learning-resource formatters,
  the `search_laravel_docs_impl` wrapper that no client could reach, and the
  "requires server context" stubs.

### Security
- `joserfc` 1.7.4 to 1.8.0 in `uv.lock`. It is a dependency of FastMCP and
  Authlib, not of this project directly. The upgrade closes two
  denial-of-service advisories: GHSA-jpxq-7h8p-2q76 (unbounded `recipients` in
  JWE General JSON) and GHSA-9pg5-8c7x-5hfx (compact JWS segments allocated
  before the size check). The lockfile covers local development only. CI and
  the Docker image install from `requirements.txt`, which does not pin
  `joserfc`, so each image build resolves it afresh.

## [0.14.0] - 2026-11-12

An audit of the nightly documentation sync, and the repairs that came out of
it. Most sources other than the Laravel framework docs had been stale or
failing without any signal, and CI itself had not run since 2026-08-04.

### Added
- The docs and release pipelines email the Harness "Pipeline Alerts" user
  group when a run fails.
- `docs_updater.py --sync-report` prints a per-source health report and exits
  non-zero when a source fetched too little, has not synced recently, or has
  never been saved. The daily sync puts it in the pull request body and fails
  on it, after publishing whatever did sync.

### Changed
- **Forge, Vapor, Nova and Envoyer are read from each site's `llms.txt` index,
  as markdown.** The per-site link discovery and HTML scraping are gone, with
  their hand-kept fallback page lists. Envoyer, whose pages were never
  discovered, now is; Forge gains the knowledge base and API reference pages
  its navigation did not link; Nova follows the newest major in its index.
  Page paths, and so `laravel-external://` URIs, are unchanged for pages that
  still exist. Saved pages now open with a `Source:` line rather than a
  generated `# Service - Section` heading.
- Unified search ranks a core hit as if it scored 5% higher, so the
  framework's own page wins a near-tie against a package or service page. With
  Filament's larger docs, "how do I retry a failed queue job" otherwise led
  with a Filament import-job page (30.04) over "Dealing With Failed Jobs"
  (29.52). A non-core hit with a real lead still ranks first, and reported
  scores are unchanged.
- The nightly sync refetches every source on every run. The fetchers' 24-hour
  cache lined up with the 24-hour schedule, so sources were skipped on
  alternate nights.
- CI no longer runs on tag pushes, which re-tested the commit `main` had just
  tested and spent build credits doing it.
- **Breaking: Filament docs track the current major automatically, and their
  file names change.** They are discovered
  from the site's `llms.txt` index instead of a hand-listed set of pages under
  a pinned `3.x`, which was two majors behind with seven dead pages. Filenames
  now follow the page path (`forms-text-input.md`), so `laravel-package://`
  URIs for the `3.x` files (`panels-*.md`, `forms-fields-*.md`) no longer
  resolve.
- **Breaking: the `laravel-bootcamp` learning source now holds the courses at
  laravel.com/learn, under new file names.** `bootcamp.laravel.com` was folded into that site and no
  longer resolves; the eight saved "bootcamp" pages were all copies of its
  landing page. Courses and lessons are discovered from the site, lessons are
  saved as `<course>-<lesson>.md` with their code samples, and the source key
  is unchanged.

### Fixed
- `docs_updater.py --all-versions` exits 0 when every version is already up to
  date. It exited 1 whenever any version had nothing to update, which the docs
  pipeline read as a failed framework update.
- Stripping image references no longer removes every blank line. Pages fetched
  as markdown (Inertia, Filament) were saved with their paragraphs run together.
- Spatie, Livewire and Debugbar record how many pages they wanted as well as
  how many they fetched, so the sync report can flag a mostly failed fetch.
- The Laracasts topic index is fetched from `laracasts.com/series`;
  `/topics` had become a 404, so the index had never been saved.
- Forge docs follow the move to `laravel.com/forge/docs`. Discovery had
  matched nothing since the move and the fallback list 404'd on 21 of 39
  sections, so 64 of the 82 Forge files in the repository were stale.
- Community package docs were never refreshed by the daily sync: cache age was
  read from file mtime, which a fresh clone resets. Livewire, Filament,
  Inertia, Debugbar and IDE Helper had sat at their 2025-07-30 snapshot.
- The Inertia fetcher saved v1, v2 and v3 pages under the same filenames, with
  v1 winning. Only the newest version in the index is fetched.
- Saved service docs no longer include non-pages (`llms.txt`, `sitemap.xml`,
  the `.md` twin of each page, `#anchor` files) or the sites' feedback widget,
  and a complete sync removes pages that have left a site.
- `--force` now refetches service docs whose cache is still valid.
- The docs pipeline no longer waits on every pull request check. A status
  that never completed hung each run until the stage timed out, so no docs
  tag or Docker image was published from 2026-09-19 to 2026-10-31.
- The docs pipeline opens a pull request only when documentation content
  changed, not for cache timestamps alone, and describes the change in it.
- CI runs again. Two step names Harness rejects had stopped every CI
  execution since 2026-08-04; a test now checks step names against its rule.

## [0.13.0] - 2026-08-03

### Added
- Unified search: `search_laravel_docs` now fans out over every aggregated
  corpus — core versions, service docs, fetched package docs, learning
  resources — with a `sources` filter and a per-hit `source` label.
  `include_external=False` keeps its historical core-only meaning; `version`
  scopes core only, since nothing else is Laravel-versioned.
- `laravel-package://{package}/{path}` resource scheme for fetched package
  documentation, mirroring `laravel-external://`.
- The Inertia fetcher discovers pages from the site's `llms.txt` markdown
  index — the configured JSX source repo was deleted upstream, so every
  daily sync had been silently failing that ecosystem. The Laracasts topic
  extractor now parses the page's SPA payload, which had been yielding zero
  topics.

### Fixed
- Search had never seen most of the corpus it advertised: enumeration was
  single-level, hiding 121 of 147 service files and every Spatie file in
  nested directories, and packages/learning resources were not indexed at
  all. The search→read flow was also broken for service hits since v0.11.0;
  corpus-prefixed files now resolve uniformly with the same containment
  rules.
- 19 of the 22 package-catalog documentation links pointed at paths that
  never existed; all now resolve and are guard-tested. The README's "50+
  curated packages" claim is corrected to the actual 22 and tied to the
  catalog by a test, and the search tool description no longer advertises
  the substring contract removed in v0.11.0.
- Opt-in rate limiting for the HTTP transport's MCP surface (operational
  endpoints stay unlimited — throttling health checks marks healthy
  instances down): `--rate-limit RPS` /
  `RATE_LIMIT_RPS` with a burst knob defaulting to `max(10, 2×RPS)` — the
  limiter counts the MCP handshake against the bucket, so small bursts
  self-throttle. One global token bucket, documented as a throughput cap
  rather than per-client fairness. Off unless configured.
- Report-only latency benchmarks (`pytest -m bench`) against the real
  corpus, printing p50/p95 per operation against the v1.0.0 sub-100ms
  target. First measurements: warm search p95 ~4ms, section reads ~1.4ms.
- Tests pinning graceful-degradation behavior that previously rested on
  luck: search surviving hostile bytes in a corpus file, and throttled
  clients recovering cleanly when the bucket refills.
- Operational endpoints for the HTTP transport: `GET /healthz` (public
  liveness/readiness JSON — `degraded` flags a stale corpus at 200, 503 is
  reserved for no readable documentation) and `GET /metrics` (Prometheus
  text: per-tool call counters, a latency histogram, request counts, uptime,
  documentation age). Metrics require a bearer token whenever auth is
  configured; collection runs through FastMCP middleware with no per-tool
  code changes and no new dependencies.
- End-to-end tests that spawn the real server over stdio and HTTP —
  initialize, search-to-section flows, `.well-known` discovery, Host
  rejection, and bearer auth, all through real transports (`pytest -m e2e`).
  Product coverage rose from 68% to 81% and the CI gate ratcheted to 80.

### Security
- CORS origins reject fnmatch patterns (`*`, `?`, `[`) at startup, the same
  rule `ALLOWED_HOSTS` has enforced since v0.11.0 and for the same reason:
  FastMCP's origin guard pattern-matches its allowlist, so
  `https://*.example.com` admitted any matching `Origin` through the
  DNS-rebinding protection while presenting as a scoped allowlist. Previously
  only a bare `*` was rejected, and only when it was the sole entry.

### Fixed
- The external-services documentation cache never validated after a real
  fetch: no fetch path stamped `cached_at`, so the cache aged from the epoch
  and every request refetched. GitHub-archive fetches additionally wrote no
  `success_rate`, reading back as zero quality — same permanent invalidation.
- An explicit `--port 0` now binds an ephemeral port instead of being
  silently rewritten to 8081.

## [0.12.0] - 2026-07-31

### Added
- The two documentation-update tools run as MCP *tasks* (SEP-1686,
  experimental in spec 2025-11-25): task-aware clients submit and poll instead
  of holding the connection open for up to five minutes. Sync clients keep the
  old behavior — task support is declared "optional". Their blocking bodies
  also moved off the event loop, fixing a live starvation bug where one update
  froze every other connected HTTP client for its full duration.
- `get_laravel_learning_path` called without a path now asks the client which
  of the ten curated paths to fetch, via elicitation with titled options.
  Decline, cancel, and clients without the capability get the old listing.
- The five tabular tools (`search_laravel_docs`, `laravel_docs_info`,
  `list_laravel_docs`, `get_laravel_package_recommendations`,
  `get_laravel_package_info`) return `structuredContent` alongside their TOON
  text and declare real output schemas, replacing FastMCP's auto-wrapped
  `{"result": "<string>"}` shape. The search transform's `call_tool` proxy
  forwards structured content, so both transform modes benefit.
- OAuth 2.1 bearer-token validation for the HTTP transport, as a resource
  server: `--auth-jwks-uri` / `--auth-issuer` / `--auth-audience` /
  `--auth-required-scope` (env: `AUTH_JWKS_URI`, `AUTH_ISSUER`,
  `AUTH_AUDIENCE`, `AUTH_REQUIRED_SCOPES`) against a real authorization
  server, or `AUTH_STATIC_TOKENS` (env only) for development. Issuer and
  audience are mandatory in JWKS mode; misconfiguration fails at startup.
  Without configuration nothing changes.
- MCP Registry metadata: `server.json` (validated against the 2025-12-11
  registry schema), the `io.modelcontextprotocol.server.name` OCI label the
  registry uses to verify image ownership, and a GitHub Actions workflow that
  publishes to the registry on `v*` tags via OIDC. HTTP deployments serve the
  metadata at `/.well-known/mcp/server.json` with the running version stamped
  in.
- The server identifies itself at initialize: version (guarded against
  pyproject drift), website URL, and an embedded SVG icon (SEP-973).

### Changed
- The all-versions `list_laravel_docs` payload is wrapped as
  `{count, versions}` instead of a bare list, because structured content must
  be a JSON object. Single-version output is unchanged.

### Removed
- `package.json`, vestigial npm metadata frozen at 0.8.0 that nothing
  consumed. Registry metadata lives in `server.json`.

## [0.11.0] - 2026-07-31

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

### Security
- `laravel_docs_info` never validated its `version` argument. v0.10.0 claimed the
  validator ran "in every tool implementation"; it was called exactly once. The
  value was joined onto the documentation path, giving a read of any
  `<dir>/.metadata/sync_info.json` on the filesystem plus an existence oracle for
  that path — reachable unauthenticated through the default search transform's
  `call_tool` proxy. Being written inline rather than delegating to an `*_impl`
  is how it escaped the sweep.
- The supported-versions cache is now filtered on read. It is the trust root for
  every version allowlist, and the `\d+\.x` shape was enforced only on the GitHub
  API response — so editing one value in `docs/.versions_cache.json`, a file
  shipped in the image and living in a directory users bind-mount, put arbitrary
  strings into the allowlist and disabled every check downstream.
- Enumeration now applies the same containment rule as reading. A symlink inside
  a version directory pointing out of the tree was denied on read but listed by
  `list_laravel_docs` and match-counted by search, and the context search
  returned the surrounding content outright — an oracle over exactly the material
  the read path withholds.
- Closed a TOCTOU between the containment check and the open. Resolving first was
  necessary but not sufficient: a path that is a regular file when checked
  resolves to itself, so replacing it with a symlink before the open still
  leaked, within two attempts under test. `O_NOFOLLOW` makes the refusal part of
  the open. Verified over 88,820 reads against a thread flipping the file between
  a regular file and a symlink to a planted secret: zero leaks.
- `ALLOWED_HOSTS` rejects wildcards. FastMCP matches allowed hosts with `fnmatch`,
  so a pattern entry matched every `Host` header and silently disabled
  DNS-rebinding protection while still presenting as a configured allowlist.
  Wildcard CORS origins were already rejected; hosts now are too, on both the flag
  and the environment path.

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
- The release pipeline fires on version tags again. Its trigger carried two
  payload conditions, `v*` and `docs-*`, and Harness ANDs them, so no tag could
  ever satisfy both and nothing released. Both triggers are now mirrored into
  `.harness/` so the configuration is reviewable rather than living only in
  clickops.

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

[Unreleased]: https://github.com/brianirish/laravel-mcp-companion/compare/v0.14.0...HEAD
[0.14.0]: https://github.com/brianirish/laravel-mcp-companion/compare/v0.13.0...v0.14.0
[0.13.0]: https://github.com/brianirish/laravel-mcp-companion/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/brianirish/laravel-mcp-companion/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/brianirish/laravel-mcp-companion/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/brianirish/laravel-mcp-companion/compare/v0.9.145...v0.10.0
