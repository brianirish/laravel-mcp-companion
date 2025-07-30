#!/usr/bin/env python3
"""
Navigation Engine for Laravel Learning Resources.

This module provides intelligent navigation and mapping between use cases,
documentation, and package combinations.
"""

import logging
import re
from typing import Dict, List, Optional, Tuple, Set
from pathlib import Path
from dataclasses import dataclass
import json

from learning_resources import (
    LearningResourceFetcher,
    ResourceType,
    DifficultyLevel,
    ResourceMetadata
)

logger = logging.getLogger("laravel-navigation-engine")


# Use case patterns for mapping user needs to resources
USE_CASE_PATTERNS = {
    "authentication": {
        "keywords": ["auth", "login", "register", "password", "session", "guard"],
        "packages": ["sanctum", "fortify", "breeze", "jetstream", "socialite"],
        "docs": ["authentication", "authorization", "passwords", "sanctum"],
        "difficulty": DifficultyLevel.BEGINNER
    },
    "api_development": {
        "keywords": ["api", "rest", "restful", "json", "endpoint", "resource"],
        "packages": ["sanctum", "passport", "scout", "dingo/api"],
        "docs": ["routing", "controllers", "eloquent-resources", "sanctum"],
        "difficulty": DifficultyLevel.INTERMEDIATE
    },
    "payment_processing": {
        "keywords": ["payment", "subscription", "billing", "stripe", "paypal"],
        "packages": ["cashier", "cashier-paddle", "laravel-stripe"],
        "docs": ["billing", "cashier", "queues"],
        "difficulty": DifficultyLevel.INTERMEDIATE
    },
    "file_uploads": {
        "keywords": ["upload", "file", "image", "media", "storage", "s3"],
        "packages": ["medialibrary", "filepond", "laravel-filemanager"],
        "docs": ["filesystem", "validation", "requests"],
        "difficulty": DifficultyLevel.BEGINNER
    },
    "search": {
        "keywords": ["search", "full-text", "elasticsearch", "algolia", "index"],
        "packages": ["scout", "tntsearch", "elasticsearch"],
        "docs": ["scout", "eloquent", "database"],
        "difficulty": DifficultyLevel.INTERMEDIATE
    },
    "testing": {
        "keywords": ["test", "unit", "feature", "pest", "phpunit", "mock"],
        "packages": ["pest", "laravel-test-tools", "mockery"],
        "docs": ["testing", "database-testing", "mocking"],
        "difficulty": DifficultyLevel.INTERMEDIATE
    },
    "frontend": {
        "keywords": ["frontend", "vue", "react", "blade", "javascript", "spa"],
        "packages": ["livewire", "inertia", "breeze", "jetstream"],
        "docs": ["blade", "frontend", "vite", "mix"],
        "difficulty": DifficultyLevel.BEGINNER
    },
    "admin_panel": {
        "keywords": ["admin", "dashboard", "crud", "panel", "backend"],
        "packages": ["filament", "nova", "orchid", "backpack"],
        "docs": ["routing", "middleware", "authorization"],
        "difficulty": DifficultyLevel.INTERMEDIATE
    },
    "performance": {
        "keywords": ["performance", "optimization", "cache", "speed", "scale"],
        "packages": ["horizon", "telescope", "debugbar", "clockwork"],
        "docs": ["cache", "queues", "database", "telescope"],
        "difficulty": DifficultyLevel.ADVANCED
    },
    "deployment": {
        "keywords": ["deploy", "production", "server", "hosting", "docker"],
        "packages": ["envoy", "forge", "vapor", "sail"],
        "docs": ["deployment", "configuration", "artisan"],
        "difficulty": DifficultyLevel.INTERMEDIATE
    }
}


