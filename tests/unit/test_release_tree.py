"""The nightly image carries released code and that night's documentation.

Documentation syncs are tagged `docs-YYYY-MM-DD` on main, and the release
pipeline builds an image from each tag and moves `latest` to it. Built
straight from the tag, that image contained whatever code had merged to main
since the last release, so every unreleased change reached `latest` users the
next night. `scripts/release_tree.sh` rearranges the checkout before the build:
the newest released version's code, with the docs tag's `docs/` directory.
"""

import os
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "release_tree.sh"


def git(cwd, *args):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.test",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.test"},
    ).stdout.strip()


def commit(repo, message, files):
    for name, content in files.items():
        path = repo / name
        if content is None:
            path.unlink()
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)


@pytest.fixture
def checkout(tmp_path):
    """A clone, as the pipeline has it, of a repository with this history:

    v0.1.0       server 0.1, docs: a
    v0.2.0       server 0.2, docs: a
    v0.3.0-rc1   server 0.3-rc
    (main)       server unreleased, new_module.py added, docs: a (edited), b; old.md removed
    docs-2026-01-02 tags main
    """
    origin = tmp_path / "origin"
    origin.mkdir()
    git(origin, "init", "-q", "-b", "main")
    commit(origin, "0.1", {"server.py": "0.1", "docs/a.md": "a", "docs/old.md": "old"})
    git(origin, "tag", "v0.1.0")
    commit(origin, "0.2", {"server.py": "0.2"})
    git(origin, "tag", "v0.2.0")
    commit(origin, "0.3 rc", {"server.py": "0.3-rc"})
    git(origin, "tag", "v0.3.0-rc1")
    commit(origin, "unreleased work", {"server.py": "unreleased", "new_module.py": "new"})
    commit(origin, "docs sync", {"docs/a.md": "a, edited", "docs/b.md": "b", "docs/old.md": None})
    git(origin, "tag", "docs-2026-01-02")

    clone = tmp_path / "clone"
    git(tmp_path, "clone", "-q", "--depth", "1", "--branch", "docs-2026-01-02", f"file://{origin}", "clone")
    return clone


def run(clone, tag):
    return subprocess.run(["bash", str(SCRIPT), tag], cwd=clone, capture_output=True, text=True)


class TestDocsTagBuild:
    def test_code_comes_from_the_newest_released_version(self, checkout):
        result = run(checkout, "docs-2026-01-02")

        assert result.returncode == 0, result.stderr
        assert (checkout / "server.py").read_text() == "0.2"

    def test_a_release_candidate_is_not_the_newest_release(self, checkout):
        run(checkout, "docs-2026-01-02")

        assert (checkout / "server.py").read_text() != "0.3-rc"

    def test_code_added_since_the_release_is_absent(self, checkout):
        run(checkout, "docs-2026-01-02")

        assert not (checkout / "new_module.py").exists()

    def test_docs_come_from_the_docs_tag(self, checkout):
        run(checkout, "docs-2026-01-02")

        assert (checkout / "docs" / "a.md").read_text() == "a, edited"
        assert (checkout / "docs" / "b.md").read_text() == "b"

    def test_a_page_the_sync_removed_does_not_come_back_from_the_release(self, checkout):
        run(checkout, "docs-2026-01-02")

        assert not (checkout / "docs" / "old.md").exists()

    def test_the_chosen_release_is_reported(self, checkout):
        result = run(checkout, "docs-2026-01-02")

        assert "v0.2.0" in result.stdout


class TestVersionTagBuild:
    def test_a_version_tag_is_built_as_it_is(self, checkout):
        git(checkout, "fetch", "-q", "--depth", "1", "origin", "refs/tags/v0.1.0:refs/tags/v0.1.0")
        git(checkout, "checkout", "-q", "v0.1.0")

        result = run(checkout, "v0.1.0")

        assert result.returncode == 0, result.stderr
        assert (checkout / "server.py").read_text() == "0.1"
        assert (checkout / "docs" / "old.md").exists()


class TestNoReleaseYet:
    def test_a_repository_with_no_version_tag_fails_rather_than_guessing(self, tmp_path):
        origin = tmp_path / "origin"
        origin.mkdir()
        git(origin, "init", "-q", "-b", "main")
        commit(origin, "first", {"server.py": "x", "docs/a.md": "a"})
        git(origin, "tag", "docs-2026-01-02")
        git(tmp_path, "clone", "-q", "--depth", "1", "--branch", "docs-2026-01-02", f"file://{origin}", "clone")

        result = run(tmp_path / "clone", "docs-2026-01-02")

        assert result.returncode != 0
        assert "no released version" in result.stderr.lower()


def moving_tag(clone, tag):
    result = subprocess.run(["bash", str(SCRIPT), "--moving-tag", tag], cwd=clone, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


class TestWhichBuildsMoveLatest:
    """`latest` follows the newest stable release and its nightly docs builds.
    A build that should not move it gets its own tag a second time, which is
    a no-op for the registry."""

    def test_a_docs_build_moves_latest(self, checkout):
        assert moving_tag(checkout, "docs-2026-01-02") == "latest"

    def test_the_newest_stable_release_moves_latest(self, checkout):
        assert moving_tag(checkout, "v0.2.0") == "latest"

    def test_a_release_candidate_does_not_move_latest(self, checkout):
        assert moving_tag(checkout, "v0.3.0-rc1") == "v0.3.0-rc1"

    def test_a_patch_to_an_older_line_does_not_move_latest(self, checkout):
        assert moving_tag(checkout, "v0.1.0") == "v0.1.0"
