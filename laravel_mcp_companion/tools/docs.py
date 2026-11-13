"""The tools that read, list, describe, compare and update documentation."""

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Any, Dict, List, Optional

import anyio.to_thread
from fastmcp import Context
from pydantic import Field

from .. import mcp_tools
from ..doc_search import chunk_markdown
from ..docs_updater import DocsUpdater, source_statuses
from .common import default_version, locate, read_text, require_version, slugify
from .errors import ToolFailure
from .registry import Reply, companion, tool
from .search import section_id

_READ = frozenset({"docs", "read"})


# --- read_laravel_doc_section -------------------------------------------------

SECTION_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["file", "section", "heading", "content"],
    "properties": {
        "file": {"type": "string"},
        "version": {"type": "string", "description": "Laravel version, for a framework page"},
        "corpus": {"type": "string", "description": "The service, package or learning source, for any other page"},
        "section": {"type": "string"},
        "heading": {"type": "string"},
        "content": {"type": "string", "description": "The section as markdown; the same text as the result's text content"},
    },
}

SECTION_DESCRIPTION = """Read one section of a documentation page.

Give it a search result's `file` (as `filename`) and `section`, and it returns that section's markdown and nothing else. This is the cheap way to read: a whole page such as queues.md runs to tens of thousands of tokens, and an answer usually needs one section of it.

`section` may be an anchor ("dealing-with-failed-jobs"), a heading ("Dealing With Failed Jobs") or a heading written as a slug. If the section is not found, the error lists the sections the page does have."""


def read_section(docs_path: Path, filename: str, section: str, version: Optional[str] = None, runtime_version: Optional[str] = None) -> Reply:
    path, name, resolved_version, corpus = locate(docs_path, filename, version, runtime_version)
    wanted = section.strip().lstrip("#").strip()
    if not wanted:
        raise ToolFailure("invalid_argument", "section is empty")

    # Chunked under the name search indexes the page by (its path inside the
    # corpus), because a page with no heading of its own is titled by that
    # name, and the section id search hands out is derived from the title.
    indexed_name = name if resolved_version else name[len(corpus or "") + 1:]
    sections = chunk_markdown(read_text(path), indexed_name, resolved_version or corpus or "")
    lowered, slug = wanted.lower(), slugify(wanted)
    for candidate in sections:
        if (
            (candidate.anchor or "").lower() == lowered
            or candidate.heading.lower() == lowered
            or (slug and slugify(candidate.heading) == slug)
        ):
            content = candidate.text.strip()
            data: Dict[str, Any] = {
                "file": name,
                "section": section_id(candidate),
                "heading": candidate.heading,
                "content": content,
            }
            data["version" if resolved_version else "corpus"] = resolved_version or corpus
            return Reply(data=data, text=content)

    raise ToolFailure(
        "not_found",
        f"No section {section!r} in {filename}",
        {"available_sections": [section_id(candidate) for candidate in sections]},
    )


@tool("read_laravel_doc_section", description=SECTION_DESCRIPTION, output_schema=SECTION_SCHEMA, tags=_READ)
def read_laravel_doc_section(filename: str, section: str, version: Optional[str] = None, ctx: Context = None) -> Reply:  # type: ignore[assignment]
    """Read one section of a documentation page.

    Args:
        filename: The page, as search returns it: "queues.md", "12.x/queues.md" or "forge/servers/php.md"
        section: The section's anchor or heading, as search returns it
        version: Laravel version for a framework page named without one. Ignored for service, package and learning pages
    """
    tc = companion(ctx)
    return read_section(tc.docs_path, filename, section, version, tc.runtime_version)


# --- read_laravel_doc_content -------------------------------------------------

