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

from .doc_search import Section, chunk_markdown
from .docs_updater import get_cached_supported_versions, get_default_version
from .path_security import no_follow_opener, resolve_contained_path, is_safe_path as is_safe_path

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
        with open(file_path, 'r', encoding='utf-8', opener=no_follow_opener) as f:
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
        default_version = runtime_version if runtime_version else get_default_version()
        return default_version, path


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


def contained_subdirectories(family_dir: Path) -> List[str]:
    """The collections inside a corpus family directory, by name.

    Listing, searching and reading must agree on what exists. A symlinked
    directory, or one that resolves outside the family, is left out here, and
    this one enumeration is what all three go through: indexing what reading
    refuses would turn search into an oracle over withheld content.
    Dot-directories hold metadata, not documentation.
    """
    family_dir = Path(family_dir)
    if not family_dir.is_dir():
        return []
    with os.scandir(family_dir) as entries:
        names = sorted(
            entry.name for entry in entries
            if entry.is_dir(follow_symlinks=False) and not entry.name.startswith(".")
        )
    return [name for name in names if resolve_contained_path(family_dir, family_dir / name) is not None]


def _load_family_sections(family_dir: Path) -> List["Section"]:
    """Chunk every collection of a corpus family into sections."""
    family_dir = Path(family_dir)
    sections: List["Section"] = []
    for name in contained_subdirectories(family_dir):
        for rel_name, path in _iter_contained_markdown_recursive(family_dir / name):
            content = get_file_content_cached(str(path))
            if content.startswith("Error") or content.startswith("File not found"):
                continue
            sections.extend(chunk_markdown(content, rel_name, name))
    return sections


def load_package_sections(packages_dir: Path) -> List["Section"]:
    """Chunk every fetched package ecosystem into one section list.

    One index for the whole packages corpus rather than one per ecosystem:
    sections carry their ecosystem subdirectory as the corpus key, so hits
    read back as "<ecosystem>/<file>" while the resident-index count stays
    flat. Enumeration and reads reuse the contained/cached helpers, so
    containment and symlink refusal carry over unchanged.
    """
    return _load_family_sections(Path(packages_dir))


def load_learning_sections(learning_dir: Path) -> List["Section"]:
    """Chunk every learning-resource source into one section list."""
    return _load_family_sections(Path(learning_dir))


# The sources a search can fan out over. "core" is the versioned Laravel
# documentation; the other three are not Laravel-versioned, which is why
# version/all_versions scope core only.
VALID_SEARCH_SOURCES = ("core", "services", "packages", "learning")

# Where each non-core corpus family lives under the docs root.
_CORPUS_FAMILY_DIRS = ("external", "packages", "learning_resources")


def resolve_corpus_file(docs_path: Path, filename: str) -> Optional[tuple[Path, str]]:
    """Resolve a corpus-prefixed filename to (corpus_root, relative_path).

    Search hits name files as "<corpus-key>/<path>" — "forge/servers/php.md",
    "spatie/laravel-permission/roles.md", "laracasts-index/topics.md". When the
    first path segment names an existing service, package ecosystem, or
    learning source directory, the file belongs to that corpus and version
    logic does not apply. Returns None for anything else so core resolution
    proceeds unchanged.
    """
    first, sep, rest = filename.partition("/")
    if not sep or not rest or not first:
        return None
    # The corpus key becomes a path component: ".." here would make the whole
    # docs tree a readable root ("../12.x-backup/leak" resolved under
    # external/..). Only plain directory names qualify, and the constructed
    # root must itself stay inside its family directory.
    if not re.fullmatch(r"[A-Za-z0-9_-][A-Za-z0-9._-]*", first) or first in (".", ".."):
        return None
    for family in _CORPUS_FAMILY_DIRS:
        family_root = Path(docs_path) / family
        if first in contained_subdirectories(family_root):
            return family_root / first, rest
    return None


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
    default = runtime_version or get_default_version()
    return [default] if default in SUPPORTED_VERSIONS else list(SUPPORTED_VERSIONS)


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


# How much a framework page's score is raised when results from several
# corpora are ranked together. Scores from separate indexes are only roughly
# comparable, since IDF is per corpus, and on a general Laravel question a
# package page can edge out the framework's own by a fraction of a point. A
# page from elsewhere with a real lead still ranks first.
CORE_NEAR_TIE_MARGIN = 0.05


def clear_caches():
    """Clear all caches, including the documentation search indexes.

    Imported locally: doc_search does not import mcp_tools, but mcp_tools
    imports doc_search, and a module-level import here would be circular.
    """
    from .doc_search import clear_indexes

    with _cache_lock:
        _file_content_cache.clear()
        _search_result_cache.clear()
    clear_indexes()
    logger.info("Caches cleared")