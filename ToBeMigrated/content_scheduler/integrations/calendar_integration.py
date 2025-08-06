"""
Calendar integration for content scheduling.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import json

# Use unified database models
from lib.database.models import ContentItem, Schedule, ScheduleStatus, ContentType, Platform, get_session

logger = logging.getLogger(__name__)

@dataclass
class CalendarEvent:
    """Calendar event representation."""
    id: str
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    attendees: List[str] = None
    event_type: str = "content_schedule"
    metadata: Dict[str, Any] = None

class CalendarIntegration:
    """Integration with calendar systems for content scheduling."""
    
    def __init__(self, calendar_provider: str = "google"):
        """Initialize calendar integration.
        
        Args:
            calendar_provider: Calendar provider (google, outlook, etc.)
        """
        self.logger = logger
        self.session = get_session()
        self.calendar_provider = calendar_provider
        
        # Calendar provider configurations
        self.provider_configs = {
            'google': {
                'api_endpoint': 'https://www.googleapis.com/calendar/v3',
                'scopes': ['https://www.googleapis.com/auth/calendar'],
                'event_duration_minutes': 30
            },
            'outlook': {
                'api_endpoint': 'https://graph.microsoft.com/v1.0',
                'scopes': ['https://graph.microsoft.com/calendars.readwrite'],
                'event_duration_minutes': 30
            },
            'apple': {
                'api_endpoint': 'https://caldav.icloud.com',
                'scopes': ['calendar'],
                'event_duration_minutes': 30
            }
        }
        
        # Event templates for different content types
        self.event_templates = {
            ContentType.ARTICLE: {
                'title_prefix': '📝 Publish Article:',
                'description_template': 'Publish article "{title}" to {platforms}',
                'duration_minutes': 15
            },
            ContentType.VIDEO: {
                'title_prefix': '🎥 Publish Video:',
                'description_template': 'Publish video "{title}" to {platforms}',
                'duration_minutes': 30
            },
            ContentType.IMAGE: {
                'title_prefix': '📸 Publish Image:',
                'description_template': 'Publish image "{title}" to {platforms}',
                'duration_minutes': 10
            },
            ContentType.SOCIAL_POST: {
                'title_prefix': '📱 Social Post:',
                'description_template': 'Publish social post "{title}" to {platforms}',
                'duration_minutes': 5
            }
        }
    
    def sync_schedules_to_calendar(self, schedules: List[Schedule] = None) -> Dict[str, Any]:
        """Sync content schedules to calendar.
        
        Args:
            schedules: List of schedules to sync (if None, sync all pending schedules)
            
        Returns:
            Dictionary with sync results
        """
        try:
            if schedules is None:
                schedules = self.session.query(Schedule).filter(
                    Schedule.status == ScheduleStatus.PENDING
                ).all()
            
            sync_results = {
                'total_schedules': len(schedules),
                'synced_successfully': 0,
                'failed_syncs': 0,
                'errors': [],
                'created_events': []
            }
            
            for schedule in schedules:
                try:
                    # Get content item details
                    content_item = self.session.query(ContentItem).filter(
                        ContentItem.id == schedule.content_item_id
                    ).first()
                    
                    if not content_item:
                        sync_results['errors'].append(f"Content item not found for schedule {schedule.id}")
                        sync_results['failed_syncs'] += 1
                        continue
                    
                    # Create calendar event
                    event = self._create_calendar_event(schedule, content_item)
                    
                    # Sync to calendar provider
                    event_id = self._sync_event_to_provider(event)
                    
                    if event_id:
                        # Update schedule with calendar event ID
                        schedule.metadata = schedule.metadata or {}
                        schedule.metadata['calendar_event_id'] = event_id
                        self.session.commit()
                        
                        sync_results['synced_successfully'] += 1
                        sync_results['created_events'].append({
                            'schedule_id': schedule.id,
                            'event_id': event_id,
                            'title': event.title
                        })
                    else:
                        sync_results['failed_syncs'] += 1
                        sync_results['errors'].append(f"Failed to create calendar event for schedule {schedule.id}")
                
                except Exception as e:
                    self.logger.error(f"Error syncing schedule {schedule.id}: {str(e)}")
                    sync_results['failed_syncs'] += 1
                    sync_results['errors'].append(f"Schedule {schedule.id}: {str(e)}")
            
            return sync_results
            
        except Exception as e:
            self.logger.error(f"Error syncing schedules to calendar: {str(e)}")
            return {
                'total_schedules': 0,
                'synced_successfully': 0,
                'failed_syncs': 0,
                'errors': [f"Sync error: {str(e)}"],
                'created_events': []
            }
    
    def import_calendar_events(self, calendar_id: str = None, date_range: Tuple[datetime, datetime] = None) -> Dict[str, Any]:
        """Import events from calendar and suggest content schedules.
        
        Args:
            calendar_id: Calendar ID to import from
            date_range: Date range to import events from
            
        Returns:
            Dictionary with import results and suggestions
        """
        try:
            if date_range is None:
                start_date = datetime.now()
                end_date = start_date + timedelta(days=30)
                date_range = (start_date, end_date)
            
            # Get events from calendar provider
            events = self._get_events_from_provider(calendar_id, date_range)
            
            import_results = {
                'total_events': len(events),
                'content_suggestions': [],
                'scheduling_gaps': [],
                'optimal_times': []
            }
            
            # Analyze events for content scheduling opportunities
            for event in events:
                suggestions = self._analyze_event_for_content_opportunities(event)
                import_results['content_suggestions'].extend(suggestions)
            
            # Find scheduling gaps
            gaps = self._find_scheduling_gaps(events, date_range)
            import_results['scheduling_gaps'] = gaps
            
            # Suggest optimal posting times
            optimal_times = self._suggest_optimal_posting_times(events, date_range)
            import_results['optimal_times'] = optimal_times
            
            return import_results
            
        except Exception as e:
            self.logger.error(f"Error importing calendar events: {str(e)}")
            return {
                'total_events': 0,
                'content_suggestions': [],
                'scheduling_gaps': [],
                'optimal_times': [],
                'error': str(e)
            }
    
    def create_content_schedule_from_event(self, event: CalendarEvent, content_item_id: int) -> Optional[Schedule]:
        """Create a content schedule from a calendar event.
        
        Args:
            event: Calendar event
            content_item_id: ID of content item to schedule
            
        Returns:
            Created schedule or None if failed
        """
        try:
            # Get content item
            content_item = self.session.query(ContentItem).filter(
                ContentItem.id == content_item_id
            ).first()
            
            if not content_item:
                self.logger.error(f"Content item {content_item_id} not found")
                return None
            
            # Create schedule
            schedule = Schedule(
                content_item_id=content_item_id,
                scheduled_time=event.start_time,
                status=ScheduleStatus.PENDING,
                priority=5,  # Default priority
                metadata={
                    'calendar_event_id': event.id,
                    'created_from_calendar': True,
                    'original_event_title': event.title
                }
            )
            
            self.session.add(schedule)
            self.session.commit()
            
            self.logger.info(f"Created schedule {schedule.id} from calendar event {event.id}")
            return schedule
            
        except Exception as e:
            self.logger.error(f"Error creating schedule from event: {str(e)}")
            self.session.rollback()
            return None
    
    def update_calendar_event_from_schedule(self, schedule: Schedule) -> bool:
        """Update calendar event when schedule changes.
        
        Args:
            schedule: Updated schedule
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if schedule has associated calendar event
            if not schedule.metadata or 'calendar_event_id' not in schedule.metadata:
                return False
            
            event_id = schedule.metadata['calendar_event_id']
            
            # Get content item
            content_item = self.session.query(ContentItem).filter(
                ContentItem.id == schedule.content_item_id
            ).first()
            
            if not content_item:
                return False
            
            # Create updated event
            updated_event = self._create_calendar_event(schedule, content_item)
            updated_event.id = event_id
            
            # Update event in calendar provider
            success = self._update_event_in_provider(updated_event)
            
            if success:
                self.logger.info(f"Updated calendar event {event_id} for schedule {schedule.id}")
            else:
                self.logger.error(f"Failed to update calendar event {event_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error updating calendar event: {str(e)}")
            return False
    
    def delete_calendar_event_from_schedule(self, schedule: Schedule) -> bool:
        """Delete calendar event when schedule is deleted.
        
        Args:
            schedule: Schedule being deleted
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if schedule has associated calendar event
            if not schedule.metadata or 'calendar_event_id' not in schedule.metadata:
                return True  # No event to delete
            
            event_id = schedule.metadata['calendar_event_id']
            
            # Delete event from calendar provider
            success = self._delete_event_from_provider(event_id)
            
            if success:
                self.logger.info(f"Deleted calendar event {event_id} for schedule {schedule.id}")
            else:
                self.logger.error(f"Failed to delete calendar event {event_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error deleting calendar event: {str(e)}")
            return False
    
    def get_calendar_view(self, date_range: Tuple[datetime, datetime] = None) -> Dict[str, Any]:
        """Get calendar view of scheduled content.
        
        Args:
            date_range: Date range for calendar view
            
        Returns:
            Dictionary with calendar view data
        """
        try:
            if date_range is None:
                start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = start_date + timedelta(days=30)
                date_range = (start_date, end_date)
            
            # Get schedules in date range
            schedules = self.session.query(Schedule).filter(
                Schedule.scheduled_time >= date_range[0],
                Schedule.scheduled_time <= date_range[1]
            ).all()
            
            calendar_events = []
            for schedule in schedules:
                content_item = self.session.query(ContentItem).filter(
                    ContentItem.id == schedule.content_item_id
                ).first()
                
                if content_item:
                    event = self._create_calendar_event(schedule, content_item)
                    calendar_events.append({
                        'id': str(schedule.id),
                        'title': event.title,
                        'description': event.description,
                        'start': event.start_time.isoformat(),
                        'end': event.end_time.isoformat(),
                        'status': schedule.status.value,
                        'priority': schedule.priority,
                        'content_type': content_item.content_type.value if content_item.content_type else 'unknown',
                        'platforms': schedule.platforms or []
                    })
            
            # Group events by day
            events_by_day = {}
            for event in calendar_events:
                day = datetime.fromisoformat(event['start']).date()
                if day not in events_by_day:
                    events_by_day[day] = []
                events_by_day[day].append(event)
            
            return {
                'date_range': {
                    'start': date_range[0].isoformat(),
                    'end': date_range[1].isoformat()
                },
                'total_events': len(calendar_events),
                'events': calendar_events,
                'events_by_day': {day.isoformat(): events for day, events in events_by_day.items()},
                'summary': self._generate_calendar_summary(calendar_events)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting calendar view: {str(e)}")
            return {
                'date_range': None,
                'total_events': 0,
                'events': [],
                'events_by_day': {},
                'summary': {},
                'error': str(e)
            }
    
    def _create_calendar_event(self, schedule: Schedule, content_item: ContentItem) -> CalendarEvent:
        """Create calendar event from schedule and content item."""
        try:
            # Get event template based on content type
            template = self.event_templates.get(
                content_item.content_type,
                self.event_templates[ContentType.SOCIAL_POST]
            )
            
            # Create event title
            title = f"{template['title_prefix']} {content_item.title}"
            
            # Create event description
            platforms_str = ', '.join(schedule.platforms) if schedule.platforms else 'Default platforms'
            description = template['description_template'].format(
                title=content_item.title,
                platforms=platforms_str
            )
            
            # Add content summary if available
            if content_item.summary:
                description += f"\n\nSummary: {content_item.summary}"
            
            # Calculate end time
            duration = timedelta(minutes=template['duration_minutes'])
            end_time = schedule.scheduled_time + duration
            
            # Create metadata
            metadata = {
                'schedule_id': schedule.id,
                'content_item_id': content_item.id,
                'content_type': content_item.content_type.value if content_item.content_type else 'unknown',
                'platforms': schedule.platforms or [],
                'priority': schedule.priority,
                'status': schedule.status.value
            }
            
            return CalendarEvent(
                id=f"schedule_{schedule.id}",
                title=title,
                description=description,
                start_time=schedule.scheduled_time,
                end_time=end_time,
                metadata=metadata
            )
            
        except Exception as e:
            self.logger.error(f"Error creating calendar event: {str(e)}")
            # Return a basic event as fallback
            return CalendarEvent(
                id=f"schedule_{schedule.id}",
                title=f"Content Schedule: {content_item.title}",
                description="Content publishing schedule",
                start_time=schedule.scheduled_time,
                end_time=schedule.scheduled_time + timedelta(minutes=30)
            )
    
    def _sync_event_to_provider(self, event: CalendarEvent) -> Optional[str]:
        """Sync event to calendar provider (mock implementation)."""
        try:
            # This is a mock implementation
            # In a real system, you would integrate with actual calendar APIs
            
            self.logger.info(f"Syncing event to {self.calendar_provider}: {event.title}")
            
            # Simulate API call
            event_id = f"{self.calendar_provider}_{event.id}_{int(datetime.now().timestamp())}"
            
            return event_id
            
        except Exception as e:
            self.logger.error(f"Error syncing event to provider: {str(e)}")
            return None
    
    def _get_events_from_provider(self, calendar_id: str, date_range: Tuple[datetime, datetime]) -> List[CalendarEvent]:
        """Get events from calendar provider (mock implementation)."""
        try:
            # This is a mock implementation
            # In a real system, you would fetch from actual calendar APIs
            
            self.logger.info(f"Fetching events from {self.calendar_provider} calendar {calendar_id}")
            
            # Return empty list for mock
            return []
            
        except Exception as e:
            self.logger.error(f"Error fetching events from provider: {str(e)}")
            return []
    
    def _update_event_in_provider(self, event: CalendarEvent) -> bool:
        """Update event in calendar provider (mock implementation)."""
        try:
            # This is a mock implementation
            self.logger.info(f"Updating event in {self.calendar_provider}: {event.id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating event in provider: {str(e)}")
            return False
    
    def _delete_event_from_provider(self, event_id: str) -> bool:
        """Delete event from calendar provider (mock implementation)."""
        try:
            # This is a mock implementation
            self.logger.info(f"Deleting event from {self.calendar_provider}: {event_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting event from provider: {str(e)}")
            return False
    
    def _analyze_event_for_content_opportunities(self, event: CalendarEvent) -> List[Dict[str, Any]]:
        """Analyze calendar event for content opportunities."""
        suggestions = []
        
        try:
            # Look for keywords that suggest content opportunities
            content_keywords = ['meeting', 'conference', 'launch', 'announcement', 'webinar', 'presentation']
            
            event_text = f"{event.title} {event.description}".lower()
            
            for keyword in content_keywords:
                if keyword in event_text:
                    suggestions.append({
                        'type': 'content_opportunity',
                        'keyword': keyword,
                        'suggested_time': event.end_time,  # Suggest posting after the event
                        'content_type': self._suggest_content_type_for_keyword(keyword),
                        'description': f"Consider creating content about the {keyword}"
                    })
            
        except Exception as e:
            self.logger.error(f"Error analyzing event for opportunities: {str(e)}")
        
        return suggestions
    
    def _find_scheduling_gaps(self, events: List[CalendarEvent], date_range: Tuple[datetime, datetime]) -> List[Dict[str, Any]]:
        """Find gaps in schedule that could be used for content posting."""
        gaps = []
        
        try:
            # Sort events by start time
            sorted_events = sorted(events, key=lambda x: x.start_time)
            
            current_time = date_range[0]
            
            for event in sorted_events:
                # Check if there's a gap before this event
                if event.start_time > current_time + timedelta(hours=2):
                    gaps.append({
                        'start': current_time.isoformat(),
                        'end': event.start_time.isoformat(),
                        'duration_hours': (event.start_time - current_time).total_seconds() / 3600,
                        'suggested_use': 'Content posting opportunity'
                    })
                
                current_time = max(current_time, event.end_time)
            
            # Check for gap after last event
            if current_time < date_range[1] - timedelta(hours=2):
                gaps.append({
                    'start': current_time.isoformat(),
                    'end': date_range[1].isoformat(),
                    'duration_hours': (date_range[1] - current_time).total_seconds() / 3600,
                    'suggested_use': 'Content posting opportunity'
                })
            
        except Exception as e:
            self.logger.error(f"Error finding scheduling gaps: {str(e)}")
        
        return gaps
    
    def _suggest_optimal_posting_times(self, events: List[CalendarEvent], date_range: Tuple[datetime, datetime]) -> List[Dict[str, Any]]:
        """Suggest optimal times for content posting based on calendar."""
        optimal_times = []
        
        try:
            # Define optimal posting hours (9 AM, 1 PM, 5 PM)
            optimal_hours = [9, 13, 17]
            
            current_date = date_range[0].date()
            end_date = date_range[1].date()
            
            while current_date <= end_date:
                for hour in optimal_hours:
                    suggested_time = datetime.combine(current_date, datetime.min.time().replace(hour=hour))
                    
                    # Check if this time conflicts with any events
                    conflicts = any(
                        event.start_time <= suggested_time <= event.end_time
                        for event in events
                    )
                    
                    if not conflicts:
                        optimal_times.append({
                            'time': suggested_time.isoformat(),
                            'reason': f'Optimal posting time ({hour}:00) with no calendar conflicts',
                            'confidence': 0.8
                        })
                
                current_date += timedelta(days=1)
            
        except Exception as e:
            self.logger.error(f"Error suggesting optimal posting times: {str(e)}")
        
        return optimal_times
    
    def _suggest_content_type_for_keyword(self, keyword: str) -> str:
        """Suggest content type based on keyword."""
        keyword_mapping = {
            'meeting': 'social_post',
            'conference': 'article',
            'launch': 'video',
            'announcement': 'social_post',
            'webinar': 'video',
            'presentation': 'article'
        }
        
        return keyword_mapping.get(keyword, 'social_post')
    
    def _generate_calendar_summary(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics for calendar events."""
        try:
            if not events:
                return {}
            
            # Count by status
            status_counts = {}
            for event in events:
                status = event.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Count by content type
            type_counts = {}
            for event in events:
                content_type = event.get('content_type', 'unknown')
                type_counts[content_type] = type_counts.get(content_type, 0) + 1
            
            # Count by day
            daily_counts = {}
            for event in events:
                day = datetime.fromisoformat(event['start']).date().isoformat()
                daily_counts[day] = daily_counts.get(day, 0) + 1
            
            return {
                'total_events': len(events),
                'by_status': status_counts,
                'by_content_type': type_counts,
                'by_day': daily_counts,
                'busiest_day': max(daily_counts.items(), key=lambda x: x[1]) if daily_counts else None
            }
            
        except Exception as e:
            self.logger.error(f"Error generating calendar summary: {str(e)}")
            return {} 