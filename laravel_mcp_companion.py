#!/usr/bin/env python3
"""
Laravel MCP Companion

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
from functools import lru_cache
import threading
from fastmcp import FastMCP

# Import documentation updater
from docs_updater import DocsUpdater, MultiSourceDocsUpdater, get_cached_supported_versions, DEFAULT_VERSION
from shutdown_handler import GracefulShutdown

# Import standalone MCP tool implementations
from mcp_tools import (
    list_laravel_docs_impl,
    read_laravel_doc_content_impl,
    search_laravel_docs_impl,
    search_laravel_docs_with_context_impl,
    get_doc_structure_impl,
    browse_docs_by_category_impl
)

# Import learning resources components
from learning_resources import (
    LearningResourceFetcher,
    ResourceType,
    DifficultyLevel,
    ResourceSource
)
from navigation_engine import (
    NavigationMapper,
    PackageCombinationGuide,
    SetupOrchestrator
)
from content_aggregators import ContentAggregatorManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("laravel-mcp-companion")

# Get supported versions
SUPPORTED_VERSIONS = get_cached_supported_versions()

# Global caches for performance optimization
_file_content_cache: Dict[str, str] = {}
_search_result_cache: Dict[str, str] = {}
_cache_lock = threading.Lock()

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
    },
    "laravel/forge": {
        "name": "Laravel Forge",
        "description": "Laravel Forge is a server management and site deployment service. Provision and deploy unlimited PHP applications on DigitalOcean, Linode, Vultr, Amazon, Hetzner and more.",
        "categories": ["deployment", "server-management", "devops", "hosting"],
        "use_cases": [
            "Automated server provisioning and management",
            "Zero-downtime application deployments",
            "SSL certificate management and renewal",
            "Database and queue management",
            "Server monitoring and backups",
            "Team collaboration on server management"
        ],
        "installation": "Web service - No installation required",
        "documentation_link": "laravel-external://forge/introduction"
    },
    "laravel/vapor": {
        "name": "Laravel Vapor",
        "description": "Laravel Vapor is a serverless deployment platform for Laravel, powered by AWS Lambda. Deploy infinitely scalable Laravel applications without managing servers.",
        "categories": ["deployment", "serverless", "aws", "scaling"],
        "use_cases": [
            "Serverless Laravel application deployment",
            "Auto-scaling based on traffic",
            "Cost-effective hosting for variable workloads",
            "Global content distribution",
            "Database and queue management on AWS",
            "CI/CD integration for serverless apps"
        ],
        "installation": "Web service - No installation required",
        "documentation_link": "laravel-external://vapor/introduction"
    },
    "laravel/envoyer": {
        "name": "Laravel Envoyer",
        "description": "Laravel Envoyer provides zero-downtime deployment for PHP applications. Deploy your code without bringing your application offline.",
        "categories": ["deployment", "ci-cd", "automation"],
        "use_cases": [
            "Zero-downtime application deployments",
            "Automated deployment pipelines",
            "Rollback capabilities for failed deployments",
            "Integration with GitHub, GitLab, and Bitbucket",
            "Team deployment management",
            "Deployment notifications and monitoring"
        ],
        "installation": "Web service - No installation required",
        "documentation_link": "laravel-external://envoyer/introduction"
    },
    "laravel/nova": {
        "name": "Laravel Nova",
        "description": "Laravel Nova is a beautifully designed administration panel for Laravel. Carefully crafted by the creators of Laravel to make you the most productive developer in the galaxy.",
        "categories": ["admin", "dashboard", "cms", "backend"],
        "use_cases": [
            "Building administrative dashboards",
            "Managing application data with elegant interfaces",
            "Creating custom admin tools and workflows",
            "User and permission management",
            "Content management systems",
            "Business intelligence and reporting"
        ],
        "installation": "composer require laravel/nova",
        "documentation_link": "laravel-external://nova/installation"
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
    "barryvdh/laravel-debugbar": ["query-debugging", "timeline", "exceptions", "views-data", "route-info"],
    "laravel/forge": ["server-provisioning", "site-deployment", "ssl-management", "database-management", "queue-management", "backups", "monitoring"],
    "laravel/vapor": ["serverless-deployment", "environment-management", "database-setup", "queue-configuration", "storage-management", "cli-deployment"],
    "laravel/envoyer": ["deployment-setup", "zero-downtime-deployment", "rollback", "notifications", "heartbeats", "team-management"],
    "laravel/nova": ["resource-management", "custom-fields", "actions", "filters", "lenses", "metrics", "authorization"]
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
- Discovering package capabilities""",

    "update_external_laravel_docs": """Updates documentation for external Laravel services like Forge, Vapor, Envoyer, and Nova.

When to use:
- Fetching latest Laravel service documentation
- Accessing official Laravel service guides
- Getting documentation for Laravel hosting/deployment services
- Updating cached external documentation""",

    "list_laravel_services": """Lists all available Laravel services with external documentation support.

When to use:
- Discovering available Laravel services
- Finding external documentation sources
- Understanding Laravel ecosystem services
- Checking service documentation availability""",

    "search_external_laravel_docs": """Searches through external Laravel service documentation.

When to use:
- Finding specific information in service docs
- Searching across multiple Laravel services
- Looking for deployment or hosting guidance
- Finding service-specific features""",

    "get_laravel_service_info": """Provides detailed information about a specific Laravel service.

When to use:
- Learning about a specific Laravel service
- Getting service documentation overview
- Understanding service capabilities
- Checking service documentation status""",

    "discover_laravel_learning_resources": """Find Laravel-specific tutorials, articles, and guides for a given topic.

When to use:
- Looking for tutorials on a specific Laravel feature
- Finding learning materials for beginners
- Discovering community articles and blog posts
- Getting curated learning paths""",

    "get_laravel_package_combination_guide": """Get integration guide for using multiple Laravel packages together.

When to use:
- Combining packages like Livewire + Alpine
- Understanding package compatibility
- Getting installation order recommendations
- Finding integration best practices""",

    "get_laravel_learning_path": """Get a structured Laravel learning path for achieving a specific goal.

When to use:
- Starting to learn a new Laravel concept
- Planning a learning journey
- Getting step-by-step guidance
- Finding prerequisite knowledge""",

    "search_laravel_community_tutorials": """Search through aggregated Laravel community tutorials and articles.

When to use:
- Finding specific Laravel tutorials
- Searching Laravel News articles
- Looking for Spatie blog posts
- Discovering conference talks""",

    "get_laravel_bootcamp_progress": """Get Laravel Bootcamp content and track learning progress.

When to use:
- Following Laravel Bootcamp tutorials
- Getting official Laravel tutorials
- Learning Laravel basics
- Building your first Laravel app""",

    "find_laravel_conference_talks": """Find Laravel conference talks and presentations on specific topics.

When to use:
- Looking for video content
- Finding expert presentations
- Learning from conference speakers
- Discovering advanced topics"""
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
        default="LaravelMCPCompanion",
        help="Name of the MCP server (default: LaravelMCPCompanion)"
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

