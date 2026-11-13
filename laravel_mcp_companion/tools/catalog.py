"""The tools that answer from the curated package catalog and the service table."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastmcp import Context

from .. import catalog
from ..docs_updater import source_statuses
from .errors import ToolFailure
from .registry import companion, tool

_PACKAGE_PROPERTIES: Dict[str, Any] = {
    "id": {"type": "string", "description": "The Composer name, e.g. laravel/cashier"},
    "name": {"type": "string"},
    "description": {"type": "string"},
    "categories": {"type": "array", "items": {"type": "string"}},
    "use_cases": {"type": "array", "items": {"type": "string"}},
    "installation": {"type": "string", "description": "The command that installs it"},
    "features": {"type": "array", "items": {"type": "string"}, "description": "What is typically built with it"},
    "related": {"type": "array", "items": {"type": "string"}, "description": "Ids of packages often used alongside"},
    "documentation_link": {"type": "string", "description": "A laravel://, laravel-external:// or laravel-package:// resource URI, or a URL"},
    "legacy": {"type": "boolean", "description": "True for a package that newer projects no longer start with"},
    "superseded_by": {"type": "string"},
}


# --- get_laravel_package ------------------------------------------------------

PACKAGE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["count", "packages"],
    "properties": {
        "count": {"type": "integer"},
        "category": {"type": "string", "description": "The category asked for, when one was"},
        "categories": {
            "type": "array", "items": {"type": "string"},
            "description": "Every category in the catalog. Present when the whole catalog was listed",
        },
        "packages": {
            "type": "array",
            "items": {"type": "object", "required": ["id", "name", "description"], "properties": _PACKAGE_PROPERTIES},
        },
    },
}

PACKAGE_DESCRIPTION = """Look up Laravel packages in the curated catalog.

With `name`: everything about one package, including what it is for, how to install it, what is typically built with it, the packages commonly used alongside it and where its documentation is. With `category`: the packages in that category. With neither: the whole catalog in brief, and the list of categories. The catalog is a hand-picked set of first-party and widely used community packages, not all of Packagist."""


def get_package(name: Optional[str] = None, category: Optional[str] = None) -> Dict[str, Any]:
    if name and category:
        raise ToolFailure("invalid_argument", "Give name or category, not both")

    if name:
        package_id = catalog.find_package(name)
        if package_id is None:
            raise ToolFailure("not_found", f"No package matching {name!r} in the catalog", {"available": sorted(catalog.PACKAGE_CATALOG)})
        return {"count": 1, "packages": [catalog.package_record(package_id)]}

    if category:
        ids = catalog.packages_in_category(category)
        if not ids:
            raise ToolFailure("not_found", f"No catalog category {category!r}", {"available_categories": catalog.all_categories()})
        return {"count": len(ids), "category": category.lower().strip(), "packages": [catalog.package_summary(i) for i in ids]}

    ids = list(catalog.PACKAGE_CATALOG)
    return {"count": len(ids), "categories": catalog.all_categories(), "packages": [catalog.package_summary(i) for i in ids]}


@tool("get_laravel_package", description=PACKAGE_DESCRIPTION, output_schema=PACKAGE_SCHEMA, tags=frozenset({"packages", "read"}))
def get_laravel_package(name: Optional[str] = None, category: Optional[str] = None, ctx: Context = None) -> Dict[str, Any]:  # type: ignore[assignment]
    """Look up packages in the curated catalog.

    Args:
        name: A package, by Composer name ("laravel/cashier") or short name ("cashier")
        category: A category to list (e.g. "payment", "authentication")
    """
    return get_package(name, category)


# --- recommend_laravel_packages -----------------------------------------------

RECOMMEND_LIMIT = 5

RECOMMEND_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["use_case", "count", "packages"],
    "properties": {
        "use_case": {"type": "string"},
        "count": {"type": "integer", "description": "0 when nothing in the catalog fits"},
        "packages": {
            "type": "array",
            "description": "Best match first",
            "items": {"type": "object", "required": ["id", "name", "description"], "properties": _PACKAGE_PROPERTIES},
        },
    },
}

RECOMMEND_DESCRIPTION = """Recommend packages for something the user wants to build.

