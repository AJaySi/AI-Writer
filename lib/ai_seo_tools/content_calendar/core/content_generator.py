from typing import Dict, List, Any, Optional
import logging
from pathlib import Path
import sys

# Add parent directory to path to import existing tools
parent_dir = str(Path(__file__).parent.parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from ..models.calendar import ContentItem, ContentType
from ..utils.error_handling import handle_calendar_error
from lib.ai_seo_tools.content_gap_analysis.main import ContentGapAnalysis
from lib.ai_seo_tools.content_title_generator import ai_title_generator
from lib.ai_seo_tools.meta_desc_generator import metadesc_generator_main

logger = logging.getLogger(__name__)

class ContentGenerator:
    """
    AI-powered content generation for content briefs.
    """
    
    def __init__(self):
        self.logger = logging.getLogger('content_calendar.content_generator')
        self.logger.info("Initializing ContentGenerator")
        self._setup_logging()
        self._load_ai_tools()
    
    def _setup_logging(self):
        """Configure logging for content generator."""
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    def _load_ai_tools(self):
        """Load and initialize AI tools."""
        try:
            # Initialize AI tools
            self.gap_analyzer = ContentGapAnalysis()
            self.title_generator = ai_title_generator
            self.meta_generator = metadesc_generator_main
            
        except Exception as e:
            logger.error(f"Error loading AI tools: {str(e)}")
            raise
    
    @handle_calendar_error
    def generate_headings(
        self,
        content_item: ContentItem,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate main headings for content.
        
        Args:
            content_item: Content item to generate headings for
            context: Content context from gap analysis
            
        Returns:
            List of main headings with metadata
        """
        try:
            # Use AI to generate headings based on content type and context
            headings = self._generate_ai_headings(
                title=content_item.title,
                content_type=content_item.content_type,
                context=context
            )
            
            # Format and validate headings
            formatted_headings = []
            for heading in headings:
                formatted_heading = {
                    'title': heading['title'],
                    'level': heading.get('level', 1),
                    'keywords': heading.get('keywords', []),
                    'summary': heading.get('summary', '')
                }
                formatted_headings.append(formatted_heading)
            
            return formatted_headings
            
        except Exception as e:
            logger.error(f"Error generating headings: {str(e)}")
            return []
    
    @handle_calendar_error
    def generate_subheadings(
        self,
        content_item: ContentItem,
        main_headings: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate subheadings for each main heading.
        
        Args:
            content_item: Content item to generate subheadings for
            main_headings: List of main headings
            context: Content context from gap analysis
            
        Returns:
            Dictionary mapping main headings to their subheadings
        """
        try:
            subheadings = {}
            
            for heading in main_headings:
                # Generate subheadings for each main heading
                heading_subheadings = self._generate_ai_subheadings(
                    main_heading=heading,
                    content_type=content_item.content_type,
                    context=context
                )
                
                # Format and validate subheadings
                formatted_subheadings = []
                for subheading in heading_subheadings:
                    formatted_subheading = {
                        'title': subheading['title'],
                        'level': subheading.get('level', 2),
                        'keywords': subheading.get('keywords', []),
                        'summary': subheading.get('summary', '')
                    }
                    formatted_subheadings.append(formatted_subheading)
                
                subheadings[heading['title']] = formatted_subheadings
            
            return subheadings
            
        except Exception as e:
            logger.error(f"Error generating subheadings: {str(e)}")
            return {}
    
    @handle_calendar_error
    def generate_key_points(
        self,
        content_item: ContentItem,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate key points for the content.
        
        Args:
            content_item: Content item to generate key points for
            context: Content context from gap analysis
            
        Returns:
            List of key points with supporting information
        """
        try:
            # Generate key points using AI
            key_points = self._generate_ai_key_points(
                title=content_item.title,
                content_type=content_item.content_type,
                context=context
            )
            
            # Format and validate key points
            formatted_points = []
            for point in key_points:
                formatted_point = {
                    'point': point['point'],
                    'importance': point.get('importance', 'medium'),
                    'supporting_evidence': point.get('evidence', []),
                    'related_keywords': point.get('keywords', [])
                }
                formatted_points.append(formatted_point)
            
            return formatted_points
            
        except Exception as e:
            logger.error(f"Error generating key points: {str(e)}")
            return []
    
    @handle_calendar_error
    def generate_content_flow(
        self,
        content_item: ContentItem,
        outline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate content flow and structure.
        
        Args:
            content_item: Content item to generate flow for
            outline: Content outline with headings and key points
            
        Returns:
            Dictionary containing content flow and structure
        """
        try:
            # Generate content flow using AI
            flow = self._generate_ai_content_flow(
                title=content_item.title,
                content_type=content_item.content_type,
                outline=outline
            )
            
            return {
                'introduction': flow.get('introduction', {}),
                'main_sections': flow.get('main_sections', []),
                'conclusion': flow.get('conclusion', {}),
                'transitions': flow.get('transitions', []),
                'content_pacing': flow.get('pacing', {})
            }
            
        except Exception as e:
            logger.error(f"Error generating content flow: {str(e)}")
            return {}
    
    def _generate_ai_headings(
        self,
        title: str,
        content_type: ContentType,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Use AI to generate content headings.
        """
        # TODO: Implement AI heading generation
        # This would use the existing AI tools to generate headings
        return []
    
    def _generate_ai_subheadings(
        self,
        main_heading: Dict[str, Any],
        content_type: ContentType,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Use AI to generate subheadings.
        """
        # TODO: Implement AI subheading generation
        return []
    
    def _generate_ai_key_points(
        self,
        title: str,
        content_type: ContentType,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Use AI to generate key points.
        """
        # TODO: Implement AI key point generation
        return []
    
    def _generate_ai_content_flow(
        self,
        title: str,
        content_type: ContentType,
        outline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Use AI to generate content flow.
        """
        # TODO: Implement AI content flow generation
        return {}
    
    def generate_variation(self, content: Dict[str, Any], variation_type: str) -> Dict[str, Any]:
        """Generate a variation of the given content.
        
        Args:
            content: Original content to vary
            variation_type: Type of variation to generate ('tone', 'length', 'style', etc.)
            
        Returns:
            Dictionary containing the varied content
        """
        try:
            self.logger.info(f"Generating {variation_type} variation for content")
            
            # Generate variation based on type
            variation = {
                'title': f"{content.get('title', '')} - {variation_type.title()} Variation",
                'content_flow': {
                    'introduction': {
                        'summary': f"Varied introduction for {content.get('title', '')}",
                        'key_points': [
                            f"Varied key point 1 for {variation_type}",
                            f"Varied key point 2 for {variation_type}",
                            f"Varied key point 3 for {variation_type}"
                        ]
                    },
                    'main_content': {
                        'sections': [
                            {
                                'title': f"Varied Section 1: {variation_type.title()} Approach",
                                'content': f"Varied content for {variation_type}",
                                'subsections': []
                            },
                            {
                                'title': f"Varied Section 2: {variation_type.title()} Details",
                                'content': "Varied details and information",
                                'subsections': []
                            }
                        ]
                    },
                    'conclusion': {
                        'summary': f"Varied conclusion for {variation_type}",
                        'call_to_action': "Varied call to action"
                    }
                },
                'metadata': {
                    'variation_type': variation_type,
                    'original_content': content.get('title', ''),
                    'platform': content.get('metadata', {}).get('platform', 'Unknown'),
                    'content_type': content.get('metadata', {}).get('content_type', 'Unknown')
                }
            }
            
            return variation
            
        except Exception as e:
            self.logger.error(f"Error generating variation: {str(e)}")
            return {} 