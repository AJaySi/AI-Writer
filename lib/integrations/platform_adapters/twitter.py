"""
Twitter platform adapter implementation with enhanced error handling and real metrics.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import tweepy
from tweepy.models import Status
import logging
import time

from .base import PlatformAdapter

logger = logging.getLogger(__name__)

class TwitterAdapter(PlatformAdapter):
    """Enhanced Twitter platform adapter with real metrics and error handling."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Twitter adapter with configuration."""
        super().__init__(config)
        self._validate_config()
        self._initialize_client()
        self.rate_limit_tracker = {}
    
    def _initialize_client(self) -> None:
        """Initialize Twitter API client with enhanced error handling."""
        try:
            # Initialize OAuth handler
            auth = tweepy.OAuthHandler(
                self.config['api_key'],
                self.config['api_secret']
            )
            auth.set_access_token(
                self.config['access_token'],
                self.config['access_token_secret']
            )
            
            # Create API client with wait_on_rate_limit
            self.client = tweepy.API(
                auth, 
                wait_on_rate_limit=True,
                retry_count=3,
                retry_delay=5
            )
            
            # Verify credentials
            user = self.client.verify_credentials()
            if not user:
                raise Exception("Failed to verify Twitter credentials")
                
            logger.info(f"Twitter client initialized for @{user.screen_name}")
            
        except tweepy.Unauthorized:
            raise Exception("Invalid Twitter API credentials")
        except tweepy.Forbidden:
            raise Exception("Access forbidden - check API permissions")
        except Exception as e:
            raise Exception(f"Failed to initialize Twitter client: {str(e)}")
    
    async def publish_content(
        self,
        content: Dict[str, Any],
        schedule_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Publish content to Twitter with enhanced error handling."""
        try:
            # Validate content first
            validation = await self.validate_content(content)
            if not validation.get('success'):
                return validation
            
            # Check rate limits
            if not self._check_rate_limit('tweets'):
                return self._format_error_response(
                    Exception("Rate limit exceeded for tweets"),
                    {'content': content}
                )
            
            # Prepare tweet content
            tweet_text = content.get('text', '')
            media_ids = []
            
            # Handle media attachments if present
            if 'media' in content and content['media']:
                for media in content['media']:
                    media_id = self._upload_media(media)
                    if media_id:
                        media_ids.append(media_id)
            
            # Create tweet
            tweet = self.client.update_status(
                status=tweet_text,
                media_ids=media_ids if media_ids else None
            )
            
            # Update rate limit tracker
            self._update_rate_limit_tracker('tweets')
            
            # Format response with comprehensive data
            tweet_data = {
                'id': tweet.id_str,
                'text': tweet.text,
                'created_at': tweet.created_at.isoformat(),
                'user': {
                    'screen_name': tweet.user.screen_name,
                    'name': tweet.user.name,
                    'followers_count': tweet.user.followers_count
                },
                'metrics': {
                    'retweet_count': tweet.retweet_count,
                    'favorite_count': tweet.favorite_count,
                    'reply_count': getattr(tweet, 'reply_count', 0)
                },
                'urls': {
                    'tweet_url': f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}"
                }
            }
            
            return self._format_success_response(tweet_data)
            
        except tweepy.Unauthorized:
            return self._format_error_response(
                Exception("Authentication failed - please reconnect your account"),
                {'content': content}
            )
        except tweepy.Forbidden as e:
            error_msg = "Access forbidden"
            if "duplicate" in str(e).lower():
                error_msg = "Duplicate tweet detected - please modify your content"
            elif "automated" in str(e).lower():
                error_msg = "Tweet appears automated - please make it more personal"
            return self._format_error_response(
                Exception(error_msg),
                {'content': content}
            )
        except tweepy.TooManyRequests:
            return self._format_error_response(
                Exception("Rate limit exceeded - please wait before posting again"),
                {'content': content}
            )
        except Exception as e:
            return self._format_error_response(e, {'content': content})
    
    async def get_content_status(self, content_id: str) -> Dict[str, Any]:
        """Get status of a tweet with real metrics."""
        try:
            tweet = self.client.get_status(
                content_id, 
                include_entities=True,
                tweet_mode='extended'
            )
            
            tweet_data = {
                'id': tweet.id_str,
                'text': tweet.full_text,
                'created_at': tweet.created_at.isoformat(),
                'metrics': {
                    'retweet_count': tweet.retweet_count,
                    'favorite_count': tweet.favorite_count,
                    'reply_count': getattr(tweet, 'reply_count', 0),
                    'quote_count': getattr(tweet, 'quote_count', 0)
                },
                'engagement': {
                    'engagement_rate': self._calculate_engagement_rate(tweet),
                    'total_engagement': tweet.retweet_count + tweet.favorite_count + getattr(tweet, 'reply_count', 0)
                },
                'user': {
                    'screen_name': tweet.user.screen_name,
                    'followers_count': tweet.user.followers_count
                }
            }
            
            return self._format_success_response(tweet_data)
            
        except tweepy.NotFound:
            return self._format_error_response(
                Exception("Tweet not found - it may have been deleted"),
                {'content_id': content_id}
            )
        except Exception as e:
            return self._format_error_response(e, {'content_id': content_id})
    
    async def get_analytics(
        self,
        content_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get comprehensive analytics for a tweet."""
        try:
            # Get tweet details
            tweet = self.client.get_status(
                content_id, 
                include_entities=True,
                tweet_mode='extended'
            )
            
            # Calculate engagement metrics
            total_engagement = (
                tweet.retweet_count + 
                tweet.favorite_count + 
                getattr(tweet, 'reply_count', 0) +
                getattr(tweet, 'quote_count', 0)
            )
            
            engagement_rate = self._calculate_engagement_rate(tweet)
            
            # Get time-based metrics (if tweet is recent)
            time_metrics = self._calculate_time_metrics(tweet)
            
            analytics_data = {
                'tweet_id': tweet.id_str,
                'metrics': {
                    'likes': tweet.favorite_count,
                    'retweets': tweet.retweet_count,
                    'replies': getattr(tweet, 'reply_count', 0),
                    'quotes': getattr(tweet, 'quote_count', 0),
                    'total_engagement': total_engagement,
                    'impressions': getattr(tweet, 'impression_count', 0)  # May not be available
                },
                'engagement': {
                    'engagement_rate': engagement_rate,
                    'likes_rate': (tweet.favorite_count / tweet.user.followers_count * 100) if tweet.user.followers_count > 0 else 0,
                    'retweets_rate': (tweet.retweet_count / tweet.user.followers_count * 100) if tweet.user.followers_count > 0 else 0
                },
                'timing': time_metrics,
                'audience': {
                    'followers_at_post': tweet.user.followers_count,
                    'reach_percentage': (total_engagement / tweet.user.followers_count * 100) if tweet.user.followers_count > 0 else 0
                },
                'content_analysis': {
                    'character_count': len(tweet.full_text),
                    'hashtag_count': len([entity for entity in tweet.entities.get('hashtags', [])]),
                    'mention_count': len([entity for entity in tweet.entities.get('user_mentions', [])]),
                    'url_count': len([entity for entity in tweet.entities.get('urls', [])])
                }
            }
            
            return self._format_success_response(analytics_data)
            
        except Exception as e:
            return self._format_error_response(e, {
                'content_id': content_id,
                'start_date': start_date,
                'end_date': end_date
            })
    
    async def validate_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced content validation."""
        try:
            errors = []
            warnings = []
            
            # Check text
            text = content.get('text', '')
            if not text.strip():
                errors.append("Tweet text cannot be empty")
            
            # Check length
            if len(text) > 280:
                errors.append(f"Tweet text exceeds 280 characters ({len(text)}/280)")
            elif len(text) > 270:
                warnings.append("Tweet is close to character limit")
            
            # Check for very short tweets
            if len(text) < 10:
                warnings.append("Very short tweets may get less engagement")
            
            # Check media
            media = content.get('media', [])
            if len(media) > 4:
                errors.append("Maximum 4 media attachments allowed")
            
            # Check for spam indicators
            if text.count('#') > 3:
                warnings.append("Too many hashtags may reduce engagement")
            
            if text.count('@') > 5:
                warnings.append("Too many mentions may appear spammy")
            
            # Check for duplicate content (basic check)
            if self._is_potential_duplicate(text):
                warnings.append("Content may be similar to recent tweets")
            
            if errors:
                return self._format_error_response(
                    ValueError(f"Validation failed: {'; '.join(errors)}"),
                    {'content': content, 'warnings': warnings}
                )
            
            validation_data = {
                'valid': True,
                'content': content,
                'warnings': warnings,
                'suggestions': self._get_content_suggestions(text)
            }
            
            return self._format_success_response(validation_data)
            
        except Exception as e:
            return self._format_error_response(e, {'content': content})
    
    def _calculate_engagement_rate(self, tweet: Status) -> float:
        """Calculate engagement rate for a tweet."""
        try:
            total_engagement = (
                tweet.favorite_count +
                tweet.retweet_count +
                getattr(tweet, 'reply_count', 0) +
                getattr(tweet, 'quote_count', 0)
            )
            followers = tweet.user.followers_count
            return (total_engagement / followers * 100) if followers > 0 else 0.0
        except Exception:
            return 0.0
    
    def _calculate_time_metrics(self, tweet: Status) -> Dict[str, Any]:
        """Calculate time-based metrics for a tweet."""
        try:
            now = datetime.now()
            tweet_time = tweet.created_at.replace(tzinfo=None)
            age_hours = (now - tweet_time).total_seconds() / 3600
            
            # Calculate engagement velocity (engagement per hour)
            total_engagement = (
                tweet.favorite_count + 
                tweet.retweet_count + 
                getattr(tweet, 'reply_count', 0)
            )
            
            engagement_velocity = total_engagement / max(age_hours, 1)
            
            return {
                'age_hours': round(age_hours, 2),
                'engagement_velocity': round(engagement_velocity, 2),
                'peak_engagement_period': self._estimate_peak_period(tweet_time),
                'posted_at': tweet_time.isoformat()
            }
        except Exception:
            return {}
    
    def _estimate_peak_period(self, tweet_time: datetime) -> str:
        """Estimate if tweet was posted during peak engagement period."""
        hour = tweet_time.hour
        
        if 9 <= hour <= 10:
            return "Morning Peak (9-10 AM)"
        elif 12 <= hour <= 13:
            return "Lunch Peak (12-1 PM)"
        elif 19 <= hour <= 21:
            return "Evening Peak (7-9 PM)"
        else:
            return "Off-Peak Hours"
    
    def _check_rate_limit(self, endpoint: str) -> bool:
        """Check if we're within rate limits for an endpoint."""
        try:
            rate_limits = self.client.get_rate_limit_status()
            
            endpoint_map = {
                'tweets': '/statuses/update',
                'user_timeline': '/statuses/user_timeline',
                'verify_credentials': '/account/verify_credentials'
            }
            
            if endpoint in endpoint_map:
                limit_info = rate_limits['resources']['statuses'].get(endpoint_map[endpoint])
                if limit_info:
                    return limit_info['remaining'] > 0
            
            return True  # Default to allowing if we can't check
            
        except Exception:
            return True  # Default to allowing if check fails
    
    def _update_rate_limit_tracker(self, endpoint: str) -> None:
        """Update internal rate limit tracker."""
        now = time.time()
        if endpoint not in self.rate_limit_tracker:
            self.rate_limit_tracker[endpoint] = []
        
        # Add current request
        self.rate_limit_tracker[endpoint].append(now)
        
        # Clean old requests (older than 15 minutes)
        self.rate_limit_tracker[endpoint] = [
            timestamp for timestamp in self.rate_limit_tracker[endpoint]
            if now - timestamp < 900  # 15 minutes
        ]
    
    def _is_potential_duplicate(self, text: str) -> bool:
        """Basic check for potential duplicate content."""
        # This is a simplified check - in production, you'd want more sophisticated detection
        try:
            # Get recent tweets from user
            recent_tweets = self.client.user_timeline(count=20, tweet_mode='extended')
            
            for tweet in recent_tweets:
                # Simple similarity check
                if self._calculate_text_similarity(text, tweet.full_text) > 0.8:
                    return True
            
            return False
        except Exception:
            return False  # If we can't check, assume it's not a duplicate
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity."""
        # Simple word-based similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _get_content_suggestions(self, text: str) -> List[str]:
        """Get suggestions for improving tweet content."""
        suggestions = []
        
        if len(text) < 50:
            suggestions.append("Consider adding more context to increase engagement")
        
        if not any(char in text for char in '!?'):
            suggestions.append("Adding punctuation can make tweets more engaging")
        
        if '#' not in text:
            suggestions.append("Consider adding 1-2 relevant hashtags")
        
        if not any(emoji_char in text for emoji_char in '😀😃😄😁😆😅😂🤣'):
            suggestions.append("Emojis can increase engagement and visual appeal")
        
        return suggestions
    
    async def delete_content(
        self,
        content_id: str
    ) -> Dict[str, Any]:
        """Delete a tweet."""
        try:
            self.client.destroy_status(content_id)
            return self._format_success_response({
                'id': content_id,
                'deleted': True
            })
        except Exception as e:
            return self._format_error_response(
                e,
                {'content_id': content_id}
            )
    
    async def update_content(
        self,
        content_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a tweet."""
        try:
            # Twitter doesn't support updating tweets
            # We'll delete the old one and create a new one
            await self.delete_content(content_id)
            return await self.publish_content(updates)
        except Exception as e:
            return self._format_error_response(
                e,
                {
                    'content_id': content_id,
                    'updates': updates
                }
            )
    
    async def get_optimal_publish_time(
        self,
        content_type: str,
        target_audience: Optional[Dict[str, Any]] = None
    ) -> datetime:
        """Get optimal publish time for content."""
        # Implement optimal time calculation based on:
        # - Content type
        # - Target audience timezone
        # - Historical engagement data
        # For now, return current time
        return datetime.now()
    
    async def get_platform_limits(
        self
    ) -> Dict[str, Any]:
        """Get Twitter platform limits."""
        return self._format_success_response({
            'tweet_length': 280,
            'media_attachments': 4,
            'poll_options': 4,
            'poll_duration': 10080,  # 7 days in minutes
            'rate_limits': {
                'tweets_per_day': 2000,
                'tweets_per_hour': 100
            }
        })
    
    async def get_supported_content_types(
        self
    ) -> List[str]:
        """Get list of supported content types."""
        return ['TWEET', 'THREAD', 'POLL']
    
    async def get_platform_metrics(
        self
    ) -> Dict[str, Any]:
        """Get Twitter platform metrics."""
        try:
            account = self.client.verify_credentials()
            return self._format_success_response({
                'followers_count': account.followers_count,
                'following_count': account.friends_count,
                'tweets_count': account.statuses_count,
                'account_created_at': account.created_at.isoformat()
            })
        except Exception as e:
            return self._format_error_response(e)
    
    def _upload_media(self, media: Dict[str, Any]) -> Optional[str]:
        """Upload media to Twitter."""
        try:
            if 'url' in media:
                # Download media from URL
                response = requests.get(media['url'])
                media_file = BytesIO(response.content)
            elif 'file' in media:
                # Use local file
                media_file = open(media['file'], 'rb')
            else:
                return None
            
            # Upload media
            media_upload = self.client.media_upload(
                filename=media.get('filename', 'media'),
                file=media_file
            )
            return media_upload.media_id_string
            
        except Exception as e:
            logger.error(f"Failed to upload media: {str(e)}")
            return None
    
    @classmethod
    def get_required_config_fields(cls) -> List[str]:
        """Get list of required configuration fields."""
        return [
            'api_key',
            'api_secret',
            'access_token',
            'access_token_secret'
        ]
    
    @classmethod
    def get_platform_description(cls) -> str:
        """Get platform description."""
        return "Twitter platform adapter for posting and managing tweets"
    
    @classmethod
    def get_platform_version(cls) -> str:
        """Get platform adapter version."""
        return "1.0.0" 