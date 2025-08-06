"""
Timeline view implementation for the Content Scheduler.
Provides interactive Gantt charts and progress tracking visualization.
"""

import streamlit as st
import plotly.figure_factory as ff
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pandas as pd
import json

# Use unified database models
from lib.database.models import ContentItem, Schedule, ScheduleStatus, get_session

class TimelineView:
    """Interactive timeline view with Gantt charts and progress tracking."""
    
    def __init__(self):
        """Initialize the timeline view."""
        self.session = get_session()
    
    def render(self):
        """Render the timeline view."""
        st.header("Schedule Timeline")
        
        # Timeline controls
        self._render_timeline_controls()
        
        # Main timeline view
        self._render_timeline()
        
        # Progress tracking
        self._render_progress_tracking()
    
    def _render_timeline_controls(self):
        """Render timeline control options."""
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            view_type = st.selectbox(
                "View Type",
                ["Gantt Chart", "Timeline", "List View"],
                help="Select the type of timeline visualization"
            )
        
        with col2:
            date_range = st.date_input(
                "Date Range",
                value=(
                    datetime.now().date(),
                    datetime.now().date() + timedelta(days=7)
                ),
                help="Select the date range to display"
            )
        
        with col3:
            if st.button("Export", help="Export timeline data"):
                self._export_timeline_data()
    
    def _render_timeline(self):
        """Render the main timeline visualization."""
        # Get schedules for the selected date range
        schedules = self._get_schedules_for_timeline()
        
        if not schedules:
            st.info("No schedules found for the selected date range.")
            return
        
        # Create Gantt chart data
        gantt_data = self._create_gantt_data(schedules)
        
        # Create and display Gantt chart
        fig = self._create_gantt_chart(gantt_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display schedule details
        self._render_schedule_details(schedules)
    
    def _render_progress_tracking(self):
        """Render progress tracking visualization."""
        st.subheader("Progress Tracking")
        
        # Progress metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self._render_progress_metric(
                "Completed",
                self._get_completed_count(),
                "green"
            )
        
        with col2:
            self._render_progress_metric(
                "In Progress",
                self._get_in_progress_count(),
                "orange"
            )
        
        with col3:
            self._render_progress_metric(
                "Pending",
                self._get_pending_count(),
                "blue"
            )
        
        # Progress chart
        self._render_progress_chart()
    
    def _get_schedules_for_timeline(self) -> List[Schedule]:
        """Get schedules for the timeline view."""
        try:
            # Get date range from session state or use default
            if hasattr(st.session_state, 'date_range') and st.session_state.date_range:
                start_date, end_date = st.session_state.date_range
            else:
                start_date = datetime.now().date()
                end_date = start_date + timedelta(days=7)
            
            # Convert to datetime
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())
            
            # Query schedules from unified database
            schedules = self.session.query(Schedule).filter(
                Schedule.scheduled_time >= start_datetime,
                Schedule.scheduled_time <= end_datetime
            ).all()
            
            return schedules
            
        except Exception as e:
            st.error(f"Failed to get schedules: {str(e)}")
            return []
    
    def _create_gantt_data(self, schedules: List[Schedule]) -> List[Dict[str, Any]]:
        """Create data for Gantt chart."""
        gantt_data = []
        
        for schedule in schedules:
            # Get content item details
            content_item = self.session.query(ContentItem).filter(
                ContentItem.id == schedule.content_item_id
            ).first()
            
            if content_item:
                # Calculate task duration
                duration = timedelta(hours=1)  # Default duration
                
                # Create task data
                task = {
                    'Task': content_item.title[:50] + "..." if len(content_item.title) > 50 else content_item.title,
                    'Start': schedule.scheduled_time,
                    'Finish': schedule.scheduled_time + duration,
                    'Resource': schedule.status.value,
                    'Status': schedule.status.value,
                    'Progress': self._calculate_progress(schedule)
                }
                
                gantt_data.append(task)
        
        return gantt_data
    
    def _create_gantt_chart(self, gantt_data: List[Dict[str, Any]]) -> go.Figure:
        """Create Gantt chart visualization."""
        if not gantt_data:
            # Return empty figure
            fig = go.Figure()
            fig.update_layout(
                title='Content Schedule Timeline',
                xaxis_title='Timeline',
                yaxis_title='Status',
                height=400
            )
            return fig
        
        # Convert data to DataFrame
        df = pd.DataFrame(gantt_data)
        
        # Create Gantt chart
        fig = ff.create_gantt(
            df,
            index_col='Resource',
            show_colorbar=True,
            group_tasks=True,
            showgrid_x=True,
            showgrid_y=True
        )
        
        # Update layout
        fig.update_layout(
            title='Content Schedule Timeline',
            xaxis_title='Timeline',
            yaxis_title='Status',
            height=400,
            showlegend=True
        )
        
        return fig
    
    def _render_schedule_details(self, schedules: List[Schedule]):
        """Render detailed schedule information."""
        st.subheader("Schedule Details")
        
        for schedule in schedules:
            # Get content item details
            content_item = self.session.query(ContentItem).filter(
                ContentItem.id == schedule.content_item_id
            ).first()
            
            if content_item:
                with st.expander(f"{content_item.title} - {schedule.status.value}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Schedule Information**")
                        st.write(f"Content Type: {content_item.content_type.value if content_item.content_type else 'Unknown'}")
                        st.write(f"Status: {schedule.status.value}")
                        st.write(f"Scheduled Time: {schedule.scheduled_time}")
                        st.write(f"Priority: {schedule.priority}")
                        if schedule.recurrence:
                            st.write(f"Recurrence: {schedule.recurrence}")
                    
                    with col2:
                        st.write("**Progress**")
                        progress = self._calculate_progress(schedule)
                        st.progress(progress / 100)
                        st.write(f"Progress: {progress:.1f}%")
                        
                        # Action buttons
                        col2a, col2b = st.columns(2)
                        with col2a:
                            if st.button(f"Edit {schedule.id}", key=f"edit_{schedule.id}"):
                                st.session_state.edit_schedule_id = schedule.id
                        with col2b:
                            if st.button(f"Cancel {schedule.id}", key=f"cancel_{schedule.id}"):
                                self._cancel_schedule(schedule.id)
    
    def _render_progress_metric(self, label: str, value: int, color: str):
        """Render a progress metric."""
        st.metric(label, value)
    
    def _render_progress_chart(self):
        """Render progress chart visualization."""
        try:
            # Get progress data
            progress_data = self._get_progress_data()
            
            if progress_data:
                # Create pie chart
                labels = list(progress_data.keys())
                values = list(progress_data.values())
                
                fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                fig.update_layout(
                    title="Schedule Status Distribution",
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No progress data available.")
                
        except Exception as e:
            st.error(f"Error rendering progress chart: {str(e)}")
    
    def _calculate_progress(self, schedule: Schedule) -> float:
        """Calculate progress percentage for a schedule."""
        try:
            if schedule.status == ScheduleStatus.COMPLETED:
                return 100.0
            elif schedule.status == ScheduleStatus.RUNNING:
                return 50.0
            elif schedule.status == ScheduleStatus.FAILED:
                return 0.0
            else:  # PENDING
                return 0.0
                
        except Exception as e:
            st.error(f"Error calculating progress: {str(e)}")
            return 0.0
    
    def _get_completed_count(self) -> int:
        """Get count of completed schedules."""
        try:
            return self.session.query(Schedule).filter(
                Schedule.status == ScheduleStatus.COMPLETED
            ).count()
        except Exception as e:
            st.error(f"Error getting completed count: {str(e)}")
            return 0
    
    def _get_in_progress_count(self) -> int:
        """Get count of in-progress schedules."""
        try:
            return self.session.query(Schedule).filter(
                Schedule.status == ScheduleStatus.RUNNING
            ).count()
        except Exception as e:
            st.error(f"Error getting in-progress count: {str(e)}")
            return 0
    
    def _get_pending_count(self) -> int:
        """Get count of pending schedules."""
        try:
            return self.session.query(Schedule).filter(
                Schedule.status == ScheduleStatus.PENDING
            ).count()
        except Exception as e:
            st.error(f"Error getting pending count: {str(e)}")
            return 0
    
    def _get_progress_data(self) -> Dict[str, int]:
        """Get progress data for visualization."""
        try:
            progress_data = {}
            
            # Count schedules by status
            for status in ScheduleStatus:
                count = self.session.query(Schedule).filter(
                    Schedule.status == status
                ).count()
                progress_data[status.value] = count
            
            return progress_data
            
        except Exception as e:
            st.error(f"Error getting progress data: {str(e)}")
            return {}
    
    def _cancel_schedule(self, schedule_id: int):
        """Cancel a schedule."""
        try:
            schedule = self.session.query(Schedule).filter(
                Schedule.id == schedule_id
            ).first()
            
            if schedule:
                schedule.status = ScheduleStatus.CANCELLED
                self.session.commit()
                st.success(f"Schedule {schedule_id} cancelled successfully!")
                st.experimental_rerun()
            else:
                st.error("Schedule not found.")
                
        except Exception as e:
            st.error(f"Error cancelling schedule: {str(e)}")
            self.session.rollback()
    
    def _export_timeline_data(self):
        """Export timeline data."""
        try:
            schedules = self._get_schedules_for_timeline()
            
            if schedules:
                # Prepare export data
                export_data = []
                
                for schedule in schedules:
                    content_item = self.session.query(ContentItem).filter(
                        ContentItem.id == schedule.content_item_id
                    ).first()
                    
                    if content_item:
                        export_data.append({
                            'Schedule ID': schedule.id,
                            'Title': content_item.title,
                            'Content Type': content_item.content_type.value if content_item.content_type else 'Unknown',
                            'Scheduled Time': schedule.scheduled_time.isoformat(),
                            'Status': schedule.status.value,
                            'Priority': schedule.priority,
                            'Recurrence': schedule.recurrence or 'None'
                        })
                
                # Convert to CSV
                df = pd.DataFrame(export_data)
                csv = df.to_csv(index=False)
                
                # Provide download
                st.download_button(
                    label="Download Timeline Data",
                    data=csv,
                    file_name=f"timeline_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data to export.")
                
        except Exception as e:
            st.error(f"Error exporting data: {str(e)}") 