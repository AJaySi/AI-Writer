"""
Twitter Database Models for ALwrity
===================================

This module defines SQLAlchemy models for storing Twitter-related data including:
- User profiles and authentication
- Tweet content and metadata
- Analytics and engagement metrics
- Scheduling and automation data
- Performance tracking and insights

This allows the application to store Twitter data locally and reduce API calls
while providing rich analytics and historical data to users.
"""

from sqlalchemy import (
    create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, 
    Enum, ForeignKey, JSON, BigInteger, Index, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime, timedelta
import enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json

Base = declarative_base()

# --- ENUMS ---

class TwitterAccountType(enum.Enum):
    PERSONAL = "personal"
    BUSINESS = "business"
    CREATOR = "creator"
    BRAND = "brand"

class TweetType(enum.Enum):
    ORIGINAL = "original"
    REPLY = "reply"
    RETWEET = "retweet"
    QUOTE_TWEET = "quote_tweet"
    THREAD = "thread"

class TweetStatus(enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    POSTED = "posted"
    FAILED = "failed"
    DELETED = "deleted"

class EngagementType(enum.Enum):
    LIKE = "like"
    RETWEET = "retweet"
    REPLY = "reply"
    QUOTE_TWEET = "quote_tweet"
    BOOKMARK = "bookmark"
    IMPRESSION = "impression"
    PROFILE_CLICK = "profile_click"
    URL_CLICK = "url_click"
    HASHTAG_CLICK = "hashtag_click"
    MENTION_CLICK = "mention_click"

class AnalyticsTimeframe(enum.Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class ContentCategory(enum.Enum):
    EDUCATIONAL = "educational"
    PROMOTIONAL = "promotional"
    PERSONAL = "personal"
    NEWS = "news"
    ENTERTAINMENT = "entertainment"
    QUESTION = "question"
    POLL = "poll"
    THREAD = "thread"

# --- DATACLASSES ---

@dataclass
class TwitterCredentials:
    """Dataclass for Twitter API credentials"""
    api_key: str = ""
    api_secret: str = ""
    access_token: str = ""
    access_token_secret: str = ""
    bearer_token: str = ""
    
    def to_dict(self) -> Dict[str, str]:
        return {
            'api_key': self.api_key,
            'api_secret': self.api_secret,
            'access_token': self.access_token,
            'access_token_secret': self.access_token_secret,
            'bearer_token': self.bearer_token
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'TwitterCredentials':
        return cls(
            api_key=data.get('api_key', ''),
            api_secret=data.get('api_secret', ''),
            access_token=data.get('access_token', ''),
            access_token_secret=data.get('access_token_secret', ''),
            bearer_token=data.get('bearer_token', '')
        )

@dataclass
class TweetMetrics:
    """Dataclass for tweet performance metrics"""
    likes: int = 0
    retweets: int = 0
    replies: int = 0
    quotes: int = 0
    bookmarks: int = 0
    impressions: int = 0
    profile_clicks: int = 0
    url_clicks: int = 0
    hashtag_clicks: int = 0
    engagement_rate: float = 0.0
    reach: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'likes': self.likes,
            'retweets': self.retweets,
            'replies': self.replies,
            'quotes': self.quotes,
            'bookmarks': self.bookmarks,
            'impressions': self.impressions,
            'profile_clicks': self.profile_clicks,
            'url_clicks': self.url_clicks,
            'hashtag_clicks': self.hashtag_clicks,
            'engagement_rate': self.engagement_rate,
            'reach': self.reach
        }

# --- MODELS ---

class TwitterUser(Base):
    """
    Stores Twitter user profile information and authentication data.
    This reduces API calls for user profile information.
    """
    __tablename__ = "twitter_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, unique=True)  # ALwrity user ID
    twitter_user_id = Column(BigInteger, nullable=False, unique=True)  # Twitter user ID
    username = Column(String, nullable=False, index=True)  # @username
    display_name = Column(String, nullable=False)
    bio = Column(Text)
    location = Column(String)
    website = Column(String)
    profile_image_url = Column(String)
    banner_image_url = Column(String)
    
    # Account metrics
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    tweet_count = Column(Integer, default=0)
    listed_count = Column(Integer, default=0)
    
    # Account details
    account_type = Column(Enum(TwitterAccountType), default=TwitterAccountType.PERSONAL)
    verified = Column(Boolean, default=False)
    protected = Column(Boolean, default=False)
    created_at_twitter = Column(DateTime)  # When Twitter account was created
    
    # Authentication and API data
    credentials_encrypted = Column(Text)  # Encrypted JSON of TwitterCredentials
    api_rate_limit_remaining = Column(Integer, default=0)
    api_rate_limit_reset = Column(DateTime)
    last_api_call = Column(DateTime)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tweets = relationship("Tweet", back_populates="user", cascade="all, delete-orphan")
    analytics = relationship("TwitterAnalytics", back_populates="user", cascade="all, delete-orphan")
    scheduled_tweets = relationship("ScheduledTweet", back_populates="user", cascade="all, delete-orphan")
    engagement_data = relationship("EngagementData", back_populates="user", cascade="all, delete-orphan")
    audience_insights = relationship("AudienceInsight", back_populates="user", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_twitter_user_username', 'username'),
        Index('idx_twitter_user_sync', 'last_sync'),
        Index('idx_twitter_user_active', 'is_active'),
    )

class Tweet(Base):
    """
    Stores tweet content, metadata, and performance data.
    Includes both posted tweets and drafts.
    """
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("twitter_users.id"), nullable=False)
    tweet_id = Column(BigInteger, unique=True, index=True)  # Twitter tweet ID (null for drafts)
    
    # Content
    text = Column(Text, nullable=False)
    hashtags = Column(JSON, default=list)  # List of hashtags
    mentions = Column(JSON, default=list)  # List of mentioned users
    urls = Column(JSON, default=list)  # List of URLs in tweet
    media_urls = Column(JSON, default=list)  # List of media URLs
    
    # Tweet metadata
    tweet_type = Column(Enum(TweetType), default=TweetType.ORIGINAL)
    status = Column(Enum(TweetStatus), default=TweetStatus.DRAFT)
    category = Column(Enum(ContentCategory))
    
    # Engagement metrics (updated periodically)
    likes_count = Column(Integer, default=0)
    retweets_count = Column(Integer, default=0)
    replies_count = Column(Integer, default=0)
    quotes_count = Column(Integer, default=0)
    bookmarks_count = Column(Integer, default=0)
    impressions_count = Column(Integer, default=0)
    
    # Performance metrics
    engagement_rate = Column(Float, default=0.0)
    reach = Column(Integer, default=0)
    click_through_rate = Column(Float, default=0.0)
    
    # AI and generation data
    ai_generated = Column(Boolean, default=False)
    ai_model_used = Column(String)  # Which AI model generated this
    ai_prompt = Column(Text)  # Original prompt used
    ai_confidence_score = Column(Float)  # AI confidence in content quality
    generation_metadata = Column(JSON, default=dict)  # Additional AI metadata
    
    # Scheduling and posting
    scheduled_for = Column(DateTime)
    posted_at = Column(DateTime)
    last_metrics_update = Column(DateTime)
    
    # Thread information
    thread_id = Column(String)  # For grouping thread tweets
    thread_position = Column(Integer)  # Position in thread (1, 2, 3...)
    parent_tweet_id = Column(BigInteger)  # For replies
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("TwitterUser", back_populates="tweets")
    analytics = relationship("TweetAnalytics", back_populates="tweet", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_tweet_user_status', 'user_id', 'status'),
        Index('idx_tweet_posted_at', 'posted_at'),
        Index('idx_tweet_engagement', 'engagement_rate'),
        Index('idx_tweet_thread', 'thread_id'),
    )

class ScheduledTweet(Base):
    """
    Stores scheduled tweets with automation settings.
    """
    __tablename__ = "scheduled_tweets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("twitter_users.id"), nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=False)
    
    # Scheduling details
    scheduled_time = Column(DateTime, nullable=False)
    timezone = Column(String, default="UTC")
    recurrence_pattern = Column(String)  # cron-like pattern for recurring tweets
    
    # Automation settings
    auto_optimize_time = Column(Boolean, default=False)  # AI-optimize posting time
    auto_add_hashtags = Column(Boolean, default=False)
    auto_add_emojis = Column(Boolean, default=False)
    
    # Status and execution
    status = Column(Enum(TweetStatus), default=TweetStatus.SCHEDULED)
    attempts = Column(Integer, default=0)
    last_attempt = Column(DateTime)
    error_message = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("TwitterUser", back_populates="scheduled_tweets")
    tweet = relationship("Tweet")
    
    # Indexes
    __table_args__ = (
        Index('idx_scheduled_time', 'scheduled_time'),
        Index('idx_scheduled_status', 'status'),
    )

class TwitterAnalytics(Base):
    """
    Stores aggregated Twitter analytics data for users.
    Updated periodically to track account performance over time.
    """
    __tablename__ = "twitter_analytics"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("twitter_users.id"), nullable=False)
    
    # Time period
    date = Column(DateTime, nullable=False)
    timeframe = Column(Enum(AnalyticsTimeframe), nullable=False)
    
    # Account metrics
    followers_gained = Column(Integer, default=0)
    followers_lost = Column(Integer, default=0)
    net_follower_change = Column(Integer, default=0)
    following_change = Column(Integer, default=0)
    
    # Content metrics
    tweets_posted = Column(Integer, default=0)
    total_impressions = Column(Integer, default=0)
    total_engagements = Column(Integer, default=0)
    total_likes = Column(Integer, default=0)
    total_retweets = Column(Integer, default=0)
    total_replies = Column(Integer, default=0)
    total_quotes = Column(Integer, default=0)
    
    # Performance metrics
    average_engagement_rate = Column(Float, default=0.0)
    top_tweet_id = Column(BigInteger)  # Best performing tweet
    top_tweet_engagement = Column(Integer, default=0)
    
    # Audience metrics
    profile_visits = Column(Integer, default=0)
    mention_count = Column(Integer, default=0)
    hashtag_performance = Column(JSON, default=dict)  # Top hashtags and their performance
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("TwitterUser", back_populates="analytics")
    
    # Indexes
    __table_args__ = (
        Index('idx_analytics_user_date', 'user_id', 'date'),
        Index('idx_analytics_timeframe', 'timeframe'),
        UniqueConstraint('user_id', 'date', 'timeframe', name='uq_user_date_timeframe'),
    )

class TweetAnalytics(Base):
    """
    Stores detailed analytics for individual tweets.
    Updated periodically to track tweet performance over time.
    """
    __tablename__ = "tweet_analytics"

    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=False)
    
    # Time period
    recorded_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Engagement metrics
    likes = Column(Integer, default=0)
    retweets = Column(Integer, default=0)
    replies = Column(Integer, default=0)
    quotes = Column(Integer, default=0)
    bookmarks = Column(Integer, default=0)
    
    # Reach metrics
    impressions = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    profile_clicks = Column(Integer, default=0)
    
    # Click metrics
    url_clicks = Column(Integer, default=0)
    hashtag_clicks = Column(Integer, default=0)
    mention_clicks = Column(Integer, default=0)
    media_views = Column(Integer, default=0)
    
    # Calculated metrics
    engagement_rate = Column(Float, default=0.0)
    click_through_rate = Column(Float, default=0.0)
    virality_score = Column(Float, default=0.0)  # Custom metric for viral potential
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tweet = relationship("Tweet", back_populates="analytics")
    
    # Indexes
    __table_args__ = (
        Index('idx_tweet_analytics_recorded', 'recorded_at'),
        Index('idx_tweet_analytics_engagement', 'engagement_rate'),
    )

