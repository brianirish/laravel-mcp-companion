"""Cheaply-testable README claims, guarded so they cannot rot.

Born from the 2026-08 claims audit (docs/superpowers/specs/
2026-08-03-claims-audit-notes.md): "50+ curated packages" had drifted from a
22-entry catalog, and the search description advertised a contract two
releases dead.
"""

import re
from pathlib import Path

import pytest

from laravel_mcp_companion import PACKAGE_CATALOG, TOOL_DESCRIPTIONS

REPO_ROOT = Path(__file__).resolve().parents[2]


def readme() -> str:
    return (REPO_ROOT / "README.md").read_text(encoding="utf-8")


def test_curated_package_count_matches_catalog():
    matches = re.findall(r"(\d+)\+? curated packages", readme())
    assert matches, "README no longer states the curated-package count"
    for figure in matches:
        assert int(figure) == len(PACKAGE_CATALOG), (
            f"README claims {figure} curated packages; the catalog has "
            f"{len(PACKAGE_CATALOG)}"
        )


def test_search_description_matches_the_actual_contract():
    description = TOOL_DESCRIPTIONS["search_laravel_docs"]
    assert "match counts" not in description  # the pre-v0.11 contract
    assert "ranked" in description.lower()
    assert "sources" in description


@pytest.mark.skipif(
    not (REPO_ROOT / "docs" / "packages").is_dir(), reason="shipped corpus absent"
)
def test_named_package_ecosystems_are_fetched():
    fetched = {p.name for p in (REPO_ROOT / "docs" / "packages").iterdir() if p.is_dir()}
    for name in ("spatie", "livewire", "inertia", "filament"):
        assert name in fetched, f"README names {name} but it is not fetched"
