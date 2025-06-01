"""
Main dashboard implementation for the Content Scheduler.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
import plotly.express as px
import plotly.graph_objects as go
from lib.database.models import ContentItem, Schedule, ScheduleStatus, ContentType, Platform, get_engine, get_session, init_db

engine = get_engine()
init_db(engine)
session = get_session(engine)

def run_dashboard():
    """Run the Streamlit dashboard."""
   
    st.title("📅 Alwrity Content Scheduler Dashboard")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Overview", "Schedule Management", "Create Schedule", "Job Monitor", "Analytics"]
    )

    if page == "Overview":
        show_overview()
    elif page == "Schedule Management":
        show_schedule_management()
    elif page == "Create Schedule":
        show_create_schedule()
    elif page == "Job Monitor":
        show_job_monitor()
    else:
        show_analytics()

def show_overview():
    """Display the overview dashboard."""
    st.header("📊 Overview")
    
    # Get data from unified database
    all_content = session.query(ContentItem).all()
    all_schedules = session.query(Schedule).all()
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Content Items", len(all_content))
    
    with col2:
        scheduled_count = len([s for s in all_schedules if s.status == ScheduleStatus.SCHEDULED])
        st.metric("Scheduled Items", scheduled_count)
    
    with col3:
        completed_count = len([s for s in all_schedules if s.status == ScheduleStatus.COMPLETED])
        st.metric("Completed", completed_count)
    
    with col4:
        failed_count = len([s for s in all_schedules if s.status == ScheduleStatus.FAILED])
        st.metric("Failed", failed_count)
    
    # Recent content
    st.subheader("📝 Recent Content Items")
    if all_content:
        recent_content = sorted(all_content, key=lambda x: x.created_at, reverse=True)[:5]
        for item in recent_content:
            with st.expander(f"{item.title} ({item.content_type.value})"):
                st.write(f"**Description:** {item.description or 'No description'}")
                st.write(f"**Platforms:** {', '.join(item.platforms) if isinstance(item.platforms, list) else item.platforms}")
                st.write(f"**Status:** {item.status}")
                st.write(f"**Created:** {item.created_at}")
                
                # Show associated schedules
                item_schedules = [s for s in all_schedules if s.content_item_id == item.id]
                if item_schedules:
                    st.write("**Schedules:**")
                    for schedule in item_schedules:
                        st.write(f"  - {schedule.scheduled_time} ({schedule.status.value})")
    else:
        st.info("No content items found. Create some content in the Content Calendar first!")

def show_schedule_management():
    """Display the schedule management interface."""
    st.header("📅 Schedule Management")
    
    # Get all schedules
    all_schedules = session.query(Schedule).all()
    
    if not all_schedules:
        st.info("No schedules found. Create schedules from the 'Create Schedule' tab.")
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            options=["All"] + [status.value for status in ScheduleStatus],
            key="schedule_status_filter"
        )
    
    with col2:
        date_filter = st.date_input(
            "Filter by Date (from)",
            value=datetime.now().date() - timedelta(days=30),
            key="schedule_date_filter"
        )
    
    # Apply filters
    filtered_schedules = all_schedules
    if status_filter != "All":
        filtered_schedules = [s for s in filtered_schedules if s.status.value == status_filter]
    
    filtered_schedules = [s for s in filtered_schedules if s.scheduled_time.date() >= date_filter]
    
    # Display schedules
    st.subheader(f"📋 Schedules ({len(filtered_schedules)} items)")
    
    for schedule in sorted(filtered_schedules, key=lambda x: x.scheduled_time, reverse=True):
        content_item = session.query(ContentItem).get(schedule.content_item_id)
        
        if content_item:
            with st.expander(f"{content_item.title} - {schedule.scheduled_time.strftime('%Y-%m-%d %H:%M')} ({schedule.status.value})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Content:** {content_item.title}")
                    st.write(f"**Type:** {content_item.content_type.value}")
                    st.write(f"**Platforms:** {', '.join(content_item.platforms) if isinstance(content_item.platforms, list) else content_item.platforms}")
                    st.write(f"**Scheduled Time:** {schedule.scheduled_time}")
                    st.write(f"**Status:** {schedule.status.value}")
                
                with col2:
                    st.write(f"**Recurrence:** {schedule.recurrence or 'One-time'}")
                    st.write(f"**Priority:** {schedule.priority}")
                    st.write(f"**Created:** {schedule.created_at}")
                    if schedule.result:
                        st.write(f"**Result:** {schedule.result}")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"Edit Schedule", key=f"edit_{schedule.id}"):
                        st.session_state.edit_schedule_id = schedule.id
                        st.rerun()
                
                with col2:
                    if schedule.status == ScheduleStatus.SCHEDULED:
                        if st.button(f"Cancel", key=f"cancel_{schedule.id}"):
                            schedule.status = ScheduleStatus.CANCELLED
                            session.commit()
                            st.success("Schedule cancelled!")
                            st.rerun()
                
                with col3:
                    if st.button(f"Delete", key=f"delete_{schedule.id}"):
                        session.delete(schedule)
                        session.commit()
                        st.success("Schedule deleted!")
                        st.rerun()

def show_create_schedule():
    """Display the schedule creation interface."""
    st.header("➕ Create New Schedule")
    
    # Get available content items
    content_items = session.query(ContentItem).all()
    
    if not content_items:
        st.warning("No content items available. Please create content in the Content Calendar first.")
        return
    
    # Create schedule form
    with st.form("create_schedule_form"):
        st.subheader("Schedule Configuration")
        
        # Select content item
        content_options = {f"{item.title} ({item.content_type.value})": item.id for item in content_items}
        selected_content = st.selectbox(
            "Select Content Item",
            options=list(content_options.keys()),
            key="schedule_content_select"
        )
        
        # Schedule timing
        col1, col2 = st.columns(2)
        with col1:
            schedule_date = st.date_input(
                "Schedule Date",
                value=datetime.now().date() + timedelta(days=1),
                key="schedule_date"
            )
        
        with col2:
            schedule_time = st.time_input(
                "Schedule Time",
                value=datetime.now().time(),
                key="schedule_time"
            )
        
        # Combine date and time
        schedule_datetime = datetime.combine(schedule_date, schedule_time)
        
        # Recurrence options
        recurrence = st.selectbox(
            "Recurrence",
            options=["none", "daily", "weekly", "monthly"],
            key="schedule_recurrence"
        )
        
        # Priority
        priority = st.slider(
            "Priority",
            min_value=1,
            max_value=10,
            value=5,
            key="schedule_priority"
        )
        
        # Platform selection (override content item platforms if needed)
        content_item_id = content_options[selected_content]
        content_item = session.query(ContentItem).get(content_item_id)
        
        if content_item:
            current_platforms = content_item.platforms if isinstance(content_item.platforms, list) else [content_item.platforms]
            st.write(f"**Current Platforms:** {', '.join(current_platforms)}")
            
            override_platforms = st.checkbox("Override Platforms", key="override_platforms")
            
            if override_platforms:
                available_platforms = [p.value for p in Platform]
                selected_platforms = st.multiselect(
                    "Select Platforms",
                    options=available_platforms,
                    default=current_platforms,
                    key="schedule_platforms"
                )
            else:
                selected_platforms = current_platforms
        
        # Submit button
        submitted = st.form_submit_button("Create Schedule")
        
        if submitted:
            try:
                # Create new schedule
                new_schedule = Schedule(
                    content_item_id=content_item_id,
                    scheduled_time=schedule_datetime,
                    status=ScheduleStatus.SCHEDULED,
                    recurrence=recurrence if recurrence != "none" else None,
                    priority=priority
                )
                
                session.add(new_schedule)
                session.commit()
                
                st.success(f"✅ Schedule created successfully! Content will be published on {schedule_datetime}")
                
                # Show schedule details
                with st.expander("Schedule Details", expanded=True):
                    st.write(f"**Content:** {content_item.title}")
                    st.write(f"**Scheduled Time:** {schedule_datetime}")
                    st.write(f"**Platforms:** {', '.join(selected_platforms)}")
                    st.write(f"**Recurrence:** {recurrence}")
                    st.write(f"**Priority:** {priority}")
                
            except Exception as e:
                st.error(f"❌ Error creating schedule: {str(e)}")

def show_job_monitor():
    """Display the job monitoring interface."""
    st.header("🔍 Job Monitor")
    
    # Get all schedules with their status
    all_schedules = session.query(Schedule).all()
    
    if not all_schedules:
        st.info("No jobs to monitor.")
        return
    
    # Status distribution
    status_counts = {}
    for schedule in all_schedules:
        status = schedule.status.value
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Display status chart
    if status_counts:
        fig = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="Job Status Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent job activity
    st.subheader("📊 Recent Job Activity")
    
    recent_schedules = sorted(all_schedules, key=lambda x: x.updated_at, reverse=True)[:10]
    
    for schedule in recent_schedules:
        content_item = session.query(ContentItem).get(schedule.content_item_id)
        
        if content_item:
            status_color = {
                ScheduleStatus.SCHEDULED: "🟡",
                ScheduleStatus.RUNNING: "🔵", 
                ScheduleStatus.COMPLETED: "🟢",
                ScheduleStatus.FAILED: "🔴",
                ScheduleStatus.CANCELLED: "⚫"
            }.get(schedule.status, "⚪")
            
            st.write(f"{status_color} **{content_item.title}** - {schedule.status.value} - {schedule.updated_at.strftime('%Y-%m-%d %H:%M')}")
            
            if schedule.result:
                st.write(f"   └─ {schedule.result}")

def show_analytics():
    """Display the analytics dashboard."""
    st.header("📈 Analytics")
    
    # Get data
    all_content = session.query(ContentItem).all()
    all_schedules = session.query(Schedule).all()
    
    if not all_schedules:
        st.info("No data available for analytics.")
        return
    
    # Time-based analytics
    st.subheader("📅 Schedule Timeline")
    
    # Create timeline data
    timeline_data = []
    for schedule in all_schedules:
        content_item = session.query(ContentItem).get(schedule.content_item_id)
        if content_item:
            timeline_data.append({
                'Date': schedule.scheduled_time.date(),
                'Content': content_item.title,
                'Status': schedule.status.value,
                'Type': content_item.content_type.value
            })
    
    if timeline_data:
        df = pd.DataFrame(timeline_data)
        
        # Schedule frequency by date
        date_counts = df.groupby('Date').size().reset_index(name='Count')
        fig = px.line(date_counts, x='Date', y='Count', title='Scheduled Content Over Time')
        st.plotly_chart(fig, use_container_width=True)
        
        # Content type distribution
        type_counts = df['Type'].value_counts()
        fig = px.bar(x=type_counts.index, y=type_counts.values, title='Content Type Distribution')
        st.plotly_chart(fig, use_container_width=True)
        
        # Status breakdown
        status_counts = df['Status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, title='Status Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance metrics
    st.subheader("📊 Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_schedules = len(all_schedules)
        st.metric("Total Schedules", total_schedules)
    
    with col2:
        completed_schedules = len([s for s in all_schedules if s.status == ScheduleStatus.COMPLETED])
        success_rate = (completed_schedules / total_schedules * 100) if total_schedules > 0 else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")
    
    with col3:
        failed_schedules = len([s for s in all_schedules if s.status == ScheduleStatus.FAILED])
        failure_rate = (failed_schedules / total_schedules * 100) if total_schedules > 0 else 0
        st.metric("Failure Rate", f"{failure_rate:.1f}%") 