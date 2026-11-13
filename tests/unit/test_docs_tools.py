"""list_laravel_docs, laravel_docs_info, compare_laravel_versions and update_laravel_docs."""

import json
import time
import urllib.error
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from laravel_mcp_companion.tools import ToolFailure
from laravel_mcp_companion.tools.docs import compare_versions, docs_info, list_docs, update_docs


@pytest.fixture
def docs(temp_dir):
    """Two Laravel versions, a service with nested pages, a package and a learning source."""
    root = temp_dir / "docs"
    for version, extra in (("11.x", "redirects.md"), ("12.x", "precognition.md")):
        version_dir = root / version
        (version_dir / ".metadata").mkdir(parents=True)
        for name in ("routing.md", "eloquent.md", extra):
            (version_dir / name).write_text(f"# {name}\n\n## Basics\n\nText for {version}.\n")
        (version_dir / ".metadata" / "sync_info.json").write_text(json.dumps({
            "version": version, "commit_sha": f"abc1234{version[:2]}", "commit_date": "2026-11-10T08:00:00Z",
            "commit_message": "Update docs", "commit_url": f"https://github.com/laravel/docs/commit/{version}",
            "sync_time": "2026-11-11T00:00:00Z",
        }))

    forge = root / "external" / "forge"
    (forge / "servers").mkdir(parents=True)
    (forge / "introduction.md").write_text("# Forge\n\n## Introduction\n\nServers.\n")
    (forge / "servers" / "php.md").write_text("# PHP\n\n## Versions\n\nPHP.\n")
    (forge / ".cache_metadata.json").write_text(json.dumps({
        "fetched_sections": ["introduction", "servers/php"], "total_sections": 2, "success_rate": 1.0,
        "discovery_method": "llms-index", "cached_at": time.time() - 3 * 86400,
    }))

    nova = root / "external" / "nova"
    nova.mkdir()
    (nova / "installation.md").write_text("# Installation\n\n## Requirements\n\nNova.\n")
    (nova / ".cache_metadata.json").write_text(json.dumps({
        "fetched_sections": ["installation"], "total_sections": 4, "success_rate": 0.25,
        "version": "v5", "cached_at": time.time(),
    }))

    livewire = root / "packages" / "livewire"
    (livewire / ".metadata").mkdir(parents=True)
    (livewire / "quickstart.md").write_text("# Quickstart\n\n## Install\n\nLivewire.\n")
    (livewire / ".metadata" / "cache.json").write_text(json.dumps({
        "sections_count": 1, "total_sections": 1, "success_rate": 1.0, "version": "4.x", "cached_at": time.time(),
    }))

    learn = root / "learning_resources" / "laravel-bootcamp"
    learn.mkdir(parents=True)
    (learn / "intro.md").write_text("# Intro\n\n## Start\n\nLearn.\n")
    return root


def collection(listing, name):
    return next(c for c in listing["collections"] if c["name"] == name)


class TestListEverything:
    def test_every_collection_is_listed_with_its_page_count(self, docs):
        listing = list_docs(docs)

        assert {(c["source"], c["name"], c["file_count"]) for c in listing["collections"]} == {
            ("core", "11.x", 3), ("core", "12.x", 3), ("services", "forge", 2), ("services", "nova", 1),
            ("packages", "livewire", 1), ("learning", "laravel-bootcamp", 1),
        }
        assert listing["count"] == 6

    def test_a_summary_does_not_carry_file_names(self, docs):
        assert all("files" not in c for c in list_docs(docs)["collections"])

    def test_metadata_directories_are_not_collections(self, docs):
        assert ".metadata" not in {c["name"] for c in list_docs(docs)["collections"]}

    def test_source_narrows_to_one_kind(self, docs):
        assert {c["name"] for c in list_docs(docs, source="services")["collections"]} == {"forge", "nova"}

    def test_an_unknown_source_is_refused(self, docs):
        with pytest.raises(ToolFailure) as raised:
            list_docs(docs, source="blogs")

        assert raised.value.code == "invalid_argument"


class TestListOneCollection:
    def test_a_version_lists_its_files_ready_for_the_read_tools(self, docs):
        listing = list_docs(docs, name="12.x")

        assert collection(listing, "12.x")["files"] == ["12.x/eloquent.md", "12.x/precognition.md", "12.x/routing.md"]

    def test_a_service_lists_nested_pages_with_their_paths(self, docs):
        assert collection(list_docs(docs, name="forge"), "forge")["files"] == ["forge/introduction.md", "forge/servers/php.md"]

    def test_a_name_that_matches_nothing_is_not_found(self, docs):
        with pytest.raises(ToolFailure) as raised:
            list_docs(docs, name="reverb")

        assert raised.value.code == "not_found"

    def test_a_name_in_the_wrong_source_is_not_found(self, docs):
        with pytest.raises(ToolFailure):
            list_docs(docs, source="packages", name="forge")

    def test_an_empty_tree_lists_nothing_and_is_not_an_error(self, temp_dir):
        assert list_docs(temp_dir) == {"count": 0, "collections": []}


