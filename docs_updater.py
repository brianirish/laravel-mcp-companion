#!/usr/bin/env python3
"""
Laravel Documentation Updater

This module handles automatic fetching and updating of Laravel documentation
from the official GitHub repository.
"""

import sys
import logging
import argparse
import shutil
import tempfile
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import urllib.request
import urllib.error
import zipfile
import json
import time
from enum import Enum
import random
import html

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("laravel-docs-updater")


# Utility functions for content filtering
def remove_social_media_lines(content: str) -> str:
    """
    Remove lines that are purely social media links from scraped content.
    Preserves legitimate documentation references (e.g., Envoy's @discord directive).
    """
    social_domains = ['x.com/laravelphp', 'x.com/laravel', 'twitter.com/laravelphp', 'twitter.com/laravel',
                      'discord.com/invite', 'discord.gg',
                      'linkedin.com/company', 'facebook.com', 'instagram.com', 'github.com/laravel']

    lines = content.split('\n')
    filtered = []

    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            filtered.append(line)
            continue

        # Skip nav list items pointing to social media
        if re.match(r'^[-*+]\s*\[Community\]\(https?://(discord|twitter)', stripped, re.IGNORECASE):
            continue

        # Count links in the line
        all_links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', stripped)
        if len(all_links) >= 3:  # If line has 3+ links, check if most are social
            social_link_count = sum(1 for text, url in all_links if any(domain in url for domain in social_domains))
            # If 50% or more of the links are social media, remove the line
            if social_link_count >= len(all_links) * 0.5:
                continue

        # Check if line is entirely composed of social media links
        # Remove all markdown links from the line to see what remains
        text_without_links = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', stripped)

        # If after removing links we have substantial text, keep the line
        # But if it's only link text that are domain names or social network names, skip it
        if text_without_links.strip():
            # Check if the remaining text is just social network names strung together
            social_names = ['x', 'github', 'discord', 'linkedin', 'facebook', 'instagram', 'twitter']
            text_lower = text_without_links.lower().strip()

            # Use word boundary matching to avoid false positives (e.g., "example" containing "x")
            # Split on non-word characters and check if all remaining words are social names
            words = re.findall(r'\b\w+\b', text_lower)
            if words and all(word in social_names for word in words):
                # All words are social network names, check if social domains are present
                if any(domain in stripped for domain in social_domains):
                    continue

        filtered.append(line)

    return '\n'.join(filtered)


def remove_image_references(content: str) -> str:
    """
    Remove markdown image references from scraped content.
    Preserves images inside code blocks.
    """
    lines = content.split('\n')
    in_code_block = False
    filtered = []

    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            filtered.append(line)
            continue

        if not in_code_block:
            # Remove image references from the line
            cleaned = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', line)

            # Skip lines that became empty or just bullet/whitespace after removal
            stripped_cleaned = cleaned.strip()
            if not stripped_cleaned or stripped_cleaned in ('*', '-', '+'):
                # Line had only image(s), skip it
                continue

            # Line has other content, keep the cleaned version
            filtered.append(cleaned)
        else:
            filtered.append(line)

    return '\n'.join(filtered)


# GitHub API URLs
GITHUB_API_URL = "https://api.github.com"
LARAVEL_DOCS_REPO = "laravel/docs"
USER_AGENT = "Laravel-MCP-Companion (+https://github.com/brianirish/laravel-mcp-companion)"

def get_supported_versions() -> list[str]:
    """Get supported Laravel versions dynamically from GitHub API.
    
    Returns:
        List of supported version branches (e.g., ['6.x', '7.x', '8.x', ...])
    """
    logger.debug("Fetching supported Laravel versions from GitHub API")
    
    url = f"{GITHUB_API_URL}/repos/{LARAVEL_DOCS_REPO}/branches"
    
    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/vnd.github.v3+json"
            }
        )
        
        with urllib.request.urlopen(request) as response:
            branches = json.loads(response.read().decode())
            
            # Filter for version branches (X.x format) starting from 6.x
            version_branches = []
            for branch in branches:
                name = branch["name"]
                if re.match(r'^\d+\.x$', name):
                    major_version = int(name.split('.')[0])
                    if major_version >= 6:
                        version_branches.append(name)
            
            # Sort versions numerically
            version_branches.sort(key=lambda v: int(v.split('.')[0]))
            
            if not version_branches:
                logger.warning("No version branches found, falling back to hardcoded list")
                return ["6.x", "7.x", "8.x", "9.x", "10.x", "11.x", "12.x"]
            
            logger.debug(f"Found {len(version_branches)} supported versions: {', '.join(version_branches)}")
            return version_branches
            
    except Exception as e:
        logger.warning(f"Error fetching versions from GitHub API: {str(e)}, falling back to hardcoded list")
        return ["6.x", "7.x", "8.x", "9.x", "10.x", "11.x", "12.x"]

# Cache supported versions to avoid repeated API calls
_SUPPORTED_VERSIONS_CACHE = None

def get_cached_supported_versions() -> list[str]:
    """Get cached supported versions or fetch them if not cached."""
    global _SUPPORTED_VERSIONS_CACHE
    if _SUPPORTED_VERSIONS_CACHE is None:
        _SUPPORTED_VERSIONS_CACHE = get_supported_versions()
    return _SUPPORTED_VERSIONS_CACHE

SUPPORTED_VERSIONS = get_cached_supported_versions()
DEFAULT_VERSION = SUPPORTED_VERSIONS[-1]  # Always use the latest version as default
USER_AGENT = "Laravel-MCP-Companion (+https://github.com/brianirish/laravel-mcp-companion)"

class DocumentationSourceType(Enum):
    """Types of documentation sources supported."""
    GITHUB_REPO = "github_repo"
    DIRECT_URL = "direct_url"
    LARAVEL_SERVICE = "laravel_service"
    COMMUNITY_PACKAGE = "community_package"

class DocumentationAutoDiscovery:
    """Handles automatic discovery of documentation sections from Laravel services."""
    
    def __init__(self, max_retries: int = 3, request_delay: float = 1.0):
        """
        Initialize the documentation auto-discovery system.
        
        Args:
            max_retries: Maximum number of retry attempts for failed requests
            request_delay: Delay between requests in seconds to be respectful
        """
        self.max_retries = max_retries
        self.request_delay = request_delay
        
        # Common asset file extensions and patterns to exclude
        self.asset_extensions = {'.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf', '.eot'}
        self.asset_patterns = {'/_next/', '/static/', '/assets/', '/images/', '/fonts/', '/favicon'}
        
    def discover_sections(self, service: str, service_config: Dict) -> List[str]:
        """
        Discover documentation sections for a given service.
        
        Args:
            service: Service name (forge, vapor, envoyer, nova)
            service_config: Service configuration dictionary
            
        Returns:
            List of discovered section paths
        """
        if not service_config.get("auto_discovery", False):
            logger.debug(f"Auto-discovery disabled for {service}")
            return []
        
        discovery_rules = service_config.get("discovery_rules", {})
        discovered_sections = []
        
        try:
            logger.info(f"Starting auto-discovery for {service}")
            
            if service == "forge":
                discovered_sections = self._discover_forge_sections(service_config, discovery_rules)
            elif service == "nova":
                discovered_sections = self._discover_nova_sections(service_config, discovery_rules)
            elif service == "vapor":
                discovered_sections = self._discover_vapor_sections(service_config, discovery_rules)
            elif service == "envoyer":
                discovered_sections = self._discover_envoyer_sections(service_config, discovery_rules)
            else:
                logger.warning(f"No discovery method available for service: {service}")
                
            logger.info(f"Auto-discovery completed for {service}: found {len(discovered_sections)} sections")
            return discovered_sections
            
        except Exception as e:
            logger.error(f"Error during auto-discovery for {service}: {str(e)}")
            return []
    
    def _is_asset_file(self, path: str) -> bool:
        """
        Check if a path represents an asset file (CSS, JS, images, etc.).
        
        Args:
            path: URL path to check
            
        Returns:
            True if the path is an asset file, False otherwise
        """
        # Remove query parameters for extension check
        clean_path = path.split('?')[0].lower()
        
        # Check if path contains common asset directories
        for pattern in self.asset_patterns:
            if pattern in clean_path:
                return True
        
        # Check file extension
        for ext in self.asset_extensions:
            if clean_path.endswith(ext):
                return True
                
        return False
    
    def _discover_forge_sections(self, config: Dict, rules: Dict) -> List[str]:
        """Discover Forge documentation sections by parsing the docs index page."""
        base_url = config["base_url"]
        sections = []
        
        try:
            # Fetch the main docs page
            content_bytes = self._retry_request(f"{base_url}")
            content = content_bytes.decode('utf-8')
            
            # Extract href="/docs/*" links using regex
            doc_links = re.findall(r'href="(/docs/[^"]*)"', content, re.IGNORECASE)
            
            for link in doc_links:
                # Remove query parameters and fragments
                clean_link = link.split('?')[0].split('#')[0]

                # Check if this is an asset file (CSS, JS, images, etc.)
                if self._is_asset_file(clean_link):
                    continue

                # Remove the /docs/ prefix to get the section name
                section = clean_link.replace('/docs/', '')

                # Exclude non-documentation files
                if section in ('sitemap.xml', 'sitemap', 'robots.txt'):
                    continue

                if section and section not in sections:
                    sections.append(section)
                    
            # Sort sections to maintain consistent ordering
            sections.sort()
            logger.debug(f"Discovered {len(sections)} Forge sections")
            
        except Exception as e:
            logger.warning(f"Error discovering Forge sections: {str(e)}")
            
        return sections
    
    def _discover_nova_sections(self, config: Dict, rules: Dict) -> List[str]:
        """Discover Nova documentation sections and auto-detect version."""
        base_url = config["base_url"]
        sections = []
        
        try:
            # First, try to detect the latest version
            nova_base = "https://nova.laravel.com/docs"
            
            # Try to find version links or check if current version is still valid
            content_bytes = self._retry_request(f"{nova_base}")
            content = content_bytes.decode('utf-8')
            
            # Look for version links like /docs/v6, /docs/v5, etc.
            version_matches = re.findall(r'/docs/(v\d+)', content)
            if version_matches:
                latest_version = max(version_matches, key=lambda v: int(v[1:]))
                actual_base_url = f"{nova_base}/{latest_version}"
                logger.info(f"Auto-detected Nova version: {latest_version}")
            else:
                actual_base_url = base_url
            
            # Fetch the navigation/index page
            nav_content_bytes = self._retry_request(f"{actual_base_url}")
            nav_content = nav_content_bytes.decode('utf-8')
            
            # Extract navigation links - Nova typically uses relative links
            nav_links = re.findall(r'href="(/docs/[^"]*)"', nav_content, re.IGNORECASE)
            
            for link in nav_links:
                # Remove fragments from link
                clean_link = link.split('#')[0]
                # Extract section after version (e.g., /docs/v5/installation -> installation)
                section_match = re.search(r'/docs/v\d+/(.+)', clean_link)
                if section_match:
                    section = section_match.group(1)

                    # Exclude non-documentation files
                    if section in ('sitemap.xml', 'sitemap', 'robots.txt'):
                        continue

                    if section and section not in sections:
                        sections.append(section)
            
            sections.sort()
            logger.debug(f"Discovered {len(sections)} Nova sections")
            
        except Exception as e:
            logger.warning(f"Error discovering Nova sections: {str(e)}")
            
        return sections
    
    def _discover_vapor_sections(self, config: Dict, rules: Dict) -> List[str]:
        """Discover Vapor documentation sections by parsing Mintlify navigation."""
        base_url = config["base_url"]
        sections = []
        
        try:
            # Vapor uses Mintlify, which often has a special navigation structure
            content_bytes = self._retry_request(f"{base_url}")
            content = content_bytes.decode('utf-8')
            
            # Look for Mintlify navigation patterns
            # Try multiple patterns that Mintlify commonly uses
            nav_patterns = [
                r'href="(/[^"]*)"[^>]*>([^<]+)</a>',  # General link pattern
                r'"href":"(/[^"]*)"',  # JSON-style navigation
                r'data-href="(/[^"]*)"',  # Data attribute pattern
            ]
            
            for pattern in nav_patterns:
                links = re.findall(pattern, content, re.IGNORECASE)
                for link in links:
                    if isinstance(link, tuple):
                        path = link[0]
                    else:
                        path = link
                    
                    # Filter for documentation paths (exclude external links, assets, etc.)
                    if (path.startswith('/') and
                        not path.startswith('//') and
                        not self._is_asset_file(path) and
                        path != '/'):

                        # Strip fragment identifier (everything after #)
                        path_without_fragment = path.split('#')[0]
                        section = path_without_fragment.lstrip('/')

                        # Exclude non-documentation files
                        if section in ('sitemap.xml', 'sitemap', 'robots.txt'):
                            continue

                        if section and section not in sections:
                            sections.append(section)
            
            # Remove dupliculates and sort
            sections = list(set(sections))
            sections.sort()
            logger.debug(f"Discovered {len(sections)} Vapor sections")
            
        except Exception as e:
            logger.warning(f"Error discovering Vapor sections: {str(e)}")
            
        return sections
    
    def _discover_envoyer_sections(self, config: Dict, rules: Dict) -> List[str]:
        """Discover Envoyer documentation sections, handling category redirects."""
        base_url = config["base_url"]
        sections = []
        
        try:
            # Fetch the main docs page
            content_bytes = self._retry_request(f"{base_url}")
            content = content_bytes.decode('utf-8')
            
            # Extract documentation links
            doc_links = re.findall(r'href="(/docs/[^"]*)"', content, re.IGNORECASE)
            
            for link in doc_links:
                # Remove fragments and /docs/ prefix
                clean_link = link.split('#')[0]
                section = clean_link.replace('/docs/', '')

                # Exclude non-documentation files
                if section in ('sitemap.xml', 'sitemap', 'robots.txt'):
                    continue

                if section and section not in sections:
                    # Test if this is a real page (not a redirect)
                    try:
                        test_url = f"{base_url}/{section}"
                        test_content_bytes = self._retry_request(test_url)
                        test_content = test_content_bytes.decode('utf-8')
                        
                        # Check if this is actual documentation content
                        if self._is_valid_envoyer_content(test_content, section):
                            sections.append(section)
                        else:
                            logger.debug(f"Skipping {section} - appears to be redirect or invalid content")
                            
                    except Exception as test_e:
                        logger.debug(f"Skipping {section} - error testing content: {str(test_e)}")
                        continue
            
            sections.sort()
            logger.debug(f"Discovered {len(sections)} Envoyer sections")
            
        except Exception as e:
            logger.warning(f"Error discovering Envoyer sections: {str(e)}")
            
        return sections
    
    def _is_valid_envoyer_content(self, content: str, section: str) -> bool:
        """Check if Envoyer content is actual documentation (not redirect page)."""
        # Look for common documentation indicators
        doc_indicators = [
            'envoyer', 'deployment', 'zero downtime', 'project', 
            'server', 'hook', 'notification', 'repository'
        ]
        
        # Look for redirect indicators (things that suggest this isn't real content)
        redirect_indicators = [
            'window.location', 'http-equiv="refresh"', 'redirecting',
            'please wait', 'loading...', 'not found'
        ]
        
        content_lower = content.lower()
        
        # Check for documentation indicators
        doc_score = sum(1 for indicator in doc_indicators if indicator in content_lower)
        
        # Check for redirect indicators
        redirect_score = sum(1 for indicator in redirect_indicators if indicator in content_lower)
        
        # Must have some documentation indicators and minimal redirect indicators
        return doc_score >= 1 and redirect_score == 0 and len(content.strip()) > 500
    
    def _retry_request(self, url: str, headers: Optional[Dict] = None) -> bytes:
        """
        Make a request with retry logic and respectful delays.
        
        Args:
            url: URL to request
            headers: Optional headers to include
            
        Returns:
            Response content as bytes
        """
        if headers is None:
            headers = {"User-Agent": USER_AGENT}
        
        last_exception: Optional[Exception] = None
        
        for attempt in range(self.max_retries + 1):
            try:
                # Add respectful delay between requests
                if attempt > 0:
                    time.sleep(self.request_delay * (2 ** (attempt - 1)))
                
                request = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(request) as response:
                    return response.read()
                    
            except urllib.error.HTTPError as e:
                last_exception = e
                if e.code == 404:
                    # Don't retry 404 errors
                    raise
                elif e.code == 429 or (e.code == 403 and "rate limit" in str(e.reason).lower()):
                    # Rate limiting - wait longer
                    if attempt < self.max_retries:
                        wait_time = min(300, (2 ** attempt) * 10 + random.uniform(0, 5))
                        logger.warning(f"Rate limited on attempt {attempt + 1}, waiting {wait_time:.1f}s")
                        time.sleep(wait_time)
                    else:
                        raise
                elif e.code >= 500 and attempt < self.max_retries:
                    # Server errors are worth retrying
                    wait_time = min(60, (2 ** attempt) + random.uniform(0, 2))
                    logger.warning(f"Server error {e.code} on attempt {attempt + 1}, retrying in {wait_time:.1f}s")
                    time.sleep(wait_time)
                else:
                    raise
                    
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    wait_time = min(30, (2 ** attempt) + random.uniform(0, 2))
                    logger.warning(f"Request error on attempt {attempt + 1}, retrying in {wait_time:.1f}s: {str(e)}")
                    time.sleep(wait_time)
                else:
                    raise
        
        # This should never be reached, but just in case
        if last_exception:
            raise last_exception
        else:
            raise RuntimeError(f"Failed to fetch {url} after {self.max_retries + 1} attempts")


