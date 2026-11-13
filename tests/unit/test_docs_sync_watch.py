"""The alarm for a documentation sync that has stopped running.

Twice the nightly sync died without creating a run: once when the account's
build allowance ran out, once when Harness rejected a pipeline file. A run
that never starts sends no failure email, and the first outage lasted five
weeks. The sync tags `docs-YYYY-MM-DD` whenever it publishes, so the age of the
newest such tag is evidence anyone can read without access to the build
system.
"""

import importlib.util
from datetime import date
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "docs_sync_watch.py"
spec = importlib.util.spec_from_file_location("docs_sync_watch", SCRIPT)
assert spec is not None and spec.loader is not None
watch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(watch)

TODAY = date(2026, 11, 20)


class TestNewestSync:
    def test_the_newest_date_among_the_tags_is_used(self):
        tags = ["docs-2026-11-12", "docs-2026-11-18", "docs-2026-11-13"]

        assert watch.newest_sync(tags) == date(2026, 11, 18)

    def test_a_second_sync_on_one_day_counts_as_that_day(self):
        assert watch.newest_sync(["docs-2026-11-12", "docs-2026-11-12-1210"]) == date(2026, 11, 12)

    def test_version_tags_and_malformed_names_are_ignored(self):
        assert watch.newest_sync(["v0.14.0", "docs-latest", "docs-2026-13-45", "docs-2026-11-10"]) == date(2026, 11, 10)

    def test_no_docs_tag_at_all_is_reported_as_none(self):
        assert watch.newest_sync(["v0.14.0"]) is None


class TestVerdict:
    def test_a_sync_from_yesterday_is_healthy(self):
        stale, message = watch.verdict(["docs-2026-11-19"], TODAY)

        assert stale is False
        assert "1 day ago" in message

    def test_a_quiet_stretch_within_the_allowance_is_healthy(self):
        """A night with no upstream changes publishes nothing, so a few days
        without a tag is normal."""
        stale, _ = watch.verdict(["docs-2026-11-16"], TODAY)

        assert stale is False

    def test_a_gap_longer_than_the_allowance_is_stale(self):
        stale, message = watch.verdict(["docs-2026-11-15"], TODAY)

        assert stale is True
        assert "5 days" in message and "2026-11-15" in message

    def test_no_docs_tag_is_stale(self):
        stale, message = watch.verdict(["v0.14.0"], TODAY)

        assert stale is True
        assert "no docs tag" in message.lower()
