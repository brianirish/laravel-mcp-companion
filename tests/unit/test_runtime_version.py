"""Unit tests for the runtime_version functionality (--version argument fix)."""

import sys
from unittest.mock import patch, MagicMock

from docs_updater import DEFAULT_VERSION
from mcp_tools import (
    get_version_from_path,
    read_laravel_doc_content_impl,
    browse_docs_by_category_impl,
    list_laravel_docs_impl,
    search_laravel_docs_impl
)

class TestRuntimeVersion:
    """Test that runtime_version parameter works correctly for all functions."""
    
    def test_get_version_from_path_without_runtime(self):
        """Test get_version_from_path without runtime_version uses DEFAULT_VERSION."""
        version, path = get_version_from_path("blade.md")
        assert version == DEFAULT_VERSION
        assert path == "blade.md"
    
    def test_get_version_from_path_with_runtime(self):
        """Test get_version_from_path with runtime_version uses that version."""
        version, path = get_version_from_path("blade.md", runtime_version="10.x")
        assert version == "10.x"
        assert path == "blade.md"
    
    def test_get_version_from_path_explicit_overrides_runtime(self):
        """Test that explicit version in path overrides runtime_version."""
        version, path = get_version_from_path("11.x/blade.md", runtime_version="10.x")
        assert version == "11.x"
        assert path == "blade.md"
    
    def test_read_laravel_doc_content_with_runtime_version(self, test_docs_dir):
        """Test reading docs with runtime_version parameter."""
        # Create test files for different versions
        for ver in ["10.x", "11.x", DEFAULT_VERSION]:
            version_dir = test_docs_dir / ver
            version_dir.mkdir(parents=True, exist_ok=True)
            (version_dir / "test.md").write_text(f"# Test for {ver}")

        # Without runtime_version, should use DEFAULT_VERSION
        content = read_laravel_doc_content_impl(test_docs_dir, "test.md")
        assert f"Test for {DEFAULT_VERSION}" in content
        
        # With runtime_version, should use that version
        content = read_laravel_doc_content_impl(test_docs_dir, "test.md", runtime_version="10.x")
        assert "Test for 10.x" in content
        
        # Explicit version parameter should override runtime_version
        content = read_laravel_doc_content_impl(test_docs_dir, "test.md", version="11.x", runtime_version="10.x")
        assert "Test for 11.x" in content
    
    def test_browse_docs_by_category_with_runtime_version(self, test_docs_dir):
        """Test browsing docs with runtime_version parameter returns TOON format."""
        # Create test files
        version_dir = test_docs_dir / "10.x"
        version_dir.mkdir(parents=True, exist_ok=True)
        (version_dir / "blade.md").write_text("# Blade Templates")

        with patch('mcp_tools.os.listdir', return_value=['blade.md']):
            # Without runtime_version, should use DEFAULT_VERSION
            result = browse_docs_by_category_impl(test_docs_dir, "frontend")
            assert DEFAULT_VERSION in result

            # With runtime_version, should use that version
            result = browse_docs_by_category_impl(test_docs_dir, "frontend", runtime_version="10.x")
            assert "10.x" in result

            # Explicit version should override runtime_version
            result = browse_docs_by_category_impl(test_docs_dir, "frontend", version="11.x", runtime_version="10.x")
            assert "11.x" in result
    
    @patch('mcp_tools.os.listdir')
    @patch('mcp_tools.get_laravel_docs_metadata')
    def test_list_laravel_docs_with_runtime_version(self, mock_metadata, mock_listdir, test_docs_dir):
        """Test listing docs with runtime_version parameter returns TOON format."""
        # Create the version directory
        version_dir = test_docs_dir / "10.x"
        version_dir.mkdir(parents=True, exist_ok=True)

        mock_listdir.return_value = ['test.md']
        mock_metadata.return_value = {
            'version': '10.x',
            'sync_time': '2024-01-01T12:00:00Z',
            'commit_sha': 'abc123'
        }

        # Test with specific version and runtime_version
        # Runtime version shouldn't affect list when specific version is provided
        result = list_laravel_docs_impl(test_docs_dir, "10.x", runtime_version="11.x")
        assert "10.x" in result
    
    @patch('mcp_tools.get_file_content_cached')
    @patch('mcp_tools.os.listdir')
    def test_search_laravel_docs_with_runtime_version(self, mock_listdir, mock_get_content, test_docs_dir):
        """Test searching docs with runtime_version parameter returns TOON format."""
        # Create version directories
        for ver in ["10.x", "11.x", "12.x"]:
            (test_docs_dir / ver).mkdir(parents=True, exist_ok=True)

        mock_listdir.return_value = ['test.md']
        mock_get_content.return_value = "Test content with search term"

        with patch('mcp_tools.SUPPORTED_VERSIONS', ['10.x', '11.x', '12.x']):
            # Without version or runtime_version, searches all versions
            result = search_laravel_docs_impl(test_docs_dir, "search")
            assert "search" in result.lower()

            # With runtime_version but no version, still searches all
            # (runtime_version doesn't affect search scope, only default serving)
            result = search_laravel_docs_impl(test_docs_dir, "search", runtime_version="10.x")
            assert "search" in result.lower()

            # With specific version, only searches that version
            result = search_laravel_docs_impl(test_docs_dir, "search", version="10.x", runtime_version="11.x")
            assert "search" in result.lower()


