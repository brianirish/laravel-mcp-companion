#!/usr/bin/env python3
"""
Content Aggregators for Laravel Learning Resources.

This module provides aggregators for various Laravel content sources including
Laravel News, Spatie Blog, Laracasts, Laravel Bootcamp, and conference talks.
"""

import feedparser
import requests
import json
import logging
import re
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any, Tuple
from pathlib import Path
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse, parse_qs, urlparse
import os

from learning_resources import (
    LearningResourceFetcher,
    ResourceType,
    ResourceSource,
    DifficultyLevel,
    ResourceMetadata
)

logger = logging.getLogger("laravel-content-aggregators")


class LaravelNewsAggregator:
    """Aggregator for Laravel News articles and tutorials."""
    
    RSS_FEED_URL = "https://laravel-news.com/feed"
    BASE_URL = "https://laravel-news.com"
    BLOG_URL = "https://laravel-news.com/blog"
    
    # Category URLs for specific content types
    CATEGORY_URLS = {
        'tutorials': 'https://laravel-news.com/category/tutorials',
        'packages': 'https://laravel-news.com/category/packages',
    }
    
    def __init__(self, resource_fetcher: LearningResourceFetcher):
        """Initialize with resource fetcher."""
        self.fetcher = resource_fetcher
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; LaravelMCPCompanion/1.0; +https://github.com/brianirish/laravel-mcp-companion)'
        })
        logger.info("Initialized LaravelNewsAggregator")
    
    def fetch_articles(self, limit: int = 50) -> List[int]:
        """Fetch recent articles from Laravel News RSS feed."""
        try:
            logger.info(f"Fetching Laravel News RSS feed: {self.RSS_FEED_URL}")
            feed = feedparser.parse(self.RSS_FEED_URL)
            
            if feed.bozo:
                logger.error(f"Error parsing RSS feed: {feed.bozo_exception}")
                return []
            
            added_resources = []
            
            for entry in feed.entries[:limit]:
                try:
                    # Extract article metadata
                    title = entry.get('title', 'Untitled')
                    url = entry.get('link', '')
                    description = entry.get('summary', '')
                    
                    # Parse publication date
                    published_date = None
                    if hasattr(entry, 'published_parsed'):
                        published_date = datetime.fromtimestamp(
                            time.mktime(entry.published_parsed),
                            tz=timezone.utc
                        )
                    
                    # Extract tags from categories
                    tags = []
                    if hasattr(entry, 'tags'):
                        tags = [tag['term'].lower() for tag in entry.tags]
                    
                    # Determine resource type based on title and tags
                    resource_type = self._determine_resource_type(title, tags)
                    
                    # Estimate difficulty based on content
                    difficulty = self._estimate_difficulty(title, description, tags)
                    
                    # Additional metadata
                    metadata = {
                        'author': entry.get('author', 'Laravel News Team'),
                        'guid': entry.get('id', url)
                    }
                    
                    # Add resource to database
                    resource_id = self.fetcher.add_resource(
                        title=title,
                        url=url,
                        resource_type=resource_type,
                        source=ResourceSource.LARAVEL_NEWS,
                        description=self._clean_description(description),
                        difficulty=difficulty,
                        tags=tags,
                        published_date=published_date,
                        metadata=metadata
                    )
                    
                    added_resources.append(resource_id)
                    logger.info(f"Added Laravel News article: {title}")
                    
                except Exception as e:
                    logger.error(f"Error processing article: {e}")
                    continue
            
            logger.info(f"Successfully fetched {len(added_resources)} articles from Laravel News")
            return added_resources
            
        except Exception as e:
            logger.error(f"Error fetching Laravel News feed: {e}")
            return []
    
    def fetch_historical_articles(
        self, 
        start_page: int = 1, 
        max_pages: int = 10,
        category: Optional[str] = None,
        delay_between_pages: float = 1.0
    ) -> List[int]:
        """
        Fetch historical articles from Laravel News by scraping paginated pages.
        
        Args:
            start_page: Starting page number (default 1)
            max_pages: Maximum number of pages to fetch (default 10)
            category: Optional category to filter ('tutorials', 'packages', None for all)
            delay_between_pages: Delay in seconds between page requests (default 1.0)
            
        Returns:
            List of added resource IDs
        """
        added_resources = []
        processed_urls = set()  # Track URLs to avoid duplicates
        
        # Determine base URL based on category
        if category and category in self.CATEGORY_URLS:
            base_url = self.CATEGORY_URLS[category]
            logger.info(f"Fetching from category: {category}")
        else:
            base_url = self.BLOG_URL
            logger.info("Fetching from all blog posts")
        
        for page_num in range(start_page, start_page + max_pages):
            try:
                # Construct URL with pagination
                url = f"{base_url}?page={page_num}"
                logger.info(f"Fetching page {page_num}: {url}")
                
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find article containers - Laravel News uses a grid layout
                articles = soup.find_all('div', class_=re.compile(r'(flex|grid)'))
                
                articles_found = 0
                for article in articles:
                    # Look for article links within the container
                    link_elem = article.find('a', href=re.compile(r'^https://laravel-news\.com/[^/]+$'))
                    if not link_elem:
                        continue
                    
                    article_url = link_elem.get('href', '')
                    
                    # Skip if already processed
                    if article_url in processed_urls:
                        continue
                    processed_urls.add(article_url)
                    
                    # Extract article data
                    title_elem = article.find(['h3', 'h2'])
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    # Get description
                    desc_elem = article.find('p')
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # Skip if not Laravel-related (though most should be)
                    if not self._is_laravel_related(title, description):
                        continue
                    
                    # Determine resource type and tags
                    tags = []
                    if category:
                        tags.append(category)
                    
                    # Check URL patterns for additional categorization
                    if 'package' in article_url or 'packages' in title.lower():
                        tags.append('packages')
                        resource_type = ResourceType.PACKAGE
                    elif category == 'tutorials' or 'tutorial' in title.lower():
                        resource_type = ResourceType.TUTORIAL
                    else:
                        resource_type = self._determine_resource_type(title, tags)
                    
                    # Extract more tags from title and description
                    additional_tags = self._extract_tags_from_content(title, description)
                    tags.extend([tag for tag in additional_tags if tag not in tags])
                    
                    # Estimate difficulty
                    difficulty = self._estimate_difficulty(title, description, tags)
                    
                    # Additional metadata
                    metadata = {
                        'author': 'Laravel News Team',
                        'fetched_from_page': page_num,
                        'category': category or 'general'
                    }
                    
                    # Add resource
                    try:
                        resource_id = self.fetcher.add_resource(
                            title=title,
                            url=article_url,
                            resource_type=resource_type,
                            source=ResourceSource.LARAVEL_NEWS,
                            description=description,
                            difficulty=difficulty,
                            tags=tags,
                            published_date=None,  # Historical scraping doesn't easily get dates
                            metadata=metadata
                        )
                        
                        added_resources.append(resource_id)
                        articles_found += 1
                        logger.info(f"Added Laravel News article: {title}")
                        
                    except Exception as e:
                        logger.error(f"Error adding article '{title}': {e}")
                        continue
                
                logger.info(f"Found {articles_found} articles on page {page_num}")
                
                # Check if we should continue (no Next button means last page)
                next_button = soup.find('button', string=re.compile(r'Next'))
                if not next_button or next_button.get('disabled'):
                    logger.info("Reached last page, stopping pagination")
                    break
                
                # Rate limiting
                time.sleep(delay_between_pages)
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching page {page_num}: {e}")
                # Continue to next page on network errors
                continue
            except Exception as e:
                logger.error(f"Unexpected error on page {page_num}: {e}")
                # Continue to next page on other errors
                continue
        
        logger.info(f"Successfully fetched {len(added_resources)} historical articles")
        return added_resources
    
    def fetch_articles_by_tag(self, tag: str, max_pages: int = 5) -> List[int]:
        """
        Fetch articles by specific tag from Laravel News.
        
        Args:
            tag: Tag name to search for
            max_pages: Maximum pages to fetch
            
        Returns:
            List of added resource IDs
        """
        tag_url = f"{self.BASE_URL}/tag/{tag}"
        added_resources = []
        
        for page_num in range(1, max_pages + 1):
            try:
                url = f"{tag_url}?page={page_num}" if page_num > 1 else tag_url
                logger.info(f"Fetching tag '{tag}' page {page_num}: {url}")
                
                response = self.session.get(url, timeout=10)
                if response.status_code == 404:
                    logger.warning(f"Tag '{tag}' not found")
                    break
                response.raise_for_status()
                
                # Parse and extract articles similar to fetch_historical_articles
                # ... (implementation similar to above)
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Error fetching tag '{tag}' page {page_num}: {e}")
                continue
        
        return added_resources
    
    def _is_laravel_related(self, title: str, description: str) -> bool:
        """Check if content is Laravel-related."""
        # On Laravel News, most content is Laravel-related
        # But we can still filter out some edge cases
        text = f"{title} {description}".lower()
        
        # Exclude certain non-Laravel content
        exclude_keywords = ['wordpress', 'drupal', 'symfony-only', 'django']
        if any(keyword in text for keyword in exclude_keywords):
            # Check if Laravel is also mentioned
            if 'laravel' not in text:
                return False
        
        return True
    
    def _extract_tags_from_content(self, title: str, description: str) -> List[str]:
        """Extract relevant tags from article content."""
        text = f"{title} {description}".lower()
        
        # Common Laravel-related tags to look for
        tag_patterns = {
            'eloquent': r'\beloquent\b',
            'blade': r'\bblade\b',
            'livewire': r'\blivewire\b',
            'inertia': r'\binertia\b',
            'pest': r'\bpest\b',
            'sail': r'\bsail\b',
            'vapor': r'\bvapor\b',
            'forge': r'\bforge\b',
            'nova': r'\bnova\b',
            'horizon': r'\bhorizon\b',
            'telescope': r'\btelescope\b',
            'sanctum': r'\bsanctum\b',
            'passport': r'\bpassport\b',
            'broadcasting': r'\bbroadcast\w*\b',
            'queues': r'\bqueue\w*\b',
            'testing': r'\b(test|testing|phpunit|pest)\b',
            'api': r'\b(api|rest|graphql)\b',
            'authentication': r'\b(auth|authentication)\b',
            'deployment': r'\b(deploy|deployment)\b',
            'docker': r'\bdocker\b',
            'vue': r'\bvue\b',
            'react': r'\breact\b',
            'alpine': r'\balpine\b',
            'tailwind': r'\btailwind\b',
        }
        
        tags = []
        for tag, pattern in tag_patterns.items():
            if re.search(pattern, text):
                tags.append(tag)
        
        return tags
    
    def _determine_resource_type(self, title: str, tags: List[str]) -> ResourceType:
        """Determine the type of resource based on title and tags."""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['tutorial', 'how to', 'guide', 'build']):
            return ResourceType.TUTORIAL
        elif any(word in title_lower for word in ['video', 'screencast', 'episode']):
            return ResourceType.VIDEO
        elif any(word in title_lower for word in ['course', 'series', 'bootcamp']):
            return ResourceType.COURSE
        elif any(word in title_lower for word in ['podcast', 'interview']):
            return ResourceType.PODCAST
        else:
            return ResourceType.ARTICLE
    
    def _estimate_difficulty(
        self,
        title: str,
        description: str,
        tags: List[str]
    ) -> Optional[DifficultyLevel]:
        """Estimate difficulty level based on content analysis."""
        text = f"{title} {description} {' '.join(tags)}".lower()
        
        # Beginner indicators
        beginner_keywords = [
            'beginner', 'getting started', 'introduction', 'basics',
            'first', 'simple', 'easy', 'newbie', 'starter'
        ]
        
        # Advanced indicators
        advanced_keywords = [
            'advanced', 'expert', 'complex', 'deep dive', 'optimization',
            'performance', 'scaling', 'architecture', 'design patterns'
        ]
        
        # Expert indicators
        expert_keywords = [
            'internals', 'under the hood', 'core', 'custom driver',
            'extending framework', 'contributing'
        ]
        
        beginner_score = sum(1 for keyword in beginner_keywords if keyword in text)
        advanced_score = sum(1 for keyword in advanced_keywords if keyword in text)
        expert_score = sum(1 for keyword in expert_keywords if keyword in text)
        
        if expert_score > 0:
            return DifficultyLevel.EXPERT
        elif advanced_score > beginner_score:
            return DifficultyLevel.ADVANCED
        elif beginner_score > 0:
            return DifficultyLevel.BEGINNER
        else:
            return DifficultyLevel.INTERMEDIATE
    
    def _clean_description(self, description: str) -> str:
        """Clean HTML from description."""
        if not description:
            return ""
        
        # Remove HTML tags
        soup = BeautifulSoup(description, 'html.parser')
        text = soup.get_text()
        
        # Clean up whitespace
        text = ' '.join(text.split())
        
        # Limit length
        if len(text) > 500:
            text = text[:497] + "..."
        
        return text


