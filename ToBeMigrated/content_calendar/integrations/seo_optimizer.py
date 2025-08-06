import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from ...meta_desc_generator import generate_blog_metadesc
from ...content_title_generator import generate_blog_titles
from ...seo_structured_data import generate_json_data

logger = logging.getLogger(__name__)

class SEOOptimizer:
    """Integrates SEO tools with content calendar system."""
    
    def __init__(self):
        """Initialize the SEO optimizer."""
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging for SEO optimizer."""
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    def optimize_content(
        self,
        content: Dict[str, Any],
        content_type: str = 'article',
        language: str = 'English',
        search_intent: str = 'Informational Intent'
    ) -> Dict[str, Any]:
        """
        Optimize content for SEO using existing tools.
        
        Args:
            content: Content to optimize
            content_type: Type of content (article, product, etc.)
            language: Content language
            search_intent: Search intent type
            
        Returns:
            Optimized content with SEO elements
        """
        try:
            # Extract content details
            title = content.get('title', '')
            keywords = content.get('keywords', [])
            content_text = content.get('content', '')
            
            # Generate SEO elements
            optimized_title = self._optimize_title(
                title=title,
                keywords=keywords,
                content_type=content_type,
                language=language,
                search_intent=search_intent
            )
            
            meta_description = self._generate_meta_description(
                keywords=keywords,
                content_type=content_type,
                language=language,
                search_intent=search_intent
            )
            
            structured_data = self._generate_structured_data(
                content=content,
                content_type=content_type
            )
            
            return {
                'original_content': content,
                'seo_optimized': {
                    'title': optimized_title,
                    'meta_description': meta_description,
                    'structured_data': structured_data,
                    'keywords': keywords,
                    'content_type': content_type,
                    'language': language,
                    'search_intent': search_intent
                }
            }
            
        except Exception as e:
            logger.error(f"Error optimizing content: {str(e)}")
            return {
                'error': str(e)
            }
    
    def _optimize_title(
        self,
        title: str,
        keywords: List[str],
        content_type: str,
        language: str,
        search_intent: str
    ) -> List[str]:
        """Generate SEO-optimized titles."""
        try:
            # Convert keywords list to comma-separated string
            keywords_str = ', '.join(keywords)
            
            # Generate titles using existing tool
            titles = generate_blog_titles(
                input_blog_keywords=keywords_str,
                input_blog_content=title,
                input_title_type=content_type,
                input_title_intent=search_intent,
                input_language=language
            )
            
            return titles.split('\n') if titles else []
            
        except Exception as e:
            logger.error(f"Error optimizing title: {str(e)}")
            return []
    
    def _generate_meta_description(
        self,
        keywords: List[str],
        content_type: str,
        language: str,
        search_intent: str
    ) -> List[str]:
        """Generate SEO-optimized meta descriptions."""
        try:
            # Convert keywords list to comma-separated string
            keywords_str = ', '.join(keywords)
            
            # Generate meta descriptions using existing tool
            descriptions = generate_blog_metadesc(
                keywords=keywords_str,
                tone='Informative',
                search_type=search_intent,
                language=language
            )
            
            return descriptions.split('\n') if descriptions else []
            
        except Exception as e:
            logger.error(f"Error generating meta description: {str(e)}")
            return []
    
    def _generate_structured_data(
        self,
        content: Dict[str, Any],
        content_type: str
    ) -> Optional[Dict[str, Any]]:
        """Generate structured data for content."""
        try:
            # Prepare content details for structured data
            details = {
                'Headline': content.get('title', ''),
                'Author': content.get('author', ''),
                'Date Published': content.get('publish_date', datetime.now().isoformat()),
                'Keywords': ', '.join(content.get('keywords', [])),
                'Description': content.get('description', ''),
                'Image URL': content.get('image_url', '')
            }
            
            # Generate structured data using existing tool
            structured_data = generate_json_data(
                content_type=content_type,
                details=details,
                url=content.get('url', '')
            )
            
            return structured_data
            
        except Exception as e:
            logger.error(f"Error generating structured data: {str(e)}")
            return None
    
    def optimize_calendar_content(
        self,
        calendar: Dict[str, Any],
        content_type: str = 'article',
        language: str = 'English',
        search_intent: str = 'Informational Intent'
    ) -> Dict[str, Any]:
        """
        Optimize all content in calendar for SEO.
        
        Args:
            calendar: Content calendar to optimize
            content_type: Type of content
            language: Content language
            search_intent: Search intent type
            
        Returns:
            Calendar with SEO-optimized content
        """
        try:
            optimized_calendar = {
                'metadata': calendar.get('metadata', {}),
                'content_items': []
            }
            
            # Optimize each content item
            for item in calendar.get('content_items', []):
                optimized_item = self.optimize_content(
                    content=item,
                    content_type=content_type,
                    language=language,
                    search_intent=search_intent
                )
                if optimized_item:
                    optimized_calendar['content_items'].append(optimized_item)
            
            return optimized_calendar
            
        except Exception as e:
            logger.error(f"Error optimizing calendar content: {str(e)}")
            return {
                'error': str(e)
            } 