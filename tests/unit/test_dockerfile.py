"""The image must not rebuild its dependency layer for a documentation change.

Documentation syncs land daily and touch only `docs/`. Whether that costs users
a dependency re-download is decided entirely by the order of two lines in the
Dockerfile, which is exactly the kind of thing that gets reordered by accident.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def dockerfile_lines() -> list[str]:
    text = (REPO_ROOT / "Dockerfile").read_text(encoding="utf-8")
    # Join continuations so a multi-line RUN is one logical instruction.
    text = re.sub(r"\\\n\s*", " ", text)
    return [line for line in (raw.strip() for raw in text.splitlines())
            if line and not line.startswith("#")]


def index_of(pattern: str) -> int:
    for i, line in enumerate(dockerfile_lines()):
        if re.search(pattern, line):
            return i
    raise AssertionError(f"no Dockerfile instruction matches {pattern!r}")


class TestLayerOrdering:
    def test_dependencies_install_before_the_source_copy(self):
        """The regression this file exists to prevent.

        With `COPY . .` above `pip install`, the daily documentation commit
        invalidates the dependency layer too, so everyone pulling :latest
        re-downloads every dependency for a content-only change.
        """
        assert index_of(r"pip install.*requirements\.txt") < index_of(r"^COPY \. \."), (
            "COPY . . must come after the dependency install, or a docs-only "
            "change busts the dependency layer for every user"
        )

    def test_requirements_are_copied_before_they_are_installed(self):
        assert index_of(r"^COPY .*requirements") < index_of(r"pip install.*requirements\.txt")

    def test_requirements_are_copied_without_the_rest_of_the_tree(self):
        """Copying the tree to get requirements.txt would defeat the ordering."""
        lines = dockerfile_lines()
        copy = lines[index_of(r"^COPY .*requirements")]
        assert not re.match(r"^COPY \s*\.\s", copy), (
            f"{copy!r} copies the whole context; copy only the requirements files"
        )


class TestDockerignore:
    @pytest.mark.parametrize("unwanted", [".git", ".venv", "htmlcov", "__pycache__"])
    def test_build_context_excludes_local_only_directories(self, unwanted):
        """.venv alone is 219MB, and none of these belong in a published image."""
        path = REPO_ROOT / ".dockerignore"
        assert path.exists(), ".dockerignore is missing; the build context ships .git and .venv"

        entries = {line.strip().strip("/") for line in path.read_text().splitlines()
                   if line.strip() and not line.startswith("#")}
        assert unwanted in entries, f"{unwanted} is not excluded from the build context"

    def test_the_documentation_corpus_is_still_shipped(self):
        """The docs ARE the product. Excluding them would produce an empty server."""
        entries = {line.strip().strip("/") for line
                   in (REPO_ROOT / ".dockerignore").read_text().splitlines()
                   if line.strip() and not line.startswith("#")}
        assert "docs" not in entries


class TestImageIsBuiltInCI:
    """Nothing built the image for the life of the project.

    The first real build of any Dockerfile change was the next release, where a
    mistake breaks the release rather than a pull request. That is how the
    layer-ordering defect above survived: it was never wrong enough to fail a
    build, and no build ran anyway.
    """

    def ci_pipeline(self) -> str:
        path = (REPO_ROOT / ".harness/orgs/default/projects/laravel_mcp_companion"
                / "pipelines/ci.yaml")
        assert path.exists(), f"CI pipeline definition not found at {path}"
        return path.read_text(encoding="utf-8")

    def test_ci_builds_the_image(self):
        assert re.search(r"docker\s+build", self.ci_pipeline()), (
            "CI must build the image, or Dockerfile changes reach users unbuilt"
        )

    def test_ci_does_not_push_from_a_pull_request(self):
        """Validation only. Publishing is the release pipeline's job."""
        ci = self.ci_pipeline()
        assert "BuildAndPushDockerRegistry" not in ci
        assert not re.search(r"docker\s+push", ci)

    def test_the_built_image_is_actually_started(self):
        """A build proves the image assembles, not that it runs."""
        assert re.search(r"docker\s+run", self.ci_pipeline()), (
            "CI should start the image it just built"
        )
