"""`--update` exits 0 when it worked, whether or not anything changed.

Its exit code was computed from `results["core"]`, which is whether the
framework docs changed. On any run where they were already current the
command exited 1, the same as a failure. The nightly pipeline had stopped
reading the code for that reason.
"""

import urllib.error
from unittest.mock import Mock

import pytest

from laravel_mcp_companion import docs_updater
from laravel_mcp_companion.docs_updater import MultiSourceDocsUpdater


@pytest.fixture
def updater(temp_dir):
    updater = MultiSourceDocsUpdater(temp_dir, "12.x")
    updater.update_external_docs = Mock(return_value={"forge": True, "vapor": True})
    updater.update_package_docs = Mock(return_value={"livewire": True})
    updater.update_learning_docs = Mock(return_value={"laravel-bootcamp": True})
    return updater


def run_update(monkeypatch, temp_dir, updater):
    monkeypatch.setattr("sys.argv", ["docs_updater", "--target-dir", str(temp_dir), "--update"])
    monkeypatch.setattr(docs_updater, "MultiSourceDocsUpdater", lambda *a, **k: updater)
    return docs_updater.main()


class TestUpdateExitCode:
    def test_framework_docs_already_current_is_a_success(self, monkeypatch, temp_dir, updater):
        updater.core_updater.update = Mock(return_value=False)

        assert run_update(monkeypatch, temp_dir, updater) == 0

    def test_framework_docs_that_changed_is_a_success(self, monkeypatch, temp_dir, updater):
        updater.core_updater.update = Mock(return_value=True)

        assert run_update(monkeypatch, temp_dir, updater) == 0

    def test_a_framework_update_that_fails_is_a_failure(self, monkeypatch, temp_dir, updater):
        updater.core_updater.update = Mock(side_effect=urllib.error.URLError("github is unreachable"))

        assert run_update(monkeypatch, temp_dir, updater) == 1

    def test_a_failed_framework_update_does_not_stop_the_other_sources(self, monkeypatch, temp_dir, updater):
        updater.core_updater.update = Mock(side_effect=urllib.error.URLError("github is unreachable"))

        run_update(monkeypatch, temp_dir, updater)

        updater.update_external_docs.assert_called_once()
        updater.update_package_docs.assert_called_once()

    def test_every_service_and_package_failing_is_a_failure(self, monkeypatch, temp_dir, updater):
        updater.core_updater.update = Mock(return_value=False)
        updater.update_external_docs = Mock(return_value={"forge": False, "vapor": False})
        updater.update_package_docs = Mock(return_value={"livewire": False})

        assert run_update(monkeypatch, temp_dir, updater) == 1
