"""Tests for documentation freshness reporting.

Documentation ships as a snapshot, so it ages. The failure mode this guards
against is silent: an assistant answering confidently about a recent Laravel
feature from a corpus months out of date, with nothing in the output hinting
that the corpus is old.
"""

import json
import time

import pytest

from mcp_tools import (
    DOCS_STALE_AFTER_DAYS,
    describe_docs_freshness,
    docs_are_stale,
    get_docs_snapshot_age,
    parse_sync_time,
)


def write_snapshot(docs_path, days_old, version="12.x"):
    """Create documentation metadata synced `days_old` days ago."""
    metadata_dir = docs_path / version / ".metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    synced = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - days_old * 86400))
    (metadata_dir / "sync_info.json").write_text(
        json.dumps({"version": version, "sync_time": synced, "commit_sha": "abc1234"})
    )
    return synced


class TestSnapshotAge:
    @pytest.mark.parametrize("days", [0, 1, 5, 45, 400])
    def test_reports_age_in_days(self, tmp_path, days):
        write_snapshot(tmp_path, days)
        _, age = get_docs_snapshot_age(tmp_path)
        assert age == days

    def test_reports_newest_version_when_several_exist(self, tmp_path):
        write_snapshot(tmp_path, 90, version="11.x")
        write_snapshot(tmp_path, 3, version="12.x")
        _, age = get_docs_snapshot_age(tmp_path)
        assert age == 3, "should report the freshest snapshot, not the oldest"

    def test_missing_metadata_is_not_an_error(self, tmp_path):
        assert get_docs_snapshot_age(tmp_path) == (None, None)

    def test_corrupt_timestamp_is_not_an_error(self, tmp_path):
        metadata_dir = tmp_path / "12.x" / ".metadata"
        metadata_dir.mkdir(parents=True)
        (metadata_dir / "sync_info.json").write_text(json.dumps({"sync_time": "garbage"}))
        assert get_docs_snapshot_age(tmp_path) == (None, None)


class TestStaleness:
    def test_fresh_docs_are_not_stale(self, tmp_path):
        write_snapshot(tmp_path, 1)
        assert docs_are_stale(tmp_path) is False

    def test_docs_just_inside_the_threshold_are_not_stale(self, tmp_path):
        write_snapshot(tmp_path, DOCS_STALE_AFTER_DAYS)
        assert docs_are_stale(tmp_path) is False

    def test_docs_past_the_threshold_are_stale(self, tmp_path):
        write_snapshot(tmp_path, DOCS_STALE_AFTER_DAYS + 1)
        assert docs_are_stale(tmp_path) is True

    def test_unknown_age_is_not_reported_as_stale(self, tmp_path):
        """Absent metadata must not produce a false staleness warning."""
        assert docs_are_stale(tmp_path) is False


class TestFreshnessDescription:
    def test_today_reads_naturally(self, tmp_path):
        write_snapshot(tmp_path, 0)
        assert "today" in describe_docs_freshness(tmp_path)

    def test_singular_day(self, tmp_path):
        write_snapshot(tmp_path, 1)
        assert "1 day ago" in describe_docs_freshness(tmp_path)

    def test_plural_days(self, tmp_path):
        write_snapshot(tmp_path, 12)
        assert "12 days ago" in describe_docs_freshness(tmp_path)

    def test_unknown_when_never_synced(self, tmp_path):
        assert "unknown" in describe_docs_freshness(tmp_path)


class TestParseSyncTime:
    @pytest.mark.parametrize("value", [None, "", "unknown", "not-a-date", "2026-13-45"])
    def test_unparseable_values_return_none(self, value):
        assert parse_sync_time(value) is None

    def test_naive_timestamps_are_treated_as_utc(self):
        parsed = parse_sync_time("2026-07-30T12:00:00")
        assert parsed is not None and parsed.tzinfo is not None

    def test_zulu_suffix_is_understood(self):
        parsed = parse_sync_time("2026-07-30T12:00:00Z")
        assert parsed is not None and parsed.year == 2026


class TestServerInstructions:
    """The assistant learns the snapshot age from the server instructions."""

    def test_instructions_state_the_snapshot_age(self, tmp_path):
        from laravel_mcp_companion import build_server_instructions

        write_snapshot(tmp_path, 45)
        instructions = build_server_instructions(tmp_path, "12.x")

        assert "45 days ago" in instructions
        assert "update_laravel_docs" in instructions, (
            "instructions must tell the assistant how to refresh"
        )

    def test_instructions_cover_usage_and_default_version(self, tmp_path):
        from laravel_mcp_companion import build_server_instructions

        write_snapshot(tmp_path, 1)
        instructions = build_server_instructions(tmp_path, "11.x")

        assert "search_laravel_docs" in instructions
        assert "11.x" in instructions

    def test_instructions_survive_missing_metadata(self, tmp_path):
        from laravel_mcp_companion import build_server_instructions

        instructions = build_server_instructions(tmp_path, "12.x")
        assert "unknown" in instructions
