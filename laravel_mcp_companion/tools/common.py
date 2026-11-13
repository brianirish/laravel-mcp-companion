"""Checks and lookups the tools share."""

import re
from pathlib import Path
from typing import Optional, Tuple

from .. import mcp_tools
from ..docs_updater import get_default_version
from ..path_security import resolve_contained_path
from .errors import ToolFailure


def require_version(version: Optional[str]) -> None:
    """Reject a Laravel version this server does not carry.

    Version strings become path components, so anything outside the allowlist
    is refused before it is joined onto a directory.
    """
    if version is not None and version not in mcp_tools.SUPPORTED_VERSIONS:
        raise ToolFailure(
            "unknown_version",
            f"Laravel version {version!r} is not available",
            {"supported_versions": list(mcp_tools.SUPPORTED_VERSIONS)},
        )


def default_version(runtime_version: Optional[str]) -> str:
    return runtime_version or get_default_version()


_ZERO_WIDTH = re.compile("[​‌‍⁠﻿]")
_MARKDOWN_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def slugify(heading: str) -> str:
    """A heading as the identifier a section can be asked for by.

    Service and package pages carry no explicit anchors, and their headings
    can include invisible characters, inline code and links. Reducing a
    heading to lowercase words joined by hyphens gives search something to
    hand back that the section reader will recognise.
    """
    text = _ZERO_WIDTH.sub("", heading)
    text = _MARKDOWN_LINK.sub(r"\1", text)
    text = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return text.strip("-")


def locate(
    docs_path: Path, filename: str, version: Optional[str], runtime_version: Optional[str]
) -> Tuple[Path, str, Optional[str], Optional[str]]:
    """Find a documentation file on disk.

    Accepts every name search produces: a bare core file ("queues.md"), a
    version-prefixed one ("12.x/queues.md"), and a corpus-prefixed file from a
    service, package or learning source ("forge/servers/php.md"). The last
    kind is not Laravel-versioned and ignores `version`.

    Returns (path, name, version, corpus): the resolved path that passed the
    containment check, which is the one to open; the name as the caller
    should see it; and either the Laravel version or the corpus key, the
    other being None.
    """
    name = filename.strip()
    if not name:
        raise ToolFailure("invalid_argument", "filename is empty")
    if not name.endswith(".md"):
        name = f"{name}.md"

    corpus = mcp_tools.resolve_corpus_file(docs_path, name)
    if corpus is not None:
        corpus_root, relative = corpus
        safe_path = resolve_contained_path(corpus_root, corpus_root / relative)
        if safe_path is None:
            raise ToolFailure("access_denied", f"{filename} resolves outside the documentation tree")
        if not safe_path.is_file():
            raise ToolFailure("not_found", f"No documentation file {name}")
        return safe_path, name, None, corpus_root.name

    require_version(version)
    prefix, separator, rest = name.partition("/")
    if separator and prefix in mcp_tools.SUPPORTED_VERSIONS:
        version, relative = prefix, rest
    else:
        version, relative = version or default_version(runtime_version), name

    version_root = Path(docs_path) / version
    safe_path = resolve_contained_path(version_root, version_root / relative)
    if safe_path is None:
        raise ToolFailure("access_denied", f"{filename} resolves outside the documentation tree")
    if not safe_path.is_file():
        raise ToolFailure("not_found", f"No documentation file {relative} for Laravel {version}", {"version": version})
    return safe_path, relative, version, None


def read_text(path: Path) -> str:
    """A located file's text, through the shared cache."""
    content = mcp_tools.get_file_content_cached(str(path))
    # The cache reports failure in-band, as a string.
    if content.startswith("Error reading file") or content.startswith("File not found"):
        raise ToolFailure("internal", content)
    return content
