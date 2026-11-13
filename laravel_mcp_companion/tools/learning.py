"""The curated learning tools: reading orders and a browsable index.

These two are shipped and tested but sit outside the versioning guarantee
(`stable=False`). They answer from hand-written tables that need a person to
keep them current, and their shape may change in a minor release as that
content does.
"""

from pathlib import Path
from typing import Annotated, Any, Dict, List, Optional

from fastmcp import Context
from pydantic import Field

from .. import mcp_tools
from ..learning_resources import (
    EXPANDED_CATEGORIES,
    LEARNING_PATHS,
    DifficultyLevel,
    get_difficulty_for_topic,
)
from .common import default_version, require_version
from .errors import ToolFailure
from .registry import companion, tool

_LEARNING = frozenset({"learning", "read"})


# --- get_laravel_learning_path ------------------------------------------------

PATH_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["count", "paths"],
    "properties": {
        "count": {"type": "integer"},
        "paths": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "name", "description", "difficulty", "estimated_hours", "doc_count"],
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "difficulty": {"type": "string", "enum": [level.value for level in DifficultyLevel]},
                    "estimated_hours": {"type": "number"},
                    "doc_count": {"type": "integer"},
                    "docs": {
                        "type": "array", "items": {"type": "string"},
                        "description": "The pages to read, in order. Present when one path was asked for",
                    },
                    "next_path": {"type": "string", "description": "The path that follows this one, if any"},
                },
            },
        },
    },
}

PATH_DESCRIPTION = """Get a curated reading order through the Laravel documentation.

A learning path is an ordered list of framework pages for a goal such as getting started or building an API. With `path_name`, returns that path and its pages in order. Without one, lists the paths; a client that supports it is asked which the user wants."""


def _summary(path_id: str) -> Dict[str, Any]:
    path = LEARNING_PATHS[path_id]
    return {
        "id": path_id,
        "name": path["name"],
        "description": path["description"],
        "difficulty": getattr(path["difficulty"], "value", path["difficulty"]),
        "estimated_hours": path.get("estimated_hours", 0),
        "doc_count": len(path.get("docs", [])),
    }


def learning_paths(path_name: str = "") -> Dict[str, Any]:
    wanted = path_name.strip()
    if not wanted:
        return {"count": len(LEARNING_PATHS), "paths": [_summary(path_id) for path_id in LEARNING_PATHS]}
    if wanted not in LEARNING_PATHS:
        raise ToolFailure("not_found", f"No learning path {path_name!r}", {"available_paths": list(LEARNING_PATHS)})
    path = LEARNING_PATHS[wanted]
    entry = _summary(wanted)
    entry["docs"] = [f"{doc}.md" for doc in path.get("docs", [])]
    if path.get("next_path"):
        entry["next_path"] = path["next_path"]
    return {"count": 1, "paths": [entry]}


@tool("get_laravel_learning_path", description=PATH_DESCRIPTION, output_schema=PATH_SCHEMA, tags=_LEARNING, stable=False)
async def get_laravel_learning_path(path_name: str = "", ctx: Context = None) -> Dict[str, Any]:  # type: ignore[assignment]
    """Get a learning path, or list them.

    Args:
        path_name: The path's id (e.g. "getting-started"). Leave empty to list the paths
    """
    if not path_name.strip() and ctx is not None:
        choices = {
            path_id: {"title": f"{summary['name']} ({summary['difficulty']}, ~{summary['estimated_hours']}h)"}
            for path_id, summary in ((path_id, _summary(path_id)) for path_id in LEARNING_PATHS)
        }
        try:
            # mypy resolves the elicit overload's unbound TypeVar to None for
            # the titled-enum dict form; the runtime accepts it.
            answer = await ctx.elicit("Which learning path would you like?", response_type=choices)  # type: ignore[arg-type]
            if answer.action == "accept":
                path_name = str(answer.data)
        except Exception:
            # The client cannot be asked; the listing is the answer.
            pass
    return learning_paths(path_name)


# --- browse_docs_by_category --------------------------------------------------

