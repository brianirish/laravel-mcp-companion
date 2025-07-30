"""Tests for learning resources components."""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock, Mock
import sqlite3

from learning_resources import (
    LearningResourceDatabase,
    LearningResourceFetcher,
    ResourceMetadata,
    ResourceType,
    DifficultyLevel,
    ResourceSource
)
from navigation_engine import (
    NavigationMapper,
    PackageCombinationGuide,
    SetupOrchestrator,
    USE_CASE_PATTERNS,
    PACKAGE_COMBINATIONS
)
from content_aggregators import (
    LaravelNewsAggregator,
    SpatieBlogAggregator,
    LaravelBootcampAggregator,
    ContentAggregatorManager
)


class TestLearningResourceDatabase:
    """Test learning resource database functionality."""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test_resources.db"
            yield db_path
    
    @pytest.fixture
    def db(self, temp_db):
        """Create a database instance."""
        return LearningResourceDatabase(temp_db)
    
    def test_init_database(self, db, temp_db):
        """Test database initialization."""
        assert temp_db.exists()
        
        # Check tables exist
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {row[0] for row in cursor.fetchall()}
            
            expected_tables = {
                'resources', 'tags', 'resource_tags',
                'use_case_mappings', 'package_combinations'
            }
            assert expected_tables.issubset(tables)
    
    def test_add_resource(self, db):
        """Test adding a resource."""
        resource = ResourceMetadata(
            id=None,
            type=ResourceType.TUTORIAL,
            title="Test Tutorial",
            description="A test tutorial",
            url="https://example.com/tutorial",
            source=ResourceSource.LARAVEL_NEWS,
            difficulty_level=DifficultyLevel.BEGINNER,
            published_date=datetime.now(timezone.utc),
            last_updated=datetime.now(timezone.utc),
            tags=["laravel", "testing"],
            metadata={"author": "Test Author"}
        )
        
        resource_id = db.add_resource(resource)
        assert resource_id > 0
        
        # Retrieve and verify
        retrieved = db.get_resource(resource_id)
        assert retrieved is not None
        assert retrieved.title == "Test Tutorial"
        assert retrieved.tags == ["laravel", "testing"]
    
    def test_search_resources(self, db):
        """Test searching resources."""
        # Add test resources
        resources = [
            ResourceMetadata(
                id=None,
                type=ResourceType.TUTORIAL,
                title="Laravel Authentication Tutorial",
                description="Learn authentication",
                url="https://example.com/auth",
                source=ResourceSource.LARAVEL_NEWS,
                difficulty_level=DifficultyLevel.BEGINNER,
                published_date=None,
                last_updated=datetime.now(timezone.utc),
                tags=["laravel", "authentication"],
                metadata={}
            ),
            ResourceMetadata(
                id=None,
                type=ResourceType.ARTICLE,
                title="Advanced Laravel Patterns",
                description="Design patterns",
                url="https://example.com/patterns",
                source=ResourceSource.SPATIE_BLOG,
                difficulty_level=DifficultyLevel.ADVANCED,
                published_date=None,
                last_updated=datetime.now(timezone.utc),
                tags=["laravel", "patterns"],
                metadata={}
            )
        ]
        
        for resource in resources:
            db.add_resource(resource)
        
        # Test search by query
        results = db.search_resources(query="authentication")
        assert len(results) == 1
        assert results[0].title == "Laravel Authentication Tutorial"
        
        # Test search by difficulty
        results = db.search_resources(difficulty=DifficultyLevel.ADVANCED)
        assert len(results) == 1
        assert results[0].title == "Advanced Laravel Patterns"
        
        # Test search by tags
        results = db.search_resources(tags=["authentication"])
        assert len(results) == 1
    
    def test_use_case_mappings(self, db):
        """Test use case mappings."""
        # Add a resource
        resource = ResourceMetadata(
            id=None,
            type=ResourceType.TUTORIAL,
            title="Test Resource",
            description="Test",
            url="https://example.com/test",
            source=ResourceSource.LARAVEL_NEWS,
            difficulty_level=None,
            published_date=None,
            last_updated=datetime.now(timezone.utc),
            tags=[],
            metadata={}
        )
        resource_id = db.add_resource(resource)
        
        # Add use case mapping
        db.add_use_case_mapping("authentication", resource_id, 0.9)
        
        # Get resources for use case
        results = db.get_resources_for_use_case("authentication")
        assert len(results) == 1
        assert results[0][0].title == "Test Resource"
        assert results[0][1] == 0.9
    
    def test_package_combinations(self, db):
        """Test package combination storage."""
        packages = ["livewire", "alpine"]
        guide_id = db.add_package_combination(
            packages=packages,
            use_case="Building reactive UI",
            guide_content="Test guide content",
            compatibility_notes="Works great together"
        )
        
        assert guide_id > 0
        
        # Retrieve combination
        result = db.get_package_combination(packages)
        assert result is not None
        assert result['use_case'] == "Building reactive UI"
        assert result['guide_content'] == "Test guide content"


class TestNavigationMapper:
    """Test navigation mapping functionality."""
    
    @pytest.fixture
    def mapper(self, temp_db):
        """Create a navigation mapper."""
        fetcher = LearningResourceFetcher(temp_db)
        return NavigationMapper(fetcher)
    
    def test_match_use_case_pattern(self, mapper):
        """Test use case pattern matching."""
        # Test direct keyword match
        result = mapper._match_use_case_pattern("i need authentication")
        assert result == "authentication"
        
        # Test package mention
        result = mapper._match_use_case_pattern("how to use sanctum")
        assert result == "authentication"
        
        # Test no match
        result = mapper._match_use_case_pattern("random query")
        assert result is None
    
    def test_find_resources_for_use_case(self, mapper):
        """Test finding resources for use case."""
        result = mapper.find_resources_for_use_case("authentication")
        
        assert result.use_case == "authentication"
        assert "sanctum" in result.recommended_packages
        assert "authentication" in result.matching_docs
        assert result.difficulty_level == DifficultyLevel.BEGINNER
    
    def test_generate_learning_path(self, mapper):
        """Test learning path generation."""
        result = mapper.find_resources_for_use_case(
            "authentication",
            DifficultyLevel.BEGINNER
        )
        
        if result.learning_path:
            assert len(result.learning_path) > 0
            assert all('step' in step for step in result.learning_path)
            assert all('title' in step for step in result.learning_path)


