"""
Schedule validation system for content scheduling.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import re

# Use unified database models
from lib.database.models import ContentItem, Schedule, ScheduleStatus, ContentType, Platform, get_session

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Result of schedule validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    confidence: float

class ScheduleValidator:
    """Validate content schedules for compliance and optimization."""
    
    def __init__(self):
        """Initialize the schedule validator."""
        self.logger = logger
        self.session = get_session()
        
        # Platform-specific validation rules
        self.platform_rules = {
            Platform.TWITTER: {
                'max_text_length': 280,
                'max_images': 4,
                'max_videos': 1,
                'allowed_formats': ['jpg', 'png', 'gif', 'mp4'],
                'max_file_size_mb': 5,
                'posting_frequency_limit': {'per_hour': 10, 'per_day': 100}
            },
            Platform.FACEBOOK: {
                'max_text_length': 63206,
                'max_images': 10,
                'max_videos': 1,
                'allowed_formats': ['jpg', 'png', 'gif', 'mp4', 'mov'],
                'max_file_size_mb': 100,
                'posting_frequency_limit': {'per_hour': 5, 'per_day': 25}
            },
            Platform.LINKEDIN: {
                'max_text_length': 3000,
                'max_images': 9,
                'max_videos': 1,
                'allowed_formats': ['jpg', 'png', 'gif', 'mp4'],
                'max_file_size_mb': 200,
                'posting_frequency_limit': {'per_hour': 3, 'per_day': 20}
            },
            Platform.INSTAGRAM: {
                'max_text_length': 2200,
                'max_images': 10,
                'max_videos': 1,
                'allowed_formats': ['jpg', 'png', 'mp4'],
                'max_file_size_mb': 100,
                'posting_frequency_limit': {'per_hour': 2, 'per_day': 10}
            }
        }
        
        # Content type validation rules
        self.content_type_rules = {
            ContentType.ARTICLE: {
                'min_title_length': 10,
                'max_title_length': 200,
                'min_content_length': 100,
                'required_fields': ['title', 'content', 'summary']
            },
            ContentType.VIDEO: {
                'min_duration_sec': 5,
                'max_duration_sec': 3600,
                'required_fields': ['title', 'description'],
                'recommended_formats': ['mp4', 'mov']
            },
            ContentType.IMAGE: {
                'min_width': 400,
                'min_height': 400,
                'max_width': 4096,
                'max_height': 4096,
                'required_fields': ['title', 'alt_text']
            },
            ContentType.SOCIAL_POST: {
                'min_length': 10,
                'max_length': 500,
                'required_fields': ['content']
            }
        }
    
    def validate_schedule(self, schedule: Schedule) -> ValidationResult:
        """Validate a single schedule.
        
        Args:
            schedule: Schedule to validate
            
        Returns:
            ValidationResult with validation details
        """
        try:
            errors = []
            warnings = []
            suggestions = []
            
            # Get content item details
            content_item = self.session.query(ContentItem).filter(
                ContentItem.id == schedule.content_item_id
            ).first()
            
            if not content_item:
                return ValidationResult(
                    is_valid=False,
                    errors=["Content item not found"],
                    warnings=[],
                    suggestions=[],
                    confidence=0.0
                )
            
            # Validate basic schedule properties
            basic_validation = self._validate_basic_properties(schedule)
            errors.extend(basic_validation['errors'])
            warnings.extend(basic_validation['warnings'])
            suggestions.extend(basic_validation['suggestions'])
            
            # Validate content properties
            content_validation = self._validate_content_properties(content_item)
            errors.extend(content_validation['errors'])
            warnings.extend(content_validation['warnings'])
            suggestions.extend(content_validation['suggestions'])
            
            # Validate timing
            timing_validation = self._validate_timing(schedule)
            errors.extend(timing_validation['errors'])
            warnings.extend(timing_validation['warnings'])
            suggestions.extend(timing_validation['suggestions'])
            
            # Validate conflicts
            conflict_validation = self._validate_conflicts(schedule)
            errors.extend(conflict_validation['errors'])
            warnings.extend(conflict_validation['warnings'])
            suggestions.extend(conflict_validation['suggestions'])
            
            # Calculate confidence
            confidence = self._calculate_validation_confidence(errors, warnings)
            
            return ValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                confidence=confidence
            )
            
        except Exception as e:
            self.logger.error(f"Error validating schedule: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation error: {str(e)}"],
                warnings=[],
                suggestions=[],
                confidence=0.0
            )
    
    def validate_multiple_schedules(self, schedules: List[Schedule]) -> Dict[str, ValidationResult]:
        """Validate multiple schedules and check for cross-schedule issues.
        
        Args:
            schedules: List of schedules to validate
            
        Returns:
            Dictionary mapping schedule IDs to validation results
        """
        try:
            results = {}
            
            # Validate individual schedules
            for schedule in schedules:
                results[str(schedule.id)] = self.validate_schedule(schedule)
            
            # Check for cross-schedule conflicts
            cross_validation = self._validate_cross_schedule_conflicts(schedules)
            
            # Add cross-validation issues to individual results
            for schedule_id, issues in cross_validation.items():
                if schedule_id in results:
                    results[schedule_id].warnings.extend(issues.get('warnings', []))
                    results[schedule_id].suggestions.extend(issues.get('suggestions', []))
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating multiple schedules: {str(e)}")
            return {}
    
    def _validate_basic_properties(self, schedule: Schedule) -> Dict[str, List[str]]:
        """Validate basic schedule properties."""
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # Check required fields
            if not schedule.content_item_id:
                errors.append("Content item ID is required")
            
            if not schedule.scheduled_time:
                errors.append("Scheduled time is required")
            
            if not schedule.status:
                errors.append("Schedule status is required")
            
            # Check priority range
            if schedule.priority < 1 or schedule.priority > 10:
                warnings.append(f"Priority {schedule.priority} is outside recommended range (1-10)")
            
            # Check if schedule is in the past
            if schedule.scheduled_time < datetime.now():
                if schedule.status == ScheduleStatus.PENDING:
                    errors.append("Cannot schedule content in the past")
                else:
                    warnings.append("Schedule time is in the past")
            
            # Check if schedule is too far in the future
            max_future_days = 365  # 1 year
            if schedule.scheduled_time > datetime.now() + timedelta(days=max_future_days):
                warnings.append(f"Schedule is more than {max_future_days} days in the future")
                suggestions.append("Consider scheduling closer to the current date for better relevance")
            
            # Validate recurrence pattern
            if schedule.recurrence:
                recurrence_validation = self._validate_recurrence_pattern(schedule.recurrence)
                errors.extend(recurrence_validation['errors'])
                warnings.extend(recurrence_validation['warnings'])
                suggestions.extend(recurrence_validation['suggestions'])
            
        except Exception as e:
            self.logger.error(f"Error validating basic properties: {str(e)}")
            errors.append(f"Basic validation error: {str(e)}")
        
        return {'errors': errors, 'warnings': warnings, 'suggestions': suggestions}
    
    def _validate_content_properties(self, content_item: ContentItem) -> Dict[str, List[str]]:
        """Validate content item properties."""
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # Check required fields
            if not content_item.title or len(content_item.title.strip()) == 0:
                errors.append("Content title is required")
            
            if not content_item.content or len(content_item.content.strip()) == 0:
                errors.append("Content body is required")
            
            # Validate based on content type
            if content_item.content_type:
                type_rules = self.content_type_rules.get(content_item.content_type)
                if type_rules:
                    type_validation = self._validate_content_type_rules(content_item, type_rules)
                    errors.extend(type_validation['errors'])
                    warnings.extend(type_validation['warnings'])
                    suggestions.extend(type_validation['suggestions'])
            
            # Check for potentially problematic content
            content_check = self._check_content_quality(content_item)
            warnings.extend(content_check['warnings'])
            suggestions.extend(content_check['suggestions'])
            
        except Exception as e:
            self.logger.error(f"Error validating content properties: {str(e)}")
            errors.append(f"Content validation error: {str(e)}")
        
        return {'errors': errors, 'warnings': warnings, 'suggestions': suggestions}
    
    def _validate_timing(self, schedule: Schedule) -> Dict[str, List[str]]:
        """Validate schedule timing."""
        errors = []
        warnings = []
        suggestions = []
        
        try:
            scheduled_time = schedule.scheduled_time
            
            # Check if it's a reasonable time to post
            hour = scheduled_time.hour
            day_of_week = scheduled_time.weekday()  # 0 = Monday, 6 = Sunday
            
            # Check for very early or very late hours
            if hour < 6 or hour > 23:
                warnings.append(f"Scheduled for {hour}:00 - consider posting during peak hours (6 AM - 11 PM)")
                suggestions.append("Peak engagement typically occurs between 9 AM and 9 PM")
            
            # Check for weekend posting (depending on content type)
            content_item = self.session.query(ContentItem).filter(
                ContentItem.id == schedule.content_item_id
            ).first()
            
            if content_item and content_item.content_type == ContentType.ARTICLE:
                if day_of_week >= 5:  # Weekend
                    warnings.append("Business content typically performs better on weekdays")
                    suggestions.append("Consider rescheduling to Monday-Friday for better engagement")
            
            # Check for holidays or special dates (simplified)
            if self._is_holiday(scheduled_time.date()):
                warnings.append("Scheduled for a holiday - engagement may be lower")
                suggestions.append("Consider rescheduling to avoid holidays for better reach")
            
            # Check frequency limits
            frequency_check = self._check_posting_frequency(schedule)
            warnings.extend(frequency_check['warnings'])
            suggestions.extend(frequency_check['suggestions'])
            
        except Exception as e:
            self.logger.error(f"Error validating timing: {str(e)}")
            errors.append(f"Timing validation error: {str(e)}")
        
        return {'errors': errors, 'warnings': warnings, 'suggestions': suggestions}
    
    def _validate_conflicts(self, schedule: Schedule) -> Dict[str, List[str]]:
        """Validate for scheduling conflicts."""
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # Check for nearby schedules
            time_window = timedelta(minutes=30)
            nearby_schedules = self.session.query(Schedule).filter(
                Schedule.id != schedule.id,
                Schedule.scheduled_time.between(
                    schedule.scheduled_time - time_window,
                    schedule.scheduled_time + time_window
                )
            ).all()
            
            if nearby_schedules:
                warnings.append(f"Found {len(nearby_schedules)} other schedule(s) within 30 minutes")
                suggestions.append("Consider spacing schedules at least 30 minutes apart for better visibility")
            
            # Check for same-day content overload
            same_day_schedules = self.session.query(Schedule).filter(
                Schedule.id != schedule.id,
                Schedule.scheduled_time >= schedule.scheduled_time.replace(hour=0, minute=0, second=0),
                Schedule.scheduled_time < schedule.scheduled_time.replace(hour=0, minute=0, second=0) + timedelta(days=1)
            ).all()
            
            if len(same_day_schedules) > 5:
                warnings.append(f"Found {len(same_day_schedules)} other schedules on the same day")
                suggestions.append("Consider distributing content across multiple days to avoid overwhelming your audience")
            
        except Exception as e:
            self.logger.error(f"Error validating conflicts: {str(e)}")
            errors.append(f"Conflict validation error: {str(e)}")
        
        return {'errors': errors, 'warnings': warnings, 'suggestions': suggestions}
    
    def _validate_recurrence_pattern(self, recurrence: str) -> Dict[str, List[str]]:
        """Validate recurrence pattern."""
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # Define valid recurrence patterns
            valid_patterns = [
                'daily', 'weekly', 'monthly', 'yearly',
                'weekdays', 'weekends',
                'every 2 days', 'every 3 days', 'every 7 days',
                'every 2 weeks', 'every 2 months'
            ]
            
            if recurrence.lower() not in valid_patterns:
                # Check if it's a cron-like pattern
                if not self._is_valid_cron_pattern(recurrence):
                    errors.append(f"Invalid recurrence pattern: {recurrence}")
                    suggestions.append(f"Valid patterns include: {', '.join(valid_patterns[:5])}")
            
            # Check for overly frequent recurrence
            if 'hour' in recurrence.lower():
                warnings.append("Hourly recurrence may overwhelm your audience")
                suggestions.append("Consider daily or weekly recurrence for better engagement")
            
        except Exception as e:
            self.logger.error(f"Error validating recurrence: {str(e)}")
            errors.append(f"Recurrence validation error: {str(e)}")
        
        return {'errors': errors, 'warnings': warnings, 'suggestions': suggestions}
    
    def _validate_content_type_rules(self, content_item: ContentItem, rules: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate content against type-specific rules."""
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # Check title length
            if 'min_title_length' in rules and len(content_item.title) < rules['min_title_length']:
                errors.append(f"Title too short (minimum {rules['min_title_length']} characters)")
            
            if 'max_title_length' in rules and len(content_item.title) > rules['max_title_length']:
                errors.append(f"Title too long (maximum {rules['max_title_length']} characters)")
            
            # Check content length
            if 'min_content_length' in rules and len(content_item.content) < rules['min_content_length']:
                errors.append(f"Content too short (minimum {rules['min_content_length']} characters)")
            
            if 'max_length' in rules and len(content_item.content) > rules['max_length']:
                errors.append(f"Content too long (maximum {rules['max_length']} characters)")
            
            # Check required fields
            if 'required_fields' in rules:
                for field in rules['required_fields']:
                    if not hasattr(content_item, field) or not getattr(content_item, field):
                        errors.append(f"Required field missing: {field}")
            
        except Exception as e:
            self.logger.error(f"Error validating content type rules: {str(e)}")
            errors.append(f"Content type validation error: {str(e)}")
        
        return {'errors': errors, 'warnings': warnings, 'suggestions': suggestions}
    
    def _check_content_quality(self, content_item: ContentItem) -> Dict[str, List[str]]:
        """Check content quality and provide suggestions."""
        warnings = []
        suggestions = []
        
        try:
            content = content_item.content
            title = content_item.title
            
            # Check for excessive capitalization
            if title and title.isupper():
                warnings.append("Title is in all caps")
                suggestions.append("Consider using proper capitalization for better readability")
            
            # Check for excessive punctuation
            if content and content.count('!') > 3:
                warnings.append("Excessive exclamation marks detected")
                suggestions.append("Reduce exclamation marks for more professional tone")
            
            # Check for spelling/grammar (simplified)
            if content:
                # Simple checks for common issues
                if '  ' in content:  # Double spaces
                    suggestions.append("Remove extra spaces for cleaner formatting")
                
                if content.count('?') > 5:
                    warnings.append("Many question marks detected")
                    suggestions.append("Consider reducing questions for clearer messaging")
            
            # Check for hashtag usage
            hashtag_count = len(re.findall(r'#\w+', content)) if content else 0
            if hashtag_count > 10:
                warnings.append(f"High number of hashtags ({hashtag_count})")
                suggestions.append("Consider using 3-5 relevant hashtags for optimal reach")
            
            # Check for URL presence
            url_count = len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)) if content else 0
            if url_count > 2:
                warnings.append(f"Multiple URLs detected ({url_count})")
                suggestions.append("Consider limiting to 1-2 URLs to avoid appearing spammy")
            
        except Exception as e:
            self.logger.error(f"Error checking content quality: {str(e)}")
        
        return {'warnings': warnings, 'suggestions': suggestions}
    
    def _check_posting_frequency(self, schedule: Schedule) -> Dict[str, List[str]]:
        """Check posting frequency limits."""
        warnings = []
        suggestions = []
        
        try:
            # Check hourly frequency
            hour_start = schedule.scheduled_time.replace(minute=0, second=0, microsecond=0)
            hour_end = hour_start + timedelta(hours=1)
            
            hourly_schedules = self.session.query(Schedule).filter(
                Schedule.scheduled_time >= hour_start,
                Schedule.scheduled_time < hour_end
            ).count()
            
            if hourly_schedules > 3:
                warnings.append(f"High posting frequency: {hourly_schedules} posts in the same hour")
                suggestions.append("Consider spacing posts throughout the day for better engagement")
            
            # Check daily frequency
            day_start = schedule.scheduled_time.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            daily_schedules = self.session.query(Schedule).filter(
                Schedule.scheduled_time >= day_start,
                Schedule.scheduled_time < day_end
            ).count()
            
            if daily_schedules > 10:
                warnings.append(f"High daily posting frequency: {daily_schedules} posts")
                suggestions.append("Consider reducing daily posts to 3-5 for optimal audience engagement")
            
        except Exception as e:
            self.logger.error(f"Error checking posting frequency: {str(e)}")
        
        return {'warnings': warnings, 'suggestions': suggestions}
    
    def _validate_cross_schedule_conflicts(self, schedules: List[Schedule]) -> Dict[str, Dict[str, List[str]]]:
        """Validate conflicts across multiple schedules."""
        conflicts = {}
        
        try:
            # Sort schedules by time
            sorted_schedules = sorted(schedules, key=lambda x: x.scheduled_time)
            
            for i, schedule in enumerate(sorted_schedules):
                schedule_id = str(schedule.id)
                conflicts[schedule_id] = {'warnings': [], 'suggestions': []}
                
                # Check with subsequent schedules
                for j in range(i + 1, len(sorted_schedules)):
                    other_schedule = sorted_schedules[j]
                    time_diff = other_schedule.scheduled_time - schedule.scheduled_time
                    
                    # Check if schedules are too close
                    if time_diff < timedelta(minutes=15):
                        conflicts[schedule_id]['warnings'].append(
                            f"Schedule conflicts with another schedule {time_diff.total_seconds() / 60:.0f} minutes later"
                        )
                        conflicts[schedule_id]['suggestions'].append(
                            "Consider spacing schedules at least 15 minutes apart"
                        )
                    
                    # Stop checking if schedules are more than 2 hours apart
                    if time_diff > timedelta(hours=2):
                        break
            
        except Exception as e:
            self.logger.error(f"Error validating cross-schedule conflicts: {str(e)}")
        
        return conflicts
    
    def _calculate_validation_confidence(self, errors: List[str], warnings: List[str]) -> float:
        """Calculate confidence in validation results."""
        try:
            # Start with full confidence
            confidence = 1.0
            
            # Reduce confidence based on errors and warnings
            confidence -= len(errors) * 0.2  # Each error reduces confidence by 20%
            confidence -= len(warnings) * 0.05  # Each warning reduces confidence by 5%
            
            # Ensure confidence is between 0 and 1
            return max(0.0, min(1.0, confidence))
            
        except Exception as e:
            self.logger.error(f"Error calculating validation confidence: {str(e)}")
            return 0.0
    
    def _is_holiday(self, date) -> bool:
        """Check if a date is a holiday (simplified implementation)."""
        try:
            # This is a simplified implementation
            # In a real system, you would use a proper holiday library
            
            # Check for some common holidays
            month = date.month
            day = date.day
            
            # New Year's Day
            if month == 1 and day == 1:
                return True
            
            # Christmas
            if month == 12 and day == 25:
                return True
            
            # Independence Day (US)
            if month == 7 and day == 4:
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking holiday: {str(e)}")
            return False
    
    def _is_valid_cron_pattern(self, pattern: str) -> bool:
        """Check if a string is a valid cron pattern (simplified)."""
        try:
            # This is a very simplified cron validation
            # A proper implementation would use a cron parsing library
            
            parts = pattern.split()
            if len(parts) != 5:
                return False
            
            # Basic validation for each part
            for part in parts:
                if not (part.isdigit() or part == '*' or '/' in part or '-' in part or ',' in part):
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating cron pattern: {str(e)}")
            return False 