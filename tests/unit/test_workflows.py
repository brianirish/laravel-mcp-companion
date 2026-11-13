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


def test_no_workflow_still_points_at_harness():
    for path in WORKFLOWS.glob("*.y*ml"):
        assert "harness" not in path.read_text(encoding="utf-8").lower(), path.name
