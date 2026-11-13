"""Spatie packages follow the major version and page list the site shows.

Each package was pinned to a version in its URL (`/v6/`, `/v11/`, `/v9/`) with
a hand-kept list of pages. Laravel Permission has since shipped v7 and v8, so
the saved pages were two majors old and nothing reported it. A package's
landing page links every page of the current major in its navigation; reading
that gives the version and the pages together.
"""

import json
from unittest.mock import patch

import pytest

from laravel_mcp_companion.docs_updater import CommunityPackageFetcher, build_sync_report


def landing(package, version, pages, other_versions=("v7", "v6")):
    links = "".join(
        f'<a href="https://spatie.be/docs/{package}/{version}/{page}">{page}</a>' for page in pages
    )
    switcher = "".join(
        f'<a href="https://spatie.be/docs/{package}/{old}/introduction">{old}</a>' for old in other_versions
    )
    return f"<html><body><nav>{links}</nav><select>{switcher}</select></body></html>".encode()


V8_PAGES = ["introduction", "installation-laravel", "basic-usage/basic-usage", "basic-usage/enums", "advanced-usage/events"]


@pytest.fixture
def packages(temp_dir):
    fetcher = CommunityPackageFetcher(temp_dir)
    only_permission = {"laravel-permission": fetcher.community_packages["spatie"]["packages"]["laravel-permission"]}
    fetcher.community_packages["spatie"]["packages"] = only_permission
    return fetcher


def sync(packages, landing_page, failing=()):
    """Run the Spatie fetch against a fake site; returns the page URLs requested."""
    requested = []

    def fetch_page(url, package, section):
        requested.append(url)
        if any(url.endswith(path) for path in failing):
            return None
        return f"# {section}\n\nDocumentation for {url}.\n"

    def fetch_landing(url):
        if landing_page is None:
            raise OSError("spatie.be is unreachable")
        return landing_page

    with patch.object(packages, "_fetch_and_process_content", side_effect=fetch_page), \
         patch.object(packages, "_fetch_raw", side_effect=fetch_landing):
        ok = packages._fetch_spatie_docs(packages.community_packages["spatie"])
    return ok, requested


def metadata(packages):
    return json.loads(packages.get_cache_metadata_path("spatie", "laravel-permission").read_text())


def saved(packages):
    return sorted(p.name for p in packages.get_package_cache_path("spatie", "laravel-permission").glob("*.md"))


class TestCurrentMajorIsFollowed:
    def test_pages_are_requested_from_the_major_the_site_is_on(self, packages):
        ok, requested = sync(packages, landing("laravel-permission", "v8", V8_PAGES))

        assert ok is True
        assert requested == [f"https://spatie.be/docs/laravel-permission/v8/{page}" for page in V8_PAGES]

    def test_the_page_list_comes_from_the_site_not_the_pinned_list(self, packages):
        sync(packages, landing("laravel-permission", "v8", V8_PAGES))

        assert saved(packages) == [
            "advanced-usage-events.md", "basic-usage-basic-usage.md", "basic-usage-enums.md",
            "installation-laravel.md", "introduction.md",
        ]

    def test_the_metadata_records_the_version(self, packages):
        sync(packages, landing("laravel-permission", "v8", V8_PAGES))

        data = metadata(packages)
        assert (data["version"], data["sections_count"], data["total_sections"], data["success_rate"]) == ("v8", 5, 5, 1.0)

    def test_links_to_older_majors_in_the_version_switcher_are_not_followed(self, packages):
        _, requested = sync(packages, landing("laravel-permission", "v8", V8_PAGES))

        assert not any("/v7/" in url or "/v6/" in url for url in requested)

    def test_a_link_to_another_package_is_not_a_page_of_this_one(self, packages):
        page = landing("laravel-permission", "v8", V8_PAGES) + \
            b'<a href="https://spatie.be/docs/laravel-backup/v10/introduction">Backup</a>'

        _, requested = sync(packages, page)

        assert not any("laravel-backup" in url for url in requested)


class TestWhenTheSiteCannotBeRead:
    def test_an_unreachable_landing_page_falls_back_to_the_pinned_version_and_pages(self, packages):
        ok, requested = sync(packages, None)

        assert ok is True
        assert requested[0] == "https://spatie.be/docs/laravel-permission/v6/introduction"
        assert len(requested) == 18

    def test_a_landing_page_with_no_recognisable_navigation_falls_back(self, packages):
        _, requested = sync(packages, b"<html><body>Under maintenance</body></html>")

        assert requested[0] == "https://spatie.be/docs/laravel-permission/v6/introduction"


class TestPagesTheSiteDroppedAreRemoved:
    def _leave_old_page(self, packages):
        old = packages.get_package_cache_path("spatie", "laravel-permission") / "api-models.md"
        old.write_text("a page from the v6 layout")
        return old

    def test_a_complete_sync_removes_a_page_no_longer_listed(self, packages):
        old = self._leave_old_page(packages)

        sync(packages, landing("laravel-permission", "v8", V8_PAGES))

        assert not old.exists()

    def test_a_partial_sync_removes_nothing(self, packages):
        old = self._leave_old_page(packages)

        sync(packages, landing("laravel-permission", "v8", V8_PAGES), failing=["basic-usage/enums"])

        assert old.exists()
        assert metadata(packages)["success_rate"] == 0.8

    def test_a_partial_sync_is_reported(self, packages, temp_dir):
        sync(packages, landing("laravel-permission", "v8", V8_PAGES), failing=["basic-usage/enums", "introduction"])

        _, problems = build_sync_report(temp_dir)

        assert "spatie/laravel-permission: fetched 3 of 5 pages" in problems
