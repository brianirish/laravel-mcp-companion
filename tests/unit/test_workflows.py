"""The GitHub Actions workflows that test, sync and publish the project.

Each test names a way these have broken before, or a promise another part of
the repository makes about them.
"""

import re
from pathlib import Path

import pytest
import yaml

WORKFLOWS = Path(__file__).resolve().parents[2] / ".github" / "workflows"


def load(name: str) -> dict:
    return yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))


def text(name: str) -> str:
    return (WORKFLOWS / name).read_text(encoding="utf-8")


def triggers(workflow: dict) -> dict:
    # YAML 1.1 reads the bare key `on` as the boolean True.
    found = workflow.get("on", workflow.get(True))
    if isinstance(found, str):
        return {found: None}
    assert isinstance(found, dict), "workflow has no triggers"
    return found


def run_scripts(workflow: dict) -> str:
    return "\n".join(
        step.get("run", "")
        for job in workflow["jobs"].values()
        for step in job["steps"]
    )


@pytest.mark.parametrize("name", sorted(p.name for p in WORKFLOWS.glob("*.y*ml")))
def test_every_workflow_parses_and_has_a_job(name):
    workflow = load(name)
    assert workflow["jobs"]
    assert triggers(workflow)


class TestCI:
    def test_runs_on_pull_requests_and_on_main(self):
        on = triggers(load("ci.yaml"))
        assert "pull_request" in on
        assert on["push"]["branches"] == ["main"]

    def test_reports_the_check_the_ruleset_on_main_requires(self):
        """The ruleset requires a check named ci-test. A job under any other
        name leaves every pull request waiting on a check that never comes."""
        jobs = load("ci.yaml")["jobs"]
        assert "ci-test" in jobs
        assert jobs["ci-test"].get("name", "ci-test") == "ci-test"

    def test_runs_the_same_checks_a_contributor_is_asked_to_run(self):
        script = run_scripts(load("ci.yaml"))
        for command in ("ruff check", "mypy", "pytest", "-m e2e", "-m bench", "uv sync --frozen"):
            assert command in script, command

    def test_the_nightly_docs_branch_skips_only_the_corpus_tests(self):
        script = run_scripts(load("ci.yaml"))
        assert "update-laravel-docs" in script
        assert "not corpus" in script

    def test_can_only_read_the_repository(self):
        assert load("ci.yaml")["permissions"] == {"contents": "read"}

    def test_tests_the_oldest_and_the_newest_python_the_readme_names(self):
        """The README says Python 3.12 or newer. ci-test runs the oldest
        version pyproject.toml allows; a second job, which the ruleset does
        not require, runs the tests on the newest."""
        jobs = load("ci.yaml")["jobs"]
        pyproject = (Path(__file__).resolve().parents[2] / "pyproject.toml").read_text(encoding="utf-8")
        oldest = re.search(r'requires-python = ">=(3\.\d+)"', pyproject).group(1)

        def pythons(job: dict) -> list[str]:
            script = "\n".join(step.get("run", "") for step in job["steps"])
            return re.findall(r"--python (3\.\d+)", script)

        assert pythons(jobs["ci-test"]) == [oldest]
        newest = pythons(jobs["newest-python"])
        assert newest and all(tuple(map(int, v.split("."))) > tuple(map(int, oldest.split("."))) for v in newest)
        assert "pytest" in "\n".join(step.get("run", "") for step in jobs["newest-python"]["steps"])


