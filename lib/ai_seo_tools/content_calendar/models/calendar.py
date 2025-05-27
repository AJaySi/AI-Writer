import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('content_calendar_debug.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd

class ContentType(Enum):
    """Types of content that can be scheduled."""
    BLOG_POST = "blog_post"
    SOCIAL_MEDIA = "social_media"
    VIDEO = "video"
    PODCAST = "podcast"
    NEWSLETTER = "newsletter"
    LANDING_PAGE = "landing_page"

class Platform(Enum):
    """Supported content platforms."""
    WEBSITE = "website"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    MEDIUM = "medium"

@dataclass
class SEOData:
    """SEO-related data for content."""
    title: str
    meta_description: str
    keywords: List[str]
    structured_data: Dict[str, Any]
    canonical_url: Optional[str] = None
    og_tags: Optional[Dict[str, str]] = None
    twitter_cards: Optional[Dict[str, str]] = None

    @staticmethod
    def from_dict(data):
        return SEOData(
            title=data.get('title', ''),
            meta_description=data.get('meta_description', ''),
            keywords=data.get('keywords', []),
            structured_data=data.get('structured_data', {}),
            canonical_url=data.get('canonical_url'),
            og_tags=data.get('og_tags'),
            twitter_cards=data.get('twitter_cards')
        )

@dataclass
class ContentItem:
    """Represents a single content item in the calendar."""
    title: str
    description: str
    content_type: ContentType
    platforms: List[Platform]
    publish_date: datetime
    seo_data: SEOData
    status: str = "draft"
    author: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert content item to dictionary."""
        return {
            'title': self.title,
            'description': self.description,
            'content_type': self.content_type.value,
            'platforms': [p.value for p in self.platforms],
            'publish_date': self.publish_date.isoformat(),
            'seo_data': {
                'title': self.seo_data.title,
                'meta_description': self.seo_data.meta_description,
                'keywords': self.seo_data.keywords,
                'structured_data': self.seo_data.structured_data,
                'canonical_url': self.seo_data.canonical_url,
                'og_tags': self.seo_data.og_tags,
                'twitter_cards': self.seo_data.twitter_cards
            },
            'status': self.status,
            'author': self.author,
            'tags': self.tags,
            'notes': self.notes
        }

    @staticmethod
    def from_dict(data):
        from .calendar import ContentType, Platform, SEOData
        return ContentItem(
            title=data['title'],
            description=data.get('description', ''),
            content_type=ContentType(data['content_type']),
            platforms=[Platform(p) for p in data['platforms']],
            publish_date=pd.to_datetime(data['publish_date']),
            seo_data=SEOData.from_dict(data.get('seo_data', {})),
            status=data.get('status', 'draft'),
            author=data.get('author'),
            tags=data.get('tags', []),
            notes=data.get('notes')
        )

@dataclass
class Calendar:
    """Represents a content calendar."""
    start_date: datetime
    duration: str  # 'weekly', 'monthly', 'quarterly'
    platforms: List[Platform]
    schedule: Dict[str, List[ContentItem]]
    name: Optional[str] = None
    description: Optional[str] = None
    
    def __init__(self, start_date: datetime, duration: str, platforms: List[Platform], 
                 schedule: Dict[str, List[ContentItem]], name: Optional[str] = None, 
                 description: Optional[str] = None):
        """Initialize a new calendar.
        
        Args:
            start_date: Start date of the calendar
            duration: Duration of the calendar ('weekly', 'monthly', 'quarterly')
            platforms: List of platforms to schedule content for
            schedule: Dictionary mapping dates to content items
            name: Optional name for the calendar
            description: Optional description of the calendar
        """
        self.start_date = start_date
        self.duration = duration
        self.platforms = platforms
        self.schedule = schedule
        self.name = name
        self.description = description
        self.content_items: List[ContentItem] = []
        self.logger = logging.getLogger('content_calendar.calendar')
        
        # Initialize content_items from schedule
        for items in self.schedule.values():
            self.content_items.extend(items)
    
    def get_all_content(self) -> List[ContentItem]:
        """Get all content items in the calendar.
        
        Returns:
            List of all ContentItem objects in the calendar
        """
        try:
            self.logger.debug(f"Getting all content items. Count: {len(self.content_items)}")
            return self.content_items
        except Exception as e:
            self.logger.error(f"Error getting all content: {str(e)}")
            return []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert calendar to dictionary."""
        return {
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'duration': self.duration,
            'platforms': [p.value for p in self.platforms],
            'schedule': {
                date: [item.to_dict() for item in items]
                for date, items in self.schedule.items()
            }
        }
    
    def export(self, format: str = 'json') -> Dict[str, Any]:
        """
        Export calendar in specified format.
        Currently only supports JSON format.
        """
        if format.lower() != 'json':
            raise ValueError(f"Unsupported export format: {format}")
        
        return self.to_dict()
    
    def get_content_for_date(self, date: datetime) -> List[ContentItem]:
        """Get all content items scheduled for a specific date."""
        date_str = date.strftime('%Y-%m-%d')
        return self.schedule.get(date_str, [])
    
    def get_content_for_platform(
        self,
        platform: Platform
    ) -> List[ContentItem]:
        """Get all content items for a specific platform."""
        all_content = []
        for items in self.schedule.values():
            platform_content = [
                item for item in items
                if platform in item.platforms
            ]
            all_content.extend(platform_content)
        return all_content
    
    def add_content(self, content: ContentItem) -> None:
        """Add a new content item to the calendar."""
        date_str = content.publish_date.strftime('%Y-%m-%d')
        if date_str not in self.schedule:
            self.schedule[date_str] = []
        self.schedule[date_str].append(content)
    
    def remove_content(self, content: ContentItem) -> None:
        """Remove a content item from the calendar."""
        date_str = content.publish_date.strftime('%Y-%m-%d')
        if date_str in self.schedule:
            self.schedule[date_str] = [
                item for item in self.schedule[date_str]
                if item != content
            ]

    @staticmethod
    def from_dict(data):
        from .calendar import ContentItem, Platform
        schedule = {
            date: [ContentItem.from_dict(item) for item in items]
            for date, items in data.get('schedule', {}).items()
        }
        return Calendar(
            start_date=pd.to_datetime(data['start_date']),
            duration=data['duration'],
            platforms=[Platform(p) for p in data['platforms']],
            schedule=schedule,
            name=data.get('name'),
            description=data.get('description')
        ) 