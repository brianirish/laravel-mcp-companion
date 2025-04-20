#!/usr/bin/env python3
"""
Example client for Laravel Docs MCP Server

This script demonstrates how to connect to the Laravel Docs MCP server
and use its tools and resources.
"""

import asyncio
import argparse
from fastmcp import Client

async def list_documentation(client):
    """List all available documentation files."""
    print("\n=== LISTING DOCUMENTATION FILES ===\n")
    result = await client.call_tool("list_docs", {})
    print(result[0].text)  # Access the text content from the response

async def search_documentation(client, query):
    """Search documentation for a specific term."""
    print(f"\n=== SEARCHING DOCUMENTATION FOR '{query}' ===\n")
    result = await client.call_tool("search_docs", {"query": query})
    print(result[0].text)  # Access the text content from the response

async def read_document(client, path):
    """Read a specific documentation file."""
    print(f"\n=== READING DOCUMENTATION: {path} ===\n")
    # Make sure path doesn't start with a slash
    path = path.lstrip('/')
    resource_uri = f"laravel://{path}"
    
    try:
        result = await client.read_resource(resource_uri)
        # Print first 500 characters with ellipsis if longer
        content = result[0].text
        if len(content) > 500:
            print(f"{content[:500]}...\n[Content truncated, total length: {len(content)} characters]")
        else:
            print(content)
    except Exception as e:
        print(f"Error reading document: {e}")

async def update_documentation(client, version=None, force=False):
    """Update the documentation from GitHub."""
    print("\n=== UPDATING DOCUMENTATION ===\n")
    params = {}
    if version:
        params["version"] = version
    if force:
        params["force"] = force
    
    result = await client.call_tool("update_docs", params)
    print(result[0].text)

async def show_docs_info(client):
    """Show information about the documentation."""
    print("\n=== DOCUMENTATION INFO ===\n")
    result = await client.call_tool("docs_info", {})
    print(result[0].text)

async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Laravel Docs MCP Client Example")
    parser.add_argument(
        "--server", 
        type=str, 
        default="laravel_docs_server.py",
        help="Path to the server script or URL to connect to"
    )
    parser.add_argument(
        "--search", 
        type=str, 
        help="Search term to look for in documentation"
    )
    parser.add_argument(
        "--read", 
        type=str, 
        help="Path to documentation file to read (e.g., 'routing.md')"
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update documentation from GitHub"
    )
    parser.add_argument(
        "--version",
        type=str,
        help="Laravel version to use when updating (e.g., '12.x')"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force update even if already up to date"
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Show documentation information"
    )
    args = parser.parse_args()
    
    # Connect to the MCP server
    print(f"Connecting to Laravel Docs MCP server: {args.server}")
    client = Client(args.server)
    
    async with client:
        print(f"Connected: {client.is_connected()}")
        
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {[tool.name for tool in tools]}")
        
        # List resources
        resources = await client.list_resources()
        print(f"Resource patterns: {[resource.pattern for resource in resources]}")
        
        # Run requested operations
        if args.update:
            await update_documentation(client, args.version, args.force)
        
        if args.info:
            await show_docs_info(client)
        
        await list_documentation(client)
        
        if args.search:
            await search_documentation(client, args.search)
        
        if args.read:
            await read_document(client, args.read)

if __name__ == "__main__":
    asyncio.run(main())