from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
import sys
import json
import os

from ..integrations.seo_tools import SEOToolsIntegration
from ..integrations.gap_analyzer import GapAnalyzerIntegration
from ..models.calendar import Calendar, ContentItem
from ..utils.date_utils import calculate_publish_dates
from ..utils.error_handling import handle_calendar_error

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('content_calendar_debug.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

CALENDAR_JSON_PATH = "calendar_data.json"

class CalendarManager:
    """
    Main calendar management system that coordinates content planning,
    scheduling, and optimization.
    """
    
    def __init__(self):
        """Initialize calendar manager."""
        self.logger = logging.getLogger('content_calendar.manager')
        self.logger.info("Initializing CalendarManager")
        
        self.seo_tools = SEOToolsIntegration()
        self.gap_analyzer = GapAnalyzerIntegration()
        self._calendar: Optional[Calendar] = None
        self.logger.info("CalendarManager initialized successfully")
    
    @handle_calendar_error
    def create_calendar(
        self,
        start_date: datetime,
        duration: str,  # 'weekly', 'monthly', 'quarterly'
        platforms: List[str],
        website_url: str
    ) -> Calendar:
        """
        Create a new content calendar based on content gap analysis and SEO requirements.
        
        Args:
            start_date: When the calendar should begin
            duration: How long the calendar should span
            platforms: List of platforms to create content for
            website_url: URL of the website to analyze
            
        Returns:
            Calendar object containing the content schedule
        """
        self.logger.info(f"Creating new calendar for {website_url}")
        self.logger.debug(f"Parameters: start_date={start_date}, duration={duration}, platforms={platforms}")
        
        try:
            # 1. Analyze content gaps
            self.logger.info("Analyzing content gaps")
            gap_analysis = self.gap_analyzer.analyze_gaps(website_url)
            
            # 2. Generate topics based on gaps
            self.logger.info("Generating topics from gap analysis")
            topics = self._generate_topics(gap_analysis, platforms)
            
            # 3. Calculate publish dates
            self.logger.info("Calculating publish dates")
            schedule = calculate_publish_dates(
                topics=topics,
                start_date=start_date,
                duration=duration
            )
            
            # 4. Create calendar
            self.logger.info("Creating calendar object")
            self._calendar = Calendar(
                start_date=start_date,
                duration=duration,
                platforms=platforms,
                schedule=schedule
            )
            
            self.logger.info("Calendar created successfully")
            return self._calendar
            
        except Exception as e:
            self.logger.error(f"Error creating calendar: {str(e)}", exc_info=True)
            raise
    
    def _generate_topics(
        self,
        gap_analysis: Dict[str, Any],
        platforms: List[str]
    ) -> List[ContentItem]:
        """
        Generate content topics based on gap analysis and platform requirements.
        """
        topics = []
        
        for gap in gap_analysis['gaps']:
            # Generate topic using AI
            topic = self._generate_topic_from_gap(gap, platforms)
            
            # Optimize for SEO
            optimized_topic = self._optimize_topic(topic)
            
            topics.append(optimized_topic)
        
        return topics
    
    def _generate_topic_from_gap(
        self,
        gap: Dict[str, Any],
        platforms: List[str]
    ) -> ContentItem:
        """
        Generate a specific topic based on a content gap.
        """
        # Use existing AI tools to generate topic
        topic_data = {
            'title': self._generate_title(gap),
            'description': self._generate_description(gap),
            'keywords': gap.get('keywords', []),
            'platforms': platforms,
            'content_type': self._determine_content_type(gap, platforms)
        }
        
        return ContentItem(**topic_data)
    
    def _optimize_topic(self, topic: ContentItem) -> ContentItem:
        """
        Optimize a topic for SEO using existing tools.
        """
        # Optimize title
        topic.title = self.seo_tools.optimize_title(topic.title)
        
        # Generate meta description
        topic.meta_description = self.seo_tools.generate_meta_description(
            topic.description
        )
        
        # Add structured data
        topic.structured_data = self.seo_tools.generate_structured_data(
            topic.content_type
        )
        
        return topic
    
    def get_calendar(self) -> Optional[Calendar]:
        """
        Get the current calendar.
        """
        self.logger.debug("Getting current calendar")
        return self._calendar
    
    def update_calendar(self, calendar: Calendar) -> None:
        """
        Update the current calendar.
        """
        self._calendar = calendar
    
    def export_calendar(self) -> Optional[Dict[str, Any]]:
        """Export the current calendar."""
        self.logger.info("Exporting calendar")
        if not self._calendar:
            self.logger.warning("No calendar to export")
            return None
        
        try:
            calendar_data = self._calendar.export()
            self.logger.info("Calendar exported successfully")
            return calendar_data
        except Exception as e:
            self.logger.error(f"Error exporting calendar: {str(e)}", exc_info=True)
            return None

    def save_calendar_to_json(self):
        calendar = self.get_calendar()
        if calendar:
            with open(CALENDAR_JSON_PATH, "w") as f:
                json.dump(calendar.to_dict(), f, indent=2, default=str)

    def load_calendar_from_json(self):
        from lib.ai_seo_tools.content_calendar.models.calendar import Calendar
        if os.path.exists(CALENDAR_JSON_PATH):
            with open(CALENDAR_JSON_PATH, "r") as f:
                data = json.load(f)
            self._calendar = Calendar.from_dict(data) 