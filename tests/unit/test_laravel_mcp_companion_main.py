"""Unit tests for Laravel MCP Companion main function and components."""

import pytest
import sys
from unittest.mock import patch, MagicMock

from laravel_mcp_companion import main, parse_arguments


class TestParseArguments:
    """Test command line argument parsing."""
    
    def test_parse_default_arguments(self):
        """Test parsing with default arguments."""
        with patch.object(sys, 'argv', ['laravel-mcp-companion']):
            args = parse_arguments()
            
            assert args.transport == "stdio"
            assert args.server_name == "LaravelMCPCompanion"
            assert args.log_level == "INFO"
            assert not args.update_docs
            assert not args.force_update
    
    def test_parse_websocket_transport(self):
        """Test parsing websocket transport arguments."""
        test_args = [
            'laravel-mcp-companion',
            '--transport', 'websocket',
            '--host', 'localhost',
            '--port', '8080'
        ]
        
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            
            assert args.transport == "websocket"
            assert args.host == "localhost"
            assert args.port == 8080
    
    def test_parse_update_arguments(self):
        """Test parsing documentation update arguments."""
        test_args = [
            'laravel-mcp-companion',
            '--update-docs',
            '--version', '11.x',
            '--docs-path', '/custom/docs'
        ]
        
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            
            assert args.update_docs is True
            assert args.version == "11.x"
            assert args.docs_path == "/custom/docs"
    
    def test_parse_force_update(self):
        """Test parsing force update argument."""
        test_args = ['laravel-mcp-companion', '--force-update']
        
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            
            assert args.force_update is True
    
    def test_parse_log_level(self):
        """Test parsing log level argument."""
        test_args = ['laravel-mcp-companion', '--log-level', 'DEBUG']
        
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            
            assert args.log_level == "DEBUG"


