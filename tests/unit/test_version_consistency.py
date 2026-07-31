"""Guard against the project version drifting from what is actually released.

`pyproject.toml` sat at 0.9.0 while release tags reached v0.9.145. Note where
that drift was: the manifest disagreed with the *tags*, not with the other
files -- ROADMAP.md and README.md both said 0.9.0 the entire time. A guard that
only cross-checks the three files would have been green throughout, which is why
`test_pyproject_version_matches_newest_release_tag` exists.

Parsing uses `tomllib`, which is standard library from 3.11. The project
declares `requires-python = ">=3.12"`, so it is always available on a supported
interpreter; CI installs 3.12 explicitly rather than inheriting the runner's.
"""

import re
import subprocess
import tomllib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

# v0.10.1 was cut by the documentation cron before it stopped consuming semantic
# versions. It points at a docs-only commit and carries no code change, so it is
# not a release the manifest should track. Nothing else belongs in this set:
# every later v* tag is a deliberate release.
NON_RELEASE_TAGS = {"v0.10.1"}


def read(filename: str) -> str:
    return (REPO_ROOT / filename).read_text(encoding="utf-8")


def pyproject() -> dict:
    with open(REPO_ROOT / "pyproject.toml", "rb") as f:
        return tomllib.load(f)


def project_version() -> str:
    return pyproject()["project"]["version"]


def newest_release_tag() -> str | None:
    """The highest v* tag that represents an actual software release."""
    try:
        result = subprocess.run(
            ["git", "tag", "--list", "v*", "--sort=-v:refname"],
            cwd=REPO_ROOT, capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    for tag in (line.strip() for line in result.stdout.splitlines()):
        if tag and tag not in NON_RELEASE_TAGS:
            return tag
    return None


def parse_version(value: str) -> tuple[int, int, int] | None:
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", value.strip())
    if not match:
        return None
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def is_release_successor(tag: str, manifest: str) -> bool:
    """Whether `manifest` is the tag's version or the next release after it.

    "Next release" means exactly one bump in exactly one slot, with the lower
    slots reset -- 0.10.0 may become 0.10.1, 0.11.0 or 1.0.0 and nothing else.
    Anything further ahead skipped a release; anything behind is the drift this
    guard exists to catch.
    """
    current = parse_version(tag)
    proposed = parse_version(manifest)
    if current is None or proposed is None:
        return False

    major, minor, patch = current
    return proposed in {
        current,
        (major, minor, patch + 1),
        (major, minor + 1, 0),
        (major + 1, 0, 0),
    }


class TestReleaseSuccessor:
    """A release PR bumps the manifest before the tag it will carry exists.

    Requiring exact equality made every release PR red, which is the failure
    mode the coverage-gate guard warns about: a check that cannot pass trains
    everyone to ignore it. Being one release ahead is the normal in-flight
    state; being *behind*, or ahead by more than one bump, is the drift.
    """

    @pytest.mark.parametrize("tag,manifest", [
        ("v0.10.0", "0.10.0"),   # steady state, between releases
        ("v0.10.0", "0.10.1"),   # patch release in flight
        ("v0.10.0", "0.11.0"),   # minor release in flight
        ("v0.10.0", "1.0.0"),    # the 1.0.0 commitment in flight
        ("v0.9.145", "0.10.0"),  # minor bump off a long patch series
    ])
    def test_at_most_one_bump_ahead_is_allowed(self, tag, manifest):
        assert is_release_successor(tag, manifest)

    @pytest.mark.parametrize("tag,manifest", [
        ("v0.9.145", "0.9.0"),   # the drift that motivated the guard
        ("v0.10.0", "0.9.0"),    # behind by a minor
        ("v0.11.0", "0.10.9"),   # behind by a minor, ahead on patch
        ("v0.10.0", "0.12.0"),   # skipped a minor
        ("v0.10.0", "0.10.3"),   # skipped patches
        ("v0.10.0", "2.0.0"),    # skipped a major
        ("v0.10.0", "1.1.0"),    # major bump must reset minor and patch
        ("v0.10.0", "0.11.2"),   # minor bump must reset patch
    ])
    def test_anything_else_is_drift(self, tag, manifest):
        assert not is_release_successor(tag, manifest)

    def test_unparseable_versions_are_not_treated_as_successors(self):
        assert not is_release_successor("v0.10.0", "not-a-version")
        assert not is_release_successor("vlatest", "0.11.0")


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


def test_pyproject_version_tracks_the_newest_release_tag():
    """The drift that actually happened: manifest 0.9.0 vs tag v0.9.145.

    The three files agreed with each other throughout, so only a tag comparison
    catches it.

    The manifest is allowed to sit one release ahead, because a release PR must
    bump it before the tag it will carry exists. Demanding exact equality made
    every release PR red for a reason that resolves itself on merge.
    """
    tag = newest_release_tag()
    if tag is None:
        pytest.skip("no git tags available (shallow clone or non-git checkout)")

    assert is_release_successor(tag, project_version()), (
        f"pyproject.toml says {project_version()} but the newest release tag is {tag}. "
        "The manifest may match that tag or be exactly one release ahead while a "
        "release is in flight. Bump the manifest (and ROADMAP.md / README.md), tag "
        "the release, or add the tag to NON_RELEASE_TAGS if it is not a software "
        "release."
    )


def test_pytest_is_configured_in_exactly_one_place():
    """Only pytest.ini configures pytest; a second source silently drifts.

    pyproject.toml previously carried a [tool.pytest.ini_options] table that
    pytest ignored (pytest.ini wins) and that had drifted to a shorter module
    list than the one actually in force.
    """
    assert "ini_options" not in pyproject().get("tool", {}).get("pytest", {}), (
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
    run_config = pyproject().get("tool", {}).get("coverage", {}).get("run", {})
    assert run_config, "pyproject.toml is missing [tool.coverage.run]"

    source = run_config.get("source", [])
    assert source, "[tool.coverage.run] must pin what is measured"
    assert "tests" not in source

    omit = run_config.get("omit", [])
    assert any("tests" in pattern for pattern in omit), (
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
