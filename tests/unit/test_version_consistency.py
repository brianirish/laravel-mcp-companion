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

import os
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


def version_tags(repo: Path = REPO_ROOT) -> list[str] | None:
    """Every v* tag, in no particular order. None when git cannot say."""
    try:
        result = subprocess.run(
            ["git", "tag", "--list", "v*"],
            cwd=repo, capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


# (major, minor, patch, candidate). The candidate is None for a final release.
Version = tuple[int, int, int, int | None]

_NUMBER = r"(0|[1-9]\d*)"
_CORE = rf"{_NUMBER}\.{_NUMBER}\.{_NUMBER}"
PROJECT_VERSION = re.compile(rf"{_CORE}(?:rc([1-9]\d*))?")   # 1.0.0, 1.0.0rc1
TAG = re.compile(rf"v{_CORE}(?:-rc([1-9]\d*))?")             # v1.0.0, v1.0.0-rc1


def _parsed(pattern: re.Pattern[str], value: str) -> Version | None:
    match = pattern.fullmatch(value)
    if not match:
        return None
    major, minor, patch, candidate = match.groups()
    return int(major), int(minor), int(patch), int(candidate) if candidate else None


def parse_project_version(value: str) -> Version | None:
    """Reads the form pyproject.toml and PyPI use: X.Y.Z or X.Y.ZrcN.

    Release candidates are the only pre-release read. Alpha, beta, dev, post
    and local versions are not versions this project releases.
    """
    return _parsed(PROJECT_VERSION, value)


def parse_tag(value: str) -> Version | None:
    """Reads the form a release tag uses: vX.Y.Z or vX.Y.Z-rcN."""
    return _parsed(TAG, value)


def is_project_version(value: str) -> bool:
    return parse_project_version(value) is not None


def release_order(version: Version) -> tuple[int, int, int, int, int]:
    """Sort key: candidates of X.Y.Z in number order, then X.Y.Z itself."""
    major, minor, patch, candidate = version
    return (major, minor, patch, 1 if candidate is None else 0, candidate or 0)


def newest_release_tag(repo: Path = REPO_ROOT) -> str | None:
    """The highest v* tag that represents an actual software release.

    Ordered here, not by git: `git tag --sort=-v:refname` lists v1.0.0-rc1
    above v1.0.0 unless `versionsort.suffix` is configured.
    """
    releases = [
        (release_order(parsed), tag)
        for tag in version_tags(repo) or []
        if tag not in NON_RELEASE_TAGS and (parsed := parse_tag(tag)) is not None
    ]
    return max(releases)[1] if releases else None


def unreadable_version_tags(repo: Path = REPO_ROOT) -> list[str] | None:
    """v* tags that `newest_release_tag` passes over without being told to."""
    tags = version_tags(repo)
    if tags is None:
        return None
    return sorted(
        tag for tag in tags if tag not in NON_RELEASE_TAGS and parse_tag(tag) is None
    )


def release_tag(version: str) -> str:
    """The git tag, and so the image tag, a project version is released under.

    A release candidate is versioned 1.0.0rc1 in pyproject.toml, the form PyPI
    takes, and tagged v1.0.0-rc1.
    """
    return "v" + re.sub(r"(?<=\d)(a|b|rc)(\d+)$", r"-\1\2", version)


@pytest.mark.parametrize("version,tag", [
    ("0.15.1", "v0.15.1"),
    ("1.0.0", "v1.0.0"),
    ("1.0.0rc1", "v1.0.0-rc1"),
    ("1.0.0rc12", "v1.0.0-rc12"),
    ("1.1.0b2", "v1.1.0-b2"),
])
def test_release_tag_keeps_the_hyphen_a_prerelease_is_tagged_with(version, tag):
    assert release_tag(version) == tag


def registry_version(version: str) -> str:
    """The semver form the MCP Registry is given: the tag without its v."""
    return release_tag(version).removeprefix("v")


def roadmap_version(text: str) -> str | None:
    match = re.search(r"^## Current Version:[ \t]*(v\S+)[ \t]*$", text, re.MULTILINE)
    return match.group(1) if match else None


def readme_version(text: str) -> str | None:
    match = re.search(r"^## Features \((v[^)\s]+)\)[ \t]*$", text, re.MULTILINE)
    return match.group(1) if match else None


def is_release_successor(tag: str, manifest: str) -> bool:
    """Whether `manifest` is the tag's version or the next release after it.

    From a final release, "next release" means exactly one bump in exactly one
    slot, with the lower slots reset -- 0.10.0 may become 0.10.1, 0.11.0 or
    1.0.0 -- or the first release candidate of one of those: 0.10.1rc1,
    0.11.0rc1 or 1.0.0rc1.

    From a release candidate, the next release is the next candidate of the
    same version or that version itself: 1.0.0rc1 may become 1.0.0rc2 or 1.0.0.

    Anything further ahead skipped a release; anything behind is the drift this
    guard exists to catch.

    `tag` is read as a tag (v1.0.0-rc1) and `manifest` as a project version
    (1.0.0rc1). Either one written in the other's form is not a successor.
    """
    current = parse_tag(tag)
    proposed = parse_project_version(manifest)
    if current is None or proposed is None:
        return False

    major, minor, patch, candidate = current
    if candidate is not None:
        return proposed in {
            current,
            (major, minor, patch, candidate + 1),
            (major, minor, patch, None),
        }

    bumps = [(major, minor, patch + 1), (major, minor + 1, 0), (major + 1, 0, 0)]
    return proposed in {
        current,
        *((*bump, None) for bump in bumps),
        *((*bump, 1) for bump in bumps),
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

    @pytest.mark.parametrize("tag,manifest", [
        ("v0.15.1", "1.0.0rc1"),      # first candidate of the next major
        ("v0.15.1", "0.16.0rc1"),     # first candidate of the next minor
        ("v0.15.1", "0.15.2rc1"),     # first candidate of the next patch
        ("v1.0.0-rc1", "1.0.0rc1"),   # steady state, the candidate is out
        ("v1.0.0-rc1", "1.0.0rc2"),   # next candidate in flight
        ("v1.0.0-rc1", "1.0.0"),      # the final release in flight
        ("v1.0.0-rc12", "1.0.0rc13"),
        ("v1.0.0", "1.0.1rc1"),
    ])
    def test_a_release_candidate_is_one_step_like_any_release(self, tag, manifest):
        assert is_release_successor(tag, manifest)

    @pytest.mark.parametrize("tag,manifest", [
        ("v0.15.1", "1.0.0rc2"),      # the first candidate is rc1
        ("v0.15.1", "2.0.0rc1"),      # candidate of a version that skips a major
        ("v0.15.1", "0.17.0rc1"),     # candidate of a version that skips a minor
        ("v0.15.1", "1.1.0rc1"),      # major bump must reset minor
        ("v0.15.1", "0.15.1rc1"),     # candidate of a version already released
        ("v1.0.0-rc1", "1.0.0rc3"),   # skipped a candidate
        ("v1.0.0-rc2", "1.0.0rc1"),   # behind by a candidate
        ("v1.0.0-rc1", "0.15.1"),     # behind: the manifest never left the last stable
        ("v1.0.0-rc1", "0.15.2"),
        ("v1.0.0-rc1", "0.16.0"),
        ("v1.0.0-rc1", "1.0.1"),      # skipped the final release
        ("v1.0.0-rc1", "1.1.0"),
        ("v1.0.0-rc1", "1.1.0rc1"),   # candidate of another version
        ("v1.0.0-rc1", "2.0.0"),
        ("v1.0.0", "1.0.0rc1"),       # behind: the final is out
        ("v1.0.0", "1.0.0rc2"),
    ])
    def test_a_release_candidate_out_of_step_is_drift(self, tag, manifest):
        assert not is_release_successor(tag, manifest)

    @pytest.mark.parametrize("tag,manifest", [
        ("v1.0.0rc1", "1.0.0rc1"),    # a tag carries the hyphen
        ("v1.0.0-rc1", "1.0.0-rc1"),  # the manifest does not
        ("v0.15.1", "v0.15.1"),       # the manifest has no leading v
        ("0.15.1", "0.15.1"),         # a tag does
        ("v1.0.0-rc0", "1.0.0rc1"),   # candidates count from 1
        ("v0.15.1", "1.0.0rc0"),
        ("v0.15.1", "1.0.0rc01"),
        ("v0.15.1", "1.0.0b1"),       # only rc is supported
        ("v0.15.1", "1.0.0a1"),
        ("v1.0.0-beta1", "1.0.0"),
        ("v0.15.1", "1.0.0.dev1"),
        ("v0.15.1", "1.0.0rc1.post1"),
    ])
    def test_each_side_is_read_in_its_own_form_only(self, tag, manifest):
        assert not is_release_successor(tag, manifest)


def git(cwd, *args):
    subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.test",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.test"},
    )


