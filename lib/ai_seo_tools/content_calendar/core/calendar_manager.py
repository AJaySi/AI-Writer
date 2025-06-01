from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
import sys
import json
import os
from lib.database.models import ContentItem, ContentType, Platform, get_engine, get_session, init_db
from ..integrations.seo_tools import SEOToolsIntegration
from ..integrations.gap_analyzer import GapAnalyzerIntegration
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

engine = get_engine()
init_db(engine)
session = get_session(engine)

class CalendarManager:
    """
    Main calendar management system that coordinates content planning,
    scheduling, and optimization.
    """
    def __init__(self):
        self.logger = logging.getLogger('content_calendar.manager')
        self.logger.info("Initializing CalendarManager")
        self.seo_tools = SEOToolsIntegration()
        self.gap_analyzer = GapAnalyzerIntegration()
        self.logger.info("CalendarManager initialized successfully")

    @handle_calendar_error
    def create_calendar(
        self,
        start_date: datetime,
        duration: str,  # 'weekly', 'monthly', 'quarterly'
        platforms: List[str],
        website_url: str
    ) -> List[ContentItem]:
        self.logger.info(f"Creating new calendar for {website_url}")
        self.logger.debug(f"Parameters: start_date={start_date}, duration={duration}, platforms={platforms}")
        try:
            gap_analysis = self.gap_analyzer.analyze_gaps(website_url)
            topics = self._generate_topics(gap_analysis, platforms)
            schedule = calculate_publish_dates(
                topics=topics,
                start_date=start_date,
                duration=duration
            )
            # Add to DB
            for topic in schedule:
                session.add(topic)
            session.commit()
            self.logger.info("Calendar created and content scheduled in DB successfully")
            return schedule
        except Exception as e:
            self.logger.error(f"Error creating calendar: {str(e)}", exc_info=True)
            raise

    def _generate_topics(
        self,
        gap_analysis: Dict[str, Any],
        platforms: List[str]
    ) -> List[ContentItem]:
        topics = []
        for gap in gap_analysis['gaps']:
            topic = self._generate_topic_from_gap(gap, platforms)
            optimized_topic = self._optimize_topic(topic)
            topics.append(optimized_topic)
        return topics

    def _generate_topic_from_gap(
        self,
        gap: Dict[str, Any],
        platforms: List[str]
    ) -> ContentItem:
        topic_data = {
            'title': self._generate_title(gap),
            'description': self._generate_description(gap),
            'keywords': gap.get('keywords', []),
            'platforms': platforms,
            'content_type': self._determine_content_type(gap, platforms),
            'publish_date': datetime.now(),
            'status': 'Draft',
            'author': None,
            'tags': [],
            'notes': None,
            'seo_data': {}
        }
        return ContentItem(**topic_data)

    def _optimize_topic(self, topic: ContentItem) -> ContentItem:
        topic.title = self.seo_tools.optimize_title(topic.title)
        topic.seo_data['meta_description'] = self.seo_tools.generate_meta_description(topic.description)
        topic.seo_data['structured_data'] = self.seo_tools.generate_structured_data(topic.content_type)
        return topic

    def get_all_content(self) -> List[ContentItem]:
        return session.query(ContentItem).all()

    def remove_content(self, content_id):
        content = session.query(ContentItem).get(content_id)
        if content:
            session.delete(content)
            session.commit()

    def update_content(self, content_id, **kwargs):
        content = session.query(ContentItem).get(content_id)
        if content:
            for key, value in kwargs.items():
                setattr(content, key, value)
            session.commit()

    def get_calendar(self) -> Optional[List[ContentItem]]:
        """
        Get the current calendar.
        """
        self.logger.debug("Getting current calendar")
        return self.get_all_content()
    
    def update_calendar(self, calendar: List[ContentItem]) -> None:
        """
        Update the current calendar.
        """
        self.get_all_content()
        for content in calendar:
            session.add(content)
        session.commit()
    
    def export_calendar(self) -> Optional[Dict[str, Any]]:
        """Export the current calendar."""
        self.logger.info("Exporting calendar")
        calendar = self.get_calendar()
        if not calendar:
            self.logger.warning("No calendar to export")
            return None
        
        try:
            calendar_data = [content.to_dict() for content in calendar]
            self.logger.info("Calendar exported successfully")
            return calendar_data
        except Exception as e:
            self.logger.error(f"Error exporting calendar: {str(e)}", exc_info=True)
            return None

    def save_calendar_to_json(self):
        calendar = self.get_calendar()
        if calendar:
            with open("calendar_data.json", "w") as f:
                json.dump(calendar, f, indent=2, default=str)

    def load_calendar_from_json(self):
        if os.path.exists("calendar_data.json"):
            with open("calendar_data.json", "r") as f:
                data = json.load(f)
            self.update_calendar(data) 