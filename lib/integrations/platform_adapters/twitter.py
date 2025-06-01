"""
Twitter platform adapter implementation.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import tweepy
from tweepy.models import Status

from .base import PlatformAdapter

class TwitterAdapter(PlatformAdapter):
    """Twitter platform adapter."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Twitter adapter with configuration."""
        super().__init__(config)
        self._validate_config()
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize Twitter API client."""
        try:
            auth = tweepy.OAuthHandler(
                self.config['api_key'],
                self.config['api_secret']
            )
            auth.set_access_token(
                self.config['access_token'],
                self.config['access_token_secret']
            )
            self.client = tweepy.API(auth)
            self.client.verify_credentials()
        except Exception as e:
            raise Exception(
                f"Failed to initialize Twitter client: {str(e)}"
            )
    
    async def publish_content(
        self,
        content: Dict[str, Any],
        schedule_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Publish content to Twitter."""
        try:
            # Validate content
            validation = await self.validate_content(content)
            if not validation.get('success'):
                return validation
            
            # Prepare tweet content
            tweet_text = content.get('text', '')
            media_ids = []
            
            # Handle media attachments if present
            if 'media' in content:
                for media in content['media']:
                    media_id = self._upload_media(media)
                    if media_id:
                        media_ids.append(media_id)
            
            # Create tweet
            tweet = self.client.update_status(
                status=tweet_text,
                media_ids=media_ids if media_ids else None
            )
            
            return self._format_success_response({
                'id': tweet.id_str,
                'text': tweet.text,
                'created_at': tweet.created_at.isoformat()
            })
            
        except Exception as e:
            return self._format_error_response(
                e,
                {'content': content, 'schedule_time': schedule_time}
            )
    
    async def get_content_status(
        self,
        content_id: str
    ) -> Dict[str, Any]:
        """Get status of a tweet."""
        try:
            tweet = self.client.get_status(content_id)
            return self._format_success_response({
                'id': tweet.id_str,
                'text': tweet.text,
                'created_at': tweet.created_at.isoformat(),
                'favorite_count': tweet.favorite_count,
                'retweet_count': tweet.retweet_count
            })
        except Exception as e:
            return self._format_error_response(
                e,
                {'content_id': content_id}
            )
    
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
    
    async def get_analytics(
        self,
        content_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get analytics for a tweet."""
        try:
            tweet = self.client.get_status(content_id)
            return self._format_success_response({
                'id': tweet.id_str,
                'metrics': {
                    'favorites': tweet.favorite_count,
                    'retweets': tweet.retweet_count,
                    'replies': tweet.reply_count if hasattr(tweet, 'reply_count') else 0,
                    'impressions': tweet.impression_count if hasattr(tweet, 'impression_count') else 0
                },
                'engagement_rate': self._calculate_engagement_rate(tweet)
            })
        except Exception as e:
            return self._format_error_response(
                e,
                {
                    'content_id': content_id,
                    'start_date': start_date,
                    'end_date': end_date
                }
            )
    
    async def validate_content(
        self,
        content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate content before publishing."""
        try:
            # Check text length
            text = content.get('text', '')
            if len(text) > 280:
                return self._format_error_response(
                    ValueError("Tweet text exceeds 280 characters"),
                    {'content': content}
                )
            
            # Check media attachments
            media = content.get('media', [])
            if len(media) > 4:
                return self._format_error_response(
                    ValueError("Maximum 4 media attachments allowed"),
                    {'content': content}
                )
            
            return self._format_success_response({
                'valid': True,
                'content': content
            })
            
        except Exception as e:
            return self._format_error_response(
                e,
                {'content': content}
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
    
    def _calculate_engagement_rate(self, tweet: Status) -> float:
        """Calculate engagement rate for a tweet."""
        try:
            total_engagement = (
                tweet.favorite_count +
                tweet.retweet_count +
                (tweet.reply_count if hasattr(tweet, 'reply_count') else 0)
            )
            followers = tweet.user.followers_count
            return (total_engagement / followers * 100) if followers > 0 else 0.0
        except Exception:
            return 0.0
    
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