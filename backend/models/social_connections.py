from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, JSON, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class SocialConnection(Base):
    """Stores social media platform connections and OAuth tokens."""
    __tablename__ = 'social_connections'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)  # References the user
    session_id = Column(Integer, ForeignKey('onboarding_sessions.id'), nullable=True)  # Optional link to onboarding
    
    # Platform details
    platform = Column(String(50), nullable=False)  # facebook, twitter, instagram, linkedin, youtube, gsc, etc.
    platform_user_id = Column(String(255))  # User ID on the platform
    platform_username = Column(String(255))  # Username/handle on the platform
    
    # OAuth tokens
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    token_type = Column(String(50), default='Bearer')
    expires_at = Column(DateTime, nullable=True)
    
    # Scope permissions
    scopes = Column(JSON)  # List of granted scopes/permissions
    
    # Connection metadata
    profile_data = Column(JSON)  # Basic profile info from the platform
    connection_status = Column(String(50), default='active')  # active, expired, revoked, error
    
    # Settings
    auto_post_enabled = Column(Boolean, default=False)
    analytics_enabled = Column(Boolean, default=True)
    
    # Timestamps
    connected_at = Column(DateTime, default=func.now())
    last_used_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<SocialConnection(id={self.id}, platform={self.platform}, user_id={self.user_id}, status={self.connection_status})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses (excluding sensitive tokens)."""
        return {
            'id': self.id,
            'platform': self.platform,
            'platform_username': self.platform_username,
            'scopes': self.scopes,
            'profile_data': self.profile_data,
            'connection_status': self.connection_status,
            'auto_post_enabled': self.auto_post_enabled,
            'analytics_enabled': self.analytics_enabled,
            'connected_at': self.connected_at.isoformat() if self.connected_at else None,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }
    
    def is_token_expired(self):
        """Check if the access token is expired."""
        if not self.expires_at:
            return False
        return datetime.datetime.utcnow() > self.expires_at

class SocialPost(Base):
    """Stores posts made to social media platforms."""
    __tablename__ = 'social_posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    connection_id = Column(Integer, ForeignKey('social_connections.id', ondelete='CASCADE'), nullable=False)
    
    # Post content
    content = Column(Text, nullable=False)
    media_urls = Column(JSON)  # List of media URLs if any
    
    # Platform-specific data
    platform_post_id = Column(String(255))  # ID of the post on the platform
    platform_url = Column(String(500))  # URL to the post on the platform
    
    # Status
    status = Column(String(50), default='pending')  # pending, posted, failed, deleted
    error_message = Column(Text)
    
    # Analytics (to be updated via API calls)
    analytics_data = Column(JSON)  # Likes, shares, comments, reach, etc.
    last_analytics_update = Column(DateTime)
    
    # Timestamps
    scheduled_at = Column(DateTime)  # When the post was scheduled
    posted_at = Column(DateTime)  # When the post was actually posted
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    connection = relationship('SocialConnection')
    
    def __repr__(self):
        return f"<SocialPost(id={self.id}, platform={self.connection.platform if self.connection else 'unknown'}, status={self.status})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'connection_id': self.connection_id,
            'content': self.content,
            'media_urls': self.media_urls,
            'platform_post_id': self.platform_post_id,
            'platform_url': self.platform_url,
            'status': self.status,
            'error_message': self.error_message,
            'analytics_data': self.analytics_data,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'posted_at': self.posted_at.isoformat() if self.posted_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_analytics_update': self.last_analytics_update.isoformat() if self.last_analytics_update else None
        }

class SocialAnalytics(Base):
    """Stores analytics data from social media platforms."""
    __tablename__ = 'social_analytics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    connection_id = Column(Integer, ForeignKey('social_connections.id', ondelete='CASCADE'), nullable=False)
    
    # Analytics data
    metric_name = Column(String(100), nullable=False)  # followers, reach, impressions, etc.
    metric_value = Column(JSON, nullable=False)  # Value (could be number, array, object)
    date_range_start = Column(DateTime)
    date_range_end = Column(DateTime)
    
    # Metadata
    fetched_at = Column(DateTime, default=func.now())
    
    # Relationships
    connection = relationship('SocialConnection')
    
    def __repr__(self):
        return f"<SocialAnalytics(id={self.id}, metric={self.metric_name}, connection_id={self.connection_id})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'connection_id': self.connection_id,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'date_range_start': self.date_range_start.isoformat() if self.date_range_start else None,
            'date_range_end': self.date_range_end.isoformat() if self.date_range_end else None,
            'fetched_at': self.fetched_at.isoformat() if self.fetched_at else None
        }