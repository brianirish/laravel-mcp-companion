"""Unit tests for learning resources module."""


from laravel_mcp_companion.learning_resources import (
    DifficultyLevel,
    TOPIC_DIFFICULTY_MAP,
    EXPANDED_CATEGORIES,
    NEED_MAPPINGS,
    LEARNING_PATHS,
    RELATED_PACKAGES,
    get_difficulty_for_topic,
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


class TestExpandedCategories:
    """Tests for the EXPANDED_CATEGORIES."""

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


class TestRelatedPackages:
    """Tests for the RELATED_PACKAGES."""

    def test_related_packages_not_empty(self):
        """Test that related packages has entries."""
        assert len(RELATED_PACKAGES) > 0

    def test_key_packages_have_related(self):
        """Test that key packages have related packages."""
        assert "laravel/sanctum" in RELATED_PACKAGES
        assert "laravel/fortify" in RELATED_PACKAGES.get("laravel/sanctum", [])
