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

from docs_updater import LearningResourceFetcher
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
        assert fetcher.is_cache_valid("laravel-blog") is False

    def test_fresh_quality_cache_is_valid(self, fetcher):
        write_metadata(fetcher, "laravel-blog")
        assert fetcher.is_cache_valid("laravel-blog") is True

    def test_low_success_rate_invalidates(self, fetcher):
        write_metadata(fetcher, "laravel-blog", success_rate=0.69)
        assert fetcher.is_cache_valid("laravel-blog") is False

    def test_threshold_is_point_seven(self, fetcher):
        write_metadata(fetcher, "laravel-blog", success_rate=0.7)
        assert fetcher.is_cache_valid("laravel-blog") is True

    def test_expired_cache_is_invalid(self, fetcher):
        write_metadata(fetcher, "laravel-blog", cached_at=time.time() - 86401)
        assert fetcher.is_cache_valid("laravel-blog") is False

    def test_corrupt_metadata_is_invalid(self, fetcher):
        fetcher.get_cache_metadata_path("laravel-blog").write_text("{not json")
        assert fetcher.is_cache_valid("laravel-blog") is False

    def test_save_stamps_cached_at(self, fetcher):
        fetcher.save_cache_metadata("laravel-blog", {"success_rate": 1.0})
        saved = json.loads(fetcher.get_cache_metadata_path("laravel-blog").read_text())
        assert saved["cached_at"] == pytest.approx(time.time(), abs=5)


class TestFetchLearningSource:
    def test_unknown_source_returns_false(self, fetcher):
        assert fetcher.fetch_learning_source("not-a-source") is False

    def test_fresh_cache_short_circuits_without_network(self, fetcher, monkeypatch):
        write_metadata(fetcher, "laravel-blog")

        def explode(*a, **k):
            raise AssertionError("network hit despite valid cache")

        monkeypatch.setattr("docs_updater.urllib.request.urlopen", explode)
        assert fetcher.fetch_learning_source("laravel-blog") is True

    def test_force_bypasses_cache(self, fetcher, monkeypatch):
        write_metadata(fetcher, "laravel-blog")
        monkeypatch.setattr(
            "docs_updater.urllib.request.urlopen",
            urlopen_returning(load_fixture("blog_index.html").encode()),
        )
        assert fetcher.fetch_learning_source("laravel-blog", force=True) is True

    def test_fetch_exception_returns_false(self, fetcher, monkeypatch):
        def explode(*a, **k):
            raise OSError("socket down")

        monkeypatch.setattr("docs_updater.urllib.request.urlopen", explode)
        monkeypatch.setattr("docs_updater.time.sleep", lambda s: None)
        assert fetcher.fetch_learning_source("laravel-blog") is False


class TestBlogAndNewsIndexes:
    def test_blog_index_written_from_recorded_page(self, fetcher, monkeypatch):
        monkeypatch.setattr(
            "docs_updater.urllib.request.urlopen",
            urlopen_returning(load_fixture("blog_index.html").encode()),
        )
        assert fetcher._fetch_blog_index(fetcher.learning_sources["laravel-blog"]) is True

        index = (fetcher.get_source_cache_path("laravel-blog") / "index.md").read_text()
        assert index.startswith("# Laravel Blog - Recent Articles")
        assert "## " in index  # at least one extracted article heading
        meta = json.loads(fetcher.get_cache_metadata_path("laravel-blog").read_text())
        assert meta["success_rate"] == 1.0
        assert meta["article_count"] > 0
        assert "cached_at" in meta
        assert fetcher.is_cache_valid("laravel-blog") is True

    def test_news_index_written_from_recorded_page(self, fetcher, monkeypatch):
        monkeypatch.setattr(
            "docs_updater.urllib.request.urlopen",
            urlopen_returning(load_fixture("news_index.html").encode()),
        )
        assert fetcher._fetch_news_index(fetcher.learning_sources["laravel-news"]) is True
        index = (fetcher.get_source_cache_path("laravel-news") / "index.md").read_text()
        assert index.startswith("# Laravel News - Recent Articles")
        assert "[Read more](https://laravel-news.com" in index

    def test_laracasts_extraction_finds_nothing_on_current_page(self, fetcher, monkeypatch):
        """Pins real drift: the live topics page no longer matches the
        extractor's selectors, so the fetch degrades to False and writes
        nothing. If this test starts failing with True, the site (or the
        extractor) changed — update the fixture and these assertions."""
        monkeypatch.setattr(
            "docs_updater.urllib.request.urlopen",
            urlopen_returning(load_fixture("laracasts_index.html").encode()),
        )
        config = fetcher.learning_sources["laracasts-index"]
        assert fetcher._fetch_laracasts_metadata(config) is False
        assert not (fetcher.get_source_cache_path("laracasts-index") / "topics.md").exists()

    def test_blog_index_returns_false_on_unrecognized_page(self, fetcher, monkeypatch):
        monkeypatch.setattr(
            "docs_updater.urllib.request.urlopen",
            urlopen_returning(load_fixture("moved_structure.html").encode()),
        )
        assert fetcher._fetch_blog_index(fetcher.learning_sources["laravel-blog"]) is False


