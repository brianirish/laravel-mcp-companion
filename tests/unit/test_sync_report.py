"""The sync health report the daily pipeline gates on and pastes into its PR.

Before this existed the pipeline ran the updater under `set +e`, discarded
both exit codes, and wrote a fixed PR body claiming auto-discovery worked for
every service. Forge fetching 18 of 39 pages, a source whose domain no longer
resolves, and one that had never been saved all passed as green.
"""

import json
import time

import pytest

from laravel_mcp_companion import docs_updater
from laravel_mcp_companion.docs_updater import (
    CommunityPackageFetcher,
    ExternalDocsFetcher,
    LearningResourceFetcher,
    build_sync_report,
)

NOW = 1_800_000_000.0
DAY = 86400


def _metadata_paths(root):
    """Where each configured source keeps its metadata, by source name."""
    paths = {}
    for service in ExternalDocsFetcher(root).laravel_services:
        paths[service] = root / "external" / service / ".cache_metadata.json"
    for source in LearningResourceFetcher(root).learning_sources:
        paths[source] = root / "learning_resources" / source / ".cache_metadata.json"
    for package, config in CommunityPackageFetcher(root).community_packages.items():
        for sub in config.get("packages", {}):
            paths[f"{package}/{sub}"] = root / "packages" / package / sub / ".metadata" / "cache.json"
        if not config.get("packages"):
            paths[package] = root / "packages" / package / ".metadata" / "cache.json"
    return paths


def _write(path, **fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(fields))


@pytest.fixture
def healthy(temp_dir):
    """A docs tree in which every configured source synced an hour ago."""
    paths = _metadata_paths(temp_dir)
    for path in paths.values():
        _write(path, success_rate=1.0, fetched_sections=["a", "b"], total_sections=2,
               discovery_method="auto-discovery", cached_at=NOW - 3600)
    return temp_dir, paths


class TestSyncReport:
    def test_a_fully_synced_tree_has_nothing_to_flag(self, healthy):
        root, _ = healthy

        report, problems = build_sync_report(root, now=NOW)

        assert problems == []
        assert "| forge | ok | 2/2 | auto-discovery |" in report

    def test_a_source_that_fetched_too_few_pages_is_flagged(self, healthy):
        root, paths = healthy
        _write(paths["forge"], success_rate=18 / 39, fetched_sections=["x"] * 18, total_sections=39,
               discovery_method="manual configuration", cached_at=NOW - 3600)

        report, problems = build_sync_report(root, now=NOW)

        assert problems == ["forge: fetched 18 of 39 pages"]
        assert "| forge | DEGRADED | 18/39 | manual configuration |" in report

    def test_a_source_that_has_never_been_saved_is_flagged(self, healthy):
        root, paths = healthy
        paths["laracasts-index"].unlink()

        _, problems = build_sync_report(root, now=NOW)

        assert problems == ["laracasts-index: never synced"]

    def test_a_source_whose_last_sync_is_old_is_flagged(self, healthy):
        """A fetch that fails outright writes no metadata, so the old file and
        its perfect success rate stay behind. Age is the only tell."""
        root, paths = healthy
        _write(paths["laravel-bootcamp"], success_rate=1.0, fetched_sections=8, total_sections=8,
               cached_at=NOW - 22 * DAY)

        _, problems = build_sync_report(root, now=NOW)

        assert problems == ["laravel-bootcamp: last synced 22 days ago"]

    def test_a_package_with_only_the_legacy_timestamp_is_aged_from_it(self, healthy):
        root, paths = healthy
        _write(paths["livewire"], cache_time=NOW - 400 * DAY, sections_count=36)

        _, problems = build_sync_report(root, now=NOW)

        assert problems == ["livewire: last synced 400 days ago"]

    def test_unreadable_metadata_is_flagged_rather_than_crashing(self, healthy):
        root, paths = healthy
        paths["nova"].write_text("{not json")

        _, problems = build_sync_report(root, now=NOW)

        assert problems == ["nova: metadata unreadable"]

    def test_problems_are_listed_in_the_report_itself(self, healthy):
        root, paths = healthy
        paths["laracasts-index"].unlink()

        report, _ = build_sync_report(root, now=NOW)

        assert "- laracasts-index: never synced" in report

    def test_core_versions_are_listed_with_their_synced_commit(self, healthy):
        root, _ = healthy
        _write(root / "13.x" / ".metadata" / "sync_info.json", version="13.x",
               commit_sha="2e7f6c6d3c515800e80da27ac0d0a214858e8d71", commit_date="2026-11-11T14:28:43Z")

        report, _ = build_sync_report(root, now=NOW)

        assert "| 13.x | 2e7f6c6 | 2026-11-11 |" in report


class TestSyncReportCommand:
    def _run(self, monkeypatch, root):
        monkeypatch.setattr("sys.argv", ["docs_updater.py", "--target-dir", str(root), "--sync-report"])
        return docs_updater.main()

    def test_exits_zero_and_prints_the_report_when_healthy(self, healthy, monkeypatch, capsys):
        root, paths = healthy
        for path in paths.values():  # the command reads the real clock
            data = json.loads(path.read_text())
            _write(path, **{**data, "cached_at": time.time() - 3600})

        assert self._run(monkeypatch, root) == 0
        assert "| forge | ok | 2/2 | auto-discovery |" in capsys.readouterr().out

    def test_exits_non_zero_when_a_source_is_degraded(self, healthy, monkeypatch, capsys):
        root, paths = healthy
        for path in paths.values():
            data = json.loads(path.read_text())
            _write(path, **{**data, "cached_at": time.time() - 3600})
        paths["laracasts-index"].unlink()

        assert self._run(monkeypatch, root) == 1
        assert "- laracasts-index: never synced" in capsys.readouterr().out