class EngagementData(Base):
    """
    Stores individual engagement events for detailed analysis.
    """
    __tablename__ = "engagement_data"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("twitter_users.id"), nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id"))
    
    # Engagement details
    engagement_type = Column(Enum(EngagementType), nullable=False)
    engaging_user_id = Column(BigInteger)  # Twitter ID of user who engaged
    engaging_username = Column(String)
    
    # Metadata
    occurred_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("TwitterUser", back_populates="engagement_data")
    tweet = relationship("Tweet")
    
    # Indexes
    __table_args__ = (
        Index('idx_engagement_user_type', 'user_id', 'engagement_type'),
        Index('idx_engagement_occurred', 'occurred_at'),
    )

class AudienceInsight(Base):
    """
    Stores audience demographics and behavior insights.
    """
    __tablename__ = "audience_insights"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("twitter_users.id"), nullable=False)
    
    # Time period
    date = Column(DateTime, nullable=False)
    
    # Demographics (aggregated data)
    top_locations = Column(JSON, default=list)  # Top follower locations
    age_demographics = Column(JSON, default=dict)  # Age distribution
    gender_demographics = Column(JSON, default=dict)  # Gender distribution
    language_demographics = Column(JSON, default=dict)  # Language distribution
    
    # Behavior insights
    most_active_hours = Column(JSON, default=list)  # When audience is most active
    top_interests = Column(JSON, default=list)  # Audience interests
    engagement_patterns = Column(JSON, default=dict)  # How audience engages
    
    # Content preferences
    preferred_content_types = Column(JSON, default=dict)
    top_hashtags_used = Column(JSON, default=list)
    response_rate_by_content = Column(JSON, default=dict)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("TwitterUser", back_populates="audience_insights")
    
    # Indexes
    __table_args__ = (
        Index('idx_audience_user_date', 'user_id', 'date'),
    )

