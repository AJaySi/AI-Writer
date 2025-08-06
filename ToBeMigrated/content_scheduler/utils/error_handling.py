from typing import Optional, Dict, Any
import logging
from functools import wraps
import traceback

logger = logging.getLogger('content_scheduler')

class SchedulingError(Exception):
    """Exception raised for errors in content scheduling."""
    
    def __init__(self, message: str):
        """Initialize the error with a message.
        
        Args:
            message: Error message
        """
        self.message = message
        super().__init__(self.message)

class JobExecutionError(SchedulingError):
    """Exception for job execution errors."""
    pass

class ScheduleValidationError(SchedulingError):
    """Exception for schedule validation errors."""
    pass

class PlatformError(SchedulingError):
    """Exception for platform-specific errors."""
    pass

class DatabaseError(SchedulingError):
    """Exception for database-related errors."""
    pass

def handle_scheduler_error(func):
    """Decorator for handling scheduler errors."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SchedulingError as e:
            logger.error(f"Scheduling error in {func.__name__}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            raise SchedulingError(
                f"Unexpected error in {func.__name__}: {str(e)}",
                {'traceback': traceback.format_exc()}
            )
    return wrapper

def handle_job_error(func):
    """Decorator for handling job execution errors."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Job execution error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            raise JobExecutionError(
                f"Job execution failed: {str(e)}",
                {
                    'function': func.__name__,
                    'traceback': traceback.format_exc()
                }
            )
    return wrapper

def handle_platform_error(func):
    """Decorator for handling platform-specific errors."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Platform error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            raise PlatformError(
                f"Platform operation failed: {str(e)}",
                {
                    'function': func.__name__,
                    'traceback': traceback.format_exc()
                }
            )
    return wrapper

def handle_database_error(func):
    """Decorator for handling database errors."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Database error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            raise DatabaseError(
                f"Database operation failed: {str(e)}",
                {
                    'function': func.__name__,
                    'traceback': traceback.format_exc()
                }
            )
    return wrapper

def format_error(error: Exception) -> Dict[str, Any]:
    """Format error for logging and reporting."""
    if isinstance(error, SchedulingError):
        return {
            'type': error.__class__.__name__,
            'message': str(error),
            'details': error.details
        }
    else:
        return {
            'type': 'UnexpectedError',
            'message': str(error),
            'details': {
                'traceback': traceback.format_exc()
            }
        }

def log_error(error: Exception, context: Optional[Dict[str, Any]] = None):
    """Log error with context."""
    error_data = format_error(error)
    if context:
        error_data['context'] = context
    
    logger.error(
        f"Error: {error_data['type']} - {error_data['message']}",
        extra={'error_data': error_data}
    ) 