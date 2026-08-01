"""Currency reporting reflects when Laravel changed its documentation.

The previous implementation measured when this project last fetched a change.
For a branch that no longer changes that recedes forever, so five of eight
shipped versions were reported stale while byte-identical to upstream.
"""

import json
import time
from datetime import datetime, timedelta, timezone

import pytest

from mcp_tools import (
    DOCS_STALE_AFTER_DAYS,
    copy_is_stale,
    describe_documentation_date,
    get_documentation_date,
    parse_timestamp,
)


def write_metadata(docs_path, version, changed_days_ago, fetched_days_ago=None):
    """Write metadata for a version, separating change date from fetch date."""
    if fetched_days_ago is None:
        fetched_days_ago = changed_days_ago
    metadata_dir = docs_path / version / ".metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    (metadata_dir / "sync_info.json").write_text(json.dumps({
        "version": version,
        "sync_time": time.strftime(fmt, time.gmtime(time.time() - fetched_days_ago * 86400)),
        "commit_date": time.strftime(fmt, time.gmtime(time.time() - changed_days_ago * 86400)),
        "commit_sha": "abc1234",
    }))


class TestDocumentationDate:
    def test_reports_when_the_documentation_changed_not_when_it_was_fetched(self, tmp_path):
        """The distinction the whole change rests on."""
        write_metadata(tmp_path, "13.x", changed_days_ago=400, fetched_days_ago=1)

        _, age = get_documentation_date(tmp_path, "13.x")

        assert age == 400

    @pytest.mark.parametrize("days", [0, 1, 30, 425])
    def test_reports_age_in_days(self, tmp_path, days):
        write_metadata(tmp_path, "13.x", changed_days_ago=days)
        _, age = get_documentation_date(tmp_path, "13.x")
        assert age == days

    def test_across_versions_reports_the_newest(self, tmp_path):
        """The newest change is a proxy for how old this copy is."""
        write_metadata(tmp_path, "8.x", changed_days_ago=425)
        write_metadata(tmp_path, "13.x", changed_days_ago=1)

        _, age = get_documentation_date(tmp_path)

        assert age == 1, "must report the newest, not the oldest"

    def test_missing_metadata_is_not_an_error(self, tmp_path):
        assert get_documentation_date(tmp_path) == (None, None)

    @pytest.mark.parametrize("bad", ["garbage", "", None, 1753900000, {"a": 1}, ["x"]])
    def test_malformed_commit_date_is_never_fatal(self, tmp_path, bad):
        metadata_dir = tmp_path / "13.x" / ".metadata"
        metadata_dir.mkdir(parents=True, exist_ok=True)
        (metadata_dir / "sync_info.json").write_text(json.dumps({"commit_date": bad}))
        assert get_documentation_date(tmp_path) == (None, None)

    def test_metadata_that_is_not_an_object_is_not_fatal(self, tmp_path):
        metadata_dir = tmp_path / "13.x" / ".metadata"
        metadata_dir.mkdir(parents=True)
        (metadata_dir / "sync_info.json").write_text('["not", "an", "object"]')
        assert get_documentation_date(tmp_path) == (None, None)

    def test_future_dates_report_unknown(self, tmp_path):
        """Clock skew must not be presented as freshness."""
        write_metadata(tmp_path, "13.x", changed_days_ago=-5)
        assert get_documentation_date(tmp_path) == (None, None)
        assert copy_is_stale(tmp_path) is False
        assert "unknown" in describe_documentation_date(tmp_path)


class TestStaleness:
    def test_end_of_life_version_is_not_stale(self, tmp_path):
        """The regression this change exists to fix.

        8.x last changed 425 days ago and is byte-identical to upstream. It is
        not stale; upstream simply stopped.
        """
        write_metadata(tmp_path, "8.x", changed_days_ago=425)
        write_metadata(tmp_path, "13.x", changed_days_ago=1)

        assert copy_is_stale(tmp_path) is False

    def test_stale_when_every_version_is_old(self, tmp_path):
        """A months-old image: even the active version stopped changing."""
        write_metadata(tmp_path, "8.x", changed_days_ago=425)
        write_metadata(tmp_path, "13.x", changed_days_ago=DOCS_STALE_AFTER_DAYS + 1)

        assert copy_is_stale(tmp_path) is True

    def test_not_stale_at_the_threshold(self, tmp_path):
        write_metadata(tmp_path, "13.x", changed_days_ago=DOCS_STALE_AFTER_DAYS)
        assert copy_is_stale(tmp_path) is False

    def test_unknown_age_is_not_stale(self, tmp_path):
        assert copy_is_stale(tmp_path) is False


class TestDescription:
    def test_returns_a_bare_date(self, tmp_path):
        """No age phrasing: '425 days ago' reintroduces the alarm being removed."""
        write_metadata(tmp_path, "8.x", changed_days_ago=425)

        described = describe_documentation_date(tmp_path, "8.x")

        assert "days ago" not in described
        assert "today" not in described
        assert described.count("-") == 2, f"expected a bare date, got {described!r}"

    def test_unknown_when_no_metadata(self, tmp_path):
        assert "unknown" in describe_documentation_date(tmp_path, "13.x")


