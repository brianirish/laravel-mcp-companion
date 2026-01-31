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
from typing import Dict, List, Optional
import json
import threading

from docs_updater import get_cached_supported_versions, DEFAULT_VERSION
from toon_helpers import (
    toon_encode,
    format_version_list,
    format_search_results,
    format_category_docs,
    format_doc_structure,
    format_error,
    format_feature_verification,
    format_version_comparison,
    format_learning_resources,
    format_learning_path,
    format_learning_paths_list,
    format_need_docs,
    format_related_packages,
    format_difficulty_content
)
from learning_resources import (
    DifficultyLevel,
    EXPANDED_CATEGORIES,
    NEED_MAPPINGS,
    LEARNING_PATHS,
    RELATED_PACKAGES,
    get_topics_by_difficulty,
    get_docs_for_need,
    get_related_packages,
    get_learning_path,
    list_learning_paths,
    get_category_docs,
    list_categories
)

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


def get_version_from_path(path: str, runtime_version: Optional[str] = None) -> tuple[str, str]:
    """Extract version and relative path from a path string.
    
    Args:
        path: Path like "12.x/blade.md" or "blade.md"
        runtime_version: Runtime default version (from --version flag)
    
    Returns:
        (version, relative_path): Tuple of version and path within that version
    """
    parts = path.split('/', 1)
    
    if len(parts) == 2 and parts[0] in SUPPORTED_VERSIONS:
        # Path includes version
        return parts[0], parts[1]
    else:
        # No version specified, use runtime version or default
        default_version = runtime_version if runtime_version else DEFAULT_VERSION
        return default_version, path


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
    # Check new location first (.metadata/sync_info.json)
    metadata_file = docs_path / version / ".metadata" / "sync_info.json"
    
    if not metadata_file.exists():
        # Fall back to old location for compatibility with tests
        metadata_file = docs_path / version / ".metadata.json"
    
    if metadata_file.exists():
        try:
            with open(metadata_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read metadata for version {version}: {str(e)}")
    
    return {}


def list_laravel_docs_impl(docs_path: Path, version: Optional[str] = None, runtime_version: Optional[str] = None) -> str:
    """List all available Laravel documentation files.

    Args:
        docs_path: Base path for documentation
        version: Specific Laravel version to list (e.g., "12.x"). If not provided, lists all versions.

    Returns:
        TOON-encoded structured data with version metadata and file lists.
    """
    logger.debug(f"list_laravel_docs_impl called (version: {version})")

    try:
        if version:
            # List docs for specific version
            version_path = docs_path / version
            if not version_path.exists():
                return format_error(
                    f"No documentation found for version {version}",
                    {"suggestion": "Use update_laravel_docs() to fetch documentation"}
                )

            metadata = get_laravel_docs_metadata(docs_path, version)
            md_files = sorted([f for f in os.listdir(version_path) if f.endswith('.md')])

            if not md_files:
                return format_error(f"No documentation files found in version {version}")

            return toon_encode({
                "version": version,
                "last_updated": metadata.get('sync_time', 'unknown'),
                "commit": metadata.get('commit_sha', 'unknown')[:7] if metadata.get('commit_sha') else 'unknown',
                "file_count": len(md_files),
                "files": md_files
            })
        else:
            # List all versions
            versions_data: List[Dict] = []
            for v in SUPPORTED_VERSIONS:
                version_path = docs_path / v
                if version_path.exists() and any(f.endswith('.md') for f in os.listdir(version_path) if os.path.isfile(version_path / f)):
                    metadata = get_laravel_docs_metadata(docs_path, v)
                    md_files = [f for f in os.listdir(version_path) if f.endswith('.md')]
                    versions_data.append({
                        "version": v,
                        "last_updated": metadata.get('sync_time', 'unknown'),
                        "commit": metadata.get('commit_sha', 'unknown')[:7] if metadata.get('commit_sha') else 'unknown',
                        "file_count": len(md_files)
                    })

            if not versions_data:
                return format_error(
                    "No documentation files found",
                    {"suggestion": "Use update_laravel_docs() to fetch documentation"}
                )

            return format_version_list(versions_data)
    except Exception as e:
        logger.error(f"Error listing documentation files: {str(e)}")
        return format_error(f"Error listing documentation files: {str(e)}")


def read_laravel_doc_content_impl(docs_path: Path, filename: str, version: Optional[str] = None, runtime_version: Optional[str] = None) -> str:
    """Read the content of a specific Laravel documentation file.
    
    Args:
        docs_path: Base path for documentation
        filename: Name of the documentation file (e.g., "blade.md" or "12.x/blade.md")
        version: Specific Laravel version to use. Overridden if filename includes version.
    """
    logger.debug(f"read_laravel_doc_content_impl called with filename: {filename}, version: {version}, runtime_version: {runtime_version}")
    
    # Extract version and relative path
    if '/' in filename and filename.split('/')[0] in SUPPORTED_VERSIONS:
        # Filename includes version
        version_from_path, relative_path = get_version_from_path(filename, runtime_version)
        version = version_from_path
    else:
        # Use provided version or runtime version or default
        relative_path = filename
        if not version:
            version = runtime_version if runtime_version else DEFAULT_VERSION
    
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


def search_laravel_docs_impl(docs_path: Path, query: str, version: Optional[str] = None, include_external: bool = True, external_dir: Optional[Path] = None, runtime_version: Optional[str] = None) -> str:
    """Search through Laravel documentation for a specific term.

    Args:
        docs_path: Base path for documentation
        query: Search term to look for
        version: Specific Laravel version to search (e.g., "12.x"). If not provided, searches all versions.
        include_external: Whether to include external Laravel services documentation in search
        external_dir: Path to external documentation directory

    Returns:
        TOON-encoded structured search results.
    """
    logger.debug(f"search_laravel_docs_impl called with query: {query}, version: {version}, include_external: {include_external}")

    if not query.strip():
        return format_error("Search query cannot be empty")

    # Check cache for search results
    cache_key = f"search:{query}:{version}:{include_external}"
    with _cache_lock:
        if cache_key in _search_result_cache:
            logger.debug(f"Returning cached search results for: {query}")
            return _search_result_cache[cache_key]

    core_results_data: List[Dict] = []
    external_results_data: List[Dict] = []
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
                            core_results_data.append({
                                "file": f"{v}/{file}",
                                "matches": count
                            })

        # Search external documentation if requested
        if include_external and external_dir and external_dir.exists():
            for service_dir in external_dir.iterdir():
                if service_dir.is_dir():
                    service_name = service_dir.name

                    for file_path in service_dir.glob("*.md"):
                        try:
                            content = get_file_content_cached(str(file_path))
                            if not content.startswith("Error") and not content.startswith("File not found"):
                                if pattern.search(content):
                                    count = len(pattern.findall(content))
                                    external_results_data.append({
                                        "service": service_name,
                                        "file": file_path.name,
                                        "matches": count
                                    })
                        except Exception as e:
                            logger.warning(f"Error searching {file_path}: {str(e)}")
                            continue

        # Format combined results
        if not core_results_data and not external_results_data:
            search_scope = f"version {version}" if version else "all sources"
            result = format_error(f"No results found for '{query}'", {"scope": search_scope})
        else:
            result = format_search_results(
                query,
                core_results_data,
                external_results_data if external_results_data else None
            )

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
        return format_error(f"Error searching documentation: {str(e)}")


def search_laravel_docs_with_context_impl(docs_path: Path, query: str, version: Optional[str] = None, 
                                         context_length: int = 200, include_external: bool = True,
                                         external_dir: Optional[Path] = None, runtime_version: Optional[str] = None) -> str:
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


def get_doc_structure_impl(docs_path: Path, filename: str, version: Optional[str] = None, runtime_version: Optional[str] = None) -> str:
    """Get the structure (headings) of a documentation file.

    Args:
        docs_path: Base path for documentation
        filename: Name of the documentation file
        version: Specific Laravel version to use

    Returns:
        TOON-encoded document structure with headings.
    """
    logger.debug(f"get_doc_structure_impl called with filename: {filename}")

    # Use read_laravel_doc_content_impl to get the content
    content = read_laravel_doc_content_impl(docs_path, filename, version)

    if content.startswith("Error") or content.startswith("Documentation file not found") or content.startswith("Access denied"):
        return content

    try:
        headings_data: List[Dict] = []
        lines = content.split('\n')

        for line in lines:
            # Match markdown headings
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                heading = line.lstrip('#').strip()
                if heading:
                    headings_data.append({
                        "level": level,
                        "text": heading
                    })

        if not headings_data:
            return format_error(f"No headings found in {filename}")

        return format_doc_structure(filename, headings_data)
    except Exception as e:
        logger.error(f"Error analyzing document structure: {str(e)}")
        return format_error(f"Error analyzing document structure: {str(e)}")


def browse_docs_by_category_impl(docs_path: Path, category: str, version: Optional[str] = None, runtime_version: Optional[str] = None) -> str:
    """Browse Laravel documentation files by category.

    Args:
        docs_path: Base path for documentation
        category: Category to filter by (e.g., "authentication", "database", "frontend")
        version: Specific Laravel version to browse. If not provided, uses default version.

    Returns:
        TOON-encoded category documentation files with descriptions.
    """
    logger.debug(f"browse_docs_by_category_impl called with category: {category}, version: {version}, runtime_version: {runtime_version}")

    if not version:
        version = runtime_version if runtime_version else DEFAULT_VERSION

    # Use expanded categories from learning_resources module
    categories = EXPANDED_CATEGORIES

    category_lower = category.lower()
    if category_lower not in categories:
        available = sorted(categories.keys())
        return format_error(f"Unknown category: {category}", {"available_categories": available})

    version_path = docs_path / version
    if not version_path.exists():
        return format_error(f"No documentation found for version {version}")

    try:
        # Find files matching the category
        category_files_data: List[Dict] = []
        keywords = categories[category_lower]

        for file in os.listdir(version_path):
            if file.endswith('.md'):
                file_lower = file.lower().replace('.md', '')
                # Check if filename contains any category keyword
                if any(keyword in file_lower for keyword in keywords):
                    # Try to get a brief description from the file
                    file_path = version_path / file
                    content = get_file_content_cached(str(file_path))
                    description = ""

                    if not content.startswith("Error"):
                        lines = content.split('\n')
                        for line in lines[:10]:
                            line = line.strip()
                            if line and not line.startswith('#') and not line.startswith('- '):
                                description = line[:100] + "..." if len(line) > 100 else line
                                break

                    category_files_data.append({
                        "file": file,
                        "description": description
                    })

        if not category_files_data:
            return format_error(f"No {category} documentation files found", {"version": version})

        # Sort by filename
        category_files_data.sort(key=lambda x: x["file"])
        return format_category_docs(category, version, category_files_data)

    except Exception as e:
        logger.error(f"Error browsing documentation: {str(e)}")
        return format_error(f"Error browsing documentation: {str(e)}")


def verify_laravel_feature_impl(docs_path: Path, feature: str, version: Optional[str] = None, runtime_version: Optional[str] = None) -> str:
    """Lightweight verification of Laravel feature existence via file pattern matching.

    This tool checks if a feature/topic exists in Laravel docs WITHOUT reading file contents.
    Uses fast Path.glob() for pattern matching on filenames only.

    Args:
        docs_path: Base path for documentation
        feature: Feature name or topic to verify (e.g., "blade", "eloquent", "sanctum")
        version: Specific Laravel version to check. If not provided, uses runtime_version or default.
        runtime_version: Runtime default version (from --version flag)

    Returns:
        TOON-encoded verification results with match status and matching files.
    """
    logger.debug(f"verify_laravel_feature_impl called with feature: {feature}, version: {version}")

    # Validate inputs
    if not feature.strip():
        return format_error("Feature name cannot be empty")

    # Determine version to use
    if not version:
        version = runtime_version if runtime_version else DEFAULT_VERSION

    version_path = docs_path / version
    if not version_path.exists():
        return format_error(
            f"Documentation not found for version {version}",
            {"suggestion": "Use update_laravel_docs() to fetch documentation"}
        )

    try:
        # Normalize feature name for comparison
        # Strip directory parts (e.g., "12.x/routing.md" -> "routing.md")
        # Strip .md suffix (e.g., "routing.md" -> "routing")
        feature_normalized = feature.strip()
        if "/" in feature_normalized:
            feature_normalized = feature_normalized.rsplit("/", 1)[-1]
        if feature_normalized.lower().endswith(".md"):
            feature_normalized = feature_normalized[:-3]
        feature_lower = feature_normalized.lower()

        # Strategy 1: Exact filename match (e.g., "blade" -> "blade.md")
        exact_match = version_path / f"{feature_lower}.md"
        exact_files = [exact_match.name] if exact_match.exists() else []

        # Strategy 2: Partial matches (e.g., "auth" matches "authentication.md", "authorization.md")
        # Use glob to find all .md files, then filter
        all_md_files = list(version_path.glob("*.md"))
        partial_matches = [
            f.name for f in all_md_files
            if feature_lower in f.stem.lower() and f.name not in exact_files
        ]

        # Combine results
        found = len(exact_files) + len(partial_matches) > 0

        return format_feature_verification(
            feature=feature,
            version=version,
            found=found,
            exact_matches=exact_files,
            partial_matches=partial_matches
        )

    except Exception as e:
        logger.error(f"Error verifying feature '{feature}': {str(e)}")
        return format_error(f"Error verifying feature: {str(e)}")


def compare_laravel_versions_impl(docs_path: Path, from_version: str, to_version: str, file_filter: Optional[str] = None, runtime_version: Optional[str] = None) -> str:
    """Compare documentation files between two Laravel versions.

    Shows which documentation files were added, removed, or persist between versions.
    Also includes git metadata diff (commit info, sync dates).
    NO content diffing - just file-level comparison for speed.

    Args:
        docs_path: Base path for documentation
        from_version: Starting Laravel version (e.g., "11.x")
        to_version: Target Laravel version (e.g., "12.x")
        file_filter: Optional substring to filter files (e.g., "auth" shows only auth-related changes)
        runtime_version: Runtime default version (from --version flag)

    Returns:
        TOON-encoded version comparison with added/removed/common files and metadata.
    """
    logger.debug(f"compare_laravel_versions_impl called: {from_version} -> {to_version}, filter: {file_filter}")

    # Validate versions
    if from_version not in SUPPORTED_VERSIONS:
        return format_error(
            f"Invalid source version: {from_version}",
            {"supported_versions": SUPPORTED_VERSIONS}
        )
    if to_version not in SUPPORTED_VERSIONS:
        return format_error(
            f"Invalid target version: {to_version}",
            {"supported_versions": SUPPORTED_VERSIONS}
        )
    if from_version == to_version:
        return format_error("Source and target versions cannot be the same")

    from_path = docs_path / from_version
    to_path = docs_path / to_version

    # Check both versions exist
    if not from_path.exists():
        return format_error(
            f"Documentation not found for version {from_version}",
            {"suggestion": "Use update_laravel_docs() to fetch documentation"}
        )
    if not to_path.exists():
        return format_error(
            f"Documentation not found for version {to_version}",
            {"suggestion": "Use update_laravel_docs() to fetch documentation"}
        )

    try:
        # Get file lists
        from_files = set(f.name for f in from_path.glob("*.md"))
        to_files = set(f.name for f in to_path.glob("*.md"))

        # Apply filter if provided
        if file_filter:
            filter_lower = file_filter.lower()
            from_files = {f for f in from_files if filter_lower in f.lower()}
            to_files = {f for f in to_files if filter_lower in f.lower()}

        # Calculate differences
        added_files = sorted(to_files - from_files)
        removed_files = sorted(from_files - to_files)
        common_files = sorted(from_files & to_files)

        # Get metadata for both versions
        from_metadata = get_laravel_docs_metadata(docs_path, from_version)
        to_metadata = get_laravel_docs_metadata(docs_path, to_version)

        return format_version_comparison(
            from_version=from_version,
            to_version=to_version,
            added_files=added_files,
            removed_files=removed_files,
            common_files=common_files,
            from_metadata=from_metadata,
            to_metadata=to_metadata,
            file_filter=file_filter
        )

    except Exception as e:
        logger.error(f"Error comparing versions {from_version} -> {to_version}: {str(e)}")
        return format_error(f"Error comparing versions: {str(e)}")


def find_laravel_docs_for_need_impl(docs_path: Path, need: str, version: Optional[str] = None, runtime_version: Optional[str] = None) -> str:
    """Find Laravel documentation for a specific user need.

    Args:
        docs_path: Base path for documentation
        need: User need description (e.g., "upload files", "send emails")
        version: Specific Laravel version to search. If not provided, uses default version.
        runtime_version: Runtime default version (from --version flag)

    Returns:
        TOON-encoded list of relevant documentation files.
    """
    logger.debug(f"find_laravel_docs_for_need_impl called with need: {need}")

    if not need.strip():
        return format_error("Need description cannot be empty")

    if not version:
        version = runtime_version if runtime_version else DEFAULT_VERSION

    # Get docs for the need using the learning_resources mappings
    docs = get_docs_for_need(need)

    if not docs:
        # Try fuzzy matching on the need
        need_lower = need.lower()
        all_needs = list(NEED_MAPPINGS.keys())
        suggestions = [n for n in all_needs if any(word in n for word in need_lower.split())][:5]

        return format_error(
            f"No documentation found for need: '{need}'",
            {"suggestions": suggestions} if suggestions else None
        )

    # Filter to only docs that exist in the version
    version_path = docs_path / version
    existing_docs = []

    if version_path.exists():
        available_files = set(f.replace('.md', '') for f in os.listdir(version_path) if f.endswith('.md'))
        for doc in docs:
            # Handle external and package docs differently
            if doc.startswith('external/') or doc.startswith('packages/'):
                existing_docs.append(doc)
            elif doc in available_files:
                existing_docs.append(f"{version}/{doc}.md")

    if not existing_docs:
        return format_error(
            f"No documentation files found for need: '{need}' in version {version}",
            {"suggested_docs": docs}
        )

    return format_need_docs(need, existing_docs, "core")


def get_laravel_learning_path_impl(path_name: str) -> str:
    """Get a specific curated learning path.

    Args:
        path_name: The learning path identifier (e.g., "getting-started", "api-development")

    Returns:
        TOON-encoded learning path with ordered documentation files.
    """
    logger.debug(f"get_laravel_learning_path_impl called with path_name: {path_name}")

    if not path_name.strip():
        # Return list of all available paths
        paths = list_learning_paths()
        return format_learning_paths_list(paths)

    path_data = get_learning_path(path_name)

    if not path_data:
        available_paths = list(LEARNING_PATHS.keys())
        return format_error(
            f"Learning path '{path_name}' not found",
            {"available_paths": available_paths}
        )

    # Convert DifficultyLevel enum to string for serialization
    result = dict(path_data)
    result["id"] = path_name
    if isinstance(result.get("difficulty"), DifficultyLevel):
        result["difficulty"] = result["difficulty"].value

    return format_learning_path(result)


def list_laravel_learning_paths_impl() -> str:
    """List all available learning paths.

    Returns:
        TOON-encoded list of learning paths with summaries.
    """
    logger.debug("list_laravel_learning_paths_impl called")

    paths = list_learning_paths()
    return format_learning_paths_list(paths)


def get_laravel_content_by_difficulty_impl(docs_path: Path, difficulty: str, version: Optional[str] = None, runtime_version: Optional[str] = None) -> str:
    """Get Laravel documentation filtered by difficulty level.

    Args:
        docs_path: Base path for documentation
        difficulty: Difficulty level ("beginner", "intermediate", "advanced")
        version: Specific Laravel version to search. If not provided, uses default version.
        runtime_version: Runtime default version (from --version flag)

    Returns:
        TOON-encoded list of documentation files at the specified difficulty level.
    """
    logger.debug(f"get_laravel_content_by_difficulty_impl called with difficulty: {difficulty}")

    # Validate difficulty level
    try:
        difficulty_level = DifficultyLevel(difficulty.lower())
    except ValueError:
        valid_levels = [level.value for level in DifficultyLevel]
        return format_error(
            f"Invalid difficulty level: '{difficulty}'",
            {"valid_levels": valid_levels}
        )

    if not version:
        version = runtime_version if runtime_version else DEFAULT_VERSION

    # Get topics at this difficulty level
    topics = get_topics_by_difficulty(difficulty_level)

    # Filter to only topics that exist in the version
    version_path = docs_path / version
    existing_docs = []

    if version_path.exists():
        available_files = set(f.replace('.md', '') for f in os.listdir(version_path) if f.endswith('.md'))
        for topic in topics:
            if topic in available_files:
                existing_docs.append(f"{version}/{topic}.md")

    return format_difficulty_content(difficulty_level.value, existing_docs, len(existing_docs))


def get_related_laravel_packages_impl(package: str) -> str:
    """Get packages related to a specific Laravel package.

    Args:
        package: Package identifier (e.g., "laravel/sanctum")

    Returns:
        TOON-encoded list of related packages.
    """
    logger.debug(f"get_related_laravel_packages_impl called with package: {package}")

    if not package.strip():
        return format_error("Package name cannot be empty")

    # Normalize package name
    package_lower = package.lower().strip()

    # Try exact match first
    related = get_related_packages(package_lower)

    # If not found, try partial match
    if not related:
        for pkg_id in RELATED_PACKAGES.keys():
            if package_lower in pkg_id.lower() or pkg_id.lower() in package_lower:
                related = RELATED_PACKAGES[pkg_id]
                package = pkg_id
                break

    if not related:
        available_packages = list(RELATED_PACKAGES.keys())
        return format_error(
            f"No related packages found for: '{package}'",
            {"available_packages": available_packages[:10]}
        )

    return format_related_packages(package, related)


def search_laravel_learning_resources_impl(
    docs_path: Path,
    query: str,
    sources: Optional[List[str]] = None,
    runtime_version: Optional[str] = None
) -> str:
    """Search through learning resources for a specific term.

    Args:
        docs_path: Base path for documentation
        query: Search term to look for
        sources: Specific sources to search (e.g., ["laravel-bootcamp", "laravel-blog"])
        runtime_version: Runtime default version (from --version flag)

    Returns:
        TOON-encoded search results from learning resources.
    """
    logger.debug(f"search_laravel_learning_resources_impl called with query: {query}, sources: {sources}")

    if not query.strip():
        return format_error("Search query cannot be empty")

    learning_dir = docs_path / "learning_resources"

    if not learning_dir.exists():
        return format_error(
            "No learning resources found",
            {"suggestion": "Use update_learning_docs() to fetch learning resources first"}
        )

    results_data: List[Dict] = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)

    # Determine which sources to search
    if sources:
        search_dirs = [learning_dir / source for source in sources if (learning_dir / source).exists()]
    else:
        search_dirs = [d for d in learning_dir.iterdir() if d.is_dir()]

    for source_dir in search_dirs:
        source_name = source_dir.name
        source_matches: List[Dict] = []

        for file_path in source_dir.glob("*.md"):
            try:
                content = get_file_content_cached(str(file_path))
                if not content.startswith("Error") and not content.startswith("File not found"):
                    if pattern.search(content):
                        count = len(pattern.findall(content))
                        source_matches.append({
                            "file": file_path.name,
                            "matches": count
                        })
            except Exception as e:
                logger.warning(f"Error searching {file_path}: {str(e)}")
                continue

        if source_matches:
            results_data.append({
                "source": source_name,
                "files": source_matches
            })

    if not results_data:
        return format_error(f"No results found for '{query}' in learning resources")

    return toon_encode({
        "query": query,
        "results": results_data,
        "source_count": len(results_data)
    })


