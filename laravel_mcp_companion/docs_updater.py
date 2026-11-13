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
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Union, Sequence
import urllib.parse
import urllib.request
import urllib.error
import zipfile
import json
import time
from enum import Enum
import random

from . import resource_path
from .path_security import is_within_directory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("laravel-docs-updater")


# Utility functions for content filtering
def remove_social_media_lines(content: str) -> str:
    """
    Remove lines that are purely social media links from scraped content.
    Preserves legitimate documentation references (e.g., Envoy's @discord directive).
    """
    social_domains = ['x.com/laravelphp', 'x.com/laravel', 'twitter.com/laravelphp', 'twitter.com/laravel',
                      'discord.com/invite', 'discord.gg',
                      'linkedin.com/company', 'facebook.com', 'instagram.com', 'github.com/laravel']

    lines = content.split('\n')
    filtered = []

    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            filtered.append(line)
            continue

        # Skip nav list items pointing to social media
        if re.match(r'^[-*+]\s*\[Community\]\(https?://(discord|twitter)', stripped, re.IGNORECASE):
            continue

        # Count links in the line
        all_links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', stripped)
        if len(all_links) >= 3:  # If line has 3+ links, check if most are social
            social_link_count = sum(1 for text, url in all_links if any(domain in url for domain in social_domains))
            # If 50% or more of the links are social media, remove the line
            if social_link_count >= len(all_links) * 0.5:
                continue

        # Check if line is entirely composed of social media links
        # Remove all markdown links from the line to see what remains
        text_without_links = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', stripped)

        # If after removing links we have substantial text, keep the line
        # But if it's only link text that are domain names or social network names, skip it
        if text_without_links.strip():
            # Check if the remaining text is just social network names strung together
            social_names = ['x', 'github', 'discord', 'linkedin', 'facebook', 'instagram', 'twitter']
            text_lower = text_without_links.lower().strip()

            # Use word boundary matching to avoid false positives (e.g., "example" containing "x")
            # Split on non-word characters and check if all remaining words are social names
            words = re.findall(r'\b\w+\b', text_lower)
            if words and all(word in social_names for word in words):
                # All words are social network names, check if social domains are present
                if any(domain in stripped for domain in social_domains):
                    continue

        filtered.append(line)

    return '\n'.join(filtered)


def remove_image_references(content: str) -> str:
    """
    Remove markdown image references from scraped content.
    Preserves images inside code blocks.
    """
    lines = content.split('\n')
    in_code_block = False
    filtered = []

    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            filtered.append(line)
            continue

        if not in_code_block:
            # Remove image references from the line
            cleaned = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', line)

            # Skip a line only when removing an image is what emptied it (or
            # left a bare bullet). A line that was blank to begin with is a
            # paragraph break: dropping those joined every paragraph of a
            # markdown page to the next.
            stripped_cleaned = cleaned.strip()
            if cleaned != line and (not stripped_cleaned or stripped_cleaned in ('*', '-', '+')):
                continue

            # Line has other content, keep the cleaned version
            filtered.append(cleaned)
        else:
            filtered.append(line)

    return '\n'.join(filtered)


# GitHub API URLs
GITHUB_API_URL = "https://api.github.com"
LARAVEL_DOCS_REPO = "laravel/docs"
USER_AGENT = "Laravel-MCP-Companion (+https://github.com/brianirish/laravel-mcp-companion)"

# Default cache file path (relative to this script)
VERSIONS_CACHE_FILE = resource_path("docs") / ".versions_cache.json"

LAST_RESORT_VERSIONS = ["12.x"]

# Network timeout for documentation fetches. Without this, urllib blocks
# indefinitely and a stalled connection hangs startup or pins a worker thread.
DEFAULT_REQUEST_TIMEOUT = 30

# How long a cached version list stays fresh before we ask GitHub again.
VERSIONS_CACHE_TTL_SECONDS = 24 * 60 * 60

# Section/version names become filesystem paths, so they are restricted to a
# conservative character set: alphanumerics, dot, dash, underscore, and single
# forward slashes for nesting. No leading slash, no '..', no backslash, no NUL.
_SAFE_PATH_SEGMENT = re.compile(r'[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*')


def is_safe_section_name(name: str) -> bool:
    """Check that a discovered section name is safe to use as a relative path.

    Section names are parsed out of remote HTML, so they are untrusted input.
    """
    if not name or len(name) > 255:
        return False
    if '..' in name or name.startswith('/') or '\\' in name or '\x00' in name:
        return False
    # Reject dot and empty components. "." is otherwise accepted by the pattern
    # below, and `base / "."` collapses to `base` itself, which would silently
    # retarget a version directory at the whole documentation root.
    if any(part in ('', '.', '..') for part in name.split('/')):
        return False
    return _SAFE_PATH_SEGMENT.fullmatch(name) is not None


def fetch_llms_index_docs(
    name: str,
    index_url: str,
    page_prefix: str,
    target_dir: Path,
    fetch: Callable[[str], bytes],
    layout: str = "basename",
    full_url: Optional[str] = None,
    exclude_paths: Sequence[str] = (),
) -> Optional[Dict[str, Any]]:
    """Save every page listed in a site's llms.txt index, as markdown.

    A growing number of documentation sites publish an llms.txt: the site's own
    list of its pages, each also served as markdown at a `.md` URL. Reading it
    means there is no page list to maintain here, no navigation to parse and no
    HTML to convert. A reorganised sidebar or a new major version is picked up
    by the next sync.

    Each listed page is saved verbatim, minus the banner blockquote it opens
    with. When the index lists several major versions, only the newest is
    fetched. A version is recognised only as the first path segment below
    `page_prefix` ("v3", "5.x"), so a numbered segment deeper in a path is left
    alone. After a complete sync, saved pages the index no longer lists are
    removed; a partial sync removes nothing.

    `layout` chooses where a page lands under `target_dir`, from its path below
    the prefix and version:
        "basename"  routing.md                 the final segment only
        "flat"      forms-text-input.md        the path, joined with "-"
        "nested"    servers/php.md             the path, as directories

    `fetch` takes a URL and returns the response body.

    `full_url` names the site's single-file export (llms-full.txt), which holds
    every page in one response. When given, pages are taken from it and only
    the ones it lacks are requested individually, so a large site costs two
    requests instead of one per page. The index still decides which pages are
    expected; the export adds none of its own. Export text is the site's
    source with its components still in it, so it is passed through
    _clean_export_markup.

    `exclude_paths` lists path prefixes, below the docs root and any version,
    that are not wanted ("api/"). Pages under them are not fetched, not kept
    and not counted.

    Returns None when the index cannot be read or lists no usable page.
    Otherwise a dict: `sections`, the pages saved, in index order and without
    ".md"; `total`, how many the index listed; `version`, the major fetched or
    None.
    """
    try:
        index_text = fetch(index_url).decode('utf-8')
    except Exception as e:
        logger.error(f"Error fetching {name} docs index: {str(e)}")
        return None

    # Only URLs on the site's own docs path qualify: the index is remote
    # input, and following arbitrary URLs from it would let a compromised
    # page turn the fetcher into a generic downloader.
    page_urls = list(dict.fromkeys(re.findall(
        rf"\(({re.escape(page_prefix)}[A-Za-z0-9/._-]+\.md)\)", index_text
    )))

    def path_of(url: str) -> str:
        return url[len(page_prefix):-len(".md")]

    # The path becomes a file path, so it gets the same checks as any other
    # name parsed out of a remote page.
    page_urls = [url for url in page_urls if is_safe_section_name(path_of(url))]
    if not page_urls:
        logger.warning(f"{name} llms.txt index yielded no documentation URLs")
        return None

    version_segment = re.compile(r"v?(\d+)(?:\.x)?")

    def version_of(url: str) -> Optional[tuple[int, str]]:
        first, _, rest = path_of(url).partition("/")
        match = version_segment.fullmatch(first) if rest else None
        return (int(match.group(1)), first) if match else None

    # An index can list every maintained major. Saved side by side their
    # pages collide -- with Inertia's v3, v2 and v1 all listed, each file
    # ended up holding the v1 page -- so keep the newest only.
    version_label: Optional[str] = None
    versions = {v for v in map(version_of, page_urls) if v}
    if versions:
        newest = max(versions)
        version_label = newest[1]
        page_urls = [url for url in page_urls if version_of(url) == newest]
        logger.info(f"{name} index lists versions {sorted(v[1] for v in versions)}; fetching {version_label}")

    def section_of(url: str) -> str:
        path = path_of(url)
        if version_label:
            path = path[len(version_label) + 1:]
        if layout == "nested":
            return path
        if layout == "flat":
            return path.replace("/", "-")
        return path.rsplit("/", 1)[-1]

    if exclude_paths:
        def unversioned(url: str) -> str:
            path = path_of(url)
            return path[len(version_label) + 1:] if version_label else path

        page_urls = [url for url in page_urls if not unversioned(url).startswith(tuple(exclude_paths))]
        if not page_urls:
            logger.warning(f"{name} index lists nothing outside the excluded paths")
            return None

    # Two URLs can map to one file under the flatter layouts; keep the first.
    pages: Dict[str, str] = {}
    for url in page_urls:
        pages.setdefault(section_of(url), url)

    exported: Dict[str, str] = {}
    if full_url:
        origin = "/".join(page_prefix.split("/")[:3])
        try:
            exported = {
                url: _clean_export_markup(text, origin, page_prefix)
                for url, text in _split_full_export(fetch(full_url).decode('utf-8'), page_prefix).items()
            }
        except Exception as e:
            logger.warning(f"Could not read the {name} single-file export, fetching page by page: {str(e)}")
        if exported:
            covered = sum(1 for url in pages.values() if url in exported)
            logger.info(f"{name} export covers {covered} of {len(pages)} indexed pages")

    fetched_sections: List[str] = []
    for section, url in pages.items():
        page_file = target_dir / f"{section}.md"
        if not is_within_directory(target_dir, page_file):
            logger.warning(f"Skipping out-of-tree {name} page: {section!r}")
            continue
        try:
            page = exported[url] if url in exported else fetch(url).decode('utf-8')

            # Strip the leading "> ..." documentation-index banner.
            lines = page.splitlines()
            while lines and (lines[0].startswith(">") or not lines[0].strip()):
                lines.pop(0)
            content = remove_image_references("\n".join(lines)).strip()
            if len(content) < 100:
                logger.warning(f"{name} page {section} too thin, skipping")
                continue

            page_file.parent.mkdir(parents=True, exist_ok=True)
            with open(page_file, 'w', encoding='utf-8') as f:
                f.write(f"Source: {url}\n\n{content}\n")
            fetched_sections.append(section)
        except Exception as e:
            logger.warning(f"Error fetching {name} page {url}: {str(e)}")

    if len(fetched_sections) == len(pages):
        # A complete fetch is the only safe moment to prune: pages the index
        # no longer lists would otherwise stay searchable forever. A partial
        # fetch keeps everything, stale included, rather than deleting docs
        # we failed to replace.
        expected = {(target_dir / f"{section}.md").resolve() for section in pages}
        saved = target_dir.rglob("*.md") if layout == "nested" else target_dir.glob("*.md")
        for stale in sorted(saved):
            if stale.resolve() not in expected:
                logger.info(f"Pruning {name} page no longer in the index: {stale.relative_to(target_dir)}")
                stale.unlink()
        if layout == "nested":
            # Remove directories the pruning emptied, deepest first.
            directories = [p for p in target_dir.rglob("*") if p.is_dir()]
            for directory in sorted(directories, key=lambda p: len(p.parts), reverse=True):
                if not any(directory.iterdir()):
                    directory.rmdir()

    return {"sections": fetched_sections, "total": len(pages), "version": version_label}


def _split_full_export(text: str, page_prefix: str) -> Dict[str, str]:
    """Split a site's llms-full.txt into its pages, keyed by each page's `.md` URL.

    The export introduces every page with two lines, its title and where it
    came from:

        # Start Guide
        Source: https://nightwatch.laravel.com/docs/start-guide

    Only a `Source:` under `page_prefix` starts a page. Anything else that
    happens to look like one, a heading above a line of prose beginning
    "Source:", or a section copied in from another site, stays in the page it
    appears in. Returns an empty dict for text that holds no such page, which
    is what an HTML error page is.
    """
    boundary = re.compile(
        rf"(?m)^# (?P<title>[^\n]*)\nSource: (?P<url>{re.escape(page_prefix)}[A-Za-z0-9/._-]+)[ \t]*\n"
    )
    starts = list(boundary.finditer(text))
    pages: Dict[str, str] = {}
    for i, match in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        body = text[match.end():end].strip()
        url = match.group("url")
        if not url.endswith(".md"):
            url += ".md"
        pages.setdefault(url, f"# {match.group('title').strip()}\n\n{body}\n")
    return pages


