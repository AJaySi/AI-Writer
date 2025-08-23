"""
OAuth Service for handling social media platform authentication.
Supports Google Search Console, Facebook, Twitter, LinkedIn, YouTube, and other platforms.
"""

import os
import json
import secrets
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from urllib.parse import urlencode
import httpx
from cryptography.fernet import Fernet

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from sqlalchemy.orm import Session
from models.social_connections import SocialConnection
from services.database import get_db

class OAuthService:
    def __init__(self):
        self.encryption_key = os.getenv('OAUTH_ENCRYPTION_KEY', Fernet.generate_key())
        self.fernet = Fernet(self.encryption_key)
        
        # OAuth configurations for different platforms
        self.oauth_configs = {
            'google_search_console': {
                'client_id': os.getenv('GOOGLE_CLIENT_ID'),
                'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
                'redirect_uri': os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8000/api/oauth/callback/google'),
                'scopes': [
                    'https://www.googleapis.com/auth/webmasters.readonly',
                    'https://www.googleapis.com/auth/webmasters'
                ],
                'auth_url': 'https://accounts.google.com/o/oauth2/auth',
                'token_url': 'https://oauth2.googleapis.com/token'
            },
            'youtube': {
                'client_id': os.getenv('GOOGLE_CLIENT_ID'),  # Same as GSC
                'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
                'redirect_uri': os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8000/api/oauth/callback/google'),
                'scopes': [
                    'https://www.googleapis.com/auth/youtube',
                    'https://www.googleapis.com/auth/youtube.upload',
                    'https://www.googleapis.com/auth/youtube.readonly'
                ],
                'auth_url': 'https://accounts.google.com/o/oauth2/auth',
                'token_url': 'https://oauth2.googleapis.com/token'
            },
            'facebook': {
                'client_id': os.getenv('FACEBOOK_APP_ID'),
                'client_secret': os.getenv('FACEBOOK_APP_SECRET'),
                'redirect_uri': os.getenv('FACEBOOK_REDIRECT_URI', 'http://localhost:8000/api/oauth/callback/facebook'),
                'scopes': [
                    'pages_manage_posts',
                    'pages_read_engagement',
                    'pages_show_list',
                    'business_management',
                    'read_insights'
                ],
                'auth_url': 'https://www.facebook.com/v18.0/dialog/oauth',
                'token_url': 'https://graph.facebook.com/v18.0/oauth/access_token'
            },
            'twitter': {
                'client_id': os.getenv('TWITTER_CLIENT_ID'),
                'client_secret': os.getenv('TWITTER_CLIENT_SECRET'),
                'redirect_uri': os.getenv('TWITTER_REDIRECT_URI', 'http://localhost:8000/api/oauth/callback/twitter'),
                'scopes': [
                    'tweet.read',
                    'tweet.write',
                    'users.read',
                    'offline.access'
                ],
                'auth_url': 'https://twitter.com/i/oauth2/authorize',
                'token_url': 'https://api.twitter.com/2/oauth2/token'
            },
            'linkedin': {
                'client_id': os.getenv('LINKEDIN_CLIENT_ID'),
                'client_secret': os.getenv('LINKEDIN_CLIENT_SECRET'),
                'redirect_uri': os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:8000/api/oauth/callback/linkedin'),
                'scopes': [
                    'w_member_social',
                    'r_liteprofile',
                    'r_emailaddress',
                    'w_organization_social',
                    'r_organization_social'
                ],
                'auth_url': 'https://www.linkedin.com/oauth/v2/authorization',
                'token_url': 'https://www.linkedin.com/oauth/v2/accessToken'
            }
        }

    def encrypt_token(self, token: str) -> str:
        """Encrypt an OAuth token for secure storage."""
        return self.fernet.encrypt(token.encode()).decode()

    def decrypt_token(self, encrypted_token: str) -> str:
        """Decrypt an OAuth token for use."""
        return self.fernet.decrypt(encrypted_token.encode()).decode()

    def generate_auth_url(self, platform: str, user_id: int, state_data: Dict = None) -> Tuple[str, str]:
        """
        Generate OAuth authorization URL for a platform.
        Returns: (auth_url, state_token)
        """
        if platform not in self.oauth_configs:
            raise ValueError(f"Unsupported platform: {platform}")
        
        config = self.oauth_configs[platform]
        
        # Generate state token for security
        state_token = secrets.token_urlsafe(32)
        state_data = state_data or {}
        state_data.update({
            'platform': platform,
            'user_id': user_id,
            'token': state_token,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Store state data temporarily (in production, use Redis or database)
        # For now, we'll encode it in the state parameter
        state_encoded = json.dumps(state_data)
        
        if platform.startswith('google') or platform == 'youtube':
            # Use Google OAuth flow
            flow = Flow.from_client_config({
                "web": {
                    "client_id": config['client_id'],
                    "client_secret": config['client_secret'],
                    "auth_uri": config['auth_url'],
                    "token_uri": config['token_url'],
                    "redirect_uris": [config['redirect_uri']]
                }
            }, scopes=config['scopes'])
            flow.redirect_uri = config['redirect_uri']
            
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                state=state_encoded
            )
            return auth_url, state_token
        
        else:
            # Standard OAuth2 flow for other platforms
            params = {
                'client_id': config['client_id'],
                'redirect_uri': config['redirect_uri'],
                'scope': ' '.join(config['scopes']),
                'response_type': 'code',
                'state': state_encoded
            }
            
            auth_url = f"{config['auth_url']}?{urlencode(params)}"
            return auth_url, state_token

    async def handle_oauth_callback(self, platform: str, code: str, state: str) -> Dict:
        """
        Handle OAuth callback and exchange code for tokens.
        Returns connection data.
        """
        if platform not in self.oauth_configs:
            raise ValueError(f"Unsupported platform: {platform}")
        
        # Decode and validate state
        try:
            state_data = json.loads(state)
            if state_data.get('platform') != platform:
                raise ValueError("Invalid state parameter")
        except (json.JSONDecodeError, KeyError):
            raise ValueError("Invalid state parameter")
        
        config = self.oauth_configs[platform]
        
        if platform.startswith('google') or platform == 'youtube':
            return await self._handle_google_callback(platform, code, state_data, config)
        elif platform == 'facebook':
            return await self._handle_facebook_callback(code, state_data, config)
        elif platform == 'twitter':
            return await self._handle_twitter_callback(code, state_data, config)
        elif platform == 'linkedin':
            return await self._handle_linkedin_callback(code, state_data, config)
        else:
            raise ValueError(f"Callback handler not implemented for {platform}")

    async def _handle_google_callback(self, platform: str, code: str, state_data: Dict, config: Dict) -> Dict:
        """Handle Google OAuth callback (GSC, YouTube)."""
        flow = Flow.from_client_config({
            "web": {
                "client_id": config['client_id'],
                "client_secret": config['client_secret'],
                "auth_uri": config['auth_url'],
                "token_uri": config['token_url'],
                "redirect_uris": [config['redirect_uri']]
            }
        }, scopes=config['scopes'])
        flow.redirect_uri = config['redirect_uri']
        
        # Exchange code for tokens
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Get user profile
        if platform == 'google_search_console':
            # For GSC, we'll use the webmasters API to get site list
            service = build('searchconsole', 'v1', credentials=credentials)
            sites_list = service.sites().list().execute()
            profile_data = {
                'sites': sites_list.get('siteEntry', []),
                'platform': 'google_search_console'
            }
            platform_user_id = credentials.client_id  # Use client ID as identifier
            platform_username = f"GSC User ({len(sites_list.get('siteEntry', []))} sites)"
        else:  # YouTube
            service = build('youtube', 'v3', credentials=credentials)
            channels = service.channels().list(part='snippet', mine=True).execute()
            if channels['items']:
                channel = channels['items'][0]
                profile_data = {
                    'channel_id': channel['id'],
                    'title': channel['snippet']['title'],
                    'description': channel['snippet']['description'],
                    'thumbnail': channel['snippet']['thumbnails'].get('default', {}).get('url'),
                    'platform': 'youtube'
                }
                platform_user_id = channel['id']
                platform_username = channel['snippet']['title']
            else:
                raise ValueError("No YouTube channel found for this account")
        
        return {
            'platform': platform,
            'user_id': state_data['user_id'],
            'access_token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'expires_at': credentials.expiry,
            'scopes': config['scopes'],
            'profile_data': profile_data,
            'platform_user_id': platform_user_id,
            'platform_username': platform_username
        }

    async def _handle_facebook_callback(self, code: str, state_data: Dict, config: Dict) -> Dict:
        """Handle Facebook OAuth callback."""
        async with httpx.AsyncClient() as client:
            # Exchange code for access token
            token_response = await client.post(config['token_url'], data={
                'client_id': config['client_id'],
                'client_secret': config['client_secret'],
                'redirect_uri': config['redirect_uri'],
                'code': code
            })
            token_data = token_response.json()
            
            if 'access_token' not in token_data:
                raise ValueError("Failed to obtain access token")
            
            # Get user profile
            profile_response = await client.get(
                'https://graph.facebook.com/v18.0/me',
                params={
                    'access_token': token_data['access_token'],
                    'fields': 'id,name,email,picture'
                }
            )
            profile_data = profile_response.json()
            
            # Get pages managed by user
            pages_response = await client.get(
                'https://graph.facebook.com/v18.0/me/accounts',
                params={
                    'access_token': token_data['access_token']
                }
            )
            pages_data = pages_response.json()
            profile_data['pages'] = pages_data.get('data', [])
            
            return {
                'platform': 'facebook',
                'user_id': state_data['user_id'],
                'access_token': token_data['access_token'],
                'refresh_token': None,  # Facebook doesn't provide refresh tokens for some flows
                'expires_at': datetime.utcnow() + timedelta(seconds=token_data.get('expires_in', 3600)),
                'scopes': config['scopes'],
                'profile_data': profile_data,
                'platform_user_id': profile_data['id'],
                'platform_username': profile_data['name']
            }

    async def _handle_twitter_callback(self, code: str, state_data: Dict, config: Dict) -> Dict:
        """Handle Twitter OAuth callback."""
        async with httpx.AsyncClient() as client:
            # Exchange code for access token
            token_response = await client.post(
                config['token_url'],
                data={
                    'client_id': config['client_id'],
                    'client_secret': config['client_secret'],
                    'redirect_uri': config['redirect_uri'],
                    'grant_type': 'authorization_code',
                    'code': code
                },
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            token_data = token_response.json()
            
            if 'access_token' not in token_data:
                raise ValueError("Failed to obtain access token")
            
            # Get user profile
            profile_response = await client.get(
                'https://api.twitter.com/2/users/me',
                headers={
                    'Authorization': f"Bearer {token_data['access_token']}"
                },
                params={
                    'user.fields': 'id,name,username,description,public_metrics,profile_image_url'
                }
            )
            profile_data = profile_response.json()
            
            return {
                'platform': 'twitter',
                'user_id': state_data['user_id'],
                'access_token': token_data['access_token'],
                'refresh_token': token_data.get('refresh_token'),
                'expires_at': datetime.utcnow() + timedelta(seconds=token_data.get('expires_in', 7200)),
                'scopes': config['scopes'],
                'profile_data': profile_data.get('data', {}),
                'platform_user_id': profile_data.get('data', {}).get('id'),
                'platform_username': profile_data.get('data', {}).get('username')
            }

    async def _handle_linkedin_callback(self, code: str, state_data: Dict, config: Dict) -> Dict:
        """Handle LinkedIn OAuth callback."""
        async with httpx.AsyncClient() as client:
            # Exchange code for access token
            token_response = await client.post(
                config['token_url'],
                data={
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': config['redirect_uri'],
                    'client_id': config['client_id'],
                    'client_secret': config['client_secret']
                },
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            token_data = token_response.json()
            
            if 'access_token' not in token_data:
                raise ValueError("Failed to obtain access token")
            
            # Get user profile
            profile_response = await client.get(
                'https://api.linkedin.com/v2/people/(id~)',
                headers={
                    'Authorization': f"Bearer {token_data['access_token']}"
                }
            )
            profile_data = profile_response.json()
            
            return {
                'platform': 'linkedin',
                'user_id': state_data['user_id'],
                'access_token': token_data['access_token'],
                'refresh_token': token_data.get('refresh_token'),
                'expires_at': datetime.utcnow() + timedelta(seconds=token_data.get('expires_in', 5184000)),
                'scopes': config['scopes'],
                'profile_data': profile_data,
                'platform_user_id': profile_data.get('id'),
                'platform_username': profile_data.get('localizedFirstName', '') + ' ' + profile_data.get('localizedLastName', '')
            }

    def save_connection(self, connection_data: Dict, db: Session) -> SocialConnection:
        """Save social media connection to database."""
        # Check if connection already exists
        existing = db.query(SocialConnection).filter(
            SocialConnection.user_id == connection_data['user_id'],
            SocialConnection.platform == connection_data['platform'],
            SocialConnection.platform_user_id == connection_data['platform_user_id']
        ).first()
        
        if existing:
            # Update existing connection
            existing.access_token = self.encrypt_token(connection_data['access_token'])
            if connection_data['refresh_token']:
                existing.refresh_token = self.encrypt_token(connection_data['refresh_token'])
            existing.expires_at = connection_data['expires_at']
            existing.scopes = connection_data['scopes']
            existing.profile_data = connection_data['profile_data']
            existing.platform_username = connection_data['platform_username']
            existing.connection_status = 'active'
            existing.last_used_at = datetime.utcnow()
            existing.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(existing)
            return existing
        else:
            # Create new connection
            connection = SocialConnection(
                user_id=connection_data['user_id'],
                platform=connection_data['platform'],
                platform_user_id=connection_data['platform_user_id'],
                platform_username=connection_data['platform_username'],
                access_token=self.encrypt_token(connection_data['access_token']),
                refresh_token=self.encrypt_token(connection_data['refresh_token']) if connection_data['refresh_token'] else None,
                expires_at=connection_data['expires_at'],
                scopes=connection_data['scopes'],
                profile_data=connection_data['profile_data'],
                connection_status='active'
            )
            
            db.add(connection)
            db.commit()
            db.refresh(connection)
            return connection

    def get_valid_token(self, connection: SocialConnection, db: Session) -> Optional[str]:
        """Get a valid access token for a connection, refreshing if necessary."""
        if connection.connection_status != 'active':
            return None
        
        # Decrypt current token
        access_token = self.decrypt_token(connection.access_token)
        
        # Check if token is expired
        if connection.is_token_expired():
            if connection.refresh_token and connection.platform in ['google_search_console', 'youtube', 'twitter', 'linkedin']:
                # Attempt to refresh token
                try:
                    refreshed_token = self._refresh_token(connection)
                    if refreshed_token:
                        return refreshed_token
                except Exception as e:
                    print(f"Failed to refresh token for {connection.platform}: {e}")
                    connection.connection_status = 'expired'
                    db.commit()
                    return None
            else:
                connection.connection_status = 'expired'
                db.commit()
                return None
        
        return access_token

    def _refresh_token(self, connection: SocialConnection) -> Optional[str]:
        """Refresh an expired access token."""
        # Implementation depends on the platform
        # For Google services, we can use the google-auth library
        if connection.platform in ['google_search_console', 'youtube']:
            return self._refresh_google_token(connection)
        
        # For other platforms, implement specific refresh logic
        return None

    def _refresh_google_token(self, connection: SocialConnection) -> Optional[str]:
        """Refresh Google OAuth token."""
        try:
            config = self.oauth_configs[connection.platform]
            credentials = Credentials(
                token=self.decrypt_token(connection.access_token),
                refresh_token=self.decrypt_token(connection.refresh_token),
                token_uri=config['token_url'],
                client_id=config['client_id'],
                client_secret=config['client_secret']
            )
            
            credentials.refresh(Request())
            
            # Update connection with new token
            connection.access_token = self.encrypt_token(credentials.token)
            if credentials.refresh_token:
                connection.refresh_token = self.encrypt_token(credentials.refresh_token)
            connection.expires_at = credentials.expiry
            connection.last_used_at = datetime.utcnow()
            
            return credentials.token
        except Exception as e:
            print(f"Failed to refresh Google token: {e}")
            return None

# Global instance
oauth_service = OAuthService()