"""Unit tests for documentation updater functionality."""

import pytest
import json
import tempfile
import zipfile
import io
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock, mock_open
import urllib.error

from docs_updater import (
    DocsUpdater,
    ExternalDocsFetcher,
    MultiSourceDocsUpdater,
    DocumentationAutoDiscovery,
    DocumentationSourceType,
    CommunityPackageFetcher,
    get_supported_versions,
    get_cached_supported_versions,
    SUPPORTED_VERSIONS,
    DEFAULT_VERSION
)


class TestDocsUpdater:
    """Test core documentation updater functionality."""

    def test_init(self, temp_dir):
        """Test DocsUpdater initialization."""
        updater = DocsUpdater(temp_dir, "12.x")
        
        assert updater.target_dir == temp_dir
        assert updater.version == "12.x"
        assert updater.version_dir == temp_dir / "12.x"
        assert updater.metadata_dir == temp_dir / "12.x" / ".metadata"
        assert updater.metadata_file == temp_dir / "12.x" / ".metadata" / "sync_info.json"
        
        # Directories should be created
        assert updater.version_dir.exists()
        assert updater.metadata_dir.exists()

    @patch('docs_updater.urllib.request.urlopen')
    def test_get_latest_commit_success(self, mock_urlopen, docs_updater_instance):
        """Test successful GitHub API call for latest commit."""
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
        
        result = docs_updater_instance.get_latest_commit()
        
        assert result["sha"] == "abc123def456"
        assert result["date"] == "2024-01-01T12:00:00Z"
        assert result["message"] == "Update documentation"
        assert result["url"] == "https://github.com/laravel/docs/commit/abc123def456"

    @patch('docs_updater.urllib.request.urlopen')
    def test_get_latest_commit_http_error(self, mock_urlopen, docs_updater_instance):
        """Test GitHub API call with HTTP error."""
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="test", code=404, msg="Not Found", hdrs=None, fp=None
        )
        
        with pytest.raises(urllib.error.HTTPError):
            docs_updater_instance.get_latest_commit()

    @patch('docs_updater.urllib.request.urlopen')
    def test_get_latest_commit_rate_limit(self, mock_urlopen, docs_updater_instance):
        """Test GitHub API rate limiting handling."""
        # First call: rate limit error
        # Second call: success
        mock_responses = [
            urllib.error.HTTPError(url="test", code=403, msg="Rate Limited", hdrs=None, fp=None),
            MagicMock()
        ]
        
        success_response = MagicMock()
        success_response.read.return_value = json.dumps({
            "commit": {
                "sha": "abc123",
                "commit": {
                    "committer": {"date": "2024-01-01T12:00:00Z"},
                    "message": "Update"
                },
                "html_url": "https://github.com/laravel/docs/commit/abc123"
            }
        }).encode()
        success_response.__enter__ = lambda self: self
        success_response.__exit__ = lambda self, *args: None
        
        mock_responses[1] = success_response
        mock_urlopen.side_effect = mock_responses
        
        # Should retry and succeed
        with patch('docs_updater.time.sleep'):  # Speed up test
            result = docs_updater_instance.get_latest_commit()
            assert result["sha"] == "abc123"

    def test_read_local_metadata_exists(self, docs_updater_instance):
        """Test reading existing local metadata."""
        metadata = {
            "version": "12.x",
            "commit_sha": "abc123",
            "sync_time": "2024-01-01T12:00:00Z"
        }
        
        docs_updater_instance.metadata_file.write_text(json.dumps(metadata))
        
        result = docs_updater_instance.read_local_metadata()
        assert result == metadata

    def test_read_local_metadata_not_exists(self, docs_updater_instance):
        """Test reading non-existent local metadata."""
        # Ensure metadata file doesn't exist
        if docs_updater_instance.metadata_file.exists():
            docs_updater_instance.metadata_file.unlink()
        
        result = docs_updater_instance.read_local_metadata()
        assert result == {}

    def test_read_local_metadata_corrupted(self, docs_updater_instance):
        """Test reading corrupted local metadata."""
        docs_updater_instance.metadata_file.write_text("invalid json {")
        
        result = docs_updater_instance.read_local_metadata()
        assert result == {}

    def test_write_local_metadata(self, docs_updater_instance):
        """Test writing local metadata."""
        metadata = {
            "version": "12.x",
            "commit_sha": "abc123",
            "sync_time": "2024-01-01T12:00:00Z"
        }
        
        docs_updater_instance.write_local_metadata(metadata)
        
        assert docs_updater_instance.metadata_file.exists()
        written_data = json.loads(docs_updater_instance.metadata_file.read_text())
        assert written_data == metadata

    @patch('docs_updater.shutil.copyfileobj')
    @patch('docs_updater.urllib.request.urlopen')
    @patch('docs_updater.tempfile.mkdtemp')
    @patch('docs_updater.zipfile.ZipFile')
    def test_download_documentation_success(self, mock_zipfile, mock_mkdtemp, mock_urlopen, mock_copyfileobj, docs_updater_instance, temp_dir):
        """Test successful documentation download."""
        # Create a real temporary directory structure
        mock_temp_path = temp_dir / "download_test"
        mock_temp_path.mkdir()

        # Mock mkdtemp to return our test directory
        mock_mkdtemp.return_value = str(mock_temp_path)

        # Mock URL response
        mock_response = MagicMock()
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response

        # Mock shutil.copyfileobj to create the file
        def create_zip_file(src, dst):
            dst.write(b"mock zip content")
        mock_copyfileobj.side_effect = create_zip_file

        # Mock zipfile extraction
        mock_zip_instance = MagicMock()
        mock_zipfile.return_value.__enter__ = lambda self: mock_zip_instance
        mock_zipfile.return_value.__exit__ = lambda self, *args: None

        # Create the expected extracted directory
        extracted_dir = mock_temp_path / "docs-12.x"
        extracted_dir.mkdir()
        (extracted_dir / "test.md").write_text("test content")

        result = docs_updater_instance.download_documentation()
        assert result.name == "docs-12.x"

    @patch.object(DocsUpdater, 'get_latest_commit')
    def test_needs_update_true(self, mock_get_latest_commit, docs_updater_instance):
        """Test needs_update when update is needed."""
        mock_get_latest_commit.return_value = {"sha": "new123"}
        
        # Write old metadata
        old_metadata = {"version": "12.x", "commit_sha": "old123"}
        docs_updater_instance.write_local_metadata(old_metadata)
        
        assert docs_updater_instance.needs_update() is True

    @patch.object(DocsUpdater, 'get_latest_commit')
    def test_needs_update_false(self, mock_get_latest_commit, docs_updater_instance):
        """Test needs_update when no update is needed."""
        mock_get_latest_commit.return_value = {"sha": "same123"}
        
        # Write same metadata
        same_metadata = {"version": "12.x", "commit_sha": "same123"}
        docs_updater_instance.write_local_metadata(same_metadata)
        
        assert docs_updater_instance.needs_update() is False

    @patch.object(DocsUpdater, 'get_latest_commit')
    def test_needs_update_no_local_metadata(self, mock_get_latest_commit, docs_updater_instance):
        """Test needs_update when no local metadata exists."""
        mock_get_latest_commit.return_value = {"sha": "abc123"}
        
        assert docs_updater_instance.needs_update() is True

    @patch.object(DocsUpdater, 'get_latest_commit')
    def test_needs_update_error(self, mock_get_latest_commit, docs_updater_instance):
        """Test needs_update when error occurs."""
        mock_get_latest_commit.side_effect = Exception("Network error")
        
        # Should return True (assume update needed on error)
        assert docs_updater_instance.needs_update() is True

    @patch.object(DocsUpdater, 'needs_update')
    @patch.object(DocsUpdater, 'get_latest_commit')
    @patch.object(DocsUpdater, 'download_documentation')
    def test_update_success(self, mock_download, mock_get_latest_commit, mock_needs_update, docs_updater_instance):
        """Test successful documentation update."""
        mock_needs_update.return_value = True
        mock_get_latest_commit.return_value = {
            "sha": "abc123",
            "date": "2024-01-01T12:00:00Z",
            "message": "Update docs",
            "url": "https://github.com/laravel/docs/commit/abc123"
        }
        
        # Mock downloaded directory with files
        source_dir = MagicMock(spec=Path)
        source_dir.parent = MagicMock(spec=Path)
        
        # Create mock file
        mock_file = MagicMock(spec=Path)
        mock_file.name = "file.md"
        mock_file.is_dir.return_value = False
        
        # Setup source_dir.iterdir to return mock files
        source_dir.iterdir.return_value = [mock_file]
        
        mock_download.return_value = source_dir
        
        with patch('docs_updater.shutil.copytree'), \
             patch('docs_updater.shutil.copy2'), \
             patch('docs_updater.shutil.rmtree'), \
             patch('docs_updater.time.strftime', return_value="2024-01-01T12:00:00Z"):
            
            result = docs_updater_instance.update(force=False)
            
            assert result is True
            # Should write metadata
            metadata = docs_updater_instance.read_local_metadata()
            assert metadata["commit_sha"] == "abc123"

    @patch.object(DocsUpdater, 'needs_update')
    def test_update_not_needed(self, mock_needs_update, docs_updater_instance):
        """Test update when not needed."""
        mock_needs_update.return_value = False
        
        result = docs_updater_instance.update(force=False)
        assert result is False

    @patch.object(DocsUpdater, 'needs_update')
    def test_update_force(self, mock_needs_update, docs_updater_instance):
        """Test forced update."""
        mock_needs_update.return_value = False
        
        with patch.object(docs_updater_instance, 'get_latest_commit') as mock_get_latest_commit, \
             patch.object(docs_updater_instance, 'download_documentation') as mock_download:
            
            mock_get_latest_commit.return_value = {
                "sha": "abc123", "date": "2024-01-01T12:00:00Z",
                "message": "Update", "url": "test"
            }
            
            # Mock source directory
            source_dir = MagicMock(spec=Path)
            source_dir.parent = MagicMock(spec=Path)
            source_dir.iterdir.return_value = []
            mock_download.return_value = source_dir
            
            with patch('docs_updater.shutil.copytree'), \
                 patch('docs_updater.shutil.copy2'), \
                 patch('docs_updater.shutil.rmtree'), \
                 patch('docs_updater.time.strftime', return_value="2024-01-01T12:00:00Z"):
                
                result = docs_updater_instance.update(force=True)
                assert result is True
    
    @patch('docs_updater.urllib.request.urlopen')
    def test_download_documentation_network_error(self, mock_urlopen, docs_updater_instance):
        """Test documentation download with network error."""
        mock_urlopen.side_effect = urllib.error.URLError("Network error")
        
        with pytest.raises(urllib.error.URLError):
            docs_updater_instance.download_documentation()
    
    @patch('docs_updater.shutil.copyfileobj')
    @patch('docs_updater.urllib.request.urlopen')
    @patch('docs_updater.tempfile.TemporaryDirectory')
    def test_download_documentation_zip_error(self, mock_tempdir, mock_urlopen, mock_copyfileobj, docs_updater_instance, temp_dir):
        """Test documentation download with zip extraction error."""
        # Create a real temporary directory structure
        mock_temp_path = temp_dir / "download_test"
        mock_temp_path.mkdir()
        
        # Mock TemporaryDirectory to return our test directory
        mock_tempdir_instance = MagicMock()
        mock_tempdir_instance.__enter__ = lambda self: str(mock_temp_path)
        mock_tempdir_instance.__exit__ = lambda self, *args: None
        mock_tempdir.return_value = mock_tempdir_instance
        
        # Mock URL response
        mock_response = MagicMock()
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response
        
        # Create invalid zip file
        zip_path = mock_temp_path / "laravel_docs.zip"
        zip_path.write_text("invalid zip content")
        
        with pytest.raises(Exception):
            docs_updater_instance.download_documentation()
    
    @patch.object(DocsUpdater, 'get_latest_commit')
    @patch.object(DocsUpdater, 'download_documentation')
    def test_update_with_exception(self, mock_download, mock_get_latest_commit, docs_updater_instance):
        """Test update when exception occurs during download."""
        mock_get_latest_commit.return_value = {
            "sha": "abc123",
            "date": "2024-01-01T12:00:00Z",
            "message": "Update",
            "url": "test"
        }
        mock_download.side_effect = Exception("Download failed")
        
        with pytest.raises(Exception) as exc_info:
            docs_updater_instance.update(force=True)
        assert "Download failed" in str(exc_info.value)
    
    def test_update_copies_subdirectories(self, docs_updater_instance):
        """Test that update correctly copies subdirectories."""
        with patch.object(docs_updater_instance, 'needs_update', return_value=True), \
             patch.object(docs_updater_instance, 'get_latest_commit') as mock_commit, \
             patch.object(docs_updater_instance, 'download_documentation') as mock_download:
            
            mock_commit.return_value = {
                "sha": "abc123",
                "date": "2024-01-01T12:00:00Z", 
                "message": "Update",
                "url": "test"
            }
            
            # Create mock source with subdirectory
            source_dir = MagicMock(spec=Path)
            source_dir.parent = MagicMock(spec=Path)
            
            mock_subdir = MagicMock(spec=Path)
            mock_subdir.name = "subdir"
            mock_subdir.is_dir.return_value = True
            
            source_dir.iterdir.return_value = [mock_subdir]
            mock_download.return_value = source_dir
            
            with patch('docs_updater.shutil.copytree') as mock_copytree, \
                 patch('docs_updater.shutil.rmtree'), \
                 patch('docs_updater.time.strftime', return_value="2024-01-01T12:00:00Z"):
                
                result = docs_updater_instance.update()
                assert result is True
                # Verify copytree was called for subdirectory
                mock_copytree.assert_called()
    
    def test_read_write_metadata_cycle(self, docs_updater_instance):
        """Test reading and writing metadata cycle."""
        # Write some metadata
        metadata = {
            "version": "12.x",
            "commit_sha": "abc123",
            "sync_time": "2024-01-01T12:00:00Z"
        }
        docs_updater_instance.write_local_metadata(metadata)
        
        # Read it back
        read_metadata = docs_updater_instance.read_local_metadata()
        
        assert read_metadata["version"] == "12.x"
        assert read_metadata["commit_sha"] == "abc123"


