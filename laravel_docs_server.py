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
from docs_updater import DocsUpdater, get_cached_supported_versions, DEFAULT_VERSION
from shutdown_handler import GracefulShutdown

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("laravel-docs-mcp")

# Get supported versions
SUPPORTED_VERSIONS = get_cached_supported_versions()

# Define the Laravel package catalog
# Updated PACKAGE_CATALOG with more Laravel packages
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
    },
    "laravel/horizon": {
        "name": "Laravel Horizon",
        "description": "Laravel Horizon provides a beautiful dashboard and code-driven configuration for your Redis queues. Horizon allows you to easily monitor key metrics of your queue system.",
        "categories": ["queue", "monitoring", "redis", "dashboard"],
        "use_cases": [
            "Monitoring Redis queue performance",
            "Managing queue workers and jobs",
            "Tracking job failures and retries",
            "Visualizing queue throughput and wait times"
        ],
        "installation": "composer require laravel/horizon",
        "documentation_link": "laravel://horizon.md"
    },
    "laravel/telescope": {
        "name": "Laravel Telescope",
        "description": "Laravel Telescope makes a wonderful companion to your local Laravel development environment. Telescope provides insight into the requests, exceptions, database queries, queued jobs, mail, notifications, cache operations, scheduled tasks, variable dumps, and more.",
        "categories": ["debugging", "monitoring", "development", "dashboard"],
        "use_cases": [
            "Debugging application requests and responses",
            "Monitoring database queries and performance",
            "Tracking exceptions and logs",
            "Inspecting queued jobs and mail"
        ],
        "installation": "composer require laravel/telescope --dev",
        "documentation_link": "laravel://telescope.md"
    },
    "laravel/jetstream": {
        "name": "Laravel Jetstream",
        "description": "Laravel Jetstream is a beautifully designed application starter kit for Laravel and provides the perfect starting point for your next Laravel application. Jetstream provides the implementation for your application's login, registration, email verification, two-factor authentication, session management, API via Laravel Sanctum, and optional team management features.",
        "categories": ["authentication", "frontend", "scaffolding", "teams"],
        "use_cases": [
            "Building applications with team support",
            "Implementing two-factor authentication",
            "Creating API tokens for users",
            "Setting up profile management"
        ],
        "installation": "composer require laravel/jetstream",
        "documentation_link": "laravel://starter-kits/jetstream.md"
    },
    "laravel/octane": {
        "name": "Laravel Octane",
        "description": "Laravel Octane supercharges your application's performance by serving your application using high-powered application servers, including Swoole and RoadRunner.",
        "categories": ["performance", "server", "optimization"],
        "use_cases": [
            "Dramatically improving application performance",
            "Running Laravel with persistent application state",
            "Handling thousands of requests per second",
            "Reducing server costs through efficiency"
        ],
        "installation": "composer require laravel/octane",
        "documentation_link": "laravel://octane.md"
    },
    "laravel/socialite": {
        "name": "Laravel Socialite",
        "description": "Laravel Socialite provides an expressive, fluent interface to OAuth authentication with Facebook, Twitter, Google, LinkedIn, GitHub, GitLab, and Bitbucket.",
        "categories": ["authentication", "oauth", "social"],
        "use_cases": [
            "Implementing social login (Google, Facebook, etc.)",
            "OAuth authentication with third-party providers",
            "Simplifying social media integration",
            "User registration via social accounts"
        ],
        "installation": "composer require laravel/socialite",
        "documentation_link": "laravel://socialite.md"
    },
    "spatie/laravel-medialibrary": {
        "name": "Spatie Media Library",
        "description": "This package can associate all sorts of media files with Eloquent models. It provides a simple API to work with.",
        "categories": ["media", "files", "uploads", "storage"],
        "use_cases": [
            "Managing file uploads and attachments",
            "Creating image thumbnails and conversions",
            "Organizing media collections",
            "Handling file storage across different disks"
        ],
        "installation": "composer require spatie/laravel-medialibrary",
        "documentation_link": "https://spatie.be/docs/laravel-medialibrary"
    },
    "laravel/excel": {
        "name": "Laravel Excel (Maatwebsite)",
        "description": "Supercharged Excel exports and imports in Laravel. A simple, but elegant Laravel wrapper around PhpSpreadsheet exports and imports.",
        "categories": ["excel", "export", "import", "files"],
        "use_cases": [
            "Exporting data to Excel files",
            "Importing Excel data into database",
            "Generating complex Excel reports",
            "Processing CSV files"
        ],
        "installation": "composer require maatwebsite/excel",
        "documentation_link": "https://laravel-excel.com"
    },
    "barryvdh/laravel-debugbar": {
        "name": "Laravel Debugbar",
        "description": "This is a package to integrate PHP Debug Bar with Laravel. It includes a ServiceProvider to register the debugbar and attach it to the output.",
        "categories": ["debugging", "development", "profiling"],
        "use_cases": [
            "Debugging database queries",
            "Profiling application performance",
            "Inspecting views and route information",
            "Monitoring memory usage"
        ],
        "installation": "composer require barryvdh/laravel-debugbar --dev",
        "documentation_link": "https://github.com/barryvdh/laravel-debugbar"
    },
    "laravel/cashier-paddle": {
        "name": "Laravel Cashier Paddle",
        "description": "Laravel Cashier Paddle provides an expressive, fluent interface to Paddle's subscription billing services.",
        "categories": ["payment", "billing", "subscription"],
        "use_cases": [
            "Implementing Paddle payment integration",
            "Managing SaaS subscriptions",
            "Handling international payments and taxes",
            "Processing one-time purchases"
        ],
        "installation": "composer require laravel/cashier-paddle",
        "documentation_link": "laravel://billing.md#paddle-billing"
    }
}