class TestMainFunction:
    """Test the main() function."""
    
    @patch('laravel_mcp_companion.GracefulShutdown')
    @patch('laravel_mcp_companion.MultiSourceDocsUpdater')
    @patch('laravel_mcp_companion.FastMCP')
    @patch('laravel_mcp_companion.setup_docs_path')
    def test_main_stdio_transport(self, mock_setup_docs, mock_fastmcp_class, 
                                  mock_updater_class, mock_shutdown_class, temp_dir):
        """Test main function with stdio transport."""
        # Setup mocks
        mock_setup_docs.return_value = temp_dir
        mock_mcp = MagicMock()
        mock_fastmcp_class.return_value = mock_mcp
        mock_updater = MagicMock()
        mock_updater_class.return_value = mock_updater
        mock_shutdown = MagicMock()
        mock_shutdown_class.return_value = mock_shutdown
        
        # Mock command line arguments
        test_args = ['laravel-mcp-companion']
        
        with patch.object(sys, 'argv', test_args):
            # Run main function (it will call mcp.run which is mocked)
            main()
            
            # Verify setup was called
            mock_setup_docs.assert_called_once()
            mock_fastmcp_class.assert_called_once_with("LaravelMCPCompanion")
            mock_updater_class.assert_called_once_with(temp_dir, "12.x")
            
            # Verify server was started
            mock_mcp.run.assert_called_once_with(transport="stdio")
    
    @patch('laravel_mcp_companion.GracefulShutdown')
    @patch('laravel_mcp_companion.MultiSourceDocsUpdater')
    @patch('laravel_mcp_companion.FastMCP')
    @patch('laravel_mcp_companion.setup_docs_path')
    @patch('laravel_mcp_companion.update_documentation')
    def test_main_with_update_docs(self, mock_update_docs, mock_setup_docs, 
                                   mock_fastmcp_class, mock_updater_class, 
                                   mock_shutdown_class, temp_dir):
        """Test main function with documentation update."""
        # Setup mocks
        mock_setup_docs.return_value = temp_dir
        mock_update_docs.return_value = True
        mock_mcp = MagicMock()
        mock_fastmcp_class.return_value = mock_mcp
        mock_updater = MagicMock()
        mock_updater_class.return_value = mock_updater
        mock_shutdown = MagicMock()
        mock_shutdown_class.return_value = mock_shutdown
        
        # Mock command line arguments
        test_args = ['laravel-mcp-companion', '--update-docs']
        
        with patch.object(sys, 'argv', test_args):
            main()
            
            # Verify documentation was updated
            mock_update_docs.assert_called_once_with(temp_dir, "12.x", False)
    
    @patch('laravel_mcp_companion.FastMCP')
    @patch('laravel_mcp_companion.setup_docs_path')
    def test_main_invalid_version(self, mock_setup_docs, mock_fastmcp_class, temp_dir):
        """Test main function with invalid version."""
        # Setup mocks
        mock_setup_docs.return_value = temp_dir
        
        # Mock command line arguments with invalid version
        test_args = ['laravel-mcp-companion', '--version', 'invalid']
        
        with patch.object(sys, 'argv', test_args), \
             pytest.raises(SystemExit) as exc_info:
            main()
            
        assert exc_info.value.code == 1
    
    @patch('laravel_mcp_companion.GracefulShutdown')
    @patch('laravel_mcp_companion.MultiSourceDocsUpdater')
    @patch('laravel_mcp_companion.FastMCP')
    @patch('laravel_mcp_companion.setup_docs_path')
    def test_main_websocket_transport(self, mock_setup_docs, mock_fastmcp_class, 
                                      mock_updater_class, mock_shutdown_class, temp_dir):
        """Test main function with websocket transport."""
        # Setup mocks
        mock_setup_docs.return_value = temp_dir
        mock_mcp = MagicMock()
        mock_fastmcp_class.return_value = mock_mcp
        mock_updater = MagicMock()
        mock_updater_class.return_value = mock_updater
        mock_shutdown = MagicMock()
        mock_shutdown_class.return_value = mock_shutdown
        
        # Mock command line arguments
        test_args = [
            'laravel-mcp-companion',
            '--transport', 'websocket',
            '--host', 'localhost',
            '--port', '8080'
        ]
        
        with patch.object(sys, 'argv', test_args):
            main()
            
            # Verify server was started with websocket transport
            mock_mcp.run.assert_called_once_with(
                transport="websocket",
                host="localhost",
                port=8080
            )
    
    @patch('laravel_mcp_companion.GracefulShutdown')
    @patch('laravel_mcp_companion.MultiSourceDocsUpdater')
    @patch('laravel_mcp_companion.FastMCP')
    @patch('laravel_mcp_companion.setup_docs_path')
    def test_main_cleanup_registration(self, mock_setup_docs, mock_fastmcp_class, 
                                       mock_updater_class, mock_shutdown_class, temp_dir):
        """Test that cleanup is registered with shutdown handler."""
        # Setup mocks
        mock_setup_docs.return_value = temp_dir
        mock_mcp = MagicMock()
        mock_fastmcp_class.return_value = mock_mcp
        mock_updater = MagicMock()
        mock_updater_class.return_value = mock_updater
        mock_shutdown = MagicMock()
        mock_shutdown_class.return_value = mock_shutdown
        
        test_args = ['laravel-mcp-companion']
        
        with patch.object(sys, 'argv', test_args):
            main()
            
            # Verify cleanup was registered
            mock_shutdown.register.assert_called_once()
            
            # Get the cleanup function that was registered
            cleanup_func = mock_shutdown.register.call_args[0][0]
            assert callable(cleanup_func)
    
    @patch('laravel_mcp_companion.FastMCP')
    @patch('laravel_mcp_companion.setup_docs_path')
    def test_main_server_error(self, mock_setup_docs, mock_fastmcp_class, temp_dir):
        """Test main function when server fails to start."""
        # Setup mocks
        mock_setup_docs.return_value = temp_dir
        mock_mcp = MagicMock()
        mock_mcp.run.side_effect = Exception("Server error")
        mock_fastmcp_class.return_value = mock_mcp
        
        test_args = ['laravel-mcp-companion']
        
        with patch.object(sys, 'argv', test_args), \
             patch('laravel_mcp_companion.GracefulShutdown'), \
             patch('laravel_mcp_companion.MultiSourceDocsUpdater'), \
             pytest.raises(SystemExit) as exc_info:
            main()
            
        assert exc_info.value.code == 1


