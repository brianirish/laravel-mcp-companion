# Laravel MCP Companion
*formerly Laravel Docs MCP Server*

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/brianirish/laravel-mcp-companion)](https://github.com/brianirish/laravel-mcp-companion/releases)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/brianirish/laravel-mcp-companion/ci.yaml?branch=main&label=tests)](https://github.com/brianirish/laravel-mcp-companion/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/brianirish/laravel-mcp-companion/graph/badge.svg?token=VC93Y921KR)](https://codecov.io/gh/brianirish/laravel-mcp-companion)
[![License](https://img.shields.io/github/license/brianirish/laravel-mcp-companion)](https://github.com/brianirish/laravel-mcp-companion/blob/main/LICENSE)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue)](https://github.com/brianirish/laravel-mcp-companion/pkgs/container/laravel-mcp-companion)
[![GitHub Stars](https://img.shields.io/github/stars/brianirish/laravel-mcp-companion?style=social)](https://github.com/brianirish/laravel-mcp-companion)
[![GitHub Forks](https://img.shields.io/github/forks/brianirish/laravel-mcp-companion?style=social)](https://github.com/brianirish/laravel-mcp-companion)

> ⚠️ **BETA SOFTWARE** - This project is in active development. Features may change and breaking changes may occur.

**Laravel MCP Companion** is a documentation aggregator and navigator for the Laravel ecosystem. It centralizes and organizes high-quality documentation from across the Laravel ecosystem, making it easily discoverable through your AI assistant.

## How It Compares

| Feature | [Laravel Boost](https://github.com/laravel/boost) | Context7 | Laravel MCP Companion |
|---------|:--------:|:--------:|:--------------------:|
| **Focus** | Code generation | General docs | Laravel documentation |
| **Best for** | Active development | Any library | Learning & reference |
| **Project-aware context** | ✅ | ❌ | ❌ |
| **Laravel multi-version support** (6.x - latest) | ❌ | ❌ | ✅ |
| **Laravel service docs** (Forge, Vapor, Nova, Envoyer) | ❌ | ❌ | ✅ |
| **Learning paths & difficulty levels** | ❌ | ❌ | ✅ |
| **"I need X" documentation finder** | ❌ | ❌ | ✅ |
| **Curated Laravel package recommendations** | ❌ | ❌ | ✅ |
| **Offline documentation access** | ❌ | ❌ | ✅ |
| **TOON format output** (30-60% fewer tokens) | ❌ | ❌ | ✅ |
| **General documentation** (non-Laravel) | ❌ | ✅ | ❌ |

**Use Boost** when writing code and you need project-aware context. **Use Context7** for non-Laravel libraries. **Use Companion** when learning, researching, or need Laravel documentation reference.

### What you get:
- **Multi-version Laravel documentation** (6.x through latest) with enhanced search
- **Learning paths** - Structured learning sequences by topic and skill level
- **"I need X" finder** - Describe what you need, get relevant documentation
- **Difficulty filtering** - Content organized by beginner/intermediate/advanced
- **15 semantic categories** - Browse documentation by topic area
- **Auto-discovery Laravel services** - Forge, Vapor, Envoyer, Nova (117+ sections)
- **Community package documentation** - 42,000+ lines from Spatie, Livewire, Inertia, Filament
- **Package integration guides** - Installation and setup for 22 curated packages
- **Cross-package compatibility** - Learn which packages work well together
- **Unified search** across core Laravel docs, services, and packages
- **Daily updates** - Automatically syncs with latest documentation

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
documentation is refreshed, so `:latest` carries the most recently published
snapshot. The catch is that **`docker run` reuses the copy you already have** —
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
documentation for the selected Laravel version during startup. Documentation for
Forge, Vapor, Nova, Envoyer and community packages refreshes separately, through the
`update_external_laravel_docs` tool your assistant can call.

With `--rm` the download is discarded when the container exits, so it repeats on
every start. A named volume keeps it — but note the trade-off:

```bash
docker run --rm -i -v laravel-mcp-docs:/app/docs \
  ghcr.io/brianirish/laravel-mcp-companion:latest --update-docs
```

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
python laravel_mcp_companion.py --transport http \
  --auth-jwks-uri https://auth.example/.well-known/jwks.json \
  --auth-issuer https://auth.example \
  --auth-audience laravel-mcp-companion

# Development only: fixed tokens from the environment (never a CLI flag,
# so secrets stay out of process listings)
AUTH_STATIC_TOKENS="my-token:my-client" python laravel_mcp_companion.py --transport http
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
python laravel_mcp_companion.py --transport http \
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


## Features (v0.12.0)

### Documentation Aggregation
- **Multi-version Laravel docs** - All versions from 6.x to latest
- **Auto-discovery engine** - Finds new docs across Forge, Vapor, Nova, Envoyer
- **Community package docs** - 42,000+ lines from Spatie, Livewire, Inertia, Filament
- **Daily updates** - Automatic sync with latest documentation

### Learning & Discovery (New in v0.9.0)
- **Learning paths** - Structured sequences for any Laravel topic
- **Difficulty levels** - Filter by beginner, intermediate, or advanced
- **15 categories** - Browse by authentication, database, testing, etc.
- **"I need X" finder** - Natural language documentation discovery
- **Related resources** - Find connected documentation automatically

### Search & Navigation
- **Ranked section search** - Ask in plain language ("how do I retry a failed
  queue job") and get the relevant *sections* ranked by relevance, each with a
  snippet, an anchor, and a source label
- **Section-level reads** - Fetch just the section you need. A whole
  documentation file can exceed 30,000 tokens; a section is typically a few
  hundred, so answers leave room for your actual code
- **Use case mapping** - Describe what you need, get relevant packages
- **Package integration guides** - Installation and setup for 22 curated packages
- **Cross-package compatibility** - Documentation for package combinations
- **Unified search** - One search across every corpus: core versions,
  services, fetched package docs, and learning resources, with a `sources`
  filter to narrow it

### MCP 2025-11-25 capabilities (new in v0.12.0)
- **Task-capable updates** - Documentation updates run as MCP tasks: submit,
  poll, fetch the result, instead of holding the connection for minutes
- **Interactive learning paths** - Ask for a learning path without naming one
  and the server asks you which of the ten curated paths you want
- **Structured output** - Tabular tools return `structuredContent` with real
  schemas alongside their TOON text
- **OAuth 2.1 resource server** - Optional bearer-token validation for the
  HTTP transport (JWKS or static dev tokens)
- **Registry-ready** - `server.json` metadata, `.well-known` discovery in
  HTTP mode, and automated MCP Registry publishing on release tags

### Upcoming
- **v0.13.0**: Production hardening, monitoring, advanced search
- **v1.0.0**: First stable release with LTS commitment

For detailed roadmap information, see [ROADMAP.md](ROADMAP.md).

## TOON Format Output

Laravel MCP Companion uses [TOON (Token-Oriented Object Notation)](https://github.com/toon-format/toon) for structured output, saving **30-60% on tokens** compared to JSON/markdown.

### Example Output

When you search for packages or list documentation, you get efficient structured data:

```
context: "authentication for SPA"
count: 2
packages[2]{id,name,description,categories,install}:
  laravel/sanctum,Laravel Sanctum,"Featherweight authentication for SPAs",[authentication,spa],"composer require laravel/sanctum"
  laravel/passport,Laravel Passport,"Full OAuth2 implementation",[authentication,api],"composer require laravel/passport"
```

Compare to the equivalent JSON (nearly 2x the tokens):

```json
{"context":"authentication for SPA","count":2,"packages":[{"id":"laravel/sanctum","name":"Laravel Sanctum",...}]}
```

### Why TOON?

- **Token efficient**: LLMs understand TOON natively - no parsing overhead
- **Structured data**: Arrays, objects, and metadata without JSON verbosity
- **AI-friendly**: Designed specifically for LLM context windows

## Auto-Discovery & Update Frequency

This application features an **intelligent auto-discovery system** that automatically finds and indexes Laravel documentation. Every day, it:

- **Auto-discovers** new documentation sections across Laravel services (Forge, Vapor, Nova, Envoyer)
- **Retrieves** the latest Laravel core documentation for all versions since 6.x
- **Fetches** community package documentation (Spatie, Livewire, Inertia, Filament)
- **Adapts** automatically to structural changes in documentation websites
- **Generates** new patch releases automatically when updates are found

## Development

### Prerequisites
- Python 3.12+
- Node.js 18+ (for MCP Inspector)

### Setup
```bash
git clone https://github.com/brianirish/laravel-mcp-companion
cd laravel-mcp-companion
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
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
```

### Manual Testing with MCP Inspector
The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) provides a visual UI for testing MCP servers.

```bash
# Launch Inspector (opens browser at http://localhost:6274)
npx @modelcontextprotocol/inspector python laravel_mcp_companion.py

# With specific version
npx @modelcontextprotocol/inspector python laravel_mcp_companion.py --version 11.x
```

Use the Inspector to:
- **Tools tab**: Test all tools with auto-generated input forms
- **Resources tab**: Browse `laravel://` and `laravel-external://` resources
- **Prompts tab**: Test prompt templates

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
