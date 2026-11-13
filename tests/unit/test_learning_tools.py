"""get_laravel_learning_path and browse_docs_by_category.

browse_docs_by_category replaces three tools: the category browser, the list
of categories and the difficulty filter. The category list used to report how
many keywords a category had as if that were how many pages it held.
"""

import pytest

from laravel_mcp_companion.learning_resources import EXPANDED_CATEGORIES, LEARNING_PATHS
from laravel_mcp_companion.tools import EXPERIMENTAL_TOOLS, ToolFailure
from laravel_mcp_companion.tools.learning import browse_docs, learning_paths


class TestLearningPaths:
    def test_with_no_name_every_path_is_listed_in_brief(self):
        result = learning_paths()

        assert result["count"] == len(LEARNING_PATHS)
        assert {path["id"] for path in result["paths"]} == set(LEARNING_PATHS)
        assert all("docs" not in path for path in result["paths"])

    def test_a_listed_path_says_how_long_and_how_hard_it_is(self):
        path = next(p for p in learning_paths()["paths"] if p["id"] == "getting-started")

        assert path["difficulty"] == "beginner"
        assert path["estimated_hours"] > 0
        assert path["doc_count"] == len(LEARNING_PATHS["getting-started"]["docs"])

    def test_a_named_path_comes_with_its_pages_in_order(self):
        result = learning_paths("getting-started")

        assert result["count"] == 1
        assert result["paths"][0]["docs"][:2] == ["installation.md", "configuration.md"]

    def test_a_named_path_points_at_the_one_that_follows(self):
        assert learning_paths("getting-started")["paths"][0]["next_path"] == LEARNING_PATHS["getting-started"]["next_path"]

    def test_an_unknown_path_is_not_found_and_the_real_ones_are_listed(self):
        with pytest.raises(ToolFailure) as raised:
            learning_paths("mastery")

        assert raised.value.code == "not_found"
        assert raised.value.details["available_paths"] == list(LEARNING_PATHS)


@pytest.fixture
def docs(temp_dir):
    root = temp_dir / "docs"
    version = root / "12.x"
    version.mkdir(parents=True)
    for name, title in [
        ("authentication.md", "Authentication"), ("sanctum.md", "Laravel Sanctum"),
        ("eloquent.md", "Eloquent: Getting Started"), ("eloquent-relationships.md", "Eloquent: Relationships"),
        ("installation.md", "Installation"), ("octane.md", "Laravel Octane"),
    ]:
        (version / name).write_text(f"# {title}\n\n## Introduction\n\nText.\n")
    return root


class TestBrowseByCategory:
    def test_a_category_lists_its_pages_with_title_and_difficulty(self, docs):
        result = browse_docs(docs, category="authentication", runtime_version="12.x")

        assert [doc["file"] for doc in result["docs"]] == ["12.x/authentication.md", "12.x/sanctum.md"]
        assert result["docs"][1]["title"] == "Laravel Sanctum"
        assert result["docs"][0]["difficulty"] in ("beginner", "intermediate", "advanced")
        assert (result["count"], result["category"]) == (2, "authentication")

    def test_a_page_reports_every_category_it_belongs_to(self, docs):
        result = browse_docs(docs, category="database", runtime_version="12.x")

        assert all("database" in doc["categories"] for doc in result["docs"])

    def test_a_category_with_no_pages_in_this_version_is_count_zero(self, temp_dir):
        (temp_dir / "12.x").mkdir()
        (temp_dir / "12.x" / "octane.md").write_text("# Octane\n")

        assert browse_docs(temp_dir, category="authentication", runtime_version="12.x")["count"] == 0

    def test_an_unknown_category_is_not_found_and_the_real_ones_are_listed(self, docs):
        with pytest.raises(ToolFailure) as raised:
            browse_docs(docs, category="astrology", runtime_version="12.x")

        assert raised.value.code == "not_found"
        assert raised.value.details["available_categories"] == sorted(EXPANDED_CATEGORIES)


class TestBrowseByDifficulty:
    def test_a_difficulty_lists_the_pages_at_that_level(self, docs):
        result = browse_docs(docs, difficulty="beginner", runtime_version="12.x")

        assert "12.x/installation.md" in [doc["file"] for doc in result["docs"]]
        assert all(doc["difficulty"] == "beginner" for doc in result["docs"])

    def test_category_and_difficulty_combine(self, docs):
        everything = browse_docs(docs, category="database", runtime_version="12.x")
        level = everything["docs"][0]["difficulty"]

        narrowed = browse_docs(docs, category="database", difficulty=level, runtime_version="12.x")

        assert narrowed["count"] == sum(1 for doc in everything["docs"] if doc["difficulty"] == level)

    def test_an_unknown_difficulty_is_refused(self, docs):
        with pytest.raises(ToolFailure) as raised:
            browse_docs(docs, difficulty="expert", runtime_version="12.x")

        assert raised.value.details["valid_difficulties"] == ["beginner", "intermediate", "advanced"]


class TestCategoryIndex:
    def test_with_no_filter_every_category_is_listed_with_a_page_count(self, docs):
        result = browse_docs(docs, runtime_version="12.x")

        assert {entry["name"] for entry in result["categories"]} == set(EXPANDED_CATEGORIES)
        assert "docs" not in result

    def test_a_categorys_count_is_the_number_of_pages_browsing_it_returns(self, docs):
        """The two used to be computed differently and disagreed."""
        index = {entry["name"]: entry["doc_count"] for entry in browse_docs(docs, runtime_version="12.x")["categories"]}

        for name in ("authentication", "database", "deployment"):
            assert index[name] == browse_docs(docs, category=name, runtime_version="12.x")["count"]

    def test_a_version_with_no_copy_is_not_found(self, docs):
        with pytest.raises(ToolFailure) as raised:
            browse_docs(docs, version="11.x")

        assert raised.value.code == "not_found"


def test_both_learning_tools_sit_outside_the_versioning_guarantee():
    assert set(EXPERIMENTAL_TOOLS) == {"get_laravel_learning_path", "browse_docs_by_category"}