@pytest.fixture
def tagged_repo(tmp_path):
    """Returns a function that makes a repository carrying the given tags."""
    def make(*tags):
        git(tmp_path, "init", "-q", "-b", "main")
        git(tmp_path, "commit", "-q", "--allow-empty", "-m", "a commit to tag")
        for tag in tags:
            git(tmp_path, "tag", tag)
        return tmp_path
    return make


class TestNewestReleaseTag:
    """Ordering is done here and not by `git tag --sort=-v:refname`.

    Without `versionsort.suffix` configured, git's version sort puts
    v1.0.0-rc1 after v1.0.0, so it would report a candidate as newer than the
    final release it preceded.
    """

    @pytest.mark.parametrize("tags,newest", [
        (["v0.15.0", "v0.15.1"], "v0.15.1"),
        (["v0.9.9", "v0.10.0", "v0.9.145"], "v0.10.0"),          # numeric, not text
        (["v0.15.1", "v1.0.0-rc1"], "v1.0.0-rc1"),               # a candidate is newer than the last stable
        (["v0.15.1", "v1.0.0-rc1", "v1.0.0-rc2"], "v1.0.0-rc2"),
        (["v1.0.0-rc2", "v1.0.0-rc10"], "v1.0.0-rc10"),
        (["v0.15.1", "v1.0.0-rc1", "v1.0.0-rc2", "v1.0.0"], "v1.0.0"),  # the final wins
        (["v1.0.0", "v1.0.0-rc2", "v1.0.1-rc1"], "v1.0.1-rc1"),
        (["v0.10.0", "v0.10.1"], "v0.10.0"),                     # NON_RELEASE_TAGS
        (["v0.15.1", "docs-2026-11-17"], "v0.15.1"),             # a docs tag is not a release
        (["v0.15.1", "v1.0.0-beta1", "vlatest"], "v0.15.1"),     # not understood, so not chosen
    ])
    def test_picks_the_newest_release(self, tagged_repo, tags, newest):
        assert newest_release_tag(tagged_repo(*tags)) == newest

    def test_no_tags_is_none(self, tagged_repo):
        assert newest_release_tag(tagged_repo()) is None

    def test_not_a_repository_is_none(self, tmp_path):
        # Stop git from walking up into whatever repository holds tmp_path.
        (tmp_path / ".git").write_text("not a git directory")
        assert newest_release_tag(tmp_path) is None

    def test_tags_this_guard_cannot_read_are_reported(self, tagged_repo):
        repo = tagged_repo("v0.10.1", "v0.15.1", "v1.0.0-rc1", "v1.0.0-beta1", "vlatest", "docs-2026-11-17")
        assert unreadable_version_tags(repo) == ["v1.0.0-beta1", "vlatest"]