# Common package combinations with compatibility notes
PACKAGE_COMBINATIONS = {
    ("livewire", "alpine"): {
        "use_case": "Building reactive UI components",
        "compatibility": "Excellent - Alpine.js is included with Livewire",
        "guide": """
## Livewire + Alpine.js Integration

Livewire includes Alpine.js by default, making them a perfect combination for building reactive UIs.

### Installation
```bash
composer require livewire/livewire
```

Alpine.js is automatically included when you add Livewire scripts:
```blade
@livewireStyles
@livewireScripts
```

### Usage Example
```blade
<div x-data="{ open: false }">
    <button @click="open = !open">Toggle</button>
    <div x-show="open" x-transition>
        @livewire('user-profile')
    </div>
</div>
```

### Best Practices
- Use Alpine for client-side state
- Use Livewire for server-side state
- Combine both for optimal user experience
"""
    },
    ("inertia", "vue"): {
        "use_case": "Building modern SPAs with Vue.js",
        "compatibility": "Excellent - Official Inertia.js adapter",
        "guide": """
## Inertia.js + Vue 3 Integration

Build modern single-page applications using classic server-side routing.

### Installation
```bash
composer require inertiajs/inertia-laravel
npm install @inertiajs/vue3
```

### Setup
1. Configure your app.js:
```javascript
import { createApp, h } from 'vue'
import { createInertiaApp } from '@inertiajs/vue3'

createInertiaApp({
    resolve: name => {
        const pages = import.meta.glob('./Pages/**/*.vue', { eager: true })
        return pages[`./Pages/${name}.vue`]
    },
    setup({ el, App, props, plugin }) {
        createApp({ render: () => h(App, props) })
            .use(plugin)
            .mount(el)
    },
})
```

### Controller Example
```php
use Inertia\\Inertia;

return Inertia::render('Users/Index', [
    'users' => User::paginate()
]);
```
"""
    },
    ("sanctum", "spa"): {
        "use_case": "Authenticating SPAs and mobile apps",
        "compatibility": "Excellent - Designed for SPA authentication",
        "guide": """
## Sanctum for SPA Authentication

Laravel Sanctum provides a simple authentication system for SPAs.

### Installation
```bash
composer require laravel/sanctum
php artisan vendor:publish --provider="Laravel\\Sanctum\\SanctumServiceProvider"
php artisan migrate
```

### Frontend Setup (Axios)
```javascript
axios.defaults.withCredentials = true;

// First, get CSRF cookie
await axios.get('/sanctum/csrf-cookie');

// Then login
await axios.post('/login', credentials);
```

### CORS Configuration
Configure cors.php for your SPA domain:
```php
'paths' => ['api/*', 'sanctum/csrf-cookie'],
'allowed_origins' => ['http://localhost:3000'],
'supports_credentials' => true,
```
"""
    },
    ("filament", "shield"): {
        "use_case": "Admin panel with role-based permissions",
        "compatibility": "Excellent - Official Filament plugin",
        "guide": """
## Filament + Shield (Spatie Permissions)

Add role-based access control to your Filament admin panel.

### Installation
```bash
composer require bezhansalleh/filament-shield
php artisan shield:install
```

### Creating Roles
```bash
php artisan shield:generate
```

### Usage in Resources
```php
protected static ?string $permissionGroup = 'User Management';

public static function canViewAny(): bool
{
    return auth()->user()->can('view_any_user');
}
```
"""
    }
}


@dataclass
class NavigationResult:
    """Result from navigation engine."""
    use_case: str
    matching_docs: List[str]
    recommended_packages: List[str]
    learning_resources: List[ResourceMetadata]
    difficulty_level: DifficultyLevel
    learning_path: Optional[List[Dict[str, str]]] = None


