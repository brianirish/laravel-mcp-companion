#!/usr/bin/env python3
"""
Laravel MCP Companion

This server provides Laravel documentation and package recommendations via the Model Context Protocol (MCP).
It allows AI assistants and other tools to access and search Laravel documentation, as well as
recommend appropriate Laravel packages for specific use cases.
"""

import math
import os
import sys
import logging
import re
import argparse
import json
from pathlib import Path
from typing import Dict, Optional, List, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
import threading
import anyio.to_thread
from fastmcp import Context, FastMCP
from fastmcp.server.auth import TokenVerifier
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

import time

from metrics import MetricsMiddleware, registry as metrics_registry, render_prometheus
from fastmcp.server.transforms.search import BM25SearchTransform
from mcp.types import Icon

# Import documentation updater
from docs_updater import DocsUpdater, MultiSourceDocsUpdater, get_cached_supported_versions, DEFAULT_VERSION
from shutdown_handler import GracefulShutdown
from fastmcp.tools.tool import ToolResult

from toon_helpers import (
    toon_encode,
    toon_result,
    error_data,
    format_package_list,
    format_package_info,
    format_service_list,
    format_error
)
from tool_schemas import OUTPUT_SCHEMAS

# Import standalone MCP tool implementations
from mcp_tools import (
    list_laravel_docs_data,
    read_laravel_doc_content_impl,
    search_laravel_docs_data,
    validate_version_data,
    read_laravel_doc_section_impl,
    get_doc_structure_impl,
    browse_docs_by_category_impl,
    verify_laravel_feature_impl,
    compare_laravel_versions_impl,
    find_laravel_docs_for_need_impl,
    get_laravel_learning_path_impl,
    list_laravel_learning_paths_impl,
    get_laravel_content_by_difficulty_impl,
    get_related_laravel_packages_impl,
    search_laravel_learning_resources_impl,
    list_laravel_learning_resources_impl,
    list_laravel_categories_impl,
    resolve_contained_path,
    validate_version as validate_version_arg,
    count_matches,
    clear_caches as clear_mcp_tools_caches,
    describe_documentation_date,
    get_documentation_date,
    copy_is_stale,
    DOCS_STALE_AFTER_DAYS
)

# Import learning resources
from learning_resources import LEARNING_PATHS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("laravel-mcp-companion")

# The server's own version, reported at initialize and stamped into the
# .well-known registry metadata. The Docker image runs this file directly with
# no installed package metadata, so importlib.metadata cannot supply it; a
# guard in tests/unit/test_version_consistency.py keeps it equal to
# pyproject.toml.
SERVER_VERSION = "0.12.0"

PROJECT_URL = "https://github.com/brianirish/laravel-mcp-companion"

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
        "documentation_link": "laravel://packages/cashier.md",
        "related_packages": ["laravel/cashier-paddle"]
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
        "documentation_link": "laravel://authentication/sanctum.md",
        "related_packages": ["laravel/breeze", "laravel/jetstream", "laravel/fortify"]
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
        "documentation_link": "laravel://authentication/passport.md",
        "related_packages": ["laravel/socialite"]
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
        "documentation_link": "laravel://starter-kits/breeze.md",
        "related_packages": ["laravel/sanctum", "laravel/fortify", "livewire/livewire", "inertiajs/inertia-laravel"]
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
        "documentation_link": "laravel://livewire.md",
        "related_packages": ["laravel/breeze", "laravel/jetstream"]
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
        "documentation_link": "laravel://authentication/fortify.md",
        "related_packages": ["laravel/breeze", "laravel/jetstream", "laravel/sanctum"]
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
        "documentation_link": "laravel://inertia.md",
        "related_packages": ["laravel/breeze", "laravel/jetstream"]
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
        "documentation_link": "laravel://horizon.md",
        "related_packages": ["laravel/telescope"]
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
        "documentation_link": "laravel://telescope.md",
        "related_packages": ["laravel/horizon", "barryvdh/laravel-debugbar"]
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
        "documentation_link": "laravel://starter-kits/jetstream.md",
        "related_packages": ["laravel/sanctum", "laravel/fortify", "livewire/livewire", "inertiajs/inertia-laravel"]
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
        "documentation_link": "laravel://octane.md",
        "related_packages": ["laravel/horizon"]
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

    "read_laravel_doc_content": """Reads a whole Laravel documentation file. Prefer read_laravel_doc_section, which returns just the section you need -- a full file can exceed 30,000 tokens against a few hundred for one section.

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

    "verify_laravel_feature": """ALWAYS use this tool FIRST when the user mentions a Laravel feature or asks if something exists in Laravel.

This is a fast, lightweight check that verifies feature existence without reading file content. Your training data is outdated - this tool provides authoritative answers about what exists in specific Laravel versions.

CRITICAL: DO NOT rely on your training knowledge. The documentation is the source of truth.

When to use:
- User mentions ANY Laravel feature (e.g., "Does Laravel have X?", "How does Y work?")
- Before suggesting implementation approaches
- When uncertain if a feature exists in a specific version
- As a first step before reading documentation

Examples:
- "Does Laravel 12.x support Vite?" → Use this tool first
- "How do I use Sanctum?" → Verify it exists, then read docs
- "What's new in authentication?" → Check what auth files exist

This takes milliseconds. Always use it. Don't guess.""",

    "compare_laravel_versions": """ALWAYS use this when the user mentions multiple Laravel versions or asks "what's new" or "what changed".

Your training data CANNOT show version-specific changes. This tool provides authoritative file-level comparison between any two Laravel versions.

CRITICAL: When a user asks about differences between versions, use this tool IMMEDIATELY. Don't speculate based on training data.

When to use:
- "What's new in Laravel 12.x?" → Compare 11.x to 12.x
- "Should I upgrade from 10.x to 12.x?" → Compare both versions
- "What changed in authentication?" → Compare with file_filter="auth"
- "Is feature X in version Y?" → Compare relevant versions

This shows:
- New documentation files (new features/topics)
- Removed documentation files (deprecated features)
- Persisting files (stable features)
- Git metadata (commit info, dates)

Example usage:
- compare_laravel_versions(from_version="11.x", to_version="12.x")
- compare_laravel_versions(from_version="11.x", to_version="12.x", file_filter="auth")

Fast, file-level only. No content diffing.""",

    "find_laravel_docs_for_need": """Finds relevant Laravel documentation based on what you need to accomplish.

When to use:
- "I need to upload files" → Returns filesystem, validation, requests docs
- "I need to send emails" → Returns mail, notifications, queues docs
- "I need to accept payments" → Returns cashier, billing docs
- Starting a new feature without knowing which docs to read
- Finding related documentation for a specific use case

This maps common needs to relevant documentation, including packages and external services.""",

    "get_laravel_learning_path": """Returns a curated learning path with ordered documentation for a specific goal.

When to use:
- User is learning Laravel from scratch
- User wants to learn a specific area (APIs, testing, etc.)
- Providing structured guidance for skill development
- Recommending documentation reading order

Available paths: getting-started, crud-basics, authentication-basics, api-development, testing-fundamentals, advanced-eloquent, background-processing, real-time-features, production-ready, full-stack-spa""",

    "list_laravel_learning_paths": """Lists all available curated learning paths with difficulty and duration estimates.

When to use:
- User asks "where should I start?"
- Helping user choose a learning path
- Showing available structured learning options
- Recommending based on skill level""",

    "get_laravel_content_by_difficulty": """Filters documentation by difficulty level (beginner, intermediate, advanced).

When to use:
- User is a beginner and needs easier content
- User wants advanced topics only
- Recommending appropriate documentation based on skill level
- Organizing learning progression""",

    "get_related_laravel_packages": """Returns packages commonly used together with a given package.

When to use:
- User is installing a package and might need related ones
- Suggesting complementary packages
- Building complete feature stacks
- Understanding package ecosystems

Example: laravel/sanctum → breeze, jetstream, fortify""",

    "search_laravel_learning_resources": """Searches through learning resources (bootcamp, blog, news, etc.).

When to use:
- Finding tutorials and guides
- Searching for recent Laravel articles
- Looking for learning content beyond official docs
- Finding practical examples and walkthroughs""",

    "list_laravel_learning_resources": """Lists available learning resource sources and their content.

When to use:
- Discovering available learning content
- Checking what resources have been fetched
- Finding tutorials and guides
- Exploring beyond official documentation""",

    "list_laravel_categories": """Lists all documentation categories with topic counts.

When to use:
- Exploring documentation organization
- Finding related topics
- Understanding coverage by category
- Planning what to learn next"""
}