class HashtagPerformance(Base):
    """
    Tracks performance of hashtags used by the user.
    """
    __tablename__ = "hashtag_performance"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("twitter_users.id"), nullable=False)
    
    # Hashtag details
    hashtag = Column(String, nullable=False, index=True)
    usage_count = Column(Integer, default=0)
    
    # Performance metrics
    total_impressions = Column(Integer, default=0)
    total_engagements = Column(Integer, default=0)
    average_engagement_rate = Column(Float, default=0.0)
    
    # Best performing tweet with this hashtag
    best_tweet_id = Column(Integer, ForeignKey("tweets.id"))
    best_tweet_engagement = Column(Integer, default=0)
    
    # Time tracking
    first_used = Column(DateTime)
    last_used = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("TwitterUser")
    best_tweet = relationship("Tweet")
    
    # Indexes
    __table_args__ = (
        Index('idx_hashtag_user_performance', 'user_id', 'average_engagement_rate'),
        UniqueConstraint('user_id', 'hashtag', name='uq_user_hashtag'),
    )

class ContentTemplate(Base):
    """
    Stores reusable tweet templates and AI prompts.
    """
    __tablename__ = "content_templates"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("twitter_users.id"), nullable=False)
    
    # Template details
    name = Column(String, nullable=False)
    description = Column(Text)
    template_text = Column(Text, nullable=False)
    category = Column(Enum(ContentCategory))
    
    # Template variables and settings
    variables = Column(JSON, default=list)  # List of template variables
    default_hashtags = Column(JSON, default=list)
    suggested_times = Column(JSON, default=list)  # Best times to post this type
    
    # AI settings
    ai_prompt = Column(Text)  # AI prompt for generating content
    ai_tone = Column(String)  # Tone for AI generation
    ai_target_audience = Column(String)
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime)
    average_performance = Column(Float, default=0.0)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("TwitterUser")
    
    # Indexes
    __table_args__ = (
        Index('idx_template_user_category', 'user_id', 'category'),
        Index('idx_template_performance', 'average_performance'),
    )

