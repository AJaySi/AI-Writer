"""
Security Middleware
FastAPI middleware for enforcing security measures across all endpoints.
"""

import time
import json
from typing import Dict, Any
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

from services.security_service import security_service

logger = logging.getLogger(__name__)

class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_paths: list = None):
        super().__init__(app)
        self.excluded_paths = excluded_paths or ['/docs', '/redoc', '/openapi.json', '/health']

    async def dispatch(self, request: Request, call_next):
        """Main middleware dispatch method."""
        start_time = time.time()
        
        try:
            # Skip security checks for excluded paths
            if any(request.url.path.startswith(path) for path in self.excluded_paths):
                response = await call_next(request)
                return self._add_security_headers(response)
            
            # Extract client information
            client_ip = self._get_client_ip(request)
            user_agent = request.headers.get('user-agent', '')
            
            # Validate IP address
            ip_validation = security_service.validate_ip_address(client_ip)
            if ip_validation['blocked']:
                logger.warning(f"Blocked request from IP {client_ip}: {ip_validation['reason']}")
                return JSONResponse(
                    status_code=403,
                    content={"error": "Access denied", "reason": "IP blocked"}
                )
            
            # Rate limiting
            rate_validation = security_service.validate_request_rate(
                client_ip, 
                self._get_endpoint_key(request)
            )
            if not rate_validation['allowed']:
                logger.warning(f"Rate limit exceeded for IP {client_ip}")
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Rate limit exceeded",
                        "retry_after": rate_validation['retry_after']
                    },
                    headers={"Retry-After": str(rate_validation['retry_after'])}
                )
            
            # Log suspicious activity
            if ip_validation['suspicious']:
                security_service.log_security_event(
                    'suspicious_ip_access',
                    {
                        'ip': client_ip,
                        'path': request.url.path,
                        'user_agent': user_agent,
                        'reason': ip_validation['reason']
                    },
                    'WARNING'
                )
            
            # Add rate limit info to request state
            request.state.rate_limit_info = rate_validation
            request.state.client_ip = client_ip
            
            # Process request
            response = await call_next(request)
            
            # Add security headers
            response = self._add_security_headers(response)
            
            # Add rate limit headers
            response.headers["X-RateLimit-Remaining"] = str(rate_validation.get('remaining', 0))
            response.headers["X-RateLimit-Limit"] = str(security_service.max_requests_per_window)
            response.headers["X-RateLimit-Window"] = str(security_service.rate_limit_window)
            
            # Log successful request
            process_time = time.time() - start_time
            self._log_request(request, response, process_time)
            
            return response
            
        except HTTPException as e:
            # Handle HTTP exceptions
            security_service.record_failed_attempt(client_ip, 'http_error')
            logger.warning(f"HTTP exception for IP {client_ip}: {e.status_code} - {e.detail}")
            response = JSONResponse(
                status_code=e.status_code,
                content={"error": e.detail}
            )
            return self._add_security_headers(response)
            
        except Exception as e:
            # Handle unexpected errors
            security_service.record_failed_attempt(client_ip, 'server_error')
            security_service.log_security_event(
                'server_error',
                {
                    'ip': client_ip,
                    'path': request.url.path,
                    'error': str(e)
                },
                'ERROR'
            )
            logger.error(f"Unexpected error for IP {client_ip}: {str(e)}")
            response = JSONResponse(
                status_code=500,
                content={"error": "Internal server error"}
            )
            return self._add_security_headers(response)

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request."""
        # Check for forwarded IPs (from load balancers/proxies)
        forwarded_for = request.headers.get('x-forwarded-for')
        if forwarded_for:
            # Take the first IP in the chain
            return forwarded_for.split(',')[0].strip()
        
        real_ip = request.headers.get('x-real-ip')
        if real_ip:
            return real_ip
        
        # Fallback to direct client IP
        return request.client.host if request.client else '127.0.0.1'

    def _get_endpoint_key(self, request: Request) -> str:
        """Generate endpoint key for rate limiting."""
        method = request.method
        path = request.url.path
        
        # Normalize path for rate limiting (remove IDs)
        normalized_path = self._normalize_path(path)
        
        return f"{method}:{normalized_path}"

    def _normalize_path(self, path: str) -> str:
        """Normalize path by removing dynamic parameters."""
        # Replace numeric IDs and UUIDs with placeholders
        import re
        
        # Replace numeric IDs
        path = re.sub(r'/\d+', '/{id}', path)
        
        # Replace UUIDs
        path = re.sub(
            r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            '/{uuid}',
            path,
            flags=re.IGNORECASE
        )
        
        return path

    def _add_security_headers(self, response: Response) -> Response:
        """Add security headers to response."""
        security_headers = security_service.get_security_headers()
        
        for header, value in security_headers.items():
            response.headers[header] = value
        
        return response

    def _log_request(self, request: Request, response: Response, process_time: float):
        """Log request details for monitoring."""
        log_data = {
            'method': request.method,
            'path': request.url.path,
            'status_code': response.status_code,
            'process_time': round(process_time, 4),
            'client_ip': getattr(request.state, 'client_ip', 'unknown'),
            'user_agent': request.headers.get('user-agent', ''),
            'content_length': response.headers.get('content-length', 0)
        }
        
        # Mask sensitive data
        masked_data = security_service.mask_sensitive_data(log_data)
        
        if response.status_code >= 400:
            logger.warning(f"Request failed: {masked_data}")
        else:
            logger.info(f"Request completed: {masked_data}")


class OAuth2SecurityMiddleware(BaseHTTPMiddleware):
    """Specialized middleware for OAuth2 endpoints."""
    
    def __init__(self, app):
        super().__init__(app)
        self.oauth_paths = ['/api/social/auth/', '/api/social/oauth/']

    async def dispatch(self, request: Request, call_next):
        """OAuth2-specific security checks."""
        
        # Only apply to OAuth paths
        if not any(request.url.path.startswith(path) for path in self.oauth_paths):
            return await call_next(request)
        
        try:
            client_ip = request.client.host if request.client else '127.0.0.1'
            
            # Enhanced rate limiting for OAuth endpoints
            rate_validation = security_service.validate_request_rate(
                client_ip, 
                'oauth',
                max_requests=3,  # Stricter limit for OAuth
                window_minutes=5
            )
            
            if not rate_validation['allowed']:
                security_service.log_security_event(
                    'oauth_rate_limit_exceeded',
                    {'ip': client_ip, 'path': request.url.path},
                    'WARNING'
                )
                return JSONResponse(
                    status_code=429,
                    content={"error": "OAuth rate limit exceeded. Please try again later."}
                )
            
            # Validate state parameter for OAuth callbacks
            if 'callback' in request.url.path and request.query_params.get('state'):
                state_param = request.query_params.get('state')
                try:
                    # Decode and validate state
                    import base64
                    import json
                    decoded_state = json.loads(base64.urlsafe_b64decode(state_param))
                    
                    state_validation = security_service.validate_oauth_state(decoded_state)
                    if not state_validation['valid']:
                        security_service.log_security_event(
                            'invalid_oauth_state',
                            {
                                'ip': client_ip,
                                'reason': state_validation['reason'],
                                'state_age': state_validation.get('age_minutes')
                            },
                            'ERROR'
                        )
                        return JSONResponse(
                            status_code=400,
                            content={"error": "Invalid or expired OAuth state"}
                        )
                        
                except Exception as e:
                    security_service.log_security_event(
                        'oauth_state_decode_error',
                        {'ip': client_ip, 'error': str(e)},
                        'ERROR'
                    )
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Malformed OAuth state parameter"}
                    )
            
            # Validate redirect URLs in OAuth initiation
            if request.method == 'GET' and 'auth' in request.url.path:
                redirect_uri = request.query_params.get('redirect_uri')
                if redirect_uri:
                    redirect_validation = security_service.validate_redirect_url(redirect_uri)
                    if not redirect_validation['valid']:
                        security_service.log_security_event(
                            'invalid_oauth_redirect',
                            {
                                'ip': client_ip,
                                'redirect_uri': redirect_uri,
                                'reason': redirect_validation['reason']
                            },
                            'WARNING'
                        )
                        return JSONResponse(
                            status_code=400,
                            content={"error": "Invalid redirect URI"}
                        )
            
            return await call_next(request)
            
        except Exception as e:
            security_service.log_security_event(
                'oauth_middleware_error',
                {'ip': client_ip, 'error': str(e)},
                'ERROR'
            )
            return JSONResponse(
                status_code=500,
                content={"error": "OAuth security validation failed"}
            )