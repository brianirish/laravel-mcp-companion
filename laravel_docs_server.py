#!/usr/bin/env python3
"""
Laravel Documentation MCP Server

This server provides Laravel documentation and package recommendations via the Model Context Protocol (MCP).
It allows AI assistants and other tools to access and search Laravel documentation, as well as
recommend appropriate Laravel packages for specific use cases.
"""

import os
import sys
import logging
import re
import argparse
import json
from pathlib import Path
from typing import Dict, Optional, List, Any
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

# Define the Laravel package catalog
PACKAGE_CATALOG = {
    "laravel/cashier": {
        "name": "Laravel Cashier",
        "description": "Laravel Cashier provides an expressive, fluent interface to Stripe's subscription billing services.",
        "categories": ["payment", "billing", "subscription"],
        "use_cases": [
            "Implementing subscription billing",
            "Processing one-time payments",
            "Managing customer payment information",
            "Handling webhooks from payment providers"
        ],
        "installation": "composer require laravel/cashier",
        "documentation_link": "laravel://packages/cashier.md"
    },
    "laravel/sanctum": {
        "name": "Laravel Sanctum",
        "description": "Laravel Sanctum provides a featherweight authentication system for SPAs, mobile applications, and simple, token-based APIs.",
        "categories": ["authentication", "api", "security"],
        "use_cases": [
            "Authenticating SPAs (Single Page Applications)",
            "Authenticating mobile applications",
            "Implementing API token authentication",
            "Creating a secure API"
        ],
        "installation": "composer require laravel/sanctum",
        "documentation_link": "laravel://authentication/sanctum.md"
    },
    "laravel/scout": {
        "name": "Laravel Scout",
        "description": "Laravel Scout provides a simple, driver-based solution for adding full-text search to Eloquent models.",
        "categories": ["search", "database", "indexing"],
        "use_cases": [
            "Adding full-text search to your application",
            "Making Eloquent models searchable",
            "Implementing search with Algolia or Meilisearch",
            "Creating custom search solutions"
        ],
        "installation": "composer require laravel/scout",
        "documentation_link": "laravel://packages/scout.md"
    },
    "laravel/passport": {
        "name": "Laravel Passport",
        "description": "Laravel Passport provides a full OAuth2 server implementation for your Laravel application in a matter of minutes.",
        "categories": ["authentication", "api", "oauth", "security"],
        "use_cases": [
            "Implementing OAuth2 authentication",
            "Creating API authentication with access tokens",
            "Building secure APIs with token scopes",
            "Supporting password grant tokens"
        ],
        "installation": "composer require laravel/passport",
        "documentation_link": "laravel://authentication/passport.md"
    },
    "laravel/breeze": {
        "name": "Laravel Breeze",
        "description": "Laravel Breeze is a minimal, simple implementation of all of Laravel's authentication features, including login, registration, password reset, email verification, and password confirmation.",
        "categories": ["authentication", "frontend", "scaffolding"],
        "use_cases": [
            "Quickly scaffolding authentication views and routes",
            "Setting up a basic Laravel authentication system",
            "Creating a starting point for authentication with Tailwind CSS"
        ],
        "installation": "composer require laravel/breeze --dev",
        "documentation_link": "laravel://starter-kits/breeze.md"
    },
    "livewire/livewire": {
        "name": "Laravel Livewire",
        "description": "Laravel Livewire is a full-stack framework for Laravel that makes building dynamic interfaces simple, without leaving the comfort of Laravel.",
        "categories": ["frontend", "ui", "reactivity"],
        "use_cases": [
            "Building reactive UI components without JavaScript",
            "Creating dynamic forms with real-time validation",
            "Implementing CRUD interfaces with Laravel syntax",
            "Adding interactive elements to Blade templates"
        ],
        "installation": "composer require livewire/livewire",
        "documentation_link": "laravel://livewire.md"
    },
    "laravel/fortify": {
        "name": "Laravel Fortify",
        "description": "Laravel Fortify is a frontend agnostic authentication backend for Laravel that implements many of the features found in Laravel's authentication scaffolding.",
        "categories": ["authentication", "backend", "security"],
        "use_cases": [
            "Implementing authentication without frontend opinions",
            "Building custom authentication UI",
            "Adding two-factor authentication",
            "Setting up email verification"
        ],
        "installation": "composer require laravel/fortify",
        "documentation_link": "laravel://authentication/fortify.md"
    },
    "spatie/laravel-permission": {
        "name": "Spatie Laravel Permission",
        "description": "Laravel Permission provides a way to manage permissions and roles in your Laravel application. It allows you to assign permissions to roles, and then assign roles to users.",
        "categories": ["authorization", "acl", "security", "permissions"],
        "use_cases": [
            "Implementing role-based access control",
            "Managing user permissions",
            "Restricting access to resources and routes",
            "Creating a permission-based authorization system"
        ],
        "installation": "composer require spatie/laravel-permission",
        "documentation_link": "https://spatie.be/docs/laravel-permission"
    },
    "inertiajs/inertia-laravel": {
        "name": "Inertia.js for Laravel",
        "description": "Inertia.js is a framework for creating server-driven single-page apps, allowing you to build fully client-side rendered, single-page apps, without the complexity of modern SPAs.",
        "categories": ["frontend", "spa", "framework"],
        "use_cases": [
            "Building single-page applications with Laravel backend",
            "Creating modern UIs with Vue.js, React, or Svelte",
            "Implementing client-side routing with server-side data",
            "Developing reactive interfaces with Laravel controllers"
        ],
        "installation": "composer require inertiajs/inertia-laravel",
        "documentation_link": "laravel://inertia.md"
    }
}