CONTENT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["file", "mode"],
    "properties": {
        "file": {"type": "string"},
        "version": {"type": "string", "description": "Laravel version, for a framework page"},
        "corpus": {"type": "string", "description": "The service, package or learning source, for any other page"},
        "mode": {"type": "string", "enum": ["full", "outline"]},
        "content": {"type": "string", "description": "mode=full: the whole page as markdown"},
        "headings": {
            "type": "array",
            "description": "mode=outline: every heading in order",
            "items": {
                "type": "object",
                "required": ["level", "text", "section"],
                "properties": {
                    "level": {"type": "integer"},
                    "text": {"type": "string"},
                    "section": {
                        "type": "string",
                        "description": "For a level-2 heading, what to pass to read_laravel_doc_section; empty otherwise",
                    },
                },
            },
        },
    },
}

CONTENT_DESCRIPTION = """Read a whole documentation page, or just its outline.

mode="outline" returns the page's headings, which is the way to see what a page covers before reading any of it. mode="full" returns the entire page as markdown. Full pages are large; when you want one topic, search and read_laravel_doc_section cost a fraction of the tokens."""

_FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
_HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
_ANCHOR_BEFORE = re.compile(r'<a name="([^"]+)"></a>\s*$')


def outline(markdown: str) -> List[Dict[str, Any]]:
    """Every heading of a page, skipping lines inside fenced code blocks, where
    a `#` begins a comment and not a heading."""
    headings: List[Dict[str, Any]] = []
    fence: Optional[str] = None
    previous = ""
    for line in markdown.split("\n"):
        opening = _FENCE.match(line)
        if fence is not None:
            if opening and opening.group(1)[0] == fence[0] and len(opening.group(1)) >= len(fence):
                fence = None
        elif opening:
            fence = opening.group(1)
        else:
            heading = _HEADING.match(line)
            if heading:
                level, text = len(heading.group(1)), heading.group(2).strip()
                anchor = _ANCHOR_BEFORE.search(previous)
                section = (anchor.group(1) if anchor else slugify(text)) if level == 2 else ""
                headings.append({"level": level, "text": text, "section": section})
        if line.strip():
            previous = line
    return headings


def read_content(docs_path: Path, filename: str, version: Optional[str] = None, mode: str = "full", runtime_version: Optional[str] = None) -> Any:
    if mode not in ("full", "outline"):
        raise ToolFailure("invalid_argument", f"mode must be \"full\" or \"outline\", not {mode!r}")
    path, name, resolved_version, corpus = locate(docs_path, filename, version, runtime_version)
    content = read_text(path)

    data: Dict[str, Any] = {"file": name, "mode": mode}
    data["version" if resolved_version else "corpus"] = resolved_version or corpus
    if mode == "outline":
        data["headings"] = outline(content)
        return data
    data["content"] = content
    return Reply(data=data, text=content)


@tool("read_laravel_doc_content", description=CONTENT_DESCRIPTION, output_schema=CONTENT_SCHEMA, tags=_READ)
def read_laravel_doc_content(
    filename: str,
    version: Optional[str] = None,
    mode: Annotated[str, Field(json_schema_extra={"enum": ["full", "outline"]})] = "full",
    ctx: Context = None,  # type: ignore[assignment]
) -> Any:
    """Read a whole documentation page or its outline.

    Args:
        filename: The page: "queues.md", "12.x/queues.md" or "forge/servers/php.md"
        version: Laravel version for a framework page named without one
        mode: "full" for the whole page, "outline" for its headings only
    """
    tc = companion(ctx)
    return read_content(tc.docs_path, filename, version, mode, tc.runtime_version)


# --- list_laravel_docs --------------------------------------------------------

LIST_SOURCES = ("core", "services", "packages", "learning")
_FAMILY_DIRECTORY = {"services": "external", "packages": "packages", "learning": "learning_resources"}

LIST_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["count", "collections"],
    "properties": {
        "count": {"type": "integer", "description": "How many collections follow"},
        "collections": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["source", "name", "file_count"],
                "properties": {
                    "source": {"type": "string", "enum": list(LIST_SOURCES)},
                    "name": {"type": "string", "description": "A Laravel version, or a service, package or learning source"},
                    "file_count": {"type": "integer"},
                    "files": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "File names ready for the read tools. Present when one collection was asked for",
                    },
                },
            },
        },
    },
}

