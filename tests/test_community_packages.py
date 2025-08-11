"""Tests for community package documentation fetching."""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from docs_updater import CommunityPackageFetcher, DocumentationSourceType


class TestCommunityPackageFetcher:
    """Test community package documentation fetching functionality."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp:
            yield Path(temp)
    
    @pytest.fixture
    def fetcher(self, temp_dir):
        """Create a CommunityPackageFetcher instance."""
        return CommunityPackageFetcher(temp_dir)
    
    def test_init(self, fetcher, temp_dir):
        """Test CommunityPackageFetcher initialization."""
        assert fetcher.target_dir == temp_dir
        assert fetcher.cache_duration == 86400
        assert fetcher.max_retries == 3
        assert (temp_dir / "packages").exists()
    
    def test_list_available_packages(self, fetcher):
        """Test listing available packages."""
        packages = fetcher.list_available_packages()
        assert "spatie" in packages
        assert "livewire" in packages
        assert "inertia" in packages
        assert "filament" in packages
        assert "debugbar" in packages
        assert "ide-helper" in packages
        assert len(packages) == 6
    
    def test_get_package_cache_path(self, fetcher, temp_dir):
        """Test getting package cache path."""
        # Test main package
        path = fetcher.get_package_cache_path("livewire")
        assert path == temp_dir / "packages" / "livewire"
        assert path.exists()
        
        # Test sub-package
        sub_path = fetcher.get_package_cache_path("spatie", "laravel-permission")
        assert sub_path == temp_dir / "packages" / "spatie" / "laravel-permission"
        assert sub_path.exists()
    
    def test_get_cache_metadata_path(self, fetcher, temp_dir):
        """Test getting cache metadata path."""
        # Test main package
        path = fetcher.get_cache_metadata_path("livewire")
        assert path == temp_dir / "packages" / "livewire" / ".metadata" / "cache.json"
        
        # Test sub-package
        sub_path = fetcher.get_cache_metadata_path("spatie", "laravel-permission")
        assert sub_path == temp_dir / "packages" / "spatie" / "laravel-permission" / ".metadata" / "cache.json"
    
    def test_is_cache_valid_no_metadata(self, fetcher):
        """Test cache validation when no metadata exists."""
        assert not fetcher.is_cache_valid("livewire")
    
    def test_is_cache_valid_expired(self, fetcher, temp_dir):
        """Test cache validation with expired cache."""
        import time
        import os
        
        # Create expired metadata
        metadata_path = fetcher.get_cache_metadata_path("livewire")
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            "cache_time": time.time() - 86401  # 1 second past expiration
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
        
        # Set file modification time to be expired
        old_time = time.time() - 86401  # 1 second past expiration
        os.utime(metadata_path, (old_time, old_time))
        
        assert not fetcher.is_cache_valid("livewire")
    
    def test_is_cache_valid_fresh(self, fetcher, temp_dir):
        """Test cache validation with fresh cache."""
        import time
        
        # Create fresh metadata
        metadata_path = fetcher.get_cache_metadata_path("livewire")
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            "cache_time": time.time() - 3600  # 1 hour ago
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
        
        assert fetcher.is_cache_valid("livewire")
    
    def test_fetch_package_docs_unknown_package(self, fetcher):
        """Test fetching docs for unknown package."""
        assert not fetcher.fetch_package_docs("unknown-package")
    
    def test_fetch_package_docs_with_cache(self, fetcher, temp_dir):
        """Test fetching docs when cache is valid."""
        # Create valid cache
        import time
        metadata_path = fetcher.get_cache_metadata_path("livewire")
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            "cache_time": time.time() - 3600  # 1 hour ago
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
        
        # Should return True without fetching
        assert fetcher.fetch_package_docs("livewire")
    
    @patch('urllib.request.urlopen')
    def test_fetch_and_process_content(self, mock_urlopen, fetcher):
        """Test content fetching and processing."""
        # Mock response
        mock_response = MagicMock()
        mock_response.read.return_value = b'''
        <html>
        <body>
            <nav>Navigation content</nav>
            <main>
                <h1>Test Documentation</h1>
                <p>This is test content.</p>
                <pre><code class="language-php">
                    echo "Hello World";
                </code></pre>
            </main>
            <footer>Footer content</footer>
        </body>
        </html>
        '''
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        content = fetcher._fetch_and_process_content("https://example.com", "test", "section")
        
        assert content is not None
        assert "# Test - Section" in content
        assert "Source: https://example.com" in content
        assert "Test Documentation" in content
        assert "This is test content." in content
        assert "echo \"Hello World\";" in content
        assert "Navigation content" not in content  # nav removed
        assert "Footer content" not in content  # footer removed
    
    def test_clean_markdown_content(self, fetcher):
        """Test markdown content cleaning."""
        dirty_content = """Too many blank lines



