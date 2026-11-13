"""Laravel Cloud, Nightwatch and Herd: the first-party products released since
the service list was last touched. Each publishes an llms.txt index, so each is
one entry in the service table and reuses the fetcher the other four use.
"""

import json
from unittest.mock import patch

import pytest

from laravel_mcp_companion.docs_updater import ExternalDocsFetcher, build_sync_report

HERD_INDEX = """# Laravel Herd

- [Installation](https://herd.laravel.com/docs/macos/getting-started/installation.md)
- [PHP versions](https://herd.laravel.com/docs/macos/technology/php-versions.md)
- [Installation](https://herd.laravel.com/docs/windows/getting-started/installation.md)
- [PHP versions](https://herd.laravel.com/docs/windows/technology/php-versions.md)
"""

CLOUD_INDEX = """# Laravel Cloud

- [Welcome to Laravel Cloud](https://laravel.com/cloud/docs/intro.md): The deployment platform.
- [Environments](https://laravel.com/cloud/docs/environments.md)
- [Create an environment](https://laravel.com/cloud/docs/api/environments/create.md)
- [Forge is elsewhere](https://laravel.com/forge/docs/introduction.md)
"""


def _site(index):
    def respond(url, *args, **kwargs):
        if url.endswith("/llms.txt"):
            return index.encode()
        return (f"# {url}\n\n> A page.\n\n## Introduction\n\n" + f"Text for {url}. " * 12).encode()
    return respond


@pytest.fixture
def fetcher(temp_dir):
    return ExternalDocsFetcher(temp_dir)


def _sync(fetcher, service, index):
    with patch.object(fetcher, "_retry_request", side_effect=_site(index)):
        return fetcher.fetch_laravel_service_docs(service, force=True)


def _saved(fetcher, service):
    root = fetcher.get_service_cache_path(service)
    return sorted(str(p.relative_to(root)) for p in root.rglob("*.md"))


class TestTheThreeServicesAreConfigured:
    @pytest.mark.parametrize("service", ["cloud", "nightwatch", "herd"])
    def test_the_index_sits_under_the_prefix_its_pages_use(self, fetcher, service):
        config = fetcher.laravel_services[service]

        assert config["llms_index"] == config["llms_page_prefix"] + "llms.txt"
        assert config["llms_page_prefix"].startswith("https://")

    @pytest.mark.parametrize("service", ["cloud", "nightwatch", "herd"])
    def test_the_sync_report_covers_it(self, fetcher, temp_dir, service):
        _, problems = build_sync_report(temp_dir)

        assert f"{service}: never synced" in problems


class TestHerd:
    def test_the_macos_and_windows_guides_do_not_overwrite_each_other(self, fetcher):
        assert _sync(fetcher, "herd", HERD_INDEX) is True

        assert _saved(fetcher, "herd") == [
            "macos/getting-started/installation.md",
            "macos/technology/php-versions.md",
            "windows/getting-started/installation.md",
            "windows/technology/php-versions.md",
        ]

    def test_each_platforms_page_keeps_its_own_text(self, fetcher):
        _sync(fetcher, "herd", HERD_INDEX)
        root = fetcher.get_service_cache_path("herd")

        assert "docs/windows/getting-started/installation.md" in (root / "windows/getting-started/installation.md").read_text()
        assert "docs/macos/getting-started/installation.md" in (root / "macos/getting-started/installation.md").read_text()


class TestCloud:
    def test_only_cloud_pages_are_taken_from_an_index_on_the_shared_laravel_domain(self, fetcher):
        assert _sync(fetcher, "cloud", CLOUD_INDEX) is True

        assert not any("forge" in page for page in _saved(fetcher, "cloud"))
        assert "intro.md" in _saved(fetcher, "cloud")


CLOUD_EXPORT = """# Welcome to Laravel Cloud
Source: https://laravel.com/cloud/docs/intro

The deployment platform.

<CardGroup cols={2}>
  <Card title="Quickstart" icon="rocket" href="/cloud/docs/quickstart">
    Deploy your first application.
  </Card>
</CardGroup>

## Regions

<Frame>
  <img src="/images/regions.png" alt="Regions" />
</Frame>

<Note>
  Regions cannot be changed after an environment is created.
</Note>

&#x20;

See [environments](/cloud/docs/environments#regions) for the list. Padding so the page is long enough to keep.

Pick a [supported runtime](/docs/runtimes#php) first.

```jsx
<Card title="An example that is code">not prose</Card>
```

# Environments
Source: https://laravel.com/cloud/docs/environments

Environments hold deployments.

<Steps>
  <Step title="Create the environment">
    Choose a branch. This paragraph is long enough that the page is kept by the fetcher.
  </Step>
</Steps>
"""


