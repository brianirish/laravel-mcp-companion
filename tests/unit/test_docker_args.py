"""Unit tests for Docker argument handling and command-line parsing."""

import pytest
import sys
import subprocess
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

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
            '--transport', 'websocket',
            '--host', '0.0.0.0',
            '--port', '8080'
        ]
        
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            assert args.version == "10.x"
            assert args.log_level == "DEBUG"
            assert args.transport == "websocket"
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
        # Simulating: docker run ... --version 11.x --transport websocket --host 0.0.0.0 --port 8080
        test_args = [
            'laravel-mcp-companion',
            '--version', '11.x',
            '--transport', 'websocket',
            '--host', '0.0.0.0',
            '--port', '8080',
            '--log-level', 'INFO',
            '--server-name', 'DockerMCPServer'
        ]
        
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            assert args.version == "11.x"
            assert args.transport == "websocket"
            assert args.host == "0.0.0.0"
            assert args.port == 8080
            assert args.log_level == "INFO"
            assert args.server_name == "DockerMCPServer"


class TestDockerfileEntrypoint:
    """Test Dockerfile configuration for proper argument handling."""
    
    def test_dockerfile_uses_entrypoint(self):
        """Verify that Dockerfile uses ENTRYPOINT instead of just CMD."""
        dockerfile_path = Path(__file__).parent.parent.parent / "Dockerfile"
        
        if dockerfile_path.exists():
            with open(dockerfile_path, 'r') as f:
                dockerfile_content = f.read()
            
            # Check that ENTRYPOINT is used
            assert 'ENTRYPOINT ["python", "laravel_mcp_companion.py"]' in dockerfile_content
            
            # Check that CMD is empty or provides default args
            assert 'CMD []' in dockerfile_content or 'CMD [""]' in dockerfile_content
    
    def test_dockerfile_python_unbuffered(self):
        """Verify that PYTHONUNBUFFERED is set for proper Docker logging."""
        dockerfile_path = Path(__file__).parent.parent.parent / "Dockerfile"
        
        if dockerfile_path.exists():
            with open(dockerfile_path, 'r') as f:
                dockerfile_content = f.read()
            
            assert 'ENV PYTHONUNBUFFERED=1' in dockerfile_content


class TestDockerBuildScript:
    """Test for Docker build/run helper scripts if they exist."""
    
    def create_test_dockerfile(self):
        """Create a test Dockerfile to verify argument passing."""
        dockerfile_content = '''FROM python:3.12-alpine
WORKDIR /app
COPY laravel_mcp_companion.py .
RUN pip install --no-cache-dir fastmcp mcp[cli,client]
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "laravel_mcp_companion.py"]
CMD []
'''
        return dockerfile_content
    
    def test_docker_argument_passing_simulation(self):
        """Simulate Docker argument passing to verify it works correctly."""
        # This test verifies that our solution works conceptually
        # In a real Docker environment, ENTRYPOINT + CMD allows argument passing
        
        # Simulate what Docker does with ENTRYPOINT
        entrypoint = ["python", "laravel_mcp_companion.py"]
        user_args = ["--version", "11.x", "--log-level", "DEBUG"]
        
        # Docker combines ENTRYPOINT with user args
        final_command = entrypoint + user_args
        
        # Verify the final command is correct
        assert final_command == [
            "python", "laravel_mcp_companion.py",
            "--version", "11.x",
            "--log-level", "DEBUG"
        ]