Describe the need in ordinary words ("accept subscription payments", "role-based permissions", "real-time notifications") and get the catalog's best matches, best first, each with its install command and documentation link. Packages a new project would no longer start with rank below current ones. No match is a normal result with count 0."""


def recommend_packages(use_case: str) -> Dict[str, Any]:
    if not use_case.strip():
        raise ToolFailure("invalid_argument", "use_case is empty")
    matches = catalog.search_by_use_case(use_case)[:RECOMMEND_LIMIT]
    return {
        "use_case": use_case,
        "count": len(matches),
        "packages": [catalog.package_record(match["id"]) for match in matches],
    }


@tool("recommend_laravel_packages", description=RECOMMEND_DESCRIPTION, output_schema=RECOMMEND_SCHEMA, tags=frozenset({"packages", "read"}))
def recommend_laravel_packages(use_case: str, ctx: Context = None) -> Dict[str, Any]:  # type: ignore[assignment]
    """Recommend packages for a need.

    Args:
        use_case: What the user wants to build or solve, in plain words
    """
    return recommend_packages(use_case)


# --- get_laravel_service_info -------------------------------------------------

SERVICE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["id", "name", "documentation_url", "status"],
    "properties": {
        "id": {"type": "string", "description": "Pass to list_laravel_docs as `name` to list its pages"},
        "name": {"type": "string"},
        "documentation_url": {"type": "string"},
        "status": {"type": "string", "enum": ["ok", "partial", "missing"], "description": "Whether this server holds its documentation"},
        "pages": {"type": "integer"},
        "pages_expected": {"type": "integer"},
        "version": {"type": "string", "description": "The major version the pages describe, when the service has one"},
        "last_synced": {"type": "string"},
    },
}

SERVICE_DESCRIPTION = """Describe one of Laravel's first-party services and what this server holds for it.

Services are Forge, Vapor, Envoyer, Nova, Cloud, Nightwatch and Herd. Returns where the service's documentation lives, how many of its pages are on this server, the major version they describe and when they were last synced. To read the pages, search with sources=["services"] or list them with list_laravel_docs."""


def service_info(tc: Any, service: str) -> Dict[str, Any]:
    fetcher = tc.updater.external_fetcher
    key = service.lower().strip()
    config = fetcher.get_service_info(key)
    if not config:
        raise ToolFailure("not_found", f"No service {service!r}", {"available_services": fetcher.list_available_services()})

    info: Dict[str, Any] = {
        "id": key,
        "name": config.get("name", key),
        "documentation_url": config.get("base_url", ""),
        "status": "missing",
    }
    for status in source_statuses(Path(tc.docs_path), max_age=None):
        if status["kind"] == "service" and status["name"] == key:
            if status["problem"] not in ("never synced", "metadata unreadable", "no sync timestamp"):
                info["status"] = "partial" if status["problem"] else "ok"
            if isinstance(status["fetched"], int):
                info["pages"] = status["fetched"]
            if isinstance(status["total"], int):
                info["pages_expected"] = status["total"]
            if status["version"]:
                info["version"] = str(status["version"])
            if status["synced_at"]:
                info["last_synced"] = datetime.fromtimestamp(status["synced_at"], timezone.utc).strftime("%Y-%m-%d")
    return info


@tool("get_laravel_service_info", description=SERVICE_DESCRIPTION, output_schema=SERVICE_SCHEMA, tags=frozenset({"services", "read"}))
def get_laravel_service_info(service: str, ctx: Context = None) -> Dict[str, Any]:  # type: ignore[assignment]
    """Describe a first-party Laravel service.

    Args:
        service: forge, vapor, envoyer, nova, cloud, nightwatch or herd
    """
    return service_info(companion(ctx), service)


__all__: List[str] = ["get_package", "recommend_packages", "service_info"]
