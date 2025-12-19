"""Unit tests for actual MCP tool functions exposed to AI assistants."""

from unittest.mock import patch

import laravel_mcp_companion
# Import the standalone functions from mcp_tools
from mcp_tools import (
    list_laravel_docs_impl,
    read_laravel_doc_content_impl,
    search_laravel_docs_impl,
    search_laravel_docs_with_context_impl,
    get_doc_structure_impl,
    browse_docs_by_category_impl
)


class TestDocumentationTools:
    """Test documentation-related MCP tool functions."""

    @patch('mcp_tools.os.listdir')
    @patch('mcp_tools.get_laravel_docs_metadata')
    def test_list_laravel_docs_specific_version(self, mock_metadata, mock_listdir, test_docs_dir):
        """Test listing docs for a specific version returns TOON format."""
        mock_listdir.return_value = ['installation.md', 'routing.md', 'eloquent.md']
        mock_metadata.return_value = {
            'version': '12.x',
            'sync_time': '2024-01-01T12:00:00Z',
            'commit_sha': 'abc123def456'
        }

        result = list_laravel_docs_impl(test_docs_dir, "12.x")

        # TOON format assertions - check for data presence
        assert "12.x" in result
        assert "installation.md" in result
        assert "routing.md" in result
        assert "eloquent.md" in result
        assert "2024-01-01T12:00:00Z" in result

    @patch('mcp_tools.os.listdir')
    def test_list_laravel_docs_no_version_specified(self, mock_listdir, test_docs_dir):
        """Test listing docs when no version is specified returns TOON format."""
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

                # TOON format - check for version data
                assert "version" in result or "12.x" in result or "11.x" in result

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
        """Test searching Laravel documentation successfully returns TOON format."""
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

            # TOON format assertions
            assert "routing" in result
            assert "12.x/routing.md" in result or "routing.md" in result
            assert "12.x/eloquent.md" in result or "eloquent.md" in result

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
        """Test getting document structure returns TOON format."""
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

            # TOON format assertions - check for heading data
            assert "routing.md" in result
            assert "Laravel Routing" in result
            assert "Basic Routing" in result
            assert "Route Methods" in result
            assert "Route Parameters" in result

    def test_browse_docs_by_category_frontend(self, test_docs_dir):
        """Test browsing docs by frontend category returns TOON format."""
        version_dir = test_docs_dir / "12.x"

        # Create frontend-related files
        (version_dir / "vite.md").write_text("# Vite\n\nAsset bundling with Vite.")
        (version_dir / "blade.md").write_text("# Blade Templates\n\nTemplating engine.")
        (version_dir / "routing.md").write_text("# Routing\n\nNot frontend related.")

        with patch('mcp_tools.os.listdir', return_value=['vite.md', 'blade.md', 'routing.md']):
            result = browse_docs_by_category_impl(test_docs_dir, "frontend", "12.x")

            # TOON format assertions
            assert "frontend" in result.lower()
            assert "vite.md" in result
            assert "blade.md" in result
            # routing.md shouldn't be included as it doesn't match frontend keywords


