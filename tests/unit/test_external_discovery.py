"""Discovery, pruning and clean-up for the Laravel service docs (Forge, Vapor,
Nova, Envoyer).

These pin what the 2026-11 audit of the daily sync found: Forge moved to
laravel.com/forge/docs, so discovery matched nothing and the manual fallback
404'd on most of its list; non-pages (llms.txt, sitemap.xml, *.md twins) were
saved as documentation; pages that disappeared upstream were kept forever; and
site chrome leaked into the saved text.
"""

import json
import urllib.error
from unittest.mock import patch

import pytest

from docs_updater import DocumentationAutoDiscovery, ExternalDocsFetcher

PAGE = "<html><body><main><h1>Title</h1>" + "<p>Real documentation content.</p>" * 20 + "</main></body></html>"

FORGE_INDEX = """
<html><head>
<link rel="stylesheet" href="/forge/docs/_mintlify/assets/index-B56Lz__T.css?dpl=dpl_6PxPD4">
<link rel="icon" href="/forge/docs/mintlify-assets/_mintlify/favicons/forge-laravel/favicon.ico">
<link rel="preload" href="/forge/docs/_mintlify/custom/forge-laravel/1bbd0658/rudder.js">
<link rel="alternate" href="/forge/docs/introduction.md">
<link rel="alternate" href="/forge/docs/llms.txt">
<link rel="sitemap" href="/forge/docs/sitemap.xml">
</head><body><nav>
<a href="/forge/docs/introduction">Introduction</a>
<a href="/forge/docs/cli">Forge CLI</a>
<a href="/forge/docs/servers/php">PHP</a>
<a href="/forge/docs/servers/php#opcache">OPcache</a>
<a href="/forge/docs/sites/the-basics">The Basics</a>
</nav></body></html>
"""


@pytest.fixture
def fetcher(temp_dir):
    return ExternalDocsFetcher(temp_dir)


def _serve(index_html, failing=()):
    """A stand-in for _retry_request: the service index at its base URL, a
    documentation page everywhere else, HTTP 500 for paths in `failing`."""
    def respond(url, *args, **kwargs):
        if any(url.endswith(f"/{path}") for path in failing):
            raise urllib.error.HTTPError(url, 500, "Server Error", None, None)
        if url.rstrip("/").endswith(("/docs", "vapor.build", "/docs/v5")):
            return index_html.encode()
        return PAGE.encode()
    return respond


def _fetch(fetcher, service, index_html, failing=()):
    # Discovery is only trusted when it finds at least 75% as many pages as the
    # manual fallback list holds. The fixture index is four pages, so give the
    # sync a fallback list of matching size; everything else is the real config.
    config = dict(fetcher.laravel_services[service], sections=["introduction", "cli"])
    respond = _serve(index_html, failing)
    with patch.object(fetcher, "_retry_request", side_effect=respond), \
         patch.object(fetcher.auto_discovery, "_retry_request", side_effect=respond):
        ok = fetcher._fetch_service_documentation(service, config, fetcher.get_service_cache_path(service))
    metadata = json.loads(fetcher.get_cache_metadata_path(service).read_text())
    return ok, metadata


class TestForgeDiscovery:
    def test_finds_pages_at_the_current_forge_location(self, fetcher):
        discovery = fetcher.auto_discovery
        config = fetcher.laravel_services["forge"]
        with patch.object(discovery, "_retry_request", return_value=FORGE_INDEX.encode()):
            sections = discovery.discover_sections("forge", config)

        assert sections == ["cli", "introduction", "servers/php", "sites/the-basics"]

    def test_a_forge_sync_uses_discovery_rather_than_the_fallback_list(self, fetcher):
        ok, metadata = _fetch(fetcher, "forge", FORGE_INDEX)

        assert ok is True
        assert metadata["discovery_method"] == "auto-discovery"
        assert metadata["fetched_sections"] == ["cli", "introduction", "servers/php", "sites/the-basics"]