def _split_env_list(env_var: str) -> Optional[List[str]]:
    """Parse a comma-separated environment variable into a list of values."""
    raw = os.environ.get(env_var, "")
    values = [item.strip() for item in raw.split(",") if item.strip()]
    return values or None


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Laravel Documentation and Package Recommendation MCP Server"
    )
    parser.add_argument(
        "--docs-path",
        type=str,
        default=os.environ.get("DOCS_PATH"),
        help="Path to Laravel documentation directory (default: ./docs, env: DOCS_PATH)"
    )
    parser.add_argument(
        "--server-name",
        type=str,
        default=os.environ.get("SERVER_NAME", "LaravelMCPCompanion"),
        help="Name of the MCP server (default: LaravelMCPCompanion, env: SERVER_NAME)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=os.environ.get("LOG_LEVEL", "INFO"),
        help="Logging level (default: INFO, env: LOG_LEVEL)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=os.environ.get("HOST"),
        help="Host to bind to (if using network transport, env: HOST)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", "0")) if os.environ.get("PORT") else None,
        help="Port to listen on (if using network transport, env: PORT)"
    )
    parser.add_argument(
        "--transport",
        type=str,
        default=os.environ.get("TRANSPORT", "stdio"),
        choices=["stdio", "http"],
        help="Transport mechanism to use (default: stdio, env: TRANSPORT)"
    )
    parser.add_argument(
        "--version",
        type=str,
        default=os.environ.get("VERSION", DEFAULT_VERSION),
        help=f"Laravel version branch to use (default: {DEFAULT_VERSION}, env: VERSION). Supported: {', '.join(SUPPORTED_VERSIONS)}"
    )
    parser.add_argument(
        "--update-docs",
        action="store_true",
        default=os.environ.get("UPDATE_DOCS", "").lower() == "true",
        help="Update documentation before starting server (env: UPDATE_DOCS=true)"
    )
    parser.add_argument(
        "--force-update",
        action="store_true",
        default=os.environ.get("FORCE_UPDATE", "").lower() == "true",
        help="Force update of documentation even if already up to date (env: FORCE_UPDATE=true)"
    )
    # These default to None rather than the env list: argparse's "append" action
    # appends to the default, so a non-empty default would union env values with
    # CLI values instead of letting the CLI replace them. The env fallback is
    # applied below, only when the flag is absent.
    parser.add_argument(
        "--cors-origin",
        action="append",
        default=None,
        metavar="ORIGIN",
        help="Browser origin allowed to call the HTTP transport (repeatable). "
             "Replaces CORS_ORIGINS when given. CORS is disabled unless at least "
             "one origin is set. Wildcards are not accepted (env: CORS_ORIGINS, comma-separated)"
    )
    parser.add_argument(
        "--allowed-host",
        action="append",
        default=None,
        metavar="HOST",
        help="Host header value accepted by the HTTP transport (repeatable). "
             "Replaces ALLOWED_HOSTS when given. Required to serve under a hostname "
             "other than localhost (env: ALLOWED_HOSTS, comma-separated)"
    )
    parser.add_argument(
        "--auth-jwks-uri",
        type=str,
        default=os.environ.get("AUTH_JWKS_URI"),
        metavar="URI",
        help="JWKS endpoint of the OAuth authorization server; enables bearer-token "
             "validation on the HTTP transport (env: AUTH_JWKS_URI)"
    )
    parser.add_argument(
        "--auth-issuer",
        type=str,
        default=os.environ.get("AUTH_ISSUER"),
        metavar="ISSUER",
        help="Required token issuer, matched against the JWT 'iss' claim (env: AUTH_ISSUER)"
    )
    parser.add_argument(
        "--auth-audience",
        type=str,
        default=os.environ.get("AUTH_AUDIENCE"),
        metavar="AUDIENCE",
        help="Required token audience, matched against the JWT 'aud' claim (env: AUTH_AUDIENCE)"
    )
    parser.add_argument(
        "--auth-required-scope",
        action="append",
        default=None,
        metavar="SCOPE",
        help="OAuth scope every token must carry (repeatable). Replaces "
             "AUTH_REQUIRED_SCOPES when given (env: AUTH_REQUIRED_SCOPES, comma-separated)"
    )
    parser.add_argument(
        "--rate-limit",
        type=float,
        default=None,
        metavar="RPS",
        help="Requests per second accepted across the whole server in HTTP mode; "
             "unset means no limiting (env: RATE_LIMIT_RPS)"
    )
    parser.add_argument(
        "--rate-limit-burst",
        type=int,
        default=None,
        metavar="N",
        help="Token-bucket burst capacity; defaults to max(10, 2*RPS) so the MCP "
             "handshake never self-throttles (env: RATE_LIMIT_BURST)"
    )
    parser.add_argument(
        "--transform-mode",
        type=str,
        default=os.environ.get("TRANSFORM_MODE", "").lower() or None,
        choices=["search", "code", "none"],
        help="Tool exposure mode: 'search' exposes BM25 search_tools/call_tool (default), "
             "'code' enables experimental Code Mode, 'none' exposes all raw tools (env: TRANSFORM_MODE)"
    )
    parser.add_argument(
        "--code-mode",
        action="store_true",
        default=os.environ.get("CODE_MODE", "").lower() == "true",
        help="Deprecated: use --transform-mode code (env: CODE_MODE=true)"
    )

    args = parser.parse_args()

    # argparse does not validate defaults against choices, so check env-provided values
    if args.transform_mode is not None and args.transform_mode not in ("search", "code", "none"):
        parser.error(f"invalid TRANSFORM_MODE: {args.transform_mode!r} (choose from 'search', 'code', 'none')")

    # Fall back to the environment only when the flag was not given, so an
    # explicit allowlist on the command line fully replaces the env value.
    if args.cors_origin is None:
        args.cors_origin = _split_env_list("CORS_ORIGINS") or []
    if args.allowed_host is None:
        args.allowed_host = _split_env_list("ALLOWED_HOSTS") or []
    if args.auth_required_scope is None:
        args.auth_required_scope = _split_env_list("AUTH_REQUIRED_SCOPES") or []

    # argparse type= does not run on defaults, so env fallbacks parse here.
    if args.rate_limit is None and os.environ.get("RATE_LIMIT_RPS"):
        try:
            args.rate_limit = float(os.environ["RATE_LIMIT_RPS"])
        except ValueError:
            parser.error(f"invalid RATE_LIMIT_RPS: {os.environ['RATE_LIMIT_RPS']!r}")
    if args.rate_limit_burst is None and os.environ.get("RATE_LIMIT_BURST"):
        try:
            args.rate_limit_burst = int(os.environ["RATE_LIMIT_BURST"])
        except ValueError:
            parser.error(f"invalid RATE_LIMIT_BURST: {os.environ['RATE_LIMIT_BURST']!r}")

    # Allowed hosts are matched with fnmatch, so a pattern entry would match
    # every Host header and silently disable the guard while still looking like
    # a configured allowlist. Reject them the way wildcard CORS origins are.
    wildcard_hosts = [h for h in args.allowed_host if any(c in h for c in "*?[")]
    if wildcard_hosts:
        parser.error(
            f"wildcard patterns are not accepted in allowed hosts: {', '.join(wildcard_hosts)}. "
            "List each hostname explicitly; a pattern would match every Host header "
            "and disable DNS-rebinding protection."
        )

    return args

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