class TwitterSettings(Base):
    """
    Stores user-specific Twitter settings and preferences.
    """
    __tablename__ = "twitter_settings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("twitter_users.id"), nullable=False, unique=True)
    
    # Posting preferences
    default_hashtags = Column(JSON, default=list)
    auto_add_hashtags = Column(Boolean, default=False)
    auto_add_emojis = Column(Boolean, default=False)
    max_hashtags_per_tweet = Column(Integer, default=2)
    
    # Scheduling preferences
    preferred_posting_times = Column(JSON, default=list)
    timezone = Column(String, default="UTC")
    auto_optimize_timing = Column(Boolean, default=False)
    
    # AI preferences
    ai_tone_preference = Column(String, default="casual")
    ai_target_audience = Column(String, default="general")
    ai_creativity_level = Column(Float, default=0.7)  # 0-1 scale
    
    # Analytics preferences
    analytics_frequency = Column(String, default="daily")  # hourly, daily, weekly
    track_competitor_hashtags = Column(JSON, default=list)
    notification_preferences = Column(JSON, default=dict)
    
    # Content preferences
    content_categories = Column(JSON, default=list)  # Preferred content types
    avoid_topics = Column(JSON, default=list)  # Topics to avoid
    brand_keywords = Column(JSON, default=list)  # Brand-related keywords
    
    # Automation settings
    auto_retweet_keywords = Column(JSON, default=list)
    auto_like_keywords = Column(JSON, default=list)
    auto_follow_back = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("TwitterUser")