class SpatieBlogAggregator:
    """Aggregator for Spatie blog Laravel tutorials."""
    
    BASE_URL = "https://spatie.be"
    BLOG_URL = "https://spatie.be/blog"
    
    def __init__(self, resource_fetcher: LearningResourceFetcher):
        """Initialize with resource fetcher."""
        self.fetcher = resource_fetcher
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; LaravelMCPCompanion/1.0; +https://github.com/brianirish/laravel-mcp-companion)'
        })
        logger.info("Initialized SpatieBlogAggregator")
    
    def fetch_tutorials(self, pages: int = 1) -> List[int]:
        """Fetch Laravel tutorials from Spatie blog."""
        added_resources = []
        processed_urls = set()  # Track processed URLs to avoid duplicates
        
        # Note: Spatie blog doesn't have traditional pagination for blog posts
        # Page 2+ shows team member content, so we only fetch the main page
        try:
            logger.info(f"Fetching Spatie blog: {self.BLOG_URL}")
            
            response = self.session.get(self.BLOG_URL, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the main featured article first
            featured_article = soup.find('article')
            if featured_article:
                self._process_featured_article(featured_article, added_resources, processed_urls)
            
            # Find "More posts" section
            more_posts_container = soup.find('div', class_='grid') or soup.find_all('div', recursive=True)
            
            # Look for article links in the more posts section
            # First, collect all unique h3 links
            for heading in soup.find_all('h3'):
                link = heading.find('a')
                if link:
                    href = link.get('href', '')
                    if '/blog/' in href and href not in processed_urls:
                        # Find the parent container that has the full context
                        container = heading.parent
                        while container and container.name not in ['div', 'article']:
                            container = container.parent
                        if container:
                            self._process_blog_post_link(link, container, added_resources, processed_urls)
            
        except Exception as e:
            logger.error(f"Error fetching Spatie blog: {e}")
        
        logger.info(f"Successfully fetched {len(added_resources)} tutorials from Spatie blog")
        return added_resources
    
    def _process_featured_article(self, article: BeautifulSoup, added_resources: List[int], processed_urls: set):
        """Process the featured article on the main page."""
        try:
            # Find the main link
            main_link = article.find('a')
            if not main_link:
                return
            
            href = main_link.get('href', '')
            if not ('/blog/' in href or href.startswith('/blog/')):
                return
            
            article_url = href if href.startswith('http') else urljoin(self.BASE_URL, href)
            
            # Skip if already processed
            if article_url in processed_urls:
                return
            processed_urls.add(article_url)
            
            # Extract title from h2
            title_elem = article.find('h2')
            if not title_elem:
                return
            
            title = title_elem.get_text(strip=True)
            
            # Get description from paragraph
            desc_elem = article.find('p')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Skip if not Laravel-related
            if not self._is_laravel_related(title, description):
                return
            
            # Get publication date
            time_elem = article.find('time')
            published_date = None
            if time_elem:
                date_text = time_elem.get_text(strip=True)
                published_date = self._parse_date(date_text)
            
            # Extract tags
            tags = self._extract_tags(title, description)
            
            # Additional metadata
            metadata = {
                'author': 'Spatie Team',
                'company': 'Spatie',
                'featured': True
            }
            
            # Add resource
            resource_id = self.fetcher.add_resource(
                title=title,
                url=article_url,
                resource_type=ResourceType.TUTORIAL,
                source=ResourceSource.SPATIE_BLOG,
                description=description,
                difficulty=DifficultyLevel.INTERMEDIATE,
                tags=tags,
                published_date=published_date,
                metadata=metadata
            )
            
            added_resources.append(resource_id)
            logger.info(f"Added Spatie featured tutorial: {title}")
            
        except Exception as e:
            logger.error(f"Error processing featured article: {e}")
    
    def _process_blog_post_link(self, link: BeautifulSoup, container: BeautifulSoup, added_resources: List[int], processed_urls: set):
        """Process a blog post link from the more posts section."""
        try:
            href = link.get('href', '')
            article_url = href if href.startswith('http') else urljoin(self.BASE_URL, href)
            
            # Skip if already processed
            if article_url in processed_urls:
                return
            processed_urls.add(article_url)
            
            title = link.get_text(strip=True)
            
            # Skip if not Laravel-related
            if not self._is_laravel_related(title, ""):
                return
            
            # Try to find description - usually in a sibling paragraph
            description = ""
            parent = link.parent
            if parent:
                # Look for following paragraphs
                next_elem = parent.find_next_sibling(['p', 'div'])
                if next_elem and next_elem.name == 'p':
                    description = next_elem.get_text(strip=True)
                # Also check within the parent for any p tags
                desc_elem = parent.find('p')
                if desc_elem and not description:
                    description = desc_elem.get_text(strip=True)
            
            # Look for date
            published_date = None
            time_elem = container.find('time')
            if time_elem:
                date_text = time_elem.get_text(strip=True)
                published_date = self._parse_date(date_text)
            
            # Look for tags (like #OSS)
            tags = self._extract_tags(title, description)
            tag_elem = container.find('ul') or container.find(string=re.compile(r'#\w+'))
            if tag_elem:
                if isinstance(tag_elem, str):
                    tag_matches = re.findall(r'#(\w+)', tag_elem)
                    tags.extend([t.lower() for t in tag_matches])
                else:
                    for li in tag_elem.find_all('li'):
                        tag_text = li.get_text(strip=True).lstrip('#').lower()
                        if tag_text and tag_text not in tags:
                            tags.append(tag_text)
            
            # Additional metadata
            metadata = {
                'author': 'Spatie Team',
                'company': 'Spatie'
            }
            
            # Add resource
            resource_id = self.fetcher.add_resource(
                title=title,
                url=article_url,
                resource_type=ResourceType.TUTORIAL,
                source=ResourceSource.SPATIE_BLOG,
                description=description,
                difficulty=DifficultyLevel.INTERMEDIATE,
                tags=tags,
                published_date=published_date,
                metadata=metadata
            )
            
            added_resources.append(resource_id)
            logger.info(f"Added Spatie tutorial: {title}")
            
        except Exception as e:
            logger.error(f"Error processing blog post link: {e}")
    
    def _is_laravel_related(self, title: str, description: str) -> bool:
        """Check if a post is Laravel-related."""
        text = f"{title} {description}".lower()
        
        # Laravel-specific keywords
        laravel_keywords = [
            'laravel', 'eloquent', 'blade', 'artisan', 'livewire', 'inertia',
            'pest', 'phpunit', 'composer', 'package', 'spatie/laravel',
            'validation', 'middleware', 'controller', 'migration',
            'model', 'route', 'view', 'queue', 'job', 'event',
            'notification', 'mail', 'broadcasting', 'cache', 'session',
            'authentication', 'authorization', 'api', 'sanctum', 'passport',
            'horizon', 'telescope', 'dusk', 'sail', 'valet', 'homestead',
            'mix', 'vite', 'tailwind', 'alpine', 'laravel-'
        ]
        
        return any(keyword in text for keyword in laravel_keywords)
    
    def _parse_date(self, date_text: str) -> Optional[datetime]:
        """Parse date from various formats."""
        try:
            # Try parsing "Month DD, YYYY" format
            return datetime.strptime(date_text, "%B %d, %Y").replace(tzinfo=timezone.utc)
        except ValueError:
            try:
                # Try parsing "July 24, 2025" format
                return datetime.strptime(date_text, "%B %d, %Y").replace(tzinfo=timezone.utc)
            except ValueError:
                logger.warning(f"Could not parse date: {date_text}")
                return None
    
    def _extract_tags(self, title: str, description: str) -> List[str]:
        """Extract relevant tags from content."""
        text = f"{title} {description}".lower()
        
        # Common Laravel-related tags to look for
        tag_patterns = {
            'eloquent': r'\beloquent\b',
            'authentication': r'\b(auth|authentication|login)\b',
            'testing': r'\b(test|testing|phpunit|pest)\b',
            'api': r'\b(api|rest|restful)\b',
            'validation': r'\bvalidat\w+\b',
            'middleware': r'\bmiddleware\b',
            'queue': r'\b(queue|job|worker)\b',
            'database': r'\b(database|migration|schema)\b',
            'performance': r'\b(performance|optimization|speed)\b',
            'security': r'\b(security|secure|csrf|xss)\b',
            'deployment': r'\b(deploy|deployment|production)\b',
            'package-development': r'\b(package|composer)\b',
            'vue': r'\bvue\b',
            'livewire': r'\blivewire\b',
            'inertia': r'\binertia\b',
            'tailwind': r'\btailwind\b'
        }
        
        tags = []
        for tag, pattern in tag_patterns.items():
            if re.search(pattern, text):
                tags.append(tag)
        
        # Always add 'laravel' tag
        if 'laravel' not in tags:
            tags.append('laravel')
        
        return tags


class LaracastsAggregator:
    """Aggregator for Laracasts Laravel tutorial series and lessons."""
    
    BASE_URL = "https://laracasts.com"
    SERIES_URL = "https://laracasts.com/series"
    LARAVEL_TOPIC_URL = "https://laracasts.com/series?topics%5B%5D=laravel"
    
    def __init__(self, resource_fetcher: LearningResourceFetcher):
        """Initialize with resource fetcher."""
        self.fetcher = resource_fetcher
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; LaravelMCPCompanion/1.0; +https://github.com/brianirish/laravel-mcp-companion)'
        })
        logger.info("Initialized LaracastsAggregator")
    
    def fetch_laravel_series(self, max_pages: int = 3) -> List[int]:
        """
        Fetch Laravel tutorial series from Laracasts.
        
        Args:
            max_pages: Maximum number of pages to fetch (default 3)
            
        Returns:
            List of added resource IDs
        """
        added_resources = []
        processed_urls = set()
        
        for page_num in range(1, max_pages + 1):
            try:
                # Construct URL with pagination
                url = f"{self.LARAVEL_TOPIC_URL}&page={page_num}" if page_num > 1 else self.LARAVEL_TOPIC_URL
                logger.info(f"Fetching Laracasts Laravel series page {page_num}: {url}")
                
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find series cards - they're in links with specific patterns
                series_links = soup.find_all('a', href=re.compile(r'^/series/[^/]+$'))
                
                series_found = 0
                for link in series_links:
                    try:
                        series_url = link.get('href', '')
                        if not series_url:
                            continue
                        
                        # Build full URL
                        full_url = urljoin(self.BASE_URL, series_url)
                        
                        # Skip if already processed
                        if full_url in processed_urls:
                            continue
                        processed_urls.add(full_url)
                        
                        # Extract series data from the card
                        series_data = self._extract_series_data(link)
                        if not series_data:
                            continue
                        
                        # Add resource
                        resource_id = self._add_series_resource(series_data, full_url)
                        if resource_id:
                            added_resources.append(resource_id)
                            series_found += 1
                            
                    except Exception as e:
                        logger.error(f"Error processing series link: {e}")
                        continue
                
                logger.info(f"Found {series_found} series on page {page_num}")
                
                # Check if there's a next page
                if not self._has_next_page(soup):
                    logger.info("No more pages available")
                    break
                
                # Rate limiting
                time.sleep(1.5)
                
            except Exception as e:
                logger.error(f"Error fetching Laracasts page {page_num}: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(added_resources)} Laravel series from Laracasts")
        return added_resources
    
    def _extract_series_data(self, link_elem: BeautifulSoup) -> Optional[Dict[str, Any]]:
        """Extract series data from a link element."""
        try:
            # Get the container that has all the info
            container = link_elem
            
            # Try to find the parent container that has all elements
            # Laracasts uses nested structure, so we might need to go up
            while container and not container.find('h3'):
                container = container.parent
                if not container or container.name == 'html':
                    return None
            
            # Extract title
            title_elem = container.find('h3')
            if not title_elem:
                return None
            title = title_elem.get_text(strip=True)
            
            # Extract instructor
            instructor_elem = container.find('div', string=re.compile(r'^With\s+'))
            instructor = instructor_elem.get_text(strip=True).replace('With ', '') if instructor_elem else 'Unknown'
            
            # Extract episode count, difficulty, and category from list items
            episode_count = None
            difficulty = None
            category = None
            
            list_items = container.find_all('li')
            for li in list_items:
                text = li.get_text(strip=True)
                
                # Episode count
                if 'Episode' in text:
                    match = re.search(r'(\d+)\s+Episode', text)
                    if match:
                        episode_count = int(match.group(1))
                
                # Difficulty
                if text in ['Beginner', 'Intermediate', 'Advanced', 'Expert']:
                    difficulty = text
                
                # Category (Frameworks, Techniques, Tooling, etc.)
                if text in ['Frameworks', 'Techniques', 'Tooling', 'Testing', 'Languages', 'DevOps']:
                    category = text
            
            # Get series slug from URL
            href = link_elem.get('href', '')
            series_slug = href.split('/')[-1] if href else None
            
            return {
                'title': title,
                'instructor': instructor,
                'episode_count': episode_count,
                'difficulty': difficulty,
                'category': category,
                'slug': series_slug,
                'is_free': self._check_if_free_series(title, series_slug)
            }
            
        except Exception as e:
            logger.error(f"Error extracting series data: {e}")
            return None
    
    def _check_if_free_series(self, title: str, slug: str) -> bool:
        """Check if a series is free based on known free series."""
        # Known free series on Laracasts
        free_series_patterns = [
            '30-days-to-learn',
            'laravel-8-from-scratch',
            'laravel-6-from-scratch',
            'laravel-5-from-scratch',
            'php-for-beginners',
            'whats-new-in-laravel',
            'fresh-look'
        ]
        
        # Check slug
        if slug:
            for pattern in free_series_patterns:
                if pattern in slug.lower():
                    return True
        
        # Check title
        title_lower = title.lower()
        free_keywords = ['from scratch', "what's new", 'fresh look', '30 days']
        return any(keyword in title_lower for keyword in free_keywords)
    
    def _has_next_page(self, soup: BeautifulSoup) -> bool:
        """Check if there's a next page button."""
        # Look for Next button/link
        next_link = soup.find('a', string='Next')
        if next_link and not next_link.get('disabled'):
            return True
        
        # Also check for disabled button
        next_button = soup.find('button', string='Next')
        if next_button and not next_button.get('disabled'):
            return True
        
        return False
    
    def _add_series_resource(self, series_data: Dict[str, Any], url: str) -> Optional[int]:
        """Add a series resource to the database."""
        try:
            # Determine difficulty level
            difficulty_map = {
                'Beginner': DifficultyLevel.BEGINNER,
                'Intermediate': DifficultyLevel.INTERMEDIATE,
                'Advanced': DifficultyLevel.ADVANCED,
                'Expert': DifficultyLevel.EXPERT
            }
            difficulty = difficulty_map.get(series_data.get('difficulty'), DifficultyLevel.INTERMEDIATE)
            
            # Build description
            description_parts = []
            if series_data.get('episode_count'):
                description_parts.append(f"{series_data['episode_count']} episodes")
            if series_data.get('instructor'):
                description_parts.append(f"by {series_data['instructor']}")
            if series_data.get('is_free'):
                description_parts.append("FREE")
            else:
                description_parts.append("Premium")
            
            description = f"Laravel series on Laracasts - {', '.join(description_parts)}"
            
            # Build tags
            tags = ['laracasts', 'video-series']
            
            # Add category as tag
            if series_data.get('category'):
                tags.append(series_data['category'].lower())
            
            # Add difficulty as tag
            if series_data.get('difficulty'):
                tags.append(series_data['difficulty'].lower())
            
            # Add free/premium tag
            if series_data.get('is_free'):
                tags.append('free')
            else:
                tags.append('premium')
            
            # Extract technology tags from title
            tech_tags = self._extract_tech_tags(series_data['title'])
            tags.extend(tech_tags)
            
            # Add instructor last name as tag if available
            if series_data.get('instructor') and series_data['instructor'] != 'Unknown':
                instructor_parts = series_data['instructor'].split()
                if len(instructor_parts) >= 2:
                    tags.append(instructor_parts[-1].lower())
            
            # Metadata
            metadata = {
                'instructor': series_data.get('instructor', 'Unknown'),
                'episode_count': series_data.get('episode_count'),
                'category': series_data.get('category'),
                'is_free': series_data.get('is_free', False),
                'platform': 'Laracasts',
                'series_type': 'video'
            }
            
            # Add resource
            resource_id = self.fetcher.add_resource(
                title=series_data['title'],
                url=url,
                resource_type=ResourceType.COURSE,
                source=ResourceSource.LARACASTS,
                description=description,
                difficulty=difficulty,
                tags=list(set(tags)),  # Remove duplicates
                metadata=metadata
            )
            
            logger.info(f"Added Laracasts series: {series_data['title']}")
            return resource_id
            
        except Exception as e:
            logger.error(f"Error adding series resource: {e}")
            return None
    
    def _extract_tech_tags(self, title: str) -> List[str]:
        """Extract technology tags from series title."""
        text = title.lower()
        tags = []
        
        tech_patterns = {
            'livewire': r'\blivewire\b',
            'pest': r'\bpest\b',
            'inertia': r'\binertia\b',
            'vue': r'\bvue\b',
            'react': r'\breact\b',
            'alpine': r'\balpine\b',
            'tailwind': r'\btailwind\b',
            'api': r'\bapi\b',
            'testing': r'\b(test|testing|tdd)\b',
            'eloquent': r'\beloquent\b',
            'blade': r'\bblade\b',
            'vite': r'\bvite\b',
            'docker': r'\bdocker\b',
            'deployment': r'\b(deploy|deployment)\b',
            'security': r'\bsecurity\b',
            'authentication': r'\b(auth|authentication)\b',
            'queue': r'\bqueue\b',
            'websockets': r'\bwebsocket\b',
            'broadcasting': r'\bbroadcast\b',
            'filament': r'\bfilament\b',
            'nova': r'\bnova\b',
            'horizon': r'\bhorizon\b',
            'forge': r'\bforge\b',
            'vapor': r'\bvapor\b',
            'sail': r'\bsail\b',
            'valet': r'\bvalet\b',
            'passport': r'\bpassport\b',
            'sanctum': r'\bsanctum\b',
            'fortify': r'\bfortify\b',
            'jetstream': r'\bjetstream\b',
            'breeze': r'\bbreeze\b',
            'scout': r'\bscout\b',
            'telescope': r'\btelescope\b',
            'dusk': r'\bdusk\b',
            'cashier': r'\bcashier\b',
            'socialite': r'\bsocialite\b',
            'spark': r'\bspark\b',
            'octane': r'\boctane\b'
        }
        
        for tag, pattern in tech_patterns.items():
            if re.search(pattern, text):
                tags.append(tag)
        
        # Always add laravel tag
        if 'laravel' not in tags:
            tags.append('laravel')
        
        return tags
    
    def fetch_series_by_category(self, category: str, max_pages: int = 2) -> List[int]:
        """
        Fetch series by specific category (frameworks, techniques, tooling, etc.).
        
        Args:
            category: Category name (frameworks, techniques, tooling, testing, languages)
            max_pages: Maximum pages to fetch
            
        Returns:
            List of added resource IDs
        """
        category_url = f"{self.SERIES_URL}?taxonomies%5B%5D={category.lower()}"
        added_resources = []
        
        logger.info(f"Fetching Laracasts series in category: {category}")
        
        # Similar implementation to fetch_laravel_series but with category URL
        # ... (implementation would be similar)
        
        return added_resources
    
    def fetch_free_series(self) -> List[int]:
        """
        Fetch known free Laravel series from Laracasts.
        
        Returns:
            List of added resource IDs
        """
        # List of known free Laravel series
        free_series = [
            {
                'title': '30 Days to Learn Laravel',
                'slug': '30-days-to-learn-laravel-11',
                'instructor': 'Jeffrey Way',
                'episode_count': 30,
                'difficulty': 'Beginner',
                'description': 'Complete Laravel course for beginners covering all essentials in 30 episodes'
            },
            {
                'title': 'Laravel 8 From Scratch',
                'slug': 'laravel-8-from-scratch',
                'instructor': 'Jeffrey Way',
                'episode_count': 70,
                'difficulty': 'Beginner',
                'description': 'Comprehensive Laravel 8 course from the ground up'
            },
            {
                'title': "What's New in Laravel 11",
                'slug': 'whats-new-in-laravel-11',
                'instructor': 'Luke Downing',
                'episode_count': 14,
                'difficulty': 'Intermediate',
                'description': 'Overview of new features and changes in Laravel 11'
            },
            {
                'title': "What's New in Laravel 10",
                'slug': 'whats-new-in-laravel-10',
                'instructor': 'Jeffrey Way',
                'episode_count': 5,
                'difficulty': 'Intermediate',
                'description': 'Overview of new features and changes in Laravel 10'
            },
            {
                'title': 'Laravel Queue Mastery',
                'slug': 'laravel-queue-mastery',
                'instructor': 'Mohamed Said',
                'episode_count': 8,
                'difficulty': 'Intermediate',
                'description': 'Deep dive into Laravel queues and job processing'
            }
        ]
        
        added_resources = []
        
        for series in free_series:
            try:
                url = f"{self.BASE_URL}/series/{series['slug']}"
                
                # Add the free series
                resource_id = self._add_series_resource(
                    {
                        'title': series['title'],
                        'instructor': series['instructor'],
                        'episode_count': series['episode_count'],
                        'difficulty': series['difficulty'],
                        'category': 'Frameworks',
                        'slug': series['slug'],
                        'is_free': True
                    },
                    url
                )
                
                if resource_id:
                    added_resources.append(resource_id)
                    logger.info(f"Added free series: {series['title']}")
                    
            except Exception as e:
                logger.error(f"Error adding free series '{series['title']}': {e}")
                continue
        
        return added_resources


