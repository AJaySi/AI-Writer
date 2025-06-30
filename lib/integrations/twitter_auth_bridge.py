"""
Twitter Authentication Bridge
Connects the platform adapter with the UI authentication system for secure Twitter integration.
"""

import streamlit as st
import tweepy
import json
import os
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import base64
from cryptography.fernet import Fernet
import logging

from .platform_adapters.twitter import TwitterAdapter

logger = logging.getLogger(__name__)

class TwitterAuthBridge:
    """Bridge between Twitter authentication and platform adapter."""
    
    def __init__(self):
        self.config_dir = Path("config/twitter")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.encryption_key = self._get_or_create_encryption_key()
        
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for secure credential storage."""
        key_file = self.config_dir / "encryption.key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def encrypt_credentials(self, credentials: Dict[str, str]) -> str:
        """Encrypt Twitter credentials for secure storage."""
        try:
            fernet = Fernet(self.encryption_key)
            credentials_json = json.dumps(credentials)
            encrypted_data = fernet.encrypt(credentials_json.encode())
            return base64.b64encode(encrypted_data).decode()
        except Exception as e:
            logger.error(f"Failed to encrypt credentials: {str(e)}")
            raise
    
    def decrypt_credentials(self, encrypted_data: str) -> Dict[str, str]:
        """Decrypt Twitter credentials from secure storage."""
        try:
            fernet = Fernet(self.encryption_key)
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted_data = fernet.decrypt(encrypted_bytes)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            logger.error(f"Failed to decrypt credentials: {str(e)}")
            raise
    
    def save_credentials(self, user_id: str, credentials: Dict[str, str]) -> bool:
        """Save encrypted Twitter credentials to file."""
        try:
            # Create user-specific credentials file
            user_hash = hashlib.sha256(user_id.encode()).hexdigest()[:16]
            creds_file = self.config_dir / f"user_{user_hash}.enc"
            
            # Add timestamp and validation
            credentials_with_meta = {
                **credentials,
                'created_at': datetime.now().isoformat(),
                'user_id_hash': user_hash
            }
            
            # Encrypt and save
            encrypted_data = self.encrypt_credentials(credentials_with_meta)
            with open(creds_file, 'w') as f:
                f.write(encrypted_data)
            
            logger.info(f"Credentials saved for user {user_hash}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save credentials: {str(e)}")
            return False
    
    def load_credentials(self, user_id: str) -> Optional[Dict[str, str]]:
        """Load and decrypt Twitter credentials from file."""
        try:
            user_hash = hashlib.sha256(user_id.encode()).hexdigest()[:16]
            creds_file = self.config_dir / f"user_{user_hash}.enc"
            
            if not creds_file.exists():
                logger.warning(f"No credentials found for user {user_hash}")
                return None
            
            # Load and decrypt
            with open(creds_file, 'r') as f:
                encrypted_data = f.read()
            
            credentials = self.decrypt_credentials(encrypted_data)
            
            # Validate credentials are not expired (optional)
            created_at = datetime.fromisoformat(credentials.get('created_at', ''))
            if datetime.now() - created_at > timedelta(days=365):  # 1 year expiry
                logger.warning(f"Credentials expired for user {user_hash}")
                return None
            
            # Remove metadata before returning
            clean_credentials = {k: v for k, v in credentials.items() 
                               if k not in ['created_at', 'user_id_hash']}
            
            return clean_credentials
            
        except Exception as e:
            logger.error(f"Failed to load credentials: {str(e)}")
            return None
    
    def delete_credentials(self, user_id: str) -> bool:
        """Delete stored Twitter credentials."""
        try:
            user_hash = hashlib.sha256(user_id.encode()).hexdigest()[:16]
            creds_file = self.config_dir / f"user_{user_hash}.enc"
            
            if creds_file.exists():
                creds_file.unlink()
                logger.info(f"Credentials deleted for user {user_hash}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete credentials: {str(e)}")
            return False
    
    def validate_credentials(self, credentials: Dict[str, str]) -> Tuple[bool, str]:
        """Validate Twitter API credentials."""
        try:
            # Check required fields
            required_fields = ['api_key', 'api_secret', 'access_token', 'access_token_secret']
            missing_fields = [field for field in required_fields if not credentials.get(field)]
            
            if missing_fields:
                return False, f"Missing required fields: {', '.join(missing_fields)}"
            
            # Test connection
            auth = tweepy.OAuthHandler(
                credentials['api_key'],
                credentials['api_secret']
            )
            auth.set_access_token(
                credentials['access_token'],
                credentials['access_token_secret']
            )
            
            api = tweepy.API(auth)
            user = api.verify_credentials()
            
            if user:
                return True, f"Valid credentials for @{user.screen_name}"
            else:
                return False, "Failed to verify credentials"
                
        except tweepy.Unauthorized:
            return False, "Invalid API credentials"
        except tweepy.Forbidden:
            return False, "Access forbidden - check API permissions"
        except tweepy.TooManyRequests:
            return False, "Rate limit exceeded - try again later"
        except Exception as e:
            return False, f"Connection error: {str(e)}"
    
    def get_twitter_adapter(self, user_id: str) -> Optional[TwitterAdapter]:
        """Get configured Twitter adapter for user."""
        try:
            # First check session state
            if 'twitter_adapter' in st.session_state:
                return st.session_state.twitter_adapter
            
            # Load credentials
            credentials = self.load_credentials(user_id)
            if not credentials:
                return None
            
            # Validate credentials
            is_valid, message = self.validate_credentials(credentials)
            if not is_valid:
                logger.error(f"Invalid credentials: {message}")
                return None
            
            # Create adapter
            adapter = TwitterAdapter(credentials)
            
            # Cache in session state
            st.session_state.twitter_adapter = adapter
            
            return adapter
            
        except Exception as e:
            logger.error(f"Failed to get Twitter adapter: {str(e)}")
            return None
    
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get Twitter user information."""
        try:
            adapter = self.get_twitter_adapter(user_id)
            if not adapter:
                return None
            
            # Get user info from Twitter
            user = adapter.client.verify_credentials()
            
            user_info = {
                'id': user.id_str,
                'screen_name': user.screen_name,
                'name': user.name,
                'description': user.description,
                'followers_count': user.followers_count,
                'friends_count': user.friends_count,
                'statuses_count': user.statuses_count,
                'profile_image_url': user.profile_image_url_https,
                'profile_banner_url': getattr(user, 'profile_banner_url', ''),
                'verified': user.verified,
                'created_at': user.created_at.isoformat(),
                'location': user.location or '',
                'url': user.url or ''
            }
            
            return user_info
            
        except Exception as e:
            logger.error(f"Failed to get user info: {str(e)}")
            return None
    
    def setup_session_state(self, user_id: str) -> bool:
        """Setup session state with Twitter authentication."""
        try:
            # Load credentials
            credentials = self.load_credentials(user_id)
            if not credentials:
                return False
            
            # Get user info
            user_info = self.get_user_info(user_id)
            if not user_info:
                return False
            
            # Setup session state
            st.session_state.twitter_authenticated = True
            st.session_state.twitter_user_id = user_id
            st.session_state.twitter_user_info = user_info
            st.session_state.twitter_config = credentials
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup session state: {str(e)}")
            return False
    
    def clear_session_state(self) -> None:
        """Clear Twitter authentication from session state."""
        keys_to_clear = [
            'twitter_authenticated',
            'twitter_user_id', 
            'twitter_user_info',
            'twitter_config',
            'twitter_adapter'
        ]
        
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated with Twitter."""
        return (
            st.session_state.get('twitter_authenticated', False) and
            st.session_state.get('twitter_user_info') is not None and
            st.session_state.get('twitter_config') is not None
        )
    
    def get_rate_limit_status(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get current rate limit status."""
        try:
            adapter = self.get_twitter_adapter(user_id)
            if not adapter:
                return None
            
            rate_limits = adapter.client.get_rate_limit_status()
            
            # Extract relevant rate limits
            relevant_limits = {
                'tweets': rate_limits['resources']['statuses']['/statuses/update'],
                'user_timeline': rate_limits['resources']['statuses']['/statuses/user_timeline'],
                'verify_credentials': rate_limits['resources']['account']['/account/verify_credentials']
            }
            
            return relevant_limits
            
        except Exception as e:
            logger.error(f"Failed to get rate limit status: {str(e)}")
            return None

