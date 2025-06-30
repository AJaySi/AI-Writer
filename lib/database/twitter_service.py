"""
Twitter Database Service Layer
=============================

This module provides high-level service functions for managing Twitter data
in the database. It acts as an interface between the application and the
database models, providing convenient methods for common operations.

Key Features:
- User profile management and synchronization
- Tweet creation, updating, and analytics tracking
- Scheduled tweet management
- Analytics data aggregation and reporting
- Hashtag performance tracking
- Audience insights management
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
import json
from cryptography.fernet import Fernet
import os

from .twitter_models import (
    TwitterUser, Tweet, ScheduledTweet, TwitterAnalytics, TweetAnalytics,
    EngagementData, AudienceInsight, HashtagPerformance, ContentTemplate,
    TwitterSettings, TwitterCredentials, TweetMetrics,
    TwitterAccountType, TweetType, TweetStatus, EngagementType,
    AnalyticsTimeframe, ContentCategory,
    get_twitter_engine, init_twitter_db, get_twitter_session,
    create_twitter_user, update_user_metrics, create_tweet_record,
    update_tweet_metrics, calculate_virality_score, get_user_analytics_summary
)

# Configure logging
logger = logging.getLogger(__name__)

class TwitterDatabaseService:
    """
    High-level service for managing Twitter data in the database.
    """
    
    def __init__(self, db_url: str = "sqlite:///twitter_data.db", encryption_key: Optional[str] = None):
        """Initialize the Twitter database service."""
        self.engine = get_twitter_engine(db_url)
        self.encryption_key = encryption_key or self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key.encode() if isinstance(self.encryption_key, str) else self.encryption_key)
        
        # Initialize database
        init_twitter_db(self.engine)
        
        logger.info("Twitter database service initialized")
    
    def _get_or_create_encryption_key(self) -> str:
        """Get or create encryption key for sensitive data."""
        key_file = "twitter_encryption.key"
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def _encrypt_credentials(self, credentials: TwitterCredentials) -> str:
        """Encrypt Twitter credentials for secure storage."""
        credentials_json = json.dumps(credentials.to_dict())
        encrypted = self.cipher.encrypt(credentials_json.encode())
        return encrypted.decode()
    
    def _decrypt_credentials(self, encrypted_credentials: str) -> TwitterCredentials:
        """Decrypt Twitter credentials from storage."""
        try:
            decrypted = self.cipher.decrypt(encrypted_credentials.encode())
            credentials_dict = json.loads(decrypted.decode())
            return TwitterCredentials.from_dict(credentials_dict)
        except Exception as e:
            logger.error(f"Failed to decrypt credentials: {e}")
            return TwitterCredentials()
    
    def get_session(self) -> Session:
        """Get a database session."""
        return get_twitter_session(self.engine)
    
    # --- USER MANAGEMENT ---
    
    def create_or_update_user(self, user_data: Dict[str, Any]) -> TwitterUser:
        """Create a new Twitter user or update existing one."""
        session = self.get_session()
        try:
            # Check if user already exists
            existing_user = session.query(TwitterUser).filter_by(
                user_id=user_data['user_id']
            ).first()
            
            if existing_user:
                # Update existing user
                for key, value in user_data.items():
                    if hasattr(existing_user, key) and key != 'id':
                        setattr(existing_user, key, value)
                existing_user.updated_at = datetime.utcnow()
                session.commit()
                logger.info(f"Updated Twitter user: {existing_user.username}")
                return existing_user
            else:
                # Create new user
                twitter_user = create_twitter_user(session, user_data)
                logger.info(f"Created new Twitter user: {twitter_user.username}")
                return twitter_user
                
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating/updating user: {e}")
            raise
        finally:
            session.close()
    
    def save_user_credentials(self, user_id: str, credentials: TwitterCredentials) -> bool:
        """Save encrypted Twitter credentials for a user."""
        session = self.get_session()
        try:
            user = session.query(TwitterUser).filter_by(user_id=user_id).first()
            if user:
                encrypted_creds = self._encrypt_credentials(credentials)
                user.credentials_encrypted = encrypted_creds
                user.updated_at = datetime.utcnow()
                session.commit()
                logger.info(f"Saved credentials for user: {user.username}")
                return True
            else:
                logger.error(f"User not found: {user_id}")
                return False
                
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving credentials: {e}")
            return False
        finally:
            session.close()
    
    def get_user_credentials(self, user_id: str) -> Optional[TwitterCredentials]:
        """Get decrypted Twitter credentials for a user."""
        session = self.get_session()
        try:
            user = session.query(TwitterUser).filter_by(user_id=user_id).first()
            if user and user.credentials_encrypted:
                return self._decrypt_credentials(user.credentials_encrypted)
            return None
            
        except Exception as e:
            logger.error(f"Error getting credentials: {e}")
            return None
        finally:
            session.close()
    
    def get_user_by_id(self, user_id: str) -> Optional[TwitterUser]:
        """Get Twitter user by ALwrity user ID."""
        session = self.get_session()
        try:
            return session.query(TwitterUser).filter_by(user_id=user_id).first()
        finally:
            session.close()
    
    def get_user_by_twitter_id(self, twitter_user_id: int) -> Optional[TwitterUser]:
        """Get Twitter user by Twitter user ID."""
        session = self.get_session()
        try:
            return session.query(TwitterUser).filter_by(twitter_user_id=twitter_user_id).first()
        finally:
            session.close()
    
    def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Update user profile information from Twitter API."""
        session = self.get_session()
        try:
            user = session.query(TwitterUser).filter_by(user_id=user_id).first()
            if user:
                update_user_metrics(session, user.id, profile_data)
                logger.info(f"Updated profile for user: {user.username}")
                return True
            return False
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating user profile: {e}")
            return False
        finally:
            session.close()
    
    # --- TWEET MANAGEMENT ---
    
    def save_tweet(self, tweet_data: Dict[str, Any]) -> Tweet:
        """Save a tweet to the database."""
        session = self.get_session()
        try:
            tweet = create_tweet_record(session, tweet_data)
            logger.info(f"Saved tweet: {tweet.id}")
            return tweet
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving tweet: {e}")
            raise
        finally:
            session.close()
    
    def update_tweet_status(self, tweet_id: int, status: TweetStatus, twitter_tweet_id: Optional[int] = None) -> bool:
        """Update tweet status (e.g., from draft to posted)."""
        session = self.get_session()
        try:
            tweet = session.query(Tweet).filter_by(id=tweet_id).first()
            if tweet:
                tweet.status = status
                if twitter_tweet_id:
                    tweet.tweet_id = twitter_tweet_id
                if status == TweetStatus.POSTED:
                    tweet.posted_at = datetime.utcnow()
                tweet.updated_at = datetime.utcnow()
                session.commit()
                logger.info(f"Updated tweet {tweet_id} status to {status.value}")
                return True
            return False
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating tweet status: {e}")
            return False
        finally:
            session.close()
    
    def get_user_tweets(self, user_id: str, status: Optional[TweetStatus] = None, limit: int = 50) -> List[Tweet]:
        """Get tweets for a user, optionally filtered by status."""
        session = self.get_session()
        try:
            user = session.query(TwitterUser).filter_by(user_id=user_id).first()
            if not user:
                return []
            
            query = session.query(Tweet).filter_by(user_id=user.id)
            
            if status:
                query = query.filter_by(status=status)
            
            return query.order_by(desc(Tweet.created_at)).limit(limit).all()
            
        finally:
            session.close()
    
    def get_tweet_by_id(self, tweet_id: int) -> Optional[Tweet]:
        """Get tweet by database ID."""
        session = self.get_session()
        try:
            return session.query(Tweet).filter_by(id=tweet_id).first()
        finally:
            session.close()
    
    def get_tweet_by_twitter_id(self, twitter_tweet_id: int) -> Optional[Tweet]:
        """Get tweet by Twitter tweet ID."""
        session = self.get_session()
        try:
            return session.query(Tweet).filter_by(tweet_id=twitter_tweet_id).first()
        finally:
            session.close()
    
    def update_tweet_analytics(self, tweet_id: int, metrics: TweetMetrics) -> bool:
        """Update tweet analytics from Twitter API."""
        session = self.get_session()
        try:
            update_tweet_metrics(session, tweet_id, metrics)
            logger.info(f"Updated analytics for tweet: {tweet_id}")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating tweet analytics: {e}")
            return False
        finally:
            session.close()
    
    def get_top_performing_tweets(self, user_id: str, days: int = 30, limit: int = 10) -> List[Tweet]:
        """Get top performing tweets for a user."""
        session = self.get_session()
        try:
            user = session.query(TwitterUser).filter_by(user_id=user_id).first()
            if not user:
                return []
            
            start_date = datetime.utcnow() - timedelta(days=days)
            
            return session.query(Tweet).filter(
                and_(
                    Tweet.user_id == user.id,
                    Tweet.status == TweetStatus.POSTED,
                    Tweet.posted_at >= start_date
                )
            ).order_by(desc(Tweet.engagement_rate)).limit(limit).all()
            
        finally:
            session.close()
    
    # --- SCHEDULED TWEETS ---
    
    def schedule_tweet(self, tweet_id: int, scheduled_time: datetime, settings: Dict[str, Any] = None) -> ScheduledTweet:
        """Schedule a tweet for posting."""
        session = self.get_session()
        try:
            tweet = session.query(Tweet).filter_by(id=tweet_id).first()
            if not tweet:
                raise ValueError(f"Tweet {tweet_id} not found")
            
            scheduled_tweet = ScheduledTweet(
                user_id=tweet.user_id,
                tweet_id=tweet_id,
                scheduled_time=scheduled_time,
                timezone=settings.get('timezone', 'UTC'),
                auto_optimize_time=settings.get('auto_optimize_time', False),
                auto_add_hashtags=settings.get('auto_add_hashtags', False),
                auto_add_emojis=settings.get('auto_add_emojis', False)
            )
            
            session.add(scheduled_tweet)
            
            # Update tweet status
            tweet.status = TweetStatus.SCHEDULED
            tweet.scheduled_for = scheduled_time
            
            session.commit()
            logger.info(f"Scheduled tweet {tweet_id} for {scheduled_time}")
            return scheduled_tweet
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error scheduling tweet: {e}")
            raise
        finally:
            session.close()
    
    def get_pending_scheduled_tweets(self, user_id: Optional[str] = None) -> List[ScheduledTweet]:
        """Get tweets scheduled for posting."""
        session = self.get_session()
        try:
            query = session.query(ScheduledTweet).filter(
                and_(
                    ScheduledTweet.status == TweetStatus.SCHEDULED,
                    ScheduledTweet.scheduled_time <= datetime.utcnow()
                )
            )
            
            if user_id:
                user = session.query(TwitterUser).filter_by(user_id=user_id).first()
                if user:
                    query = query.filter_by(user_id=user.id)
            
            return query.order_by(ScheduledTweet.scheduled_time).all()
            
        finally:
            session.close()
    
    def mark_scheduled_tweet_posted(self, scheduled_tweet_id: int, twitter_tweet_id: int) -> bool:
        """Mark a scheduled tweet as posted."""
        session = self.get_session()
        try:
            scheduled_tweet = session.query(ScheduledTweet).filter_by(id=scheduled_tweet_id).first()
            if scheduled_tweet:
                scheduled_tweet.status = TweetStatus.POSTED
                
                # Update the associated tweet
                tweet = session.query(Tweet).filter_by(id=scheduled_tweet.tweet_id).first()
                if tweet:
                    tweet.status = TweetStatus.POSTED
                    tweet.tweet_id = twitter_tweet_id
                    tweet.posted_at = datetime.utcnow()
                
                session.commit()
                logger.info(f"Marked scheduled tweet {scheduled_tweet_id} as posted")
                return True
            return False
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error marking scheduled tweet as posted: {e}")
            return False
        finally:
            session.close()
    
    # --- ANALYTICS ---
    
    def save_daily_analytics(self, user_id: str, analytics_data: Dict[str, Any]) -> TwitterAnalytics:
        """Save daily analytics data for a user."""
        session = self.get_session()
        try:
            user = session.query(TwitterUser).filter_by(user_id=user_id).first()
            if not user:
                raise ValueError(f"User {user_id} not found")
            
            # Check if analytics for today already exist
            today = datetime.utcnow().date()
            existing = session.query(TwitterAnalytics).filter(
                and_(
                    TwitterAnalytics.user_id == user.id,
                    func.date(TwitterAnalytics.date) == today,
                    TwitterAnalytics.timeframe == AnalyticsTimeframe.DAILY
                )
            ).first()
            
            if existing:
                # Update existing record
                for key, value in analytics_data.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                existing.updated_at = datetime.utcnow()
                session.commit()
                return existing
            else:
                # Create new record
                analytics = TwitterAnalytics(
                    user_id=user.id,
                    date=datetime.utcnow(),
                    timeframe=AnalyticsTimeframe.DAILY,
                    **analytics_data
                )
                session.add(analytics)
                session.commit()
                logger.info(f"Saved daily analytics for user: {user.username}")
                return analytics
                
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving analytics: {e}")
            raise
        finally:
            session.close()
    
    def get_analytics_summary(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive analytics summary for a user."""
        session = self.get_session()
        try:
            return get_user_analytics_summary(session, user_id, days)
        finally:
            session.close()
    
    def get_engagement_trends(self, user_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get engagement trends over time."""
        session = self.get_session()
        try:
            user = session.query(TwitterUser).filter_by(user_id=user_id).first()
            if not user:
                return []
            
            start_date = datetime.utcnow() - timedelta(days=days)
            
            analytics = session.query(TwitterAnalytics).filter(
                and_(
                    TwitterAnalytics.user_id == user.id,
                    TwitterAnalytics.date >= start_date,
                    TwitterAnalytics.timeframe == AnalyticsTimeframe.DAILY
                )
            ).order_by(TwitterAnalytics.date).all()
            
            return [
                {
                    'date': a.date.isoformat(),
                    'engagement_rate': a.average_engagement_rate,
                    'total_engagements': a.total_engagements,
                    'impressions': a.total_impressions,
                    'followers_change': a.net_follower_change
                }
                for a in analytics
            ]
            
        finally:
            session.close()
    
    # --- HASHTAG PERFORMANCE ---
    
    def track_hashtag_performance(self, user_id: str, hashtag: str, tweet_id: int, engagement_metrics: Dict[str, Any]) -> bool:
        """Track performance of a hashtag."""
        session = self.get_session()
        try:
            user = session.query(TwitterUser).filter_by(user_id=user_id).first()
            if not user:
                return False
            
            # Get or create hashtag performance record
            hashtag_perf = session.query(HashtagPerformance).filter(
                and_(
                    HashtagPerformance.user_id == user.id,
                    HashtagPerformance.hashtag == hashtag
                )
            ).first()
            
            if hashtag_perf:
                # Update existing record
                hashtag_perf.usage_count += 1
                hashtag_perf.total_impressions += engagement_metrics.get('impressions', 0)
                hashtag_perf.total_engagements += engagement_metrics.get('engagements', 0)
                hashtag_perf.last_used = datetime.utcnow()
                
                # Update average engagement rate
                if hashtag_perf.usage_count > 0:
                    hashtag_perf.average_engagement_rate = (
                        hashtag_perf.total_engagements / hashtag_perf.total_impressions * 100
                        if hashtag_perf.total_impressions > 0 else 0
                    )
                
                # Update best performing tweet if this one is better
                current_engagement = engagement_metrics.get('engagements', 0)
                if current_engagement > hashtag_perf.best_tweet_engagement:
                    hashtag_perf.best_tweet_id = tweet_id
                    hashtag_perf.best_tweet_engagement = current_engagement
                    
            else:
                # Create new record
                hashtag_perf = HashtagPerformance(
                    user_id=user.id,
                    hashtag=hashtag,
                    usage_count=1,
                    total_impressions=engagement_metrics.get('impressions', 0),
                    total_engagements=engagement_metrics.get('engagements', 0),
                    average_engagement_rate=(
                        engagement_metrics.get('engagements', 0) / 
                        max(engagement_metrics.get('impressions', 1), 1) * 100
                    ),
                    best_tweet_id=tweet_id,
                    best_tweet_engagement=engagement_metrics.get('engagements', 0),
                    first_used=datetime.utcnow(),
                    last_used=datetime.utcnow()
                )
                session.add(hashtag_perf)
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error tracking hashtag performance: {e}")
            return False
        finally:
            session.close()
    
    def get_top_hashtags(self, user_id: str, limit: int = 10) -> List[HashtagPerformance]:
        """Get top performing hashtags for a user."""
        session = self.get_session()
        try:
            user = session.query(TwitterUser).filter_by(user_id=user_id).first()
            if not user:
                return []
            
            return session.query(HashtagPerformance).filter_by(
                user_id=user.id
            ).order_by(desc(HashtagPerformance.average_engagement_rate)).limit(limit).all()
            
        finally:
            session.close()
    
    # --- CONTENT TEMPLATES ---
    
    def save_content_template(self, user_id: str, template_data: Dict[str, Any]) -> ContentTemplate:
        """Save a content template."""
        session = self.get_session()
        try:
            user = session.query(TwitterUser).filter_by(user_id=user_id).first()
            if not user:
                raise ValueError(f"User {user_id} not found")
            
            template = ContentTemplate(
                user_id=user.id,
                name=template_data['name'],
                description=template_data.get('description', ''),
                template_text=template_data['template_text'],
                category=ContentCategory(template_data['category']) if template_data.get('category') else None,
                variables=template_data.get('variables', []),
                default_hashtags=template_data.get('default_hashtags', []),
                ai_prompt=template_data.get('ai_prompt', ''),
                ai_tone=template_data.get('ai_tone', ''),
                ai_target_audience=template_data.get('ai_target_audience', '')
            )
            
            session.add(template)
            session.commit()
            logger.info(f"Saved content template: {template.name}")
            return template
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving content template: {e}")
            raise
        finally:
            session.close()
    
    def get_user_templates(self, user_id: str, category: Optional[ContentCategory] = None) -> List[ContentTemplate]:
        """Get content templates for a user."""
        session = self.get_session()
        try:
            user = session.query(TwitterUser).filter_by(user_id=user_id).first()
            if not user:
                return []
            
            query = session.query(ContentTemplate).filter(
                and_(
                    ContentTemplate.user_id == user.id,
                    ContentTemplate.is_active == True
                )
            )
            
            if category:
                query = query.filter_by(category=category)
            
            return query.order_by(desc(ContentTemplate.average_performance)).all()
            
        finally:
            session.close()
    
    # --- SETTINGS ---
    
    def save_user_settings(self, user_id: str, settings_data: Dict[str, Any]) -> TwitterSettings:
        """Save user Twitter settings."""
        session = self.get_session()
        try:
            user = session.query(TwitterUser).filter_by(user_id=user_id).first()
            if not user:
                raise ValueError(f"User {user_id} not found")
            
            # Check if settings already exist
            existing_settings = session.query(TwitterSettings).filter_by(user_id=user.id).first()
            
            if existing_settings:
                # Update existing settings
                for key, value in settings_data.items():
                    if hasattr(existing_settings, key):
                        setattr(existing_settings, key, value)
                existing_settings.updated_at = datetime.utcnow()
                session.commit()
                return existing_settings
            else:
                # Create new settings
                settings = TwitterSettings(
                    user_id=user.id,
                    **settings_data
                )
                session.add(settings)
                session.commit()
                logger.info(f"Saved settings for user: {user.username}")
                return settings
                
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving user settings: {e}")
            raise
        finally:
            session.close()
    
    def get_user_settings(self, user_id: str) -> Optional[TwitterSettings]:
        """Get user Twitter settings."""
        session = self.get_session()
        try:
            user = session.query(TwitterUser).filter_by(user_id=user_id).first()
            if not user:
                return None
            
            return session.query(TwitterSettings).filter_by(user_id=user.id).first()
            
        finally:
            session.close()
    
    # --- UTILITY METHODS ---
    
    def cleanup_old_data(self, days_old: int = 30) -> Dict[str, int]:
        """
        Clean up old data to maintain database performance.
        
        Args:
            days_old: Number of days old data to keep
            
        Returns:
            Dictionary with cleanup statistics
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
            with self.get_session() as session:
                # Clean up old analytics data
                old_analytics = session.query(TwitterAnalytics).filter(
                    TwitterAnalytics.created_at < cutoff_date
                ).count()
                
                session.query(TwitterAnalytics).filter(
                    TwitterAnalytics.created_at < cutoff_date
                ).delete()
                
                # Clean up old tweet analytics
                old_tweet_analytics = session.query(TweetAnalytics).filter(
                    TweetAnalytics.created_at < cutoff_date
                ).count()
                
                session.query(TweetAnalytics).filter(
                    TweetAnalytics.created_at < cutoff_date
                ).delete()
                
                session.commit()
                
                stats = {
                    'old_analytics_removed': old_analytics,
                    'old_tweet_analytics_removed': old_tweet_analytics,
                    'cutoff_date': cutoff_date.isoformat()
                }
                
                logger.info(f"Cleaned up old data: {stats}")
                return stats
                
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            return {'error': str(e)}
    
    def get_database_stats(self) -> Dict[str, int]:
        """
        Get database statistics.
        
        Returns:
            Dictionary with database statistics
        """
        try:
            with self.get_session() as session:
                stats = {
                    'total_users': session.query(TwitterUser).count(),
                    'total_tweets': session.query(Tweet).count(),
                    'posted_tweets': session.query(Tweet).filter(
                        Tweet.status == TweetStatus.POSTED
                    ).count(),
                    'scheduled_tweets': session.query(ScheduledTweet).filter(
                        ScheduledTweet.status == TweetStatus.SCHEDULED
                    ).count(),
                    'total_analytics_records': session.query(TwitterAnalytics).count(),
                    'total_templates': session.query(ContentTemplate).count()
                }
                
                return stats
                
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {'error': str(e)}
    
    def close(self):
        """
        Close database connections and clean up resources.
        """
        try:
            if hasattr(self, 'engine') and self.engine:
                self.engine.dispose()
                logger.info("Database connections closed successfully")
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")

# Create a global instance for easy access
twitter_db = TwitterDatabaseService()

# Export the service and key functions
__all__ = [
    'TwitterDatabaseService',
    'twitter_db'
] 