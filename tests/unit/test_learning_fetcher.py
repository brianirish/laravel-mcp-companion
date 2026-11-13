"""LearningResourceFetcher tests (docs_updater.py).

This class had zero coverage. Tests run against recorded pages in
tests/fixtures/ — no live network. Where the recorded page no longer matches
the extractor's expectations (Laracasts), the test pins the degraded behavior
rather than pretending the extraction works.
"""

import json
import time
import urllib.error

import pytest

from laravel_mcp_companion.docs_updater import LearningResourceFetcher
from tests.conftest import load_fixture, urlopen_returning

GOOD_PAGE = """
<html><body><main>
<h1>Install Laravel</h1>
<p>To get started, create a new application. This paragraph is long enough to
clear the hundred-character floor the fetcher enforces for useful content, and
then some.</p>
<script>tracking()</script>
</main></body></html>
"""


@pytest.fixture
def fetcher(temp_dir):
    return LearningResourceFetcher(temp_dir)


def write_metadata(fetcher, source, **overrides):
    meta = {"source": source, "success_rate": 1.0, "cached_at": time.time()}
    meta.update(overrides)
    fetcher.get_cache_metadata_path(source).write_text(json.dumps(meta))
    return meta


class TestCacheValidity:
    def test_missing_metadata_is_invalid(self, fetcher):
        assert fetcher.is_cache_valid("laracasts-index") is False

    def test_fresh_quality_cache_is_valid(self, fetcher):
        write_metadata(fetcher, "laracasts-index")
        assert fetcher.is_cache_valid("laracasts-index") is True

    def test_low_success_rate_invalidates(self, fetcher):
        write_metadata(fetcher, "laracasts-index", success_rate=0.69)
        assert fetcher.is_cache_valid("laracasts-index") is False

    def test_threshold_is_point_seven(self, fetcher):
        write_metadata(fetcher, "laracasts-index", success_rate=0.7)
        assert fetcher.is_cache_valid("laracasts-index") is True

    def test_expired_cache_is_invalid(self, fetcher):
        write_metadata(fetcher, "laracasts-index", cached_at=time.time() - 86401)
        assert fetcher.is_cache_valid("laracasts-index") is False

    def test_corrupt_metadata_is_invalid(self, fetcher):
        fetcher.get_cache_metadata_path("laracasts-index").write_text("{not json")
        assert fetcher.is_cache_valid("laracasts-index") is False

    def test_save_stamps_cached_at(self, fetcher):
        fetcher.save_cache_metadata("laracasts-index", {"success_rate": 1.0})
        saved = json.loads(fetcher.get_cache_metadata_path("laracasts-index").read_text())
        assert saved["cached_at"] == pytest.approx(time.time(), abs=5)


class TestFetchLearningSource:
    def test_unknown_source_returns_false(self, fetcher):
        assert fetcher.fetch_learning_source("not-a-source") is False

    def test_fresh_cache_short_circuits_without_network(self, fetcher, monkeypatch):
        write_metadata(fetcher, "laracasts-index")

        def explode(*a, **k):
            raise AssertionError("network hit despite valid cache")

        monkeypatch.setattr("laravel_mcp_companion.docs_updater.urllib.request.urlopen", explode)
        assert fetcher.fetch_learning_source("laracasts-index") is True

    def test_force_bypasses_cache(self, fetcher, monkeypatch):
        write_metadata(fetcher, "laracasts-index")
        monkeypatch.setattr(
            "laravel_mcp_companion.docs_updater.urllib.request.urlopen",
            urlopen_returning(load_fixture("laracasts_index.html").encode()),
        )
        assert fetcher.fetch_learning_source("laracasts-index", force=True) is True

    def test_fetch_exception_returns_false(self, fetcher, monkeypatch):
        def explode(*a, **k):
            raise OSError("socket down")

        monkeypatch.setattr("laravel_mcp_companion.docs_updater.urllib.request.urlopen", explode)
        monkeypatch.setattr("laravel_mcp_companion.docs_updater.time.sleep", lambda s: None)
        assert fetcher.fetch_learning_source("laracasts-index") is False