class TestExtractors:
    def test_blog_articles_extracted_with_expected_keys(self, fetcher):
        articles = fetcher._extract_blog_articles(load_fixture("blog_index.html"))
        assert articles
        assert set(articles[0]) >= {"title", "url"}

    def test_news_articles_extracted(self, fetcher):
        from urllib.parse import urlparse

        articles = fetcher._extract_news_articles(load_fixture("news_index.html"))
        assert articles
        parsed = urlparse(articles[0]["url"])
        assert parsed.scheme == "https"
        assert parsed.hostname == "laravel-news.com"

    @pytest.mark.parametrize("method", [
        "_extract_blog_articles", "_extract_news_articles", "_extract_laracasts_topics",
    ])
    def test_extractors_return_empty_on_moved_structure(self, fetcher, method):
        assert getattr(fetcher, method)(load_fixture("moved_structure.html")) == []


class TestBootcampFetch:
    def test_partial_success_records_honest_success_rate(self, fetcher, monkeypatch):
        config = dict(fetcher.learning_sources["laravel-bootcamp"])
        config["sections"] = ["introduction", "installation"]
        # introduction hits base_url, installation hits /blade/installation
        monkeypatch.setattr(
            "docs_updater.urllib.request.urlopen",
            urlopen_returning(b"", url_map={
                "/blade/installation": load_fixture("moved_structure.html").encode(),
                "bootcamp.laravel.com": GOOD_PAGE.encode(),
            }),
        )
        assert fetcher._fetch_bootcamp_docs(config) is True
        meta = json.loads(fetcher.get_cache_metadata_path("laravel-bootcamp").read_text())
        assert meta["success_rate"] == 0.5
        # 0.5 < 0.7 quality floor: the cache it just wrote is already invalid,
        # so the next fetch retries rather than serving the half-empty copy.
        assert fetcher.is_cache_valid("laravel-bootcamp") is False

    def test_total_failure_returns_false(self, fetcher, monkeypatch):
        config = dict(fetcher.learning_sources["laravel-bootcamp"])
        config["sections"] = ["introduction"]
        monkeypatch.setattr(
            "docs_updater.urllib.request.urlopen",
            urlopen_returning(load_fixture("moved_structure.html").encode()),
        )
        assert fetcher._fetch_bootcamp_docs(config) is False


class TestFetchAndProcessHtml:
    def test_good_page_becomes_markdown(self, fetcher, monkeypatch):
        monkeypatch.setattr(
            "docs_updater.urllib.request.urlopen",
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
            "docs_updater.urllib.request.urlopen",
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

        monkeypatch.setattr("docs_updater.urllib.request.urlopen", raise_404)
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

        monkeypatch.setattr("docs_updater.urllib.request.urlopen", flaky)
        monkeypatch.setattr("docs_updater.time.sleep", sleeps.append)
        monkeypatch.setattr("docs_updater.random.uniform", lambda a, b: 0)
        assert fetcher._retry_request("https://x.test/flaky") == b"payload"
        # 2**attempt with no cap: attempt 0 -> 1s, attempt 1 -> 2s
        assert sleeps == [1, 2]

    def test_exhaustion_raises_last_error(self, fetcher, monkeypatch):
        monkeypatch.setattr(
            "docs_updater.urllib.request.urlopen",
            lambda *a, **k: (_ for _ in ()).throw(self._http_error(500)),
        )
        monkeypatch.setattr("docs_updater.time.sleep", lambda s: None)
        with pytest.raises(urllib.error.HTTPError):
            fetcher._retry_request("https://x.test/dead")
