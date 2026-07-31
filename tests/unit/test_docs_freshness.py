"""Tests for documentation freshness reporting.

Documentation ships as a snapshot, so it ages. The failure mode this guards
against is silent: an assistant answering confidently about a recent Laravel
feature from a corpus months out of date, with nothing in the output hinting
that the corpus is old.
"""

import json
import time
from datetime import datetime, timedelta, timezone

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

    def test_reports_the_requested_version_not_the_freshest(self, tmp_path):
        """A pinned old version must not inherit a newer version's freshness."""
        write_snapshot(tmp_path, 101, version="11.x")
        write_snapshot(tmp_path, 0, version="13.x")

        _, age = get_docs_snapshot_age(tmp_path, "11.x")
        assert age == 101, "asking about 11.x must report 11.x"

    def test_aggregate_reports_the_oldest_version(self, tmp_path):
        """Across versions, trustworthiness is governed by the stalest part."""
        write_snapshot(tmp_path, 90, version="11.x")
        write_snapshot(tmp_path, 3, version="12.x")

        _, age = get_docs_snapshot_age(tmp_path)
        assert age == 90, "the aggregate must not quote the freshest version"

    def test_missing_metadata_is_not_an_error(self, tmp_path):
        assert get_docs_snapshot_age(tmp_path) == (None, None)

    @pytest.mark.parametrize("sync_time", [
        "garbage", "2026-13-45", "", None, 1753900000, 12.5, True,
        {"nested": "object"}, ["list"],
    ])
    def test_malformed_sync_time_is_never_fatal(self, tmp_path, sync_time):
        """Metadata is user-mountable and network-populated; it must never raise."""
        metadata_dir = tmp_path / "12.x" / ".metadata"
        metadata_dir.mkdir(parents=True, exist_ok=True)
        (metadata_dir / "sync_info.json").write_text(json.dumps({"sync_time": sync_time}))
        assert get_docs_snapshot_age(tmp_path) == (None, None)

    def test_metadata_that_is_not_an_object_is_not_fatal(self, tmp_path):
        metadata_dir = tmp_path / "12.x" / ".metadata"
        metadata_dir.mkdir(parents=True)
        (metadata_dir / "sync_info.json").write_text('["not", "an", "object"]')
        assert get_docs_snapshot_age(tmp_path) == (None, None)

    @pytest.mark.parametrize("days_ahead", [1, 2, 365])
    def test_future_timestamps_report_unknown(self, tmp_path, days_ahead):
        """Clock skew must not be presented as freshness.

        Clamping a future age to zero would render the snapshot permanently
        'today' and silently disable the staleness warning.
        """
        write_snapshot(tmp_path, -days_ahead)
        assert get_docs_snapshot_age(tmp_path) == (None, None)
        assert docs_are_stale(tmp_path) is False
        assert "unknown" in describe_docs_freshness(tmp_path)


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
    @pytest.mark.parametrize("value", [
        None, "", "unknown", "not-a-date", "2026-13-45", 1753900000, 12.5, True, {}, [],
    ])
    def test_unparseable_values_return_none(self, value):
        assert parse_sync_time(value) is None

    def test_naive_timestamps_are_treated_as_utc(self):
        parsed = parse_sync_time("2026-07-30T12:00:00")
        assert parsed is not None
        assert parsed.utcoffset() == timedelta(0), "a naive timestamp must be read as UTC"

    def test_zulu_suffix_is_understood(self):
        parsed = parse_sync_time("2026-07-30T12:00:00Z")
        assert parsed == datetime(2026, 7, 30, 12, 0, 0, tzinfo=timezone.utc)

    def test_explicit_offset_is_converted_not_ignored(self):
        """+02:00 is two hours ahead of the same wall-clock time in UTC."""
        offset = parse_sync_time("2026-07-30T12:00:00+02:00")
        utc = parse_sync_time("2026-07-30T12:00:00Z")
        assert offset is not None and utc is not None
        assert offset == utc - timedelta(hours=2)


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

    def test_instructions_report_the_served_version_not_the_freshest(self, tmp_path):
        """The bug this guards: a pinned old version inheriting a newer one's date.

        A user on 11.x whose docs are 101 days old must not be told the corpus
        was synced today because 13.x happens to be current.
        """
        from laravel_mcp_companion import build_server_instructions

        write_snapshot(tmp_path, 101, version="11.x")
        write_snapshot(tmp_path, 0, version="13.x")

        instructions = build_server_instructions(tmp_path, "11.x")

        assert "101 days ago" in instructions
        assert "(today)" not in instructions

    def test_instructions_name_the_default_version_explicitly(self, tmp_path):
        from laravel_mcp_companion import build_server_instructions

        write_snapshot(tmp_path, 1, version="11.x")
        instructions = build_server_instructions(tmp_path, "11.x")

        # The bare string "11.x" also appears in the supported-versions list, so
        # assert the phrase that actually depends on runtime_version.
        assert "default to Laravel 11.x" in instructions

    @pytest.mark.parametrize("mode,expected,forbidden", [
        ("search", "search_tools", "read_laravel_doc_content"),
        (None, "read_laravel_doc_content", "search_tools"),
        ("code", "get_schema", "read_laravel_doc_content"),
    ])
    def test_instructions_describe_the_exposed_tool_surface(self, tmp_path, mode, expected, forbidden):
        """Transforms replace the individual tools, so the described flow must follow.

        Naming hidden tools invites calls the client cannot route.
        """
        from laravel_mcp_companion import build_server_instructions

        write_snapshot(tmp_path, 1)
        instructions = build_server_instructions(tmp_path, "12.x", transform_mode=mode)

        assert expected in instructions
        assert forbidden not in instructions

    def test_instructions_survive_missing_metadata(self, tmp_path):
        from laravel_mcp_companion import build_server_instructions

        instructions = build_server_instructions(tmp_path, "12.x")
        assert "unknown" in instructions

    def test_server_starts_with_corrupt_metadata(self, tmp_path):
        """Instructions are built during server construction, so this must not raise."""
        from laravel_mcp_companion import create_mcp_server

        metadata_dir = tmp_path / "12.x" / ".metadata"
        metadata_dir.mkdir(parents=True)
        (metadata_dir / "sync_info.json").write_text(json.dumps({"sync_time": 1753900000}))

        server = create_mcp_server("Test", tmp_path, "12.x", transform_mode=None)
        assert server is not None
