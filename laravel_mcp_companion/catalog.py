"""The curated package catalog: what each package is for and how it relates to the others.

This is hand-written content, not fetched documentation. `PACKAGE_CATALOG`
describes each package; `FEATURE_MAP` lists what one typically builds with it;
`learning_resources.RELATED_PACKAGES` records which packages go together. The
functions here read those three tables and return plain data.
"""

import re
from typing import Any, Dict, List, Optional

from .learning_resources import RELATED_PACKAGES

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
        "documentation_link": "laravel://billing.md",
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
        "documentation_link": "laravel://sanctum.md",
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
        "documentation_link": "laravel://scout.md"
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
        "documentation_link": "laravel://passport.md",
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
        "documentation_link": "laravel://starter-kits.md",
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
        "documentation_link": "laravel-package://livewire/quickstart.md",
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
        "documentation_link": "laravel://fortify.md",
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
        "documentation_link": "laravel-package://spatie/laravel-permission/introduction.md"
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
        "documentation_link": "laravel-package://inertia/how-it-works.md",
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
        "documentation_link": "laravel://starter-kits.md",
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
        "documentation_link": "laravel-package://spatie/laravel-medialibrary/introduction.md"
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
        "documentation_link": "laravel-package://debugbar/installation.md"
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
        "documentation_link": "laravel://cashier-paddle.md"
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


_STOP_WORDS = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'to', 'for', 'in', 'with'}


def find_package(name: str) -> Optional[str]:
    """The catalog id a name refers to: the id itself, or the one id it is part
    of ("cashier" for "laravel/cashier"). None when nothing or several match."""
    wanted = name.lower().strip()
    if not wanted:
        return None
    for package_id in PACKAGE_CATALOG:
        if package_id.lower() == wanted:
            return package_id
    # "cashier" names laravel/cashier, not laravel/cashier-paddle as well.
    unqualified = [package_id for package_id in PACKAGE_CATALOG if package_id.lower().split("/")[-1] == wanted]
    if len(unqualified) == 1:
        return unqualified[0]
    partial = [package_id for package_id in PACKAGE_CATALOG if wanted in package_id.lower()]
    return partial[0] if len(partial) == 1 else None


def package_record(package_id: str) -> Dict[str, Any]:
    """Everything the catalog says about one package, in one object."""
    entry = PACKAGE_CATALOG[package_id]
    record: Dict[str, Any] = {
        "id": package_id,
        "name": entry.get("name", package_id),
        "description": entry.get("description", ""),
        "categories": list(entry.get("categories", [])),
        "use_cases": list(entry.get("use_cases", [])),
        "installation": entry.get("installation", ""),
        "features": list(FEATURE_MAP.get(package_id, [])),
        "related": list(RELATED_PACKAGES.get(package_id, [])),
        "documentation_link": entry.get("documentation_link", ""),
    }
    if entry.get("legacy"):
        record["legacy"] = True
        if entry.get("superseded_by"):
            record["superseded_by"] = entry["superseded_by"]
    return record


def package_summary(package_id: str) -> Dict[str, Any]:
    """The short form used in lists."""
    entry = PACKAGE_CATALOG[package_id]
    summary: Dict[str, Any] = {
        "id": package_id,
        "name": entry.get("name", package_id),
        "description": entry.get("description", ""),
        "categories": list(entry.get("categories", [])),
        "installation": entry.get("installation", ""),
        "documentation_link": entry.get("documentation_link", ""),
    }
    if entry.get("legacy"):
        summary["legacy"] = True
    return summary


def all_categories() -> List[str]:
    return sorted({category for entry in PACKAGE_CATALOG.values() for category in entry.get("categories", [])})


def packages_in_category(category: str) -> List[str]:
    wanted = category.lower().strip()
    return [
        package_id for package_id, entry in PACKAGE_CATALOG.items()
        if wanted in (c.lower() for c in entry.get("categories", []))
    ]


def search_by_use_case(use_case: str) -> List[Dict[str, Any]]:
    """Catalog entries ranked by how well they match a description of a need.

    A word of the description counts 2 when it appears in one of a package's
    categories, 1 in one of its use cases and 0.5 in its name or description.
    Current packages rank ahead of legacy ones on an equal score. Each entry
    is returned with its `id` and `score`.
    """
    words = set(re.findall(r'\b\w+\b', use_case.lower())) - _STOP_WORDS

    scores: Dict[str, float] = {}
    for package_id, entry in PACKAGE_CATALOG.items():
        score = 0.0
        for category in entry.get('categories', []):
            if any(word in category.lower() for word in words):
                score += 2
        for candidate in entry.get('use_cases', []):
            lowered = candidate.lower()
            score += sum(1 for word in words if word in lowered)
        name_and_description = f"{entry.get('name', '')} {entry.get('description', '')}".lower()
        score += sum(0.5 for word in words if word in name_and_description)
        if score > 0:
            scores[package_id] = score

    ranked = sorted(scores.items(), key=lambda item: (item[1], not PACKAGE_CATALOG[item[0]].get("legacy", False)), reverse=True)
    return [{**PACKAGE_CATALOG[package_id], "id": package_id, "score": score} for package_id, score in ranked]
