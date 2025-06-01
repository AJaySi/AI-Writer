from typing import Dict, List, Any, Optional
import logging
from pathlib import Path
import sys

# Add parent directory to path to import existing tools
parent_dir = str(Path(__file__).parent.parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from lib.database.models import ContentType, ContentItem, Platform
from lib.ai_seo_tools.content_calendar.utils.error_handling import handle_calendar_error
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
from lib.ai_seo_tools.content_gap_analysis.main import ContentGapAnalysis
from lib.ai_seo_tools.content_title_generator import ai_title_generator
from lib.ai_seo_tools.meta_desc_generator import metadesc_generator_main
from .ai_generator import AIGenerator

logger = logging.getLogger(__name__)

class ContentBriefGenerator:
    """
    Generates comprehensive content briefs using AI-powered analysis.
    """
    
    def __init__(self):
        self.logger = logging.getLogger('content_calendar.content_brief')
        self.logger.info("Initializing ContentBriefGenerator")
        self._setup_logging()
        self._load_ai_tools()
    
    def _setup_logging(self):
        """Configure logging for content brief generator."""
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
            self.ai_generator = AIGenerator()
            
        except Exception as e:
            logger.error(f"Error loading AI tools: {str(e)}")
            raise
    
    @handle_calendar_error
    def generate_brief(
        self,
        content_item: ContentItem,
        target_audience: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive content brief.
        
        Args:
            content_item: Content item to generate brief for
            target_audience: Optional target audience data
            
        Returns:
            Dictionary containing the content brief
        """
        try:
            logger.info(f"Generating content brief for: {content_item.title}")
            
            # Generate content outline
            outline = self._generate_outline(content_item)
            
            # Generate key points
            key_points = self.ai_generator.generate_key_points(
                title=content_item.title,
                content_type=content_item.content_type,
                context=content_item.context
            )
            
            # Generate content flow
            content_flow = self.ai_generator.generate_content_flow(
                title=content_item.title,
                content_type=content_item.content_type,
                outline=outline
            )
            
            # Compile the brief
            brief = {
                'title': content_item.title,
                'content_type': content_item.content_type.value,
                'outline': outline,
                'key_points': key_points,
                'content_flow': content_flow,
                'target_audience': target_audience or {},
                'seo_data': content_item.seo_data,
                'platform_specs': content_item.platform_specs
            }
            
            logger.info("Content brief generated successfully")
            return brief
            
        except Exception as e:
            logger.error(f"Error generating content brief: {str(e)}")
            raise
    
    def _generate_outline(
        self,
        content_item: ContentItem
    ) -> Dict[str, Any]:
        """
        Generate content outline with headings and subheadings.
        
        Args:
            content_item: Content item to generate outline for
            
        Returns:
            Dictionary containing the content outline
        """
        try:
            # Generate main headings
            main_headings = self.ai_generator.generate_headings(
                title=content_item.title,
                content_type=content_item.content_type,
                context=content_item.context
            )
            
            # Generate subheadings for each main heading
            subheadings = {}
            for heading in main_headings:
                heading_subheadings = self.ai_generator.generate_subheadings(
                    main_heading=heading,
                    content_type=content_item.content_type,
                    context=content_item.context
                )
                subheadings[heading['title']] = heading_subheadings
            
            return {
                'main_headings': main_headings,
                'subheadings': subheadings
            }
            
        except Exception as e:
            logger.error(f"Error generating outline: {str(e)}")
            return {
                'main_headings': [],
                'subheadings': {}
            } 