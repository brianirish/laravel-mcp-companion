"""Where the server reads documentation from, and where an update writes it.

A checkout and the Docker image hold one copy of the documentation, beside
the package, and update it in place. An installed wheel holds its copy inside
the package directory: a reinstall replaces it, and some environments cannot
write there. So on a wheel install an update goes to a directory of the
user's own, and the server reads whichever copy is newer.
"""

import json
from pathlib import Path

import pytest

from laravel_mcp_companion import docs_location


def make_docs(root: Path, date: str, marker: str = "") -> Path:
    """A minimal corpus whose newest upstream change is `date`."""
    version = root / "12.x"
    (version / ".metadata").mkdir(parents=True)
    (version / "queues.md").write_text(f"# Queues\n\n{marker}\n", encoding="utf-8")
    (version / ".metadata" / "sync_info.json").write_text(
        json.dumps({"commit_date": f"{date}T00:00:00Z", "sync_time": f"{date}T01:00:00Z"}),
        encoding="utf-8",
    )
    return root


@pytest.fixture
def wheel(tmp_path, monkeypatch):
    """An installed wheel: docs inside the package, and a user directory."""
    package = tmp_path / "site-packages" / "laravel_mcp_companion"
    bundled = make_docs(package / "docs", "2026-06-01", "bundled")
    home = tmp_path / "home"
    monkeypatch.setattr(docs_location, "PACKAGE_DIR", package)
    monkeypatch.setenv(docs_location.ENV_HOME, str(home))
    return bundled, home / "docs"


@pytest.fixture
def checkout(tmp_path, monkeypatch):
    """A source checkout or the Docker image: docs beside the package."""
    package = tmp_path / "repo" / "laravel_mcp_companion"
    package.mkdir(parents=True)
    beside = make_docs(tmp_path / "repo" / "docs", "2026-06-01", "beside")
    home = tmp_path / "home"
    monkeypatch.setattr(docs_location, "PACKAGE_DIR", package)
    monkeypatch.setenv(docs_location.ENV_HOME, str(home))
    return beside, home / "docs"


class TestTheUserDirectory:
    def test_the_environment_variable_names_it(self, tmp_path, monkeypatch):
        monkeypatch.setenv(docs_location.ENV_HOME, str(tmp_path / "elsewhere"))
        assert docs_location.user_docs_path() == tmp_path / "elsewhere" / "docs"

    def test_without_the_variable_it_is_a_per_user_data_directory(self, monkeypatch):
        monkeypatch.delenv(docs_location.ENV_HOME, raising=False)
        path = docs_location.user_docs_path()
        assert path.name == "docs"
        assert path.parent.name == "laravel-mcp-companion"
        assert path.is_absolute()


class TestReading:
    def test_a_wheel_install_reads_its_bundled_copy_by_default(self, wheel):
        bundled, _ = wheel
        assert docs_location.reading_path() == bundled

    def test_a_newer_user_copy_is_read_instead(self, wheel):
        bundled, user = wheel
        make_docs(user, "2026-07-01", "updated")
        assert docs_location.reading_path() == user

    def test_a_user_copy_as_new_as_the_bundled_one_is_read(self, wheel):
        """It was fetched after the package was built, so its services and
        packages are at least as new even when the framework date ties."""
        bundled, user = wheel
        make_docs(user, "2026-06-01", "updated")
        assert docs_location.reading_path() == user

    def test_an_older_user_copy_does_not_shadow_a_newer_package(self, wheel):
        """Upgrading the package must not leave the user on last year's
        update."""
        bundled, user = wheel
        make_docs(user, "2026-01-01", "old update")
        assert docs_location.reading_path() == bundled

    def test_an_empty_user_directory_is_not_a_copy(self, wheel):
        bundled, user = wheel
        user.mkdir(parents=True)
        assert docs_location.reading_path() == bundled

    def test_a_checkout_reads_the_docs_beside_it_whatever_the_user_holds(self, checkout):
        beside, user = checkout
        make_docs(user, "2026-12-01", "updated")
        assert docs_location.reading_path() == beside


class TestUpdating:
    def test_a_checkout_updates_in_place(self, checkout):
        beside, user = checkout
        assert docs_location.updating_path() == beside
        assert not user.exists()

    def test_a_wheel_install_updates_a_copy_in_the_user_directory(self, wheel):
        bundled, user = wheel
        assert docs_location.updating_path() == user
        assert "bundled" in (user / "12.x" / "queues.md").read_text(encoding="utf-8")
        assert (user / "12.x" / ".metadata" / "sync_info.json").is_file()

    def test_the_bundled_copy_is_left_alone(self, wheel):
        bundled, user = wheel
        before = sorted(p.relative_to(bundled) for p in bundled.rglob("*"))
        docs_location.updating_path()
        assert sorted(p.relative_to(bundled) for p in bundled.rglob("*")) == before

    def test_an_existing_newer_user_copy_is_kept(self, wheel):
        bundled, user = wheel
        make_docs(user, "2026-07-01", "updated")
        assert docs_location.updating_path() == user
        assert "updated" in (user / "12.x" / "queues.md").read_text(encoding="utf-8")

    def test_an_older_user_copy_is_replaced_from_the_newer_package(self, wheel):
        """Updating from an old copy would keep pages the newer package has
        since dropped."""
        bundled, user = wheel
        make_docs(user, "2026-01-01", "old update")
        (user / "12.x" / "dropped.md").write_text("# Gone\n", encoding="utf-8")
        assert docs_location.updating_path() == user
        assert "bundled" in (user / "12.x" / "queues.md").read_text(encoding="utf-8")
        assert not (user / "12.x" / "dropped.md").exists()

    def test_a_failed_copy_leaves_no_half_written_user_directory(self, wheel, monkeypatch):
        bundled, user = wheel

        def broken(src, dst, **kwargs):
            Path(dst).mkdir(parents=True)
            raise OSError("disk full")

        monkeypatch.setattr(docs_location.shutil, "copytree", broken)
        with pytest.raises(OSError):
            docs_location.updating_path()
        assert not user.exists()
        assert not [p for p in user.parent.iterdir() if p.name.startswith("docs")]


class TestTheServerUsesIt:
    def test_a_given_path_is_used_as_it_is(self, wheel, tmp_path):
        from laravel_mcp_companion import server

        given = tmp_path / "mine"
        assert server.setup_docs_path(str(given)) == given.resolve()
        assert server.setup_docs_path(str(given), for_update=True) == given.resolve()

    def test_serving_reads_and_updating_writes_the_user_copy(self, wheel):
        from laravel_mcp_companion import server

        bundled, user = wheel
        assert server.setup_docs_path() == bundled.resolve()
        assert server.setup_docs_path(for_update=True) == user.resolve()
        # The update wrote there, so the next start reads there.
        assert server.setup_docs_path() == user.resolve()

    @pytest.mark.parametrize("flags, expected", [
        ([], False), (["--update-docs"], True), (["--force-update"], True),
    ])
    def test_the_update_flags_choose_the_writable_copy(self, monkeypatch, flags, expected):
        from laravel_mcp_companion import server

        seen = {}

        def record(user_path=None, for_update=False):
            seen["for_update"] = for_update
            return Path("/nowhere")

        monkeypatch.setattr(server, "setup_docs_path", record)
        monkeypatch.setattr("sys.argv", ["laravel-mcp-companion", *flags])
        server.setup_server_environment(server.parse_arguments())
        assert seen["for_update"] is expected