LIST_DESCRIPTION = """List what documentation this server holds.

With no arguments: every collection (each Laravel version, service, package and learning source) with its page count. With `source`, only that kind. With `name` (a Laravel version such as "12.x", or a service or package such as "forge"), that collection's files, named the way the read tools accept them."""


def _collection_files(root: Path) -> List[str]:
    return sorted(name for name, _ in mcp_tools._iter_contained_markdown_recursive(root))


def list_docs(docs_path: Path, source: Optional[str] = None, name: Optional[str] = None) -> Dict[str, Any]:
    if source is not None and source not in LIST_SOURCES:
        raise ToolFailure("invalid_argument", f"Unknown source {source!r}", {"valid_sources": list(LIST_SOURCES)})
    if name is not None and not re.fullmatch(r"[A-Za-z0-9_-][A-Za-z0-9._-]*", name):
        raise ToolFailure("invalid_argument", f"{name!r} is not a collection name")

    collections: List[Dict[str, Any]] = []

    if source in (None, "core"):
        for version in mcp_tools.SUPPORTED_VERSIONS:
            if name not in (None, version):
                continue
            version_dir = Path(docs_path) / version
            if not version_dir.is_dir():
                continue
            files = sorted(file_name for file_name, _ in mcp_tools.list_contained_markdown(version_dir))
            if files:
                entry: Dict[str, Any] = {"source": "core", "name": version, "file_count": len(files)}
                if name:
                    entry["files"] = [f"{version}/{file_name}" for file_name in files]
                collections.append(entry)

    for kind, directory in _FAMILY_DIRECTORY.items():
        if source not in (None, kind):
            continue
        family_dir = Path(docs_path) / directory
        # The same enumeration search indexes and the read tools resolve
        # against, so a collection listed here can be searched and read.
        for collection in mcp_tools.contained_subdirectories(family_dir):
            if name not in (None, collection):
                continue
            files = _collection_files(family_dir / collection)
            if files:
                entry = {"source": kind, "name": collection, "file_count": len(files)}
                if name:
                    entry["files"] = [f"{collection}/{file_name}" for file_name in files]
                collections.append(entry)

    if name and not collections:
        raise ToolFailure("not_found", f"No documentation collection named {name!r}")
    return {"count": len(collections), "collections": collections}


@tool("list_laravel_docs", description=LIST_DESCRIPTION, output_schema=LIST_SCHEMA, tags=_READ)
def list_laravel_docs(
    source: Annotated[Optional[str], Field(json_schema_extra={"enum": [*LIST_SOURCES, None]})] = None,
    name: Optional[str] = None,
    ctx: Context = None,  # type: ignore[assignment]
) -> Dict[str, Any]:
    """List documentation collections, or the files of one.

    Args:
        source: Only this kind of collection: "core", "services", "packages" or "learning"
        name: One collection to list the files of: a Laravel version ("12.x") or a service, package or learning source ("forge", "livewire")
    """
    return list_docs(companion(ctx).docs_path, source, name)


# --- laravel_docs_info --------------------------------------------------------

