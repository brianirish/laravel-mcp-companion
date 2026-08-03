"""Conversion edges: JSX extraction, HTML content-area fallback, and the
section-sanitization skip branches inside the service fetch loop."""

import json
from unittest.mock import Mock, patch

import pytest

from docs_updater import CommunityPackageFetcher, ExternalDocsFetcher
from tests.conftest import load_fixture

GOOD_PAGE = "<html><body><main>" + "Documentation words here. " * 30 + "</main></body></html>"


@pytest.fixture
def packages(temp_dir):
    return CommunityPackageFetcher(temp_dir)


@pytest.fixture
def external(temp_dir):
    return ExternalDocsFetcher(temp_dir)


class TestJsxToMarkdown:
    def test_recorded_page_converts(self, packages):
        out = packages._process_jsx_to_markdown(load_fixture("inertia_page.jsx"), "routing")
        assert out is not None
        assert "# Routing" in out
        assert "## Shorthand routes" in out
        assert "defined server-side" in out
        assert "Route::inertia('/about', 'About');" in out
        assert "- Generate URLs server-side and include them as props." in out
        # imports/JSX plumbing never leak through
        assert "import React" not in out
        assert "export default" not in out

    def test_pure_code_yields_none(self, packages):
        assert packages._process_jsx_to_markdown("const x = 1;", "routing") is None

    def test_exception_yields_none(self, packages):
        assert packages._process_jsx_to_markdown(None, "routing") is None  # type: ignore[arg-type]


class TestExtractHtmlContent:
    def test_main_area_preferred(self, external):
        html = "<html><body><nav>menu</nav><main>" + "content " * 40 + "</main></body></html>"
        out = external._extract_html_content(html)
        assert "content" in out
        assert "menu" not in out

    def test_unrecognized_structure_falls_back_to_text(self, external):
        out = external._extract_html_content(load_fixture("moved_structure.html"))
        assert "We moved!" in out

    def test_truncates_at_fifty_thousand_chars(self, external):
        big = "<html><body><main>" + ("word " * 20000) + "</main></body></html>"
        assert len(external._extract_html_content(big)) <= 50100

    def test_truncated_html_still_yields_content(self, external):
        out = external._html_to_text(load_fixture("truncated.html"))
        assert "Start of content" in out


class TestSectionSanitizationSkips:
    def _fetch(self, external, sections, discovered=None):
        config = {
            "name": "Forge",
            "base_url": "https://forge.laravel.com/docs",
            "auto_discovery": discovered is not None,
            "sections": sections,
        }
        if discovered is not None:
            external.auto_discovery.discover_sections = Mock(return_value=discovered)
        target = external.get_service_cache_path("forge")
        with patch.object(external, "_retry_request", return_value=GOOD_PAGE.encode()):
            result = external._fetch_service_documentation("forge", config, target)
        return result, target

    def test_hostile_and_asset_sections_skipped_but_counted(self, external):
        result, target = self._fetch(external, ["../evil", "logo.png", "good-section"])
        assert result is True
        assert (target / "good-section.md").exists()
        assert not (target.parent / "evil.md").exists()
        assert not (target / "logo.png.md").exists()

        meta = json.loads(external.get_cache_metadata_path("forge").read_text())
        # Skipped sections stay in the denominator: hostile input drags the
        # rate below the 0.9 floor and the cache is immediately invalid, so
        # the next run retries rather than trusting a partial fetch.
        assert meta["success_rate"] == pytest.approx(1 / 3)
        assert external.is_cache_valid("forge") is False

    def test_all_sections_hostile_returns_false(self, external):
        result, target = self._fetch(external, ["../a", "..\\b"])
        assert result is False


class TestDiscoveryArbitration:
    def _fetch(self, external, manual, discovered):
        config = {
            "name": "Forge",
            "base_url": "https://forge.laravel.com/docs",
            "auto_discovery": True,
            "sections": manual,
        }
        external.auto_discovery.discover_sections = Mock(return_value=discovered)
        target = external.get_service_cache_path("forge")
        with patch.object(external, "_retry_request", return_value=GOOD_PAGE.encode()):
            assert external._fetch_service_documentation("forge", config, target) is True
        return json.loads(external.get_cache_metadata_path("forge").read_text())

    def test_thin_discovery_loses_to_manual(self, external):
        meta = self._fetch(external, manual=["a", "b", "c", "d"], discovered=["x", "y"])
        assert meta["discovery_method"] == "manual configuration"
        assert meta["total_sections"] == 4
        assert meta["manual_fallback"] is True

    def test_discovery_wins_at_three_quarters_threshold(self, external):
        meta = self._fetch(external, manual=["a", "b", "c", "d"], discovered=["x", "y", "z"])
        assert meta["discovery_method"] == "auto-discovery"
        assert meta["total_sections"] == 3
