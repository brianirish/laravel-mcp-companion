"""Unit tests for Laravel MCP Companion MCP framework integration."""

import pytest
from unittest.mock import MagicMock, patch
import argparse

from laravel_mcp_companion import (
    validate_version,
    setup_server_environment,
    handle_documentation_update,
)


class TestValidateVersion:
    """Test version validation function."""
    
    def test_validate_valid_version(self):
        """Test validation of valid version."""
        assert validate_version("12.x") is True
        assert validate_version("11.x") is True
        assert validate_version("10.x") is True
    
    def test_validate_invalid_version(self):
        """Test validation of invalid version."""
        assert validate_version("5.x") is False
        assert validate_version("13.x") is False
        assert validate_version("invalid") is False
        assert validate_version("") is False


class TestSetupServerEnvironment:
    """Test server environment setup."""
    
    def test_setup_with_default_transport(self, temp_dir):
        """Test setup with default stdio transport."""
        args = argparse.Namespace(
            log_level="INFO",
            docs_path=str(temp_dir),
            version="12.x",
            transport="stdio",
            websocket_host=None,
            websocket_port=None
        )
        
        with patch('laravel_mcp_companion.setup_docs_path', return_value=temp_dir):
            docs_path, transport_options = setup_server_environment(args)
            
            assert docs_path == temp_dir
            assert transport_options == {}
    
    def test_setup_with_websocket_transport(self, temp_dir):
        """Test setup with websocket transport."""
        args = argparse.Namespace(
            log_level="DEBUG",
            docs_path=str(temp_dir),
            version="12.x",
            transport="websocket",
            host="localhost",
            port=8080
        )
        
        with patch('laravel_mcp_companion.setup_docs_path', return_value=temp_dir):
            docs_path, transport_options = setup_server_environment(args)
            
            assert docs_path == temp_dir
            assert transport_options == {
                "host": "localhost",
                "port": 8080
            }
    
    def test_setup_with_invalid_version(self, temp_dir):
        """Test setup with invalid version."""
        args = argparse.Namespace(
            log_level="INFO",
            docs_path=str(temp_dir),
            version="invalid",
            transport="stdio",
            websocket_host=None,
            websocket_port=None
        )
        
        with patch('laravel_mcp_companion.setup_docs_path', return_value=temp_dir), \
             pytest.raises(SystemExit) as exc_info:
            setup_server_environment(args)
            
        assert exc_info.value.code == 1


class TestHandleDocumentationUpdate:
    """Test documentation update handling."""
    
    def test_update_not_requested(self, temp_dir):
        """Test when update is not requested."""
        result = handle_documentation_update(temp_dir, "12.x", False, False)
        assert result is False
    
    def test_update_requested_success(self, temp_dir):
        """Test successful documentation update."""
        with patch('laravel_mcp_companion.update_documentation', return_value=True):
            result = handle_documentation_update(temp_dir, "12.x", True, False)
            assert result is True
    
    def test_force_update_requested(self, temp_dir):
        """Test force documentation update."""
        with patch('laravel_mcp_companion.update_documentation', return_value=True) as mock_update:
            result = handle_documentation_update(temp_dir, "12.x", False, True)
            assert result is True
            mock_update.assert_called_once_with(temp_dir, "12.x", True)
    
    def test_update_requested_no_changes(self, temp_dir):
        """Test documentation update with no changes needed."""
        with patch('laravel_mcp_companion.update_documentation', return_value=False):
            result = handle_documentation_update(temp_dir, "12.x", True, False)
            assert result is False