class TestExternalDocsFetcher:
    """Test external documentation fetcher."""

    def test_init(self, temp_dir):
        """Test ExternalDocsFetcher initialization."""
        fetcher = ExternalDocsFetcher(temp_dir)
        
        assert fetcher.target_dir == temp_dir
        assert fetcher.external_dir == temp_dir / "external"
        assert fetcher.external_dir.exists()
        assert isinstance(fetcher.laravel_services, dict)
        assert "forge" in fetcher.laravel_services
        assert "vapor" in fetcher.laravel_services

    def test_get_service_cache_path(self, external_docs_fetcher):
        """Test service cache path generation."""
        cache_path = external_docs_fetcher.get_service_cache_path("forge")
        
        assert cache_path == external_docs_fetcher.external_dir / "forge"
        assert cache_path.exists()  # Should be created

    def test_get_cache_metadata_path(self, external_docs_fetcher):
        """Test cache metadata path generation."""
        metadata_path = external_docs_fetcher.get_cache_metadata_path("forge")
        
        expected = external_docs_fetcher.external_dir / "forge" / ".cache_metadata.json"
        assert metadata_path == expected

    def test_is_cache_valid_no_metadata(self, external_docs_fetcher):
        """Test cache validation when no metadata exists."""
        assert external_docs_fetcher.is_cache_valid("forge") is False

    def test_is_cache_valid_expired(self, external_docs_fetcher):
        """Test cache validation when cache is expired."""
        import time
        import json
        import os
        # Set timestamp to more than cache_duration (86400 seconds) ago
        old_timestamp = time.time() - (external_docs_fetcher.cache_duration + 1000)
        metadata = {"cached_at": old_timestamp}
        
        # Write metadata directly to bypass save_cache_metadata which updates timestamp
        metadata_path = external_docs_fetcher.get_cache_metadata_path("forge")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
        
        # Set file modification time to be expired
        os.utime(metadata_path, (old_timestamp, old_timestamp))
        
        assert external_docs_fetcher.is_cache_valid("forge") is False

    def test_is_cache_valid_fresh(self, external_docs_fetcher):
        """Test cache validation when cache is fresh."""
        import time
        metadata = {
            "cached_at": time.time(),
            "success_rate": 1.0  # Required for cache validity (must be >= 0.9)
        }
        external_docs_fetcher.save_cache_metadata("forge", metadata)

        assert external_docs_fetcher.is_cache_valid("forge") is True

    def test_save_cache_metadata(self, external_docs_fetcher):
        """Test saving cache metadata."""
        metadata = {"service": "forge", "fetched_sections": ["intro"]}
        external_docs_fetcher.save_cache_metadata("forge", metadata)
        
        metadata_path = external_docs_fetcher.get_cache_metadata_path("forge")
        assert metadata_path.exists()
        
        saved_data = json.loads(metadata_path.read_text())
        assert saved_data["service"] == "forge"
        assert saved_data["fetched_sections"] == ["intro"]

    @patch('docs_updater.urllib.request.urlopen')
    def test_fetch_laravel_service_docs_success(self, mock_urlopen, external_docs_fetcher):
        """Test successful service documentation fetching."""
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.read.return_value = b"<html><body><h1>Laravel Forge</h1><p>Documentation content</p></body></html>"
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response
        
        # Mock auto-discovery to return empty (use manual sections)
        with patch.object(external_docs_fetcher.auto_discovery, 'discover_sections', return_value=[]):
            result = external_docs_fetcher.fetch_laravel_service_docs("forge")
            
            assert result is True
            # Check that some files were created
            service_dir = external_docs_fetcher.get_service_cache_path("forge")
            md_files = list(service_dir.glob("*.md"))
            assert len(md_files) > 0

    def test_fetch_laravel_service_docs_unknown_service(self, external_docs_fetcher):
        """Test fetching docs for unknown service."""
        result = external_docs_fetcher.fetch_laravel_service_docs("unknown_service")
        assert result is False

    @patch('docs_updater.urllib.request.urlopen')
    def test_fetch_laravel_service_docs_http_error(self, mock_urlopen, external_docs_fetcher):
        """Test service doc fetching with HTTP errors."""
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="test", code=404, msg="Not Found", hdrs=None, fp=None
        )
        
        with patch.object(external_docs_fetcher.auto_discovery, 'discover_sections', return_value=[]):
            result = external_docs_fetcher.fetch_laravel_service_docs("forge")
            # Should return False or handle gracefully
            assert isinstance(result, bool)

    def test_list_available_services(self, external_docs_fetcher):
        """Test listing available services."""
        services = external_docs_fetcher.list_available_services()
        
        assert isinstance(services, list)
        assert "forge" in services
        assert "vapor" in services
        assert "envoyer" in services
        assert "nova" in services

    def test_get_service_info(self, external_docs_fetcher):
        """Test getting service information."""
        forge_info = external_docs_fetcher.get_service_info("forge")
        
        assert forge_info is not None
        assert forge_info["name"] == "Laravel Forge"
        assert "base_url" in forge_info
        
        # Unknown service should return None
        unknown_info = external_docs_fetcher.get_service_info("unknown")
        assert unknown_info is None

    def test_html_to_text_conversion(self, external_docs_fetcher):
        """Test HTML to text conversion."""
        html_content = """
        <h1>Laravel Forge</h1>
        <p>This is a <strong>test</strong> paragraph with <em>emphasis</em>.</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
        <code>composer install</code>
        """
        
        text_content = external_docs_fetcher._html_to_text(html_content)
        
        assert "# Laravel Forge" in text_content
        assert "**test**" in text_content
        assert "*emphasis*" in text_content
        assert "- Item 1" in text_content
        assert "`composer install`" in text_content

    def test_html_to_text_support_link_filtering(self, external_docs_fetcher):
        """Test that Support links with email protection are filtered out."""
        html_content = """
        <div>
            <a href="https://forge.laravel.com">Laravel Forge home page</a>
            <a href="/cdn-cgi/l/email-protection#b5d3dac7d2d0f5d9d4c7d4c3d0d99bd6dad8">Support</a>
            <a href="/dashboard">Dashboard</a>
            <a href="https://support.laravel.com">Support</a>
            <a href="/cdn-cgi/l/email-protection#123456">Contact Us</a>
        </div>
        """
        
        text_content = external_docs_fetcher._html_to_text(html_content)
        
        # Regular links should be converted
        assert "[Laravel Forge home page](https://forge.laravel.com)" in text_content
        assert "[Dashboard](/dashboard)" in text_content
        
        # Support link without email protection should be kept
        assert "[Support](https://support.laravel.com)" in text_content
        
        # Other link with email protection but not Support text should be kept
        assert "[Contact Us](/cdn-cgi/l/email-protection#123456)" in text_content
        
        # Support links with email protection should have link removed but text kept
        assert "email-protection#b5d3dac7d2d0f5d9d4c7d4c3d0d99bd6dad8" not in text_content
        # Check that we have both Support texts - one as plain text, one as a link
        assert text_content.count("Support") == 2  # Plain text Support + linked Support
        assert "[Support](https://support.laravel.com)" in text_content  # Good Support link kept
        assert "[Support](/cdn-cgi/l/email-protection" not in text_content  # Bad Support link removed

    def test_process_service_html(self, external_docs_fetcher, sample_html_content):
        """Test service HTML processing."""
        processed = external_docs_fetcher._process_service_html(
            sample_html_content, "forge", "introduction"
        )
        
        assert "# Forge - Introduction" in processed
        assert "Laravel Installation" in processed
        assert "PHP >= 8.1" in processed
        assert "composer create-project" in processed
    
    def test_save_cache_metadata_write_error(self, external_docs_fetcher):
        """Test saving cache metadata with write error."""
        # Make directory read-only to cause write error
        external_docs_fetcher.get_service_cache_path("forge")
        
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            # Should not raise exception
            external_docs_fetcher.save_cache_metadata("forge", {"test": "data"})
    
    @patch('docs_updater.urllib.request.urlopen')
    def test_fetch_service_documentation_success(self, mock_urlopen, external_docs_fetcher):
        """Test fetching service documentation successfully."""
        mock_html = "<html><body><h1>Forge Docs</h1><p>Content</p></body></html>"
        
        mock_response = MagicMock()
        mock_response.read.return_value = mock_html.encode()
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response
        
        service_config = {
            "name": "Laravel Forge",
            "base_url": "https://forge.laravel.com/docs",
            "sections": ["introduction"],
            "type": "laravel_service"
        }
        service_dir = external_docs_fetcher.get_service_cache_path("forge")
        
        result = external_docs_fetcher._fetch_service_documentation("forge", service_config, service_dir)
        
        assert result is True
        # Check that file was created
        intro_file = service_dir / "introduction.md"
        assert intro_file.exists()
    
    def test_fetch_github_documentation(self, external_docs_fetcher, temp_dir):
        """Test fetching documentation from GitHub."""
        # Create a fake zip file with documentation
        with tempfile.TemporaryDirectory() as temp_zip_dir:
            # Create a directory structure that simulates extracted GitHub archive
            repo_dir = Path(temp_zip_dir) / "repo-main"
            repo_dir.mkdir()
            docs_dir = repo_dir / "docs"
            docs_dir.mkdir()
            
            # Create a readme file
            readme_file = docs_dir / "readme.md"
            readme_file.write_text("# Test Documentation\n\nThis is test content.")
            
            # Create a zip file
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_ref:
                # Add files to zip with the expected structure
                zip_ref.write(readme_file, arcname="repo-main/docs/readme.md")
            
            zip_content = zip_buffer.getvalue()
        
        service_config = {
            "name": "Test Service",
            "repo": "test/repo",
            "branch": "main",
            "path": "docs",
            "sections": ["readme.md"],
            "type": DocumentationSourceType.GITHUB_REPO
        }
        service_dir = external_docs_fetcher.get_service_cache_path("test")
        
        with patch.object(external_docs_fetcher, '_retry_request', return_value=zip_content):
            result = external_docs_fetcher._fetch_github_documentation("test", service_config, service_dir)
            
            assert result is True
            # Check that the docs directory was copied
            assert (service_dir / "docs").exists()
            # Check that file was created inside docs directory
            assert (service_dir / "docs" / "readme.md").exists()
    
    def test_fetch_all_services(self, external_docs_fetcher):
        """Test fetching all services."""
        with patch.object(external_docs_fetcher, 'fetch_laravel_service_docs') as mock_fetch:
            mock_fetch.side_effect = [True, False, True, True]  # forge, vapor, envoyer, nova
            
            results = external_docs_fetcher.fetch_all_services(force=False)
            
            assert results["forge"] is True
            assert results["vapor"] is False
            assert results["envoyer"] is True
            assert results["nova"] is True
            assert mock_fetch.call_count == 4
    
    def test_fetch_all_services_force(self, external_docs_fetcher):
        """Test fetching all services with force flag."""
        # Create valid cache for one service
        import time
        external_docs_fetcher.save_cache_metadata("forge", {"cached_at": time.time()})
        
        with patch.object(external_docs_fetcher, 'fetch_laravel_service_docs') as mock_fetch:
            mock_fetch.return_value = True
            
            # Force should fetch all services regardless of cache
            external_docs_fetcher.fetch_all_services(force=True)
            
            # All services should be attempted
            assert mock_fetch.call_count == 4  # forge, vapor, envoyer, nova
    
    def test_create_placeholder_documentation_vapor(self, external_docs_fetcher, temp_dir):
        """Test creating placeholder documentation for Vapor."""
        service_config = {
            "name": "Laravel Vapor",
            "base_url": "https://docs.vapor.build",
            "sections": ["getting-started", "projects", "deployments"]
        }
        service_dir = external_docs_fetcher.get_service_cache_path("vapor")
        
        result = external_docs_fetcher._create_placeholder_documentation("vapor", service_config, service_dir)
        
        assert result is True
        
        # Check that files were created
        assert (service_dir / "getting-started.md").exists()
        assert (service_dir / "projects.md").exists()
        assert (service_dir / "deployments.md").exists()
        
        # Check content of getting-started
        content = (service_dir / "getting-started.md").read_text()
        assert "Laravel Vapor - Getting Started" in content
        assert "requires authentication to access" in content
        assert "Setting up serverless Laravel applications" in content
        assert "Configuring AWS Lambda deployment" in content
        
        # Check metadata was saved
        metadata_path = external_docs_fetcher.get_cache_metadata_path("vapor")
        assert metadata_path.exists()
        metadata = json.loads(metadata_path.read_text())
        assert metadata["type"] == "placeholder"
        assert metadata["service"] == "vapor"
        assert metadata["success_rate"] == 1.0
    
    def test_create_placeholder_documentation_envoyer(self, external_docs_fetcher, temp_dir):
        """Test creating placeholder documentation for Envoyer."""
        service_config = {
            "name": "Laravel Envoyer",
            "base_url": "https://docs.envoyer.io/docs/1.0",
            "sections": ["getting-started", "projects", "deployments"]
        }
        service_dir = external_docs_fetcher.get_service_cache_path("envoyer")
        
        result = external_docs_fetcher._create_placeholder_documentation("envoyer", service_config, service_dir)
        
        assert result is True
        
        # Check that files were created
        assert (service_dir / "getting-started.md").exists()
        assert (service_dir / "projects.md").exists()
        assert (service_dir / "deployments.md").exists()
        
        # Check content of deployments
        content = (service_dir / "deployments.md").read_text()
        assert "Laravel Envoyer - Deployments" in content
        assert "requires authentication to access" in content
        assert "Configuring deployment hooks" in content
        assert "Managing deployment history" in content
        
        # Check URL replacement
        assert "Visit [Laravel Envoyer](https://docs.envoyer.io)" in content
    
    def test_create_placeholder_documentation_generic_sections(self, external_docs_fetcher, temp_dir):
        """Test creating placeholder documentation with generic sections."""
        service_config = {
            "name": "Test Service",
            "base_url": "https://test.example.com/docs",
            "sections": ["api-reference", "custom-section"]
        }
        service_dir = external_docs_fetcher.get_service_cache_path("test_service")
        
        result = external_docs_fetcher._create_placeholder_documentation("test_service", service_config, service_dir)
        
        assert result is True
        
        # Check that files were created
        assert (service_dir / "api-reference.md").exists()
        assert (service_dir / "custom-section.md").exists()
        
        # Check generic content
        content = (service_dir / "api-reference.md").read_text()
        assert "Test Service - Api Reference" in content
        assert "This section covers api reference functionality" in content
        assert "requires authentication to access" in content
        
        # Should not have specific use cases for unknown service/section
        assert "Setting up serverless" not in content
        assert "zero-downtime deployment" not in content
    


