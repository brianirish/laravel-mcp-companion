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
- **Package integration guides** - Installation and setup for 50+ curated packages
- **Cross-package compatibility** - Learn which packages work well together
- **Unified search** across core Laravel docs, services, and packages
- **Daily updates** - Automatically syncs with latest documentation

## Installation

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
| `--cors-origin ORIGIN` | Browser origin allowed to call the HTTP transport, repeatable (env: `CORS_ORIGINS`) | none |
| `--allowed-host HOST` | Host header accepted in HTTP mode, repeatable (env: `ALLOWED_HOSTS`) | localhost only |

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

**This server ships no authentication.** Anyone who can reach the HTTP port can call every tool, so treat network exposure as granting full access to the documentation tree.

Defaults are conservative:

- **Binds `127.0.0.1`** outside Docker. Inside the container it binds `0.0.0.0`, where the container boundary and explicit `-p` publishing are the access control.
- **Host and Origin validation is on**, which blocks DNS-rebinding and drive-by-localhost attacks from a victim's browser.
- **CORS is disabled** unless you pass `--cors-origin`. Wildcard origins are rejected; credentials are never allowed cross-origin.

To serve browser clients or a non-loopback interface, list exactly what you trust:

```bash
python laravel_mcp_companion.py --transport http \
  --host 0.0.0.0 \
  --allowed-host mcp.internal.example \
  --cors-origin https://app.example
```

Requests with an unrecognized `Host` get `421`; requests from an unlisted `Origin` get `403`. If you expose this beyond localhost, put an authenticating reverse proxy in front of it. Avoid `--transform-mode code` over HTTP entirely — `execute` is a code execution endpoint.


## Features (v0.10.0)

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
- **Use case mapping** - Describe what you need, get relevant packages
- **Package integration guides** - Installation and setup for 50+ packages
- **Cross-package compatibility** - Documentation for package combinations
- **Unified search** - One search across all documentation sources

### Upcoming
- **v0.10.0**: MCP 2025-11-25 spec support, Registry publishing
- **v0.11.0**: Production hardening, monitoring, security audit
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
