from sqlalchemy import (
    create_engine, Column, Integer, String, Text, DateTime, Enum, ForeignKey, JSON
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import enum
from dataclasses import dataclass
from typing import List, Dict, Any

Base = declarative_base()

# --- DATACLASSES ---

@dataclass
class SEOData:
    title: str = ""
    meta_description: str = ""
    keywords: List[str] = None
    structured_data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.structured_data is None:
            self.structured_data = {}

# --- ENUMS ---

class ContentType(enum.Enum):
    BLOG_POST = "blog_post"
    SOCIAL_MEDIA = "social_media"
    VIDEO = "video"
    NEWSLETTER = "newsletter"

class Platform(enum.Enum):
    WEBSITE = "website"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"

class ScheduleStatus(enum.Enum):
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

# --- MODELS ---

class ContentItem(Base):
    __tablename__ = "content_items"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    content_type = Column(Enum(ContentType), nullable=False)
    platforms = Column(JSON, nullable=False)  # List of platforms (as strings)
    publish_date = Column(DateTime, nullable=False)
    status = Column(String, default="draft")
    author = Column(String)
    tags = Column(JSON, default=list)
    notes = Column(Text)
    seo_data = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    schedules = relationship("Schedule", back_populates="content_item", cascade="all, delete-orphan")

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    content_item_id = Column(Integer, ForeignKey("content_items.id"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(Enum(ScheduleStatus), default=ScheduleStatus.SCHEDULED)
    recurrence = Column(String)  # e.g., 'none', 'daily', 'weekly'
    priority = Column(Integer, default=1)
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    content_item = relationship("ContentItem", back_populates="schedules")

# --- DB INIT & SESSION ---

def get_engine(db_url="sqlite:///content_scheduler.db"):
    return create_engine(db_url, echo=False)

def init_db(engine):
    Base.metadata.create_all(engine)

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

__all__ = [
    'ContentItem',
    'ContentType',
    'Platform',
    'SEOData',
    'get_engine',
    'get_session',
    'init_db',
]