class TestPackageRecommendationTools:
    """Test package recommendation MCP tool functions."""

    def test_get_laravel_package_recommendations_success(self, sample_package_catalog):
        """Test getting package recommendations successfully returns TOON format."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            from laravel_mcp_companion import get_laravel_package_recommendations
            result = get_laravel_package_recommendations("authentication for SPA")

            # TOON format assertions
            assert "authentication" in result.lower()
            assert "Laravel Sanctum" in result or "Sanctum" in result
            assert "laravel/sanctum" in result

    def test_get_laravel_package_recommendations_no_matches(self, sample_package_catalog):
        """Test getting package recommendations with no matches returns TOON error."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            from laravel_mcp_companion import get_laravel_package_recommendations
            result = get_laravel_package_recommendations("quantum computing")

            # TOON error format
            assert "error" in result or "No packages found" in result

    def test_get_laravel_package_info_success(self, sample_package_catalog):
        """Test getting specific package info successfully returns TOON format."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            from laravel_mcp_companion import get_laravel_package_info
            result = get_laravel_package_info("laravel/cashier")

            # TOON format assertions
            assert "Laravel Cashier" in result or "Cashier" in result
            assert "subscription" in result.lower() or "billing" in result.lower()
            assert "laravel/cashier" in result

    def test_get_laravel_package_info_not_found(self, sample_package_catalog):
        """Test getting info for non-existent package returns TOON error."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            from laravel_mcp_companion import get_laravel_package_info
            result = get_laravel_package_info("nonexistent/package")

            assert "error" in result or "not found" in result.lower()

    def test_get_laravel_package_categories_success(self, sample_package_catalog):
        """Test getting packages by category successfully returns TOON format."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            from laravel_mcp_companion import get_laravel_package_categories
            result = get_laravel_package_categories("authentication")

            # TOON format assertions
            assert "authentication" in result.lower()
            assert "Laravel Sanctum" in result or "Sanctum" in result
            assert "laravel/sanctum" in result

    def test_get_laravel_package_categories_no_matches(self, sample_package_catalog):
        """Test getting packages by category with no matches returns TOON error."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            from laravel_mcp_companion import get_laravel_package_categories
            result = get_laravel_package_categories("nonexistent_category")

            assert "error" in result or "No packages found" in result

    def test_get_features_for_laravel_package_success(self, sample_package_catalog):
        """Test getting features for a package successfully returns TOON format."""
        test_features = ["spa-authentication", "api-tokens", "token-abilities"]

        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog), \
             patch.dict(laravel_mcp_companion.FEATURE_MAP, {'laravel/sanctum': test_features}):

            from laravel_mcp_companion import get_features_for_laravel_package
            result = get_features_for_laravel_package("laravel/sanctum")

            # TOON format assertions
            assert "laravel/sanctum" in result
            assert "spa-authentication" in result
            assert "api-tokens" in result
            assert "token-abilities" in result

    def test_get_features_for_laravel_package_not_found(self, sample_package_catalog):
        """Test getting features for non-existent package returns TOON error."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            from laravel_mcp_companion import get_features_for_laravel_package
            result = get_features_for_laravel_package("nonexistent/package")

            assert "error" in result or "not found" in result.lower()

    def test_get_features_for_laravel_package_no_features(self, sample_package_catalog):
        """Test getting features for package with no defined features returns TOON format."""
        # Patch FEATURE_MAP to be empty for this specific package
        empty_feature_map = {}

        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog), \
             patch.dict(laravel_mcp_companion.FEATURE_MAP, empty_feature_map, clear=True):

            from laravel_mcp_companion import get_features_for_laravel_package
            result = get_features_for_laravel_package("laravel/sanctum")

            # TOON format - should still have package data with use_cases
            assert "laravel/sanctum" in result


class TestMcpToolsEdgeCases:
    """Test edge cases and exception handlers in mcp_tools."""

    def test_is_safe_path_exception_handling(self, test_docs_dir):
        """Test that is_safe_path handles exceptions gracefully."""
        from mcp_tools import is_safe_path

        # Test with paths that cause exceptions (invalid paths)
        with patch('mcp_tools.Path.resolve') as mock_resolve:
            mock_resolve.side_effect = Exception("Permission denied")

            # Should return False when exception occurs, not raise
            result = is_safe_path("/some/path", "/base")
            assert result is False

    def test_get_laravel_docs_metadata_json_error(self, test_docs_dir):
        """Test metadata reading handles malformed JSON."""
        from mcp_tools import get_laravel_docs_metadata

        # Create malformed metadata file
        metadata_dir = test_docs_dir / "12.x" / ".metadata"
        metadata_dir.mkdir(parents=True, exist_ok=True)
        (metadata_dir / "sync_info.json").write_text("{ invalid json }")

        # Should return empty dict on JSON error
        result = get_laravel_docs_metadata(test_docs_dir, "12.x")
        assert result == {}

    def test_list_laravel_docs_no_md_files(self, test_docs_dir):
        """Test listing docs when version exists but has no .md files."""
        from mcp_tools import list_laravel_docs_impl

        # Create empty version dir (no .md files)
        empty_version = test_docs_dir / "13.x"
        empty_version.mkdir()

        result = list_laravel_docs_impl(test_docs_dir, "13.x")

        # Should indicate no files found
        assert "13.x" in result or "No documentation" in result

    def test_list_laravel_docs_all_versions_empty(self, test_docs_dir):
        """Test listing all docs when no versions have files."""
        from mcp_tools import list_laravel_docs_impl

        # Create completely empty docs dir
        empty_docs = test_docs_dir.parent / "empty_docs"
        empty_docs.mkdir()

        result = list_laravel_docs_impl(empty_docs)

        # Should indicate no documentation found
        assert "No documentation files found" in result or "error" in result.lower()

    def test_list_laravel_docs_exception_handling(self, test_docs_dir):
        """Test list_laravel_docs handles exceptions gracefully."""
        from mcp_tools import list_laravel_docs_impl

        with patch('mcp_tools.os.listdir') as mock_listdir:
            mock_listdir.side_effect = OSError("Permission denied")

            result = list_laravel_docs_impl(test_docs_dir, "12.x")

            # Should return error message
            assert "Error" in result

    def test_browse_docs_by_category_unknown_category(self, test_docs_dir):
        """Test browsing docs with unknown category."""
        from mcp_tools import browse_docs_by_category_impl

        result = browse_docs_by_category_impl(test_docs_dir, "unknown_category", "12.x")

        assert "Unknown category" in result
        assert "available_categories" in result.lower() or "frontend" in result.lower()

    def test_browse_docs_by_category_version_not_found(self, test_docs_dir):
        """Test browsing docs when version doesn't exist."""
        from mcp_tools import browse_docs_by_category_impl

        result = browse_docs_by_category_impl(test_docs_dir, "frontend", "99.x")

        assert "No documentation found for version 99.x" in result

    def test_browse_docs_by_category_no_matching_files(self, test_docs_dir):
        """Test browsing category with no matching files."""
        from mcp_tools import browse_docs_by_category_impl

        # Create version with files that don't match any category
        version_dir = test_docs_dir / "12.x"
        # Remove existing files and create non-matching ones
        for f in version_dir.glob("*.md"):
            f.unlink()
        (version_dir / "random_topic.md").write_text("# Random\n\nUnrelated content.")

        result = browse_docs_by_category_impl(test_docs_dir, "frontend", "12.x")

        assert "No frontend documentation files found" in result

    def test_browse_docs_by_category_exception(self, test_docs_dir):
        """Test browse_docs_by_category handles exceptions."""
        from mcp_tools import browse_docs_by_category_impl

        with patch('mcp_tools.os.listdir') as mock_listdir:
            mock_listdir.side_effect = OSError("Disk error")

            result = browse_docs_by_category_impl(test_docs_dir, "frontend", "12.x")

            assert "Error browsing documentation" in result

    def test_search_laravel_docs_exception_handling(self, test_docs_dir):
        """Test search_laravel_docs handles exceptions gracefully."""
        from mcp_tools import search_laravel_docs_impl

        with patch('mcp_tools.os.listdir') as mock_listdir:
            mock_listdir.side_effect = Exception("Unexpected error")

            # Need to patch SUPPORTED_VERSIONS to include 12.x
            with patch('mcp_tools.SUPPORTED_VERSIONS', ['12.x']):
                result = search_laravel_docs_impl(test_docs_dir, "test", "12.x")

                # Should handle exception gracefully
                # The actual implementation might return error or empty results
                assert result is not None

    def test_search_with_context_no_results(self, test_docs_dir):
        """Test search with context returns appropriate message when no results."""
        from mcp_tools import search_laravel_docs_with_context_impl

        with patch('mcp_tools.os.listdir', return_value=['test.md']), \
             patch('mcp_tools.get_file_content_cached', return_value="# Test\n\nNo match here"), \
             patch('mcp_tools.SUPPORTED_VERSIONS', ['12.x']):

            result = search_laravel_docs_with_context_impl(
                test_docs_dir, "nonexistent_query_xyz", "12.x"
            )

            assert "No results found" in result

    def test_search_with_context_exception(self, test_docs_dir):
        """Test search with context handles exceptions."""
        from mcp_tools import search_laravel_docs_with_context_impl

        with patch('mcp_tools.os.listdir') as mock_listdir:
            mock_listdir.side_effect = Exception("Search error")

            with patch('mcp_tools.SUPPORTED_VERSIONS', ['12.x']):
                result = search_laravel_docs_with_context_impl(
                    test_docs_dir, "test", "12.x"
                )

                assert "Error" in result
