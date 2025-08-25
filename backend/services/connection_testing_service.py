"""
Connection Testing Service
Comprehensive testing and validation for social media connections.
Provides detailed feedback and debugging information.
"""

import os
import httpx
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import json
import logging

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from sqlalchemy.orm import Session
from models.social_connections import SocialConnection
from services.oauth_service import oauth_service

# Setup detailed logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionTestingService:
    def __init__(self):
        self.test_functions = {
            'google_search_console': self._test_gsc_connection,
            'youtube': self._test_youtube_connection,
            'facebook': self._test_facebook_connection,
            'instagram': self._test_instagram_connection,
            'twitter': self._test_twitter_connection,
            'linkedin': self._test_linkedin_connection,
            'tiktok': self._test_tiktok_connection,
            'pinterest': self._test_pinterest_connection,
            'snapchat': self._test_snapchat_connection,
            'reddit': self._test_reddit_connection,
            'discord': self._test_discord_connection
        }

    async def test_connection(
        self,
        connection: SocialConnection,
        db: Session,
        comprehensive: bool = True
    ) -> Dict[str, Any]:
        """
        Test a social media connection comprehensively.
        
        Args:
            connection: SocialConnection instance
            db: Database session
            comprehensive: Whether to run comprehensive tests
            
        Returns:
            Detailed test results with debugging information
        """
        test_start_time = datetime.utcnow()
        
        logger.info(f"Starting connection test for {connection.platform} (ID: {connection.id})")
        
        result = {
            'connection_id': connection.id,
            'platform': connection.platform,
            'test_timestamp': test_start_time.isoformat(),
            'status': 'testing',
            'tests_performed': [],
            'errors': [],
            'warnings': [],
            'debug_info': {},
            'recommendations': [],
            'platform_specific_data': {},
            'performance_metrics': {}
        }
        
        try:
            # Basic connection validation
            basic_test = await self._test_basic_connection(connection, db)
            result['tests_performed'].append('basic_connection')
            result['debug_info']['basic_test'] = basic_test
            
            if not basic_test['success']:
                result['status'] = 'failed'
                result['errors'].extend(basic_test['errors'])
                return result
            
            # Platform-specific tests
            if connection.platform in self.test_functions:
                platform_test = await self.test_functions[connection.platform](connection, db, comprehensive)
                result['tests_performed'].append(f'{connection.platform}_specific')
                result['platform_specific_data'] = platform_test.get('data', {})
                result['debug_info']['platform_test'] = platform_test
                
                if not platform_test['success']:
                    result['errors'].extend(platform_test.get('errors', []))
                    result['warnings'].extend(platform_test.get('warnings', []))
                    result['status'] = 'failed'
                else:
                    result['warnings'].extend(platform_test.get('warnings', []))
                    result['status'] = 'passed'
            else:
                result['warnings'].append(f"No specific tests available for {connection.platform}")
                result['status'] = 'passed'
            
            # Permission validation
            if comprehensive:
                permission_test = await self._test_permissions(connection, db)
                result['tests_performed'].append('permissions')
                result['debug_info']['permission_test'] = permission_test
                
                if permission_test['missing_permissions']:
                    result['warnings'].append(f"Missing permissions: {', '.join(permission_test['missing_permissions'])}")
            
            # Generate recommendations
            result['recommendations'] = self._generate_recommendations(result, connection)
            
            # Update connection status in database
            await self._update_connection_status(connection, result, db)
            
        except Exception as e:
            logger.error(f"Connection test failed for {connection.platform}: {str(e)}")
            result['status'] = 'error'
            result['errors'].append(f"Test execution failed: {str(e)}")
            result['debug_info']['exception'] = str(e)
        
        # Calculate test duration
        test_end_time = datetime.utcnow()
        result['performance_metrics']['test_duration_seconds'] = (test_end_time - test_start_time).total_seconds()
        
        logger.info(f"Connection test completed for {connection.platform}. Status: {result['status']}")
        
        return result

    async def _test_basic_connection(self, connection: SocialConnection, db: Session) -> Dict[str, Any]:
        """Test basic connection validity."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'data': {}
        }
        
        try:
            # Check if connection exists and is active
            if connection.connection_status != 'active':
                result['errors'].append(f"Connection status is {connection.connection_status}, expected 'active'")
                return result
            
            # Check token validity
            access_token = oauth_service.get_valid_token(connection, db)
            if not access_token:
                result['errors'].append("Unable to obtain valid access token")
                return result
            
            result['data']['token_length'] = len(access_token)
            result['data']['has_refresh_token'] = bool(connection.refresh_token)
            result['data']['expires_at'] = connection.expires_at.isoformat() if connection.expires_at else None
            
            # Check token expiration
            if connection.is_token_expired():
                result['warnings'].append("Token is expired but may be refreshable")
            
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(f"Basic connection test failed: {str(e)}")
        
        return result

    async def _test_gsc_connection(self, connection: SocialConnection, db: Session, comprehensive: bool) -> Dict[str, Any]:
        """Test Google Search Console connection."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'data': {}
        }
        
        try:
            access_token = oauth_service.get_valid_token(connection, db)
            if not access_token:
                result['errors'].append("No valid access token available")
                return result
            
            # Create GSC service
            credentials = Credentials(
                token=access_token,
                refresh_token=oauth_service.decrypt_token(connection.refresh_token) if connection.refresh_token else None,
                token_uri='https://oauth2.googleapis.com/token',
                client_id=os.getenv('GOOGLE_CLIENT_ID'),
                client_secret=os.getenv('GOOGLE_CLIENT_SECRET')
            )
            
            service = build('searchconsole', 'v1', credentials=credentials)
            
            # Test 1: List sites
            sites_response = service.sites().list().execute()
            sites = sites_response.get('siteEntry', [])
            result['data']['sites_count'] = len(sites)
            result['data']['sites'] = sites
            
            if not sites:
                result['warnings'].append("No verified sites found in Search Console")
            
            # Test 2: If comprehensive, test data retrieval from first site
            if comprehensive and sites:
                test_site = sites[0]['siteUrl']
                try:
                    # Test search analytics query
                    analytics_request = {
                        'startDate': '2024-01-01',
                        'endDate': '2024-01-07',
                        'dimensions': ['query'],
                        'rowLimit': 5
                    }
                    
                    analytics_response = service.searchanalytics().query(
                        siteUrl=test_site,
                        body=analytics_request
                    ).execute()
                    
                    result['data']['sample_analytics'] = {
                        'site': test_site,
                        'rows_count': len(analytics_response.get('rows', [])),
                        'has_data': len(analytics_response.get('rows', [])) > 0
                    }
                    
                except HttpError as e:
                    result['warnings'].append(f"Could not fetch analytics for {test_site}: {e}")
            
            result['success'] = True
            
        except HttpError as e:
            result['errors'].append(f"Google API error: {e}")
        except Exception as e:
            result['errors'].append(f"GSC test failed: {str(e)}")
        
        return result

    async def _test_youtube_connection(self, connection: SocialConnection, db: Session, comprehensive: bool) -> Dict[str, Any]:
        """Test YouTube connection."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'data': {}
        }
        
        try:
            access_token = oauth_service.get_valid_token(connection, db)
            if not access_token:
                result['errors'].append("No valid access token available")
                return result
            
            credentials = Credentials(
                token=access_token,
                refresh_token=oauth_service.decrypt_token(connection.refresh_token) if connection.refresh_token else None,
                token_uri='https://oauth2.googleapis.com/token',
                client_id=os.getenv('GOOGLE_CLIENT_ID'),
                client_secret=os.getenv('GOOGLE_CLIENT_SECRET')
            )
            
            service = build('youtube', 'v3', credentials=credentials)
            
            # Test: Get channel information
            channels_response = service.channels().list(part='snippet,statistics', mine=True).execute()
            channels = channels_response.get('items', [])
            
            if not channels:
                result['errors'].append("No YouTube channel found for this account")
                return result
            
            channel = channels[0]
            result['data']['channel_info'] = {
                'id': channel['id'],
                'title': channel['snippet']['title'],
                'subscriber_count': channel['statistics'].get('subscriberCount', 'Hidden'),
                'video_count': channel['statistics'].get('videoCount', '0'),
                'view_count': channel['statistics'].get('viewCount', '0')
            }
            
            if comprehensive:
                # Test: List recent videos
                try:
                    videos_response = service.search().list(
                        part='snippet',
                        channelId=channel['id'],
                        type='video',
                        order='date',
                        maxResults=5
                    ).execute()
                    
                    result['data']['recent_videos_count'] = len(videos_response.get('items', []))
                    
                except HttpError as e:
                    result['warnings'].append(f"Could not fetch recent videos: {e}")
            
            result['success'] = True
            
        except HttpError as e:
            result['errors'].append(f"YouTube API error: {e}")
        except Exception as e:
            result['errors'].append(f"YouTube test failed: {str(e)}")
        
        return result

    async def _test_facebook_connection(self, connection: SocialConnection, db: Session, comprehensive: bool) -> Dict[str, Any]:
        """Test Facebook connection."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'data': {}
        }
        
        try:
            access_token = oauth_service.get_valid_token(connection, db)
            if not access_token:
                result['errors'].append("No valid access token available")
                return result
            
            async with httpx.AsyncClient() as client:
                # Test: Get user profile
                profile_response = await client.get(
                    'https://graph.facebook.com/v18.0/me',
                    params={
                        'access_token': access_token,
                        'fields': 'id,name,email'
                    }
                )
                
                if profile_response.status_code != 200:
                    result['errors'].append(f"Facebook API error: {profile_response.status_code}")
                    return result
                
                profile_data = profile_response.json()
                result['data']['user_info'] = profile_data
                
                # Test: Get managed pages
                pages_response = await client.get(
                    'https://graph.facebook.com/v18.0/me/accounts',
                    params={'access_token': access_token}
                )
                
                if pages_response.status_code == 200:
                    pages_data = pages_response.json()
                    result['data']['pages_count'] = len(pages_data.get('data', []))
                    result['data']['pages'] = pages_data.get('data', [])
                    
                    if not pages_data.get('data'):
                        result['warnings'].append("No Facebook pages found for this account")
                else:
                    result['warnings'].append("Could not fetch Facebook pages")
                
                if comprehensive and pages_data.get('data'):
                    # Test posting capability on first page
                    test_page = pages_data['data'][0]
                    permissions_response = await client.get(
                        f"https://graph.facebook.com/v18.0/{test_page['id']}/roles",
                        params={'access_token': test_page['access_token']}
                    )
                    
                    result['data']['page_permissions_accessible'] = permissions_response.status_code == 200
            
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(f"Facebook test failed: {str(e)}")
        
        return result

    async def _test_instagram_connection(self, connection: SocialConnection, db: Session, comprehensive: bool) -> Dict[str, Any]:
        """Test Instagram connection."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'data': {}
        }
        
        try:
            access_token = oauth_service.get_valid_token(connection, db)
            if not access_token:
                result['errors'].append("No valid access token available")
                return result
            
            async with httpx.AsyncClient() as client:
                # Get Facebook pages first (Instagram requires Facebook page)
                pages_response = await client.get(
                    'https://graph.facebook.com/v18.0/me/accounts',
                    params={'access_token': access_token}
                )
                
                if pages_response.status_code != 200:
                    result['errors'].append("Could not access Facebook pages (required for Instagram)")
                    return result
                
                pages_data = pages_response.json()
                instagram_accounts = []
                
                # Check each page for Instagram business account
                for page in pages_data.get('data', []):
                    instagram_response = await client.get(
                        f"https://graph.facebook.com/v18.0/{page['id']}?fields=instagram_business_account",
                        params={'access_token': page['access_token']}
                    )
                    
                    if instagram_response.status_code == 200:
                        instagram_data = instagram_response.json()
                        if 'instagram_business_account' in instagram_data:
                            instagram_accounts.append({
                                'page_name': page['name'],
                                'instagram_id': instagram_data['instagram_business_account']['id']
                            })
                
                result['data']['instagram_accounts_count'] = len(instagram_accounts)
                result['data']['instagram_accounts'] = instagram_accounts
                
                if not instagram_accounts:
                    result['warnings'].append("No Instagram business accounts linked to Facebook pages")
                else:
                    result['success'] = True
                    
                    if comprehensive and instagram_accounts:
                        # Test accessing Instagram account info
                        test_account = instagram_accounts[0]
                        try:
                            ig_info_response = await client.get(
                                f"https://graph.facebook.com/v18.0/{test_account['instagram_id']}?fields=account_type,media_count,followers_count",
                                params={'access_token': access_token}
                            )
                            
                            if ig_info_response.status_code == 200:
                                result['data']['sample_instagram_info'] = ig_info_response.json()
                            
                        except Exception as e:
                            result['warnings'].append(f"Could not fetch Instagram account details: {e}")
            
            if not result['success'] and not result['errors']:
                result['success'] = True  # Basic connection works even without Instagram accounts
            
        except Exception as e:
            result['errors'].append(f"Instagram test failed: {str(e)}")
        
        return result

    async def _test_twitter_connection(self, connection: SocialConnection, db: Session, comprehensive: bool) -> Dict[str, Any]:
        """Test Twitter connection."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'data': {}
        }
        
        try:
            access_token = oauth_service.get_valid_token(connection, db)
            if not access_token:
                result['errors'].append("No valid access token available")
                return result
            
            async with httpx.AsyncClient() as client:
                # Test: Get user profile
                profile_response = await client.get(
                    'https://api.twitter.com/2/users/me',
                    headers={'Authorization': f'Bearer {access_token}'},
                    params={'user.fields': 'public_metrics,verified'}
                )
                
                if profile_response.status_code != 200:
                    result['errors'].append(f"Twitter API error: {profile_response.status_code} - {profile_response.text}")
                    return result
                
                profile_data = profile_response.json()
                result['data']['user_info'] = profile_data.get('data', {})
                
                if comprehensive:
                    # Test: Get recent tweets
                    tweets_response = await client.get(
                        'https://api.twitter.com/2/users/me/tweets',
                        headers={'Authorization': f'Bearer {access_token}'},
                        params={'max_results': 5}
                    )
                    
                    if tweets_response.status_code == 200:
                        tweets_data = tweets_response.json()
                        result['data']['recent_tweets_count'] = len(tweets_data.get('data', []))
                    else:
                        result['warnings'].append("Could not fetch recent tweets")
            
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(f"Twitter test failed: {str(e)}")
        
        return result

    async def _test_linkedin_connection(self, connection: SocialConnection, db: Session, comprehensive: bool) -> Dict[str, Any]:
        """Test LinkedIn connection."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'data': {}
        }
        
        try:
            access_token = oauth_service.get_valid_token(connection, db)
            if not access_token:
                result['errors'].append("No valid access token available")
                return result
            
            async with httpx.AsyncClient() as client:
                # Test: Get user profile
                profile_response = await client.get(
                    'https://api.linkedin.com/v2/people/(id~)',
                    headers={'Authorization': f'Bearer {access_token}'}
                )
                
                if profile_response.status_code != 200:
                    result['errors'].append(f"LinkedIn API error: {profile_response.status_code}")
                    return result
                
                profile_data = profile_response.json()
                result['data']['user_info'] = profile_data
                
                if comprehensive:
                    # Test: Check posting permissions
                    try:
                        # This is a test call to see if we can access the posts endpoint
                        posts_response = await client.get(
                            'https://api.linkedin.com/v2/ugcPosts?q=authors&authors=List((id~))',
                            headers={
                                'Authorization': f'Bearer {access_token}',
                                'X-Restli-Protocol-Version': '2.0.0'
                            }
                        )
                        
                        result['data']['can_access_posts'] = posts_response.status_code == 200
                        
                    except Exception as e:
                        result['warnings'].append(f"Could not test posting permissions: {e}")
            
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(f"LinkedIn test failed: {str(e)}")
        
        return result

    async def _test_tiktok_connection(self, connection: SocialConnection, db: Session, comprehensive: bool) -> Dict[str, Any]:
        """Test TikTok connection."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'data': {}
        }
        
        try:
            access_token = oauth_service.get_valid_token(connection, db)
            if not access_token:
                result['errors'].append("No valid access token available")
                return result
            
            async with httpx.AsyncClient() as client:
                # Test: Get user info
                user_response = await client.post(
                    'https://open-api.tiktok.com/user/info/',
                    headers={'Authorization': f'Bearer {access_token}'},
                    json={'fields': ['open_id', 'union_id', 'avatar_url', 'display_name']}
                )
                
                if user_response.status_code != 200:
                    result['errors'].append(f"TikTok API error: {user_response.status_code}")
                    return result
                
                user_data = user_response.json()
                if user_data.get('error'):
                    result['errors'].append(f"TikTok API error: {user_data['error']}")
                    return result
                
                result['data']['user_info'] = user_data.get('data', {})
                
                if comprehensive:
                    # Test: Get video list
                    try:
                        videos_response = await client.post(
                            'https://open-api.tiktok.com/video/list/',
                            headers={'Authorization': f'Bearer {access_token}'},
                            json={'fields': ['id', 'title'], 'max_count': 5}
                        )
                        
                        if videos_response.status_code == 200:
                            videos_data = videos_response.json()
                            result['data']['videos_accessible'] = not videos_data.get('error')
                        
                    except Exception as e:
                        result['warnings'].append(f"Could not test video access: {e}")
            
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(f"TikTok test failed: {str(e)}")
        
        return result

    async def _test_pinterest_connection(self, connection: SocialConnection, db: Session, comprehensive: bool) -> Dict[str, Any]:
        """Test Pinterest connection."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'data': {}
        }
        
        try:
            access_token = oauth_service.get_valid_token(connection, db)
            if not access_token:
                result['errors'].append("No valid access token available")
                return result
            
            async with httpx.AsyncClient() as client:
                # Test: Get user account info
                account_response = await client.get(
                    'https://api.pinterest.com/v5/user_account',
                    headers={'Authorization': f'Bearer {access_token}'}
                )
                
                if account_response.status_code != 200:
                    result['errors'].append(f"Pinterest API error: {account_response.status_code}")
                    return result
                
                account_data = account_response.json()
                result['data']['user_info'] = account_data
                
                if comprehensive:
                    # Test: Get boards
                    try:
                        boards_response = await client.get(
                            'https://api.pinterest.com/v5/boards',
                            headers={'Authorization': f'Bearer {access_token}'},
                            params={'page_size': 5}
                        )
                        
                        if boards_response.status_code == 200:
                            boards_data = boards_response.json()
                            result['data']['boards_count'] = len(boards_data.get('items', []))
                        
                    except Exception as e:
                        result['warnings'].append(f"Could not fetch boards: {e}")
            
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(f"Pinterest test failed: {str(e)}")
        
        return result

    async def _test_snapchat_connection(self, connection: SocialConnection, db: Session, comprehensive: bool) -> Dict[str, Any]:
        """Test Snapchat connection."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'data': {}
        }
        
        try:
            access_token = oauth_service.get_valid_token(connection, db)
            if not access_token:
                result['errors'].append("No valid access token available")
                return result
            
            async with httpx.AsyncClient() as client:
                # Test: Get organization info
                me_response = await client.get(
                    'https://adsapi.snapchat.com/v1/me',
                    headers={'Authorization': f'Bearer {access_token}'}
                )
                
                if me_response.status_code != 200:
                    result['errors'].append(f"Snapchat API error: {me_response.status_code}")
                    return result
                
                me_data = me_response.json()
                result['data']['user_info'] = me_data
                
                # Snapchat API is primarily for advertising, so basic connection test is sufficient
                result['success'] = True
            
        except Exception as e:
            result['errors'].append(f"Snapchat test failed: {str(e)}")
        
        return result

    async def _test_reddit_connection(self, connection: SocialConnection, db: Session, comprehensive: bool) -> Dict[str, Any]:
        """Test Reddit connection."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'data': {}
        }
        
        try:
            access_token = oauth_service.get_valid_token(connection, db)
            if not access_token:
                result['errors'].append("No valid access token available")
                return result
            
            async with httpx.AsyncClient() as client:
                # Test: Get user info
                me_response = await client.get(
                    'https://oauth.reddit.com/api/v1/me',
                    headers={
                        'Authorization': f'Bearer {access_token}',
                        'User-Agent': 'ALwrity/1.0'
                    }
                )
                
                if me_response.status_code != 200:
                    result['errors'].append(f"Reddit API error: {me_response.status_code}")
                    return result
                
                me_data = me_response.json()
                result['data']['user_info'] = me_data
                
                if comprehensive:
                    # Test: Get user's subreddits
                    try:
                        subreddits_response = await client.get(
                            'https://oauth.reddit.com/subreddits/mine/subscriber',
                            headers={
                                'Authorization': f'Bearer {access_token}',
                                'User-Agent': 'ALwrity/1.0'
                            },
                            params={'limit': 5}
                        )
                        
                        if subreddits_response.status_code == 200:
                            subreddits_data = subreddits_response.json()
                            result['data']['subscribed_subreddits_count'] = len(subreddits_data.get('data', {}).get('children', []))
                        
                    except Exception as e:
                        result['warnings'].append(f"Could not fetch subreddits: {e}")
            
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(f"Reddit test failed: {str(e)}")
        
        return result

    async def _test_discord_connection(self, connection: SocialConnection, db: Session, comprehensive: bool) -> Dict[str, Any]:
        """Test Discord connection."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'data': {}
        }
        
        try:
            access_token = oauth_service.get_valid_token(connection, db)
            if not access_token:
                result['errors'].append("No valid access token available")
                return result
            
            async with httpx.AsyncClient() as client:
                # Test: Get user info
                user_response = await client.get(
                    'https://discord.com/api/users/@me',
                    headers={'Authorization': f'Bearer {access_token}'}
                )
                
                if user_response.status_code != 200:
                    result['errors'].append(f"Discord API error: {user_response.status_code}")
                    return result
                
                user_data = user_response.json()
                result['data']['user_info'] = user_data
                
                if comprehensive:
                    # Test: Get user's guilds
                    try:
                        guilds_response = await client.get(
                            'https://discord.com/api/users/@me/guilds',
                            headers={'Authorization': f'Bearer {access_token}'}
                        )
                        
                        if guilds_response.status_code == 200:
                            guilds_data = guilds_response.json()
                            result['data']['guilds_count'] = len(guilds_data)
                        
                    except Exception as e:
                        result['warnings'].append(f"Could not fetch guilds: {e}")
            
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(f"Discord test failed: {str(e)}")
        
        return result

    async def _test_permissions(self, connection: SocialConnection, db: Session) -> Dict[str, Any]:
        """Test if connection has all required permissions."""
        result = {
            'granted_permissions': connection.scopes or [],
            'missing_permissions': [],
            'recommended_permissions': []
        }
        
        # Define required permissions for each platform
        required_permissions = {
            'google_search_console': ['https://www.googleapis.com/auth/webmasters'],
            'youtube': ['https://www.googleapis.com/auth/youtube'],
            'facebook': ['pages_manage_posts', 'pages_read_engagement'],
            'instagram': ['instagram_basic', 'instagram_content_publish'],
            'twitter': ['tweet.write', 'users.read'],
            'linkedin': ['w_member_social', 'r_liteprofile'],
            'tiktok': ['user.info.basic', 'video.upload'],
            'pinterest': ['read_public', 'write_public'],
            'snapchat': ['snapchat-marketing-api'],
            'reddit': ['identity', 'submit'],
            'discord': ['identify', 'guilds']
        }
        
        if connection.platform in required_permissions:
            required = set(required_permissions[connection.platform])
            granted = set(connection.scopes or [])
            result['missing_permissions'] = list(required - granted)
        
        return result

    def _generate_recommendations(self, test_result: Dict[str, Any], connection: SocialConnection) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        if test_result['status'] == 'failed':
            recommendations.append("Reconnect the account to resolve authentication issues")
        
        if test_result.get('warnings'):
            recommendations.append("Review warnings and consider additional platform setup")
        
        # Platform-specific recommendations
        platform_data = test_result.get('platform_specific_data', {})
        
        if connection.platform == 'google_search_console':
            if platform_data.get('sites_count', 0) == 0:
                recommendations.append("Verify your website in Google Search Console")
        
        elif connection.platform == 'facebook':
            if platform_data.get('pages_count', 0) == 0:
                recommendations.append("Create or manage a Facebook page for posting capabilities")
        
        elif connection.platform == 'instagram':
            if platform_data.get('instagram_accounts_count', 0) == 0:
                recommendations.append("Convert your Instagram account to a business account and link it to a Facebook page")
        
        elif connection.platform == 'youtube':
            if not platform_data.get('channel_info'):
                recommendations.append("Create a YouTube channel to enable content management")
        
        return recommendations

    async def _update_connection_status(self, connection: SocialConnection, test_result: Dict[str, Any], db: Session):
        """Update connection status based on test results."""
        try:
            if test_result['status'] == 'failed':
                connection.connection_status = 'error'
            elif test_result['status'] == 'passed':
                connection.connection_status = 'active'
            
            # Update last used timestamp
            connection.last_used_at = datetime.utcnow()
            
            # Store test results in profile_data
            if not connection.profile_data:
                connection.profile_data = {}
            
            connection.profile_data['last_test'] = {
                'timestamp': test_result['test_timestamp'],
                'status': test_result['status'],
                'errors': test_result['errors'],
                'warnings': test_result['warnings']
            }
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Failed to update connection status: {e}")

# Global instance
connection_testing_service = ConnectionTestingService()