# Updated FEATURE_MAP with more implementation details
FEATURE_MAP = {
    "laravel/cashier": ["subscription-setup", "one-time-payments", "webhook-handling", "subscription-swapping", "trial-periods", "invoice-generation"],
    "laravel/sanctum": ["spa-authentication", "api-tokens", "token-abilities", "mobile-auth", "token-revocation"],
    "laravel/scout": ["basic-search", "algolia-driver", "meilisearch-driver", "custom-engines", "search-filters", "pagination"],
    "livewire/livewire": ["components", "data-binding", "actions", "validation", "file-uploads", "polling", "events"],
    "laravel/fortify": ["login", "registration", "password-reset", "email-verification", "two-factor-auth", "profile-update"],
    "laravel/passport": ["oauth-server", "password-grant", "client-credentials", "authorization-code", "token-scopes", "personal-tokens"],
    "laravel/breeze": ["blade-views", "react-setup", "vue-setup", "inertia-setup", "api-setup", "dark-mode"],
    "spatie/laravel-permission": ["roles", "permissions", "direct-permissions", "role-hierarchy", "middleware", "blade-directives"],
    "inertiajs/inertia-laravel": ["setup", "routing", "shared-data", "asset-versioning", "ssr", "form-helper"],
    "laravel/horizon": ["configuration", "metrics", "failed-jobs", "job-retries", "tags", "notifications"],
    "laravel/telescope": ["entries", "filtering", "pruning", "authorization", "custom-watchers"],
    "laravel/jetstream": ["profile", "api-tokens", "teams", "team-permissions", "billing-integration"],
    "laravel/octane": ["swoole-setup", "roadrunner-setup", "state-management", "concurrent-tasks", "cache-optimization"],
    "laravel/socialite": ["provider-setup", "scopes", "optional-parameters", "stateless-auth", "custom-providers"],
    "spatie/laravel-medialibrary": ["conversions", "collections", "s3-upload", "responsive-images", "media-streams"],
    "laravel/excel": ["exports", "imports", "queued-exports", "multiple-sheets", "csv-handling", "styling"],
    "barryvdh/laravel-debugbar": ["query-debugging", "timeline", "exceptions", "views-data", "route-info"]
}