class TestReleaseImage:
    def test_builds_on_version_tags_and_docs_tags(self):
        on = triggers(load("release.yaml"))
        assert on["push"]["tags"] == ["v*", "docs-*"]
        assert "workflow_dispatch" in on

    def test_publishes_both_platforms(self):
        """From January to November 2026 the image was amd64 only: the build
        step named two platforms and built one, and nothing looked."""
        workflow = load("release.yaml")
        build = next(
            step for job in workflow["jobs"].values() for step in job["steps"]
            if "build-push-action" in step.get("uses", "")
        )
        assert build["with"]["platforms"] == "linux/amd64,linux/arm64"
        assert "imagetools inspect" in run_scripts(workflow), (
            "the workflow should check the published manifest lists both platforms"
        )

    def test_a_docs_tag_is_built_from_released_code(self):
        script = run_scripts(load("release.yaml"))
        assert "scripts/release_tree.sh" in script
        assert "--moving-tag" in script

    def test_a_build_is_never_cancelled_by_another_tag(self):
        """A shared queue keeps one waiting run and cancels the rest, which
        could drop a release build behind a nightly one."""
        concurrency = load("release.yaml")["concurrency"]
        assert concurrency["cancel-in-progress"] is False
        assert "inputs.tag" in concurrency["group"]
        assert "github.ref_name" in concurrency["group"]

    def test_only_the_image_job_can_write_packages(self):
        workflow = load("release.yaml")
        assert workflow["permissions"] == {"contents": "read"}
        writers = [name for name, job in workflow["jobs"].items()
                   if job.get("permissions", {}).get("packages") == "write"]
        assert len(writers) == 1


class TestDocsUpdate:
    def test_runs_nightly_and_can_be_run_by_hand(self):
        on = triggers(load("docs-update.yaml"))
        assert on["schedule"]
        assert "dry_run" in on["workflow_dispatch"]["inputs"]

    def test_never_waits_on_every_check(self):
        """`gh pr checks --watch` returns when every check has finished,
        required or not. One that never finished held the sync for six weeks."""
        assert not re.search(r"gh pr checks[^\n]*--watch", run_scripts(load("docs-update.yaml")))

    def test_pushes_as_a_user_so_that_other_workflows_run(self):
        """A push or pull request made with the workflow's own token starts no
        other workflow: no CI on the pull request, no image for the tag."""
        workflow = text("docs-update.yaml")
        assert "secrets.PAT_FOR_WORKFLOWS" in workflow
        assert "persist-credentials: false" in workflow

    def test_tags_by_date_and_does_not_publish_a_release(self):
        script = run_scripts(load("docs-update.yaml"))
        assert "docs-$(date -u +%Y-%m-%d)" in script
        assert "gh release create" not in script

    def test_a_degraded_sync_fails_the_run_after_publishing(self):
        steps = [step.get("name", "") for job in load("docs-update.yaml")["jobs"].values()
                 for step in job["steps"]]
        tag = next(i for i, name in enumerate(steps) if "tag" in name.lower())
        fail = max(i for i, name in enumerate(steps) if "degraded" in name.lower())
        assert fail > tag


class TestPyPIPublish:
    def test_a_version_tag_publishes_and_it_can_be_run_by_hand(self):
        found = triggers(load("publish-pypi.yml"))
        assert found["push"]["tags"] == ["v*"]
        assert "tag" in found["workflow_dispatch"]["inputs"]

    def test_a_docs_tag_does_not_publish(self):
        # A docs tag is main as it stands, not a release. `v*` cannot match
        # `docs-2026-11-17`; this fails if the pattern is ever widened.
        for pattern in triggers(load("publish-pypi.yml"))["push"]["tags"]:
            assert pattern.startswith("v")

    def test_refuses_a_tag_that_is_not_the_project_version(self):
        assert "does not match pyproject.toml version" in text("publish-pypi.yml")

    def test_authenticates_without_a_stored_token(self):
        job = load("publish-pypi.yml")["jobs"]["publish"]
        assert job["environment"] == "pypi"
        assert job["permissions"]["id-token"] == "write"
        assert "password" not in text("publish-pypi.yml")


    def test_a_run_by_hand_finishes_an_upload_that_stopped_part_way(self):
        # PyPI refuses a file it already has. A tag's run stays strict; the
        # retry by hand skips what is there and uploads what is missing.
        steps = load("publish-pypi.yml")["jobs"]["publish"]["steps"]
        publish = next(step for step in steps if "pypi-publish" in step.get("uses", ""))
        assert publish["with"]["skip-existing"] == "${{ github.event_name == 'workflow_dispatch' }}"


