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
- **Curated package recommendations** with detailed integration guides
- **Community resource discovery** - tutorials, guides, and best practices
- **Smart navigation** - find exactly what you need for your use case

## Update Frequency

This application is written in a way to maximize the value out of GitHub Actions. Every day, it retrieves the latest Laravel documentation for all versions since 6.x (sometimes the old docs get updated too!). If it finds any updates, a new patch release will automatically be generated here and then distributed to both Pypi and GHCR for your consumption. Mmm, delicious.

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

### First Run

The server automatically downloads Laravel documentation on first use. This may take a few moments initially.


## Features and Roadmap

### Current Features (v0.4.0)
- ✅ **Laravel MCP Companion**: Rebranded as comprehensive documentation aggregator and navigator
- ✅ **Multi-Version Support**: Access documentation for Laravel 6.x through latest version simultaneously
- ✅ **Enhanced Content Retrieval**: Context-aware search, document structure extraction, category browsing
- ✅ **Package Recommendations**: 50+ curated packages with detailed integration guides
- ✅ **Future-Proof Version Detection**: Automatically detects and supports new Laravel releases
- ✅ **Daily Documentation Updates**: Automatically syncs with Laravel's GitHub repository
- ✅ **Streamlined Distribution**: Docker images and Smithery marketplace (PyPI removed)
- ✅ **Documentation Aggregator Strategy**: Focus on centralizing existing high-quality content

### Upcoming Features
- 📦 **v0.5.0**: Laravel ecosystem documentation (Sanctum, Cashier, Scout, Forge, Vapor, Nova)
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