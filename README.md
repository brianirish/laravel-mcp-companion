# Laravel MCP Companion
*formerly Laravel Docs MCP Server*

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/brianirish/laravel-mcp-companion)](https://github.com/brianirish/laravel-mcp-companion/releases)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/brianirish/laravel-mcp-companion/ci.yaml?branch=main&label=tests)](https://github.com/brianirish/laravel-mcp-companion/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/brianirish/laravel-mcp-companion/graph/badge.svg?token=VC93Y921KR)](https://codecov.io/gh/brianirish/laravel-mcp-companion)
[![License](https://img.shields.io/github/license/brianirish/laravel-mcp-companion)](https://github.com/brianirish/laravel-mcp-companion/blob/main/LICENSE)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fbrianirish%2Flaravel-mcp-companion.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fbrianirish%2Flaravel-mcp-companion?ref=badge_shield)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue)](https://github.com/brianirish/laravel-mcp-companion/pkgs/container/laravel-mcp-companion)
[![smithery badge](https://smithery.ai/badge/@brianirish/laravel-mcp-companion)](https://smithery.ai/server/@brianirish/laravel-mcp-companion)
[![GitHub Stars](https://img.shields.io/github/stars/brianirish/laravel-mcp-companion?style=social)](https://github.com/brianirish/laravel-mcp-companion)
[![GitHub Forks](https://img.shields.io/github/forks/brianirish/laravel-mcp-companion?style=social)](https://github.com/brianirish/laravel-mcp-companion)


> ⚠️ **BETA SOFTWARE** - This project is in early development. Features may not work as expected and breaking changes may occur without notice.

**Laravel MCP Companion** is a comprehensive documentation aggregator and navigator for the Laravel ecosystem. Rather than generating content, it centralizes and organizes existing high-quality documentation from across the Laravel ecosystem, making it easily discoverable through your AI assistant.

## Why Laravel MCP Companion?

| Feature | Laravel MCP Companion | Context7 |
|---------|:--------------------:|:--------:|
| **Laravel documentation support** | ✅ | ✅ |
| **Instant retrieval** (zero latency) | ✅ | ❌ |
| **Laravel multi-version support** (6.x - latest) | ✅ | ❓ |
| **Laravel service docs** (Forge, Vapor, Nova, Envoyer) | ✅ | ❌ |
| **Community learning resources** (tutorials, videos) | ✅ | ❌ |
| **Curated package recommendations** | ✅ | ❌ |
| **Offline documentation access** | ✅ | ❌ |
| **Pre-cached & pre-processed** (saves tokens) | ✅ | ❌ |
| **No internet required during use** | ✅ | ❌ |
| **Laravel-specific search & navigation** | ✅ | ❌ |
| **JavaScript/TypeScript libraries** | ❌ | ✅ |
| **Real-time doc fetching** | ❌ | ✅ |
| **Multiple programming languages** | ❌ | ✅ |

*Context7 excels at real-time documentation fetching for multiple languages (especially JS/TS), while Laravel MCP Companion provides instant, offline-capable, comprehensive Laravel ecosystem coverage with learning resources.*

### Key Differences

**Context7** requires an internet connection and fetches documentation in real-time when you add "use context7" to your prompts. It supports multiple programming languages with a focus on JavaScript/TypeScript libraries.

**Laravel MCP Companion** pre-caches all documentation locally, providing instant access without internet connectivity. It includes not just Laravel core docs, but also service documentation, community packages, tutorials, conference talks, and curated learning resources specifically for the Laravel ecosystem.

### What you get:
- **Multi-version Laravel documentation** (6.x through latest) with enhanced search
- **Auto-discovery Laravel services** - Forge, Vapor, Envoyer, Nova
- **Community package documentation** - Spatie, Livewire, Inertia, Filament
- **Curated package recommendations** with detailed integration guides  
- **Unified search** across core Laravel docs, services, and packages
- **Smart navigation** - find exactly what you need for your use case
- **Future-proof updates** - automatically adapts to Laravel service changes

## Auto-Discovery & Update Frequency

This application features an **intelligent auto-discovery system** that automatically finds and indexes Laravel documentation. Every day, it:

- ✅ **Auto-discovers** new documentation sections across Laravel services (Forge, Vapor, Nova, Envoyer)  
- ✅ **Retrieves** the latest Laravel core documentation for all versions since 6.x
- ✅ **Fetches** community package documentation (Spatie, Livewire, Inertia, Filament)
- ✅ **Adapts** automatically to structural changes in documentation websites
- ✅ **Generates** new patch releases automatically when updates are found

## Installation

### Quick Install via Smithery

```bash
npx -y @smithery/cli install @brianirish/laravel-mcp-companion --client claude
```

*Note: Smithery automatically configures your AI client.*

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
claude mcp add laravel-mcp-companion docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest

# Or add to project-specific config (for team sharing)
claude mcp add laravel-mcp-companion docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest --scope project
```

The `--scope project` option creates a `.mcp.json` file in your project root that can be committed to version control.

### Configuration Options

These options can be used with the Docker command. For example:

```bash
# Update docs for Laravel 11.x only
docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest --version 11.x

# Force update all documentation
docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest --force-update

# Update only Forge and Vapor services
docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest --services forge vapor

# Update only Livewire and Filament packages
docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest --packages livewire filament
```

| Option | Description | Default |
|--------|-------------|---------|
| `--version VERSION` | Laravel version (e.g., "12.x", "11.x") | Latest |
| `--docs-path PATH` | Documentation directory | `./docs` |
| `--log-level LEVEL` | DEBUG, INFO, WARNING, ERROR, CRITICAL | INFO |
| `--update-docs` | Update documentation on startup | false |
| `--force-update` | Force documentation update | false |
| `--external-only` | Update only external Laravel services | false |
| `--core-only` | Update only core Laravel documentation | false |
| `--packages-only` | Update only community package documentation | false |
| `--services SERVICE1 SERVICE2` | Update specific services (forge, vapor, etc.) | All |
| `--packages PACKAGE1 PACKAGE2` | Update specific packages (spatie, livewire, etc.) | All |
| `--list-services` | List available Laravel services | - |
| `--list-packages` | List available community packages | - |
| `--status` | Show documentation status for all sources | - |


## Features and Roadmap

### Current Features
- ✅ **Multi-version Laravel docs** - All versions from 6.x to latest
- ✅ **Auto-discovery engine** - Finds new docs across Forge, Vapor, Nova, Envoyer
- ✅ **Community package docs** - Documentation for Spatie, Livewire, Inertia, Filament
- ✅ **Smart package recommendations** - Curated Laravel ecosystem packages
- ✅ **Conference talk aggregator** - Fetches Laravel conference talks from YouTube (API or scraping)
- ✅ **Unified search** - One search across all documentation sources
- ✅ **Daily updates** - Automatic sync with latest documentation
- ✅ **Battle-tested** - Comprehensive test suite ensures reliability

### Upcoming Features
- 📚 **v0.8.0**: Community learning resources (Laravel News, tutorials, guides)
- 🔍 **v0.9.0**: Advanced search and smart navigation across all sources
- 🚀 **v1.0.0**: The complete Laravel documentation navigator

For detailed roadmap information, see [ROADMAP.md](ROADMAP.md).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fbrianirish%2Flaravel-mcp-companion.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fbrianirish%2Flaravel-mcp-companion?ref=badge_large)

## Contributing

Contributions are welcome! See CONTRIBUTING.md for guidelines.

## Acknowledgements

- Laravel for their excellent documentation
- Laravel package authors for their contributions to the ecosystem
