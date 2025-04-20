# Laravel Docs MCP Server

A Model Context Protocol (MCP) server that provides access to Laravel documentation for AI assistants, language models, and other tools.

## Overview

This project provides a server that enables AI assistants to access and search Laravel documentation using the Model Context Protocol (MCP). It allows AI tools to:

- List all available documentation files
- Read specific documentation files
- Search documentation for specific terms
- Automatically fetch and update documentation from Laravel's GitHub repository
- Support different Laravel versions (via command line option)

## Installation

### Prerequisites

- Python 3.12 or higher
- `uv` package manager (recommended)

### Steps

1. Clone this repository:

```bash
git clone https://github.com/yourusername/laravel-docs-mcp.git
cd laravel-docs-mcp
```

2. Create a virtual environment and install dependencies with `uv`:

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
# On Linux/macOS
source .venv/bin/activate
# On Windows
.venv\Scripts\activate

# Install the package and its dependencies
uv pip install .
```

3. The server will automatically fetch the latest Laravel 12 documentation from GitHub when first run.

## Usage

### Starting the Server

Run the server with:

```bash
python laravel_docs_server.py
```

The server can be stopped gracefully at any time by pressing Ctrl+C, which will trigger proper cleanup of resources.

#### Command Line Options

- `--docs-path PATH` - Path to Laravel documentation directory (default: ./docs)
- `--server-name NAME` - Name of the MCP server (default: LaravelDocs)
- `--log-level LEVEL` - Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)
- `--transport TYPE` - Transport mechanism: stdio, websocket, sse (default: stdio)
- `--host HOST` - Host to bind to (for network transports)
- `--port PORT` - Port to listen on (for network transports)
- `--version VERSION` - Laravel version branch to use (default: 12.x)
- `--update-docs` - Update documentation before starting server
- `--force-update` - Force update of documentation even if already up to date

Example with custom options:

```bash
python laravel_docs_server.py --docs-path /path/to/docs --version 11.x --update-docs --log-level DEBUG --transport websocket --host localhost --port 8000
```

### Documentation Updater

The server includes a documentation updater that can automatically fetch and update Laravel documentation from GitHub:

```bash
# Update documentation separately
python docs_updater.py --target-dir ./docs --version 12.x

# Check if documentation needs updating without performing the update
python docs_updater.py --check-only

# Force update even if already up to date
python docs_updater.py --force
```

### Connecting to the Server

You can use the FastMCP client library to connect to the server:

```python
import asyncio
from fastmcp import Client

async def main():
    # Connect to the server
    client = Client("path/to/laravel_docs_server.py")  # STDIO transport
    
    async with client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        
        # Update documentation
        result = await client.call_tool("update_docs", {"version": "12.x"})
        print(result)
        
        # List documentation files
        result = await client.call_tool("list_docs", {})
        print(result)
        
        # Search documentation
        result = await client.call_tool("search_docs", {"query": "routing"})
        print(result)
        
        # Read specific documentation
        resource = await client.read_resource("laravel://routing.md")
        print(resource)

if __name__ == "__main__":
    asyncio.run(main())
```

### Available Tools

The server provides the following MCP tools:

1. `list_docs()` - Lists all available documentation files
2. `search_docs(query: str)` - Searches documentation for a specific term
3. `update_docs(version: Optional[str], force: bool)` - Updates documentation from GitHub
4. `docs_info()` - Shows information about the current documentation version
5. `echo(message: str)` - Simple echo tool for testing connectivity

### Available Resources

Documentation files are available as resources with the URI format:

```
laravel://{path}
```

Where `{path}` is the path to the documentation file relative to the docs directory.

Example:
```
laravel://routing.md
laravel://authentication.md
```

## Integration with AI Assistants

This MCP server is designed to work with AI assistants that support the Model Context Protocol. When properly configured, these assistants can use the documentation to provide more accurate answers about Laravel.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for details.

## Roadmap

- ✅ **Dynamic Documentation Sourcing** - Automatically fetch and update documentation from Laravel's official GitHub repository
- ✅ **Graceful Shutdown** - Handle termination signals properly for clean server shutdown
- ✅ **Version Agnostic** - Support any Laravel version through command line options
- **Docker Deployment** - Run the server as a containerized application for easier deployment and isolation
- **Multi-version Support** - Access documentation for multiple Laravel versions (10.x, 11.x, 12.x) through a single server instance

## Acknowledgements

- Laravel for their excellent documentation