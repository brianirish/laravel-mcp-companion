"""A service's pages are read from the site's single-file export when it names one.

Besides llms.txt, the list of pages, these sites publish llms-full.txt: every
page in one response, each introduced by its title and a `Source:` line. Laravel
Cloud lists 228 pages, and fetching them one at a time got the updater rate
limited by laravel.com about 180 requests in, which also blocked Forge on the
same host. Reading the export makes a service two requests, whatever its size.

The index still decides what is expected: a page it lists that the export
lacks is fetched on its own, and the export contributes nothing the index does
not list.
"""

import json
import urllib.error
from unittest.mock import patch

import pytest

from laravel_mcp_companion.docs_updater import ExternalDocsFetcher

INDEX = """# Laravel Nightwatch

- [Start Guide](https://nightwatch.laravel.com/docs/start-guide.md): Get started
- [Sampling](https://nightwatch.laravel.com/docs/guides/sampling.md)
- [Cache](https://nightwatch.laravel.com/docs/cache.md)
"""


def _section(title, path, marker):
    return (f"# {title}\nSource: https://nightwatch.laravel.com/docs/{path}\n\n"
            f"About {title}.\n\n## Details\n\n" + f"{marker} " * 30 + "\n\n")


FULL = (
    _section("Start Guide", "start-guide", "from-the-export-start")
    + _section("Sampling", "guides/sampling", "from-the-export-sampling")
    + _section("Cache", "cache", "from-the-export-cache")
)


def _site(index=INDEX, full=FULL):
    requested = []

    def respond(url, *args, **kwargs):
        requested.append(url)
        if url.endswith("/llms.txt"):
            return index.encode()
        if url.endswith("/llms-full.txt"):
            if full is None:
                raise urllib.error.HTTPError(url, 404, "Not Found", None, None)
            return full.encode()
        return (f"# {url}\n\n> A page.\n\n## Details\n\n" + "fetched-on-its-own " * 30).encode()

    respond.requested = requested
    return respond


@pytest.fixture
def fetcher(temp_dir):
    """A fetcher whose Nightwatch entry names an export. In the shipped
    configuration only Laravel Cloud does; the mechanism is the same for any
    service, and Nightwatch's small index keeps these tests short."""
    fetcher = ExternalDocsFetcher(temp_dir)
    fetcher.laravel_services["nightwatch"]["llms_full"] = "https://nightwatch.laravel.com/docs/llms-full.txt"
    return fetcher


def _sync(fetcher, site):
    with patch.object(fetcher, "_retry_request", side_effect=site):
        ok = fetcher.fetch_laravel_service_docs("nightwatch", force=True)
    return ok


def _page(fetcher, relative):
    return (fetcher.get_service_cache_path("nightwatch") / relative).read_text()


class TestPagesComeFromTheExport:
    def test_a_whole_service_is_two_requests(self, fetcher):
        site = _site()

        assert _sync(fetcher, site) is True
        assert site.requested == [
            "https://nightwatch.laravel.com/docs/llms.txt",
            "https://nightwatch.laravel.com/docs/llms-full.txt",
        ]

    def test_every_listed_page_is_saved_under_its_path(self, fetcher):
        _sync(fetcher, _site())

        root = fetcher.get_service_cache_path("nightwatch")
        assert sorted(str(p.relative_to(root)) for p in root.rglob("*.md")) == [
            "cache.md", "guides/sampling.md", "start-guide.md",
        ]

    def test_a_page_keeps_the_saved_shape(self, fetcher):
        _sync(fetcher, _site())

        page = _page(fetcher, "guides/sampling.md")
        assert page.startswith(
            "Source: https://nightwatch.laravel.com/docs/guides/sampling.md\n\n# Sampling\n\nAbout Sampling.\n"
        )
        assert "from-the-export-sampling" in page
        assert "from-the-export-cache" not in page

    def test_the_metadata_counts_against_the_index(self, fetcher):
        _sync(fetcher, _site())

        metadata = json.loads(fetcher.get_cache_metadata_path("nightwatch").read_text())
        assert (len(metadata["fetched_sections"]), metadata["total_sections"], metadata["success_rate"]) == (3, 3, 1.0)


class TestTheIndexStaysInCharge:
    def test_a_listed_page_the_export_lacks_is_fetched_on_its_own(self, fetcher):
        partial = _section("Start Guide", "start-guide", "from-the-export-start")
        site = _site(full=partial + _section("Cache", "cache", "from-the-export-cache"))

        _sync(fetcher, site)

        assert "https://nightwatch.laravel.com/docs/guides/sampling.md" in site.requested
        assert "fetched-on-its-own" in _page(fetcher, "guides/sampling.md")
        assert "from-the-export-start" in _page(fetcher, "start-guide.md")

    def test_a_page_only_the_export_has_is_not_saved(self, fetcher):
        site = _site(full=FULL + _section("Retired", "retired-page", "retired"))

        _sync(fetcher, site)

        assert not (fetcher.get_service_cache_path("nightwatch") / "retired-page.md").exists()

    def test_a_section_from_another_site_is_not_a_page_boundary(self, fetcher):
        foreign = "# Elsewhere\nSource: https://example.com/docs/cache\n\nforeign-text " * 3
        site = _site(full=_section("Start Guide", "start-guide", "start") + foreign
                     + _section("Sampling", "guides/sampling", "sampling") + _section("Cache", "cache", "cache-own"))

        _sync(fetcher, site)

        assert "foreign-text" not in _page(fetcher, "cache.md")
        assert "cache-own" in _page(fetcher, "cache.md")


class TestWithoutAnExport:
    def test_a_site_with_no_export_is_fetched_page_by_page(self, fetcher):
        site = _site(full=None)

        assert _sync(fetcher, site) is True
        assert len([u for u in site.requested if u.endswith(".md")]) == 3
        assert "fetched-on-its-own" in _page(fetcher, "cache.md")

    def test_an_export_that_is_not_a_page_export_is_ignored(self, fetcher):
        site = _site(full="<html><body>Not found</body></html>")

        assert _sync(fetcher, site) is True
        assert "fetched-on-its-own" in _page(fetcher, "start-guide.md")