class TestParseTimestamp:
    @pytest.mark.parametrize("value", [None, "", "unknown", "not-a-date", 17539, {}, []])
    def test_unparseable_values_return_none(self, value):
        assert parse_timestamp(value) is None

    def test_naive_timestamps_are_treated_as_utc(self):
        parsed = parse_timestamp("2026-07-30T12:00:00")
        assert parsed is not None
        assert parsed.utcoffset() == timedelta(0), "a naive timestamp must be read as UTC"

    def test_zulu_suffix_is_understood(self):
        parsed = parse_timestamp("2026-07-30T12:00:00Z")
        assert parsed == datetime(2026, 7, 30, 12, 0, 0, tzinfo=timezone.utc)

    def test_explicit_offset_is_converted_not_ignored(self):
        """+02:00 is two hours ahead of the same wall-clock time in UTC."""
        offset = parse_timestamp("2026-07-30T12:00:00+02:00")
        utc = parse_timestamp("2026-07-30T12:00:00Z")
        assert offset is not None and utc is not None
        assert offset == utc - timedelta(hours=2)


class TestServerInstructions:
    def test_instructions_state_the_documentation_date(self, tmp_path):
        from laravel_mcp_companion import build_server_instructions

        write_metadata(tmp_path, "13.x", changed_days_ago=2)
        instructions = build_server_instructions(tmp_path, "13.x")

        assert "reflects Laravel's documentation as of" in instructions

    def test_instructions_do_not_call_an_eol_version_stale(self, tmp_path):
        """8.x is byte-identical to upstream; the model must not be told to refresh."""
        from laravel_mcp_companion import build_server_instructions

        write_metadata(tmp_path, "8.x", changed_days_ago=425)
        instructions = build_server_instructions(tmp_path, "8.x")

        assert "425 days ago" not in instructions
        assert "stale" not in instructions.lower()

    def test_instructions_report_the_served_version(self, tmp_path):
        from laravel_mcp_companion import build_server_instructions

        write_metadata(tmp_path, "8.x", changed_days_ago=425)
        write_metadata(tmp_path, "13.x", changed_days_ago=0)

        instructions = build_server_instructions(tmp_path, "8.x")
        eight, _ = get_documentation_date(tmp_path, "8.x")

        assert eight in instructions

    def test_instructions_name_the_default_version_explicitly(self, tmp_path):
        from laravel_mcp_companion import build_server_instructions

        write_metadata(tmp_path, "11.x", changed_days_ago=1)
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

        write_metadata(tmp_path, "13.x", changed_days_ago=1)
        instructions = build_server_instructions(tmp_path, "13.x", transform_mode=mode)

        assert expected in instructions
        assert forbidden not in instructions

    def test_instructions_survive_missing_metadata(self, tmp_path):
        from laravel_mcp_companion import build_server_instructions

        assert "unknown" in build_server_instructions(tmp_path, "13.x")

    def test_server_starts_with_corrupt_metadata(self, tmp_path):
        """Instructions are built during server construction, so this must not raise."""
        from laravel_mcp_companion import create_mcp_server

        metadata_dir = tmp_path / "13.x" / ".metadata"
        metadata_dir.mkdir(parents=True)
        (metadata_dir / "sync_info.json").write_text(json.dumps({"commit_date": 1753900000}))

        server = create_mcp_server("Test", tmp_path, "13.x", transform_mode=None)
        assert server is not None


class TestDocsInfoTool:
    @pytest.mark.asyncio
    async def test_summary_does_not_warn_when_the_copy_is_current(self, tmp_path):
        """The permanent-warning bug: 6.x can never get fresher."""
        from fastmcp import Client

        from laravel_mcp_companion import create_mcp_server

        write_metadata(tmp_path, "6.x", changed_days_ago=425)
        write_metadata(tmp_path, "13.x", changed_days_ago=1)

        server = create_mcp_server("T", tmp_path, "13.x", transform_mode=None)
        async with Client(server) as client:
            result = await client.call_tool("laravel_docs_info", {})
            text = result.content[0].text

        assert "note" not in text, f"warned about a current copy: {text}"
        assert "documentation_current_to" in text

    @pytest.mark.asyncio
    async def test_summary_warns_when_the_whole_copy_is_old(self, tmp_path):
        from fastmcp import Client

        from laravel_mcp_companion import create_mcp_server

        write_metadata(tmp_path, "6.x", changed_days_ago=425)
        write_metadata(tmp_path, "13.x", changed_days_ago=DOCS_STALE_AFTER_DAYS + 5)

        server = create_mcp_server("T", tmp_path, "13.x", transform_mode=None)
        async with Client(server) as client:
            result = await client.call_tool("laravel_docs_info", {})
            text = result.content[0].text

        assert "note" in text
        assert "pull" in text.lower(), "should advise pulling a newer image"
        assert "update_laravel_docs" not in text, "that tool cannot fix a stale image"

    @pytest.mark.asyncio
    async def test_per_version_reports_a_date_and_never_warns(self, tmp_path):
        from fastmcp import Client

        from laravel_mcp_companion import create_mcp_server

        write_metadata(tmp_path, "8.x", changed_days_ago=425)

        server = create_mcp_server("T", tmp_path, "8.x", transform_mode=None)
        async with Client(server) as client:
            result = await client.call_tool("laravel_docs_info", {"version": "8.x"})
            text = result.content[0].text

        assert "documentation_date" in text
        assert "note" not in text, "a version whose upstream stopped is not a problem"


class TestUpdateToolParameterName:
    @pytest.mark.asyncio
    async def test_accepts_the_parameter_name_every_other_tool_uses(self, tmp_path):
        """An assistant told to refresh guesses `version`; it used to hard-error."""
        from fastmcp import Client

        from laravel_mcp_companion import create_mcp_server

        write_metadata(tmp_path, "13.x", changed_days_ago=1)
        server = create_mcp_server("T", tmp_path, "13.x", transform_mode=None)

        async with Client(server) as client:
            tools = {t.name: t for t in await client.list_tools()}
            schema = tools["update_laravel_docs"].inputSchema

        assert "version" in schema["properties"]
        assert "version_param" not in schema["properties"]
