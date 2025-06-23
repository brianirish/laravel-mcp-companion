# Laravel Docs MCP Server

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/brianirish/laravel-docs-mcp)](https://github.com/brianirish/laravel-docs-mcp/releases)
[![PyPI](https://img.shields.io/pypi/v/laravel-docs-mcp)](https://pypi.org/project/laravel-docs-mcp/)
[![Python Version](https://img.shields.io/pypi/pyversions/laravel-docs-mcp)](https://pypi.org/project/laravel-docs-mcp/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/brianirish/laravel-docs-mcp/ci.yaml?branch=main&label=tests)](https://github.com/brianirish/laravel-docs-mcp/actions/workflows/ci.yaml)
[![License](https://img.shields.io/github/license/brianirish/laravel-docs-mcp)](https://github.com/brianirish/laravel-docs-mcp/blob/main/LICENSE)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue)](https://github.com/brianirish/laravel-docs-mcp/pkgs/container/laravel-docs-mcp)
[![smithery badge](https://smithery.ai/badge/@brianirish/laravel-docs-mcp)](https://smithery.ai/server/@brianirish/laravel-docs-mcp)
[![GitHub Stars](https://img.shields.io/github/stars/brianirish/laravel-docs-mcp?style=social)](https://github.com/brianirish/laravel-docs-mcp)
[![GitHub Forks](https://img.shields.io/github/forks/brianirish/laravel-docs-mcp?style=social)](https://github.com/brianirish/laravel-docs-mcp)

> ⚠️ **BETA SOFTWARE** - This project is in early development. Features may not work as expected and breaking changes may occur without notice.

Are you creating or modifying a Laravel app? Hook this MCP up to your AI assistant and immediately get access to:
- The latest Laravel documentation, for all versions from 6.x
- Intelligent Laravel package recommendations based on the context from your codebase, and what you're trying to accomplish.

This is like having a very book-smart and up-to-date Laravel dev sit next to you as you code your application.

## Update Frequency

This application is written in a way to maximize the value out of GitHub Actions. Every day, it retrieves the latest Laravel documentation for all versions since 6.x (sometimes the old docs get updated too!). If it finds any updates, a new patch release will automatically be generated here and then distributed to both Pypi and GHCR for your consumption. Mmm, delicious.

## Installation

### Quick Install via Smithery

```bash
npx -y @smithery/cli install @brianirish/laravel-docs-mcp --client claude
```

*Note: Smithery automatically configures your AI client. Skip to "First Run" below.*

### Install from PyPI

```bash
pip install laravel-docs-mcp
```

### Docker

```bash
docker run ghcr.io/brianirish/laravel-docs-mcp:latest
```

## Usage

### Smithery Installation
No additional configuration needed - Smithery automatically sets up your AI client.

### PyPI Installation
Add this to your AI client's MCP configuration:

```json
{
  "mcpServers": {
    "laravel-docs": {
      "command": "python",
      "args": ["laravel_docs_server.py"]
    }
  }
}
```

### Docker Installation
Add this to your AI client's MCP configuration:

```json
{
  "mcpServers": {
    "laravel-docs": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "ghcr.io/brianirish/laravel-docs-mcp:latest"]
    }
  }
}
```

### Custom Options
For PyPI installations, add options to the args array:

```json
{
  "mcpServers": {
    "laravel-docs": {
      "command": "python",
      "args": [
        "laravel_docs_server.py",
        "--version", "11.x",
        "--log-level", "INFO",
        "--update-docs"
      ]
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

### Current Features (v0.3.x)
- ✅ **Multi-Version Support**: Access documentation for Laravel 6.x through latest version simultaneously
- ✅ **Future-Proof Version Detection**: Automatically detects and supports new Laravel releases (13.x, 14.x, etc.)
- ✅ **Daily Documentation Updates**: Automatically syncs with Laravel's GitHub repository every day
- ✅ **Dynamic Versioning**: Automatic version management based on git tags
- ✅ **Automated Releases**: Patch releases triggered by documentation updates
- ✅ **Multiple Deployment Options**: PyPI package, Docker images, and Smithery marketplace
- ✅ **Package Recommendations**: Intelligent suggestions based on specific use cases
- ✅ **Implementation Guidance**: Detailed information for common Laravel packages
- ✅ **Flexible Configuration**: Support for multiple Laravel versions
- ✅ **Graceful Shutdown**: Proper cleanup and signal handling

### Upcoming Features
- 🔧 **v0.4.0**: Comprehensive testing, performance optimization, enhanced error handling
- 🔍 **v0.5.0**: Semantic search, code example extraction, cross-version comparison
- 📦 **v0.6.0**: Extended Laravel ecosystem support, community package integration
- 🎯 **v0.7.0**: Project analysis, personalized recommendations, migration assistance
- 🚀 **v1.0.0**: The definitive Laravel documentation companion

For detailed roadmap information, see [ROADMAP.md](ROADMAP.md).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! See CONTRIBUTING.md for guidelines.

## Acknowledgements

- Laravel for their excellent documentation
- Laravel package authors for their contributions to the ecosystem

---
*✅ Certified by [MCP Review](https://mcpreview.com/mcp-servers/brianirish/laravel-docs-mcp)*