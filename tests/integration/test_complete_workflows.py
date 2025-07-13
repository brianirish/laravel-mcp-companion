"""Integration tests for complete Laravel MCP Companion workflows."""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import laravel_mcp_companion
from docs_updater import DocsUpdater, MultiSourceDocsUpdater


@pytest.mark.integration
class TestDocumentationWorkflows:
    """Test complete documentation workflows."""

    def test_full_documentation_update_and_search_workflow(self, test_docs_dir):
        """Test complete workflow: update docs, then search and read."""
        # Import standalone implementations
        from mcp_tools import (
            list_laravel_docs_impl,
            search_laravel_docs_impl,
            read_laravel_doc_content_impl,
            get_laravel_docs_metadata
        )
        
        # Setup: Mock the updater to simulate successful update
        with patch('docs_updater.DocsUpdater') as mock_updater_class:
            mock_updater = MagicMock()
            mock_updater.needs_update.return_value = True
            mock_updater.update.return_value = True
            mock_updater_class.return_value = mock_updater
            
            # Mock metadata after update
            with patch('mcp_tools.get_laravel_docs_metadata') as mock_metadata:
                mock_metadata.return_value = {
                    'commit_sha': 'abc123def456',
                    'commit_date': '2024-01-01T12:00:00Z',
                    'commit_message': 'Update documentation'
                }
                
                # Step 1: Update documentation (simulate with DocsUpdater)
                updater = DocsUpdater(test_docs_dir, "12.x")
                update_result = updater.update(force=False)
                assert update_result is True
                
                # Step 2: List available documentation
                with patch('mcp_tools.os.listdir', return_value=['routing.md', 'eloquent.md']):
                    list_result = list_laravel_docs_impl(test_docs_dir, "12.x")
                    assert "routing.md" in list_result
                    assert "eloquent.md" in list_result
                
                # Step 3: Search documentation
                with patch('mcp_tools.os.listdir', return_value=['routing.md']), \
                     patch('mcp_tools.get_file_content_cached', return_value="# Routing\n\nLaravel routing documentation."):
                    
                    search_result = search_laravel_docs_impl(test_docs_dir, "routing", "12.x")
                    assert "Search results for 'routing'" in search_result
                    assert "12.x/routing.md" in search_result
                
                # Step 4: Read specific documentation
                (test_docs_dir / "12.x" / "routing.md").write_text("# Routing\n\nDetailed routing info")
                
                read_result = read_laravel_doc_content_impl(test_docs_dir, "routing.md", "12.x")
                assert "# Routing" in read_result
                assert "Detailed routing info" in read_result

    def test_package_recommendation_workflow(self, sample_package_catalog):
        """Test complete package recommendation workflow."""
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, sample_package_catalog):
            # Step 1: Get recommendations for a use case
            from laravel_mcp_companion import get_laravel_package_recommendations
            recommendations = get_laravel_package_recommendations("authentication for single page applications")
            
            assert "Laravel Sanctum" in recommendations
            assert "composer require laravel/sanctum" in recommendations
            
            # Step 2: Get detailed info about specific package
            from laravel_mcp_companion import get_laravel_package_info
            package_info = get_laravel_package_info("laravel/sanctum")
            
            assert "# Laravel Sanctum" in package_info
            assert "featherweight authentication system" in package_info
            
            # Step 3: Get packages by category
            from laravel_mcp_companion import get_laravel_package_categories
            category_packages = get_laravel_package_categories("authentication")
            
            assert "Laravel Sanctum" in category_packages
            
            # Step 4: Get implementation features
            from laravel_mcp_companion import get_features_for_laravel_package
            with patch.dict(laravel_mcp_companion.FEATURE_MAP, {'laravel/sanctum': ['spa-auth', 'api-tokens']}):
                features = get_features_for_laravel_package("laravel/sanctum")
                
                assert "spa-auth" in features
                assert "api-tokens" in features

    def test_external_documentation_workflow(self, test_external_docs_dir):
        """Test external documentation fetching and reading workflow."""
        from docs_updater import ExternalDocsFetcher, MultiSourceDocsUpdater
        
        # Create an external docs fetcher
        external_fetcher = ExternalDocsFetcher(test_external_docs_dir.parent)
        
        # Step 1: List available services
        services = external_fetcher.list_available_services()
        assert "forge" in services
        assert "vapor" in services
        
        # Step 2: Update external documentation (simulate)
        with patch.object(external_fetcher, 'fetch_laravel_service_docs', return_value=True) as mock_fetch:
            result = external_fetcher.fetch_laravel_service_docs("forge")
            assert result is True
            
        # Step 3: Check that external docs exist
        # The test fixture should have created these files
        forge_dir = test_external_docs_dir / "forge"
        assert forge_dir.exists()
        assert (forge_dir / "introduction.md").exists()
        
        # Step 4: Read external documentation content
        content = (forge_dir / "introduction.md").read_text()
        assert "Forge" in content
        assert "Introduction" in content