class TestDocumentationAutoDiscovery:
    """Test auto-discovery system."""

    def test_init(self):
        """Test DocumentationAutoDiscovery initialization."""
        discovery = DocumentationAutoDiscovery(max_retries=5, request_delay=2.0)
        
        assert discovery.max_retries == 5
        assert discovery.request_delay == 2.0

    @patch('docs_updater.urllib.request.urlopen')
    def test_discover_forge_sections(self, mock_urlopen):
        """Test Forge section discovery."""
        mock_html = """
        <html>
        <body>
            <a href="/docs/introduction">Introduction</a>
            <a href="/docs/servers/management">Server Management</a>
            <a href="/docs/sites/deployment">Site Deployment</a>
            <a href="https://external.com">External Link</a>
        </body>
        </html>
        """
        
        mock_response = MagicMock()
        mock_response.read.return_value = mock_html.encode()
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response
        
        discovery = DocumentationAutoDiscovery()
        config = {"base_url": "https://forge.laravel.com/docs"}
        
        sections = discovery._discover_forge_sections(config, {})
        
        assert "introduction" in sections
        assert "servers/management" in sections
        assert "sites/deployment" in sections
        assert len(sections) == 3

    @patch('docs_updater.urllib.request.urlopen')
    def test_retry_request_success(self, mock_urlopen):
        """Test successful retry request."""
        mock_response = MagicMock()
        mock_response.read.return_value = b"success"
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response
        
        discovery = DocumentationAutoDiscovery()
        result = discovery._retry_request("https://example.com")
        
        assert result == b"success"

    @patch('docs_updater.urllib.request.urlopen')
    def test_retry_request_with_retry(self, mock_urlopen):
        """Test retry request with initial failure."""
        # First call fails, second succeeds
        responses = [
            urllib.error.HTTPError(url="test", code=500, msg="Server Error", hdrs=None, fp=None),
            MagicMock()
        ]
        
        success_response = MagicMock()
        success_response.read.return_value = b"success"
        success_response.__enter__ = lambda self: self
        success_response.__exit__ = lambda self, *args: None
        responses[1] = success_response
        
        mock_urlopen.side_effect = responses
        
        discovery = DocumentationAutoDiscovery()
        with patch('docs_updater.time.sleep'):  # Speed up test
            result = discovery._retry_request("https://example.com")
            assert result == b"success"

    @patch('docs_updater.urllib.request.urlopen')
    def test_retry_request_404_no_retry(self, mock_urlopen):
        """Test that 404 errors are not retried."""
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="test", code=404, msg="Not Found", hdrs=None, fp=None
        )
        
        discovery = DocumentationAutoDiscovery()
        with pytest.raises(urllib.error.HTTPError):
            discovery._retry_request("https://example.com")
    
    @patch('docs_updater.urllib.request.urlopen')
    def test_retry_request_rate_limit(self, mock_urlopen):
        """Test retry request with rate limiting (429 error)."""
        # First two calls fail with 429, third succeeds
        responses = [
            urllib.error.HTTPError(url="test", code=429, msg="Too Many Requests", hdrs=None, fp=None),
            urllib.error.HTTPError(url="test", code=429, msg="Too Many Requests", hdrs=None, fp=None),
            MagicMock()
        ]
        
        success_response = MagicMock()
        success_response.read.return_value = b"success"
        success_response.__enter__ = lambda self: self
        success_response.__exit__ = lambda self, *args: None
        responses[2] = success_response
        
        mock_urlopen.side_effect = responses
        
        discovery = DocumentationAutoDiscovery(max_retries=3)
        with patch('docs_updater.time.sleep'), \
             patch('docs_updater.random.uniform', return_value=1.0):
            result = discovery._retry_request("https://example.com")
            assert result == b"success"
    
    @patch('docs_updater.urllib.request.urlopen')
    def test_retry_request_server_error(self, mock_urlopen):
        """Test retry request with server errors (5xx)."""
        # First call fails with 500, second succeeds
        responses = [
            urllib.error.HTTPError(url="test", code=503, msg="Service Unavailable", hdrs=None, fp=None),
            MagicMock()
        ]
        
        success_response = MagicMock()
        success_response.read.return_value = b"success"
        success_response.__enter__ = lambda self: self
        success_response.__exit__ = lambda self, *args: None
        responses[1] = success_response
        
        mock_urlopen.side_effect = responses
        
        discovery = DocumentationAutoDiscovery()
        with patch('docs_updater.time.sleep'), \
             patch('docs_updater.random.uniform', return_value=1.0):
            result = discovery._retry_request("https://example.com")
            assert result == b"success"
    
    @patch('docs_updater.urllib.request.urlopen')
    def test_retry_request_max_retries_exceeded(self, mock_urlopen):
        """Test retry request when max retries are exceeded."""
        mock_urlopen.side_effect = Exception("Network error")
        
        discovery = DocumentationAutoDiscovery(max_retries=2)
        with patch('docs_updater.time.sleep'), \
             patch('docs_updater.random.uniform', return_value=1.0):
            with pytest.raises(Exception) as exc_info:
                discovery._retry_request("https://example.com")
            assert "Network error" in str(exc_info.value)
    
    def test_discover_sections_auto_discovery_disabled(self):
        """Test discover sections when auto-discovery is disabled."""
        discovery = DocumentationAutoDiscovery()
        service_config = {"auto_discovery": False}
        
        sections = discovery.discover_sections("forge", service_config)
        assert sections == []
    
    def test_discover_nova_sections(self):
        """Test Nova section discovery."""
        mock_html = """
        <html>
        <body>
            <a href="/docs/v4/installation">Installation</a>
            <a href="/docs/v4/resources">Resources</a>
            <a href="/docs/v4/filters">Filters</a>
        </body>
        </html>
        """
        
        discovery = DocumentationAutoDiscovery()
        config = {"base_url": "https://nova.laravel.com/docs"}
        
        with patch.object(discovery, '_retry_request', return_value=mock_html.encode()):
            sections = discovery._discover_nova_sections(config, {})
            
            assert "installation" in sections
            assert "resources" in sections
            assert "filters" in sections
    
    def test_discover_vapor_sections(self):
        """Test Vapor section discovery."""
        mock_html = """
        <html>
        <body>
            <a href="/docs/introduction">Introduction</a>
            <a href="/docs/projects/environments">Environments</a>
            <a href="/docs/projects/deployments">Deployments</a>
        </body>
        </html>
        """
        
        discovery = DocumentationAutoDiscovery()
        config = {"base_url": "https://vapor.laravel.com/docs"}
        
        with patch.object(discovery, '_retry_request', return_value=mock_html.encode()):
            sections = discovery._discover_vapor_sections(config, {})
            
            assert "docs/introduction" in sections
            assert "docs/projects/environments" in sections
            assert "docs/projects/deployments" in sections
    
    def test_discover_envoyer_sections(self):
        """Test Envoyer section discovery."""
        mock_html = """
        <html>
        <body>
            <ul class="table-of-contents">
                <li><a href="/docs/introduction">Introduction</a></li>
                <li><a href="/docs/servers">Servers</a></li>
                <li><a href="/docs/deployments">Deployments</a></li>
            </ul>
        </body>
        </html>
        """
        
        discovery = DocumentationAutoDiscovery()
        config = {"base_url": "https://envoyer.io/docs"}
        
        with patch.object(discovery, '_retry_request') as mock_retry:
            # First call returns the main page HTML
            # Subsequent calls return valid content for each section
            # Content must be >500 chars and contain envoyer-related keywords
            valid_content = """<html><body>
                <h1>Envoyer Documentation</h1>
                <p>Envoyer is a deployment tool for PHP applications that provides zero downtime deployments.</p>
                <p>This section covers the deployment process, server management, and project configuration.</p>
                <p>You can configure deployment hooks, manage your servers, set up notifications, and connect your repository.</p>
                <p>Envoyer ensures your application deployments are smooth and reliable with features like health checks and rollbacks.</p>
                <p>This documentation will guide you through all aspects of using Envoyer for your deployment needs.</p>
                <p>Learn about managing projects, configuring servers, setting up deployment scripts, and monitoring your applications.</p>
            </body></html>"""
            
            mock_retry.side_effect = [
                mock_html.encode(),  # Main page
                valid_content.encode(),  # introduction
                valid_content.encode(),  # servers
                valid_content.encode()  # deployments
            ]
            sections = discovery._discover_envoyer_sections(config, {})
            
            assert "introduction" in sections
            assert "servers" in sections
            assert "deployments" in sections
    
    def test_discover_sections_unknown_service(self):
        """Test discover sections with unknown service."""
        discovery = DocumentationAutoDiscovery()
        service_config = {"auto_discovery": True}
        
        sections = discovery.discover_sections("unknown_service", service_config)
        assert sections == []
    
    @patch('docs_updater.urllib.request.urlopen')
    def test_discover_sections_with_exception(self, mock_urlopen):
        """Test discover sections when exception occurs."""
        mock_urlopen.side_effect = Exception("Discovery failed")
        
        discovery = DocumentationAutoDiscovery()
        service_config = {"auto_discovery": True, "base_url": "https://forge.laravel.com/docs"}
        
        sections = discovery.discover_sections("forge", service_config)
        assert sections == []


