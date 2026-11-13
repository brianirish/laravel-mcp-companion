"""The two learning sources whose upstream moved.

Laravel Bootcamp: bootcamp.laravel.com first redirected to laravel.com/learn,
so all eight saved "bootcamp" pages were copies of that landing page, and then
stopped resolving altogether. The source now reads the courses on
laravel.com/learn, discovering courses and lessons from the site.

Laracasts: laracasts.com/topics became a 404, so the topic index was never
saved. The topic list lives on laracasts.com/series.
"""

import json
import urllib.error
from unittest.mock import patch

import pytest

from laravel_mcp_companion.docs_updater import LearningResourceFetcher
from tests.conftest import load_fixture

LANDING = """
<html><body><main>
  <a href="/learn">Learn</a>
  <a href="/learn/getting-started-with-laravel">Getting Started with Laravel</a>
  <a href="/learn/php-fundamentals">PHP Fundamentals</a>
  <a href="/learn/getting-started-with-laravel">Start course</a>
</main></body></html>
"""

COURSES = {
    "getting-started-with-laravel": """
        <main>
          <a href="/learn/getting-started-with-laravel/what-are-we-building">What are we building?</a>
          <a href="/learn/getting-started-with-laravel/your-first-route">Your first route</a>
          <a href="/learn/getting-started-with-laravel/what-are-we-building">Start</a>
        </main>""",
    "php-fundamentals": """
        <main><a href="/learn/php-fundamentals/why-php">Why PHP?</a></main>""",
}


def _lesson(course, lesson):
    return (f"<html><body><main><h1>{lesson}</h1>"
            f"<p>Lesson text for {course} / {lesson}.</p>" + "<p>More explanation of the lesson.</p>" * 10 +
            "</main></body></html>")


def _learn_site(failing=()):
    def respond(url, *args, **kwargs):
        path = url.split("laravel.com/learn", 1)[1].strip("/")
        if path in failing:
            raise urllib.error.HTTPError(url, 500, "Server Error", None, None)
        if path == "":
            return LANDING.encode()
        if path in COURSES:
            return COURSES[path].encode()
        course, lesson = path.split("/")
        return _lesson(course, lesson).encode()
    return respond


@pytest.fixture
def fetcher(temp_dir):
    return LearningResourceFetcher(temp_dir)


def _fetch_learn(fetcher, **site):
    with patch.object(fetcher, "_retry_request", side_effect=_learn_site(**site)):
        return fetcher.fetch_learning_source("laravel-bootcamp", force=True)


class TestLaravelLearnCourses:
    def test_every_lesson_of_every_course_is_saved(self, fetcher):
        assert _fetch_learn(fetcher) is True

        source_dir = fetcher.get_source_cache_path("laravel-bootcamp")
        assert sorted(p.name for p in source_dir.glob("*.md")) == [
            "getting-started-with-laravel-what-are-we-building.md",
            "getting-started-with-laravel-your-first-route.md",
            "php-fundamentals-why-php.md",
        ]

    def test_a_lesson_file_holds_that_lesson_and_names_its_source(self, fetcher):
        _fetch_learn(fetcher)

        text = (fetcher.get_source_cache_path("laravel-bootcamp")
                / "getting-started-with-laravel-your-first-route.md").read_text()
        assert "Lesson text for getting-started-with-laravel / your-first-route." in text
        assert "Source: https://laravel.com/learn/getting-started-with-laravel/your-first-route" in text

    def test_metadata_records_a_complete_sync(self, fetcher):
        _fetch_learn(fetcher)

        metadata = json.loads(fetcher.get_cache_metadata_path("laravel-bootcamp").read_text())
        assert (metadata["fetched_sections"], metadata["total_sections"], metadata["success_rate"]) == (3, 3, 1.0)

    def test_a_complete_sync_removes_the_old_bootcamp_pages(self, fetcher):
        stale = fetcher.get_source_cache_path("laravel-bootcamp") / "creating-chirps.md"
        stale.write_text("a copy of the landing page")

        _fetch_learn(fetcher)

        assert not stale.exists()

    def test_a_partial_sync_keeps_what_is_already_saved(self, fetcher):
        stale = fetcher.get_source_cache_path("laravel-bootcamp") / "creating-chirps.md"
        stale.write_text("a copy of the landing page")

        assert _fetch_learn(fetcher, failing=("php-fundamentals/why-php",)) is True

        assert stale.exists()
        metadata = json.loads(fetcher.get_cache_metadata_path("laravel-bootcamp").read_text())
        assert (metadata["fetched_sections"], metadata["total_sections"]) == (2, 3)

    def test_a_landing_page_without_courses_is_a_failed_sync(self, fetcher):
        with patch.object(fetcher, "_retry_request", return_value=b"<html><body><main>Coming soon</main></body></html>"):
            assert fetcher.fetch_learning_source("laravel-bootcamp", force=True) is False

        assert not fetcher.get_cache_metadata_path("laravel-bootcamp").exists()