class LaravelBootcampAggregator:
    """Aggregator for Laravel Bootcamp content."""
    
    BASE_URL = "https://bootcamp.laravel.com"
    
    def __init__(self, resource_fetcher: LearningResourceFetcher):
        """Initialize with resource fetcher."""
        self.fetcher = resource_fetcher
        logger.info("Initialized LaravelBootcampAggregator")
    
    def fetch_bootcamp_content(self) -> List[int]:
        """Fetch Laravel Bootcamp structured content."""
        # Laravel Bootcamp has a known structure, so we can define it directly
        bootcamp_sections = [
            {
                'title': 'Laravel Bootcamp - Getting Started',
                'url': f'{self.BASE_URL}/',
                'description': 'Introduction to Laravel Bootcamp and setting up your development environment',
                'tags': ['bootcamp', 'getting-started', 'setup'],
                'difficulty': DifficultyLevel.BEGINNER
            },
            {
                'title': 'Laravel Bootcamp - Blade: Installation',
                'url': f'{self.BASE_URL}/blade/installation',
                'description': 'Installing Laravel and creating your first Laravel project using Blade templates',
                'tags': ['bootcamp', 'blade', 'installation', 'setup'],
                'difficulty': DifficultyLevel.BEGINNER
            },
            {
                'title': 'Laravel Bootcamp - Blade: Creating Chirps',
                'url': f'{self.BASE_URL}/blade/creating-chirps',
                'description': 'Building a microblogging platform - creating the Chirp model and forms',
                'tags': ['bootcamp', 'blade', 'forms', 'models', 'crud'],
                'difficulty': DifficultyLevel.BEGINNER
            },
            {
                'title': 'Laravel Bootcamp - Blade: Showing Chirps',
                'url': f'{self.BASE_URL}/blade/showing-chirps',
                'description': 'Displaying Chirps from the database using Blade templates',
                'tags': ['bootcamp', 'blade', 'views', 'database'],
                'difficulty': DifficultyLevel.BEGINNER
            },
            {
                'title': 'Laravel Bootcamp - Blade: Editing Chirps',
                'url': f'{self.BASE_URL}/blade/editing-chirps',
                'description': 'Implementing edit functionality for Chirps',
                'tags': ['bootcamp', 'blade', 'crud', 'forms'],
                'difficulty': DifficultyLevel.INTERMEDIATE
            },
            {
                'title': 'Laravel Bootcamp - Blade: Deleting Chirps',
                'url': f'{self.BASE_URL}/blade/deleting-chirps',
                'description': 'Adding delete functionality and authorization',
                'tags': ['bootcamp', 'blade', 'crud', 'authorization'],
                'difficulty': DifficultyLevel.INTERMEDIATE
            },
            {
                'title': 'Laravel Bootcamp - Blade: Notifications & Events',
                'url': f'{self.BASE_URL}/blade/notifications-and-events',
                'description': 'Sending email notifications when new Chirps are created',
                'tags': ['bootcamp', 'blade', 'notifications', 'events', 'email'],
                'difficulty': DifficultyLevel.INTERMEDIATE
            },
            # Livewire versions
            {
                'title': 'Laravel Bootcamp - Livewire: Installation',
                'url': f'{self.BASE_URL}/livewire/installation',
                'description': 'Installing Laravel with Livewire for reactive components',
                'tags': ['bootcamp', 'livewire', 'installation', 'setup'],
                'difficulty': DifficultyLevel.BEGINNER
            },
            {
                'title': 'Laravel Bootcamp - Livewire: Creating Chirps',
                'url': f'{self.BASE_URL}/livewire/creating-chirps',
                'description': 'Building reactive forms with Livewire components',
                'tags': ['bootcamp', 'livewire', 'forms', 'components', 'crud'],
                'difficulty': DifficultyLevel.INTERMEDIATE
            },
            # Inertia + React versions
            {
                'title': 'Laravel Bootcamp - Inertia & React: Installation',
                'url': f'{self.BASE_URL}/inertia/installation',
                'description': 'Setting up Laravel with Inertia.js and React',
                'tags': ['bootcamp', 'inertia', 'react', 'installation', 'spa'],
                'difficulty': DifficultyLevel.INTERMEDIATE
            },
            {
                'title': 'Laravel Bootcamp - Inertia & React: Creating Chirps',
                'url': f'{self.BASE_URL}/inertia/creating-chirps',
                'description': 'Building a SPA with Inertia.js and React components',
                'tags': ['bootcamp', 'inertia', 'react', 'spa', 'crud'],
                'difficulty': DifficultyLevel.INTERMEDIATE
            }
        ]
        
        added_resources = []
        
        for section in bootcamp_sections:
            try:
                resource_id = self.fetcher.add_resource(
                    title=section['title'],
                    url=section['url'],
                    resource_type=ResourceType.TUTORIAL,
                    source=ResourceSource.LARAVEL_BOOTCAMP,
                    description=section['description'],
                    difficulty=section['difficulty'],
                    tags=section['tags'],
                    published_date=None,  # Bootcamp content doesn't have specific dates
                    metadata={
                        'type': 'bootcamp',
                        'official': True,
                        'interactive': True
                    }
                )
                
                added_resources.append(resource_id)
                logger.info(f"Added Laravel Bootcamp section: {section['title']}")
                
            except Exception as e:
                logger.error(f"Error adding bootcamp section: {e}")
                continue
        
        logger.info(f"Successfully added {len(added_resources)} Laravel Bootcamp sections")
        return added_resources