class NavigationMapper:
    """Maps use cases to relevant documentation and resources."""
    
    def __init__(self, resource_fetcher: LearningResourceFetcher):
        """Initialize with resource fetcher."""
        self.fetcher = resource_fetcher
        logger.info("Initialized NavigationMapper")
    
    def find_resources_for_use_case(
        self,
        use_case: str,
        user_level: Optional[DifficultyLevel] = None
    ) -> NavigationResult:
        """Find all relevant resources for a given use case."""
        use_case_lower = use_case.lower()
        
        # Find matching use case pattern
        matched_pattern = self._match_use_case_pattern(use_case_lower)
        
        if matched_pattern:
            pattern_info = USE_CASE_PATTERNS[matched_pattern]
            
            # Get recommended packages
            packages = pattern_info["packages"]
            
            # Get relevant documentation sections
            docs = pattern_info["docs"]
            
            # Get difficulty level
            difficulty = user_level or pattern_info["difficulty"]
            
            # Search for learning resources
            resources = self._search_learning_resources(
                use_case_lower,
                matched_pattern,
                difficulty
            )
            
            # Generate learning path if requested
            learning_path = self._generate_learning_path(
                matched_pattern,
                difficulty,
                resources
            )
            
            return NavigationResult(
                use_case=matched_pattern,
                matching_docs=docs,
                recommended_packages=packages,
                learning_resources=resources,
                difficulty_level=difficulty,
                learning_path=learning_path
            )
        else:
            # Fallback: search by keywords
            resources = self.fetcher.search(query=use_case, limit=20)
            
            return NavigationResult(
                use_case=use_case,
                matching_docs=[],
                recommended_packages=[],
                learning_resources=resources,
                difficulty_level=user_level or DifficultyLevel.INTERMEDIATE,
                learning_path=None
            )
    
    def _match_use_case_pattern(self, query: str) -> Optional[str]:
        """Match query to known use case patterns."""
        best_match = None
        best_score = 0
        
        for use_case, pattern in USE_CASE_PATTERNS.items():
            score = 0
            
            # Check for keyword matches
            for keyword in pattern["keywords"]:
                if keyword in query:
                    score += 1
            
            # Check for package mentions
            for package in pattern["packages"]:
                if package in query:
                    score += 2  # Package names are more specific
            
            if score > best_score:
                best_score = score
                best_match = use_case
        
        return best_match if best_score > 0 else None
    
    def _search_learning_resources(
        self,
        query: str,
        use_case: str,
        difficulty: DifficultyLevel
    ) -> List[ResourceMetadata]:
        """Search for learning resources matching the use case."""
        # First, check for direct use case mappings
        mapped_resources = self.fetcher.get_by_use_case(use_case, limit=10)
        
        # Then search by query
        searched_resources = self.fetcher.search(
            query=query,
            difficulty=difficulty.value,
            limit=10
        )
        
        # Combine and deduplicate
        all_resources = {}
        
        # Add mapped resources with higher priority
        for resource, relevance in mapped_resources:
            if resource.url not in all_resources:
                all_resources[resource.url] = resource
        
        # Add searched resources
        for resource in searched_resources:
            if resource.url not in all_resources:
                all_resources[resource.url] = resource
        
        return list(all_resources.values())
    
    def _generate_learning_path(
        self,
        use_case: str,
        difficulty: DifficultyLevel,
        resources: List[ResourceMetadata]
    ) -> List[Dict[str, str]]:
        """Generate a structured learning path."""
        learning_path = []
        
        # Define learning path templates
        if use_case == "authentication":
            if difficulty == DifficultyLevel.BEGINNER:
                learning_path = [
                    {
                        "step": "1",
                        "title": "Understanding Laravel Authentication",
                        "description": "Learn the basics of Laravel's authentication system",
                        "resource_type": "documentation"
                    },
                    {
                        "step": "2",
                        "title": "Setting up Laravel Breeze",
                        "description": "Install and configure Laravel Breeze for basic auth",
                        "resource_type": "tutorial"
                    },
                    {
                        "step": "3",
                        "title": "Customizing Authentication Views",
                        "description": "Learn to customize login and registration forms",
                        "resource_type": "tutorial"
                    },
                    {
                        "step": "4",
                        "title": "Adding Email Verification",
                        "description": "Implement email verification for new users",
                        "resource_type": "tutorial"
                    }
                ]
            elif difficulty == DifficultyLevel.INTERMEDIATE:
                learning_path = [
                    {
                        "step": "1",
                        "title": "Laravel Sanctum for API Authentication",
                        "description": "Set up token-based API authentication",
                        "resource_type": "documentation"
                    },
                    {
                        "step": "2",
                        "title": "Implementing OAuth with Socialite",
                        "description": "Add social login capabilities",
                        "resource_type": "tutorial"
                    },
                    {
                        "step": "3",
                        "title": "Multi-Guard Authentication",
                        "description": "Set up different user types with guards",
                        "resource_type": "tutorial"
                    }
                ]
        
        elif use_case == "api_development":
            learning_path = [
                {
                    "step": "1",
                    "title": "RESTful API Design Principles",
                    "description": "Understanding REST conventions in Laravel",
                    "resource_type": "article"
                },
                {
                    "step": "2",
                    "title": "API Resources and Transformers",
                    "description": "Transform models to JSON responses",
                    "resource_type": "documentation"
                },
                {
                    "step": "3",
                    "title": "API Versioning Strategies",
                    "description": "Implement API versioning in Laravel",
                    "resource_type": "tutorial"
                },
                {
                    "step": "4",
                    "title": "API Testing with Pest",
                    "description": "Write comprehensive API tests",
                    "resource_type": "tutorial"
                }
            ]
        
        # Match resources to learning path steps
        for step in learning_path:
            # Find best matching resource for this step
            for resource in resources:
                if (step["resource_type"] == resource.type.value and
                    any(keyword in resource.title.lower() 
                        for keyword in step["title"].lower().split())):
                    step["resource_url"] = resource.url
                    step["resource_title"] = resource.title
                    break
        
        return learning_path