class TestLessonContentComesFromThePagePayload:
    """laravel.com is an Inertia app. The server-rendered <main> carries the
    lesson's prose but not its code samples, and leads with the course sidebar;
    the complete lesson HTML is in the page's JSON payload."""

    PAYLOAD = {
        "component": "learn/lesson",
        "props": {
            "course": {"name": "Getting Started with Laravel", "slug": "getting-started-with-laravel"},
            "lesson": {
                "name": "Your first route",
                "slug": "your-first-route",
                "description": "Create your first Laravel route and view.",
                "content": (
                    "<p>Routes connect URLs to code. Open the routes file and look at what is there, "
                    "then change it so the homepage renders a view of your own.</p>"
                    "<pre><code class=\"language-php\">Route::get('/', fn () =&gt; view('home'));</code></pre>"
                    "<h2>Step 1: Change the rendered view</h2><p>Refresh the browser to see the result.</p>"
                ),
            },
        },
    }

    def _site(self):
        lesson_page = (
            "<html><body><main><div>All Lessons</div><div>What are we building?</div>"
            "<p>Routes connect URLs to code.</p></main>"
            f"<script data-page=\"app\" type=\"application/json\">{json.dumps(self.PAYLOAD)}</script>"
            "</body></html>"
        )

        def respond(url, *args, **kwargs):
            path = url.split("laravel.com/learn", 1)[1].strip("/")
            if path == "":
                return b'<a href="/learn/getting-started-with-laravel">Course</a>'
            if path == "getting-started-with-laravel":
                return b'<a href="/learn/getting-started-with-laravel/your-first-route">Lesson</a>'
            return lesson_page.encode()
        return respond

    def _lesson_text(self, fetcher):
        with patch.object(fetcher, "_retry_request", side_effect=self._site()):
            assert fetcher.fetch_learning_source("laravel-bootcamp", force=True) is True
        return (fetcher.get_source_cache_path("laravel-bootcamp")
                / "getting-started-with-laravel-your-first-route.md").read_text()

    def test_code_samples_are_kept(self, fetcher):
        text = self._lesson_text(fetcher)

        assert "```php\nRoute::get('/', fn () => view('home'));\n```" in text

    def test_the_course_sidebar_is_not_part_of_the_lesson(self, fetcher):
        assert "All Lessons" not in self._lesson_text(fetcher)

    def test_the_heading_uses_the_course_and_lesson_names_from_the_site(self, fetcher):
        text = self._lesson_text(fetcher)

        assert text.startswith("# Laravel Learn - Getting Started with Laravel: Your first route\n")
        assert "Source: https://laravel.com/learn/getting-started-with-laravel/your-first-route" in text
        assert "Create your first Laravel route and view." in text


class TestLaracastsTopicIndex:
    def test_the_topic_index_is_saved_from_where_laracasts_lists_topics_now(self, fetcher):
        def respond(url, *args, **kwargs):
            if url.rstrip("/").endswith("/topics"):
                raise urllib.error.HTTPError(url, 404, "Not Found", None, None)
            return load_fixture("laracasts_index.html").encode()

        with patch.object(fetcher, "_retry_request", side_effect=respond):
            assert fetcher.fetch_learning_source("laracasts-index", force=True) is True

        assert (fetcher.get_source_cache_path("laracasts-index") / "topics.md").exists()
