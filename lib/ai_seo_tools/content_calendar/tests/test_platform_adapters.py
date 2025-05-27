import unittest
from typing import Dict, Any
from datetime import datetime

from ..integrations.platform_adapters import UnifiedPlatformAdapter

class TestUnifiedPlatformAdapter(unittest.TestCase):
    """Test cases for the UnifiedPlatformAdapter."""
    
    def setUp(self):
        """Set up test cases."""
        self.adapter = UnifiedPlatformAdapter()
        self.test_content = {
            'title': 'Test Content',
            'content': 'This is a test content for platform adaptation.',
            'keywords': ['test', 'content', 'platform'],
            'tone': 'professional',
            'cta': 'Learn More',
            'audience': 'For All',
            'language': 'English',
            'industry': 'technology',
            'word_count': 1000
        }
    
    def test_adapt_instagram_content(self):
        """Test Instagram content adaptation."""
        adapted_content = self.adapter.adapt_content(
            content=self.test_content,
            platform='instagram'
        )
        
        self.assertIsInstance(adapted_content, dict)
        self.assertIn('captions', adapted_content)
        self.assertIn('hashtags', adapted_content)
        self.assertIn('media_suggestions', adapted_content)
        self.assertIn('platform_specific', adapted_content)
    
    def test_adapt_twitter_content(self):
        """Test Twitter content adaptation."""
        adapted_content = self.adapter.adapt_content(
            content=self.test_content,
            platform='twitter'
        )
        
        self.assertIsInstance(adapted_content, dict)
        self.assertIn('tweets', adapted_content)
        self.assertIn('thread_structure', adapted_content)
        self.assertIn('media_suggestions', adapted_content)
        self.assertIn('platform_specific', adapted_content)
    
    def test_adapt_linkedin_content(self):
        """Test LinkedIn content adaptation."""
        adapted_content = self.adapter.adapt_content(
            content=self.test_content,
            platform='linkedin'
        )
        
        self.assertIsInstance(adapted_content, dict)
        self.assertIn('post', adapted_content)
        self.assertIn('engagement_optimization', adapted_content)
        self.assertIn('media_suggestions', adapted_content)
        self.assertIn('platform_specific', adapted_content)
    
    def test_adapt_blog_content(self):
        """Test blog content adaptation."""
        adapted_content = self.adapter.adapt_content(
            content=self.test_content,
            platform='blog'
        )
        
        self.assertIsInstance(adapted_content, dict)
        self.assertIn('post', adapted_content)
        self.assertIn('seo_optimization', adapted_content)
        self.assertIn('media_suggestions', adapted_content)
        self.assertIn('platform_specific', adapted_content)
    
    def test_adapt_facebook_content(self):
        """Test Facebook content adaptation."""
        adapted_content = self.adapter.adapt_content(
            content=self.test_content,
            platform='facebook'
        )
        
        self.assertIsInstance(adapted_content, dict)
        self.assertIn('post', adapted_content)
        self.assertIn('engagement_optimization', adapted_content)
        self.assertIn('media_suggestions', adapted_content)
        self.assertIn('platform_specific', adapted_content)
    
    def test_validate_content(self):
        """Test content validation."""
        # Test valid content
        self.assertTrue(
            self.adapter.validate_content(
                self.test_content,
                'instagram'
            )
        )
        
        # Test invalid content (missing required fields)
        invalid_content = {
            'title': 'Test Content',
            'content': 'This is a test content.'
        }
        self.assertFalse(
            self.adapter.validate_content(
                invalid_content,
                'instagram'
            )
        )
    
    def test_unsupported_platform(self):
        """Test handling of unsupported platform."""
        with self.assertRaises(ValueError):
            self.adapter.adapt_content(
                content=self.test_content,
                platform='unsupported_platform'
            )
    
    def test_content_adaptation_with_context(self):
        """Test content adaptation with additional context."""
        context = {
            'target_audience': 'professionals',
            'campaign_goals': ['awareness', 'engagement'],
            'brand_voice': 'authoritative'
        }
        
        adapted_content = self.adapter.adapt_content(
            content=self.test_content,
            platform='linkedin',
            context=context
        )
        
        self.assertIsInstance(adapted_content, dict)
        self.assertIn('post', adapted_content)
        self.assertIn('engagement_optimization', adapted_content)
    
    def test_error_handling(self):
        """Test error handling in content adaptation."""
        # Test with invalid content structure
        invalid_content = {
            'title': 123,  # Invalid type
            'content': None  # Missing required field
        }
        
        adapted_content = self.adapter.adapt_content(
            content=invalid_content,
            platform='blog'
        )
        
        self.assertIn('error', adapted_content)
    
    def test_platform_specs(self):
        """Test platform specifications."""
        specs = self.adapter.platform_specs
        
        # Check Instagram specs
        self.assertIn('instagram', specs)
        self.assertIn('max_caption_length', specs['instagram'])
        self.assertIn('max_hashtags', specs['instagram'])
        self.assertIn('required_fields', specs['instagram'])
        
        # Check Twitter specs
        self.assertIn('twitter', specs)
        self.assertIn('max_tweet_length', specs['twitter'])
        self.assertIn('max_thread_length', specs['twitter'])
        self.assertIn('required_fields', specs['twitter'])
        
        # Check LinkedIn specs
        self.assertIn('linkedin', specs)
        self.assertIn('max_post_length', specs['linkedin'])
        self.assertIn('required_fields', specs['linkedin'])
        
        # Check blog specs
        self.assertIn('blog', specs)
        self.assertIn('min_word_count', specs['blog'])
        self.assertIn('max_word_count', specs['blog'])
        self.assertIn('required_fields', specs['blog'])
        
        # Check Facebook specs
        self.assertIn('facebook', specs)
        self.assertIn('max_post_length', specs['facebook'])
        self.assertIn('required_fields', specs['facebook'])

if __name__ == '__main__':
    unittest.main() 