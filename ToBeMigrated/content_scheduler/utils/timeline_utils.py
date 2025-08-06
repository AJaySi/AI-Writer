"""
Timeline utilities for content scheduling.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Use unified database models
from lib.database.models import ContentItem, Schedule, ScheduleStatus

logger = logging.getLogger(__name__)

class TimelineAnalyzer:
    """Analyze and visualize content scheduling timelines."""
    
    def __init__(self):
        """Initialize the timeline analyzer."""
        self.logger = logger
    
    def analyze_schedule_distribution(
        self,
        schedules: List[Schedule],
        time_range: str = "week"
    ) -> Dict[str, Any]:
        """Analyze the distribution of schedules over time.
        
        Args:
            schedules: List of Schedule objects
            time_range: Time range for analysis ('day', 'week', 'month')
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            if not schedules:
                return {
                    'total_schedules': 0,
                    'distribution': {},
                    'peak_times': [],
                    'gaps': []
                }
            
            # Group schedules by time period
            distribution = {}
            for schedule in schedules:
                if time_range == "day":
                    key = schedule.scheduled_time.strftime("%Y-%m-%d")
                elif time_range == "week":
                    # Get week start (Monday)
                    week_start = schedule.scheduled_time - timedelta(days=schedule.scheduled_time.weekday())
                    key = week_start.strftime("%Y-%m-%d")
                else:  # month
                    key = schedule.scheduled_time.strftime("%Y-%m")
                
                distribution[key] = distribution.get(key, 0) + 1
            
            # Find peak times
            peak_times = sorted(distribution.items(), key=lambda x: x[1], reverse=True)[:3]
            
            # Find gaps (periods with no content)
            gaps = self._find_gaps(schedules, time_range)
            
            return {
                'total_schedules': len(schedules),
                'distribution': distribution,
                'peak_times': peak_times,
                'gaps': gaps
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing schedule distribution: {str(e)}")
            return {}
    
    def _find_gaps(
        self,
        schedules: List[Schedule],
        time_range: str
    ) -> List[str]:
        """Find gaps in the schedule timeline.
        
        Args:
            schedules: List of Schedule objects
            time_range: Time range for analysis
            
        Returns:
            List of time periods with no scheduled content
        """
        try:
            if not schedules:
                return []
            
            # Get date range
            dates = [s.scheduled_time.date() for s in schedules]
            start_date = min(dates)
            end_date = max(dates)
            
            # Generate all periods in range
            current_date = start_date
            all_periods = set()
            
            while current_date <= end_date:
                if time_range == "day":
                    period = current_date.strftime("%Y-%m-%d")
                    current_date += timedelta(days=1)
                elif time_range == "week":
                    # Get week start (Monday)
                    week_start = current_date - timedelta(days=current_date.weekday())
                    period = week_start.strftime("%Y-%m-%d")
                    current_date += timedelta(weeks=1)
                else:  # month
                    period = current_date.strftime("%Y-%m")
                    # Move to next month
                    if current_date.month == 12:
                        current_date = current_date.replace(year=current_date.year + 1, month=1)
                    else:
                        current_date = current_date.replace(month=current_date.month + 1)
                
                all_periods.add(period)
            
            # Find periods with schedules
            scheduled_periods = set()
            for schedule in schedules:
                if time_range == "day":
                    period = schedule.scheduled_time.strftime("%Y-%m-%d")
                elif time_range == "week":
                    week_start = schedule.scheduled_time - timedelta(days=schedule.scheduled_time.weekday())
                    period = week_start.strftime("%Y-%m-%d")
                else:  # month
                    period = schedule.scheduled_time.strftime("%Y-%m")
                
                scheduled_periods.add(period)
            
            # Return gaps
            gaps = list(all_periods - scheduled_periods)
            return sorted(gaps)
            
        except Exception as e:
            self.logger.error(f"Error finding gaps: {str(e)}")
            return []
    
    def create_timeline_chart(
        self,
        schedules: List[Schedule],
        chart_type: str = "gantt"
    ) -> go.Figure:
        """Create a timeline visualization chart.
        
        Args:
            schedules: List of Schedule objects
            chart_type: Type of chart ('gantt', 'scatter', 'bar')
            
        Returns:
            Plotly figure object
        """
        try:
            if not schedules:
                fig = go.Figure()
                fig.add_annotation(
                    text="No schedules to display",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    showarrow=False
                )
                return fig
            
            if chart_type == "gantt":
                return self._create_gantt_chart(schedules)
            elif chart_type == "scatter":
                return self._create_scatter_chart(schedules)
            else:  # bar
                return self._create_bar_chart(schedules)
                
        except Exception as e:
            self.logger.error(f"Error creating timeline chart: {str(e)}")
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error creating chart: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False
            )
            return fig
    
    def _create_gantt_chart(self, schedules: List[Schedule]) -> go.Figure:
        """Create a Gantt chart for schedules."""
        try:
            # Prepare data for Gantt chart
            data = []
            for i, schedule in enumerate(schedules):
                # Estimate duration (default 1 hour)
                start_time = schedule.scheduled_time
                end_time = start_time + timedelta(hours=1)
                
                data.append({
                    'Task': f"Schedule {schedule.id}",
                    'Start': start_time,
                    'Finish': end_time,
                    'Status': schedule.status.value
                })
            
            df = pd.DataFrame(data)
            
            # Create Gantt chart
            fig = px.timeline(
                df,
                x_start="Start",
                x_end="Finish",
                y="Task",
                color="Status",
                title="Content Schedule Timeline"
            )
            
            fig.update_layout(
                xaxis_title="Time",
                yaxis_title="Schedules",
                height=max(400, len(schedules) * 30)
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating Gantt chart: {str(e)}")
            return go.Figure()
    
    def _create_scatter_chart(self, schedules: List[Schedule]) -> go.Figure:
        """Create a scatter plot for schedules."""
        try:
            # Prepare data
            dates = [s.scheduled_time for s in schedules]
            statuses = [s.status.value for s in schedules]
            ids = [s.id for s in schedules]
            
            # Create scatter plot
            fig = px.scatter(
                x=dates,
                y=statuses,
                title="Schedule Status Over Time",
                labels={'x': 'Scheduled Time', 'y': 'Status'},
                hover_data={'Schedule ID': ids}
            )
            
            fig.update_layout(
                xaxis_title="Scheduled Time",
                yaxis_title="Status"
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating scatter chart: {str(e)}")
            return go.Figure()
    
    def _create_bar_chart(self, schedules: List[Schedule]) -> go.Figure:
        """Create a bar chart for schedule distribution."""
        try:
            # Group by date
            date_counts = {}
            for schedule in schedules:
                date_key = schedule.scheduled_time.strftime("%Y-%m-%d")
                date_counts[date_key] = date_counts.get(date_key, 0) + 1
            
            # Create bar chart
            fig = px.bar(
                x=list(date_counts.keys()),
                y=list(date_counts.values()),
                title="Scheduled Content by Date",
                labels={'x': 'Date', 'y': 'Number of Schedules'}
            )
            
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Number of Schedules"
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating bar chart: {str(e)}")
            return go.Figure()
    
    def get_schedule_conflicts(
        self,
        schedules: List[Schedule],
        time_window: int = 60  # minutes
    ) -> List[Dict[str, Any]]:
        """Identify potential scheduling conflicts.
        
        Args:
            schedules: List of Schedule objects
            time_window: Time window in minutes to check for conflicts
            
        Returns:
            List of conflict information
        """
        try:
            conflicts = []
            
            # Sort schedules by time
            sorted_schedules = sorted(schedules, key=lambda x: x.scheduled_time)
            
            for i in range(len(sorted_schedules) - 1):
                current = sorted_schedules[i]
                next_schedule = sorted_schedules[i + 1]
                
                # Check if schedules are too close
                time_diff = (next_schedule.scheduled_time - current.scheduled_time).total_seconds() / 60
                
                if time_diff < time_window:
                    conflicts.append({
                        'schedule_1': current.id,
                        'schedule_2': next_schedule.id,
                        'time_1': current.scheduled_time,
                        'time_2': next_schedule.scheduled_time,
                        'gap_minutes': time_diff,
                        'severity': 'high' if time_diff < 30 else 'medium'
                    })
            
            return conflicts
            
        except Exception as e:
            self.logger.error(f"Error finding conflicts: {str(e)}")
            return []
    
    def suggest_optimal_times(
        self,
        existing_schedules: List[Schedule],
        target_date: datetime,
        duration_hours: int = 1
    ) -> List[datetime]:
        """Suggest optimal times for new content based on existing schedules.
        
        Args:
            existing_schedules: List of existing Schedule objects
            target_date: Target date for new content
            duration_hours: Expected duration of content in hours
            
        Returns:
            List of suggested optimal times
        """
        try:
            suggestions = []
            
            # Get schedules for target date
            target_schedules = [
                s for s in existing_schedules
                if s.scheduled_time.date() == target_date.date()
            ]
            
            # Define business hours (9 AM to 6 PM)
            business_start = target_date.replace(hour=9, minute=0, second=0, microsecond=0)
            business_end = target_date.replace(hour=18, minute=0, second=0, microsecond=0)
            
            # Generate potential time slots (every 30 minutes)
            current_time = business_start
            while current_time < business_end:
                # Check if this slot conflicts with existing schedules
                conflict = False
                for schedule in target_schedules:
                    schedule_end = schedule.scheduled_time + timedelta(hours=duration_hours)
                    slot_end = current_time + timedelta(hours=duration_hours)
                    
                    # Check for overlap
                    if (current_time < schedule_end and slot_end > schedule.scheduled_time):
                        conflict = True
                        break
                
                if not conflict:
                    suggestions.append(current_time)
                
                current_time += timedelta(minutes=30)
            
            return suggestions[:5]  # Return top 5 suggestions
            
        except Exception as e:
            self.logger.error(f"Error suggesting optimal times: {str(e)}")
            return [] 