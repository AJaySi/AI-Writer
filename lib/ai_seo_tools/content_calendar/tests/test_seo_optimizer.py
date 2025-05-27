import unittest
from datetime import datetime
from typing import Dict, Any

from ..integrations.seo_optimizer import SEOOptimizer

class TestSEOOptimizer(unittest.TestCase):
    """Test cases for the SEOOptimizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.seo_optimizer = SEOOptimizer()
        
        # Sample content for testing
        self.sample_content = {
            'title': 'The Future of AI in Content Marketing',
            'content': 'AI is revolutionizing content marketing...',
            'keywords': ['AI', 'content marketing', 'automation'],
            'author': 'John Doe',
            'publish_date': datetime.now().isoformat(),
            'description': 'An in-depth look at AI in content marketing',
            'image_url': 'https://example.com/image.jpg',
            'url': 'https://example.com/article'
        }
        
        # Sample calendar for testing
        self.sample_calendar = {
            'metadata': {
                'start_date': datetime.now().isoformat(),
                'end_date': datetime.now().isoformat(),
                'platforms': ['blog', 'social'],
                'content_types': ['article']
            },
            'content_items': [self.sample_content]
        }
    
    def test_optimize_content(self):
        """Test content optimization."""
        optimized = self.seo_optimizer.optimize_content(
            content=self.sample_content,
            content_type='article',
            language='English',
            search_intent='Informational Intent'
        )
        
        # Check structure
        self.assertIn('original_content', optimized)
        self.assertIn('seo_optimized', optimized)
        
        # Check SEO elements
        seo_elements = optimized['seo_optimized']
        self.assertIn('title', seo_elements)
        self.assertIn('meta_description', seo_elements)
        self.assertIn('structured_data', seo_elements)
        self.assertIn('keywords', seo_elements)
    
    def test_optimize_title(self):
        """Test title optimization."""
        titles = self.seo_optimizer._optimize_title(
            title=self.sample_content['title'],
            keywords=self.sample_content['keywords'],
            content_type='article',
            language='English',
            search_intent='Informational Intent'
        )
        
        # Check titles
        self.assertIsInstance(titles, list)
        self.assertTrue(len(titles) > 0)
    
    def test_generate_meta_description(self):
        """Test meta description generation."""
        descriptions = self.seo_optimizer._generate_meta_description(
            keywords=self.sample_content['keywords'],
            content_type='article',
            language='English',
            search_intent='Informational Intent'
        )
        
        # Check descriptions
        self.assertIsInstance(descriptions, list)
        self.assertTrue(len(descriptions) > 0)
    
    def test_generate_structured_data(self):
        """Test structured data generation."""
        structured_data = self.seo_optimizer._generate_structured_data(
            content=self.sample_content,
            content_type='article'
        )
        
        # Check structured data
        self.assertIsNotNone(structured_data)
    
    def test_optimize_calendar_content(self):
        """Test calendar content optimization."""
        optimized_calendar = self.seo_optimizer.optimize_calendar_content(
            calendar=self.sample_calendar,
            content_type='article',
            language='English',
            search_intent='Informational Intent'
        )
        
        # Check structure
        self.assertIn('metadata', optimized_calendar)
        self.assertIn('content_items', optimized_calendar)
        
        # Check content items
        self.assertTrue(len(optimized_calendar['content_items']) > 0)
        for item in optimized_calendar['content_items']:
            self.assertIn('original_content', item)
            self.assertIn('seo_optimized', item)
    
    def test_error_handling(self):
        """Test error handling with invalid inputs."""
        # Test with invalid content
        invalid_content = {'title': 'Invalid Content'}
        optimized = self.seo_optimizer.optimize_content(
            content=invalid_content,
            content_type='article'
        )
        self.assertIn('error', optimized)
        
        # Test with invalid calendar
        invalid_calendar = {'metadata': {}}
        optimized_calendar = self.seo_optimizer.optimize_calendar_content(
            calendar=invalid_calendar,
            content_type='article'
        )
        self.assertIn('error', optimized_calendar)

if __name__ == '__main__':
    unittest.main() 