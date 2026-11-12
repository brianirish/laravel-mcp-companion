"""Forge, Vapor, Nova and Envoyer are read from the llms.txt index each site
publishes, as markdown, instead of being discovered from navigation links and
scraped from HTML.

The scraping path needed a link pattern per site, broke silently when a site
moved (Forge) or changed its link shape (Envoyer never discovered a page), and
carried the site's chrome into the saved text. The index is the site's own list
of its pages.
"""

import json
import urllib.error
from unittest.mock import patch

import pytest

from docs_updater import ExternalDocsFetcher

FORGE_INDEX = """# Laravel Forge

## Docs

- [Welcome to Laravel Forge](https://laravel.com/forge/docs/introduction.md): Server management for Laravel.
- [PHP](https://laravel.com/forge/docs/servers/php.md): Manage PHP versions.
- [Servers](https://laravel.com/forge/docs/knowledge-base/servers.md)

## Optional

- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/forge)
"""


def _page(title):
    return (
        "> ## Documentation Index\n"
        "> Fetch the complete documentation index at: https://example.test/llms.txt\n"
        "> Use this file to discover all available pages before exploring further.\n\n"
        f"# {title}\n\n> About {title}.\n\n## Introduction\n\n"
        f"This page documents {title}. " + "It goes into detail. " * 10
    ).encode()


def _site(index, failing=()):
    requested = []

    def respond(url, *args, **kwargs):
        requested.append(url)
        if url.endswith("/llms.txt"):
            return index.encode()
        if any(url.endswith(path) for path in failing):
            raise urllib.error.HTTPError(url, 500, "Server Error", None, None)
        return _page(url.rsplit("/", 1)[-1][:-len(".md")])

    respond.requested = requested
    return respond


@pytest.fixture
def fetcher(temp_dir):
    return ExternalDocsFetcher(temp_dir)


def _sync(fetcher, service, index, failing=()):
    site = _site(index, failing)
    with patch.object(fetcher, "_retry_request", side_effect=site):
        ok = fetcher.fetch_laravel_service_docs(service, force=True)
    return ok, site.requested


def _saved(fetcher, service):
    root = fetcher.get_service_cache_path(service)
    return sorted(str(p.relative_to(root)) for p in root.rglob("*.md"))


def _metadata(fetcher, service):
    return json.loads(fetcher.get_cache_metadata_path(service).read_text())


class TestServicePagesComeFromTheIndex:
    def test_every_page_in_the_index_is_saved_at_its_path(self, fetcher):
        ok, _ = _sync(fetcher, "forge", FORGE_INDEX)

        assert ok is True
        assert _saved(fetcher, "forge") == ["introduction.md", "knowledge-base/servers.md", "servers/php.md"]

    def test_a_page_is_saved_without_the_index_banner_and_names_its_source(self, fetcher):
        _sync(fetcher, "forge", FORGE_INDEX)

        text = (fetcher.get_service_cache_path("forge") / "servers" / "php.md").read_text()
        assert text.startswith("Source: https://laravel.com/forge/docs/servers/php.md\n\n# php\n")
        assert "This page documents php." in text
        assert "Documentation Index" not in text

    def test_links_outside_the_docs_are_not_fetched(self, fetcher):
        _, requested = _sync(fetcher, "forge", FORGE_INDEX)

        assert [url for url in requested if "laravel.com/forge/docs/" not in url] == []

    def test_metadata_lists_what_was_fetched_and_how(self, fetcher):
        _sync(fetcher, "forge", FORGE_INDEX)

        metadata = _metadata(fetcher, "forge")
        assert metadata["fetched_sections"] == ["introduction", "servers/php", "knowledge-base/servers"]
        assert (metadata["total_sections"], metadata["success_rate"]) == (3, 1.0)
        assert metadata["discovery_method"] == "llms-index"

    def test_a_synced_service_has_a_valid_cache(self, fetcher):
        _sync(fetcher, "forge", FORGE_INDEX)

        assert fetcher.is_cache_valid("forge") is True

    def test_envoyer_picks_up_a_page_nobody_listed_by_hand(self, fetcher):
        """Envoyer's link discovery never matched its site, so it ran from a
        hand-kept list and a new page would have been missed."""
        index = (
            "- [Introduction](https://docs.envoyer.io/introduction.md)\n"
            "- [Rollbacks](https://docs.envoyer.io/projects/rollbacks.md)\n"
        )

        _sync(fetcher, "envoyer", index)

        assert _saved(fetcher, "envoyer") == ["introduction.md", "projects/rollbacks.md"]

    def test_vapor_is_read_from_its_index(self, fetcher):
        index = "- [Deployments](https://docs.vapor.build/projects/deployments.md)\n"

        _sync(fetcher, "vapor", index)

        assert _saved(fetcher, "vapor") == ["projects/deployments.md"]


