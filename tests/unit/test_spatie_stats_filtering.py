"""Tests for Spatie package documentation statistics filtering."""

from pathlib import Path
from unittest.mock import Mock, patch

from docs_updater import CommunityPackageFetcher


class TestSpatieStatsFiltering:
    """Test that Spatie package statistics are properly filtered during documentation fetching."""
    
    def test_removes_repository_stats_section(self):
        """Test that Repository/Open Issues section with stats is removed."""
        html_content = """
        <html>
            <body>
                <div class="stats-container">
                    <h3>Repository</h3>
                    <p>Open Issues</p>
                    <div>17,716,982</div>
                    <div>5,853</div>
                </div>
                <main>
                    <h1>Laravel Backup</h1>
                    <p>This is the actual documentation content.</p>
                </main>
            </body>
        </html>
        """
        
        fetcher = CommunityPackageFetcher(Path("/tmp/docs"))
        with patch('docs_updater.urllib.request.urlopen') as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = html_content.encode('utf-8')
            mock_response.__enter__ = lambda self: self
            mock_response.__exit__ = lambda self, *args: None
            mock_urlopen.return_value = mock_response
            
            content = fetcher._fetch_and_process_content("https://example.com", "spatie", "test")
            
            # Stats should be removed
            assert "17,716,982" not in content
            assert "5,853" not in content
            # Documentation content should remain
            assert "Laravel Backup" in content
            assert "actual documentation content" in content
    
    def test_removes_standalone_large_numbers(self):
        """Test that standalone large numbers are removed unless they're in code blocks."""
        html_content = """
        <html>
            <body>
                <div>29,053,153</div>
                <span>1,234,567</span>
                <pre><code>
                // This number should remain
                $maxSize = 1048576; // 1MB
                </code></pre>
                <p>Normal text here.</p>
            </body>
        </html>
        """
        
        fetcher = CommunityPackageFetcher(Path("/tmp/docs"))
        with patch('docs_updater.urllib.request.urlopen') as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = html_content.encode('utf-8')
            mock_response.__enter__ = lambda self: self
            mock_response.__exit__ = lambda self, *args: None
            mock_urlopen.return_value = mock_response
            
            content = fetcher._fetch_and_process_content("https://example.com", "spatie", "test")
            
            # Standalone large stats numbers should be removed
            assert "29,053,153" not in content
            assert "1,234,567" not in content
            # But code block numbers should remain
            assert "1048576" in content
            assert "Normal text here" in content
    
    def test_preserves_small_numbers(self):
        """Test that small numbers (likely not stats) are preserved."""
        html_content = """
        <html>
            <body>
                <h2>Step 1: Install the package</h2>
                <p>Run composer require spatie/laravel-backup</p>
                <p>This will take about 30 seconds.</p>
                <p>Version 9.0.0 requires PHP 8.</p>
            </body>
        </html>
        """
        
        fetcher = CommunityPackageFetcher(Path("/tmp/docs"))
        with patch('docs_updater.urllib.request.urlopen') as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = html_content.encode('utf-8')
            mock_response.__enter__ = lambda self: self
            mock_response.__exit__ = lambda self, *args: None
            mock_urlopen.return_value = mock_response
            
            content = fetcher._fetch_and_process_content("https://example.com", "spatie", "test")
            
            # Small numbers should be preserved
            assert "Step 1" in content
            assert "30 seconds" in content
            assert "9.0.0" in content
            assert "PHP 8" in content
    
    def test_removes_stats_containers_by_class(self):
        """Test that divs/sections with stats-related classes are removed."""
        html_content = """
        <html>
            <body>
                <div class="package-stats">
                    <span>Total Downloads</span>
                    <span>69,144,081</span>
                </div>
                <section class="metrics-container">
                    <div>Weekly Downloads: 123,456</div>
                </section>
                <div class="documentation">
                    <h1>Getting Started</h1>
                    <p>Welcome to the documentation.</p>
                </div>
            </body>
        </html>
        """
        
        fetcher = CommunityPackageFetcher(Path("/tmp/docs"))
        with patch('docs_updater.urllib.request.urlopen') as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = html_content.encode('utf-8')
            mock_response.__enter__ = lambda self: self
            mock_response.__exit__ = lambda self, *args: None
            mock_urlopen.return_value = mock_response
            
            content = fetcher._fetch_and_process_content("https://example.com", "spatie", "test")
            
            # Stats containers should be removed
            assert "69,144,081" not in content
            assert "123,456" not in content
            assert "Total Downloads" not in content
            assert "Weekly Downloads" not in content
            # Documentation should remain
            assert "Getting Started" in content
            assert "Welcome to the documentation" in content
    
    def test_stats_filtering_only_applies_to_spatie(self):
        """Test that stats filtering only applies to Spatie packages."""
        html_content = """
        <html>
            <body>
                <div>Downloads: 1,234,567</div>
                <h1>Package Documentation</h1>
                <p>This package has 1,234,567 downloads.</p>
            </body>
        </html>
        """
        
        fetcher = CommunityPackageFetcher(Path("/tmp/docs"))
        with patch('docs_updater.urllib.request.urlopen') as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = html_content.encode('utf-8')
            mock_response.__enter__ = lambda self: self
            mock_response.__exit__ = lambda self, *args: None
            mock_urlopen.return_value = mock_response
            
            # Test with non-Spatie package
            content = fetcher._fetch_and_process_content("https://example.com", "other-vendor", "test")
            
            # Stats should NOT be removed for non-Spatie packages
            assert "1,234,567" in content
            assert "Package Documentation" in content
    
    def test_handles_nested_stats_containers(self):
        """Test handling of nested containers with stats."""
        html_content = """
        <html>
            <body>
                <header>
                    <div class="package-header">
                        <div class="package-info">
                            <h2>Repository</h2>
                            <p>Open Issues</p>
                            <span>17,704,897</span>
                            <span>5,853</span>
                        </div>
                    </div>
                </header>
                <main>
                    <h1>Documentation</h1>
                    <p>Actual content here.</p>
                </main>
            </body>
        </html>
        """
        
        fetcher = CommunityPackageFetcher(Path("/tmp/docs"))
        with patch('docs_updater.urllib.request.urlopen') as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = html_content.encode('utf-8')
            mock_response.__enter__ = lambda self: self
            mock_response.__exit__ = lambda self, *args: None
            mock_urlopen.return_value = mock_response
            
            content = fetcher._fetch_and_process_content("https://example.com", "spatie", "test")
            
            # Nested stats should be removed
            assert "17,704,897" not in content
            assert "5,853" not in content
            # Main content should remain
            assert "Documentation" in content
            assert "Actual content here" in content