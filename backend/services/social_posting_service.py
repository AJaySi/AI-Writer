"""
Social Media Posting Service
Handles posting content to connected social media platforms.
"""

import os
import httpx
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from sqlalchemy.orm import Session
from models.social_connections import SocialConnection, SocialPost
from services.oauth_service import oauth_service

class SocialPostingService:
    def __init__(self):
        self.supported_platforms = {
            'facebook': self._post_to_facebook,
            'twitter': self._post_to_twitter,
            'linkedin': self._post_to_linkedin,
            'youtube': self._post_to_youtube
        }

    async def post_content(
        self,
        connection_id: int,
        content: str,
        media_urls: List[str] = None,
        scheduled_at: datetime = None,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Post content to a connected social media platform.
        
        Args:
            connection_id: ID of the social media connection
            content: Text content to post
            media_urls: Optional list of media URLs to include
            scheduled_at: Optional scheduled posting time
            db: Database session
        
        Returns:
            Dictionary with posting result and metadata
        """
        try:
            # Get the connection
            connection = db.query(SocialConnection).filter(
                SocialConnection.id == connection_id,
                SocialConnection.connection_status == 'active'
            ).first()
            
            if not connection:
                raise ValueError("Active connection not found")
            
            if not connection.auto_post_enabled:
                raise ValueError("Auto-posting is disabled for this connection")
            
            # Get valid access token
            access_token = oauth_service.get_valid_token(connection, db)
            if not access_token:
                raise ValueError("No valid access token available")
            
            # Create social post record
            social_post = SocialPost(
                connection_id=connection_id,
                content=content,
                media_urls=media_urls,
                scheduled_at=scheduled_at,
                status='pending'
            )
            db.add(social_post)
            db.commit()
            db.refresh(social_post)
            
            # Check if platform is supported
            if connection.platform not in self.supported_platforms:
                social_post.status = 'failed'
                social_post.error_message = f"Platform {connection.platform} not supported for posting"
                db.commit()
                raise ValueError(f"Platform {connection.platform} not supported for posting")
            
            # Post immediately or schedule
            if scheduled_at and scheduled_at > datetime.utcnow():
                # For now, just mark as scheduled (in production, use a job queue)
                social_post.status = 'scheduled'
                db.commit()
                return {
                    'success': True,
                    'message': 'Content scheduled successfully',
                    'post_id': social_post.id,
                    'scheduled_at': scheduled_at.isoformat()
                }
            else:
                # Post immediately
                result = await self.supported_platforms[connection.platform](
                    access_token, content, media_urls, connection
                )
                
                # Update post record
                social_post.status = 'posted' if result['success'] else 'failed'
                social_post.platform_post_id = result.get('platform_post_id')
                social_post.platform_url = result.get('platform_url')
                social_post.error_message = result.get('error_message')
                social_post.posted_at = datetime.utcnow() if result['success'] else None
                db.commit()
                
                return {
                    'success': result['success'],
                    'message': result.get('message', 'Content posted successfully' if result['success'] else 'Failed to post content'),
                    'post_id': social_post.id,
                    'platform_post_id': result.get('platform_post_id'),
                    'platform_url': result.get('platform_url'),
                    'error_message': result.get('error_message')
                }
                
        except Exception as e:
            # Update post record if it exists
            if 'social_post' in locals():
                social_post.status = 'failed'
                social_post.error_message = str(e)
                db.commit()
            
            return {
                'success': False,
                'message': str(e),
                'error_message': str(e)
            }

    async def _post_to_facebook(
        self,
        access_token: str,
        content: str,
        media_urls: List[str],
        connection: SocialConnection
    ) -> Dict[str, Any]:
        """Post content to Facebook."""
        try:
            async with httpx.AsyncClient() as client:
                # Get user's pages
                pages_response = await client.get(
                    'https://graph.facebook.com/v18.0/me/accounts',
                    params={'access_token': access_token}
                )
                pages_data = pages_response.json()
                
                if not pages_data.get('data'):
                    return {
                        'success': False,
                        'error_message': 'No Facebook pages found'
                    }
                
                # Use the first page
                page = pages_data['data'][0]
                page_access_token = page['access_token']
                page_id = page['id']
                
                # Prepare post data
                post_data = {
                    'message': content,
                    'access_token': page_access_token
                }
                
                # Post to page
                response = await client.post(
                    f'https://graph.facebook.com/v18.0/{page_id}/feed',
                    data=post_data
                )
                result = response.json()
                
                if 'id' in result:
                    return {
                        'success': True,
                        'platform_post_id': result['id'],
                        'platform_url': f"https://facebook.com/{result['id']}"
                    }
                else:
                    return {
                        'success': False,
                        'error_message': result.get('error', {}).get('message', 'Unknown Facebook error')
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'error_message': f"Facebook posting error: {str(e)}"
            }

    async def _post_to_twitter(
        self,
        access_token: str,
        content: str,
        media_urls: List[str],
        connection: SocialConnection
    ) -> Dict[str, Any]:
        """Post content to Twitter."""
        try:
            async with httpx.AsyncClient() as client:
                # Prepare tweet data
                tweet_data = {
                    'text': content[:280]  # Twitter character limit
                }
                
                # Post tweet
                response = await client.post(
                    'https://api.twitter.com/2/tweets',
                    headers={
                        'Authorization': f'Bearer {access_token}',
                        'Content-Type': 'application/json'
                    },
                    json=tweet_data
                )
                result = response.json()
                
                if 'data' in result:
                    tweet_id = result['data']['id']
                    username = connection.platform_username
                    return {
                        'success': True,
                        'platform_post_id': tweet_id,
                        'platform_url': f"https://twitter.com/{username}/status/{tweet_id}"
                    }
                else:
                    return {
                        'success': False,
                        'error_message': result.get('detail', 'Unknown Twitter error')
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'error_message': f"Twitter posting error: {str(e)}"
            }

    async def _post_to_linkedin(
        self,
        access_token: str,
        content: str,
        media_urls: List[str],
        connection: SocialConnection
    ) -> Dict[str, Any]:
        """Post content to LinkedIn."""
        try:
            async with httpx.AsyncClient() as client:
                # Get user profile
                profile_response = await client.get(
                    'https://api.linkedin.com/v2/people/(id~)',
                    headers={'Authorization': f'Bearer {access_token}'}
                )
                profile_data = profile_response.json()
                person_urn = f"urn:li:person:{profile_data['id']}"
                
                # Prepare post data
                post_data = {
                    'author': person_urn,
                    'lifecycleState': 'PUBLISHED',
                    'specificContent': {
                        'com.linkedin.ugc.ShareContent': {
                            'shareCommentary': {
                                'text': content
                            },
                            'shareMediaCategory': 'NONE'
                        }
                    },
                    'visibility': {
                        'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
                    }
                }
                
                # Post to LinkedIn
                response = await client.post(
                    'https://api.linkedin.com/v2/ugcPosts',
                    headers={
                        'Authorization': f'Bearer {access_token}',
                        'Content-Type': 'application/json',
                        'X-Restli-Protocol-Version': '2.0.0'
                    },
                    json=post_data
                )
                
                if response.status_code == 201:
                    # LinkedIn returns the post URN in the Location header
                    location = response.headers.get('Location', '')
                    post_id = location.split('/')[-1] if location else None
                    
                    return {
                        'success': True,
                        'platform_post_id': post_id,
                        'platform_url': f"https://linkedin.com/feed/update/{post_id}" if post_id else None
                    }
                else:
                    result = response.json()
                    return {
                        'success': False,
                        'error_message': result.get('message', 'Unknown LinkedIn error')
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'error_message': f"LinkedIn posting error: {str(e)}"
            }

    async def _post_to_youtube(
        self,
        access_token: str,
        content: str,
        media_urls: List[str],
        connection: SocialConnection
    ) -> Dict[str, Any]:
        """Post content to YouTube (community post)."""
        try:
            # YouTube community posts require special handling
            # For now, we'll return a not implemented message
            return {
                'success': False,
                'error_message': 'YouTube community posting not yet implemented'
            }
                    
        except Exception as e:
            return {
                'success': False,
                'error_message': f"YouTube posting error: {str(e)}"
            }

    def get_post_analytics(
        self,
        post_id: int,
        db: Session
    ) -> Optional[Dict[str, Any]]:
        """Get analytics for a posted content."""
        try:
            post = db.query(SocialPost).filter(SocialPost.id == post_id).first()
            if not post:
                return None
            
            return {
                'post_id': post.id,
                'platform': post.connection.platform,
                'content': post.content,
                'status': post.status,
                'posted_at': post.posted_at.isoformat() if post.posted_at else None,
                'analytics_data': post.analytics_data,
                'platform_url': post.platform_url
            }
            
        except Exception as e:
            return None

    def get_user_posts(
        self,
        user_id: int,
        platform: str = None,
        limit: int = 50,
        db: Session = None
    ) -> List[Dict[str, Any]]:
        """Get posts for a user across all connected platforms."""
        try:
            query = db.query(SocialPost).join(SocialConnection).filter(
                SocialConnection.user_id == user_id
            )
            
            if platform:
                query = query.filter(SocialConnection.platform == platform)
            
            posts = query.order_by(SocialPost.created_at.desc()).limit(limit).all()
            
            return [
                {
                    'id': post.id,
                    'platform': post.connection.platform,
                    'content': post.content,
                    'status': post.status,
                    'posted_at': post.posted_at.isoformat() if post.posted_at else None,
                    'platform_url': post.platform_url,
                    'analytics_data': post.analytics_data
                }
                for post in posts
            ]
            
        except Exception as e:
            return []

# Global instance
social_posting_service = SocialPostingService()