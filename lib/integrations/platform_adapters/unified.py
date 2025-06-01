"""
Unified platform adapter for content adaptation across different platforms.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger

from lib.utils.website_analyzer.analyzer import WebsiteAnalyzer
from lib.ai_seo_tools.content_gap_analysis.main import ContentGapAnalysis
from lib.ai_seo_tools.content_title_generator import ai_title_generator
from lib.ai_seo_tools.meta_desc_generator import metadesc_generator_main
from lib.ai_seo_tools.seo_structured_data import ai_structured_data

class UnifiedPlatformAdapter:
    """Unified adapter for different social media platforms."""
    
    def __init__(self):
        """Initialize the platform adapter."""
        self.platform_handlers = {
            'instagram': self._handle_instagram,
            'linkedin': self._handle_linkedin,
            'twitter': self._handle_twitter,
            'facebook': self._handle_facebook
        }
        logger.info("UnifiedPlatformAdapter initialized")
    
    def generate_content(self, platform: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate content for a specific platform.
        
        Args:
            platform: Target platform
            data: Content data
            
        Returns:
            Dictionary containing generated content
        """
        try:
            handler = self.platform_handlers.get(platform.lower())
            if not handler:
                raise ValueError(f"Unsupported platform: {platform}")
            
            return handler(data)
            
        except Exception as e:
            error_msg = f"Error generating content for {platform}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'error': error_msg,
                'content': None
            }
    
    def get_content_performance(self, content_item: Dict[str, Any]) -> Dict[str, Any]:
        """Get performance metrics for content across platforms."""
        try:
            logger.info(f"Getting performance metrics for content: {content_item.get('title', 'Untitled')}")
            
            # Get platform from content item
            platform = content_item.get('platforms', ['Unknown'])[0]
            
            # Initialize performance metrics
            performance = {
                'engagement_metrics': {
                    'likes': 0,
                    'comments': 0,
                    'shares': 0,
                    'reach': 0
                },
                'seo_metrics': {
                    'impressions': 0,
                    'clicks': 0,
                    'ctr': 0,
                    'position': 0
                },
                'conversion_metrics': {
                    'conversions': 0,
                    'conversion_rate': 0,
                    'revenue': 0
                },
                'platform_specific': {},
                'performance_trends': [],
                'recommendations': []
            }
            
            # Add platform-specific metrics
            if platform == 'WEBSITE':
                performance['platform_specific'] = {
                    'bounce_rate': 0,
                    'time_on_page': 0,
                    'page_views': 0
                }
            
            return performance
            
        except Exception as e:
            error_msg = f"Error getting content performance: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'error': error_msg,
                'metrics': {},
                'trends': {},
                'recommendations': []
            }
    
    def _handle_instagram(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Instagram content generation."""
        try:
            # Generate Instagram-specific content
            caption = metadesc_generator_main(data)
            hashtags = self._generate_hashtags(data)
            
            return {
                'platform': 'instagram',
                'content': {
                    'caption': caption,
                    'hashtags': hashtags,
                    'media_suggestions': self._get_media_suggestions(data)
                }
            }
        except Exception as e:
            logger.error(f"Error generating Instagram content: {str(e)}")
            return {
                'platform': 'instagram',
                'error': str(e)
            }
    
    def _handle_linkedin(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle LinkedIn content generation."""
        try:
            # Generate LinkedIn-specific content
            post = metadesc_generator_main(data)
            
            return {
                'platform': 'linkedin',
                'content': {
                    'post': post,
                    'engagement_optimization': self._get_engagement_suggestions(data),
                    'media_suggestions': self._get_media_suggestions(data)
                }
            }
        except Exception as e:
            logger.error(f"Error generating LinkedIn content: {str(e)}")
            return {
                'platform': 'linkedin',
                'error': str(e)
            }
    
    def _handle_twitter(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Twitter content generation."""
        try:
            # Generate Twitter-specific content
            tweet = metadesc_generator_main(data)
            hashtags = self._generate_hashtags(data)
            
            return {
                'platform': 'twitter',
                'content': {
                    'tweet': tweet,
                    'hashtags': hashtags,
                    'thread_structure': self._get_thread_structure(data),
                    'media_suggestions': self._get_media_suggestions(data)
                }
            }
        except Exception as e:
            logger.error(f"Error generating Twitter content: {str(e)}")
            return {
                'platform': 'twitter',
                'error': str(e)
            }
    
    def _handle_facebook(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Facebook content generation."""
        try:
            # Generate Facebook-specific content
            post = metadesc_generator_main(data)
            
            return {
                'platform': 'facebook',
                'content': {
                    'post': post,
                    'engagement_optimization': self._get_engagement_suggestions(data),
                    'media_suggestions': self._get_media_suggestions(data)
                }
            }
        except Exception as e:
            logger.error(f"Error generating Facebook content: {str(e)}")
            return {
                'platform': 'facebook',
                'error': str(e)
            }
    
    def _generate_hashtags(self, data: Dict[str, Any]) -> List[str]:
        """Generate relevant hashtags for content."""
        try:
            # Extract keywords from content
            keywords = data.get('keywords', [])
            
            # Add platform-specific hashtags
            platform = data.get('platform', '').lower()
            platform_hashtags = {
                'instagram': ['#instagood', '#photooftheday'],
                'twitter': ['#trending', '#followme'],
                'linkedin': ['#business', '#professional'],
                'facebook': ['#social', '#community']
            }.get(platform, [])
            
            return keywords + platform_hashtags
            
        except Exception as e:
            logger.error(f"Error generating hashtags: {str(e)}")
            return []
    
    def _get_media_suggestions(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get media suggestions for content."""
        try:
            # Generate media suggestions based on content type
            content_type = data.get('type', 'post')
            
            suggestions = []
            if content_type == 'blog':
                suggestions.append({
                    'type': 'featured_image',
                    'description': 'Main blog post image',
                    'dimensions': '1200x630'
                })
            elif content_type == 'social':
                suggestions.append({
                    'type': 'post_image',
                    'description': 'Social media post image',
                    'dimensions': '1080x1080'
                })
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error getting media suggestions: {str(e)}")
            return []
    
    def _get_engagement_suggestions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get engagement optimization suggestions."""
        try:
            return {
                'best_posting_times': ['9:00 AM', '5:00 PM'],
                'engagement_tips': [
                    'Ask questions to encourage comments',
                    'Use relevant hashtags',
                    'Include a clear call-to-action'
                ],
                'content_length': {
                    'optimal': '150-200 characters',
                    'maximum': '300 characters'
                }
            }
        except Exception as e:
            logger.error(f"Error getting engagement suggestions: {str(e)}")
            return {}
    
    def _get_thread_structure(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get thread structure for Twitter threads."""
        try:
            content = data.get('content', '')
            sentences = content.split('.')
            
            thread = []
            current_tweet = ''
            
            for sentence in sentences:
                if len(current_tweet + sentence) <= 280:
                    current_tweet += sentence + '.'
                else:
                    if current_tweet:
                        thread.append({
                            'content': current_tweet.strip(),
                            'type': 'tweet'
                        })
                    current_tweet = sentence + '.'
            
            if current_tweet:
                thread.append({
                    'content': current_tweet.strip(),
                    'type': 'tweet'
                })
            
            return thread
            
        except Exception as e:
            logger.error(f"Error generating thread structure: {str(e)}")
            return [] 