class TestVersionArgumentIntegration:
    """Integration tests for --version argument functionality."""
    
    def test_version_argument_affects_default_serving(self, test_docs_dir):
        """Test that --version argument changes default serving behavior."""
        # This simulates what happens when server starts with --version 10.x
        runtime_version = "10.x"
        
        # Create test content
        for ver in ["10.x", "11.x", "12.x"]:
            version_dir = test_docs_dir / ver
            version_dir.mkdir(parents=True, exist_ok=True)
            (version_dir / "routing.md").write_text(f"# Routing for Laravel {ver}")
        
        # When requesting a file without version, it should use runtime_version
        content = read_laravel_doc_content_impl(
            test_docs_dir, 
            "routing.md", 
            runtime_version=runtime_version
        )
        assert "Routing for Laravel 10.x" in content
        
        # But explicit version in path should still work
        content = read_laravel_doc_content_impl(
            test_docs_dir,
            "12.x/routing.md",
            runtime_version=runtime_version
        )
        assert "Routing for Laravel 12.x" in content
    
    def test_backward_compatibility_without_runtime_version(self, test_docs_dir):
        """Test that functions still work without runtime_version (backward compatibility)."""
        # Create test content for DEFAULT_VERSION
        version_dir = test_docs_dir / DEFAULT_VERSION
        version_dir.mkdir(parents=True, exist_ok=True)
        (version_dir / "test.md").write_text("# Default version content")
        (version_dir / "blade.md").write_text("# Blade Templates")  # Frontend-related file

        # All functions should work without runtime_version parameter
        content = read_laravel_doc_content_impl(test_docs_dir, "test.md")
        assert "Default version content" in content

        with patch('mcp_tools.os.listdir', return_value=['blade.md', 'test.md']):
            result = browse_docs_by_category_impl(test_docs_dir, "frontend")
            assert DEFAULT_VERSION in result


