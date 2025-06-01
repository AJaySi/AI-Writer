from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import pytz
from .error_handling import ScheduleValidationError

def validate_schedule_data(schedule_data: Dict[str, Any]) -> None:
    """Validate schedule data before creation."""
    required_fields = ['content_id', 'schedule_type', 'platforms', 'publish_date']
    missing_fields = [field for field in required_fields if field not in schedule_data]
    
    if missing_fields:
        raise ScheduleValidationError(
            f"Missing required fields: {', '.join(missing_fields)}",
            {'missing_fields': missing_fields}
        )
    
    validate_schedule_type(schedule_data['schedule_type'])
    validate_platforms(schedule_data['platforms'])
    validate_publish_date(schedule_data['publish_date'])
    
    if 'recurrence' in schedule_data:
        validate_recurrence(schedule_data['recurrence'])

def validate_schedule_type(schedule_type: str) -> None:
    """Validate schedule type."""
    valid_types = ['ONE_TIME', 'RECURRING', 'BATCH']
    if schedule_type not in valid_types:
        raise ScheduleValidationError(
            f"Invalid schedule type: {schedule_type}",
            {'valid_types': valid_types}
        )

def validate_platforms(platforms: List[str]) -> None:
    """Validate platform list."""
    valid_platforms = ['TWITTER', 'FACEBOOK', 'LINKEDIN', 'INSTAGRAM']
    invalid_platforms = [p for p in platforms if p not in valid_platforms]
    
    if invalid_platforms:
        raise ScheduleValidationError(
            f"Invalid platforms: {', '.join(invalid_platforms)}",
            {'valid_platforms': valid_platforms}
        )
    
    if not platforms:
        raise ScheduleValidationError(
            "At least one platform must be specified",
            {'valid_platforms': valid_platforms}
        )

def validate_publish_date(publish_date: datetime) -> None:
    """Validate publish date."""
    if not isinstance(publish_date, datetime):
        raise ScheduleValidationError(
            "Publish date must be a datetime object",
            {'type': type(publish_date).__name__}
        )
    
    if publish_date.tzinfo is None:
        raise ScheduleValidationError(
            "Publish date must be timezone-aware",
            {'date': str(publish_date)}
        )
    
    if publish_date < datetime.now(pytz.UTC):
        raise ScheduleValidationError(
            "Publish date must be in the future",
            {'date': str(publish_date)}
        )

def validate_recurrence(recurrence: Dict[str, Any]) -> None:
    """Validate recurrence settings."""
    required_fields = ['frequency', 'interval']
    missing_fields = [field for field in required_fields if field not in recurrence]
    
    if missing_fields:
        raise ScheduleValidationError(
            f"Missing required recurrence fields: {', '.join(missing_fields)}",
            {'missing_fields': missing_fields}
        )
    
    valid_frequencies = ['DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']
    if recurrence['frequency'] not in valid_frequencies:
        raise ScheduleValidationError(
            f"Invalid recurrence frequency: {recurrence['frequency']}",
            {'valid_frequencies': valid_frequencies}
        )
    
    if not isinstance(recurrence['interval'], int) or recurrence['interval'] < 1:
        raise ScheduleValidationError(
            "Recurrence interval must be a positive integer",
            {'interval': recurrence['interval']}
        )
    
    if 'end_date' in recurrence:
        if not isinstance(recurrence['end_date'], datetime):
            raise ScheduleValidationError(
                "End date must be a datetime object",
                {'type': type(recurrence['end_date']).__name__}
            )
        
        if recurrence['end_date'].tzinfo is None:
            raise ScheduleValidationError(
                "End date must be timezone-aware",
                {'date': str(recurrence['end_date'])}
            )

def validate_job_data(job_data: Dict[str, Any]) -> None:
    """Validate job data before creation."""
    required_fields = ['content_id', 'schedule_id', 'platform']
    missing_fields = [field for field in required_fields if field not in job_data]
    
    if missing_fields:
        raise ScheduleValidationError(
            f"Missing required job fields: {', '.join(missing_fields)}",
            {'missing_fields': missing_fields}
        )
    
    validate_platforms([job_data['platform']])

def validate_retry_settings(retry_settings: Optional[Dict[str, Any]]) -> None:
    """Validate retry settings."""
    if retry_settings is None:
        return
    
    if 'max_retries' in retry_settings:
        if not isinstance(retry_settings['max_retries'], int) or retry_settings['max_retries'] < 0:
            raise ScheduleValidationError(
                "Max retries must be a non-negative integer",
                {'max_retries': retry_settings['max_retries']}
            )
    
    if 'retry_delay' in retry_settings:
        if not isinstance(retry_settings['retry_delay'], (int, float)) or retry_settings['retry_delay'] < 0:
            raise ScheduleValidationError(
                "Retry delay must be a non-negative number",
                {'retry_delay': retry_settings['retry_delay']}
            )

def validate_notification_settings(notification_settings: Optional[Dict[str, Any]]) -> None:
    """Validate notification settings."""
    if notification_settings is None:
        return
    
    if 'channels' in notification_settings:
        valid_channels = ['EMAIL', 'SLACK', 'WEBHOOK']
        invalid_channels = [c for c in notification_settings['channels'] if c not in valid_channels]
        
        if invalid_channels:
            raise ScheduleValidationError(
                f"Invalid notification channels: {', '.join(invalid_channels)}",
                {'valid_channels': valid_channels}
            )
    
    if 'events' in notification_settings:
        valid_events = ['ON_SUCCESS', 'ON_FAILURE', 'ON_RETRY', 'ON_CANCELLATION']
        invalid_events = [e for e in notification_settings['events'] if e not in valid_events]
        
        if invalid_events:
            raise ScheduleValidationError(
                f"Invalid notification events: {', '.join(invalid_events)}",
                {'valid_events': valid_events}
            ) 