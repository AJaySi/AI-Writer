"""
Twitter Database Initialization and Migration Script
===================================================

This module provides utilities for initializing the Twitter database,
handling schema migrations, and managing database setup.

Features:
- Database initialization and table creation
- Schema migration utilities
- Data seeding for development/testing
- Database health checks and maintenance
"""

import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from pathlib import Path

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from .twitter_models import (
    Base, TwitterUser, Tweet, ScheduledTweet, TwitterAnalytics,
    TweetAnalytics, EngagementData, AudienceInsight, HashtagPerformance,
    ContentTemplate, TwitterSettings, TwitterAccountType, TweetType,
    TweetStatus, EngagementType, AnalyticsTimeframe, ContentCategory
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwitterDatabaseInitializer:
    """
    Handles Twitter database initialization and management.
    """
    
    def __init__(self, db_url: str = "sqlite:///twitter_data.db"):
        """Initialize the database initializer."""
        self.db_url = db_url
        self.engine = create_engine(db_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create database directory if using SQLite
        if db_url.startswith('sqlite:///'):
            db_path = db_url.replace('sqlite:///', '')
            os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    
    def initialize_database(self, force_recreate: bool = False) -> bool:
        """
        Initialize the Twitter database with all required tables.
        
        Args:
            force_recreate: If True, drop existing tables and recreate
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if force_recreate:
                logger.info("Dropping existing tables...")
                Base.metadata.drop_all(bind=self.engine)
            
            logger.info("Creating Twitter database tables...")
            Base.metadata.create_all(bind=self.engine)
            
            # Verify tables were created
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            
            expected_tables = [
                'twitter_users', 'tweets', 'scheduled_tweets', 'twitter_analytics',
                'tweet_analytics', 'engagement_data', 'audience_insights',
                'hashtag_performance', 'content_templates', 'twitter_settings'
            ]
            
            missing_tables = [table for table in expected_tables if table not in tables]
            
            if missing_tables:
                logger.error(f"Missing tables: {missing_tables}")
                return False
            
            logger.info(f"Successfully created {len(tables)} tables")
            
            # Create indexes for better performance
            self._create_indexes()
            
            # Seed initial data if needed
            self._seed_initial_data()
            
            logger.info("Twitter database initialization completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            return False
    
    def _create_indexes(self):
        """Create database indexes for better query performance."""
        try:
            with self.engine.connect() as conn:
                # User indexes
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_twitter_users_user_id ON twitter_users(user_id)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_twitter_users_twitter_user_id ON twitter_users(twitter_user_id)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_twitter_users_username ON twitter_users(username)"))
                
                # Tweet indexes
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tweets_user_id ON tweets(user_id)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tweets_status ON tweets(status)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tweets_posted_at ON tweets(posted_at)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tweets_tweet_id ON tweets(tweet_id)"))
                
                # Scheduled tweet indexes
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_scheduled_tweets_user_id ON scheduled_tweets(user_id)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_scheduled_tweets_status ON scheduled_tweets(status)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_scheduled_tweets_scheduled_time ON scheduled_tweets(scheduled_time)"))
                
                # Analytics indexes
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_twitter_analytics_user_id ON twitter_analytics(user_id)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_twitter_analytics_date ON twitter_analytics(date)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_twitter_analytics_timeframe ON twitter_analytics(timeframe)"))
                
                # Tweet analytics indexes
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tweet_analytics_tweet_id ON tweet_analytics(tweet_id)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tweet_analytics_recorded_at ON tweet_analytics(recorded_at)"))
                
                # Engagement data indexes
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_engagement_data_tweet_id ON engagement_data(tweet_id)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_engagement_data_occurred_at ON engagement_data(occurred_at)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_engagement_data_type ON engagement_data(engagement_type)"))
                
                # Hashtag performance indexes
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_hashtag_performance_user_id ON hashtag_performance(user_id)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_hashtag_performance_hashtag ON hashtag_performance(hashtag)"))
                
                # Content template indexes
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_content_templates_user_id ON content_templates(user_id)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_content_templates_category ON content_templates(category)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_content_templates_is_active ON content_templates(is_active)"))
                
                conn.commit()
                logger.info("Database indexes created successfully")
                
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
    
    def _seed_initial_data(self):
        """Seed the database with initial data for development/testing."""
        try:
            session = self.SessionLocal()
            
            # Check if we already have data
            if session.query(TwitterUser).count() > 0:
                logger.info("Database already contains data, skipping seeding")
                session.close()
                return
            
            # Create sample content templates
            sample_templates = [
                {
                    'name': 'Daily Motivation',
                    'description': 'Motivational quotes and thoughts',
                    'template_text': 'Start your day with this thought: {quote} #motivation #success',
                    'category': ContentCategory.PERSONAL,
                    'variables': ['quote'],
                    'default_hashtags': ['#motivation', '#success', '#mindset'],
                    'ai_prompt': 'Generate an inspiring motivational quote',
                    'ai_tone': 'inspirational',
                    'ai_target_audience': 'professionals and entrepreneurs'
                },
                {
                    'name': 'Tech News Share',
                    'description': 'Template for sharing tech news',
                    'template_text': 'Interesting development in {topic}: {summary} {link} #tech #innovation',
                    'category': ContentCategory.EDUCATIONAL,
                    'variables': ['topic', 'summary', 'link'],
                    'default_hashtags': ['#tech', '#innovation', '#technology'],
                    'ai_prompt': 'Summarize this tech news in an engaging way',
                    'ai_tone': 'informative',
                    'ai_target_audience': 'tech enthusiasts and professionals'
                },
                {
                    'name': 'Question Engagement',
                    'description': 'Template for asking engaging questions',
                    'template_text': 'Quick question for my followers: {question} What do you think? #community #discussion',
                    'category': ContentCategory.QUESTION,
                    'variables': ['question'],
                    'default_hashtags': ['#community', '#discussion', '#question'],
                    'ai_prompt': 'Generate an engaging question for social media',
                    'ai_tone': 'conversational',
                    'ai_target_audience': 'general audience'
                },
                {
                    'name': 'Product Update',
                    'description': 'Template for product announcements',
                    'template_text': 'Excited to share: {update} {details} #product #update #announcement',
                    'category': ContentCategory.PROMOTIONAL,
                    'variables': ['update', 'details'],
                    'default_hashtags': ['#product', '#update', '#announcement'],
                    'ai_prompt': 'Write an exciting product update announcement',
                    'ai_tone': 'enthusiastic',
                    'ai_target_audience': 'customers and prospects'
                }
            ]
            
            # Note: We can't create templates without a user, so we'll skip this for now
            # In a real scenario, templates would be created when users are added
            
            session.close()
            logger.info("Initial data seeding completed")
            
        except Exception as e:
            logger.error(f"Error seeding initial data: {e}")
    
    def check_database_health(self) -> Dict[str, Any]:
        """
        Check the health and status of the Twitter database.
        
        Returns:
            Dict containing health check results
        """
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'tables': {},
            'indexes': {},
            'issues': []
        }
        
        try:
            inspector = inspect(self.engine)
            
            # Check table existence and row counts
            expected_tables = [
                'twitter_users', 'tweets', 'scheduled_tweets', 'twitter_analytics',
                'tweet_analytics', 'engagement_data', 'audience_insights',
                'hashtag_performance', 'content_templates', 'twitter_settings'
            ]
            
            session = self.SessionLocal()
            
            for table_name in expected_tables:
                if table_name in inspector.get_table_names():
                    # Get row count
                    try:
                        result = session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                        count = result.scalar()
                        health_status['tables'][table_name] = {
                            'exists': True,
                            'row_count': count
                        }
                    except Exception as e:
                        health_status['tables'][table_name] = {
                            'exists': True,
                            'row_count': 'error',
                            'error': str(e)
                        }
                        health_status['issues'].append(f"Error counting rows in {table_name}: {e}")
                else:
                    health_status['tables'][table_name] = {'exists': False}
                    health_status['issues'].append(f"Missing table: {table_name}")
            
            # Check indexes
            for table_name in inspector.get_table_names():
                indexes = inspector.get_indexes(table_name)
                health_status['indexes'][table_name] = len(indexes)
            
            session.close()
            
            # Set overall status
            if health_status['issues']:
                health_status['status'] = 'issues_found'
            
            return health_status
            
        except Exception as e:
            health_status['status'] = 'error'
            health_status['error'] = str(e)
            logger.error(f"Error checking database health: {e}")
            return health_status
    
    def backup_database(self, backup_path: str) -> bool:
        """
        Create a backup of the database.
        
        Args:
            backup_path: Path where to save the backup
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.db_url.startswith('sqlite:///'):
                logger.error("Backup currently only supported for SQLite databases")
                return False
            
            # Get the database file path
            db_file = self.db_url.replace('sqlite:///', '')
            
            if not os.path.exists(db_file):
                logger.error(f"Database file not found: {db_file}")
                return False
            
            # Create backup directory if it doesn't exist
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            # Copy the database file
            import shutil
            shutil.copy2(db_file, backup_path)
            
            logger.info(f"Database backed up to: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error backing up database: {e}")
            return False
    
    def restore_database(self, backup_path: str) -> bool:
        """
        Restore database from a backup.
        
        Args:
            backup_path: Path to the backup file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.db_url.startswith('sqlite:///'):
                logger.error("Restore currently only supported for SQLite databases")
                return False
            
            if not os.path.exists(backup_path):
                logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Get the database file path
            db_file = self.db_url.replace('sqlite:///', '')
            
            # Copy the backup file to the database location
            import shutil
            shutil.copy2(backup_path, db_file)
            
            logger.info(f"Database restored from: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring database: {e}")
            return False
    
    def migrate_schema(self, migration_scripts: List[str]) -> bool:
        """
        Apply schema migration scripts.
        
        Args:
            migration_scripts: List of SQL migration scripts
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self.engine.connect() as conn:
                # Create migration tracking table if it doesn't exist
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS schema_migrations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        migration_name TEXT NOT NULL UNIQUE,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                for script in migration_scripts:
                    # Check if migration was already applied
                    result = conn.execute(text(
                        "SELECT COUNT(*) FROM schema_migrations WHERE migration_name = :name"
                    ), {"name": script})
                    
                    if result.scalar() == 0:
                        # Apply migration
                        logger.info(f"Applying migration: {script}")
                        
                        # Read and execute migration script
                        script_path = Path(script)
                        if script_path.exists():
                            with open(script_path, 'r') as f:
                                migration_sql = f.read()
                            
                            conn.execute(text(migration_sql))
                            
                            # Record migration as applied
                            conn.execute(text(
                                "INSERT INTO schema_migrations (migration_name) VALUES (:name)"
                            ), {"name": script})
                        else:
                            logger.error(f"Migration script not found: {script}")
                            return False
                    else:
                        logger.info(f"Migration already applied: {script}")
                
                conn.commit()
                logger.info("Schema migration completed successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error applying schema migration: {e}")
            return False
    
    def cleanup_old_data(self, days: int = 90) -> Dict[str, int]:
        """
        Clean up old data to maintain database performance.
        
        Args:
            days: Number of days to keep data for
            
        Returns:
            Dict with cleanup statistics
        """
        try:
            cutoff_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            cutoff_date = cutoff_date.replace(day=cutoff_date.day - days)
            
            session = self.SessionLocal()
            
            # Count records to be deleted
            old_tweet_analytics = session.query(TweetAnalytics).filter(
                TweetAnalytics.recorded_at < cutoff_date
            ).count()
            
            old_engagement_data = session.query(EngagementData).filter(
                EngagementData.occurred_at < cutoff_date
            ).count()
            
            # Delete old records
            session.query(TweetAnalytics).filter(
                TweetAnalytics.recorded_at < cutoff_date
            ).delete()
            
            session.query(EngagementData).filter(
                EngagementData.occurred_at < cutoff_date
            ).delete()
            
            session.commit()
            session.close()
            
            cleanup_stats = {
                'tweet_analytics_deleted': old_tweet_analytics,
                'engagement_data_deleted': old_engagement_data,
                'cutoff_date': cutoff_date.isoformat()
            }
            
            logger.info(f"Cleanup completed: {cleanup_stats}")
            return cleanup_stats
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            return {'error': str(e)}

def initialize_twitter_database(db_url: str = "sqlite:///twitter_data.db", force_recreate: bool = False) -> bool:
    """
    Convenience function to initialize the Twitter database.
    
    Args:
        db_url: Database URL
        force_recreate: Whether to recreate existing tables
        
    Returns:
        bool: True if successful, False otherwise
    """
    initializer = TwitterDatabaseInitializer(db_url)
    return initializer.initialize_database(force_recreate)

def check_twitter_database_health(db_url: str = "sqlite:///twitter_data.db") -> Dict[str, Any]:
    """
    Convenience function to check Twitter database health.
    
    Args:
        db_url: Database URL
        
    Returns:
        Dict with health check results
    """
    initializer = TwitterDatabaseInitializer(db_url)
    return initializer.check_database_health()

if __name__ == "__main__":
    # Command line interface for database management
    import argparse
    
    parser = argparse.ArgumentParser(description="Twitter Database Management")
    parser.add_argument("--db-url", default="sqlite:///twitter_data.db", help="Database URL")
    parser.add_argument("--init", action="store_true", help="Initialize database")
    parser.add_argument("--force", action="store_true", help="Force recreate tables")
    parser.add_argument("--health", action="store_true", help="Check database health")
    parser.add_argument("--backup", help="Create database backup")
    parser.add_argument("--restore", help="Restore from backup")
    parser.add_argument("--cleanup", type=int, help="Cleanup data older than N days")
    
    args = parser.parse_args()
    
    initializer = TwitterDatabaseInitializer(args.db_url)
    
    if args.init:
        success = initializer.initialize_database(args.force)
        print(f"Database initialization: {'SUCCESS' if success else 'FAILED'}")
    
    if args.health:
        health = initializer.check_database_health()
        print(json.dumps(health, indent=2))
    
    if args.backup:
        success = initializer.backup_database(args.backup)
        print(f"Database backup: {'SUCCESS' if success else 'FAILED'}")
    
    if args.restore:
        success = initializer.restore_database(args.restore)
        print(f"Database restore: {'SUCCESS' if success else 'FAILED'}")
    
    if args.cleanup:
        stats = initializer.cleanup_old_data(args.cleanup)
        print(f"Cleanup completed: {stats}") 