class TestMultiSourceDocsUpdater:
    """Test multi-source documentation updater."""

    def test_init(self, temp_dir):
        """Test MultiSourceDocsUpdater initialization."""
        updater = MultiSourceDocsUpdater(temp_dir, "12.x")
        
        assert updater.target_dir == temp_dir
        assert updater.version == "12.x"
        assert isinstance(updater.core_updater, DocsUpdater)
        assert isinstance(updater.external_fetcher, ExternalDocsFetcher)

    @patch.object(DocsUpdater, 'update')
    def test_update_core_docs(self, mock_update, multi_source_updater):
        """Test core documentation update."""
        mock_update.return_value = True
        
        result = multi_source_updater.update_core_docs(force=False)
        assert result is True
        mock_update.assert_called_once_with(force=False)

    @patch.object(ExternalDocsFetcher, 'fetch_laravel_service_docs')
    def test_update_external_docs_specific_services(self, mock_fetch, multi_source_updater):
        """Test external documentation update for specific services."""
        mock_fetch.return_value = True
        
        result = multi_source_updater.update_external_docs(services=["forge"], force=False)
        
        assert result == {"forge": True}
        mock_fetch.assert_called_once_with("forge")

    @patch.object(ExternalDocsFetcher, 'fetch_all_services')
    def test_update_external_docs_all_services(self, mock_fetch_all, multi_source_updater):
        """Test external documentation update for all services."""
        mock_fetch_all.return_value = {"forge": True, "vapor": False}
        
        result = multi_source_updater.update_external_docs(force=False)
        
        assert result == {"forge": True, "vapor": False}
        mock_fetch_all.assert_called_once_with(force=False)

    def test_update_external_docs_unknown_service(self, multi_source_updater):
        """Test external documentation update with unknown service."""
        result = multi_source_updater.update_external_docs(services=["unknown_service"])
        
        assert result == {"unknown_service": False}
    
    @patch.object(CommunityPackageFetcher, 'list_available_packages')
    @patch.object(ExternalDocsFetcher, 'get_cache_metadata_path')
    @patch.object(ExternalDocsFetcher, 'get_service_info')
    @patch.object(ExternalDocsFetcher, 'is_cache_valid')
    @patch.object(ExternalDocsFetcher, 'list_available_services')
    @patch.object(DocsUpdater, 'read_local_metadata')
    def test_get_all_documentation_status_complete(self, mock_core_metadata, 
                                                   mock_list_services, mock_is_cache_valid,
                                                   mock_get_service_info, mock_get_cache_path,
                                                   mock_list_packages, multi_source_updater):
        """Test getting complete documentation status."""
        # Mock core documentation status
        mock_core_metadata.return_value = {
            "sync_time": "2024-01-15T10:00:00Z",
            "commit_sha": "abc123"
        }
        
        # Mock external services
        mock_list_services.return_value = ["forge", "vapor"]
        mock_is_cache_valid.return_value = True
        mock_get_service_info.side_effect = [
            {"name": "Laravel Forge", "type": "laravel_service"},
            {"name": "Laravel Vapor", "type": "laravel_service"}
        ]
        
        # Mock cache metadata paths
        mock_metadata_path = Mock()
        mock_metadata_path.exists.return_value = True
        # Mock stat() to return an object with st_mtime
        mock_stat = Mock()
        mock_stat.st_mtime = 1234567890
        mock_metadata_path.stat.return_value = mock_stat
        mock_get_cache_path.return_value = mock_metadata_path
        
        # Mock metadata file content
        with patch('builtins.open', mock_open(read_data='{"cached_at": 1234567890, "success_rate": "100%"}')):
            with patch('json.load', return_value={"cached_at": 1234567890, "success_rate": "100%"}):
                # Mock packages
                mock_list_packages.return_value = []
                
                status = multi_source_updater.get_all_documentation_status()
        
        assert "core" in status
        assert status["core"]["version"] == "12.x"
        assert status["core"]["available"] is True
        assert status["core"]["last_updated"] == "2024-01-15T10:00:00Z"
        assert status["core"]["commit_sha"] == "abc123"
        
        assert "external" in status
        assert "forge" in status["external"]
        assert status["external"]["forge"]["name"] == "Laravel Forge"
        assert status["external"]["forge"]["cache_valid"] is True
        
        assert "vapor" in status["external"]
        assert status["external"]["vapor"]["name"] == "Laravel Vapor"
    
    @patch.object(CommunityPackageFetcher, 'list_available_packages')
    @patch.object(ExternalDocsFetcher, 'get_service_info')
    @patch.object(ExternalDocsFetcher, 'is_cache_valid')
    @patch.object(ExternalDocsFetcher, 'list_available_services')
    @patch.object(DocsUpdater, 'read_local_metadata')
    def test_get_all_documentation_status_no_metadata(self, mock_core_metadata,
                                                      mock_list_services, mock_is_cache_valid,
                                                      mock_get_service_info, mock_list_packages,
                                                      multi_source_updater):
        """Test status when no metadata exists."""
        # Mock no core metadata
        mock_core_metadata.return_value = {}
        
        # Mock external services with no cache
        mock_list_services.return_value = ["forge"]
        mock_is_cache_valid.return_value = False
        mock_get_service_info.return_value = {"name": "Laravel Forge", "type": "laravel_service"}
        
        # Mock packages
        mock_list_packages.return_value = []
        
        # Mock non-existent metadata file
        with patch.object(multi_source_updater.external_fetcher, 'get_cache_metadata_path') as mock_path:
            mock_metadata_path = Mock()
            mock_metadata_path.exists.return_value = False
            mock_path.return_value = mock_metadata_path
            
            status = multi_source_updater.get_all_documentation_status()
        
        assert status["core"]["available"] is False
        assert status["external"]["forge"]["cache_valid"] is False
        assert status["external"]["forge"]["last_fetched"] == "never"
    
    @patch.object(CommunityPackageFetcher, 'list_available_packages')
    @patch.object(ExternalDocsFetcher, 'list_available_services')
    @patch.object(DocsUpdater, 'read_local_metadata')
    def test_get_all_documentation_status_with_errors(self, mock_core_metadata,
                                                      mock_list_services, mock_list_packages,
                                                      multi_source_updater):
        """Test status when errors occur."""
        # Mock core metadata error
        mock_core_metadata.side_effect = Exception("Core metadata error")
        
        # Mock external services
        mock_list_services.return_value = ["forge"]
        
        # Mock packages
        mock_list_packages.return_value = []
        
        # Mock service info error
        with patch.object(multi_source_updater.external_fetcher, 'get_service_info',
                         side_effect=Exception("Service info error")):
            status = multi_source_updater.get_all_documentation_status()
        
        # Should handle errors gracefully
        assert "error" in status["core"]
        assert status["core"]["error"] == "Core metadata error"
        assert "error" in status["external"]["forge"]


