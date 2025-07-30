"""Tests for package fetcher methods in docs_updater."""

import pytest
import json
import time
from unittest.mock import patch, MagicMock
import urllib.error

from docs_updater import CommunityPackageFetcher


class TestPackageFetchers:
    """Test individual package fetcher methods."""
    
    @pytest.fixture
    def package_fetcher(self, temp_dir):
        """Create a CommunityPackageFetcher instance for testing."""
        return CommunityPackageFetcher(temp_dir)
    
    @patch('urllib.request.urlopen')
    def test_fetch_spatie_docs_single_package(self, mock_urlopen, package_fetcher):
        """Test fetching documentation for a single Spatie package."""
        config = {
            "packages": {
                "laravel-permission": {
                    "name": "Laravel Permission",
                    "docs_url": "https://spatie.be/docs/laravel-permission/v6/introduction",
                    "sections": ["introduction"]
                }
            }
        }
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.read.return_value = b"""
        <html>
        <body>
            <div class="markup">
                <h1>Laravel Permission Documentation</h1>
                <p>This package allows you to manage user permissions and roles.</p>
                <h2>Installation</h2>
                <pre><code>composer require spatie/laravel-permission</code></pre>
            </div>
        </body>
        </html>
        """
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response
        
        result = package_fetcher._fetch_spatie_docs(config)
        
        assert result is True
        
        # Check that directory was created
        package_dir = package_fetcher.get_package_cache_path("spatie", "laravel-permission")
        assert package_dir.exists()
        
        # Check that file was created
        intro_file = package_dir / "introduction.md"
        assert intro_file.exists()
        
        # Check content
        content = intro_file.read_text()
        assert "Laravel Permission Documentation" in content
        assert "manage user permissions and roles" in content
        assert "composer require spatie/laravel-permission" in content
    
    @patch('urllib.request.urlopen')
    def test_fetch_spatie_docs_multiple_packages(self, mock_urlopen, package_fetcher):
        """Test fetching documentation for multiple Spatie packages."""
        config = {
            "packages": {
                "laravel-permission": {
                    "name": "Laravel Permission",
                    "docs_url": "https://spatie.be/docs/laravel-permission/v6/introduction",
                    "sections": ["introduction"]
                },
                "laravel-medialibrary": {
                    "name": "Laravel Media Library",
                    "docs_url": "https://spatie.be/docs/laravel-medialibrary/v11/introduction",
                    "sections": ["introduction"]
                }
            }
        }
        
        # Mock responses for both packages
        responses = [
            b"<html><body><div class='markup'><h1>Permission</h1></div></body></html>",
            b"<html><body><div class='markup'><h1>Media Library</h1></div></body></html>"
        ]
        
        mock_response = MagicMock()
        mock_response.read.side_effect = responses
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response
        
        result = package_fetcher._fetch_spatie_docs(config)
        
        assert result is True
        assert mock_urlopen.call_count == 2
        
        # Check both packages were created
        perm_dir = package_fetcher.get_package_cache_path("spatie", "laravel-permission")
        media_dir = package_fetcher.get_package_cache_path("spatie", "laravel-medialibrary")
        assert perm_dir.exists()
        assert media_dir.exists()
    
    @patch('urllib.request.urlopen')
    def test_fetch_spatie_docs_with_http_error(self, mock_urlopen, package_fetcher):
        """Test Spatie docs fetching with HTTP errors."""
        config = {
            "packages": {
                "laravel-permission": {
                    "name": "Laravel Permission",
                    "docs_url": "https://spatie.be/docs/laravel-permission/v6/introduction",
                    "sections": ["introduction"]
                },
                "laravel-medialibrary": {
                    "name": "Laravel Media Library", 
                    "docs_url": "https://spatie.be/docs/laravel-medialibrary/v11/introduction",
                    "sections": ["introduction"]
                }
            }
        }
        
        # First succeeds, second fails
        mock_response_success = MagicMock()
        mock_response_success.read.return_value = b"<html><body><div class='markup'><h1>Success</h1></div></body></html>"
        mock_response_success.__enter__ = lambda self: self
        mock_response_success.__exit__ = lambda self, *args: None
        
        mock_urlopen.side_effect = [
            mock_response_success,
            urllib.error.HTTPError(url="test", code=404, msg="Not Found", hdrs=None, fp=None)
        ]
        
        result = package_fetcher._fetch_spatie_docs(config)
        
        # Should still return True if at least one package succeeded
        assert result is True
        
        # Check that first package was created
        perm_dir = package_fetcher.get_package_cache_path("spatie", "laravel-permission")
        assert perm_dir.exists()
    
    @patch('urllib.request.urlopen')
    def test_fetch_livewire_docs_success(self, mock_urlopen, package_fetcher):
        """Test fetching Livewire documentation."""
        config = {
            "name": "Livewire",
            "base_url": "https://livewire.laravel.com/docs",
            "sections": ["quickstart", "installation", "components"]
        }
        
        # Mock responses for each section
        responses = [
            b"<html><body><h1>Quickstart</h1><p>Get started with Livewire</p></body></html>",
            b"<html><body><h1>Installation</h1><pre>composer require livewire/livewire</pre></body></html>",
            b"<html><body><h1>Components</h1><p>Building Livewire components</p></body></html>"
        ]
        
        mock_response = MagicMock()
        mock_response.read.side_effect = responses
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response
        
        result = package_fetcher._fetch_livewire_docs(config)
        
        assert result is True
        assert mock_urlopen.call_count == 3
        
        # Check files were created
        package_dir = package_fetcher.get_package_cache_path("livewire")
        assert (package_dir / "quickstart.md").exists()
        assert (package_dir / "installation.md").exists()
        assert (package_dir / "components.md").exists()
        
        # Check content conversion
        content = (package_dir / "installation.md").read_text()
        assert "composer require livewire/livewire" in content
    
    @patch('urllib.request.urlopen')
    def test_fetch_livewire_docs_partial_failure(self, mock_urlopen, package_fetcher):
        """Test Livewire docs with some sections failing."""
        config = {
            "name": "Livewire",
            "base_url": "https://livewire.laravel.com/docs",
            "sections": ["quickstart", "missing-section", "components"]
        }
        
        # Mock responses - second one fails
        mock_response_success = MagicMock()
        mock_response_success.read.return_value = b"<html><body><h1>Content</h1></body></html>"
        mock_response_success.__enter__ = lambda self: self
        mock_response_success.__exit__ = lambda self, *args: None
        
        mock_urlopen.side_effect = [
            mock_response_success,
            urllib.error.HTTPError(url="test", code=404, msg="Not Found", hdrs=None, fp=None),
            mock_response_success
        ]
        
        result = package_fetcher._fetch_livewire_docs(config)
        
        # Should return True if at least one section succeeded
        assert result is True
        
        # Check that successful sections were created
        package_dir = package_fetcher.get_package_cache_path("livewire")
        assert (package_dir / "quickstart.md").exists()
        assert (package_dir / "components.md").exists()
        assert not (package_dir / "missing-section.md").exists()
    
    @patch('urllib.request.urlopen')
    def test_fetch_filament_docs_with_version(self, mock_urlopen, package_fetcher):
        """Test fetching Filament documentation with version."""
        config = {
            "name": "Filament",
            "base_url": "https://filamentphp.com/docs",
            "version": "3.x",
            "sections": ["panels/installation", "forms/fields", "tables/columns"]
        }
        
        # Mock responses
        mock_response = MagicMock()
        mock_response.read.return_value = b"""
        <html>
        <body>
            <div class="prose">
                <h1>Filament Documentation</h1>
                <p>Building admin panels with Filament</p>
                <code>composer require filament/filament</code>
            </div>
        </body>
        </html>
        """
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response
        
        result = package_fetcher._fetch_filament_docs(config)
        
        assert result is True
        
        # Verify URLs were constructed with version
        expected_urls = [
            "https://filamentphp.com/docs/3.x/panels/installation",
            "https://filamentphp.com/docs/3.x/forms/fields",
            "https://filamentphp.com/docs/3.x/tables/columns"
        ]
        
        # Get the actual URLs that were called
        actual_urls = [call[0][0].full_url for call in mock_urlopen.call_args_list]
        assert actual_urls == expected_urls
        
        # Check files were created with dashes instead of directories
        package_dir = package_fetcher.get_package_cache_path("filament")
        assert (package_dir / "panels-installation.md").exists()
        assert (package_dir / "forms-fields.md").exists()
        assert (package_dir / "tables-columns.md").exists()
    
    @patch('urllib.request.urlopen')
    def test_fetch_filament_docs_all_fail(self, mock_urlopen, package_fetcher):
        """Test Filament docs when all sections fail."""
        config = {
            "name": "Filament",
            "base_url": "https://filamentphp.com/docs",
            "version": "3.x",
            "sections": ["missing1", "missing2"]
        }
        
        # All requests fail
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="test", code=404, msg="Not Found", hdrs=None, fp=None
        )
        
        result = package_fetcher._fetch_filament_docs(config)
        
        # Should return False when all sections fail
        assert result is False
    
    def test_fetch_package_docs_with_cache(self, package_fetcher):
        """Test that cached packages aren't re-fetched."""
        # Create valid cache metadata for the main package
        metadata_path = package_fetcher.get_cache_metadata_path("spatie")
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            "cache_time": time.time(),  # Current time - cache is fresh
            "package": "spatie"
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
        
        # Mock the fetch method to ensure it's not called
        with patch.object(package_fetcher, '_fetch_spatie_docs') as mock_fetch:
            result = package_fetcher.fetch_package_docs("spatie")
            
            # Should return True without calling fetch
            assert result is True
            mock_fetch.assert_not_called()
    
    def test_fetch_package_docs_force_update(self, package_fetcher):
        """Test force update ignores cache."""
        # Create valid cache metadata
        metadata_path = package_fetcher.get_cache_metadata_path("livewire")
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            "cache_time": time.time(),  # Current time - cache is fresh
            "package": "livewire"
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
        
        # Mock the fetch method
        with patch.object(package_fetcher, '_fetch_livewire_docs', return_value=True) as mock_fetch:
            result = package_fetcher.fetch_package_docs("livewire", force=True)
            
            # Should call fetch despite valid cache
            assert result is True
            mock_fetch.assert_called_once()
    
    def test_fetch_inertia_docs_from_github(self, package_fetcher):
        """Test that Inertia docs use GitHub fetching."""
        with patch.object(package_fetcher, '_fetch_inertia_docs', return_value=True) as mock_fetch:
            result = package_fetcher.fetch_package_docs("inertia")
            
            assert result is True
            mock_fetch.assert_called_once()
    
    def test_fetch_unknown_package(self, package_fetcher):
        """Test fetching unknown package returns False."""
        result = package_fetcher.fetch_package_docs("unknown-package")
        assert result is False
    
    @patch('urllib.request.urlopen')
    def test_fetch_debugbar_docs_success(self, mock_urlopen, package_fetcher):
        """Test fetching Laravel Debugbar documentation."""
        config = {
            "name": "Laravel Debugbar",
            "base_url": "https://laraveldebugbar.com",
            "sections": ["installation", "usage", "features", "collectors"]
        }
        
        # Mock responses for each section
        mock_response = MagicMock()
        mock_response.read.return_value = b"""
        <html>
        <body>
            <div class="prose">
                <h1>Installation</h1>
                <p>Install Laravel Debugbar with composer:</p>
                <pre><code>composer require barryvdh/laravel-debugbar --dev</code></pre>
                <p>The package provides debugging capabilities for Laravel applications.</p>
            </div>
        </body>
        </html>
        """
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response
        
        result = package_fetcher._fetch_debugbar_docs(config)
        
        assert result is True
        
        # Check that files were created
        package_dir = package_fetcher.get_package_cache_path("debugbar")
        assert (package_dir / "installation.md").exists()
        assert (package_dir / "usage.md").exists()
        assert (package_dir / "features.md").exists()
        assert (package_dir / "collectors.md").exists()
        
        # Check content was processed
        content = (package_dir / "installation.md").read_text()
        assert "Installation" in content
        assert "composer require barryvdh/laravel-debugbar" in content
    
    @patch('urllib.request.urlopen')
    def test_fetch_ide_helper_docs_success(self, mock_urlopen, package_fetcher):
        """Test fetching Laravel IDE Helper documentation from GitHub."""
        config = {
            "name": "Laravel IDE Helper",
            "repo": "barryvdh/laravel-ide-helper",
            "branch": "master",
            "file": "README.md"
        }
        
        # Mock README content
        mock_response = MagicMock()
        mock_response.read.return_value = b"""# Laravel IDE Helper Generator

This package generates helper files that enable your IDE to provide accurate autocompletion.

## Installation

```bash
composer require --dev barryvdh/laravel-ide-helper
```

## Usage

Generate helper files:

```bash
php artisan ide-helper:generate
```

Generate model docs:

```bash
php artisan ide-helper:models
```
"""
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response
        
        result = package_fetcher._fetch_ide_helper_docs(config)
        
        assert result is True
        
        # Check that file was created
        package_dir = package_fetcher.get_package_cache_path("ide-helper")
        readme_file = package_dir / "readme.md"
        assert readme_file.exists()
        
        # Check content
        content = readme_file.read_text()
        assert "Laravel IDE Helper" in content
        assert "Source: https://github.com/barryvdh/laravel-ide-helper" in content
        assert "composer require --dev barryvdh/laravel-ide-helper" in content
        assert "php artisan ide-helper:generate" in content
    
    @patch('urllib.request.urlopen')
    def test_fetch_ide_helper_docs_404_error(self, mock_urlopen, package_fetcher):
        """Test IDE Helper docs with 404 error."""
        config = {
            "name": "Laravel IDE Helper",
            "repo": "barryvdh/laravel-ide-helper",
            "branch": "invalid",
            "file": "README.md"
        }
        
        # Mock 404 error
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="test", code=404, msg="Not Found", hdrs=None, fp=None
        )
        
        result = package_fetcher._fetch_ide_helper_docs(config)
        
        assert result is False