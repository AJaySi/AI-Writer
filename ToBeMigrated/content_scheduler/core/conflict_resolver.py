"""
Conflict resolution system for content scheduling.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# Use unified database models
from lib.database.models import ContentItem, Schedule, ScheduleStatus

logger = logging.getLogger(__name__)

@dataclass
class ConflictInfo:
    """Information about a scheduling conflict."""
    schedule_1: Schedule
    schedule_2: Schedule
    conflict_type: str
    severity: str
    description: str
    suggested_resolution: str

class ConflictResolver:
    """Resolve scheduling conflicts automatically."""
    
    def __init__(self):
        """Initialize the conflict resolver."""
        self.logger = logger
        self.resolution_strategies = {
            'time_overlap': self._resolve_time_overlap,
            'platform_conflict': self._resolve_platform_conflict,
            'resource_conflict': self._resolve_resource_conflict,
            'priority_conflict': self._resolve_priority_conflict
        }
    
    def detect_conflicts(self, schedules: List[Schedule]) -> List[ConflictInfo]:
        """Detect conflicts between schedules.
        
        Args:
            schedules: List of Schedule objects to check
            
        Returns:
            List of detected conflicts
        """
        try:
            conflicts = []
            
            # Sort schedules by time
            sorted_schedules = sorted(schedules, key=lambda x: x.scheduled_time)
            
            for i in range(len(sorted_schedules)):
                for j in range(i + 1, len(sorted_schedules)):
                    schedule_1 = sorted_schedules[i]
                    schedule_2 = sorted_schedules[j]
                    
                    # Check for time overlap conflicts
                    time_conflicts = self._check_time_overlap(schedule_1, schedule_2)
                    conflicts.extend(time_conflicts)
                    
                    # Check for platform conflicts
                    platform_conflicts = self._check_platform_conflict(schedule_1, schedule_2)
                    conflicts.extend(platform_conflicts)
                    
                    # Check for priority conflicts
                    priority_conflicts = self._check_priority_conflict(schedule_1, schedule_2)
                    conflicts.extend(priority_conflicts)
            
            return conflicts
            
        except Exception as e:
            self.logger.error(f"Error detecting conflicts: {str(e)}")
            return []
    
    def _check_time_overlap(self, schedule_1: Schedule, schedule_2: Schedule) -> List[ConflictInfo]:
        """Check for time overlap conflicts."""
        conflicts = []
        
        try:
            # Assume each schedule takes 1 hour (can be made configurable)
            duration = timedelta(hours=1)
            
            end_1 = schedule_1.scheduled_time + duration
            end_2 = schedule_2.scheduled_time + duration
            
            # Check for overlap
            if (schedule_1.scheduled_time < end_2 and end_1 > schedule_2.scheduled_time):
                time_diff = abs((schedule_2.scheduled_time - schedule_1.scheduled_time).total_seconds() / 60)
                
                severity = 'high' if time_diff < 30 else 'medium'
                
                conflicts.append(ConflictInfo(
                    schedule_1=schedule_1,
                    schedule_2=schedule_2,
                    conflict_type='time_overlap',
                    severity=severity,
                    description=f"Schedules overlap by {60 - time_diff:.0f} minutes",
                    suggested_resolution=f"Move one schedule by at least {60 - time_diff + 15:.0f} minutes"
                ))
        
        except Exception as e:
            self.logger.error(f"Error checking time overlap: {str(e)}")
        
        return conflicts
    
    def _check_platform_conflict(self, schedule_1: Schedule, schedule_2: Schedule) -> List[ConflictInfo]:
        """Check for platform conflicts."""
        conflicts = []
        
        try:
            # This is a placeholder - platform conflicts would depend on specific platform limitations
            # For now, we'll check if schedules are too close on the same platform
            
            time_diff = abs((schedule_2.scheduled_time - schedule_1.scheduled_time).total_seconds() / 60)
            
            # If schedules are within 15 minutes, it might be a platform conflict
            if time_diff < 15:
                conflicts.append(ConflictInfo(
                    schedule_1=schedule_1,
                    schedule_2=schedule_2,
                    conflict_type='platform_conflict',
                    severity='medium',
                    description=f"Schedules too close for optimal platform performance",
                    suggested_resolution="Space schedules at least 15 minutes apart"
                ))
        
        except Exception as e:
            self.logger.error(f"Error checking platform conflict: {str(e)}")
        
        return conflicts
    
    def _check_priority_conflict(self, schedule_1: Schedule, schedule_2: Schedule) -> List[ConflictInfo]:
        """Check for priority conflicts."""
        conflicts = []
        
        try:
            # Check if high priority items are scheduled too close to low priority items
            if schedule_1.priority > 7 and schedule_2.priority < 4:
                time_diff = abs((schedule_2.scheduled_time - schedule_1.scheduled_time).total_seconds() / 60)
                
                if time_diff < 60:  # Within 1 hour
                    conflicts.append(ConflictInfo(
                        schedule_1=schedule_1,
                        schedule_2=schedule_2,
                        conflict_type='priority_conflict',
                        severity='low',
                        description="High priority content scheduled close to low priority content",
                        suggested_resolution="Consider spacing high and low priority content further apart"
                    ))
        
        except Exception as e:
            self.logger.error(f"Error checking priority conflict: {str(e)}")
        
        return conflicts
    
    def resolve_conflicts(self, conflicts: List[ConflictInfo]) -> Dict[str, Any]:
        """Resolve detected conflicts automatically.
        
        Args:
            conflicts: List of conflicts to resolve
            
        Returns:
            Dictionary containing resolution results
        """
        try:
            resolved_conflicts = []
            unresolved_conflicts = []
            schedule_adjustments = {}
            
            for conflict in conflicts:
                try:
                    # Get resolution strategy
                    strategy = self.resolution_strategies.get(conflict.conflict_type)
                    
                    if strategy:
                        resolution = strategy(conflict)
                        
                        if resolution['success']:
                            resolved_conflicts.append({
                                'conflict': conflict,
                                'resolution': resolution
                            })
                            
                            # Track schedule adjustments
                            for schedule_id, adjustments in resolution.get('adjustments', {}).items():
                                if schedule_id not in schedule_adjustments:
                                    schedule_adjustments[schedule_id] = {}
                                schedule_adjustments[schedule_id].update(adjustments)
                        else:
                            unresolved_conflicts.append(conflict)
                    else:
                        unresolved_conflicts.append(conflict)
                        
                except Exception as e:
                    self.logger.error(f"Error resolving conflict: {str(e)}")
                    unresolved_conflicts.append(conflict)
            
            return {
                'resolved_conflicts': resolved_conflicts,
                'unresolved_conflicts': unresolved_conflicts,
                'schedule_adjustments': schedule_adjustments,
                'success_rate': len(resolved_conflicts) / len(conflicts) if conflicts else 1.0
            }
            
        except Exception as e:
            self.logger.error(f"Error resolving conflicts: {str(e)}")
            return {
                'resolved_conflicts': [],
                'unresolved_conflicts': conflicts,
                'schedule_adjustments': {},
                'success_rate': 0.0
            }
    
    def _resolve_time_overlap(self, conflict: ConflictInfo) -> Dict[str, Any]:
        """Resolve time overlap conflicts."""
        try:
            # Strategy: Move the lower priority schedule
            schedule_1 = conflict.schedule_1
            schedule_2 = conflict.schedule_2
            
            # Determine which schedule to move
            if schedule_1.priority >= schedule_2.priority:
                schedule_to_move = schedule_2
                anchor_schedule = schedule_1
            else:
                schedule_to_move = schedule_1
                anchor_schedule = schedule_2
            
            # Calculate new time (move 1.5 hours after anchor)
            new_time = anchor_schedule.scheduled_time + timedelta(hours=1.5)
            
            return {
                'success': True,
                'strategy': 'move_lower_priority',
                'adjustments': {
                    str(schedule_to_move.id): {
                        'new_scheduled_time': new_time,
                        'reason': 'Resolved time overlap conflict'
                    }
                },
                'description': f"Moved schedule {schedule_to_move.id} to {new_time}"
            }
            
        except Exception as e:
            self.logger.error(f"Error resolving time overlap: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _resolve_platform_conflict(self, conflict: ConflictInfo) -> Dict[str, Any]:
        """Resolve platform conflicts."""
        try:
            # Strategy: Space schedules 20 minutes apart
            schedule_1 = conflict.schedule_1
            schedule_2 = conflict.schedule_2
            
            # Move the later schedule
            if schedule_1.scheduled_time < schedule_2.scheduled_time:
                schedule_to_move = schedule_2
                anchor_time = schedule_1.scheduled_time
            else:
                schedule_to_move = schedule_1
                anchor_time = schedule_2.scheduled_time
            
            new_time = anchor_time + timedelta(minutes=20)
            
            return {
                'success': True,
                'strategy': 'space_schedules',
                'adjustments': {
                    str(schedule_to_move.id): {
                        'new_scheduled_time': new_time,
                        'reason': 'Resolved platform conflict'
                    }
                },
                'description': f"Spaced schedule {schedule_to_move.id} to {new_time}"
            }
            
        except Exception as e:
            self.logger.error(f"Error resolving platform conflict: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _resolve_resource_conflict(self, conflict: ConflictInfo) -> Dict[str, Any]:
        """Resolve resource conflicts."""
        try:
            # This is a placeholder for resource conflict resolution
            return {
                'success': False,
                'reason': 'Resource conflict resolution not implemented'
            }
            
        except Exception as e:
            self.logger.error(f"Error resolving resource conflict: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _resolve_priority_conflict(self, conflict: ConflictInfo) -> Dict[str, Any]:
        """Resolve priority conflicts."""
        try:
            # Strategy: Move low priority content away from high priority content
            schedule_1 = conflict.schedule_1
            schedule_2 = conflict.schedule_2
            
            # Identify high and low priority schedules
            if schedule_1.priority > schedule_2.priority:
                high_priority = schedule_1
                low_priority = schedule_2
            else:
                high_priority = schedule_2
                low_priority = schedule_1
            
            # Move low priority content 2 hours away
            new_time = high_priority.scheduled_time + timedelta(hours=2)
            
            return {
                'success': True,
                'strategy': 'separate_priorities',
                'adjustments': {
                    str(low_priority.id): {
                        'new_scheduled_time': new_time,
                        'reason': 'Resolved priority conflict'
                    }
                },
                'description': f"Moved low priority schedule {low_priority.id} to {new_time}"
            }
            
        except Exception as e:
            self.logger.error(f"Error resolving priority conflict: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def suggest_optimal_schedule(
        self,
        new_schedule: Schedule,
        existing_schedules: List[Schedule]
    ) -> Dict[str, Any]:
        """Suggest optimal scheduling for new content.
        
        Args:
            new_schedule: New schedule to optimize
            existing_schedules: List of existing schedules
            
        Returns:
            Dictionary containing optimization suggestions
        """
        try:
            suggestions = []
            
            # Check for conflicts with proposed time
            all_schedules = existing_schedules + [new_schedule]
            conflicts = self.detect_conflicts(all_schedules)
            
            if not conflicts:
                return {
                    'optimal_time': new_schedule.scheduled_time,
                    'conflicts': [],
                    'suggestions': ['Current time is optimal']
                }
            
            # Generate alternative times
            base_time = new_schedule.scheduled_time
            alternative_times = []
            
            # Try different time slots
            for hours_offset in [1, 2, 3, -1, -2, -3]:
                alt_time = base_time + timedelta(hours=hours_offset)
                alt_schedule = Schedule(
                    content_item_id=new_schedule.content_item_id,
                    scheduled_time=alt_time,
                    status=new_schedule.status,
                    recurrence=new_schedule.recurrence,
                    priority=new_schedule.priority
                )
                
                # Check conflicts for this alternative
                alt_conflicts = self.detect_conflicts(existing_schedules + [alt_schedule])
                
                alternative_times.append({
                    'time': alt_time,
                    'conflicts': len(alt_conflicts),
                    'severity': max([c.severity for c in alt_conflicts], default='none')
                })
            
            # Sort by number of conflicts and severity
            alternative_times.sort(key=lambda x: (x['conflicts'], x['severity']))
            
            optimal_time = alternative_times[0]['time'] if alternative_times else new_schedule.scheduled_time
            
            return {
                'optimal_time': optimal_time,
                'conflicts': conflicts,
                'alternatives': alternative_times[:3],  # Top 3 alternatives
                'suggestions': [
                    f"Consider scheduling at {optimal_time}",
                    f"Current time has {len(conflicts)} conflicts",
                    "Review alternative times for better optimization"
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error suggesting optimal schedule: {str(e)}")
            return {
                'optimal_time': new_schedule.scheduled_time,
                'conflicts': [],
                'suggestions': ['Error occurred during optimization']
            } 