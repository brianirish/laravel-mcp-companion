#!/usr/bin/env python3
"""
Standalone MCP tool functions for Laravel MCP Companion.

This module contains the core functionality of MCP tools as standalone functions
that can be imported and tested independently of the FastMCP server setup.
"""

import os
import re
import logging
from pathlib import Path
from typing import Dict, Optional, List, Any
import json
import threading

from docs_updater import get_cached_supported_versions, DEFAULT_VERSION

logger = logging.getLogger("laravel-mcp-companion")

# Get supported versions
SUPPORTED_VERSIONS = get_cached_supported_versions()

# Global caches for performance optimization
_file_content_cache: Dict[str, str] = {}
_search_result_cache: Dict[str, str] = {}
_cache_lock = threading.Lock()


def get_file_content_cached(file_path: str) -> str:
    """Get file content with caching."""
    with _cache_lock:
        if file_path in _file_content_cache:
            logger.debug(f"Cache hit for file: {file_path}")
            return _file_content_cache[file_path]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cache the content
        with _cache_lock:
            _file_content_cache[file_path] = content
            # Limit cache size to prevent memory issues
            if len(_file_content_cache) > 100:
                # Remove oldest entries
                oldest_keys = list(_file_content_cache.keys())[:20]
                for key in oldest_keys:
                    del _file_content_cache[key]
        
        return content
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


def get_version_from_path(path: str) -> tuple[str, str]:
    """Extract version and relative path from a path string."""
    parts = path.split('/', 1)
    
    if len(parts) == 2 and parts[0] in SUPPORTED_VERSIONS:
        # Path includes version
        return parts[0], parts[1]
    else:
        # No version specified, use default
        return DEFAULT_VERSION, path


def is_safe_path(base_path: Path, target_path: Path) -> bool:
    """Check if target path is within base path (prevent directory traversal)."""
    try:
        # Resolve both paths to handle any .. or . components
        base = base_path.resolve()
        target = target_path.resolve()
        
        # Check if target is within base
        return str(target).startswith(str(base))
    except Exception:
        return False