class TestRegistryPublish:
    def test_waits_for_the_pypi_package_it_lists(self):
        # The registry checks that each package it is given exists. The PyPI
        # workflow starts on the same tag and may finish later.
        body = text("publish-mcp.yml")
        assert "https://pypi.org/pypi/laravel-mcp-companion/" in body

    def test_stamps_each_package_by_its_registry_and_not_its_position(self):
        body = text("publish-mcp.yml")
        assert ".packages[0]" not in body
        assert 'registryType == "oci"' in body
        assert 'registryType == "pypi"' in body


ALL_WORKFLOWS = sorted(p.name for p in WORKFLOWS.glob("*.y*ml"))


class TestSupplyChain:
    """What a workflow runs with its tokens is whatever its `uses:` lines
    name. A tag such as v5 can be moved to different code by whoever controls
    the action's repository; a commit cannot."""

    @pytest.mark.parametrize("name", ALL_WORKFLOWS)
    def test_every_action_is_pinned_to_a_commit(self, name):
        uses = re.findall(r"^\s*(?:- )?uses:\s*(\S+)(.*)$", text(name), re.MULTILINE)
        for reference, rest in uses:
            action, _, ref = reference.partition("@")
            assert re.fullmatch(r"[0-9a-f]{40}", ref), f"{name}: {action} is pinned to {ref!r}, not a commit"
            assert re.search(r"#\s*v?\d", rest), f"{name}: {action} has no comment naming the version its commit is"

    @pytest.mark.parametrize("name", ALL_WORKFLOWS)
    def test_no_checkout_leaves_its_token_on_disk(self, name):
        for job in load(name)["jobs"].values():
            for step in job["steps"]:
                if "actions/checkout@" in step.get("uses", ""):
                    assert step.get("with", {}).get("persist-credentials") is False, f"{name}: {step.get('name')}"

    def test_dependabot_keeps_the_pins_current(self):
        """A pinned commit never moves, so something has to propose the next one."""
        config = yaml.safe_load((WORKFLOWS.parent / "dependabot.yml").read_text(encoding="utf-8"))
        ecosystems = {update["package-ecosystem"] for update in config["updates"]}
        assert {"github-actions", "docker"} <= ecosystems

    def test_dependabot_does_not_propose_a_different_python_for_the_image(self):
        """Its first proposal was 3.12 to 3.15, which cannot build from the
        lockfile. The Python version changes with uv.lock and CI, by hand."""
        config = yaml.safe_load((WORKFLOWS.parent / "dependabot.yml").read_text(encoding="utf-8"))
        docker = next(update for update in config["updates"] if update["package-ecosystem"] == "docker")
        python = next(rule for rule in docker["ignore"] if rule["dependency-name"] == "python")
        assert set(python["update-types"]) == {"version-update:semver-major", "version-update:semver-minor"}

    def test_the_registry_publisher_is_a_named_release_with_a_checked_digest(self):
        install = next(
            step for step in load("publish-mcp.yml")["jobs"]["publish"]["steps"]
            if step.get("name") == "Install mcp-publisher"
        )
        script = install["run"]
        assert re.fullmatch(r"v\d+\.\d+\.\d+", install["env"]["PUBLISHER_VERSION"])
        assert re.fullmatch(r"[0-9a-f]{64}", install["env"]["PUBLISHER_SHA256"])
        assert "releases/download/${PUBLISHER_VERSION}/mcp-publisher_linux_amd64.tar.gz" in script
        assert "releases/latest/" not in script
        assert "| tar" not in script, "the archive must be checked before it is unpacked"
        assert script.index("sha256sum --check") < script.index("tar x")

    def test_the_image_build_refreshes_the_os_packages_on_every_run(self):
        """The Dockerfile upgrades Alpine's packages. With the build cache,
        that step would run once and be reused until the base image changed."""
        build = next(
            step for step in load("release.yaml")["jobs"]["image"]["steps"]
            if "docker/build-push-action" in step.get("uses", "")
        )
        # The run id alone is the same when a failed run is run again.
        assert "OS_PACKAGES_REFRESH=${{ github.run_id }}-${{ github.run_attempt }}" in build["with"]["build-args"]


def test_no_workflow_still_points_at_harness():
    for path in WORKFLOWS.glob("*.y*ml"):
        assert "harness" not in path.read_text(encoding="utf-8").lower(), path.name