_CALLOUT_LABELS = {"Note": "Note", "Info": "Note", "Check": "Note", "Tip": "Tip", "Warning": "Warning", "Danger": "Warning"}
_COMPONENT_TAG = re.compile(r"^<(?P<close>/)?(?P<name>[A-Z][A-Za-z0-9.]*)(?P<attrs>(?:\s[^>]*)?)>(?P<rest>.*)$")


def _clean_export_markup(text: str, origin: str, page_prefix: str = "") -> str:
    """Turn a page of a site's llms-full.txt export into plain markdown.

    The export is the page's source, with the documentation platform's
    components still in it. Left as they are they read as noise, and the text
    inside them is indented far enough that markdown takes it for a code
    block. This keeps what a component says and drops the tag:

        <Card title="Quickstart" href="/docs/quickstart">   **[Quickstart](.../docs/quickstart)**
        <Note> ... </Note>                                   **Note:** ...
        <Step title="Create it">, <Tab>, <Accordion>         **Create it**
        <Frame> ... </Frame>                                 dropped (it wraps an image)
        any other component tag on a line of its own         dropped

    Site-relative links are made absolute. A link that starts with the last
    segment of `page_prefix` ("/docs/runtimes" under ".../cloud/docs/") was
    written against the docs root and is resolved there; any other is
    resolved against `origin`. Nothing inside a fenced code block is touched.
    """
    docs_root = "/" + page_prefix.rstrip("/").rsplit("/", 1)[-1] + "/" if page_prefix else ""

    def resolve(path: str) -> str:
        if docs_root and path.startswith(docs_root):
            return page_prefix + path[len(docs_root):]
        return origin + path

    out: List[str] = []
    fence: Optional[str] = None
    fence_indent = 0
    in_frame = False
    pending_label: Optional[str] = None

    def attribute(attrs: str, key: str) -> Optional[str]:
        found = re.search(rf'\b{key}="([^"]*)"', attrs)
        return found.group(1) if found else None

    def absolute(line: str) -> str:
        return re.sub(r"\]\((/[^)\s]*)\)", lambda m: f"]({resolve(m.group(1))})", line)

    for raw in text.split("\n"):
        stripped = raw.strip()

        if fence is not None:
            # Inside a code block. Remove only the indentation the block
            # itself was nested by, so the code keeps its own.
            line = raw[fence_indent:] if raw[:fence_indent].strip() == "" else raw.lstrip()
            out.append(line)
            if stripped.startswith(fence) and stripped.strip(fence[0]) == "":
                fence = None
            continue

        opening = re.match(r"^(`{3,}|~{3,})", stripped)
        if opening and not in_frame:
            fence = opening.group(1)
            fence_indent = len(raw) - len(raw.lstrip())
            out.append(stripped)
            continue

        if in_frame:
            if "</Frame>" in stripped:
                in_frame = False
            continue
        if stripped.startswith("<Frame"):
            in_frame = "</Frame>" not in stripped
            continue
        if re.match(r"^<img\b[^>]*/?>$", stripped) or stripped == "&#x20;":
            continue

        tag = _COMPONENT_TAG.match(stripped)
        if tag:
            name, attrs = tag.group("name"), tag.group("attrs")
            rest = re.sub(rf"</{re.escape(name)}>\s*$", "", tag.group("rest")).strip()
            if tag.group("close"):
                continue
            if name in _CALLOUT_LABELS:
                label = f"**{_CALLOUT_LABELS[name]}:**"
                if rest:
                    out.append(absolute(f"{label} {rest}"))
                else:
                    pending_label = label
                continue
            title = attribute(attrs, "title") or attribute(attrs, "label")
            if title:
                href = attribute(attrs, "href")
                if href and href.startswith("/"):
                    href = resolve(href)
                out.append(f"**[{title}]({href})**" if href else f"**{title}**")
                if rest:
                    out.append(absolute(rest))
            elif rest and not rest.startswith("<"):
                out.append(absolute(rest))
            continue

        line = absolute(stripped if raw[:1] in (" ", "\t") and _is_component_text(raw) else raw)
        if pending_label and stripped:
            line = f"{pending_label} {line.lstrip()}"
            pending_label = None
        out.append(line)

    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"


def _is_component_text(line: str) -> bool:
    """Whether an indented line is prose nested inside a component, as opposed
    to a markdown construct that depends on its indentation (a nested list
    item or a continuation of one)."""
    stripped = line.lstrip()
    return not re.match(r"^([-*+]|\d+\.)\s", stripped)


def _write_versions_cache(versions: list[str], cache_file: Path) -> None:
    """Write versions to cache file. Errors are logged but not raised."""
    try:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps({
            "versions": versions,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }, indent=2))
    except Exception as e:
        logger.warning(f"Failed to write versions cache: {e}")


def _read_versions_cache(cache_file: Path, max_age_seconds: float | None = None) -> list[str] | None:
    """Read versions from cache file. Returns None if unavailable or corrupt.

    Args:
        cache_file: Path to the cache file.
        max_age_seconds: If set, ignore the cache when its timestamp is older
            than this (or missing/unparseable).
    """
    try:
        if not cache_file.exists():
            return None
        data = json.loads(cache_file.read_text())
        versions = data.get("versions")
        if not (isinstance(versions, list) and len(versions) > 0):
            return None

        # This list is the trust root for every version allowlist, and it is read
        # from a file that ships in the image, is tracked in git, and sits in a
        # directory users bind-mount and the server itself writes to. The API
        # response is filtered to this shape already; the cache never was, so a
        # single edited JSON value could smuggle "../.." past every check.
        versions = [v for v in versions if isinstance(v, str) and re.fullmatch(r"\d+\.x", v)]
        if not versions:
            logger.warning("Versions cache contained no well-formed version strings")
            return None

        if max_age_seconds is not None:
            updated_at = data.get("updated_at")
            if not updated_at:
                return None
            try:
                cached_at = datetime.fromisoformat(updated_at)
            except (TypeError, ValueError):
                return None
            if cached_at.tzinfo is None:
                cached_at = cached_at.replace(tzinfo=timezone.utc)
            age = (datetime.now(timezone.utc) - cached_at).total_seconds()
            if age > max_age_seconds:
                logger.debug(f"Versions cache is stale ({age:.0f}s old)")
                return None

        return versions
    except Exception as e:
        logger.warning(f"Failed to read versions cache: {e}")
        return None


def get_supported_versions(cache_file: Path | None = None) -> list[str]:
    """Get supported Laravel versions with three-tier fallback.

    1. Fresh cache file (docs/.versions_cache.json, younger than the TTL)
    2. GitHub API (writes cache on success)
    3. Stale cache file, then last resort: ["12.x"]

    The cache is consulted first: a network round trip on every process start
    is wasteful, and a stalled connection would otherwise block startup.

    Args:
        cache_file: Override cache file path (for testing). Defaults to VERSIONS_CACHE_FILE.

    Returns:
        List of supported version branches (e.g., ['6.x', '7.x', '8.x', ...])
    """
    if cache_file is None:
        cache_file = VERSIONS_CACHE_FILE

    fresh = _read_versions_cache(cache_file, max_age_seconds=VERSIONS_CACHE_TTL_SECONDS)
    if fresh:
        logger.debug(f"Using cached Laravel versions: {', '.join(fresh)}")
        return fresh

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

        with urllib.request.urlopen(request, timeout=DEFAULT_REQUEST_TIMEOUT) as response:
            branches = json.loads(response.read().decode())

            version_branches = []
            for branch in branches:
                name = branch["name"]
                if re.match(r'^\d+\.x$', name):
                    major_version = int(name.split('.')[0])
                    if major_version >= 6:
                        version_branches.append(name)

            version_branches.sort(key=lambda v: int(v.split('.')[0]))

            if not version_branches:
                logger.warning("No version branches found from API, trying cache")
                cached = _read_versions_cache(cache_file)
                if cached:
                    return cached
                logger.warning("No cache available, using last resort")
                return LAST_RESORT_VERSIONS

            logger.debug(f"Found {len(version_branches)} supported versions: {', '.join(version_branches)}")
            _write_versions_cache(version_branches, cache_file)
            return version_branches

    except Exception as e:
        logger.warning(f"Error fetching versions from GitHub API: {e}, trying cache")
        cached = _read_versions_cache(cache_file)
        if cached:
            return cached
        logger.warning("No cache available, using last resort")
        return LAST_RESORT_VERSIONS

# The supported versions, as one list object shared by every module that
# imports it. Importing this module reads the versions cache and nothing else:
# no request, no cache write. refresh_supported_versions() is the only path to
# the network, and it updates the list in place so that modules which bound the
# name at import see the result.
_SUPPORTED_VERSIONS_CACHE = None

def get_cached_supported_versions() -> list[str]:
    """The supported versions as last resolved. Never touches the network."""
    global _SUPPORTED_VERSIONS_CACHE
    if _SUPPORTED_VERSIONS_CACHE is None:
        _SUPPORTED_VERSIONS_CACHE = (
            _read_versions_cache(VERSIONS_CACHE_FILE) or list(LAST_RESORT_VERSIONS)
        )
    return _SUPPORTED_VERSIONS_CACHE

SUPPORTED_VERSIONS = get_cached_supported_versions()
# Frozen at import, so it goes stale after a refresh. Kept for importers that
# still read it; new code calls get_default_version().
DEFAULT_VERSION = SUPPORTED_VERSIONS[-1]


def get_default_version() -> str:
    """The newest supported version, as of the last refresh."""
    return SUPPORTED_VERSIONS[-1]


def refresh_supported_versions() -> list[str]:
    """Resolve the supported versions, asking GitHub if the cache has expired.

    Called once at startup by the server and by this module's command line. A
    failure leaves the versions already loaded in place: being offline must
    not stop the server from starting.
    """
    try:
        resolved = get_supported_versions()
    except Exception as e:
        logger.warning(f"Could not refresh the supported versions, keeping the cached list: {e}")
        return SUPPORTED_VERSIONS
    if resolved:
        SUPPORTED_VERSIONS[:] = resolved
    return SUPPORTED_VERSIONS


class DocumentationSourceType(Enum):
    """Types of documentation sources supported."""
    GITHUB_REPO = "github_repo"
    DIRECT_URL = "direct_url"
    LARAVEL_SERVICE = "laravel_service"
    COMMUNITY_PACKAGE = "community_package"

# The longest a single rate-limit pause may be, whatever the server asks for.
MAX_RATE_LIMIT_WAIT = 120