# --- DATABASE FUNCTIONS ---

def get_twitter_engine(db_url: str = "sqlite:///twitter_data.db"):
    """Create and return database engine for Twitter data."""
    return create_engine(db_url, echo=False)

def init_twitter_db(engine):
    """Initialize Twitter database tables."""
    Base.metadata.create_all(engine)

def get_twitter_session(engine):
    """Create and return database session for Twitter data."""
    Session = sessionmaker(bind=engine)
    return Session()

def create_twitter_user(session, user_data: Dict[str, Any]) -> TwitterUser:
    """Create a new Twitter user record."""
    twitter_user = TwitterUser(
        user_id=user_data['user_id'],
        twitter_user_id=user_data['twitter_user_id'],
        username=user_data['username'],
        display_name=user_data['display_name'],
        bio=user_data.get('bio', ''),
        location=user_data.get('location', ''),
        website=user_data.get('website', ''),
        profile_image_url=user_data.get('profile_image_url', ''),
        banner_image_url=user_data.get('banner_image_url', ''),
        followers_count=user_data.get('followers_count', 0),
        following_count=user_data.get('following_count', 0),
        tweet_count=user_data.get('tweet_count', 0),
        verified=user_data.get('verified', False),
        protected=user_data.get('protected', False),
        created_at_twitter=user_data.get('created_at_twitter'),
        credentials_encrypted=user_data.get('credentials_encrypted', ''),
    )
    
    session.add(twitter_user)
    session.commit()
    return twitter_user

def update_user_metrics(session, user_id: int, metrics: Dict[str, Any]):
    """Update user metrics from Twitter API."""
    user = session.query(TwitterUser).filter_by(id=user_id).first()
    if user:
        user.followers_count = metrics.get('followers_count', user.followers_count)
        user.following_count = metrics.get('following_count', user.following_count)
        user.tweet_count = metrics.get('tweet_count', user.tweet_count)
        user.last_sync = datetime.utcnow()
        session.commit()

def create_tweet_record(session, tweet_data: Dict[str, Any]) -> Tweet:
    """Create a new tweet record."""
    # Handle both 'text' and 'content' field names for compatibility
    text_content = tweet_data.get('text') or tweet_data.get('content')
    if not text_content:
        raise ValueError("Tweet must have either 'text' or 'content' field")
    
    tweet = Tweet(
        user_id=tweet_data['user_id'],
        tweet_id=tweet_data.get('tweet_id'),
        text=text_content,
        hashtags=tweet_data.get('hashtags', []),
        mentions=tweet_data.get('mentions', []),
        urls=tweet_data.get('urls', []),
        media_urls=tweet_data.get('media_urls', []),
        tweet_type=TweetType(tweet_data.get('tweet_type', 'original')),
        status=TweetStatus(tweet_data.get('status', 'draft')),
        category=ContentCategory(tweet_data['category']) if tweet_data.get('category') else None,
        ai_generated=tweet_data.get('ai_generated', False),
        ai_model_used=tweet_data.get('ai_model_used'),
        ai_prompt=tweet_data.get('ai_prompt'),
        ai_confidence_score=tweet_data.get('ai_confidence_score'),
        generation_metadata=tweet_data.get('generation_metadata', {}),
        scheduled_for=tweet_data.get('scheduled_for'),
        posted_at=tweet_data.get('posted_at'),
        thread_id=tweet_data.get('thread_id'),
        thread_position=tweet_data.get('thread_position'),
        parent_tweet_id=tweet_data.get('parent_tweet_id'),
    )
    
    session.add(tweet)
    session.commit()
    return tweet

