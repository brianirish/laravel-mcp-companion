"""The curated tables must agree with the documentation that is shipped.

The package catalog, the need table, the learning paths, the difficulty map
and the categories are written by hand. They were written once and not
revisited: by 2026 twenty-three need mappings and the first learning path
pointed at pages that no longer existed, nine difficulty entries named no
page, and Laravel Cloud, Nightwatch, Herd, Pest, Reverb and Pulse appeared
nowhere while two retired starter kits were recommended.

These tests make that kind of drift a failing build. They compare every
reference in the tables with the corpus in `docs/`, for the newest Laravel
version, and the tables with each other. When Laravel adds or removes a page,
the nightly documentation pull request fails here until the tables say where
the page belongs.
"""

import json
import re
from pathlib import Path

import pytest

from laravel_mcp_companion import catalog
from laravel_mcp_companion.docs_updater import DEFAULT_VERSION
from laravel_mcp_companion.learning_resources import (
    EXPANDED_CATEGORIES,
    LEARNING_PATHS,
    NEED_MAPPINGS,
    RELATED_PACKAGES,
    TOPIC_DIFFICULTY_MAP,
    categories_of,
    keyword_selects,
)

REPO_DOCS = Path(__file__).resolve().parents[2] / "docs"
NEWEST = REPO_DOCS / DEFAULT_VERSION

pytestmark = pytest.mark.skipif(not NEWEST.is_dir(), reason="shipped corpus absent")

# Pages about the documentation itself, not about Laravel.
NOT_CONTENT = {"readme", "license", "documentation", "contributions"}


def pages() -> set:
    return {path.stem for path in NEWEST.glob("*.md")}


def content_pages() -> set:
    return pages() - NOT_CONTENT


class TestEveryReferenceResolves:
    def test_every_need_points_at_pages_that_exist(self):
        dead = {need: sorted(set(targets) - pages()) for need, targets in NEED_MAPPINGS.items() if set(targets) - pages()}

        assert dead == {}

    def test_no_need_is_left_pointing_at_nothing(self):
        assert [need for need, targets in NEED_MAPPINGS.items() if not targets] == []

    def test_every_learning_path_lists_pages_that_exist(self):
        dead = {
            path_id: sorted(set(path["docs"]) - pages())
            for path_id, path in LEARNING_PATHS.items() if set(path["docs"]) - pages()
        }

        assert dead == {}

    def test_every_prerequisite_is_a_path(self):
        assert [
            (path_id, sorted(set(path["prerequisites"]) - set(LEARNING_PATHS)))
            for path_id, path in LEARNING_PATHS.items()
            if set(path.get("prerequisites", [])) - set(LEARNING_PATHS)
        ] == []

    def test_every_service_a_path_names_has_documentation_held(self):
        held = {path.name for path in (REPO_DOCS / "external").iterdir() if path.is_dir()}

        assert [
            (path_id, sorted(set(path["services"]) - held))
            for path_id, path in LEARNING_PATHS.items() if set(path.get("services", [])) - held
        ] == []

    def test_every_package_a_path_names_is_catalogued(self):
        assert [
            (path_id, sorted(set(path["packages"]) - set(catalog.PACKAGE_CATALOG)))
            for path_id, path in LEARNING_PATHS.items()
            if set(path.get("packages", [])) - set(catalog.PACKAGE_CATALOG)
        ] == []

    def test_no_path_recommends_a_legacy_package_or_service(self):
        legacy = {package_id for package_id, entry in catalog.PACKAGE_CATALOG.items() if entry.get("legacy")}
        legacy_services = {package_id.split("/")[1] for package_id in legacy}

        for path_id, path in LEARNING_PATHS.items():
            assert not set(path.get("packages", [])) & legacy, path_id
            assert not set(path.get("services", [])) & legacy_services, path_id

    def test_a_path_uses_only_the_fields_the_tool_returns(self):
        known = {"name", "description", "difficulty", "estimated_hours", "docs", "prerequisites", "services", "packages", "next_path"}

        assert {path_id: sorted(set(path) - known) for path_id, path in LEARNING_PATHS.items() if set(path) - known} == {}

    def test_every_next_path_is_a_path(self):
        assert [
            (path_id, path["next_path"]) for path_id, path in LEARNING_PATHS.items()
            if path.get("next_path") and path["next_path"] not in LEARNING_PATHS
        ] == []

    def test_every_difficulty_entry_names_a_page(self):
        assert sorted(set(TOPIC_DIFFICULTY_MAP) - pages()) == []

    def test_every_category_keyword_matches_a_page(self):
        """A keyword selects the page of that name and any page whose name
        extends it with a hyphen. One that selects nothing is a leftover from
        a page that was renamed or removed."""
        dead = {
            category: [keyword for keyword in keywords if not any(keyword_selects(keyword, page) for page in pages())]
            for category, keywords in EXPANDED_CATEGORIES.items()
        }

        assert {category: keywords for category, keywords in dead.items() if keywords} == {}