INFO_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["documentation_current_to", "default_version", "versions", "sources"],
    "properties": {
        "documentation_current_to": {
            "type": "string",
            "description": "The date Laravel last changed any framework page in this copy, or \"unknown\"",
        },
        "copy_age_days": {"type": "integer", "description": "Days since that date. Absent when unknown"},
        "stale": {"type": "boolean", "description": "True when no version has changed for long enough that this copy is probably behind"},
        "note": {"type": "string", "description": "What to do about a stale copy. Present only when stale is true"},
        "default_version": {"type": "string"},
        "versions": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["version", "available"],
                "properties": {
                    "version": {"type": "string"},
                    "available": {"type": "boolean"},
                    "documentation_date": {"type": "string", "description": "When Laravel last changed this version's docs"},
                    "last_synced": {"type": "string"},
                    "commit": {"type": "string"},
                    "commit_message": {"type": "string"},
                    "commit_url": {"type": "string"},
                },
            },
        },
        "sources": {
            "type": "array",
            "description": "Every service, package and learning source",
            "items": {
                "type": "object",
                "required": ["name", "kind", "status"],
                "properties": {
                    "name": {"type": "string"},
                    "kind": {"type": "string", "enum": ["service", "package", "learning"]},
                    "status": {"type": "string", "enum": ["ok", "partial", "missing"]},
                    "pages": {"type": "integer"},
                    "pages_expected": {"type": "integer"},
                    "version": {"type": "string", "description": "The major the source's docs are on, when it has one"},
                    "last_synced": {"type": "string", "description": "Date of the last successful sync"},
                    "problem": {"type": "string"},
                },
            },
        },
    },
}

INFO_DESCRIPTION = """Report how current this server's documentation is.

For the framework docs: the date Laravel last changed each version, and the commit this copy was taken at. For every service, package and learning source: how many pages are held, which major version they describe, and when they were last synced. Use it when a user asks how up to date the documentation is, or before telling them something newer may exist. Pass `version` to get one Laravel version only."""


def _date(timestamp: Any) -> Optional[str]:
    if isinstance(timestamp, (int, float)):
        return datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-%d")
    parsed = mcp_tools.parse_timestamp(timestamp)
    return parsed.strftime("%Y-%m-%d") if parsed else None


def docs_info(docs_path: Path, version: Optional[str] = None, runtime_version: Optional[str] = None) -> Dict[str, Any]:
    require_version(version)

    versions: List[Dict[str, Any]] = []
    for candidate in ([version] if version else mcp_tools.SUPPORTED_VERSIONS):
        metadata = mcp_tools.get_laravel_docs_metadata(Path(docs_path), candidate)
        if not isinstance(metadata, dict) or "version" not in metadata:
            versions.append({"version": candidate, "available": False})
            continue
        entry: Dict[str, Any] = {"version": candidate, "available": True}
        documentation_date, _ = mcp_tools.get_documentation_date(docs_path, candidate)
        optional = {
            "documentation_date": documentation_date,
            "last_synced": _date(metadata.get("sync_time")),
            "commit": str(metadata.get("commit_sha") or "")[:7] or None,
            "commit_message": metadata.get("commit_message"),
            "commit_url": metadata.get("commit_url"),
        }
        entry.update({key: value for key, value in optional.items() if value})
        versions.append(entry)

    sources: List[Dict[str, Any]] = []
    for status in source_statuses(Path(docs_path), max_age=None):
        if status["problem"] in ("never synced", "metadata unreadable", "no sync timestamp"):
            label = "missing"
        else:
            label = "partial" if status["problem"] else "ok"
        entry = {"name": status["name"], "kind": status["kind"], "status": label}
        if isinstance(status["fetched"], int):
            entry["pages"] = status["fetched"]
        if isinstance(status["total"], int):
            entry["pages_expected"] = status["total"]
        if status["version"]:
            entry["version"] = str(status["version"])
        if status["synced_at"]:
            entry["last_synced"] = _date(status["synced_at"])
        if status["problem"]:
            entry["problem"] = status["problem"]
        sources.append(entry)

    current_to, age = mcp_tools.get_documentation_date(docs_path)
    info: Dict[str, Any] = {
        "documentation_current_to": current_to or "unknown",
        "default_version": default_version(runtime_version),
        "versions": versions,
        "sources": sources,
    }
    if age is not None and version is None:
        info["copy_age_days"] = age
        # Judged across versions, and only when all of them were asked about:
        # one old version means Laravel stopped changing that branch, which
        # is not a fault and not something anyone can act on.
        info["stale"] = mcp_tools.copy_is_stale(docs_path)
        if info["stale"]:
            info["note"] = (
                f"No Laravel version has changed in over {mcp_tools.DOCS_STALE_AFTER_DAYS} days, which "
                "suggests this copy is behind. Pull a newer image or package to get current documentation."
            )
    return info


