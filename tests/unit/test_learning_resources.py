"""Unit tests for learning resources module."""

import pytest
from pathlib import Path
import json
import tempfile

from learning_resources import (
    DifficultyLevel,
    TOPIC_DIFFICULTY_MAP,
    EXPANDED_CATEGORIES,
    NEED_MAPPINGS,
    LEARNING_PATHS,
    RELATED_PACKAGES,
    get_difficulty_for_topic,
    get_topics_by_difficulty,
    get_docs_for_need,
    get_related_packages,
    get_learning_path,
    list_learning_paths,
    get_category_docs,
    list_categories
)

from mcp_tools import (
    find_laravel_docs_for_need_impl,
    get_laravel_learning_path_impl,
    list_laravel_learning_paths_impl,
    get_laravel_content_by_difficulty_impl,
    get_related_laravel_packages_impl,
    search_laravel_learning_resources_impl,
    list_laravel_learning_resources_impl,
    list_laravel_categories_impl
)


class TestDifficultyLevel:
    """Tests for the DifficultyLevel enum."""

    def test_difficulty_levels_exist(self):
        """Test that all difficulty levels are defined."""
        assert DifficultyLevel.BEGINNER.value == "beginner"
        assert DifficultyLevel.INTERMEDIATE.value == "intermediate"
        assert DifficultyLevel.ADVANCED.value == "advanced"

    def test_difficulty_level_count(self):
        """Test that we have exactly 3 difficulty levels."""
        assert len(DifficultyLevel) == 3


class TestTopicDifficultyMap:
    """Tests for the TOPIC_DIFFICULTY_MAP."""

    def test_topic_difficulty_map_not_empty(self):
        """Test that the topic difficulty map has entries."""
        assert len(TOPIC_DIFFICULTY_MAP) > 0

    def test_beginner_topics_exist(self):
        """Test that beginner topics are correctly mapped."""
        assert TOPIC_DIFFICULTY_MAP.get("installation") == DifficultyLevel.BEGINNER
        assert TOPIC_DIFFICULTY_MAP.get("routing") == DifficultyLevel.BEGINNER
        assert TOPIC_DIFFICULTY_MAP.get("blade") == DifficultyLevel.BEGINNER

    def test_intermediate_topics_exist(self):
        """Test that intermediate topics are correctly mapped."""
        assert TOPIC_DIFFICULTY_MAP.get("eloquent") == DifficultyLevel.INTERMEDIATE
        assert TOPIC_DIFFICULTY_MAP.get("queues") == DifficultyLevel.INTERMEDIATE
        assert TOPIC_DIFFICULTY_MAP.get("authentication") == DifficultyLevel.INTERMEDIATE

    def test_advanced_topics_exist(self):
        """Test that advanced topics are correctly mapped."""
        assert TOPIC_DIFFICULTY_MAP.get("container") == DifficultyLevel.ADVANCED
        assert TOPIC_DIFFICULTY_MAP.get("octane") == DifficultyLevel.ADVANCED
        assert TOPIC_DIFFICULTY_MAP.get("broadcasting") == DifficultyLevel.ADVANCED

    def test_get_difficulty_for_topic_known(self):
        """Test getting difficulty for a known topic."""
        assert get_difficulty_for_topic("installation") == DifficultyLevel.BEGINNER
        assert get_difficulty_for_topic("eloquent") == DifficultyLevel.INTERMEDIATE
        assert get_difficulty_for_topic("container") == DifficultyLevel.ADVANCED

    def test_get_difficulty_for_topic_unknown(self):
        """Test that unknown topics default to INTERMEDIATE."""
        result = get_difficulty_for_topic("nonexistent-topic")
        assert result == DifficultyLevel.INTERMEDIATE

    def test_get_topics_by_difficulty(self):
        """Test getting all topics at a specific difficulty level."""
        beginner_topics = get_topics_by_difficulty(DifficultyLevel.BEGINNER)
        assert "installation" in beginner_topics
        assert "routing" in beginner_topics

        intermediate_topics = get_topics_by_difficulty(DifficultyLevel.INTERMEDIATE)
        assert "eloquent" in intermediate_topics

        advanced_topics = get_topics_by_difficulty(DifficultyLevel.ADVANCED)
        assert "container" in advanced_topics