def test_every_version_tag_is_one_this_guard_can_read():
    """`newest_release_tag` passes over a v* tag it cannot parse.

    Such a tag (v2.0.0-beta1, say) would otherwise be invisible to the drift
    check below, so its existence fails here instead.
    """
    unreadable = unreadable_version_tags()
    if unreadable is None:
        pytest.skip("no git tags available (shallow clone or non-git checkout)")
    assert unreadable == [], (
        f"These v* tags are neither vX.Y.Z nor vX.Y.Z-rcN: {unreadable}. Teach "
        "parse_tag the form, or add the tag to NON_RELEASE_TAGS if it is not a "
        "software release."
    )


@pytest.mark.parametrize("version,registry", [
    ("0.15.1", "0.15.1"),
    ("1.0.0", "1.0.0"),
    ("1.0.0rc1", "1.0.0-rc1"),
    ("1.0.0rc12", "1.0.0-rc12"),
])
def test_registry_version_is_the_tag_without_its_v(version, registry):
    assert registry_version(version) == registry


@pytest.mark.parametrize("version", ["0.15.1", "1.0.0", "10.20.30", "1.0.0rc1", "1.0.0rc12"])
def test_versions_the_project_may_carry(version):
    assert is_project_version(version)


@pytest.mark.parametrize("version", [
    "1.0", "1.0.0.0", "v1.0.0", "01.0.0",
    "1.0.0-rc1",   # the tag form; PyPI and __version__ would then disagree
    "1.0.0rc0", "1.0.0rc", "1.0.0rc01", "1.0.0.rc1", "1.0.0RC1",
    "1.0.0a1", "1.0.0b1", "1.0.0.dev1", "1.0.0.post1", "1.0.0+local", "1.0.0rc1 ",
])
def test_versions_the_project_may_not_carry(version):
    assert not is_project_version(version)