def get_file_content_cached(file_path: str) -> str:
    """
    Get file content, keyed on path and modification time.

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
            # Clear stale entries for this file (previous mtimes)
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
    """Clear every documentation cache, in this module and in mcp_tools."""
    with _cache_lock:
        _file_content_cache.clear()
        _search_result_cache.clear()
    # The tool implementations keep their own caches; stale entries there would
    # otherwise survive a docs update until the process restarts.
    clear_mcp_tools_caches()

def update_documentation(docs_path: Path, version: str, force: bool = False) -> bool:
    """Update the documentation if needed or forced."""
    try:
        updater = DocsUpdater(docs_path, version)
        updated = updater.update(force=force)
        return updated
    except Exception as e:
        logger.error(f"Failed to update documentation: {str(e)}")
        return False

def get_version_from_path(path: str, runtime_version: Optional[str] = None) -> tuple[str, str]:
    """Extract version and relative path from a documentation path.
    
    Args:
        path: Path like "12.x/blade.md" or "blade.md"
        runtime_version: Runtime default version (from --version flag)
        
    Returns:
        (version, relative_path): Tuple of version and path within that version
    """
    path_parts = Path(path).parts
    
    # Check if first part is a version
    if path_parts and path_parts[0] in SUPPORTED_VERSIONS:
        version = path_parts[0]
        relative_path = str(Path(*path_parts[1:]))
        return version, relative_path
    
    # Default to runtime version or latest version if no version specified
    default_version = runtime_version if runtime_version else DEFAULT_VERSION
    return default_version, path

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
    scores: Dict[str, float] = {}
    for pkg_id, pkg_info in PACKAGE_CATALOG.items():
        score = 0.0

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
                score += 0.5
        
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

def package_recommendation_data(package: Dict) -> Dict[str, Any]:
    """Build the package recommendation payload, as data."""
    pkg_id = package.get('id', 'unknown')

    data: Dict[str, Any] = {
        "id": pkg_id,
        "name": package.get('name', pkg_id),
        "description": package.get('description', 'No description available'),
    }

    if 'use_cases' in package:
        data["use_cases"] = package['use_cases']

    if 'installation' in package:
        data["installation"] = package['installation']

    # Add features if available in map
    if pkg_id in FEATURE_MAP:
        data["features"] = FEATURE_MAP[pkg_id]

    if 'documentation_link' in package:
        data["documentation_link"] = package['documentation_link']

    return data


def format_package_recommendation(package: Dict) -> str:
    """Format a package recommendation as TOON."""
    return format_package_info(package_recommendation_data(package))


# Standalone implementations for testing
def get_laravel_package_recommendations(use_case: str) -> str:
    """Get Laravel package recommendations for a specific use case (for testing).

    Returns:
        TOON-encoded package recommendations.
    """
    logger.debug(f"get_laravel_package_recommendations called with use_case: {use_case}")
    use_case_lower = use_case.lower()
    recommendations: List[Dict[str, Any]] = []

    for pkg_id, package in PACKAGE_CATALOG.items():
        # Check if use case matches categories or use cases
        if any(cat in use_case_lower for cat in package.get('categories', [])):
            recommendations.append({
                "id": pkg_id,
                "name": package['name'],
                "description": package['description'],
                "installation": package['installation'],
                "use_cases": package.get('use_cases', [])[:3]
            })
            continue

        # Check if use case matches any defined use cases
        if any(use_case_lower in defined_use.lower() for defined_use in package.get('use_cases', [])):
            recommendations.append({
                "id": pkg_id,
                "name": package['name'],
                "description": package['description'],
                "installation": package['installation'],
                "use_cases": package.get('use_cases', [])[:3]
            })

    if not recommendations:
        return format_error(f"No packages found matching: '{use_case}'")

    return format_package_list(recommendations, f"Packages for: {use_case}")


def get_laravel_package_info(package_name: str) -> str:
    """Get detailed information about a specific Laravel package (for testing).

    Returns:
        TOON-encoded package information.
    """
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
        return format_error(f"Package '{package_name}' not found")

    # Add the package ID to the package dict for format_package_recommendation
    package_with_id = package.copy()
    package_with_id['id'] = package_id or ''
    return format_package_recommendation(package_with_id)


def get_laravel_package_categories(category: str) -> str:
    """Get packages by category (for testing).

    Returns:
        TOON-encoded packages in category.
    """
    logger.debug(f"get_laravel_package_categories called with category: {category}")
    category_lower = category.lower()
    matching_packages: List[Dict[str, Any]] = []

    for pkg_id, package in PACKAGE_CATALOG.items():
        if category_lower in [cat.lower() for cat in package.get('categories', [])]:
            matching_packages.append({
                "id": pkg_id,
                "name": package['name'],
                "description": package['description'],
                "installation": package['installation'],
                "documentation_link": package.get('documentation_link')
            })

    if not matching_packages:
        # List available categories
        all_categories: set[str] = set()
        for package in PACKAGE_CATALOG.values():
            all_categories.update(package.get('categories', []))

        return format_error(
            f"No packages found in category: '{category}'",
            {"available_categories": sorted(all_categories)}
        )

    return format_package_list(matching_packages, f"Category: {category}")


def get_features_for_laravel_package(package: str) -> str:
    """Get implementation features for a Laravel package (for testing).

    Returns:
        TOON-encoded package features.
    """
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
        return format_error(f"Package '{package}' not found")

    # Get features from the feature map
    features = FEATURE_MAP.get(package_id or '', [])

    return toon_encode({
        "package": package_id,
        "name": found_package['name'],
        "features": features if features else found_package.get('use_cases', [])[:5],
        "has_defined_features": bool(features)
    })


def update_laravel_docs(version: Optional[str] = None, force: bool = False) -> str:
    """Update Laravel documentation (for testing)."""
    # This is a stub for testing - the real implementation needs access to docs_path
    return "This function requires server context to execute"


def laravel_docs_info(version: Optional[str] = None) -> str:
    """Get Laravel documentation info (for testing)."""
    # This is a stub for testing - the real implementation needs access to docs_path
    return "This function requires server context to execute"


def build_server_instructions(
    docs_path: Path,
    runtime_version: str,
    transform_mode: Optional[str] = "search",
) -> str:
    """Compose the instructions an MCP client injects into the model's context.

    This is where the assistant learns what date the bundled documentation
    describes. Without it, the model answers questions about features newer than
    the corpus without knowing the corpus could not contain them, and the user
    has no reason to suspect it.

    The date reported is that of `runtime_version`, the version this server
    actually answers from. Reporting the newest version present would describe a
    corpus the user is not reading -- an older pinned version can be a year
    behind while another sits at today's date.

    The described workflow follows `transform_mode`, because the search and code
    transforms replace the individual tools with a small synthetic surface.
    Naming hidden tools would invite calls the client cannot route.
    """
    documentation_date = describe_documentation_date(docs_path, runtime_version)

    if transform_mode == "search":
        workflow = """Tools are exposed through a search interface rather than listed \
individually. Call search_tools with a natural-language description to find the right \
tool, then invoke it through call_tool with its name and arguments. \
search_laravel_docs is also available directly."""
        info_tool = 'call_tool with "laravel_docs_info"'
    elif transform_mode == "code":
        workflow = """Tools are exposed through Code Mode. Use tags and search to \
discover them, get_schema for their parameters, and execute to run Python that calls \
them."""
        info_tool = "the laravel_docs_info tool"
    else:
        workflow = """Typical flow: search_laravel_docs to locate relevant files, then \
read_laravel_doc_content for the full text. For a natural-language request such as \
"I need to upload files", find_laravel_docs_for_need maps it to the right pages. \
get_laravel_package_recommendations suggests packages for a described use case."""
        info_tool = "laravel_docs_info"

    return f"""Laravel documentation for the whole ecosystem: core Laravel \
{', '.join(SUPPORTED_VERSIONS)}, the first-party services (Forge, Vapor, Nova, \
Envoyer), and community packages (Spatie, Livewire, Filament, Inertia).

{workflow}

Documentation answers default to Laravel {runtime_version}; pass `version` to target \
another, or `all_versions` to search every one.

This copy reflects Laravel's documentation as of {documentation_date}. If you are \
asked about a feature that may have been added after that date, say so rather than \
answering as if the documentation covered it. {info_tool} reports this date at any \
time."""


def validate_version(version: str) -> bool:
    """Validate that the version is supported.
    
    Args:
        version: Version string to validate
        
    Returns:
        True if version is supported, False otherwise
    """
    return version in SUPPORTED_VERSIONS


