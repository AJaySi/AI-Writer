import streamlit as st
from datetime import datetime, timedelta

def render_filters():
    with st.expander("Filters", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", st.session_state.get('filter_start_date', datetime.now()))
            end_date = st.date_input("End Date", st.session_state.get('filter_end_date', datetime.now() + timedelta(days=30)))
            st.session_state['filter_start_date'] = start_date
            st.session_state['filter_end_date'] = end_date
        with col2:
            platforms = st.multiselect(
                "Platforms",
                ["Blog", "Instagram", "Twitter", "LinkedIn", "Facebook"],
                default=st.session_state.get('filter_platforms', ["Blog"])
            )
            st.session_state['filter_platforms'] = platforms
            content_types = st.multiselect(
                "Content Types",
                ["Article", "Social Post", "Video", "Newsletter"],
                default=st.session_state.get('filter_content_types', ["Article"])
            )
            st.session_state['filter_content_types'] = content_types
            statuses = st.multiselect(
                "Status",
                ["Draft", "Scheduled", "Published", "Archived"],
                default=st.session_state.get('filter_statuses', ["Draft", "Scheduled"])
            )
            st.session_state['filter_statuses'] = statuses 