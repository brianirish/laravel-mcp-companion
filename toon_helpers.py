"""TOON format helpers for Laravel MCP Companion.

This module provides helper functions for encoding MCP tool responses
in TOON (Token-Oriented Object Notation) format for optimal token efficiency.
"""

from typing import Any, Dict, List, Optional
from toon_format import encode


def toon_encode(data: Any) -> str:
    """Encode data to TOON format with error handling."""
    try:
        return encode(data)
    except Exception:
        # Fallback to string representation if encoding fails
        return str(data)


def format_version_list(versions: List[Dict[str, Any]]) -> str:
    """Format version metadata list for list_laravel_docs."""
    return toon_encode(versions)


def format_search_results(
    query: str,
    core_results: List[Dict[str, Any]],
    external_results: Optional[List[Dict[str, Any]]] = None
) -> str:
    """Format search results for search_laravel_docs."""
    data = {
        "query": query,
        "core_results": core_results,
        "core_count": len(core_results),
    }
    if external_results:
        data["external_results"] = external_results
        data["external_count"] = len(external_results)
    return toon_encode(data)


def format_package_list(packages: List[Dict[str, Any]], context: str) -> str:
    """Format package recommendations list."""
    return toon_encode({
        "context": context,
        "count": len(packages),
        "packages": packages
    })


def format_package_info(package: Dict[str, Any]) -> str:
    """Format single package information."""
    return toon_encode(package)


def format_service_list(services: List[Dict[str, Any]]) -> str:
    """Format Laravel services list."""
    return toon_encode({
        "services": services,
        "count": len(services)
    })


def format_category_docs(
    category: str,
    version: str,
    files: List[Dict[str, str]]
) -> str:
    """Format documentation files by category."""
    return toon_encode({
        "category": category,
        "version": version,
        "count": len(files),
        "files": files
    })


def format_doc_structure(filename: str, headings: List[Dict[str, Any]]) -> str:
    """Format document structure/headings."""
    return toon_encode({
        "filename": filename,
        "headings": headings
    })


def format_error(message: str, context: Optional[Dict[str, Any]] = None) -> str:
    """Format error messages consistently."""
    data: Dict[str, Any] = {"error": message}
    if context:
        data["context"] = context
    return toon_encode(data)