class TestEveryPageIsReachable:
    """A page nobody mapped can still be found by searching, but it is missing
    from every browse, every reading order and every difficulty filter."""

    def test_every_page_is_in_a_category(self):
        assert sorted(page for page in content_pages() if not categories_of(page)) == []

    def test_a_short_keyword_does_not_select_pages_that_merely_contain_it(self):
        """Matching by substring put mail and container in the "ai" category."""
        assert "ai" in categories_of("ai-sdk")
        assert "ai" not in categories_of("mail")
        assert "ai" not in categories_of("container")

    def test_every_page_has_a_difficulty(self):
        assert sorted(content_pages() - set(TOPIC_DIFFICULTY_MAP)) == []

    def test_every_page_is_reached_by_a_need_or_a_learning_path(self):
        reached = {target for targets in NEED_MAPPINGS.values() for target in targets}
        reached |= {doc for path in LEARNING_PATHS.values() for doc in path["docs"]}

        assert sorted(content_pages() - reached) == []


class TestTheCatalogIsWhole:
    def test_every_package_has_a_feature_list(self):
        assert sorted(set(catalog.PACKAGE_CATALOG) - set(catalog.FEATURE_MAP)) == []

    def test_every_feature_list_belongs_to_a_package(self):
        assert sorted(set(catalog.FEATURE_MAP) - set(catalog.PACKAGE_CATALOG)) == []

    def test_every_package_has_a_relations_row(self):
        """An empty list is an answer; a missing row is an oversight."""
        assert sorted(set(catalog.PACKAGE_CATALOG) - set(RELATED_PACKAGES)) == []

    def test_every_relation_points_at_a_catalogued_package(self):
        known = set(catalog.PACKAGE_CATALOG)
        dead = {package: sorted(set(related) - known) for package, related in RELATED_PACKAGES.items() if set(related) - known}

        assert dead == {}
        assert sorted(set(RELATED_PACKAGES) - known) == []

    def test_no_package_is_related_to_itself(self):
        assert [package for package, related in RELATED_PACKAGES.items() if package in related] == []

    @pytest.mark.parametrize("package_id", sorted(catalog.PACKAGE_CATALOG))
    def test_every_entry_says_how_to_get_it_and_where_its_docs_are(self, package_id):
        entry = catalog.PACKAGE_CATALOG[package_id]

        assert entry.get("installation"), "no installation line"
        assert entry.get("documentation_link"), "no documentation link"

    def test_what_supersedes_a_legacy_package_is_itself_current(self):
        for package_id, entry in catalog.PACKAGE_CATALOG.items():
            successor = entry.get("superseded_by")
            if successor in catalog.PACKAGE_CATALOG:
                assert not catalog.PACKAGE_CATALOG[successor].get("legacy"), (package_id, successor)

    def test_only_a_legacy_package_names_a_successor(self):
        assert [
            package_id for package_id, entry in catalog.PACKAGE_CATALOG.items()
            if entry.get("superseded_by") and not entry.get("legacy")
        ] == []