class TestExpandedCategories:
    """Tests for the EXPANDED_CATEGORIES."""

    def test_expanded_categories_count(self):
        """Test that we have 15 categories (8 original + 7 new)."""
        assert len(EXPANDED_CATEGORIES) == 15

    def test_original_categories_exist(self):
        """Test that original 8 categories are present."""
        original_categories = [
            "authentication", "database", "frontend", "api",
            "testing", "deployment", "packages", "security"
        ]
        for cat in original_categories:
            assert cat in EXPANDED_CATEGORIES

    def test_new_categories_exist(self):
        """Test that new 7 categories are present."""
        new_categories = [
            "performance", "development", "realtime",
            "payments", "search", "files", "jobs"
        ]
        for cat in new_categories:
            assert cat in EXPANDED_CATEGORIES

    def test_category_has_docs(self):
        """Test that each category has at least one doc."""
        for category, docs in EXPANDED_CATEGORIES.items():
            assert len(docs) > 0, f"Category {category} has no docs"

    def test_get_category_docs(self):
        """Test getting docs for a category."""
        auth_docs = get_category_docs("authentication")
        assert "authentication" in auth_docs
        assert "sanctum" in auth_docs

    def test_get_category_docs_unknown(self):
        """Test getting docs for unknown category returns empty list."""
        result = get_category_docs("nonexistent")
        assert result == []

    def test_list_categories(self):
        """Test listing all categories."""
        categories = list_categories()
        assert len(categories) == 15
        assert "authentication" in categories
        assert "performance" in categories


class TestNeedMappings:
    """Tests for the NEED_MAPPINGS."""

    def test_need_mappings_not_empty(self):
        """Test that need mappings has entries."""
        assert len(NEED_MAPPINGS) > 0

    def test_common_needs_mapped(self):
        """Test that common user needs are mapped."""
        assert "upload files" in NEED_MAPPINGS
        assert "send emails" in NEED_MAPPINGS
        assert "accept payments" in NEED_MAPPINGS
        assert "authenticate" in NEED_MAPPINGS

    def test_get_docs_for_need_exact_match(self):
        """Test getting docs for an exact need match."""
        docs = get_docs_for_need("upload files")
        assert "filesystem" in docs

    def test_get_docs_for_need_partial_match(self):
        """Test getting docs for a partial need match."""
        docs = get_docs_for_need("files")
        assert len(docs) > 0

    def test_get_docs_for_need_no_match(self):
        """Test getting docs for a non-existent need."""
        docs = get_docs_for_need("xyzzy nonexistent need")
        assert docs == []


class TestLearningPaths:
    """Tests for the LEARNING_PATHS."""

    def test_learning_paths_not_empty(self):
        """Test that learning paths has entries."""
        assert len(LEARNING_PATHS) > 0

    def test_required_paths_exist(self):
        """Test that required learning paths are present."""
        required_paths = [
            "getting-started",
            "crud-basics",
            "api-development",
            "testing-fundamentals",
            "production-ready"
        ]
        for path in required_paths:
            assert path in LEARNING_PATHS

    def test_learning_path_structure(self):
        """Test that each learning path has required fields."""
        for path_id, path_data in LEARNING_PATHS.items():
            assert "name" in path_data, f"Path {path_id} missing name"
            assert "description" in path_data, f"Path {path_id} missing description"
            assert "difficulty" in path_data, f"Path {path_id} missing difficulty"
            assert "docs" in path_data, f"Path {path_id} missing docs"
            assert isinstance(path_data["docs"], list), f"Path {path_id} docs should be a list"

    def test_get_learning_path_found(self):
        """Test getting a known learning path."""
        path = get_learning_path("getting-started")
        assert path is not None
        assert path["name"] == "Getting Started with Laravel"

    def test_get_learning_path_not_found(self):
        """Test getting a non-existent learning path."""
        path = get_learning_path("nonexistent-path")
        assert path == {}

    def test_list_learning_paths(self):
        """Test listing all learning paths."""
        paths = list_learning_paths()
        assert len(paths) > 0
        for path in paths:
            assert "id" in path
            assert "name" in path
            assert "difficulty" in path


