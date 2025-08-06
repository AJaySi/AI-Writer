from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import pytz
from dateutil import rrule
from .error_handling import ScheduleValidationError

def get_optimal_publish_time(
    platform: str,
    content_type: str,
    target_audience: Optional[Dict[str, Any]] = None
) -> datetime:
    """Calculate optimal publish time based on platform and content type."""
    now = datetime.now(pytz.UTC)
    
    # Default optimal times by platform and content type
    optimal_times = {
        'TWITTER': {
            'POST': {'hour': 12, 'minute': 0},  # Noon UTC
            'THREAD': {'hour': 15, 'minute': 0},  # 3 PM UTC
            'POLL': {'hour': 18, 'minute': 0},  # 6 PM UTC
        },
        'FACEBOOK': {
            'POST': {'hour': 15, 'minute': 0},  # 3 PM UTC
            'LIVE': {'hour': 19, 'minute': 0},  # 7 PM UTC
            'EVENT': {'hour': 10, 'minute': 0},  # 10 AM UTC
        },
        'LINKEDIN': {
            'POST': {'hour': 9, 'minute': 0},  # 9 AM UTC
            'ARTICLE': {'hour': 11, 'minute': 0},  # 11 AM UTC
            'POLL': {'hour': 14, 'minute': 0},  # 2 PM UTC
        },
        'INSTAGRAM': {
            'POST': {'hour': 17, 'minute': 0},  # 5 PM UTC
            'STORY': {'hour': 20, 'minute': 0},  # 8 PM UTC
            'REEL': {'hour': 21, 'minute': 0},  # 9 PM UTC
        }
    }
    
    if platform not in optimal_times:
        raise ScheduleValidationError(
            f"Unsupported platform: {platform}",
            {'supported_platforms': list(optimal_times.keys())}
        )
    
    if content_type not in optimal_times[platform]:
        raise ScheduleValidationError(
            f"Unsupported content type for {platform}: {content_type}",
            {'supported_types': list(optimal_times[platform].keys())}
        )
    
    optimal_time = optimal_times[platform][content_type]
    publish_time = now.replace(
        hour=optimal_time['hour'],
        minute=optimal_time['minute'],
        second=0,
        microsecond=0
    )
    
    # If the optimal time has passed for today, schedule for tomorrow
    if publish_time < now:
        publish_time += timedelta(days=1)
    
    return publish_time

def calculate_recurrence_dates(
    start_date: datetime,
    frequency: str,
    interval: int,
    end_date: Optional[datetime] = None,
    count: Optional[int] = None
) -> List[datetime]:
    """Calculate recurrence dates based on frequency and interval."""
    if not isinstance(start_date, datetime):
        raise ScheduleValidationError(
            "Start date must be a datetime object",
            {'type': type(start_date).__name__}
        )
    
    if start_date.tzinfo is None:
        raise ScheduleValidationError(
            "Start date must be timezone-aware",
            {'date': str(start_date)}
        )
    
    frequency_map = {
        'DAILY': rrule.DAILY,
        'WEEKLY': rrule.WEEKLY,
        'MONTHLY': rrule.MONTHLY,
        'YEARLY': rrule.YEARLY
    }
    
    if frequency not in frequency_map:
        raise ScheduleValidationError(
            f"Invalid frequency: {frequency}",
            {'valid_frequencies': list(frequency_map.keys())}
        )
    
    if not isinstance(interval, int) or interval < 1:
        raise ScheduleValidationError(
            "Interval must be a positive integer",
            {'interval': interval}
        )
    
    if end_date is not None and not isinstance(end_date, datetime):
        raise ScheduleValidationError(
            "End date must be a datetime object",
            {'type': type(end_date).__name__}
        )
    
    if end_date is not None and end_date.tzinfo is None:
        raise ScheduleValidationError(
            "End date must be timezone-aware",
            {'date': str(end_date)}
        )
    
    if count is not None and (not isinstance(count, int) or count < 1):
        raise ScheduleValidationError(
            "Count must be a positive integer",
            {'count': count}
        )
    
    rule = rrule.rrule(
        freq=frequency_map[frequency],
        interval=interval,
        dtstart=start_date,
        until=end_date,
        count=count
    )
    
    return list(rule)

def adjust_for_timezone(
    date: datetime,
    target_timezone: str
) -> datetime:
    """Adjust datetime to target timezone."""
    if not isinstance(date, datetime):
        raise ScheduleValidationError(
            "Date must be a datetime object",
            {'type': type(date).__name__}
        )
    
    if date.tzinfo is None:
        raise ScheduleValidationError(
            "Date must be timezone-aware",
            {'date': str(date)}
        )
    
    try:
        target_tz = pytz.timezone(target_timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        raise ScheduleValidationError(
            f"Invalid timezone: {target_timezone}",
            {'timezone': target_timezone}
        )
    
    return date.astimezone(target_tz)

def calculate_time_difference(
    date1: datetime,
    date2: datetime
) -> timedelta:
    """Calculate time difference between two dates."""
    if not isinstance(date1, datetime) or not isinstance(date2, datetime):
        raise ScheduleValidationError(
            "Both dates must be datetime objects",
            {
                'date1_type': type(date1).__name__,
                'date2_type': type(date2).__name__
            }
        )
    
    if date1.tzinfo is None or date2.tzinfo is None:
        raise ScheduleValidationError(
            "Both dates must be timezone-aware",
            {
                'date1': str(date1),
                'date2': str(date2)
            }
        )
    
    return date2 - date1

def format_date_for_display(
    date: datetime,
    format_str: str = "%Y-%m-%d %H:%M:%S %Z"
) -> str:
    """Format datetime for display."""
    if not isinstance(date, datetime):
        raise ScheduleValidationError(
            "Date must be a datetime object",
            {'type': type(date).__name__}
        )
    
    if date.tzinfo is None:
        raise ScheduleValidationError(
            "Date must be timezone-aware",
            {'date': str(date)}
        )
    
    return date.strftime(format_str) 