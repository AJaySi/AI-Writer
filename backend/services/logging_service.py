"""
Logging Service
Comprehensive logging and debugging service for social media integration.
"""

import os
import logging
import json
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps
import inspect

class CustomFormatter(logging.Formatter):
    """Custom formatter with colors and detailed information."""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }

    def format(self, record):
        # Add color
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Enhanced format with more details
        log_format = f"{color}[{record.levelname}]{reset} {record.asctime} | {record.name} | {record.funcName}:{record.lineno} | {record.getMessage()}"
        
        formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

class SocialMediaLogger:
    """Enhanced logger for social media integration debugging."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.setup_logger()
    
    def setup_logger(self):
        """Setup logger with appropriate handlers and formatting."""
        if not self.logger.handlers:
            # Set level from environment or default to INFO
            log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
            self.logger.setLevel(getattr(logging, log_level))
            
            # Console handler with custom formatting
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(CustomFormatter())
            
            # File handler for persistent logs
            if os.getenv('LOG_TO_FILE', 'false').lower() == 'true':
                log_dir = os.getenv('LOG_DIR', 'logs')
                os.makedirs(log_dir, exist_ok=True)
                
                file_handler = logging.FileHandler(
                    os.path.join(log_dir, f'social_media_{datetime.now().strftime("%Y%m%d")}.log')
                )
                file_handler.setFormatter(logging.Formatter(
                    '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s'
                ))
                self.logger.addHandler(file_handler)
            
            self.logger.addHandler(console_handler)
    
    def debug_oauth_flow(self, platform: str, step: str, data: Dict[str, Any]):
        """Log OAuth flow debugging information."""
        masked_data = self._mask_sensitive_data(data)
        self.logger.debug(f"OAuth {step} for {platform}: {json.dumps(masked_data, default=str)}")
    
    def info_connection_event(self, event: str, platform: str, user_id: int, details: Dict = None):
        """Log connection-related events."""
        details = details or {}
        self.logger.info(f"Connection {event}: platform={platform}, user_id={user_id}, details={details}")
    
    def warning_security_event(self, event: str, details: Dict[str, Any]):
        """Log security-related warnings."""
        masked_details = self._mask_sensitive_data(details)
        self.logger.warning(f"Security Event: {event} | {json.dumps(masked_details, default=str)}")
    
    def error_platform_api(self, platform: str, endpoint: str, error: Exception, context: Dict = None):
        """Log platform API errors with context."""
        context = context or {}
        error_details = {
            'platform': platform,
            'endpoint': endpoint,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': self._mask_sensitive_data(context),
            'traceback': traceback.format_exc()
        }
        self.logger.error(f"Platform API Error: {json.dumps(error_details, default=str)}")
    
    def debug_token_operation(self, operation: str, platform: str, success: bool, details: Dict = None):
        """Log token operations (refresh, validation, etc.)."""
        details = details or {}
        masked_details = self._mask_sensitive_data(details)
        status = "SUCCESS" if success else "FAILED"
        self.logger.debug(f"Token {operation} {status}: platform={platform}, details={masked_details}")
    
    def info_performance_metric(self, operation: str, duration: float, platform: str = None, details: Dict = None):
        """Log performance metrics."""
        details = details or {}
        metric_data = {
            'operation': operation,
            'duration_seconds': round(duration, 4),
            'platform': platform,
            'details': details
        }
        self.logger.info(f"Performance: {json.dumps(metric_data, default=str)}")
    
    def debug_api_request(self, method: str, url: str, headers: Dict = None, data: Any = None, response_code: int = None):
        """Log API request details."""
        headers = headers or {}
        # Mask authorization headers
        safe_headers = {k: v if 'auth' not in k.lower() and 'token' not in k.lower() else '***' for k, v in headers.items()}
        
        request_data = {
            'method': method,
            'url': url,
            'headers': safe_headers,
            'data': self._mask_sensitive_data(data) if data else None,
            'response_code': response_code
        }
        self.logger.debug(f"API Request: {json.dumps(request_data, default=str)}")
    
    def critical_system_error(self, component: str, error: Exception, context: Dict = None):
        """Log critical system errors."""
        context = context or {}
        error_details = {
            'component': component,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'traceback': traceback.format_exc(),
            'timestamp': datetime.utcnow().isoformat()
        }
        self.logger.critical(f"CRITICAL ERROR in {component}: {json.dumps(error_details, default=str)}")
    
    def _mask_sensitive_data(self, data: Any) -> Any:
        """Mask sensitive data in logs."""
        if isinstance(data, dict):
            masked = {}
            for key, value in data.items():
                if any(sensitive in key.lower() for sensitive in ['password', 'token', 'secret', 'key', 'auth']):
                    if isinstance(value, str) and len(value) > 8:
                        masked[key] = value[:4] + '*' * (len(value) - 8) + value[-4:]
                    else:
                        masked[key] = '***'
                else:
                    masked[key] = self._mask_sensitive_data(value) if isinstance(value, (dict, list)) else value
            return masked
        elif isinstance(data, list):
            return [self._mask_sensitive_data(item) for item in data]
        else:
            return data
    
    def log_method_entry(self, method_name: str, args: tuple = None, kwargs: dict = None):
        """Log method entry with parameters."""
        args = args or ()
        kwargs = kwargs or {}
        
        # Mask sensitive parameters
        safe_args = tuple(self._mask_sensitive_data(arg) for arg in args)
        safe_kwargs = self._mask_sensitive_data(kwargs)
        
        self.logger.debug(f"ENTER {method_name}: args={safe_args}, kwargs={safe_kwargs}")
    
    def log_method_exit(self, method_name: str, result: Any = None, duration: float = None):
        """Log method exit with result."""
        result_info = {
            'result_type': type(result).__name__ if result is not None else 'None',
            'duration_seconds': round(duration, 4) if duration else None
        }
        
        # Include result details for certain types
        if isinstance(result, dict):
            result_info['result_summary'] = {
                'keys': list(result.keys()) if result else [],
                'size': len(result) if result else 0
            }
        elif isinstance(result, (list, tuple)):
            result_info['result_summary'] = {
                'length': len(result),
                'first_item_type': type(result[0]).__name__ if result else None
            }
        
        self.logger.debug(f"EXIT {method_name}: {json.dumps(result_info, default=str)}")


def log_method_calls(logger: SocialMediaLogger):
    """Decorator to automatically log method entry and exit."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.utcnow()
            method_name = f"{func.__module__}.{func.__qualname__}"
            
            # Log entry
            logger.log_method_entry(method_name, args[1:], kwargs)  # Skip 'self' parameter
            
            try:
                result = func(*args, **kwargs)
                
                # Log successful exit
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.log_method_exit(method_name, result, duration)
                
                return result
                
            except Exception as e:
                # Log error exit
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.logger.error(f"ERROR in {method_name} after {duration:.4f}s: {str(e)}")
                raise
        
        return wrapper
    return decorator


def log_async_method_calls(logger: SocialMediaLogger):
    """Decorator to automatically log async method entry and exit."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = datetime.utcnow()
            method_name = f"{func.__module__}.{func.__qualname__}"
            
            # Log entry
            logger.log_method_entry(method_name, args[1:], kwargs)  # Skip 'self' parameter
            
            try:
                result = await func(*args, **kwargs)
                
                # Log successful exit
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.log_method_exit(method_name, result, duration)
                
                return result
                
            except Exception as e:
                # Log error exit
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.logger.error(f"ERROR in {method_name} after {duration:.4f}s: {str(e)}")
                raise
        
        return wrapper
    return decorator


# Global logger instances for different components
oauth_logger = SocialMediaLogger('oauth_service')
connection_logger = SocialMediaLogger('connection_service')
security_logger = SocialMediaLogger('security_service')
api_logger = SocialMediaLogger('api_endpoints')
testing_logger = SocialMediaLogger('connection_testing')