def get_laravel_docs_metadata(docs_path: Path, version: str) -> dict:
    """Get metadata for a specific Laravel documentation version."""
    metadata_file = docs_path / version / ".metadata.json"
    
    if metadata_file.exists():
        try:
            with open(metadata_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read metadata for version {version}: {str(e)}")
    
    return {}


def list_laravel_docs_impl(docs_path: Path, version: Optional[str] = None) -> str:
    """List all available Laravel documentation files.
    
    Args:
        docs_path: Base path for documentation
        version: Specific Laravel version to list (e.g., "12.x"). If not provided, lists all versions.
    """
    logger.debug(f"list_laravel_docs_impl called (version: {version})")
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


def read_laravel_doc_content_impl(docs_path: Path, filename: str, version: Optional[str] = None) -> str:
    """Read the content of a specific Laravel documentation file.
    
    Args:
        docs_path: Base path for documentation
        filename: Name of the documentation file (e.g., "blade.md" or "12.x/blade.md")
        version: Specific Laravel version to use. Overridden if filename includes version.
    """
    logger.debug(f"read_laravel_doc_content_impl called with filename: {filename}, version: {version}")
    
    # Extract version and relative path
    if '/' in filename and filename.split('/')[0] in SUPPORTED_VERSIONS:
        # Filename includes version
        version_from_path, relative_path = get_version_from_path(filename)
        version = version_from_path
    else:
        # Use provided version or default
        relative_path = filename
        if not version:
            version = DEFAULT_VERSION
    
    # Make sure the path ends with .md
    if not relative_path.endswith('.md'):
        relative_path = f"{relative_path}.md"
    
    file_path = docs_path / version / relative_path
    
    # Security check - ensure we stay within version directory
    version_path = docs_path / version
    if not is_safe_path(version_path, file_path):
        logger.warning(f"Access denied: {filename} (attempted directory traversal)")
        return f"Access denied: {filename} (attempted directory traversal)"
    
    if not file_path.exists():
        logger.warning(f"Documentation file not found: {file_path}")
        return f"Documentation file not found: {filename} (version: {version})"
    
    try:
        content = get_file_content_cached(str(file_path))
        if not content.startswith("Error") and not content.startswith("File not found"):
            logger.debug(f"Successfully read file: {file_path} ({len(content)} bytes)")
        return content
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return f"Error reading file: {str(e)}"


def search_laravel_docs_impl(docs_path: Path, query: str, version: Optional[str] = None, include_external: bool = True, external_dir: Optional[Path] = None) -> str:
    """Search through Laravel documentation for a specific term.
    
    Args:
        docs_path: Base path for documentation
        query: Search term to look for
        version: Specific Laravel version to search (e.g., "12.x"). If not provided, searches all versions.
        include_external: Whether to include external Laravel services documentation in search
        external_dir: Path to external documentation directory
    """
    logger.debug(f"search_laravel_docs_impl called with query: {query}, version: {version}, include_external: {include_external}")
    
    if not query.strip():
        return "Search query cannot be empty"
    
    # Check cache for search results
    cache_key = f"search:{query}:{version}:{include_external}"
    with _cache_lock:
        if cache_key in _search_result_cache:
            logger.debug(f"Returning cached search results for: {query}")
            return _search_result_cache[cache_key]
    
    core_results = []
    external_results = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    
    try:
        # Search core Laravel documentation
        search_versions = [version] if version else SUPPORTED_VERSIONS
        
        for v in search_versions:
            version_path = docs_path / v
            if not version_path.exists():
                continue
            
            for file in os.listdir(version_path):
                if file.endswith('.md'):
                    file_path = version_path / file
                    
                    content = get_file_content_cached(str(file_path))
                    if not content.startswith("Error") and not content.startswith("File not found"):
                        if pattern.search(content):
                            count = len(pattern.findall(content))
                            core_results.append(f"{v}/{file} ({count} matches)")
        
        # Search external documentation if requested
        if include_external and external_dir and external_dir.exists():
            for service_dir in external_dir.iterdir():
                if service_dir.is_dir():
                    service_name = service_dir.name
                    service_matches = []
                    
                    for file_path in service_dir.glob("*.md"):
                        try:
                            content = get_file_content_cached(str(file_path))
                            if not content.startswith("Error") and not content.startswith("File not found"):
                                if pattern.search(content):
                                    count = len(pattern.findall(content))
                                    service_matches.append(f"{file_path.name} ({count} matches)")
                        except Exception as e:
                            logger.warning(f"Error searching {file_path}: {str(e)}")
                            continue
                    
                    if service_matches:
                        external_results.append(f"**{service_name.title()}:** {', '.join(service_matches)}")
        
        # Format combined results
        response = []
        
        if core_results or external_results:
            response.append(f"Search results for '{query}':")
            response.append("")
            
            if core_results:
                response.append(f"**Core Laravel Documentation ({len(core_results)} files):**")
                for result in core_results:
                    response.append(f"  - {result}")
                response.append("")
            
            if external_results:
                response.append(f"**External Laravel Services ({len(external_results)} services):**")
                for result in external_results:
                    response.append(f"  - {result}")
            
            result = "\n".join(response)
        else:
            search_scope = f"version {version}" if version else "all sources"
            result = f"No results found for '{query}' in {search_scope}"
        
        # Cache the search result
        with _cache_lock:
            _search_result_cache[cache_key] = result
            # Limit cache size
            if len(_search_result_cache) > 100:
                # Remove oldest entries
                oldest_keys = list(_search_result_cache.keys())[:20]
                for key in oldest_keys:
                    del _search_result_cache[key]
        
        return result
    except Exception as e:
        logger.error(f"Error searching documentation: {str(e)}")
        return f"Error searching documentation: {str(e)}"


def search_laravel_docs_with_context_impl(docs_path: Path, query: str, version: Optional[str] = None, 
                                         context_length: int = 200, include_external: bool = True,
                                         external_dir: Optional[Path] = None) -> str:
    """Search Laravel documentation and return matches with surrounding context.
    
    Args:
        docs_path: Base path for documentation
        query: Search term to look for
        version: Specific Laravel version to search. If not provided, searches all versions.
        context_length: Number of characters to show before/after match
        include_external: Whether to include external Laravel services documentation
        external_dir: Path to external documentation directory
    """
    logger.debug(f"search_laravel_docs_with_context_impl called with query: {query}")
    
    if not query.strip():
        return "Search query cannot be empty"
    
    results = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    
    try:
        # Search core documentation
        search_versions = [version] if version else SUPPORTED_VERSIONS
        
        for v in search_versions:
            version_path = docs_path / v
            if not version_path.exists():
                continue
            
            for file in os.listdir(version_path):
                if file.endswith('.md'):
                    file_path = version_path / file
                    
                    content = get_file_content_cached(str(file_path))
                    if not content.startswith("Error") and not content.startswith("File not found"):
                        matches = list(pattern.finditer(content))
                        if matches:
                            file_results = [f"\n### {v}/{file} ({len(matches)} matches):\n"]
                            
                            for i, match in enumerate(matches[:5]):  # Limit to 5 matches per file
                                start = max(0, match.start() - context_length)
                                end = min(len(content), match.end() + context_length)
                                
                                # Find line boundaries
                                while start > 0 and content[start] != '\n':
                                    start -= 1
                                while end < len(content) and content[end] != '\n':
                                    end += 1
                                
                                context = content[start:end].strip()
                                # Highlight the match
                                context = pattern.sub(lambda m: f"**{m.group()}**", context)
                                
                                file_results.append(f"Match {i+1}:\n```\n{context}\n```\n")
                            
                            results.extend(file_results)
        
        # Search external documentation if requested
        if include_external and external_dir and external_dir.exists():
            for service_dir in external_dir.iterdir():
                if service_dir.is_dir():
                    service_name = service_dir.name
                    
                    for file_path in service_dir.glob("*.md"):
                        try:
                            content = get_file_content_cached(str(file_path))
                            if not content.startswith("Error") and not content.startswith("File not found"):
                                matches = list(pattern.finditer(content))
                                if matches:
                                    file_results = [f"\n### {service_name.title()}/{file_path.name} ({len(matches)} matches):\n"]
                                    
                                    for i, match in enumerate(matches[:5]):
                                        start = max(0, match.start() - context_length)
                                        end = min(len(content), match.end() + context_length)
                                        
                                        while start > 0 and content[start] != '\n':
                                            start -= 1
                                        while end < len(content) and content[end] != '\n':
                                            end += 1
                                        
                                        context = content[start:end].strip()
                                        context = pattern.sub(lambda m: f"**{m.group()}**", context)
                                        
                                        file_results.append(f"Match {i+1}:\n```\n{context}\n```\n")
                                    
                                    results.extend(file_results)
                        except Exception as e:
                            logger.warning(f"Error searching {file_path}: {str(e)}")
                            continue
        
        if results:
            return f"Search results for '{query}':\n" + "".join(results)
        else:
            search_scope = f"version {version}" if version else "all sources"
            return f"No results found for '{query}' in {search_scope}"
            
    except Exception as e:
        logger.error(f"Error searching documentation: {str(e)}")
        return f"Error searching documentation: {str(e)}"


def get_doc_structure_impl(docs_path: Path, filename: str, version: Optional[str] = None) -> str:
    """Get the structure (headings) of a documentation file.
    
    Args:
        docs_path: Base path for documentation
        filename: Name of the documentation file
        version: Specific Laravel version to use
    """
    logger.debug(f"get_doc_structure_impl called with filename: {filename}")
    
    # Use read_laravel_doc_content_impl to get the content
    content = read_laravel_doc_content_impl(docs_path, filename, version)
    
    if content.startswith("Error") or content.startswith("Documentation file not found") or content.startswith("Access denied"):
        return content
    
    try:
        structure = []
        lines = content.split('\n')
        
        for line in lines:
            # Match markdown headings
            if line.startswith('#'):
                # Count the number of # characters
                level = len(line) - len(line.lstrip('#'))
                heading = line.lstrip('#').strip()
                if heading:
                    indent = "  " * (level - 1)
                    structure.append(f"{indent}- {heading}")
        
        if structure:
            result = f"Structure of {filename}:\n\n" + "\n".join(structure)
        else:
            result = f"No headings found in {filename}"
        
        return result
    except Exception as e:
        logger.error(f"Error analyzing document structure: {str(e)}")
        return f"Error analyzing document structure: {str(e)}"


def browse_docs_by_category_impl(docs_path: Path, category: str, version: Optional[str] = None) -> str:
    """Browse Laravel documentation files by category.
    
    Args:
        docs_path: Base path for documentation
        category: Category to filter by (e.g., "authentication", "database", "frontend")
        version: Specific Laravel version to browse. If not provided, uses default version.
    """
    logger.debug(f"browse_docs_by_category_impl called with category: {category}")
    
    if not version:
        version = DEFAULT_VERSION
    
    # Define category mappings
    categories = {
        "authentication": ["authentication", "sanctum", "passport", "fortify", "breeze", "jetstream", "passwords", "verification"],
        "database": ["database", "eloquent", "migrations", "seeding", "queries", "pagination", "redis"],
        "frontend": ["blade", "frontend", "vite", "mix", "views", "localization", "validation"],
        "api": ["api", "sanctum", "passport", "eloquent-resources", "routing"],
        "testing": ["testing", "dusk", "http-tests", "console-tests", "database-testing", "mocking"],
        "deployment": ["deployment", "octane", "sail", "homestead", "valet", "forge", "vapor"],
        "packages": ["packages", "cashier", "scout", "socialite", "telescope", "horizon"],
        "security": ["authentication", "authorization", "encryption", "hashing", "passwords", "csrf", "sanctum", "passport"]
    }
    
    category_lower = category.lower()
    if category_lower not in categories:
        available = ", ".join(sorted(categories.keys()))
        return f"Unknown category: {category}. Available categories: {available}"
    
    version_path = docs_path / version
    if not version_path.exists():
        return f"No documentation found for version {version}"
    
    try:
        # Find files matching the category
        category_files = []
        keywords = categories[category_lower]
        
        for file in os.listdir(version_path):
            if file.endswith('.md'):
                file_lower = file.lower().replace('.md', '')
                # Check if filename contains any category keyword
                if any(keyword in file_lower for keyword in keywords):
                    category_files.append(file)
        
        if category_files:
            result = [f"Laravel {version} - {category.title()} Documentation:"]
            result.append("")
            
            for file in sorted(category_files):
                # Try to get a brief description from the file
                file_path = version_path / file
                content = get_file_content_cached(str(file_path))
                
                if not content.startswith("Error"):
                    # Extract first paragraph or first few lines
                    lines = content.split('\n')
                    description = ""
                    
                    for line in lines[:10]:
                        line = line.strip()
                        if line and not line.startswith('#') and not line.startswith('- '):
                            description = line[:100] + "..." if len(line) > 100 else line
                            break
                    
                    result.append(f"- **{file}**: {description}")
                else:
                    result.append(f"- **{file}**")
            
            return "\n".join(result)
        else:
            return f"No {category} documentation files found in version {version}"
            
    except Exception as e:
        logger.error(f"Error browsing documentation: {str(e)}")
        return f"Error browsing documentation: {str(e)}"


def clear_caches():
    """Clear all caches."""
    with _cache_lock:
        _file_content_cache.clear()
        _search_result_cache.clear()
    logger.info("Caches cleared")