"""
Security Service
Implements advanced security measures and best practices for social media integration.
"""

import os
import hashlib
import hmac
import time
import re
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
from collections import defaultdict
import ipaddress

from sqlalchemy.orm import Session
from models.social_connections import SocialConnection

# Setup logging
logger = logging.getLogger(__name__)

class SecurityService:
    def __init__(self):
        self.rate_limits = defaultdict(list)
        self.failed_attempts = defaultdict(list)
        self.blocked_ips = set()
        
        # Security configurations
        self.max_connections_per_user = int(os.getenv('MAX_CONNECTIONS_PER_USER', '20'))
        self.rate_limit_window = int(os.getenv('RATE_LIMIT_WINDOW', '300'))  # 5 minutes
        self.max_requests_per_window = int(os.getenv('MAX_REQUESTS_PER_WINDOW', '10'))
        self.max_failed_attempts = int(os.getenv('MAX_FAILED_ATTEMPTS', '5'))
        self.lockout_duration = int(os.getenv('LOCKOUT_DURATION', '3600'))  # 1 hour
        
        # Webhook security
        self.webhook_secret = os.getenv('WEBHOOK_SECRET', 'default_secret_change_me')
        
        # Allowed domains for redirects
        self.allowed_redirect_domains = [
            'localhost',
            '127.0.0.1',
            os.getenv('FRONTEND_DOMAIN', 'localhost:3000')
        ]

    def validate_request_rate(self, identifier: str, endpoint: str = 'general') -> Dict[str, Any]:
        """
        Validate request rate limits for an identifier (IP, user ID, etc.).
        
        Args:
            identifier: Unique identifier for rate limiting
            endpoint: Specific endpoint for granular rate limiting
            
        Returns:
            Dict with validation result and metadata
        """
        current_time = time.time()
        rate_key = f"{identifier}:{endpoint}"
        
        # Clean old requests
        self.rate_limits[rate_key] = [
            req_time for req_time in self.rate_limits[rate_key]
            if current_time - req_time < self.rate_limit_window
        ]
        
        # Check rate limit
        if len(self.rate_limits[rate_key]) >= self.max_requests_per_window:
            logger.warning(f"Rate limit exceeded for {identifier} on {endpoint}")
            return {
                'allowed': False,
                'reason': 'rate_limit_exceeded',
                'retry_after': self.rate_limit_window,
                'current_count': len(self.rate_limits[rate_key])
            }
        
        # Add current request
        self.rate_limits[rate_key].append(current_time)
        
        return {
            'allowed': True,
            'current_count': len(self.rate_limits[rate_key]),
            'remaining': self.max_requests_per_window - len(self.rate_limits[rate_key])
        }

    def validate_ip_address(self, ip_address: str) -> Dict[str, Any]:
        """
        Validate and analyze IP address for security threats.
        
        Args:
            ip_address: IP address to validate
            
        Returns:
            Dict with validation result and threat analysis
        """
        result = {
            'valid': False,
            'blocked': False,
            'suspicious': False,
            'reason': None,
            'analysis': {}
        }
        
        try:
            # Validate IP format
            ip_obj = ipaddress.ip_address(ip_address)
            result['valid'] = True
            result['analysis']['version'] = ip_obj.version
            result['analysis']['private'] = ip_obj.is_private
            
            # Check if IP is blocked
            if ip_address in self.blocked_ips:
                result['blocked'] = True
                result['reason'] = 'ip_blocked'
                return result
            
            # Check for suspicious patterns
            if self._is_suspicious_ip(ip_address):
                result['suspicious'] = True
                result['reason'] = 'suspicious_patterns'
            
            # Check failed attempts
            current_time = time.time()
            self.failed_attempts[ip_address] = [
                attempt_time for attempt_time in self.failed_attempts[ip_address]
                if current_time - attempt_time < self.lockout_duration
            ]
            
            if len(self.failed_attempts[ip_address]) >= self.max_failed_attempts:
                self.blocked_ips.add(ip_address)
                result['blocked'] = True
                result['reason'] = 'too_many_failed_attempts'
                logger.warning(f"IP {ip_address} blocked due to too many failed attempts")
            
        except ValueError:
            result['reason'] = 'invalid_ip_format'
        
        return result

    def _is_suspicious_ip(self, ip_address: str) -> bool:
        """Check if IP shows suspicious patterns."""
        # Check for Tor exit nodes, known VPN ranges, etc.
        # This is a simplified version - in production, use threat intelligence feeds
        suspicious_patterns = [
            # Example patterns - replace with real threat intelligence
            r'^10\.0\.0\.',  # Example private range pattern
            r'^192\.168\.',  # Local network (might be suspicious depending on context)
        ]
        
        for pattern in suspicious_patterns:
            if re.match(pattern, ip_address):
                return True
        
        return False

    def validate_user_connections(self, user_id: int, db: Session) -> Dict[str, Any]:
        """
        Validate user's connection limits and patterns.
        
        Args:
            user_id: User ID to validate
            db: Database session
            
        Returns:
            Dict with validation result
        """
        # Count user's active connections
        active_connections = db.query(SocialConnection).filter(
            SocialConnection.user_id == user_id,
            SocialConnection.connection_status == 'active'
        ).count()
        
        result = {
            'allowed': True,
            'current_connections': active_connections,
            'max_connections': self.max_connections_per_user,
            'reason': None
        }
        
        if active_connections >= self.max_connections_per_user:
            result['allowed'] = False
            result['reason'] = 'max_connections_exceeded'
            logger.warning(f"User {user_id} exceeded max connections limit ({active_connections}/{self.max_connections_per_user})")
        
        return result

    def validate_oauth_state(self, state_data: Dict, max_age_minutes: int = 10) -> Dict[str, Any]:
        """
        Validate OAuth state parameter for CSRF protection.
        
        Args:
            state_data: Decoded state data from OAuth callback
            max_age_minutes: Maximum age of state token in minutes
            
        Returns:
            Dict with validation result
        """
        result = {
            'valid': False,
            'reason': None,
            'age_minutes': None
        }
        
        try:
            # Check required fields
            if not all(key in state_data for key in ['timestamp', 'token', 'platform', 'user_id']):
                result['reason'] = 'missing_required_fields'
                return result
            
            # Check timestamp
            timestamp_str = state_data['timestamp']
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            age = datetime.utcnow() - timestamp.replace(tzinfo=None)
            result['age_minutes'] = age.total_seconds() / 60
            
            if age > timedelta(minutes=max_age_minutes):
                result['reason'] = 'state_expired'
                return result
            
            # Validate token format (should be URL-safe base64)
            token = state_data['token']
            if not re.match(r'^[A-Za-z0-9_-]+$', token):
                result['reason'] = 'invalid_token_format'
                return result
            
            result['valid'] = True
            
        except (ValueError, KeyError, TypeError) as e:
            result['reason'] = f'validation_error: {str(e)}'
        
        return result

    def validate_webhook_signature(self, payload: bytes, signature: str, platform: str) -> bool:
        """
        Validate webhook signature from social media platforms.
        
        Args:
            payload: Raw webhook payload
            signature: Signature from platform
            platform: Platform name (facebook, twitter, etc.)
            
        Returns:
            True if signature is valid
        """
        try:
            if platform == 'facebook':
                return self._validate_facebook_signature(payload, signature)
            elif platform == 'twitter':
                return self._validate_twitter_signature(payload, signature)
            # Add other platforms as needed
            else:
                logger.warning(f"No signature validation implemented for platform: {platform}")
                return False
        except Exception as e:
            logger.error(f"Webhook signature validation error: {e}")
            return False

    def _validate_facebook_signature(self, payload: bytes, signature: str) -> bool:
        """Validate Facebook webhook signature."""
        expected_signature = hmac.new(
            self.webhook_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        # Facebook sends signature as "sha256=<signature>"
        if signature.startswith('sha256='):
            signature = signature[7:]
        
        return hmac.compare_digest(expected_signature, signature)

    def _validate_twitter_signature(self, payload: bytes, signature: str) -> bool:
        """Validate Twitter webhook signature."""
        expected_signature = hmac.new(
            self.webhook_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)

    def sanitize_input(self, input_data: Any, max_length: int = 1000) -> Any:
        """
        Sanitize user input to prevent injection attacks.
        
        Args:
            input_data: Input to sanitize
            max_length: Maximum allowed length for strings
            
        Returns:
            Sanitized input
        """
        if isinstance(input_data, str):
            # Remove potentially dangerous characters
            sanitized = re.sub(r'[<>"\';\\]', '', input_data)
            # Limit length
            if len(sanitized) > max_length:
                sanitized = sanitized[:max_length]
            return sanitized.strip()
        
        elif isinstance(input_data, dict):
            return {key: self.sanitize_input(value, max_length) for key, value in input_data.items()}
        
        elif isinstance(input_data, list):
            return [self.sanitize_input(item, max_length) for item in input_data]
        
        else:
            return input_data

    def validate_redirect_url(self, url: str) -> Dict[str, Any]:
        """
        Validate redirect URL to prevent open redirect attacks.
        
        Args:
            url: URL to validate
            
        Returns:
            Dict with validation result
        """
        result = {
            'valid': False,
            'reason': None,
            'parsed_domain': None
        }
        
        try:
            # Basic URL format validation
            if not url.startswith(('http://', 'https://')):
                result['reason'] = 'invalid_protocol'
                return result
            
            # Extract domain
            domain_match = re.match(r'https?://([^/]+)', url)
            if not domain_match:
                result['reason'] = 'invalid_url_format'
                return result
            
            domain = domain_match.group(1).lower()
            result['parsed_domain'] = domain
            
            # Check against allowed domains
            if not any(allowed in domain for allowed in self.allowed_redirect_domains):
                result['reason'] = 'domain_not_allowed'
                return result
            
            # Check for suspicious patterns
            if self._has_suspicious_redirect_patterns(url):
                result['reason'] = 'suspicious_patterns'
                return result
            
            result['valid'] = True
            
        except Exception as e:
            result['reason'] = f'validation_error: {str(e)}'
        
        return result

    def _has_suspicious_redirect_patterns(self, url: str) -> bool:
        """Check for suspicious patterns in redirect URLs."""
        suspicious_patterns = [
            r'[\\@]',  # Backslash or @ in URL
            r'\.\./',  # Directory traversal
            r'javascript:',  # JavaScript protocol
            r'data:',  # Data URLs
            r'file:',  # File protocol
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return True
        
        return False

    def log_security_event(self, event_type: str, details: Dict[str, Any], severity: str = 'INFO'):
        """
        Log security events for monitoring and analysis.
        
        Args:
            event_type: Type of security event
            details: Event details
            severity: Event severity (INFO, WARNING, ERROR, CRITICAL)
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'severity': severity,
            'details': details
        }
        
        log_message = f"Security Event [{severity}]: {event_type} - {details}"
        
        if severity == 'CRITICAL':
            logger.critical(log_message)
        elif severity == 'ERROR':
            logger.error(log_message)
        elif severity == 'WARNING':
            logger.warning(log_message)
        else:
            logger.info(log_message)

    def record_failed_attempt(self, identifier: str, attempt_type: str = 'general'):
        """
        Record a failed authentication/authorization attempt.
        
        Args:
            identifier: Identifier (IP, user ID, etc.)
            attempt_type: Type of failed attempt
        """
        current_time = time.time()
        self.failed_attempts[identifier].append(current_time)
        
        self.log_security_event(
            'failed_attempt',
            {
                'identifier': identifier,
                'attempt_type': attempt_type,
                'total_recent_attempts': len(self.failed_attempts[identifier])
            },
            'WARNING'
        )

    def get_security_headers(self) -> Dict[str, str]:
        """
        Get security headers for HTTP responses.
        
        Returns:
            Dict of security headers
        """
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
        }

    def mask_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mask sensitive data in logs and responses.
        
        Args:
            data: Data dictionary to mask
            
        Returns:
            Dict with sensitive data masked
        """
        sensitive_keys = [
            'password', 'token', 'secret', 'key', 'api_key', 
            'access_token', 'refresh_token', 'client_secret',
            'webhook_secret', 'private_key'
        ]
        
        masked_data = {}
        for key, value in data.items():
            if any(sensitive_key in key.lower() for sensitive_key in sensitive_keys):
                if isinstance(value, str) and len(value) > 8:
                    masked_data[key] = value[:4] + '*' * (len(value) - 8) + value[-4:]
                else:
                    masked_data[key] = '*' * 8
            else:
                masked_data[key] = value
        
        return masked_data

# Global instance
security_service = SecurityService()