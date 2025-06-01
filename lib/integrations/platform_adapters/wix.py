"""
Wix platform adapter implementation.
"""

from io import BytesIO
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
from pathlib import Path

import requests

from .base import PlatformAdapter
from lib.integrations.wix.wix_api_client import WixAPIClient

logger = logging.getLogger(__name__)

class WixAdapter(PlatformAdapter):
    """Wix platform adapter."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Wix adapter with configuration."""
        super().__init__(config)
        self._validate_config()
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize Wix API client."""
        try:
            self.client = WixAPIClient(
                api_key=self.config.get('api_key'),
                refresh_token=self.config.get('refresh_token'),
                site_id=self.config.get('site_id')
            )
            logger.info("Successfully initialized Wix API client")
        except Exception as e:
            raise Exception(f"Failed to initialize Wix client: {str(e)}")
    
    async def publish_content(
        self,
        content: Dict[str, Any],
        schedule_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Publish content to Wix blog."""
        try:
            # Validate content
            validation = await self.validate_content(content)
            if not validation.get('success'):
                return validation
            
            # Prepare blog post data
            post_data = {
                'title': content.get('title', ''),
                'content': content.get('content', ''),
                'excerpt': content.get('excerpt', ''),
                'slug': content.get('slug', ''),
                'tags': content.get('tags', []),
                'categories': content.get('categories', []),
                'seo': content.get('seo', {}),
                'publish_date': schedule_time.isoformat() if schedule_time else None
            }
            
            # Handle media attachments
            media_ids = []
            if 'media' in content:
                for media in content['media']:
                    media_id = await self._upload_media(media)
                    if media_id:
                        media_ids.append(media_id)
            
            # Create blog post
            post = self.client.create_post(post_data)
            
            # Add media to post if any
            if media_ids:
                self.client.add_media_to_post(post['id'], media_ids)
            
            return self._format_success_response({
                'id': post['id'],
                'title': post['title'],
                'url': post['url'],
                'created_at': post['created_at']
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
        """Get status of a blog post."""
        try:
            post = self.client.get_post(content_id)
            return self._format_success_response({
                'id': post['id'],
                'title': post['title'],
                'status': post['status'],
                'url': post['url'],
                'created_at': post['created_at'],
                'updated_at': post['updated_at'],
                'published_at': post.get('published_at')
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
        """Delete a blog post."""
        try:
            self.client.delete_post(content_id)
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
        """Update a blog post."""
        try:
            post = self.client.update_post(content_id, updates)
            return self._format_success_response({
                'id': post['id'],
                'title': post['title'],
                'url': post['url'],
                'updated_at': post['updated_at']
            })
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
        """Get analytics for a blog post."""
        try:
            analytics = self.client.get_post_analytics(
                content_id,
                start_date,
                end_date
            )
            return self._format_success_response({
                'id': content_id,
                'metrics': {
                    'views': analytics.get('views', 0),
                    'unique_visitors': analytics.get('unique_visitors', 0),
                    'average_time_on_page': analytics.get('average_time_on_page', 0),
                    'bounce_rate': analytics.get('bounce_rate', 0)
                }
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
            # Check required fields
            required_fields = ['title', 'content']
            missing_fields = [
                field for field in required_fields
                if field not in content
            ]
            
            if missing_fields:
                return self._format_error_response(
                    ValueError(f"Missing required fields: {', '.join(missing_fields)}"),
                    {'content': content}
                )
            
            # Check content length
            if len(content['content']) > 100000:  # Wix limit
                return self._format_error_response(
                    ValueError("Content exceeds maximum length of 100,000 characters"),
                    {'content': content}
                )
            
            # Check media attachments
            media = content.get('media', [])
            if len(media) > 20:  # Wix limit
                return self._format_error_response(
                    ValueError("Maximum 20 media attachments allowed"),
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
        """Get Wix platform limits."""
        return self._format_success_response({
            'content_length': 100000,
            'media_attachments': 20,
            'tags_per_post': 50,
            'categories_per_post': 10,
            'rate_limits': {
                'posts_per_day': 100,
                'media_uploads_per_day': 1000
            }
        })
    
    async def get_supported_content_types(
        self
    ) -> List[str]:
        """Get list of supported content types."""
        return ['BLOG_POST', 'PAGE', 'COLLECTION_ITEM']
    
    async def get_platform_metrics(
        self
    ) -> Dict[str, Any]:
        """Get Wix platform metrics."""
        try:
            site_stats = self.client.get_site_statistics()
            return self._format_success_response({
                'total_posts': site_stats.get('total_posts', 0),
                'total_views': site_stats.get('total_views', 0),
                'total_comments': site_stats.get('total_comments', 0),
                'average_engagement': site_stats.get('average_engagement', 0)
            })
        except Exception as e:
            return self._format_error_response(e)
    
    async def _upload_media(
        self,
        media: Dict[str, Any]
    ) -> Optional[str]:
        """Upload media to Wix."""
        try:
            if 'url' in media:
                # Download media from URL
                response = requests.get(media['url'])
                media_file = BytesIO(response.content)
                filename = media.get('filename', 'media')
            elif 'file' in media:
                # Use local file
                file_path = Path(media['file'])
                media_file = open(file_path, 'rb')
                filename = file_path.name
            else:
                return None
            
            # Upload media
            media_id = self.client.upload_media(
                file=media_file,
                filename=filename,
                mime_type=media.get('mime_type')
            )
            return media_id
            
        except Exception as e:
            logger.error(f"Failed to upload media: {str(e)}")
            return None
    
    @classmethod
    def get_required_config_fields(cls) -> List[str]:
        """Get list of required configuration fields."""
        return [
            'api_key',
            'refresh_token',
            'site_id'
        ]
    
    @classmethod
    def get_platform_description(cls) -> str:
        """Get platform description."""
        return "Wix platform adapter for managing blog posts and content"
    
    @classmethod
    def get_platform_version(cls) -> str:
        """Get platform adapter version."""
        return "1.0.0" 