"""Three defects found in review of the docs-sync change (PR #499).

1. `--all-versions` exited 1 whenever a version was already up to date, which
   is every day for the old Laravel versions. The pipeline reads that exit code
   as "the framework update failed" and would have marked every run degraded.
2. Spatie, Livewire and Debugbar recorded how many pages they fetched but not
   how many they wanted, so a fetch that got one page of thirty-six looked
   healthy in the sync report.
3. When a Laravel Learn course page failed to load, its lessons were simply
   absent from the list, the remaining lessons counted as a complete sync, and
   the failed course's saved lessons were pruned.
"""

import json
import urllib.error
from unittest.mock import Mock, patch

import pytest

from laravel_mcp_companion import docs_updater
from laravel_mcp_companion.docs_updater import CommunityPackageFetcher, LearningResourceFetcher, build_sync_report


class TestAllVersionsExitCode:
    def _run(self, monkeypatch, temp_dir, update):
        fake = Mock()
        fake.update.side_effect = update
        monkeypatch.setattr("sys.argv", ["docs_updater.py", "--target-dir", str(temp_dir), "--all-versions"])
        with patch.object(docs_updater, "SUPPORTED_VERSIONS", ["11.x", "12.x", "13.x"]), \
             patch.object(docs_updater, "DocsUpdater", return_value=fake):
            return docs_updater.main(), fake

    def test_versions_that_are_already_current_are_not_a_failure(self, monkeypatch, temp_dir):
        code, _ = self._run(monkeypatch, temp_dir, update=lambda force=False: False)

        assert code == 0

    def test_a_mix_of_updated_and_current_versions_is_a_success(self, monkeypatch, temp_dir):
        results = iter([False, False, True])
        code, _ = self._run(monkeypatch, temp_dir, update=lambda force=False: next(results))

        assert code == 0

    def test_a_version_that_fails_to_update_is_a_failure(self, monkeypatch, temp_dir):
        def update(force=False):
            raise urllib.error.URLError("github is unreachable")

        code, _ = self._run(monkeypatch, temp_dir, update=update)

        assert code == 1

    def test_one_failing_version_does_not_stop_the_others(self, monkeypatch, temp_dir):
        calls = []

        def update(force=False):
            calls.append(1)
            if len(calls) == 1:
                raise urllib.error.URLError("github is unreachable")
            return True

        code, _ = self._run(monkeypatch, temp_dir, update=update)

        assert (code, len(calls)) == (1, 3)


class TestPackageFetchesRecordCompleteness:
    @pytest.fixture
    def packages(self, temp_dir):
        return CommunityPackageFetcher(temp_dir)

    def _one_page_only(self, packages):
        """Every package page fails to fetch except the first one requested."""
        seen = []

        def fetch(url, package, section):
            seen.append(url)
            return "# Page\n\nFetched content.\n" if len(seen) == 1 else None

        return patch.object(packages, "_fetch_and_process_content", side_effect=fetch)

    def _metadata(self, packages, package, subpackage=None):
        return json.loads(packages.get_cache_metadata_path(package, subpackage).read_text())

    def test_livewire_records_how_many_pages_it_wanted(self, packages):
        config = dict(packages.community_packages["livewire"], sections=["quickstart", "components", "actions", "forms"])
        with self._one_page_only(packages):
            packages._fetch_livewire_docs(config)

        metadata = self._metadata(packages, "livewire")
        assert (metadata["sections_count"], metadata["total_sections"], metadata["success_rate"]) == (1, 4, 0.25)

    def test_debugbar_records_how_many_pages_it_wanted(self, packages):
        config = dict(packages.community_packages["debugbar"], sections=["installation", "usage", "features", "collectors"])
        with self._one_page_only(packages):
            packages._fetch_debugbar_docs(config)

        metadata = self._metadata(packages, "debugbar")
        assert (metadata["sections_count"], metadata["total_sections"], metadata["success_rate"]) == (1, 4, 0.25)

    def test_a_spatie_package_records_how_many_pages_it_wanted(self, packages):
        config = {"packages": {"laravel-backup": {
            "name": "Laravel Backup",
            "docs_url": "https://spatie.be/docs/laravel-backup/v9/introduction",
            "sections": ["introduction", "installation", "backing-up", "cleaning-up"],
        }}}
        with self._one_page_only(packages):
            packages._fetch_spatie_docs(config)

        metadata = self._metadata(packages, "spatie", "laravel-backup")
        assert (metadata["sections_count"], metadata["total_sections"], metadata["success_rate"]) == (1, 4, 0.25)

    def test_a_mostly_failed_package_fetch_is_flagged_by_the_sync_report(self, packages, temp_dir):
        config = dict(packages.community_packages["livewire"], sections=["quickstart", "components", "actions", "forms"])
        with self._one_page_only(packages):
            packages._fetch_livewire_docs(config)

        _, problems = build_sync_report(temp_dir)

        assert "livewire: fetched 1 of 4 pages" in problems