# Feature map for Laravel packages
FEATURE_MAP = {
    "laravel/cashier": ["subscription", "one-time-payment", "webhook-handling"],
    "laravel/sanctum": ["api-authentication", "token-abilities", "spa-authentication"],
    "laravel/scout": ["basic-search", "meilisearch-setup", "custom-engines"],
    "livewire/livewire": ["basic-component", "form-validation", "real-time-search"],
    "laravel/fortify": ["basic-setup", "two-factor-auth", "email-verification"],
    "laravel/passport": ["oauth-setup", "token-scopes", "client-credentials"],
    "laravel/breeze": ["blade-setup", "react-setup", "vue-setup"],
    "spatie/laravel-permission": ["basic-setup", "role-management", "policies-integration"],
    "inertiajs/inertia-laravel": ["vue-setup", "react-setup", "spa-navigation"]
}

# Tool descriptions for MCP tools
TOOL_DESCRIPTIONS = {
    "list_docs": """A comprehensive documentation indexing tool that provides access to all available Laravel documentation files. Use this tool to get a complete overview of the available documentation landscape before diving into specific topics.

When to use this tool:
- Getting started with Laravel documentation exploration
- Creating a mental map of available resources
- Planning which documentation sections to explore
- Finding specific documentation file names
- Understanding the organization of Laravel documentation""",

    "search_docs": """A powerful search engine for finding specific information across the entire Laravel documentation. This tool allows precise querying to locate exact features, functions, or concepts within the documentation.

When to use this tool:
- Finding specific Laravel functionality or features
- Researching how particular components work
- Locating examples for implementation techniques
- Exploring detailed API references
- Discovering configuration options for Laravel features""",

    "update_docs": """A documentation synchronization tool that ensures you have access to the latest Laravel documentation. This tool can target specific versions and force updates when necessary.

When to use this tool:
- Working with newer Laravel releases
- Ensuring documentation reflects the latest features
- Switching between different Laravel version documentation
- Resolving documentation inconsistencies
- Preparing for Laravel version migrations""",

    "docs_info": """A metadata retrieval tool that provides information about the current documentation version and status. This tool helps understand the context and relevance of the documentation you're exploring.

When to use this tool:
- Verifying documentation version matches your project
- Checking when documentation was last updated
- Understanding which Laravel features are documented
- Assessing documentation completeness
- Planning for potential documentation updates""",

    "get_package_recommendations": """An intelligent recommendation engine that suggests Laravel packages based on implementation needs. This tool analyzes your use case to provide contextually relevant package options.

When to use this tool:
- Starting a new Laravel implementation
- Exploring solutions for specific functionality needs
- Comparing alternative approaches to a problem
- Discovering community-recommended packages
- Finding specialized tools for particular use cases""",

    "get_package_info": """A detailed package analysis tool that provides comprehensive information about specific Laravel packages. This tool helps evaluate packages for your implementation needs.

When to use this tool:
- Researching package capabilities and limitations
- Checking package compatibility with your Laravel version
- Understanding package dependencies and requirements
- Evaluating package maintenance status and community support
- Reviewing package documentation and usage instructions""",

    "get_package_categories": """A categorical exploration tool that organizes Laravel packages by functionality domain. This tool helps discover related packages within specific application areas.

When to use this tool:
- Exploring available options within a functional domain
- Comparing packages that solve similar problems
- Discovering specialized packages for particular needs
- Understanding how Laravel ecosystem addresses specific requirements
- Finding alternatives to currently used packages""",

    "get_features_for_package": """A feature inspection tool that provides detailed information about capabilities available within a specific package. This tool helps understand what a package can do before implementation.

When to use this tool:
- Understanding a package's complete feature set
- Verifying a package meets all your requirements
- Planning implementation based on available features
- Comparing feature sets between similar packages
- Discovering advanced capabilities you might leverage"""
}

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Laravel Documentation and Package Recommendation MCP Server"
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