class TestNonPagesAreNotDocumentation:
    @pytest.mark.parametrize("path", [
        "llms.txt",
        "llms-full.txt",
        "sitemap.xml",
        "robots.txt",
        "introduction.md",
        "installation.md",
        "cdn-cgi/l/email-protection",
        "_mintlify/assets/index-B56Lz__T.css",
        "mintlify-assets/_mintlify/favicons/forge-laravel/favicon.ico",
        "_next/static/css/19e66b131dc509b0.css",
    ])
    def test_non_page_paths_are_rejected(self, path):
        assert DocumentationAutoDiscovery()._is_page_section(path) is False

    @pytest.mark.parametrize("path", [
        "introduction",
        "servers/php",
        "api-reference/introduction",
        "resources/the-basics",
        "sites/environment-variables",
    ])
    def test_real_pages_are_kept(self, path):
        assert DocumentationAutoDiscovery()._is_page_section(path) is True

    def test_vapor_discovery_skips_non_pages(self, fetcher):
        index = """
        <a href="/introduction">Introduction</a>
        <a href="/introduction#permissions">Permissions</a>
        <a href="/projects/the-basics">The Basics</a>
        <a href="/llms.txt">llms</a>
        <a href="/introduction.md">Markdown</a>
        <a href="/sitemap.xml">Sitemap</a>
        <a href="/cdn-cgi/l/email-protection">[email&#160;protected]</a>
        """
        discovery = fetcher.auto_discovery
        with patch.object(discovery, "_retry_request", return_value=index.encode()):
            sections = discovery.discover_sections("vapor", fetcher.laravel_services["vapor"])

        assert sections == ["introduction", "projects/the-basics"]

    def test_nova_discovery_skips_markdown_twins(self, fetcher):
        index = """
        <a href="/docs/v5/installation">Installation</a>
        <a href="/docs/v5/installation.md">Markdown</a>
        <a href="/docs/v5/resources/fields">Fields</a>
        <a href="/docs/v5/llms.txt">llms</a>
        """
        discovery = fetcher.auto_discovery
        with patch.object(discovery, "_retry_request", return_value=index.encode()):
            sections = discovery.discover_sections("nova", fetcher.laravel_services["nova"])

        assert sections == ["installation", "resources/fields"]


class TestPruningPagesThatLeftTheSite:
    def _seed_stale(self, fetcher):
        root = fetcher.get_service_cache_path("forge")
        stale = [
            root / "servers" / "providers.md",          # page removed upstream
            root / "accounts" / "circles.md",           # whole category removed
            root / "sitemap.xml.md",                    # junk saved by an old run
            root / "servers" / "php#opcache.md",        # fragment saved as a page
            root / "_next" / "static" / "css" / "19e66b131dc509b0.css.md",
        ]
        for path in stale:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("stale")
        return root, stale

    def test_a_complete_discovered_sync_removes_pages_no_longer_on_the_site(self, fetcher):
        root, stale = self._seed_stale(fetcher)

        _fetch(fetcher, "forge", FORGE_INDEX)

        assert [p for p in stale if p.exists()] == []
        assert sorted(str(p.relative_to(root)) for p in root.rglob("*.md")) == [
            "cli.md", "introduction.md", "servers/php.md", "sites/the-basics.md",
        ]
        assert not (root / "accounts").exists()
        assert not (root / "_next").exists()
        assert fetcher.get_cache_metadata_path("forge").exists()

    def test_a_partial_sync_prunes_nothing(self, fetcher):
        """A page that failed to download is indistinguishable from a site
        having a bad day; deleting on that evidence would lose good docs."""
        _, stale = self._seed_stale(fetcher)

        _fetch(fetcher, "forge", FORGE_INDEX, failing=("cli",))

        assert all(p.exists() for p in stale)

    def test_a_sync_that_fell_back_to_the_manual_list_prunes_nothing(self, fetcher):
        """No discovery means no evidence of what the site currently holds."""
        _, stale = self._seed_stale(fetcher)

        _, metadata = _fetch(fetcher, "forge", "<html><body>no links here</body></html>")

        assert metadata["discovery_method"] == "manual configuration"
        assert all(p.exists() for p in stale)


class TestSiteChromeIsStripped:
    def test_feedback_widget_and_back_to_top_are_removed(self, fetcher):
        html = """
        <main>
          <h2>On this page</h2><button>Back to top</button>
          <h1>Deployments</h1>
          <p>Push to deploy your application.</p>
          <div>Was this page helpful?</div>
          <div><button>Yes</button><button>No</button></div>
        </main>
        """
        text = fetcher._html_to_text(html)

        assert "Push to deploy your application." in text
        assert "Was this page helpful?" not in text
        assert "YesNo" not in text
        assert "Back to top" not in text

    def test_prose_that_merely_mentions_the_phrases_is_kept(self, fetcher):
        html = "<main><p>Click Back to top to return, then answer Yes or No.</p></main>"

        assert "Click Back to top to return, then answer Yes or No." in fetcher._html_to_text(html)


class TestForceRefetchesAValidCache:
    def test_force_refetches_a_service_whose_cache_is_still_valid(self, fetcher):
        """`force` was dropped between fetch_all_services and the per-service
        fetch, which re-checked the cache and returned early: --force only ever
        refetched services that were going to be refetched anyway."""
        fetcher.save_cache_metadata("vapor", {"service": "vapor", "success_rate": 1.0})
        assert fetcher.is_cache_valid("vapor") is True

        with patch.object(fetcher, "_fetch_service_documentation", return_value=True) as fetch:
            fetcher.fetch_all_services(force=True)

        assert "vapor" in [call.args[0] for call in fetch.call_args_list]

    def test_without_force_a_valid_cache_is_left_alone(self, fetcher):
        fetcher.save_cache_metadata("vapor", {"service": "vapor", "success_rate": 1.0})

        with patch.object(fetcher, "_fetch_service_documentation", return_value=True) as fetch:
            fetcher.fetch_all_services(force=False)

        assert "vapor" not in [call.args[0] for call in fetch.call_args_list]
