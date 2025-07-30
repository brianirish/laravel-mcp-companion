#!/usr/bin/env python3
"""
Script to populate the learning resources database with comprehensive data.
This fetches real content from various sources to build a useful knowledge base.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from content_aggregators import ContentAggregatorManager
import logging
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Populate learning resources with real data from various sources."""
    print("=" * 60)
    print("Laravel MCP Companion - Learning Resources Population")
    print("=" * 60)
    
    # Use the project data directory
    data_dir = Path(__file__).parent.parent / 'data' / 'learning_resources'
    manager = ContentAggregatorManager(data_dir)
    
    results = {
        'success': {},
        'errors': []
    }
    
    # 1. Fetch Laravel News RSS (most recent)
    print("\n1. Fetching Laravel News RSS feed...")
    try:
        count = manager.update_single('laravel-news')
        results['success']['laravel-news-rss'] = count
        print(f"   ✓ Fetched {count} recent articles")
    except Exception as e:
        results['errors'].append(f"Laravel News RSS: {e}")
        print(f"   ✗ Error: {e}")
    
    # 2. Fetch Spatie Blog posts
    print("\n2. Fetching Spatie Blog Laravel posts...")
    try:
        # Fetch multiple pages
        count = 0
        for page in range(1, 6):  # Fetch 5 pages
            try:
                page_count = manager.aggregators['spatie-blog'].fetch_tutorials(pages=1)
                if isinstance(page_count, list):
                    count += len(page_count)
                else:
                    count += page_count
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"   - Page {page} error: {e}")
        
        results['success']['spatie-blog'] = count
        print(f"   ✓ Fetched {count} blog posts")
    except Exception as e:
        results['errors'].append(f"Spatie Blog: {e}")
        print(f"   ✗ Error: {e}")
    
    # 3. Fetch Conference Talks
    print("\n3. Fetching Laravel Conference Talks...")
    try:
        # This will fetch from curated list and YouTube if possible
        count = manager.update_single('conference-talks')
        results['success']['conference-talks'] = count
        print(f"   ✓ Fetched {count} conference talks")
    except Exception as e:
        results['errors'].append(f"Conference Talks: {e}")
        print(f"   ✗ Error: {e}")
    
    # 4. Fetch Laracasts series
    print("\n4. Fetching Laracasts Laravel series...")
    try:
        # First fetch free series
        free_count = manager.update_single('laracasts', mode='free')
        results['success']['laracasts-free'] = free_count
        print(f"   ✓ Fetched {free_count} free series")
        
        # Then fetch some Laravel series (will include both free and premium)
        time.sleep(2)  # Rate limiting
        series_count = manager.aggregators['laracasts'].fetch_laravel_series(pages=2)
        if isinstance(series_count, list):
            series_count = len(series_count)
        results['success']['laracasts-series'] = series_count
        print(f"   ✓ Fetched {series_count} additional series")
        
    except Exception as e:
        results['errors'].append(f"Laracasts: {e}")
        print(f"   ✗ Error: {e}")
    
    # 5. Laravel Bootcamp should already be populated
    print("\n5. Laravel Bootcamp content...")
    try:
        bootcamp_count = len(manager.aggregators['laravel-bootcamp'].bootcamp_sections)
        results['success']['laravel-bootcamp'] = bootcamp_count
        print(f"   ✓ {bootcamp_count} bootcamp sections available")
    except Exception as e:
        results['errors'].append(f"Laravel Bootcamp: {e}")
        print(f"   ✗ Error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    total_resources = sum(results['success'].values())
    print(f"\nTotal resources fetched: {total_resources}")
    
    print("\nBy source:")
    for source, count in results['success'].items():
        print(f"  - {source}: {count}")
    
    if results['errors']:
        print(f"\nErrors encountered: {len(results['errors'])}")
        for error in results['errors']:
            print(f"  - {error}")
    
    print("\n✓ Population complete!")
    print("\nNote: Some sources may be limited due to:")
    print("  - Rate limiting protection")
    print("  - Available free content")
    print("  - API restrictions")
    print("\nYou can run this script periodically to fetch new content.")

if __name__ == '__main__':
    main()