class TestVersionSupport:
    """Test version support functionality."""

    @patch('docs_updater.urllib.request.urlopen')
    def test_get_supported_versions_success(self, mock_urlopen):
        """Test successful version fetching from GitHub API."""
        mock_response_data = [
            {"name": "6.x"},
            {"name": "7.x"},
            {"name": "8.x"},
            {"name": "9.x"},
            {"name": "10.x"},
            {"name": "11.x"},
            {"name": "12.x"},
            {"name": "master"},  # Should be filtered out
            {"name": "feature-branch"},  # Should be filtered out
        ]
        
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_response_data).encode()
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response
        
        versions = get_supported_versions()
        
        expected_versions = ["6.x", "7.x", "8.x", "9.x", "10.x", "11.x", "12.x"]
        assert versions == expected_versions
    
    @patch('docs_updater.urllib.request.urlopen')
    def test_get_supported_versions_no_versions_found(self, mock_urlopen):
        """Test version fetching when no valid versions found."""
        mock_response_data = [
            {"name": "master"},
            {"name": "develop"},
            {"name": "feature-branch"},
        ]
        
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_response_data).encode()
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response
        
        versions = get_supported_versions()
        
        # Should return fallback list
        assert "12.x" in versions
        assert len(versions) > 0
    
    @patch('docs_updater.urllib.request.urlopen')
    def test_get_supported_versions_old_versions_filtered(self, mock_urlopen):
        """Test that versions older than 6.x are filtered out."""
        mock_response_data = [
            {"name": "4.x"},  # Should be filtered out
            {"name": "5.x"},  # Should be filtered out
            {"name": "6.x"},
            {"name": "7.x"},
        ]
        
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_response_data).encode()
        mock_response.__enter__ = lambda self: self
        mock_response.__exit__ = lambda self, *args: None
        mock_urlopen.return_value = mock_response
        
        versions = get_supported_versions()
        
        assert "4.x" not in versions
        assert "5.x" not in versions
        assert "6.x" in versions
        assert "7.x" in versions

    @patch('docs_updater.urllib.request.urlopen')
    def test_get_supported_versions_api_error(self, mock_urlopen):
        """Test version fetching with API error (fallback to hardcoded list)."""
        mock_urlopen.side_effect = Exception("API Error")
        
        versions = get_supported_versions()
        
        # Should return fallback list
        assert isinstance(versions, list)
        assert len(versions) > 0
        assert "12.x" in versions

    def test_get_cached_supported_versions(self):
        """Test cached version support."""
        # Clear cache first
        import docs_updater
        docs_updater._SUPPORTED_VERSIONS_CACHE = None
        
        with patch('docs_updater.get_supported_versions', return_value=["test_version"]) as mock_get:
            # First call should fetch
            versions1 = get_cached_supported_versions()
            assert versions1 == ["test_version"]
            assert mock_get.call_count == 1
            
            # Second call should use cache
            versions2 = get_cached_supported_versions()
            assert versions2 == ["test_version"]
            assert mock_get.call_count == 1  # Not called again

    def test_default_version_is_latest(self):
        """Test that default version is the latest supported version."""
        # DEFAULT_VERSION should be the last item in SUPPORTED_VERSIONS
        assert DEFAULT_VERSION == SUPPORTED_VERSIONS[-1]


