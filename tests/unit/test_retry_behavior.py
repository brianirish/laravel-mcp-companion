"""Backoff branch matrix for the retry implementations (docs_updater.py).

Four independent retry loops live in this module and their backoff branches
were almost entirely uncovered. Sleeps and jitter are patched so tests assert
exact wait sequences; the happy paths are covered elsewhere.
"""

import json
import urllib.error
from unittest.mock import MagicMock

import pytest

from docs_updater import DocsUpdater, DocumentationAutoDiscovery, ExternalDocsFetcher


def http_error(code, reason="err"):
    return urllib.error.HTTPError("https://x.test", code, reason, {}, None)


def ok_response(body: bytes):
    response = MagicMock()
    response.read.return_value = body
    cm = MagicMock()
    cm.__enter__.return_value = response
    cm.__exit__.return_value = False
    return cm


@pytest.fixture
def sleeps(monkeypatch):
    recorded = []
    monkeypatch.setattr("docs_updater.time.sleep", recorded.append)
    monkeypatch.setattr("docs_updater.random.uniform", lambda a, b: 0)
    return recorded


@pytest.fixture
def external(temp_dir):
    return ExternalDocsFetcher(temp_dir)


class TestExternalRetryRequest:
    def test_rate_limit_backs_off_with_5x_multiplier(self, external, sleeps, monkeypatch):
        attempts = []

        def flaky(request, *a, **k):
            attempts.append(1)
            if len(attempts) < 3:
                raise http_error(403, "API rate limit exceeded")
            return ok_response(b"done")

        monkeypatch.setattr("docs_updater.urllib.request.urlopen", flaky)
        assert external._retry_request("https://x.test") == b"done"
        # min(300, 2**attempt * 5): attempt 0 -> 5, attempt 1 -> 10
        assert sleeps == [5, 10]

    def test_plain_403_raises_immediately(self, external, sleeps, monkeypatch):
        monkeypatch.setattr(
            "docs_updater.urllib.request.urlopen",
            lambda *a, **k: (_ for _ in ()).throw(http_error(403, "Forbidden")),
        )
        with pytest.raises(urllib.error.HTTPError):
            external._retry_request("https://x.test")
        assert sleeps == []

    def test_rate_limit_exhaustion_raises_via_fallthrough(self, external, sleeps, monkeypatch):
        """The rate-limit branch never checks attempt < retries: it sleeps on
        the final attempt too and exhausts through the bottom
        `raise last_exception` (:1464) rather than an in-branch raise."""
        monkeypatch.setattr(
            "docs_updater.urllib.request.urlopen",
            lambda *a, **k: (_ for _ in ()).throw(http_error(403, "rate limit hit")),
        )
        with pytest.raises(urllib.error.HTTPError):
            external._retry_request("https://x.test", max_retries=1)
        assert len(sleeps) == 2  # slept even on the final attempt

    def test_url_error_retries_then_raises(self, external, sleeps, monkeypatch):
        monkeypatch.setattr(
            "docs_updater.urllib.request.urlopen",
            lambda *a, **k: (_ for _ in ()).throw(urllib.error.URLError("dns down")),
        )
        with pytest.raises(urllib.error.URLError):
            external._retry_request("https://x.test", max_retries=2)
        # min(30, 2**attempt): attempts 0,1 sleep; final attempt raises
        assert sleeps == [1, 2]

    def test_generic_exception_retries(self, external, sleeps, monkeypatch):
        attempts = []

        def flaky(request, *a, **k):
            attempts.append(1)
            if len(attempts) == 1:
                raise ValueError("weird payload")
            return ok_response(b"ok")

        monkeypatch.setattr("docs_updater.urllib.request.urlopen", flaky)
        assert external._retry_request("https://x.test") == b"ok"
        assert sleeps == [1]

    def test_max_retries_zero_means_single_attempt(self, external, sleeps, monkeypatch):
        attempts = []

        def count(*a, **k):
            attempts.append(1)
            raise urllib.error.URLError("down")

        monkeypatch.setattr("docs_updater.urllib.request.urlopen", count)
        with pytest.raises(urllib.error.URLError):
            external._retry_request("https://x.test", max_retries=0)
        assert len(attempts) == 1
        assert sleeps == []


class TestGetLatestCommitRetries:
    @pytest.fixture
    def updater(self, test_docs_dir):
        return DocsUpdater(test_docs_dir, "12.x")

    def test_rate_limit_backoff_is_exact_no_jitter(self, updater, sleeps, monkeypatch):
        attempts = []
        good = json.dumps({
            "commit": {
                "sha": "abc", "html_url": "https://x",
                "commit": {"committer": {"date": "2026-01-01"}, "message": "m"},
            }
        }).encode()

        def flaky(request, *a, **k):
            attempts.append(1)
            if len(attempts) < 3:
                raise http_error(403, "API rate limit exceeded for 1.2.3.4")
            return ok_response(good)

        monkeypatch.setattr("docs_updater.urllib.request.urlopen", flaky)
        commit = updater.get_latest_commit()
        assert commit["sha"] == "abc"
        # min(300, 2**attempt * 30), no jitter term: 30, then 60 exactly
        assert sleeps == [30, 60]

    def test_rate_limit_exhaustion_raises(self, updater, sleeps, monkeypatch):
        monkeypatch.setattr(
            "docs_updater.urllib.request.urlopen",
            lambda *a, **k: (_ for _ in ()).throw(http_error(403, "rate limit")),
        )
        with pytest.raises(urllib.error.HTTPError):
            updater.get_latest_commit(max_retries=1)

    def test_5xx_retries_then_succeeds(self, updater, sleeps, monkeypatch):
        attempts = []
        good = json.dumps({
            "commit": {
                "sha": "def", "html_url": "https://x",
                "commit": {"committer": {"date": "2026-01-01"}, "message": "m"},
            }
        }).encode()

        def flaky(request, *a, **k):
            attempts.append(1)
            if len(attempts) == 1:
                raise http_error(502)
            return ok_response(good)

        monkeypatch.setattr("docs_updater.urllib.request.urlopen", flaky)
        assert updater.get_latest_commit()["sha"] == "def"
        assert sleeps == [1]

    def test_malformed_json_retries_then_raises_keyerror(self, updater, sleeps, monkeypatch):
        """A response missing the expected keys is caught by the generic
        retry branch, retried, and finally raises KeyError to the caller —
        which needs_update() then swallows into 'needs update'."""
        monkeypatch.setattr(
            "docs_updater.urllib.request.urlopen",
            lambda *a, **k: ok_response(b'{"unexpected": "shape"}'),
        )
        with pytest.raises(KeyError):
            updater.get_latest_commit(max_retries=1)
        assert len(sleeps) == 1

        assert updater.needs_update() is True


class TestAutoDiscoveryCourtesyDelay:
    def test_pre_attempt_courtesy_sleep_on_retries_only(self, sleeps, monkeypatch):
        discovery = DocumentationAutoDiscovery(max_retries=2, request_delay=1.5)
        attempts = []

        def flaky(request, *a, **k):
            attempts.append(1)
            if len(attempts) < 2:
                raise ValueError("hiccup")
            return ok_response(b"page")

        monkeypatch.setattr("docs_updater.urllib.request.urlopen", flaky)
        assert discovery._retry_request("https://x.test") == b"page"
        # attempt 0: no courtesy delay; failure sleeps min(30, 2**0)=1;
        # attempt 1: courtesy delay request_delay * 2**(1-1) = 1.5
        assert sleeps == [1, 1.5]
