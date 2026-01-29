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

## Laravel Boost vs Laravel MCP Companion

These tools serve different purposes and work well together:

| Aspect | [laravel/boost](https://github.com/laravel/boost) | Laravel MCP Companion |
|--------|--------------|----------------------|
| **Focus** | Code generation context | Documentation navigation |
| **Use case** | Writing Laravel code | Learning & reference |
| **Approach** | Project-aware context | Version-aware docs |
| **Best for** | Active development | Research & learning |

**Use Boost** when you're writing code and need project-aware context.
**Use Companion** when you're learning, researching, or need documentation reference.

## Why Laravel MCP Companion?

| Feature | Laravel MCP Companion | Context7 |
|---------|:--------------------:|:--------:|
| **Instant documentation retrieval** (zero latency) | ✅ | ❌ |
| **Laravel multi-version support** (6.x - latest) | ✅ | ❌ |
| **Laravel service docs** (Forge, Vapor, Nova, Envoyer) | ✅ | ❌ |
| **Learning paths & difficulty levels** | ✅ | ❌ |
| **"I need X" documentation finder** | ✅ | ❌ |
| **Curated Laravel package recommendations** | ✅ | ❌ |
| **Offline documentation access** | ✅ | ❌ |
| **TOON format output** (30-60% fewer tokens) | ✅ | ❌ |
| **No internet requests during use** | ✅ | ❌ |
| **Laravel-specific search** | ✅ | ❌ |
| **Auto-discovery of service docs** | ✅ | ❌ |
| **General documentation** (non-Laravel) | ❌ | ✅ |

*Context7 excels at general documentation. Laravel MCP Companion is purpose-built for Laravel with faster, offline-capable, Laravel-specific features.*

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
# Update docs for Laravel 11.x only
docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest --version 11.x

# Force update all documentation
docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest --force-update
```

| Option | Description | Default |
|--------|-------------|---------|
| `--version VERSION` | Laravel version (e.g., "12.x", "11.x") | Latest |
| `--docs-path PATH` | Documentation directory | `./docs` |
| `--log-level LEVEL` | DEBUG, INFO, WARNING, ERROR, CRITICAL | INFO |
| `--update-docs` | Update documentation on startup | false |
| `--force-update` | Force documentation update | false |


## Features (v0.9.0)

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
npx @modelcontextprotocol/inspector python laravel_mcp_companion.py --version 12.x
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