class TestLaracastsIndex:
    def test_laracasts_topics_extracted_from_spa_payload(self, fetcher, monkeypatch):
        """The 2026 page is an SPA: topics live in an embedded JSON array.
        (This test previously pinned the drift — extraction finding nothing —
        until the extractor learned the JSON shape.)"""
        monkeypatch.setattr(
            "laravel_mcp_companion.docs_updater.urllib.request.urlopen",
            urlopen_returning(load_fixture("laracasts_index.html").encode()),
        )
        config = fetcher.learning_sources["laracasts-index"]
        assert fetcher._fetch_laracasts_metadata(config) is True

        topics_md = (fetcher.get_source_cache_path("laracasts-index") / "topics.md").read_text()
        assert "# Laracasts - Topic Index" in topics_md
        assert "## Laravel" in topics_md
        assert "series available" in topics_md
        assert "https://laracasts.com/series?topics[]=laravel" in topics_md

    def test_laracasts_json_extractor_shapes(self, fetcher):
        topics = fetcher._extract_laracasts_topics(load_fixture("laracasts_index.html"))
        assert len(topics) >= 10
        laravel = next(t for t in topics if t["name"] == "Laravel")
        assert laravel["series_count"] > 0
        assert laravel["url"].startswith("https://laracasts.com/")

class TestExtractors:
    def test_laracasts_extractor_returns_empty_on_moved_structure(self, fetcher):
        assert fetcher._extract_laracasts_topics(load_fixture("moved_structure.html")) == []


class TestBootcampFetch:
    def test_total_failure_returns_false(self, fetcher, monkeypatch):
        # Course discovery, partial syncs and pruning: test_learning_sources.py.
        config = dict(fetcher.learning_sources["laravel-bootcamp"])
        monkeypatch.setattr(
            "laravel_mcp_companion.docs_updater.urllib.request.urlopen",
            urlopen_returning(load_fixture("moved_structure.html").encode()),
        )
        assert fetcher._fetch_bootcamp_docs(config) is False


class TestFetchAndProcessHtml:
    def test_good_page_becomes_markdown(self, fetcher, monkeypatch):
        monkeypatch.setattr(
            "laravel_mcp_companion.docs_updater.urllib.request.urlopen",
            urlopen_returning(GOOD_PAGE.encode()),
        )
        result = fetcher._fetch_and_process_html("https://x.test/p", "laravel-bootcamp", "introduction")
        assert result is not None
        # This converter doesn't pass heading_style, so markdownify emits
        # setext headings ("Install Laravel\n====="), unlike _html_to_text.
        assert "Install Laravel" in result
        assert result.startswith("# Laravel Bootcamp - Introduction")
        assert "tracking()" not in result  # scripts decomposed

    def test_thin_page_returns_none(self, fetcher, monkeypatch):
        monkeypatch.setattr(
            "laravel_mcp_companion.docs_updater.urllib.request.urlopen",
            urlopen_returning(load_fixture("moved_structure.html").encode()),
        )
        assert fetcher._fetch_and_process_html("https://x.test/p", "s", "sec") is None


class TestRetryRequest:
    def _http_error(self, code, msg="err"):
        return urllib.error.HTTPError("https://x.test", code, msg, {}, None)

    def test_404_raises_immediately(self, fetcher, monkeypatch):
        calls = []

        def raise_404(*a, **k):
            calls.append(1)
            raise self._http_error(404)

        monkeypatch.setattr("laravel_mcp_companion.docs_updater.urllib.request.urlopen", raise_404)
        with pytest.raises(urllib.error.HTTPError):
            fetcher._retry_request("https://x.test/gone")
        assert len(calls) == 1

    def test_5xx_retries_with_uncapped_backoff_then_succeeds(self, fetcher, monkeypatch):
        sleeps = []
        attempts = []

        def flaky(request, *a, **k):
            attempts.append(1)
            if len(attempts) < 3:
                raise self._http_error(503)
            return urlopen_returning(b"payload")(request)

        monkeypatch.setattr("laravel_mcp_companion.docs_updater.urllib.request.urlopen", flaky)
        monkeypatch.setattr("laravel_mcp_companion.docs_updater.time.sleep", sleeps.append)
        monkeypatch.setattr("laravel_mcp_companion.docs_updater.random.uniform", lambda a, b: 0)
        assert fetcher._retry_request("https://x.test/flaky") == b"payload"
        # 2**attempt with no cap: attempt 0 -> 1s, attempt 1 -> 2s
        assert sleeps == [1, 2]

    def test_exhaustion_raises_last_error(self, fetcher, monkeypatch):
        monkeypatch.setattr(
            "laravel_mcp_companion.docs_updater.urllib.request.urlopen",
            lambda *a, **k: (_ for _ in ()).throw(self._http_error(500)),
        )
        monkeypatch.setattr("laravel_mcp_companion.docs_updater.time.sleep", lambda s: None)
        with pytest.raises(urllib.error.HTTPError):
            fetcher._retry_request("https://x.test/dead")
