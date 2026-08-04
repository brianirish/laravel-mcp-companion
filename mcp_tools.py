#!/usr/bin/env python3
"""
Standalone MCP tool functions for Laravel MCP Companion.

This module contains the core functionality of MCP tools as standalone functions
that can be imported and tested independently of the FastMCP server setup.
"""

import os
import re
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import threading

from doc_search import Section, chunk_markdown
from docs_updater import get_cached_supported_versions, DEFAULT_VERSION
from toon_helpers import (
    toon_encode,
    error_data,
    format_version_list,
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

# Global caches for performance optimization.
# A single version of the Laravel docs is ~103 files, so a 100-entry cache was
# evicted continuously by any full-corpus search. Size it to hold several
# versions plus external service docs.
_FILE_CACHE_MAX_ENTRIES = 512
_FILE_CACHE_EVICT_COUNT = 64
_SEARCH_CACHE_MAX_ENTRIES = 100
_SEARCH_CACHE_EVICT_COUNT = 20

_file_content_cache: Dict[str, str] = {}
_search_result_cache: Dict[str, Dict[str, Any]] = {}
_cache_lock = threading.Lock()


def _no_follow_opener(path, flags):
    """open() opener that refuses to follow a symlink in the final component.

    Passed to open() rather than calling os.open directly so that the read still
    goes through the normal open(), which keeps the behaviour observable to
    callers and testable in the usual way.

    O_NOFOLLOW is POSIX. Where it is unavailable this degrades to an ordinary
    open rather than refusing to read anything.
    """
    return os.open(path, flags | getattr(os, "O_NOFOLLOW", 0))


def get_file_content_cached(file_path: str) -> str:
    """Get file content with caching.

    Refuses to open a path whose final component is a symbolic link. Containment
    is checked before the open, and a path that is a regular file when checked
    can be replaced by a link before it is opened -- resolving first does not
    help, because a regular file resolves to itself. O_NOFOLLOW closes that
    window by making the refusal part of the open itself.

    Callers that legitimately want a linked file should resolve it first (see
    resolve_contained_path) and pass the resolved path, which is not a link.
    """
    with _cache_lock:
        if file_path in _file_content_cache:
            logger.debug(f"Cache hit for file: {file_path}")
            return _file_content_cache[file_path]

    try:
        with open(file_path, 'r', encoding='utf-8', opener=_no_follow_opener) as f:
            content = f.read()

        # Cache the content
        with _cache_lock:
            _file_content_cache[file_path] = content
            # Limit cache size to prevent memory issues
            if len(_file_content_cache) > _FILE_CACHE_MAX_ENTRIES:
                # Remove oldest entries
                oldest_keys = list(_file_content_cache.keys())[:_FILE_CACHE_EVICT_COUNT]
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


def resolve_contained_path(base_path: Path, target_path: Path) -> Optional[Path]:
    """Resolve target_path, returning it only if it lands inside base_path.

    Callers must read the path this returns, not the one they passed in.
    Validating one path and then opening another leaves a window in which a
    symlink can be swapped between the check and the open, so the file that was
    approved and the file that gets read need not be the same one.

    Uses is_relative_to() on fully resolved paths. A plain string prefix check
    is not sufficient: it treats "/docs/12.x-backup" as living under "/docs/12.x".

    Returns None if the path escapes, or if either path cannot be resolved --
    any error denies access.
    """
    try:
        base = Path(base_path).resolve()
        resolved = Path(target_path).resolve()
    except Exception:
        return None
    return resolved if resolved.is_relative_to(base) else None


def is_safe_path(base_path: Path, target_path: Path) -> bool:
    """Whether target_path resolves to a location inside base_path.

    Prefer resolve_contained_path when the caller goes on to read the file, so
    that the path checked is the path opened.
    """
    return resolve_contained_path(base_path, target_path) is not None


def list_contained_markdown(version_path: Path) -> List[tuple[str, Path]]:
    """Return (name, readable_path) for .md files that stay inside version_path.

    Enumeration has to apply the same containment rule as reading. Without it a
    symlink pointing out of the tree is listed and searched while
    read_laravel_doc_content refuses to serve it -- which turns search into an
    oracle over content the read path deliberately withholds.

    The second element is the path callers should read: for a symlink it is the
    resolved target, since the reader refuses to follow links at open time.

    Only symlinks are resolved. A plain file that is a direct child of
    version_path cannot escape it, and resolving every file turned a search over
    the corpus into hundreds of unnecessary readlink walks.
    """
    # Errors are deliberately not swallowed. An unreadable documentation
    # directory must surface as an error, not as "no files found" -- the callers
    # already wrap this and turn exceptions into a message.
    contained: List[tuple[str, Path]] = []
    with os.scandir(version_path) as entries:
        for entry in entries:
            if not entry.name.endswith('.md'):
                continue

            if not entry.is_symlink():
                contained.append((entry.name, Path(entry.path)))
                continue

            resolved = resolve_contained_path(version_path, Path(entry.path))
            if resolved is not None:
                contained.append((entry.name, resolved))
            else:
                logger.warning(
                    f"Skipping documentation file outside its version directory: {entry.name}"
                )
    return contained


def load_version_sections(docs_path: Path, version: str) -> List["Section"]:
    """Chunk every contained markdown file of a version into sections.

    Enumeration goes through list_contained_markdown and reads through
    get_file_content_cached, so containment and the refusal to follow symlinks
    at open time both carry over unchanged rather than being reimplemented.
    """
    version_path = Path(docs_path) / version
    if not version_path.is_dir():
        return []

    sections: List["Section"] = []
    for name, path in list_contained_markdown(version_path):
        content = get_file_content_cached(str(path))
        if content.startswith("Error") or content.startswith("File not found"):
            continue
        sections.extend(chunk_markdown(content, name, version))
    return sections


def load_service_sections(external_dir: Path, service: str) -> List["Section"]:
    """Chunk an external service's documentation, keyed by service name."""
    service_path = Path(external_dir) / service
    if not service_path.is_dir():
        return []

    sections: List["Section"] = []
    for name, path in _iter_contained_markdown_recursive(service_path):
        content = get_file_content_cached(str(path))
        if content.startswith("Error") or content.startswith("File not found"):
            continue
        sections.extend(chunk_markdown(content, name, service))
    return sections


def _iter_contained_markdown_recursive(root: Path, prefix: str = "") -> List[tuple[str, Path]]:
    """(relative_name, readable_path) for markdown under root, at any depth.

    list_contained_markdown is deliberately single-level for the flat core
    corpus, but services and packages nest (121 of 147 service files and all
    of Spatie's live in subdirectories — invisible to search until this
    existed). Files at each level go through list_contained_markdown so the
    containment and symlink rules apply unchanged; symlinked directories are
    never followed, and dot-directories (.metadata and friends) are skipped.
    """
    results = [(f"{prefix}{name}", path) for name, path in list_contained_markdown(root)]
    with os.scandir(root) as entries:
        subdirs = sorted(
            entry.name for entry in entries
            if entry.is_dir(follow_symlinks=False) and not entry.name.startswith(".")
        )
    for name in subdirs:
        results.extend(
            _iter_contained_markdown_recursive(Path(root) / name, f"{prefix}{name}/")
        )
    return results


def load_package_sections(packages_dir: Path) -> List["Section"]:
    """Chunk every fetched package ecosystem into one section list.

    One index for the whole packages corpus rather than one per ecosystem:
    sections carry their ecosystem subdirectory as the corpus key, so hits
    read back as "<ecosystem>/<file>" while the resident-index count stays
    flat. Enumeration and reads reuse the contained/cached helpers, so
    containment and symlink refusal carry over unchanged.
    """
    packages_path = Path(packages_dir)
    if not packages_path.is_dir():
        return []

    sections: List["Section"] = []
    for sub in sorted(p for p in packages_path.iterdir() if p.is_dir()):
        for name, path in _iter_contained_markdown_recursive(sub):
            content = get_file_content_cached(str(path))
            if content.startswith("Error") or content.startswith("File not found"):
                continue
            sections.extend(chunk_markdown(content, name, sub.name))
    return sections


def load_learning_sections(learning_dir: Path) -> List["Section"]:
    """Chunk every learning-resource source into one section list."""
    learning_path = Path(learning_dir)
    if not learning_path.is_dir():
        return []

    sections: List["Section"] = []
    for sub in sorted(p for p in learning_path.iterdir() if p.is_dir()):
        for name, path in _iter_contained_markdown_recursive(sub):
            content = get_file_content_cached(str(path))
            if content.startswith("Error") or content.startswith("File not found"):
                continue
            sections.extend(chunk_markdown(content, name, sub.name))
    return sections


# The sources a search can fan out over. "core" is the versioned Laravel
# documentation; the other three are not Laravel-versioned, which is why
# version/all_versions scope core only.
VALID_SEARCH_SOURCES = ("core", "services", "packages", "learning")


def validate_version_data(version: Optional[str]) -> Optional[Dict[str, Any]]:
    """Validate a caller-supplied Laravel version against the supported allowlist.

    Version strings are used to build filesystem paths, so anything outside the
    allowlist is rejected before it can be joined onto a base directory.

    Returns:
        An error dict if the version is invalid, otherwise None.
    """
    if version is not None and version not in SUPPORTED_VERSIONS:
        logger.warning(f"Rejected unsupported version parameter: {version!r}")
        return error_data(
            f"Invalid version: {version}",
            {"supported_versions": SUPPORTED_VERSIONS}
        )
    return None


def validate_version(version: Optional[str]) -> Optional[str]:
    """String-returning form of validate_version_data for the TOON-only tools."""
    error = validate_version_data(version)
    return toon_encode(error) if error else None


def resolve_search_versions(
    version: Optional[str],
    runtime_version: Optional[str] = None,
    all_versions: bool = False,
) -> List[str]:
    """Decide which versions a search should cover.

    Searching every supported version re-reads the entire corpus and returns
    near-duplicate hits for the same file, so scope defaults to the configured
    version unless the caller explicitly asks for all of them.
    """
    if version:
        return [version]
    if all_versions:
        return list(SUPPORTED_VERSIONS)
    default = runtime_version or DEFAULT_VERSION
    return [default] if default in SUPPORTED_VERSIONS else list(SUPPORTED_VERSIONS)


def count_matches(pattern: re.Pattern, content: str) -> int:
    """Count regex matches in a single pass.

    Replaces the search()-then-findall() pattern, which scanned each file twice
    and materialized every match just to take its length.
    """
    return sum(1 for _ in pattern.finditer(content))


def validate_subdirectory(base_dir: Path, name: str) -> bool:
    """Check that `name` refers to a direct subdirectory of base_dir.

    Guards caller-supplied directory names (learning resource sources, service
    names) that would otherwise be joined onto a base path unchecked.
    """
    if not name or '/' in name or '\\' in name or name in ('.', '..') or '\x00' in name:
        return False

    candidate = base_dir / name
    # Compare the parent rather than resolving the candidate. The name checks
    # above already guarantee a single path component, so this cannot traverse;
    # resolving instead rejected directories the operator had deliberately
    # relocated via symlink, which listing and search both accepted -- the same
    # inconsistency that DocsUpdater had for version directories.
    try:
        return candidate.parent.resolve() == base_dir.resolve() and candidate.is_dir()
    except (OSError, ValueError):
        return False


# Laravel changes 13.x most days. When nothing has changed anywhere in this many
# days, the copy itself is behind rather than upstream being quiet.
DOCS_STALE_AFTER_DAYS = 30


def parse_timestamp(value: object) -> Optional[datetime]:
    """Parse a metadata timestamp into an aware UTC datetime, or None.

    Total by design. Metadata lives in a mutable, network-populated directory
    that users can mount over, and this runs during server construction -- a
    malformed value must degrade to "unknown", never raise.
    """
    if not isinstance(value, str) or not value or value == "unknown":
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def get_documentation_date(
    docs_path: Path, version: Optional[str] = None
) -> tuple[Optional[str], Optional[int]]:
    """Return (date, age_in_days) for when Laravel last changed the documentation.

    Reads `commit_date`, not `sync_time`. `sync_time` records when this project
    last fetched a change, which for a branch that no longer changes recedes
    forever -- reporting an end-of-life version as increasingly stale while it
    is byte-identical to upstream.

    For a specific version, that version's date. Across versions, the *newest*:
    13.x changes near-daily, so the most recent change is a proxy for how old
    this copy is, which is the only part a user can act on.

    Returns (None, None) when no metadata is readable, or when the date is in
    the future -- clock skew we cannot interpret and must not present as fresh.
    """
    # Callers reach this through server construction, where docs_path may still
    # be a plain string; joining one would raise rather than report "unknown".
    base = Path(docs_path)
    versions = [version] if version is not None else SUPPORTED_VERSIONS
    newest: Optional[datetime] = None

    for candidate in versions:
        metadata = get_laravel_docs_metadata(base, candidate)
        if not isinstance(metadata, dict):
            continue
        changed = parse_timestamp(metadata.get("commit_date"))
        if changed and (newest is None or changed > newest):
            newest = changed

    if newest is None:
        return None, None

    age = (datetime.now(timezone.utc) - newest).days
    if age < 0:
        logger.warning(f"Documentation commit_date is in the future: {newest.isoformat()}")
        return None, None

    return newest.strftime("%Y-%m-%d"), age


def describe_documentation_date(docs_path: Path, version: Optional[str] = None) -> str:
    """A bare date for the server instructions, or "unknown".

    Deliberately carries no age phrasing. Rendering "425 days ago" would
    reintroduce exactly the alarm this reporting exists to remove, even though
    the number is factual.
    """
    date, _ = get_documentation_date(docs_path, version)
    return date or "unknown (no documentation synced yet)"


def copy_is_stale(docs_path: Path) -> bool:
    """Whether this copy of the documentation is behind, judged offline.

    Takes no version argument: a single version's date being old means upstream
    stopped changing, which is neither a problem nor actionable. What is
    actionable is a stale *image*, which shows up as every version being old --
    including the one that normally changes daily.
    """
    _, age = get_documentation_date(docs_path)
    return age is not None and age > DOCS_STALE_AFTER_DAYS


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


def list_laravel_docs_data(docs_path: Path, version: Optional[str] = None, runtime_version: Optional[str] = None) -> Dict[str, Any]:
    """List all available Laravel documentation files, as data.

    Args:
        docs_path: Base path for documentation
        version: Specific Laravel version to list (e.g., "12.x"). If not provided, lists all versions.

    Returns:
        Dict with version metadata and file lists, or an error dict.
    """
    logger.debug(f"list_laravel_docs_data called (version: {version})")

    version_error = validate_version_data(version)
    if version_error:
        return version_error

    try:
        if version:
            # List docs for specific version
            version_path = docs_path / version
            if not version_path.exists():
                return error_data(
                    f"No documentation found for version {version}",
                    {"suggestion": "Use update_laravel_docs() to fetch documentation"}
                )

            metadata = get_laravel_docs_metadata(docs_path, version)
            md_files = sorted(name for name, _ in list_contained_markdown(version_path))

            if not md_files:
                return error_data(f"No documentation files found in version {version}")

            return {
                "version": version,
                "last_updated": metadata.get('sync_time', 'unknown'),
                "commit": metadata.get('commit_sha', 'unknown')[:7] if metadata.get('commit_sha') else 'unknown',
                "file_count": len(md_files),
                "files": md_files
            }
        else:
            # List all versions
            versions_data: List[Dict] = []
            for v in SUPPORTED_VERSIONS:
                version_path = docs_path / v
                if not version_path.is_dir():
                    continue
                md_files = [name for name, _ in list_contained_markdown(version_path)]
                if md_files:
                    metadata = get_laravel_docs_metadata(docs_path, v)
                    versions_data.append({
                        "version": v,
                        "last_updated": metadata.get('sync_time', 'unknown'),
                        "commit": metadata.get('commit_sha', 'unknown')[:7] if metadata.get('commit_sha') else 'unknown',
                        "file_count": len(md_files)
                    })

            if not versions_data:
                return error_data(
                    "No documentation files found",
                    {"suggestion": "Use update_laravel_docs() to fetch documentation"}
                )

            return {"count": len(versions_data), "versions": versions_data}
    except Exception as e:
        logger.error(f"Error listing documentation files: {str(e)}")
        return error_data(f"Error listing documentation files: {str(e)}")


def list_laravel_docs_impl(docs_path: Path, version: Optional[str] = None, runtime_version: Optional[str] = None) -> str:
    """TOON-encoded form of list_laravel_docs_data.

    The bare all-versions list used to be encoded unwrapped; structured content
    must be a JSON object, so both serializations now share the wrapped shape.
    """
    data = list_laravel_docs_data(docs_path, version, runtime_version=runtime_version)
    if version and "files" in data:
        return toon_encode(data)
    if "versions" in data:
        return format_version_list(data["versions"])
    return toon_encode(data)


def read_laravel_doc_content_impl(docs_path: Path, filename: str, version: Optional[str] = None, runtime_version: Optional[str] = None) -> str:
    """Read the content of a specific Laravel documentation file.
    
    Args:
        docs_path: Base path for documentation
        filename: Name of the documentation file (e.g., "blade.md" or "12.x/blade.md")
        version: Specific Laravel version to use. Overridden if filename includes version.
    """
    logger.debug(f"read_laravel_doc_content_impl called with filename: {filename}, version: {version}, runtime_version: {runtime_version}")

    version_error = validate_version(version)
    if version_error:
        return version_error

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
    
    # Security check - ensure we stay within version directory. Read the
    # resolved path this returns, not file_path: opening the unresolved path
    # would follow the symlink a second time, after the check.
    version_path = docs_path / version
    safe_path = resolve_contained_path(version_path, file_path)
    if safe_path is None:
        logger.warning(f"Access denied: {filename} (attempted directory traversal)")
        return f"Access denied: {filename} (attempted directory traversal)"

    if not safe_path.exists():
        logger.warning(f"Documentation file not found: {safe_path}")
        return f"Documentation file not found: {filename} (version: {version})"

    try:
        content = get_file_content_cached(str(safe_path))
        if not content.startswith("Error") and not content.startswith("File not found"):
            logger.debug(f"Successfully read file: {safe_path} ({len(content)} bytes)")
        return content
    except Exception as e:
        logger.error(f"Error reading file {safe_path}: {str(e)}")
        return f"Error reading file: {str(e)}"


def read_laravel_doc_section_impl(
    docs_path: Path,
    filename: str,
    section: str,
    version: Optional[str] = None,
    runtime_version: Optional[str] = None,
) -> str:
    """Return one ## section of a documentation file.

    `section` matches either the anchor or the heading text, case-insensitively.
    Search output shows both, and the caller should not have to guess which one
    is canonical.

    This exists because whole-file reads are the dominant cost of answering a
    question: queues.md alone is around 34,000 tokens, of which a typical answer
    needs a small fraction.
    """
    version_error = validate_version(version)
    if version_error:
        return version_error

    if not version:
        version = runtime_version if runtime_version else DEFAULT_VERSION

    if not filename.endswith('.md'):
        filename = f"{filename}.md"

    version_path = Path(docs_path) / version
    safe_path = resolve_contained_path(version_path, version_path / filename)
    if safe_path is None:
        logger.warning(f"Access denied: {filename} (attempted directory traversal)")
        return f"Access denied: {filename} (attempted directory traversal)"

    if not safe_path.exists():
        return f"Documentation file not found: {filename} (version: {version})"

    content = get_file_content_cached(str(safe_path))
    if content.startswith("Error") or content.startswith("File not found"):
        return content

    wanted = section.strip().lower().lstrip('#')
    sections = chunk_markdown(content, filename, version)

    for candidate in sections:
        if (candidate.anchor or "").lower() == wanted or candidate.heading.lower() == wanted:
            return candidate.text.strip()

    return format_error(
        f"Section '{section}' not found in {filename}",
        {"available_sections": [s.anchor or s.heading for s in sections]},
    )


def search_laravel_docs_data(
    docs_path: Path,
    query: str,
    version: Optional[str] = None,
    include_external: bool = True,
    external_dir: Optional[Path] = None,
    runtime_version: Optional[str] = None,
    all_versions: bool = False,
    limit: int = 5,
    sources: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Search documentation, returning ranked sections with snippets, as data.

    Ranked by BM25 over ## sections rather than by literal substring count, so a
    multi-word question matches at all and long files no longer outrank relevant
    ones. Each hit carries an anchor so the full section can be fetched with
    read_laravel_doc_section instead of reading the whole file.

    Fans out over every aggregated corpus by default — core versions, external
    services, fetched package ecosystems, learning resources — with `sources`
    narrowing the set. `include_external=False` is the historical core-only
    switch and is superseded by an explicit `sources`.
    """
    from doc_search import extract_snippet, get_index

    version_error = validate_version_data(version)
    if version_error:
        return version_error

    if not query.strip():
        return error_data("Search query cannot be empty")

    if sources is not None:
        invalid = [s for s in sources if s not in VALID_SEARCH_SOURCES]
        if invalid:
            return error_data(
                f"Invalid sources: {', '.join(invalid)}",
                {"valid_sources": list(VALID_SEARCH_SOURCES)},
            )
        effective_sources = list(dict.fromkeys(sources))
    elif not include_external:
        effective_sources = ["core"]
    else:
        effective_sources = list(VALID_SEARCH_SOURCES)

    search_versions = resolve_search_versions(version, runtime_version, all_versions)

    cache_key = (
        f"search:{query}:{','.join(search_versions)}:{','.join(effective_sources)}:{limit}"
    )
    with _cache_lock:
        if cache_key in _search_result_cache:
            logger.debug(f"Returning cached search results for: {query}")
            return _search_result_cache[cache_key]

    # (section, score, family) — the family names how the hit's corpus key in
    # section.version becomes a user-facing source label.
    hits: List[tuple] = []

    if "core" in effective_sources:
        for candidate in search_versions:
            def load_version(c: str = candidate) -> List[Section]:
                return load_version_sections(docs_path, c)

            index = get_index(docs_path, f"version:{candidate}", load_version)
            # Literal fallback preserves exact-symbol lookup such as
            # `queue:retry`, which tokenized scoring splits apart.
            found = index.search(query, limit) or index.substring_search(query, limit)
            hits.extend((s, score, "core") for s, score in found)

    if "services" in effective_sources and external_dir and Path(external_dir).is_dir():
        for service_dir in sorted(Path(external_dir).iterdir()):
            if not service_dir.is_dir():
                continue
            service = service_dir.name
            def load_service(name: str = service) -> List[Section]:
                return load_service_sections(external_dir, name)

            index = get_index(docs_path, f"service:{service}", load_service)
            found = index.search(query, limit) or index.substring_search(query, limit)
            hits.extend((s, score, "service") for s, score in found)

    if "packages" in effective_sources:
        packages_dir = Path(docs_path) / "packages"
        if packages_dir.is_dir():
            index = get_index(docs_path, "packages", lambda: load_package_sections(packages_dir))
            found = index.search(query, limit) or index.substring_search(query, limit)
            hits.extend((s, score, "package") for s, score in found)

    if "learning" in effective_sources:
        learning_dir = Path(docs_path) / "learning_resources"
        if learning_dir.is_dir():
            index = get_index(docs_path, "learning", lambda: load_learning_sections(learning_dir))
            found = index.search(query, limit) or index.substring_search(query, limit)
            hits.extend((s, score, "learning") for s, score in found)

    # Scores from separate indexes are only approximately comparable, since IDF
    # is per-corpus. Close enough to rank against each other; the quality tests
    # hold the line on core queries still surfacing core docs first.
    hits.sort(key=lambda triple: triple[1], reverse=True)
    hits = hits[:limit]

    if not hits:
        result = error_data(
            f"No results found for '{query}'",
            {"scope": ", ".join(search_versions), "sources": effective_sources},
        )
    else:
        result = {
            "query": query,
            "scope": ", ".join(search_versions),
            "results": [
                {
                    "file": f"{section.version}/{section.filename}",
                    "anchor": section.anchor or "",
                    "heading": section.heading,
                    "score": round(score, 2),
                    "snippet": extract_snippet(section.text, query),
                    "source": "core" if family == "core" else f"{family}:{section.version}",
                }
                for section, score, family in hits
            ],
        }

    with _cache_lock:
        _search_result_cache[cache_key] = result
        if len(_search_result_cache) > _SEARCH_CACHE_MAX_ENTRIES:
            for key in list(_search_result_cache.keys())[:_SEARCH_CACHE_EVICT_COUNT]:
                del _search_result_cache[key]

    return result


def search_laravel_docs_impl(
    docs_path: Path,
    query: str,
    version: Optional[str] = None,
    include_external: bool = True,
    external_dir: Optional[Path] = None,
    runtime_version: Optional[str] = None,
    all_versions: bool = False,
    limit: int = 5,
) -> str:
    """TOON-encoded form of search_laravel_docs_data."""
    return toon_encode(search_laravel_docs_data(
        docs_path, query, version, include_external, external_dir,
        runtime_version=runtime_version, all_versions=all_versions, limit=limit,
    ))


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

    version_error = validate_version(version)
    if version_error:
        return version_error

    # Use read_laravel_doc_content_impl to get the content
    content = read_laravel_doc_content_impl(docs_path, filename, version, runtime_version=runtime_version)

    if (content.startswith("Error") or content.startswith("error:")
            or content.startswith("Documentation file not found") or content.startswith("Access denied")):
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

    version_error = validate_version(version)
    if version_error:
        return version_error

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

    version_error = validate_version(version)
    if version_error:
        return version_error

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

    version_error = validate_version(version)
    if version_error:
        return version_error

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

    version_error = validate_version(version)
    if version_error:
        return version_error

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
            {"suggestion": "Learning resources ship with the server; this documentation path is missing them. Check DOCS_PATH, or the mount if running in Docker."}
        )

    results_data: List[Dict] = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)

    # Determine which sources to search
    if sources:
        invalid = [s for s in sources if not validate_subdirectory(learning_dir, s)]
        if invalid:
            available = sorted(d.name for d in learning_dir.iterdir() if d.is_dir())
            logger.warning(f"Rejected invalid learning resource sources: {invalid}")
            return format_error(
                f"Invalid sources: {', '.join(invalid)}",
                {"available_sources": available}
            )
        search_dirs = [learning_dir / source for source in sources]
    else:
        search_dirs = [d for d in learning_dir.iterdir() if d.is_dir()]

    for source_dir in search_dirs:
        source_name = source_dir.name
        source_matches: List[Dict] = []

        for file_path in source_dir.glob("*.md"):
            try:
                content = get_file_content_cached(str(file_path))
                if not content.startswith("Error") and not content.startswith("File not found"):
                    count = count_matches(pattern, content)
                    if count:
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
            {"suggestion": "Learning resources ship with the server; this documentation path is missing them. Check DOCS_PATH, or the mount if running in Docker."}
        )

    if source:
        if not validate_subdirectory(learning_dir, source):
            available_sources = sorted(d.name for d in learning_dir.iterdir() if d.is_dir())
            logger.warning(f"Rejected invalid learning resource source: {source!r}")
            return format_error(
                f"Learning source '{source}' not found",
                {"available_sources": available_sources}
            )
        source_dir = learning_dir / source

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
    """Clear all caches, including the documentation search indexes.

    Imported locally: doc_search does not import mcp_tools, but mcp_tools
    imports doc_search, and a module-level import here would be circular.
    """
    from doc_search import clear_indexes

    with _cache_lock:
        _file_content_cache.clear()
        _search_result_cache.clear()
    clear_indexes()
    logger.info("Caches cleared")