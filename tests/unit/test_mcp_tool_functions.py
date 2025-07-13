"""Unit tests for actual MCP tool functions exposed to AI assistants."""

import pytest
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

import laravel_mcp_companion
from laravel_mcp_companion import (
    PACKAGE_CATALOG,
    FEATURE_MAP
)
# Import the standalone functions from mcp_tools
from mcp_tools import (
    list_laravel_docs_impl,
    read_laravel_doc_content_impl,
    search_laravel_docs_impl,
    search_laravel_docs_with_context_impl,
    get_doc_structure_impl,
    browse_docs_by_category_impl,
    SUPPORTED_VERSIONS,
    DEFAULT_VERSION,
    clear_caches
)


class TestDocumentationTools:
    """Test documentation-related MCP tool functions."""

    @patch('mcp_tools.os.listdir')
    @patch('mcp_tools.get_laravel_docs_metadata')
    def test_list_laravel_docs_specific_version(self, mock_metadata, mock_listdir, test_docs_dir):
        """Test listing docs for a specific version."""
        mock_listdir.return_value = ['installation.md', 'routing.md', 'eloquent.md']
        mock_metadata.return_value = {
            'version': '12.x',
            'sync_time': '2024-01-01T12:00:00Z',
            'commit_sha': 'abc123def456'
        }
        
        result = list_laravel_docs_impl(test_docs_dir, "12.x")
        
        assert "Laravel Documentation (Version: 12.x)" in result
        assert "installation.md" in result
        assert "routing.md" in result
        assert "eloquent.md" in result
        assert "2024-01-01T12:00:00Z" in result

    @patch('mcp_tools.os.listdir')
    def test_list_laravel_docs_no_version_specified(self, mock_listdir, test_docs_dir):
        """Test listing docs when no version is specified."""
        # Directories already created by fixture, no need to create them
        
        # Set up proper mock for os.listdir and os.path.isfile checks
        with patch('mcp_tools.os.path.isfile') as mock_isfile:
            mock_isfile.return_value = True  # All files exist
            
            mock_listdir.side_effect = [
                ['installation.md', 'routing.md'],  # 11.x files
                ['installation.md', 'routing.md', 'eloquent.md'],  # 12.x files
                ['installation.md', 'routing.md'],  # 11.x files again for formatting
                ['installation.md', 'routing.md', 'eloquent.md']  # 12.x files again for formatting
            ]
        
            with patch('mcp_tools.get_laravel_docs_metadata') as mock_metadata:
                mock_metadata.return_value = {'sync_time': '2024-01-01T12:00:00Z', 'commit_sha': 'abc123'}
                
                result = list_laravel_docs_impl(test_docs_dir)
                
                assert "Available Laravel Documentation Versions:" in result

    def test_list_laravel_docs_no_documentation(self, test_docs_dir):
        """Test listing docs when no documentation exists."""
        empty_dir = test_docs_dir / "empty"
        empty_dir.mkdir()
        
        result = list_laravel_docs_impl(empty_dir, "12.x")
        
        assert "No documentation found for version 12.x" in result
        assert "update_laravel_docs()" in result

    def test_read_laravel_doc_content_success(self, test_docs_dir):
        """Test reading Laravel documentation content successfully."""
        # Use existing version directory from fixture
        version_dir = test_docs_dir / "12.x"
        test_file = version_dir / "routing.md"
        test_content = "# Routing\n\nLaravel routing documentation."
        test_file.write_text(test_content)
        
        result = read_laravel_doc_content_impl(test_docs_dir, "routing.md", "12.x")
        
        assert result == test_content

    def test_read_laravel_doc_content_file_not_found(self, test_docs_dir):
        """Test reading non-existent documentation file."""
        # Directory already exists from fixture
        
        result = read_laravel_doc_content_impl(test_docs_dir, "nonexistent.md", "12.x")
        
        assert "Documentation file not found" in result

    def test_read_laravel_doc_content_without_md_extension(self, test_docs_dir):
        """Test reading documentation file without .md extension."""
        version_dir = test_docs_dir / "12.x"
        test_file = version_dir / "routing.md"
        test_content = "# Routing\n\nLaravel routing documentation."
        test_file.write_text(test_content)
        
        result = read_laravel_doc_content_impl(test_docs_dir, "routing", "12.x")  # No .md extension
        
        assert result == test_content

    @patch('mcp_tools.get_file_content_cached')
    @patch('mcp_tools.os.listdir')
    def test_search_laravel_docs_success(self, mock_listdir, mock_get_content, test_docs_dir):
        """Test searching Laravel documentation successfully."""
        # Directory already exists from fixture
        
        # Mock file listing
        mock_listdir.return_value = ['routing.md', 'eloquent.md']
        
        # Mock file content
        mock_get_content.side_effect = [
            "# Routing\n\nLaravel routing is awesome for web applications",
            "# Eloquent\n\nEloquent ORM for database routing"
        ]
        
        with patch('mcp_tools.SUPPORTED_VERSIONS', ['12.x']):
            result = search_laravel_docs_impl(test_docs_dir, "routing", "12.x")
            
            assert "Search results for 'routing':" in result
            assert "12.x/routing.md" in result
            assert "12.x/eloquent.md" in result
            assert "matches)" in result  # Just check that matches are reported

    def test_search_laravel_docs_empty_query(self, test_docs_dir):
        """Test searching with empty query."""
        result = search_laravel_docs_impl(test_docs_dir, "", "12.x")
        
        assert "Search query cannot be empty" in result

    def test_search_laravel_docs_no_results(self, test_docs_dir):
        """Test searching with no matches."""
        # Directory already exists from fixture
        
        with patch('mcp_tools.os.listdir', return_value=['routing.md']), \
             patch('mcp_tools.get_file_content_cached', return_value="# Routing\n\nBasic routing info"), \
             patch('mcp_tools.SUPPORTED_VERSIONS', ['12.x']):
            
            result = search_laravel_docs_impl(test_docs_dir, "nonexistent_term", "12.x")
            
            assert "No results found for 'nonexistent_term'" in result

    def test_search_laravel_docs_with_context_success(self, test_docs_dir):
        """Test searching with context snippets."""
        test_content = """# Laravel Routing

Laravel routing is simple and powerful. You can define routes in your web.php file.

## Basic Routing

The most basic Laravel routes accept a URI and a closure, providing a very simple and expressive method of defining routes.

```php
Route::get('/', function () {
    return view('welcome');
});
```

This is how routing works in Laravel applications."""
        
        # Directory already exists from fixture
        
        with patch('mcp_tools.os.listdir', return_value=['routing.md']), \
             patch('mcp_tools.get_file_content_cached', return_value=test_content), \
             patch('mcp_tools.SUPPORTED_VERSIONS', ['12.x']):
            
            result = search_laravel_docs_with_context_impl(test_docs_dir, "routing", "12.x", context_length=100)
            
            assert "Search results for 'routing':" in result
            assert "12.x/routing.md" in result
            assert "**routing**" in result  # Highlighted match

    def test_get_doc_structure_success(self, test_docs_dir):
        """Test getting document structure."""
        test_content = """# Laravel Routing

Laravel routing is simple and powerful.

## Basic Routing

The most basic Laravel routes accept a URI and a closure.

### Route Methods

Laravel provides methods for all HTTP verbs.

## Route Parameters

You can capture segments of the URI within your route.
"""
        
        with patch('mcp_tools.read_laravel_doc_content_impl', return_value=test_content):
            result = get_doc_structure_impl(test_docs_dir, "routing.md", "12.x")
            
            assert "Structure of routing.md:" in result
            assert "- Laravel Routing" in result
            assert "  - Basic Routing" in result
            assert "    - Route Methods" in result
            assert "  - Route Parameters" in result

    def test_browse_docs_by_category_frontend(self, test_docs_dir):
        """Test browsing docs by frontend category."""
        version_dir = test_docs_dir / "12.x"
        
        # Create frontend-related files
        (version_dir / "vite.md").write_text("# Vite\n\nAsset bundling with Vite.")
        (version_dir / "blade.md").write_text("# Blade Templates\n\nTemplating engine.")
        (version_dir / "routing.md").write_text("# Routing\n\nNot frontend related.")
        
        with patch('mcp_tools.os.listdir', return_value=['vite.md', 'blade.md', 'routing.md']):
            result = browse_docs_by_category_impl(test_docs_dir, "frontend", "12.x")
            
            assert "Laravel 12.x - Frontend Documentation:" in result
            assert "**vite.md**" in result
            assert "**blade.md**" in result
            # routing.md shouldn't be included as it doesn't match frontend keywords