class TestPackageCombinationGuide:
    """Test package combination guide functionality."""
    
    @pytest.fixture
    def guide(self, temp_db):
        """Create a package combination guide."""
        fetcher = LearningResourceFetcher(temp_db)
        return PackageCombinationGuide(fetcher)
    
    def test_get_predefined_combination(self, guide):
        """Test getting predefined package combinations."""
        result = guide.get_combination_guide(["livewire", "alpine"])
        
        assert result is not None
        assert "livewire" in result['packages']
        assert "alpine" in result['packages']
        assert 'guide_content' in result
        assert 'compatibility_notes' in result
    
    def test_analyze_package_compatibility(self, guide):
        """Test package compatibility analysis."""
        result = guide._analyze_package_compatibility(["livewire", "inertia"])
        
        assert 'compatibility_notes' in result
        assert 'guide_content' in result
        assert result['has_conflicts'] is True  # These packages conflict


class TestSetupOrchestrator:
    """Test setup orchestration functionality."""
    
    @pytest.fixture
    def orchestrator(self):
        """Create a setup orchestrator."""
        return SetupOrchestrator()
    
    def test_generate_setup_workflow(self, orchestrator):
        """Test setup workflow generation."""
        workflow = orchestrator.generate_setup_workflow(
            ["sanctum", "livewire"],
            "Building SPA with authentication"
        )
        
        assert workflow['use_case'] == "Building SPA with authentication"
        assert len(workflow['packages']) == 2
        assert len(workflow['workflow']) > 0
        
        # Check workflow steps
        for step in workflow['workflow']:
            assert 'order' in step
            assert 'package' in step
            assert 'commands' in step
    
    def test_installation_order(self, orchestrator):
        """Test package installation order determination."""
        packages = ["jetstream", "sanctum", "livewire"]
        ordered = orchestrator._determine_installation_order(packages)
        
        # Sanctum should come before jetstream (dependency)
        sanctum_idx = ordered.index("sanctum")
        jetstream_idx = ordered.index("jetstream")
        assert sanctum_idx < jetstream_idx


class TestLaravelNewsAggregator:
    """Test Laravel News content aggregation."""
    
    @pytest.fixture
    def aggregator(self, temp_db):
        """Create a Laravel News aggregator."""
        fetcher = LearningResourceFetcher(temp_db)
        return LaravelNewsAggregator(fetcher)
    
    @patch('feedparser.parse')
    def test_fetch_articles(self, mock_parse, aggregator):
        """Test fetching articles from RSS feed."""
        # Mock RSS feed response
        mock_parse.return_value = MagicMock(
            bozo=False,
            entries=[
                MagicMock(
                    title="Test Laravel Article",
                    link="https://laravel-news.com/test-article",
                    summary="This is a test article about Laravel",
                    published_parsed=(2024, 1, 1, 0, 0, 0, 0, 0, 0),
                    tags=[{'term': 'laravel'}, {'term': 'testing'}],
                    author="Test Author",
                    id="test-guid"
                )
            ]
        )
        
        result = aggregator.fetch_articles(limit=1)
        
        assert len(result) == 1
        mock_parse.assert_called_once_with(LaravelNewsAggregator.RSS_FEED_URL)
    
    def test_determine_resource_type(self, aggregator):
        """Test resource type determination."""
        assert aggregator._determine_resource_type("Laravel Tutorial: Authentication", []) == ResourceType.TUTORIAL
        assert aggregator._determine_resource_type("Building an API", []) == ResourceType.ARTICLE
        assert aggregator._determine_resource_type("Laravel Podcast Episode 5", []) == ResourceType.PODCAST
    
    def test_estimate_difficulty(self, aggregator):
        """Test difficulty estimation."""
        assert aggregator._estimate_difficulty(
            "Getting Started with Laravel",
            "A beginner's guide",
            ["beginner"]
        ) == DifficultyLevel.BEGINNER
        
        assert aggregator._estimate_difficulty(
            "Advanced Laravel Patterns",
            "Deep dive into design patterns",
            ["advanced"]
        ) == DifficultyLevel.ADVANCED


class TestContentAggregatorManager:
    """Test content aggregator management."""
    
    @pytest.fixture
    def manager(self, temp_db):
        """Create a content aggregator manager."""
        return ContentAggregatorManager(temp_db)
    
    @patch.object(LaravelNewsAggregator, 'fetch_articles')
    @patch.object(SpatieBlogAggregator, 'fetch_tutorials')
    @patch.object(LaravelBootcampAggregator, 'fetch_bootcamp_content')
    def test_update_all(self, mock_bootcamp, mock_spatie, mock_news, manager):
        """Test updating all aggregators."""
        # Mock return values
        mock_news.return_value = [1, 2, 3]
        mock_spatie.return_value = [4, 5]
        mock_bootcamp.return_value = [6, 7, 8]
        
        results = manager.update_all()
        
        assert 'laravel-news' in results
        assert len(results['laravel-news']) == 3
        assert 'spatie-blog' in results
        assert len(results['spatie-blog']) == 2
        assert 'laravel-bootcamp' in results
        assert len(results['laravel-bootcamp']) == 3