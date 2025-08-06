"""
Schedule optimization system for content scheduling.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from collections import defaultdict

# Use unified database models
from lib.database.models import ContentItem, Schedule, ScheduleStatus, ContentType, Platform, get_session

logger = logging.getLogger(__name__)

@dataclass
class OptimizationResult:
    """Result of schedule optimization."""
    original_schedule: Schedule
    optimized_time: datetime
    improvement_score: float
    optimization_reason: str
    confidence: float

class ScheduleOptimizer:
    """Optimize content scheduling for maximum engagement."""
    
    def __init__(self):
        """Initialize the schedule optimizer."""
        self.logger = logger
        self.session = get_session()
        
        # Platform-specific optimal times (can be made configurable)
        self.platform_optimal_times = {
            Platform.TWITTER: [9, 12, 15, 18],  # Hours of day
            Platform.FACEBOOK: [9, 13, 15],
            Platform.LINKEDIN: [8, 12, 17],
            Platform.INSTAGRAM: [11, 14, 17, 19],
            Platform.YOUTUBE: [14, 16, 18, 20]
        }
        
        # Content type engagement patterns
        self.content_type_patterns = {
            ContentType.ARTICLE: {'peak_hours': [9, 14, 16], 'duration': 2},
            ContentType.VIDEO: {'peak_hours': [12, 18, 20], 'duration': 3},
            ContentType.IMAGE: {'peak_hours': [11, 15, 19], 'duration': 1},
            ContentType.SOCIAL_POST: {'peak_hours': [8, 12, 17, 21], 'duration': 1}
        }
    
    def optimize_schedule(self, schedule: Schedule) -> OptimizationResult:
        """Optimize a single schedule for better engagement.
        
        Args:
            schedule: Schedule to optimize
            
        Returns:
            OptimizationResult with optimization details
        """
        try:
            # Get content item details
            content_item = self.session.query(ContentItem).filter(
                ContentItem.id == schedule.content_item_id
            ).first()
            
            if not content_item:
                return OptimizationResult(
                    original_schedule=schedule,
                    optimized_time=schedule.scheduled_time,
                    improvement_score=0.0,
                    optimization_reason="Content item not found",
                    confidence=0.0
                )
            
            # Calculate current engagement score
            current_score = self._calculate_engagement_score(
                schedule.scheduled_time,
                content_item.content_type,
                schedule.priority
            )
            
            # Find optimal time
            optimal_time, optimal_score = self._find_optimal_time(
                schedule,
                content_item
            )
            
            # Calculate improvement
            improvement_score = optimal_score - current_score
            confidence = min(improvement_score / current_score, 1.0) if current_score > 0 else 0.0
            
            # Generate optimization reason
            reason = self._generate_optimization_reason(
                schedule.scheduled_time,
                optimal_time,
                content_item.content_type,
                improvement_score
            )
            
            return OptimizationResult(
                original_schedule=schedule,
                optimized_time=optimal_time,
                improvement_score=improvement_score,
                optimization_reason=reason,
                confidence=confidence
            )
            
        except Exception as e:
            self.logger.error(f"Error optimizing schedule: {str(e)}")
            return OptimizationResult(
                original_schedule=schedule,
                optimized_time=schedule.scheduled_time,
                improvement_score=0.0,
                optimization_reason=f"Optimization error: {str(e)}",
                confidence=0.0
            )
    
    def optimize_multiple_schedules(
        self,
        schedules: List[Schedule],
        avoid_conflicts: bool = True
    ) -> List[OptimizationResult]:
        """Optimize multiple schedules considering conflicts.
        
        Args:
            schedules: List of schedules to optimize
            avoid_conflicts: Whether to avoid scheduling conflicts
            
        Returns:
            List of optimization results
        """
        try:
            results = []
            optimized_times = []
            
            # Sort schedules by priority (high priority first)
            sorted_schedules = sorted(schedules, key=lambda x: x.priority, reverse=True)
            
            for schedule in sorted_schedules:
                # Optimize individual schedule
                result = self.optimize_schedule(schedule)
                
                if avoid_conflicts:
                    # Check for conflicts with already optimized schedules
                    conflict_free_time = self._find_conflict_free_time(
                        result.optimized_time,
                        optimized_times,
                        schedule
                    )
                    
                    if conflict_free_time != result.optimized_time:
                        # Recalculate scores for conflict-free time
                        content_item = self.session.query(ContentItem).filter(
                            ContentItem.id == schedule.content_item_id
                        ).first()
                        
                        if content_item:
                            new_score = self._calculate_engagement_score(
                                conflict_free_time,
                                content_item.content_type,
                                schedule.priority
                            )
                            
                            original_score = self._calculate_engagement_score(
                                schedule.scheduled_time,
                                content_item.content_type,
                                schedule.priority
                            )
                            
                            result.optimized_time = conflict_free_time
                            result.improvement_score = new_score - original_score
                            result.optimization_reason += " (adjusted to avoid conflicts)"
                
                results.append(result)
                optimized_times.append(result.optimized_time)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error optimizing multiple schedules: {str(e)}")
            return []
    
    def suggest_optimal_times(
        self,
        content_type: ContentType,
        date_range: Tuple[datetime, datetime],
        count: int = 5
    ) -> List[Dict[str, Any]]:
        """Suggest optimal times for new content.
        
        Args:
            content_type: Type of content to schedule
            date_range: Date range to consider
            count: Number of suggestions to return
            
        Returns:
            List of suggested optimal times with scores
        """
        try:
            suggestions = []
            start_date, end_date = date_range
            
            # Generate candidate times
            current_date = start_date
            while current_date <= end_date:
                # Get optimal hours for this content type
                if content_type in self.content_type_patterns:
                    optimal_hours = self.content_type_patterns[content_type]['peak_hours']
                else:
                    optimal_hours = [9, 12, 15, 18]  # Default hours
                
                for hour in optimal_hours:
                    candidate_time = current_date.replace(
                        hour=hour,
                        minute=0,
                        second=0,
                        microsecond=0
                    )
                    
                    if start_date <= candidate_time <= end_date:
                        score = self._calculate_engagement_score(
                            candidate_time,
                            content_type,
                            priority=5  # Default priority
                        )
                        
                        suggestions.append({
                            'time': candidate_time,
                            'score': score,
                            'day_of_week': candidate_time.strftime('%A'),
                            'hour': hour,
                            'reason': self._get_time_suggestion_reason(candidate_time, content_type)
                        })
                
                current_date += timedelta(days=1)
            
            # Sort by score and return top suggestions
            suggestions.sort(key=lambda x: x['score'], reverse=True)
            return suggestions[:count]
            
        except Exception as e:
            self.logger.error(f"Error suggesting optimal times: {str(e)}")
            return []
    
    def _calculate_engagement_score(
        self,
        scheduled_time: datetime,
        content_type: ContentType,
        priority: int
    ) -> float:
        """Calculate engagement score for a given time and content type."""
        try:
            score = 0.0
            
            # Base score from priority
            score += priority * 10
            
            # Hour of day factor
            hour = scheduled_time.hour
            if content_type in self.content_type_patterns:
                optimal_hours = self.content_type_patterns[content_type]['peak_hours']
                if hour in optimal_hours:
                    score += 50
                else:
                    # Penalty for non-optimal hours
                    min_distance = min(abs(hour - oh) for oh in optimal_hours)
                    score += max(0, 30 - min_distance * 5)
            
            # Day of week factor
            day_of_week = scheduled_time.weekday()  # 0 = Monday, 6 = Sunday
            
            if content_type == ContentType.ARTICLE:
                # Articles perform better on weekdays
                if day_of_week < 5:  # Monday to Friday
                    score += 20
                else:
                    score += 5
            elif content_type == ContentType.VIDEO:
                # Videos perform better on weekends and evenings
                if day_of_week >= 5 or hour >= 18:
                    score += 25
                else:
                    score += 10
            elif content_type == ContentType.SOCIAL_POST:
                # Social posts are consistent throughout the week
                score += 15
            
            # Time spacing factor (avoid clustering)
            existing_schedules = self.session.query(Schedule).filter(
                Schedule.scheduled_time.between(
                    scheduled_time - timedelta(hours=2),
                    scheduled_time + timedelta(hours=2)
                )
            ).all()
            
            if len(existing_schedules) > 3:
                score -= len(existing_schedules) * 5
            
            return max(score, 0.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating engagement score: {str(e)}")
            return 0.0
    
    def _find_optimal_time(
        self,
        schedule: Schedule,
        content_item: ContentItem
    ) -> Tuple[datetime, float]:
        """Find the optimal time for a schedule."""
        try:
            best_time = schedule.scheduled_time
            best_score = self._calculate_engagement_score(
                schedule.scheduled_time,
                content_item.content_type,
                schedule.priority
            )
            
            # Search within a week of the original time
            base_date = schedule.scheduled_time.date()
            
            for day_offset in range(-3, 4):  # ±3 days
                candidate_date = base_date + timedelta(days=day_offset)
                
                # Get optimal hours for this content type
                if content_item.content_type in self.content_type_patterns:
                    optimal_hours = self.content_type_patterns[content_item.content_type]['peak_hours']
                else:
                    optimal_hours = [9, 12, 15, 18]
                
                for hour in optimal_hours:
                    candidate_time = datetime.combine(candidate_date, datetime.min.time()).replace(hour=hour)
                    
                    score = self._calculate_engagement_score(
                        candidate_time,
                        content_item.content_type,
                        schedule.priority
                    )
                    
                    if score > best_score:
                        best_time = candidate_time
                        best_score = score
            
            return best_time, best_score
            
        except Exception as e:
            self.logger.error(f"Error finding optimal time: {str(e)}")
            return schedule.scheduled_time, 0.0
    
    def _find_conflict_free_time(
        self,
        preferred_time: datetime,
        existing_times: List[datetime],
        schedule: Schedule,
        min_gap: timedelta = timedelta(minutes=30)
    ) -> datetime:
        """Find a conflict-free time close to the preferred time."""
        try:
            # Check if preferred time has conflicts
            has_conflict = any(
                abs((preferred_time - existing_time).total_seconds()) < min_gap.total_seconds()
                for existing_time in existing_times
            )
            
            if not has_conflict:
                return preferred_time
            
            # Search for nearby conflict-free times
            for offset_minutes in [30, 60, 90, 120, -30, -60, -90, -120]:
                candidate_time = preferred_time + timedelta(minutes=offset_minutes)
                
                has_conflict = any(
                    abs((candidate_time - existing_time).total_seconds()) < min_gap.total_seconds()
                    for existing_time in existing_times
                )
                
                if not has_conflict:
                    return candidate_time
            
            # If no conflict-free time found nearby, return preferred time
            return preferred_time
            
        except Exception as e:
            self.logger.error(f"Error finding conflict-free time: {str(e)}")
            return preferred_time
    
    def _generate_optimization_reason(
        self,
        original_time: datetime,
        optimized_time: datetime,
        content_type: ContentType,
        improvement_score: float
    ) -> str:
        """Generate a human-readable optimization reason."""
        try:
            if improvement_score <= 0:
                return "Current time is already optimal"
            
            reasons = []
            
            # Time difference
            time_diff = optimized_time - original_time
            if abs(time_diff.total_seconds()) > 3600:  # More than 1 hour
                if time_diff.total_seconds() > 0:
                    reasons.append(f"Moved {time_diff.total_seconds() / 3600:.1f} hours later")
                else:
                    reasons.append(f"Moved {abs(time_diff.total_seconds()) / 3600:.1f} hours earlier")
            
            # Hour optimization
            original_hour = original_time.hour
            optimized_hour = optimized_time.hour
            
            if content_type in self.content_type_patterns:
                optimal_hours = self.content_type_patterns[content_type]['peak_hours']
                if optimized_hour in optimal_hours and original_hour not in optimal_hours:
                    reasons.append(f"Moved to peak engagement hour ({optimized_hour}:00)")
            
            # Day optimization
            original_day = original_time.strftime('%A')
            optimized_day = optimized_time.strftime('%A')
            
            if original_day != optimized_day:
                reasons.append(f"Moved from {original_day} to {optimized_day}")
            
            # Improvement score
            reasons.append(f"Expected {improvement_score:.1f}% engagement improvement")
            
            return "; ".join(reasons) if reasons else "Optimized for better engagement"
            
        except Exception as e:
            self.logger.error(f"Error generating optimization reason: {str(e)}")
            return "Optimized for better engagement"
    
    def _get_time_suggestion_reason(self, time: datetime, content_type: ContentType) -> str:
        """Get reason for suggesting a specific time."""
        try:
            reasons = []
            
            hour = time.hour
            day_name = time.strftime('%A')
            
            # Hour-based reasons
            if content_type in self.content_type_patterns:
                optimal_hours = self.content_type_patterns[content_type]['peak_hours']
                if hour in optimal_hours:
                    reasons.append(f"Peak engagement hour for {content_type.value}")
            
            # Day-based reasons
            if content_type == ContentType.ARTICLE and time.weekday() < 5:
                reasons.append("Weekday optimal for articles")
            elif content_type == ContentType.VIDEO and (time.weekday() >= 5 or hour >= 18):
                reasons.append("Evening/weekend optimal for videos")
            
            return "; ".join(reasons) if reasons else f"Good time for {content_type.value}"
            
        except Exception as e:
            self.logger.error(f"Error getting suggestion reason: {str(e)}")
            return "Recommended time"
    
    def analyze_schedule_performance(self, days_back: int = 30) -> Dict[str, Any]:
        """Analyze historical schedule performance."""
        try:
            # Get schedules from the last N days
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            schedules = self.session.query(Schedule).filter(
                Schedule.created_at >= cutoff_date
            ).all()
            
            if not schedules:
                return {'error': 'No schedules found for analysis'}
            
            # Analyze by hour
            hour_performance = defaultdict(list)
            day_performance = defaultdict(list)
            content_type_performance = defaultdict(list)
            
            for schedule in schedules:
                content_item = self.session.query(ContentItem).filter(
                    ContentItem.id == schedule.content_item_id
                ).first()
                
                if content_item:
                    hour = schedule.scheduled_time.hour
                    day = schedule.scheduled_time.strftime('%A')
                    
                    # Calculate performance score (simplified)
                    performance_score = self._calculate_performance_score(schedule)
                    
                    hour_performance[hour].append(performance_score)
                    day_performance[day].append(performance_score)
                    content_type_performance[content_item.content_type.value].append(performance_score)
            
            # Calculate averages
            analysis = {
                'total_schedules': len(schedules),
                'analysis_period_days': days_back,
                'best_hours': self._get_top_performers(hour_performance),
                'best_days': self._get_top_performers(day_performance),
                'content_type_performance': self._get_top_performers(content_type_performance),
                'recommendations': self._generate_performance_recommendations(
                    hour_performance,
                    day_performance,
                    content_type_performance
                )
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing schedule performance: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_performance_score(self, schedule: Schedule) -> float:
        """Calculate a performance score for a schedule (simplified)."""
        try:
            # This is a simplified performance calculation
            # In a real implementation, this would use actual engagement metrics
            
            base_score = 50.0  # Base performance
            
            # Status-based scoring
            if schedule.status == ScheduleStatus.COMPLETED:
                base_score += 30
            elif schedule.status == ScheduleStatus.RUNNING:
                base_score += 15
            elif schedule.status == ScheduleStatus.FAILED:
                base_score -= 20
            
            # Priority-based scoring
            base_score += schedule.priority * 2
            
            return max(base_score, 0.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating performance score: {str(e)}")
            return 0.0
    
    def _get_top_performers(self, performance_data: Dict[str, List[float]]) -> List[Dict[str, Any]]:
        """Get top performing items from performance data."""
        try:
            performers = []
            
            for key, scores in performance_data.items():
                if scores:
                    avg_score = np.mean(scores)
                    performers.append({
                        'key': key,
                        'average_score': avg_score,
                        'sample_count': len(scores)
                    })
            
            # Sort by average score
            performers.sort(key=lambda x: x['average_score'], reverse=True)
            
            return performers[:5]  # Top 5
            
        except Exception as e:
            self.logger.error(f"Error getting top performers: {str(e)}")
            return []
    
    def _generate_performance_recommendations(
        self,
        hour_performance: Dict[int, List[float]],
        day_performance: Dict[str, List[float]],
        content_type_performance: Dict[str, List[float]]
    ) -> List[str]:
        """Generate performance-based recommendations."""
        try:
            recommendations = []
            
            # Hour recommendations
            if hour_performance:
                best_hours = self._get_top_performers(hour_performance)
                if best_hours:
                    best_hour = best_hours[0]['key']
                    recommendations.append(f"Schedule more content around {best_hour}:00 for better performance")
            
            # Day recommendations
            if day_performance:
                best_days = self._get_top_performers(day_performance)
                if best_days:
                    best_day = best_days[0]['key']
                    recommendations.append(f"Consider scheduling more content on {best_day}s")
            
            # Content type recommendations
            if content_type_performance:
                best_types = self._get_top_performers(content_type_performance)
                if best_types:
                    best_type = best_types[0]['key']
                    recommendations.append(f"{best_type} content shows the best performance")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
            return [] 