"""The curated tables must agree with the documentation that is shipped.

The package catalog, the need table, the learning paths, the difficulty map
and the categories are written by hand. They were written once and not
revisited: by 2026 twenty-three need mappings and the first learning path
pointed at pages that no longer existed, nine difficulty entries named no
page, and Laravel Cloud, Nightwatch, Herd, Pest, Reverb and Pulse appeared
nowhere while two retired starter kits were recommended.

These tests make that kind of drift a failing build. They compare the tables
with each other, and, in the tests marked `corpus`, with the documentation in
`docs/` for the newest Laravel version.

The `corpus` tests are left out of CI for the nightly documentation pull
request. That pull request is where a page Laravel added or removed first
shows up, and failing it would hold back every other page of that night's
documentation. The sync report raises the same findings there, and every
later pull request fails here until the tables are brought up to date.
"""

import json
import re
from pathlib import Path

import pytest

from laravel_mcp_companion import catalog, curation
from laravel_mcp_companion.docs_updater import DEFAULT_VERSION
from laravel_mcp_companion.learning_resources import (
    LEARNING_PATHS,
    NEED_MAPPINGS,
    RELATED_PACKAGES,
    categories_of,
)

REPO_DOCS = Path(__file__).resolve().parents[2] / "docs"


@pytest.mark.corpus
class TestTheTablesAgreeWithTheCorpus:
    """Each kind of disagreement `curation.audit` reports, against the corpus
    this repository ships. Marked `corpus`: CI leaves these out for the
    nightly documentation pull request, whose whole content is a change to
    the corpus, and the sync report raises them there instead."""

    @pytest.mark.parametrize("kind", sorted(curation.DESCRIPTIONS))
    def test_nothing_of_this_kind(self, kind):
        assert curation.audit(REPO_DOCS)[kind] == [], curation.DESCRIPTIONS[kind]

    def test_every_service_a_path_names_has_documentation_held(self):
        held = {path.name for path in (REPO_DOCS / "external").iterdir() if path.is_dir()}

        assert [
            (path_id, sorted(set(path["services"]) - held))
            for path_id, path in LEARNING_PATHS.items() if set(path.get("services", [])) - held
        ] == []


@pytest.fixture
def small_corpus(tmp_path):
    """A version directory holding only the pages named."""
    def build(*pages):
        version_dir = tmp_path / DEFAULT_VERSION
        version_dir.mkdir(exist_ok=True)
        for page in pages:
            (version_dir / f"{page}.md").write_text(f"# {page}\n")
        return tmp_path
    return build


class TestWhatTheAuditNotices:
    def test_a_need_pointing_at_a_page_that_was_removed(self, small_corpus):
        problems = curation.audit(small_corpus("routing"))

        assert "send emails -> mail" in problems["dead_need_targets"]

    def test_a_learning_path_listing_a_page_that_was_removed(self, small_corpus):
        problems = curation.audit(small_corpus("routing"))

        assert "getting-started -> installation" in problems["dead_path_docs"]

    def test_a_page_laravel_added_that_no_table_mentions(self, small_corpus):
        problems = curation.audit(small_corpus("routing", "teleportation"))

        assert "teleportation" in problems["uncategorised_pages"]
        assert "teleportation" in problems["pages_without_difficulty"]
        assert "teleportation" in problems["unreached_pages"]

    def test_pages_about_the_documentation_itself_need_no_mapping(self, small_corpus):
        problems = curation.audit(small_corpus("routing", "readme", "license"))

        assert not {"readme", "license"} & set(problems["uncategorised_pages"])

    def test_a_version_with_no_pages_is_not_audited(self, tmp_path):
        assert curation.audit(tmp_path) == {}

    def test_the_sync_report_raises_what_the_audit_finds(self, small_corpus):
        from laravel_mcp_companion.docs_updater import build_sync_report

        report, problems = build_sync_report(small_corpus("routing", "teleportation"))
        raised = [problem for problem in problems if problem.startswith("curated tables:")]

        assert any("framework pages in no category (teleportation)" in problem for problem in raised)
        assert "- curated tables:" in report

    def test_a_short_keyword_does_not_select_pages_that_merely_contain_it(self):
        """Matching by substring put mail and container in the "ai" category."""
        assert "ai" in categories_of("ai-sdk")
        assert "ai" not in categories_of("mail")
        assert "ai" not in categories_of("container")


class TestLearningPathsAreWellFormed:
    def test_every_prerequisite_is_a_path(self):
        assert [
            (path_id, sorted(set(path["prerequisites"]) - set(LEARNING_PATHS)))
            for path_id, path in LEARNING_PATHS.items()
            if set(path.get("prerequisites", [])) - set(LEARNING_PATHS)
        ] == []

    def test_every_next_path_is_a_path(self):
        assert [
            (path_id, path["next_path"]) for path_id, path in LEARNING_PATHS.items()
            if path.get("next_path") and path["next_path"] not in LEARNING_PATHS
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

    def test_no_need_is_left_pointing_at_nothing(self):
        assert [need for need, targets in NEED_MAPPINGS.items() if not targets] == []


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


@pytest.mark.corpus
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
