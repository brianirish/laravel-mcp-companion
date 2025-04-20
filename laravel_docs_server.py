#!/usr/bin/env python3
"""
Laravel Documentation MCP Server

This server provides Laravel documentation via the Model Context Protocol (MCP).
It allows AI assistants and other tools to access and search Laravel documentation.
"""

import os
import sys
import logging
import re
import argparse
import json
import atexit
from pathlib import Path
from typing import List, Dict, Optional, Union
from fastmcp import FastMCP

# Import documentation updater
from docs_updater import DocsUpdater
from shutdown_handler import GracefulShutdown

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("laravel-docs-mcp")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Laravel Documentation MCP Server"
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
        default="LaravelDocs",
        help="Name of the MCP server (default: LaravelDocs)"
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
    parser.add_argument(
        "--version",
        type=str,
        default="12.x",
        help="Laravel version branch to use (default: 12.x)"
    )
    parser.add_argument(
        "--update-docs",
        action="store_true",
        help="Update documentation before starting server"
    )
    parser.add_argument(
        "--force-update",
        action="store_true",
        help="Force update of documentation even if already up to date"
    )
    
    return parser.parse_args()

def setup_docs_path(user_path: Optional[str] = None) -> Path:
    """Set up and validate the docs directory path."""
    if user_path:
        docs_path = Path(user_path).resolve()
    else:
        # Default to 'docs' directory in the same directory as the script
        docs_path = (Path(__file__).parent / "docs").resolve()
    
    # Create directory if it doesn't exist
    docs_path.mkdir(parents=True, exist_ok=True)
    
    return docs_path

def is_safe_path(base_path: Path, path: Path) -> bool:
    """Check if a path is safe (doesn't escape the base directory)."""
    return base_path in path.absolute().parents or base_path == path.absolute()

def update_documentation(docs_path: Path, version: str, force: bool = False) -> bool:
    """Update the documentation if needed or forced."""
    try:
        updater = DocsUpdater(docs_path, version)
        updated = updater.update(force=force)
        return updated
    except Exception as e:
        logger.error(f"Failed to update documentation: {str(e)}")
        return False

