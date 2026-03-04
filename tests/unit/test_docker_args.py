"""Unit tests for Docker argument handling and command-line parsing."""

import sys
from unittest.mock import patch

from laravel_mcp_companion import parse_arguments


class TestDockerArgumentHandling:
    """Test that Docker correctly passes arguments to the Python script."""
    
    def test_parse_version_argument(self):
        """Test parsing --version argument as used in the bug report."""
        test_args = ['laravel-mcp-companion', '--version', '11.x']
        
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            assert args.version == "11.x"
    
    def test_parse_multiple_arguments(self):
        """Test parsing multiple arguments that might be passed via Docker."""
        test_args = [
            'laravel-mcp-companion',
            '--version', '10.x',
            '--log-level', 'DEBUG',
            '--transport', 'http',
            '--host', '0.0.0.0',
            '--port', '8080'
        ]

        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            assert args.version == "10.x"
            assert args.log_level == "DEBUG"
            assert args.transport == "http"
            assert args.host == "0.0.0.0"
            assert args.port == 8080
    
    def test_all_supported_versions(self):
        """Test that all supported Laravel versions can be parsed."""
        supported_versions = ['10.x', '11.x', '12.x']
        
        for version in supported_versions:
            test_args = ['laravel-mcp-companion', '--version', version]
            with patch.object(sys, 'argv', test_args):
                args = parse_arguments()
                assert args.version == version
    
    def test_docs_path_argument(self):
        """Test --docs-path argument parsing."""
        test_args = ['laravel-mcp-companion', '--docs-path', '/app/docs']
        
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            assert args.docs_path == "/app/docs"
    
    def test_update_docs_flags(self):
        """Test --update-docs and --force-update flags."""
        # Test update-docs alone
        test_args = ['laravel-mcp-companion', '--update-docs']
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            assert args.update_docs is True
            assert args.force_update is False
        
        # Test force-update alone
        test_args = ['laravel-mcp-companion', '--force-update']
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            assert args.force_update is True
            assert args.update_docs is False
        
        # Test both together
        test_args = ['laravel-mcp-companion', '--update-docs', '--force-update']
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            assert args.update_docs is True
            assert args.force_update is True
    
    def test_server_name_argument(self):
        """Test --server-name argument parsing."""
        test_args = ['laravel-mcp-companion', '--server-name', 'CustomServer']
        
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            assert args.server_name == "CustomServer"
    
    def test_combined_docker_scenario(self):
        """Test a typical Docker scenario with multiple arguments."""
        # Simulating: docker run ... --version 11.x --transport http --host 0.0.0.0 --port 8080
        test_args = [
            'laravel-mcp-companion',
            '--version', '11.x',
            '--transport', 'http',
            '--host', '0.0.0.0',
            '--port', '8080',
            '--log-level', 'INFO',
            '--server-name', 'DockerMCPServer'
        ]

        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            assert args.version == "11.x"
            assert args.transport == "http"
            assert args.host == "0.0.0.0"
            assert args.port == 8080
            assert args.log_level == "INFO"
            assert args.server_name == "DockerMCPServer"


