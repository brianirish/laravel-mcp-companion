"""Output schemas for the tools that return structured content.

Shapes document the success payload. `required` is deliberately empty and
`additionalProperties` is left at its default: every one of these tools
returns ``{"error": ..., "context": ...}`` on failure, and that shape must
validate against the same schema.
"""

from typing import Any, Dict

_ERROR_PROPERTIES: Dict[str, Any] = {
    "error": {"type": "string", "description": "Present instead of the success keys when the call failed"},
    "context": {"type": "object", "description": "Extra detail accompanying an error"},
}


def _schema(properties: Dict[str, Any]) -> Dict[str, Any]:
    # Tool-defined keys win: get_laravel_package_recommendations uses "context"
    # as a string in its success payload, and its error paths never attach an
    # error context, so the collision is harmless as long as we don't clobber.
    merged = {**_ERROR_PROPERTIES, **properties}
    return {"type": "object", "properties": merged}


OUTPUT_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "search_laravel_docs": _schema({
        "query": {"type": "string"},
        "scope": {"type": "string", "description": "Comma-separated versions/services searched"},
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "file": {"type": "string"},
                    "anchor": {"type": "string"},
                    "heading": {"type": "string"},
                    "score": {"type": "number"},
                    "snippet": {"type": "string"},
                },
            },
        },
    }),
    "laravel_docs_info": _schema({
        "version": {"type": "string"},
        "documentation_date": {"type": "string"},
        "last_updated": {"type": "string"},
        "commit_sha": {"type": "string"},
        "commit_date": {"type": "string"},
        "commit_message": {"type": "string"},
        "github_url": {"type": "string"},
        # all-versions summary shape
        "documentation_current_to": {"type": "string"},
        "copy_age_days": {"description": "Days since upstream last changed, or 'unknown'"},
        "default_version": {"type": "string"},
        "versions": {"type": "array", "items": {"type": "object"}},
        "note": {"type": "string"},
    }),
    "list_laravel_docs": _schema({
        "version": {"type": "string"},
        "last_updated": {"type": "string"},
        "commit": {"type": "string"},
        "file_count": {"type": "integer"},
        "files": {"type": "array", "items": {"type": "string"}},
        # all-versions shape
        "count": {"type": "integer"},
        "versions": {"type": "array", "items": {"type": "object"}},
    }),
    "get_laravel_package_recommendations": _schema({
        "context": {"type": "string", "description": "Echo of the use case searched"},
        "count": {"type": "integer"},
        "packages": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "use_cases": {"type": "array", "items": {"type": "string"}},
                    "installation": {"type": "string"},
                    "documentation_link": {"type": "string"},
                },
            },
        },
    }),
    "get_laravel_package_info": _schema({
        "id": {"type": "string"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "use_cases": {"type": "array", "items": {"type": "string"}},
        "installation": {"type": "string"},
        "documentation_link": {"type": "string"},
        "related_packages": {"type": "array", "items": {"type": "string"}},
        "categories": {"type": "array", "items": {"type": "string"}},
    }),
}
