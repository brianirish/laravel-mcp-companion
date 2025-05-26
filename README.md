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

### Manual Installation

#### Prerequisites
- Python 3.12+
- `uv` package manager (recommended)

#### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/laravel-docs-mcp.git
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
| `--version VERSION` | Laravel version branch (default: 12.x) |
| `--update-docs` | Update documentation before starting |
| `--force-update` | Force documentation update |

Example with custom options:
```bash
python laravel_docs_server.py --docs-path /path/to/docs --version 11.x --update-docs --transport websocket --host localhost --port 8000
```

### Documentation Updater

You can update the documentation separately:

```bash
# Update documentation
python docs_updater.py --target-dir ./docs --version 12.x

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
        # List documentation
        result = await client.call_tool("list_docs", {})
        print(result)
        
        # Search documentation
        result = await client.call_tool("search_docs", {"query": "routing"})
        print(result)
        
        # Get package recommendations
        result = await client.call_tool("get_package_recommendations", 
                                       {"use_case": "implementing subscription billing"})
        print(result)
        
        # Read documentation
        resource = await client.read_resource("laravel://routing.md")
        print(resource)

if __name__ == "__main__":
    asyncio.run(main())
```

### Available Tools

#### Documentation Tools
- `list_docs()` - List all documentation files
- `search_docs(query: str)` - Search documentation for specific terms
- `update_docs(version: Optional[str], force: bool)` - Update documentation
- `docs_info()` - Get documentation version information

#### Package Recommendation Tools
- `get_package_recommendations(use_case: str)` - Get package recommendations for a use case
- `get_package_info(package_name: str)` - Get details about a specific package
- `get_package_categories(category: str)` - List packages in a specific category
- `get_features_for_package(package: str)` - Get available features for a package

### Resource Access

Documentation files can be accessed as resources using:
```
laravel://{path}
```

Examples:
- `laravel://routing.md`
- `laravel://authentication.md`

## Features and Roadmap

Current Features:
- ✅ Dynamic documentation updates from Laravel's GitHub repository
- ✅ Graceful shutdown handling
- ✅ Version flexibility through command-line options
- ✅ Package recommendations based on use cases
- ✅ Implementation guidance for common Laravel packages
- ✅ Docker deployment support

Planned Features:
- Multi-version support (access documentation for multiple Laravel versions simultaneously)
- User project analysis for tailored recommendations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! See CONTRIBUTING.md for guidelines.

## Acknowledgements

- Laravel for their excellent documentation
- Laravel package authors for their contributions to the ecosystem