def get_docs_metadata(docs_path: Path) -> Dict:
    """Get documentation metadata if available."""
    metadata_file = docs_path / ".metadata" / "sync_info.json"
    
    if not metadata_file.exists():
        return {"status": "unknown", "message": "No metadata available"}
    
    try:
        with open(metadata_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Error reading metadata file: {str(e)}")
        return {"status": "error", "message": f"Error reading metadata: {str(e)}"}

def main():
    """Main entry point for the Laravel Docs MCP Server."""
    args = parse_arguments()
    
    # Set logging level
    logger.setLevel(getattr(logging, args.log_level))
    
    # Setup docs path
    docs_path = setup_docs_path(args.docs_path)
    logger.info(f"Using docs path: {docs_path}")
    
    # Update documentation if requested
    if args.update_docs or args.force_update:
        logger.info(f"Updating documentation (version: {args.version}, force: {args.force_update})")
        updated = update_documentation(docs_path, args.version, args.force_update)
        if updated:
            logger.info("Documentation updated successfully")
        else:
            logger.info("Documentation update not performed or not needed")
    
    # Create temporary file paths if needed
    temp_files = []
    
    # Function to clean up temporary files
    def cleanup_temp_files():
        for file_path in temp_files:
            try:
                if os.path.exists(file_path):
                    logger.debug(f"Removing temporary file: {file_path}")
                    os.remove(file_path)
            except Exception as e:
                logger.warning(f"Failed to remove temporary file {file_path}: {str(e)}")
    
    # Create the MCP server
    mcp = FastMCP(args.server_name)
    
    @mcp.tool()
    def list_docs() -> str:
        """List all available Laravel documentation files."""
        logger.debug("list_docs function called")
        result = []
        
        try:
            # First, check if there are any docs at all
            md_files_exist = False
            for root, _, files in os.walk(docs_path):
                if any(f.endswith('.md') for f in files):
                    md_files_exist = True
                    break
            
            if not md_files_exist:
                return "No documentation files found. Use update_docs() to fetch documentation."
            
            # Add metadata if available
            metadata = get_docs_metadata(docs_path)
            if metadata.get("version"):
                result.append(f"Laravel Documentation (Version: {metadata['version']})")
                result.append(f"Last updated: {metadata.get('sync_time', 'unknown')}")
                result.append(f"Commit: {metadata.get('commit_sha', 'unknown')[:7]}")
                result.append("")
            
            # List all markdown files
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
        """Read a specific Laravel documentation file."""
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
        """Search through all Laravel documentation for a specific term."""
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
    def update_docs(version: Optional[str] = None, force: bool = False) -> str:
        """
        Update Laravel documentation from official GitHub repository.
        
        Args:
            version: Laravel version branch (e.g., "12.x")
            force: Force update even if already up to date
        """
        logger.debug(f"update_docs function called (version: {version}, force: {force})")
        
        # Use provided version or default to the one specified at startup
        doc_version = version or args.version
        
        try:
            updater = DocsUpdater(docs_path, doc_version)
            
            # Check if update is needed
            if not force and not updater.needs_update():
                return f"Documentation is already up to date (version: {doc_version})"
            
            # Perform the update
            updated = updater.update(force=force)
            
            if updated:
                metadata = get_docs_metadata(docs_path)
                return (
                    f"Documentation updated successfully to {doc_version}\n"
                    f"Commit: {metadata.get('commit_sha', 'unknown')[:7]}\n"
                    f"Date: {metadata.get('commit_date', 'unknown')}\n"
                    f"Message: {metadata.get('commit_message', 'unknown')}"
                )
            else:
                return f"Documentation update not performed or not needed"
        except Exception as e:
            logger.error(f"Error updating documentation: {str(e)}")
            return f"Error updating documentation: {str(e)}"
    
    @mcp.tool()
    def docs_info() -> str:
        """Get information about the documentation version and status."""
        logger.debug("docs_info function called")
        
        metadata = get_docs_metadata(docs_path)
        
        if "version" not in metadata:
            return "No documentation metadata available. Use update_docs() to fetch documentation."
        
        return (
            f"Laravel Documentation\n"
            f"Version: {metadata.get('version', 'unknown')}\n"
            f"Last updated: {metadata.get('sync_time', 'unknown')}\n"
            f"Commit SHA: {metadata.get('commit_sha', 'unknown')}\n"
            f"Commit date: {metadata.get('commit_date', 'unknown')}\n"
            f"Commit message: {metadata.get('commit_message', 'unknown')}\n"
            f"GitHub URL: {metadata.get('commit_url', 'unknown')}"
        )
    
    @mcp.tool()
    def echo(message: str) -> str:
        """Simple echo tool for testing."""
        logger.debug(f"echo function called with message: {message}")
        return f"Echo: {message}"
    
    # Log server startup
    logger.info(f"Starting Laravel Docs MCP Server ({args.server_name})")
    logger.info(f"Transport: {args.transport}")
    logger.info(f"Laravel version: {args.version}")
    
    # Get transport options
    transport_options = {}
    if args.host:
        transport_options["host"] = args.host
    if args.port:
        transport_options["port"] = args.port
    
    # Setup graceful shutdown handler
    shutdown_handler = GracefulShutdown(logger)
    
    # Define cleanup function
    def cleanup():
        logger.info("Performing cleanup before shutdown")
        
        # Clean up any temporary files
        cleanup_temp_files()
        
        # Save any pending state if needed
        try:
            # Example: save server stats or state
            logger.debug("Saving server state")
        except Exception as e:
            logger.error(f"Error saving server state: {str(e)}")
        
        logger.info("Cleanup complete")
    
    # Register cleanup with shutdown handler only (not with atexit)
    shutdown_handler.register(cleanup)
    
    # Run the server
    try:
        logger.info("Server ready. Press Ctrl+C to stop.")
        mcp.run(transport=args.transport, **transport_options)
    except Exception as e:
        logger.critical(f"Server error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()