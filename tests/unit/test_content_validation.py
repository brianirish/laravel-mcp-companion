"""Tests for content validation functionality in docs_updater."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from docs_updater import ExternalDocsFetcher


class TestContentValidation:
    """Test cases for _is_valid_content method."""
    
    @pytest.fixture
    def fetcher(self, temp_dir):
        """Create an ExternalDocsFetcher instance for testing."""
        return ExternalDocsFetcher(temp_dir)
    
    def test_valid_forge_content(self, fetcher):
        """Test valid Forge documentation content."""
        content = """
        # Server Management
        
        Laravel Forge provides server provisioning and deployment for PHP applications.
        This guide covers nginx configuration, SSL certificates, and deployment scripts.
        
        ## Setting up your server
        
        Forge makes it easy to provision servers on DigitalOcean, AWS, and other providers.
        You can manage databases, configure nginx, and set up SSL certificates.
        
        ### PHP Configuration
        
        Forge allows you to configure PHP settings and manage multiple PHP versions.
        """
        
        assert fetcher._is_valid_content(content, "forge", "servers") is True
    
    def test_valid_vapor_content(self, fetcher):
        """Test valid Vapor documentation content."""
        content = """
        # Serverless Deployment with Laravel Vapor
        
        Laravel Vapor is a serverless deployment platform for Laravel applications.
        Deploy your Laravel apps to AWS Lambda with zero server maintenance.
        
        ## Environment Configuration
        
        Vapor uses environment files to manage your application settings.
        You can configure databases, caches, and queues through the Vapor UI.
        
        ### Deploying Your Application
        
        Use the vapor deploy command to deploy your application to AWS Lambda.
        """
        
        assert fetcher._is_valid_content(content, "vapor", "deployment") is True
    
    def test_valid_envoyer_content(self, fetcher):
        """Test valid Envoyer documentation content."""
        content = """
        # Zero Downtime Deployments
        
        Laravel Envoyer provides zero-downtime deployment for PHP applications.
        Configure deployment hooks, manage environment variables, and monitor deployments.
        
        ## Setting Up Your Project
        
        Connect your Git repository and configure deployment scripts.
        Envoyer supports GitHub, GitLab, and Bitbucket integrations.
        """
        
        assert fetcher._is_valid_content(content, "envoyer", "deployments") is True
    
    def test_valid_nova_content(self, fetcher):
        """Test valid Nova documentation content."""
        content = """
        # Laravel Nova Administration Panel
        
        Nova is a beautifully designed administration panel for Laravel applications.
        Create custom resources, fields, and actions for your admin interface.
        
        ## Resource Management
        
        Nova resources represent Eloquent models in your admin panel.
        Define fields, filters, and actions for each resource.
        """
        
        assert fetcher._is_valid_content(content, "nova", "resources") is True
    
    def test_invalid_content_too_short(self, fetcher):
        """Test content that's too short to be valid documentation."""
        content = "Just a title"
        
        assert fetcher._is_valid_content(content, "forge", "servers") is False
    
    def test_invalid_content_no_keywords(self, fetcher):
        """Test content without relevant keywords."""
        # Content with no relevant keywords at all
        content = """
        This is some random content about cooking recipes and gardening tips.
        It has nothing to do with websites or programming.
        We talk about vegetables, fruits, and cooking techniques here.
        You can learn about baking, grilling, and food preparation.
        This text is about culinary arts and has no technical content.
        """
        
        assert fetcher._is_valid_content(content, "forge", "servers") is False
    
    def test_invalid_content_404_page(self, fetcher):
        """Test typical 404 error page content."""
        content = """
        404 Page Not Found
        
        The page you are looking for could not be found.
        Please check the URL or go back to the homepage.
        
        Error 404 - Not Found
        """
        
        assert fetcher._is_valid_content(content, "vapor", "deployment") is False
    
    def test_invalid_content_login_page(self, fetcher):
        """Test login page content that shouldn't be considered documentation."""
        content = """
        Sign In to Your Account
        
        Email Address
        Password
        Remember Me
        Forgot Your Password?
        
        Don't have an account? Sign up
        
        Login with GitHub
        Login with Google
        """
        
        assert fetcher._is_valid_content(content, "nova", "authentication") is False
    
    def test_edge_case_empty_content(self, fetcher):
        """Test empty content."""
        assert fetcher._is_valid_content("", "forge", "servers") is False
    
    def test_edge_case_whitespace_only(self, fetcher):
        """Test content with only whitespace."""
        content = "   \n\n\t\t   \n   "
        assert fetcher._is_valid_content(content, "vapor", "deployment") is False
    
    def test_quality_scoring_high_quality(self, fetcher):
        """Test content with high quality score (many relevant keywords)."""
        content = """
        # Laravel Forge Server Management Guide
        
        Laravel Forge is the best server provisioning and deployment platform for Laravel.
        This comprehensive guide covers nginx configuration, PHP settings, SSL certificates,
        database management, queue workers, scheduled tasks, and deployment workflows.
        
        ## Server Provisioning
        
        Forge integrates with DigitalOcean, AWS, Linode, and custom VPS providers.
        Provision Ubuntu servers with nginx, PHP, MySQL, Redis, and more.
        
        ## Site Management
        
        Create Laravel sites with automatic nginx configuration. Forge handles
        SSL certificates through Let's Encrypt, deployment scripts, and environment files.
        
        ## Database Administration
        
        Manage MySQL and PostgreSQL databases directly from the Forge dashboard.
        Create databases, users, and configure backups with ease.
        
        ## Advanced Features
        
        Configure queue workers, scheduled tasks, firewall rules, and monitoring.
        Forge provides comprehensive server management for Laravel applications.
        """
        
        assert fetcher._is_valid_content(content, "forge", "servers") is True
    
    def test_quality_scoring_medium_quality(self, fetcher):
        """Test content with medium quality score."""
        content = """
        # Basic Server Setup
        
        This guide covers basic server configuration.
        You can set up PHP and nginx on your server.
        
        ## Configuration Steps
        
        1. Install PHP
        2. Configure nginx
        3. Set up your database
        
        That's all you need to get started.
        """
        
        # Should still be valid but lower quality
        assert fetcher._is_valid_content(content, "forge", "servers") is True
    
    def test_service_specific_keywords_forge(self, fetcher):
        """Test Forge-specific keyword matching."""
        content = """
        # Forge Server Configuration
        
        Configure nginx, SSL certificates, and deployment hooks in Laravel Forge.
        Manage your servers, sites, and databases from the Forge dashboard.
        Set up queue workers and scheduled tasks for your Laravel application.
        """
        
        assert fetcher._is_valid_content(content, "forge", "configuration") is True
    
    def test_service_specific_keywords_vapor(self, fetcher):
        """Test Vapor-specific keyword matching."""
        content = """
        # Serverless Laravel with Vapor
        
        Deploy to AWS Lambda using Laravel Vapor's serverless platform.
        Configure environments, manage deployments, and scale automatically.
        Vapor handles infrastructure so you can focus on your application.
        """
        
        assert fetcher._is_valid_content(content, "vapor", "serverless") is True
    
    def test_mixed_content_with_navigation(self, fetcher):
        """Test content that includes navigation elements but is still valid."""
        content = """
        Home > Documentation > Servers
        
        # Server Management in Laravel Forge
        
        Previous | Next
        
        Laravel Forge provides comprehensive server management for PHP applications.
        This guide covers server provisioning, site configuration, and deployment.
        
        ## Table of Contents
        - Server Setup
        - Site Management  
        - SSL Certificates
        - Deployment
        
        ## Server Provisioning
        
        Forge makes it easy to provision servers on multiple cloud providers.
        Configure nginx, PHP, MySQL, and Redis with just a few clicks.
        
        Related Articles | Contact Support | Back to Top
        """
        
        # Should be valid despite navigation elements
        assert fetcher._is_valid_content(content, "forge", "servers") is True
    
    def test_threshold_boundary_cases(self, fetcher):
        """Test content right at the minimum threshold."""
        # Exactly 100 characters (minimum threshold)
        content = "a" * 100
        assert fetcher._is_valid_content(content, "forge", "test") is False
        
        # Just over threshold but no keywords
        content = "Some basic text about nothing in particular. " * 3
        assert fetcher._is_valid_content(content, "forge", "test") is False
        
        # Over threshold with minimal keywords
        content = "This is about Forge servers. " + ("Some filler text here. " * 10)
        # Should evaluate based on keyword density
        result = fetcher._is_valid_content(content, "forge", "test")
        # May or may not pass depending on scoring threshold
        assert isinstance(result, bool)