def setup_server_environment(args: argparse.Namespace) -> Path:
    """Setup the server environment based on command line arguments.

    Args:
        args: Parsed command line arguments

    Returns:
        Validated docs_path
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

    return docs_path


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


def build_rate_limiter(args) -> Optional["RateLimitingMiddleware"]:
    """Build the opt-in token-bucket limiter from CLI/env configuration.

    One global bucket for the whole server — a total-throughput cap, not
    per-client fairness; without auth there is no reliable client identity
    to key on. The limiter counts every MCP request including the initialize
    handshake, so the burst default stays comfortably above handshake size.

    Returns None when unset, or when the transport is stdio, where a single
    local client throttling itself serves nobody.
    """
    if args.rate_limit is None:
        return None

    if args.transport != "http":
        logger.warning(
            "A rate limit is configured but the transport is stdio; ignoring it. "
            "Rate limiting only applies to the HTTP transport."
        )
        return None

    if args.rate_limit <= 0:
        logger.error(f"--rate-limit must be positive, got {args.rate_limit}")
        sys.exit(1)

    burst = args.rate_limit_burst
    if burst is None:
        burst = max(10, math.ceil(2 * args.rate_limit))
    elif burst < 1:
        logger.error(f"--rate-limit-burst must be at least 1, got {burst}")
        sys.exit(1)

    from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
    logger.info(f"Rate limiting enabled: {args.rate_limit} req/s, burst {burst}")
    return RateLimitingMiddleware(
        max_requests_per_second=args.rate_limit,
        burst_capacity=burst,
    )


def harden_verifier(verifier: "TokenVerifier") -> "TokenVerifier":
    """Make verify_token fail closed instead of raising.

    FastMCP's auth middleware eagerly verifies any request that carries an
    Authorization header — on every route, custom ones included — and an
    exception from the verifier (a JWKS fetch failing, say) becomes an
    app-wide 500, taking /healthz and /.well-known down with it. Catching
    here turns an outage into 401s for token-bearing requests while every
    public route keeps answering.
    """
    inner = verifier.verify_token

    async def resilient(token: str):
        try:
            return await inner(token)
        except Exception as e:
            logger.error(f"Token verification failed closed: {e}")
            return None

    verifier.verify_token = resilient  # type: ignore[method-assign]
    return verifier


def build_auth_provider(args) -> Optional["TokenVerifier"]:
    """Build the OAuth 2.1 token verifier from CLI/env configuration.

    The server is a resource server only: it validates bearer tokens issued
    elsewhere and never issues its own. Two mutually exclusive modes:

    - JWKS (production): --auth-jwks-uri + --auth-issuer + --auth-audience.
      Issuer and audience are mandatory -- accepting any issuer's tokens, or
      tokens minted for a different service, is authentication theater.
    - Static tokens (dev/internal, env only): AUTH_STATIC_TOKENS as
      "token:client_id[,token:client_id...]". Deliberately not a CLI flag so
      secrets stay out of process listings.

    Returns None when no auth is configured, or when the transport is stdio,
    where the process boundary is the access control.
    """
    static_tokens = os.environ.get("AUTH_STATIC_TOKENS", "").strip()
    jwks_configured = bool(args.auth_jwks_uri)

    if not static_tokens and not jwks_configured:
        return None

    if args.transport != "http":
        logger.warning(
            "Auth is configured but the transport is stdio; ignoring it. "
            "Bearer-token auth only applies to the HTTP transport."
        )
        return None

    if static_tokens and jwks_configured:
        logger.error("AUTH_STATIC_TOKENS and --auth-jwks-uri are mutually exclusive")
        sys.exit(1)

    if jwks_configured:
        if not args.auth_issuer or not args.auth_audience:
            logger.error(
                "--auth-jwks-uri requires --auth-issuer and --auth-audience: "
                "without them any issuer's tokens, or tokens minted for another "
                "service, would be accepted"
            )
            sys.exit(1)
        from fastmcp.server.auth.providers.jwt import JWTVerifier
        logger.info(f"Bearer-token auth enabled (JWKS: {args.auth_jwks_uri})")
        return harden_verifier(JWTVerifier(
            jwks_uri=args.auth_jwks_uri,
            issuer=args.auth_issuer,
            audience=args.auth_audience,
            required_scopes=args.auth_required_scope or None,
        ))

    tokens: Dict[str, Dict[str, Any]] = {}
    for entry in static_tokens.split(","):
        token, sep, client_id = entry.strip().partition(":")
        if not sep or not token or not client_id:
            logger.error(
                "AUTH_STATIC_TOKENS must be 'token:client_id[,token:client_id...]'"
            )
            sys.exit(1)
        tokens[token] = {"client_id": client_id, "scopes": args.auth_required_scope or []}
    from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
    logger.warning(
        "Static-token auth enabled; fine for development, use --auth-jwks-uri "
        "with a real authorization server in production"
    )
    return harden_verifier(StaticTokenVerifier(tokens=tokens, required_scopes=args.auth_required_scope or None))


def _registry_metadata() -> Dict[str, Any]:
    """The repo's server.json with the running server's version stamped in.

    The checked-in file carries the last released version; a deployment built
    from a later commit should describe itself, not the file's snapshot.
    """
    data = json.loads((Path(__file__).parent / "server.json").read_text(encoding="utf-8"))
    data["version"] = SERVER_VERSION
    for package in data.get("packages", []):
        identifier = package.get("identifier", "")
        if ":" in identifier:
            # OCI packages have no separate version field (the registry
            # rejects one); the tag keeps its leading v because Harness tags
            # images with the git tag verbatim.
            package["identifier"] = f"{identifier.rsplit(':', 1)[0]}:v{SERVER_VERSION}"
    return data


def _server_icon() -> "Icon":
    """The repo icon as a self-contained data URI (SEP-973).

    Embedded rather than linked so clients need no network fetch and stdio
    servers have an icon at all.
    """
    import base64

    svg = (Path(__file__).parent / "icon.svg").read_bytes()
    encoded = base64.b64encode(svg).decode("ascii")
    return Icon(src=f"data:image/svg+xml;base64,{encoded}", mimeType="image/svg+xml")


def create_mcp_server(server_name: str, docs_path: Path, runtime_version: str, transform_mode: Optional[str] = "search", auth: Optional["TokenVerifier"] = None) -> FastMCP:
    """Create and configure the MCP server with all tools and resources.

    Args:
        server_name: Name for the MCP server
        docs_path: Path to documentation directory
        runtime_version: Runtime default Laravel version (from --version flag)
        transform_mode: "search" for BM25SearchTransform (default),
                       "code" for CodeMode transform,
                       None for no transforms
        auth: Optional token verifier for the HTTP transport (see
              build_auth_provider); None leaves the server unauthenticated

    Returns:
        Configured FastMCP server instance
    """
    # Store configuration globally for resource handlers
    global _server_config
    _server_config = {
        'docs_path': docs_path,
        'version': runtime_version
    }

    # Create the MCP server
    mcp: FastMCP = FastMCP(
        server_name,
        version=SERVER_VERSION,
        website_url=PROJECT_URL,
        icons=[_server_icon()],
        auth=auth,
        instructions=build_server_instructions(docs_path, runtime_version, transform_mode)
    )
    
    # Registry discovery endpoint (HTTP mode only; stdio never builds the app).
    # Public by design even when the MCP endpoint requires auth: it is the
    # same metadata the MCP Registry republishes to everyone.
    @mcp.custom_route("/.well-known/mcp/server.json", methods=["GET"])
    async def well_known_server_json(request: "Request") -> "JSONResponse":
        return JSONResponse(_registry_metadata())

    # Metrics collection is always on (negligible overhead: one lock and a
    # clock read per call) so the HTTP endpoints never lie about "since when".
    mcp.add_middleware(MetricsMiddleware())
    start_time = time.monotonic()
    metrics_registry.set_info(SERVER_VERSION)
    metrics_registry.set_gauge_callable(
        "laravel_mcp_uptime_seconds",
        lambda: round(time.monotonic() - start_time, 3),
    )

    def _docs_age_days() -> Optional[float]:
        _, age = get_documentation_date(docs_path)
        return float(age) if age is not None else None

    metrics_registry.set_gauge_callable("laravel_mcp_docs_copy_age_days", _docs_age_days)

    def _health_payload() -> tuple[Dict[str, Any], int]:
        versions_available = sum(
            1 for v in SUPPORTED_VERSIONS if (docs_path / v).is_dir() and any((docs_path / v).glob("*.md"))
        )
        current_to, age = get_documentation_date(docs_path)
        stale = copy_is_stale(docs_path)
        if versions_available == 0:
            status, code = "unhealthy", 503
        elif stale:
            status, code = "degraded", 200
        else:
            status, code = "ok", 200
        return {
            "status": status,
            "version": SERVER_VERSION,
            "uptime_seconds": round(time.monotonic() - start_time, 3),
            "docs": {
                "versions_available": versions_available,
                "documentation_current_to": current_to or "unknown",
                # Numeric or null, never a string: monitors parse this field.
                "copy_age_days": age,
                "stale": stale,
            },
        }, code

    # Always public: load balancers cannot do OAuth. "degraded" (stale corpus)
    # still serves traffic; 503 is reserved for "no documentation readable".
    @mcp.custom_route("/healthz", methods=["GET"])
    async def healthz(request: "Request") -> "JSONResponse":
        payload, code = _health_payload()
        return JSONResponse(payload, status_code=code)

    # Custom routes bypass FastMCP's auth middleware (the .well-known route
    # relies on that), so this route enforces its own check with the same
    # TokenVerifier the MCP endpoint uses — token semantics cannot drift.
    @mcp.custom_route("/metrics", methods=["GET"])
    async def metrics_endpoint(request: "Request") -> "Response":
        if auth is not None:
            header = request.headers.get("authorization", "")
            token = header[7:] if header.lower().startswith("bearer ") else ""
            # verify_token is hardened at construction (see harden_verifier):
            # a verifier-side outage returns None rather than raising, so it
            # reads as 401 here — same as FastMCP's own middleware, which
            # verifies first on any request carrying an Authorization header.
            if not token or await auth.verify_token(token) is None:
                return Response(
                    "unauthorized\n", status_code=401,
                    headers={"WWW-Authenticate": "Bearer"},
                    media_type="text/plain",
                )
        return Response(
            render_prometheus(metrics_registry),
            media_type="text/plain; version=0.0.4; charset=utf-8",
        )

    # Initialize multi-source documentation updater
    multi_updater = MultiSourceDocsUpdater(docs_path, runtime_version)
    
    # Define resource handler functions
    def read_laravel_doc(path: str) -> str:
        """Read a specific Laravel documentation file."""
        config = _server_config
        logger.debug(f"read_laravel_doc function called with path: {path}")
        
        # Extract version and relative path, using runtime version as default
        version_inner, relative_path = get_version_from_path(path, config.get('version'))
        
        # Make sure the path ends with .md
        if not relative_path.endswith('.md'):
            relative_path = f"{relative_path}.md"
        
        file_path = Path(config['docs_path']) / version_inner / relative_path
        
        # Security check - read the resolved path this returns, not file_path,
        # so the file that was checked is the file that gets opened.
        version_path = Path(config['docs_path']) / version_inner
        safe_path = resolve_contained_path(version_path, file_path)
        if safe_path is None:
            logger.warning(f"Access denied: {path} (attempted directory traversal)")
            return f"Access denied: {path} (attempted directory traversal)"

        if not safe_path.exists():
            logger.warning(f"Documentation file not found: {safe_path}")
            return f"Documentation file not found: {path} (version: {version_inner})"

        try:
            content = get_file_content_cached(str(safe_path))
            if not content.startswith("Error") and not content.startswith("File not found"):
                logger.debug(f"Successfully read file: {safe_path} ({len(content)} bytes)")
            return content
        except Exception as e:
            logger.error(f"Error reading file {safe_path}: {str(e)}")
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
            
            # Security check - open the resolved path this returns, not
            # file_path, so the check and the open see the same file.
            safe_path = resolve_contained_path(service_dir, file_path)
            if safe_path is None:
                return f"Access denied: {service}/{path} (path traversal attempted)"

            if not safe_path.exists():
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
            
            with open(safe_path, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.debug(f"Successfully read external file: {safe_path} ({len(content)} bytes)")
                return content
        except Exception as e:
            logger.error(f"Error reading external file {service}/{path}: {str(e)}")
            return f"Error reading file: {str(e)}"
    
    # Register resources using functional approach (decorator as function)
    mcp.resource("laravel://{path*}")(read_laravel_doc)
    mcp.resource("laravel-external://{service}/{path*}")(read_external_laravel_doc)
    logger.debug("Registered resource template: laravel://{path*}")
    logger.debug("Registered resource template: laravel-external://{service}/{path*}")
    
    
    # Configure all tools
    configure_mcp_server(mcp, docs_path, runtime_version, multi_updater)

    # Apply transforms
    apply_transforms(mcp, transform_mode)

    return mcp

# Global configuration storage
_server_config: Dict[str, Any] = {}


def configure_mcp_server(mcp: FastMCP, docs_path: Path, runtime_version: str, multi_updater: MultiSourceDocsUpdater) -> None:
    """Configure the MCP server with all tools and resources.
    
    Args:
        mcp: FastMCP server instance
        docs_path: Path to documentation directory
        runtime_version: Runtime default Laravel version (from --version flag)
        multi_updater: Multi-source documentation updater instance
    """
    # Register documentation tools
    @mcp.tool(
        description=TOOL_DESCRIPTIONS["list_laravel_docs"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"docs", "read"},
        output_schema=OUTPUT_SCHEMAS["list_laravel_docs"]
    )
    def list_laravel_docs(version: Optional[str] = None) -> ToolResult:
        """List all available Laravel documentation files.

        Args:
            version: Specific Laravel version to list (e.g., "12.x"). If not provided, lists all versions.
        """
        return toon_result(list_laravel_docs_data(docs_path, version, runtime_version=runtime_version))


    @mcp.tool(
        description=TOOL_DESCRIPTIONS["search_laravel_docs"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"docs", "read"},
        output_schema=OUTPUT_SCHEMAS["search_laravel_docs"]
    )
    def search_laravel_docs(query: str, version: Optional[str] = None, include_external: bool = True, all_versions: bool = False) -> ToolResult:
        """Search through Laravel documentation for a specific term.

        Args:
            query: Search term to look for
            version: Specific Laravel version to search (e.g., "12.x"). Defaults to the configured version.
            include_external: Whether to include external Laravel services documentation in search
            all_versions: Search every supported version instead of just the configured one
        """
        external_dir = multi_updater.external_fetcher.external_dir if include_external else None
        return toon_result(search_laravel_docs_data(docs_path, query, version, include_external, external_dir, runtime_version=runtime_version, all_versions=all_versions))
    
    @mcp.tool(
        description=TOOL_DESCRIPTIONS["update_laravel_docs"],
        annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
        tags={"docs", "write"},
        task=True,
        timeout=120.0
    )
    async def update_laravel_docs(version: Optional[str] = None, force: bool = False) -> str:
        """
        Update Laravel documentation from official GitHub repository.

        Task-capable (SEP-1686): task-aware clients get a handle to poll
        instead of holding the connection open; everyone else runs it
        synchronously as before.

        Args:
            version: Laravel version branch (e.g., "12.x")
            force: Force update even if already up to date
        """
        logger.debug(f"update_laravel_docs function called (version: {version}, force: {force})")

        # Use provided version or default to the one specified at startup
        doc_version = version or runtime_version

        version_error = validate_version_arg(version)
        if version_error:
            return version_error

        def _run() -> str:
            try:
                updater = DocsUpdater(docs_path, doc_version)

                # update() performs its own needs_update() check; calling it here too
                # would spend an extra unauthenticated GitHub API request (60/hr limit).
                updated = updater.update(force=force)

                if not updated:
                    return f"Documentation is already up to date (version: {doc_version})"

                # Clear caches when documentation is updated
                clear_file_cache()

                metadata = get_laravel_docs_metadata(docs_path, doc_version)
                return (
                    f"Documentation updated successfully to {doc_version}\n"
                    f"Commit: {metadata.get('commit_sha', 'unknown')[:7]}\n"
                    f"Date: {metadata.get('commit_date', 'unknown')}\n"
                    f"Message: {metadata.get('commit_message', 'unknown')}"
                )
            except Exception as e:
                logger.error(f"Error updating documentation: {str(e)}")
                return f"Error updating documentation: {str(e)}"

        # The body is blocking urllib I/O; keep it off the event loop so a
        # two-minute update cannot starve every other connected client.
        return await anyio.to_thread.run_sync(_run)
    
    @mcp.tool(
        description=TOOL_DESCRIPTIONS["laravel_docs_info"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"docs", "read"},
        output_schema=OUTPUT_SCHEMAS["laravel_docs_info"]
    )
    def laravel_docs_info(version: Optional[str] = None) -> ToolResult:
        """Get information about the documentation version and status.

        Args:
            version: Specific Laravel version to get info for (e.g., "12.x"). If not provided, shows all versions.

        Returns:
            Documentation metadata as TOON text plus structured content.
        """
        logger.debug(f"laravel_docs_info function called (version: {version})")

        # This tool is implemented inline rather than delegating to an *_impl in
        # mcp_tools, which is how it escaped the validation added everywhere else.
        version_error = validate_version_data(version)
        if version_error:
            return toon_result(version_error)

        if version:
            metadata = get_laravel_docs_metadata(docs_path, version)

            if "version" not in metadata:
                return toon_result(error_data(
                    f"No documentation metadata available for version {version}",
                    {"suggestion": "Use update_laravel_docs() to fetch documentation"}
                ))

            # No staleness note here. An old date means Laravel stopped changing
            # this branch, which is neither a problem nor something a tool can fix.
            documentation_date, _ = get_documentation_date(docs_path, version)
            info: Dict[str, Any] = {
                "version": version,
                "documentation_date": documentation_date or "unknown",
                "last_updated": metadata.get('sync_time', 'unknown'),
                "commit_sha": metadata.get('commit_sha', 'unknown'),
                "commit_date": metadata.get('commit_date', 'unknown'),
                "commit_message": metadata.get('commit_message', 'unknown'),
                "github_url": metadata.get('commit_url', 'unknown')
            }
            return toon_result(info)
        else:
            # Show info for all available versions
            versions_data: List[Dict[str, Any]] = []

            for v in SUPPORTED_VERSIONS:
                metadata = get_laravel_docs_metadata(docs_path, v)
                if "version" in metadata:
                    v_date, _ = get_documentation_date(docs_path, v)
                    versions_data.append({
                        "version": v,
                        "documentation_date": v_date or "unknown",
                        "last_updated": metadata.get('sync_time', 'unknown'),
                        "commit": metadata.get('commit_sha', 'unknown')[:7] if metadata.get('commit_sha') else 'unknown',
                        "available": True
                    })
                else:
                    versions_data.append({
                        "version": v,
                        "available": False
                    })

            # The headline is the NEWEST change across versions. Laravel changes
            # its current branch most days, so that date is a proxy for how old
            # this copy is -- the only part the user can act on. Quoting the
            # oldest instead reports an end-of-life branch that upstream simply
            # stopped touching, and warns forever about nothing.
            current_to, copy_age = get_documentation_date(docs_path)
            summary: Dict[str, Any] = {
                "documentation_current_to": current_to or "unknown",
                "copy_age_days": copy_age if copy_age is not None else "unknown",
                "default_version": runtime_version,
                "versions": versions_data
            }
            if copy_is_stale(docs_path):
                summary["note"] = (
                    f"No version has changed in over {DOCS_STALE_AFTER_DAYS} days, which "
                    "suggests this copy is behind. Pull a newer image to get current "
                    "documentation."
                )
            return toon_result(summary)
    
    # Register package recommendation tools
    @mcp.tool(
        description=TOOL_DESCRIPTIONS["get_laravel_package_recommendations"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"packages", "read"},
        output_schema=OUTPUT_SCHEMAS["get_laravel_package_recommendations"]
    )
    def get_laravel_package_recommendations(use_case: str) -> ToolResult:
        """
        Get Laravel package recommendations based on a use case.

        Args:
            use_case: Description of what the user wants to implement

        Returns:
            Package recommendations as TOON text plus structured content.
        """
        logger.info(f"Searching for packages matching use case: {use_case}")

        # Search for packages by use case
        packages = search_by_use_case(use_case)

        if not packages:
            return toon_result(error_data(f"No packages found matching: '{use_case}'"))

        # Build TOON-friendly package list (limit to top 3)
        packages_data: List[Dict[str, Any]] = []
        for package in packages[:3]:
            packages_data.append({
                "id": package.get('id'),
                "name": package.get('name', package.get('id', 'Unknown Package')),
                "description": package.get('description', 'No description available'),
                "use_cases": package.get('use_cases', []),
                "installation": package.get('installation'),
                "documentation_link": package.get('documentation_link')
            })

        return toon_result({
            "context": f"Packages for: {use_case}",
            "count": len(packages_data),
            "packages": packages_data
        })

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["get_laravel_package_info"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"packages", "read"},
        output_schema=OUTPUT_SCHEMAS["get_laravel_package_info"]
    )
    def get_laravel_package_info(package_name: str) -> ToolResult:
        """
        Get detailed information about a specific Laravel package.

        Args:
            package_name: The name of the package (e.g., 'laravel/cashier')

        Returns:
            Package information as TOON text plus structured content.
        """
        logger.info(f"Getting information for package: {package_name}")

        # Get the package information
        if package_name not in PACKAGE_CATALOG:
            return toon_result(error_data(f"Package '{package_name}' not found"))

        package = PACKAGE_CATALOG[package_name].copy()
        package['id'] = package_name

        return toon_result(package_recommendation_data(package))
    
    @mcp.tool(
        description=TOOL_DESCRIPTIONS["get_laravel_package_categories"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"packages", "read"}
    )
    def get_laravel_package_categories(category: str) -> str:
        """
        Get Laravel packages in a specific category.

        Args:
            category: The category to filter by (e.g., 'authentication', 'payment')

        Returns:
            TOON-encoded list of packages in the category.
        """
        logger.info(f"Getting packages for category: {category}")

        # Find packages in the category
        matches: List[Dict[str, Any]] = []
        category_lower = category.lower()

        for pkg_id, pkg_info in PACKAGE_CATALOG.items():
            if any(cat.lower() == category_lower for cat in pkg_info.get('categories', [])):
                matches.append({
                    "id": pkg_id,
                    "name": pkg_info.get('name', pkg_id),
                    "description": pkg_info.get('description', 'No description available'),
                    "installation": pkg_info.get('installation'),
                    "documentation_link": pkg_info.get('documentation_link')
                })

        if not matches:
            return format_error(f"No packages found in category: '{category}'")

        return format_package_list(matches, f"Category: {category}")
    
    @mcp.tool(
        description=TOOL_DESCRIPTIONS["get_features_for_laravel_package"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"packages", "read"}
    )
    def get_features_for_laravel_package(package: str) -> str:
        """
        Get available features/implementations for a Laravel package.

        Args:
            package: The Laravel package name (e.g., 'laravel/cashier')

        Returns:
            TOON-encoded list of features.
        """
        logger.info(f"Getting features for package: {package}")

        # Check if the package exists
        if package not in PACKAGE_CATALOG:
            return format_error(f"Package '{package}' not found")

        # Get features from the feature map
        features = FEATURE_MAP.get(package, [])
        package_info = PACKAGE_CATALOG[package]

        return toon_encode({
            "package": package,
            "name": package_info.get('name', package),
            "features": features if features else package_info.get('use_cases', [])[:5],
            "has_defined_features": bool(features)
        })

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["read_laravel_doc_content"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"docs", "read"}
    )
    def read_laravel_doc_content(filename: str, version: Optional[str] = None) -> str:
        """
        Read a specific Laravel documentation file.
        
        Args:
            filename: Name of the file (e.g., 'mix.md', 'vite.md')
            version: Laravel version (e.g., '12.x'). Defaults to latest.
        
        Returns:
            Full markdown content of the documentation file
        """
        return read_laravel_doc_content_impl(docs_path, filename, version, runtime_version=runtime_version)

    @mcp.tool(
        description=(
            "Read one section of a Laravel documentation file by the anchor or "
            "heading returned by search_laravel_docs. Prefer this over "
            "read_laravel_doc_content: a whole file can exceed 30,000 tokens, "
            "while a section is typically a few hundred."
        ),
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"docs", "read"}
    )
    def read_laravel_doc_section(filename: str, section: str, version: Optional[str] = None) -> str:
        """Read a single documentation section.

        Args:
            filename: Documentation file, e.g. 'queues.md'
            section: Anchor or heading, e.g. 'dealing-with-failed-jobs'
            version: Laravel version. Defaults to the configured version.
        """
        return read_laravel_doc_section_impl(
            docs_path, filename, section, version, runtime_version=runtime_version
        )

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["get_doc_structure"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"docs", "read"}
    )
    def get_doc_structure(filename: str, version: Optional[str] = None) -> str:
        """
        Get the table of contents / structure of a documentation file.
        
        Args:
            filename: Documentation file name
            version: Laravel version
        
        Returns:
            Structured outline of the document
        """
        return get_doc_structure_impl(docs_path, filename, version, runtime_version=runtime_version)

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["browse_docs_by_category"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"docs", "read"}
    )
    def browse_docs_by_category(category: str, version: Optional[str] = None) -> str:
        """
        Browse documentation files by category.
        
        Args:
            category: Category like 'frontend', 'database', 'authentication', etc.
            version: Laravel version
        
        Returns:
            List of relevant documentation files
        """
        return browse_docs_by_category_impl(docs_path, category, version, runtime_version=runtime_version)

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["verify_laravel_feature"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"docs", "read"}
    )
    def verify_laravel_feature(feature: str, version: Optional[str] = None) -> str:
        """Quickly verify if a Laravel feature/topic exists in documentation.

        Args:
            feature: Feature name or topic to verify (e.g., "blade", "eloquent", "sanctum")
            version: Specific Laravel version to check (e.g., "12.x"). Defaults to configured version.
        """
        return verify_laravel_feature_impl(docs_path, feature, version, runtime_version=runtime_version)

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["compare_laravel_versions"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"docs", "read"}
    )
    def compare_laravel_versions(from_version: str, to_version: str, file_filter: Optional[str] = None) -> str:
        """Compare documentation files between two Laravel versions.

        Args:
            from_version: Starting Laravel version (e.g., "11.x")
            to_version: Target Laravel version (e.g., "12.x")
            file_filter: Optional substring to filter files (e.g., "auth" shows only auth-related changes)
        """
        return compare_laravel_versions_impl(docs_path, from_version, to_version, file_filter, runtime_version=runtime_version)

    # Register external documentation tools
    @mcp.tool(
        description=TOOL_DESCRIPTIONS["update_external_laravel_docs"],
        annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
        tags={"external", "write"},
        task=True,
        timeout=300.0
    )
    async def update_external_laravel_docs(services: Optional[List[str]] = None, force: bool = False) -> str:
        """
        Update documentation for external Laravel services.

        Task-capable (SEP-1686): this is the five-minute call, so task-aware
        clients poll instead of blocking on it.

        Args:
            services: List of services to update (forge, vapor, envoyer, nova). If None, updates all.
            force: Force update even if cache is valid

        Returns:
            Status of the update operation
        """
        logger.info(f"Updating external Laravel services documentation (services: {services}, force: {force})")

        def _run() -> str:
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

        # Blocking urllib I/O with retries and sleeps; keep it off the event loop.
        return await anyio.to_thread.run_sync(_run)

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["list_laravel_services"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"external", "read"}
    )
    def list_laravel_services() -> str:
        """
        List all available Laravel services with external documentation.

        Returns:
            TOON-encoded list of available Laravel services.
        """
        logger.debug("Listing available Laravel services")

        try:
            services = multi_updater.external_fetcher.list_available_services()
            services_data: List[Dict[str, Any]] = []

            for service in services:
                service_info = multi_updater.external_fetcher.get_service_info(service)
                if service_info:
                    service_type = service_info.get('type', 'unknown')
                    if hasattr(service_type, 'value'):
                        service_type = service_type.value

                    services_data.append({
                        "id": service,
                        "name": service_info.get('name', service),
                        "type": service_type,
                        "url": service_info.get('base_url') or service_info.get('repo'),
                        "cache_valid": multi_updater.external_fetcher.is_cache_valid(service)
                    })

            return format_service_list(services_data)
        except Exception as e:
            logger.error(f"Error listing Laravel services: {str(e)}")
            return format_error(f"Error listing Laravel services: {str(e)}")

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["search_external_laravel_docs"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"external", "read"}
    )
    def search_external_laravel_docs(query: str, services: Optional[List[str]] = None) -> str:
        """
        Search through external Laravel service documentation.

        Args:
            query: Search term to look for
            services: List of services to search. If None, searches all cached services.

        Returns:
            TOON-encoded search results from external documentation.
        """
        logger.debug(f"Searching external Laravel docs for: {query}")

        if not query.strip():
            return format_error("Search query cannot be empty")

        try:
            external_dir = multi_updater.external_fetcher.external_dir

            if not external_dir.exists():
                return format_error(
                    "No external documentation found",
                    {"suggestion": "Use update_external_laravel_docs() to fetch documentation first"}
                )

            # Determine which services to search
            if services:
                available_services = multi_updater.external_fetcher.list_available_services()
                invalid_services = [s for s in services if s not in available_services]
                if invalid_services:
                    return format_error(
                        f"Invalid services: {', '.join(invalid_services)}",
                        {"available_services": available_services}
                    )
                search_services = services
            else:
                search_services = [d.name for d in external_dir.iterdir() if d.is_dir()]

            results_data: List[Dict[str, Any]] = []
            pattern = re.compile(re.escape(query), re.IGNORECASE)

            for service in search_services:
                service_dir = external_dir / service
                if not service_dir.exists():
                    continue

                service_matches: List[Dict[str, Any]] = []
                for file_path in service_dir.glob("*.md"):
                    try:
                        content = get_file_content_cached(str(file_path))
                        # The cached reader signals failure with a sentinel string;
                        # matching against it would fabricate hits for queries like
                        # "error" or "file" on a file that was never read.
                        if content.startswith("Error") or content.startswith("File not found"):
                            continue
                        count = count_matches(pattern, content)
                        if count:
                            service_matches.append({
                                "file": file_path.name,
                                "matches": count
                            })
                    except Exception as e:
                        logger.warning(f"Error searching {file_path}: {str(e)}")
                        continue

                if service_matches:
                    results_data.append({
                        "service": service,
                        "files": service_matches
                    })

            if not results_data:
                return format_error(f"No results found for '{query}' in external documentation")

            return toon_encode({
                "query": query,
                "results": results_data,
                "service_count": len(results_data)
            })
        except Exception as e:
            logger.error(f"Error searching external documentation: {str(e)}")
            return format_error(f"Error searching external documentation: {str(e)}")

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["get_laravel_service_info"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"external", "read"}
    )
    def get_laravel_service_info(service: str) -> str:
        """
        Get detailed information about a specific Laravel service.

        Args:
            service: Service name (forge, vapor, envoyer, nova)

        Returns:
            TOON-encoded detailed information about the service.
        """
        logger.debug(f"Getting information for Laravel service: {service}")

        try:
            service_info = multi_updater.external_fetcher.get_service_info(service)

            if not service_info:
                available_services = multi_updater.external_fetcher.list_available_services()
                return format_error(
                    f"Service '{service}' not found",
                    {"available_services": available_services}
                )

            # Service type
            service_type = service_info.get('type', 'unknown')
            if hasattr(service_type, 'value'):
                service_type = service_type.value

            data: Dict[str, Any] = {
                "id": service,
                "name": service_info.get('name', service),
                "type": service_type,
                "cache_valid": multi_updater.external_fetcher.is_cache_valid(service)
            }

            if 'base_url' in service_info:
                data["documentation_url"] = service_info['base_url']
                if 'sections' in service_info:
                    data["available_sections"] = service_info['sections']
            elif 'repo' in service_info:
                data["github_repo"] = service_info['repo']
                data["branch"] = service_info.get('branch', 'main')

            # Try to get cache metadata
            metadata_path = multi_updater.external_fetcher.get_cache_metadata_path(service)
            if metadata_path.exists():
                try:
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)

                    if 'cached_at' in metadata:
                        import datetime
                        cache_time = datetime.datetime.fromtimestamp(metadata['cached_at'])
                        data["last_fetched"] = cache_time.strftime('%Y-%m-%d %H:%M:%S')

                    if 'success_rate' in metadata:
                        data["success_rate"] = metadata['success_rate']

                    if 'fetched_sections' in metadata:
                        data["fetched_sections"] = metadata['fetched_sections']
                except Exception:
                    pass

            return toon_encode(data)
        except Exception as e:
            logger.error(f"Error getting service info: {str(e)}")
            return format_error(f"Error getting service info: {str(e)}")

    # Register learning resource and discovery tools
    @mcp.tool(
        description=TOOL_DESCRIPTIONS["find_laravel_docs_for_need"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"learning", "read"}
    )
    def find_laravel_docs_for_need(need: str, version: Optional[str] = None) -> str:
        """Find Laravel documentation for a specific user need."""
        return find_laravel_docs_for_need_impl(docs_path, need, version, runtime_version=runtime_version)

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["get_laravel_learning_path"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"learning", "read"}
    )
    async def get_laravel_learning_path(ctx: Context, path_name: str = "") -> str:
        """Get a specific curated learning path.

        Called without a path, asks the client to pick one (elicitation).
        Clients that decline, cancel, or cannot elicit get the listing —
        exactly the pre-elicitation behavior.
        """
        if not path_name:
            choices: Dict[str, Dict[str, str]] = {
                key: {
                    "title": (
                        f"{path['name']} "
                        f"({getattr(path['difficulty'], 'value', path['difficulty'])}, "
                        f"~{path['estimated_hours']}h)"
                    )
                }
                for key, path in LEARNING_PATHS.items()
            }
            try:
                # mypy resolves the elicit overload's unbound TypeVar to None
                # for the titled-enum dict form; the runtime accepts it.
                result = await ctx.elicit(
                    "Which learning path would you like?",
                    response_type=choices,  # type: ignore[arg-type]
                )
            except Exception:
                # Client doesn't support elicitation; fall back to the listing.
                return get_laravel_learning_path_impl("")
            if result.action == "accept":
                path_name = str(result.data)
            else:
                return get_laravel_learning_path_impl("")
        return get_laravel_learning_path_impl(path_name)

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["list_laravel_learning_paths"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"learning", "read"}
    )
    def list_laravel_learning_paths() -> str:
        """List all available learning paths."""
        return list_laravel_learning_paths_impl()

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["get_laravel_content_by_difficulty"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"learning", "read"}
    )
    def get_laravel_content_by_difficulty(difficulty: str, version: Optional[str] = None) -> str:
        """Get Laravel documentation filtered by difficulty level."""
        return get_laravel_content_by_difficulty_impl(docs_path, difficulty, version, runtime_version=runtime_version)

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["get_related_laravel_packages"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"packages", "read"}
    )
    def get_related_laravel_packages(package: str) -> str:
        """Get packages related to a specific Laravel package."""
        return get_related_laravel_packages_impl(package)

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["search_laravel_learning_resources"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"learning", "read"}
    )
    def search_laravel_learning_resources(query: str, sources: Optional[List[str]] = None) -> str:
        """Search through learning resources."""
        return search_laravel_learning_resources_impl(docs_path, query, sources, runtime_version=runtime_version)

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["list_laravel_learning_resources"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"learning", "read"}
    )
    def list_laravel_learning_resources(source: Optional[str] = None) -> str:
        """List available learning resources."""
        return list_laravel_learning_resources_impl(docs_path, source)

    @mcp.tool(
        description=TOOL_DESCRIPTIONS["list_laravel_categories"],
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"docs", "read"}
    )
    def list_laravel_categories() -> str:
        """List all documentation categories."""
        return list_laravel_categories_impl()

    # Register prompts to demonstrate common use cases
    @mcp.prompt(name="laravel-authentication-setup")
    def prompt_authentication_setup() -> str:
        """Guide user through setting up authentication in Laravel"""
        return """I need help setting up authentication in my Laravel application.