class TestNovaFollowsItsNewestMajor:
    INDEX = (
        "- [Installation](https://nova.laravel.com/docs/v4/installation.md)\n"
        "- [Fields](https://nova.laravel.com/docs/v4/resources/fields.md)\n"
        "- [Installation](https://nova.laravel.com/docs/v5/installation.md)\n"
        "- [Fields](https://nova.laravel.com/docs/v5/resources/fields.md)\n"
    )

    def test_only_the_newest_major_is_requested(self, fetcher):
        _, requested = _sync(fetcher, "nova", self.INDEX)

        assert [url for url in requested if "/v4/" in url] == []

    def test_pages_are_saved_below_the_service_not_below_the_version(self, fetcher):
        _sync(fetcher, "nova", self.INDEX)

        assert _saved(fetcher, "nova") == ["installation.md", "resources/fields.md"]

    def test_metadata_records_the_major(self, fetcher):
        _sync(fetcher, "nova", self.INDEX)

        metadata = _metadata(fetcher, "nova")
        assert (metadata["version"], metadata["total_sections"]) == ("v5", 2)

    def test_a_numbered_segment_deeper_in_a_path_is_not_a_version(self, fetcher):
        index = (
            "- [Servers](https://laravel.com/forge/docs/api-reference/v1/servers.md)\n"
            "- [Introduction](https://laravel.com/forge/docs/introduction.md)\n"
        )

        _sync(fetcher, "forge", index)

        assert _saved(fetcher, "forge") == ["api-reference/v1/servers.md", "introduction.md"]


class TestPruning:
    def _seed(self, fetcher):
        root = fetcher.get_service_cache_path("forge")
        stale = [
            root / "servers" / "providers.md",
            root / "accounts" / "circles.md",
            root / "sitemap.xml.md",
            root / "_next" / "static" / "css" / "19e66b131dc509b0.css.md",
        ]
        for path in stale:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("stale")
        return root, stale

    def test_a_complete_sync_removes_pages_the_index_no_longer_lists(self, fetcher):
        root, stale = self._seed(fetcher)

        _sync(fetcher, "forge", FORGE_INDEX)

        assert [p for p in stale if p.exists()] == []
        assert not (root / "accounts").exists()
        assert not (root / "_next").exists()

    def test_a_partial_sync_removes_nothing_and_reports_its_rate(self, fetcher):
        _, stale = self._seed(fetcher)

        ok, _ = _sync(fetcher, "forge", FORGE_INDEX, failing=("servers/php.md",))

        assert ok is True
        assert all(p.exists() for p in stale)
        metadata = _metadata(fetcher, "forge")
        assert metadata["fetched_sections"] == ["introduction", "knowledge-base/servers"]
        assert metadata["success_rate"] == pytest.approx(2 / 3)


class TestAnUnusableIndex:
    def test_an_index_with_no_pages_fails_and_leaves_everything_in_place(self, fetcher):
        root = fetcher.get_service_cache_path("forge")
        (root / "introduction.md").write_text("existing page")

        ok, _ = _sync(fetcher, "forge", "# Laravel Forge\n\nNothing listed.\n")

        assert ok is False
        assert (root / "introduction.md").read_text() == "existing page"
        assert not fetcher.get_cache_metadata_path("forge").exists()

    def test_an_index_that_cannot_be_fetched_fails(self, fetcher):
        def respond(url, *args, **kwargs):
            raise urllib.error.HTTPError(url, 404, "Not Found", None, None)

        with patch.object(fetcher, "_retry_request", side_effect=respond):
            assert fetcher.fetch_laravel_service_docs("forge", force=True) is False

    def test_an_entry_that_climbs_out_of_the_service_directory_is_ignored(self, fetcher, temp_dir):
        index = (
            "- [Escape](https://laravel.com/forge/docs/servers/../../../../escaped.md)\n"
            "- [Introduction](https://laravel.com/forge/docs/introduction.md)\n"
        )

        _, requested = _sync(fetcher, "forge", index)

        assert _saved(fetcher, "forge") == ["introduction.md"]
        assert [url for url in requested if ".." in url] == []
        assert not list(temp_dir.rglob("escaped.md"))


class TestForce:
    def test_force_refetches_a_service_whose_cache_is_still_valid(self, fetcher):
        """`force` was once dropped between fetch_all_services and the
        per-service fetch, which re-checked the cache and returned early."""
        fetcher.save_cache_metadata("vapor", {"service": "vapor", "success_rate": 1.0})
        assert fetcher.is_cache_valid("vapor") is True

        with patch.object(fetcher, "_fetch_service_from_index", return_value=True) as fetch:
            fetcher.fetch_all_services(force=True)

        assert "vapor" in [call.args[0] for call in fetch.call_args_list]

    def test_without_force_a_valid_cache_is_left_alone(self, fetcher):
        fetcher.save_cache_metadata("vapor", {"service": "vapor", "success_rate": 1.0})

        with patch.object(fetcher, "_fetch_service_from_index", return_value=True) as fetch:
            fetcher.fetch_all_services(force=False)

        assert "vapor" not in [call.args[0] for call in fetch.call_args_list]
