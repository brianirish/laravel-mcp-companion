"""Path, cache and startup helpers the server module exposes."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from laravel_mcp_companion import server as companion_server
from laravel_mcp_companion.mcp_tools import is_safe_path
from laravel_mcp_companion.docs_updater import DEFAULT_VERSION
from laravel_mcp_companion.server import (
    get_version_from_path,
    get_file_content_cached,
    clear_file_cache,
    setup_docs_path,
    update_documentation,
)


class TestPathHelpers:
    """Version parsing and path containment."""

    def test_get_version_from_path_with_version(self):
        """Test version extraction from path with version."""
        version, relative_path = get_version_from_path("12.x/blade.md")
        
        assert version == "12.x"
        assert relative_path == "blade.md"

    def test_get_version_from_path_without_version(self):
        """Test version extraction from path without version."""
        version, relative_path = get_version_from_path("blade.md")

        assert version == DEFAULT_VERSION
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
        from laravel_mcp_companion import mcp_tools
        test_file = temp_dir / "test.md"
        test_content = "# Test Content"
        test_file.write_text(test_content)

        # Populate cache. The cache now lives solely in mcp_tools; this module
        # only re-exports the function and delegates clearing to it.
        get_file_content_cached(str(test_file))
        assert len(mcp_tools._file_content_cache) > 0

        # Clear cache
        clear_file_cache()
        assert len(mcp_tools._file_content_cache) == 0
        assert len(mcp_tools._search_result_cache) == 0


class TestUtilityFunctions:
    """Test utility functions used by MCP tools."""

    def test_setup_docs_path_default(self, temp_dir):
        """With no path given, the corpus that ships with the project is used and created if absent."""
        shipped = temp_dir / "shipped" / "docs"
        with patch('laravel_mcp_companion.server.resource_path', return_value=shipped):
            result = companion_server.setup_docs_path()

        assert result == shipped.resolve()
        assert shipped.is_dir()

    def test_setup_docs_path_custom(self):
        """Test docs path setup with custom location."""
        custom_path = "/custom/docs/path"
        
        with patch('laravel_mcp_companion.server.Path') as mock_path:
            mock_path_instance = MagicMock()
            mock_path.return_value = mock_path_instance
            mock_path_instance.resolve.return_value = mock_path_instance
            
            companion_server.setup_docs_path(custom_path)
            
            mock_path.assert_called_with(custom_path)
            mock_path_instance.mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_parse_arguments_default(self):
        """Test argument parsing with defaults."""
        with patch('sys.argv', ['laravel_mcp_companion.py']):
            args = companion_server.parse_arguments()
            
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
            args = companion_server.parse_arguments()

            assert args.docs_path == '/custom/docs'
            assert args.server_name == 'CustomServer'
            assert args.log_level == 'DEBUG'
            assert args.transport == 'http'
            assert args.version == '11.x'
            assert args.update_docs is True
            assert args.force_update is True


@pytest.mark.unit
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
            
            # In a checkout the corpus is docs/ at the repository root
            expected = (Path(companion_server.__file__).parent.parent / "docs").resolve()
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
    
    @patch('laravel_mcp_companion.server.DocsUpdater')
    def test_update_documentation_success(self, mock_updater_class, temp_dir):
        """Test successful documentation update."""
        mock_updater = MagicMock()
        mock_updater.update.return_value = True
        mock_updater_class.return_value = mock_updater
        
        result = update_documentation(temp_dir, "12.x", force=False)
        
        assert result is True
        mock_updater_class.assert_called_once_with(temp_dir, "12.x")
        mock_updater.update.assert_called_once_with(force=False)
    
    @patch('laravel_mcp_companion.server.DocsUpdater')
    def test_update_documentation_no_changes(self, mock_updater_class, temp_dir):
        """Test documentation update with no changes."""
        mock_updater = MagicMock()
        mock_updater.update.return_value = False
        mock_updater_class.return_value = mock_updater
        
        result = update_documentation(temp_dir, "12.x", force=True)
        
        assert result is False
        mock_updater.update.assert_called_once_with(force=True)
    
    @patch('laravel_mcp_companion.server.DocsUpdater')
    def test_update_documentation_error(self, mock_updater_class, temp_dir):
        """Test documentation update with error."""
        mock_updater_class.side_effect = Exception("Update failed")
        
        result = update_documentation(temp_dir, "12.x", force=False)
        
        assert result is False