def _cloud_site(requested):
    def respond(url, *args, **kwargs):
        requested.append(url)
        if url.endswith("/llms.txt"):
            return CLOUD_INDEX.encode()
        if url.endswith("/llms-full.txt"):
            return CLOUD_EXPORT.encode()
        return (f"# {url}\n\n> A page.\n\n## Introduction\n\n" + f"Text for {url}. " * 12).encode()
    return respond


class TestCloudIsReadFromItsExport:
    """228 single-page requests to laravel.com got the updater blocked there,
    and the block also covers Forge and Laravel Learn on the same host."""

    def _sync(self, fetcher):
        requested = []
        with patch.object(fetcher, "_retry_request", side_effect=_cloud_site(requested)):
            ok = fetcher.fetch_laravel_service_docs("cloud", force=True)
        return ok, requested

    def test_the_pages_the_export_has_cost_no_request_of_their_own(self, fetcher):
        _, requested = self._sync(fetcher)

        assert "https://laravel.com/cloud/docs/llms-full.txt" in requested
        assert "https://laravel.com/cloud/docs/intro.md" not in requested
        assert "https://laravel.com/cloud/docs/environments.md" not in requested

    def test_the_api_reference_is_left_out(self, fetcher):
        """It is about 130 pages, each the whole OpenAPI document as YAML."""
        _, requested = self._sync(fetcher)

        assert _saved(fetcher, "cloud") == ["environments.md", "intro.md"]
        assert not any("/api/" in url for url in requested)

    def test_left_out_pages_do_not_count_as_missing(self, fetcher):
        self._sync(fetcher)

        metadata = json.loads(fetcher.get_cache_metadata_path("cloud").read_text())
        assert (metadata["total_sections"], metadata["success_rate"]) == (2, 1.0)


class TestExportTextIsCleanedOfComponentMarkup:
    """The export is the site's source with its components left in. Read as
    prose, `<Frame>` and `<Card>` are noise, and site-relative links lead
    nowhere from a saved page."""

    @pytest.fixture
    def intro(self, fetcher):
        requested = []
        with patch.object(fetcher, "_retry_request", side_effect=_cloud_site(requested)):
            fetcher.fetch_laravel_service_docs("cloud", force=True)
        return (fetcher.get_service_cache_path("cloud") / "intro.md").read_text()

    def test_a_card_becomes_a_linked_title_with_its_text(self, intro):
        assert "**[Quickstart](https://laravel.com/cloud/docs/quickstart)**" in intro
        assert "Deploy your first application." in intro
        assert '<Card title="Quickstart"' not in intro and "CardGroup" not in intro

    def test_an_image_frame_is_dropped(self, intro):
        assert "<Frame>" not in intro and "<img" not in intro

    def test_a_callout_keeps_its_text(self, intro):
        assert "**Note:** Regions cannot be changed after an environment is created." in intro
        assert "<Note>" not in intro

    def test_a_spacer_entity_on_a_line_of_its_own_is_dropped(self, intro):
        assert "&#x20;" not in intro

    def test_a_site_relative_link_is_made_absolute(self, intro):
        assert "[environments](https://laravel.com/cloud/docs/environments#regions)" in intro

    def test_a_link_written_against_the_docs_root_lands_under_the_services_own_path(self, intro):
        """Cloud's pages link to "/docs/runtimes", written for a site whose
        docs sit at /docs. They are served from laravel.com/cloud/docs, and
        laravel.com/docs is the framework's documentation."""
        assert "[supported runtime](https://laravel.com/cloud/docs/runtimes#php)" in intro

    def test_markup_inside_a_code_block_is_left_alone(self, intro):
        assert '<Card title="An example that is code">not prose</Card>' in intro

    def test_a_step_keeps_its_title(self, fetcher):
        requested = []
        with patch.object(fetcher, "_retry_request", side_effect=_cloud_site(requested)):
            fetcher.fetch_laravel_service_docs("cloud", force=True)
        page = (fetcher.get_service_cache_path("cloud") / "environments.md").read_text()

        assert "**Create the environment**" in page
        assert "<Step" not in page