@pytest.mark.integration
class TestErrorRecoveryWorkflows:
    """Test error recovery and resilience workflows."""

    def test_documentation_update_failure_recovery(self, test_docs_dir):
        """Test recovery from documentation update failures."""
        from docs_updater import DocsUpdater
        
        with patch.object(DocsUpdater, 'update') as mock_update:
            # First attempt fails
            mock_update.side_effect = Exception("Network error")
            
            updater = DocsUpdater(test_docs_dir, "12.x")
            
            # Should handle error gracefully
            try:
                result = updater.update(force=False)
            except Exception as e:
                # Error is expected
                assert "Network error" in str(e)
            
            # System should still be functional for other operations
            # Test that we can still read metadata
            metadata = updater.read_local_metadata()
            assert isinstance(metadata, dict)  # Should return empty dict or existing metadata

    def test_file_system_error_recovery(self, test_docs_dir):
        """Test recovery from file system errors."""
        from mcp_tools import read_laravel_doc_content_impl, clear_caches
        
        # Clear caches first
        clear_caches()
        
        # Create documentation file
        version_dir = test_docs_dir / "12.x"
        version_dir.mkdir(parents=True, exist_ok=True)
        test_file = version_dir / "test.md"
        test_file.write_text("# Test Documentation")
        
        # Test normal operation
        result = read_laravel_doc_content_impl(test_docs_dir, "test.md", "12.x")
        assert "# Test Documentation" in result
        
        # Clear cache before testing error case
        clear_caches()
        
        # Simulate file permission error
        with patch('builtins.open', side_effect=PermissionError("Access denied")):
            result = read_laravel_doc_content_impl(test_docs_dir, "test.md", "12.x")
            # Should handle the error and return error message
            assert "Documentation file not found" in result or "Error" in result
            
            # Other operations should still work
            from laravel_mcp_companion import get_laravel_package_info
            with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, {'test/package': {'name': 'Test', 'description': 'Test package'}}):
                package_result = get_laravel_package_info("test/package")
                assert "Test" in package_result

    def test_network_error_resilience(self, test_docs_dir):
        """Test resilience to network errors."""
        # Test external service fetching with network issues
        with patch('docs_updater.urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = Exception("Network timeout")
            
            fetcher = DocsUpdater(test_docs_dir, "12.x")
            
            # Should handle network errors gracefully
            try:
                fetcher.get_latest_commit()
                assert False, "Should have raised an exception"
            except Exception as e:
                # Error should be handled at the appropriate level
                assert "Network timeout" in str(e) or "Error fetching" in str(e)

    def test_malformed_data_handling(self, test_docs_dir):
        """Test handling of malformed or corrupted data."""
        from docs_updater import DocsUpdater
        
        # Create corrupted metadata file
        version_dir = test_docs_dir / "12.x"
        version_dir.mkdir(parents=True, exist_ok=True)
        metadata_dir = version_dir / ".metadata"
        metadata_dir.mkdir(exist_ok=True)
        metadata_file = metadata_dir / "sync_info.json"
        metadata_file.write_text("{ invalid json content }")
        
        # Create a DocsUpdater instance
        updater = DocsUpdater(test_docs_dir, "12.x")
        
        # Should handle corrupted metadata gracefully
        metadata = updater.read_local_metadata()
        assert metadata == {}  # Should return empty dict for corrupted metadata


@pytest.mark.integration
class TestCachingWorkflows:
    """Test caching behavior across operations."""

    def test_file_content_caching_workflow(self, test_docs_dir):
        """Test file content caching across multiple operations."""
        from mcp_tools import get_file_content_cached, clear_caches, _file_content_cache
        
        # Clear caches first
        clear_caches()
        
        # Setup test file
        test_file = test_docs_dir / "test_cache.md"
        test_content = "# Caching Test\n\nThis content should be cached."
        test_file.write_text(test_content)
        
        # First read - should cache the content
        result1 = get_file_content_cached(test_file)
        assert result1 == test_content
        
        # Verify cache is populated
        assert len(_file_content_cache) > 0
        
        # Modify the file
        test_file.write_text("Modified content")
        
        # Second read - should still use cache (not detect modification in this test)
        result2 = get_file_content_cached(test_file)
        assert result2 == test_content  # Still cached content
        
        # Clear cache and read again
        clear_caches()
        result3 = get_file_content_cached(test_file)
        assert result3 == "Modified content"  # Now reads new content

    def test_search_result_caching(self, test_docs_dir):
        """Test search result caching."""
        from mcp_tools import search_laravel_docs_impl, clear_caches, _search_result_cache
        
        # Clear caches first
        clear_caches()
        
        # Create test files
        version_dir = test_docs_dir / "12.x"
        version_dir.mkdir(exist_ok=True)
        (version_dir / "test.md").write_text("test content with keyword")
        
        with patch('mcp_tools.os.listdir', return_value=['test.md']):
            # First search - should cache result
            result1 = search_laravel_docs_impl(test_docs_dir, "keyword", "12.x")
            assert "Search results" in result1
            
            # Verify search cache is populated
            assert len(_search_result_cache) > 0
            
            # Second search with same query - should use cache
            # We can verify by checking the cache directly
            # The cache key format is "search:query:version:include_external"
            cache_key = "search:keyword:12.x:True"
            assert cache_key in _search_result_cache
            cached_result = _search_result_cache[cache_key]
            assert "test.md" in cached_result

    def test_cache_invalidation_workflow(self, test_docs_dir):
        """Test cache invalidation during documentation updates."""
        from mcp_tools import clear_caches, _file_content_cache, _search_result_cache
        from docs_updater import DocsUpdater
        
        # Populate caches
        _file_content_cache["test"] = "cached_content"
        _search_result_cache[("test", "12.x", True)] = "cached_search"
        
        # Verify caches are populated
        assert len(_file_content_cache) > 0
        assert len(_search_result_cache) > 0
        
        # Clear caches (simulating what would happen after an update)
        clear_caches()
        
        # Verify caches are cleared
        assert len(_file_content_cache) == 0
        assert len(_search_result_cache) == 0


@pytest.mark.integration 
class TestSecurityWorkflows:
    """Test security-related workflows."""

    def test_path_traversal_protection_workflow(self, test_docs_dir):
        """Test path traversal protection across different operations."""
        from mcp_tools import read_laravel_doc_content_impl
        from laravel_mcp_companion import is_safe_path
        
        # Setup safe file
        version_dir = test_docs_dir / "12.x"
        version_dir.mkdir(parents=True, exist_ok=True)
        safe_file = version_dir / "safe.md"
        safe_file.write_text("# Safe Content")
        
        # Setup file outside version directory
        outside_file = test_docs_dir / "outside.md" 
        outside_file.write_text("# Outside Content - Should not be accessible")
        
        # Test safe access
        result = read_laravel_doc_content_impl(test_docs_dir, "safe.md", "12.x")
        assert "# Safe Content" in result
        
        # Path traversal attempts should be blocked
        traversal_attempts = [
            "../outside.md",
            "../../outside.md", 
            "../12.x/../outside.md"
        ]
        
        for attempt in traversal_attempts:
            result = read_laravel_doc_content_impl(test_docs_dir, attempt, "12.x")
            # Should either return error or safe content, never outside content
            assert "# Outside Content" not in result
            # Should indicate access denied or file not found
            assert "Documentation file not found" in result or "Access denied" in result

    def test_input_validation_workflow(self, test_docs_dir):
        """Test input validation across different functions."""
        from mcp_tools import search_laravel_docs_impl
        
        # Test search input validation
        # Empty search should be rejected
        result = search_laravel_docs_impl(test_docs_dir, "", "12.x")
        assert "Search query cannot be empty" in result
        
        # Whitespace-only search should be rejected  
        result = search_laravel_docs_impl(test_docs_dir, "   ", "12.x")
        assert "Search query cannot be empty" in result
        
        # Package name validation
        from laravel_mcp_companion import get_laravel_package_info
        
        # Empty package name should be handled
        with patch.dict(laravel_mcp_companion.PACKAGE_CATALOG, {}, clear=True):
            result = get_laravel_package_info("")
            assert "not found" in result
        
        # Very long package name should be handled
        long_name = "a" * 1000
        result = get_laravel_package_info(long_name)
        assert "not found" in result


@pytest.mark.integration
class TestPerformanceWorkflows:
    """Test performance-related workflows."""

    def test_large_file_handling(self, test_docs_dir):
        """Test handling of large documentation files."""
        from mcp_tools import read_laravel_doc_content_impl
        
        # Create a large test file
        version_dir = test_docs_dir / "12.x"
        version_dir.mkdir(parents=True, exist_ok=True)
        large_file = version_dir / "large.md"
        
        # Create content with ~10KB of text
        large_content = "# Large File\n\n" + ("This is a large documentation file. " * 500)
        large_file.write_text(large_content)
        
        # Should handle large file without issues
        result = read_laravel_doc_content_impl(test_docs_dir, "large.md", "12.x")
        assert "# Large File" in result
        assert len(result) > 1000  # Should contain substantial content
        
        # Search should also work with large files
        from mcp_tools import search_laravel_docs_impl
        with patch('mcp_tools.os.listdir', return_value=['large.md']):
            search_result = search_laravel_docs_impl(test_docs_dir, "Large", "12.x")
            assert "12.x/large.md" in search_result

    def test_multiple_version_handling(self, test_docs_dir):
        """Test performance with multiple Laravel versions."""
        from mcp_tools import search_laravel_docs_impl
        
        # Create multiple version directories with files
        versions = ["10.x", "11.x", "12.x"]
        
        for version in versions:
            version_dir = test_docs_dir / version
            version_dir.mkdir(parents=True, exist_ok=True)
            
            # Create several files per version
            for i in range(5):
                test_file = version_dir / f"file_{i}.md"
                test_file.write_text(f"# File {i} for {version}\n\nContent for version {version}")
        
        # Search across all versions should be reasonably fast
        import time
        start_time = time.time()
        
        with patch('mcp_tools.SUPPORTED_VERSIONS', versions), \
             patch('mcp_tools.os.listdir', return_value=[f'file_{i}.md' for i in range(5)]):
            result = search_laravel_docs_impl(test_docs_dir, "File", version=None)  # Search all versions
                
            end_time = time.time()
            
            # Should complete in reasonable time (< 1 second for this test)
            assert end_time - start_time < 1.0
            assert "Search results" in result

    def test_concurrent_access_simulation(self, test_docs_dir):
        """Test behavior under simulated concurrent access."""
        from mcp_tools import read_laravel_doc_content_impl
        
        # Setup test file
        version_dir = test_docs_dir / "12.x"
        version_dir.mkdir(parents=True, exist_ok=True)
        test_file = version_dir / "concurrent.md"
        test_file.write_text("# Concurrent Access Test")
        
        # Simulate multiple rapid accesses
        results = []
        for i in range(10):
            result = read_laravel_doc_content_impl(test_docs_dir, "concurrent.md", "12.x")
            results.append(result)
        
        # All results should be consistent
        assert all("# Concurrent Access Test" in result for result in results)
        assert len(set(results)) == 1  # All results should be identical