BROWSE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["version"],
    "properties": {
        "version": {"type": "string"},
        "category": {"type": "string"},
        "difficulty": {"type": "string", "enum": [level.value for level in DifficultyLevel]},
        "count": {"type": "integer", "description": "How many pages matched. Present when a filter was given"},
        "docs": {
            "type": "array",
            "description": "The matching pages. Present when a filter was given",
            "items": {
                "type": "object",
                "required": ["file", "title", "difficulty", "categories"],
                "properties": {
                    "file": {"type": "string"},
                    "title": {"type": "string"},
                    "difficulty": {"type": "string"},
                    "categories": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "categories": {
            "type": "array",
            "description": "Every category with its page count. Present when no filter was given",
            "items": {
                "type": "object",
                "required": ["name", "doc_count"],
                "properties": {"name": {"type": "string"}, "doc_count": {"type": "integer"}},
            },
        },
    },
}

BROWSE_DESCRIPTION = """Browse the framework documentation by topic or by difficulty.

With no arguments: the categories (authentication, database, testing and so on) and how many pages each holds for the selected Laravel version. With `category`, `difficulty` ("beginner", "intermediate" or "advanced") or both: the matching pages, each with its title, difficulty and categories. For a specific question, search is the better tool; this one is for seeing what exists in an area."""


def _categories_of(stem: str) -> List[str]:
    return sorted(category for category, keywords in EXPANDED_CATEGORIES.items() if any(keyword in stem for keyword in keywords))


def _title(path: Path, fallback: str) -> str:
    for line in mcp_tools.get_file_content_cached(str(path)).split("\n", 20)[:20]:
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def browse_docs(
    docs_path: Path,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    version: Optional[str] = None,
    runtime_version: Optional[str] = None,
) -> Dict[str, Any]:
    require_version(version)
    version = version or default_version(runtime_version)

    wanted_category = category.lower().strip() if category else None
    if wanted_category is not None and wanted_category not in EXPANDED_CATEGORIES:
        raise ToolFailure("not_found", f"No category {category!r}", {"available_categories": sorted(EXPANDED_CATEGORIES)})

    wanted_difficulty = difficulty.lower().strip() if difficulty else None
    levels = [level.value for level in DifficultyLevel]
    if wanted_difficulty is not None and wanted_difficulty not in levels:
        raise ToolFailure("invalid_argument", f"Unknown difficulty {difficulty!r}", {"valid_difficulties": levels})

    version_dir = Path(docs_path) / version
    if not version_dir.is_dir():
        raise ToolFailure("not_found", f"No documentation on this server for Laravel {version}", {"version": version})

    pages = []
    for name, path in sorted(mcp_tools.list_contained_markdown(version_dir)):
        stem = name[: -len(".md")].lower()
        pages.append((name, path, _categories_of(stem), get_difficulty_for_topic(stem).value))

    if wanted_category is None and wanted_difficulty is None:
        # Counted from the same pages a filtered call would return, so the
        # two can never disagree.
        counts = {name: 0 for name in sorted(EXPANDED_CATEGORIES)}
        for _name, _path, categories, _level in pages:
            for name in categories:
                counts[name] += 1
        return {"version": version, "categories": [{"name": name, "doc_count": count} for name, count in counts.items()]}

    docs = [
        {"file": f"{version}/{name}", "title": _title(path, name), "difficulty": level, "categories": categories}
        for name, path, categories, level in pages
        if (wanted_category is None or wanted_category in categories)
        and (wanted_difficulty is None or wanted_difficulty == level)
    ]
    result: Dict[str, Any] = {"version": version, "count": len(docs), "docs": docs}
    if wanted_category:
        result["category"] = wanted_category
    if wanted_difficulty:
        result["difficulty"] = wanted_difficulty
    return result


@tool("browse_docs_by_category", description=BROWSE_DESCRIPTION, output_schema=BROWSE_SCHEMA, tags=_LEARNING, stable=False)
def browse_docs_by_category(
    category: Optional[str] = None,
    difficulty: Annotated[Optional[str], Field(json_schema_extra={"enum": [*(level.value for level in DifficultyLevel), None]})] = None,
    version: Optional[str] = None,
    ctx: Context = None,  # type: ignore[assignment]
) -> Dict[str, Any]:
    """Browse framework documentation by category and difficulty.

    Args:
        category: A topic area (e.g. "authentication", "database"). Omit both filters to list the categories
        difficulty: "beginner", "intermediate" or "advanced"
        version: Laravel version (e.g. "12.x"). Defaults to the server's configured version
    """
    tc = companion(ctx)
    return browse_docs(tc.docs_path, category, difficulty, version, tc.runtime_version)
