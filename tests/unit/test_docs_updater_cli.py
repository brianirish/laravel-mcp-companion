"""docs_updater's own CLI: update_version, handle_update_command, and the
list/status commands of main() (docs_updater.py:3683-3880)."""

from unittest.mock import Mock, patch


import docs_updater
from docs_updater import handle_update_command, update_version


class TestUpdateVersion:
    def test_check_only_reports_without_updating(self, temp_dir):
        fake = Mock()
        fake.needs_update.return_value = True
        with patch.object(docs_updater, "DocsUpdater", return_value=fake) as cls:
            assert update_version(temp_dir, "12.x", force=False, check_only=True) == (True, True)
        cls.assert_called_once_with(temp_dir, "12.x")
        fake.update.assert_not_called()

    def test_update_path_returns_updated_flag(self, temp_dir):
        fake = Mock()
        fake.update.return_value = False
        with patch.object(docs_updater, "DocsUpdater", return_value=fake):
            assert update_version(temp_dir, "12.x", force=True, check_only=False) == (True, False)
        fake.update.assert_called_once_with(force=True)

    def test_failure_is_reported_not_raised(self, temp_dir):
        with patch.object(docs_updater, "DocsUpdater", side_effect=ValueError("bad version")):
            assert update_version(temp_dir, "nope", force=False, check_only=False) == (False, False)


class TestHandleUpdateCommand:
    def _args(self, force=False):
        return Mock(force=force)

    def test_success_exits_zero(self):
        updater = Mock()
        updater.update_all.return_value = {
            "core": True, "external": {"forge": True}, "packages": {"livewire": True},
        }
        assert handle_update_command(self._args(), updater) == 0

    def test_core_failure_exits_one(self):
        updater = Mock()
        updater.update_all.return_value = {"core": False, "external": {}, "packages": {}}
        assert handle_update_command(self._args(), updater) == 1

    def test_force_flag_fans_out(self):
        updater = Mock()
        updater.update_all.return_value = {"core": True, "external": {}, "packages": {}}
        handle_update_command(self._args(force=True), updater)
        updater.update_all.assert_called_once_with(
            force_core=True, force_external=True, force_packages=True, force_learning=True
        )


class TestMainCommands:
    def _run_main(self, monkeypatch, temp_dir, *flags):
        monkeypatch.setattr(
            "sys.argv",
            ["docs_updater.py", "--target-dir", str(temp_dir), "--version", "12.x", *flags],
        )
        return docs_updater.main()

    def test_list_services_prints_registry(self, monkeypatch, temp_dir, capsys):
        assert self._run_main(monkeypatch, temp_dir, "--list-services") == 0
        out = capsys.readouterr().out
        assert "Available Laravel Services:" in out
        for service in ("forge", "vapor", "envoyer", "nova"):
            assert service in out

    def test_list_packages_prints_subpackages(self, monkeypatch, temp_dir, capsys):
        assert self._run_main(monkeypatch, temp_dir, "--list-packages") == 0
        out = capsys.readouterr().out
        assert "Available Community Packages:" in out
        assert "spatie" in out
        assert "laravel-permission" in out  # a spatie sub-package line

    def test_status_reports_all_source_families(self, monkeypatch, temp_dir, capsys):
        assert self._run_main(monkeypatch, temp_dir, "--status") == 0
        out = capsys.readouterr().out
        assert "Documentation Status:" in out
        assert "Core Laravel Documentation (12.x):" in out
        assert "External Services:" in out
        assert "forge" in out