@tool("laravel_docs_info", description=INFO_DESCRIPTION, output_schema=INFO_SCHEMA, tags=_READ)
def laravel_docs_info(version: Optional[str] = None, ctx: Context = None) -> Dict[str, Any]:  # type: ignore[assignment]
    """How current the documentation is, for every corpus.

    Args:
        version: Report this Laravel version only (e.g. "12.x"). Default: every version
    """
    tc = companion(ctx)
    return docs_info(tc.docs_path, version, tc.runtime_version)


# --- compare_laravel_versions -------------------------------------------------

COMPARE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["from_version", "to_version", "added_files", "removed_files", "common_files"],
    "properties": {
        "from_version": {"type": "string"},
        "to_version": {"type": "string"},
        "filter": {"type": "string", "description": "The file_filter that was applied, if any"},
        "added_files": {"type": "array", "items": {"type": "string"}, "description": "Pages in to_version only"},
        "removed_files": {"type": "array", "items": {"type": "string"}, "description": "Pages in from_version only"},
        "common_files": {"type": "array", "items": {"type": "string"}},
    },
}

COMPARE_DESCRIPTION = """Compare the documentation of two Laravel versions.

Lists the pages one version has and the other lacks, which is the quickest way to see what an upgrade introduces or retires. To see how a page that exists in both versions changed, read it from each with read_laravel_doc_section. `file_filter` keeps only pages whose name contains it."""


def compare_versions(docs_path: Path, from_version: str, to_version: str, file_filter: Optional[str] = None) -> Dict[str, Any]:
    require_version(from_version)
    require_version(to_version)
    if from_version == to_version:
        raise ToolFailure("invalid_argument", "from_version and to_version are the same")

    def pages(version: str) -> set:
        version_dir = Path(docs_path) / version
        if not version_dir.is_dir():
            raise ToolFailure("not_found", f"No documentation on this server for Laravel {version}", {"version": version})
        names = {name for name, _ in mcp_tools.list_contained_markdown(version_dir)}
        return {name for name in names if file_filter.lower() in name.lower()} if file_filter else names

    before, after = pages(from_version), pages(to_version)
    result: Dict[str, Any] = {
        "from_version": from_version,
        "to_version": to_version,
        "added_files": sorted(after - before),
        "removed_files": sorted(before - after),
        "common_files": sorted(before & after),
    }
    if file_filter:
        result["filter"] = file_filter
    return result


@tool("compare_laravel_versions", description=COMPARE_DESCRIPTION, output_schema=COMPARE_SCHEMA, tags=_READ)
def compare_laravel_versions(from_version: str, to_version: str, file_filter: Optional[str] = None, ctx: Context = None) -> Dict[str, Any]:  # type: ignore[assignment]
    """Compare the documentation pages of two Laravel versions.

    Args:
        from_version: The older version (e.g. "11.x")
        to_version: The newer version (e.g. "12.x")
        file_filter: Keep only pages whose name contains this text (e.g. "eloquent")
    """
    return compare_versions(companion(ctx).docs_path, from_version, to_version, file_filter)


# --- update_laravel_docs ------------------------------------------------------

UPDATE_SCOPES = ("core", "services", "packages", "learning", "all")

UPDATE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["scope", "results"],
    "properties": {
        "scope": {"type": "string", "enum": list(UPDATE_SCOPES)},
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["source", "name", "outcome"],
                "properties": {
                    "source": {"type": "string", "enum": ["core", "services", "packages", "learning"]},
                    "name": {"type": "string"},
                    "outcome": {"type": "string", "enum": ["updated", "unchanged", "failed"]},
                    "commit": {"type": "string", "description": "For the framework docs, the commit now held"},
                },
            },
        },
    },
}

