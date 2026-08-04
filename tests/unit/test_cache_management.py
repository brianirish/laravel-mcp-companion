"""Tests for cache management functionality."""

import threading
from pathlib import Path
from unittest.mock import patch, mock_open
from mcp_tools import (
    get_file_content_cached,
    search_laravel_docs_impl,
    clear_caches,
    _FILE_CACHE_MAX_ENTRIES,
    _FILE_CACHE_EVICT_COUNT,
)


class TestCacheManagement:
    """Test cases for cache size limits and LRU eviction."""
    
    def setup_method(self):
        """Clear caches before each test."""
        clear_caches()
    
    def teardown_method(self):
        """Clear caches after each test."""
        clear_caches()
    
    def test_file_cache_size_limit(self):
        """Test that the file cache evicts once it exceeds its entry limit."""
        limit = _FILE_CACHE_MAX_ENTRIES
        evicted = _FILE_CACHE_EVICT_COUNT

        # Mock file reading
        with patch('builtins.open', mock_open(read_data='content')):
            # Fill cache to exactly the limit
            for i in range(limit):
                content = get_file_content_cached(f'/path/file{i}.txt')
                assert content == 'content'

            from mcp_tools import _file_content_cache
            assert len(_file_content_cache) == limit

            # Add one more entry - should trigger cleanup
            get_file_content_cached(f'/path/file{limit}.txt')

            assert len(_file_content_cache) == limit - evicted + 1

            # The oldest entries should be removed
            for i in range(evicted):
                assert f'/path/file{i}.txt' not in _file_content_cache

            # The rest should still be cached
            for i in range(evicted, limit):
                assert f'/path/file{i}.txt' in _file_content_cache

            # The new file should be in cache
            assert f'/path/file{limit}.txt' in _file_content_cache

    def test_file_cache_lru_eviction_order(self):
        """Test that oldest entries are removed first (FIFO behavior)."""
        limit = _FILE_CACHE_MAX_ENTRIES
        evicted = _FILE_CACHE_EVICT_COUNT

        with patch('builtins.open', mock_open(read_data='content')):
            # Fill cache with entries in a specific order
            for i in range(limit):
                get_file_content_cached(f'/path/ordered{i}.txt')

            # Trigger eviction
            get_file_content_cached('/path/trigger.txt')

            from mcp_tools import _file_content_cache
            # The oldest entries should be evicted first
            for i in range(evicted):
                assert f'/path/ordered{i}.txt' not in _file_content_cache

            # Newer entries should remain
            for i in range(evicted, limit):
                assert f'/path/ordered{i}.txt' in _file_content_cache
    
    def test_search_cache_size_limit(self):
        """Test that search cache respects 100-entry limit."""
        # Mock the actual search implementation
        with patch('mcp_tools.get_laravel_docs_metadata') as mock_metadata:
            mock_metadata.return_value = {'11.x': {'version': '11.x', 'files': []}}
            
            with patch('mcp_tools.get_file_content_cached') as mock_file_content:
                mock_file_content.return_value = "No match here"
                
                # Fill search cache with 100 entries
                for i in range(100):
                    result = search_laravel_docs_impl(Path("/fake/docs"), f"query{i}", version="11.x")
                    assert "No results found" in result
                
                # Check cache size
                from mcp_tools import _search_result_cache
                assert len(_search_result_cache) == 100
                
                # Add one more - should trigger cleanup
                search_laravel_docs_impl(Path("/fake/docs"), "query100", version="11.x")
                
                # Should have 81 entries now
                assert len(_search_result_cache) == 81
                
                # First 20 should be removed
                for i in range(20):
                    cache_key = f"search:query{i}:11.x:True:5"
                    assert cache_key not in _search_result_cache
    
    def test_concurrent_cache_access(self):
        """Test thread-safe cache operations."""
        results = []
        errors = []
        
        def cache_writer(thread_id):
            """Write to cache from multiple threads."""
            try:
                with patch('builtins.open', mock_open(read_data=f'content{thread_id}')):
                    for i in range(10):
                        content = get_file_content_cached(f'/path/thread{thread_id}_file{i}.txt')
                        results.append((thread_id, i, content))
            except Exception as e:
                errors.append((thread_id, str(e)))
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=cache_writer, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # Check no errors occurred
        assert len(errors) == 0
        
        # Check all operations completed
        assert len(results) == 50  # 5 threads * 10 files each
        
        # Verify cache integrity
        from mcp_tools import _file_content_cache
        # Should have 50 entries (under the 100 limit)
        assert len(_file_content_cache) == 50
    
    def test_cache_eviction_under_concurrent_load(self):
        """Test cache eviction works correctly with concurrent access."""
        completed_operations = []
        
        def fill_cache(start_idx):
            """Fill cache to trigger eviction."""
            try:
                with patch('builtins.open', mock_open(read_data='content')):
                    for i in range(start_idx, start_idx + 30):
                        get_file_content_cached(f'/path/concurrent{i}.txt')
                        completed_operations.append(i)
            except Exception:
                pass
        
        # Start 4 threads that will collectively add 120 entries
        threads = []
        for i in range(4):
            thread = threading.Thread(target=fill_cache, args=(i * 30,))
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Verify operations completed
        assert len(completed_operations) == 120

        # Check cache size stays within its configured bound
        from mcp_tools import _file_content_cache
        assert len(_file_content_cache) <= _FILE_CACHE_MAX_ENTRIES
    
    def test_cache_hit_behavior(self):
        """Test that cache hits don't affect eviction order."""
        with patch('builtins.open', mock_open(read_data='content')) as mock_file:
            # Add first file
            content1 = get_file_content_cached('/path/file1.txt')
            assert mock_file.call_count == 1
            
            # Access same file again - should be cache hit
            content2 = get_file_content_cached('/path/file1.txt')
            assert content1 == content2
            assert mock_file.call_count == 1  # No new file read
            
            limit = _FILE_CACHE_MAX_ENTRIES
            evicted = _FILE_CACHE_EVICT_COUNT

            # Fill cache to exactly the limit (file1 is already entry 1)
            for i in range(2, limit + 1):
                get_file_content_cached(f'/path/file{i}.txt')

            # Access first file again before eviction
            content3 = get_file_content_cached('/path/file1.txt')
            assert content3 == 'content'

            # Trigger eviction
            get_file_content_cached(f'/path/file{limit + 1}.txt')

            # Eviction removes the oldest keys from the dict.
            # Since Python 3.7+, dicts maintain insertion order, and a cache hit
            # does not refresh an entry's position.
            from mcp_tools import _file_content_cache

            # Files are evicted in insertion order, starting with file1.txt
            for i in range(1, evicted + 1):
                assert f'/path/file{i}.txt' not in _file_content_cache, f"file{i}.txt should have been evicted"

            # The remainder, plus the newest entry, should still be cached
            for i in range(evicted + 1, limit + 1):
                assert f'/path/file{i}.txt' in _file_content_cache, f"file{i}.txt should still be in cache"
            assert f'/path/file{limit + 1}.txt' in _file_content_cache
    
    def test_cache_with_file_not_found(self):
        """Test cache behavior with file not found errors."""
        # First call should attempt to read and get FileNotFoundError
        with patch('builtins.open', side_effect=FileNotFoundError):
            content1 = get_file_content_cached('/path/missing.txt')
            assert content1 == "File not found: /path/missing.txt"
        
        # Check that error response is NOT cached
        from mcp_tools import _file_content_cache
        assert '/path/missing.txt' not in _file_content_cache
        
        # Second call should also attempt to read
        with patch('builtins.open', mock_open(read_data='now exists')):
            content2 = get_file_content_cached('/path/missing.txt')
            assert content2 == 'now exists'
            # Now it should be cached
            assert '/path/missing.txt' in _file_content_cache
    
    def test_cache_with_encoding_error(self):
        """Test cache behavior with encoding errors."""
        # Simulate encoding error
        with patch('builtins.open', side_effect=UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid')):
            content = get_file_content_cached('/path/bad_encoding.txt')
            assert "Error reading file" in content
        
        # Should not be cached
        from mcp_tools import _file_content_cache
        assert '/path/bad_encoding.txt' not in _file_content_cache
    
    def test_search_cache_key_format(self):
        """Cache keys record the versions actually searched, not the raw argument."""
        from mcp_tools import resolve_search_versions

        with patch('mcp_tools.get_laravel_docs_metadata') as mock_metadata:
            mock_metadata.return_value = {}

            # Test different parameter combinations
            search_laravel_docs_impl(Path("/fake/docs"), "test", version="11.x", include_external=True)
            search_laravel_docs_impl(Path("/fake/docs"), "test", version="11.x", include_external=False)
            search_laravel_docs_impl(Path("/fake/docs"), "test", version=None, include_external=True)
            search_laravel_docs_impl(Path("/fake/docs"), "test", version=None, include_external=True, all_versions=True)

            from mcp_tools import _search_result_cache

            default_scope = ','.join(resolve_search_versions(None))
            all_scope = ','.join(resolve_search_versions(None, all_versions=True))

            assert "search:test:11.x:core,services,packages,learning:5" in _search_result_cache
            assert "search:test:11.x:core:5" in _search_result_cache
            assert f"search:test:{default_scope}:core,services,packages,learning:5" in _search_result_cache
            # Scoped and all-versions searches must not share a cache entry
            assert f"search:test:{all_scope}:core,services,packages,learning:5" in _search_result_cache
            assert default_scope != all_scope
    
    def test_clear_caches_function(self):
        """Test that clear_caches properly empties both caches."""
        with patch('builtins.open', mock_open(read_data='content')):
            # Add entries to both caches
            get_file_content_cached('/path/file.txt')
            
            with patch('mcp_tools.get_laravel_docs_metadata') as mock_metadata:
                mock_metadata.return_value = {}
                search_laravel_docs_impl(Path("/fake/docs"), "test")
            
            from mcp_tools import _file_content_cache, _search_result_cache
            assert len(_file_content_cache) > 0
            assert len(_search_result_cache) > 0
            
            # Clear caches
            clear_caches()
            
            # Both should be empty
            assert len(_file_content_cache) == 0
            assert len(_search_result_cache) == 0