Please help me:
1. Understand the available authentication options in Laravel
2. Choose the right authentication package for my needs
3. Get step-by-step implementation guidance

Start by searching the Laravel documentation for authentication options and recommending appropriate packages."""

    @mcp.prompt(name="find-payment-solution")
    def prompt_payment_solution() -> str:
        """Help user find and implement payment processing"""
        return """I need to add payment processing to my Laravel application.

Please help me:
1. Find Laravel packages for payment processing
2. Compare different payment solutions (Stripe, Paddle, etc.)
3. Provide installation and setup instructions

Start by searching for payment-related packages."""

    @mcp.prompt(name="laravel-forge-deployment")
    def prompt_forge_deployment() -> str:
        """Guide user through Laravel Forge deployment"""
        return """I want to deploy my Laravel application using Laravel Forge.

Please help me:
1. Understand what Laravel Forge is and what it does
2. Learn about server provisioning and deployment
3. Get guidance on setting up deployments

Start by providing information about Laravel Forge and its key features."""


def apply_transforms(mcp: FastMCP, transform_mode: Optional[str] = "search") -> None:
    """Apply search or code mode transforms to the MCP server.

    Args:
        mcp: FastMCP server instance
        transform_mode: "search" for BM25SearchTransform (default),
                       "code" for CodeMode transform,
                       None for no transforms
    """
    if transform_mode is None:
        logger.info("No transforms applied (raw tool mode)")
        return

    if transform_mode == "code":
        try:
            from fastmcp.experimental.transforms.code_mode import (
                CodeMode,
                GetTags,
                Search,
                GetSchemas,
            )
        except ImportError as e:
            raise RuntimeError(
                "Code Mode requires the code-mode extra. "
                "Install with: pip install 'fastmcp[code-mode]'"
            ) from e

        code_mode = CodeMode(
            discovery_tools=[GetTags(), Search(), GetSchemas()],
        )
        mcp.add_transform(code_mode)
        logger.info("Code Mode transform applied (experimental)")
    elif transform_mode == "search":
        mcp.add_transform(BM25SearchTransform(
            max_results=10,
            # Search returns section anchors; reading one is the other half of
            # the same move. Leaving the reader behind a search_tools lookup put
            # a round trip in the middle of the most common path.
            always_visible=["search_laravel_docs", "read_laravel_doc_section"],
        ))
        logger.info(
            "BM25 Search transform applied (max_results=10; search_laravel_docs "
            "and read_laravel_doc_section pinned)"
        )
    else:
        raise ValueError(f"Unknown transform_mode: {transform_mode!r}. Use 'search', 'code', or None.")


def build_http_app(args, mcp: FastMCP):
    """Assemble the HTTP app: host/origin guard, CORS, bind address.

    Extracted from main() so the assembled result is testable in-process;
    binding the socket stays in main(). Returns (app, host, port).
    """
    from starlette.middleware.cors import CORSMiddleware

    # Use PORT from environment or args, default to 8081. An explicit
    # --port 0 stays 0 (ephemeral bind); only an omitted port defaults.
    # Bind loopback by default: this server ships no authentication unless
    # auth flags are configured, so every tool is exposed to anyone who can
    # reach the socket.
    port = args.port if args.port is not None else 8081
    host = args.host or "127.0.0.1"
    is_loopback = host in ("127.0.0.1", "::1", "localhost")

    # FastMCP's origin guard matches allowed_origins with fnmatch, the same
    # way it matches allowed hosts: "https://*.example.com" in this list lets
    # any matching Origin through the DNS-rebinding protection while
    # presenting as a scoped allowlist. Reject every pattern entry loudly,
    # exactly like the ALLOWED_HOSTS check in parse_arguments.
    cors_origins = args.cors_origin or []
    pattern_origins = [o for o in cors_origins if any(c in o for c in "*?[")]
    if pattern_origins:
        logger.error(
            f"wildcard patterns are not accepted in CORS origins: {', '.join(pattern_origins)}. "
            "Pass explicit origins."
        )
        sys.exit(1)

    if not is_loopback:
        logger.warning(
            f"Binding {host} exposes the MCP server to the network. "
            "Restrict access at the network layer and set --allowed-host."
        )

    # Enable FastMCP's Host/Origin guard (off by default upstream). Strict
    # mode is required off-loopback, where the 'auto' heuristic disengages.
    app = mcp.http_app(
        host_origin_protection="auto" if is_loopback else True,
        allowed_hosts=args.allowed_host or None,
        allowed_origins=cors_origins or None,
    )

    # Browser clients need CORS; everything else does not. Only add the
    # middleware when explicit origins are configured, and never reflect
    # arbitrary origins with credentials attached.
    if cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=False,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["content-type", "mcp-session-id", "mcp-protocol-version", "authorization"],
            expose_headers=["mcp-session-id", "mcp-protocol-version"],
            max_age=86400,
        )
        logger.info(f"CORS enabled for: {', '.join(cors_origins)}")

    return app, host, port


def main():
    """Main entry point for the Laravel MCP Companion."""
    args = parse_arguments()
    
    # Setup server environment
    docs_path = setup_server_environment(args)
    
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
    
    # Resolve transform mode (--code-mode is a deprecated alias for --transform-mode code)
    if args.transform_mode is not None:
        mode = args.transform_mode
        if args.code_mode and mode != "code":
            logger.warning(f"--code-mode ignored because --transform-mode={mode} was given")
    elif args.code_mode:
        logger.warning("--code-mode is deprecated; use --transform-mode code")
        mode = "code"
    else:
        mode = "search"

    if mode == "code" and args.transport == "http":
        logger.warning(
            "Code Mode over HTTP exposes an execution endpoint. "
            "Do not expose this publicly unless you have reviewed sandbox and network risk."
        )

    # Create and configure the MCP server
    mcp = create_mcp_server(
        args.server_name, docs_path, args.version,
        transform_mode=None if mode == "none" else mode,
        auth=build_auth_provider(args)
    )

    # Log server startup
    logger.info(f"Starting Laravel MCP Companion ({args.server_name})")
    logger.info(f"Transport: {args.transport}")
    logger.info(f"Transform mode: {mode}")
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
        if args.transport == "http":
            # HTTP mode for web-based deployments
            logger.info("Starting in HTTP mode...")
            import uvicorn

            app, host, port = build_http_app(args, mcp)
            logger.info(f"Listening on {host}:{port}")

            uvicorn.run(app, host=host, port=port, log_level="info")
        else:
            logger.info("Server ready. Press Ctrl+C to stop.")
            mcp.run()
    except Exception as e:
        logger.critical(f"Server error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