class TestTheCatalogIsCurrent:
    CURRENT = [
        "laravel/cloud", "laravel/nightwatch", "laravel/herd", "pestphp/pest", "laravel/reverb", "laravel/pulse",
        "laravel/pennant", "laravel/folio", "filament/filament", "laravel/sail", "laravel/pint", "laravel/prompts",
    ]
    LEGACY = [
        "laravel/vapor", "laravel/envoyer", "laravel/homestead", "laravel/valet", "laravel/breeze",
        "laravel/jetstream", "livewire/volt",
    ]

    @pytest.mark.parametrize("package_id", CURRENT)
    def test_a_current_first_party_product_is_catalogued(self, package_id):
        assert package_id in catalog.PACKAGE_CATALOG
        assert not catalog.PACKAGE_CATALOG[package_id].get("legacy")

    @pytest.mark.parametrize("package_id", LEGACY)
    def test_a_superseded_product_is_kept_and_flagged(self, package_id):
        """Kept, because people maintaining older applications still need
        them; flagged, so a recommendation prefers what replaced them."""
        assert catalog.PACKAGE_CATALOG[package_id].get("legacy") is True

    @pytest.mark.parametrize("need,legacy", [
        ("deploy my application", {"laravel/vapor", "laravel/envoyer"}),
        ("authentication scaffolding", {"laravel/breeze", "laravel/jetstream"}),
        ("local development environment", {"laravel/homestead", "laravel/valet"}),
    ])
    def test_a_recommendation_leads_with_something_current(self, need, legacy):
        ranked = [match["id"] for match in catalog.search_by_use_case(need)]

        assert ranked, f"nothing recommended for {need!r}"
        assert ranked[0] not in legacy, ranked[:4]

    def test_octane_names_the_servers_its_documentation_does(self):
        description = catalog.PACKAGE_CATALOG["laravel/octane"]["description"]

        assert all(server in description for server in ("FrankenPHP", "RoadRunner", "Swoole"))

    def test_socialite_lists_the_providers_its_documentation_does(self):
        description = catalog.PACKAGE_CATALOG["laravel/socialite"]["description"]

        assert "Twitter" not in description
        assert all(provider in description for provider in ("X", "Slack", "GitHub", "Google"))

    def test_scout_names_every_engine_its_documentation_does(self):
        text = json.dumps(catalog.PACKAGE_CATALOG["laravel/scout"]) + json.dumps(catalog.FEATURE_MAP["laravel/scout"])

        assert all(engine in text.lower() for engine in ("algolia", "meilisearch", "typesense", "database"))


class TestNoVersionOlderThanTheDocsHeld:
    """The fetchers follow each package's current major. Catalog prose that
    names an older one describes software the shipped docs no longer cover."""

    HELD = {
        "livewire/livewire": ("packages/livewire/.metadata/cache.json", "Livewire"),
        "filament/filament": ("packages/filament/.metadata/cache.json", "Filament"),
        "inertiajs/inertia-laravel": ("packages/inertia/.metadata/cache.json", "Inertia"),
        "spatie/laravel-permission": ("packages/spatie/laravel-permission/.metadata/cache.json", "Permission"),
        "spatie/laravel-medialibrary": ("packages/spatie/laravel-medialibrary/.metadata/cache.json", "Media ?Library"),
        "laravel/nova": ("external/nova/.cache_metadata.json", "Nova"),
    }

    @pytest.mark.parametrize("package_id", sorted(HELD))
    def test_the_entry_names_no_major_below_the_one_held(self, package_id):
        metadata_path, name = self.HELD[package_id]
        metadata = json.loads((REPO_DOCS / metadata_path).read_text())
        held = int(re.search(r"\d+", str(metadata["version"])).group())
        entry = catalog.PACKAGE_CATALOG[package_id]
        prose = " ".join([entry["description"], *entry.get("use_cases", []), entry.get("installation", "")])

        mentioned = [int(number) for number in re.findall(rf"(?:{name})\s+v?(\d+)", prose)]
        mentioned += [int(number) for number in re.findall(r":\"?\^(\d+)", entry.get("installation", ""))]

        assert [major for major in mentioned if major < held] == []
