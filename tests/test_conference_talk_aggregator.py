#!/usr/bin/env python3
"""
Tests for ConferenceTalkAggregator.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from content_aggregators import ConferenceTalkAggregator
from learning_resources import LearningResourceFetcher, DifficultyLevel


class TestConferenceTalkAggregator(unittest.TestCase):
    """Test cases for ConferenceTalkAggregator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_fetcher = Mock(spec=LearningResourceFetcher)
        self.aggregator = ConferenceTalkAggregator(self.mock_fetcher)
        
    def test_initialization(self):
        """Test aggregator initialization."""
        self.assertIsNotNone(self.aggregator)
        self.assertEqual(self.aggregator.fetcher, self.mock_fetcher)
        self.assertIsNotNone(self.aggregator.session)
        
    def test_is_laravel_conference_talk(self):
        """Test conference talk identification."""
        # Should identify as conference talk
        self.assertTrue(
            self.aggregator._is_laravel_conference_talk(
                "Laravel 11 - Taylor Otwell at Laracon US 2024",
                "Taylor presents new features at the conference"
            )
        )
        
        self.assertTrue(
            self.aggregator._is_laravel_conference_talk(
                "Building Livewire Apps - Caleb Porzio",
                "Conference presentation about Livewire"
            )
        )
        
        # Should NOT identify as conference talk
        self.assertFalse(
            self.aggregator._is_laravel_conference_talk(
                "Laravel Tutorial Part 1",
                "Learn Laravel basics in this tutorial"
            )
        )
        
        self.assertFalse(
            self.aggregator._is_laravel_conference_talk(
                "PHP Development Best Practices",
                "General PHP development with no Laravel content"
            )
        )
        
    def test_extract_speaker_from_title(self):
        """Test speaker extraction from titles."""
        # Test various title formats
        self.assertEqual(
            self.aggregator._extract_speaker_from_title(
                "Laravel 11 - Taylor Otwell"
            ),
            "Taylor Otwell"
        )
        
        self.assertEqual(
            self.aggregator._extract_speaker_from_title(
                "Nuno Maduro: Testing with Pest"
            ),
            "Nuno Maduro"
        )
        
        self.assertEqual(
            self.aggregator._extract_speaker_from_title(
                "Building Apps by Caleb Porzio"
            ),
            "Caleb Porzio"
        )
        
        # Should return None for unknown speakers
        self.assertIsNone(
            self.aggregator._extract_speaker_from_title(
                "Random Talk - Unknown Person"
            )
        )
        
    def test_extract_conference_info(self):
        """Test conference name and year extraction."""
        # Test Laracon formats
        conf, year = self.aggregator._extract_conference_info(
            "Talk at Laracon US 2024",
            "Great conference"
        )
        self.assertEqual(conf, "Laracon US 2024")
        self.assertEqual(year, "2024")
        
        conf, year = self.aggregator._extract_conference_info(
            "Laracon EU 2023 Keynote",
            ""
        )
        self.assertEqual(conf, "Laracon EU 2023")
        self.assertEqual(year, "2023")
        
        # Test other conference formats
        conf, year = self.aggregator._extract_conference_info(
            "Laravel Live UK 2024",
            "Conference talk"
        )
        self.assertEqual(conf, "Laravel Live UK 2024")
        self.assertEqual(year, "2024")
        
    def test_extract_tech_tags(self):
        """Test technology tag extraction."""
        tags = self.aggregator._extract_tech_tags(
            "Building with Livewire and Alpine",
            "Learn about Livewire components and Alpine.js integration"
        )
        self.assertIn('livewire', tags)
        self.assertIn('alpine', tags)
        
        tags = self.aggregator._extract_tech_tags(
            "Testing Laravel Apps with Pest",
            "Advanced testing strategies using Pest PHP"
        )
        self.assertIn('pest', tags)
        self.assertIn('testing', tags)
        
    def test_estimate_talk_difficulty(self):
        """Test difficulty estimation."""
        # Beginner
        self.assertEqual(
            self.aggregator._estimate_talk_difficulty(
                "Getting Started with Laravel",
                "Introduction for beginners"
            ),
            DifficultyLevel.BEGINNER
        )
        
        # Expert
        self.assertEqual(
            self.aggregator._estimate_talk_difficulty(
                "Laravel Internals Deep Dive",
                "Understanding the framework under the hood"
            ),
            DifficultyLevel.EXPERT
        )
        
        # Advanced
        self.assertEqual(
            self.aggregator._estimate_talk_difficulty(
                "Scaling Laravel Applications",
                "Performance optimization patterns"
            ),
            DifficultyLevel.ADVANCED
        )
        
        # Intermediate (default)
        self.assertEqual(
            self.aggregator._estimate_talk_difficulty(
                "Building a Blog with Laravel",
                "Standard Laravel application"
            ),
            DifficultyLevel.INTERMEDIATE
        )
        
    def test_parse_duration(self):
        """Test duration parsing."""
        # YouTube API format
        self.assertEqual(
            self.aggregator._parse_duration("PT1H23M45S"),
            "1h 23m"
        )
        
        self.assertEqual(
            self.aggregator._parse_duration("PT45M"),
            "45m"
        )
        
        self.assertEqual(
            self.aggregator._parse_duration("PT30S"),
            "30s"
        )
        
        # Already formatted
        self.assertEqual(
            self.aggregator._parse_duration("45:30"),
            "45:30"
        )
        
    def test_get_curated_talks(self):
        """Test curated talks list."""
        talks = self.aggregator._get_curated_talks()
        
        self.assertIsInstance(talks, list)
        self.assertGreater(len(talks), 0)
        
        # Check structure of first talk
        first_talk = talks[0]
        self.assertIn('title', first_talk)
        self.assertIn('url', first_talk)
        self.assertIn('description', first_talk)
        self.assertIn('video_id', first_talk)
        self.assertIn('youtube.com/watch?v=', first_talk['url'])
        
    @patch('requests.Session.get')
    def test_fetch_without_api(self, mock_get):
        """Test fetching without API."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><script>var ytInitialData = {}</script></html>'
        mock_get.return_value = mock_response
        
        # Mock add_resource to return IDs
        self.mock_fetcher.add_resource.return_value = 1
        
        talks = self.aggregator._fetch_without_api(max_videos=5)
        
        # Should return some talks (from curated list at minimum)
        self.assertIsInstance(talks, list)
        self.assertGreater(len(talks), 0)
        
    def test_add_video_resource(self):
        """Test adding video resource to database."""
        video_info = {
            'title': 'Laravel 11 - Taylor Otwell at Laracon US 2024',
            'url': 'https://www.youtube.com/watch?v=test123',
            'description': 'New features in Laravel 11',
            'channel': 'Laravel',
            'video_id': 'test123',
            'duration': 'PT45M30S',
            'speaker': 'Taylor Otwell',
            'conference': 'Laracon US 2024'
        }
        
        self.mock_fetcher.add_resource.return_value = 123
        
        resource_id = self.aggregator._add_video_resource(video_info)
        
        self.assertEqual(resource_id, 123)
        self.mock_fetcher.add_resource.assert_called_once()
        
        # Check call arguments
        call_args = self.mock_fetcher.add_resource.call_args[1]
        self.assertEqual(call_args['title'], video_info['title'])
        self.assertEqual(call_args['url'], video_info['url'])
        self.assertIn('conference-talk', call_args['tags'])
        self.assertIn('video', call_args['tags'])
        self.assertIn('2024', call_args['tags'])
        
    def test_backward_compatibility(self):
        """Test that add_known_talks still works."""
        self.mock_fetcher.add_resource.return_value = 1
        
        talks = self.aggregator.add_known_talks()
        
        self.assertIsInstance(talks, list)
        # Should call fetch_conference_talks internally
        self.assertGreater(len(talks), 0)


if __name__ == '__main__':
    unittest.main()