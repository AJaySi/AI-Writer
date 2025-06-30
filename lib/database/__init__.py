"""
Database Package for ALwrity
============================

This package provides database models and services for managing data
in the ALwrity application, including Twitter-specific functionality.

Main Components:
- models.py: Core application database models
- twitter_models.py: Twitter-specific database models
- twitter_service.py: High-level Twitter database service
- twitter_init.py: Database initialization and management utilities

Usage:
    # Initialize Twitter database
    from lib.database import initialize_twitter_database
    initialize_twitter_database()
    
    # Use Twitter database service
    from lib.database import twitter_db
    user = twitter_db.create_or_update_user(user_data)
    
    # Use Twitter models directly
    from lib.database.twitter_models import TwitterUser, Tweet
"""

# Import core models
from .models import (
    SEOData, ContentType, Platform, ScheduleStatus,
    ContentItem, Schedule, create_engine, init_db, get_session
)

# Import Twitter-specific components
try:
    from .twitter_models import (
        # Models
        TwitterUser, Tweet, ScheduledTweet, TwitterAnalytics,
        TweetAnalytics, EngagementData, AudienceInsight,
        HashtagPerformance, ContentTemplate, TwitterSettings,
        
        # Enums and Data Classes
        TwitterAccountType, TweetType, TweetStatus, EngagementType,
        AnalyticsTimeframe, ContentCategory, TwitterCredentials, TweetMetrics,
        
        # Database functions
        get_twitter_engine, init_twitter_db, get_twitter_session,
        create_twitter_user, update_user_metrics, create_tweet_record,
        update_tweet_metrics, calculate_virality_score, get_user_analytics_summary
    )
    
    from .twitter_service import TwitterDatabaseService, twitter_db
    
    from .twitter_init import (
        TwitterDatabaseInitializer, initialize_twitter_database,
        check_twitter_database_health
    )
    
    TWITTER_AVAILABLE = True
    
except ImportError as e:
    # Twitter components not available (missing dependencies)
    TWITTER_AVAILABLE = False
    print(f"Warning: Twitter database components not available: {e}")

# Package metadata
__version__ = "1.0.0"
__author__ = "ALwrity Team"

# Export main components
__all__ = [
    # Core models
    'SEOData', 'ContentType', 'Platform', 'ScheduleStatus',
    'ContentItem', 'Schedule', 'create_engine', 'init_db', 'get_session',
    
    # Twitter availability flag
    'TWITTER_AVAILABLE',
]

# Add Twitter exports if available
if TWITTER_AVAILABLE:
    __all__.extend([
        # Twitter Models
        'TwitterUser', 'Tweet', 'ScheduledTweet', 'TwitterAnalytics',
        'TweetAnalytics', 'EngagementData', 'AudienceInsight',
        'HashtagPerformance', 'ContentTemplate', 'TwitterSettings',
        
        # Twitter Enums and Data Classes
        'TwitterAccountType', 'TweetType', 'TweetStatus', 'EngagementType',
        'AnalyticsTimeframe', 'ContentCategory', 'TwitterCredentials', 'TweetMetrics',
        
        # Twitter Database Functions
        'get_twitter_engine', 'init_twitter_db', 'get_twitter_session',
        'create_twitter_user', 'update_user_metrics', 'create_tweet_record',
        'update_tweet_metrics', 'calculate_virality_score', 'get_user_analytics_summary',
        
        # Twitter Service
        'TwitterDatabaseService', 'twitter_db',
        
        # Twitter Initialization
        'TwitterDatabaseInitializer', 'initialize_twitter_database',
        'check_twitter_database_health'
    ])

def setup_database(db_url: str = "sqlite:///alwrity.db", twitter_db_url: str = "sqlite:///twitter_data.db"):
    """
    Setup both core and Twitter databases.
    
    Args:
        db_url: URL for the core database
        twitter_db_url: URL for the Twitter database
        
    Returns:
        dict: Setup results
    """
    results = {
        'core_db': False,
        'twitter_db': False,
        'errors': []
    }
    
    try:
        # Initialize core database
        engine = create_engine(db_url)
        init_db(engine)
        results['core_db'] = True
    except Exception as e:
        results['errors'].append(f"Core database setup failed: {e}")
    
    if TWITTER_AVAILABLE:
        try:
            # Initialize Twitter database
            success = initialize_twitter_database(twitter_db_url)
            results['twitter_db'] = success
            if not success:
                results['errors'].append("Twitter database initialization failed")
        except Exception as e:
            results['errors'].append(f"Twitter database setup failed: {e}")
    else:
        results['errors'].append("Twitter database components not available")
    
    return results

def get_database_info():
    """
    Get information about available database components.
    
    Returns:
        dict: Database component information
    """
    info = {
        'core_models_available': True,
        'twitter_models_available': TWITTER_AVAILABLE,
        'version': __version__
    }
    
    if TWITTER_AVAILABLE:
        try:
            # Get Twitter database stats if service is available
            stats = twitter_db.get_database_stats()
            info['twitter_stats'] = stats
        except Exception as e:
            info['twitter_stats_error'] = str(e)
    
    return info 