def test_pyproject_version_is_a_release_or_a_release_candidate():
    version = project_version()
    assert is_project_version(version), (
        f"pyproject.toml version {version!r} is neither X.Y.Z nor X.Y.ZrcN"
    )


def test_roadmap_current_version_matches_pyproject():
    """The line shows the tag, so a release candidate reads v1.0.0-rc1."""
    assert roadmap_version(read("ROADMAP.md")) == release_tag(project_version()), (
        f"ROADMAP.md says {roadmap_version(read('ROADMAP.md'))} but pyproject.toml "
        f"says {project_version()}, which is tagged {release_tag(project_version())}"
    )


def test_roadmap_line_is_read_whole():
    assert roadmap_version("# Roadmap\n\n## Current Version: v0.15.1\n") == "v0.15.1"
    assert roadmap_version("## Current Version: v1.0.0-rc1\n") == "v1.0.0-rc1"
    assert roadmap_version("## Current Version: v1.0.0rc1\n") == "v1.0.0rc1"
    assert roadmap_version("## Current Version: 1.0.0\n") is None
    assert roadmap_version("no such line") is None


def test_readme_features_heading_matches_pyproject():
    """The heading shows the tag, so a release candidate reads v1.0.0-rc1."""
    assert readme_version(read("README.md")) == release_tag(project_version()), (
        f"README.md says {readme_version(read('README.md'))} but pyproject.toml "
        f"says {project_version()}, which is tagged {release_tag(project_version())}"
    )


def test_readme_heading_is_read_whole():
    assert readme_version("## Features (v0.15.1)\n") == "v0.15.1"
    assert readme_version("intro\n\n## Features (v1.0.0-rc1)\n\ntext") == "v1.0.0-rc1"
    assert readme_version("## Features (v1.0.0rc1)\n") == "v1.0.0rc1"
    assert readme_version("## Features\n") is None


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


def test_server_version_constant_matches_pyproject():
    """The running server reports its version at initialize; it must not drift.

    There is no installed package metadata inside the Docker image (the source
    is COPYed and run directly), so the version lives in a constant that this
    guard chains to the same source of truth as everything else.
    """
    from laravel_mcp_companion import server as lmc
    assert lmc.SERVER_VERSION == project_version(), (
        f"SERVER_VERSION says {lmc.SERVER_VERSION} but pyproject.toml says "
        f"{project_version()}"
    )


def test_server_json_version_matches_pyproject():
    """server.json is the registry's view of the release; it must not drift.

    The publish workflow stamps the tag version in at release time, but the
    checked-in copy is what the .well-known endpoint serves and what reviewers
    read, so it tracks pyproject like everything else.
    """
    import json

    data = json.loads((REPO_ROOT / "server.json").read_text(encoding="utf-8"))
    # The registry's own version is semver: 1.0.0-rc1 for a release candidate.
    assert data["version"] == registry_version(project_version())
    packages = {pkg["registryType"]: pkg for pkg in data["packages"]}
    assert set(packages) == {"oci", "pypi"}

    # OCI packages carry no separate version field (the live registry rejects
    # one); the canonical identifier is the whole reference. Its tag keeps the
    # leading v because the image is tagged with the git tag verbatim.
    image = packages["oci"]
    assert "version" not in image
    assert image["identifier"].endswith(f":{release_tag(project_version())}")

    # The PyPI package is named by the project name and an exact version, in
    # the form PyPI lists it under: 1.0.0rc1 for a release candidate.
    wheel = packages["pypi"]
    assert wheel["identifier"] == "laravel-mcp-companion"
    assert wheel["version"] == project_version()
    assert wheel["runtimeHint"] == "uvx"
    assert wheel["transport"] == {"type": "stdio"}


def test_package_json_is_gone():
    """package.json was vestigial npm metadata frozen at 0.8.0.

    Nothing consumed it, no guard checked it, and it shipped a wrong version
    number in the image for two years. Registry metadata lives in server.json.
    """
    assert not (REPO_ROOT / "package.json").exists()


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
