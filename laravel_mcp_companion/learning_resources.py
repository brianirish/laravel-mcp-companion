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
    "directory-structure": DifficultyLevel.BEGINNER,
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
    "url": DifficultyLevel.BEGINNER,
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
    "browser-tests": DifficultyLevel.INTERMEDIATE,
    "database-testing": DifficultyLevel.INTERMEDIATE,
    "mocking": DifficultyLevel.INTERMEDIATE,

    # Advanced - Architecture Deep Dive
    "container": DifficultyLevel.ADVANCED,
    "providers": DifficultyLevel.ADVANCED,
    "facades": DifficultyLevel.ADVANCED,

    # Advanced - Packages
    "billing": DifficultyLevel.ADVANCED,
    "cashier-stripe": DifficultyLevel.ADVANCED,
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
    "spark-billing": DifficultyLevel.ADVANCED,
    "telescope": DifficultyLevel.INTERMEDIATE,
    "valet": DifficultyLevel.BEGINNER,

    # Advanced - Architecture
    "broadcasting": DifficultyLevel.ADVANCED,
    "context": DifficultyLevel.ADVANCED,

    # External Services
    "forge": DifficultyLevel.INTERMEDIATE,
    "vapor": DifficultyLevel.ADVANCED,
    "envoyer": DifficultyLevel.INTERMEDIATE,
    "nova": DifficultyLevel.ADVANCED,
}


# Expanded semantic categories (8 -> 15)
EXPANDED_CATEGORIES: Dict[str, List[str]] = {
    # Original 8 categories
    "authentication": [
        "authentication", "sanctum", "passport", "fortify", "breeze",
        "jetstream", "passwords", "verification", "socialite"
    ],
    "database": [
        "database", "eloquent", "eloquent-relationships", "eloquent-collections",
        "eloquent-mutators", "eloquent-resources", "eloquent-serialization",
        "eloquent-factories", "migrations", "seeding", "queries", "pagination", "redis"
    ],
    "frontend": [
        "blade", "frontend", "vite", "views", "localization", "validation",
        "livewire", "inertia", "precognition"
    ],
    "api": [
        "sanctum", "passport", "eloquent-resources", "routing", "rate-limiting",
        "http-client", "responses"
    ],
    "testing": [
        "testing", "dusk", "http-tests", "console-tests", "database-testing",
        "mocking", "browser-tests"
    ],
    "deployment": [
        "deployment", "octane", "sail", "homestead", "valet", "forge", "vapor",
        "envoy", "envoyer"
    ],
    "packages": [
        "packages", "cashier", "scout", "socialite", "telescope", "horizon",
        "passport", "sanctum", "fortify", "breeze", "jetstream", "pennant",
        "pulse", "pint", "prompts", "reverb", "spark-billing"
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
        "artisan", "telescope", "logging", "errors", "debugging",
        "pint", "sail", "valet", "homestead", "prompts"
    ],
    "realtime": [
        "broadcasting", "reverb", "events", "notifications", "queues"
    ],
    "payments": [
        "billing", "cashier-stripe", "cashier-paddle", "spark-billing"
    ],
    "search": [
        "scout", "database", "queries", "eloquent", "collections"
    ],
    "files": [
        "filesystem", "responses", "requests", "validation"
    ],
    "jobs": [
        "queues", "horizon", "scheduling", "events", "notifications"
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
    "accept payments": ["billing", "cashier-stripe", "cashier-paddle"],
    "payment processing": ["billing", "cashier-stripe", "cashier-paddle"],
    "subscriptions": ["billing", "cashier-stripe", "cashier-paddle"],
    "stripe integration": ["cashier-stripe", "billing"],
    "paddle integration": ["cashier-paddle", "billing"],
    "invoices": ["billing", "cashier-stripe", "cashier-paddle"],

    # Admin & CMS
    "build admin": ["nova"],
    "admin panel": ["nova"],
    "admin dashboard": ["nova"],
    "cms": ["nova"],
    "content management": ["nova"],

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
    "login": ["authentication", "sanctum", "fortify", "breeze"],
    "register users": ["authentication", "fortify", "breeze"],
    "user registration": ["authentication", "fortify", "breeze"],
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
    "browser tests": ["dusk", "browser-tests"],
    "test database": ["database-testing"],
    "mock services": ["mocking"],

    # Deployment
    "deploy": ["deployment", "forge", "vapor", "envoyer"],
    "hosting": ["deployment", "forge", "vapor"],
    "server setup": ["deployment", "forge"],
    "serverless": ["vapor", "deployment"],
    "ci/cd": ["deployment", "envoyer"],
    "zero downtime": ["envoyer", "deployment"],

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
    "starter kit": ["starter-kits", "breeze", "jetstream"],
    "scaffolding": ["starter-kits", "breeze", "jetstream"],
    "boilerplate": ["starter-kits", "breeze", "jetstream"],

    # Miscellaneous
    "feature flags": ["pennant"],
    "localization": ["localization"],
    "translation": ["localization"],
    "multi-language": ["localization"],
    "encryption": ["encryption", "hashing"],
    "security": ["encryption", "hashing", "authentication", "authorization"],
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
            "directory-structure",
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
        "packages": ["laravel/breeze", "laravel/fortify"],
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
        "description": "Write comprehensive tests for your Laravel application",
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
        "description": "Deploy and scale your Laravel application",
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
        "external_docs": ["forge", "vapor"],
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
        "community_packages": ["inertia", "livewire"],
    },
}


