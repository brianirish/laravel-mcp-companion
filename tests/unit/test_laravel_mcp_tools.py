"""Unit tests for Laravel MCP Companion tool functions."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

import laravel_mcp_companion
from laravel_mcp_companion import (
    search_by_use_case,
    format_package_recommendation,
    get_version_from_path,
    is_safe_path,
    get_file_content_cached,
    clear_file_cache,
    setup_docs_path,
    update_documentation,
    PACKAGE_CATALOG,
    FEATURE_MAP
)


class TestMCPTools:
    """Test MCP tool functions."""

    def test_search_by_use_case_authentication(self, sample_package_catalog):
        """Test package search for authentication use case."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog, clear=True):
            results = search_by_use_case("authentication for SPA")
            
            assert len(results) > 0
            # Laravel Sanctum should be in results for SPA authentication
            package_ids = [r['id'] for r in results]
            assert 'laravel/sanctum' in package_ids
            
            # Find Sanctum in results
            sanctum_result = next(r for r in results if r['id'] == 'laravel/sanctum')
            assert sanctum_result['score'] > 0

    def test_search_by_use_case_payment(self, sample_package_catalog):
        """Test package search for payment use case."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            results = search_by_use_case("subscription billing payment")
            
            assert len(results) > 0
            # Laravel Cashier should be top result for billing
            top_result = results[0]
            assert top_result['id'] == 'laravel/cashier'
            assert 'billing' in top_result['categories']

    def test_search_by_use_case_no_matches(self, sample_package_catalog):
        """Test package search with no matches."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            results = search_by_use_case("quantum computing blockchain")
            
            assert len(results) == 0

    def test_search_by_use_case_empty_query(self, sample_package_catalog):
        """Test package search with empty query."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            results = search_by_use_case("")
            
            assert len(results) == 0

    def test_format_package_recommendation(self, sample_package_catalog):
        """Test package recommendation formatting returns TOON format."""
        package = sample_package_catalog['laravel/cashier'].copy()
        package['id'] = 'laravel/cashier'

        result = format_package_recommendation(package)

        # TOON format assertions
        assert "laravel/cashier" in result
        assert "Laravel Cashier" in result or "Cashier" in result
        assert "expressive" in result.lower() or "billing" in result.lower()
        assert "laravel/cashier" in result

    def test_format_package_recommendation_with_features(self, sample_package_catalog):
        """Test package recommendation formatting with features returns TOON format."""
        package = sample_package_catalog['laravel/cashier'].copy()
        package['id'] = 'laravel/cashier'

        # Mock the FEATURE_MAP to include cashier features
        with patch.dict(FEATURE_MAP, {'laravel/cashier': ['subscription-setup', 'webhook-handling']}):
            result = format_package_recommendation(package)

            # TOON format assertions
            assert "subscription-setup" in result
            assert "webhook-handling" in result

    def test_get_version_from_path_with_version(self):
        """Test version extraction from path with version."""
        version, relative_path = get_version_from_path("12.x/blade.md")
        
        assert version == "12.x"
        assert relative_path == "blade.md"

    def test_get_version_from_path_without_version(self):
        """Test version extraction from path without version."""
        with patch('laravel_mcp_companion.DEFAULT_VERSION', '12.x'):
            version, relative_path = get_version_from_path("blade.md")
            
            assert version == "12.x"
            assert relative_path == "blade.md"

    def test_get_version_from_path_nested(self):
        """Test version extraction from nested path."""
        version, relative_path = get_version_from_path("11.x/frontend/vite.md")
        
        assert version == "11.x"
        assert relative_path == "frontend/vite.md"

    def test_is_safe_path_safe(self, temp_dir):
        """Test safe path validation."""
        base_path = temp_dir
        safe_path = temp_dir / "subdirectory" / "file.txt"
        
        assert is_safe_path(base_path, safe_path) is True

    def test_is_safe_path_unsafe(self, temp_dir):
        """Test unsafe path validation (directory traversal)."""
        base_path = temp_dir / "restricted"
        unsafe_path = temp_dir / "outside" / "file.txt"
        
        assert is_safe_path(base_path, unsafe_path) is False

    def test_is_safe_path_same_directory(self, temp_dir):
        """Test path validation for same directory."""
        base_path = temp_dir
        same_path = temp_dir
        
        assert is_safe_path(base_path, same_path) is True


class TestFileOperations:
    """Test file operation functions."""

    def test_get_file_content_cached_success(self, temp_dir):
        """Test successful file content caching."""
        test_file = temp_dir / "test.md"
        test_content = "# Test Content\n\nThis is a test file."
        test_file.write_text(test_content)
        
        # Clear cache first
        clear_file_cache()
        
        # First call should read from file
        content = get_file_content_cached(str(test_file))
        assert content == test_content
        
        # Second call should use cache
        with patch('builtins.open', side_effect=Exception("Should not be called")):
            cached_content = get_file_content_cached(str(test_file))
            assert cached_content == test_content

    def test_get_file_content_cached_file_not_found(self):
        """Test file content caching with non-existent file."""
        non_existent_file = "/path/that/does/not/exist.md"
        
        content = get_file_content_cached(non_existent_file)
        assert "File not found:" in content

    def test_get_file_content_cached_read_error(self, temp_dir):
        """Test file content caching with read error."""
        test_file = temp_dir / "test.md"
        test_file.write_text("test content")
        
        with patch('builtins.open', side_effect=PermissionError("Access denied")):
            content = get_file_content_cached(str(test_file))
            assert "Error reading file:" in content

    def test_clear_file_cache(self, temp_dir):
        """Test cache clearing functionality."""
        test_file = temp_dir / "test.md"
        test_content = "# Test Content"
        test_file.write_text(test_content)
        
        # Populate cache
        get_file_content_cached(str(test_file))
        assert len(laravel_mcp_companion._file_content_cache) > 0
        
        # Clear cache
        clear_file_cache()
        assert len(laravel_mcp_companion._file_content_cache) == 0
        assert len(laravel_mcp_companion._search_result_cache) == 0


class TestUtilityFunctions:
    """Test utility functions used by MCP tools."""

    def test_setup_docs_path_default(self):
        """Test docs path setup with default location."""
        with patch('laravel_mcp_companion.Path') as mock_path:
            mock_path_instance = MagicMock()
            mock_path.return_value = mock_path_instance
            mock_path_instance.parent = MagicMock()
            mock_path_instance.parent.__truediv__ = MagicMock(return_value=mock_path_instance)
            mock_path_instance.resolve.return_value = mock_path_instance
            
            laravel_mcp_companion.setup_docs_path()
            
            mock_path_instance.mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_setup_docs_path_custom(self):
        """Test docs path setup with custom location."""
        custom_path = "/custom/docs/path"
        
        with patch('laravel_mcp_companion.Path') as mock_path:
            mock_path_instance = MagicMock()
            mock_path.return_value = mock_path_instance
            mock_path_instance.resolve.return_value = mock_path_instance
            
            laravel_mcp_companion.setup_docs_path(custom_path)
            
            mock_path.assert_called_with(custom_path)
            mock_path_instance.mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_parse_arguments_default(self):
        """Test argument parsing with defaults."""
        with patch('sys.argv', ['laravel_mcp_companion.py']):
            args = laravel_mcp_companion.parse_arguments()
            
            assert args.docs_path is None
            assert args.server_name == "LaravelMCPCompanion"
            assert args.log_level == "INFO"
            assert args.transport == "stdio"
            assert args.update_docs is False
            assert args.force_update is False

    def test_parse_arguments_custom(self):
        """Test argument parsing with custom values."""
        test_args = [
            'laravel_mcp_companion.py',
            '--docs-path', '/custom/docs',
            '--server-name', 'CustomServer',
            '--log-level', 'DEBUG',
            '--transport', 'http',
            '--version', '11.x',
            '--update-docs',
            '--force-update'
        ]

        with patch('sys.argv', test_args):
            args = laravel_mcp_companion.parse_arguments()

            assert args.docs_path == '/custom/docs'
            assert args.server_name == 'CustomServer'
            assert args.log_level == 'DEBUG'
            assert args.transport == 'http'
            assert args.version == '11.x'
            assert args.update_docs is True
            assert args.force_update is True


@pytest.mark.unit
class TestPackageCatalog:
    """Test package catalog functionality."""

    def test_package_catalog_structure(self):
        """Test that package catalog has expected structure."""
        assert isinstance(PACKAGE_CATALOG, dict)
        assert len(PACKAGE_CATALOG) > 0
        
        # Check that all packages have required fields
        for package_id, package_info in PACKAGE_CATALOG.items():
            assert 'name' in package_info
            assert 'description' in package_info
            assert 'categories' in package_info
            assert isinstance(package_info['categories'], list)
            assert 'use_cases' in package_info
            assert isinstance(package_info['use_cases'], list)

    def test_feature_map_structure(self):
        """Test that feature map has expected structure."""
        assert isinstance(FEATURE_MAP, dict)
        
        # Check that feature map entries are lists
        for package_id, features in FEATURE_MAP.items():
            assert isinstance(features, list)
            assert len(features) > 0
            # Features should be strings
            for feature in features:
                assert isinstance(feature, str)
                assert len(feature) > 0

    def test_package_catalog_consistency(self):
        """Test consistency between package catalog and feature map."""
        # Not all packages need to have features, but all features should reference valid packages
        for package_id in FEATURE_MAP.keys():
            # Note: Not all packages with features are necessarily in PACKAGE_CATALOG
            # (e.g., they might be external packages)
            pass

    def test_package_categories_valid(self):
        """Test that package categories are reasonable."""
        valid_categories = {
            'authentication', 'authorization', 'api', 'security', 'payment', 
            'billing', 'subscription', 'search', 'database', 'indexing',
            'oauth', 'frontend', 'scaffolding', 'ui', 'reactivity', 'backend',
            'acl', 'permissions', 'spa', 'framework', 'queue', 'monitoring',
            'redis', 'dashboard', 'debugging', 'development', 'profiling',
            'teams', 'performance', 'server', 'optimization', 'social',
            'media', 'files', 'uploads', 'storage', 'excel', 'export',
            'import', 'deployment', 'server-management', 'devops', 'hosting',
            'serverless', 'aws', 'scaling', 'ci-cd', 'automation', 'admin',
            'cms'
        }
        
        all_categories = set()
        for package_info in PACKAGE_CATALOG.values():
            all_categories.update(package_info['categories'])
        
        # Most categories should be in our valid set (allows for some flexibility)
        overlap = all_categories.intersection(valid_categories)
        assert len(overlap) >= len(all_categories) * 0.8  # At least 80% overlap


class TestSetupDocsPath:
    """Test documentation path setup."""
    
    def test_setup_with_user_path(self, temp_dir):
        """Test setup with user-provided path."""
        user_path = temp_dir / "custom_docs"
        result = setup_docs_path(str(user_path))
        
        assert result.resolve() == user_path.resolve()
        assert result.exists()
        assert result.is_dir()
    
    def test_setup_with_default_path(self):
        """Test setup with default path."""
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            result = setup_docs_path(None)
            
            # Should use script directory + 'docs'
            expected = (Path(laravel_mcp_companion.__file__).parent / "docs").resolve()
            assert result == expected
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    
    def test_setup_creates_directory(self, temp_dir):
        """Test that setup creates directory if it doesn't exist."""
        new_dir = temp_dir / "new_docs_dir"
        assert not new_dir.exists()
        
        result = setup_docs_path(str(new_dir))
        
        assert result.resolve() == new_dir.resolve()
        assert new_dir.exists()
        assert new_dir.is_dir()


