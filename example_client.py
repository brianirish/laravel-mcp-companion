#!/usr/bin/env python3
"""
Example client for Laravel 12 Docs MCP Server

This script demonstrates how to connect to the Laravel 12 Docs MCP server
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

async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Laravel 12 Docs MCP Client Example")
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
    args = parser.parse_args()
    
    # Connect to the MCP server
    print(f"Connecting to Laravel 12 Docs MCP server: {args.server}")
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
        await list_documentation(client)
        
        if args.search:
            await search_documentation(client, args.search)
        
        if args.read:
            await read_document(client, args.read)

if __name__ == "__main__":
    asyncio.run(main())