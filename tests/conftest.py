"""Pytest configuration and fixtures for Laravel MCP Companion tests."""

import os
import tempfile
import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from typing import Dict, Any, Generator

# Import the modules we'll be testing
import laravel_mcp_companion
import docs_updater
from shutdown_handler import GracefulShutdown

# Register custom markers to avoid warnings
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "network: marks tests that require network access")
    config.addinivalue_line("markers", "external: marks tests that interact with external services")


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def test_docs_dir(temp_dir: Path) -> Path:
    """Create a test documentation directory structure."""
    docs_dir = temp_dir / "docs"
    docs_dir.mkdir()
    
    # Create version directories
    for version in ["11.x", "12.x"]:
        version_dir = docs_dir / version
        version_dir.mkdir()
        
        # Create sample markdown files
        (version_dir / "installation.md").write_text(f"# Installation\n\nLaravel {version} installation guide.")
        (version_dir / "routing.md").write_text(f"# Routing\n\nLaravel {version} routing documentation.")
        (version_dir / "eloquent.md").write_text(f"# Eloquent ORM\n\nEloquent documentation for {version}.")
        
        # Create metadata directory and file
        metadata_dir = version_dir / ".metadata"
        metadata_dir.mkdir()
        
        metadata = {
            "version": version,
            "commit_sha": f"abc123{version[-1]}",
            "commit_date": "2024-01-01T12:00:00Z",
            "commit_message": f"Update {version} documentation",
            "commit_url": f"https://github.com/laravel/docs/commit/abc123{version[-1]}",
            "sync_time": "2024-01-01T12:00:00Z"
        }
        
        (metadata_dir / "sync_info.json").write_text(json.dumps(metadata, indent=2))
    
    return docs_dir


@pytest.fixture
def test_external_docs_dir(temp_dir: Path) -> Path:
    """Create a test external documentation directory structure."""
    external_dir = temp_dir / "docs" / "external"
    external_dir.mkdir(parents=True)
    
    # Create service directories with sample files
    services = ["forge", "vapor", "envoyer", "nova"]
    
    for service in services:
        service_dir = external_dir / service
        service_dir.mkdir()
        
        # Create sample documentation files
        (service_dir / "introduction.md").write_text(f"# {service.title()}\n\nIntroduction to Laravel {service.title()}.")
        (service_dir / "getting-started.md").write_text(f"# Getting Started\n\nHow to get started with {service.title()}.")
        
        # Create cache metadata
        metadata = {
            "service": service,
            "fetched_sections": ["introduction", "getting-started"],
            "total_sections": 2,
            "success_rate": 1.0,
            "discovery_method": "manual configuration",
            "cached_at": 1704110400.0  # 2024-01-01 12:00:00
        }
        
        (service_dir / ".cache_metadata.json").write_text(json.dumps(metadata, indent=2))
    
    return external_dir


@pytest.fixture
def sample_package_catalog() -> Dict[str, Any]:
    """Sample package catalog for testing."""
    return {
        "laravel/cashier": {
            "name": "Laravel Cashier",
            "description": "Laravel Cashier provides an expressive, fluent interface to Stripe's subscription billing services.",
            "categories": ["payment", "billing", "subscription"],
            "use_cases": [
                "Implementing subscription billing",
                "Processing one-time payments"
            ],
            "installation": "composer require laravel/cashier",
            "documentation_link": "laravel://packages/cashier.md"
        },
        "laravel/sanctum": {
            "name": "Laravel Sanctum",
            "description": "Laravel Sanctum provides a featherweight authentication system for SPAs.",
            "categories": ["authentication", "api", "security"],
            "use_cases": [
                "Authenticating SPAs",
                "API token authentication"
            ],
            "installation": "composer require laravel/sanctum",
            "documentation_link": "laravel://authentication/sanctum.md"
        }
    }


@pytest.fixture
def mock_github_api() -> Generator[MagicMock, None, None]:
    """Mock GitHub API responses."""
    with patch('docs_updater.urllib.request.urlopen') as mock_urlopen:
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "commit": {
                "sha": "abc123def456",
                "commit": {
                    "committer": {"date": "2024-01-01T12:00:00Z"},
                    "message": "Update documentation"
                },
                "html_url": "https://github.com/laravel/docs/commit/abc123def456"
            }
        }).encode()
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        
        mock_urlopen.return_value = mock_response
        yield mock_urlopen


