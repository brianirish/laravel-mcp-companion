"""Unit tests for Laravel MCP Companion MCP framework integration."""

import pytest
from typing import Dict, Any, Callable, Optional
from unittest.mock import MagicMock, patch
import argparse

from laravel_mcp_companion import (
    validate_version,
    setup_server_environment,
    handle_documentation_update,
    configure_mcp_server
)
from docs_updater import MultiSourceDocsUpdater


class MockFastMCP:
    """Mock implementation of FastMCP for testing."""
    
    def __init__(self, name: str):
        self.name = name
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.resources: Dict[str, Dict[str, Any]] = {}
        self._tool_functions: Dict[str, Callable] = {}
        self._resource_functions: Dict[str, Callable] = {}
        
    def tool(self, description: str, annotations: Optional[Dict[str, Any]] = None, **kwargs):
        """Mock tool decorator."""
        def decorator(func: Callable) -> Callable:
            self.tools[func.__name__] = {
                'description': description,
                'function': func,
                'doc': func.__doc__,
                'annotations': annotations or {}
            }
            self._tool_functions[func.__name__] = func
            return func
        return decorator
    
    def resource(self, pattern: str):
        """Mock resource decorator."""
        def decorator(func: Callable) -> Callable:
            self.resources[pattern] = {
                'pattern': pattern,
                'function': func,
                'doc': func.__doc__
            }
            self._resource_functions[func.__name__] = func
            return func
        return decorator

    def prompt(self, name: str, **kwargs):
        """Mock prompt decorator."""
        def decorator(func: Callable) -> Callable:
            # Just return the function, we don't need to track prompts in tests
            return func
        return decorator
    
    def run(self, transport: str = "stdio", **kwargs):
        """Mock run method."""
        pass
    
    def get_tool(self, name: str) -> Optional[Callable]:
        """Get a registered tool function by name."""
        return self._tool_functions.get(name)
    
    def get_resource(self, pattern: str) -> Optional[Callable]:
        """Get a registered resource function by pattern."""
        return self.resources.get(pattern, {}).get('function')


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


class TestConfigureMCPServer:
    """Test MCP server configuration."""
    
    def test_configure_server_basic(self, temp_dir):
        """Test basic server configuration."""
        mcp = MockFastMCP("test-server")
        multi_updater = MagicMock(spec=MultiSourceDocsUpdater)
        
        # For now, configure_mcp_server is a placeholder
        # This test will be expanded when we move the tool registrations
        configure_mcp_server(mcp, temp_dir, "12.x", multi_updater)
        
        # Verify the server was configured (placeholder test)
        assert mcp.name == "test-server"


class TestMCPToolRegistration:
    """Test MCP tool registration through mock."""
    
    def test_tool_registration(self):
        """Test that tools can be registered with the mock."""
        mcp = MockFastMCP("test-server")
        
        @mcp.tool(description="Test tool")
        def test_tool(param: str) -> str:
            """A test tool function."""
            return f"Result: {param}"
        
        # Verify tool was registered
        assert "test_tool" in mcp.tools
        assert mcp.tools["test_tool"]["description"] == "Test tool"
        
        # Verify tool can be called
        tool_func = mcp.get_tool("test_tool")
        assert tool_func is not None
        assert tool_func("test") == "Result: test"
    
    def test_resource_registration(self):
        """Test that resources can be registered with the mock."""
        mcp = MockFastMCP("test-server")
        
        @mcp.resource("test://{path}")
        def test_resource(path: str) -> str:
            """A test resource function."""
            return f"Content of {path}"
        
        # Verify resource was registered
        assert "test://{path}" in mcp.resources
        
        # Verify resource can be called
        resource_func = mcp.get_resource("test://{path}")
        assert resource_func is not None
        assert resource_func("file.txt") == "Content of file.txt"
    
    def test_multiple_tool_registration(self):
        """Test registering multiple tools."""
        mcp = MockFastMCP("test-server")
        
        @mcp.tool(description="Tool 1")
        def tool1() -> str:
            return "Tool 1 result"
        
        @mcp.tool(description="Tool 2")
        def tool2() -> str:
            return "Tool 2 result"
        
        assert len(mcp.tools) == 2
        assert "tool1" in mcp.tools
        assert "tool2" in mcp.tools


class TestMCPServerIntegration:
    """Test integration between components and MCP server."""
    
    def test_server_lifecycle(self, temp_dir):
        """Test basic server lifecycle."""
        # Create mock arguments
        args = argparse.Namespace(
            log_level="INFO",
            docs_path=str(temp_dir),
            version="12.x",
            transport="stdio",
            websocket_host=None,
            websocket_port=None,
            update_docs=False,
            force_update=False,
            server_name="test-server",
            host=None,
            port=None
        )
        
        # Test that all components work together
        with patch('laravel_mcp_companion.setup_docs_path', return_value=temp_dir), \
             patch('laravel_mcp_companion.FastMCP', MockFastMCP), \
             patch('laravel_mcp_companion.MultiSourceDocsUpdater'):
            
            # Setup environment
            docs_path, transport_options = setup_server_environment(args)
            assert docs_path == temp_dir
            
            # Handle documentation update
            result = handle_documentation_update(docs_path, args.version, args.update_docs, args.force_update)
            assert result is False  # No update requested