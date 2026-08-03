"""MultiSourceDocsUpdater orchestration paths (docs_updater.py:2692-3006).

The composed fetchers have no injection point, so tests patch the composed
instances' methods directly. Existing tests cover __init__/update_core_docs/
update_external_docs/get_all_documentation_status basics — these cover the
package/learning delegation, update_all, and needs_update, which were red.
"""

import json
import time
from unittest.mock import Mock

import pytest

from docs_updater import MultiSourceDocsUpdater


@pytest.fixture
def updater(temp_dir):
    return MultiSourceDocsUpdater(temp_dir, "12.x")


class TestUpdatePackageDocs:
    def test_named_packages_delegate_and_report(self, updater):
        updater.package_fetcher.fetch_package_docs = Mock(side_effect=[True, False])
        results = updater.update_package_docs(packages=["livewire", "filament"], force=True)
        assert results == {"livewire": True, "filament": False}
        updater.package_fetcher.fetch_package_docs.assert_any_call("livewire", force=True)

    def test_unknown_package_is_false_without_delegation(self, updater):
        updater.package_fetcher.fetch_package_docs = Mock()
        results = updater.update_package_docs(packages=["not-a-package"])
        assert results == {"not-a-package": False}
        updater.package_fetcher.fetch_package_docs.assert_not_called()

    def test_no_packages_means_all(self, updater):
        updater.package_fetcher.fetch_all_packages = Mock(return_value={"livewire": True})
        assert updater.update_package_docs() == {"livewire": True}
        updater.package_fetcher.fetch_all_packages.assert_called_once_with(force=False)


class TestUpdateLearningDocs:
    def test_named_sources_delegate(self, updater):
        updater.learning_fetcher.fetch_learning_source = Mock(return_value=True)
        results = updater.update_learning_docs(sources=["laravel-blog"], force=True)
        assert results == {"laravel-blog": True}
        updater.learning_fetcher.fetch_learning_source.assert_called_once_with(
            "laravel-blog", force=True
        )

    def test_unknown_source_is_false(self, updater):
        results = updater.update_learning_docs(sources=["udemy"])
        assert results == {"udemy": False}

    def test_no_sources_means_all(self, updater):
        updater.learning_fetcher.fetch_all_sources = Mock(return_value={"laravel-blog": True})
        assert updater.update_learning_docs() == {"laravel-blog": True}


class TestUpdateAll:
    def _stub_all(self, updater, **overrides):
        updater.update_core_docs = Mock(return_value=overrides.get("core", True))
        updater.update_external_docs = Mock(return_value=overrides.get("external", {"forge": True}))
        updater.update_package_docs = Mock(return_value=overrides.get("packages", {"livewire": True}))
        updater.update_learning_docs = Mock(return_value=overrides.get("learning", {"laravel-blog": True}))

    def test_all_sections_updated_and_reported(self, updater):
        self._stub_all(updater)
        results = updater.update_all(force_core=True, force_external=True,
                                     force_packages=True, force_learning=True)
        assert results == {
            "core": True,
            "external": {"forge": True},
            "packages": {"livewire": True},
            "learning": {"laravel-blog": True},
        }
        updater.update_core_docs.assert_called_once_with(force=True)
        updater.update_external_docs.assert_called_once_with(force=True)
        updater.update_package_docs.assert_called_once_with(force=True)
        updater.update_learning_docs.assert_called_once_with(force=True)

    def test_midway_exception_returns_partial_results(self, updater):
        """update_all swallows the exception (:2806) and returns what it has:
        core landed, everything after the blast stays at its initial value."""
        self._stub_all(updater)
        updater.update_external_docs = Mock(side_effect=RuntimeError("upstream down"))
        results = updater.update_all()
        assert results["core"] is True
        assert results["external"] == {}
        assert results["packages"] == {}
        assert results["learning"] == {}
        updater.update_package_docs.assert_not_called()


class TestNeedsUpdate:
    def test_check_flags_gate_each_section(self, updater):
        updater.core_updater.needs_update = Mock(return_value=False)
        result = updater.needs_update(check_external=False, check_packages=False,
                                      check_learning=False)
        assert result == {"core": False, "external": {}, "packages": {}, "learning": {}}

    def test_core_check_error_defaults_to_true(self, updater):
        updater.core_updater.needs_update = Mock(side_effect=OSError("no metadata"))
        result = updater.needs_update(check_external=False, check_packages=False,
                                      check_learning=False)
        assert result["core"] is True

    def test_sections_reflect_cache_validity(self, updater):
        updater.core_updater.needs_update = Mock(return_value=False)
        updater.external_fetcher.is_cache_valid = Mock(return_value=True)
        updater.package_fetcher.is_cache_valid = Mock(return_value=False)
        updater.learning_fetcher.is_cache_valid = Mock(side_effect=OSError("boom"))
        result = updater.needs_update()
        assert all(v is False for v in result["external"].values())
        assert all(v is True for v in result["packages"].values())
        # a check that blows up counts as "needs update", not "fine"
        assert all(v is True for v in result["learning"].values())
        assert set(result["learning"]) == set(updater.learning_fetcher.learning_sources)


class TestStatusLearningSection:
    def test_learning_status_reports_cached_source(self, updater):
        meta_path = updater.learning_fetcher.get_cache_metadata_path("laravel-blog")
        meta_path.write_text(json.dumps({
            "success_rate": 1.0, "cached_at": time.time(), "article_count": 4,
        }))
        status = updater.get_all_documentation_status()
        blog = status["learning"]["laravel-blog"]
        assert blog["cache_valid"] is True
        assert blog["success_rate"] == 1.0
        assert blog["last_fetched"] != "never"
        # uncached sources report never
        assert status["learning"]["laravel-news"]["last_fetched"] == "never"
