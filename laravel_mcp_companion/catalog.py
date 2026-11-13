"""The curated package catalog: what each package is for and how it relates to the others.

This is hand-written content, not fetched documentation. `PACKAGE_CATALOG`
describes each package; `FEATURE_MAP` lists what one typically builds with it;
`learning_resources.RELATED_PACKAGES` records which packages go together. The
functions here read those three tables and return plain data.
"""

import re
from typing import Any, Dict, List, Optional

from .learning_resources import RELATED_PACKAGES

PACKAGE_CATALOG: Dict[str, Dict[str, Any]] = {
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
        "documentation_link": "laravel://billing.md"
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
        "documentation_link": "laravel://sanctum.md"
    },
    "laravel/scout": {
        "name": "Laravel Scout",
        "description": "Laravel Scout provides a simple, driver-based solution for adding full-text search to Eloquent models, with Algolia, Meilisearch and Typesense drivers and built-in database and collection engines.",
        "categories": ["search", "database", "indexing"],
        "use_cases": [
            "Adding full-text search to your application",
            "Making Eloquent models searchable",
            "Implementing search with Algolia, Meilisearch or Typesense",
            "Searching with the database engine, with no external service",
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
        "documentation_link": "laravel://passport.md"
    },
    "laravel/breeze": {
        "name": "Laravel Breeze",
        "legacy": True,
        "superseded_by": "laravel/starter-kits",
        "description": "Laravel Breeze is a minimal, simple implementation of all of Laravel's authentication features, including login, registration, password reset, email verification, and password confirmation. New applications use Laravel's starter kits instead; Breeze is documented up to Laravel 11.",
        "categories": ["authentication", "frontend", "scaffolding"],
        "use_cases": [
            "Quickly scaffolding authentication views and routes",
            "Setting up a basic Laravel authentication system",
            "Creating a starting point for authentication with Tailwind CSS"
        ],
        "installation": "composer require laravel/breeze --dev",
        "documentation_link": "laravel://11.x/starter-kits.md"
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
        "documentation_link": "laravel-package://livewire/quickstart.md"
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
        "documentation_link": "laravel://fortify.md"
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
        "documentation_link": "laravel-package://inertia/how-it-works.md"
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
        "legacy": True,
        "superseded_by": "laravel/starter-kits",
        "description": "Laravel Jetstream is a beautifully designed application starter kit for Laravel and provides the perfect starting point for your next Laravel application. Jetstream provides the implementation for your application's login, registration, email verification, two-factor authentication, session management, API via Laravel Sanctum, and optional team management features.",
        "categories": ["authentication", "frontend", "scaffolding", "teams"],
        "use_cases": [
            "Building applications with team support",
            "Implementing two-factor authentication",
            "Creating API tokens for users",
            "Setting up profile management"
        ],
        "installation": "composer require laravel/jetstream",
        "documentation_link": "https://jetstream.laravel.com"
    },
    "laravel/octane": {
        "name": "Laravel Octane",
        "description": "Laravel Octane supercharges your application's performance by serving your application using high-powered application servers, including FrankenPHP, RoadRunner and Swoole.",
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
        "description": "Laravel Socialite provides an expressive, fluent interface to OAuth authentication with Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket and Slack.",
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
        "legacy": True,
        "superseded_by": "laravel/cloud",
        "description": "Laravel Vapor is a serverless deployment platform for Laravel, powered by AWS Lambda. Deploy infinitely scalable Laravel applications without managing servers. Laravel Cloud is the current first-party platform for new deployments.",
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
        "legacy": True,
        "superseded_by": "laravel/forge",
        "description": "Laravel Envoyer provides zero-downtime deployment for PHP applications. Deploy your code without bringing your application offline. Laravel Forge now performs zero-downtime deployments itself.",
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
    },
    "laravel/starter-kits": {
        "name": "Laravel Starter Kits",
        "description": "Laravel's starter kits scaffold a new application with authentication already built: login, registration, password reset, email verification and two-factor authentication, on a React, Svelte, Vue or Livewire frontend, with optional teams and WorkOS AuthKit.",
        "categories": ["authentication", "scaffolding", "frontend", "starter-kit"],
        "use_cases": [
            "Starting a new application with authentication scaffolding in place",
            "Choosing a React, Svelte, Vue or Livewire frontend at project creation",
            "Adding two-factor authentication and team support from the start",
            "Delegating authentication to WorkOS AuthKit"
        ],
        "installation": "laravel new my-app",
        "documentation_link": "laravel://starter-kits.md"
    },
    "laravel/cloud": {
        "name": "Laravel Cloud",
        "description": "Laravel Cloud is a fully managed infrastructure platform for deploying and scaling Laravel applications, with built-in web and worker compute, relational databases, caches, managed queues and object storage.",
        "categories": ["deployment", "hosting", "scaling", "devops"],
        "use_cases": [
            "Deploying a Laravel application without managing servers",
            "Scaling web and worker compute with traffic",
            "Provisioning a managed database, cache or queue alongside the application",
            "Preview environments for pull requests"
        ],
        "installation": "Web service - No installation required",
        "documentation_link": "laravel-external://cloud/intro"
    },
    "laravel/nightwatch": {
        "name": "Laravel Nightwatch",
        "description": "Laravel Nightwatch monitors a Laravel application in production: requests, exceptions, queries, jobs, mail, notifications, scheduled tasks and outgoing requests, with alerts to Slack, Linear and webhooks.",
        "categories": ["monitoring", "debugging", "performance", "devops"],
        "use_cases": [
            "Monitoring a production application's requests and exceptions",
            "Finding slow queries, jobs and outgoing requests",
            "Being alerted to new exceptions in Slack or Linear",
            "Tracing what one user or one request did"
        ],
        "installation": "composer require laravel/nightwatch",
        "documentation_link": "laravel-external://nightwatch/start-guide"
    },
    "laravel/herd": {
        "name": "Laravel Herd",
        "description": "Laravel Herd is a native Laravel and PHP development environment for macOS and Windows. It includes everything needed to start developing with Laravel, and Herd Pro adds local services.",
        "categories": ["development", "local-development", "environment"],
        "use_cases": [
            "Setting up a local development environment on macOS or Windows",
            "Running several PHP versions side by side",
            "Serving local sites without Docker",
            "Running local databases and other services with Herd Pro"
        ],
        "installation": "Desktop application - download from https://herd.laravel.com",
        "documentation_link": "laravel-external://herd/macos/getting-started/installation"
    },
    "laravel/sail": {
        "name": "Laravel Sail",
        "description": "Laravel Sail is a light-weight command-line interface for interacting with Laravel's default Docker development environment, a starting point for building with PHP, MySQL and Redis without prior Docker experience.",
        "categories": ["development", "local-development", "docker", "environment"],
        "use_cases": [
            "Running a local development environment in Docker",
            "Giving a whole team the same environment",
            "Adding MySQL, PostgreSQL, Redis or Meilisearch containers to a project"
        ],
        "installation": "composer require laravel/sail --dev",
        "documentation_link": "laravel://sail.md"
    },
    "laravel/homestead": {
        "name": "Laravel Homestead",
        "legacy": True,
        "superseded_by": "laravel/sail",
        "description": "Laravel Homestead is a pre-packaged Vagrant box for local development. It is a legacy package that is no longer actively maintained; Laravel's documentation names Sail as the modern alternative.",
        "categories": ["development", "local-development", "environment"],
        "use_cases": [
            "Maintaining a project whose local environment already runs on Homestead"
        ],
        "installation": "composer require laravel/homestead --dev",
        "documentation_link": "laravel://homestead.md"
    },
    "laravel/valet": {
        "name": "Laravel Valet",
        "legacy": True,
        "superseded_by": "laravel/herd",
        "description": "Laravel Valet is a minimal development environment for macOS that serves local sites with Nginx and DnsMasq. Laravel's documentation points to Herd as the easier way to develop on macOS or Windows.",
        "categories": ["development", "local-development", "environment"],
        "use_cases": [
            "Maintaining a macOS setup that already uses Valet"
        ],
        "installation": "composer global require laravel/valet",
        "documentation_link": "laravel://valet.md"
    },
    "pestphp/pest": {
        "name": "Pest",
        "description": "Pest is a PHP testing framework with a focus on simplicity. Laravel supports testing with Pest out of the box, and the framework's testing documentation shows its examples in both Pest and PHPUnit.",
        "categories": ["testing", "development"],
        "use_cases": [
            "Writing feature and unit tests in a concise, expressive syntax",
            "Testing HTTP endpoints, the database and console commands",
            "Adopting the test style Laravel's own documentation leads with"
        ],
        "installation": "composer require pestphp/pest --dev --with-all-dependencies",
        "documentation_link": "laravel://testing.md"
    },
    "laravel/dusk": {
        "name": "Laravel Dusk",
        "description": "Laravel Dusk provides an expressive, easy-to-use browser automation and testing API.",
        "categories": ["testing", "browser"],
        "use_cases": [
            "End-to-end testing in a real browser",
            "Testing JavaScript-driven pages",
            "Automating browser interactions"
        ],
        "installation": "composer require laravel/dusk --dev",
        "documentation_link": "laravel://dusk.md"
    },
    "laravel/reverb": {
        "name": "Laravel Reverb",
        "description": "Laravel Reverb brings fast, scalable real-time WebSocket communication directly to a Laravel application, integrated with Laravel's event broadcasting tools.",
        "categories": ["realtime", "websockets", "broadcasting"],
        "use_cases": [
            "Running a first-party WebSocket server",
            "Broadcasting events to the browser in real time",
            "Live notifications, chat and presence channels"
        ],
        "installation": "php artisan install:broadcasting",
        "documentation_link": "laravel://reverb.md"
    },
    "laravel/pulse": {
        "name": "Laravel Pulse",
        "description": "Laravel Pulse delivers at-a-glance insights into an application's performance and usage: slow jobs and endpoints, the most active users and more.",
        "categories": ["monitoring", "performance", "dashboard"],
        "use_cases": [
            "A self-hosted performance dashboard",
            "Finding slow endpoints, queries and jobs",
            "Seeing which users are most active"
        ],
        "installation": "composer require laravel/pulse",
        "documentation_link": "laravel://pulse.md"
    },
    "laravel/pennant": {
        "name": "Laravel Pennant",
        "description": "Laravel Pennant is a simple, light-weight feature flag package for rolling out features incrementally, A/B testing and trunk-based development.",
        "categories": ["feature-flags", "development"],
        "use_cases": [
            "Rolling a feature out to a share of users",
            "A/B testing an interface",
            "Gating unfinished work behind a flag"
        ],
        "installation": "composer require laravel/pennant",
        "documentation_link": "laravel://pennant.md"
    },
    "laravel/folio": {
        "name": "Laravel Folio",
        "description": "Laravel Folio is a page-based router: a Blade template in resources/views/pages becomes a route.",
        "categories": ["routing", "frontend"],
        "use_cases": [
            "File-based routing for Blade pages",
            "Building content-heavy sites without route definitions"
        ],
        "installation": "composer require laravel/folio",
        "documentation_link": "laravel://folio.md"
    },
    "livewire/volt": {
        "name": "Livewire Volt",
        "legacy": True,
        "superseded_by": "livewire/livewire",
        "description": "Volt is a single-file component API for Livewire. Livewire 4 has single-file components built in, using the same syntax as Volt's class-based components, and its upgrade guide covers moving from Volt.",
        "categories": ["frontend", "ui", "reactivity"],
        "use_cases": [
            "Maintaining a Livewire 3 application built with Volt"
        ],
        "installation": "composer require livewire/volt",
        "documentation_link": "laravel-package://livewire/upgrading.md"
    },
    "filament/filament": {
        "name": "Filament",
        "description": "Filament is an open-source framework for building admin panels and other business software with Laravel, from resources, forms, tables, actions and notifications.",
        "categories": ["admin", "dashboard", "ui", "backend"],
        "use_cases": [
            "Building an admin panel over Eloquent models",
            "CRUD interfaces with forms and tables",
            "Internal tools, customer portals and back-office software"
        ],
        "installation": "composer require filament/filament:\"^5.0\"",
        "documentation_link": "laravel-package://filament/introduction-overview.md"
    },
    "laravel/pint": {
        "name": "Laravel Pint",
        "description": "Laravel Pint is an opinionated PHP code style fixer built on PHP CS Fixer.",
        "categories": ["development", "code-style"],
        "use_cases": [
            "Keeping code style consistent across a team",
            "Fixing style in CI or before commit"
        ],
        "installation": "composer require laravel/pint --dev",
        "documentation_link": "laravel://pint.md"
    },
    "laravel/prompts": {
        "name": "Laravel Prompts",
        "description": "Laravel Prompts adds user-friendly forms to command-line applications, with placeholder text and validation.",
        "categories": ["console", "development"],
        "use_cases": [
            "Interactive Artisan commands",
            "Validated input in CLI tools"
        ],
        "installation": "composer require laravel/prompts",
        "documentation_link": "laravel://prompts.md"
    },
    "laravel/ai": {
        "name": "Laravel AI SDK",
        "description": "The Laravel AI SDK provides a unified API for interacting with AI providers such as OpenAI, Anthropic and Gemini, for building agents with tools and structured output.",
        "categories": ["ai", "llm"],
        "use_cases": [
            "Calling a language model from a Laravel application",
            "Building agents with tools and structured output",
            "Switching AI providers without rewriting application code"
        ],
        "installation": "composer require laravel/ai",
        "documentation_link": "laravel://ai-sdk.md"
    },
    "laravel/boost": {
        "name": "Laravel Boost",
        "description": "Laravel Boost accelerates AI-assisted development by providing the guidelines and agent skills that help AI agents write Laravel code that follows Laravel's best practices.",
        "categories": ["ai", "development"],
        "use_cases": [
            "Giving a coding agent Laravel-specific guidelines for one project",
            "AI-assisted development inside an existing application"
        ],
        "installation": "composer require laravel/boost --dev",
        "documentation_link": "laravel://boost.md"
    },
    "laravel/mcp": {
        "name": "Laravel MCP",
        "description": "Laravel MCP lets AI clients interact with a Laravel application through the Model Context Protocol.",
        "categories": ["ai", "api"],
        "use_cases": [
            "Exposing an application's data and actions to AI clients",
            "Building an MCP server in Laravel"
        ],
        "installation": "composer require laravel/mcp",
        "documentation_link": "laravel://mcp.md"
    }
}

