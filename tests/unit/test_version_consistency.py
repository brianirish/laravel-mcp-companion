"""Guard against the project version drifting between the files that record it.

`pyproject.toml` sat at 0.9.0 while release tags had reached v0.9.145, because
nothing asserted the two agreed. The documentation-sync pipeline no longer
touches version numbers, so they now change only when someone bumps them
deliberately -- these tests make sure that bump reaches every file.
"""

import re
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def project_version() -> str:
    with open(REPO_ROOT / "pyproject.toml", "rb") as f:
        return tomllib.load(f)["project"]["version"]


def test_pyproject_version_is_valid_semver():
    version = project_version()
    assert re.fullmatch(r"\d+\.\d+\.\d+", version), f"Not a semver version: {version!r}"


def test_roadmap_current_version_matches_pyproject():
    roadmap = (REPO_ROOT / "ROADMAP.md").read_text()
    match = re.search(r"^## Current Version:\s*v(\S+)", roadmap, re.MULTILINE)
    assert match, "ROADMAP.md is missing a '## Current Version: vX.Y.Z' line"
    assert match.group(1) == project_version(), (
        f"ROADMAP.md says v{match.group(1)} but pyproject.toml says {project_version()}"
    )


def test_readme_features_heading_matches_pyproject():
    readme = (REPO_ROOT / "README.md").read_text()
    match = re.search(r"^## Features \(v(\S+?)\)", readme, re.MULTILINE)
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
    with open(REPO_ROOT / "pyproject.toml", "rb") as f:
        config = tomllib.load(f)

    assert "ini_options" not in config.get("tool", {}).get("pytest", {}), (
        "pyproject.toml must not configure pytest; pytest.ini takes precedence "
        "and the two will drift"
    )
    assert "[pytest]" in (REPO_ROOT / "pytest.ini").read_text()


def test_coverage_measures_product_code_not_tests():
    """A bare --cov must not count the test suite.

    CI ran `pytest --cov`, which measured everything including tests/. Their
    near-total coverage inflated the reported figure past the gate while
    product coverage was far lower.
    """
    with open(REPO_ROOT / "pyproject.toml", "rb") as f:
        config = tomllib.load(f)

    run_config = config.get("tool", {}).get("coverage", {}).get("run", {})
    assert run_config, "pyproject.toml is missing [tool.coverage.run]"

    source = run_config.get("source", [])
    assert source, "[tool.coverage.run] must pin the measured source modules"
    assert "tests" not in source

    omit = run_config.get("omit", [])
    assert any("tests" in pattern for pattern in omit), (
        "[tool.coverage.run] omit must exclude the test suite"
    )
