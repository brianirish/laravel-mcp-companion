"""Guard against the project version drifting between the files that record it.

`pyproject.toml` sat at 0.9.0 while release tags had reached v0.9.145, because
nothing asserted the two agreed. The documentation-sync pipeline no longer
touches version numbers, so they now change only when someone bumps them
deliberately -- these tests make sure that bump reaches every file.

These assertions are made against the configuration files as text rather than
through a TOML parser, so they run identically on any interpreter. `tomllib` is
standard library only from 3.11, and depending on it here would couple this
suite to whichever Python the CI runner happens to ship.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def read(filename: str) -> str:
    return (REPO_ROOT / filename).read_text(encoding="utf-8")


def toml_table(content: str, table: str) -> str | None:
    """Return the raw body of a TOML table, or None when it is absent.

    Only table headers at the start of a line count, so a table name mentioned
    inside a comment is not treated as a declaration.
    """
    pattern = rf"^\[{re.escape(table)}\]$(.*?)(?=^\[|\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else None


def project_version() -> str:
    table = toml_table(read("pyproject.toml"), "project")
    assert table is not None, "pyproject.toml has no [project] table"
    match = re.search(r'^version\s*=\s*"([^"]+)"', table, re.MULTILINE)
    assert match, "pyproject.toml [project] has no version"
    return match.group(1)


def test_pyproject_version_is_valid_semver():
    version = project_version()
    assert re.fullmatch(r"\d+\.\d+\.\d+", version), f"Not a semver version: {version!r}"


def test_roadmap_current_version_matches_pyproject():
    match = re.search(r"^## Current Version:\s*v(\S+)", read("ROADMAP.md"), re.MULTILINE)
    assert match, "ROADMAP.md is missing a '## Current Version: vX.Y.Z' line"
    assert match.group(1) == project_version(), (
        f"ROADMAP.md says v{match.group(1)} but pyproject.toml says {project_version()}"
    )


def test_readme_features_heading_matches_pyproject():
    match = re.search(r"^## Features \(v(\S+?)\)", read("README.md"), re.MULTILINE)
    assert match, "README.md is missing a '## Features (vX.Y.Z)' heading"
    assert match.group(1) == project_version(), (
        f"README.md says v{match.group(1)} but pyproject.toml says {project_version()}"
    )


def test_pytest_is_configured_in_exactly_one_place():
    """Only pytest.ini configures pytest; a second source silently drifts.

    pyproject.toml previously carried a [tool.pytest.ini_options] table that
    pytest ignored (pytest.ini wins) and that had drifted to a shorter module
    list than the one actually in force.
    """
    assert toml_table(read("pyproject.toml"), "tool.pytest.ini_options") is None, (
        "pyproject.toml must not configure pytest; pytest.ini takes precedence "
        "and the two will drift"
    )
    assert "[pytest]" in read("pytest.ini")


def test_coverage_measures_product_code_not_tests():
    """A bare --cov must not count the test suite.

    CI ran `pytest --cov`, which measured everything including tests/. Their
    near-total coverage inflated the reported figure past the gate while
    product coverage was far lower.
    """
    table = toml_table(read("pyproject.toml"), "tool.coverage.run")
    assert table is not None, "pyproject.toml is missing [tool.coverage.run]"

    source_match = re.search(r"^source\s*=\s*\[(.*?)\]", table, re.MULTILINE | re.DOTALL)
    assert source_match, "[tool.coverage.run] must pin the measured source modules"
    source = source_match.group(1)
    assert "laravel_mcp_companion" in source
    assert '"tests"' not in source

    omit_match = re.search(r"^omit\s*=\s*\[(.*?)\]", table, re.MULTILINE | re.DOTALL)
    assert omit_match, "[tool.coverage.run] must declare an omit list"
    assert "tests" in omit_match.group(1), (
        "[tool.coverage.run] omit must exclude the test suite"
    )


def test_coverage_gate_is_configured():
    """The gate must exist and sit at or below current coverage.

    An unreachable threshold is worse than none: it fails every run, which
    trains everyone to ignore the result.
    """
    match = re.search(r"--cov-fail-under=(\d+)", read("pytest.ini"))
    assert match, "pytest.ini must set --cov-fail-under"
    assert 0 < int(match.group(1)) <= 100
