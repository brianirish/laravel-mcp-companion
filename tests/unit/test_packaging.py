"""The wheel carries the documentation, and the package finds it wherever it is.

`pip install` was impossible while a dependency came from a git URL, and a
wheel would have been empty anyway: the corpus lives at the repository root,
outside any package. A build hook copies it in, and `resource_path` looks
inside the package first and beside it second, so one lookup serves an
installed wheel, a checkout and the Docker image.
"""

import tomllib
from pathlib import Path

import laravel_mcp_companion as package
from hatch_build import bundled_files

REPO_ROOT = Path(__file__).resolve().parents[2]


def pyproject() -> dict:
    return tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))


class TestWhatTheWheelCarries:
    def _tree(self, tmp_path):
        for name in ("6.x", "13.x", "14.x", "external", "packages", "learning_resources", "superpowers"):
            (tmp_path / "docs" / name).mkdir(parents=True)
        (tmp_path / "docs" / ".versions_cache.json").write_text("{}")
        (tmp_path / "server.json").write_text("{}")
        return tmp_path

    def test_every_corpus_directory_is_bundled_including_a_version_added_later(self, tmp_path):
        files = bundled_files(self._tree(tmp_path))

        assert files[str(tmp_path / "docs" / "14.x")] == "laravel_mcp_companion/docs/14.x"
        assert files[str(tmp_path / "docs" / "external")] == "laravel_mcp_companion/docs/external"

    def test_the_versions_cache_travels_with_the_corpus(self, tmp_path):
        files = bundled_files(self._tree(tmp_path))

        assert str(tmp_path / "docs" / ".versions_cache.json") in files

    def test_working_notes_are_not_shipped(self, tmp_path):
        files = bundled_files(self._tree(tmp_path))

        assert not any("superpowers" in source for source in files)

    def test_server_json_is_bundled_for_the_registry_metadata_route(self, tmp_path):
        files = bundled_files(self._tree(tmp_path))

        assert files[str(tmp_path / "server.json")] == "laravel_mcp_companion/server.json"


class TestResourceLookup:
    def test_a_checkout_finds_the_corpus_at_the_repository_root(self):
        assert package.resource_path("docs") == REPO_ROOT / "docs"

    def test_a_copy_inside_the_package_wins(self, tmp_path, monkeypatch):
        installed = tmp_path / "site-packages" / "laravel_mcp_companion"
        (installed / "docs").mkdir(parents=True)
        monkeypatch.setattr(package, "PACKAGE_DIR", installed)

        assert package.resource_path("docs") == installed / "docs"

    def test_the_icon_lives_inside_the_package(self):
        assert (package.PACKAGE_DIR / "icon.svg").is_file()


class TestInstallMetadata:
    def test_no_dependency_comes_from_a_url(self):
        """A direct URL dependency is what kept the project off PyPI."""
        for requirement in pyproject()["project"]["dependencies"]:
            assert "@" not in requirement and "git+" not in requirement, requirement

    def test_the_console_script_starts_the_server(self):
        scripts = pyproject()["project"]["scripts"]

        assert scripts["laravel-mcp-companion"] == "laravel_mcp_companion.server:main"

    def test_the_version_is_read_from_pyproject(self):
        assert package.__version__ == pyproject()["project"]["version"]
