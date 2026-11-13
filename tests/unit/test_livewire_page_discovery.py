"""Livewire's pages are read from the site's navigation, on its current major.

The fetcher had 36 page names typed in when Livewire was on v3. Livewire 4
lists 81 pages; the 45 added since were never fetched, and nothing would have
removed a page the site dropped.
"""

import json
from unittest.mock import patch

import pytest

from laravel_mcp_companion.docs_updater import CommunityPackageFetcher

PAGES = ["quickstart", "components", "attribute-computed", "islands"]


def landing(version="4.x", pages=PAGES):
    nav = "".join(f'<a href="/docs/{version}/{page}">{page}</a>' for page in pages)
    older = '<a href="/docs/3.x/quickstart">3.x</a><a href="https://laravel-livewire.com/docs/2.x/quickstart">2.x</a>'
    return f"<html><nav>{nav}</nav><footer>{older}</footer></html>".encode()


@pytest.fixture
def packages(temp_dir):
    return CommunityPackageFetcher(temp_dir)


def sync(packages, landing_page, failing=()):
    requested = []

    def fetch_page(url, package, section):
        requested.append(url)
        return None if any(url.endswith(f"/{name}") for name in failing) else f"# {section}\n\nText from {url}.\n"

    def fetch_landing(url):
        if landing_page is None:
            raise OSError("livewire.laravel.com is unreachable")
        return landing_page

    with patch.object(packages, "_fetch_and_process_content", side_effect=fetch_page), \
         patch.object(packages, "_fetch_raw", side_effect=fetch_landing):
        ok = packages._fetch_livewire_docs(packages.community_packages["livewire"])
    return ok, requested


def metadata(packages):
    return json.loads(packages.get_cache_metadata_path("livewire").read_text())


class TestPagesComeFromTheNavigation:
    def test_every_page_the_site_lists_is_requested_on_its_current_major(self, packages):
        ok, requested = sync(packages, landing())

        assert ok is True
        assert requested == [f"https://livewire.laravel.com/docs/4.x/{page}" for page in PAGES]

    def test_a_page_missing_from_the_old_pinned_list_is_saved(self, packages):
        sync(packages, landing())

        assert (packages.get_package_cache_path("livewire") / "islands.md").exists()

    def test_the_metadata_records_the_major(self, packages):
        sync(packages, landing())

        data = metadata(packages)
        assert (data["version"], data["sections_count"], data["total_sections"]) == ("4.x", 4, 4)

    def test_an_older_major_linked_from_the_page_is_not_followed(self, packages):
        _, requested = sync(packages, landing())

        assert not any("/3.x/" in url or "/2.x/" in url for url in requested)


class TestFallbackAndPruning:
    def test_an_unreachable_landing_page_falls_back_to_the_pinned_page_list(self, packages):
        ok, requested = sync(packages, None)

        assert ok is True
        assert requested[0] == "https://livewire.laravel.com/docs/quickstart"
        assert len(requested) == 36

    def test_a_complete_sync_removes_a_page_the_site_no_longer_lists(self, packages):
        old = packages.get_package_cache_path("livewire") / "wire-offline.md"
        old.write_text("a page from an earlier major")

        sync(packages, landing())

        assert not old.exists()

    def test_a_partial_sync_removes_nothing(self, packages):
        old = packages.get_package_cache_path("livewire") / "wire-offline.md"
        old.write_text("a page from an earlier major")

        sync(packages, landing(), failing=["islands"])

        assert old.exists()
        assert metadata(packages)["success_rate"] == 0.75


class TestPromotionalBlockIsRemoved:
    """Every Livewire docs page opens with an advertisement for a paid UI kit,
    which was being saved at the top of all 36 pages."""

    PAGE = (
        "Quickstart\n==========\n\nThe official Livewire UI kit\n\nBuild polished Livewire apps faster.\n\n"
        "Explore Flux Pro\n→\n\n\nLivewire allows you to build dynamic interfaces using only PHP.\n"
    )

    def test_the_advertisement_is_not_saved(self, packages):
        cleaned = packages._clean_markdown_content(self.PAGE)

        assert "Flux Pro" not in cleaned and "UI kit" not in cleaned

    def test_the_page_text_around_it_is_kept(self, packages):
        cleaned = packages._clean_markdown_content(self.PAGE)

        assert cleaned.startswith("Quickstart\n==========\n\nLivewire allows you to build")

    def test_a_sentence_that_merely_mentions_flux_is_left_alone(self, packages):
        text = "Heading\n=======\n\nYou can pair Livewire with Flux Pro components if you like.\n"

        assert "Flux Pro components" in packages._clean_markdown_content(text)