def _retry_after_seconds(error: urllib.error.HTTPError) -> Optional[float]:
    """The pause a 429 response asks for, in seconds, capped. None when the
    response gives no Retry-After or gives one that is not a number of seconds."""
    value = error.headers.get("Retry-After") if error.headers else None
    if value is None:
        return None
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        return None
    return min(MAX_RATE_LIMIT_WAIT, max(0.0, seconds))


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
        
        # Laravel services documentation sources. Each site publishes an
        # llms.txt index of its pages, served as markdown, so a service needs
        # only where its index is and which URLs in it belong to the docs:
        # no page list, no link pattern, no pinned version. Pages are
        # requested one at a time, as markdown, except where a service names
        # its single-file export in "llms_full".
        self.laravel_services = {
            "forge": {
                "name": "Laravel Forge",
                "type": DocumentationSourceType.LARAVEL_SERVICE,
                "base_url": "https://laravel.com/forge/docs",
                "llms_index": "https://laravel.com/forge/docs/llms.txt",
                "llms_page_prefix": "https://laravel.com/forge/docs/",
            },
            "vapor": {
                "name": "Laravel Vapor",
                "type": DocumentationSourceType.LARAVEL_SERVICE,
                "base_url": "https://docs.vapor.build",
                "llms_index": "https://docs.vapor.build/llms.txt",
                "llms_page_prefix": "https://docs.vapor.build/",
            },
            "envoyer": {
                "name": "Laravel Envoyer",
                "type": DocumentationSourceType.LARAVEL_SERVICE,
                "base_url": "https://docs.envoyer.io",
                "llms_index": "https://docs.envoyer.io/llms.txt",
                "llms_page_prefix": "https://docs.envoyer.io/",
            },
            "nova": {
                "name": "Laravel Nova",
                "type": DocumentationSourceType.LARAVEL_SERVICE,
                # Pages live under a major ("/docs/v5/..."); the newest one in
                # the index is fetched and saved without the version segment.
                "base_url": "https://nova.laravel.com/docs",
                "llms_index": "https://nova.laravel.com/docs/llms.txt",
                "llms_page_prefix": "https://nova.laravel.com/docs/",
            },
            "cloud": {
                "name": "Laravel Cloud",
                "type": DocumentationSourceType.LARAVEL_SERVICE,
                # cloud.laravel.com/docs redirects here. The prefix keeps the
                # fetch to Cloud's pages on a domain Forge's docs share.
                "base_url": "https://laravel.com/cloud/docs",
                "llms_index": "https://laravel.com/cloud/docs/llms.txt",
                "llms_page_prefix": "https://laravel.com/cloud/docs/",
                # 228 pages, too many to request one at a time: laravel.com
                # blocks the client partway through, and Forge and Laravel
                # Learn are on the same host. The export is one request.
                "llms_full": "https://laravel.com/cloud/docs/llms-full.txt",
                # The API reference is some 130 pages, each one the whole
                # OpenAPI document as YAML.
                "exclude_paths": ["api/"],
            },
            "nightwatch": {
                "name": "Laravel Nightwatch",
                "type": DocumentationSourceType.LARAVEL_SERVICE,
                "base_url": "https://nightwatch.laravel.com/docs",
                "llms_index": "https://nightwatch.laravel.com/docs/llms.txt",
                "llms_page_prefix": "https://nightwatch.laravel.com/docs/",
            },
            "herd": {
                "name": "Laravel Herd",
                "type": DocumentationSourceType.LARAVEL_SERVICE,
                # The index has a macos/ and a windows/ tree with the same page
                # names in each; pages are saved under their full path.
                "base_url": "https://herd.laravel.com/docs",
                "llms_index": "https://herd.laravel.com/docs/llms.txt",
                "llms_page_prefix": "https://herd.laravel.com/docs/",
            },
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
        """Check if the cached documentation for a service is still valid.

        Cache is considered invalid if:
        - Metadata file doesn't exist
        - Cache is older than cache_duration
        - Success rate is below 90%
        """
        metadata_path = self.get_cache_metadata_path(service)

        if not metadata_path.exists():
            return False

        try:
            # Read metadata to get cached_at timestamp and success_rate
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

            cache_time = metadata.get('cached_at', 0)
            success_rate = metadata.get('success_rate', 0.0)

            # Check if cache is too old
            is_fresh = (time.time() - cache_time) < self.cache_duration

            # Check if success rate is acceptable (90% threshold)
            is_quality = success_rate >= 0.9

            if not is_quality:
                logger.info(f"Cache for {service} has low success rate ({success_rate:.1%}), invalidating")
                return False

            return is_fresh
        except Exception as e:
            logger.warning(f"Error reading cache metadata for {service}: {str(e)}")
            return False
    
    def save_cache_metadata(self, service: str, metadata: Dict) -> None:
        """Save cache metadata for a service."""
        metadata_path = self.get_cache_metadata_path(service)

        # is_cache_valid ages the cache from this field. No fetch path stamped
        # it, so every cache read back as epoch-old and cache_duration was
        # decorative: each request refetched. setdefault keeps deliberate
        # back-dating (tests, manual invalidation) working.
        metadata.setdefault("cached_at", time.time())

        try:
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving cache metadata for {service}: {str(e)}")
    
    def fetch_laravel_service_docs(self, service: str, force: bool = False) -> bool:
        """
        Fetch documentation for a Laravel service.
        
        Args:
            service: Service name (forge, vapor, envoyer, nova)
            force: Refetch even if the cache is still valid
            
        Returns:
            True if successful, False otherwise
        """
        if service not in self.laravel_services:
            logger.error(f"Unknown Laravel service: {service}")
            return False
        
        # Check if cache is valid
        if not force and self.is_cache_valid(service):
            logger.debug(f"Using cached documentation for {service}")
            return True
        
        service_config = self.laravel_services[service]
        service_dir = self.get_service_cache_path(service)
        
        logger.info(f"Fetching documentation for {service_config['name']}")
        
        try:
            return self._fetch_service_from_index(service, service_config, service_dir)
        except Exception as e:
            logger.error(f"Error fetching documentation for {service}: {str(e)}")
            return False
    
    def _fetch_service_from_index(self, service: str, config: Dict, target_dir: Path) -> bool:
        """Fetch a Laravel service's documentation from its llms.txt index.

        Pages keep their path below the docs root ("servers/php.md"), so the
        laravel-external:// URIs that name them do not change.
        """
        result = fetch_llms_index_docs(
            name=config["name"],
            index_url=config["llms_index"],
            page_prefix=config["llms_page_prefix"],
            target_dir=target_dir,
            fetch=self._retry_request,
            layout="nested",
            full_url=config.get("llms_full"),
            exclude_paths=config.get("exclude_paths", ()),
        )
        if not result or not result["sections"]:
            return False

        metadata = {
            "service": service,
            "fetched_sections": result["sections"],
            "total_sections": result["total"],
            "success_rate": len(result["sections"]) / result["total"],
            "discovery_method": "llms-index",
            "index_url": config["llms_index"],
        }
        if result["version"]:
            metadata["version"] = result["version"]
        self.save_cache_metadata(service, metadata)
        logger.info(
            f"Successfully fetched {len(result['sections'])}/{result['total']} pages for {service} from its llms.txt index"
        )
        return True

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
                results[service] = self.fetch_laravel_service_docs(service, force=force)
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
                with urllib.request.urlopen(request, timeout=DEFAULT_REQUEST_TIMEOUT) as response:
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
                elif e.code == 429:
                    # The site is asking for a pause, not refusing the page.
                    # Wait as long as it says, or back off, and ask again.
                    if attempt < retries:
                        wait_time = _retry_after_seconds(e)
                        if wait_time is None:
                            wait_time = min(MAX_RATE_LIMIT_WAIT, (2 ** attempt) * 10 + random.uniform(0, 5))
                        logger.warning(f"Rate limited (429) on attempt {attempt + 1}/{retries + 1}, retrying in {wait_time:.1f}s")
                        time.sleep(wait_time)
                    else:
                        raise
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
        # `version` is joined onto target_dir, so validate before any mkdir.
        # Callers include MCP tools, which may pass caller-supplied values.
        if not is_safe_section_name(version) or '/' in version:
            raise ValueError(f"Invalid Laravel version: {version!r}")

        self.target_dir = target_dir
        self.version = version
        self.github_api_url = GITHUB_API_URL
        self.repo = LARAVEL_DOCS_REPO

        # Create version-specific directory. update() clears everything under
        # version_dir, so it must be a strict subdirectory of target_dir --
        # equality would wipe every version in the documentation root.
        #
        # Compare the parent rather than resolving version_dir itself: the name
        # checks above already guarantee a single path component, and resolving
        # through a symlink rejected legitimately-relocated version directories,
        # which aborted server startup rather than just the update path.
        self.version_dir = target_dir / version
        if self.version_dir.parent.resolve() != target_dir.resolve():
            raise ValueError(f"Version directory escapes target directory: {version!r}")
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
                
                with urllib.request.urlopen(request, timeout=DEFAULT_REQUEST_TIMEOUT) as response:
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
        
        # Create a temporary directory (persists after function exits)
        # Note: Using mkdtemp instead of TemporaryDirectory for Python 3.9 compatibility
        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir)

        try:
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

                    with urllib.request.urlopen(request, timeout=DEFAULT_REQUEST_TIMEOUT) as response, open(zip_path, 'wb') as out_file:
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
    
    def needs_update(self, latest_commit: Optional[Dict[str, str]] = None) -> bool:
        """Check if documentation needs to be updated based on remote commits.

        Args:
            latest_commit: Already-fetched commit info, to avoid a redundant
                GitHub API request (the unauthenticated limit is 60/hour).
        """
        try:
            # Get the latest commit info
            if latest_commit is None:
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
        # Fetch the commit once and reuse it for both the up-to-date check and
        # the metadata written below, instead of hitting the API twice.
        latest_commit: Optional[Dict[str, str]] = None
        if not force:
            try:
                latest_commit = self.get_latest_commit()
            except Exception as e:
                logger.error(f"Error checking for updates: {str(e)}")
                logger.info("Assuming update is needed due to error")

            if latest_commit is not None and not self.needs_update(latest_commit):
                return False

        try:
            # Get the latest commit info for metadata
            if latest_commit is None:
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


