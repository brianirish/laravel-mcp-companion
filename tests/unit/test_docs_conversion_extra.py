"""Conversion edges: JSX extraction, HTML content-area fallback, and the
section-sanitization skip branches inside the service fetch loop."""


import pytest

from laravel_mcp_companion.docs_updater import CommunityPackageFetcher, ExternalDocsFetcher
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


