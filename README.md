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

> ⚠️ **Alpha Software** - This project is in early development. Features may not work as expected and breaking changes may occur without notice.

An AI assistant for Laravel developers that provides access to the latest Laravel documentation and intelligent package recommendations through the Model Context Protocol (MCP). This enables AI tools to help you build Laravel applications with up-to-date information and best practices.

## Overview

This server enables AI assistants to access Laravel documentation and package recommendations using the Model Context Protocol (MCP). It allows AI tools to:

- Access and search Laravel documentation
- Receive package recommendations based on specific use cases
- Get implementation guidance for popular Laravel packages
- Automatically update documentation from Laravel's GitHub repository

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

### Starting the Server

```bash
python laravel_docs_server.py
```

The server automatically fetches Laravel documentation on first run and can be stopped with Ctrl+C.

### Command Line Options

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

### Documentation Updater

You can update the documentation separately:

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

### Client Example

```python
import asyncio
from fastmcp import Client

async def main():
    client = Client("path/to/laravel_docs_server.py")
    
    async with client:
        # List documentation for all versions
        result = await client.call_tool("list_laravel_docs", {})
        print(result)
        
        # List documentation for specific version
        result = await client.call_tool("list_laravel_docs", {"version": "11.x"})
        print(result)
        
        # Search documentation across all versions
        result = await client.call_tool("search_laravel_docs", {"query": "routing"})
        print(result)
        
        # Search in specific version
        result = await client.call_tool("search_laravel_docs", 
                                       {"query": "blade components", "version": "12.x"})
        print(result)
        
        # Get package recommendations
        result = await client.call_tool("get_laravel_package_recommendations", 
                                       {"use_case": "implementing subscription billing"})
        print(result)
        
        # Read documentation (latest version)
        resource = await client.read_resource("laravel://routing.md")
        print(resource)
        
        # Read documentation (specific version)
        resource = await client.read_resource("laravel://11.x/blade.md")
        print(resource)

if __name__ == "__main__":
    asyncio.run(main())
```

### Available Tools

#### Documentation Tools
- `list_laravel_docs(version: Optional[str])` - List documentation files (all versions or specific version)
- `search_laravel_docs(query: str, version: Optional[str])` - Search documentation for specific terms
- `update_laravel_docs(version: Optional[str], force: bool)` - Update documentation
- `laravel_docs_info(version: Optional[str])` - Get documentation version information

#### Package Recommendation Tools
- `get_laravel_package_recommendations(use_case: str)` - Get package recommendations for a use case
- `get_laravel_package_info(package_name: str)` - Get details about a specific package
- `get_laravel_package_categories(category: str)` - List packages in a specific category
- `get_features_for_laravel_package(package: str)` - Get available features for a package

### Resource Access

Documentation files can be accessed as resources using:
```
laravel://{path}
laravel://{version}/{path}
```

Examples:
- `laravel://routing.md` (uses latest version)
- `laravel://11.x/authentication.md` (specific version)
- `laravel://12.x/blade.md`

## Automated Workflows

This project includes several automated GitHub Actions workflows:

### Daily Documentation Updates
- **Trigger**: Every day at midnight UTC (can also be triggered manually)
- **Process**: Checks for Laravel documentation updates → Creates PR → Auto-merges → Creates patch version tag
- **Result**: Automatic patch releases when Laravel docs are updated

### Release Publishing
- **Trigger**: When version tags are pushed (e.g., `v0.1.4`)
- **Process**: Builds packages → Publishes to PyPI → Builds and pushes Docker images to GHCR
- **Result**: Synchronized releases across PyPI and Docker Hub

### Dynamic Versioning
- **Version Source**: Automatically derived from git tags using `hatch-vcs`
- **Development Builds**: Get unique identifiers (e.g., `0.1.3.dev1+g75aec71`)
- **Release Builds**: Clean version numbers matching tags (e.g., `0.1.4`)

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