@pytest.fixture
def mock_file_download() -> Generator[MagicMock, None, None]:
    """Mock file downloads for testing."""
    with patch('docs_updater.urllib.request.urlopen') as mock_urlopen:
        # Mock successful download
        mock_response = MagicMock()
        mock_response.read.return_value = b"Mock file content"
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        
        mock_urlopen.return_value = mock_response
        yield mock_urlopen


@pytest.fixture
def mock_fastmcp():
    """Mock FastMCP for testing tool registration."""
    with patch('laravel_mcp_companion.FastMCP') as mock_mcp:
        mock_instance = MagicMock()
        mock_mcp.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def docs_updater_instance(test_docs_dir: Path) -> docs_updater.DocsUpdater:
    """Create a DocsUpdater instance for testing."""
    return docs_updater.DocsUpdater(test_docs_dir, "12.x")


@pytest.fixture
def external_docs_fetcher(test_docs_dir: Path) -> docs_updater.ExternalDocsFetcher:
    """Create an ExternalDocsFetcher instance for testing."""
    return docs_updater.ExternalDocsFetcher(test_docs_dir)


@pytest.fixture
def multi_source_updater(test_docs_dir: Path) -> docs_updater.MultiSourceDocsUpdater:
    """Create a MultiSourceDocsUpdater instance for testing."""
    return docs_updater.MultiSourceDocsUpdater(test_docs_dir, "12.x")


@pytest.fixture
def shutdown_handler() -> GracefulShutdown:
    """Create a GracefulShutdown instance for testing."""
    return GracefulShutdown()


@pytest.fixture
def mock_logger():
    """Mock logger for testing."""
    return MagicMock()


@pytest.fixture(autouse=True)
def clear_caches():
    """Clear all caches before each test."""
    # Import mcp_tools for cache clearing
    import mcp_tools
    
    # Clear mcp_tools caches
    mcp_tools.clear_caches()
    
    # Clear main module caches if they exist
    if hasattr(laravel_mcp_companion, '_file_content_cache'):
        laravel_mcp_companion._file_content_cache.clear()
    if hasattr(laravel_mcp_companion, '_search_result_cache'):
        laravel_mcp_companion._search_result_cache.clear()
    
    # Clear function cache if it exists
    if hasattr(laravel_mcp_companion, 'get_file_content_cached') and hasattr(laravel_mcp_companion.get_file_content_cached, 'cache_clear'):
        laravel_mcp_companion.get_file_content_cached.cache_clear()
    
    yield
    
    # Clear caches after test
    mcp_tools.clear_caches()
    
    if hasattr(laravel_mcp_companion, '_file_content_cache'):
        laravel_mcp_companion._file_content_cache.clear()
    if hasattr(laravel_mcp_companion, '_search_result_cache'):
        laravel_mcp_companion._search_result_cache.clear()
    
    if hasattr(laravel_mcp_companion, 'get_file_content_cached') and hasattr(laravel_mcp_companion.get_file_content_cached, 'cache_clear'):
        laravel_mcp_companion.get_file_content_cached.cache_clear()


@pytest.fixture
def sample_html_content() -> str:
    """Sample HTML content for testing HTML processing."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Laravel Documentation</title></head>
    <body>
        <main>
            <h1>Laravel Installation</h1>
            <p>Welcome to Laravel! This guide will help you install Laravel.</p>
            
            <h2>Requirements</h2>
            <ul>
                <li>PHP >= 8.1</li>
                <li>Composer</li>
            </ul>
            
            <h2>Installation Steps</h2>
            <ol>
                <li>Run <code>composer create-project laravel/laravel myapp</code></li>
                <li>Navigate to your project: <code>cd myapp</code></li>
                <li>Start the development server: <code>php artisan serve</code></li>
            </ol>
        </main>
    </body>
    </html>
    """


# Mock environment variables for consistent testing
@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Set up test environment variables."""
    monkeypatch.setenv("PYTEST_RUNNING", "1")
    # Ensure we don't accidentally hit real APIs during tests
    monkeypatch.setenv("GITHUB_API_URL", "http://mock-api.test")