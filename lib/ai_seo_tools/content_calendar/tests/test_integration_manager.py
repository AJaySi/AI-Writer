import unittest
from datetime import datetime, timedelta
from typing import Dict, Any

from ..integrations.integration_manager import IntegrationManager

class TestIntegrationManager(unittest.TestCase):
    """Test cases for the IntegrationManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.integration_manager = IntegrationManager()
        self.start_date = datetime.now()
        self.end_date = self.start_date + timedelta(days=30)
        self.platforms = ['instagram', 'twitter', 'linkedin', 'blog', 'facebook']
        self.content_types = ['article', 'social', 'video']
        self.target_audience = {
            'age_range': '25-34',
            'interests': ['technology', 'marketing'],
            'location': 'global'
        }
        self.industry = 'technology'
        self.keywords = ['AI', 'content marketing', 'social media']
        
        # Sample content item
        self.sample_content = {
            'title': 'The Future of AI in Content Marketing',
            'content': 'AI is revolutionizing content marketing...',
            'content_type': 'article',
            'keywords': ['AI', 'content marketing', 'automation'],
            'target_audience': self.target_audience,
            'industry': self.industry
        }
    
    def test_create_cross_platform_calendar(self):
        """Test creating a cross-platform content calendar."""
        calendar = self.integration_manager.create_cross_platform_calendar(
            start_date=self.start_date,
            end_date=self.end_date,
            platforms=self.platforms,
            content_types=self.content_types,
            target_audience=self.target_audience,
            industry=self.industry,
            keywords=self.keywords
        )
        
        # Check basic structure
        self.assertIn('base_calendar', calendar)
        self.assertIn('platform_calendars', calendar)
        self.assertIn('metadata', calendar)
        
        # Check platform calendars
        platform_calendars = calendar['platform_calendars']
        self.assertEqual(len(platform_calendars), len(self.platforms))
        
        for platform in self.platforms:
            self.assertIn(platform, platform_calendars)
            platform_calendar = platform_calendars[platform]
            self.assertIn('content_items', platform_calendar)
            self.assertIn('metadata', platform_calendar)
    
    def test_adapt_calendar_for_platform(self):
        """Test adapting calendar for a specific platform."""
        # Create base calendar
        calendar = self.integration_manager.create_cross_platform_calendar(
            start_date=self.start_date,
            end_date=self.end_date,
            platforms=[self.platforms[0]],  # Test with just Instagram
            content_types=self.content_types,
            target_audience=self.target_audience,
            industry=self.industry,
            keywords=self.keywords
        )
        
        # Get platform calendar
        platform_calendar = calendar['platform_calendars'][self.platforms[0]]
        
        # Check structure
        self.assertIn('content_items', platform_calendar)
        self.assertIn('metadata', platform_calendar)
        
        # Check content items
        for item in platform_calendar['content_items']:
            self.assertIn('original_item', item)
            self.assertIn('adapted_content', item)
            self.assertIn('platform_specifics', item)
    
    def test_adapt_content_item(self):
        """Test adapting a content item for a platform."""
        adapted_item = self.integration_manager._adapt_content_item(
            item=self.sample_content,
            platform='instagram'
        )
        
        # Check structure
        self.assertIsNotNone(adapted_item)
        self.assertIn('original_item', adapted_item)
        self.assertIn('adapted_content', adapted_item)
        self.assertIn('platform_specifics', adapted_item)
        
        # Check content adaptation
        adapted_content = adapted_item['adapted_content']
        self.assertIn('captions', adapted_content)
        self.assertIn('hashtags', adapted_content)
        self.assertIn('media_suggestions', adapted_content)
    
    def test_get_platform_suggestions(self):
        """Test getting platform-specific suggestions."""
        suggestions = self.integration_manager.get_platform_suggestions(
            content=self.sample_content,
            platforms=self.platforms
        )
        
        # Check structure
        self.assertEqual(len(suggestions), len(self.platforms))
        
        for platform in self.platforms:
            self.assertIn(platform, suggestions)
            platform_suggestions = suggestions[platform]
            self.assertIsInstance(platform_suggestions, dict)
    
    def test_validate_platform_content(self):
        """Test validating content for a platform."""
        validation = self.integration_manager.validate_platform_content(
            content=self.sample_content,
            platform='instagram'
        )
        
        # Check structure
        self.assertIn('platform', validation)
        self.assertIn('is_valid', validation)
        self.assertIn('specifications', validation)
        
        # Check validation result
        self.assertIsInstance(validation['is_valid'], bool)
    
    def test_optimize_cross_platform_content(self):
        """Test optimizing content for multiple platforms."""
        optimized = self.integration_manager.optimize_cross_platform_content(
            content=self.sample_content,
            platforms=self.platforms
        )
        
        # Check structure
        self.assertEqual(len(optimized), len(self.platforms))
        
        for platform in self.platforms:
            self.assertIn(platform, optimized)
            platform_optimized = optimized[platform]
            self.assertIsInstance(platform_optimized, dict)
    
    def test_error_handling(self):
        """Test error handling with invalid inputs."""
        # Test with invalid platform
        with self.assertRaises(Exception):
            self.integration_manager.validate_platform_content(
                content=self.sample_content,
                platform='invalid_platform'
            )
        
        # Test with invalid content
        invalid_content = {'title': 'Invalid Content'}
        validation = self.integration_manager.validate_platform_content(
            content=invalid_content,
            platform='instagram'
        )
        self.assertFalse(validation['is_valid'])
        self.assertIn('error', validation)

if __name__ == '__main__':
    unittest.main() 