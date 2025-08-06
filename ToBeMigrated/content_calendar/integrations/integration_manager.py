import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from ..core.calendar_manager import CalendarManager
from ..core.content_brief import ContentBriefGenerator
from .platform_adapters import UnifiedPlatformAdapter

logger = logging.getLogger(__name__)

class IntegrationManager:
    """Manages integration between content calendar and platform adapters."""
    
    def __init__(self):
        """Initialize the integration manager."""
        self.calendar_manager = CalendarManager()
        self.content_brief_generator = ContentBriefGenerator()
        self.platform_adapter = UnifiedPlatformAdapter()
        
    def create_cross_platform_calendar(
        self,
        start_date: datetime,
        end_date: datetime,
        platforms: List[str],
        content_types: List[str],
        target_audience: Optional[Dict[str, Any]] = None,
        industry: Optional[str] = None,
        keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create a cross-platform content calendar."""
        try:
            # Generate base calendar
            calendar = self.calendar_manager.create_calendar(
                start_date=start_date,
                end_date=end_date,
                content_types=content_types,
                target_audience=target_audience,
                industry=industry,
                keywords=keywords
            )
            
            # Adapt content for each platform
            platform_calendars = {}
            for platform in platforms:
                platform_calendars[platform] = self._adapt_calendar_for_platform(
                    calendar=calendar,
                    platform=platform
                )
            
            return {
                'base_calendar': calendar,
                'platform_calendars': platform_calendars,
                'metadata': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'platforms': platforms,
                    'content_types': content_types,
                    'industry': industry,
                    'keywords': keywords
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating cross-platform calendar: {str(e)}")
            raise
    
    def _adapt_calendar_for_platform(
        self,
        calendar: Dict[str, Any],
        platform: str
    ) -> Dict[str, Any]:
        """Adapt calendar content for a specific platform."""
        try:
            adapted_calendar = {
                'platform': platform,
                'content_items': [],
                'metadata': calendar.get('metadata', {})
            }
            
            # Adapt each content item
            for item in calendar.get('content_items', []):
                adapted_item = self._adapt_content_item(item, platform)
                if adapted_item:
                    adapted_calendar['content_items'].append(adapted_item)
            
            return adapted_calendar
            
        except Exception as e:
            logger.error(f"Error adapting calendar for platform {platform}: {str(e)}")
            return {
                'platform': platform,
                'content_items': [],
                'error': str(e)
            }
    
    def _adapt_content_item(
        self,
        item: Dict[str, Any],
        platform: str
    ) -> Optional[Dict[str, Any]]:
        """Adapt a content item for a specific platform."""
        try:
            # Generate content brief if not exists
            if 'brief' not in item:
                item['brief'] = self.content_brief_generator.generate_brief(item)
            
            # Adapt content for platform
            adapted_content = self.platform_adapter.adapt_content(
                content=item,
                platform=platform
            )
            
            if adapted_content:
                return {
                    'original_item': item,
                    'adapted_content': adapted_content,
                    'platform_specifics': self.platform_adapter.get_platform_specs(platform)
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error adapting content item for platform {platform}: {str(e)}")
            return None
    
    def get_platform_suggestions(
        self,
        content: Dict[str, Any],
        platforms: List[str]
    ) -> Dict[str, Any]:
        """Get platform-specific suggestions for content."""
        try:
            suggestions = {}
            
            for platform in platforms:
                platform_suggestions = self.platform_adapter.get_platform_suggestions(
                    content=content,
                    platform=platform
                )
                if platform_suggestions:
                    suggestions[platform] = platform_suggestions
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error getting platform suggestions: {str(e)}")
            return {}
    
    def validate_platform_content(
        self,
        content: Dict[str, Any],
        platform: str
    ) -> Dict[str, Any]:
        """Validate content for a specific platform."""
        try:
            validation_result = self.platform_adapter.validate_content(
                content=content,
                platform=platform
            )
            
            return {
                'platform': platform,
                'is_valid': validation_result,
                'specifications': self.platform_adapter.get_platform_specs(platform)
            }
            
        except Exception as e:
            logger.error(f"Error validating platform content: {str(e)}")
            return {
                'platform': platform,
                'is_valid': False,
                'error': str(e)
            }
    
    def optimize_cross_platform_content(
        self,
        content: Dict[str, Any],
        platforms: List[str]
    ) -> Dict[str, Any]:
        """Optimize content for multiple platforms."""
        try:
            optimized_content = {}
            
            for platform in platforms:
                platform_optimized = self.platform_adapter.optimize_content(
                    content=content,
                    platform=platform
                )
                if platform_optimized:
                    optimized_content[platform] = platform_optimized
            
            return optimized_content
            
        except Exception as e:
            logger.error(f"Error optimizing cross-platform content: {str(e)}")
            return {} 