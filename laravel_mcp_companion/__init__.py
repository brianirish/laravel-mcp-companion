"""Laravel MCP Companion: Laravel's documentation, every version, served over MCP."""

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
DISTRIBUTION_NAME = "laravel-mcp-companion"


def resource_path(name: str) -> Path:
    """Where a file or directory that ships with the project lives.

    An installed wheel carries the documentation corpus and server.json inside
    the package directory. A source checkout, and the Docker image, keep them
    beside it at the repository root. The packaged copy wins when both exist.
    """
    bundled = PACKAGE_DIR / name
    return bundled if bundled.exists() else PACKAGE_DIR.parent / name


def _read_version() -> str:
    """The project version, from pyproject.toml when there is one beside the
    package and from the installed distribution's metadata otherwise.

    pyproject.toml is the single place the version is written. A checkout or
    the Docker image has the file, and reading it there cannot go stale the
    way an old editable install's metadata can. An installed wheel has no
    pyproject.toml, only metadata.
    """
    pyproject = PACKAGE_DIR.parent / "pyproject.toml"
    if pyproject.is_file():
        import tomllib

        try:
            project = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("project", {})
        except (OSError, tomllib.TOMLDecodeError):
            project = {}
        if project.get("name") == DISTRIBUTION_NAME and project.get("version"):
            return str(project["version"])

    from importlib.metadata import PackageNotFoundError, version

    try:
        return version(DISTRIBUTION_NAME)
    except PackageNotFoundError:
        return "0+unknown"


__version__ = _read_version()