@lru_cache(maxsize=100)
def get_file_content_cached(file_path: str) -> str:
    """
    Get file content with caching.
    
    Args:
        file_path: Absolute path to the file
        
    Returns:
        File content as string
    """
    try:
        path_obj = Path(file_path)
        if not path_obj.exists():
            return f"File not found: {file_path}"
        
        # Check file modification time for cache invalidation
        mtime = path_obj.stat().st_mtime
        cache_key = f"{file_path}:{mtime}"
        
        with _cache_lock:
            if cache_key in _file_content_cache:
                return _file_content_cache[cache_key]
        
        # Read file content
        with open(path_obj, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cache the content
        with _cache_lock:
            # Clear old cache entries for this file
            keys_to_remove = [k for k in _file_content_cache.keys() if k.startswith(f"{file_path}:")]
            for key in keys_to_remove:
                del _file_content_cache[key]
            
            # Add new cache entry
            _file_content_cache[cache_key] = content
            
            # Limit cache size
            if len(_file_content_cache) > 200:
                # Remove oldest entries
                oldest_keys = list(_file_content_cache.keys())[:50]
                for key in oldest_keys:
                    del _file_content_cache[key]
        
        return content
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return f"Error reading file: {str(e)}"

def clear_file_cache():
    """Clear the file content cache."""
    with _cache_lock:
        _file_content_cache.clear()
        _search_result_cache.clear()

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
        # Check new location first
        metadata_file = docs_path / version / ".metadata" / "sync_info.json"
        if not metadata_file.exists():
            # Fall back to test location
            metadata_file = docs_path / version / ".metadata.json"
    else:
        # Try to find any version metadata
        for v in SUPPORTED_VERSIONS:
            metadata_file = docs_path / v / ".metadata" / "sync_info.json"
            if metadata_file.exists():
                break
            # Also check test location
            metadata_file = docs_path / v / ".metadata.json"
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


# Standalone implementations for testing
def get_laravel_package_recommendations(use_case: str) -> str:
    """Get Laravel package recommendations for a specific use case (for testing)."""
    logger.debug(f"get_laravel_package_recommendations called with use_case: {use_case}")
    use_case_lower = use_case.lower()
    recommendations = []
    
    for pkg_id, package in PACKAGE_CATALOG.items():
        # Check if use case matches categories or use cases
        if any(cat in use_case_lower for cat in package.get('categories', [])):
            recommendations.append(package)
            continue
        
        # Check if use case matches any defined use cases
        if any(use_case_lower in defined_use.lower() for defined_use in package.get('use_cases', [])):
            recommendations.append(package)
    
    if not recommendations:
        return f"No packages found matching the use case: '{use_case}'. Try different keywords or browse categories."
    
    result = [f"# Laravel Packages for: {use_case}\n"]
    result.append(f"Found {len(recommendations)} relevant packages:\n")
    
    for package in recommendations:
        result.append(f"## {package['name']}")
        result.append(f"{package['description']}\n")
        result.append(f"**Installation:** `{package['installation']}`\n")
        
        if package.get('use_cases'):
            result.append("**Common use cases:**")
            for uc in package['use_cases'][:3]:  # Show first 3 use cases
                result.append(f"- {uc}")
            result.append("")
    
    return "\n".join(result)


def get_laravel_package_info(package_name: str) -> str:
    """Get detailed information about a specific Laravel package (for testing)."""
    logger.debug(f"get_laravel_package_info called with package_name: {package_name}")
    
    # Clean the package name
    package_name = package_name.lower().strip()
    
    # Look for exact match or partial match
    package = None
    package_id: Optional[str] = None
    for pkg_id, pkg in PACKAGE_CATALOG.items():
        if pkg_id.lower() == package_name or package_name in pkg_id.lower():
            package = pkg
            package_id = pkg_id
            break
    
    if not package:
        return f"Package '{package_name}' not found. Use get_laravel_package_categories() to browse available packages."
    
    # Add the package ID to the package dict for format_package_recommendation
    package_with_id = package.copy()
    package_with_id['id'] = package_id or ''
    return format_package_recommendation(package_with_id)


def get_laravel_package_categories(category: str) -> str:
    """Get packages by category (for testing)."""
    logger.debug(f"get_laravel_package_categories called with category: {category}")
    category_lower = category.lower()
    matching_packages = []
    
    for pkg_id, package in PACKAGE_CATALOG.items():
        if category_lower in [cat.lower() for cat in package.get('categories', [])]:
            matching_packages.append((pkg_id, package))
    
    if not matching_packages:
        # List available categories
        all_categories: set[str] = set()
        for package in PACKAGE_CATALOG.values():
            all_categories.update(package.get('categories', []))
        
        return (f"No packages found in category: '{category}'. "
                f"Available categories: {', '.join(sorted(all_categories))}")
    
    result = [f"# Laravel Packages for Category: {category}\n"]
    result.append(f"Found {len(matching_packages)} packages:\n")
    
    for pkg_id, package in matching_packages:
        result.append(f"## {package['name']} ({pkg_id})")
        result.append(f"{package['description']}\n")
        result.append(f"**Installation:** `{package['installation']}`\n")
    
    return "\n".join(result)


def get_features_for_laravel_package(package: str) -> str:
    """Get implementation features for a Laravel package (for testing)."""
    logger.debug(f"get_features_for_laravel_package called with package: {package}")
    
    # Clean the package name
    package_lower = package.lower().strip()
    
    # Find the package in catalog
    found_package = None
    package_id = None
    
    for pkg_id, pkg in PACKAGE_CATALOG.items():
        if pkg_id.lower() == package_lower or package_lower in pkg_id.lower():
            found_package = pkg
            package_id = pkg_id
            break
    
    if not found_package:
        return f"Package '{package}' not found in the catalog."
    
    # Get features from the feature map
    features = FEATURE_MAP.get(package_id or '', [])
    
    results = [f"# Implementation Features for {found_package['name']}\n"]
    
    if features:
        results.append("Common implementation patterns and features:\n")
        for feature in features:
            results.append(f"- **{feature}**: Common implementation pattern")
        results.append("")
        results.append("The AI can provide detailed code examples for any of these features.")
    else:
        results.append(f"No specific features listed for {package_id}, but this package supports:")
        results.append("")
        for use_case in found_package.get('use_cases', [])[:5]:
            results.append(f"- {use_case}")
        results.append("")
        results.append("The AI can generate example code for this implementation based on best practices.")
    
    return "\n".join(results)


def update_laravel_docs(version: Optional[str] = None, force: bool = False) -> str:
    """Update Laravel documentation (for testing)."""
    # This is a stub for testing - the real implementation needs access to docs_path
    return "This function requires server context to execute"


def laravel_docs_info(version: Optional[str] = None) -> str:
    """Get Laravel documentation info (for testing)."""
    # This is a stub for testing - the real implementation needs access to docs_path
    return "This function requires server context to execute"


def validate_version(version: str) -> bool:
    """Validate that the version is supported.
    
    Args:
        version: Version string to validate
        
    Returns:
        True if version is supported, False otherwise
    """
    return version in SUPPORTED_VERSIONS


def setup_server_environment(args: argparse.Namespace) -> tuple[Path, Dict[str, Any]]:
    """Setup the server environment based on command line arguments.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Tuple of (docs_path, transport_options)
    """
    # Set logging level
    logger.setLevel(getattr(logging, args.log_level))
    
    # Setup docs path
    docs_path = setup_docs_path(args.docs_path)
    logger.info(f"Using docs path: {docs_path}")
    
    # Validate version
    if not validate_version(args.version):
        logger.error(f"Unsupported version: {args.version}. Supported versions: {', '.join(SUPPORTED_VERSIONS)}")
        sys.exit(1)
    
    # Setup transport options
    transport_options = {}
    if args.transport == "websocket" and (args.host or args.port):
        transport_options = {
            "host": args.host,
            "port": args.port,
        }
    
    return docs_path, transport_options


def handle_documentation_update(docs_path: Path, version: str, update_docs: bool, force_update: bool) -> bool:
    """Handle documentation update if requested.
    
    Args:
        docs_path: Path to documentation directory
        version: Laravel version
        update_docs: Whether to update docs
        force_update: Whether to force update
        
    Returns:
        True if update was performed, False otherwise
    """
    if update_docs or force_update:
        logger.info(f"Updating documentation (version: {version}, force: {force_update})")
        updated = update_documentation(docs_path, version, force_update)
        if updated:
            logger.info("Documentation updated successfully")
        else:
            logger.info("Documentation update not performed or not needed")
        return updated
    return False


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


def create_mcp_server(server_name: str, docs_path: Path, version: str) -> FastMCP:
    """Create and configure the MCP server with all tools and resources.
    
    Args:
        server_name: Name for the MCP server
        docs_path: Path to documentation directory
        version: Laravel version
        
    Returns:
        Configured FastMCP server instance
    """
    # Store configuration globally for resource handlers
    global _server_config
    _server_config = {
        'docs_path': docs_path,
        'version': version
    }
    
    # Create the MCP server
    mcp: FastMCP = FastMCP(server_name)
    
    # Initialize multi-source documentation updater
    multi_updater = MultiSourceDocsUpdater(docs_path, version)
    
    # Define resource handler functions
    def read_laravel_doc(path: str) -> str:
        """Read a specific Laravel documentation file."""
        config = _server_config
        logger.debug(f"read_laravel_doc function called with path: {path}")
        
        # Extract version and relative path
        version_inner, relative_path = get_version_from_path(path)
        
        # Make sure the path ends with .md
        if not relative_path.endswith('.md'):
            relative_path = f"{relative_path}.md"
        
        file_path = Path(config['docs_path']) / version_inner / relative_path
        
        # Security check - ensure we stay within version directory
        version_path = Path(config['docs_path']) / version_inner
        if not is_safe_path(version_path, file_path):
            logger.warning(f"Access denied: {path} (attempted directory traversal)")
            return f"Access denied: {path} (attempted directory traversal)"
        
        if not file_path.exists():
            logger.warning(f"Documentation file not found: {file_path}")
            return f"Documentation file not found: {path} (version: {version_inner})"
        
        try:
            content = get_file_content_cached(str(file_path))
            if not content.startswith("Error") and not content.startswith("File not found"):
                logger.debug(f"Successfully read file: {file_path} ({len(content)} bytes)")
            return content
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return f"Error reading file: {str(e)}"
    
    def read_external_laravel_doc(service: str, path: str) -> str:
        """Read a specific external Laravel service documentation file."""
        logger.debug(f"Reading external Laravel doc: {service}/{path}")
        
        try:
            # Validate service
            if service not in multi_updater.external_fetcher.list_available_services():
                available_services = multi_updater.external_fetcher.list_available_services()
                return f"Service '{service}' not found. Available: {', '.join(available_services)}"
            
            # Get service directory
            service_dir = multi_updater.external_fetcher.get_service_cache_path(service)
            
            # Make sure the path ends with .md
            if not path.endswith('.md'):
                path = f"{path}.md"
            
            file_path = service_dir / path
            
            # Security check - ensure we stay within service directory
            if not is_safe_path(service_dir, file_path):
                return f"Access denied: {service}/{path} (path traversal attempted)"
            
            if not file_path.exists():
                # List available files to help user
                available_files = []
                try:
                    available_files = [f.name for f in service_dir.glob("*.md")][:10]
                except Exception:
                    pass
                
                if available_files:
                    return f"File not found: {service}/{path}. Available files: {', '.join(available_files)}"
                else:
                    return f"File not found: {service}/{path}. No documentation cached for {service}. Use update_external_laravel_docs(['{service}']) to fetch documentation."
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.debug(f"Successfully read external file: {file_path} ({len(content)} bytes)")
                return content
        except Exception as e:
            logger.error(f"Error reading external file {service}/{path}: {str(e)}")
            return f"Error reading file: {str(e)}"
    
    # Register resources using functional approach (decorator as function)
    laravel_resource = mcp.resource("laravel://{path}")(read_laravel_doc)
    external_resource = mcp.resource("laravel-external://{service}/{path}")(read_external_laravel_doc)
    logger.debug(f"Registered Laravel resource: {laravel_resource}")
    logger.debug(f"Registered external resource: {external_resource}")
    
    
    # Configure all tools
    configure_mcp_server(mcp, docs_path, version, multi_updater)
    
    return mcp

# Global configuration storage
_server_config: Dict[str, Any] = {}


def configure_mcp_server(mcp: FastMCP, docs_path: Path, version: str, multi_updater: MultiSourceDocsUpdater) -> None:
    """Configure the MCP server with all tools and resources.
    
    Args:
        mcp: FastMCP server instance
        docs_path: Path to documentation directory
        version: Laravel version
        multi_updater: Multi-source documentation updater instance
    """
    # Register documentation tools
    @mcp.tool(description=TOOL_DESCRIPTIONS["list_laravel_docs"])
    def list_laravel_docs(version: Optional[str] = None) -> str:
        """List all available Laravel documentation files.
        
        Args:
            version: Specific Laravel version to list (e.g., "12.x"). If not provided, lists all versions.
        """
        return list_laravel_docs_impl(docs_path, version)
    
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["search_laravel_docs"])
    def search_laravel_docs(query: str, version: Optional[str] = None, include_external: bool = True) -> str:
        """Search through Laravel documentation for a specific term.
        
        Args:
            query: Search term to look for
            version: Specific Laravel version to search (e.g., "12.x"). If not provided, searches all versions.
            include_external: Whether to include external Laravel services documentation in search
        """
        external_dir = multi_updater.external_fetcher.external_dir if include_external else None
        return search_laravel_docs_impl(docs_path, query, version, include_external, external_dir)
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["update_laravel_docs"])
    def update_laravel_docs(version_param: Optional[str] = None, force: bool = False) -> str:
        """
        Update Laravel documentation from official GitHub repository.
        
        Args:
            version_param: Laravel version branch (e.g., "12.x")
            force: Force update even if already up to date
        """
        logger.debug(f"update_laravel_docs function called (version: {version_param}, force: {force})")
        
        # Use provided version or default to the one specified at startup
        doc_version = version_param or version
        
        try:
            updater = DocsUpdater(docs_path, doc_version)
            
            # Check if update is needed
            if not force and not updater.needs_update():
                return f"Documentation is already up to date (version: {doc_version})"
            
            # Perform the update
            updated = updater.update(force=force)
            
            if updated:
                # Clear caches when documentation is updated
                clear_file_cache()
                get_file_content_cached.cache_clear()
                
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
        return read_laravel_doc_content_impl(docs_path, filename, version)

    @mcp.tool(description="Search Laravel docs with context snippets")
    def search_laravel_docs_with_context(
        query: str, 
        version: Optional[str] = None,
        context_length: int = 200,
        include_external: bool = True
    ) -> str:
        """
        Search through Laravel documentation with context snippets.
        
        Args:
            query: Search term
            version: Specific version or None for all
            context_length: Characters of context to show (default: 200)
            include_external: Whether to include external Laravel services documentation
        
        Returns:
            Search results with context snippets
        """
        external_dir = multi_updater.external_fetcher.external_dir if include_external else None
        return search_laravel_docs_with_context_impl(docs_path, query, version, context_length, include_external, external_dir)

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
        return get_doc_structure_impl(docs_path, filename, version)

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
        return browse_docs_by_category_impl(docs_path, category, version)
    
    # Register external documentation tools
    @mcp.tool(description=TOOL_DESCRIPTIONS["update_external_laravel_docs"])
    def update_external_laravel_docs(services: Optional[List[str]] = None, force: bool = False) -> str:
        """
        Update documentation for external Laravel services.
        
        Args:
            services: List of services to update (forge, vapor, envoyer, nova). If None, updates all.
            force: Force update even if cache is valid
            
        Returns:
            Status of the update operation
        """
        logger.info(f"Updating external Laravel services documentation (services: {services}, force: {force})")
        
        try:
            if services:
                # Validate service names
                available_services = multi_updater.external_fetcher.list_available_services()
                invalid_services = [s for s in services if s not in available_services]
                if invalid_services:
                    return f"Invalid services: {', '.join(invalid_services)}. Available: {', '.join(available_services)}"
                
                results = multi_updater.update_external_docs(services=services, force=force)
            else:
                results = multi_updater.update_external_docs(force=force)
            
            # Clear caches if any services were updated successfully
            successful = [service for service, success in results.items() if success]
            failed = [service for service, success in results.items() if not success]
            
            if successful:
                clear_file_cache()
                get_file_content_cached.cache_clear()
            
            response = []
            response.append("External Laravel Services Documentation Update Results:")
            response.append(f"Successfully updated: {len(successful)}/{len(results)} services")
            
            if successful:
                response.append(f"\nSuccessful: {', '.join(successful)}")
            
            if failed:
                response.append(f"\nFailed: {', '.join(failed)}")
                response.append("Note: Some services may require additional setup or may be temporarily unavailable.")
            
            return "\n".join(response)
        except Exception as e:
            logger.error(f"Error updating external documentation: {str(e)}")
            return f"Error updating external documentation: {str(e)}"

    @mcp.tool(description=TOOL_DESCRIPTIONS["list_laravel_services"])
    def list_laravel_services() -> str:
        """
        List all available Laravel services with external documentation.
        
        Returns:
            List of available Laravel services
        """
        logger.debug("Listing available Laravel services")
        
        try:
            services = multi_updater.external_fetcher.list_available_services()
            response = ["Available Laravel Services:\n"]
            
            for service in services:
                service_info = multi_updater.external_fetcher.get_service_info(service)
                if service_info:
                    service_type = service_info.get('type', 'unknown')
                    if hasattr(service_type, 'value'):
                        service_type = service_type.value
                    
                    response.append(f"## {service_info.get('name', service)}")
                    response.append(f"**ID:** {service}")
                    response.append(f"**Type:** {service_type}")
                    
                    if 'base_url' in service_info:
                        response.append(f"**Documentation URL:** {service_info['base_url']}")
                    elif 'repo' in service_info:
                        response.append(f"**GitHub Repository:** {service_info['repo']}")
                    
                    # Check cache status
                    cache_valid = multi_updater.external_fetcher.is_cache_valid(service)
                    response.append(f"**Cache Status:** {'Valid' if cache_valid else 'Needs Update'}")
                    response.append("")
            
            return "\n".join(response)
        except Exception as e:
            logger.error(f"Error listing Laravel services: {str(e)}")
            return f"Error listing Laravel services: {str(e)}"

    @mcp.tool(description=TOOL_DESCRIPTIONS["search_external_laravel_docs"])
    def search_external_laravel_docs(query: str, services: Optional[List[str]] = None) -> str:
        """
        Search through external Laravel service documentation.
        
        Args:
            query: Search term to look for
            services: List of services to search. If None, searches all cached services.
            
        Returns:
            Search results from external documentation
        """
        logger.debug(f"Searching external Laravel docs for: {query}")
        
        if not query.strip():
            return "Search query cannot be empty"
        
        try:
            external_dir = multi_updater.external_fetcher.external_dir
            
            if not external_dir.exists():
                return "No external documentation found. Use update_external_laravel_docs() to fetch documentation first."
            
            # Determine which services to search
            if services:
                available_services = multi_updater.external_fetcher.list_available_services()
                invalid_services = [s for s in services if s not in available_services]
                if invalid_services:
                    return f"Invalid services: {', '.join(invalid_services)}. Available: {', '.join(available_services)}"
                search_services = services
            else:
                search_services = [d.name for d in external_dir.iterdir() if d.is_dir()]
            
            results = []
            pattern = re.compile(re.escape(query), re.IGNORECASE)
            
            for service in search_services:
                service_dir = external_dir / service
                if not service_dir.exists():
                    continue
                
                service_matches = []
                for file_path in service_dir.glob("*.md"):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if pattern.search(content):
                                count = len(pattern.findall(content))
                                service_matches.append(f"{file_path.name} ({count} matches)")
                    except Exception as e:
                        logger.warning(f"Error searching {file_path}: {str(e)}")
                        continue
                
                if service_matches:
                    results.append(f"**{service.title()}:**")
                    for match in service_matches:
                        results.append(f"  - {match}")
                    results.append("")
            
            if results:
                return f"Found '{query}' in external Laravel service documentation:\n\n" + "\n".join(results)
            else:
                return f"No results found for '{query}' in external Laravel service documentation."
        except Exception as e:
            logger.error(f"Error searching external documentation: {str(e)}")
            return f"Error searching external documentation: {str(e)}"

    @mcp.tool(description=TOOL_DESCRIPTIONS["get_laravel_service_info"])
    def get_laravel_service_info(service: str) -> str:
        """
        Get detailed information about a specific Laravel service.
        
        Args:
            service: Service name (forge, vapor, envoyer, nova)
            
        Returns:
            Detailed information about the service
        """
        logger.debug(f"Getting information for Laravel service: {service}")
        
        try:
            service_info = multi_updater.external_fetcher.get_service_info(service)
            
            if not service_info:
                available_services = multi_updater.external_fetcher.list_available_services()
                return f"Service '{service}' not found. Available services: {', '.join(available_services)}"
            
            response = []
            response.append(f"# {service_info.get('name', service)}")
            response.append("")
            
            # Service type and source
            service_type = service_info.get('type', 'unknown')
            if hasattr(service_type, 'value'):
                service_type = service_type.value
            response.append(f"**Type:** {service_type}")
            
            if 'base_url' in service_info:
                response.append(f"**Documentation URL:** {service_info['base_url']}")
                if 'sections' in service_info:
                    response.append(f"**Available Sections:** {', '.join(service_info['sections'])}")
            elif 'repo' in service_info:
                response.append(f"**GitHub Repository:** {service_info['repo']}")
                response.append(f"**Branch:** {service_info.get('branch', 'main')}")
            
            # Cache information
            cache_valid = multi_updater.external_fetcher.is_cache_valid(service)
            response.append(f"**Cache Status:** {'Valid' if cache_valid else 'Needs Update'}")
            
            # Try to get cache metadata
            metadata_path = multi_updater.external_fetcher.get_cache_metadata_path(service)
            if metadata_path.exists():
                try:
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    
                    if 'cached_at' in metadata:
                        import datetime
                        cache_time = datetime.datetime.fromtimestamp(metadata['cached_at'])
                        response.append(f"**Last Fetched:** {cache_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    if 'success_rate' in metadata:
                        response.append(f"**Success Rate:** {metadata['success_rate']:.1%}")
                    
                    if 'fetched_sections' in metadata:
                        response.append(f"**Fetched Sections:** {', '.join(metadata['fetched_sections'])}")
                except Exception:
                    pass
            
            response.append("")
            response.append("Use `update_external_laravel_docs()` to fetch or refresh this service's documentation.")
            
            return "\n".join(response)
        except Exception as e:
            logger.error(f"Error getting service info: {str(e)}")
            return f"Error getting service info: {str(e)}"
    
    # Initialize learning resources components
    learning_db_path = docs_path / "learning_resources.db"
    resource_fetcher = LearningResourceFetcher(learning_db_path)
    navigation_mapper = NavigationMapper(resource_fetcher)
    package_guide = PackageCombinationGuide(resource_fetcher)
    setup_orchestrator = SetupOrchestrator()
    content_manager = ContentAggregatorManager(learning_db_path)
    
    # Register learning resource tools
    @mcp.tool(description=TOOL_DESCRIPTIONS["discover_laravel_learning_resources"])
    def discover_laravel_learning_resources(
        topic: str,
        difficulty: Optional[str] = None
    ) -> str:
        """
        Find Laravel-specific tutorials, articles, and guides for a given topic.
        
        Args:
            topic: The Laravel topic or feature to find resources for
            difficulty: Optional difficulty level (beginner, intermediate, advanced, expert)
            
        Returns:
            Markdown-formatted list of learning resources
        """
        logger.info(f"Discovering learning resources for topic: {topic}")
        
        try:
            # Convert difficulty string to enum if provided
            difficulty_enum = None
            if difficulty:
                try:
                    difficulty_enum = DifficultyLevel(difficulty.lower())
                except ValueError:
                    return f"Invalid difficulty level: {difficulty}. Valid options: beginner, intermediate, advanced, expert"
            
            # Use navigation mapper to find resources
            result = navigation_mapper.find_resources_for_use_case(topic, difficulty_enum)
            
            # Format response
            response = [f"# Laravel Learning Resources: {topic}\n"]
            
            if result.learning_path:
                response.append("## Suggested Learning Path\n")
                for step in result.learning_path:
                    response.append(f"**Step {step['step']}:** {step['title']}")
                    response.append(f"   {step['description']}")
                    if 'resource_url' in step:
                        response.append(f"   📚 [View Resource]({step['resource_url']})")
                    response.append("")
            
            if result.recommended_packages:
                response.append(f"## Recommended Packages\n")
                response.append(", ".join(f"`{pkg}`" for pkg in result.recommended_packages))
                response.append("")
            
            if result.learning_resources:
                response.append(f"## Available Resources ({len(result.learning_resources)})\n")
                
                # Group by resource type
                by_type = {}
                for resource in result.learning_resources:
                    type_name = resource.type.value
                    if type_name not in by_type:
                        by_type[type_name] = []
                    by_type[type_name].append(resource)
                
                for type_name, resources in by_type.items():
                    response.append(f"### {type_name.title()}s\n")
                    for resource in resources[:5]:  # Limit to 5 per type
                        response.append(f"- **[{resource.title}]({resource.url})**")
                        if resource.description:
                            response.append(f"  {resource.description[:150]}...")
                        if resource.difficulty_level:
                            response.append(f"  📊 Difficulty: {resource.difficulty_level.value}")
                        if resource.tags:
                            response.append(f"  🏷️ Tags: {', '.join(resource.tags[:5])}")
                        response.append("")
            
            return "\n".join(response)
            
        except Exception as e:
            logger.error(f"Error discovering learning resources: {str(e)}")
            return f"Error discovering learning resources: {str(e)}"
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["get_laravel_package_combination_guide"])
    def get_laravel_package_combination_guide(packages: List[str]) -> str:
        """
        Get integration guide for using multiple Laravel packages together.
        
        Args:
            packages: List of package names to combine
            
        Returns:
            Markdown-formatted integration guide
        """
        logger.info(f"Getting package combination guide for: {packages}")
        
        try:
            guide = package_guide.get_combination_guide(packages)
            
            if not guide:
                return f"No specific guide available for combining: {', '.join(packages)}"
            
            response = [f"# Package Combination Guide\n"]
            response.append(f"**Packages:** {', '.join(packages)}\n")
            
            if 'compatibility_notes' in guide:
                response.append(f"## Compatibility\n")
                response.append(guide['compatibility_notes'])
                response.append("")
            
            if 'guide_content' in guide:
                response.append(guide['guide_content'])
            
            return "\n".join(response)
            
        except Exception as e:
            logger.error(f"Error getting package combination guide: {str(e)}")
            return f"Error getting package combination guide: {str(e)}"
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["get_laravel_learning_path"])
    def get_laravel_learning_path(
        goal: str,
        current_level: str = "beginner"
    ) -> str:
        """
        Get a structured Laravel learning path for achieving a specific goal.
        
        Args:
            goal: The learning goal or objective
            current_level: Current skill level (beginner, intermediate, advanced)
            
        Returns:
            Markdown-formatted learning path
        """
        logger.info(f"Getting learning path for goal: {goal}, level: {current_level}")
        
        try:
            # Convert level to enum
            try:
                level_enum = DifficultyLevel(current_level.lower())
            except ValueError:
                level_enum = DifficultyLevel.BEGINNER
            
            # Get resources and learning path
            result = navigation_mapper.find_resources_for_use_case(goal, level_enum)
            
            response = [f"# Laravel Learning Path: {goal}\n"]
            response.append(f"**Starting Level:** {current_level}")
            response.append(f"**Target:** {goal}\n")
            
            if result.learning_path:
                response.append("## Recommended Steps\n")
                total_steps = len(result.learning_path)
                
                for i, step in enumerate(result.learning_path, 1):
                    response.append(f"### Step {step['step']}: {step['title']}")
                    response.append(f"{step['description']}")
                    
                    if 'resource_url' in step:
                        response.append(f"\n📚 **Resource:** [{step.get('resource_title', 'View Resource')}]({step['resource_url']})")
                    
                    response.append(f"\n**Type:** {step['resource_type']}")
                    
                    if i < total_steps:
                        response.append("\n---\n")
                    else:
                        response.append("")
            
            # Add additional resources
            if result.learning_resources:
                response.append("\n## Additional Resources\n")
                for resource in result.learning_resources[:10]:
                    response.append(f"- [{resource.title}]({resource.url})")
                    if resource.difficulty_level:
                        response.append(f"  (Level: {resource.difficulty_level.value})")
            
            # Add package recommendations
            if result.recommended_packages:
                response.append("\n## Relevant Packages\n")
                response.append("Consider these packages for your implementation:")
                for pkg in result.recommended_packages:
                    response.append(f"- `{pkg}`")
            
            return "\n".join(response)
            
        except Exception as e:
            logger.error(f"Error getting learning path: {str(e)}")
            return f"Error getting learning path: {str(e)}"
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["search_laravel_community_tutorials"])
    def search_laravel_community_tutorials(
        query: str,
        source: Optional[str] = None
    ) -> str:
        """
        Search through aggregated Laravel community tutorials and articles.
        
        Args:
            query: Search query
            source: Optional source filter (laravel-news, spatie-blog, etc.)
            
        Returns:
            Markdown-formatted search results
        """
        logger.info(f"Searching community tutorials for: {query}")
        
        try:
            # Convert source to enum if provided
            source_enum = None
            if source:
                try:
                    source_enum = ResourceSource(source.lower().replace(' ', '-'))
                except ValueError:
                    return f"Invalid source: {source}. Valid options: laravel-news, spatie-blog, laracasts, etc."
            
            # Search resources
            resources = resource_fetcher.search(
                query=query,
                source=source_enum.value if source_enum else None,
                limit=30
            )
            
            if not resources:
                return f"No tutorials found for query: '{query}'"
            
            response = [f"# Community Tutorial Search: {query}\n"]
            response.append(f"Found {len(resources)} resources\n")
            
            # Group by source
            by_source = {}
            for resource in resources:
                source_name = resource.source.value
                if source_name not in by_source:
                    by_source[source_name] = []
                by_source[source_name].append(resource)
            
            for source_name, source_resources in by_source.items():
                response.append(f"## {source_name.replace('-', ' ').title()}\n")
                
                for resource in source_resources[:10]:
                    response.append(f"### [{resource.title}]({resource.url})")
                    
                    if resource.published_date:
                        response.append(f"*Published: {resource.published_date.strftime('%Y-%m-%d')}*")
                    
                    if resource.description:
                        response.append(f"\n{resource.description[:200]}...")
                    
                    if resource.tags:
                        response.append(f"\n🏷️ {', '.join(resource.tags[:5])}")
                    
                    response.append("")
            
            return "\n".join(response)
            
        except Exception as e:
            logger.error(f"Error searching community tutorials: {str(e)}")
            return f"Error searching community tutorials: {str(e)}"
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["get_laravel_bootcamp_progress"])
    def get_laravel_bootcamp_progress(section: Optional[str] = None) -> str:
        """
        Get Laravel Bootcamp content and track learning progress.
        
        Args:
            section: Optional specific bootcamp section (blade, livewire, inertia)
            
        Returns:
            Markdown-formatted bootcamp content
        """
        logger.info(f"Getting Laravel Bootcamp content for section: {section}")
        
        try:
            # Search for bootcamp resources
            resources = resource_fetcher.search(
                source=ResourceSource.LARAVEL_BOOTCAMP.value,
                limit=50
            )
            
            if not resources:
                return "Laravel Bootcamp content not found. Run documentation update to fetch bootcamp resources."
            
            response = ["# Laravel Bootcamp\n"]
            response.append("Build a fully functional Laravel application with our official tutorial.\n")
            
            # Group by stack
            stacks = {
                'blade': [],
                'livewire': [],
                'inertia': []
            }
            
            for resource in resources:
                title_lower = resource.title.lower()
                if 'blade:' in title_lower:
                    stacks['blade'].append(resource)
                elif 'livewire:' in title_lower:
                    stacks['livewire'].append(resource)
                elif 'inertia' in title_lower:
                    stacks['inertia'].append(resource)
            
            # Filter by section if specified
            if section and section.lower() in stacks:
                stack_resources = stacks[section.lower()]
                response.append(f"## {section.title()} Track\n")
                
                for i, resource in enumerate(stack_resources, 1):
                    response.append(f"### {i}. [{resource.title.split(': ', 1)[1]}]({resource.url})")
                    response.append(f"{resource.description}")
                    response.append("")
            else:
                # Show all tracks
                for stack_name, stack_resources in stacks.items():
                    if stack_resources:
                        response.append(f"## {stack_name.title()} Track ({len(stack_resources)} lessons)\n")
                        
                        for resource in stack_resources[:3]:  # Show first 3
                            title_parts = resource.title.split(': ', 1)
                            lesson_title = title_parts[1] if len(title_parts) > 1 else title_parts[0]
                            response.append(f"- [{lesson_title}]({resource.url})")
                        
                        if len(stack_resources) > 3:
                            response.append(f"- ...and {len(stack_resources) - 3} more lessons")
                        response.append("")
            
            response.append("## Getting Started\n")
            response.append("1. Choose your preferred stack (Blade, Livewire, or Inertia)")
            response.append("2. Follow the installation guide for your stack")
            response.append("3. Build the Chirper application step by step")
            response.append("4. Learn Laravel fundamentals through practical examples")
            
            return "\n".join(response)
            
        except Exception as e:
            logger.error(f"Error getting bootcamp content: {str(e)}")
            return f"Error getting bootcamp content: {str(e)}"
    
    @mcp.tool(description=TOOL_DESCRIPTIONS["find_laravel_conference_talks"])
    def find_laravel_conference_talks(
        topic: str,
        year: Optional[int] = None
    ) -> str:
        """
        Find Laravel conference talks and presentations on specific topics.
        
        Args:
            topic: Topic to search for in conference talks
            year: Optional year filter
            
        Returns:
            Markdown-formatted list of conference talks
        """
        logger.info(f"Finding conference talks for topic: {topic}, year: {year}")
        
        try:
            # Search for conference talks
            resources = resource_fetcher.search(
                query=topic,
                resource_type=ResourceType.VIDEO.value,
                source=ResourceSource.CONFERENCE_TALK.value,
                limit=20
            )
            
            # Filter by year if specified
            if year and resources:
                resources = [
                    r for r in resources
                    if r.metadata.get('conference', '').endswith(str(year))
                ]
            
            if not resources:
                return f"No conference talks found for topic: '{topic}'" + (f" in {year}" if year else "")
            
            response = [f"# Laravel Conference Talks: {topic}\n"]
            
            if year:
                response.append(f"**Year:** {year}\n")
            
            response.append(f"Found {len(resources)} conference talks\n")
            
            # Group by conference
            by_conference = {}
            for resource in resources:
                conf = resource.metadata.get('conference', 'General')
                if conf not in by_conference:
                    by_conference[conf] = []
                by_conference[conf].append(resource)
            
            for conference, talks in by_conference.items():
                response.append(f"## {conference}\n")
                
                for talk in talks:
                    response.append(f"### [{talk.title}]({talk.url})")
                    
                    if 'speaker' in talk.metadata:
                        response.append(f"**Speaker:** {talk.metadata['speaker']}")
                    
                    if 'duration' in talk.metadata:
                        response.append(f"**Duration:** {talk.metadata['duration']}")
                    
                    if talk.description:
                        response.append(f"\n{talk.description}")
                    
                    if talk.tags:
                        response.append(f"\n🏷️ {', '.join(talk.tags)}")
                    
                    response.append("")
            
            return "\n".join(response)
            
        except Exception as e:
            logger.error(f"Error finding conference talks: {str(e)}")
            return f"Error finding conference talks: {str(e)}"
    
    # Initialize learning resources on first run
    if not (docs_path / "learning_resources.db").exists():
        logger.info("Initializing learning resources database...")
        try:
            # Run content aggregators to populate initial data
            results = content_manager.update_all()
            logger.info(f"Learning resources initialized: {sum(len(r) for r in results.values())} resources added")
        except Exception as e:
            logger.warning(f"Could not initialize learning resources: {str(e)}")



def main():
    """Main entry point for the Laravel MCP Companion."""
    args = parse_arguments()
    
    # Setup server environment
    docs_path, transport_options = setup_server_environment(args)
    
    # Update documentation if requested
    handle_documentation_update(docs_path, args.version, args.update_docs, args.force_update)
    
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
    
    # Create and configure the MCP server
    mcp = create_mcp_server(args.server_name, docs_path, args.version)
    
    # Log server startup
    logger.info(f"Starting Laravel MCP Companion ({args.server_name})")
    logger.info(f"Transport: {args.transport}")
    logger.info(f"Supported Laravel versions: {', '.join(SUPPORTED_VERSIONS)}")
    
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