class ConferenceTalkAggregator:
    """Aggregator for Laravel conference talks and videos."""
    
    # Known Laravel conference YouTube channels and playlists
    LARAVEL_CHANNELS = {
        'laravel': {
            'channel_id': 'UCTuplgOBi6tJIlesIboymGA',
            'channel_name': 'Laravel',
            'channel_url': 'https://www.youtube.com/@LaravelPHP',
            'playlists': {
                'laracon_us_2023': 'PLhhNHvAOFAvOMtIy-a-eoM5qtCJr3CRSU',
                'laracon_online_2022': 'PLhhNHvAOFAvN79AsNAuLpTtU9v5tTkfh3',
                'laracon_eu_2019': 'PLhhNHvAOFAvNJQUfsFz8mhj0vJ0rXlhLA',
                'laracon_us_2019': 'PLhhNHvAOFAvMYG6cxBiVzn7ts2bFmqnqx'
            }
        },
        'laracon_eu': {
            'channel_id': 'UCb9XEo_1SDNR8Ucpbktrg5A',  
            'channel_name': 'Laracon EU',
            'channel_url': 'https://www.youtube.com/@LaraconEU',
            'playlists': {}
        },
        'phpuk': {
            'channel_id': 'UCLCl5Fmu5mJE_IHHVYo0pGA',
            'channel_name': 'PHP UK Conference',
            'channel_url': 'https://www.youtube.com/@phpukconference',
            'playlists': {}
        }
    }
    
    # Popular Laravel speakers to look for
    KNOWN_SPEAKERS = [
        'Taylor Otwell', 'Nuno Maduro', 'Caleb Porzio', 'Dries Vints',
        'Marcel Pociot', 'Freek Van der Herten', 'Mohamed Said',
        'Jeffrey Way', 'Matt Stauffer', 'Adam Wathan', 'Jonathan Reinink',
        'Christoph Rumpel', 'Bobby Bouwmann', 'Jess Archer', 'Tim MacDonald'
    ]
    
    def __init__(self, resource_fetcher: LearningResourceFetcher, youtube_api_key: Optional[str] = None):
        """Initialize with resource fetcher and optional YouTube API key."""
        self.fetcher = resource_fetcher
        self.youtube_api_key = youtube_api_key or os.environ.get('YOUTUBE_API_KEY')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; LaravelMCPCompanion/1.0; +https://github.com/brianirish/laravel-mcp-companion)'
        })
        logger.info("Initialized ConferenceTalkAggregator")
    
    def fetch_conference_talks(self, use_api: bool = None, max_videos: int = 100) -> List[int]:
        """
        Fetch Laravel conference talks from YouTube.
        
        Args:
            use_api: Whether to use YouTube API (None = auto-detect based on API key)
            max_videos: Maximum number of videos to fetch
            
        Returns:
            List of added resource IDs
        """
        if use_api is None:
            use_api = bool(self.youtube_api_key)
        
        if use_api and self.youtube_api_key:
            logger.info("Using YouTube API to fetch conference talks")
            return self._fetch_with_api(max_videos)
        else:
            logger.info("Using web scraping to fetch conference talks")
            return self._fetch_without_api(max_videos)
    
    def _fetch_with_api(self, max_videos: int) -> List[int]:
        """Fetch videos using YouTube Data API."""
        if not self.youtube_api_key:
            logger.error("YouTube API key not configured")
            return []
        
        added_resources = []
        videos_fetched = 0
        
        # Fetch from known playlists
        for channel_key, channel_info in self.LARAVEL_CHANNELS.items():
            if videos_fetched >= max_videos:
                break
                
            for playlist_name, playlist_id in channel_info.get('playlists', {}).items():
                if videos_fetched >= max_videos:
                    break
                    
                try:
                    playlist_videos = self._fetch_playlist_videos_api(
                        playlist_id, 
                        channel_info['channel_name'],
                        min(50, max_videos - videos_fetched)
                    )
                    
                    for video in playlist_videos:
                        resource_id = self._add_video_resource(video)
                        if resource_id:
                            added_resources.append(resource_id)
                            videos_fetched += 1
                    
                    # Rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error fetching playlist {playlist_name}: {e}")
                    continue
        
        # Search for Laravel conference talks if we need more
        if videos_fetched < max_videos:
            try:
                search_results = self._search_conference_talks_api(max_videos - videos_fetched)
                for video in search_results:
                    resource_id = self._add_video_resource(video)
                    if resource_id:
                        added_resources.append(resource_id)
                        videos_fetched += 1
            except Exception as e:
                logger.error(f"Error searching for conference talks: {e}")
        
        logger.info(f"Successfully fetched {len(added_resources)} conference talks using API")
        return added_resources
    
    def _fetch_playlist_videos_api(self, playlist_id: str, channel_name: str, max_results: int = 50) -> List[Dict]:
        """Fetch videos from a YouTube playlist using API."""
        videos = []
        next_page_token = None
        
        while len(videos) < max_results:
            try:
                # Build API request
                params = {
                    'part': 'snippet,contentDetails',
                    'playlistId': playlist_id,
                    'maxResults': min(50, max_results - len(videos)),
                    'key': self.youtube_api_key
                }
                
                if next_page_token:
                    params['pageToken'] = next_page_token
                
                response = self.session.get(
                    'https://www.googleapis.com/youtube/v3/playlistItems',
                    params=params,
                    timeout=10
                )
                response.raise_for_status()
                
                data = response.json()
                
                for item in data.get('items', []):
                    snippet = item.get('snippet', {})
                    video_id = item.get('snippet', {}).get('resourceId', {}).get('videoId')
                    
                    if not video_id:
                        continue
                    
                    video_info = {
                        'title': snippet.get('title', ''),
                        'url': f'https://www.youtube.com/watch?v={video_id}',
                        'description': snippet.get('description', ''),
                        'channel': channel_name,
                        'published_at': snippet.get('publishedAt'),
                        'video_id': video_id,
                        'thumbnail': snippet.get('thumbnails', {}).get('high', {}).get('url')
                    }
                    
                    # Only add if Laravel-related
                    if self._is_laravel_conference_talk(video_info['title'], video_info['description']):
                        videos.append(video_info)
                
                # Check for next page
                next_page_token = data.get('nextPageToken')
                if not next_page_token:
                    break
                    
            except Exception as e:
                logger.error(f"Error fetching playlist videos: {e}")
                break
        
        return videos
    
    def _search_conference_talks_api(self, max_results: int = 50) -> List[Dict]:
        """Search for Laravel conference talks using YouTube API."""
        videos = []
        search_queries = [
            'Laravel conference talk',
            'Laracon keynote',
            'Laravel summit presentation',
            'Laravel Live talk'
        ]
        
        for query in search_queries:
            if len(videos) >= max_results:
                break
                
            try:
                params = {
                    'part': 'snippet',
                    'q': query,
                    'type': 'video',
                    'videoDuration': 'medium',  # 4-20 minutes
                    'maxResults': min(25, max_results - len(videos)),
                    'order': 'relevance',
                    'key': self.youtube_api_key
                }
                
                response = self.session.get(
                    'https://www.googleapis.com/youtube/v3/search',
                    params=params,
                    timeout=10
                )
                response.raise_for_status()
                
                data = response.json()
                
                for item in data.get('items', []):
                    snippet = item.get('snippet', {})
                    video_id = item.get('id', {}).get('videoId')
                    
                    if not video_id:
                        continue
                    
                    video_info = {
                        'title': snippet.get('title', ''),
                        'url': f'https://www.youtube.com/watch?v={video_id}',
                        'description': snippet.get('description', ''),
                        'channel': snippet.get('channelTitle', ''),
                        'published_at': snippet.get('publishedAt'),
                        'video_id': video_id,
                        'thumbnail': snippet.get('thumbnails', {}).get('high', {}).get('url')
                    }
                    
                    # Only add if it's a conference talk
                    if self._is_laravel_conference_talk(video_info['title'], video_info['description']):
                        videos.append(video_info)
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error searching for talks with query '{query}': {e}")
                continue
        
        return videos
    
    def _fetch_without_api(self, max_videos: int) -> List[int]:
        """Fetch videos by scraping YouTube channels (no API required)."""
        added_resources = []
        videos_fetched = 0
        
        # Known Laravel conference talk playlists (direct URLs)
        known_playlists = [
            {
                'url': 'https://www.youtube.com/playlist?list=PLhhNHvAOFAvOMtIy-a-eoM5qtCJr3CRSU',
                'name': 'Laracon US 2023',
                'conference': 'Laracon US 2023'
            },
            {
                'url': 'https://www.youtube.com/playlist?list=PLhhNHvAOFAvN79AsNAuLpTtU9v5tTkfh3',
                'name': 'Laracon Online 2022',
                'conference': 'Laracon Online 2022'
            },
            {
                'url': 'https://www.youtube.com/playlist?list=PLhhNHvAOFAvMYG6cxBiVzn7ts2bFmqnqx',
                'name': 'Laracon US 2019',
                'conference': 'Laracon US 2019'
            }
        ]
        
        # Fetch from known playlists
        for playlist in known_playlists:
            if videos_fetched >= max_videos:
                break
                
            try:
                logger.info(f"Fetching playlist: {playlist['name']}")
                playlist_videos = self._scrape_playlist(
                    playlist['url'], 
                    playlist['conference'],
                    min(50, max_videos - videos_fetched)
                )
                
                for video in playlist_videos:
                    resource_id = self._add_video_resource(video)
                    if resource_id:
                        added_resources.append(resource_id)
                        videos_fetched += 1
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error scraping playlist {playlist['name']}: {e}")
                continue
        
        # Add some manually curated recent talks if we haven't hit the limit
        if videos_fetched < max_videos:
            curated_talks = self._get_curated_talks()
            for talk in curated_talks[:max_videos - videos_fetched]:
                resource_id = self._add_video_resource(talk)
                if resource_id:
                    added_resources.append(resource_id)
                    videos_fetched += 1
        
        logger.info(f"Successfully fetched {len(added_resources)} conference talks without API")
        return added_resources
    
    def _scrape_playlist(self, playlist_url: str, conference_name: str, max_videos: int = 50) -> List[Dict]:
        """Scrape videos from a YouTube playlist without API."""
        videos = []
        
        try:
            response = self.session.get(playlist_url, timeout=10)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for video data in the page
            # YouTube loads data dynamically, but initial videos are in the HTML
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string and 'var ytInitialData' in script.string:
                    # Extract JSON data
                    json_text = script.string
                    start = json_text.find('{')
                    end = json_text.rfind('}') + 1
                    
                    if start > -1 and end > start:
                        try:
                            data = json.loads(json_text[start:end])
                            videos_data = self._extract_playlist_videos_from_json(data)
                            
                            for video_data in videos_data[:max_videos]:
                                video_info = {
                                    'title': video_data.get('title', ''),
                                    'url': f"https://www.youtube.com/watch?v={video_data.get('videoId', '')}",
                                    'description': video_data.get('description', ''),
                                    'channel': video_data.get('channel', 'Laravel'),
                                    'conference': conference_name,
                                    'duration': video_data.get('duration', ''),
                                    'video_id': video_data.get('videoId', '')
                                }
                                
                                if video_info['video_id'] and self._is_laravel_conference_talk(
                                    video_info['title'], 
                                    video_info['description']
                                ):
                                    videos.append(video_info)
                                    
                        except json.JSONDecodeError:
                            logger.error("Failed to parse YouTube JSON data")
                            continue
        
        except Exception as e:
            logger.error(f"Error scraping playlist: {e}")
        
        return videos
    
    def _extract_playlist_videos_from_json(self, data: Dict) -> List[Dict]:
        """Extract video information from YouTube's JSON data structure."""
        videos = []
        
        try:
            # Navigate through YouTube's nested JSON structure
            contents = data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
            
            for tab in contents:
                tab_renderer = tab.get('tabRenderer', {})
                if tab_renderer.get('selected'):
                    content = tab_renderer.get('content', {}).get('sectionListRenderer', {}).get('contents', [])
                    
                    for section in content:
                        playlist_items = section.get('itemSectionRenderer', {}).get('contents', [])
                        
                        for item in playlist_items:
                            playlist_video = item.get('playlistVideoRenderer', {})
                            if playlist_video:
                                video_info = {
                                    'videoId': playlist_video.get('videoId'),
                                    'title': self._extract_text(playlist_video.get('title', {})),
                                    'duration': playlist_video.get('lengthText', {}).get('simpleText', ''),
                                    'channel': self._extract_text(
                                        playlist_video.get('shortBylineText', {})
                                    )
                                }
                                
                                if video_info['videoId']:
                                    videos.append(video_info)
        
        except Exception as e:
            logger.error(f"Error extracting videos from JSON: {e}")
        
        return videos
    
    def _extract_text(self, text_obj: Dict) -> str:
        """Extract text from YouTube's text object structure."""
        if isinstance(text_obj, str):
            return text_obj
        
        # Handle 'runs' format
        runs = text_obj.get('runs', [])
        if runs:
            return ''.join(run.get('text', '') for run in runs)
        
        # Handle 'simpleText' format
        return text_obj.get('simpleText', '')
    
    def _get_curated_talks(self) -> List[Dict]:
        """Get a curated list of recent Laravel conference talks."""
        return [
            {
                'title': 'Laravel 11: What\'s New - Taylor Otwell at Laracon US 2024',
                'url': 'https://www.youtube.com/watch?v=9NNDPDlBrJQ',
                'description': 'Taylor Otwell unveils Laravel 11 features and improvements at Laracon US 2024',
                'channel': 'Laravel',
                'conference': 'Laracon US 2024',
                'speaker': 'Taylor Otwell',
                'video_id': '9NNDPDlBrJQ'
            },
            {
                'title': 'Pest 3: The Architect\'s Vision - Nuno Maduro',
                'url': 'https://www.youtube.com/watch?v=bqBW_E1Y-OI',
                'description': 'Nuno Maduro presents Pest 3 and its architectural improvements',
                'channel': 'Laravel',
                'conference': 'Laracon US 2024',
                'speaker': 'Nuno Maduro',
                'video_id': 'bqBW_E1Y-OI'
            },
            {
                'title': 'Building Laravel Pulse - Jess Archer & Tim MacDonald',
                'url': 'https://www.youtube.com/watch?v=HaexnkKWqdM',
                'description': 'The story behind building Laravel Pulse, a real-time application performance monitoring tool',
                'channel': 'Laravel',
                'conference': 'Laracon US 2023',
                'speaker': 'Jess Archer & Tim MacDonald',
                'video_id': 'HaexnkKWqdM'
            },
            {
                'title': 'Livewire 3: Beyond the Basics - Caleb Porzio',
                'url': 'https://www.youtube.com/watch?v=f4QShF42c6E',
                'description': 'Advanced Livewire 3 techniques and patterns for building dynamic interfaces',
                'channel': 'Laravel',
                'conference': 'Laracon US 2023',
                'speaker': 'Caleb Porzio',
                'video_id': 'f4QShF42c6E'
            },
            {
                'title': 'Laravel Folio & Volt - Taylor Otwell',
                'url': 'https://www.youtube.com/watch?v=im-iN7l5U_A',
                'description': 'Introduction to Laravel Folio page-based routing and Volt single-file components',
                'channel': 'Laravel',
                'conference': 'Laracon US 2023',
                'speaker': 'Taylor Otwell',
                'video_id': 'im-iN7l5U_A'
            }
        ]
    
    def _is_laravel_conference_talk(self, title: str, description: str) -> bool:
        """Check if a video is a Laravel conference talk."""
        text = f"{title} {description}".lower()
        
        # Must contain Laravel or related framework
        laravel_keywords = ['laravel', 'laracon', 'livewire', 'inertia', 'pest', 'forge', 'vapor']
        if not any(keyword in text for keyword in laravel_keywords):
            return False
        
        # Should be from a conference
        conference_keywords = ['conference', 'talk', 'keynote', 'presentation', 'summit', 'live']
        if not any(keyword in text for keyword in conference_keywords):
            # Check if it mentions known conferences
            known_conferences = ['laracon', 'phpuk', 'phpworld', 'laravel live']
            if not any(conf in text for conf in known_conferences):
                return False
        
        # Exclude tutorials, courses, and non-conference content
        exclude_keywords = ['tutorial', 'course', 'episode', 'lesson', 'part 1', 'ep.']
        if any(keyword in text for keyword in exclude_keywords):
            return False
        
        return True
    
    def _extract_speaker_from_title(self, title: str) -> Optional[str]:
        """Extract speaker name from video title."""
        # Common patterns: "Title - Speaker Name", "Speaker Name: Title", "Title by Speaker"
        patterns = [
            r' - ([A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)$',
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)?):',
            r' by ([A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title)
            if match:
                speaker = match.group(1)
                # Verify it's a known speaker
                if any(known in speaker for known in self.KNOWN_SPEAKERS):
                    return speaker
        
        return None
    
    def _extract_conference_info(self, title: str, description: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract conference name and year from video info."""
        text = f"{title} {description}"
        
        # Look for conference patterns
        conference_patterns = [
            (r'Laracon\s+(US|EU|AU|Online)\s+(\d{4})', 'Laracon {0} {1}'),
            (r'Laracon\s+(\d{4})', 'Laracon {0}'),
            (r'Laravel\s+Live\s+(UK|India|Denmark)\s+(\d{4})', 'Laravel Live {0} {1}'),
            (r'PHP\s*UK\s+Conference\s+(\d{4})', 'PHP UK Conference {0}'),
            (r'(\d{4})\s+Laracon\s+(US|EU|AU|Online)', 'Laracon {1} {0}')
        ]
        
        for pattern, template in conference_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                conference = template.format(*match.groups())
                year = re.search(r'\d{4}', conference)
                return conference, year.group() if year else None
        
        return None, None
    
    def _parse_duration(self, duration_str: str) -> Optional[str]:
        """Parse duration string to a readable format."""
        if not duration_str:
            return None
        
        # YouTube API format: PT15M33S
        if duration_str.startswith('PT'):
            match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
            if match:
                hours, minutes, seconds = match.groups()
                parts = []
                if hours:
                    parts.append(f"{hours}h")
                if minutes:
                    parts.append(f"{minutes}m")
                if seconds and not minutes:
                    parts.append(f"{seconds}s")
                return ' '.join(parts) if parts else None
        
        # Already formatted
        if re.match(r'\d+:\d+', duration_str):
            return duration_str
        
        return duration_str
    
    def _add_video_resource(self, video_info: Dict) -> Optional[int]:
        """Add a video resource to the database."""
        try:
            # Extract additional metadata
            speaker = video_info.get('speaker') or self._extract_speaker_from_title(video_info['title'])
            conference = video_info.get('conference')
            year = video_info.get('year')
            
            if not conference:
                conference, year = self._extract_conference_info(
                    video_info['title'], 
                    video_info.get('description', '')
                )
            elif conference and not year:
                # Extract year from conference name if not provided separately
                year_match = re.search(r'\d{4}', conference)
                if year_match:
                    year = year_match.group()
            
            # Parse published date
            published_date = None
            if video_info.get('published_at'):
                try:
                    published_date = datetime.fromisoformat(
                        video_info['published_at'].replace('Z', '+00:00')
                    )
                except:
                    pass
            
            # Build tags
            tags = ['conference-talk', 'video']
            if conference:
                # Add conference as tag (e.g., 'laracon-us-2023')
                conf_tag = conference.lower().replace(' ', '-')
                tags.append(conf_tag)
            
            if year and year not in tags:
                tags.append(year)
            
            if speaker:
                # Add speaker last name as tag
                speaker_parts = speaker.split()
                if len(speaker_parts) >= 2:
                    tags.append(speaker_parts[-1].lower())
            
            # Extract technology tags from title/description
            tech_tags = self._extract_tech_tags(
                video_info['title'], 
                video_info.get('description', '')
            )
            tags.extend(tech_tags)
            
            # Determine difficulty
            difficulty = self._estimate_talk_difficulty(
                video_info['title'], 
                video_info.get('description', '')
            )
            
            # Build metadata
            metadata = {
                'video_id': video_info.get('video_id'),
                'channel': video_info.get('channel', 'Unknown'),
                'duration': self._parse_duration(video_info.get('duration', '')),
                'thumbnail': video_info.get('thumbnail')
            }
            
            if speaker:
                metadata['speaker'] = speaker
            if conference:
                metadata['conference'] = conference
            if year:
                metadata['year'] = year
            
            # Add to database
            resource_id = self.fetcher.add_resource(
                title=video_info['title'],
                url=video_info['url'],
                resource_type=ResourceType.VIDEO,
                source=ResourceSource.CONFERENCE_TALK,
                description=video_info.get('description', '')[:500],  # Limit description length
                difficulty=difficulty,
                tags=list(set(tags)),  # Remove duplicates
                published_date=published_date,
                metadata=metadata
            )
            
            logger.info(f"Added conference talk: {video_info['title']}")
            return resource_id
            
        except Exception as e:
            logger.error(f"Error adding video resource: {e}")
            return None
    
    def _extract_tech_tags(self, title: str, description: str) -> List[str]:
        """Extract technology-related tags from content."""
        text = f"{title} {description}".lower()
        tags = []
        
        tech_keywords = {
            'livewire': 'livewire',
            'inertia': 'inertia',
            'pest': 'pest',
            'phpunit': 'testing',
            'testing': 'testing',
            'vue': 'vue',
            'react': 'react',
            'alpine': 'alpine',
            'tailwind': 'tailwind',
            'eloquent': 'eloquent',
            'blade': 'blade',
            'api': 'api',
            'graphql': 'graphql',
            'websocket': 'websockets',
            'broadcasting': 'broadcasting',
            'queue': 'queues',
            'job': 'queues',
            'event': 'events',
            'middleware': 'middleware',
            'authentication': 'authentication',
            'authorization': 'authorization',
            'security': 'security',
            'performance': 'performance',
            'deployment': 'deployment',
            'docker': 'docker',
            'sail': 'sail',
            'vapor': 'vapor',
            'forge': 'forge',
            'horizon': 'horizon',
            'telescope': 'telescope',
            'pulse': 'pulse',
            'folio': 'folio',
            'volt': 'volt',
            'reverb': 'reverb',
            'herd': 'herd',
            'valet': 'valet'
        }
        
        for keyword, tag in tech_keywords.items():
            if keyword in text and tag not in tags:
                tags.append(tag)
        
        return tags
    
    def _estimate_talk_difficulty(self, title: str, description: str) -> DifficultyLevel:
        """Estimate the difficulty level of a conference talk."""
        text = f"{title} {description}".lower()
        
        # Beginner indicators
        if any(word in text for word in ['introduction', 'getting started', 'beginner', 'basics', 'first steps']):
            return DifficultyLevel.BEGINNER
        
        # Expert indicators
        if any(word in text for word in ['internals', 'deep dive', 'advanced', 'architecture', 'under the hood']):
            return DifficultyLevel.EXPERT
        
        # Advanced indicators
        if any(word in text for word in ['scaling', 'performance', 'optimization', 'patterns', 'best practices']):
            return DifficultyLevel.ADVANCED
        
        # Default to intermediate for most conference talks
        return DifficultyLevel.INTERMEDIATE
    
    # Keep the old method for backward compatibility but make it use the new implementation
    def add_known_talks(self) -> List[int]:
        """Add known high-quality Laravel conference talks (backward compatibility)."""
        return self.fetch_conference_talks(use_api=False, max_videos=20)


class ContentAggregatorManager:
    """Manager for running all content aggregators."""
    
    def __init__(self, db_path: Path):
        """Initialize with database path."""
        self.fetcher = LearningResourceFetcher(db_path)
        self.aggregators = {
            'laravel-news': LaravelNewsAggregator(self.fetcher),
            'spatie-blog': SpatieBlogAggregator(self.fetcher),
            'laracasts': LaracastsAggregator(self.fetcher),
            'laravel-bootcamp': LaravelBootcampAggregator(self.fetcher),
            'conference-talks': ConferenceTalkAggregator(self.fetcher)
        }
        logger.info("Initialized ContentAggregatorManager")
    
    def update_all(self) -> Dict[str, int]:
        """Run all aggregators and return results."""
        results = {}
        
        for name, aggregator in self.aggregators.items():
            logger.info(f"Running {name} aggregator...")
            
            try:
                if name == 'laravel-news':
                    resources = aggregator.fetch_articles(limit=30)
                elif name == 'spatie-blog':
                    resources = aggregator.fetch_tutorials(pages=1)
                elif name == 'laracasts':
                    # Fetch free series first, then some Laravel series
                    free_resources = aggregator.fetch_free_series()
                    series_resources = aggregator.fetch_laravel_series(max_pages=2)
                    resources = free_resources + series_resources
                elif name == 'laravel-bootcamp':
                    resources = aggregator.fetch_bootcamp_content()
                elif name == 'conference-talks':
                    resources = aggregator.add_known_talks()
                else:
                    resources = []
                
                count = len(resources) if isinstance(resources, list) else resources
                results[name] = count
                logger.info(f"{name}: Added {count} resources")
                
            except Exception as e:
                logger.error(f"Error running {name} aggregator: {e}")
                results[name] = 0
        
        return results
    
    def update_single(self, aggregator_name: str, **kwargs) -> List[int]:
        """
        Update a single aggregator.
        
        Args:
            aggregator_name: Name of the aggregator to run
            **kwargs: Additional arguments to pass to specific aggregators
                - For 'laravel-news':
                    - mode: 'rss' (default), 'historical', 'category', 'tag'
                    - limit: Number of RSS items (for mode='rss')
                    - start_page: Starting page (for mode='historical')
                    - max_pages: Max pages to fetch (for mode='historical')
                    - category: Category name (for mode='category')
                    - tag: Tag name (for mode='tag')
                    - delay_between_pages: Delay in seconds
                - For 'laracasts':
                    - mode: 'all' (default), 'free', 'series', 'category'
                    - max_pages: Max pages to fetch (for mode='series' or 'category')
                    - category: Category name (for mode='category')
        """
        if aggregator_name not in self.aggregators:
            logger.error(f"Unknown aggregator: {aggregator_name}")
            return []
        
        aggregator = self.aggregators[aggregator_name]
        
        try:
            if aggregator_name == 'laravel-news':
                mode = kwargs.get('mode', 'rss')
                
                if mode == 'rss':
                    limit = kwargs.get('limit', 30)
                    return aggregator.fetch_articles(limit=limit)
                    
                elif mode == 'historical':
                    start_page = kwargs.get('start_page', 1)
                    max_pages = kwargs.get('max_pages', 10)
                    category = kwargs.get('category', None)
                    delay = kwargs.get('delay_between_pages', 1.0)
                    return aggregator.fetch_historical_articles(
                        start_page=start_page,
                        max_pages=max_pages,
                        category=category,
                        delay_between_pages=delay
                    )
                    
                elif mode == 'category':
                    category = kwargs.get('category', 'tutorials')
                    max_pages = kwargs.get('max_pages', 10)
                    delay = kwargs.get('delay_between_pages', 1.0)
                    return aggregator.fetch_historical_articles(
                        start_page=1,
                        max_pages=max_pages,
                        category=category,
                        delay_between_pages=delay
                    )
                    
                elif mode == 'tag':
                    tag = kwargs.get('tag', 'laravel')
                    max_pages = kwargs.get('max_pages', 5)
                    return aggregator.fetch_articles_by_tag(tag, max_pages)
                    
                else:
                    logger.error(f"Unknown mode for laravel-news: {mode}")
                    return aggregator.fetch_articles(limit=30)
                    
            elif aggregator_name == 'spatie-blog':
                return aggregator.fetch_tutorials(pages=1)
            elif aggregator_name == 'laracasts':
                mode = kwargs.get('mode', 'all')
                
                if mode == 'all':
                    # Fetch both free series and general Laravel series
                    free_resources = aggregator.fetch_free_series()
                    series_resources = aggregator.fetch_laravel_series(max_pages=kwargs.get('max_pages', 2))
                    return free_resources + series_resources
                elif mode == 'free':
                    return aggregator.fetch_free_series()
                elif mode == 'series':
                    max_pages = kwargs.get('max_pages', 3)
                    return aggregator.fetch_laravel_series(max_pages=max_pages)
                elif mode == 'category':
                    category = kwargs.get('category', 'frameworks')
                    max_pages = kwargs.get('max_pages', 2)
                    return aggregator.fetch_series_by_category(category, max_pages)
                else:
                    return aggregator.fetch_free_series()
            elif aggregator_name == 'laravel-bootcamp':
                return aggregator.fetch_bootcamp_content()
            elif aggregator_name == 'conference-talks':
                return aggregator.add_known_talks()
            else:
                return []
        except Exception as e:
            logger.error(f"Error updating {aggregator_name}: {e}")
            return []
    
    def fetch_laravel_news_historical(
        self, 
        total_pages: int = 50, 
        batch_size: int = 10,
        start_from_page: int = 1
    ) -> Dict[str, Any]:
        """
        Fetch a large amount of historical Laravel News content in batches.
        
        Args:
            total_pages: Total number of pages to fetch
            batch_size: Number of pages per batch
            start_from_page: Page to start from
            
        Returns:
            Dictionary with results including total articles fetched
        """
        results = {
            'total_articles': 0,
            'batches_completed': 0,
            'errors': []
        }
        
        aggregator = self.aggregators.get('laravel-news')
        if not aggregator:
            logger.error("Laravel News aggregator not found")
            return results
        
        current_page = start_from_page
        
        while current_page < start_from_page + total_pages:
            try:
                logger.info(f"Fetching batch starting at page {current_page}")
                
                # Fetch a batch
                articles = aggregator.fetch_historical_articles(
                    start_page=current_page,
                    max_pages=min(batch_size, (start_from_page + total_pages) - current_page),
                    delay_between_pages=1.5  # Slightly longer delay for courtesy
                )
                
                results['total_articles'] += len(articles)
                results['batches_completed'] += 1
                
                logger.info(f"Batch complete. Total articles so far: {results['total_articles']}")
                
                # Longer delay between batches
                time.sleep(5)
                
                current_page += batch_size
                
            except Exception as e:
                error_msg = f"Error in batch starting at page {current_page}: {e}"
                logger.error(error_msg)
                results['errors'].append(error_msg)
                
                # Continue with next batch
                current_page += batch_size
        
        return results