# Related packages - packages commonly used together
RELATED_PACKAGES: Dict[str, List[str]] = {
    # Authentication ecosystem
    "laravel/sanctum": ["laravel/breeze", "laravel/jetstream", "laravel/fortify"],
    "laravel/passport": ["laravel/socialite"],
    "laravel/fortify": ["laravel/breeze", "laravel/jetstream", "laravel/sanctum"],
    "laravel/breeze": ["laravel/sanctum", "laravel/fortify", "livewire/livewire", "inertiajs/inertia-laravel"],
    "laravel/jetstream": ["laravel/sanctum", "laravel/fortify", "livewire/livewire", "inertiajs/inertia-laravel"],
    "laravel/socialite": ["laravel/passport", "laravel/sanctum"],

    # Payment processing
    "laravel/cashier": ["laravel/cashier-paddle"],
    "laravel/cashier-paddle": ["laravel/cashier"],

    # Queue management
    "laravel/horizon": ["laravel/telescope"],

    # Search
    "laravel/scout": [],

    # Development tools
    "laravel/telescope": ["laravel/horizon", "barryvdh/laravel-debugbar"],
    "barryvdh/laravel-debugbar": ["laravel/telescope"],

    # Frontend frameworks
    "livewire/livewire": ["laravel/breeze", "laravel/jetstream"],
    "inertiajs/inertia-laravel": ["laravel/breeze", "laravel/jetstream"],

    # Admin panels
    "laravel/nova": ["spatie/laravel-permission"],

    # Spatie packages (commonly used together)
    "spatie/laravel-permission": ["laravel/nova", "spatie/laravel-medialibrary"],
    "spatie/laravel-medialibrary": ["spatie/laravel-permission"],

    # Performance
    "laravel/octane": ["laravel/horizon"],

    # Deployment
    "laravel/forge": ["laravel/envoyer"],
    "laravel/vapor": [],
    "laravel/envoyer": ["laravel/forge"],
}


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


def get_topics_by_difficulty(difficulty: DifficultyLevel) -> List[str]:
    """Get all topics at a specific difficulty level.

    Args:
        difficulty: The difficulty level to filter by

    Returns:
        List of topic names at that difficulty level
    """
    return [topic for topic, level in TOPIC_DIFFICULTY_MAP.items() if level == difficulty]


def get_docs_for_need(need: str) -> List[str]:
    """Get documentation files for a specific user need.

    Args:
        need: User need description (e.g., "upload files", "send emails")

    Returns:
        List of relevant documentation file names
    """
    need_lower = need.lower().strip()

    # Exact match
    if need_lower in NEED_MAPPINGS:
        return NEED_MAPPINGS[need_lower]

    # Partial match - find needs that contain the query
    matches = []
    for key, docs in NEED_MAPPINGS.items():
        if need_lower in key or key in need_lower:
            matches.extend(docs)

    # Remove duplicates while preserving order
    seen = set()
    unique_matches = []
    for doc in matches:
        if doc not in seen:
            seen.add(doc)
            unique_matches.append(doc)

    return unique_matches


def get_related_packages(package: str) -> List[str]:
    """Get packages related to the given package.

    Args:
        package: Package identifier (e.g., "laravel/sanctum")

    Returns:
        List of related package identifiers
    """
    return RELATED_PACKAGES.get(package, [])


def get_learning_path(path_name: str) -> Dict[str, Any]:
    """Get a specific learning path.

    Args:
        path_name: The learning path identifier

    Returns:
        Learning path dictionary or empty dict if not found
    """
    return LEARNING_PATHS.get(path_name, {})


def list_learning_paths() -> List[Dict[str, Any]]:
    """List all available learning paths with summary info.

    Returns:
        List of learning path summaries
    """
    paths = []
    for path_id, path_data in LEARNING_PATHS.items():
        paths.append({
            "id": path_id,
            "name": path_data["name"],
            "description": path_data["description"],
            "difficulty": path_data["difficulty"].value,
            "estimated_hours": path_data.get("estimated_hours", 0),
            "doc_count": len(path_data.get("docs", [])),
        })
    return paths


def get_category_docs(category: str) -> List[str]:
    """Get documentation files for a category.

    Args:
        category: Category name

    Returns:
        List of documentation file names in that category
    """
    return EXPANDED_CATEGORIES.get(category.lower(), [])


def list_categories() -> List[str]:
    """List all available categories.

    Returns:
        Sorted list of category names
    """
    return sorted(EXPANDED_CATEGORIES.keys())