def update_tweet_metrics(session, tweet_id: int, metrics: TweetMetrics):
    """Update tweet metrics from Twitter API."""
    tweet = session.query(Tweet).filter_by(id=tweet_id).first()
    if tweet:
        tweet.likes_count = metrics.likes
        tweet.retweets_count = metrics.retweets
        tweet.replies_count = metrics.replies
        tweet.quotes_count = metrics.quotes
        tweet.bookmarks_count = metrics.bookmarks
        tweet.impressions_count = metrics.impressions
        tweet.engagement_rate = metrics.engagement_rate
        tweet.reach = metrics.reach
        tweet.last_metrics_update = datetime.utcnow()
        session.commit()
        
        # Also create analytics record
        analytics = TweetAnalytics(
            tweet_id=tweet_id,
            likes=metrics.likes,
            retweets=metrics.retweets,
            replies=metrics.replies,
            quotes=metrics.quotes,
            bookmarks=metrics.bookmarks,
            impressions=metrics.impressions,
            reach=metrics.reach,
            engagement_rate=metrics.engagement_rate,
            click_through_rate=metrics.url_clicks / max(metrics.impressions, 1) * 100,
            virality_score=calculate_virality_score(metrics)
        )
        session.add(analytics)
        session.commit()

def calculate_virality_score(metrics: TweetMetrics) -> float:
    """Calculate a custom virality score based on engagement metrics."""
    if metrics.impressions == 0:
        return 0.0
    
    # Weight different engagement types
    engagement_score = (
        metrics.likes * 1.0 +
        metrics.retweets * 3.0 +  # Retweets are more valuable
        metrics.replies * 2.0 +
        metrics.quotes * 2.5 +
        metrics.bookmarks * 1.5
    )
    
    # Normalize by impressions and scale
    virality = (engagement_score / metrics.impressions) * 100
    return min(virality, 100.0)  # Cap at 100

def get_user_analytics_summary(session, user_id: int, days: int = 30) -> Dict[str, Any]:
    """Get analytics summary for a user over specified days."""
    from sqlalchemy import func
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get tweet metrics
    tweet_stats = session.query(
        func.count(Tweet.id).label('total_tweets'),
        func.avg(Tweet.engagement_rate).label('avg_engagement'),
        func.sum(Tweet.likes_count).label('total_likes'),
        func.sum(Tweet.retweets_count).label('total_retweets'),
        func.sum(Tweet.impressions_count).label('total_impressions')
    ).filter(
        Tweet.user_id == user_id,
        Tweet.posted_at >= start_date,
        Tweet.status == TweetStatus.POSTED
    ).first()
    
    # Get follower growth
    user = session.query(TwitterUser).filter_by(id=user_id).first()
    
    return {
        'total_tweets': tweet_stats.total_tweets or 0,
        'average_engagement_rate': float(tweet_stats.avg_engagement or 0),
        'total_likes': tweet_stats.total_likes or 0,
        'total_retweets': tweet_stats.total_retweets or 0,
        'total_impressions': tweet_stats.total_impressions or 0,
        'current_followers': user.followers_count if user else 0,
        'period_days': days
    }

# Export all models and functions
__all__ = [
    # Models
    'TwitterUser', 'Tweet', 'ScheduledTweet', 'TwitterAnalytics', 'TweetAnalytics',
    'EngagementData', 'AudienceInsight', 'HashtagPerformance', 'ContentTemplate',
    'TwitterSettings',
    
    # Enums
    'TwitterAccountType', 'TweetType', 'TweetStatus', 'EngagementType',
    'AnalyticsTimeframe', 'ContentCategory',
    
    # Dataclasses
    'TwitterCredentials', 'TweetMetrics',
    
    # Functions
    'get_twitter_engine', 'init_twitter_db', 'get_twitter_session',
    'create_twitter_user', 'update_user_metrics', 'create_tweet_record',
    'update_tweet_metrics', 'calculate_virality_score', 'get_user_analytics_summary'
] 