def search_by_use_case(use_case: str) -> List[Dict]:
    """
    Find packages that match a specific use case description.
    
    Args:
        use_case: Description of what the user wants to implement
        
    Returns:
        List of matching packages
    """
    # Convert to lowercase and tokenize
    words = set(re.findall(r'\b\w+\b', use_case.lower()))
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'to', 'for', 'in', 'with'}
    words = words - stop_words
    
    # Score packages based on matching words
    scores = {}
    for pkg_id, pkg_info in PACKAGE_CATALOG.items():
        score = 0
        
        # Check categories
        for category in pkg_info.get('categories', []):
            if any(word in category.lower() for word in words):
                score += 2
        
        # Check use cases
        for pkg_use_case in pkg_info.get('use_cases', []):
            pkg_use_case_lower = pkg_use_case.lower()
            for word in words:
                if word in pkg_use_case_lower:
                    score += 1
        
        # Check package name and description
        name_desc = (str(pkg_info.get('name', '')) + ' ' + str(pkg_info.get('description', ''))).lower()
        for word in words:
            if word in name_desc:
                score += int(0.5)
        
        if score > 0:
            scores[pkg_id] = score
    
    # Sort by score and return package info
    ranked_packages = []
    for pkg_id, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        appendable_pkg_info: Dict[str, Any] = PACKAGE_CATALOG[pkg_id].copy()
        appendable_pkg_info['id'] = pkg_id
        appendable_pkg_info['score'] = score
        ranked_packages.append(appendable_pkg_info)
    
    return ranked_packages