class TestNewVersionSimulation:
    """Simulate a new Laravel version (e.g. 14.x) appearing in the GitHub API.

    These tests verify that the entire stack handles a version bump gracefully
    without hardcoded version assumptions breaking things.
    """

    FUTURE_VERSION = "14.x"
    FUTURE_VERSIONS = ["6.x", "7.x", "8.x", "9.x", "10.x", "11.x", "12.x", "13.x", "14.x"]

    def test_version_parsing_accepts_future_version(self):
        """New version from API is recognized as valid."""
        with patch('mcp_tools.SUPPORTED_VERSIONS', self.FUTURE_VERSIONS), \
             patch('mcp_tools.DEFAULT_VERSION', self.FUTURE_VERSION):
            version, path = get_version_from_path("blade.md")
            assert version == self.FUTURE_VERSION
            assert path == "blade.md"

    def test_explicit_version_still_overrides(self):
        """Explicit version in path overrides the new default."""
        with patch('mcp_tools.SUPPORTED_VERSIONS', self.FUTURE_VERSIONS), \
             patch('mcp_tools.DEFAULT_VERSION', self.FUTURE_VERSION):
            version, path = get_version_from_path("12.x/blade.md")
            assert version == "12.x"
            assert path == "blade.md"

    def test_read_doc_uses_future_default(self, test_docs_dir):
        """Reading a doc without explicit version uses the new default."""
        future_dir = test_docs_dir / self.FUTURE_VERSION
        future_dir.mkdir(parents=True, exist_ok=True)
        (future_dir / "routing.md").write_text("# Routing for 14.x")

        with patch('mcp_tools.SUPPORTED_VERSIONS', self.FUTURE_VERSIONS), \
             patch('mcp_tools.DEFAULT_VERSION', self.FUTURE_VERSION):
            content = read_laravel_doc_content_impl(test_docs_dir, "routing.md")
            assert "Routing for 14.x" in content

    def test_browse_category_uses_future_default(self, test_docs_dir):
        """Browsing by category uses the new default version."""
        future_dir = test_docs_dir / self.FUTURE_VERSION
        future_dir.mkdir(parents=True, exist_ok=True)
        (future_dir / "blade.md").write_text("# Blade")

        with patch('mcp_tools.SUPPORTED_VERSIONS', self.FUTURE_VERSIONS), \
             patch('mcp_tools.DEFAULT_VERSION', self.FUTURE_VERSION), \
             patch('mcp_tools.os.listdir', return_value=['blade.md']):
            result = browse_docs_by_category_impl(test_docs_dir, "frontend")
            assert self.FUTURE_VERSION in result

    def test_search_includes_future_version(self, test_docs_dir):
        """Search across all versions includes the new one."""
        future_dir = test_docs_dir / self.FUTURE_VERSION
        future_dir.mkdir(parents=True, exist_ok=True)

        with patch('mcp_tools.SUPPORTED_VERSIONS', self.FUTURE_VERSIONS), \
             patch('mcp_tools.DEFAULT_VERSION', self.FUTURE_VERSION), \
             patch('mcp_tools.os.listdir', return_value=['routing.md']), \
             patch('mcp_tools.get_file_content_cached', return_value="New routing features"):
            result = search_laravel_docs_impl(test_docs_dir, "routing")
            assert "routing" in result.lower()

    def test_validate_version_accepts_future(self):
        """validate_version recognizes the new version."""
        with patch('laravel_mcp_companion.SUPPORTED_VERSIONS', self.FUTURE_VERSIONS):
            from laravel_mcp_companion import validate_version
            assert validate_version(self.FUTURE_VERSION) is True

    def test_main_uses_future_default(self):
        """Main function wires through the new default version."""
        with patch('laravel_mcp_companion.GracefulShutdown'), \
             patch('laravel_mcp_companion.MultiSourceDocsUpdater') as mock_updater_class, \
             patch('laravel_mcp_companion.FastMCP') as mock_fastmcp_class, \
             patch('laravel_mcp_companion.setup_docs_path') as mock_setup_docs, \
             patch('laravel_mcp_companion.SUPPORTED_VERSIONS', self.FUTURE_VERSIONS), \
             patch('laravel_mcp_companion.DEFAULT_VERSION', self.FUTURE_VERSION), \
             patch.object(sys, 'argv', ['laravel-mcp-companion']):
            mock_setup_docs.return_value = "/tmp/test"
            mock_mcp = MagicMock()
            mock_fastmcp_class.return_value = mock_mcp

            from laravel_mcp_companion import main
            main()

            mock_updater_class.assert_called_once_with("/tmp/test", self.FUTURE_VERSION)

    def test_fallback_list_includes_current_latest(self):
        """Hardcoded fallback list includes the current latest version."""
        from docs_updater import DEFAULT_VERSION
        with patch('docs_updater.urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = Exception("API down")
            from docs_updater import get_supported_versions
            fallback = get_supported_versions()
            assert DEFAULT_VERSION in fallback