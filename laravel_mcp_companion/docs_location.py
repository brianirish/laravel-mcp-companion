"""Where the server reads documentation from, and where an update writes it.

A source checkout and the Docker image hold one copy of the documentation,
beside the package, and update it in place.

An installed wheel holds its copy inside the package directory. Updating it
there does not last: a reinstall or an upgrade replaces the directory, and
some environments cannot write to it at all. So a wheel install serves and
updates a copy in a directory of the user's own. The copy is made from the
bundled one at first start, and made again when an upgrade ships newer
documentation than the copy holds.
"""

import logging
import os
import shutil
import uuid
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

PACKAGE_DIR = Path(__file__).resolve().parent

# Names the directory that holds the user's copy, in place of the platform's
# per-user data directory.
ENV_HOME = "LARAVEL_MCP_COMPANION_HOME"

APP_NAME = "laravel-mcp-companion"


def bundled_docs_path() -> Path:
    """The documentation that ships with the project: inside the package in an
    installed wheel, beside it in a checkout or the Docker image."""
    inside = PACKAGE_DIR / "docs"
    return inside if inside.exists() else PACKAGE_DIR.parent / "docs"


def is_wheel_install() -> bool:
    return (PACKAGE_DIR / "docs").exists()


def user_docs_path() -> Path:
    """The user's own copy of the documentation, whether or not it exists."""
    home = os.environ.get(ENV_HOME, "").strip()
    if home:
        return Path(home).expanduser() / "docs"

    from platformdirs import user_data_path

    return user_data_path(APP_NAME, appauthor=False) / "docs"


def _documentation_date(docs_path: Path) -> Optional[str]:
    """The date of the newest upstream change in a copy, or None when the
    directory holds no documentation this project can date."""
    # Imported here: mcp_tools imports the updater, which is more than a
    # caller that only wants a path should have to load.
    from .mcp_tools import get_documentation_date

    if not docs_path.is_dir():
        return None
    date, _ = get_documentation_date(docs_path)
    return date


def _user_copy_is_current(bundled: Path, user: Path) -> bool:
    """Whether the user's copy is at least as new as the bundled one.

    A tie goes to the user's copy. It was fetched after the package was built,
    so its service and package pages are at least as new even when the
    framework's own date is the same.
    """
    user_date = _documentation_date(user)
    if user_date is None:
        return False
    bundled_date = _documentation_date(bundled)
    return bundled_date is None or user_date >= bundled_date


def reading_path() -> Path:
    """The documentation directory the server serves when none is given.

    On a wheel install this is the user's copy, the same directory an update
    writes to. The server keeps the path it starts with, and the
    update_laravel_docs tool writes to that path while the server runs, so
    serving the bundled copy would send those updates into the package
    directory.

    Where the user's directory cannot be written, the bundled copy is served.
    A read-only home should not stop the server from starting.
    """
    try:
        return updating_path()
    except OSError as error:
        bundled = bundled_docs_path()
        logger.warning(
            "Could not prepare the documentation directory %s (%s). Serving the copy "
            "that ships with this version from %s; documentation updates will not "
            "outlast a reinstall.", user_docs_path(), error, bundled,
        )
        return bundled


def updating_path() -> Path:
    """The documentation directory an update writes to when none is given.

    On a wheel install this is the user's copy, created from the bundled one
    when it is missing or older. An older copy is replaced, not updated: a
    newer package is otherwise hidden behind last year's fetch, and updating
    from the old copy would keep pages the newer package has dropped.
    """
    bundled = bundled_docs_path()
    if not is_wheel_install():
        return bundled

    user = user_docs_path()
    if not _user_copy_is_current(bundled, user):
        try:
            _replace_with_copy(bundled, user)
        except OSError:
            # Two servers started together both make the copy, and the slower
            # one cannot move its own into place. The copy it wanted is there.
            if not _user_copy_is_current(bundled, user):
                raise
    return user


def _replace_with_copy(source: Path, destination: Path) -> None:
    """Copy `source` to `destination`, replacing what is there.

    The copy is made beside the destination and moved into place, so a copy
    that fails part-way leaves the old directory, or none, and never half of
    a new one.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = destination.with_name(f"{destination.name}.{uuid.uuid4().hex}.partial")
    try:
        shutil.copytree(source, staging)
        if destination.exists():
            shutil.rmtree(destination)
        staging.rename(destination)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    logger.info("Copied the shipped documentation to %s", destination)
