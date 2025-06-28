# Laravel MCP Companion
*formerly Laravel Docs MCP Server*

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/brianirish/laravel-mcp-companion)](https://github.com/brianirish/laravel-mcp-companion/releases)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/brianirish/laravel-mcp-companion/ci.yaml?branch=main&label=tests)](https://github.com/brianirish/laravel-mcp-companion/actions/workflows/ci.yaml)
[![License](https://img.shields.io/github/license/brianirish/laravel-mcp-companion)](https://github.com/brianirish/laravel-mcp-companion/blob/main/LICENSE)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue)](https://github.com/brianirish/laravel-mcp-companion/pkgs/container/laravel-mcp-companion)
[![smithery badge](https://smithery.ai/badge/@brianirish/laravel-mcp-companion)](https://smithery.ai/server/@brianirish/laravel-mcp-companion)
[![GitHub Stars](https://img.shields.io/github/stars/brianirish/laravel-mcp-companion?style=social)](https://github.com/brianirish/laravel-mcp-companion)
[![GitHub Forks](https://img.shields.io/github/forks/brianirish/laravel-mcp-companion?style=social)](https://github.com/brianirish/laravel-mcp-companion)

> ⚠️ **BETA SOFTWARE** - This project is in early development. Features may not work as expected and breaking changes may occur without notice.

**Laravel MCP Companion** is a comprehensive documentation aggregator and navigator for the Laravel ecosystem. Rather than generating content, it centralizes and organizes existing high-quality documentation from across the Laravel ecosystem, making it easily discoverable through your AI assistant.

✨ **Perfect for developers making the most of the Laravel ecosystem**

### What you get:
- **Multi-version Laravel documentation** (6.x through latest) with enhanced search
- **Auto-discovery Laravel services** - Forge, Vapor, Envoyer, Nova with 117+ sections
- **Curated package recommendations** with detailed integration guides  
- **Unified search** across core Laravel docs and external services
- **Smart navigation** - find exactly what you need for your use case
- **Future-proof updates** - automatically adapts to Laravel service changes

## Auto-Discovery & Update Frequency

This application features an **intelligent auto-discovery system** that automatically finds and indexes Laravel service documentation. Every day, it:

- ✅ **Auto-discovers** new documentation sections across Laravel services (Forge, Vapor, Nova, Envoyer)  
- ✅ **Retrieves** the latest Laravel core documentation for all versions since 6.x
- ✅ **Adapts** automatically to structural changes in Laravel service websites
- ✅ **Generates** new patch releases automatically when updates are found

**Current Coverage**: 117+ documentation sections (vs 95 manually-configured) with intelligent fallback mechanisms.

## Installation

### Quick Install via Smithery

```bash
npx -y @smithery/cli install @brianirish/laravel-mcp-companion --client claude
```

*Note: Smithery automatically configures your AI client. Skip to "First Run" below.*

### Docker

```bash
docker run ghcr.io/brianirish/laravel-mcp-companion:latest
```

## Usage

### Smithery Installation
No additional configuration needed - Smithery automatically sets up your AI client.

### Docker Installation
Add this to your AI client's MCP configuration:

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

### Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `--version VERSION` | Laravel version (e.g., "12.x", "11.x") | Latest |
| `--docs-path PATH` | Documentation directory | `./docs` |
| `--log-level LEVEL` | DEBUG, INFO, WARNING, ERROR, CRITICAL | INFO |
| `--update-docs` | Update documentation on startup | false |
| `--force-update` | Force documentation update | false |
| `--external-only` | Update only external Laravel services | false |
| `--core-only` | Update only core Laravel documentation | false |
| `--services SERVICE1 SERVICE2` | Update specific services (forge, vapor, etc.) | All |
| `--list-services` | List available Laravel services | - |
| `--status` | Show documentation status for all sources | - |

### First Run

The server automatically downloads Laravel documentation on first use. This may take a few moments initially.

### External Laravel Services (Auto-Discovery Enabled)

Laravel MCP Companion includes auto-discovery for official Laravel services with enhanced coverage:

- **Laravel Forge** - Server management and deployment *(53 sections auto-discovered)*
- **Laravel Vapor** - Serverless deployment platform *(16 sections auto-discovered)*
- **Laravel Nova** - Administration panel *(38 sections auto-discovered)*
- **Laravel Envoyer** - Zero-downtime deployment *(10 sections with intelligent fallback)*

**Auto-Discovery Features:**
- 🔍 **Smart Detection**: Automatically finds new documentation sections
- 🔄 **Version Detection**: Auto-detects latest Nova versions (currently v5)
- 🛡️ **Content Validation**: Quality scoring ensures only useful documentation
- 🔙 **Graceful Fallback**: Uses manual configuration when auto-discovery fails

Use `update_external_laravel_docs()` to trigger auto-discovery, or `list_laravel_services()` to see all available services.


## Features and Roadmap

### Current Features (v0.5.0)
- ✅ **Laravel MCP Companion**: Comprehensive documentation aggregator and navigator
- ✅ **Multi-Version Support**: Access documentation for Laravel 6.x through latest version simultaneously
- ✅ **Auto-Discovery System**: Automatically discovers Laravel service documentation (117+ sections)
- ✅ **Laravel Ecosystem Services**: Forge, Vapor, Envoyer, Nova with intelligent section detection
- ✅ **Enhanced Search**: Unified search across core Laravel docs and external services with caching
- ✅ **Package Recommendations**: 50+ curated packages including Laravel services
- ✅ **Content Validation**: Quality scoring and validation for discovered documentation sections
- ✅ **Robust Error Handling**: Retry mechanisms and graceful fallback to manual configuration
- ✅ **Performance Optimized**: File content caching and search result caching for faster responses
- ✅ **Future-Proof Updates**: Automatically adapts to Laravel service documentation changes
- ✅ **Daily Auto-Discovery**: Enhanced GitHub Actions with auto-discovery metrics and reporting

### Upcoming Features
- 🌟 **v0.6.0**: Community package documentation (Spatie, Livewire, Inertia, Filament)
- 📚 **v0.7.0**: Community learning resources (Laravel News, tutorials, guides)
- 🔍 **v0.8.0**: Advanced search and smart navigation across all sources
- 🚀 **v1.0.0**: The complete Laravel documentation navigator

For detailed roadmap information, see [ROADMAP.md](ROADMAP.md).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! See CONTRIBUTING.md for guidelines.

## Acknowledgements

- Laravel for their excellent documentation
- Laravel package authors for their contributions to the ecosystem

---
*✅ Certified by [MCP Review](https://mcpreview.com/mcp-servers/brianirish/laravel-mcp-companion)*