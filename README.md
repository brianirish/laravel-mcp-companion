# Laravel 12 Docs MCP Server

A Model Context Protocol (MCP) server that provides access to Laravel 12 documentation for AI assistants, language models, and other tools.

## Overview

This project provides a server that enables AI assistants to access and search Laravel 12 documentation using the Model Context Protocol (MCP). It allows AI tools to:

- List all available documentation files
- Read specific documentation files
- Search documentation for specific terms

## Installation

### Prerequisites

- Python 3.12 or higher
- `uv` package manager (recommended)
- Laravel 12 documentation files (markdown format)

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

3. Ensure you have Laravel 12 documentation files in the `docs` directory. If not, you can download them from Laravel's official documentation repository.

## Usage

### Starting the Server

Run the server with:

```bash
python laravel_docs_server.py
```

#### Command Line Options

- `--docs-path PATH` - Path to Laravel documentation directory (default: ./docs)
- `--server-name NAME` - Name of the MCP server (default: Laravel12Docs)
- `--log-level LEVEL` - Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)
- `--transport TYPE` - Transport mechanism: stdio, websocket, sse (default: stdio)
- `--host HOST` - Host to bind to (for network transports)
- `--port PORT` - Port to listen on (for network transports)

Example with custom options:

```bash
python laravel_docs_server.py --docs-path /path/to/docs --log-level DEBUG --transport websocket --host localhost --port 8000
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
3. `echo(message: str)` - Simple echo tool for testing connectivity

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

- **Docker Deployment** - Run the server as a containerized application for easier deployment and isolation
- **Dynamic Documentation Sourcing** - Automatically fetch and update documentation from Laravel's official GitHub repository
- **Multi-version Support** - Access documentation for multiple Laravel versions (10.x, 11.x, 12.x) through a single server instance

## Acknowledgements

- Laravel for their excellent documentation