class ExternalDocsFetcher:
    """Handles fetching documentation from external Laravel services and packages."""
    
    def __init__(self, target_dir: Path, cache_duration: int = 86400, max_retries: int = 3):
        """
        Initialize the external documentation fetcher.
        
        Args:
            target_dir: Directory where external docs should be stored
            cache_duration: Cache duration in seconds (default: 24 hours)
            max_retries: Maximum number of retry attempts for failed requests
        """
        self.target_dir = target_dir
        self.cache_duration = cache_duration
        self.max_retries = max_retries
        self.external_dir = target_dir / "external"
        self.external_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize auto-discovery system
        self.auto_discovery = DocumentationAutoDiscovery(max_retries=max_retries)
        
        # Laravel services documentation sources
        self.laravel_services = {
            "forge": {
                "name": "Laravel Forge",
                "type": DocumentationSourceType.LARAVEL_SERVICE,
                "base_url": "https://forge.laravel.com/docs",
                "auto_discovery": True,
                "discovery_rules": {
                    "index_url": "https://forge.laravel.com/docs",
                    "link_pattern": r'href="(/docs/[^"]*)"',
                    "nested_sections": ["accounts", "servers", "sites", "resources"]
                },
                "sections": [
                    # Get Started (manual fallback)
                    "introduction", "cli", "sdk",
                    # Accounts  
                    "accounts/your-account", "accounts/circles", "accounts/source-control", "accounts/ssh", "accounts/api",
                    # Servers
                    "servers/providers", "servers/types", "servers/management", "servers/provisioning-process",
                    "servers/ssh", "servers/php", "servers/packages", "servers/recipes", "servers/load-balancing",
                    "servers/nginx-templates", "servers/backups", "servers/monitoring", "servers/cookbook",
                    # Sites
                    "sites/the-basics", "sites/applications", "sites/deployments", "sites/commands",
                    "sites/packages", "sites/queues", "sites/security-rules", "sites/redirects",
                    "sites/ssl", "sites/user-isolation", "sites/cookbook",
                    # Resources
                    "resources/daemons", "resources/databases", "resources/caches", "resources/network",
                    "resources/scheduler", "resources/integrations", "resources/cookbook"
                ]
            },
            "vapor": {
                "name": "Laravel Vapor", 
                "type": DocumentationSourceType.LARAVEL_SERVICE,
                "base_url": "https://docs.vapor.build",
                "auto_discovery": True,
                "discovery_rules": {
                    "index_url": "https://docs.vapor.build",
                    "navigation_patterns": [
                        r'href="(/[^"]*)"[^>]*>([^<]+)</a>',
                        r'"href":"(/[^"]*)"',
                        r'data-href="(/[^"]*)"'
                    ],
                    "exclude_extensions": [".css", ".js", ".png", ".jpg", ".svg"],
                    "min_content_length": 500
                },
                "sections": [
                    # Manual fallback sections
                    "introduction", "projects/the-basics", "projects/environments",
                    "projects/deployments", "resources/queues", "resources/storage",
                    "resources/databases", "resources/caches"
                ]
            },
            "envoyer": {
                "name": "Laravel Envoyer",
                "type": DocumentationSourceType.LARAVEL_SERVICE,
                "base_url": "https://docs.envoyer.io",
                "auto_discovery": True,
                "discovery_rules": {
                    "index_url": "https://docs.envoyer.io",
                    "link_pattern": r'href="(/docs/[^"]*)"',
                    "validate_content": True,
                    "content_indicators": ["envoyer", "deployment", "zero downtime", "project"],
                    "redirect_indicators": ["window.location", "redirecting", "loading..."]
                },
                "sections": [
                    # Manual fallback sections
                    "introduction", "quick-start",
                    "accounts/source-control", "accounts/your-account",
                    "projects/management", "projects/servers", "projects/deployment-hooks",
                    "projects/heartbeats", "projects/notifications", "projects/collaborators"
                ]
            },
            "nova": {
                "name": "Laravel Nova",
                "type": DocumentationSourceType.LARAVEL_SERVICE,
                "base_url": "https://nova.laravel.com/docs/v5",
                "auto_discovery": True,
                "discovery_rules": {
                    "base_url": "https://nova.laravel.com/docs",
                    "version_detection": True,
                    "version_pattern": r'/docs/(v\d+)',
                    "link_pattern": r'href="(/docs/[^"]*)"',
                    "section_pattern": r'/docs/v\d+/(.+)',
                    "navigation_sections": ["Get Started", "Resources", "Search", "Filters", "Lenses", "Actions", "Metrics", "Digging Deeper"]
                },
                "sections": [
                    # Manual fallback sections
                    # Get Started
                    "installation", "releases", "upgrade",
                    # Resources
                    "resources/the-basics", "resources/fields", "resources/dependent-fields",
                    "resources/date-fields", "resources/file-fields", "resources/repeater-fields",
                    "resources/panels", "resources/relationships", "resources/validation", "resources/authorization",
                    # Search
                    "search/the-basics", "search/global-search", "search/scout-integration", 
                    # Filters
                    "filters/defining-filters", "filters/registering-filters",
                    # Lenses  
                    "lenses/defining-lenses", "lenses/registering-lenses",
                    # Actions
                    "actions/defining-actions", "actions/registering-actions",
                    # Metrics
                    "metrics/defining-metrics", "metrics/registering-metrics",
                    # Digging Deeper (Customization)
                    "customization/dashboards", "customization/menus", "customization/notifications",
                    "customization/authentication", "customization/impersonation", "customization/tools",
                    "customization/resource-tools", "customization/cards", "customization/fields",
                    "customization/filters", "customization/frontend", "customization/assets",
                    "customization/localization", "customization/stubs"
                ]
            }
        }
    
    def get_service_cache_path(self, service: str) -> Path:
        """Get the cache directory path for a service."""
        service_dir = self.external_dir / service
        service_dir.mkdir(exist_ok=True)
        return service_dir
    
    def get_cache_metadata_path(self, service: str) -> Path:
        """Get the metadata file path for a service."""
        return self.get_service_cache_path(service) / ".cache_metadata.json"
    
    def is_cache_valid(self, service: str) -> bool:
        """Check if the cached documentation for a service is still valid.

        Cache is considered invalid if:
        - Metadata file doesn't exist
        - Cache is older than cache_duration
        - Success rate is below 90%
        """
        metadata_path = self.get_cache_metadata_path(service)

        if not metadata_path.exists():
            return False

        try:
            # Read metadata to get cached_at timestamp and success_rate
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

            cache_time = metadata.get('cached_at', 0)
            success_rate = metadata.get('success_rate', 0.0)

            # Check if cache is too old
            is_fresh = (time.time() - cache_time) < self.cache_duration

            # Check if success rate is acceptable (90% threshold)
            is_quality = success_rate >= 0.9

            if not is_quality:
                logger.info(f"Cache for {service} has low success rate ({success_rate:.1%}), invalidating")
                return False

            return is_fresh
        except Exception as e:
            logger.warning(f"Error reading cache metadata for {service}: {str(e)}")
            return False
    
    def save_cache_metadata(self, service: str, metadata: Dict) -> None:
        """Save cache metadata for a service."""
        metadata_path = self.get_cache_metadata_path(service)
        
        try:
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving cache metadata for {service}: {str(e)}")
    
    def fetch_laravel_service_docs(self, service: str) -> bool:
        """
        Fetch documentation for a Laravel service.
        
        Args:
            service: Service name (forge, vapor, envoyer, nova)
            
        Returns:
            True if successful, False otherwise
        """
        if service not in self.laravel_services:
            logger.error(f"Unknown Laravel service: {service}")
            return False
        
        # Check if cache is valid
        if self.is_cache_valid(service):
            logger.debug(f"Using cached documentation for {service}")
            return True
        
        service_config = self.laravel_services[service]
        service_dir = self.get_service_cache_path(service)
        
        logger.info(f"Fetching documentation for {service_config['name']}")
        
        try:
            if service_config["type"] == DocumentationSourceType.LARAVEL_SERVICE:
                return self._fetch_service_documentation(service, service_config, service_dir)
            elif service_config["type"] == DocumentationSourceType.GITHUB_REPO:
                return self._fetch_github_documentation(service, service_config, service_dir)
            else:
                logger.error(f"Unsupported documentation source type for {service}")
                return False
        except Exception as e:
            logger.error(f"Error fetching documentation for {service}: {str(e)}")
            return False
    
    def _fetch_service_documentation(self, service: str, config: Dict, target_dir: Path) -> bool:
        """Fetch documentation from Laravel service websites."""
        base_url = config["base_url"]
        
        # Try auto-discovery first, fallback to manual sections
        discovered_sections = []
        manual_sections = config.get("sections", [])

        if config.get("auto_discovery", False):
            try:
                discovered_sections = self.auto_discovery.discover_sections(service, config)
                logger.info(f"Auto-discovery found {len(discovered_sections)} sections for {service}")
            except Exception as e:
                logger.warning(f"Auto-discovery failed for {service}: {str(e)}, falling back to manual sections")

        # Use discovered sections if available AND better than manual fallback
        # Otherwise use manual sections
        should_use_discovery = (
            discovered_sections and
            (not manual_sections or len(discovered_sections) >= len(manual_sections) * 0.75)
        )

        if should_use_discovery:
            sections = discovered_sections
            discovery_method = "auto-discovery"
        else:
            if discovered_sections and manual_sections:
                logger.info(f"Auto-discovery found only {len(discovered_sections)} sections but manual config has {len(manual_sections)}, using manual")
            sections = manual_sections
            discovery_method = "manual configuration"

        logger.info(f"Using {discovery_method} for {service}: {len(sections)} sections")
        
        # All configured services are now publicly accessible
        # No longer creating placeholder documentation
        
        fetched_sections = []
        
        for section in sections:
            # Double-check that this isn't an asset file
            if self.auto_discovery._is_asset_file(section):
                logger.debug(f"Skipping asset file: {section}")
                continue
                
            section_url = f"{base_url}/{section}"
            section_file = target_dir / f"{section}.md"
            
            # Create parent directories if needed for nested sections
            section_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                logger.debug(f"Fetching {section} documentation from {section_url}")
                content_bytes = self._retry_request(section_url)
                content = content_bytes.decode('utf-8')
                
                # Extract main content (this would need service-specific parsing)
                # For now, we'll save the raw HTML and note that it needs processing
                processed_content = self._process_service_html(content, service, section)
                
                with open(section_file, 'w', encoding='utf-8') as f:
                    f.write(processed_content)
                
                fetched_sections.append(section)
                logger.debug(f"Successfully fetched {section} documentation")
                
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    logger.info(f"Section {section} not found (404) - may not be available")
                else:
                    logger.warning(f"Failed to fetch {section} documentation: HTTP {e.code}")
                continue
            except Exception as e:
                logger.warning(f"Failed to fetch {section} documentation: {str(e)}")
                continue
        
        if fetched_sections:
            # Save metadata about what was fetched
            metadata = {
                "service": service,
                "fetched_sections": fetched_sections,
                "total_sections": len(sections),
                "success_rate": len(fetched_sections) / len(sections),
                "discovery_method": discovery_method,
                "auto_discovery_enabled": config.get("auto_discovery", False),
                "discovered_count": len(discovered_sections) if discovered_sections else 0,
                "manual_fallback": discovery_method == "manual configuration" and config.get("auto_discovery", False)
            }
            self.save_cache_metadata(service, metadata)
            logger.info(f"Successfully fetched {len(fetched_sections)}/{len(sections)} sections for {service} using {discovery_method}")
            return True
        
        return False
    
    def _create_placeholder_documentation(self, service: str, config: Dict, target_dir: Path) -> bool:
        """Create placeholder documentation for services that require authentication."""
        logger.info(f"Creating placeholder documentation for {service} (authentication required)")
        
        sections = config.get("sections", [])
        service_name = config.get("name", service.title())
        base_url = config.get("base_url", "")
        
        for section in sections:
            section_file = target_dir / f"{section}.md"
            
            content = f"# {service_name} - {section.replace('-', ' ').title()}\n\n"
            content += f"*Note: {service_name} documentation requires authentication to access.*\n\n"
            content += "## Overview\n\n"
            content += f"This section covers {section.replace('-', ' ')} functionality in {service_name}.\n\n"
            content += "## Documentation Access\n\n"
            content += f"To access the complete {service_name} documentation:\n\n"
            content += f"1. Visit [{service_name}]({base_url.replace('/docs/1.0', '')})\n"
            content += "2. Sign in to your account\n"
            content += "3. Navigate to the documentation section\n\n"
            content += "## Common Use Cases\n\n"
            
            if service == "vapor":
                if section == "getting-started":
                    content += "- Setting up serverless Laravel applications\n"
                    content += "- Configuring AWS Lambda deployment\n"
                elif section == "projects":
                    content += "- Creating and managing Vapor projects\n"
                    content += "- Environment configuration\n"
                elif section == "deployments":
                    content += "- Deploying Laravel applications to AWS Lambda\n"
                    content += "- Managing deployment rollbacks\n"
            elif service == "envoyer":
                if section == "getting-started":
                    content += "- Setting up zero-downtime deployment\n"
                    content += "- Connecting your repositories\n"
                elif section == "projects":
                    content += "- Creating deployment projects\n"
                    content += "- Managing project settings\n"
                elif section == "deployments":
                    content += "- Configuring deployment hooks\n"
                    content += "- Managing deployment history\n"
            
            content += f"\n*For detailed information, please visit the official {service_name} documentation.*\n"
            
            with open(section_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Save metadata
        metadata = {
            "service": service,
            "fetched_sections": sections,
            "total_sections": len(sections),
            "success_rate": 1.0,
            "type": "placeholder"
        }
        self.save_cache_metadata(service, metadata)
        
        logger.info(f"Created placeholder documentation for {service} with {len(sections)} sections")
        return True
    
    def _fetch_github_documentation(self, service: str, config: Dict, target_dir: Path) -> bool:
        """Fetch documentation from GitHub repositories."""
        repo = config["repo"]
        branch = config.get("branch", "main")
        
        # Use similar logic to the main DocsUpdater but for external repos
        archive_url = f"https://github.com/{repo}/archive/refs/heads/{branch}.zip"
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                zip_path = temp_path / f"{service}_docs.zip"
                
                logger.debug(f"Downloading {service} documentation from {archive_url}")
                content_bytes = self._retry_request(archive_url)
                
                with open(zip_path, 'wb') as out_file:
                    out_file.write(content_bytes)
                
                # Extract the zip file
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_path)
                
                # Find the extracted directory
                extracted_dirs = [d for d in temp_path.iterdir() if d.is_dir() and d.name.startswith(repo.split('/')[-1])]
                
                if not extracted_dirs:
                    raise FileNotFoundError(f"Could not find extracted {service} documentation directory")
                
                extracted_dir = extracted_dirs[0]
                
                # Clear the target directory
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                target_dir.mkdir(parents=True)
                
                # Copy documentation files
                for item in extracted_dir.iterdir():
                    if item.is_dir():
                        shutil.copytree(item, target_dir / item.name)
                    else:
                        shutil.copy2(item, target_dir / item.name)
                
                # Save metadata
                metadata = {
                    "service": service,
                    "repo": repo,
                    "branch": branch,
                    "fetch_method": "github_archive"
                }
                self.save_cache_metadata(service, metadata)
                
                logger.info(f"Successfully fetched GitHub documentation for {service}")
                return True
                
        except Exception as e:
            logger.error(f"Error fetching GitHub documentation for {service}: {str(e)}")
            return False
    
    def _process_service_html(self, html_content: str, service: str, section: str) -> str:
        """
        Process HTML content from Laravel services to extract documentation.
        Extracts main content from HTML and converts to markdown-like format.
        """
        # Basic HTML content extraction
        processed_content = f"# {service.title()} - {section.title()}\n\n"
        processed_content += f"*Source: {self.laravel_services[service]['base_url']}/{section}*\n\n"
        processed_content += "---\n\n"
        
        try:
            # Try to extract meaningful content from HTML
            content_text = self._extract_html_content(html_content)
            if len(content_text.strip()) > 100:  # Simplified validation for testing
                processed_content += content_text
            else:
                # Log warning but don't create fake content
                logger.warning(f"Content extraction failed for {service}/{section} - content too short or invalid")
                processed_content += f"*Content extraction failed for {service.title()} {section}.*\n"
                processed_content += "*This may indicate a URL redirect or parsing issue.*\n\n"
                processed_content += "*Please visit the official documentation at the source URL above.*\n\n"
                processed_content += f"<!-- Content length: {len(content_text.strip()) if content_text else 0} characters -->\n"
        except Exception as e:
            logger.warning(f"Error processing HTML content for {service}/{section}: {str(e)}")
            processed_content += f"*Content processing error: {str(e)}*\n\n"
            processed_content += "*Please visit the official documentation at the source URL above.*\n\n"
        
        return processed_content
    
    def _extract_html_content(self, html_content: str) -> str:
        """
        Extract readable content from HTML using markdownify.
        Simplified approach that leverages markdownify's built-in HTML parsing.
        """
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            logger.warning("BeautifulSoup not installed, using simple extraction")
            # Fallback to just converting the entire HTML
            text_content = self._html_to_text(html_content)
            return text_content[:10000] if len(text_content) > 10000 else text_content
        
        # Parse HTML with BeautifulSoup for better content extraction
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Try to find main content areas
        content_areas = [
            soup.find('main'),
            soup.find('article'),
            soup.find('div', class_=re.compile(r'prose|content|documentation|markdown', re.I)),
            soup.find('div', id=re.compile(r'content|docs|documentation', re.I)),
            soup.find('section', class_=re.compile(r'content|docs', re.I)),
        ]
        
        # Use the first valid content area found
        content_html = None
        for area in content_areas:
            if area and len(str(area)) > 200:  # Ensure it has substantial content
                content_html = str(area)
                break
        
        # If no specific content area found, use the body
        if not content_html:
            body = soup.find('body')
            content_html = str(body) if body else html_content
        
        # Convert to markdown
        text_content = self._html_to_text(content_html)
        
        # Limit length to prevent extremely long outputs
        if len(text_content) > 50000:
            text_content = text_content[:50000] + "\n\n*[Content truncated for length]*"
        
        return text_content
    
    def _is_valid_content(self, content: str, service: str, section: str) -> bool:
        """
        Validate that extracted content is actually documentation.
        Enhanced version with better quality scoring.
        
        Args:
            content: Extracted text content
            service: Service name (forge, vapor, etc.)
            section: Section name
            
        Returns:
            True if content appears to be valid documentation
        """
        if not content or len(content.strip()) < 200:
            return False
        
        # Check for service-specific keywords that indicate real documentation
        service_keywords = {
            "forge": ["server", "deployment", "laravel", "forge", "provision", "ssh", "nginx", "database"],
            "vapor": ["serverless", "lambda", "aws", "vapor", "deployment", "environment", "queue", "cache"],
            "envoyer": ["zero downtime", "deployment", "envoyer", "rollback", "hook", "notification", "repository"],
            "nova": ["admin", "resource", "nova", "eloquent", "dashboard", "field", "filter", "lens", "action", "metric"]
        }
        
        # Enhanced section-specific keywords
        section_keywords = {
            "introduction": ["overview", "getting started", "what is", "welcome"],
            "installation": ["install", "composer", "requirements", "setup"],
            "deployment": ["deploy", "release", "production", "build"],
            "backups": ["backup", "database", "restore", "snapshot"],
            "ssl": ["certificate", "https", "tls", "ssl", "encryption"],
            "authentication": ["auth", "login", "user", "password", "token"],
            "configuration": ["config", "settings", "environment", "env"],
            "database": ["mysql", "postgresql", "migration", "schema", "query"]
        }
        
        content_lower = content.lower()
        
        # Quality scoring system
        quality_score = 0
        
        # Service keyword matching (higher weight)
        service_matches = 0
        if service in service_keywords:
            service_matches = sum(1 for keyword in service_keywords[service] if keyword in content_lower)
            quality_score += service_matches * 2
        
        # Section keyword matching
        section_base = section.split('/')[-1].replace('-', ' ')
        if section_base in section_keywords:
            section_matches = sum(1 for keyword in section_keywords[section_base] if keyword in content_lower)
            quality_score += section_matches
        
        # Generic documentation indicators
        doc_indicators = [
            "documentation", "guide", "tutorial", "reference", "api", "configuration", 
            "deploy", "server", "application", "framework", "laravel", "php",
            "example", "usage", "method", "class", "function", "parameter"
        ]
        doc_matches = sum(1 for indicator in doc_indicators if indicator in content_lower)
        quality_score += doc_matches
        
        # Structural indicators (signs of well-structured documentation)
        structure_indicators = ["# ", "## ", "### ", "```", "**", "*", "1.", "2.", "-", "•"]
        structure_matches = sum(1 for indicator in structure_indicators if indicator in content)
        quality_score += min(structure_matches, 5)  # Cap at 5 to avoid over-weighting
        
        # Negative indicators (things that suggest this isn't documentation)
        bad_indicators = [
            "search...", "⌘k", "dashboard", "login", "sign in", "register", 
            "404", "not found", "error", "loading...", "please wait",
            "window.location", "redirect", "javascript:", "mailto:",
            "cookie", "privacy policy", "terms of service"
        ]
        bad_matches = sum(1 for indicator in bad_indicators if indicator in content_lower)
        quality_score -= bad_matches * 2
        
        # Length bonus (longer content is generally better documentation)
        if len(content) > 1000:
            quality_score += 2
        elif len(content) > 500:
            quality_score += 1
        
        # Content must have a minimum quality score to be considered valid
        min_score = 3
        is_valid = quality_score >= min_score
        
        if not is_valid:
            logger.debug(f"Content validation failed for {service}/{section}: score {quality_score} < {min_score}")
        
        return is_valid
    
    def _html_to_text(self, html_content: str) -> str:
        """
        Convert HTML to Markdown using markdownify.
        """
        try:
            from markdownify import markdownify as md
            from bs4 import BeautifulSoup
        except ImportError:
            logger.error("markdownify not installed. Please install it with: pip install markdownify")
            # Fallback to basic conversion
            return re.sub(r'<[^>]+>', '', html_content)
        
        # Parse HTML and remove script and style elements completely
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove all script and style tags and their contents
        for tag in soup(['script', 'style']):
            tag.decompose()
        
        # Get the cleaned HTML
        cleaned_html = str(soup)
        
        # Convert HTML to Markdown with specific options
        markdown = md(
            cleaned_html,
            strip=['nav', 'header', 'footer', 'aside', 'meta', 'link'],
            heading_style='ATX',  # Use # style headings
            bullets='-',  # Use - for unordered lists
            code_language='',  # Don't assume code language
            escape_asterisks=False,  # Don't escape asterisks
            escape_underscores=False,  # Don't escape underscores
            escape_misc=False,  # Don't escape other special chars
            autolinks=True,  # Convert URLs to links automatically
        )
        
        # Post-process to handle CloudFlare email protection links
        # Replace all email protection links with placeholder
        # In practice, these are always used for email addresses, not navigation
        # Note: markdownify escapes @ as \@, creating patterns like [[email protected]]
        markdown = re.sub(
            r'\[+[^\]]*\]+\(/cdn-cgi/l/email-protection[^)]*\)',
            '[email protected]',
            markdown
        )
        
        # Remove any remaining inline JavaScript patterns
        markdown = re.sub(r'\(self\.__next_s=self\.__next_s\|\|\[\]\)\.push[^\n]+', '', markdown)
        markdown = re.sub(r'\(function\s+[a-zA-Z]\([^)]*\)\s*\{[^}]+\}\)[^\n]*', '', markdown)
        
        # Remove CSS blocks that might have been left
        markdown = re.sub(r'h1,\s*h2,\s*h3,\s*h4\s*\{[^}]+\}', '', markdown)
        markdown = re.sub(r'\.[a-zA-Z0-9-]+\s*\{[^}]+\}', '', markdown)
        markdown = re.sub(r'#[a-zA-Z0-9-]+\s*>\s*[^{]+\{[^}]+\}', '', markdown)
        
        # Clean up excessive newlines
        markdown = re.sub(r'\n\s*\n\s*\n', '\n\n', markdown)

        # Remove social media links
        markdown = remove_social_media_lines(markdown)

        # Remove image references
        markdown = remove_image_references(markdown)

        return markdown.strip()

    def fetch_all_services(self, force: bool = False) -> Dict[str, bool]:
        """
        Fetch documentation for all configured Laravel services.
        
        Args:
            force: Force refresh even if cache is valid
            
        Returns:
            Dictionary mapping service names to success status
        """
        results = {}
        
        for service in self.laravel_services.keys():
            if force or not self.is_cache_valid(service):
                results[service] = self.fetch_laravel_service_docs(service)
            else:
                results[service] = True
                logger.debug(f"Skipping {service} (cache valid)")
        
        return results
    
    def list_available_services(self) -> List[str]:
        """List all available Laravel services."""
        return list(self.laravel_services.keys())
    
    def get_service_info(self, service: str) -> Optional[Dict]:
        """Get information about a specific service."""
        return self.laravel_services.get(service)
    
    def _retry_request(self, url: str, headers: Optional[Dict] = None, max_retries: Optional[int] = None) -> bytes:
        """
        Make a request with retry logic and exponential backoff.
        
        Args:
            url: URL to request
            headers: Optional headers to include
            max_retries: Override default max_retries
            
        Returns:
            Response content as bytes
            
        Raises:
            urllib.error.URLError: If all retry attempts fail
        """
        if headers is None:
            headers = {"User-Agent": USER_AGENT}
        
        retries = max_retries if max_retries is not None else self.max_retries
        last_exception: Optional[Union[urllib.error.HTTPError, urllib.error.URLError, Exception]] = None
        
        for attempt in range(retries + 1):
            try:
                request = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(request) as response:
                    return response.read()
            except urllib.error.HTTPError as e:
                last_exception = e
                if e.code == 404:
                    # Don't retry 404 errors
                    raise
                elif e.code == 403 and "rate limit" in str(e.reason).lower():
                    # For rate limiting, wait longer
                    wait_time = min(300, (2 ** attempt) * 5 + random.uniform(0, 5))
                    logger.warning(f"Rate limited on attempt {attempt + 1}/{retries + 1}, waiting {wait_time:.1f}s")
                    time.sleep(wait_time)
                elif e.code >= 500:
                    # Server errors are worth retrying
                    if attempt < retries:
                        wait_time = min(60, (2 ** attempt) + random.uniform(0, 2))
                        logger.warning(f"Server error {e.code} on attempt {attempt + 1}/{retries + 1}, retrying in {wait_time:.1f}s")
                        time.sleep(wait_time)
                    else:
                        raise
                else:
                    # Other HTTP errors shouldn't be retried
                    raise
            except urllib.error.URLError as e:
                last_exception = e
                if attempt < retries:
                    wait_time = min(30, (2 ** attempt) + random.uniform(0, 2))
                    logger.warning(f"Network error on attempt {attempt + 1}/{retries + 1}, retrying in {wait_time:.1f}s: {str(e)}")
                    time.sleep(wait_time)
                else:
                    raise
            except Exception as e:
                last_exception = e
                if attempt < retries:
                    wait_time = min(30, (2 ** attempt) + random.uniform(0, 2))
                    logger.warning(f"Unexpected error on attempt {attempt + 1}/{retries + 1}, retrying in {wait_time:.1f}s: {str(e)}")
                    time.sleep(wait_time)
                else:
                    raise
        
        # This should never be reached, but just in case
        if last_exception:
            raise last_exception
        else:
            raise RuntimeError(f"Failed to fetch {url} after {retries + 1} attempts")

