"""Cache validity contracts across the three fetcher families.

The headline test pins the bug this file was created for: a real external
fetch never produced a valid cache, because nothing stamped `cached_at` —
`is_cache_valid` read `.get('cached_at', 0)` and compared age-since-epoch
against a 24-hour budget, so every request refetched and `cache_duration`
was decorative.
"""

import json
import os
import time
from unittest.mock import Mock, patch

import pytest

from docs_updater import (
    CommunityPackageFetcher,
    ExternalDocsFetcher,
    _read_versions_cache,
    _write_versions_cache,
)


@pytest.fixture
def fetcher(temp_dir):
    return ExternalDocsFetcher(temp_dir)


class TestExternalCacheStampsItsOwnValidity:
    def test_service_fetch_produces_a_valid_cache(self, fetcher):
        """After a successful fetch, the cache must be valid — this is the
        entire point of cache_duration."""
        config = {
            "name": "Forge",
            "base_url": "https://forge.laravel.com/docs",
            "auto_discovery": False,
            "sections": ["introduction"],
        }
        page = "<html><body><main>" + "Real documentation content. " * 20 + "</main></body></html>"
        with patch.object(fetcher, "_retry_request", return_value=page.encode()):
            assert fetcher._fetch_service_documentation(
                "forge", config, fetcher.get_service_cache_path("forge")
            ) is True

        assert fetcher.is_cache_valid("forge") is True

    def test_github_fetch_produces_a_valid_cache(self, fetcher, temp_dir):
        """_fetch_github_documentation wrote no success_rate at all, so its
        cache read back as 0.0 quality and was always invalid."""
        fetcher.save_cache_metadata = Mock(wraps=fetcher.save_cache_metadata)
        # Simulate the successful tail of a github fetch: metadata write only.
        # (The download/extract path is covered elsewhere.)
        fetcher.save_cache_metadata("nova", {
            "service": "nova", "repo": "r", "branch": "b",
            "fetch_method": "github_archive", "success_rate": 1.0,
        })
        assert fetcher.is_cache_valid("nova") is True

    def test_save_cache_metadata_stamps_cached_at(self, fetcher):
        fetcher.save_cache_metadata("vapor", {"success_rate": 1.0})
        saved = json.loads(fetcher.get_cache_metadata_path("vapor").read_text())
        assert saved["cached_at"] == pytest.approx(time.time(), abs=5)

    def test_explicit_cached_at_is_preserved(self, fetcher):
        """Tests and callers that back-date a cache deliberately must stay
        able to: stamping only fills the field in when absent."""
        fetcher.save_cache_metadata("vapor", {"success_rate": 1.0, "cached_at": 123.0})
        saved = json.loads(fetcher.get_cache_metadata_path("vapor").read_text())
        assert saved["cached_at"] == 123.0


class TestCommunityPackageMtimeCache:
    @pytest.fixture
    def packages(self, temp_dir):
        return CommunityPackageFetcher(temp_dir)

    def test_fresh_metadata_file_is_valid(self, packages):
        path = packages.get_cache_metadata_path("livewire")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}")
        assert packages.is_cache_valid("livewire") is True

    def test_backdated_metadata_file_is_invalid(self, packages):
        path = packages.get_cache_metadata_path("livewire")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}")
        old = time.time() - 86401
        os.utime(path, (old, old))
        assert packages.is_cache_valid("livewire") is False


class TestVersionsCacheErrorPaths:
    def test_corrupt_json_returns_none(self, temp_dir):
        cache = temp_dir / "cache.json"
        cache.write_text("{nope")
        assert _read_versions_cache(cache) is None

    def test_non_list_payload_rejected(self, temp_dir):
        cache = temp_dir / "cache.json"
        cache.write_text(json.dumps({"versions": "12.x"}))
        assert _read_versions_cache(cache) is None

    def test_hostile_entry_filtered_good_ones_kept(self, temp_dir):
        """The cache file ships in the image and lives in a bind-mountable
        directory: entries are untrusted, so malformed ones are dropped on
        read while well-formed ones survive."""
        cache = temp_dir / "cache.json"
        _write_versions_cache(["11.x", "../etc"], cache)
        assert _read_versions_cache(cache) == ["11.x"]

    def test_all_hostile_entries_reject_the_cache(self, temp_dir):
        cache = temp_dir / "cache.json"
        _write_versions_cache(["../etc", "latest;rm"], cache)
        assert _read_versions_cache(cache) is None

    def test_missing_updated_at_fails_ttl_read(self, temp_dir):
        cache = temp_dir / "cache.json"
        cache.write_text(json.dumps({"versions": ["12.x"]}))
        assert _read_versions_cache(cache, max_age_seconds=60) is None
        # without a TTL the same payload is acceptable
        assert _read_versions_cache(cache) == ["12.x"]

    def test_naive_timestamp_is_coerced_not_crashed(self, temp_dir):
        cache = temp_dir / "cache.json"
        cache.write_text(json.dumps({
            "versions": ["12.x"],
            "updated_at": "2026-01-01T00:00:00",  # no timezone
        }))
        # Stale (months old) → None under TTL, but no exception.
        assert _read_versions_cache(cache, max_age_seconds=60) is None