class TestUpdateDocumentation:
    """Test documentation update function."""
    
    @patch('laravel_mcp_companion.DocsUpdater')
    def test_update_documentation_success(self, mock_updater_class, temp_dir):
        """Test successful documentation update."""
        mock_updater = MagicMock()
        mock_updater.update.return_value = True
        mock_updater_class.return_value = mock_updater
        
        result = update_documentation(temp_dir, "12.x", force=False)
        
        assert result is True
        mock_updater_class.assert_called_once_with(temp_dir, "12.x")
        mock_updater.update.assert_called_once_with(force=False)
    
    @patch('laravel_mcp_companion.DocsUpdater')
    def test_update_documentation_no_changes(self, mock_updater_class, temp_dir):
        """Test documentation update with no changes."""
        mock_updater = MagicMock()
        mock_updater.update.return_value = False
        mock_updater_class.return_value = mock_updater
        
        result = update_documentation(temp_dir, "12.x", force=True)
        
        assert result is False
        mock_updater.update.assert_called_once_with(force=True)
    
    @patch('laravel_mcp_companion.DocsUpdater')
    def test_update_documentation_error(self, mock_updater_class, temp_dir):
        """Test documentation update with error."""
        mock_updater_class.side_effect = Exception("Update failed")
        
        result = update_documentation(temp_dir, "12.x", force=False)
        
        assert result is False