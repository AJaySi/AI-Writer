from datetime import datetime
from typing import List, Dict, Any

from ..core.calendar_manager import CalendarManager
from ..models.calendar import ContentType, Platform

def create_content_calendar(
    website_url: str,
    start_date: datetime,
    duration: str,
    platforms: List[str]
) -> Dict[str, Any]:
    """
    Example of creating a content calendar.
    
    Args:
        website_url: URL of the website to analyze
        start_date: When to start the calendar
        duration: How long the calendar should span
        platforms: List of platforms to create content for
        
    Returns:
        Dictionary containing the calendar data
    """
    # Initialize calendar manager
    calendar_manager = CalendarManager()
    
    # Create calendar
    calendar = calendar_manager.create_calendar(
        start_date=start_date,
        duration=duration,
        platforms=platforms,
        website_url=website_url
    )
    
    # Export calendar
    calendar_data = calendar_manager.export_calendar()
    
    return calendar_data

def main():
    """Example usage of the content calendar system."""
    # Example parameters
    website_url = "https://example.com"
    start_date = datetime.now()
    duration = "monthly"
    platforms = [
        Platform.WEBSITE.value,
        Platform.FACEBOOK.value,
        Platform.TWITTER.value,
        Platform.LINKEDIN.value
    ]
    
    try:
        # Create calendar
        calendar_data = create_content_calendar(
            website_url=website_url,
            start_date=start_date,
            duration=duration,
            platforms=platforms
        )
        
        # Print calendar summary
        print("\nContent Calendar Summary:")
        print(f"Duration: {calendar_data['duration']}")
        print(f"Platforms: {', '.join(calendar_data['platforms'])}")
        print("\nScheduled Content:")
        
        for date, items in calendar_data['schedule'].items():
            print(f"\n{date}:")
            for item in items:
                print(f"- {item['title']} ({item['content_type']})")
                print(f"  Platforms: {', '.join(item['platforms'])}")
                print(f"  Status: {item['status']}")
        
    except Exception as e:
        print(f"Error creating calendar: {str(e)}")

if __name__ == "__main__":
    main() 