class PackageCombinationGuide:
    """Provides guidance for using multiple packages together."""
    
    def __init__(self, resource_fetcher: LearningResourceFetcher):
        """Initialize with resource fetcher."""
        self.fetcher = resource_fetcher
        logger.info("Initialized PackageCombinationGuide")
    
    def get_combination_guide(
        self,
        packages: List[str]
    ) -> Optional[Dict[str, any]]:
        """Get guide for using multiple packages together."""
        # Normalize package names
        packages_normalized = [p.lower().strip() for p in packages]
        packages_tuple = tuple(sorted(packages_normalized))
        
        # Check predefined combinations
        if packages_tuple in PACKAGE_COMBINATIONS:
            combination_info = PACKAGE_COMBINATIONS[packages_tuple]
            
            # Check if we have a saved guide in the database
            saved_guide = self.fetcher.get_package_combination_guide(
                list(packages_tuple)
            )
            
            if saved_guide:
                return saved_guide
            else:
                # Save the predefined guide to database
                guide_id = self.fetcher.add_package_combination_guide(
                    packages=list(packages_tuple),
                    use_case=combination_info["use_case"],
                    guide=combination_info["guide"],
                    notes=combination_info["compatibility"]
                )
                
                return {
                    "id": guide_id,
                    "packages": list(packages_tuple),
                    "use_case": combination_info["use_case"],
                    "guide_content": combination_info["guide"],
                    "compatibility_notes": combination_info["compatibility"]
                }
        
        # Generate compatibility analysis for unknown combinations
        return self._analyze_package_compatibility(packages_normalized)
    
    def _analyze_package_compatibility(
        self,
        packages: List[str]
    ) -> Dict[str, any]:
        """Analyze compatibility between packages."""
        compatibility_notes = []
        potential_conflicts = []
        
        # Check for known compatibility patterns
        if "livewire" in packages and "inertia" in packages:
            potential_conflicts.append(
                "Livewire and Inertia.js serve similar purposes (building reactive UIs). "
                "Choose one approach for consistency."
            )
        
        if "breeze" in packages and "jetstream" in packages:
            potential_conflicts.append(
                "Breeze and Jetstream are alternative starter kits. "
                "Use Breeze for simplicity or Jetstream for more features."
            )
        
        if "sanctum" in packages and "passport" in packages:
            potential_conflicts.append(
                "Sanctum and Passport both handle API authentication. "
                "Sanctum is simpler for SPAs, Passport for OAuth2."
            )
        
        # Check for complementary packages
        if "filament" in packages and "spatie/laravel-permission" in packages:
            compatibility_notes.append(
                "Excellent combination: Filament has built-in support for "
                "Spatie's permission package through Filament Shield."
            )
        
        if "livewire" in packages and "alpine" in packages:
            compatibility_notes.append(
                "Perfect match: Alpine.js is included with Livewire by default."
            )
        
        # Generate guide
        guide_content = f"""
## Package Combination Analysis

**Packages:** {', '.join(packages)}

### Compatibility Assessment
"""
        
        if compatibility_notes:
            guide_content += "\n#### ✅ Compatible Packages\n"
            for note in compatibility_notes:
                guide_content += f"- {note}\n"
        
        if potential_conflicts:
            guide_content += "\n#### ⚠️ Potential Conflicts\n"
            for conflict in potential_conflicts:
                guide_content += f"- {conflict}\n"
        
        if not compatibility_notes and not potential_conflicts:
            guide_content += "\nNo specific compatibility information available for this combination.\n"
        
        guide_content += """
### General Integration Tips

1. **Check Documentation**: Review each package's documentation for integration guides
2. **Version Compatibility**: Ensure all packages support your Laravel version
3. **Load Order**: Some packages may need specific service provider registration order
4. **Configuration**: Check for any conflicting configuration keys
5. **Testing**: Write integration tests to verify packages work together correctly
"""
        
        return {
            "packages": packages,
            "compatibility_notes": "\n".join(compatibility_notes) if compatibility_notes else "No known compatibility issues",
            "guide_content": guide_content,
            "has_conflicts": len(potential_conflicts) > 0
        }


