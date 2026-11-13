# Laravel MCP Companion

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/brianirish/laravel-mcp-companion)](https://github.com/brianirish/laravel-mcp-companion/releases)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/brianirish/laravel-mcp-companion)](https://github.com/brianirish/laravel-mcp-companion/blob/main/LICENSE)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue)](https://github.com/brianirish/laravel-mcp-companion/pkgs/container/laravel-mcp-companion)
[![GitHub Stars](https://img.shields.io/github/stars/brianirish/laravel-mcp-companion?style=social)](https://github.com/brianirish/laravel-mcp-companion)

**Every Laravel version, the whole ecosystem, fully local.**

Laravel MCP Companion is an [MCP](https://modelcontextprotocol.io) server that keeps Laravel's
documentation on your machine and lets an AI assistant search and read it. It holds the framework
docs for every version from 6.x to the newest, the first-party services, and widely used packages.
Nothing is fetched while you work, so it answers without a network connection.

> **Status:** 0.15 is a breaking release. It makes the tool surface what 1.0 will freeze.
> [MIGRATING.md](MIGRATING.md) lists what changed for anyone upgrading.

## A reference library

Three things set it apart:

- **Every version, side by side.** Laravel 6.x through 13.x are all held. Ask about the version an
  older application runs on, or compare two versions to see what an upgrade brings.
- **Fully local.** The documentation ships inside the image or the Python package. Nothing leaves
  your machine and no vendor API is called, so it works offline and behind an air gap.
- **It needs no project.** It works in a chat client with no code open, where there is no
  `composer.lock` to read.

[Laravel Boost](https://github.com/laravel/boost) is the first-party tool for writing code inside a
Laravel project: it is installed into the application and knows what the application uses. Use Boost
while building. Use Companion to look something up in any Laravel version, in a client with no
project open, or where the documentation has to stay on the machine.

## Documentation held

- **The framework documentation** for Laravel 6.x through 13.x.
- **First-party services:** Forge, Vapor, Envoyer, Nova, Cloud, Nightwatch and Herd.
- **Packages:** Livewire, Filament, Inertia, and Spatie's Permission, Media Library and Backup, each
  at its current major version, plus Debugbar and IDE Helper.
- **Learning material:** the courses at laravel.com/learn and an index of Laracasts topics.
- **A hand-written catalog** of 42 curated packages: what each is for, how to install it, what goes
  with it, and which ones newer projects no longer start with.

A nightly job refreshes all of it. Ask your assistant how current the documentation is, or call
`laravel_docs_info`, to see the date and page count of every source.

## Installation

Listed in the [official MCP Registry](https://registry.modelcontextprotocol.io/?search=laravel-mcp-companion)
as `io.github.brianirish/laravel-mcp-companion` — clients with registry
support can install it from there directly. Manual setup:

### Claude Desktop

1. **Open Claude Desktop Settings**
   - Click Claude menu → Settings → Developer → Edit Config

2. **Add to your configuration file:**
   ```json
   {
     "mcpServers": {
       "laravel-mcp-companion": {
         "command": "docker",
         "args": ["run", "--rm", "-i", "ghcr.io/brianirish/laravel-mcp-companion:latest"]
       }
     }
   }
   ```

3. **Restart Claude Desktop** for changes to take effect

**Config file locations:**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Claude Code

Use the `claude mcp add` command:

```bash
# Add with Docker
claude mcp add laravel-mcp-companion -- docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest

# Or add to project-specific config (for team sharing)
claude mcp add laravel-mcp-companion --scope project -- docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest
```

The `--scope project` option creates a `.mcp.json` file in your project root that can be committed to version control.

### Without Docker

The project is also an ordinary Python package (3.12+), with the documentation
bundled, so it runs without Docker and without a network connection. It is not
on PyPI yet; install it from the repository:

```bash
# Run it without installing anything permanently
uvx --from git+https://github.com/brianirish/laravel-mcp-companion laravel-mcp-companion

# Or install it
pip install git+https://github.com/brianirish/laravel-mcp-companion
laravel-mcp-companion
```

In an MCP client config, use `uvx` as the command and
`["--from", "git+https://github.com/brianirish/laravel-mcp-companion", "laravel-mcp-companion"]`
as the arguments. The options below work the same way. An install carries the
documentation as it was at that commit; `--update-docs` refreshes it in place.

### Configuration Options

These options can be used with the Docker command. For example:

```bash
# Pin to a specific older Laravel version
docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest --version 11.x

# Force update all documentation
docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest --force-update
```

| Option | Description | Default |
|--------|-------------|---------|
| `--version VERSION` | Laravel version (e.g., "11.x", "12.x") | Latest |
| `--docs-path PATH` | Documentation directory | `./docs` |
| `--log-level LEVEL` | DEBUG, INFO, WARNING, ERROR, CRITICAL | INFO |
| `--update-docs` | Update documentation on startup | false |
| `--force-update` | Force documentation update | false |
| `--transform-mode MODE` | Tool exposure mode: `search`, `code`, or `none` (env: `TRANSFORM_MODE`) | search |
| `--host HOST` | Interface to bind in HTTP mode (env: `HOST`) | `127.0.0.1` (`0.0.0.0` in Docker) |
| `--cors-origin ORIGIN` | Browser origin allowed to call the HTTP transport, repeatable (env: `CORS_ORIGINS`) | none (CORS off) |
| `--allowed-host HOST` | Additional `Host` header accepted in HTTP mode, repeatable (env: `ALLOWED_HOSTS`) | `localhost`, `127.0.0.1`, `::1` |
| `--auth-jwks-uri URI` | JWKS endpoint enabling bearer-token auth in HTTP mode (env: `AUTH_JWKS_URI`) | none (auth off) |
| `--auth-issuer ISSUER` | Required token issuer, with `--auth-jwks-uri` (env: `AUTH_ISSUER`) | none |
| `--auth-audience AUD` | Required token audience, with `--auth-jwks-uri` (env: `AUTH_AUDIENCE`) | none |
| `--auth-required-scope SCOPE` | Scope every token must carry, repeatable (env: `AUTH_REQUIRED_SCOPES`) | none |
| `--rate-limit RPS` | MCP requests/second accepted in HTTP mode; operational endpoints are never limited (env: `RATE_LIMIT_RPS`) | none (no limiting) |
| `--rate-limit-burst N` | Token-bucket burst capacity (env: `RATE_LIMIT_BURST`) | `max(10, 2×RPS)` |

### Keeping documentation current

Documentation ships inside the image, and a new image is published whenever the
documentation is refreshed. Which documentation you get depends on the tag:

| Tag | Code | Documentation |
|-----|------|---------------|
| `:latest` | the newest release | refreshed nightly |
| `:v0.15.0` and other version tags | that release | as it was on the release date |
| `:docs-YYYY-MM-DD` | the newest release as of that date (`main`, for tags older than this scheme) | that night's sync |

`:latest` never carries unreleased code: the nightly image is the newest
release with that night's documentation.

The catch is that **`docker run` reuses the copy you already have** —
once you've pulled the image, you keep running it until you pull again. Refresh
whenever you like:

```bash
docker pull ghcr.io/brianirish/laravel-mcp-companion:latest
```

Or add `--pull=always` to your MCP config so every start checks for a newer image.
It costs a moment of startup time and needs a working connection, so it's opt-in
rather than the default:

```jsonc
"args": ["run", "--rm", "-i", "--pull=always",
         "ghcr.io/brianirish/laravel-mcp-companion:latest"]
```

You don't have to track this yourself. The server tells your assistant how old the
documentation is for the Laravel version it's serving, so if you ask about something
newer than that snapshot it will say so and offer to refresh instead of answering
from stale pages. You can also just ask — *"how current are your Laravel docs?"*

To update in place without pulling a new image, `--update-docs` fetches fresh
documentation for the selected Laravel version during startup. Your assistant can
refresh any source while the server runs with the `update_laravel_docs` tool, whose
`scope` selects the framework docs, the services, the packages or all of them.

With `--rm` the download is discarded when the container exits, so it repeats on
every start. A named volume keeps it — but note the trade-off:

```bash
docker run --rm -i -v laravel-mcp-docs:/app/docs \
  ghcr.io/brianirish/laravel-mcp-companion:latest --update-docs
```

The server runs as an unprivileged user (uid 10001), which owns `/app/docs` in
the image, so a new named volume is writable. A volume created by an image
before this change is owned by root: remove it (`docker volume rm
laravel-mcp-docs`) and let the next run recreate it.

> **A volume overrides the image's documentation.** Once populated it masks
> `/app/docs`, so pulling a newer image no longer updates what the server reads —
> the volume becomes your source of truth and `--update-docs` becomes the way you
> refresh it. Use a volume when you want to control updates explicitly; stick to
> plain `docker pull` if you'd rather the image stay in charge.

### Transform Modes

By default the server no longer lists all of its tools. Instead it exposes a compact, search-first interface that keeps your AI client's context window lean:

- **`search`** (default) — Exposes `search_tools` (BM25 relevance search over the tool catalog) and `call_tool` (proxy to invoke any underlying tool). `search_laravel_docs` stays pinned and directly callable.
- **`code`** (experimental) — Exposes Code Mode meta-tools (`tags`, `search`, `get_schema`, `execute`) that let the client discover tools and orchestrate them with sandboxed Python. Requires the `fastmcp[code-mode]` extra (included in `requirements.txt`). Avoid exposing this publicly over HTTP — `execute` is a code execution endpoint.
- **`none`** — Pre-0.9 behavior: every tool listed directly. Use this if your MCP client doesn't handle the synthetic search tools well.

```bash
# Restore the old flat tool listing
docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest --transform-mode none
```

### HTTP transport security

**Authentication is off by default.** Anyone who can reach the HTTP port can call every tool, so treat network exposure as granting full access to the documentation tree — or turn on bearer-token auth:

```bash
# Validate tokens issued by a real OAuth 2.1 authorization server
python -m laravel_mcp_companion --transport http \
  --auth-jwks-uri https://auth.example/.well-known/jwks.json \
  --auth-issuer https://auth.example \
  --auth-audience laravel-mcp-companion

# Development only: fixed tokens from the environment (never a CLI flag,
# so secrets stay out of process listings)
AUTH_STATIC_TOKENS="my-token:my-client" python -m laravel_mcp_companion --transport http
```

The server is a *resource server*: it validates tokens, it never issues them.
Issuer and audience are mandatory with `--auth-jwks-uri` — accepting any
issuer's tokens, or tokens minted for another service, would be authentication
theater. Unauthenticated requests get `401` with a `WWW-Authenticate` header
(RFC 9728), and misconfiguration fails at startup rather than at request time.
Auth applies to the HTTP transport only; stdio's access control is the process
boundary.

Defaults are conservative:

- **Binds `127.0.0.1`** outside Docker. Inside the container it binds `0.0.0.0`, where the container boundary and explicit `-p` publishing are the access control.
- **Host and Origin validation is on**, which blocks DNS-rebinding and drive-by-localhost attacks from a victim's browser.
- **CORS is disabled** unless you pass `--cors-origin`. Wildcard origins are rejected; credentials are never allowed cross-origin.

Only `localhost`, `127.0.0.1`, and `::1` are accepted as `Host` values out of the box. **If you bind a non-loopback interface you must add the hostname clients actually use**, or every request is rejected with `421`:

```bash
python -m laravel_mcp_companion --transport http \
  --host 0.0.0.0 \
  --allowed-host mcp.internal.example \
  --cors-origin https://app.example
```

Requests with an unrecognized `Host` get `421`; requests from an unlisted `Origin` get `403`. Passing `--allowed-host` or `--cors-origin` on the command line replaces the corresponding environment variable rather than adding to it. If you expose this beyond localhost, put an authenticating reverse proxy in front of it. Avoid `--transform-mode code` over HTTP entirely — `execute` is a code execution endpoint.

### Rate limiting (HTTP mode)

Off by default. `--rate-limit 20` caps **MCP requests** — tool calls,
searches, the protocol surface — at 20/second with a single global token
bucket: a total throughput cap, not per-client fairness (without auth there
is no reliable client identity to key on). The operational endpoints
(`/healthz`, `/metrics`, `/.well-known/...`) are deliberately outside the
limit: throttling a load balancer's health checks marks healthy instances
down, and those handlers are trivial reads. The limit counts every MCP
request including the initialize handshake, which is why the burst default
stays at `max(10, 2×RPS)`; keep the burst comfortably above your clients'
handshake size if you lower it. Throttled requests receive a clean MCP error
and succeed again once the bucket refills.

### Operational endpoints (HTTP mode)

- **`GET /healthz`** — liveness/readiness JSON, always public (load balancers
  can't do OAuth). `ok` and `degraded` both return 200 — degraded means the
  documentation copy is stale and a newer image should be pulled; 503 means no
  documentation is readable and traffic should not be routed here.
- **`GET /metrics`** — Prometheus text format: per-tool call counters, a
  latency histogram, request counts, uptime, and documentation age. Public on
  unauthenticated deployments; requires a valid bearer token whenever auth is
  configured.


## Features (v0.15.0)

### Tools

Twelve tools. [API.md](API.md) documents every argument and result field, and is generated from
the running server.

| Tool | What it does |
|------|--------------|
| `search_laravel_docs` | Ranked search over everything held; returns sections, each with a snippet |
| `read_laravel_doc_section` | Reads one section of a page |
| `read_laravel_doc_content` | Reads a whole page, or lists its headings |
| `list_laravel_docs` | Lists what is held, or the files of one collection |
| `laravel_docs_info` | Reports how current every source is |
| `compare_laravel_versions` | Lists the pages one Laravel version has and another lacks |
| `update_laravel_docs` | Fetches newer documentation |
| `get_laravel_package` | Looks up a package, or a category, in the catalog |
| `recommend_laravel_packages` | Suggests packages for a described need |
| `get_laravel_service_info` | Describes a first-party service and what is held for it |
| `get_laravel_learning_path` | Returns a reading order for a goal *(experimental)* |
| `browse_docs_by_category` | Lists pages by topic and difficulty *(experimental)* |

Three resource templates serve the same pages: `laravel://`, `laravel-external://` and
`laravel-package://`.

### Search

- **Ranked sections, not files.** Ask in plain language ("how do I retry a failed queue job") and
  get the sections that answer it, each with a snippet and the `file` and `section` to read next.
- **Section reads.** A whole page such as `queues.md` runs to tens of thousands of tokens. A
  section is usually a few hundred, which leaves room for your code.
- **Unified search** - One search covers the core framework docs, the services, the package docs
  and the learning resources, and labels each result with its source. `sources` narrows it, and
  no single source fills the page when others match.
- **Common tasks are recognised.** "Upload files" or "send emails" favours the pages a person has
  marked as covering that task.

### Results a program can use

- Every tool returns structured content matching a declared schema, beside the text.
- A failure is an error result with a `code` to branch on. Finding nothing is not a failure.
- `tests/protocol/contract.json` records the whole surface, and a test fails when it changes.
  [VERSIONING.md](VERSIONING.md) says what is promised from 1.0.

### MCP capabilities

- **Tasks.** `update_laravel_docs` can run as an MCP task: submit, poll, fetch the result.
- **Elicitation.** `get_laravel_learning_path` asks which path you want when the client supports
  that, and lists the paths when the client cannot be asked.
- **Registry listed.** Installable from the
  [official MCP Registry](https://registry.modelcontextprotocol.io/?search=laravel-mcp-companion),
  with `.well-known` discovery in HTTP mode.

### Production operations (HTTP mode)

- **Health and metrics.** `GET /healthz` for load balancers and a Prometheus `GET /metrics` with
  per-tool counters, a latency histogram and the age of the documentation.
- **OAuth 2.1 resource server.** Optional bearer-token validation by JWKS. Misconfiguration fails
  at startup, and an outage of the key server fails closed.
- **Rate limiting.** An opt-in token bucket over the MCP surface.
- **Hardened by default.** Loopback bind, Host and Origin validation, no wildcard CORS, and the
  same path containment for search, listing and reads.
- **Container health check.** The image declares a `HEALTHCHECK` and runs as an unprivileged user.

### Tested

About 1,400 tests, with a coverage gate of 80% over every product module (currently about 90%),
end-to-end tests over real stdio and HTTP transports, and report-only latency benchmarks.

[ROADMAP.md](ROADMAP.md) has what is left before 1.0.

## Output format

The text of a result is [TOON](https://toonformat.dev) (Token-Oriented Object Notation), which
says what JSON says in fewer characters. A search for "retry a failed job", limited to two results:

```
query: retry a failed job
scope: 13.x
sources[4]: core,services,packages,learning
count: 2
results[2]{file,section,heading,score,snippet,source}:
  13.x/queues.md,dealing-with-failed-jobs,Dealing With Failed Jobs,22.53,"## Dealing With Failed Jobs ...",core
  cloud/metrics/queues.md,job-volume,Job volume,21.55,"... A job failed permanently because ...","service:cloud"
```

How much smaller than JSON depends on the shape. Measured in characters on real results: a search
result is 16 to 20% smaller, a uniform table such as the list of collections about 60% smaller, and
a list of catalog entries, whose rows are not uniform, about 3% smaller.

The two read tools return the page's markdown as their text. Every tool also returns the same data
as a JSON object in `structuredContent`, which is what a program should read.

## How the documentation stays current

A pipeline runs every night at 00:00 UTC. It refetches every source, and when the content has
changed it opens a pull request, which merges itself once the tests pass. The merge is tagged
`docs-YYYY-MM-DD` and an image is built from it: the newest release's code with that night's
documentation, published as `:latest`.

- **The framework docs** come from the `laravel/docs` repository, one branch per version.
- **Services** are read from the `llms.txt` index each site publishes, as markdown.
- **Packages** are read from the same kind of index where one exists (Filament, Inertia) and from
  the site's own navigation where it does not (Livewire, Spatie). Each follows its current major.
- **A page a site drops is removed** after a sync that fetched everything else. A sync that fetched
  only part of a source removes nothing.

Each pull request carries a report of every source: how many pages it fetched, of how many, and
when. A source that fetched too little is flagged in that report and in an issue.

## Development

### Prerequisites
- Python 3.12+
- Node.js 18+ (for MCP Inspector)

### Setup
```bash
git clone https://github.com/brianirish/laravel-mcp-companion
cd laravel-mcp-companion
uv sync                    # creates .venv from uv.lock, development tools included
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### Running Tests
```bash
# All tests with coverage
pytest --cov --cov-report=html

# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Protocol compliance tests
pytest tests/protocol/ -m protocol

# End-to-end and benchmark suites (not run by default)
pytest -m e2e --no-cov
pytest -m bench --no-cov -s
```

### Manual Testing with MCP Inspector
The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) provides a visual UI for testing MCP servers.

```bash
# Launch Inspector (opens browser at http://localhost:6274)
npx @modelcontextprotocol/inspector python -m laravel_mcp_companion

# With specific version
npx @modelcontextprotocol/inspector python -m laravel_mcp_companion --version 11.x
```

Use the Inspector to:
- **Tools tab**: Test all tools with auto-generated input forms
- **Resources tab**: Browse `laravel://`, `laravel-external://` and `laravel-package://` resources

### Code Quality
```bash
ruff check --fix .     # Linting
mypy --ignore-missing-imports .  # Type checking
black .                # Formatting
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! See CONTRIBUTING.md for guidelines.

## Acknowledgements

- Laravel for their excellent documentation
- Laravel package authors for their contributions to the ecosystem

<!-- mcp-name: io.github.brianirish/laravel-mcp-companion -->
