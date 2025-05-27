import functools
import logging
from typing import Any, Callable, TypeVar, cast
from datetime import datetime

logger = logging.getLogger(__name__)

T = TypeVar('T')

def handle_calendar_error(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator to handle errors in calendar operations.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function with error handling
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Invalid input in {func.__name__}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise CalendarError(f"Calendar operation failed: {str(e)}")
    return cast(Callable[..., T], wrapper)

class CalendarError(Exception):
    """Base exception for calendar-related errors."""
    pass

class ContentError(CalendarError):
    """Exception for content-related errors."""
    pass

class SchedulingError(CalendarError):
    """Exception for scheduling-related errors."""
    pass

class ValidationError(CalendarError):
    """Exception for validation-related errors."""
    pass

def validate_date_range(
    start_date: datetime,
    end_date: datetime
) -> None:
    """
    Validate date range for calendar operations.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Raises:
        ValidationError: If date range is invalid
    """
    if not isinstance(start_date, datetime):
        raise ValidationError("Start date must be a datetime object")
    
    if not isinstance(end_date, datetime):
        raise ValidationError("End date must be a datetime object")
    
    if start_date > end_date:
        raise ValidationError("Start date must be before end date")
    
    if (end_date - start_date).days > 365:
        raise ValidationError("Calendar duration cannot exceed one year")

def validate_content_item(content: dict) -> None:
    """
    Validate content item structure.
    
    Args:
        content: Content item to validate
        
    Raises:
        ValidationError: If content item is invalid
    """
    required_fields = ['title', 'description', 'content_type', 'platforms']
    
    for field in required_fields:
        if field not in content:
            raise ValidationError(f"Missing required field: {field}")
    
    if not isinstance(content['platforms'], list):
        raise ValidationError("Platforms must be a list")
    
    if not content['platforms']:
        raise ValidationError("At least one platform must be specified")

def validate_calendar_duration(duration: str) -> None:
    """
    Validate calendar duration.
    
    Args:
        duration: Duration to validate ('weekly', 'monthly', 'quarterly')
        
    Raises:
        ValidationError: If duration is invalid
    """
    valid_durations = ['weekly', 'monthly', 'quarterly']
    
    if duration not in valid_durations:
        raise ValidationError(
            f"Invalid duration: {duration}. "
            f"Must be one of: {', '.join(valid_durations)}"
        )

def log_calendar_operation(
    operation: str,
    details: dict
) -> None:
    """
    Log calendar operation details.
    
    Args:
        operation: Name of the operation
        details: Operation details to log
    """
    logger.info(f"Calendar operation: {operation}")
    logger.debug(f"Operation details: {details}")

def handle_api_error(
    error: Exception,
    operation: str
) -> None:
    """
    Handle API-related errors.
    
    Args:
        error: The error that occurred
        operation: The operation that failed
    """
    logger.error(f"API error in {operation}: {str(error)}")
    raise CalendarError(f"API operation failed: {str(error)}")

def handle_integration_error(
    error: Exception,
    integration: str
) -> None:
    """
    Handle integration-related errors.
    
    Args:
        error: The error that occurred
        integration: The integration that failed
    """
    logger.error(f"Integration error with {integration}: {str(error)}")
    raise CalendarError(f"Integration failed: {str(error)}") 