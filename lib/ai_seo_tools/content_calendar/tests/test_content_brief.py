import unittest
from datetime import datetime
from typing import Dict, Any

from ..models.calendar import ContentItem, ContentType, Platform, SEOData
from ..core.content_brief import ContentBriefGenerator

class TestContentBriefGenerator(unittest.TestCase):
    """Test cases for ContentBriefGenerator."""
    
    def setUp(self):
        """Set up test cases."""
        self.generator = ContentBriefGenerator()
        self.test_content_item = self._create_test_content_item()
    
    def _create_test_content_item(self) -> ContentItem:
        """Create a test content item."""
        return ContentItem(
            id="test-001",
            title="10 Ways to Improve Your SEO Strategy",
            description="A comprehensive guide to enhancing your website's SEO performance",
            content_type=ContentType.BLOG_POST,
            platforms=[Platform.WEBSITE, Platform.LINKEDIN],
            publish_date=datetime.now(),
            seo_data=SEOData(
                keywords=["SEO", "search engine optimization", "digital marketing"],
                meta_description="Learn effective SEO strategies to boost your website's visibility",
                structured_data={}
            ),
            platform_specs={
                "website": {
                    "format": "blog post",
                    "min_length": 1500
                },
                "linkedin": {
                    "format": "article",
                    "min_length": 800
                }
            },
            context={
                "website_url": "https://example.com",
                "target_audience": "digital marketers",
                "content_goals": ["educate", "generate leads"]
            }
        )
    
    def test_generate_brief(self):
        """Test content brief generation."""
        # Generate brief
        brief = self.generator.generate_brief(
            content_item=self.test_content_item,
            target_audience={
                "demographics": {
                    "age_range": "25-45",
                    "profession": "digital marketers"
                },
                "interests": ["SEO", "content marketing", "digital strategy"],
                "pain_points": [
                    "low search rankings",
                    "poor content performance",
                    "lack of organic traffic"
                ]
            }
        )
        
        # Verify brief structure
        self.assertIsInstance(brief, dict)
        self.assertIn('title', brief)
        self.assertIn('content_type', brief)
        self.assertIn('outline', brief)
        self.assertIn('key_points', brief)
        self.assertIn('content_flow', brief)
        self.assertIn('target_audience', brief)
        self.assertIn('seo_data', brief)
        self.assertIn('platform_specs', brief)
        
        # Verify outline structure
        outline = brief['outline']
        self.assertIn('main_headings', outline)
        self.assertIn('subheadings', outline)
        
        # Verify key points
        self.assertIsInstance(brief['key_points'], list)
        
        # Verify content flow
        flow = brief['content_flow']
        self.assertIn('introduction', flow)
        self.assertIn('main_sections', flow)
        self.assertIn('conclusion', flow)
        self.assertIn('transitions', flow)
        self.assertIn('content_pacing', flow)
    
    def test_generate_brief_without_audience(self):
        """Test content brief generation without target audience data."""
        brief = self.generator.generate_brief(
            content_item=self.test_content_item
        )
        
        self.assertIsInstance(brief, dict)
        self.assertIn('target_audience', brief)
        self.assertEqual(brief['target_audience'], {})
    
    def test_generate_outline(self):
        """Test outline generation."""
        outline = self.generator._generate_outline(self.test_content_item)
        
        self.assertIsInstance(outline, dict)
        self.assertIn('main_headings', outline)
        self.assertIn('subheadings', outline)
        
        # Verify main headings
        main_headings = outline['main_headings']
        self.assertIsInstance(main_headings, list)
        for heading in main_headings:
            self.assertIn('title', heading)
            self.assertIn('level', heading)
            self.assertIn('keywords', heading)
            self.assertIn('summary', heading)
        
        # Verify subheadings
        subheadings = outline['subheadings']
        self.assertIsInstance(subheadings, dict)
        for heading_title, heading_subheadings in subheadings.items():
            self.assertIsInstance(heading_subheadings, list)
            for subheading in heading_subheadings:
                self.assertIn('title', subheading)
                self.assertIn('level', subheading)
                self.assertIn('keywords', subheading)
                self.assertIn('summary', subheading)

if __name__ == '__main__':
    unittest.main() 