class CommunityPackageFetcher:
    """Handles fetching documentation from community Laravel packages."""
    
    def __init__(self, target_dir: Path, cache_duration: int = 86400, max_retries: int = 3):
        """
        Initialize the community package documentation fetcher.
        
        Args:
            target_dir: Directory where package docs should be stored
            cache_duration: Cache duration in seconds (default: 24 hours)
            max_retries: Maximum number of retry attempts for failed requests
        """
        self.target_dir = target_dir
        self.cache_duration = cache_duration
        self.max_retries = max_retries
        self.packages_dir = target_dir / "packages"
        self.packages_dir.mkdir(parents=True, exist_ok=True)
        
        # Community packages documentation sources
        self.community_packages = {
            "spatie": {
                "name": "Spatie Packages",
                "type": DocumentationSourceType.COMMUNITY_PACKAGE,
                "base_url": "https://spatie.be/docs",
                "packages": {
                    "laravel-permission": {
                        "name": "Laravel Permission",
                        "docs_url": "https://spatie.be/docs/laravel-permission/v6/introduction",
                        "version_pattern": r'/v(\d+)/',
                        "sections": [
                            "introduction", "installation-laravel", "basic-usage/basic-usage",
                            "basic-usage/role-permissions", "basic-usage/direct-permissions",
                            "basic-usage/multiple-guards", "basic-usage/teams-permissions",
                            "basic-usage/blade-directives", "basic-usage/artisan",
                            "basic-usage/middleware", "basic-usage/wildcard-permissions",
                            "advanced-usage/cache", "advanced-usage/extending",
                            "advanced-usage/exceptions", "advanced-usage/seeding",
                            "advanced-usage/testing", "api/models", "api/traits"
                        ]
                    },
                    "laravel-medialibrary": {
                        "name": "Laravel Media Library",
                        "docs_url": "https://spatie.be/docs/laravel-medialibrary/v11/introduction",
                        "version_pattern": r'/v(\d+)/',
                        "sections": [
                            "introduction", "installation-setup", "basic-usage/associating-files",
                            "basic-usage/retrieving-media", "converting-images/defining-conversions",
                            "converting-images/retrieving-converted-images", "responsive-images",
                            "downloading-media/downloading-a-single-file", "advanced-usage/using-s3"
                        ]
                    },
                    "laravel-backup": {
                        "name": "Laravel Backup",
                        "docs_url": "https://spatie.be/docs/laravel-backup/v9/introduction",
                        "version_pattern": r'/v(\d+)/',
                        "sections": [
                            "introduction", "installation-and-setup", "backing-up/overview",
                            "backing-up/events", "cleaning-up-old-backups/overview",
                            "sending-notifications/overview", "monitoring-health/overview"
                        ]
                    }
                }
            },
            "livewire": {
                "name": "Livewire",
                "type": DocumentationSourceType.COMMUNITY_PACKAGE,
                "base_url": "https://livewire.laravel.com/docs",
                "sections": [
                    "quickstart", "installation", "components", "properties", "actions",
                    "forms", "lifecycle-hooks", "nesting", "events", "security",
                    "uploads", "downloads", "validation", "pagination",
                    "redirecting", "wire-model", "wire-click", "wire-submit", 
                    "wire-loading", "wire-transition", "wire-poll", "wire-init", 
                    "wire-dirty", "wire-offline", "alpine", "morphing", "teleport",
                    "lazy", "locked", "computed-properties", "url", "navigate", 
                    "offline", "testing", "troubleshooting", "javascript"
                ]
            },
            "inertia": {
                "name": "Inertia.js",
                "type": DocumentationSourceType.DIRECT_URL,
                # The old JSX source repo (inertiajs/inertiajs.com) was deleted
                # upstream; the site publishes markdown endpoints indexed by
                # llms.txt, and the fetcher discovers pages from that index.
                "llms_index": "https://inertiajs.com/docs/llms.txt",
                "llms_page_prefix": "https://inertiajs.com/docs/",
                # Final URL segment ("routing.md"): unique within one major
                # version, and what existing catalog links point at.
                "llms_filenames": "basename",
            },
            "filament": {
                "name": "Filament",
                "type": DocumentationSourceType.COMMUNITY_PACKAGE,
                "base_url": "https://filamentphp.com/docs",
                # No pinned version and no page list. The site's llms.txt names
                # the current major and every page in it, served as markdown.
                # The previous config pinned "3.x" and listed 62 pages by hand:
                # it was two majors behind and seven of its pages 404'd.
                "llms_index": "https://filamentphp.com/docs/llms.txt",
                "llms_page_prefix": "https://filamentphp.com/docs/",
                # Path below the version ("forms-text-input.md"): Filament has
                # an overview.md in most sections, so the final segment alone
                # would collide.
                "llms_filenames": "path",
            },
            "debugbar": {
                "name": "Laravel Debugbar",
                "type": DocumentationSourceType.COMMUNITY_PACKAGE,
                "base_url": "https://laraveldebugbar.com",
                "sections": [
                    "installation", "usage", "features", "collectors"
                ]
            },
            "ide-helper": {
                "name": "Laravel IDE Helper",
                "type": DocumentationSourceType.GITHUB_REPO,
                "repo": "barryvdh/laravel-ide-helper",
                "branch": "master",
                "file": "README.md"
            }
        }
    
    def get_package_cache_path(self, package: str, subpackage: Optional[str] = None) -> Path:
        """Get the cache directory path for a package."""
        if subpackage:
            package_dir = self.packages_dir / package / subpackage
        else:
            package_dir = self.packages_dir / package
        package_dir.mkdir(parents=True, exist_ok=True)
        return package_dir
    
    def get_cache_metadata_path(self, package: str, subpackage: Optional[str] = None) -> Path:
        """Get the cache metadata file path for a package."""
        cache_dir = self.get_package_cache_path(package, subpackage)
        return cache_dir / ".metadata" / "cache.json"
    
    def is_cache_valid(self, package: str, subpackage: Optional[str] = None) -> bool:
        """Check if the cache for a package is still valid.

        Age is read from the timestamp stored in the metadata, not from the
        file's mtime. The daily sync runs in a fresh clone, where every mtime
        is the checkout time, so an mtime check called every package fresh on
        every run and nothing was ever refetched.
        """
        # Spatie has no metadata of its own, only one file per sub-package.
        if subpackage is None:
            sub_packages = self.community_packages.get(package, {}).get("packages")
            if isinstance(sub_packages, dict) and sub_packages:
                return all(self.is_cache_valid(package, sub) for sub in sub_packages)

        metadata_path = self.get_cache_metadata_path(package, subpackage)

        if not metadata_path.exists():
            return False

        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

            # `cache_time` is the key older committed metadata carries.
            cache_time = float(metadata.get("cached_at") or metadata.get("cache_time") or 0)

            if time.time() - cache_time > self.cache_duration:
                logger.debug(f"Cache expired for {package}/{subpackage or 'all'}")
                return False

            return True
        except Exception as e:
            logger.warning(f"Error reading cache metadata for {package}: {str(e)}")
            return False

    def save_cache_metadata(self, package: str, metadata: Dict, subpackage: Optional[str] = None) -> None:
        """Write cache metadata for a package, stamping when it was fetched."""
        metadata.setdefault("cached_at", time.time())

        metadata_path = self.get_cache_metadata_path(package, subpackage)
        metadata_path.parent.mkdir(parents=True, exist_ok=True)

        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def fetch_package_docs(self, package: str, force: bool = False) -> bool:
        """
        Fetch documentation for a community package.
        
        Args:
            package: Package name (spatie, livewire, inertia, filament)
            force: Force refresh even if cache is valid
            
        Returns:
            True if successful, False otherwise
        """
        if package not in self.community_packages:
            logger.error(f"Unknown package: {package}")
            return False
        
        # Check cache validity
        if not force and self.is_cache_valid(package):
            logger.info(f"Using cached documentation for {package}")
            return True
        
        logger.info(f"Fetching documentation for {package}")
        package_config = self.community_packages[package]
        
        try:
            if package == "spatie":
                return self._fetch_spatie_docs(package_config)
            elif package == "livewire":
                return self._fetch_livewire_docs(package_config)
            elif package == "inertia":
                return self._fetch_inertia_docs(package_config)
            elif package == "filament":
                return self._fetch_filament_docs(package_config)
            elif package == "debugbar":
                return self._fetch_debugbar_docs(package_config)
            elif package == "ide-helper":
                return self._fetch_ide_helper_docs(package_config)
            else:
                logger.error(f"No fetch method implemented for package: {package}")
                return False
        except Exception as e:
            logger.error(f"Error fetching {package} documentation: {str(e)}")
            return False
    
    def _fetch_raw(self, url: str) -> bytes:
        """One GET, following redirects, with the project's user agent."""
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=DEFAULT_REQUEST_TIMEOUT) as response:
            return response.read()

    def _discover_pages(self, landing_url: str, link_pattern: str, name: str) -> Optional[tuple[str, List[str]]]:
        """The major version a package's docs are on, and its pages, read
        from the navigation of one of its pages.

        `link_pattern` matches a documentation link and captures the version
        and the page path. A docs page links every page of the current major
        in its navigation and, in a version switcher, one page of each older
        major, so the current major is the one most links point at. Returns
        (version, pages in navigation order) or None when the page cannot be
        read or shows no navigation.
        """
        try:
            html_text = self._fetch_raw(landing_url).decode("utf-8", errors="replace")
        except Exception as e:
            logger.warning(f"Could not read the {name} docs navigation: {str(e)}")
            return None

        by_version: Dict[str, List[str]] = {}
        for version, page in re.findall(link_pattern, html_text):
            pages = by_version.setdefault(version, [])
            if page not in pages and is_safe_section_name(page):
                pages.append(page)
        if not by_version:
            return None

        def major(version: str) -> int:
            digits = re.search(r"\d+", version)
            return int(digits.group()) if digits else 0

        version, pages = max(by_version.items(), key=lambda item: (len(item[1]), major(item[0])))
        # A lone link is a version switcher entry, not a navigation.
        if len(pages) < 3:
            return None
        return version, pages

    def _discover_spatie_package(self, package_key: str, docs_root: str) -> Optional[tuple[str, List[str]]]:
        """`docs_root/<package>` redirects to the current major's introduction,
        whose navigation links every page as an absolute URL."""
        return self._discover_pages(
            f"{docs_root}/{package_key}",
            rf'href="{re.escape(docs_root)}/{re.escape(package_key)}/(v\d+)/([a-z0-9][a-z0-9/-]*)"',
            f"Spatie {package_key}",
        )

    def _fetch_spatie_docs(self, config: Dict) -> bool:
        """Fetch documentation for Spatie packages.

        Each package's version and page list are read from the site. The
        `docs_url` and `sections` in the configuration are the fallback for a
        night when the landing page cannot be read.
        """
        success_count = 0
        packages = config.get("packages", {})
        docs_root = config.get("base_url", "https://spatie.be/docs")

        for package_key, package_info in packages.items():
            try:
                logger.info(f"Fetching Spatie {package_info['name']} documentation")
                package_dir = self.get_package_cache_path("spatie", package_key)

                discovered = self._discover_spatie_package(package_key, docs_root)
                if discovered:
                    version, sections = discovered
                    base_url = f"{docs_root}/{package_key}/{version}"
                    logger.info(f"Spatie {package_info['name']} is on {version} with {len(sections)} pages")
                else:
                    base_url = package_info["docs_url"].rsplit('/', 1)[0]
                    sections = package_info.get("sections", [])
                    pinned = re.search(r"/(v\d+)$", base_url)
                    version = pinned.group(1) if pinned else ""
                    logger.warning(f"Using the pinned version and page list for Spatie {package_info['name']}")

                saved_files = []
                for section in sections:
                    section_url = f"{base_url}/{section}"
                    content = self._fetch_and_process_content(section_url, "spatie", section)

                    if content:
                        # Save the processed content
                        file_path = package_dir / f"{section.replace('/', '-')}.md"
                        file_path.parent.mkdir(parents=True, exist_ok=True)

                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)

                        saved_files.append(file_path)

                fetched_sections = len(saved_files)
                if fetched_sections > 0:
                    if fetched_sections == len(sections):
                        self._prune_unlisted_pages(package_dir, saved_files, f"Spatie {package_info['name']}")

                    # Update cache metadata
                    metadata = {
                        "package": package_key,
                        "name": package_info['name'],
                        "sections_count": fetched_sections,
                        "total_sections": len(sections),
                        "success_rate": fetched_sections / len(sections),
                        "base_url": base_url,
                        "source_type": "site_navigation" if discovered else "pinned_list",
                    }
                    if version:
                        metadata["version"] = version

                    self.save_cache_metadata("spatie", metadata, subpackage=package_key)

                    success_count += 1
                    logger.info(f"Successfully fetched {fetched_sections} sections for Spatie {package_info['name']}")

            except Exception as e:
                logger.error(f"Error fetching Spatie {package_key} documentation: {str(e)}")

        return success_count > 0

    def _prune_unlisted_pages(self, directory: Path, kept: List[Path], name: str) -> None:
        """Remove saved pages a complete sync did not write.

        Called only after every listed page was fetched: pages left over then
        are ones the site dropped or renamed. A partial sync must not call
        this, or a failed fetch would delete the copy it failed to replace.
        """
        expected = {path.resolve() for path in kept}
        for stale in sorted(directory.glob("*.md")):
            if stale.resolve() not in expected:
                logger.info(f"Pruning {name} page no longer listed: {stale.name}")
                stale.unlink()

    def _fetch_livewire_docs(self, config: Dict) -> bool:
        """Fetch Livewire documentation.

        The major version and the page list are read from the site's
        navigation. The `sections` in the configuration, requested without a
        version in the URL, are the fallback for a night when it cannot be.
        """
        base_url = config["base_url"]
        package_dir = self.get_package_cache_path("livewire")

        # Any docs URL without a version redirects to the current major.
        discovered = self._discover_pages(
            f"{base_url}/quickstart",
            r'href="(?:https://livewire\.laravel\.com)?/docs/(\d+\.x)/([a-z0-9][a-z0-9/-]*)"',
            "Livewire",
        )
        if discovered:
            version: Optional[str] = discovered[0]
            sections = discovered[1]
            pages_url = f"{base_url}/{version}"
            logger.info(f"Livewire is on {version} with {len(sections)} pages")
        else:
            version = None
            sections = config.get("sections", [])
            pages_url = base_url
            logger.warning("Using the pinned page list for Livewire")

        saved_files = []
        for section in sections:
            try:
                section_url = f"{pages_url}/{section}"
                content = self._fetch_and_process_content(section_url, "livewire", section)

                if content:
                    file_path = package_dir / f"{section.replace('/', '-')}.md"
                    file_path.parent.mkdir(parents=True, exist_ok=True)

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                    saved_files.append(file_path)
            except Exception as e:
                logger.warning(f"Error fetching Livewire section {section}: {str(e)}")

        fetched_sections = len(saved_files)
        if fetched_sections > 0:
            if fetched_sections == len(sections):
                self._prune_unlisted_pages(package_dir, saved_files, "Livewire")

            # Update cache metadata
            metadata = {
                "package": "livewire",
                "name": config['name'],
                "sections_count": fetched_sections,
                "total_sections": len(sections),
                "success_rate": fetched_sections / len(sections),
                "base_url": pages_url,
                "source_type": "site_navigation" if discovered else "pinned_list",
            }
            if version:
                metadata["version"] = version

            self.save_cache_metadata("livewire", metadata)

            logger.info(f"Successfully fetched {fetched_sections} sections for Livewire")
            return True

        return False

    def _fetch_inertia_docs(self, config: Dict) -> bool:
        """Fetch Inertia.js documentation from its llms.txt markdown index.

        The old source repo of JSX pages (inertiajs/inertiajs.com) was deleted
        upstream; the site now publishes clean markdown at .md endpoints with
        an llms.txt index.
        """
        return self._fetch_llms_index_docs("inertia", config)

    def _fetch_llms_index_docs(self, package: str, config: Dict) -> bool:
        """Fetch a package's documentation from the llms.txt index its site publishes.

        See fetch_llms_index_docs. Filenames come from the page URL: its final
        segment, or its whole path below the version, per `llms_filenames`.
        """
        def fetch(url: str) -> bytes:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=DEFAULT_REQUEST_TIMEOUT) as response:
                return response.read()

        name = config["name"]
        result = fetch_llms_index_docs(
            name=name,
            index_url=config["llms_index"],
            page_prefix=config["llms_page_prefix"],
            target_dir=self.get_package_cache_path(package),
            fetch=fetch,
            layout="flat" if config.get("llms_filenames") == "path" else "basename",
        )
        if not result or not result["sections"]:
            return False

        fetched = len(result["sections"])
        metadata = {
            "package": package,
            "name": name,
            "sections_count": fetched,
            "total_sections": result["total"],
            "success_rate": fetched / result["total"],
            "source_type": "llms_index",
            "index_url": config["llms_index"],
        }
        if result["version"]:
            metadata["version"] = result["version"]
        self.save_cache_metadata(package, metadata)
        logger.info(f"Successfully fetched {fetched}/{result['total']} {name} pages")
        return True

    def _fetch_filament_docs(self, config: Dict) -> bool:
        """Fetch Filament documentation from its llms.txt markdown index."""
        return self._fetch_llms_index_docs("filament", config)

    def _fetch_debugbar_docs(self, config: Dict) -> bool:
        """Fetch Laravel Debugbar documentation from website."""
        base_url = config["base_url"]
        sections = config.get("sections", [])
        package_dir = self.get_package_cache_path("debugbar")

        fetched_sections = 0
        saved_files: List[Path] = []
        for section in sections:
            try:
                section_url = f"{base_url}/{section}/"
                content = self._fetch_and_process_content(section_url, "debugbar", section)
                
                if content:
                    file_path = package_dir / f"{section}.md"
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    fetched_sections += 1
                    saved_files.append(file_path)
            except Exception as e:
                logger.warning(f"Error fetching Debugbar section {section}: {str(e)}")

        if fetched_sections > 0:
            if fetched_sections == len(sections):
                self._prune_unlisted_pages(package_dir, saved_files, "Laravel Debugbar")
            # Update cache metadata
            metadata = {
                "package": "debugbar",
                "name": config['name'],
                "sections_count": fetched_sections,
                "total_sections": len(sections),
                "success_rate": fetched_sections / len(sections),
                "base_url": base_url
            }
            
            self.save_cache_metadata("debugbar", metadata)
            
            logger.info(f"Successfully fetched {fetched_sections} sections for Laravel Debugbar")
            return True
        
        return False
    
    def _fetch_ide_helper_docs(self, config: Dict) -> bool:
        """Fetch Laravel IDE Helper documentation from GitHub README."""
        repo = config["repo"]
        branch = config.get("branch", "master")
        file = config.get("file", "README.md")
        package_dir = self.get_package_cache_path("ide-helper")
        
        try:
            # Fetch README from GitHub
            github_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{file}"
            
            logger.info(f"Fetching IDE Helper documentation from {github_url}")
            
            request = urllib.request.Request(
                github_url,
                headers={"User-Agent": USER_AGENT}
            )
            
            with urllib.request.urlopen(request, timeout=DEFAULT_REQUEST_TIMEOUT) as response:
                content = response.read().decode('utf-8')
            
            # Process the README content
            if content:
                # Add header
                header = f"# {config['name']}\n\n"
                header += f"Source: https://github.com/{repo}\n\n"
                header += "---\n\n"
                
                # Save the processed content
                file_path = package_dir / "readme.md"
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(header + content)
                
                # Update cache metadata
                metadata = {
                    "package": "ide-helper",
                    "name": config['name'],
                    "source_type": "github_readme",
                    "repo": repo,
                    "branch": branch,
                    "file": file
                }
                
                self.save_cache_metadata("ide-helper", metadata)
                
                logger.info("Successfully fetched documentation for Laravel IDE Helper")
                return True
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                logger.error(f"IDE Helper README not found at {github_url}")
            else:
                logger.error(f"HTTP error fetching IDE Helper documentation: {e}")
        except Exception as e:
            logger.error(f"Error fetching IDE Helper documentation: {str(e)}")
        
        return False
    
    def _fetch_and_process_content(self, url: str, package: str, section: str) -> Optional[str]:
        """Fetch and process content from a URL."""
        try:
            # Use markdownify for HTML to Markdown conversion
            from markdownify import markdownify as md
            from bs4 import BeautifulSoup
            
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/html,application/xhtml+xml"
                }
            )
            
            with urllib.request.urlopen(request, timeout=DEFAULT_REQUEST_TIMEOUT) as response:
                content_bytes = response.read()
                content = content_bytes.decode('utf-8')
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove navigation, header, footer elements
            for tag in soup.find_all(['nav', 'header', 'footer', 'aside']):
                tag.decompose()
            
            # Remove stats/metrics elements that contain dynamic numbers
            # For Spatie packages, remove elements that contain download counts and issue numbers
            if package == "spatie":
                # Find and remove the stats section that appears at the top of Spatie docs
                # This typically contains Repository, Open Issues, and download counts
                stats_removed = False
                
                # Look for the pattern: Repository -> Open Issues -> large numbers
                for element in soup.find_all(string=re.compile(r'^Repository$', re.I)):
                    # Find the container that holds this stats section
                    container = element.parent
                    while container and container.name not in ['body', 'html', 'main', 'article']:
                        # Check if this container has "Open Issues" and large numbers
                        text_content = container.get_text()
                        if 'Open Issues' in text_content and re.search(r'\d{3,}', text_content):
                            # This looks like the stats container
                            container.decompose()
                            stats_removed = True
                            logger.debug(f"Removed stats container from {url}")
                            break
                        # Try parent container
                        if container.parent and container.parent.name in ['div', 'section', 'aside', 'header']:
                            container = container.parent
                        else:
                            break
                    if stats_removed:
                        break
                
                # Also remove any standalone large numbers that might be stats
                for text_node in soup.find_all(string=re.compile(r'^\s*[\d,]+\s*$')):
                    if text_node.parent:
                        num_str = str(text_node).strip().replace(',', '')
                        try:
                            # Remove numbers larger than 1000 (likely stats, not code examples)
                            if num_str.isdigit() and int(num_str) > 1000:
                                # Don't remove if it's inside a code block
                                if not any(p.name in ['code', 'pre'] for p in text_node.parents):
                                    text_node.parent.extract()
                        except Exception:
                            pass
                
                # Remove any divs or sections that look like stats containers
                for tag in soup.find_all(['div', 'section'], class_=re.compile(r'stats|metrics|numbers|count', re.I)):
                    tag.decompose()
            
            # Try to find main content area
            main_content = None
            
            # Package-specific selectors
            if package == "inertia":
                # Inertia uses div with id="top" for main content
                main_content = soup.find('div', id='top')
                if not main_content:
                    logger.debug(f"Could not find #top div for Inertia on {url}")
            elif package == "filament":
                # Filament might use different selectors
                main_content = soup.select_one('.docs-content, .prose, main')
            elif package == "debugbar":
                # Debugbar documentation site selectors
                main_content = soup.select_one('.prose, .content, main, article')
            
            # If no package-specific selector worked, try common selectors
            if not main_content:
                content_selectors = [
                    '#top',  # Try #top first as it seems common
                    'main', 'article', '[role="main"]', '.content', '.docs-content',
                    '.documentation', '#content', '.prose', '.markdown-body'
                ]
                
                for selector in content_selectors:
                    main_content = soup.select_one(selector)
                    if main_content:
                        logger.debug(f"Found content using selector: {selector}")
                        break
            
            if not main_content:
                logger.warning(f"Could not find main content area for {url}, using body")
                main_content = soup.find('body') or soup
            
            # Convert to markdown
            markdown_content = md(str(main_content), strip=['a'], code_language='php')
            
            # Clean up the content
            markdown_content = self._clean_markdown_content(markdown_content)
            
            # Check if we got any actual content
            if len(markdown_content.strip()) < 50:
                logger.warning(f"Very little content extracted from {url} (len: {len(markdown_content.strip())})")
                # Log first 200 chars of HTML to debug
                html_preview = str(main_content)[:500]
                logger.debug(f"HTML preview: {html_preview}")
            
            # Add metadata header
            header = f"# {package.title()} - {section.replace('-', ' ').title()}\n\n"
            header += f"Source: {url}\n\n"
            
            return header + markdown_content
            
        except Exception as e:
            logger.error(f"Error fetching content from {url}: {str(e)}")
            return None
    
    def _clean_markdown_content(self, content: str) -> str:
        """Clean up markdown content."""
        # Remove excessive blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Fix code blocks
        content = re.sub(r'```\s*\n', '```\n', content)
        
        # Remove CloudFlare email protection links
        # Catch all CloudFlare email protection links regardless of link text
        # Note: markdownify escapes @ as \@, creating patterns like [[email protected]]
        content = re.sub(
            r'\[+[^\]]*\]+\(/cdn-cgi/l/email-protection[^)]*\)',
            '[email protected]',
            content
        )
        
        # Remove trailing whitespace
        content = '\n'.join(line.rstrip() for line in content.split('\n'))

        # Livewire's docs open every page with an advertisement for its paid
        # UI kit. Matched as the whole block, so prose that mentions the
        # product is left alone.
        content = re.sub(
            r"The official Livewire UI kit\n+Build polished Livewire apps faster\.\n+Explore Flux Pro\n+→\n+",
            "",
            content,
        )

        # Remove social media links
        content = remove_social_media_lines(content)

        # Remove image references
        content = remove_image_references(content)

        return content.strip()

    def list_available_packages(self) -> List[str]:
        """List all available community packages."""
        return list(self.community_packages.keys())
    
    def fetch_all_packages(self, force: bool = False) -> Dict[str, bool]:
        """
        Fetch documentation for all community packages.
        
        Args:
            force: Force refresh even if cache is valid
            
        Returns:
            Dictionary mapping package names to success status
        """
        results = {}
        
        for package in self.list_available_packages():
            logger.info(f"Processing community package: {package}")
            results[package] = self.fetch_package_docs(package, force=force)
        
        # Log summary
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        logger.info(f"Community package documentation update complete: {success_count}/{total_count} packages")
        
        return results


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
        
        # Initialize community package fetcher
        self.package_fetcher = CommunityPackageFetcher(target_dir)

        # Initialize learning resource fetcher
        self.learning_fetcher = LearningResourceFetcher(target_dir)

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
    
    def update_package_docs(self, packages: Optional[List[str]] = None, force: bool = False) -> Dict[str, bool]:
        """
        Update community package documentation.
        
        Args:
            packages: List of specific packages to update. If None, updates all.
            force: Force refresh even if cache is valid
            
        Returns:
            Dictionary mapping package names to success status
        """
        logger.info("Updating community package documentation")
        
        if packages:
            results = {}
            for package in packages:
                if package in self.package_fetcher.community_packages:
                    results[package] = self.package_fetcher.fetch_package_docs(package, force=force)
                else:
                    logger.error(f"Unknown package: {package}")
                    results[package] = False
            return results
        else:
            return self.package_fetcher.fetch_all_packages(force=force)

    def update_learning_docs(self, sources: Optional[List[str]] = None, force: bool = False) -> Dict[str, bool]:
        """
        Update learning resource documentation.

        Args:
            sources: List of specific sources to update. If None, updates all.
            force: Force refresh even if cache is valid

        Returns:
            Dictionary mapping source names to success status
        """
        logger.info("Updating learning resource documentation")

        if sources:
            results = {}
            for source in sources:
                if source in self.learning_fetcher.learning_sources:
                    results[source] = self.learning_fetcher.fetch_learning_source(source, force=force)
                else:
                    logger.error(f"Unknown learning source: {source}")
                    results[source] = False
            return results
        else:
            return self.learning_fetcher.fetch_all_sources(force=force)

    def update_all(self, force_core: bool = False, force_external: bool = False, force_packages: bool = False, force_learning: bool = False) -> Dict[str, object]:
        """
        Update all documentation sources.

        Args:
            force_core: Force update of core documentation
            force_external: Force update of external documentation
            force_packages: Force update of community packages
            force_learning: Force update of learning resources

        Returns:
            Dictionary with results for core, external, package, and learning updates
        """
        logger.info("Starting comprehensive documentation update")

        results: Dict[str, object] = {
            "core": False,
            "external": {},
            "packages": {},
            "learning": {}
        }

        try:
            # Update core Laravel documentation. "core" records whether the
            # docs changed; a failure is recorded on its own and does not
            # stop the other sources from being updated.
            try:
                results["core"] = self.update_core_docs(force=force_core)
            except Exception as e:
                logger.error(f"Core documentation update failed: {str(e)}")
                results["core_error"] = str(e)

            # Update external services documentation
            results["external"] = self.update_external_docs(force=force_external)

            # Update community package documentation
            results["packages"] = self.update_package_docs(force=force_packages)

            # Update learning resource documentation
            results["learning"] = self.update_learning_docs(force=force_learning)

            # Log summary
            core_status = "updated" if results["core"] else "up-to-date"
            external_results = results["external"]
            package_results = results["packages"]
            learning_results = results["learning"]

            if isinstance(external_results, dict):
                external_count = sum(1 for success in external_results.values() if success)
                total_external = len(external_results)
            else:
                external_count = 0
                total_external = 0

            if isinstance(package_results, dict):
                package_count = sum(1 for success in package_results.values() if success)
                total_packages = len(package_results)
            else:
                package_count = 0
                total_packages = 0

            if isinstance(learning_results, dict):
                learning_count = sum(1 for success in learning_results.values() if success)
                total_learning = len(learning_results)
            else:
                learning_count = 0
                total_learning = 0

            logger.info(f"Documentation update complete: Core {core_status}, External {external_count}/{total_external}, Packages {package_count}/{total_packages}, Learning {learning_count}/{total_learning}")
            
        except Exception as e:
            logger.error(f"Error during comprehensive documentation update: {str(e)}")
        
        return results
    
    def get_all_documentation_status(self) -> Dict[str, Dict]:
        """Get status information for all documentation sources."""
        status: Dict[str, Dict] = {
            "core": {},
            "external": {},
            "packages": {},
            "learning": {}
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
                    "last_fetched": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(metadata_path.stat().st_mtime)) if metadata_path.exists() else "never",
                    "success_rate": metadata.get("success_rate", "unknown")
                }
            except Exception as e:
                status["external"][service] = {"error": str(e)}
        
        # Get community package documentation status
        for package in self.package_fetcher.list_available_packages():
            try:
                cache_valid = self.package_fetcher.is_cache_valid(package)
                package_info = self.package_fetcher.community_packages.get(package, {})
                
                # Try to read cache metadata
                metadata_path = self.package_fetcher.get_cache_metadata_path(package)
                if metadata_path.exists():
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                    except Exception:
                        metadata = {}
                else:
                    metadata = {}
                
                # Get the type value safely
                package_type = package_info.get("type", DocumentationSourceType.COMMUNITY_PACKAGE)
                if hasattr(package_type, 'value'):
                    type_value = package_type.value
                else:
                    type_value = str(package_type) if package_type else "community_package"
                
                status["packages"][package] = {
                    "name": package_info.get("name", package),
                    "type": type_value,
                    "cache_valid": cache_valid,
                    "last_fetched": metadata.get("cached_at", metadata.get("cache_time", "never")),
                    "sections_count": metadata.get("sections_count", 0)
                }
                
                # For Spatie, include sub-packages
                if package == "spatie" and "packages" in package_info:
                    status["packages"][package]["sub_packages"] = {}
                    packages_dict = package_info.get("packages", {})
                    if isinstance(packages_dict, dict):
                        for sub_pkg, sub_info in packages_dict.items():
                            sub_metadata_path = self.package_fetcher.get_cache_metadata_path("spatie", sub_pkg)
                            if sub_metadata_path.exists():
                                try:
                                    with open(sub_metadata_path, 'r') as f:
                                        sub_metadata = json.load(f)
                                    status["packages"][package]["sub_packages"][sub_pkg] = {
                                        "name": sub_info.get("name", sub_pkg),
                                        "sections_count": sub_metadata.get("sections_count", 0)
                                    }
                                except Exception:
                                    pass
                
            except Exception as e:
                status["packages"][package] = {"error": str(e)}

        # Get learning resource documentation status
        for source in self.learning_fetcher.list_available_sources():
            try:
                cache_valid = self.learning_fetcher.is_cache_valid(source)
                source_info = self.learning_fetcher.get_source_info(source)

                if source_info is None:
                    continue

                # Try to read cache metadata
                metadata_path = self.learning_fetcher.get_cache_metadata_path(source)
                if metadata_path.exists():
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                    except Exception:
                        metadata = {}
                else:
                    metadata = {}

                status["learning"][source] = {
                    "name": source_info.get("name", source),
                    "description": source_info.get("description", ""),
                    "difficulty": source_info.get("difficulty", "mixed"),
                    "cache_valid": cache_valid,
                    "last_fetched": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(metadata.get("cached_at", 0))) if metadata.get("cached_at") else "never",
                    "success_rate": metadata.get("success_rate", "unknown")
                }
            except Exception as e:
                status["learning"][source] = {"error": str(e)}

        return status

    def needs_update(self, check_external: bool = True, check_packages: bool = True, check_learning: bool = True) -> Dict[str, Union[bool, Dict[str, bool]]]:
        """
        Check which documentation sources need updating.

        Args:
            check_external: Whether to check external services
            check_packages: Whether to check community packages
            check_learning: Whether to check learning resources

        Returns:
            Dictionary indicating which sources need updates
        """
        needs_update: Dict[str, Union[bool, Dict[str, bool]]] = {
            "core": False,
            "external": {},
            "packages": {},
            "learning": {}
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
        
        # Check community package documentation
        if check_packages:
            packages_dict = needs_update["packages"]
            if isinstance(packages_dict, dict):
                for package in self.package_fetcher.list_available_packages():
                    try:
                        packages_dict[package] = not self.package_fetcher.is_cache_valid(package)
                    except Exception as e:
                        logger.warning(f"Error checking {package} documentation status: {str(e)}")
                        packages_dict[package] = True

        # Check learning resource documentation
        if check_learning:
            learning_dict = needs_update["learning"]
            if isinstance(learning_dict, dict):
                for source in self.learning_fetcher.list_available_sources():
                    try:
                        learning_dict[source] = not self.learning_fetcher.is_cache_valid(source)
                    except Exception as e:
                        logger.warning(f"Error checking {source} learning resource status: {str(e)}")
                        learning_dict[source] = True

        return needs_update


class LearningResourceFetcher:
    """Handles fetching documentation from learning resource sources."""

    def __init__(self, target_dir: Path, cache_duration: int = 86400, max_retries: int = 3):
        """
        Initialize the learning resource fetcher.

        Args:
            target_dir: Directory where learning resources should be stored
            cache_duration: Cache duration in seconds (default: 24 hours)
            max_retries: Maximum number of retry attempts for failed requests
        """
        self.target_dir = target_dir
        self.cache_duration = cache_duration
        self.max_retries = max_retries
        self.learning_dir = target_dir / "learning_resources"
        self.learning_dir.mkdir(parents=True, exist_ok=True)

        # Learning resource sources
        self.learning_sources = {
            # The key predates the move: bootcamp.laravel.com was folded into
            # laravel.com/learn and no longer resolves. It is kept so callers
            # filtering on "laravel-bootcamp" keep working.
            "laravel-bootcamp": {
                "name": "Laravel Learn",
                "type": DocumentationSourceType.DIRECT_URL,
                "base_url": "https://laravel.com/learn",
                "description": "Official Laravel courses for beginners (formerly Laravel Bootcamp)",
                "difficulty": "beginner",
                # No course or lesson list: both are discovered from the site.
            },
            "laracasts-index": {
                "name": "Laracasts Index",
                "type": DocumentationSourceType.DIRECT_URL,
                "base_url": "https://laracasts.com",
                "description": "Video tutorial metadata (respects paywall)",
                "difficulty": "mixed",
                "fetch_type": "metadata",  # Only fetch metadata, respect paywall
                # /topics is a 404 now; the topic list is part of the series
                # browser, whose page payload the extractor already parses.
                "topics_url": "https://laracasts.com/series",
            },
        }

    def get_source_cache_path(self, source: str) -> Path:
        """Get the cache directory path for a learning source."""
        source_dir = self.learning_dir / source
        source_dir.mkdir(parents=True, exist_ok=True)
        return source_dir

    def get_cache_metadata_path(self, source: str) -> Path:
        """Get the metadata file path for a learning source."""
        return self.get_source_cache_path(source) / ".cache_metadata.json"

    def is_cache_valid(self, source: str) -> bool:
        """Check if the cached learning resources for a source are still valid."""
        metadata_path = self.get_cache_metadata_path(source)

        if not metadata_path.exists():
            return False

        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)

            cache_time = metadata.get('cached_at', 0)
            success_rate = metadata.get('success_rate', 0.0)

            is_fresh = (time.time() - cache_time) < self.cache_duration
            is_quality = success_rate >= 0.7  # Lower threshold for learning resources

            if not is_quality:
                logger.info(f"Cache for {source} has low success rate ({success_rate:.1%}), invalidating")
                return False

            return is_fresh
        except Exception as e:
            logger.warning(f"Error reading cache metadata for {source}: {str(e)}")
            return False

    def save_cache_metadata(self, source: str, metadata: Dict) -> None:
        """Save cache metadata for a learning source."""
        metadata_path = self.get_cache_metadata_path(source)
        metadata["cached_at"] = time.time()

        try:
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving cache metadata for {source}: {str(e)}")

    def fetch_learning_source(self, source: str, force: bool = False) -> bool:
        """
        Fetch learning resources from a specific source.

        Args:
            source: Source name (laravel-bootcamp, laravel-blog, etc.)
            force: Force refresh even if cache is valid

        Returns:
            True if successful, False otherwise
        """
        if source not in self.learning_sources:
            logger.error(f"Unknown learning source: {source}")
            return False

        if not force and self.is_cache_valid(source):
            logger.debug(f"Using cached learning resources for {source}")
            return True

        source_config = self.learning_sources[source]
        logger.info(f"Fetching learning resources from {source_config['name']}")

        try:
            if source == "laravel-bootcamp":
                return self._fetch_bootcamp_docs(source_config)
            elif source == "laracasts-index":
                return self._fetch_laracasts_metadata(source_config)
            else:
                logger.error(f"No fetch method implemented for source: {source}")
                return False
        except Exception as e:
            logger.error(f"Error fetching learning resources from {source}: {str(e)}")
            return False

    def _fetch_bootcamp_docs(self, config: Dict) -> bool:
        """Fetch the courses published at laravel.com/learn.

        Courses are discovered from the landing page and lessons from each
        course page, so a new course or lesson needs no change here. Lessons
        are saved flat, as "<course>-<lesson>.md", because the learning tools
        list a source's directory without recursing.
        """
        base_url = config["base_url"].rstrip("/")
        prefix = urllib.parse.urlparse(base_url).path  # "/learn"
        source_dir = self.get_source_cache_path("laravel-bootcamp")
        slug = r"[A-Za-z0-9][A-Za-z0-9-]*"

        try:
            landing = self._retry_request(base_url).decode('utf-8')
        except Exception as e:
            logger.error(f"Error fetching Laravel Learn course list: {str(e)}")
            return False

        courses = list(dict.fromkeys(re.findall(rf'href="{re.escape(prefix)}/({slug})"', landing)))
        if not courses:
            logger.warning("Laravel Learn landing page listed no courses")
            return False

        # A course whose page fails to load, or lists no lessons, contributes
        # nothing to `lessons`. Left uncounted, the lessons that were found
        # would pass for the whole site: a complete sync, a success rate of
        # 1.0, and that course's saved lessons pruned as if it had been removed.
        lessons: List[tuple[str, str]] = []
        courses_discovered = 0
        for course in courses:
            try:
                course_page = self._retry_request(f"{base_url}/{course}").decode('utf-8')
            except Exception as e:
                logger.warning(f"Error fetching Laravel Learn course {course}: {str(e)}")
                continue
            found = list(dict.fromkeys(
                re.findall(rf'href="{re.escape(prefix)}/{re.escape(course)}/({slug})"', course_page)
            ))
            if not found:
                logger.warning(f"Laravel Learn course {course} listed no lessons")
                continue
            courses_discovered += 1
            lessons.extend((course, lesson) for lesson in found)

        discovery_complete = courses_discovered == len(courses)

        if not lessons:
            logger.warning("Laravel Learn courses listed no lessons")
            return False

        fetched = 0
        expected = set()
        for course, lesson in lessons:
            filename = f"{course}-{lesson}.md"
            expected.add(filename)
            lesson_url = f"{base_url}/{course}/{lesson}"
            content = None
            try:
                content = self._learn_lesson_from_payload(self._retry_request(lesson_url).decode('utf-8'), lesson_url)
            except Exception as e:
                logger.warning(f"Error fetching Laravel Learn lesson {course}/{lesson}: {str(e)}")
                continue
            if content is None:
                # No usable payload: fall back to the rendered page, which has
                # the prose but neither the code samples nor a clean heading.
                title = f"Laravel Learn - {course.replace('-', ' ').title()} - {lesson.replace('-', ' ').title()}"
                content = self._fetch_and_process_html(lesson_url, "laravel-bootcamp", lesson, title=title)
            if content:
                with open(source_dir / filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                fetched += 1
                logger.debug(f"Fetched Laravel Learn lesson: {course}/{lesson}")

        if discovery_complete and fetched == len(lessons):
            # Complete sync: drop whatever the site no longer lists, including
            # the pages saved under the old Bootcamp layout.
            for stale in source_dir.glob("*.md"):
                if stale.name not in expected:
                    logger.info(f"Pruning Laravel Learn page no longer on the site: {stale.name}")
                    stale.unlink()

        if fetched > 0:
            metadata = {
                "source": "laravel-bootcamp",
                "name": config['name'],
                "courses": courses,
                "courses_discovered": courses_discovered,
                "fetched_sections": fetched,
                "total_sections": len(lessons),
                # Lessons fetched, scaled by the share of courses whose lesson
                # list could be read at all.
                "success_rate": (fetched / len(lessons)) * (courses_discovered / len(courses)),
                "difficulty": config.get("difficulty", "beginner"),
            }
            self.save_cache_metadata("laravel-bootcamp", metadata)
            logger.info(f"Successfully fetched {fetched}/{len(lessons)} Laravel Learn lessons")
            return True

        return False

    def _learn_lesson_from_payload(self, page_html: str, lesson_url: str) -> Optional[str]:
        """Build a lesson's markdown from the Inertia payload embedded in its page.

        laravel.com is an Inertia app: the server-rendered <main> has the
        lesson's prose but not its code samples, and opens with the course
        sidebar. The complete lesson HTML is in the page's JSON payload, under
        props.lesson.content. Returns None when the payload is missing or has
        no lesson content, so the caller can fall back to the rendered page.
        """
        try:
            from bs4 import BeautifulSoup
            from markdownify import markdownify as md
        except ImportError:
            return None

        script = BeautifulSoup(page_html, 'html.parser').find(
            'script', attrs={'data-page': True, 'type': 'application/json'}
        )
        if script is None or not script.string:
            return None

        try:
            props = json.loads(script.string).get("props", {})
            lesson = props.get("lesson") or {}
            course = props.get("course") or {}
            lesson_html = lesson.get("content")
        except (ValueError, AttributeError):
            return None

        if not isinstance(lesson_html, str) or not lesson_html.strip():
            return None

        def language_of(element: Any) -> str:
            code = element.find('code')
            classes = (code.get('class') or []) if code else []
            return next((c[len('language-'):] for c in classes if c.startswith('language-')), '')

        body = md(lesson_html, heading_style='ATX', bullets='-', code_language_callback=language_of)
        body = remove_image_references(re.sub(r'\n{3,}', '\n\n', body)).strip()
        if len(body) < 100:
            return None

        names = [str(n) for n in (course.get("name"), lesson.get("name")) if n]
        parts = [f"# Laravel Learn - {': '.join(names)}" if names else "# Laravel Learn", f"Source: {lesson_url}", "---"]
        if lesson.get("description"):
            parts.append(str(lesson["description"]).strip())
        parts.append(body)
        return "\n\n".join(parts) + "\n"

    def _fetch_laracasts_metadata(self, config: Dict) -> bool:
        """Fetch Laracasts topic metadata (respects paywall)."""
        topics_url = config["topics_url"]
        source_dir = self.get_source_cache_path("laracasts-index")

        try:
            content_bytes = self._retry_request(topics_url)
            content = content_bytes.decode('utf-8')

            # Extract topic list (publicly available)
            topics = self._extract_laracasts_topics(content)

            if topics:
                index_content = "# Laracasts - Topic Index\n\n"
                index_content += f"Source: {topics_url}\n\n"
                index_content += "*Note: Laracasts is a premium service. This index provides topic metadata only.*\n\n"
                index_content += "---\n\n"

                for topic in topics:
                    index_content += f"## {topic.get('name', 'Untitled')}\n\n"
                    if topic.get('description'):
                        index_content += f"{topic['description']}\n\n"
                    if topic.get('series_count'):
                        index_content += f"*{topic['series_count']} series available*\n\n"
                    if topic.get('url'):
                        index_content += f"[View on Laracasts]({topic['url']})\n\n"
                    index_content += "---\n\n"

                index_file = source_dir / "topics.md"
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(index_content)

                metadata = {
                    "source": "laracasts-index",
                    "name": config['name'],
                    "topic_count": len(topics),
                    "success_rate": 1.0,
                    "difficulty": "mixed",
                    "type": "metadata_only",
                }
                self.save_cache_metadata("laracasts-index", metadata)
                logger.info(f"Successfully fetched {len(topics)} Laracasts topic metadata")
                return True

        except Exception as e:
            logger.error(f"Error fetching Laracasts metadata: {str(e)}")

        return False

    def _extract_laracasts_topics(self, html_content: str) -> List[Dict]:
        """Extract topic metadata from the Laracasts topics page.

        The page became an SPA in 2026: topics live in an embedded JSON blob
        as a "topics":[{name, slug, path, series_count}, ...] array rather
        than DOM links. The JSON path is tried first; the legacy DOM
        extraction stays as a fallback for older page shapes.
        """
        topics = self._extract_laracasts_topics_json(html_content)
        if topics:
            return topics
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Legacy shape: topic cards/links in the DOM
            topic_elements = soup.find_all('a', href=re.compile(r'/topics/'))

            seen_topics: set = set()
            for elem in topic_elements:
                topic_data: Dict[str, Any] = {}

                href = str(elem.get('href', ''))
                if href and href not in seen_topics:
                    seen_topics.add(href)
                    topic_data['url'] = f"https://laracasts.com{href}" if not href.startswith('http') else href

                    # Extract topic name from URL or text
                    name = elem.get_text(strip=True) or href.split('/')[-1].replace('-', ' ').title()
                    if name and len(name) > 1:
                        topic_data['name'] = name

                        # Look for description in parent or sibling
                        parent = elem.parent
                        if parent:
                            desc_elem = parent.find('p') or parent.find(class_=re.compile(r'description', re.I))
                            if desc_elem:
                                topic_data['description'] = desc_elem.get_text(strip=True)[:200]

                        if topic_data.get('name'):
                            topics.append(topic_data)

        except ImportError:
            logger.warning("BeautifulSoup not installed, skipping topic extraction")
        except Exception as e:
            logger.warning(f"Error extracting Laracasts topics: {str(e)}")

        return topics

    def _extract_laracasts_topics_json(self, html_content: str) -> List[Dict]:
        """Parse the SPA payload's "topics" array out of the page source."""
        marker = '"topics":['
        start = html_content.find(marker)
        if start == -1:
            return []
        # Walk to the matching close bracket; entries are flat objects, so a
        # simple depth count over brackets suffices.
        i = start + len(marker) - 1
        depth = 0
        for j in range(i, min(len(html_content), i + 200_000)):
            if html_content[j] == '[':
                depth += 1
            elif html_content[j] == ']':
                depth -= 1
                if depth == 0:
                    break
        else:
            return []

        try:
            entries = json.loads(html_content[i:j + 1])
        except (json.JSONDecodeError, ValueError):
            return []

        topics: List[Dict] = []
        for entry in entries:
            if not isinstance(entry, dict) or not entry.get("name") or not entry.get("path"):
                continue
            path = str(entry["path"])
            topic: Dict[str, Any] = {
                "name": entry["name"],
                "url": path if path.startswith("http") else f"https://laracasts.com{path}",
            }
            if entry.get("series_count"):
                topic["series_count"] = entry["series_count"]
            topics.append(topic)
        return topics

    def _fetch_and_process_html(self, url: str, source: str, section: str, title: Optional[str] = None) -> Optional[str]:
        """Fetch and process HTML content to markdown.

        `title` overrides the heading otherwise built from the source key and
        section name.
        """
        try:
            content_bytes = self._retry_request(url)
            content = content_bytes.decode('utf-8')

            try:
                from bs4 import BeautifulSoup
                from markdownify import markdownify as md

                soup = BeautifulSoup(content, 'html.parser')

                # Remove navigation, header, footer
                for tag in soup.find_all(['nav', 'header', 'footer', 'aside', 'script', 'style']):
                    tag.decompose()

                # Find main content
                main_content = (
                    soup.find('main') or
                    soup.find('article') or
                    soup.find('div', class_=re.compile(r'content|prose|documentation', re.I)) or
                    soup.find('body')
                )

                if main_content:
                    markdown_content = md(str(main_content), strip=['a'], code_language='php')

                    # Clean up
                    markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)

                    # Remove CloudFlare email protection links
                    # Note: markdownify escapes @ as \@, creating patterns like [[email protected]]
                    markdown_content = re.sub(
                        r'\[+[^\]]*\]+\(/cdn-cgi/l/email-protection[^)]*\)',
                        '[email protected]',
                        markdown_content
                    )

                    # Remove social media links
                    markdown_content = remove_social_media_lines(markdown_content)

                    # Remove image references
                    markdown_content = remove_image_references(markdown_content)

                    markdown_content = markdown_content.strip()

                    if len(markdown_content) > 100:
                        heading = title or f"{source.replace('-', ' ').title()} - {section.replace('-', ' ').title()}"
                        header = f"# {heading}\n\n"
                        header += f"Source: {url}\n\n---\n\n"
                        return header + markdown_content

            except ImportError:
                logger.warning("BeautifulSoup/markdownify not installed")

        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")

        return None

    def _retry_request(self, url: str, headers: Optional[Dict] = None) -> bytes:
        """Make a request with retry logic."""
        if headers is None:
            headers = {"User-Agent": USER_AGENT}

        last_exception: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                request = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(request, timeout=DEFAULT_REQUEST_TIMEOUT) as response:
                    return response.read()
            except urllib.error.HTTPError as e:
                last_exception = e
                if e.code == 404:
                    raise
                elif e.code >= 500 and attempt < self.max_retries:
                    wait_time = (2 ** attempt) + random.uniform(0, 2)
                    logger.warning(f"Server error {e.code}, retrying in {wait_time:.1f}s")
                    time.sleep(wait_time)
                else:
                    raise
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    wait_time = (2 ** attempt) + random.uniform(0, 2)
                    logger.warning(f"Request error, retrying in {wait_time:.1f}s: {str(e)}")
                    time.sleep(wait_time)
                else:
                    raise

        if last_exception:
            raise last_exception
        raise RuntimeError(f"Failed to fetch {url}")

    def fetch_all_sources(self, force: bool = False) -> Dict[str, bool]:
        """Fetch learning resources from all sources."""
        results = {}
        for source in self.learning_sources.keys():
            results[source] = self.fetch_learning_source(source, force=force)
        return results

    def list_available_sources(self) -> List[str]:
        """List all available learning sources."""
        return list(self.learning_sources.keys())

    def get_source_info(self, source: str) -> Optional[Dict]:
        """Get information about a specific learning source."""
        return self.learning_sources.get(source)