class TestInfoForTheFrameworkDocs:
    def test_each_version_reports_its_date_and_commit(self, docs):
        info = docs_info(docs, runtime_version="12.x")
        twelve = next(v for v in info["versions"] if v["version"] == "12.x")

        assert twelve == {
            "version": "12.x", "available": True, "documentation_date": "2026-11-10", "last_synced": "2026-11-11",
            "commit": "abc1234", "commit_message": "Update docs",
            "commit_url": "https://github.com/laravel/docs/commit/12.x",
        }

    def test_a_version_with_no_copy_is_marked_unavailable(self, docs):
        info = docs_info(docs, runtime_version="12.x")

        assert {"version": "10.x", "available": False} in info["versions"]

    def test_the_headline_date_is_the_newest_change(self, docs):
        info = docs_info(docs, runtime_version="12.x")

        assert info["documentation_current_to"] == "2026-11-10"
        assert info["default_version"] == "12.x"
        assert isinstance(info["copy_age_days"], int)

    def test_one_version_can_be_asked_for(self, docs):
        assert [v["version"] for v in docs_info(docs, version="11.x")["versions"]] == ["11.x"]

    def test_an_empty_tree_reports_unknown_rather_than_failing(self, temp_dir):
        info = docs_info(temp_dir, runtime_version="12.x")

        assert info["documentation_current_to"] == "unknown"
        assert "copy_age_days" not in info


class TestInfoForEveryOtherSource:
    """The old tool reported the framework docs only, so it said "current"
    while every other fetcher could have been dead for a year."""

    def _source(self, docs, name):
        return next(s for s in docs_info(docs, runtime_version="12.x")["sources"] if s["name"] == name)

    def test_a_complete_source_is_ok_with_its_page_count_and_sync_date(self, docs):
        forge = self._source(docs, "forge")

        assert (forge["kind"], forge["status"], forge["pages"], forge["pages_expected"]) == ("service", "ok", 2, 2)
        assert forge["last_synced"]

    def test_a_copy_that_is_a_few_days_old_is_still_ok(self, docs):
        """Age alone is not a fault at runtime: an image pulled last week holds
        last week's sync. The pipeline's two-day rule does not apply here."""
        assert self._source(docs, "forge")["status"] == "ok"

    def test_a_source_that_fetched_too_little_is_partial_and_says_so(self, docs):
        nova = self._source(docs, "nova")

        assert (nova["status"], nova["pages"], nova["pages_expected"]) == ("partial", 1, 4)
        assert nova["problem"] == "fetched 1 of 4 pages"

    def test_the_major_version_a_source_is_on_is_reported(self, docs):
        assert self._source(docs, "nova")["version"] == "v5"
        assert self._source(docs, "livewire")["version"] == "4.x"

    def test_a_configured_source_with_no_copy_is_missing(self, docs):
        assert self._source(docs, "cloud")["status"] == "missing"

    def test_every_configured_source_appears(self, docs):
        names = {s["name"] for s in docs_info(docs, runtime_version="12.x")["sources"]}

        assert {"forge", "vapor", "envoyer", "nova", "cloud", "nightwatch", "herd", "livewire", "filament",
                "inertia", "spatie/laravel-permission", "laravel-bootcamp", "laracasts-index"} <= names


class TestCompare:
    def test_pages_only_in_the_newer_version_are_added(self, docs):
        assert compare_versions(docs, "11.x", "12.x")["added_files"] == ["precognition.md"]

    def test_pages_only_in_the_older_version_are_removed(self, docs):
        assert compare_versions(docs, "11.x", "12.x")["removed_files"] == ["redirects.md"]

    def test_pages_in_both_are_common(self, docs):
        assert compare_versions(docs, "11.x", "12.x")["common_files"] == ["eloquent.md", "routing.md"]

    def test_a_filter_keeps_only_matching_pages_and_is_echoed(self, docs):
        result = compare_versions(docs, "11.x", "12.x", file_filter="ELOQ")

        assert (result["common_files"], result["added_files"], result["filter"]) == (["eloquent.md"], [], "ELOQ")

    def test_comparing_a_version_with_itself_is_refused(self, docs):
        with pytest.raises(ToolFailure) as raised:
            compare_versions(docs, "12.x", "12.x")

        assert raised.value.code == "invalid_argument"

    def test_a_supported_version_with_no_copy_is_not_found(self, docs):
        with pytest.raises(ToolFailure) as raised:
            compare_versions(docs, "10.x", "12.x")

        assert raised.value.code == "not_found"