LANDING = '<a href="/learn/course-a">A</a><a href="/learn/course-b">B</a>'
COURSE_PAGES = {
    "course-a": '<a href="/learn/course-a/first-lesson">First</a>',
    "course-b": '<a href="/learn/course-b/other-lesson">Other</a>',
}
LESSON = "<html><body><main><h1>Lesson</h1>" + "<p>Lesson explanation text.</p>" * 12 + "</main></body></html>"


def _learn_site(broken_course=None, empty_course=None):
    def respond(url, *args, **kwargs):
        path = url.split("laravel.com/learn", 1)[1].strip("/")
        if path == "":
            return LANDING.encode()
        if path == broken_course:
            raise urllib.error.HTTPError(url, 500, "Server Error", None, None)
        if path == empty_course:
            return b"<main>Lessons coming soon</main>"
        if path in COURSE_PAGES:
            return COURSE_PAGES[path].encode()
        return LESSON.encode()
    return respond


class TestLearnCourseDiscoveryFailures:
    @pytest.fixture
    def fetcher(self, temp_dir):
        return LearningResourceFetcher(temp_dir)

    def _sync(self, fetcher, **site):
        saved = fetcher.get_source_cache_path("laravel-bootcamp") / "course-b-other-lesson.md"
        saved.write_text("lesson saved by an earlier sync")
        with patch.object(fetcher, "_retry_request", side_effect=_learn_site(**site)):
            ok = fetcher.fetch_learning_source("laravel-bootcamp", force=True)
        metadata = json.loads(fetcher.get_cache_metadata_path("laravel-bootcamp").read_text())
        return ok, saved, metadata

    def test_a_course_page_that_fails_to_load_does_not_cost_its_saved_lessons(self, fetcher):
        ok, saved, _ = self._sync(fetcher, broken_course="course-b")

        assert ok is True
        assert saved.read_text() == "lesson saved by an earlier sync"

    def test_a_course_page_that_fails_to_load_is_not_a_complete_sync(self, fetcher, temp_dir):
        _, _, metadata = self._sync(fetcher, broken_course="course-b")

        assert metadata["success_rate"] == 0.5
        _, problems = build_sync_report(temp_dir)
        assert [p for p in problems if p.startswith("laravel-bootcamp:")] != []

    def test_a_course_that_lists_no_lessons_does_not_cost_its_saved_lessons(self, fetcher):
        _, saved, metadata = self._sync(fetcher, empty_course="course-b")

        assert saved.exists()
        assert metadata["success_rate"] == 0.5

    def test_when_every_course_loads_the_stale_lesson_is_still_pruned(self, fetcher):
        stale = fetcher.get_source_cache_path("laravel-bootcamp") / "creating-chirps.md"
        stale.write_text("old bootcamp page")

        with patch.object(fetcher, "_retry_request", side_effect=_learn_site()):
            fetcher.fetch_learning_source("laravel-bootcamp", force=True)

        assert not stale.exists()


class TestImageStrippingKeepsParagraphBreaks:
    """remove_image_references skipped every blank line, not only the lines an
    image had occupied. On HTML-scraped pages that went unnoticed; on pages
    fetched as markdown (Inertia, Filament) it joined every paragraph to the
    next and ran headings and lists into the text around them."""

    def test_blank_lines_between_paragraphs_survive(self):
        text = "# Routing\n\nFirst paragraph.\n\nSecond paragraph.\n\n- one\n- two\n"

        assert docs_updater.remove_image_references(text) == text

    def test_a_line_that_held_only_an_image_is_removed(self):
        text = "Before.\n\n![Screenshot](https://example.test/shot.png)\n\nAfter."

        assert docs_updater.remove_image_references(text) == "Before.\n\n\nAfter."

    def test_an_image_inside_a_sentence_is_removed_and_the_sentence_kept(self):
        text = "See ![icon](https://example.test/i.png) the toolbar."

        assert docs_updater.remove_image_references(text) == "See  the toolbar."

    def test_a_bullet_that_held_only_an_image_is_removed(self):
        text = "- ![a](https://example.test/a.png)\n- real item"

        assert docs_updater.remove_image_references(text) == "- real item"

    def test_images_inside_code_blocks_are_left_alone(self):
        text = "```md\n![alt](path.png)\n\n```"

        assert docs_updater.remove_image_references(text) == text


class TestDebugbarPrunesAfterACompleteSync:
    @pytest.fixture
    def packages(self, temp_dir):
        return CommunityPackageFetcher(temp_dir)

    def _sync(self, packages, failing=()):
        stale = packages.get_package_cache_path("debugbar") / "old-page.md"
        stale.write_text("a page the site no longer has")

        def fetch(url, package, section):
            return None if section in failing else f"# {section}\n\nText.\n"

        config = dict(packages.community_packages["debugbar"], sections=["installation", "usage"])
        with patch.object(packages, "_fetch_and_process_content", side_effect=fetch):
            packages._fetch_debugbar_docs(config)
        return stale

    def test_a_page_no_longer_listed_is_removed(self, packages):
        assert not self._sync(packages).exists()

    def test_a_partial_sync_removes_nothing(self, packages):
        assert self._sync(packages, failing=["usage"]).exists()