def source_statuses(
    target_dir: Path,
    now: Optional[float] = None,
    max_age: Optional[float] = 2 * 86400,
    min_success_rate: float = 0.9,
) -> List[Dict[str, Any]]:
    """The state of every configured documentation source other than the
    framework docs, read from the metadata each fetcher leaves behind.

    One dict per source: `name`; `kind` ("service", "learning" or "package");
    `fetched` and `total` page counts, either of which may be None; `version`
    when the source follows a major; `discovery`, how its pages were found;
    `synced_at`, a Unix time, and `age_days`; and `problem`, None when the
    source is healthy.

    A source has a problem when its metadata is missing or unreadable, when it
    fetched less than `min_success_rate` of its pages, or when its last
    successful sync is older than `max_age`. The age check matters to the
    pipeline because a fetch that fails outright writes nothing: the previous
    metadata, with its perfect success rate, is all that is left behind. Pass
    `max_age=None` to leave age out of it, as the server does: a copy that is
    simply a few days old is not broken.
    """
    now = time.time() if now is None else now

    sources: List[tuple[str, str, Path]] = []
    for service in ExternalDocsFetcher(target_dir).laravel_services:
        sources.append((service, "service", target_dir / "external" / service / ".cache_metadata.json"))
    for source in LearningResourceFetcher(target_dir).learning_sources:
        sources.append((source, "learning", target_dir / "learning_resources" / source / ".cache_metadata.json"))
    for package, config in CommunityPackageFetcher(target_dir).community_packages.items():
        sub_packages = config.get("packages")
        if isinstance(sub_packages, dict) and sub_packages:
            for sub in sub_packages:
                sources.append((f"{package}/{sub}", "package", target_dir / "packages" / package / sub / ".metadata" / "cache.json"))
        else:
            sources.append((package, "package", target_dir / "packages" / package / ".metadata" / "cache.json"))

    statuses: List[Dict[str, Any]] = []
    for name, kind, metadata_path in sources:
        status: Dict[str, Any] = {
            "name": name, "kind": kind, "fetched": None, "total": None, "version": None,
            "discovery": None, "synced_at": None, "age_days": None, "problem": None,
        }
        statuses.append(status)

        if not metadata_path.exists():
            status["problem"] = "never synced"
            continue
        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            if not isinstance(metadata, dict):
                raise ValueError("metadata is not an object")
        except Exception:
            status["problem"] = "metadata unreadable"
            continue

        fetched = next((metadata[key] for key in ("fetched_sections", "sections_count", "article_count", "topic_count")
                        if key in metadata), None)
        if isinstance(fetched, list):
            fetched = len(fetched)
        total = metadata.get("total_sections")
        status["fetched"], status["total"] = fetched, total
        status["version"] = metadata.get("version") or None
        status["discovery"] = metadata.get("discovery_method") or metadata.get("source_type") or None

        synced_at = metadata.get("cached_at") or metadata.get("cache_time")
        success_rate = metadata.get("success_rate")
        if not isinstance(synced_at, (int, float)):
            status["problem"] = "no sync timestamp"
            continue

        age_days = int((now - synced_at) // 86400)
        status["synced_at"], status["age_days"] = synced_at, age_days
        if max_age is not None and now - synced_at > max_age:
            status["problem"] = f"last synced {age_days} days ago"
        elif isinstance(success_rate, (int, float)) and success_rate < min_success_rate:
            if fetched is not None and total is not None and fetched != total:
                status["problem"] = f"fetched {fetched} of {total} pages"
            else:
                status["problem"] = f"success rate {success_rate:.0%}"

    return statuses


def build_sync_report(
    target_dir: Path,
    now: Optional[float] = None,
    max_age: float = 2 * 86400,
    min_success_rate: float = 0.9,
) -> tuple[str, List[str]]:
    """Summarise the state of every documentation source after a sync.

    Returns the report as Markdown and a list of problems, one per degraded
    source. The daily pipeline pastes the Markdown into its pull request and
    fails when the list is non-empty. See source_statuses for what makes a
    source degraded.
    """
    rows: List[str] = []
    problems: List[str] = []

    for status in source_statuses(target_dir, now, max_age, min_success_rate):
        pages = synced = "-"
        if status["fetched"] is not None:
            pages = f"{status['fetched']}/{status['total']}" if status["total"] is not None else str(status["fetched"])
        if status["age_days"] is not None:
            synced = "today" if status["age_days"] <= 0 else f"{status['age_days']}d ago"
        if status["problem"]:
            problems.append(f"{status['name']}: {status['problem']}")
        rows.append(
            f"| {status['name']} | {'DEGRADED' if status['problem'] else 'ok'} | {pages} "
            f"| {status['discovery'] or '-'} | {synced} |"
        )

    lines = [
        "## Sync health",
        "",
        "| Source | Status | Pages | Discovery | Last synced |",
        "| --- | --- | --- | --- | --- |",
        *rows,
    ]

    if problems:
        lines += ["", "### Needs attention", "", *[f"- {problem}" for problem in problems]]

    core_rows = []
    for version_dir in target_dir.iterdir() if target_dir.is_dir() else []:
        sync_info = version_dir / ".metadata" / "sync_info.json"
        if not sync_info.is_file():
            continue
        try:
            with open(sync_info, 'r') as f:
                info = json.load(f)
            core_rows.append((
                str(info.get("version", version_dir.name)),
                str(info.get("commit_sha", ""))[:7] or "-",
                str(info.get("commit_date", ""))[:10] or "-",
            ))
        except Exception:
            core_rows.append((version_dir.name, "unreadable", "-"))

    if core_rows:
        def version_key(row: tuple[str, str, str]) -> float:
            try:
                return float(row[0].rstrip("x").rstrip("."))
            except ValueError:
                return -1.0

        lines += [
            "",
            "## Laravel framework docs",
            "",
            "| Version | Commit | Upstream date |",
            "| --- | --- | --- |",
            *[f"| {version} | {sha} | {date} |" for version, sha, date in sorted(core_rows, key=version_key, reverse=True)],
        ]

    return "\n".join(lines) + "\n", problems


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
        default=get_default_version(),
        help=f"Laravel version branch to use (default: {get_default_version()}). Supported: {', '.join(SUPPORTED_VERSIONS)}"
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
        "--update",
        action="store_true",
        help="Update all documentation (Laravel core, services, and community packages)"
    )
    parser.add_argument(
        "--external-only",
        action="store_true",
        help="Only update external Laravel services documentation (deprecated: use --update)"
    )
    parser.add_argument(
        "--core-only",
        action="store_true",
        help="Only update core Laravel documentation (deprecated: use --update)"
    )
    parser.add_argument(
        "--packages-only",
        action="store_true",
        help="Only update community package documentation (deprecated: use --update)"
    )
    parser.add_argument(
        "--services",
        type=str,
        nargs="+",
        help="Specific Laravel services to update (deprecated: use --update)"
    )
    parser.add_argument(
        "--packages",
        type=str,
        nargs="+",
        help="Specific community packages to update (deprecated: use --update)"
    )
    parser.add_argument(
        "--list-services",
        action="store_true",
        help="List all available Laravel services"
    )
    parser.add_argument(
        "--list-packages",
        action="store_true",
        help="List all available community packages"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show status of all documentation sources"
    )
    parser.add_argument(
        "--sync-report",
        action="store_true",
        help="Print a Markdown health report for every documentation source; exits 1 if any is degraded"
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

def update_exit_code(results: Dict[str, Any]) -> int:
    """The exit code for a run of update_all.

    0 when the framework docs update completed, changed or not, and at least
    one service or package synced. 1 when the framework update raised, or
    every service and every package failed.
    """
    external_results = results.get("external") or {}
    package_results = results.get("packages") or {}
    external_ok = sum(1 for success in external_results.values() if success)
    package_ok = sum(1 for success in package_results.values() if success)
    core_failed = "core_error" in results
    core_state = "failed" if core_failed else ("updated" if results.get("core") else "already current")

    logger.info(
        f"Complete documentation update: Core {core_state}, "
        f"External {external_ok}/{len(external_results)}, Packages {package_ok}/{len(package_results)}"
    )

    others_ok = (external_ok > 0 or not external_results) or (package_ok > 0 or not package_results)
    return 0 if not core_failed and others_ok else 1


def handle_update_command(args, updater):
    """Handle the unified --update command - updates everything."""
    results = updater.update_all(force_core=args.force, force_external=args.force, force_packages=args.force, force_learning=args.force)
    return update_exit_code(results)


def main():
    """Main entry point for the Laravel Docs Updater."""
    # Before the arguments are parsed: --version is validated against this
    # list, and --all-versions walks it, so a new Laravel branch has to be
    # known by then.
    refresh_supported_versions()
    args = parse_arguments()
    
    # Set logging level
    logger.setLevel(getattr(logging, args.log_level))
    
    # Create target directory if it doesn't exist
    target_dir = Path(args.target_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    # Read-only: handled before the updater is built, which creates directories.
    if args.sync_report:
        report, problems = build_sync_report(target_dir)
        print(report)
        return 1 if problems else 0
    
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
        
        # Handle list packages command
        if args.list_packages:
            packages = updater.package_fetcher.list_available_packages()
            print("Available Community Packages:")
            for package in packages:
                info = updater.package_fetcher.community_packages.get(package, {})
                print(f"  {package}: {info.get('name', package)}")
                # Show sub-packages for Spatie
                if package == "spatie" and "packages" in info:
                    for sub_pkg, sub_info in info["packages"].items():
                        print(f"    - {sub_pkg}: {sub_info.get('name', sub_pkg)}")
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
                    
                    # Show how the pages were discovered, if recorded
                    metadata_path = updater.external_fetcher.get_cache_metadata_path(service)
                    if metadata_path.exists():
                        try:
                            with open(metadata_path, 'r') as f:
                                metadata = json.load(f)
                            if metadata.get('discovery_method'):
                                fetched = len(metadata.get('fetched_sections', []))
                                print(f"    Discovery: {metadata['discovery_method']} ({fetched}/{metadata.get('total_sections', '?')} pages)")
                        except Exception:
                            pass
            
            print("\nCommunity Packages:")
            for package, info in status["packages"].items():
                if "error" in info:
                    print(f"  {package}: Error - {info['error']}")
                else:
                    print(f"  {package} ({info.get('name', package)}):")
                    print(f"    Cache Valid: {info.get('cache_valid', False)}")
                    print(f"    Sections: {info.get('sections_count', 0)}")
                    
                    # Show sub-packages for Spatie
                    if package == "spatie" and "sub_packages" in info:
                        print("    Sub-packages:")
                        for sub_pkg, sub_info in info["sub_packages"].items():
                            print(f"      - {sub_info.get('name', sub_pkg)}: {sub_info.get('sections_count', 0)} sections")
            
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
            print("Community Packages:")
            for package, needs in needs_update["packages"].items():
                print(f"  {package}: {'needs update' if needs else 'up to date'}")
            
            # Return 1 if any updates needed, 0 if all up to date
            any_needs_update = needs_update["core"] or any(needs_update["external"].values()) or any(needs_update["packages"].values())
            return 1 if any_needs_update else 0
        
        # Handle new unified --update parameter
        if args.update:
            return handle_update_command(args, updater)
        
        # Handle deprecated parameters - all now just update everything
        if args.external_only or args.core_only or args.packages_only or args.packages or args.services:
            logger.warning("Deprecated parameter used. Please use --update instead.")
            return handle_update_command(args, updater)
        
        # Handle specific update modes (deprecated but still supported)
        if args.all_versions:
            # Update all supported versions (core only)
            all_success = True
            
            # update() returns False for a version that is already current,
            # which is not a failure: the old Laravel versions never change, so
            # treating it as one made this command exit 1 on every run.
            # update_version separates "did it work" from "did anything change"
            # and turns an exception into a failed version rather than a crash,
            # so the remaining versions are still processed.
            for version in SUPPORTED_VERSIONS:
                logger.info(f"Processing version {version}...")
                success, _updated = update_version(target_dir, version, force=args.force, check_only=False)

                if not success:
                    all_success = False

            return 0 if all_success else 1
        
        else:
            # Default: update all (core, external services, and packages)
            results = updater.update_all(force_core=args.force, force_external=args.force, force_packages=args.force, force_learning=args.force)
            return update_exit_code(results)

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130

if __name__ == "__main__":
    sys.exit(main())