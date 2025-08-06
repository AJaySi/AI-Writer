from datetime import datetime, timedelta
from typing import Dict, List, Any
import calendar
import random

def calculate_publish_dates(
    topics: List[Dict[str, Any]],
    start_date: datetime,
    duration: str
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Calculate optimal publish dates for content topics.
    
    Args:
        topics: List of content topics to schedule
        start_date: When to start publishing
        duration: How long the calendar should span ('weekly', 'monthly', 'quarterly')
        
    Returns:
        Dictionary mapping dates to scheduled content
    """
    # Calculate end date based on duration
    end_date = _calculate_end_date(start_date, duration)
    
    # Get all dates in range
    dates = _get_dates_in_range(start_date, end_date)
    
    # Calculate optimal posting frequency
    frequency = _calculate_posting_frequency(len(topics), len(dates))
    
    # Schedule content
    schedule = _schedule_content(topics, dates, frequency)
    
    return schedule

def _calculate_end_date(start_date: datetime, duration: str) -> datetime:
    """Calculate end date based on duration."""
    if duration == 'weekly':
        return start_date + timedelta(days=7)
    elif duration == 'monthly':
        # Add one month
        if start_date.month == 12:
            return datetime(start_date.year + 1, 1, start_date.day)
        return datetime(start_date.year, start_date.month + 1, start_date.day)
    elif duration == 'quarterly':
        # Add three months
        new_month = start_date.month + 3
        new_year = start_date.year
        if new_month > 12:
            new_month -= 12
            new_year += 1
        return datetime(new_year, new_month, start_date.day)
    else:
        raise ValueError(f"Invalid duration: {duration}")

def _get_dates_in_range(
    start_date: datetime,
    end_date: datetime
) -> List[datetime]:
    """Get all dates in the given range."""
    dates = []
    current_date = start_date
    
    while current_date <= end_date:
        # Skip weekends
        if current_date.weekday() < 5:  # 0-4 are weekdays
            dates.append(current_date)
        current_date += timedelta(days=1)
    
    return dates

def _calculate_posting_frequency(
    num_topics: int,
    num_dates: int
) -> Dict[str, int]:
    """
    Calculate optimal posting frequency based on number of topics and dates.
    
    Returns:
        Dictionary with posting frequency for each content type
    """
    # Calculate base frequency
    base_frequency = num_dates / num_topics
    
    # Adjust for content types
    return {
        'blog_post': max(1, int(base_frequency * 0.4)),  # 40% of content
        'social_media': max(1, int(base_frequency * 0.3)),  # 30% of content
        'video': max(1, int(base_frequency * 0.2)),  # 20% of content
        'newsletter': max(1, int(base_frequency * 0.1))  # 10% of content
    }

def _schedule_content(
    topics: List[Dict[str, Any]],
    dates: List[datetime],
    frequency: Dict[str, int]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Schedule content topics across available dates.
    
    Args:
        topics: List of content topics to schedule
        dates: Available dates for scheduling
        frequency: Posting frequency for each content type
        
    Returns:
        Dictionary mapping dates to scheduled content
    """
    schedule = {}
    current_date_index = 0
    
    # Group topics by content type
    topics_by_type = _group_topics_by_type(topics)
    
    # Schedule each content type
    for content_type, type_topics in topics_by_type.items():
        type_frequency = frequency.get(content_type, 1)
        
        for topic in type_topics:
            # Find next available date
            while current_date_index < len(dates):
                date = dates[current_date_index]
                date_str = date.strftime('%Y-%m-%d')
                
                # Check if date is available
                if date_str not in schedule:
                    schedule[date_str] = []
                
                # Add topic to schedule
                schedule[date_str].append(topic)
                
                # Move to next date based on frequency
                current_date_index += type_frequency
                break
            
            # If we've used all dates, wrap around
            if current_date_index >= len(dates):
                current_date_index = 0
    
    return schedule

def _group_topics_by_type(
    topics: List[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:
    """Group topics by their content type."""
    grouped = {}
    
    for topic in topics:
        content_type = topic.get('content_type', 'blog_post')
        if content_type not in grouped:
            grouped[content_type] = []
        grouped[content_type].append(topic)
    
    return grouped

def get_optimal_posting_time(
    content_type: str,
    platform: str
) -> datetime.time:
    """
    Get optimal posting time for content type and platform.
    
    Args:
        content_type: Type of content
        platform: Target platform
        
    Returns:
        Optimal time to post
    """
    # Default optimal times (can be customized based on platform analytics)
    optimal_times = {
        'blog_post': {
            'website': datetime.time(9, 0),  # 9 AM
            'medium': datetime.time(10, 0)   # 10 AM
        },
        'social_media': {
            'facebook': datetime.time(15, 0),  # 3 PM
            'twitter': datetime.time(12, 0),   # 12 PM
            'linkedin': datetime.time(8, 0),   # 8 AM
            'instagram': datetime.time(19, 0)  # 7 PM
        },
        'video': {
            'youtube': datetime.time(14, 0)   # 2 PM
        },
        'newsletter': {
            'email': datetime.time(6, 0)      # 6 AM
        }
    }
    
    # Get optimal time for content type and platform
    content_times = optimal_times.get(content_type, {})
    optimal_time = content_times.get(platform)
    
    if optimal_time is None:
        # Default to 9 AM if no specific time is set
        optimal_time = datetime.time(9, 0)
    
    return optimal_time 