"""Filament docs are discovered from the site's own llms.txt index.

They used to be 62 hand-listed pages under a pinned "3.x". Filament has since
shipped 4.x and 5.x, the pinned pages were two majors stale, and seven of them
404. The index names the current major and every page in it, so a new release
or a reorganised sidebar needs no change here.
"""

import json

import pytest

from docs_updater import CommunityPackageFetcher
from tests.conftest import urlopen_returning

INDEX_5X = """# Filament 5.x

> Documentation for Filament 5.x only. Do not mix APIs from other major versions.

- [Installation](https://filamentphp.com/docs/5.x/introduction/installation.md)
- [Overview](https://filamentphp.com/docs/5.x/resources/overview.md)
- [Overview](https://filamentphp.com/docs/5.x/forms/overview.md)
- [Text input](https://filamentphp.com/docs/5.x/forms/text-input.md)
- [Deployment](https://filamentphp.com/docs/5.x/deployment.md)
- [Elsewhere](https://example.com/docs/5.x/not-filament.md)
"""


def _page(title):
    return (f"# {title}\n\n> Filament documentation\n\n## Introduction\n\n"
            f"This page explains {title}. " + "More detail follows. " * 10).encode()


@pytest.fixture
def fetcher(temp_dir):
    return CommunityPackageFetcher(temp_dir)


def _fetch(fetcher, monkeypatch, index=INDEX_5X, pages=None):
    url_map = {"docs/llms.txt": index.encode()}
    url_map.update(pages if pages is not None else {
        "introduction/installation.md": _page("installing Filament"),
        "resources/overview.md": _page("resources"),
        "forms/overview.md": _page("forms"),
        "forms/text-input.md": _page("the text input"),
        "5.x/deployment.md": _page("deployment"),
    })
    monkeypatch.setattr("docs_updater.urllib.request.urlopen", urlopen_returning(b"", url_map=url_map))
    return fetcher.fetch_package_docs("filament", force=True)


class TestFilamentFromItsIndex:
    def test_every_page_in_the_index_is_saved_under_its_path(self, fetcher, monkeypatch):
        assert _fetch(fetcher, monkeypatch) is True

        package_dir = fetcher.get_package_cache_path("filament")
        assert sorted(p.name for p in package_dir.glob("*.md")) == [
            "deployment.md",
            "forms-overview.md",
            "forms-text-input.md",
            "introduction-installation.md",
            "resources-overview.md",
        ]

    def test_pages_sharing_a_final_segment_do_not_overwrite_each_other(self, fetcher, monkeypatch):
        _fetch(fetcher, monkeypatch)

        package_dir = fetcher.get_package_cache_path("filament")
        assert "This page explains resources." in (package_dir / "resources-overview.md").read_text()
        assert "This page explains forms." in (package_dir / "forms-overview.md").read_text()

    def test_metadata_records_the_major_version_the_site_is_on(self, fetcher, monkeypatch):
        _fetch(fetcher, monkeypatch)

        metadata = json.loads(fetcher.get_cache_metadata_path("filament").read_text())
        assert metadata["version"] == "5.x"
        assert (metadata["sections_count"], metadata["total_sections"], metadata["success_rate"]) == (5, 5, 1.0)

    def test_a_new_major_in_the_index_is_followed_and_the_old_one_dropped(self, fetcher, monkeypatch):
        index = (
            "- [Installation](https://filamentphp.com/docs/6.x/introduction/installation.md)\n"
            "- [Installation](https://filamentphp.com/docs/5.x/introduction/installation.md)\n"
        )
        # Only the 6.x page is mapped: requesting the 5.x one fails the fetch.
        assert _fetch(fetcher, monkeypatch, index=index,
                      pages={"docs/6.x/introduction/installation.md": _page("installing Filament 6")}) is True

        metadata = json.loads(fetcher.get_cache_metadata_path("filament").read_text())
        assert (metadata["version"], metadata["total_sections"], metadata["success_rate"]) == ("6.x", 1, 1.0)

    def test_a_complete_sync_removes_pages_from_the_previous_layout(self, fetcher, monkeypatch):
        stale = fetcher.get_package_cache_path("filament") / "panels-installation.md"
        stale.write_text("Filament 3.x installation")

        _fetch(fetcher, monkeypatch)

        assert not stale.exists()

    def test_a_partial_sync_keeps_what_is_already_saved(self, fetcher, monkeypatch):
        stale = fetcher.get_package_cache_path("filament") / "panels-installation.md"
        stale.write_text("Filament 3.x installation")

        # forms/text-input.md is left unmapped, so that one request fails.
        assert _fetch(fetcher, monkeypatch, pages={
            "introduction/installation.md": _page("installing Filament"),
            "resources/overview.md": _page("resources"),
            "forms/overview.md": _page("forms"),
            "5.x/deployment.md": _page("deployment"),
        }) is True

        assert stale.exists()
        metadata = json.loads(fetcher.get_cache_metadata_path("filament").read_text())
        assert (metadata["sections_count"], metadata["total_sections"]) == (4, 5)

    def test_an_index_with_no_filament_pages_is_a_failed_sync(self, fetcher, monkeypatch):
        assert _fetch(fetcher, monkeypatch, index="# Filament\n\nNothing here yet.\n", pages={}) is False