class TestRelatedPackages:
    """Tests for the RELATED_PACKAGES."""

    def test_related_packages_not_empty(self):
        """Test that related packages has entries."""
        assert len(RELATED_PACKAGES) > 0

    def test_key_packages_have_related(self):
        """Test that key packages have related packages."""
        assert "laravel/sanctum" in RELATED_PACKAGES
        assert "laravel/breeze" in RELATED_PACKAGES.get("laravel/sanctum", [])

    def test_get_related_packages_found(self):
        """Test getting related packages for a known package."""
        related = get_related_packages("laravel/sanctum")
        assert len(related) > 0
        assert "laravel/breeze" in related

    def test_get_related_packages_not_found(self):
        """Test getting related packages for an unknown package."""
        related = get_related_packages("unknown/package")
        assert related == []


class TestMCPToolImplementations:
    """Tests for the MCP tool implementations."""

    @pytest.fixture
    def temp_docs_dir(self):
        """Create a temporary docs directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir)

            # Create version directory with sample docs
            version_dir = docs_path / "12.x"
            version_dir.mkdir()
            (version_dir / "installation.md").write_text("# Installation")
            (version_dir / "routing.md").write_text("# Routing")
            (version_dir / "eloquent.md").write_text("# Eloquent ORM")
            (version_dir / "authentication.md").write_text("# Authentication")
            (version_dir / "filesystem.md").write_text("# Filesystem")
            (version_dir / "mail.md").write_text("# Mail")
            (version_dir / "container.md").write_text("# Service Container")

            # Create learning resources directory
            learning_dir = docs_path / "learning_resources"
            learning_dir.mkdir()

            bootcamp_dir = learning_dir / "laravel-bootcamp"
            bootcamp_dir.mkdir()
            (bootcamp_dir / "introduction.md").write_text("# Introduction to Laravel Bootcamp")
            (bootcamp_dir / ".cache_metadata.json").write_text(json.dumps({
                "name": "Laravel Bootcamp",
                "difficulty": "beginner",
                "cached_at": 1704110400.0
            }))

            yield docs_path

    def test_find_laravel_docs_for_need_impl_found(self, temp_docs_dir):
        """Test finding docs for a specific need."""
        result = find_laravel_docs_for_need_impl(temp_docs_dir, "upload files", "12.x")
        assert "filesystem" in result

    def test_find_laravel_docs_for_need_impl_empty_need(self, temp_docs_dir):
        """Test finding docs with empty need."""
        result = find_laravel_docs_for_need_impl(temp_docs_dir, "", "12.x")
        assert "error" in result.lower()

    def test_get_laravel_learning_path_impl_found(self):
        """Test getting a learning path."""
        result = get_laravel_learning_path_impl("getting-started")
        assert "Getting Started" in result
        assert "installation" in result

    def test_get_laravel_learning_path_impl_list_all(self):
        """Test listing all learning paths when empty name."""
        result = get_laravel_learning_path_impl("")
        assert "paths" in result
        assert "getting-started" in result or "Getting Started" in result

    def test_get_laravel_learning_path_impl_not_found(self):
        """Test getting non-existent learning path."""
        result = get_laravel_learning_path_impl("nonexistent")
        assert "error" in result.lower() or "not found" in result.lower()

    def test_list_laravel_learning_paths_impl(self):
        """Test listing all learning paths."""
        result = list_laravel_learning_paths_impl()
        assert "paths" in result
        assert "count" in result

    def test_get_laravel_content_by_difficulty_impl_valid(self, temp_docs_dir):
        """Test getting content by valid difficulty level."""
        result = get_laravel_content_by_difficulty_impl(temp_docs_dir, "beginner", "12.x")
        assert "beginner" in result

    def test_get_laravel_content_by_difficulty_impl_invalid(self, temp_docs_dir):
        """Test getting content by invalid difficulty level."""
        result = get_laravel_content_by_difficulty_impl(temp_docs_dir, "expert", "12.x")
        assert "error" in result.lower() or "invalid" in result.lower()

    def test_get_related_laravel_packages_impl_found(self):
        """Test getting related packages for known package."""
        result = get_related_laravel_packages_impl("laravel/sanctum")
        assert "breeze" in result or "fortify" in result

    def test_get_related_laravel_packages_impl_empty(self):
        """Test getting related packages with empty package name."""
        result = get_related_laravel_packages_impl("")
        assert "error" in result.lower()

    def test_search_laravel_learning_resources_impl(self, temp_docs_dir):
        """Test searching learning resources."""
        result = search_laravel_learning_resources_impl(temp_docs_dir, "Introduction")
        # Should find the introduction.md file
        assert "laravel-bootcamp" in result or "introduction" in result

    def test_search_laravel_learning_resources_impl_empty_query(self, temp_docs_dir):
        """Test searching with empty query."""
        result = search_laravel_learning_resources_impl(temp_docs_dir, "")
        assert "error" in result.lower()

    def test_list_laravel_learning_resources_impl(self, temp_docs_dir):
        """Test listing learning resources."""
        result = list_laravel_learning_resources_impl(temp_docs_dir)
        assert "laravel-bootcamp" in result

    def test_list_laravel_learning_resources_impl_specific_source(self, temp_docs_dir):
        """Test listing specific learning resource source."""
        result = list_laravel_learning_resources_impl(temp_docs_dir, "laravel-bootcamp")
        assert "laravel-bootcamp" in result
        assert "introduction.md" in result

    def test_list_laravel_learning_resources_impl_unknown_source(self, temp_docs_dir):
        """Test listing unknown learning resource source."""
        result = list_laravel_learning_resources_impl(temp_docs_dir, "unknown-source")
        assert "error" in result.lower() or "not found" in result.lower()

    def test_list_laravel_categories_impl(self):
        """Test listing all categories."""
        result = list_laravel_categories_impl()
        assert "categories" in result
        assert "authentication" in result
        assert "performance" in result


class TestTOONFormatters:
    """Tests for TOON formatters."""

    def test_format_learning_resources(self):
        """Test formatting learning resources."""
        from toon_helpers import format_learning_resources
        result = format_learning_resources("test-source", [{"file": "test.md"}])
        assert "test-source" in result
        assert "test.md" in result

    def test_format_learning_resources_with_count(self):
        """Test formatting learning resources with explicit count."""
        from toon_helpers import format_learning_resources
        result = format_learning_resources("test-source", [{"file": "test.md"}], 5)
        assert "test-source" in result
        assert "5" in result

    def test_format_learning_path(self):
        """Test formatting a learning path."""
        from toon_helpers import format_learning_path
        result = format_learning_path({"name": "Test Path", "docs": ["a", "b"]})
        assert "Test Path" in result

    def test_format_learning_paths_list(self):
        """Test formatting list of learning paths."""
        from toon_helpers import format_learning_paths_list
        result = format_learning_paths_list([{"id": "test", "name": "Test"}])
        assert "test" in result or "Test" in result

    def test_format_need_docs(self):
        """Test formatting need docs."""
        from toon_helpers import format_need_docs
        result = format_need_docs("upload files", ["filesystem.md"], "core")
        assert "upload files" in result
        assert "filesystem" in result

    def test_format_related_packages(self):
        """Test formatting related packages."""
        from toon_helpers import format_related_packages
        result = format_related_packages("laravel/sanctum", ["breeze", "fortify"])
        assert "sanctum" in result
        assert "breeze" in result

    def test_format_difficulty_content(self):
        """Test formatting difficulty content."""
        from toon_helpers import format_difficulty_content
        result = format_difficulty_content("beginner", ["installation.md"], 1)
        assert "beginner" in result
        assert "installation" in result

    def test_format_learning_resource_search(self):
        """Test formatting learning resource search results."""
        from toon_helpers import format_learning_resource_search
        result = format_learning_resource_search(
            "test",
            [{"file": "core.md"}],
            [{"file": "learning.md"}],
            [{"file": "external.md"}]
        )
        assert "test" in result
        assert "core" in result
        assert "learning" in result

    def test_format_learning_resource_search_core_only(self):
        """Test formatting learning resource search with core results only."""
        from toon_helpers import format_learning_resource_search
        result = format_learning_resource_search("test", [{"file": "core.md"}])
        assert "test" in result
        assert "core" in result
