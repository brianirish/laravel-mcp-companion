#!/usr/bin/env python3
"""
Laravel 12 Documentation MCP Server

This server provides Laravel 12 documentation via the Model Context Protocol (MCP).
It allows AI assistants and other tools to access and search Laravel documentation.
"""

import os
import sys
import logging
import re
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Union
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("laravel-docs-mcp")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Laravel 12 Documentation MCP Server"
    )
    parser.add_argument(
        "--docs-path", 
        type=str,
        default=None,
        help="Path to Laravel documentation directory (default: ./docs)"
    )
    parser.add_argument(
        "--server-name",
        type=str,
        default="Laravel12Docs",
        help="Name of the MCP server (default: Laravel12Docs)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=None,
        help="Host to bind to (if using network transport)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to listen on (if using network transport)"
    )
    parser.add_argument(
        "--transport",
        type=str,
        default="stdio",
        choices=["stdio", "websocket", "sse"],
        help="Transport mechanism to use (default: stdio)"
    )
    
    return parser.parse_args()

def setup_docs_path(user_path: Optional[str] = None) -> Path:
    """Set up and validate the docs directory path."""
    if user_path:
        docs_path = Path(user_path).resolve()
    else:
        # Default to 'docs' directory in the same directory as the script
        docs_path = (Path(__file__).parent / "docs").resolve()
    
    # Validate docs path
    if not docs_path.exists():
        logger.error(f"Documentation directory not found: {docs_path}")
        raise FileNotFoundError(f"Documentation directory not found: {docs_path}")
    
    if not docs_path.is_dir():
        logger.error(f"Documentation path is not a directory: {docs_path}")
        raise NotADirectoryError(f"Documentation path is not a directory: {docs_path}")
    
    # Check for markdown files
    md_files = list(docs_path.glob("**/*.md"))
    if not md_files:
        logger.warning(f"No markdown files found in {docs_path}")
    else:
        logger.info(f"Found {len(md_files)} markdown files in {docs_path}")
    
    return docs_path

def is_safe_path(base_path: Path, path: Path) -> bool:
    """Check if a path is safe (doesn't escape the base directory)."""
    return base_path in path.absolute().parents or base_path == path.absolute()

def main():
    """Main entry point for the Laravel Docs MCP Server."""
    args = parse_arguments()
    
    # Set logging level
    logger.setLevel(getattr(logging, args.log_level))
    
    # Setup docs path
    try:
        docs_path = setup_docs_path(args.docs_path)
        logger.info(f"Using docs path: {docs_path}")
    except (FileNotFoundError, NotADirectoryError) as e:
        logger.critical(str(e))
        sys.exit(1)
    
    # Create the MCP server
    mcp = FastMCP(args.server_name)
    
    @mcp.tool()
    def list_docs() -> str:
        """List all available Laravel 12 documentation files."""
        logger.debug("list_docs function called")
        result = []
        
        try:
            for root, _, files in os.walk(docs_path):
                rel_path = Path(root).relative_to(docs_path)
                md_files = [f for f in files if f.endswith('.md')]
                
                if md_files:
                    if str(rel_path) == '.':
                        result.append("Root:")
                    else:
                        result.append(f"\n{rel_path}:")
                    for file in md_files:
                        result.append(f"  {file}")
            
            return "\n".join(result) if result else "No documentation files found"
        except Exception as e:
            logger.error(f"Error listing documentation files: {str(e)}")
            return f"Error listing documentation files: {str(e)}"
    
    @mcp.resource("laravel://{path}")
    def read_doc(path: str) -> str:
        """Read a specific Laravel 12 documentation file."""
        logger.debug(f"read_doc function called with path: {path}")
        
        # Make sure the path ends with .md
        if not path.endswith('.md'):
            path = f"{path}.md"
        
        file_path = docs_path / Path(path)
        
        # Security check
        if not is_safe_path(docs_path, file_path):
            logger.warning(f"Access denied: {path} (attempted directory traversal)")
            return f"Access denied: {path} (attempted directory traversal)"
        
        if not file_path.exists():
            logger.warning(f"Documentation file not found: {file_path}")
            return f"Documentation file not found: {path}"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.debug(f"Successfully read file: {file_path} ({len(content)} bytes)")
                return content
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return f"Error reading file: {str(e)}"
    
    @mcp.tool()
    def search_docs(query: str) -> str:
        """Search through all Laravel 12 documentation for a specific term."""
        logger.debug(f"search_docs function called with query: {query}")
        
        if not query.strip():
            return "Search query cannot be empty"
        
        results = []
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        
        try:
            for root, _, files in os.walk(docs_path):
                for file in [f for f in files if f.endswith('.md')]:
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(docs_path)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if pattern.search(content):
                            count = len(pattern.findall(content))
                            results.append(f"{rel_path} ({count} matches)")
            
            if results:
                return f"Found {len(results)} files containing '{query}':\n" + "\n".join(results)
            else:
                return f"No results found for '{query}'"
        except Exception as e:
            logger.error(f"Error searching documentation: {str(e)}")
            return f"Error searching documentation: {str(e)}"
    
    @mcp.tool()
    def echo(message: str) -> str:
        """Simple echo tool for testing."""
        logger.debug(f"echo function called with message: {message}")
        return f"Echo: {message}"
    
    # Log server startup
    logger.info(f"Starting Laravel 12 Docs MCP Server ({args.server_name})")
    logger.info(f"Transport: {args.transport}")
    
    # Get transport options
    transport_options = {}
    if args.host:
        transport_options["host"] = args.host
    if args.port:
        transport_options["port"] = args.port
    
    # Run the server
    try:
        mcp.run(transport=args.transport, **transport_options)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.critical(f"Server error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()