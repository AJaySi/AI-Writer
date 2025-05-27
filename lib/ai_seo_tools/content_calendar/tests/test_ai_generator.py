import unittest
from typing import Dict, Any

from ..models.calendar import ContentType
from ..core.ai_generator import AIContentGenerator

class TestAIContentGenerator(unittest.TestCase):
    """Test cases for AIContentGenerator."""
    
    def setUp(self):
        """Set up test cases."""
        self.generator = AIContentGenerator()
        self.test_title = "10 Ways to Improve Your SEO Strategy"
        self.test_content_type = ContentType.BLOG_POST
        self.test_context = {
            "website_url": "https://example.com",
            "target_audience": "digital marketers",
            "content_goals": ["educate", "generate leads"]
        }
    
    def test_generate_headings(self):
        """Test heading generation."""
        headings = self.generator.generate_headings(
            title=self.test_title,
            content_type=self.test_content_type,
            context=self.test_context
        )
        
        self.assertIsInstance(headings, list)
        for heading in headings:
            self.assertIn('title', heading)
            self.assertIn('level', heading)
            self.assertIn('keywords', heading)
            self.assertIn('summary', heading)
            
            # Verify heading level
            self.assertEqual(heading['level'], 1)
            
            # Verify heading content
            self.assertIsInstance(heading['title'], str)
            self.assertIsInstance(heading['keywords'], list)
            self.assertIsInstance(heading['summary'], str)
    
    def test_generate_subheadings(self):
        """Test subheading generation."""
        main_heading = {
            'title': 'Understanding SEO Basics',
            'level': 1,
            'keywords': ['SEO', 'basics', 'fundamentals'],
            'summary': 'Introduction to core SEO concepts'
        }
        
        subheadings = self.generator.generate_subheadings(
            main_heading=main_heading,
            content_type=self.test_content_type,
            context=self.test_context
        )
        
        self.assertIsInstance(subheadings, list)
        for subheading in subheadings:
            self.assertIn('title', subheading)
            self.assertIn('level', subheading)
            self.assertIn('keywords', subheading)
            self.assertIn('summary', subheading)
            
            # Verify subheading level
            self.assertEqual(subheading['level'], 2)
            
            # Verify subheading content
            self.assertIsInstance(subheading['title'], str)
            self.assertIsInstance(subheading['keywords'], list)
            self.assertIsInstance(subheading['summary'], str)
    
    def test_generate_key_points(self):
        """Test key points generation."""
        key_points = self.generator.generate_key_points(
            title=self.test_title,
            content_type=self.test_content_type,
            context=self.test_context
        )
        
        self.assertIsInstance(key_points, list)
        for point in key_points:
            self.assertIn('point', point)
            self.assertIn('importance', point)
            self.assertIn('supporting_evidence', point)
            self.assertIn('related_keywords', point)
            
            # Verify point content
            self.assertIsInstance(point['point'], str)
            self.assertIn(point['importance'], ['high', 'medium', 'low'])
            self.assertIsInstance(point['supporting_evidence'], list)
            self.assertIsInstance(point['related_keywords'], list)
    
    def test_generate_content_flow(self):
        """Test content flow generation."""
        outline = {
            'main_headings': [
                {
                    'title': 'Introduction',
                    'level': 1,
                    'keywords': ['SEO', 'introduction'],
                    'summary': 'Overview of SEO importance'
                }
            ],
            'subheadings': {
                'Introduction': [
                    {
                        'title': 'What is SEO?',
                        'level': 2,
                        'keywords': ['definition', 'basics'],
                        'summary': 'Basic definition of SEO'
                    }
                ]
            }
        }
        
        flow = self.generator.generate_content_flow(
            title=self.test_title,
            content_type=self.test_content_type,
            outline=outline
        )
        
        self.assertIsInstance(flow, dict)
        self.assertIn('introduction', flow)
        self.assertIn('main_sections', flow)
        self.assertIn('conclusion', flow)
        self.assertIn('transitions', flow)
        self.assertIn('content_pacing', flow)
        
        # Verify flow content
        self.assertIsInstance(flow['introduction'], dict)
        self.assertIsInstance(flow['main_sections'], list)
        self.assertIsInstance(flow['conclusion'], dict)
        self.assertIsInstance(flow['transitions'], list)
        self.assertIsInstance(flow['content_pacing'], dict)
    
    def test_prompt_creation(self):
        """Test prompt creation methods."""
        # Test heading prompt
        heading_prompt = self.generator._create_heading_prompt(
            title=self.test_title,
            content_type=self.test_content_type,
            gaps={'opportunities': ['keyword research', 'content optimization']}
        )
        self.assertIsInstance(heading_prompt, str)
        self.assertIn(self.test_title, heading_prompt)
        self.assertIn(self.test_content_type.value, heading_prompt)
        
        # Test subheading prompt
        main_heading = {
            'title': 'Understanding SEO Basics',
            'level': 1,
            'keywords': ['SEO', 'basics'],
            'summary': 'Introduction to SEO'
        }
        subheading_prompt = self.generator._create_subheading_prompt(
            main_heading=main_heading,
            content_type=self.test_content_type,
            context=self.test_context
        )
        self.assertIsInstance(subheading_prompt, str)
        self.assertIn(main_heading['title'], subheading_prompt)
        
        # Test key points prompt
        key_points_prompt = self.generator._create_key_points_prompt(
            title=self.test_title,
            content_type=self.test_content_type,
            seo_data={'keywords': ['SEO', 'strategy']},
            context=self.test_context
        )
        self.assertIsInstance(key_points_prompt, str)
        self.assertIn(self.test_title, key_points_prompt)
        
        # Test flow prompt
        flow_prompt = self.generator._create_flow_prompt(
            title=self.test_title,
            content_type=self.test_content_type,
            outline={'main_headings': []}
        )
        self.assertIsInstance(flow_prompt, str)
        self.assertIn(self.test_title, flow_prompt)

if __name__ == '__main__':
    unittest.main() 