# Global instance
twitter_auth = TwitterAuthBridge()

# Convenience functions for UI
def save_twitter_credentials(user_id: str, credentials: Dict[str, str]) -> bool:
    """Save Twitter credentials (convenience function)."""
    return twitter_auth.save_credentials(user_id, credentials)

def load_twitter_credentials(user_id: str) -> Optional[Dict[str, str]]:
    """Load Twitter credentials (convenience function)."""
    return twitter_auth.load_credentials(user_id)

def get_twitter_adapter(user_id: str) -> Optional[TwitterAdapter]:
    """Get Twitter adapter (convenience function)."""
    return twitter_auth.get_twitter_adapter(user_id)

def is_twitter_authenticated() -> bool:
    """Check if Twitter is authenticated (convenience function)."""
    return twitter_auth.is_authenticated()

def setup_twitter_session(user_id: str) -> bool:
    """Setup Twitter session (convenience function)."""
    return twitter_auth.setup_session_state(user_id)

def clear_twitter_session() -> None:
    """Clear Twitter session (convenience function)."""
    twitter_auth.clear_session_state()

def validate_twitter_credentials(credentials: Dict[str, str]) -> Tuple[bool, str]:
    """Validate Twitter credentials (convenience function)."""
    return twitter_auth.validate_credentials(credentials) 