@pytest.fixture
def server(docs):
    """A stand-in for the server context whose fetchers record what they are asked."""
    def fetcher(method, lister, names):
        mock = Mock()
        getattr(mock, lister).return_value = list(names)
        getattr(mock, method).side_effect = lambda name, force=False: name != "broken"
        return mock

    updater = SimpleNamespace(
        external_fetcher=fetcher("fetch_laravel_service_docs", "list_available_services", ["forge", "nova", "broken"]),
        package_fetcher=fetcher("fetch_package_docs", "list_available_packages", ["livewire"]),
        learning_fetcher=fetcher("fetch_learning_source", "list_available_sources", ["laravel-bootcamp"]),
    )
    return SimpleNamespace(docs_path=docs, runtime_version="12.x", updater=updater)


def framework_update(result=True, error=None):
    updater = Mock()
    updater.update.side_effect = error
    updater.update.return_value = result
    return patch("laravel_mcp_companion.tools.docs.DocsUpdater", return_value=updater)


class TestUpdateTheFrameworkDocs:
    def test_a_change_is_reported_with_the_commit_now_held(self, server):
        with framework_update(True) as updater:
            result = update_docs(server)

        assert result == {"scope": "core", "results": [
            {"source": "core", "name": "12.x", "outcome": "updated", "commit": "abc1234"},
        ]}
        updater.assert_called_once_with(server.docs_path, "12.x")

    def test_nothing_new_is_unchanged_not_a_failure(self, server):
        with framework_update(False):
            assert update_docs(server)["results"][0]["outcome"] == "unchanged"

    def test_a_named_version_is_the_one_updated(self, server):
        with framework_update(True) as updater:
            update_docs(server, version="11.x", force=True)

        updater.assert_called_once_with(server.docs_path, "11.x")
        updater.return_value.update.assert_called_once_with(force=True)

    def test_a_failure_is_an_update_failed_error(self, server):
        with framework_update(error=urllib.error.URLError("github is unreachable")):
            with pytest.raises(ToolFailure) as raised:
                update_docs(server)

        assert raised.value.code == "update_failed"
        assert raised.value.details == {"version": "12.x"}

    def test_caches_are_cleared_after_a_change(self, server):
        with framework_update(True), patch("laravel_mcp_companion.tools.docs.mcp_tools.clear_caches") as clear:
            update_docs(server)

        clear.assert_called_once()

    def test_caches_are_left_alone_when_nothing_changed(self, server):
        with framework_update(False), patch("laravel_mcp_companion.tools.docs.mcp_tools.clear_caches") as clear:
            update_docs(server)

        clear.assert_not_called()


class TestUpdateOtherSources:
    def test_a_scope_refetches_every_source_of_that_kind(self, server):
        result = update_docs(server, scope="services")

        assert result["results"] == [
            {"source": "services", "name": "forge", "outcome": "updated"},
            {"source": "services", "name": "nova", "outcome": "updated"},
            {"source": "services", "name": "broken", "outcome": "failed"},
        ]

    def test_names_restrict_the_refetch(self, server):
        update_docs(server, scope="services", names=["nova"], force=True)

        server.updater.external_fetcher.fetch_laravel_service_docs.assert_called_once_with("nova", force=True)

    def test_an_unknown_name_is_refused_before_anything_is_fetched(self, server):
        with pytest.raises(ToolFailure) as raised:
            update_docs(server, scope="services", names=["forge", "reverb"])

        assert raised.value.code == "invalid_argument"
        assert raised.value.details["available"] == ["forge", "nova", "broken"]
        server.updater.external_fetcher.fetch_laravel_service_docs.assert_not_called()

    def test_all_updates_everything(self, server):
        with framework_update(True):
            result = update_docs(server, scope="all")

        assert {(r["source"], r["name"]) for r in result["results"]} == {
            ("core", "12.x"), ("services", "forge"), ("services", "nova"), ("services", "broken"),
            ("packages", "livewire"), ("learning", "laravel-bootcamp"),
        }

    def test_with_all_a_framework_failure_is_reported_and_the_rest_still_runs(self, server):
        with framework_update(error=urllib.error.URLError("github is unreachable")):
            result = update_docs(server, scope="all")

        assert {"source": "core", "name": "12.x", "outcome": "failed"} in result["results"]
        assert {"source": "packages", "name": "livewire", "outcome": "updated"} in result["results"]

    def test_names_make_no_sense_with_the_framework_docs(self, server):
        with pytest.raises(ToolFailure) as raised:
            update_docs(server, scope="core", names=["forge"])

        assert raised.value.code == "invalid_argument"

    def test_an_unknown_scope_is_refused(self, server):
        with pytest.raises(ToolFailure) as raised:
            update_docs(server, scope="everything")

        assert raised.value.details["valid_scopes"] == ["core", "services", "packages", "learning", "all"]