class SetupOrchestrator:
    """Orchestrates installation and setup workflows."""
    
    def __init__(self):
        """Initialize the setup orchestrator."""
        logger.info("Initialized SetupOrchestrator")
    
    def generate_setup_workflow(
        self,
        packages: List[str],
        use_case: Optional[str] = None
    ) -> Dict[str, any]:
        """Generate installation and setup workflow for packages."""
        workflow_steps = []
        
        # Determine installation order based on dependencies
        ordered_packages = self._determine_installation_order(packages)
        
        # Generate installation steps
        for i, package in enumerate(ordered_packages, 1):
            step = {
                "order": i,
                "package": package,
                "commands": self._get_installation_commands(package),
                "configuration": self._get_configuration_steps(package),
                "verification": self._get_verification_steps(package)
            }
            workflow_steps.append(step)
        
        # Add integration steps if multiple packages
        if len(packages) > 1:
            integration_steps = self._get_integration_steps(packages)
            workflow_steps.extend(integration_steps)
        
        return {
            "use_case": use_case or "Custom package setup",
            "packages": packages,
            "total_steps": len(workflow_steps),
            "estimated_time": f"{len(workflow_steps) * 5} minutes",
            "workflow": workflow_steps
        }
    
    def _determine_installation_order(self, packages: List[str]) -> List[str]:
        """Determine the optimal installation order."""
        # Define package dependencies
        dependencies = {
            "jetstream": ["sanctum", "livewire", "inertia"],
            "breeze": ["sanctum"],
            "filament": ["livewire"],
            "horizon": ["redis"],
            "telescope": [],
            "sanctum": [],
            "livewire": [],
            "inertia": []
        }
        
        ordered = []
        remaining = set(p.lower() for p in packages)
        
        # Install packages without dependencies first
        while remaining:
            for package in list(remaining):
                deps = dependencies.get(package, [])
                # Check if all dependencies are either installed or not in our list
                if all(dep not in remaining or dep in ordered for dep in deps):
                    ordered.append(package)
                    remaining.remove(package)
        
        return ordered
    
    def _get_installation_commands(self, package: str) -> List[str]:
        """Get installation commands for a package."""
        commands = {
            "sanctum": [
                "composer require laravel/sanctum",
                "php artisan vendor:publish --provider=\"Laravel\\Sanctum\\SanctumServiceProvider\"",
                "php artisan migrate"
            ],
            "livewire": [
                "composer require livewire/livewire",
                "php artisan livewire:publish --config"
            ],
            "inertia": [
                "composer require inertiajs/inertia-laravel",
                "php artisan inertia:middleware",
                "npm install @inertiajs/vue3"  # or react
            ],
            "filament": [
                "composer require filament/filament:\"^3.0\"",
                "php artisan filament:install --panels"
            ],
            "breeze": [
                "composer require laravel/breeze --dev",
                "php artisan breeze:install",
                "npm install && npm run dev"
            ],
            "horizon": [
                "composer require laravel/horizon",
                "php artisan horizon:install",
                "php artisan migrate"
            ],
            "telescope": [
                "composer require laravel/telescope",
                "php artisan telescope:install",
                "php artisan migrate"
            ]
        }
        
        return commands.get(package.lower(), [f"composer require {package}"])
    
    def _get_configuration_steps(self, package: str) -> List[str]:
        """Get configuration steps for a package."""
        configs = {
            "sanctum": [
                "Add Sanctum's middleware to api middleware group in app/Http/Kernel.php",
                "Configure stateful domains in config/sanctum.php",
                "Update config/cors.php for SPA support"
            ],
            "livewire": [
                "Add @livewireStyles and @livewireScripts to your layout",
                "Configure config/livewire.php as needed"
            ],
            "inertia": [
                "Set up your app.js with Inertia initialization",
                "Configure HandleInertiaRequests middleware",
                "Set up your root template with @inertia directive"
            ],
            "horizon": [
                "Configure config/horizon.php with your queue settings",
                "Set up Horizon authentication in HorizonServiceProvider",
                "Add horizon command to your deployment scripts"
            ]
        }
        
        return configs.get(package.lower(), ["Review package documentation for configuration"])
    
    def _get_verification_steps(self, package: str) -> List[str]:
        """Get verification steps for a package."""
        verifications = {
            "sanctum": [
                "Check migration: php artisan migrate:status",
                "Verify config: php artisan config:show sanctum"
            ],
            "livewire": [
                "Create test component: php artisan make:livewire counter",
                "Check Livewire scripts are loaded in browser console"
            ],
            "horizon": [
                "Start Horizon: php artisan horizon",
                "Visit /horizon to see dashboard"
            ],
            "telescope": [
                "Visit /telescope to see dashboard",
                "Make a request and verify it appears in Telescope"
            ]
        }
        
        return verifications.get(package.lower(), ["Verify package is listed in composer.json"])
    
    def _get_integration_steps(self, packages: List[str]) -> List[Dict[str, any]]:
        """Get integration steps for multiple packages."""
        integration_steps = []
        packages_lower = [p.lower() for p in packages]
        
        # Livewire + Alpine integration
        if "livewire" in packages_lower and "alpine" in packages_lower:
            integration_steps.append({
                "order": 100,
                "package": "integration",
                "commands": [],
                "configuration": [
                    "Alpine.js is included with Livewire - no extra setup needed",
                    "Use x-data for Alpine components alongside Livewire"
                ],
                "verification": ["Check Alpine is available in browser console: window.Alpine"]
            })
        
        return integration_steps