def format_package_recommendation(package: Dict) -> str:
    """Format a package recommendation as markdown."""
    pkg_id = package.get('id', 'unknown')
    result = [
        f"# {package.get('name', pkg_id)}",
        package.get('description', 'No description available'),
        ""
    ]
    
    # Add use cases
    if 'use_cases' in package:
        result.append("## Use Cases")
        for use_case in package['use_cases']:
            result.append(f"- {use_case}")
        result.append("")
    
    # Add installation
    if 'installation' in package:
        result.append("## Installation")
        result.append(f"```bash\n{package['installation']}\n```")
        result.append("")
    
    # Add features if available in map
    if pkg_id in FEATURE_MAP:
        result.append("## Common Implementations")
        for feature in FEATURE_MAP[pkg_id]:
            result.append(f"- {feature}")
        result.append("")
    
    # Add documentation link
    if 'documentation_link' in package:
        result.append("## Documentation")
        result.append(f"For more information, see: {package['documentation_link']}")
    
    return "\n".join(result)

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
    
    # Register documentation tools
    @mcp.tool(description=TOOL_DESCRIPTIONS["list_docs"])
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
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["search_docs"])
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
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["update_docs"])
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
                return "Documentation update not performed or not needed"
        except Exception as e:
            logger.error(f"Error updating documentation: {str(e)}")
            return f"Error updating documentation: {str(e)}"
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["docs_info"])
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
    
    # Register package recommendation tools
    @mcp.tool(description=TOOL_DESCRIPTIONS["get_package_recommendations"])
    def get_package_recommendations(use_case: str) -> str:
        """
        Get Laravel package recommendations based on a use case.
        
        Args:
            use_case: Description of what the user wants to implement
            
        Returns:
            Markdown-formatted package recommendations
        """
        logger.info(f"Searching for packages matching use case: {use_case}")
        
        # Search for packages by use case
        packages = search_by_use_case(use_case)
        
        if not packages:
            return f"No packages found matching the use case: '{use_case}'"
        
        # Format the results
        results = [f"# Laravel Packages for: {use_case}"]
        
        for i, package in enumerate(packages[:3]):  # Limit to top 3 matches
            results.append(f"\n## {i+1}. {package.get('name', package.get('id', 'Unknown Package'))}")
            results.append(f"{package.get('description', 'No description available')}")
            
            # Add use cases section
            results.append("\n**Use Cases:**")
            for use_case_item in package.get('use_cases', []):
                results.append(f"- {use_case_item}")
            
            # Add installation instructions
            if 'installation' in package:
                results.append("\n**Installation:**")
                results.append(f"```bash\n{package['installation']}\n```")
            
            # Add documentation link
            if 'documentation_link' in package:
                results.append("\n**Documentation:**")
                results.append(f"For more information, see: {package['documentation_link']}")
        
        return "\n".join(results)
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["get_package_info"])
    def get_package_info(package_name: str) -> str:
        """
        Get detailed information about a specific Laravel package.
        
        Args:
            package_name: The name of the package (e.g., 'laravel/cashier')
            
        Returns:
            Markdown-formatted package information
        """
        logger.info(f"Getting information for package: {package_name}")
        
        # Get the package information
        if package_name not in PACKAGE_CATALOG:
            return f"Package '{package_name}' not found"
        
        package = PACKAGE_CATALOG[package_name].copy()
        package['id'] = package_name
        
        # Format the package information as markdown
        return format_package_recommendation(package)
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["get_package_categories"])
    def get_package_categories(category: str) -> str:
        """
        Get Laravel packages in a specific category.
        
        Args:
            category: The category to filter by (e.g., 'authentication', 'payment')
            
        Returns:
            Markdown-formatted list of packages in the category
        """
        logger.info(f"Getting packages for category: {category}")
        
        # Find packages in the category
        matches = []
        category_lower = category.lower()
        
        for pkg_id, pkg_info in PACKAGE_CATALOG.items():
            if any(cat.lower() == category_lower for cat in pkg_info.get('categories', [])):
                pkg = pkg_info.copy()
                pkg['id'] = pkg_id
                matches.append(pkg)
        
        if not matches:
            return f"No packages found in category: '{category}'"
        
        # Format the results
        results = [f"# Laravel Packages for Category: {category}"]
        
        for i, package in enumerate(matches):
            results.append(f"\n## {i+1}. {package.get('name', package.get('id', 'Unknown Package'))}")
            results.append(f"{package.get('description', 'No description available')}")
            
            # Add installation instructions
            if 'installation' in package:
                results.append("\n**Installation:**")
                results.append(f"```bash\n{package['installation']}\n```")
            
            # Add documentation link
            if 'documentation_link' in package:
                results.append("\n**Documentation:**")
                results.append(f"For more information, see: {package['documentation_link']}")
        
        return "\n".join(results)
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["get_features_for_package"])
    def get_features_for_package(package: str) -> str:
        """
        Get available features/implementations for a Laravel package.
        
        Args:
            package: The Laravel package name (e.g., 'laravel/cashier')
            
        Returns:
            Markdown-formatted list of features
        """
        logger.info(f"Getting features for package: {package}")
        
        # Check if the package exists
        if package not in PACKAGE_CATALOG:
            return f"Package '{package}' not found"
        
        # Get features from the feature map
        features = FEATURE_MAP.get(package, [])
        
        if not features:
            return f"No specific features listed for {package}"
        
        # Format the results
        package_info = PACKAGE_CATALOG[package]
        results = [f"# Implementation Features for {package_info.get('name', package)}"]
        
        results.append("\nThe following implementation features are commonly needed:")
        
        for i, feature in enumerate(features):
            results.append(f"\n## {i+1}. {feature}")
            results.append("The AI can generate example code for this implementation based on best practices.")
        
        return "\n".join(results)
    
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