UPDATE_DESCRIPTION = """Fetch newer documentation into this server's copy.

Needs network access and takes from seconds to a couple of minutes. scope="core" updates the framework docs for one Laravel version from GitHub. "services", "packages" and "learning" refetch those sources, all of them or the ones given in `names`. "all" does everything. Use it when laravel_docs_info shows the copy is behind and the user wants current pages; pulling a newer image or package is the other way to get them."""


def _refetch(fetch: Any, known: List[str], names: Optional[List[str]], source: str, force: bool) -> List[Dict[str, Any]]:
    chosen = names if names else known
    unknown = [name for name in chosen if name not in known]
    if unknown:
        raise ToolFailure("invalid_argument", f"Unknown {source}: {', '.join(unknown)}", {"available": known})
    return [
        {"source": source, "name": name, "outcome": "updated" if fetch(name, force=force) else "failed"}
        for name in chosen
    ]


def update_docs(tc: Any, scope: str = "core", version: Optional[str] = None, names: Optional[List[str]] = None, force: bool = False) -> Dict[str, Any]:
    if scope not in UPDATE_SCOPES:
        raise ToolFailure("invalid_argument", f"Unknown scope {scope!r}", {"valid_scopes": list(UPDATE_SCOPES)})
    require_version(version)
    if names and scope in ("core", "all"):
        raise ToolFailure("invalid_argument", f"names applies to services, packages or learning, not scope={scope!r}")

    results: List[Dict[str, Any]] = []

    if scope in ("core", "all"):
        target = version or default_version(tc.runtime_version)
        try:
            changed = DocsUpdater(tc.docs_path, target).update(force=force)
        except Exception as exc:
            if scope == "core":
                raise ToolFailure("update_failed", f"Could not update the Laravel {target} docs: {exc}", {"version": target})
            results.append({"source": "core", "name": target, "outcome": "failed"})
        else:
            entry = {"source": "core", "name": target, "outcome": "updated" if changed else "unchanged"}
            commit = str(mcp_tools.get_laravel_docs_metadata(Path(tc.docs_path), target).get("commit_sha") or "")[:7]
            if commit:
                entry["commit"] = commit
            results.append(entry)

    updater = tc.updater
    if scope in ("services", "all"):
        fetcher = updater.external_fetcher
        results += _refetch(fetcher.fetch_laravel_service_docs, fetcher.list_available_services(), names, "services", force)
    if scope in ("packages", "all"):
        fetcher = updater.package_fetcher
        results += _refetch(fetcher.fetch_package_docs, fetcher.list_available_packages(), names, "packages", force)
    if scope in ("learning", "all"):
        fetcher = updater.learning_fetcher
        results += _refetch(fetcher.fetch_learning_source, fetcher.list_available_sources(), names, "learning", force)

    if any(entry["outcome"] == "updated" for entry in results):
        mcp_tools.clear_caches()
    return {"scope": scope, "results": results}


@tool(
    "update_laravel_docs", description=UPDATE_DESCRIPTION, output_schema=UPDATE_SCHEMA,
    tags=frozenset({"docs", "write"}), read_only=False, open_world=True, task=True, timeout=300.0,
)
async def update_laravel_docs(
    scope: Annotated[str, Field(json_schema_extra={"enum": list(UPDATE_SCOPES)})] = "core",
    version: Optional[str] = None,
    names: Optional[List[str]] = None,
    force: bool = False,
    ctx: Context = None,  # type: ignore[assignment]
) -> Dict[str, Any]:
    """Fetch newer documentation.

    Args:
        scope: What to update: "core" (default), "services", "packages", "learning" or "all"
        version: Laravel version for the framework docs (e.g. "12.x"). Defaults to the server's configured version
        names: With scope services, packages or learning: which ones (e.g. ["forge", "nova"]). Default: all of them
        force: Refetch even if the copy is recent
    """
    tc = companion(ctx)
    # Blocking network I/O: keep it off the event loop so a long update does
    # not stall every other connected client.
    return await anyio.to_thread.run_sync(lambda: update_docs(tc, scope, version, names, force))