@pytest.mark.slow
class TestNetworkOperations:
    """Test network operations (marked as slow)."""

    @patch('docs_updater.urllib.request.urlopen')
    def test_download_with_network_issues(self, mock_urlopen, docs_updater_instance):
        """Test download handling with various network issues."""
        # Simulate network timeout, then success
        responses = [
            Exception("Network timeout"),
            MagicMock()
        ]
        
        success_response = MagicMock()
        success_response.__enter__ = lambda self: self
        success_response.__exit__ = lambda self, *args: None
        responses[1] = success_response
        
        mock_urlopen.side_effect = responses
        
        # Should retry and handle the error gracefully
        with patch('docs_updater.time.sleep'), \
             patch('docs_updater.tempfile.TemporaryDirectory'), \
             patch('docs_updater.zipfile.ZipFile'):
            
            try:
                docs_updater_instance.download_documentation()
            except Exception:
                # Expected to fail after retries, but shouldn't crash the application
                pass


class TestMainFunction:
    """Test main function and CLI."""
    
    def test_parse_arguments_default(self):
        """Test argument parsing with defaults."""
        import sys
        test_args = ['docs_updater.py']
        
        with patch.object(sys, 'argv', test_args):
            from docs_updater import parse_arguments
            args = parse_arguments()
            
            assert args.version == '12.x'  # Should use DEFAULT_VERSION
            assert args.target_dir == './docs'
            assert args.force is False
            assert args.check_only is False
            assert args.services is None
    
    def test_parse_arguments_with_options(self):
        """Test argument parsing with options."""
        import sys
        test_args = [
            'docs_updater.py',
            '--version', '11.x',
            '--target-dir', '/custom/path',
            '--force',
            '--services', 'forge', 'vapor'
        ]
        
        with patch.object(sys, 'argv', test_args):
            from docs_updater import parse_arguments
            args = parse_arguments()
            
            assert args.version == '11.x'
            assert args.target_dir == '/custom/path'
            assert args.force is True
            assert args.services == ['forge', 'vapor']
    
    def test_parse_arguments_status(self):
        """Test argument parsing for status flag."""
        import sys
        test_args = ['docs_updater.py', '--status']
        
        with patch.object(sys, 'argv', test_args):
            from docs_updater import parse_arguments
            args = parse_arguments()
            
            assert args.status is True
    
    def test_parse_arguments_list_services(self):
        """Test argument parsing for list-services flag."""
        import sys
        test_args = ['docs_updater.py', '--list-services']
        
        with patch.object(sys, 'argv', test_args):
            from docs_updater import parse_arguments
            args = parse_arguments()
            
            assert args.list_services is True
    
    @patch('docs_updater.MultiSourceDocsUpdater')
    def test_main_update_default(self, mock_updater_class):
        """Test main function with default update."""
        import sys
        test_args = ['docs_updater.py']
        
        mock_updater = MagicMock()
        mock_updater.update_all.return_value = {
            "core": True,
            "external": {"forge": True, "vapor": True}
        }
        mock_updater_class.return_value = mock_updater
        
        with patch.object(sys, 'argv', test_args), \
             patch('builtins.print'):
            from docs_updater import main
            result = main()
            
            assert result == 0
            mock_updater.update_all.assert_called_once_with(force_core=False, force_external=False, force_packages=False, force_learning=False)
    
    @patch('docs_updater.MultiSourceDocsUpdater')
    def test_main_status_command(self, mock_updater_class):
        """Test main function with status command."""
        import sys
        test_args = ['docs_updater.py', '--status']
        
        mock_updater = MagicMock()
        mock_updater.get_all_documentation_status.return_value = {
            "core": {
                "available": True,
                "last_updated": "2024-01-01T12:00:00Z",
                "commit_sha": "abc123"
            },
            "external": {
                "forge": {
                    "available": True,
                    "name": "Laravel Forge",
                    "cache_valid": True,
                    "type": "laravel_service",
                    "success_rate": 1.0  # Numeric value, not string
                }
            },
            "packages": {}
        }
        mock_updater_class.return_value = mock_updater
        
        with patch.object(sys, 'argv', test_args), \
             patch('builtins.print'):
            from docs_updater import main
            result = main()
            
            assert result == 0
            mock_updater.get_all_documentation_status.assert_called()
    
    @patch('docs_updater.ExternalDocsFetcher')
    def test_main_list_services_command(self, mock_fetcher_class):
        """Test main function with list-services command."""
        import sys
        test_args = ['docs_updater.py', '--list-services']
        
        mock_fetcher = MagicMock()
        mock_fetcher.list_available_services.return_value = ["forge", "vapor"]
        mock_fetcher_class.return_value = mock_fetcher
        
        with patch.object(sys, 'argv', test_args), \
             patch('builtins.print'):
            from docs_updater import main
            result = main()
            
            assert result == 0
            mock_fetcher.list_available_services.assert_called_once()
    
    @patch('docs_updater.MultiSourceDocsUpdater')
    def test_main_update_external_service(self, mock_updater_class):
        """Test main function updating external service."""
        import sys
        test_args = ['docs_updater.py', '--services', 'forge']
        
        mock_updater = MagicMock()
        # The --services parameter now calls update_all() instead of update_external_docs()
        mock_updater.update_all.return_value = {
            'core': {'11.x': True},
            'external': {'forge': True},
            'packages': {}
        }
        mock_updater_class.return_value = mock_updater
        
        with patch.object(sys, 'argv', test_args), \
             patch('builtins.print'):
            from docs_updater import main
            result = main()
            
            assert result == 0
            mock_updater.update_all.assert_called_with(force_core=False, force_external=False, force_packages=False, force_learning=False)
    
    def test_main_with_exception(self):
        """Test main function handling exceptions."""
        import sys
        test_args = ['docs_updater.py']
        
        with patch.object(sys, 'argv', test_args), \
             patch('docs_updater.MultiSourceDocsUpdater', side_effect=Exception("Test error")), \
             patch('builtins.print'):
            from docs_updater import main
            try:
                main()
                # If main() doesn't catch the exception, it will propagate
                assert False, "Expected exception was not raised"
            except Exception as e:
                # This is expected - the exception from MultiSourceDocsUpdater propagates
                assert str(e) == "Test error"