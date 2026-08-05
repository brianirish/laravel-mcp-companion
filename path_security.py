#!/usr/bin/env python3
"""
Single source of truth for path containment and symlink-refusing opens; both
the server and the updater import from here so the rules cannot drift.
"""

import os
from pathlib import Path
from typing import Optional


def no_follow_opener(path, flags):
    """open() opener that refuses to follow a symlink in the final component.

    Passed to open() rather than calling os.open directly so that the read still
    goes through the normal open(), which keeps the behaviour observable to
    callers and testable in the usual way.

    O_NOFOLLOW is POSIX. Where it is unavailable this degrades to an ordinary
    open rather than refusing to read anything.
    """
    return os.open(path, flags | getattr(os, "O_NOFOLLOW", 0))


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


def is_within_directory(base_dir: Path, target: Path) -> bool:
    """Check that target resolves to a location inside base_dir.

    Fails closed: any error resolving either path denies the write.
    """
    return is_safe_path(base_dir, target)