# Updated TOOL_DESCRIPTIONS with new tools
TOOL_DESCRIPTIONS = {
    "list_laravel_docs": """Lists all available Laravel documentation files across versions. Essential for discovering what documentation exists before diving into specific topics.

When to use:
- Initial exploration of Laravel documentation
- Finding available documentation files
- Checking which versions have specific documentation
- Getting an overview of documentation coverage""",

    "read_laravel_doc_content": """Reads the complete content of a specific Laravel documentation file. This is the primary tool for accessing actual documentation content.

When to use:
- Reading full documentation for a feature
- Getting complete implementation details
- Accessing code examples from docs
- Understanding concepts in depth""",

    "search_laravel_docs": """Searches for specific terms across all Laravel documentation files. Returns file names and match counts.

When to use:
- Finding which files mention a specific feature
- Quick lookup of where topics are discussed
- Discovering related documentation files""",

    "search_laravel_docs_with_context": """Advanced search that returns matching text with surrounding context. Shows exactly how terms are used in documentation.

When to use:
- Understanding how a feature is described
- Finding specific code examples
- Getting quick answers without reading full files
- Seeing usage context for technical terms""",

    "get_doc_structure": """Extracts the table of contents and structure from a documentation file. Shows headers and brief content previews.

When to use:
- Understanding document organization
- Finding specific sections within large files
- Getting a quick overview before deep reading
- Navigating to relevant parts of documentation""",

    "browse_docs_by_category": """Discovers documentation files related to specific categories like 'frontend', 'database', or 'authentication'.

When to use:
- Exploring all docs for a particular domain
- Finding related documentation files
- Learning about category-specific features
- Discovering documentation you didn't know existed""",

    "update_laravel_docs": """Updates documentation from the official Laravel GitHub repository. Ensures access to the latest documentation changes.

When to use:
- Working with newly released Laravel versions
- Ensuring documentation is current
- Resolving missing documentation issues
- Syncing after Laravel updates""",

    "laravel_docs_info": """Provides metadata about documentation versions, including last update times and commit information.

When to use:
- Checking documentation freshness
- Verifying version compatibility
- Understanding documentation state
- Troubleshooting sync issues""",

    "get_laravel_package_recommendations": """Intelligently recommends Laravel packages based on described use cases or implementation needs.

When to use:
- Starting new feature implementation
- Finding packages for specific functionality
- Discovering ecosystem solutions
- Comparing implementation approaches""",

    "get_laravel_package_info": """Provides comprehensive details about a specific Laravel package including installation and use cases.

When to use:
- Learning about a specific package
- Getting installation instructions
- Understanding package capabilities
- Checking package categories""",

    "get_laravel_package_categories": """Lists all packages within a specific functional category.

When to use:
- Exploring packages by domain
- Comparing similar packages
- Finding category-specific solutions
- Discovering package alternatives""",

    "get_features_for_laravel_package": """Details common implementation features and patterns for a specific package.

When to use:
- Planning package implementation
- Understanding feature scope
- Learning implementation patterns
- Discovering package capabilities"""
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
        default=DEFAULT_VERSION,
        help=f"Laravel version branch to use (default: {DEFAULT_VERSION}). Supported: {', '.join(SUPPORTED_VERSIONS)}"
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

def get_version_from_path(path: str) -> tuple[str, str]:
    """Extract version and relative path from a documentation path.
    
    Args:
        path: Path like "12.x/blade.md" or "blade.md"
        
    Returns:
        (version, relative_path): Tuple of version and path within that version
    """
    path_parts = Path(path).parts
    
    # Check if first part is a version
    if path_parts and path_parts[0] in SUPPORTED_VERSIONS:
        version = path_parts[0]
        relative_path = str(Path(*path_parts[1:]))
        return version, relative_path
    
    # Default to latest version if no version specified
    return DEFAULT_VERSION, path

def get_laravel_docs_metadata(docs_path: Path, version: Optional[str] = None) -> Dict:
    """Get documentation metadata if available."""
    if version:
        metadata_file = docs_path / version / ".metadata" / "sync_info.json"
    else:
        # Try to find any version metadata
        for v in SUPPORTED_VERSIONS:
            metadata_file = docs_path / v / ".metadata" / "sync_info.json"
            if metadata_file.exists():
                break
        else:
            return {"status": "unknown", "message": "No metadata available"}
    
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
    
    # Validate version
    if args.version not in SUPPORTED_VERSIONS:
        logger.error(f"Unsupported version: {args.version}. Supported versions: {', '.join(SUPPORTED_VERSIONS)}")
        sys.exit(1)
    
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
    @mcp.tool(description=TOOL_DESCRIPTIONS["list_laravel_docs"])
    def list_laravel_docs(version: Optional[str] = None) -> str:
        """List all available Laravel documentation files.
        
        Args:
            version: Specific Laravel version to list (e.g., "12.x"). If not provided, lists all versions.
        """
        logger.debug(f"list_laravel_docs function called (version: {version})")
        result = []
        
        try:
            if version:
                # List docs for specific version
                version_path = docs_path / version
                if not version_path.exists():
                    return f"No documentation found for version {version}. Use update_laravel_docs() to fetch documentation."
                
                # Add metadata if available
                metadata = get_laravel_docs_metadata(docs_path, version)
                if metadata.get("version"):
                    result.append(f"Laravel Documentation (Version: {metadata['version']})")
                    result.append(f"Last updated: {metadata.get('sync_time', 'unknown')}")
                    result.append(f"Commit: {metadata.get('commit_sha', 'unknown')[:7]}")
                    result.append("")
                
                # List markdown files in this version
                md_files = [f for f in os.listdir(version_path) if f.endswith('.md')]
                if md_files:
                    result.append(f"Files in {version}:")
                    for file in sorted(md_files):
                        result.append(f"  {file}")
                else:
                    result.append(f"No documentation files found in version {version}")
            else:
                # List all versions and their files
                available_versions = []
                for v in SUPPORTED_VERSIONS:
                    version_path = docs_path / v
                    if version_path.exists() and any(f.endswith('.md') for f in os.listdir(version_path) if os.path.isfile(version_path / f)):
                        available_versions.append(v)
                
                if not available_versions:
                    return "No documentation files found. Use update_laravel_docs() to fetch documentation."
                
                result.append("Available Laravel Documentation Versions:")
                result.append("")
                
                for v in available_versions:
                    version_path = docs_path / v
                    metadata = get_laravel_docs_metadata(docs_path, v)
                    
                    result.append(f"## Version {v}")
                    if metadata.get('sync_time'):
                        result.append(f"Last updated: {metadata.get('sync_time', 'unknown')}")
                        result.append(f"Commit: {metadata.get('commit_sha', 'unknown')[:7]}")
                    
                    md_files = [f for f in os.listdir(version_path) if f.endswith('.md')]
                    result.append(f"Files: {len(md_files)} documentation files")
                    result.append("")
            
            return "\n".join(result) if result else "No documentation files found"
        except Exception as e:
            logger.error(f"Error listing documentation files: {str(e)}")
            return f"Error listing documentation files: {str(e)}"
    
    @mcp.resource("laravel://{path}")
    def read_laravel_doc(path: str) -> str:
        """Read a specific Laravel documentation file.
        
        Args:
            path: Path like "12.x/blade.md" or "blade.md" (defaults to latest version)
        """
        logger.debug(f"read_laravel_doc function called with path: {path}")
        
        # Extract version and relative path
        version, relative_path = get_version_from_path(path)
        
        # Make sure the path ends with .md
        if not relative_path.endswith('.md'):
            relative_path = f"{relative_path}.md"
        
        file_path = docs_path / version / relative_path
        
        # Security check - ensure we stay within version directory
        version_path = docs_path / version
        if not is_safe_path(version_path, file_path):
            logger.warning(f"Access denied: {path} (attempted directory traversal)")
            return f"Access denied: {path} (attempted directory traversal)"
        
        if not file_path.exists():
            logger.warning(f"Documentation file not found: {file_path}")
            return f"Documentation file not found: {path} (version: {version})"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.debug(f"Successfully read file: {file_path} ({len(content)} bytes)")
                return content
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return f"Error reading file: {str(e)}"
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["search_laravel_docs"])
    def search_laravel_docs(query: str, version: Optional[str] = None) -> str:
        """Search through Laravel documentation for a specific term.
        
        Args:
            query: Search term to look for
            version: Specific Laravel version to search (e.g., "12.x"). If not provided, searches all versions.
        """
        logger.debug(f"search_laravel_docs function called with query: {query}, version: {version}")
        
        if not query.strip():
            return "Search query cannot be empty"
        
        results = []
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        
        try:
            search_versions = [version] if version else SUPPORTED_VERSIONS
            
            for v in search_versions:
                version_path = docs_path / v
                if not version_path.exists():
                    continue
                
                for file in os.listdir(version_path):
                    if file.endswith('.md'):
                        file_path = version_path / file
                        
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if pattern.search(content):
                                count = len(pattern.findall(content))
                                results.append(f"{v}/{file} ({count} matches)")
            
            if results:
                return f"Found {len(results)} files containing '{query}':\n" + "\n".join(results)
            else:
                search_scope = f"version {version}" if version else "all versions"
                return f"No results found for '{query}' in {search_scope}"
        except Exception as e:
            logger.error(f"Error searching documentation: {str(e)}")
            return f"Error searching documentation: {str(e)}"
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["update_laravel_docs"])
    def update_laravel_docs(version: Optional[str] = None, force: bool = False) -> str:
        """
        Update Laravel documentation from official GitHub repository.
        
        Args:
            version: Laravel version branch (e.g., "12.x")
            force: Force update even if already up to date
        """
        logger.debug(f"update_laravel_docs function called (version: {version}, force: {force})")
        
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
                metadata = get_laravel_docs_metadata(docs_path, doc_version)
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
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["laravel_docs_info"])
    def laravel_docs_info(version: Optional[str] = None) -> str:
        """Get information about the documentation version and status.
        
        Args:
            version: Specific Laravel version to get info for (e.g., "12.x"). If not provided, shows all versions.
        """
        logger.debug(f"laravel_docs_info function called (version: {version})")
        
        if version:
            metadata = get_laravel_docs_metadata(docs_path, version)
            
            if "version" not in metadata:
                return f"No documentation metadata available for version {version}. Use update_laravel_docs() to fetch documentation."
            
            return (
                f"Laravel Documentation (Version {version})\n"
                f"Last updated: {metadata.get('sync_time', 'unknown')}\n"
                f"Commit SHA: {metadata.get('commit_sha', 'unknown')}\n"
                f"Commit date: {metadata.get('commit_date', 'unknown')}\n"
                f"Commit message: {metadata.get('commit_message', 'unknown')}\n"
                f"GitHub URL: {metadata.get('commit_url', 'unknown')}"
            )
        else:
            # Show info for all available versions
            result = ["Laravel Documentation Status\n"]
            
            for v in SUPPORTED_VERSIONS:
                metadata = get_laravel_docs_metadata(docs_path, v)
                if "version" in metadata:
                    result.append(f"## Version {v}")
                    result.append(f"Last updated: {metadata.get('sync_time', 'unknown')}")
                    result.append(f"Commit: {metadata.get('commit_sha', 'unknown')[:7]}")
                    result.append(f"Commit date: {metadata.get('commit_date', 'unknown')}")
                    result.append("")
                else:
                    result.append(f"## Version {v}")
                    result.append("Not available (use update_laravel_docs() to fetch)")
                    result.append("")
            
            return "\n".join(result)
    
    # Register package recommendation tools
    @mcp.tool(description=TOOL_DESCRIPTIONS["get_laravel_package_recommendations"])
    def get_laravel_package_recommendations(use_case: str) -> str:
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
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["get_laravel_package_info"])
    def get_laravel_package_info(package_name: str) -> str:
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
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["get_laravel_package_categories"])
    def get_laravel_package_categories(category: str) -> str:
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
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["get_features_for_laravel_package"])
    def get_features_for_laravel_package(package: str) -> str:
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

    @mcp.tool(description="Read the full content of a specific Laravel documentation file")
    def read_laravel_doc_content(filename: str, version: Optional[str] = None) -> str:
        """
        Read a specific Laravel documentation file.
        
        Args:
            filename: Name of the file (e.g., 'mix.md', 'vite.md')
            version: Laravel version (e.g., '12.x'). Defaults to latest.
        
        Returns:
            Full markdown content of the documentation file
        """
        logger.debug(f"read_laravel_doc_content called: {filename}, version: {version}")
        
        if not version:
            version = DEFAULT_VERSION
        
        if not filename.endswith('.md'):
            filename = f"{filename}.md"
        
        file_path = docs_path / version / filename
        
        version_path = docs_path / version
        if not is_safe_path(version_path, file_path):
            return f"Access denied: {filename}"
        
        if not file_path.exists():
            # Try to list available files to help the user
            available = [f for f in os.listdir(version_path) if f.endswith('.md')][:10]
            return f"File not found: {filename} in version {version}. Available files: {', '.join(available)}..."
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return f"Error reading file: {str(e)}"


    @mcp.tool(description="Search Laravel docs with context snippets")
    def search_laravel_docs_with_context(
        query: str, 
        version: Optional[str] = None,
        context_length: int = 200
    ) -> str:
        """
        Search through Laravel documentation with context snippets.
        
        Args:
            query: Search term
            version: Specific version or None for all
            context_length: Characters of context to show (default: 200)
        
        Returns:
            Search results with context snippets
        """
        logger.debug(f"search_with_context: query={query}, version={version}")
        
        if not query.strip():
            return "Search query cannot be empty"
        
        results = []
        patterns = [
            re.compile(r'\b' + re.escape(query) + r'\b', re.IGNORECASE),  # Exact word
            re.compile(re.escape(query), re.IGNORECASE)  # Substring match
        ]
        
        search_versions = [version] if version else SUPPORTED_VERSIONS
        
        for v in search_versions:
            version_path = docs_path / v
            if not version_path.exists():
                continue
            
            for file in os.listdir(version_path):
                if not file.endswith('.md'):
                    continue
                    
                file_path = version_path / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Try patterns in order
                    matches = []
                    for pattern in patterns:
                        for match in pattern.finditer(content):
                            start = max(0, match.start() - context_length // 2)
                            end = min(len(content), match.end() + context_length // 2)
                            
                            # Find line boundaries for cleaner snippets
                            while start > 0 and content[start] not in '\n.!?':
                                start -= 1
                            while end < len(content) and content[end] not in '\n.!?':
                                end += 1
                            
                            snippet = content[start:end].strip()
                            # Highlight the match
                            snippet = pattern.sub(f"**{match.group()}**", snippet)
                            
                            matches.append({
                                'line': content[:match.start()].count('\n') + 1,
                                'snippet': snippet
                            })
                            
                            if len(matches) >= 3:  # Limit matches per file
                                break
                        
                        if matches:
                            break
                    
                    if matches:
                        results.append({
                            'file': f"{v}/{file}",
                            'matches': matches
                        })
                        
                except Exception as e:
                    logger.error(f"Error searching {file_path}: {str(e)}")
        
        # Format results
        if not results:
            return f"No results found for '{query}'"
        
        output = [f"Found '{query}' in {len(results)} files:\n"]
        
        for result in results[:10]:  # Limit total results
            output.append(f"## {result['file']}")
            for i, match in enumerate(result['matches'][:2]):  # Show first 2 matches
                output.append(f"\nLine {match['line']}:")
                output.append(f"...{match['snippet']}...")
            output.append("")
        
        return "\n".join(output)


    @mcp.tool(description="Get the structure and sections of a documentation file")
    def get_doc_structure(filename: str, version: Optional[str] = None) -> str:
        """
        Get the table of contents / structure of a documentation file.
        
        Args:
            filename: Documentation file name
            version: Laravel version
        
        Returns:
            Structured outline of the document
        """
        content = read_laravel_doc_content(filename, version)
        if content.startswith("Error") or content.startswith("File not found"):
            return content
        
        lines = content.split('\n')
        structure = []
        current_section = []
        
        for line in lines:
            if line.startswith('#'):
                # Extract header
                level = len(line) - len(line.lstrip('#'))
                header = line.strip('#').strip()
                indent = "  " * (level - 1)
                structure.append(f"{indent}- {header}")
                
                # Get first paragraph after header as preview
                for next_line in lines[lines.index(line)+1:]:
                    if next_line.strip() and not next_line.startswith('#'):
                        preview = next_line.strip()[:100]
                        if len(next_line.strip()) > 100:
                            preview += "..."
                        structure.append(f"{indent}  {preview}")
                        break
        
        return f"Structure of {filename}:\n\n" + "\n".join(structure)


    def fuzzy_search(query: str, text: str, threshold: float = 0.6) -> List[Dict]:
        """
        Simple fuzzy search implementation.
        Returns matches with similarity scores.
        """
        from difflib import SequenceMatcher
        
        query_lower = query.lower()
        text_lower = text.lower()
        words = text_lower.split()
        matches = []
        
        # Check each word in the text
        for i, word in enumerate(words):
            similarity = SequenceMatcher(None, query_lower, word).ratio()
            if similarity >= threshold:
                # Get context around the match
                start = max(0, i - 10)
                end = min(len(words), i + 10)
                context = ' '.join(words[start:end])
                
                matches.append({
                    'score': similarity,
                    'word': word,
                    'context': context,
                    'position': sum(len(w) + 1 for w in words[:i])
                })
        
        # Also check for multi-word matches
        query_words = query_lower.split()
        if len(query_words) > 1:
            for i in range(len(words) - len(query_words) + 1):
                phrase = ' '.join(words[i:i+len(query_words)])
                similarity = SequenceMatcher(None, query_lower, phrase).ratio()
                if similarity >= threshold:
                    start = max(0, i - 5)
                    end = min(len(words), i + len(query_words) + 5)
                    context = ' '.join(words[start:end])
                    
                    matches.append({
                        'score': similarity,
                        'word': phrase,
                        'context': context,
                        'position': sum(len(w) + 1 for w in words[:i])
                    })
        
        return sorted(matches, key=lambda x: x['score'], reverse=True)


    @mcp.tool(description="Browse Laravel documentation by category")
    def browse_docs_by_category(category: str, version: Optional[str] = None) -> str:
        """
        Browse documentation files by category.
        
        Args:
            category: Category like 'frontend', 'database', 'authentication', etc.
            version: Laravel version
        
        Returns:
            List of relevant documentation files
        """
        # Category mappings
        categories = {
            'frontend': ['vite', 'mix', 'blade', 'frontend', 'asset', 'css', 'javascript'],
            'database': ['eloquent', 'database', 'migrations', 'seeding', 'query'],
            'authentication': ['authentication', 'authorization', 'sanctum', 'passport', 'fortify'],
            'api': ['api', 'sanctum', 'passport', 'routes', 'controllers'],
            'testing': ['testing', 'dusk', 'mocking', 'http-tests'],
            'deployment': ['deployment', 'forge', 'vapor', 'octane'],
        }
        
        # Find relevant keywords for the category
        keywords = categories.get(category.lower(), [category.lower()])
        
        version = version or DEFAULT_VERSION
        version_path = docs_path / version
        
        if not version_path.exists():
            return f"Documentation not found for version {version}"
        
        relevant_files = []
        
        for file in os.listdir(version_path):
            if not file.endswith('.md'):
                continue
            
            # Check if filename matches any keyword
            file_lower = file.lower()
            if any(keyword in file_lower for keyword in keywords):
                # Get first few lines as description
                file_path = version_path / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()[:10]
                        description = ""
                        for line in lines:
                            if line.strip() and not line.startswith('#'):
                                description = line.strip()[:150]
                                if len(line.strip()) > 150:
                                    description += "..."
                                break
                        
                        relevant_files.append({
                            'file': file,
                            'description': description
                        })
                except:
                    relevant_files.append({'file': file, 'description': 'Unable to read description'})
        
        if not relevant_files:
            return f"No documentation found for category '{category}' in version {version}"
        
        output = [f"Documentation for '{category}' in Laravel {version}:\n"]
        for item in relevant_files:
            output.append(f"**{item['file']}**")
            if item['description']:
                output.append(f"  {item['description']}")
            output.append("")
        
        return "\n".join(output)
        
    # Log server startup
    logger.info(f"Starting Laravel Docs MCP Server ({args.server_name})")
    logger.info(f"Transport: {args.transport}")
    logger.info(f"Supported Laravel versions: {', '.join(SUPPORTED_VERSIONS)}")
    
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