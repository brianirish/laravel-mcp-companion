"""Tests for asset file filtering in documentation fetching."""
from docs_updater import DocumentationAutoDiscovery


class TestAssetFiltering:
    """Test that asset files are properly filtered during documentation discovery."""
    
    def test_is_asset_file_with_extensions(self):
        """Test that common asset file extensions are detected."""
        discovery = DocumentationAutoDiscovery()
        
        # CSS files with and without query parameters
        assert discovery._is_asset_file('/docs/style.css')
        assert discovery._is_asset_file('/docs/style.css?v=123')
        assert discovery._is_asset_file('/docs/style.css?dpl=dpl_ADXvxQy4mwn4NXij5CJr1F1vi76Z')
        
        # JavaScript files
        assert discovery._is_asset_file('/docs/app.js')
        assert discovery._is_asset_file('/docs/app.min.js')
        assert discovery._is_asset_file('/docs/app.js?v=1.2.3')
        
        # Image files
        assert discovery._is_asset_file('/docs/logo.png')
        assert discovery._is_asset_file('/docs/banner.jpg')
        assert discovery._is_asset_file('/docs/icon.svg')
        assert discovery._is_asset_file('/docs/photo.jpeg')
        assert discovery._is_asset_file('/docs/animation.gif')
        
        # Font files
        assert discovery._is_asset_file('/docs/font.woff')
        assert discovery._is_asset_file('/docs/font.woff2')
        assert discovery._is_asset_file('/docs/font.ttf')
        assert discovery._is_asset_file('/docs/font.eot')
        
        # Icon files
        assert discovery._is_asset_file('/docs/favicon.ico')
    
    def test_is_asset_file_with_patterns(self):
        """Test that common asset directory patterns are detected."""
        discovery = DocumentationAutoDiscovery()
        
        # Next.js static files
        assert discovery._is_asset_file('/docs/_next/static/css/style.css')
        assert discovery._is_asset_file('/docs/_next/static/js/app.js')
        assert discovery._is_asset_file('/_next/data/build.json')
        
        # Static directories
        assert discovery._is_asset_file('/static/css/main.css')
        assert discovery._is_asset_file('/docs/static/images/logo.png')
        
        # Assets directories
        assert discovery._is_asset_file('/assets/styles/theme.css')
        assert discovery._is_asset_file('/docs/assets/js/bundle.js')
        
        # Images directories
        assert discovery._is_asset_file('/images/header.jpg')
        assert discovery._is_asset_file('/docs/images/screenshot.png')
        
        # Fonts directories
        assert discovery._is_asset_file('/fonts/roboto.woff2')
        assert discovery._is_asset_file('/docs/fonts/arial.ttf')
        
        # Favicon
        assert discovery._is_asset_file('/favicon.ico')
        assert discovery._is_asset_file('/favicon-32x32.png')
    
    def test_is_not_asset_file(self):
        """Test that documentation files are not detected as assets."""
        discovery = DocumentationAutoDiscovery()
        
        # Documentation paths
        assert not discovery._is_asset_file('/docs/introduction')
        assert not discovery._is_asset_file('/docs/getting-started')
        assert not discovery._is_asset_file('/docs/servers/management')
        assert not discovery._is_asset_file('/docs/sites/ssl')
        
        # Even with query parameters
        assert not discovery._is_asset_file('/docs/authentication?section=api')
        assert not discovery._is_asset_file('/docs/database?v=latest')
        
        # Markdown files (should be allowed)
        assert not discovery._is_asset_file('/docs/readme.md')
        assert not discovery._is_asset_file('/docs/guide.markdown')
    
    def test_case_insensitive_detection(self):
        """Test that asset detection is case-insensitive."""
        discovery = DocumentationAutoDiscovery()
        
        # Uppercase extensions
        assert discovery._is_asset_file('/docs/STYLE.CSS')
        assert discovery._is_asset_file('/docs/APP.JS')
        assert discovery._is_asset_file('/docs/LOGO.PNG')
        
        # Mixed case
        assert discovery._is_asset_file('/docs/Style.Css')
        assert discovery._is_asset_file('/docs/App.Js')
        
        # Uppercase patterns
        assert discovery._is_asset_file('/STATIC/style.css')
        assert discovery._is_asset_file('/_NEXT/static/css/main.css')
        assert discovery._is_asset_file('/ASSETS/logo.png')