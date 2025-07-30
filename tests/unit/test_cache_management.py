"""Tests for cache management functionality."""

import threading
from pathlib import Path
from unittest.mock import patch, mock_open
from mcp_tools import get_file_content_cached, search_laravel_docs_impl, clear_caches


class TestCacheManagement:
    """Test cases for cache size limits and LRU eviction."""
    
    def setup_method(self):
        """Clear caches before each test."""
        clear_caches()
    
    def teardown_method(self):
        """Clear caches after each test."""
        clear_caches()
    
    def test_file_cache_size_limit(self):
        """Test that file cache respects 100-entry limit."""
        # Mock file reading
        with patch('builtins.open', mock_open(read_data='content')):
            # Fill cache with 100 entries
            for i in range(100):
                content = get_file_content_cached(f'/path/file{i}.txt')
                assert content == 'content'
            
            # Access cache to verify it has 100 entries
            from mcp_tools import _file_content_cache
            assert len(_file_content_cache) == 100
            
            # Add one more entry - should trigger cleanup
            get_file_content_cached('/path/file100.txt')
            
            # Cache should now have 81 entries (100 - 20 + 1)
            assert len(_file_content_cache) == 81
            
            # First 20 files should be removed
            for i in range(20):
                assert f'/path/file{i}.txt' not in _file_content_cache
            
            # Files 20-99 should still be in cache
            for i in range(20, 100):
                assert f'/path/file{i}.txt' in _file_content_cache
            
            # The new file should be in cache
            assert '/path/file100.txt' in _file_content_cache
    
    def test_file_cache_lru_eviction_order(self):
        """Test that oldest entries are removed first (FIFO behavior)."""
        with patch('builtins.open', mock_open(read_data='content')):
            # Fill cache with entries in a specific order
            for i in range(100):
                get_file_content_cached(f'/path/ordered{i}.txt')
            
            # Trigger eviction
            get_file_content_cached('/path/trigger.txt')
            
            from mcp_tools import _file_content_cache
            # Files 0-19 should be evicted (oldest)
            for i in range(20):
                assert f'/path/ordered{i}.txt' not in _file_content_cache
            
            # Files 20-99 should remain
            for i in range(20, 100):
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
                    cache_key = f"search:query{i}:11.x:True"
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
        
        # Check cache size is within limits
        from mcp_tools import _file_content_cache
        assert len(_file_content_cache) <= 100
        # Should have evicted some entries
        assert len(_file_content_cache) >= 80  # At least 80 after eviction
    
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
            
            # Fill cache to near limit
            for i in range(2, 101):
                get_file_content_cached(f'/path/file{i}.txt')
            
            # Access first file again before eviction
            content3 = get_file_content_cached('/path/file1.txt')
            assert content3 == 'content'
            
            # Trigger eviction
            get_file_content_cached('/path/file101.txt')
            
            # The cache eviction removes the first 20 keys from the dict
            # Since Python 3.7+, dicts maintain insertion order
            from mcp_tools import _file_content_cache
            
            # Files should be evicted in insertion order: file1.txt through file20.txt
            for i in range(1, 21):
                assert f'/path/file{i}.txt' not in _file_content_cache, f"file{i}.txt should have been evicted"
            
            # Files 21-100 and 101 should still be in cache
            for i in range(21, 101):
                assert f'/path/file{i}.txt' in _file_content_cache, f"file{i}.txt should still be in cache"
            assert '/path/file101.txt' in _file_content_cache
    
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
        """Test search cache key generation."""
        with patch('mcp_tools.get_laravel_docs_metadata') as mock_metadata:
            mock_metadata.return_value = {}
            
            # Test different parameter combinations
            search_laravel_docs_impl(Path("/fake/docs"), "test", version="11.x", include_external=True)
            search_laravel_docs_impl(Path("/fake/docs"), "test", version="11.x", include_external=False)
            search_laravel_docs_impl(Path("/fake/docs"), "test", version=None, include_external=True)
            
            from mcp_tools import _search_result_cache
            # Should have 3 different cache entries
            assert len(_search_result_cache) == 3
            assert "search:test:11.x:True" in _search_result_cache
            assert "search:test:11.x:False" in _search_result_cache
            assert "search:test:None:True" in _search_result_cache
    
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