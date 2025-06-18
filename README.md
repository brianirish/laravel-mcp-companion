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

### Install from PyPI

```bash
pip install laravel-docs-mcp
```

### Docker

```bash
# Pull and run the latest version
docker run -p 8000:8000 ghcr.io/brianirish/laravel-docs-mcp:latest

# Or run a specific version
docker run -p 8000:8000 ghcr.io/brianirish/laravel-docs-mcp:v0.1.4
```

### Manual Installation from Source

#### Prerequisites
- Python 3.12+
- `uv` package manager (recommended)

#### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/brianirish/laravel-docs-mcp.git
   cd laravel-docs-mcp
   ```

2. Set up environment and install dependencies:
   ```bash
   # Create and activate virtual environment
   uv venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   
   # Install dependencies
   uv pip install .
   ```

## Usage

### Using with AI Clients

Once installed, the MCP server integrates directly with your AI client (Claude Desktop, Cursor, etc.). The server provides Laravel documentation and package recommendation tools that your AI assistant can use automatically.

### Smithery (Recommended)

After installing via Smithery, the server is automatically configured with your AI client:

```bash
npx -y @smithery/cli install @brianirish/laravel-docs-mcp --client claude
```

The server runs automatically when your AI client needs it. No manual startup required.

### Docker

The Docker container runs the server immediately:

```bash
# Basic usage with default settings
docker run ghcr.io/brianirish/laravel-docs-mcp:latest

# Custom configuration with environment variables
docker run -e LOG_LEVEL=DEBUG -e LARAVEL_VERSION=11.x ghcr.io/brianirish/laravel-docs-mcp:latest

# Network transport for remote access
docker run -p 8000:8000 ghcr.io/brianirish/laravel-docs-mcp:latest --transport websocket --host 0.0.0.0 --port 8000
```

### PyPI / Manual Installation

After installing from PyPI or source, start the server manually:

```bash
# Basic server start
laravel-docs-server

# Or if installed from source
python laravel_docs_server.py
```

The server automatically fetches Laravel documentation on first run and can be stopped with Ctrl+C.

### Advanced Configuration

For custom deployments, you can configure various options:

| Option | Description |
|--------|-------------|
| `--docs-path PATH` | Documentation directory path (default: ./docs) |
| `--server-name NAME` | Server name (default: LaravelDocs) |
| `--log-level LEVEL` | Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO) |
| `--transport TYPE` | Transport method: stdio, websocket, sse (default: stdio) |
| `--host HOST` | Host to bind to (network transport) |
| `--port PORT` | Port to listen on (network transport) |
| `--version VERSION` | Laravel version branch (default: latest available) |
| `--update-docs` | Update documentation before starting |
| `--force-update` | Force documentation update |

Example with custom options:
```bash
python laravel_docs_server.py --docs-path /path/to/docs --version 11.x --update-docs --transport websocket --host localhost --port 8000
```

### Documentation Management

Update documentation independently of the server:

```bash
# Update documentation for latest version
python docs_updater.py --target-dir ./docs

# Update specific version
python docs_updater.py --target-dir ./docs --version 11.x

# Update all supported versions
python docs_updater.py --all-versions

# Check if update is needed
python docs_updater.py --check-only

# Force update
python docs_updater.py --force
```

## API Reference

### Documentation Tools
- `list_laravel_docs(version: Optional[str])` - List documentation files (all versions or specific version)
- `search_laravel_docs(query: str, version: Optional[str])` - Search documentation for specific terms
- `update_laravel_docs(version: Optional[str], force: bool)` - Update documentation
- `laravel_docs_info(version: Optional[str])` - Get documentation version information

### Package Recommendation Tools
- `get_laravel_package_recommendations(use_case: str)` - Get package recommendations for a use case
- `get_laravel_package_info(package_name: str)` - Get details about a specific package
- `get_laravel_package_categories(category: str)` - List packages in a specific category
- `get_features_for_laravel_package(package: str)` - Get available features for a package

## Features and Roadmap

### Current Features (v0.2.0)
- ✅ **Multi-Version Support**: Access documentation for Laravel 6.x through latest version simultaneously
- ✅ **Future-Proof Version Detection**: Automatically detects and supports new Laravel releases (13.x, 14.x, etc.)
- ✅ **Daily Documentation Updates**: Automatically syncs with Laravel's GitHub repository every day
- ✅ **Dynamic Versioning**: Automatic version management based on git tags
- ✅ **Automated Releases**: Patch releases triggered by documentation updates
- ✅ **Multiple Deployment Options**: PyPI package, Docker images, and Smithery marketplace
- ✅ **Package Recommendations**: Intelligent suggestions based on specific use cases
- ✅ **Implementation Guidance**: Detailed information for common Laravel packages
- ✅ **Flexible Configuration**: Support for multiple Laravel versions and transport methods
- ✅ **Graceful Shutdown**: Proper cleanup and signal handling

### Upcoming Features
- 🔧 **v0.3.0**: Comprehensive testing, performance optimization, enhanced error handling
- 🔍 **v0.4.0**: Semantic search, code example extraction, cross-version comparison
- 📦 **v0.5.0**: Extended Laravel ecosystem support, community package integration
- 🎯 **v0.6.0**: Project analysis, personalized recommendations, migration assistance
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