```

Code block
```

Trailing spaces     
More content"""
        
        clean = fetcher._clean_markdown_content(dirty_content)
        
        assert "\n\n\n" not in clean  # No triple newlines
        assert "Trailing spaces\nMore content" in clean  # Trailing whitespace removed
        assert "```\nCode block" in clean  # Code block cleaned
    
    def test_spatie_package_structure(self, fetcher):
        """Test Spatie package structure."""
        spatie_config = fetcher.community_packages["spatie"]
        
        assert spatie_config["name"] == "Spatie Packages"
        assert spatie_config["type"] == DocumentationSourceType.COMMUNITY_PACKAGE
        assert "packages" in spatie_config
        
        # Check sub-packages
        packages = spatie_config["packages"]
        assert "laravel-permission" in packages
        assert "laravel-medialibrary" in packages
        assert "laravel-backup" in packages
        
        # Check a sub-package structure
        permission = packages["laravel-permission"]
        assert permission["name"] == "Laravel Permission"
        assert "docs_url" in permission
        assert "sections" in permission
        assert "introduction" in permission["sections"]
    
    def test_fetch_all_packages(self, fetcher):
        """Test fetching all packages with mocked responses."""
        with patch.object(fetcher, 'fetch_package_docs') as mock_fetch:
            mock_fetch.return_value = True
            
            results = fetcher.fetch_all_packages()
            
            assert len(results) == 6
            assert all(results.values())
            assert mock_fetch.call_count == 6
    
    def test_process_jsx_to_markdown(self, fetcher):
        """Test JSX content extraction to markdown."""
        jsx_content = '''
        import { H1, P, Code, Strong } from '@/Components'
        
        export const meta = {
            title: 'How it works',
        }
        
        export default function() {
            return (
                <>
                    <H1>How it works</H1>
                    <P>
                        With Inertia you build applications just like you've always done with your 
                        server-side web framework of choice. You use your framework's existing 
                        functionality for routing, controllers, middleware, authentication, 
                        authorization, data fetching, and more.
                    </P>
                    <P>
                        However, Inertia replaces your application's view layer. Instead of using 
                        server-side rendering via PHP or Ruby templates, the views returned by your 
                        application are JavaScript page components.
                    </P>
                    <P>
                        At its core, Inertia is essentially a client-side routing library. It allows 
                        you to make page visits without forcing a full page reload. This is done using 
                        the <Code>Link</Code> component.
                    </P>
                    <P>
                        <Strong>The end result is a silky smooth single-page experience.</Strong>
                    </P>
                </>
            )
        }
        '''
        
        result = fetcher._process_jsx_to_markdown(jsx_content, "how-it-works")
        
        assert result is not None
        assert "# How it works" in result
        assert "With Inertia you build applications" in result
        assert "However, Inertia replaces" in result
        assert "At its core, Inertia is essentially" in result
        assert "`Link`" in result  # Code component
        assert "**The end result is a silky smooth single-page experience.**" in result  # Strong component
        # Should not contain JSX syntax
        assert "import {" not in result
        assert "export default" not in result
        assert "return (" not in result
    
    def test_clean_jsx_text(self, fetcher):
        """Test JSX text cleaning functionality."""
        # Test basic text cleaning
        jsx_text = "This is {some.variable} text with <span>HTML</span> tags"
        result = fetcher._clean_jsx_text(jsx_text)
        assert result == "This is text with HTML tags"
        
        # Test HTML entity decoding
        jsx_text = "Text with &amp; entities &lt;and&gt; more"
        result = fetcher._clean_jsx_text(jsx_text)
        assert result == "Text with & entities <and> more"
        
        # Test whitespace cleanup
        jsx_text = "  Multiple   spaces   and  \n  newlines  "
        result = fetcher._clean_jsx_text(jsx_text)
        assert result == "Multiple spaces and newlines"
    
    @patch('urllib.request.urlopen')
    def test_fetch_inertia_docs_github(self, mock_urlopen, fetcher):
        """Test fetching Inertia docs from GitHub repository."""
        # Mock GitHub response with JSX content
        mock_response = MagicMock()
        mock_response.read.return_value = b'''
        import { H1, P } from '@/Components'
        
        export default function() {
            return (
                <>
                    <H1>Test Page</H1>
                    <P>This is test content from GitHub.</P>
                </>
            )
        }
        '''
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        # Mock the configuration for Inertia
        config = {
            "repo": "inertiajs/inertiajs.com",
            "branch": "master", 
            "docs_path": "resources/js/Pages",
            "name": "Inertia.js",
            "sections": ["test-page"]
        }
        
        result = fetcher._fetch_inertia_docs(config)
        
        assert result is True
        # Check that file was created
        file_path = fetcher.get_package_cache_path("inertia") / "test-page.md"
        assert file_path.exists()
        
        # Check file content
        content = file_path.read_text()
        assert "# Inertia - Test Page" in content
        assert "Source: https://inertiajs.com/test-page" in content
        assert "# Test Page" in content
        assert "This is test content from GitHub." in content
    
    def test_inertia_configuration_structure(self, fetcher):
        """Test Inertia configuration structure."""
        inertia_config = fetcher.community_packages["inertia"]
        
        assert inertia_config["name"] == "Inertia.js"
        assert inertia_config["type"] == DocumentationSourceType.GITHUB_REPO
        assert inertia_config["repo"] == "inertiajs/inertiajs.com"
        assert inertia_config["branch"] == "master"
        assert inertia_config["docs_path"] == "resources/js/Pages"
        assert "sections" in inertia_config
        
        # Check that problematic sections are removed
        sections = inertia_config["sections"]
        assert "installation" not in sections  # Should be removed (404)
        assert "server-side-setup" in sections  # Should exist
        assert "client-side-setup" in sections  # Should exist
    
    def test_livewire_configuration_fixed(self, fetcher):
        """Test that Livewire configuration has been fixed to remove 404 sections."""
        livewire_config = fetcher.community_packages["livewire"]
        sections = livewire_config["sections"]
        
        # Check that problematic sections are removed
        assert "file-uploads" not in sections  # Should be "uploads"
        assert "file-downloads" not in sections  # Should be "downloads"  
        assert "alpine-js" not in sections  # Should be "alpine"
        assert "flash-messages" not in sections  # Doesn't exist
        assert "traits" not in sections  # Doesn't exist
        assert "javascript-hooks" not in sections  # Consolidated into "javascript"
        assert "defer" not in sections  # Consolidated into "javascript"
        assert "entangle" not in sections  # Consolidated into "javascript"
        assert "reactive" not in sections  # Consolidated into "javascript"
        assert "spa-mode" not in sections  # Covered by "navigate"
        
        # Check that correct sections exist
        assert "uploads" in sections
        assert "downloads" in sections
        assert "alpine" in sections
        assert "javascript" in sections
        assert "navigate" in sections
    
    def test_simplified_update_behavior(self, fetcher):
        """Test that the simplified --update parameter updates everything."""
        # The --update parameter should update all packages
        available_packages = fetcher.list_available_packages()
        assert len(available_packages) == 6  # All packages should be updated
        assert "spatie" in available_packages
        assert "livewire" in available_packages
        assert "inertia" in available_packages
        assert "filament" in available_packages
        assert "debugbar" in available_packages
        assert "ide-helper" in available_packages