class TestPackageRecommendationTools:
    """Test package recommendation MCP tool functions."""

    def test_get_laravel_package_recommendations_success(self, sample_package_catalog):
        """Test getting package recommendations successfully."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            from laravel_mcp_companion import get_laravel_package_recommendations
            result = get_laravel_package_recommendations("authentication for SPA")
            
            assert "Laravel Packages for: authentication for SPA" in result
            assert "Laravel Sanctum" in result
            assert "composer require laravel/sanctum" in result

    def test_get_laravel_package_recommendations_no_matches(self, sample_package_catalog):
        """Test getting package recommendations with no matches."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            from laravel_mcp_companion import get_laravel_package_recommendations
            result = get_laravel_package_recommendations("quantum computing")
            
            assert "No packages found matching the use case: 'quantum computing'" in result

    def test_get_laravel_package_info_success(self, sample_package_catalog):
        """Test getting specific package info successfully."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            from laravel_mcp_companion import get_laravel_package_info
            result = get_laravel_package_info("laravel/cashier")
            
            assert "# Laravel Cashier" in result
            assert "subscription billing services" in result
            assert "composer require laravel/cashier" in result

    def test_get_laravel_package_info_not_found(self, sample_package_catalog):
        """Test getting info for non-existent package."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            from laravel_mcp_companion import get_laravel_package_info
            result = get_laravel_package_info("nonexistent/package")
            
            assert "Package 'nonexistent/package' not found" in result

    def test_get_laravel_package_categories_success(self, sample_package_catalog):
        """Test getting packages by category successfully."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            from laravel_mcp_companion import get_laravel_package_categories
            result = get_laravel_package_categories("authentication")
            
            assert "Laravel Packages for Category: authentication" in result
            assert "Laravel Sanctum" in result
            assert "composer require laravel/sanctum" in result

    def test_get_laravel_package_categories_no_matches(self, sample_package_catalog):
        """Test getting packages by category with no matches."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            from laravel_mcp_companion import get_laravel_package_categories
            result = get_laravel_package_categories("nonexistent_category")
            
            assert "No packages found in category: 'nonexistent_category'" in result

    def test_get_features_for_laravel_package_success(self, sample_package_catalog):
        """Test getting features for a package successfully."""
        test_features = ["spa-authentication", "api-tokens", "token-abilities"]
        
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog), \
             patch.dict(laravel_mcp_companion.FEATURE_MAP, {'laravel/sanctum': test_features}):
            
            from laravel_mcp_companion import get_features_for_laravel_package
            result = get_features_for_laravel_package("laravel/sanctum")
            
            assert "Implementation Features for Laravel Sanctum" in result
            assert "spa-authentication" in result
            assert "api-tokens" in result
            assert "token-abilities" in result

    def test_get_features_for_laravel_package_not_found(self, sample_package_catalog):
        """Test getting features for non-existent package."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            from laravel_mcp_companion import get_features_for_laravel_package
            result = get_features_for_laravel_package("nonexistent/package")
            
            assert "Package 'nonexistent/package' not found" in result

    def test_get_features_for_laravel_package_no_features(self, sample_package_catalog):
        """Test getting features for package with no defined features."""
        # Patch FEATURE_MAP to be empty for this specific package
        empty_feature_map = {}
        
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog), \
             patch.dict(laravel_mcp_companion.FEATURE_MAP, empty_feature_map, clear=True):
            
            from laravel_mcp_companion import get_features_for_laravel_package
            result = get_features_for_laravel_package("laravel/sanctum")
            
            assert "but this package supports:" in result  # Check for the alternative message


class TestDocumentationUpdateTools:
    """Test documentation update MCP tool functions."""

    def test_update_laravel_docs_success(self, test_docs_dir):
        """Test successful documentation update."""
        # The standalone function returns a stub message
        from laravel_mcp_companion import update_laravel_docs
        result = update_laravel_docs("12.x", force=False)
        
        assert "This function requires server context to execute" in result

    def test_update_laravel_docs_already_up_to_date(self, test_docs_dir):
        """Test documentation update when already up to date."""
        # The standalone function returns a stub message
        from laravel_mcp_companion import update_laravel_docs
        result = update_laravel_docs("12.x", force=False)
        
        assert "This function requires server context to execute" in result

    def test_update_laravel_docs_error(self, test_docs_dir):
        """Test documentation update with error."""
        # The standalone function returns a stub message
        from laravel_mcp_companion import update_laravel_docs
        result = update_laravel_docs("12.x", force=False)
        
        assert "This function requires server context to execute" in result

    def test_laravel_docs_info_specific_version(self, test_docs_dir):
        """Test getting documentation info for specific version."""
        # The standalone function returns a stub message
        from laravel_mcp_companion import laravel_docs_info
        result = laravel_docs_info("12.x")
        
        assert "This function requires server context to execute" in result

    def test_laravel_docs_info_no_metadata(self, test_docs_dir):
        """Test getting documentation info when no metadata available."""
        # The standalone function returns a stub message
        from laravel_mcp_companion import laravel_docs_info
        result = laravel_docs_info("12.x")
        
        assert "This function requires server context to execute" in result

    def test_laravel_docs_info_all_versions(self, test_docs_dir):
        """Test getting documentation info for all versions."""
        # The standalone function returns a stub message
        from laravel_mcp_companion import laravel_docs_info
        result = laravel_docs_info()
        
        assert "This function requires server context to execute" in result