def list_laravel_learning_resources_impl(docs_path: Path, source: Optional[str] = None) -> str:
    """List available learning resources.

    Args:
        docs_path: Base path for documentation
        source: Specific source to list (e.g., "laravel-bootcamp")

    Returns:
        TOON-encoded list of learning resources.
    """
    logger.debug(f"list_laravel_learning_resources_impl called with source: {source}")

    learning_dir = docs_path / "learning_resources"

    if not learning_dir.exists():
        return format_error(
            "No learning resources found",
            {"suggestion": "Use update_learning_docs() to fetch learning resources first"}
        )

    if source:
        source_dir = learning_dir / source
        if not source_dir.exists():
            available_sources = [d.name for d in learning_dir.iterdir() if d.is_dir()]
            return format_error(
                f"Learning source '{source}' not found",
                {"available_sources": available_sources}
            )

        # List files in specific source
        files = []
        for file_path in source_dir.glob("*.md"):
            files.append({
                "file": file_path.name,
                "size": file_path.stat().st_size
            })

        return format_learning_resources(source, files)

    # List all sources
    sources_data: List[Dict] = []
    for source_dir in learning_dir.iterdir():
        if source_dir.is_dir():
            file_count = len(list(source_dir.glob("*.md")))
            metadata_path = source_dir / ".cache_metadata.json"

            source_info = {
                "source": source_dir.name,
                "file_count": file_count
            }

            if metadata_path.exists():
                try:
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    source_info["name"] = metadata.get("name", source_dir.name)
                    source_info["difficulty"] = metadata.get("difficulty", "mixed")
                except Exception:
                    pass

            sources_data.append(source_info)

    return toon_encode({
        "count": len(sources_data),
        "sources": sources_data
    })


def list_laravel_categories_impl() -> str:
    """List all available documentation categories.

    Returns:
        TOON-encoded list of categories.
    """
    logger.debug("list_laravel_categories_impl called")

    categories = list_categories()
    categories_with_counts = []

    for cat in categories:
        docs = get_category_docs(cat)
        categories_with_counts.append({
            "category": cat,
            "doc_count": len(docs)
        })

    return toon_encode({
        "count": len(categories_with_counts),
        "categories": categories_with_counts
    })


def clear_caches():
    """Clear all caches."""
    with _cache_lock:
        _file_content_cache.clear()
        _search_result_cache.clear()
    logger.info("Caches cleared")