# Updated FEATURE_MAP with more implementation details
FEATURE_MAP: Dict[str, List[str]] = {
    "laravel/cashier": ["subscription-setup", "one-time-payments", "webhook-handling", "subscription-swapping", "trial-periods", "invoice-generation"],
    "laravel/sanctum": ["spa-authentication", "api-tokens", "token-abilities", "mobile-auth", "token-revocation"],
    "laravel/scout": ["basic-search", "algolia-driver", "meilisearch-driver", "typesense-driver", "database-engine", "custom-engines", "search-filters", "pagination"],
    "livewire/livewire": ["components", "data-binding", "actions", "validation", "file-uploads", "polling", "events"],
    "laravel/fortify": ["login", "registration", "password-reset", "email-verification", "two-factor-auth", "profile-update"],
    "laravel/passport": ["oauth-server", "password-grant", "client-credentials", "authorization-code", "token-scopes", "personal-tokens"],
    "laravel/breeze": ["blade-views", "react-setup", "vue-setup", "inertia-setup", "api-setup", "dark-mode"],
    "spatie/laravel-permission": ["roles", "permissions", "direct-permissions", "role-hierarchy", "middleware", "blade-directives"],
    "inertiajs/inertia-laravel": ["setup", "routing", "shared-data", "asset-versioning", "ssr", "form-helper"],
    "laravel/horizon": ["configuration", "metrics", "failed-jobs", "job-retries", "tags", "notifications"],
    "laravel/telescope": ["entries", "filtering", "pruning", "authorization", "custom-watchers"],
    "laravel/jetstream": ["profile", "api-tokens", "teams", "team-permissions", "billing-integration"],
    "laravel/octane": ["frankenphp-setup", "roadrunner-setup", "swoole-setup", "state-management", "concurrent-tasks", "cache-optimization"],
    "laravel/socialite": ["provider-setup", "scopes", "optional-parameters", "stateless-auth", "custom-providers"],
    "spatie/laravel-medialibrary": ["conversions", "collections", "s3-upload", "responsive-images", "media-streams"],
    "laravel/excel": ["exports", "imports", "queued-exports", "multiple-sheets", "csv-handling", "styling"],
    "barryvdh/laravel-debugbar": ["query-debugging", "timeline", "exceptions", "views-data", "route-info"],
    "laravel/forge": ["server-provisioning", "site-deployment", "ssl-management", "database-management", "queue-management", "backups", "monitoring"],
    "laravel/vapor": ["serverless-deployment", "environment-management", "database-setup", "queue-configuration", "storage-management", "cli-deployment"],
    "laravel/envoyer": ["deployment-setup", "zero-downtime-deployment", "rollback", "notifications", "heartbeats", "team-management"],
    "laravel/nova": ["resource-management", "custom-fields", "actions", "filters", "lenses", "metrics", "authorization"],
    "laravel/cashier-paddle": ["subscription-setup", "one-time-charges", "webhook-handling", "paddle-checkout", "trial-periods"],
    "laravel/starter-kits": ["react-kit", "svelte-kit", "vue-kit", "livewire-kit", "two-factor-authentication", "teams", "workos-authkit"],
    "laravel/cloud": ["application-deployment", "environments", "compute-scaling", "managed-databases", "managed-queues", "object-storage", "preview-environments"],
    "laravel/nightwatch": ["request-monitoring", "exception-tracking", "query-monitoring", "job-monitoring", "sampling", "alerting"],
    "laravel/herd": ["php-version-management", "site-serving", "herd-pro-services", "debugging-tools"],
    "laravel/sail": ["docker-services", "sail-commands", "database-containers", "sharing-sites"],
    "laravel/homestead": ["vagrant-box", "site-mapping"],
    "laravel/valet": ["site-parking", "site-linking", "secure-sites"],
    "pestphp/pest": ["expectations", "datasets", "hooks", "architecture-tests", "parallel-testing"],
    "laravel/dusk": ["browser-tests", "page-objects", "components", "waiting-for-elements"],
    "laravel/reverb": ["websocket-server", "broadcasting-integration", "scaling", "monitoring"],
    "laravel/pulse": ["dashboard", "recorders", "custom-cards", "sampling"],
    "laravel/pennant": ["defining-features", "checking-features", "scopes", "rich-values"],
    "laravel/folio": ["page-routes", "route-parameters", "model-binding", "middleware"],
    "livewire/volt": ["class-based-components", "functional-components"],
    "filament/filament": ["panels", "resources", "forms", "tables", "actions", "notifications", "widgets"],
    "laravel/pint": ["presets", "rules", "ci-usage"],
    "laravel/prompts": ["text-input", "select", "confirm", "validation", "progress"],
    "laravel/ai": ["agents", "tools", "structured-output", "provider-switching"],
    "laravel/boost": ["guidelines", "agent-skills"],
    "laravel/mcp": ["servers", "tools", "resources", "prompts"]
}

# Updated TOOL_DESCRIPTIONS with new tools


# A legacy package's match counts for this much of a current package's, so
# that asked how to deploy, the catalog leads with what a new project would use.
LEGACY_WEIGHT = 0.5

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
    A legacy package's score is halved, so it ranks below a current package
    that matches as well. Each entry
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
            scores[package_id] = score * (LEGACY_WEIGHT if entry.get("legacy") else 1.0)

    ranked = sorted(scores.items(), key=lambda item: (item[1], not PACKAGE_CATALOG[item[0]].get("legacy", False)), reverse=True)
    return [{**PACKAGE_CATALOG[package_id], "id": package_id, "score": score} for package_id, score in ranked]
