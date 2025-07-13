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
from typing import Dict, List, Optional, Union
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
                # Remove query parameters if present
                clean_link = link.split('?')[0]
                
                # Check if this is an asset file (CSS, JS, images, etc.)
                if self._is_asset_file(clean_link):
                    continue
                    
                # Remove the /docs/ prefix to get the section name
                section = clean_link.replace('/docs/', '')
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
                # Extract section after version (e.g., /docs/v5/installation -> installation)
                section_match = re.search(r'/docs/v\d+/(.+)', link)
                if section_match:
                    section = section_match.group(1)
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
                        
                        section = path.lstrip('/')
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
                # Remove the /docs/ prefix
                section = link.replace('/docs/', '')
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
                    "nested_sections": ["accounts", "servers", "sites", "resources"],
                    "exclude_patterns": ["#", "javascript:", "mailto:"]
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
        """Check if the cached documentation for a service is still valid."""
        metadata_path = self.get_cache_metadata_path(service)
        
        if not metadata_path.exists():
            return False
        
        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            cache_time = metadata.get('cached_at', 0)
            return (time.time() - cache_time) < self.cache_duration
        except Exception as e:
            logger.warning(f"Error reading cache metadata for {service}: {str(e)}")
            return False
    
    def save_cache_metadata(self, service: str, metadata: Dict) -> None:
        """Save cache metadata for a service."""
        metadata_path = self.get_cache_metadata_path(service)
        metadata['cached_at'] = time.time()
        
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
        if config.get("auto_discovery", False):
            try:
                discovered_sections = self.auto_discovery.discover_sections(service, config)
                logger.info(f"Auto-discovery found {len(discovered_sections)} sections for {service}")
            except Exception as e:
                logger.warning(f"Auto-discovery failed for {service}: {str(e)}, falling back to manual sections")
        
        # Use discovered sections if available, otherwise use manual sections
        if discovered_sections:
            sections = discovered_sections
            discovery_method = "auto-discovery"
        else:
            sections = config.get("sections", [])
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
        Extract readable content from HTML.
        This is a basic implementation using regex patterns.
        """
        # Remove script and style tags
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Look for main content containers (Laravel docs specific patterns)
        content_patterns = [
            r'<main[^>]*>(.*?)</main>',
            r'<article[^>]*>(.*?)</article>',
            # Mintlify patterns (used by Vapor)
            r'<div[^>]*class="[^"]*prose[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*prose-lg[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*prose-gray[^"]*"[^>]*>(.*?)</div>',
            # Standard Laravel docs patterns  
            r'<div[^>]*class="[^"]*markdown[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*documentation[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*id="[^"]*content[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*data-docs-content[^>]*>(.*?)</div>',
        ]
        
        extracted_content = None
        for pattern in content_patterns:
            matches = re.findall(pattern, html_content, flags=re.DOTALL | re.IGNORECASE)
            if matches:
                # Combine multiple matches (useful for sites like Mintlify with multiple prose sections)
                extracted_content = '\n\n'.join(matches)
                break
        
        # If no specific content container found, try to get body content
        if not extracted_content:
            body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, flags=re.DOTALL | re.IGNORECASE)
            if body_match:
                extracted_content = body_match.group(1)
        
        # If still no content, use the entire HTML
        if not extracted_content:
            extracted_content = html_content
        
        # Basic HTML to text conversion
        text_content = self._html_to_text(extracted_content)
        
        # Clean up the text
        text_content = re.sub(r'\n\s*\n\s*\n', '\n\n', text_content)  # Remove excessive newlines
        text_content = text_content.strip()
        
        # Limit length to prevent extremely long outputs
        if len(text_content) > 10000:
            text_content = text_content[:10000] + "\n\n*[Content truncated for length]*"
        
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
        Convert HTML to readable text with basic markdown-like formatting.
        """
        # Convert headings
        html_content = re.sub(r'<h([1-6])[^>]*>(.*?)</h\1>', lambda m: '#' * int(m.group(1)) + ' ' + m.group(2) + '\n\n', html_content, flags=re.IGNORECASE)
        
        # Convert paragraphs
        html_content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Convert line breaks
        html_content = re.sub(r'<br[^>]*/?>', '\n', html_content, flags=re.IGNORECASE)
        
        # Convert lists
        html_content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<[ou]l[^>]*>', '\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'</[ou]l>', '\n', html_content, flags=re.IGNORECASE)
        
        # Convert code blocks
        html_content = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', r'```\n\1\n```\n', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Convert strong/bold
        html_content = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Convert emphasis/italic
        html_content = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Convert links
        html_content = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove remaining HTML tags
        html_content = re.sub(r'<[^>]+>', '', html_content)
        
        # Decode HTML entities
        html_content = html.unescape(html_content)
        
        return html_content
    
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
        
        try:
            # Create a temporary directory
            with tempfile.TemporaryDirectory(delete=False) as temp_dir:
                temp_path = Path(temp_dir)
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
    
    def update_all(self, force_core: bool = False, force_external: bool = False) -> Dict[str, object]:
        """
        Update all documentation sources.
        
        Args:
            force_core: Force update of core documentation
            force_external: Force update of external documentation
            
        Returns:
            Dictionary with results for core and external updates
        """
        logger.info("Starting comprehensive documentation update")
        
        results: Dict[str, object] = {
            "core": False,
            "external": {}
        }
        
        try:
            # Update core Laravel documentation
            results["core"] = self.update_core_docs(force=force_core)
            
            # Update external services documentation
            results["external"] = self.update_external_docs(force=force_external)
            
            # Log summary
            core_status = "updated" if results["core"] else "up-to-date"
            external_results = results["external"]
            if isinstance(external_results, dict):
                external_count = sum(1 for success in external_results.values() if success)
                total_external = len(external_results)
            else:
                external_count = 0
                total_external = 0
            
            logger.info(f"Documentation update complete: Core {core_status}, External {external_count}/{total_external} services")
            
        except Exception as e:
            logger.error(f"Error during comprehensive documentation update: {str(e)}")
        
        return results
    
    def get_all_documentation_status(self) -> Dict[str, Dict]:
        """Get status information for all documentation sources."""
        status: Dict[str, Dict] = {
            "core": {},
            "external": {}
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
                    "last_fetched": metadata.get("cached_at", "never"),
                    "success_rate": metadata.get("success_rate", "unknown")
                }
            except Exception as e:
                status["external"][service] = {"error": str(e)}
        
        return status
    
    def needs_update(self, check_external: bool = True) -> Dict[str, Union[bool, Dict[str, bool]]]:
        """
        Check which documentation sources need updating.
        
        Args:
            check_external: Whether to check external services
            
        Returns:
            Dictionary indicating which sources need updates
        """
        needs_update: Dict[str, Union[bool, Dict[str, bool]]] = {
            "core": False,
            "external": {}
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
        
        return needs_update

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
        "--external-only",
        action="store_true",
        help="Only update external Laravel services documentation"
    )
    parser.add_argument(
        "--core-only",
        action="store_true",
        help="Only update core Laravel documentation"
    )
    parser.add_argument(
        "--services",
        type=str,
        nargs="+",
        help="Specific Laravel services to update (forge, vapor, envoyer, nova)"
    )
    parser.add_argument(
        "--list-services",
        action="store_true",
        help="List all available Laravel services"
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
            
            # Return 1 if any updates needed, 0 if all up to date
            any_needs_update = needs_update["core"] or any(needs_update["external"].values())
            return 1 if any_needs_update else 0
        
        # Handle specific update modes
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
            
        elif args.external_only:
            # Update only external services
            if args.services:
                results = updater.update_external_docs(services=args.services, force=args.force)
            else:
                results = updater.update_external_docs(force=args.force)
            
            success_count = sum(1 for success in results.values() if success)
            total_count = len(results)
            logger.info(f"External documentation update: {success_count}/{total_count} services successful")
            return 0 if success_count == total_count else 1
            
        elif args.core_only:
            # Update only core documentation
            success = updater.update_core_docs(force=args.force)
            return 0 if success else 1
            
        elif args.services:
            # Update specific services only
            results = updater.update_external_docs(services=args.services, force=args.force)
            success_count = sum(1 for success in results.values() if success)
            total_count = len(results)
            logger.info(f"Service documentation update: {success_count}/{total_count} services successful")
            return 0 if success_count == total_count else 1
        
        else:
            # Default: update both core and external
            results = updater.update_all(force_core=args.force, force_external=args.force)
            
            core_success = results["core"]
            external_results = results["external"]
            external_success_count = sum(1 for success in external_results.values() if success)
            external_total = len(external_results)
            
            logger.info(f"Complete documentation update: Core {'successful' if core_success else 'failed'}, External {external_success_count}/{external_total}")
            
            # Return success if core succeeded and at least some external services succeeded
            overall_success = core_success and (external_success_count > 0 or external_total == 0)
            return 0 if overall_success else 1
                
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130

if __name__ == "__main__":
    sys.exit(main())