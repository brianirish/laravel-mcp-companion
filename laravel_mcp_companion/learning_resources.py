#!/usr/bin/env python3
"""
Learning Resources Module for Laravel MCP Companion.

This module contains difficulty classifications, semantic categories,
need-to-docs mappings, learning paths, and related package definitions.
"""

from enum import Enum
from typing import Dict, List, Any


class DifficultyLevel(Enum):
    """Difficulty levels for Laravel documentation topics."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


# Map documentation topics to difficulty levels
# Based on typical learning progression and prerequisite knowledge
TOPIC_DIFFICULTY_MAP: Dict[str, DifficultyLevel] = {
    # Beginner - Getting Started
    "installation": DifficultyLevel.BEGINNER,
    "configuration": DifficultyLevel.BEGINNER,
    "structure": DifficultyLevel.BEGINNER,
    "frontend": DifficultyLevel.BEGINNER,
    "starter-kits": DifficultyLevel.BEGINNER,
    "deployment": DifficultyLevel.BEGINNER,

    # Beginner - Architecture Basics
    "lifecycle": DifficultyLevel.BEGINNER,
    "routing": DifficultyLevel.BEGINNER,
    "middleware": DifficultyLevel.BEGINNER,
    "controllers": DifficultyLevel.BEGINNER,
    "requests": DifficultyLevel.BEGINNER,
    "responses": DifficultyLevel.BEGINNER,
    "views": DifficultyLevel.BEGINNER,
    "blade": DifficultyLevel.BEGINNER,
    "vite": DifficultyLevel.BEGINNER,
    "urls": DifficultyLevel.BEGINNER,
    "session": DifficultyLevel.BEGINNER,
    "validation": DifficultyLevel.BEGINNER,
    "errors": DifficultyLevel.BEGINNER,
    "logging": DifficultyLevel.BEGINNER,

    # Intermediate - Database
    "database": DifficultyLevel.INTERMEDIATE,
    "queries": DifficultyLevel.INTERMEDIATE,
    "pagination": DifficultyLevel.INTERMEDIATE,
    "migrations": DifficultyLevel.INTERMEDIATE,
    "seeding": DifficultyLevel.INTERMEDIATE,
    "redis": DifficultyLevel.INTERMEDIATE,
    "eloquent": DifficultyLevel.INTERMEDIATE,
    "eloquent-relationships": DifficultyLevel.INTERMEDIATE,
    "eloquent-collections": DifficultyLevel.INTERMEDIATE,
    "eloquent-mutators": DifficultyLevel.INTERMEDIATE,
    "eloquent-resources": DifficultyLevel.INTERMEDIATE,
    "eloquent-serialization": DifficultyLevel.INTERMEDIATE,
    "eloquent-factories": DifficultyLevel.INTERMEDIATE,

    # Intermediate - Security
    "authentication": DifficultyLevel.INTERMEDIATE,
    "authorization": DifficultyLevel.INTERMEDIATE,
    "verification": DifficultyLevel.INTERMEDIATE,
    "encryption": DifficultyLevel.INTERMEDIATE,
    "hashing": DifficultyLevel.INTERMEDIATE,
    "passwords": DifficultyLevel.INTERMEDIATE,

    # Intermediate - Features
    "artisan": DifficultyLevel.INTERMEDIATE,
    "cache": DifficultyLevel.INTERMEDIATE,
    "collections": DifficultyLevel.INTERMEDIATE,
    "contracts": DifficultyLevel.INTERMEDIATE,
    "events": DifficultyLevel.INTERMEDIATE,
    "filesystem": DifficultyLevel.INTERMEDIATE,
    "helpers": DifficultyLevel.INTERMEDIATE,
    "http-client": DifficultyLevel.INTERMEDIATE,
    "localization": DifficultyLevel.INTERMEDIATE,
    "mail": DifficultyLevel.INTERMEDIATE,
    "notifications": DifficultyLevel.INTERMEDIATE,
    "packages": DifficultyLevel.INTERMEDIATE,
    "processes": DifficultyLevel.INTERMEDIATE,
    "queues": DifficultyLevel.INTERMEDIATE,
    "rate-limiting": DifficultyLevel.INTERMEDIATE,
    "strings": DifficultyLevel.INTERMEDIATE,
    "scheduling": DifficultyLevel.INTERMEDIATE,

    # Intermediate - Testing
    "testing": DifficultyLevel.INTERMEDIATE,
    "http-tests": DifficultyLevel.INTERMEDIATE,
    "console-tests": DifficultyLevel.INTERMEDIATE,
    "database-testing": DifficultyLevel.INTERMEDIATE,
    "mocking": DifficultyLevel.INTERMEDIATE,

    # Advanced - Architecture Deep Dive
    "container": DifficultyLevel.ADVANCED,
    "providers": DifficultyLevel.ADVANCED,
    "facades": DifficultyLevel.ADVANCED,

    # Advanced - Packages
    "billing": DifficultyLevel.ADVANCED,
    "cashier-paddle": DifficultyLevel.ADVANCED,
    "dusk": DifficultyLevel.ADVANCED,
    "envoy": DifficultyLevel.ADVANCED,
    "fortify": DifficultyLevel.ADVANCED,
    "homestead": DifficultyLevel.ADVANCED,
    "horizon": DifficultyLevel.ADVANCED,
    "octane": DifficultyLevel.ADVANCED,
    "passport": DifficultyLevel.ADVANCED,
    "pennant": DifficultyLevel.ADVANCED,
    "pint": DifficultyLevel.INTERMEDIATE,
    "precognition": DifficultyLevel.ADVANCED,
    "prompts": DifficultyLevel.INTERMEDIATE,
    "pulse": DifficultyLevel.ADVANCED,
    "reverb": DifficultyLevel.ADVANCED,
    "sail": DifficultyLevel.INTERMEDIATE,
    "sanctum": DifficultyLevel.INTERMEDIATE,
    "scout": DifficultyLevel.ADVANCED,
    "socialite": DifficultyLevel.INTERMEDIATE,
    "telescope": DifficultyLevel.INTERMEDIATE,
    "valet": DifficultyLevel.BEGINNER,

    # Advanced - Architecture
    "broadcasting": DifficultyLevel.ADVANCED,
    "context": DifficultyLevel.ADVANCED,

    # External Services

    # Pages added to the framework docs since this map was first written
    "releases": DifficultyLevel.BEGINNER,
    "upgrade": DifficultyLevel.INTERMEDIATE,
    "csrf": DifficultyLevel.BEGINNER,
    "head": DifficultyLevel.BEGINNER,
    "folio": DifficultyLevel.INTERMEDIATE,
    "images": DifficultyLevel.INTERMEDIATE,
    "search": DifficultyLevel.INTERMEDIATE,
    "mongodb": DifficultyLevel.INTERMEDIATE,
    "mix": DifficultyLevel.INTERMEDIATE,
    "concurrency": DifficultyLevel.ADVANCED,
    "ai": DifficultyLevel.BEGINNER,
    "boost": DifficultyLevel.BEGINNER,
    "ai-sdk": DifficultyLevel.INTERMEDIATE,
    "mcp": DifficultyLevel.ADVANCED,
}


# Expanded semantic categories (8 -> 15)
EXPANDED_CATEGORIES: Dict[str, List[str]] = {
    # Original 8 categories
    "authentication": [
        "authentication", "sanctum", "passport", "fortify", "passwords", "verification", "socialite"
    ],
    "database": [
        "database", "mongodb", "eloquent", "eloquent-relationships", "eloquent-collections",
        "eloquent-mutators", "eloquent-resources", "eloquent-serialization",
        "eloquent-factories", "migrations", "seeding", "queries", "pagination", "redis"
    ],
    "frontend": [
        "blade", "frontend", "vite", "views", "localization", "validation", "precognition"
    ],
    "api": [
        "sanctum", "passport", "eloquent-resources", "routing", "rate-limiting",
        "http-client", "responses"
    ],
    "testing": [
        "testing", "dusk", "http-tests", "console-tests", "database-testing",
        "mocking"
    ],
    "deployment": [
        "deployment", "octane", "sail", "homestead", "valet",
        "envoy"
    ],
    "packages": [
        "packages", "cashier", "scout", "socialite", "telescope", "horizon",
        "passport", "sanctum", "fortify", "pennant",
        "pulse", "pint", "prompts", "reverb"
    ],
    "security": [
        "authentication", "authorization", "encryption", "hashing", "passwords",
        "csrf", "sanctum", "passport", "verification", "rate-limiting"
    ],

    # New 7 categories
    "performance": [
        "cache", "queues", "octane", "horizon", "redis", "database",
        "eloquent", "rate-limiting", "pulse"
    ],
    "development": [
        "artisan", "telescope", "logging", "errors",
        "pint", "sail", "valet", "homestead", "prompts"
    ],
    "realtime": [
        "broadcasting", "reverb", "events", "notifications", "queues"
    ],
    "payments": [
        "billing", "cashier-paddle"
    ],
    "search": [
        "search", "scout", "database", "queries", "eloquent", "collections"
    ],
    "files": [
        "filesystem", "images", "responses", "requests", "validation"
    ],
    "jobs": [
        "queues", "horizon", "scheduling", "events", "notifications"
    ],
    "basics": [
        "installation", "configuration", "structure", "starter-kits", "routing", "controllers",
        "middleware", "requests", "responses", "views", "session", "urls", "csrf", "errors",
        "logging", "helpers", "strings", "collections", "upgrade", "releases"
    ],
    "architecture": [
        "lifecycle", "container", "providers", "facades", "contracts", "context", "concurrency",
        "processes", "packages"
    ],
    "ai": [
        "ai", "boost", "mcp"
    ],
    "communication": [
        "mail", "notifications", "broadcasting"
    ],
    "frontend-tooling": [
        "vite", "mix", "folio", "head", "precognition", "starter-kits"
    ],
}


# "I need X" -> documentation mappings
# Maps common user needs to relevant documentation files
NEED_MAPPINGS: Dict[str, List[str]] = {
    # File handling
    "upload files": ["filesystem", "validation", "requests"],
    "handle uploads": ["filesystem", "validation", "requests"],
    "store files": ["filesystem"],
    "download files": ["filesystem", "responses"],
    "serve files": ["filesystem", "responses"],
    "manage media": ["filesystem"],
    "image upload": ["filesystem", "validation"],

    # Email & Notifications
    "send emails": ["mail", "notifications", "queues"],
    "send mail": ["mail", "notifications", "queues"],
    "email templates": ["mail", "blade"],
    "notifications": ["notifications", "mail", "broadcasting"],
    "push notifications": ["notifications", "broadcasting"],
    "sms notifications": ["notifications"],

    # Payments & Billing
    "accept payments": ["billing", "cashier-paddle"],
    "payment processing": ["billing", "cashier-paddle"],
    "subscriptions": ["billing", "cashier-paddle"],
    "stripe integration": ["billing"],
    "paddle integration": ["cashier-paddle", "billing"],
    "invoices": ["billing", "cashier-paddle"],

    # Admin & CMS

    # Search
    "add search": ["scout"],
    "full-text search": ["scout", "database"],
    "search functionality": ["scout"],
    "algolia": ["scout"],
    "meilisearch": ["scout"],
    "typesense": ["scout"],
    "elasticsearch": ["scout"],

    # Authentication
    "authenticate": ["authentication", "sanctum", "fortify"],
    "login": ["authentication", "sanctum", "fortify", "starter-kits"],
    "register users": ["authentication", "fortify", "starter-kits"],
    "user registration": ["authentication", "fortify", "starter-kits"],
    "password reset": ["passwords", "authentication", "fortify"],
    "social login": ["socialite", "authentication"],
    "oauth": ["socialite", "passport"],
    "api authentication": ["sanctum", "passport"],
    "spa authentication": ["sanctum", "authentication"],
    "token authentication": ["sanctum", "passport"],
    "two-factor auth": ["fortify"],
    "2fa": ["fortify"],

    # Authorization
    "permissions": ["authorization"],
    "roles": ["authorization"],
    "access control": ["authorization", "middleware"],
    "policies": ["authorization"],
    "gates": ["authorization"],

    # API Development
    "build api": ["routing", "controllers", "eloquent-resources", "sanctum"],
    "rest api": ["routing", "controllers", "eloquent-resources"],
    "api resources": ["eloquent-resources"],
    "api versioning": ["routing"],
    "api rate limiting": ["rate-limiting"],

    # Background Processing
    "background jobs": ["queues", "horizon"],
    "async processing": ["queues", "horizon"],
    "queue workers": ["queues", "horizon"],
    "scheduled tasks": ["scheduling"],
    "cron jobs": ["scheduling"],
    "task scheduling": ["scheduling"],
    "job batching": ["queues"],

    # Real-time
    "websockets": ["broadcasting", "reverb"],
    "real-time": ["broadcasting", "reverb"],
    "live updates": ["broadcasting", "reverb"],
    "chat": ["broadcasting", "reverb"],
    "push events": ["broadcasting", "reverb"],

    # Database
    "database queries": ["queries", "eloquent", "database"],
    "orm": ["eloquent"],
    "models": ["eloquent"],
    "relationships": ["eloquent-relationships"],
    "migrations": ["migrations"],
    "seeds": ["seeding"],
    "factories": ["eloquent-factories"],

    # Caching
    "caching": ["cache", "redis"],
    "redis": ["redis", "cache"],
    "memcached": ["cache"],
    "performance": ["cache", "queues", "octane"],

    # Testing
    "write tests": ["testing", "http-tests", "database-testing"],
    "unit tests": ["testing", "mocking"],
    "feature tests": ["http-tests", "testing"],
    "browser tests": ["dusk"],
    "test database": ["database-testing"],
    "mock services": ["mocking"],

    # Deployment
    "deploy": ["deployment"],
    "hosting": ["deployment"],
    "server setup": ["deployment"],
    "serverless": ["deployment"],
    "ci/cd": ["deployment", "envoy"],
    "zero downtime": ["deployment", "envoy"],

    # Development Tools
    "debugging": ["telescope", "logging", "errors"],
    "logging": ["logging"],
    "error handling": ["errors", "logging"],
    "code style": ["pint"],
    "linting": ["pint"],

    # Frontend
    "forms": ["validation", "blade", "requests"],
    "form validation": ["validation"],
    "templates": ["blade", "views"],
    "components": ["blade"],
    "assets": ["vite", "frontend"],
    "css/js": ["vite", "frontend"],

    # Starter Kits
    "starter kit": ["starter-kits"],
    "scaffolding": ["starter-kits"],
    "boilerplate": ["starter-kits"],

    # Miscellaneous
    "feature flags": ["pennant"],
    "localization": ["localization"],
    "translation": ["localization"],
    "multi-language": ["localization"],
    "encryption": ["encryption", "hashing"],
    "security": ["encryption", "hashing", "authentication", "authorization"],

    # Pages the table did not reach before the 2026 audit
    "ai agents": ["ai-sdk", "ai"],
    "call an llm": ["ai-sdk"],
    "ai assisted development": ["ai", "boost"],
    "coding agent": ["boost", "ai"],
    "mcp server": ["mcp"],
    "artisan commands": ["artisan", "prompts"],
    "console commands": ["artisan", "prompts", "console-tests"],
    "collections": ["collections"],
    "run tasks concurrently": ["concurrency", "processes"],
    "run shell commands": ["processes"],
    "dependency injection": ["container", "providers", "contracts"],
    "service container": ["container", "providers"],
    "service providers": ["providers", "container"],
    "facades": ["facades", "contracts"],
    "request lifecycle": ["lifecycle"],
    "share context": ["context"],
    "csrf": ["csrf"],
    "deployment scripts": ["envoy"],
    "page based routing": ["folio"],
    "meta tags": ["head"],
    "seo": ["head"],
    "helper functions": ["helpers", "strings"],
    "string manipulation": ["strings", "helpers"],
    "local development": ["sail", "valet", "homestead"],
    "docker": ["sail"],
    "resize images": ["images"],
    "image manipulation": ["images", "filesystem"],
    "mongodb": ["mongodb"],
    "nosql": ["mongodb"],
    "build a package": ["packages"],
    "package development": ["packages"],
    "pagination": ["pagination"],
    "live validation": ["precognition", "validation"],
    "monitor performance": ["pulse", "telescope"],
    "semantic search": ["search", "scout"],
    "sessions": ["session"],
    "project structure": ["structure"],
    "directory structure": ["structure"],
    "upgrade laravel": ["upgrade", "releases"],
    "generate urls": ["urls"],
    "asset bundling": ["vite", "mix"],
}


# Curated learning paths for different goals
LEARNING_PATHS: Dict[str, Dict[str, Any]] = {
    "getting-started": {
        "name": "Getting Started with Laravel",
        "description": "Learn the fundamentals of Laravel framework",
        "difficulty": DifficultyLevel.BEGINNER,
        "estimated_hours": 4,
        "docs": [
            "installation",
            "configuration",
            "structure",
            "routing",
            "controllers",
            "views",
            "blade",
        ],
        "next_path": "crud-basics",
    },
    "crud-basics": {
        "name": "Building CRUD Applications",
        "description": "Learn to build complete CRUD (Create, Read, Update, Delete) applications",
        "difficulty": DifficultyLevel.BEGINNER,
        "estimated_hours": 6,
        "docs": [
            "database",
            "migrations",
            "eloquent",
            "eloquent-relationships",
            "controllers",
            "validation",
            "blade",
        ],
        "prerequisites": ["getting-started"],
        "next_path": "authentication-basics",
    },
    "authentication-basics": {
        "name": "Adding Authentication",
        "description": "Implement user authentication in your Laravel application",
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "estimated_hours": 3,
        "docs": [
            "authentication",
            "passwords",
            "verification",
            "middleware",
        ],
        "prerequisites": ["crud-basics"],
        "packages": ["laravel/starter-kits", "laravel/fortify"],
        "next_path": "api-development",
    },
    "api-development": {
        "name": "Building APIs",
        "description": "Create RESTful APIs with Laravel",
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "estimated_hours": 5,
        "docs": [
            "routing",
            "controllers",
            "eloquent-resources",
            "sanctum",
            "validation",
            "rate-limiting",
        ],
        "prerequisites": ["crud-basics"],
        "packages": ["laravel/sanctum"],
        "next_path": "testing-fundamentals",
    },
    "testing-fundamentals": {
        "name": "Testing Your Application",
        "description": "Write tests for your Laravel application, with Pest or PHPUnit",
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "estimated_hours": 4,
        "docs": [
            "testing",
            "http-tests",
            "database-testing",
            "mocking",
        ],
        "prerequisites": ["crud-basics"],
        "next_path": "advanced-eloquent",
    },
    "advanced-eloquent": {
        "name": "Mastering Eloquent ORM",
        "description": "Deep dive into Eloquent's advanced features",
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "estimated_hours": 6,
        "docs": [
            "eloquent",
            "eloquent-relationships",
            "eloquent-collections",
            "eloquent-mutators",
            "eloquent-serialization",
            "eloquent-factories",
        ],
        "prerequisites": ["crud-basics"],
        "next_path": "background-processing",
    },
    "background-processing": {
        "name": "Background Jobs & Queues",
        "description": "Handle long-running tasks with queues and scheduled jobs",
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "estimated_hours": 4,
        "docs": [
            "queues",
            "scheduling",
            "events",
            "notifications",
        ],
        "prerequisites": ["crud-basics"],
        "packages": ["laravel/horizon"],
        "next_path": "production-ready",
    },
    "real-time-features": {
        "name": "Real-time Features",
        "description": "Add WebSocket-based real-time functionality",
        "difficulty": DifficultyLevel.ADVANCED,
        "estimated_hours": 5,
        "docs": [
            "broadcasting",
            "reverb",
            "events",
            "notifications",
        ],
        "prerequisites": ["background-processing"],
        "packages": ["laravel/reverb"],
    },
    "production-ready": {
        "name": "Production Deployment",
        "description": "Deploy and scale your Laravel application, on Laravel Cloud or on servers you manage",
        "difficulty": DifficultyLevel.ADVANCED,
        "estimated_hours": 5,
        "docs": [
            "deployment",
            "octane",
            "queues",
            "cache",
            "logging",
        ],
        "prerequisites": ["testing-fundamentals", "background-processing"],
        "services": ["cloud", "forge"],
        "packages": ["laravel/octane"],
    },
    "full-stack-spa": {
        "name": "Full-Stack SPA Development",
        "description": "Build single-page applications with Laravel backend",
        "difficulty": DifficultyLevel.ADVANCED,
        "estimated_hours": 8,
        "docs": [
            "sanctum",
            "eloquent-resources",
            "validation",
            "http-client",
        ],
        "prerequisites": ["api-development", "authentication-basics"],
        "packages": ["inertiajs/inertia-laravel", "livewire/livewire"],
    },
}


# Related packages - packages commonly used together
RELATED_PACKAGES: Dict[str, List[str]] = {
    # Authentication ecosystem
    "laravel/sanctum": ["laravel/starter-kits", "laravel/fortify", "laravel/passport"],
    "laravel/passport": ["laravel/socialite"],
    "laravel/fortify": ["laravel/starter-kits", "laravel/sanctum"],
    "laravel/breeze": ["laravel/starter-kits", "laravel/sanctum", "laravel/fortify"],
    "laravel/jetstream": ["laravel/starter-kits", "laravel/sanctum", "laravel/fortify"],
    "laravel/socialite": ["laravel/passport", "laravel/sanctum"],

    # Payment processing
    "laravel/cashier": ["laravel/cashier-paddle"],
    "laravel/cashier-paddle": ["laravel/cashier"],

    # Queue management
    "laravel/horizon": ["laravel/telescope"],

    # Search
    "laravel/scout": [],

    # Development tools
    "laravel/telescope": ["laravel/pulse", "laravel/nightwatch", "laravel/horizon", "barryvdh/laravel-debugbar"],
    "barryvdh/laravel-debugbar": ["laravel/telescope"],

    # Frontend frameworks
    "livewire/livewire": ["laravel/starter-kits", "filament/filament", "livewire/volt"],
    "inertiajs/inertia-laravel": ["laravel/starter-kits"],

    # Admin panels
    "laravel/nova": ["filament/filament", "spatie/laravel-permission"],

    # Spatie packages (commonly used together)
    "spatie/laravel-permission": ["laravel/nova", "spatie/laravel-medialibrary"],
    "spatie/laravel-medialibrary": ["spatie/laravel-permission"],

    # Performance
    "laravel/octane": ["laravel/cloud", "laravel/horizon"],

    # Deployment
    "laravel/forge": ["laravel/cloud", "laravel/envoyer"],
    "laravel/vapor": ["laravel/cloud"],
    "laravel/envoyer": ["laravel/forge"],

    # Added with the 2026 catalog refresh
    "laravel/excel": [],
    "laravel/starter-kits": ["laravel/fortify", "laravel/sanctum", "livewire/livewire", "inertiajs/inertia-laravel"],
    "laravel/cloud": ["laravel/forge", "laravel/nightwatch", "laravel/octane"],
    "laravel/nightwatch": ["laravel/cloud", "laravel/pulse", "laravel/telescope"],
    "laravel/herd": ["laravel/sail"],
    "laravel/sail": ["laravel/herd"],
    "laravel/homestead": ["laravel/sail"],
    "laravel/valet": ["laravel/herd"],
    "pestphp/pest": ["laravel/dusk"],
    "laravel/dusk": ["pestphp/pest"],
    "laravel/reverb": ["laravel/pulse"],
    "laravel/pulse": ["laravel/nightwatch", "laravel/telescope", "laravel/horizon"],
    "laravel/pennant": [],
    "laravel/folio": [],
    "livewire/volt": ["livewire/livewire"],
    "filament/filament": ["livewire/livewire"],
    "laravel/pint": [],
    "laravel/prompts": [],
    "laravel/ai": ["laravel/mcp", "laravel/boost"],
    "laravel/boost": ["laravel/ai", "laravel/mcp"],
    "laravel/mcp": ["laravel/ai", "laravel/boost"],
}


def keyword_selects(keyword: str, page: str) -> bool:
    """Whether a category keyword selects a page, by the page's name without
    ".md": the page of that name, or one whose name extends it with a hyphen.
    "eloquent" selects eloquent and eloquent-relationships; "ai" selects ai
    and ai-sdk and does not select mail."""
    return page == keyword or page.startswith(f"{keyword}-")


def categories_of(page: str) -> List[str]:
    """Every category a page belongs to, sorted."""
    return sorted(
        category for category, keywords in EXPANDED_CATEGORIES.items()
        if any(keyword_selects(keyword, page) for keyword in keywords)
    )


def get_difficulty_for_topic(topic: str) -> DifficultyLevel:
    """Get the difficulty level for a documentation topic.

    Args:
        topic: The topic name (e.g., "eloquent", "routing")

    Returns:
        DifficultyLevel enum value, defaults to INTERMEDIATE if not found
    """
    # Normalize the topic name
    normalized = topic.lower().replace(".md", "").replace("-", "-")
    return TOPIC_DIFFICULTY_MAP.get(normalized, DifficultyLevel.INTERMEDIATE)