class DocsUpdater:
    """Handles downloading and updating Laravel documentation from GitHub."""
    
    def __init__(self, target_dir: Path, version: str = DEFAULT_VERSION):
        """
        Initialize the documentation updater.
        
        Args:
            target_dir: Directory where docs should be stored
            version: Laravel version branch to pull documentation from (e.g., "12.x")
        """
        self.target_dir = target_dir
        self.version = version
        self.github_api_url = GITHUB_API_URL
        self.repo = LARAVEL_DOCS_REPO
        
        # Create version-specific directory
        self.version_dir = target_dir / version
        self.version_dir.mkdir(parents=True, exist_ok=True)
        
        # Create metadata directory if it doesn't exist
        self.metadata_dir = self.version_dir / ".metadata"
        self.metadata_dir.mkdir(exist_ok=True)
        self.metadata_file = self.metadata_dir / "sync_info.json"
    
    def get_latest_commit(self, max_retries: int = 3) -> Dict[str, str]:
        """Get information about the latest commit on the specified branch."""
        logger.debug(f"Getting latest commit info for {self.repo} on branch {self.version}")
        
        url = f"{self.github_api_url}/repos/{self.repo}/branches/{self.version}"
        
        last_exception: Optional[Exception] = None
        for attempt in range(max_retries + 1):
            try:
                request = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": USER_AGENT,
                        "Accept": "application/vnd.github.v3+json"
                    }
                )
                
                with urllib.request.urlopen(request) as response:
                    data = json.loads(response.read().decode())
                    return {
                        "sha": data["commit"]["sha"],
                        "date": data["commit"]["commit"]["committer"]["date"],
                        "message": data["commit"]["commit"]["message"],
                        "url": data["commit"]["html_url"]
                    }
            except urllib.error.HTTPError as e:
                last_exception = e
                if e.code == 403 and "rate limit" in str(e.reason).lower():
                    if attempt < max_retries:
                        wait_time = min(300, (2 ** attempt) * 30)
                        logger.warning(f"GitHub API rate limit exceeded on attempt {attempt + 1}/{max_retries + 1}, waiting {wait_time}s")
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.error("GitHub API rate limit exceeded. Try again later.")
                        raise
                elif e.code == 404:
                    logger.error(f"Branch {self.version} not found in repository {self.repo}")
                    raise
                else:
                    if attempt < max_retries and e.code >= 500:
                        wait_time = min(60, (2 ** attempt) + random.uniform(0, 2))
                        logger.warning(f"GitHub API error {e.code} on attempt {attempt + 1}/{max_retries + 1}, retrying in {wait_time:.1f}s")
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.error(f"HTTP error {e.code}: {e.reason}")
                        raise
            except Exception as e:
                last_exception = e
                if attempt < max_retries:
                    wait_time = min(30, (2 ** attempt) + random.uniform(0, 2))
                    logger.warning(f"Error fetching commit info on attempt {attempt + 1}/{max_retries + 1}, retrying in {wait_time:.1f}s: {str(e)}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Error fetching latest commit info: {str(e)}")
                    raise
        
        # This should never be reached, but just in case
        if last_exception:
            raise last_exception
        else:
            raise RuntimeError(f"Failed to get latest commit after {max_retries + 1} attempts")
    
    def read_local_metadata(self) -> Dict:
        """Read local metadata about the last sync."""
        if not self.metadata_file.exists():
            return {}
        
        try:
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Error reading metadata file: {str(e)}")
            return {}
    
    def write_local_metadata(self, data: Dict) -> None:
        """Write local metadata about the current sync."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error writing metadata file: {str(e)}")
    
    def download_documentation(self) -> Path:
        """
        Download the Laravel documentation as a zip file.
        
        Returns:
            Path to the downloaded and extracted documentation directory
        """
        logger.info(f"Downloading documentation for Laravel {self.version}")
        
        # GitHub archive URL for the specific branch
        archive_url = f"https://github.com/{self.repo}/archive/refs/heads/{self.version}.zip"
        
        # Create a temporary directory (persists after function exits)
        # Note: Using mkdtemp instead of TemporaryDirectory for Python 3.9 compatibility
        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir)

        try:
            zip_path = temp_path / "laravel_docs.zip"

            # Download the zip file
            logger.debug(f"Downloading from {archive_url}")

            # Retry mechanism for downloading
            max_retries = 3

            for attempt in range(max_retries + 1):
                try:
                    request = urllib.request.Request(
                        archive_url,
                        headers={"User-Agent": USER_AGENT}
                    )

                    with urllib.request.urlopen(request) as response, open(zip_path, 'wb') as out_file:
                        shutil.copyfileobj(response, out_file)
                    break  # Success, exit retry loop
                except Exception as e:
                    if attempt < max_retries:
                        wait_time = min(30, (2 ** attempt) + random.uniform(0, 2))
                        logger.warning(f"Download failed on attempt {attempt + 1}/{max_retries + 1}, retrying in {wait_time:.1f}s: {str(e)}")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Failed to download after {max_retries + 1} attempts: {str(e)}")
                        raise

            # Extract the zip file
            logger.debug(f"Extracting archive to {temp_path}")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_path)

            # Find the extracted directory (should be named like "docs-12.x")
            extracted_dirs = [d for d in temp_path.iterdir() if d.is_dir() and (d.name.startswith(f"{self.repo.split('/')[-1]}-"))]

            if not extracted_dirs:
                raise FileNotFoundError("Could not find extracted documentation directory")

            extracted_dir = extracted_dirs[0]
            logger.debug(f"Found extracted directory: {extracted_dir}")

            # Return the directory containing markdown files
            return extracted_dir
        except Exception as e:
            logger.error(f"Error downloading documentation: {str(e)}")
            raise
    
    def needs_update(self) -> bool:
        """Check if documentation needs to be updated based on remote commits."""
        try:
            # Get the latest commit info
            latest_commit = self.get_latest_commit()
            
            # Get local metadata
            local_meta = self.read_local_metadata()
            
            # Check if we already have the latest version
            if local_meta.get("version") == self.version and local_meta.get("commit_sha") == latest_commit["sha"]:
                logger.debug("Documentation is already up to date.")
                return False
            
            # If we reach here, an update is needed
            return True
        except Exception as e:
            logger.error(f"Error checking for updates: {str(e)}")
            logger.info("Assuming update is needed due to error")
            return True
    
    def update(self, force: bool = False) -> bool:
        """
        Update the documentation if needed or if forced.
        
        Args:
            force: Force update even if already up to date
            
        Returns:
            True if update was performed, False otherwise
        """
        if not force and not self.needs_update():
            return False
        
        try:
            # Get the latest commit info for metadata
            latest_commit = self.get_latest_commit()
            
            # Download the documentation
            source_dir = self.download_documentation()
            
            # Clear the version directory (except .metadata)
            for item in self.version_dir.iterdir():
                if item.name != ".metadata":
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
            
            # Copy files to the version directory
            for item in source_dir.iterdir():
                if item.is_dir():
                    shutil.copytree(item, self.version_dir / item.name)
                else:
                    shutil.copy2(item, self.version_dir / item.name)
            
            # Update metadata
            metadata = {
                "version": self.version,
                "commit_sha": latest_commit["sha"],
                "commit_date": latest_commit["date"],
                "commit_message": latest_commit["message"],
                "commit_url": latest_commit["url"],
                "sync_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            self.write_local_metadata(metadata)

            shutil.rmtree(source_dir.parent)  # Remove the temporary directory
            logger.debug(f"Removed temporary directory: {source_dir.parent}")
            
            logger.info(f"Documentation updated successfully to {self.version} ({latest_commit['sha'][:7]})")
            return True
        except Exception as e:
            logger.error(f"Error updating documentation: {str(e)}")
            raise


class CommunityPackageFetcher:
    """Handles fetching documentation from community Laravel packages."""
    
    def __init__(self, target_dir: Path, cache_duration: int = 86400, max_retries: int = 3):
        """
        Initialize the community package documentation fetcher.
        
        Args:
            target_dir: Directory where package docs should be stored
            cache_duration: Cache duration in seconds (default: 24 hours)
            max_retries: Maximum number of retry attempts for failed requests
        """
        self.target_dir = target_dir
        self.cache_duration = cache_duration
        self.max_retries = max_retries
        self.packages_dir = target_dir / "packages"
        self.packages_dir.mkdir(parents=True, exist_ok=True)
        
        # Community packages documentation sources
        self.community_packages = {
            "spatie": {
                "name": "Spatie Packages",
                "type": DocumentationSourceType.COMMUNITY_PACKAGE,
                "base_url": "https://spatie.be/docs",
                "packages": {
                    "laravel-permission": {
                        "name": "Laravel Permission",
                        "docs_url": "https://spatie.be/docs/laravel-permission/v6/introduction",
                        "version_pattern": r'/v(\d+)/',
                        "sections": [
                            "introduction", "installation-laravel", "basic-usage/basic-usage",
                            "basic-usage/role-permissions", "basic-usage/direct-permissions",
                            "basic-usage/multiple-guards", "basic-usage/teams-permissions",
                            "basic-usage/blade-directives", "basic-usage/artisan",
                            "basic-usage/middleware", "basic-usage/wildcard-permissions",
                            "advanced-usage/cache", "advanced-usage/extending",
                            "advanced-usage/exceptions", "advanced-usage/seeding",
                            "advanced-usage/testing", "api/models", "api/traits"
                        ]
                    },
                    "laravel-medialibrary": {
                        "name": "Laravel Media Library",
                        "docs_url": "https://spatie.be/docs/laravel-medialibrary/v11/introduction",
                        "version_pattern": r'/v(\d+)/',
                        "sections": [
                            "introduction", "installation-setup", "basic-usage/associating-files",
                            "basic-usage/retrieving-media", "converting-images/defining-conversions",
                            "converting-images/retrieving-converted-images", "responsive-images",
                            "downloading-media/downloading-a-single-file", "advanced-usage/using-s3"
                        ]
                    },
                    "laravel-backup": {
                        "name": "Laravel Backup",
                        "docs_url": "https://spatie.be/docs/laravel-backup/v9/introduction",
                        "version_pattern": r'/v(\d+)/',
                        "sections": [
                            "introduction", "installation-and-setup", "backing-up/overview",
                            "backing-up/events", "cleaning-up-old-backups/overview",
                            "sending-notifications/overview", "monitoring-health/overview"
                        ]
                    }
                }
            },
            "livewire": {
                "name": "Livewire",
                "type": DocumentationSourceType.COMMUNITY_PACKAGE,
                "base_url": "https://livewire.laravel.com/docs",
                "sections": [
                    "quickstart", "installation", "components", "properties", "actions",
                    "forms", "lifecycle-hooks", "nesting", "events", "security",
                    "uploads", "downloads", "validation", "pagination",
                    "redirecting", "wire-model", "wire-click", "wire-submit", 
                    "wire-loading", "wire-transition", "wire-poll", "wire-init", 
                    "wire-dirty", "wire-offline", "alpine", "morphing", "teleport",
                    "lazy", "locked", "computed-properties", "url", "navigate", 
                    "offline", "testing", "troubleshooting", "javascript"
                ]
            },
            "inertia": {
                "name": "Inertia.js",
                "type": DocumentationSourceType.GITHUB_REPO,
                "repo": "inertiajs/inertiajs.com",
                "branch": "master",
                "docs_path": "resources/js/Pages",
                "sections": [
                    "how-it-works", "who-is-it-for", "the-protocol",
                    "server-side-setup", "client-side-setup", "pages", "responses", 
                    "redirects", "routing", "title-and-meta", "links", "manual-visits", 
                    "forms", "file-uploads", "validation", "shared-data", "partial-reloads", 
                    "scroll-management", "authentication", "authorization", "csrf-protection",
                    "error-handling", "asset-versioning", "progress-indicators",
                    "remembering-state", "server-side-rendering", "testing"
                ]
            },
            "filament": {
                "name": "Filament",
                "type": DocumentationSourceType.COMMUNITY_PACKAGE,
                "base_url": "https://filamentphp.com/docs",
                "version": "3.x",
                "sections": [
                    "panels/installation", "panels/configuration", "panels/resources/getting-started",
                    "panels/resources/listing-records", "panels/resources/creating-records",
                    "panels/resources/editing-records", "panels/resources/viewing-records",
                    "panels/resources/deleting-records", "panels/resources/custom-pages",
                    "panels/resources/relation-managers", "panels/resources/widgets",
                    "panels/pages", "panels/dashboard", "panels/navigation",
                    "panels/users", "panels/tenancy", "panels/plugins",
                    "forms/fields/getting-started", "forms/fields/text-input",
                    "forms/fields/select", "forms/fields/checkbox", "forms/fields/toggle",
                    "forms/fields/radio", "forms/fields/date-time-picker",
                    "forms/fields/file-upload", "forms/fields/rich-editor",
                    "forms/fields/markdown-editor", "forms/fields/repeater",
                    "forms/fields/builder", "forms/fields/tags-input",
                    "forms/fields/textarea", "forms/fields/key-value",
                    "forms/fields/color-picker", "forms/fields/hidden",
                    "forms/fields/placeholder", "forms/fields/fieldset",
                    "forms/layout/getting-started", "forms/layout/grid",
                    "forms/layout/tabs", "forms/layout/wizard",
                    "forms/validation", "forms/advanced",
                    "tables/columns/getting-started", "tables/columns/text",
                    "tables/columns/icon", "tables/columns/image", "tables/columns/badge",
                    "tables/columns/tags", "tables/columns/toggle",
                    "tables/filters", "tables/actions", "tables/bulk-actions",
                    "tables/summaries", "tables/grouping", "tables/advanced",
                    "actions/overview", "actions/prebuilt-actions", "actions/modals",
                    "notifications/overview", "notifications/sending-notifications",
                    "notifications/database-notifications", "widgets/overview"
                ]
            },
            "debugbar": {
                "name": "Laravel Debugbar",
                "type": DocumentationSourceType.COMMUNITY_PACKAGE,
                "base_url": "https://laraveldebugbar.com",
                "sections": [
                    "installation", "usage", "features", "collectors"
                ]
            },
            "ide-helper": {
                "name": "Laravel IDE Helper",
                "type": DocumentationSourceType.GITHUB_REPO,
                "repo": "barryvdh/laravel-ide-helper",
                "branch": "master",
                "file": "README.md"
            }
        }
    
    def get_package_cache_path(self, package: str, subpackage: Optional[str] = None) -> Path:
        """Get the cache directory path for a package."""
        if subpackage:
            package_dir = self.packages_dir / package / subpackage
        else:
            package_dir = self.packages_dir / package
        package_dir.mkdir(parents=True, exist_ok=True)
        return package_dir
    
    def get_cache_metadata_path(self, package: str, subpackage: Optional[str] = None) -> Path:
        """Get the cache metadata file path for a package."""
        cache_dir = self.get_package_cache_path(package, subpackage)
        return cache_dir / ".metadata" / "cache.json"
    
    def is_cache_valid(self, package: str, subpackage: Optional[str] = None) -> bool:
        """Check if the cache for a package is still valid."""
        metadata_path = self.get_cache_metadata_path(package, subpackage)
        
        if not metadata_path.exists():
            return False
        
        try:
            # Use file modification time instead of stored cache_time
            cache_time = metadata_path.stat().st_mtime
            current_time = time.time()
            
            if current_time - cache_time > self.cache_duration:
                logger.debug(f"Cache expired for {package}/{subpackage or 'all'}")
                return False
            
            return True
        except Exception as e:
            logger.warning(f"Error reading cache metadata for {package}: {str(e)}")
            return False
    
    def fetch_package_docs(self, package: str, force: bool = False) -> bool:
        """
        Fetch documentation for a community package.
        
        Args:
            package: Package name (spatie, livewire, inertia, filament)
            force: Force refresh even if cache is valid
            
        Returns:
            True if successful, False otherwise
        """
        if package not in self.community_packages:
            logger.error(f"Unknown package: {package}")
            return False
        
        # Check cache validity
        if not force and self.is_cache_valid(package):
            logger.info(f"Using cached documentation for {package}")
            return True
        
        logger.info(f"Fetching documentation for {package}")
        package_config = self.community_packages[package]
        
        try:
            if package == "spatie":
                return self._fetch_spatie_docs(package_config)
            elif package == "livewire":
                return self._fetch_livewire_docs(package_config)
            elif package == "inertia":
                return self._fetch_inertia_docs(package_config)
            elif package == "filament":
                return self._fetch_filament_docs(package_config)
            elif package == "debugbar":
                return self._fetch_debugbar_docs(package_config)
            elif package == "ide-helper":
                return self._fetch_ide_helper_docs(package_config)
            else:
                logger.error(f"No fetch method implemented for package: {package}")
                return False
        except Exception as e:
            logger.error(f"Error fetching {package} documentation: {str(e)}")
            return False
    
    def _fetch_spatie_docs(self, config: Dict) -> bool:
        """Fetch documentation for Spatie packages."""
        success_count = 0
        packages = config.get("packages", {})
        
        for package_key, package_info in packages.items():
            try:
                logger.info(f"Fetching Spatie {package_info['name']} documentation")
                package_dir = self.get_package_cache_path("spatie", package_key)
                
                base_url = package_info["docs_url"].rsplit('/', 1)[0]
                sections = package_info.get("sections", [])
                
                fetched_sections = 0
                for section in sections:
                    section_url = f"{base_url}/{section}"
                    content = self._fetch_and_process_content(section_url, "spatie", section)
                    
                    if content:
                        # Save the processed content
                        file_path = package_dir / f"{section.replace('/', '-')}.md"
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        fetched_sections += 1
                
                if fetched_sections > 0:
                    # Update cache metadata
                    metadata = {
                        "package": package_key,
                        "name": package_info['name'],
                        "sections_count": fetched_sections,
                        "base_url": base_url
                    }
                    
                    metadata_path = self.get_cache_metadata_path("spatie", package_key)
                    metadata_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(metadata_path, 'w') as f:
                        json.dump(metadata, f, indent=2)
                    
                    success_count += 1
                    logger.info(f"Successfully fetched {fetched_sections} sections for Spatie {package_info['name']}")
                
            except Exception as e:
                logger.error(f"Error fetching Spatie {package_key} documentation: {str(e)}")
        
        return success_count > 0
    
    def _fetch_livewire_docs(self, config: Dict) -> bool:
        """Fetch Livewire documentation."""
        base_url = config["base_url"]
        sections = config.get("sections", [])
        package_dir = self.get_package_cache_path("livewire")
        
        fetched_sections = 0
        for section in sections:
            try:
                section_url = f"{base_url}/{section}"
                content = self._fetch_and_process_content(section_url, "livewire", section)
                
                if content:
                    file_path = package_dir / f"{section}.md"
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    fetched_sections += 1
            except Exception as e:
                logger.warning(f"Error fetching Livewire section {section}: {str(e)}")
        
        if fetched_sections > 0:
            # Update cache metadata
            metadata = {
                "package": "livewire",
                "name": config['name'],
                "sections_count": fetched_sections,
                "base_url": base_url
            }
            
            metadata_path = self.get_cache_metadata_path("livewire")
            metadata_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Successfully fetched {fetched_sections} sections for Livewire")
            return True
        
        return False
    
    def _fetch_inertia_docs(self, config: Dict) -> bool:
        """Fetch Inertia.js documentation from GitHub repository."""
        repo = config["repo"]
        branch = config["branch"]
        docs_path = config["docs_path"]
        sections = config.get("sections", [])
        package_dir = self.get_package_cache_path("inertia")
        
        fetched_sections = 0
        for section in sections:
            try:
                # Map section names to JSX file names
                jsx_filename = f"{section}.jsx"
                github_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{docs_path}/{jsx_filename}"
                
                logger.debug(f"Fetching {section} from {github_url}")
                
                request = urllib.request.Request(
                    github_url,
                    headers={"User-Agent": "Laravel-MCP-Companion/1.0"}
                )
                
                with urllib.request.urlopen(request) as response:
                    jsx_content = response.read().decode('utf-8')
                
                # Extract content from JSX file and convert to markdown
                markdown_content = self._process_jsx_to_markdown(jsx_content, section)
                
                if markdown_content:
                    file_path = package_dir / f"{section}.md"
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"# Inertia - {section.replace('-', ' ').title()}\n\n")
                        f.write(f"Source: https://inertiajs.com/{section}\n\n")
                        f.write(markdown_content)
                    
                    fetched_sections += 1
                    logger.debug(f"Successfully processed {section}")
                else:
                    logger.warning(f"No content extracted from {section}")
                    
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    logger.warning(f"Inertia section {section} not found (404)")
                else:
                    logger.warning(f"HTTP error fetching Inertia section {section}: {e}")
            except Exception as e:
                logger.warning(f"Error fetching Inertia section {section}: {str(e)}")
        
        if fetched_sections > 0:
            # Update cache metadata
            metadata = {
                "package": "inertia",
                "name": config['name'],
                "sections_count": fetched_sections,
                "source_type": "github_repo",
                "repo": repo,
                "branch": branch,
                "docs_path": docs_path
            }
            
            metadata_path = self.get_cache_metadata_path("inertia")
            metadata_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Successfully fetched {fetched_sections} sections for Inertia.js from GitHub")
            return True
        
        return False
    
    def _process_jsx_to_markdown(self, jsx_content: str, section: str) -> Optional[str]:
        """
        Process JSX content and extract documentation text to markdown.
        
        Args:
            jsx_content: Raw JSX file content
            section: Section name for context
            
        Returns:
            Extracted markdown content or None if no content found
        """
        try:
            import re
            
            # Remove import statements and React component structure
            content = jsx_content
            
            # Remove imports
            content = re.sub(r'^import\s+.*?from\s+.*?[;\n]', '', content, flags=re.MULTILINE)
            
            # Remove export statements
            content = re.sub(r'^export\s+.*?[;\n]', '', content, flags=re.MULTILINE)
            
            # Extract text content from JSX elements
            text_content = []
            
            # Extract headings (both standard and custom components)
            heading_patterns = [
                r'<[Hh]([1-6])[^>]*>(.*?)</[Hh][1-6]>',  # Standard h1-h6
                r'<H([1-6])[^>]*>(.*?)</H[1-6]>',         # Custom H1-H6 components
            ]
            
            for pattern in heading_patterns:
                headings = re.findall(pattern, content, re.DOTALL)
                for level, text in headings:
                    clean_text = self._clean_jsx_text(text)
                    if clean_text.strip():
                        text_content.append(f"{'#' * int(level)} {clean_text}\n")
            
            # Extract paragraphs (both standard and custom components)
            paragraph_patterns = [
                r'<[Pp][^>]*>(.*?)</[Pp]>',  # Standard p tags
                r'<P[^>]*>(.*?)</P>',        # Custom P components
            ]
            
            for pattern in paragraph_patterns:
                paragraphs = re.findall(pattern, content, re.DOTALL)
                for para in paragraphs:
                    clean_text = self._clean_jsx_text(para)
                    if clean_text.strip():
                        text_content.append(f"{clean_text}\n")
            
            # Extract code blocks (both standard and custom components)
            code_patterns = [
                r'<pre[^>]*><code[^>]*>(.*?)</code></pre>',  # Standard code blocks
                r'<Code[^>]*>(.*?)</Code>',                   # Custom Code components
                r'<code[^>]*>(.*?)</code>',                   # Inline code
            ]
            
            for pattern in code_patterns:
                code_blocks = re.findall(pattern, content, re.DOTALL)
                for code in code_blocks:
                    clean_code = self._clean_jsx_text(code)
                    if clean_code.strip():
                        if '\n' in clean_code:
                            text_content.append(f"```\n{clean_code}\n```\n")
                        else:
                            text_content.append(f"`{clean_code}`")
            
            # Extract list items
            list_items = re.findall(r'<li[^>]*>(.*?)</li>', content, re.DOTALL)
            for item in list_items:
                clean_text = self._clean_jsx_text(item)
                if clean_text.strip():
                    text_content.append(f"- {clean_text}")
            
            # Extract strong/bold text
            strong_patterns = [
                r'<strong[^>]*>(.*?)</strong>',
                r'<Strong[^>]*>(.*?)</Strong>',
                r'<b[^>]*>(.*?)</b>',
            ]
            
            for pattern in strong_patterns:
                strong_texts = re.findall(pattern, content, re.DOTALL)
                for text in strong_texts:
                    clean_text = self._clean_jsx_text(text)
                    if clean_text.strip():
                        text_content.append(f"**{clean_text}**")
            
            # Extract links
            link_patterns = [
                r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>',
                r'<A[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</A>',
            ]
            
            for pattern in link_patterns:
                links = re.findall(pattern, content, re.DOTALL)
                for href, link_text in links:
                    clean_text = self._clean_jsx_text(link_text)
                    if clean_text.strip():
                        text_content.append(f"[{clean_text}]({href})")
            
            # Extract any remaining text content from string literals (but exclude JSX markup)
            # Look for strings that appear to be documentation content
            string_content = re.findall(r'["`\']([^"`\']{30,})["`\']', content)
            for text in string_content:
                # Skip if it looks like code, imports, JSX, or other non-documentation content
                if not any(pattern in text.lower() for pattern in [
                    'import', 'export', 'from', 'require', 'function', 'const', 'let', 'var', 
                    '===', '!==', '=>', 'return', 'props', 'component', '</', '/>', 'jsx', 'react'
                ]):
                    clean_text = text.strip()
                    if clean_text and len(clean_text.split()) > 5:  # At least 5 words
                        # Don't add if it's already covered by component extraction
                        if not any(clean_text in existing for existing in text_content):
                            text_content.append(f"{clean_text}\n")
            
            if text_content:
                # Remove duplicates while preserving order
                seen = set()
                unique_content = []
                for item in text_content:
                    item_clean = item.strip()
                    if item_clean and item_clean not in seen:
                        # Skip if it looks like JSX remnants
                        if not any(jsx_marker in item_clean for jsx_marker in ['<', '>', '{', '}', 'return (', '=>', 'export default']):
                            seen.add(item_clean)
                            unique_content.append(item)
                
                return '\n'.join(unique_content)
            else:
                logger.debug(f"No extractable content found in {section} JSX file")
                return None
                
        except Exception as e:
            logger.warning(f"Error processing JSX content for {section}: {str(e)}")
            return None
    
    def _clean_jsx_text(self, text: str) -> str:
        """Clean JSX text content of React syntax and HTML entities."""
        import re
        
        # Remove JSX curly braces and expressions
        text = re.sub(r'\{[^}]*\}', '', text)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]*>', '', text)
        
        # Decode HTML entities
        text = html.unescape(text)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def _fetch_filament_docs(self, config: Dict) -> bool:
        """Fetch Filament documentation."""
        base_url = config["base_url"]
        version = config.get("version", "3.x")
        sections = config.get("sections", [])
        package_dir = self.get_package_cache_path("filament")
        
        fetched_sections = 0
        for section in sections:
            try:
                section_url = f"{base_url}/{version}/{section}"
                content = self._fetch_and_process_content(section_url, "filament", section)
                
                if content:
                    file_path = package_dir / f"{section.replace('/', '-')}.md"
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    fetched_sections += 1
            except Exception as e:
                logger.warning(f"Error fetching Filament section {section}: {str(e)}")
        
        if fetched_sections > 0:
            # Update cache metadata
            metadata = {
                "package": "filament",
                "name": config['name'],
                "version": version,
                "sections_count": fetched_sections,
                "base_url": base_url
            }
            
            metadata_path = self.get_cache_metadata_path("filament")
            metadata_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Successfully fetched {fetched_sections} sections for Filament")
            return True
        
        return False
    
    def _fetch_debugbar_docs(self, config: Dict) -> bool:
        """Fetch Laravel Debugbar documentation from website."""
        base_url = config["base_url"]
        sections = config.get("sections", [])
        package_dir = self.get_package_cache_path("debugbar")
        
        fetched_sections = 0
        for section in sections:
            try:
                section_url = f"{base_url}/{section}/"
                content = self._fetch_and_process_content(section_url, "debugbar", section)
                
                if content:
                    file_path = package_dir / f"{section}.md"
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    fetched_sections += 1
            except Exception as e:
                logger.warning(f"Error fetching Debugbar section {section}: {str(e)}")
        
        if fetched_sections > 0:
            # Update cache metadata
            metadata = {
                "package": "debugbar",
                "name": config['name'],
                "sections_count": fetched_sections,
                "base_url": base_url
            }
            
            metadata_path = self.get_cache_metadata_path("debugbar")
            metadata_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Successfully fetched {fetched_sections} sections for Laravel Debugbar")
            return True
        
        return False
    
    def _fetch_ide_helper_docs(self, config: Dict) -> bool:
        """Fetch Laravel IDE Helper documentation from GitHub README."""
        repo = config["repo"]
        branch = config.get("branch", "master")
        file = config.get("file", "README.md")
        package_dir = self.get_package_cache_path("ide-helper")
        
        try:
            # Fetch README from GitHub
            github_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{file}"
            
            logger.info(f"Fetching IDE Helper documentation from {github_url}")
            
            request = urllib.request.Request(
                github_url,
                headers={"User-Agent": USER_AGENT}
            )
            
            with urllib.request.urlopen(request) as response:
                content = response.read().decode('utf-8')
            
            # Process the README content
            if content:
                # Add header
                header = f"# {config['name']}\n\n"
                header += f"Source: https://github.com/{repo}\n\n"
                header += "---\n\n"
                
                # Save the processed content
                file_path = package_dir / "readme.md"
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(header + content)
                
                # Update cache metadata
                metadata = {
                    "package": "ide-helper",
                    "name": config['name'],
                    "source_type": "github_readme",
                    "repo": repo,
                    "branch": branch,
                    "file": file
                }
                
                metadata_path = self.get_cache_metadata_path("ide-helper")
                metadata_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                logger.info("Successfully fetched documentation for Laravel IDE Helper")
                return True
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                logger.error(f"IDE Helper README not found at {github_url}")
            else:
                logger.error(f"HTTP error fetching IDE Helper documentation: {e}")
        except Exception as e:
            logger.error(f"Error fetching IDE Helper documentation: {str(e)}")
        
        return False
    
    def _fetch_and_process_content(self, url: str, package: str, section: str) -> Optional[str]:
        """Fetch and process content from a URL."""
        try:
            # Use markdownify for HTML to Markdown conversion
            from markdownify import markdownify as md
            from bs4 import BeautifulSoup
            
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/html,application/xhtml+xml"
                }
            )
            
            with urllib.request.urlopen(request, timeout=30) as response:
                content_bytes = response.read()
                content = content_bytes.decode('utf-8')
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove navigation, header, footer elements
            for tag in soup.find_all(['nav', 'header', 'footer', 'aside']):
                tag.decompose()
            
            # Remove stats/metrics elements that contain dynamic numbers
            # For Spatie packages, remove elements that contain download counts and issue numbers
            if package == "spatie":
                # Find and remove the stats section that appears at the top of Spatie docs
                # This typically contains Repository, Open Issues, and download counts
                stats_removed = False
                
                # Look for the pattern: Repository -> Open Issues -> large numbers
                for element in soup.find_all(string=re.compile(r'^Repository$', re.I)):
                    # Find the container that holds this stats section
                    container = element.parent
                    while container and container.name not in ['body', 'html', 'main', 'article']:
                        # Check if this container has "Open Issues" and large numbers
                        text_content = container.get_text()
                        if 'Open Issues' in text_content and re.search(r'\d{3,}', text_content):
                            # This looks like the stats container
                            container.decompose()
                            stats_removed = True
                            logger.debug(f"Removed stats container from {url}")
                            break
                        # Try parent container
                        if container.parent and container.parent.name in ['div', 'section', 'aside', 'header']:
                            container = container.parent
                        else:
                            break
                    if stats_removed:
                        break
                
                # Also remove any standalone large numbers that might be stats
                for text_node in soup.find_all(string=re.compile(r'^\s*[\d,]+\s*$')):
                    if text_node.parent:
                        num_str = str(text_node).strip().replace(',', '')
                        try:
                            # Remove numbers larger than 1000 (likely stats, not code examples)
                            if num_str.isdigit() and int(num_str) > 1000:
                                # Don't remove if it's inside a code block
                                if not any(p.name in ['code', 'pre'] for p in text_node.parents):
                                    text_node.parent.extract()
                        except Exception:
                            pass
                
                # Remove any divs or sections that look like stats containers
                for tag in soup.find_all(['div', 'section'], class_=re.compile(r'stats|metrics|numbers|count', re.I)):
                    tag.decompose()
            
            # Try to find main content area
            main_content = None
            
            # Package-specific selectors
            if package == "inertia":
                # Inertia uses div with id="top" for main content
                main_content = soup.find('div', id='top')
                if not main_content:
                    logger.debug(f"Could not find #top div for Inertia on {url}")
            elif package == "filament":
                # Filament might use different selectors
                main_content = soup.select_one('.docs-content, .prose, main')
            elif package == "debugbar":
                # Debugbar documentation site selectors
                main_content = soup.select_one('.prose, .content, main, article')
            
            # If no package-specific selector worked, try common selectors
            if not main_content:
                content_selectors = [
                    '#top',  # Try #top first as it seems common
                    'main', 'article', '[role="main"]', '.content', '.docs-content',
                    '.documentation', '#content', '.prose', '.markdown-body'
                ]
                
                for selector in content_selectors:
                    main_content = soup.select_one(selector)
                    if main_content:
                        logger.debug(f"Found content using selector: {selector}")
                        break
            
            if not main_content:
                logger.warning(f"Could not find main content area for {url}, using body")
                main_content = soup.find('body') or soup
            
            # Convert to markdown
            markdown_content = md(str(main_content), strip=['a'], code_language='php')
            
            # Clean up the content
            markdown_content = self._clean_markdown_content(markdown_content)
            
            # Check if we got any actual content
            if len(markdown_content.strip()) < 50:
                logger.warning(f"Very little content extracted from {url} (len: {len(markdown_content.strip())})")
                # Log first 200 chars of HTML to debug
                html_preview = str(main_content)[:500]
                logger.debug(f"HTML preview: {html_preview}")
            
            # Add metadata header
            header = f"# {package.title()} - {section.replace('-', ' ').title()}\n\n"
            header += f"Source: {url}\n\n"
            
            return header + markdown_content
            
        except Exception as e:
            logger.error(f"Error fetching content from {url}: {str(e)}")
            return None
    
    def _clean_markdown_content(self, content: str) -> str:
        """Clean up markdown content."""
        # Remove excessive blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Fix code blocks
        content = re.sub(r'```\s*\n', '```\n', content)
        
        # Remove CloudFlare email protection links
        # Catch all CloudFlare email protection links regardless of link text
        content = re.sub(
            r'\[[^\]]*\]\(/cdn-cgi/l/email-protection[^)]*\)',
            '[email protected]',
            content
        )
        
        # Remove trailing whitespace
        content = '\n'.join(line.rstrip() for line in content.split('\n'))

        # Remove social media links
        content = remove_social_media_lines(content)

        # Remove image references
        content = remove_image_references(content)

        return content.strip()

    def list_available_packages(self) -> List[str]:
        """List all available community packages."""
        return list(self.community_packages.keys())
    
    def fetch_all_packages(self, force: bool = False) -> Dict[str, bool]:
        """
        Fetch documentation for all community packages.
        
        Args:
            force: Force refresh even if cache is valid
            
        Returns:
            Dictionary mapping package names to success status
        """
        results = {}
        
        for package in self.list_available_packages():
            logger.info(f"Processing community package: {package}")
            results[package] = self.fetch_package_docs(package, force=force)
        
        # Log summary
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        logger.info(f"Community package documentation update complete: {success_count}/{total_count} packages")
        
        return results


class MultiSourceDocsUpdater:
    """Handles updating documentation from multiple sources including core Laravel and external services."""
    
    def __init__(self, target_dir: Path, version: str = DEFAULT_VERSION):
        """
        Initialize the multi-source documentation updater.
        
        Args:
            target_dir: Directory where all docs should be stored
            version: Laravel version for core documentation
        """
        self.target_dir = target_dir
        self.version = version
        
        # Initialize core Laravel docs updater
        self.core_updater = DocsUpdater(target_dir, version)
        
        # Initialize external docs fetcher
        self.external_fetcher = ExternalDocsFetcher(target_dir)
        
        # Initialize community package fetcher
        self.package_fetcher = CommunityPackageFetcher(target_dir)

        # Initialize learning resource fetcher
        self.learning_fetcher = LearningResourceFetcher(target_dir)

    def update_core_docs(self, force: bool = False) -> bool:
        """Update core Laravel documentation."""
        logger.info("Updating core Laravel documentation")
        return self.core_updater.update(force=force)
    
    def update_external_docs(self, services: Optional[List[str]] = None, force: bool = False) -> Dict[str, bool]:
        """
        Update external Laravel services documentation.
        
        Args:
            services: List of specific services to update. If None, updates all.
            force: Force refresh even if cache is valid
            
        Returns:
            Dictionary mapping service names to success status
        """
        logger.info("Updating external Laravel services documentation")
        
        if services:
            results = {}
            for service in services:
                if service in self.external_fetcher.laravel_services:
                    results[service] = self.external_fetcher.fetch_laravel_service_docs(service)
                else:
                    logger.error(f"Unknown service: {service}")
                    results[service] = False
            return results
        else:
            return self.external_fetcher.fetch_all_services(force=force)
    
    def update_package_docs(self, packages: Optional[List[str]] = None, force: bool = False) -> Dict[str, bool]:
        """
        Update community package documentation.
        
        Args:
            packages: List of specific packages to update. If None, updates all.
            force: Force refresh even if cache is valid
            
        Returns:
            Dictionary mapping package names to success status
        """
        logger.info("Updating community package documentation")
        
        if packages:
            results = {}
            for package in packages:
                if package in self.package_fetcher.community_packages:
                    results[package] = self.package_fetcher.fetch_package_docs(package, force=force)
                else:
                    logger.error(f"Unknown package: {package}")
                    results[package] = False
            return results
        else:
            return self.package_fetcher.fetch_all_packages(force=force)

    def update_learning_docs(self, sources: Optional[List[str]] = None, force: bool = False) -> Dict[str, bool]:
        """
        Update learning resource documentation.

        Args:
            sources: List of specific sources to update. If None, updates all.
            force: Force refresh even if cache is valid

        Returns:
            Dictionary mapping source names to success status
        """
        logger.info("Updating learning resource documentation")

        if sources:
            results = {}
            for source in sources:
                if source in self.learning_fetcher.learning_sources:
                    results[source] = self.learning_fetcher.fetch_learning_source(source, force=force)
                else:
                    logger.error(f"Unknown learning source: {source}")
                    results[source] = False
            return results
        else:
            return self.learning_fetcher.fetch_all_sources(force=force)

    def update_all(self, force_core: bool = False, force_external: bool = False, force_packages: bool = False, force_learning: bool = False) -> Dict[str, object]:
        """
        Update all documentation sources.

        Args:
            force_core: Force update of core documentation
            force_external: Force update of external documentation
            force_packages: Force update of community packages
            force_learning: Force update of learning resources

        Returns:
            Dictionary with results for core, external, package, and learning updates
        """
        logger.info("Starting comprehensive documentation update")

        results: Dict[str, object] = {
            "core": False,
            "external": {},
            "packages": {},
            "learning": {}
        }

        try:
            # Update core Laravel documentation
            results["core"] = self.update_core_docs(force=force_core)

            # Update external services documentation
            results["external"] = self.update_external_docs(force=force_external)

            # Update community package documentation
            results["packages"] = self.update_package_docs(force=force_packages)

            # Update learning resource documentation
            results["learning"] = self.update_learning_docs(force=force_learning)

            # Log summary
            core_status = "updated" if results["core"] else "up-to-date"
            external_results = results["external"]
            package_results = results["packages"]
            learning_results = results["learning"]

            if isinstance(external_results, dict):
                external_count = sum(1 for success in external_results.values() if success)
                total_external = len(external_results)
            else:
                external_count = 0
                total_external = 0

            if isinstance(package_results, dict):
                package_count = sum(1 for success in package_results.values() if success)
                total_packages = len(package_results)
            else:
                package_count = 0
                total_packages = 0

            if isinstance(learning_results, dict):
                learning_count = sum(1 for success in learning_results.values() if success)
                total_learning = len(learning_results)
            else:
                learning_count = 0
                total_learning = 0

            logger.info(f"Documentation update complete: Core {core_status}, External {external_count}/{total_external}, Packages {package_count}/{total_packages}, Learning {learning_count}/{total_learning}")
            
        except Exception as e:
            logger.error(f"Error during comprehensive documentation update: {str(e)}")
        
        return results
    
    def get_all_documentation_status(self) -> Dict[str, Dict]:
        """Get status information for all documentation sources."""
        status: Dict[str, Dict] = {
            "core": {},
            "external": {},
            "packages": {},
            "learning": {}
        }
        
        # Get core documentation status
        try:
            core_metadata = self.core_updater.read_local_metadata()
            status["core"] = {
                "version": self.version,
                "available": bool(core_metadata),
                "last_updated": core_metadata.get("sync_time", "unknown"),
                "commit_sha": core_metadata.get("commit_sha", "unknown")
            }
        except Exception as e:
            status["core"] = {"error": str(e)}
        
        # Get external documentation status
        for service in self.external_fetcher.list_available_services():
            try:
                cache_valid = self.external_fetcher.is_cache_valid(service)
                service_info = self.external_fetcher.get_service_info(service)
                if service_info is None:
                    continue
                
                # Try to read cache metadata
                metadata_path = self.external_fetcher.get_cache_metadata_path(service)
                if metadata_path.exists():
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                    except Exception:
                        metadata = {}
                else:
                    metadata = {}
                
                status["external"][service] = {
                    "name": service_info.get("name", service),
                    "type": service_info.get("type", "unknown").value if hasattr(service_info.get("type"), 'value') else str(service_info.get("type", "unknown")),
                    "cache_valid": cache_valid,
                    "last_fetched": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(metadata_path.stat().st_mtime)) if metadata_path.exists() else "never",
                    "success_rate": metadata.get("success_rate", "unknown")
                }
            except Exception as e:
                status["external"][service] = {"error": str(e)}
        
        # Get community package documentation status
        for package in self.package_fetcher.list_available_packages():
            try:
                cache_valid = self.package_fetcher.is_cache_valid(package)
                package_info = self.package_fetcher.community_packages.get(package, {})
                
                # Try to read cache metadata
                metadata_path = self.package_fetcher.get_cache_metadata_path(package)
                if metadata_path.exists():
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                    except Exception:
                        metadata = {}
                else:
                    metadata = {}
                
                # Get the type value safely
                package_type = package_info.get("type", DocumentationSourceType.COMMUNITY_PACKAGE)
                if hasattr(package_type, 'value'):
                    type_value = package_type.value
                else:
                    type_value = str(package_type) if package_type else "community_package"
                
                status["packages"][package] = {
                    "name": package_info.get("name", package),
                    "type": type_value,
                    "cache_valid": cache_valid,
                    "last_fetched": metadata.get("cache_time", "never"),
                    "sections_count": metadata.get("sections_count", 0)
                }
                
                # For Spatie, include sub-packages
                if package == "spatie" and "packages" in package_info:
                    status["packages"][package]["sub_packages"] = {}
                    packages_dict = package_info.get("packages", {})
                    if isinstance(packages_dict, dict):
                        for sub_pkg, sub_info in packages_dict.items():
                            sub_metadata_path = self.package_fetcher.get_cache_metadata_path("spatie", sub_pkg)
                            if sub_metadata_path.exists():
                                try:
                                    with open(sub_metadata_path, 'r') as f:
                                        sub_metadata = json.load(f)
                                    status["packages"][package]["sub_packages"][sub_pkg] = {
                                        "name": sub_info.get("name", sub_pkg),
                                        "sections_count": sub_metadata.get("sections_count", 0)
                                    }
                                except Exception:
                                    pass
                
            except Exception as e:
                status["packages"][package] = {"error": str(e)}

        # Get learning resource documentation status
        for source in self.learning_fetcher.list_available_sources():
            try:
                cache_valid = self.learning_fetcher.is_cache_valid(source)
                source_info = self.learning_fetcher.get_source_info(source)

                if source_info is None:
                    continue

                # Try to read cache metadata
                metadata_path = self.learning_fetcher.get_cache_metadata_path(source)
                if metadata_path.exists():
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                    except Exception:
                        metadata = {}
                else:
                    metadata = {}

                status["learning"][source] = {
                    "name": source_info.get("name", source),
                    "description": source_info.get("description", ""),
                    "difficulty": source_info.get("difficulty", "mixed"),
                    "cache_valid": cache_valid,
                    "last_fetched": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(metadata.get("cached_at", 0))) if metadata.get("cached_at") else "never",
                    "success_rate": metadata.get("success_rate", "unknown")
                }
            except Exception as e:
                status["learning"][source] = {"error": str(e)}

        return status

    def needs_update(self, check_external: bool = True, check_packages: bool = True, check_learning: bool = True) -> Dict[str, Union[bool, Dict[str, bool]]]:
        """
        Check which documentation sources need updating.

        Args:
            check_external: Whether to check external services
            check_packages: Whether to check community packages
            check_learning: Whether to check learning resources

        Returns:
            Dictionary indicating which sources need updates
        """
        needs_update: Dict[str, Union[bool, Dict[str, bool]]] = {
            "core": False,
            "external": {},
            "packages": {},
            "learning": {}
        }
        
        # Check core documentation
        try:
            needs_update["core"] = self.core_updater.needs_update()
        except Exception as e:
            logger.warning(f"Error checking core documentation update status: {str(e)}")
            needs_update["core"] = True
        
        # Check external documentation
        if check_external:
            external_dict = needs_update["external"]
            if isinstance(external_dict, dict):
                for service in self.external_fetcher.list_available_services():
                    try:
                        external_dict[service] = not self.external_fetcher.is_cache_valid(service)
                    except Exception as e:
                        logger.warning(f"Error checking {service} documentation status: {str(e)}")
                        external_dict[service] = True
        
        # Check community package documentation
        if check_packages:
            packages_dict = needs_update["packages"]
            if isinstance(packages_dict, dict):
                for package in self.package_fetcher.list_available_packages():
                    try:
                        packages_dict[package] = not self.package_fetcher.is_cache_valid(package)
                    except Exception as e:
                        logger.warning(f"Error checking {package} documentation status: {str(e)}")
                        packages_dict[package] = True

        # Check learning resource documentation
        if check_learning:
            learning_dict = needs_update["learning"]
            if isinstance(learning_dict, dict):
                for source in self.learning_fetcher.list_available_sources():
                    try:
                        learning_dict[source] = not self.learning_fetcher.is_cache_valid(source)
                    except Exception as e:
                        logger.warning(f"Error checking {source} learning resource status: {str(e)}")
                        learning_dict[source] = True

        return needs_update


class LearningResourceFetcher:
    """Handles fetching documentation from learning resource sources."""

    def __init__(self, target_dir: Path, cache_duration: int = 86400, max_retries: int = 3):
        """
        Initialize the learning resource fetcher.

        Args:
            target_dir: Directory where learning resources should be stored
            cache_duration: Cache duration in seconds (default: 24 hours)
            max_retries: Maximum number of retry attempts for failed requests
        """
        self.target_dir = target_dir
        self.cache_duration = cache_duration
        self.max_retries = max_retries
        self.learning_dir = target_dir / "learning_resources"
        self.learning_dir.mkdir(parents=True, exist_ok=True)

        # Learning resource sources
        self.learning_sources = {
            "laravel-bootcamp": {
                "name": "Laravel Bootcamp",
                "type": DocumentationSourceType.DIRECT_URL,
                "base_url": "https://bootcamp.laravel.com",
                "description": "Official Laravel tutorial for beginners",
                "difficulty": "beginner",
                "sections": [
                    "introduction",
                    "installation",
                    "creating-chirps",
                    "showing-chirps",
                    "editing-chirps",
                    "deleting-chirps",
                    "notifications-and-events",
                    "deploying",
                ],
            },
            "laravel-blog": {
                "name": "Laravel Blog",
                "type": DocumentationSourceType.DIRECT_URL,
                "base_url": "https://blog.laravel.com",
                "description": "Official Laravel announcements and articles",
                "difficulty": "mixed",
                "fetch_type": "index",  # Only fetch index/list, not full articles
            },
            "laravel-news": {
                "name": "Laravel News",
                "type": DocumentationSourceType.DIRECT_URL,
                "base_url": "https://laravel-news.com",
                "description": "Community news, tutorials, and package announcements",
                "difficulty": "mixed",
                "fetch_type": "index",  # Only fetch index/summaries
            },
            "laracasts-index": {
                "name": "Laracasts Index",
                "type": DocumentationSourceType.DIRECT_URL,
                "base_url": "https://laracasts.com",
                "description": "Video tutorial metadata (respects paywall)",
                "difficulty": "mixed",
                "fetch_type": "metadata",  # Only fetch metadata, respect paywall
                "topics_url": "https://laracasts.com/topics",
            },
        }

    def get_source_cache_path(self, source: str) -> Path:
        """Get the cache directory path for a learning source."""
        source_dir = self.learning_dir / source
        source_dir.mkdir(parents=True, exist_ok=True)
        return source_dir

    def get_cache_metadata_path(self, source: str) -> Path:
        """Get the metadata file path for a learning source."""
        return self.get_source_cache_path(source) / ".cache_metadata.json"

    def is_cache_valid(self, source: str) -> bool:
        """Check if the cached learning resources for a source are still valid."""
        metadata_path = self.get_cache_metadata_path(source)

        if not metadata_path.exists():
            return False

        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

            cache_time = metadata.get('cached_at', 0)
            success_rate = metadata.get('success_rate', 0.0)

            is_fresh = (time.time() - cache_time) < self.cache_duration
            is_quality = success_rate >= 0.7  # Lower threshold for learning resources

            if not is_quality:
                logger.info(f"Cache for {source} has low success rate ({success_rate:.1%}), invalidating")
                return False

            return is_fresh
        except Exception as e:
            logger.warning(f"Error reading cache metadata for {source}: {str(e)}")
            return False

    def save_cache_metadata(self, source: str, metadata: Dict) -> None:
        """Save cache metadata for a learning source."""
        metadata_path = self.get_cache_metadata_path(source)
        metadata["cached_at"] = time.time()

        try:
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving cache metadata for {source}: {str(e)}")

    def fetch_learning_source(self, source: str, force: bool = False) -> bool:
        """
        Fetch learning resources from a specific source.

        Args:
            source: Source name (laravel-bootcamp, laravel-blog, etc.)
            force: Force refresh even if cache is valid

        Returns:
            True if successful, False otherwise
        """
        if source not in self.learning_sources:
            logger.error(f"Unknown learning source: {source}")
            return False

        if not force and self.is_cache_valid(source):
            logger.debug(f"Using cached learning resources for {source}")
            return True

        source_config = self.learning_sources[source]
        logger.info(f"Fetching learning resources from {source_config['name']}")

        try:
            if source == "laravel-bootcamp":
                return self._fetch_bootcamp_docs(source_config)
            elif source == "laravel-blog":
                return self._fetch_blog_index(source_config)
            elif source == "laravel-news":
                return self._fetch_news_index(source_config)
            elif source == "laracasts-index":
                return self._fetch_laracasts_metadata(source_config)
            else:
                logger.error(f"No fetch method implemented for source: {source}")
                return False
        except Exception as e:
            logger.error(f"Error fetching learning resources from {source}: {str(e)}")
            return False

    def _fetch_bootcamp_docs(self, config: Dict) -> bool:
        """Fetch Laravel Bootcamp documentation."""
        base_url = config["base_url"]
        sections = config.get("sections", [])
        source_dir = self.get_source_cache_path("laravel-bootcamp")

        fetched_sections = 0
        for section in sections:
            try:
                # Bootcamp uses /docs/{section} URLs
                section_url = f"{base_url}/blade/{section}" if section != "introduction" else f"{base_url}"
                content = self._fetch_and_process_html(section_url, "laravel-bootcamp", section)

                if content:
                    file_path = source_dir / f"{section}.md"
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fetched_sections += 1
                    logger.debug(f"Fetched bootcamp section: {section}")
            except Exception as e:
                logger.warning(f"Error fetching bootcamp section {section}: {str(e)}")

        if fetched_sections > 0:
            metadata = {
                "source": "laravel-bootcamp",
                "name": config['name'],
                "fetched_sections": fetched_sections,
                "total_sections": len(sections),
                "success_rate": fetched_sections / len(sections),
                "difficulty": config.get("difficulty", "beginner"),
            }
            self.save_cache_metadata("laravel-bootcamp", metadata)
            logger.info(f"Successfully fetched {fetched_sections}/{len(sections)} bootcamp sections")
            return True

        return False

    def _fetch_blog_index(self, config: Dict) -> bool:
        """Fetch Laravel Blog article index (summaries only)."""
        base_url = config["base_url"]
        source_dir = self.get_source_cache_path("laravel-blog")

        try:
            # Fetch the main blog page to get article list
            content_bytes = self._retry_request(base_url)
            content = content_bytes.decode('utf-8')

            # Extract article titles and summaries
            articles = self._extract_blog_articles(content)

            if articles:
                # Save as index file
                index_content = "# Laravel Blog - Recent Articles\n\n"
                index_content += f"Source: {base_url}\n\n"
                index_content += "---\n\n"

                for article in articles[:20]:  # Limit to 20 most recent
                    index_content += f"## {article.get('title', 'Untitled')}\n\n"
                    if article.get('date'):
                        index_content += f"*Published: {article['date']}*\n\n"
                    if article.get('summary'):
                        index_content += f"{article['summary']}\n\n"
                    if article.get('url'):
                        index_content += f"[Read more]({article['url']})\n\n"
                    index_content += "---\n\n"

                index_file = source_dir / "index.md"
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(index_content)

                metadata = {
                    "source": "laravel-blog",
                    "name": config['name'],
                    "article_count": len(articles),
                    "success_rate": 1.0,
                    "difficulty": "mixed",
                }
                self.save_cache_metadata("laravel-blog", metadata)
                logger.info(f"Successfully fetched {len(articles)} blog article summaries")
                return True

        except Exception as e:
            logger.error(f"Error fetching Laravel blog index: {str(e)}")

        return False

    def _fetch_news_index(self, config: Dict) -> bool:
        """Fetch Laravel News article index (summaries only)."""
        base_url = config["base_url"]
        source_dir = self.get_source_cache_path("laravel-news")

        try:
            content_bytes = self._retry_request(base_url)
            content = content_bytes.decode('utf-8')

            # Extract article titles and summaries
            articles = self._extract_news_articles(content)

            if articles:
                index_content = "# Laravel News - Recent Articles\n\n"
                index_content += f"Source: {base_url}\n\n"
                index_content += "---\n\n"

                for article in articles[:30]:  # Limit to 30 most recent
                    index_content += f"## {article.get('title', 'Untitled')}\n\n"
                    if article.get('category'):
                        index_content += f"*Category: {article['category']}*\n\n"
                    if article.get('summary'):
                        index_content += f"{article['summary']}\n\n"
                    if article.get('url'):
                        index_content += f"[Read more]({article['url']})\n\n"
                    index_content += "---\n\n"

                index_file = source_dir / "index.md"
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(index_content)

                metadata = {
                    "source": "laravel-news",
                    "name": config['name'],
                    "article_count": len(articles),
                    "success_rate": 1.0,
                    "difficulty": "mixed",
                }
                self.save_cache_metadata("laravel-news", metadata)
                logger.info(f"Successfully fetched {len(articles)} Laravel News article summaries")
                return True

        except Exception as e:
            logger.error(f"Error fetching Laravel News index: {str(e)}")

        return False

    def _fetch_laracasts_metadata(self, config: Dict) -> bool:
        """Fetch Laracasts topic metadata (respects paywall)."""
        topics_url = config.get("topics_url", "https://laracasts.com/topics")
        source_dir = self.get_source_cache_path("laracasts-index")

        try:
            content_bytes = self._retry_request(topics_url)
            content = content_bytes.decode('utf-8')

            # Extract topic list (publicly available)
            topics = self._extract_laracasts_topics(content)

            if topics:
                index_content = "# Laracasts - Topic Index\n\n"
                index_content += f"Source: {topics_url}\n\n"
                index_content += "*Note: Laracasts is a premium service. This index provides topic metadata only.*\n\n"
                index_content += "---\n\n"

                for topic in topics:
                    index_content += f"## {topic.get('name', 'Untitled')}\n\n"
                    if topic.get('description'):
                        index_content += f"{topic['description']}\n\n"
                    if topic.get('series_count'):
                        index_content += f"*{topic['series_count']} series available*\n\n"
                    if topic.get('url'):
                        index_content += f"[View on Laracasts]({topic['url']})\n\n"
                    index_content += "---\n\n"

                index_file = source_dir / "topics.md"
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(index_content)

                metadata = {
                    "source": "laracasts-index",
                    "name": config['name'],
                    "topic_count": len(topics),
                    "success_rate": 1.0,
                    "difficulty": "mixed",
                    "type": "metadata_only",
                }
                self.save_cache_metadata("laracasts-index", metadata)
                logger.info(f"Successfully fetched {len(topics)} Laracasts topic metadata")
                return True

        except Exception as e:
            logger.error(f"Error fetching Laracasts metadata: {str(e)}")

        return False

    def _extract_blog_articles(self, html_content: str) -> List[Dict]:
        """Extract article summaries from Laravel Blog HTML."""
        articles = []
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Look for article elements
            article_elements = soup.find_all('article') or soup.find_all('div', class_=re.compile(r'post|article|entry', re.I))

            for article in article_elements[:20]:
                article_data: Dict[str, Any] = {}

                # Find title
                title_elem = article.find(['h1', 'h2', 'h3']) or article.find('a', class_=re.compile(r'title', re.I))
                if title_elem:
                    article_data['title'] = title_elem.get_text(strip=True)

                # Find link
                link_elem = article.find('a', href=True)
                if link_elem:
                    href = str(link_elem.get('href', ''))
                    if href and not href.startswith('#'):
                        article_data['url'] = href if href.startswith('http') else f"https://blog.laravel.com{href}"

                # Find summary/excerpt
                summary_elem = article.find('p') or article.find(class_=re.compile(r'excerpt|summary|description', re.I))
                if summary_elem:
                    summary = summary_elem.get_text(strip=True)
                    if len(summary) > 20:
                        article_data['summary'] = summary[:300] + "..." if len(summary) > 300 else summary

                # Find date
                date_elem = article.find('time') or article.find(class_=re.compile(r'date|time', re.I))
                if date_elem:
                    article_data['date'] = date_elem.get_text(strip=True)

                if article_data.get('title'):
                    articles.append(article_data)

        except ImportError:
            logger.warning("BeautifulSoup not installed, skipping article extraction")
        except Exception as e:
            logger.warning(f"Error extracting blog articles: {str(e)}")

        return articles

    def _extract_news_articles(self, html_content: str) -> List[Dict]:
        """Extract article summaries from Laravel News HTML."""
        articles = []
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Look for article cards
            article_elements = soup.find_all('article') or soup.find_all('div', class_=re.compile(r'card|post|article', re.I))

            for article in article_elements[:30]:
                article_data: Dict[str, Any] = {}

                # Find title
                title_elem = article.find(['h1', 'h2', 'h3', 'h4'])
                if title_elem:
                    article_data['title'] = title_elem.get_text(strip=True)

                # Find link
                link_elem = article.find('a', href=True)
                if link_elem:
                    href = str(link_elem.get('href', ''))
                    if href and not href.startswith('#'):
                        article_data['url'] = href if href.startswith('http') else f"https://laravel-news.com{href}"

                # Find category
                category_elem = article.find(class_=re.compile(r'category|tag', re.I))
                if category_elem:
                    article_data['category'] = category_elem.get_text(strip=True)

                # Find summary
                summary_elem = article.find('p')
                if summary_elem:
                    summary = summary_elem.get_text(strip=True)
                    if len(summary) > 20:
                        article_data['summary'] = summary[:300] + "..." if len(summary) > 300 else summary

                if article_data.get('title'):
                    articles.append(article_data)

        except ImportError:
            logger.warning("BeautifulSoup not installed, skipping article extraction")
        except Exception as e:
            logger.warning(f"Error extracting news articles: {str(e)}")

        return articles

    def _extract_laracasts_topics(self, html_content: str) -> List[Dict]:
        """Extract topic metadata from Laracasts topics page."""
        topics = []
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Look for topic cards/links
            topic_elements = soup.find_all('a', href=re.compile(r'/topics/'))

            seen_topics: set = set()
            for elem in topic_elements:
                topic_data: Dict[str, Any] = {}

                href = str(elem.get('href', ''))
                if href and href not in seen_topics:
                    seen_topics.add(href)
                    topic_data['url'] = f"https://laracasts.com{href}" if not href.startswith('http') else href

                    # Extract topic name from URL or text
                    name = elem.get_text(strip=True) or href.split('/')[-1].replace('-', ' ').title()
                    if name and len(name) > 1:
                        topic_data['name'] = name

                        # Look for description in parent or sibling
                        parent = elem.parent
                        if parent:
                            desc_elem = parent.find('p') or parent.find(class_=re.compile(r'description', re.I))
                            if desc_elem:
                                topic_data['description'] = desc_elem.get_text(strip=True)[:200]

                        if topic_data.get('name'):
                            topics.append(topic_data)

        except ImportError:
            logger.warning("BeautifulSoup not installed, skipping topic extraction")
        except Exception as e:
            logger.warning(f"Error extracting Laracasts topics: {str(e)}")

        return topics

    def _fetch_and_process_html(self, url: str, source: str, section: str) -> Optional[str]:
        """Fetch and process HTML content to markdown."""
        try:
            content_bytes = self._retry_request(url)
            content = content_bytes.decode('utf-8')

            try:
                from bs4 import BeautifulSoup
                from markdownify import markdownify as md

                soup = BeautifulSoup(content, 'html.parser')

                # Remove navigation, header, footer
                for tag in soup.find_all(['nav', 'header', 'footer', 'aside', 'script', 'style']):
                    tag.decompose()

                # Find main content
                main_content = (
                    soup.find('main') or
                    soup.find('article') or
                    soup.find('div', class_=re.compile(r'content|prose|documentation', re.I)) or
                    soup.find('body')
                )

                if main_content:
                    markdown_content = md(str(main_content), strip=['a'], code_language='php')

                    # Clean up
                    markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)

                    # Remove CloudFlare email protection links
                    markdown_content = re.sub(
                        r'\[[^\]]*\]\(/cdn-cgi/l/email-protection[^)]*\)',
                        '[email protected]',
                        markdown_content
                    )

                    # Remove social media links
                    markdown_content = remove_social_media_lines(markdown_content)

                    # Remove image references
                    markdown_content = remove_image_references(markdown_content)

                    markdown_content = markdown_content.strip()

                    if len(markdown_content) > 100:
                        header = f"# {source.replace('-', ' ').title()} - {section.replace('-', ' ').title()}\n\n"
                        header += f"Source: {url}\n\n---\n\n"
                        return header + markdown_content

            except ImportError:
                logger.warning("BeautifulSoup/markdownify not installed")

        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")

        return None

    def _retry_request(self, url: str, headers: Optional[Dict] = None) -> bytes:
        """Make a request with retry logic."""
        if headers is None:
            headers = {"User-Agent": USER_AGENT}

        last_exception: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                request = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(request, timeout=30) as response:
                    return response.read()
            except urllib.error.HTTPError as e:
                last_exception = e
                if e.code == 404:
                    raise
                elif e.code >= 500 and attempt < self.max_retries:
                    wait_time = (2 ** attempt) + random.uniform(0, 2)
                    logger.warning(f"Server error {e.code}, retrying in {wait_time:.1f}s")
                    time.sleep(wait_time)
                else:
                    raise
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    wait_time = (2 ** attempt) + random.uniform(0, 2)
                    logger.warning(f"Request error, retrying in {wait_time:.1f}s: {str(e)}")
                    time.sleep(wait_time)
                else:
                    raise

        if last_exception:
            raise last_exception
        raise RuntimeError(f"Failed to fetch {url}")

    def fetch_all_sources(self, force: bool = False) -> Dict[str, bool]:
        """Fetch learning resources from all sources."""
        results = {}
        for source in self.learning_sources.keys():
            results[source] = self.fetch_learning_source(source, force=force)
        return results

    def list_available_sources(self) -> List[str]:
        """List all available learning sources."""
        return list(self.learning_sources.keys())

    def get_source_info(self, source: str) -> Optional[Dict]:
        """Get information about a specific learning source."""
        return self.learning_sources.get(source)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Laravel Documentation Updater"
    )
    parser.add_argument(
        "--target-dir", 
        type=str,
        default="./docs",
        help="Path to store documentation (default: ./docs)"
    )
    parser.add_argument(
        "--version",
        type=str,
        default=DEFAULT_VERSION,
        help=f"Laravel version branch to use (default: {DEFAULT_VERSION}). Supported: {', '.join(SUPPORTED_VERSIONS)}"
    )
    parser.add_argument(
        "--all-versions",
        action="store_true",
        help="Update documentation for all supported versions"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force update even if already up to date"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check if update is needed, don't perform update"
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update all documentation (Laravel core, services, and community packages)"
    )
    parser.add_argument(
        "--external-only",
        action="store_true",
        help="Only update external Laravel services documentation (deprecated: use --update)"
    )
    parser.add_argument(
        "--core-only",
        action="store_true",
        help="Only update core Laravel documentation (deprecated: use --update)"
    )
    parser.add_argument(
        "--packages-only",
        action="store_true",
        help="Only update community package documentation (deprecated: use --update)"
    )
    parser.add_argument(
        "--services",
        type=str,
        nargs="+",
        help="Specific Laravel services to update (deprecated: use --update)"
    )
    parser.add_argument(
        "--packages",
        type=str,
        nargs="+",
        help="Specific community packages to update (deprecated: use --update)"
    )
    parser.add_argument(
        "--list-services",
        action="store_true",
        help="List all available Laravel services"
    )
    parser.add_argument(
        "--list-packages",
        action="store_true",
        help="List all available community packages"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show status of all documentation sources"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    return parser.parse_args()

def update_version(target_dir: Path, version: str, force: bool, check_only: bool) -> tuple[bool, bool]:
    """Update documentation for a single version.
    
    Returns:
        (success, updated): success indicates if operation completed without error,
                           updated indicates if files were actually updated
    """
    try:
        updater = DocsUpdater(target_dir, version)
        
        if check_only:
            needs_update = updater.needs_update()
            logger.info(f"Version {version}: {'needs' if needs_update else 'does not need'} updating.")
            return True, needs_update
        else:
            updated = updater.update(force=force)
            if updated:
                logger.info(f"Version {version}: Updated successfully")
            else:
                logger.info(f"Version {version}: Already up to date")
            return True, updated
    except Exception as e:
        logger.error(f"Version {version}: Update failed - {str(e)}")
        return False, False

def handle_update_command(args, updater):
    """Handle the unified --update command - updates everything."""
    # Just update all documentation
    results = updater.update_all(force_core=args.force, force_external=args.force, force_packages=args.force, force_learning=args.force)

    core_success = results["core"]
    external_results = results["external"]
    package_results = results.get("packages", {})
    external_success_count = sum(1 for success in external_results.values() if success)
    external_total = len(external_results)
    package_success_count = sum(1 for success in package_results.values() if success)
    package_total = len(package_results)
    
    logger.info(f"Complete documentation update: Core {'successful' if core_success else 'failed'}, External {external_success_count}/{external_total}, Packages {package_success_count}/{package_total}")
    
    # Return success if core succeeded and at least some external services/packages succeeded
    overall_success = core_success and ((external_success_count > 0 or external_total == 0) or (package_success_count > 0 or package_total == 0))
    return 0 if overall_success else 1


def main():
    """Main entry point for the Laravel Docs Updater."""
    args = parse_arguments()
    
    # Set logging level
    logger.setLevel(getattr(logging, args.log_level))
    
    # Create target directory if it doesn't exist
    target_dir = Path(args.target_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize multi-source updater
    updater = MultiSourceDocsUpdater(target_dir, args.version)
    
    try:
        # Handle list services command
        if args.list_services:
            services = updater.external_fetcher.list_available_services()
            print("Available Laravel Services:")
            for service in services:
                info = updater.external_fetcher.get_service_info(service)
                print(f"  {service}: {info.get('name', service)}")
            return 0
        
        # Handle list packages command
        if args.list_packages:
            packages = updater.package_fetcher.list_available_packages()
            print("Available Community Packages:")
            for package in packages:
                info = updater.package_fetcher.community_packages.get(package, {})
                print(f"  {package}: {info.get('name', package)}")
                # Show sub-packages for Spatie
                if package == "spatie" and "packages" in info:
                    for sub_pkg, sub_info in info["packages"].items():
                        print(f"    - {sub_pkg}: {sub_info.get('name', sub_pkg)}")
            return 0
        
        # Handle status command
        if args.status:
            status = updater.get_all_documentation_status()
            print("Documentation Status:")
            print(f"\nCore Laravel Documentation ({args.version}):")
            core_status = status["core"]
            if "error" in core_status:
                print(f"  Error: {core_status['error']}")
            else:
                print(f"  Available: {core_status.get('available', False)}")
                print(f"  Last Updated: {core_status.get('last_updated', 'unknown')}")
                print(f"  Commit: {core_status.get('commit_sha', 'unknown')[:7]}")
            
            print("\nExternal Services:")
            for service, info in status["external"].items():
                if "error" in info:
                    print(f"  {service}: Error - {info['error']}")
                else:
                    print(f"  {service} ({info.get('name', service)}):")
                    print(f"    Cache Valid: {info.get('cache_valid', False)}")
                    print(f"    Type: {info.get('type', 'unknown')}")
                    if info.get('success_rate') != 'unknown':
                        print(f"    Success Rate: {info.get('success_rate', 'unknown'):.1%}")
                    
                    # Show auto-discovery status if available
                    metadata_path = updater.external_fetcher.get_cache_metadata_path(service)
                    if metadata_path.exists():
                        try:
                            import json
                            with open(metadata_path, 'r') as f:
                                metadata = json.load(f)
                            if metadata.get('auto_discovery_enabled'):
                                discovery_method = metadata.get('discovery_method', 'unknown')
                                discovered_count = metadata.get('discovered_count', 0)
                                print(f"    Auto-Discovery: ✅ {discovery_method} ({discovered_count} sections)")
                                if metadata.get('manual_fallback'):
                                    print("    Fallback: Used manual configuration (auto-discovery failed)")
                            else:
                                print("    Auto-Discovery: ❌ disabled (using manual configuration)")
                        except Exception:
                            pass
            
            print("\nCommunity Packages:")
            for package, info in status["packages"].items():
                if "error" in info:
                    print(f"  {package}: Error - {info['error']}")
                else:
                    print(f"  {package} ({info.get('name', package)}):")
                    print(f"    Cache Valid: {info.get('cache_valid', False)}")
                    print(f"    Sections: {info.get('sections_count', 0)}")
                    
                    # Show sub-packages for Spatie
                    if package == "spatie" and "sub_packages" in info:
                        print("    Sub-packages:")
                        for sub_pkg, sub_info in info["sub_packages"].items():
                            print(f"      - {sub_info.get('name', sub_pkg)}: {sub_info.get('sections_count', 0)} sections")
            
            return 0
        
        # Validate version if not updating all
        if not args.all_versions and args.version not in SUPPORTED_VERSIONS:
            logger.error(f"Unsupported version: {args.version}. Supported versions: {', '.join(SUPPORTED_VERSIONS)}")
            return 1
        
        # Handle check-only command
        if args.check_only:
            needs_update = updater.needs_update()
            print("Update Status:")
            print(f"Core Laravel ({args.version}): {'needs update' if needs_update['core'] else 'up to date'}")
            print("External Services:")
            for service, needs in needs_update["external"].items():
                print(f"  {service}: {'needs update' if needs else 'up to date'}")
            print("Community Packages:")
            for package, needs in needs_update["packages"].items():
                print(f"  {package}: {'needs update' if needs else 'up to date'}")
            
            # Return 1 if any updates needed, 0 if all up to date
            any_needs_update = needs_update["core"] or any(needs_update["external"].values()) or any(needs_update["packages"].values())
            return 1 if any_needs_update else 0
        
        # Handle new unified --update parameter
        if args.update:
            return handle_update_command(args, updater)
        
        # Handle deprecated parameters - all now just update everything
        if args.external_only or args.core_only or args.packages_only or args.packages or args.services:
            logger.warning("Deprecated parameter used. Please use --update instead.")
            return handle_update_command(args, updater)
        
        # Handle specific update modes (deprecated but still supported)
        if args.all_versions:
            # Update all supported versions (core only)
            all_success = True
            
            for version in SUPPORTED_VERSIONS:
                logger.info(f"Processing version {version}...")
                version_updater = MultiSourceDocsUpdater(target_dir, version)
                success = version_updater.update_core_docs(force=args.force)
                
                if not success:
                    all_success = False
            
            return 0 if all_success else 1
        
        else:
            # Default: update all (core, external services, and packages)
            results = updater.update_all(force_core=args.force, force_external=args.force, force_packages=args.force, force_learning=args.force)
            
            core_success = results["core"]
            external_results = results["external"]
            package_results = results.get("packages", {})
            external_success_count = sum(1 for success in external_results.values() if success)
            external_total = len(external_results)
            package_success_count = sum(1 for success in package_results.values() if success)
            package_total = len(package_results)
            
            logger.info(f"Complete documentation update: Core {'successful' if core_success else 'failed'}, External {external_success_count}/{external_total}, Packages {package_success_count}/{package_total}")
            
            # Return success if core succeeded and at least some external services/packages succeeded
            overall_success = core_success and ((external_success_count > 0 or external_total == 0) or (package_success_count > 0 or package_total == 0))
            return 0 if overall_success else 1
                
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130

if __name__ == "__main__":
    sys.exit(main())