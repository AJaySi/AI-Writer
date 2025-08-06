import streamlit as st
from typing import Dict, Any
from lib.database.models import ContentItem
import logging

logger = logging.getLogger(__name__)

def render_performance_insights(content_item: ContentItem, platform_adapter) -> None:
    """Render performance insights for a content item."""
    try:
        logger.info(f"Rendering performance insights for: {content_item.title}")
        
        # Get performance data from platform adapter
        performance_data = platform_adapter.get_content_performance(content_item)
        
        if not performance_data:
            st.warning("No performance data available for this content")
            return
        
        # Create metrics section
        st.subheader("Performance Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Engagement Rate",
                f"{performance_data.get('engagement_rate', 0):.1f}%",
                f"{performance_data.get('engagement_rate_change', 0):+.1f}%"
            )
        
        with col2:
            st.metric(
                "Reach",
                f"{performance_data.get('reach', 0):,}",
                f"{performance_data.get('reach_change', 0):+,}"
            )
        
        with col3:
            st.metric(
                "Conversion Rate",
                f"{performance_data.get('conversion_rate', 0):.1f}%",
                f"{performance_data.get('conversion_rate_change', 0):+.1f}%"
            )
        
        # Create audience insights section
        st.subheader("Audience Insights")
        audience_data = performance_data.get('audience_insights', {})
        
        if audience_data:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Demographics")
                st.write(f"- Age: {audience_data.get('age_range', 'N/A')}")
                st.write(f"- Gender: {audience_data.get('gender', 'N/A')}")
                st.write(f"- Location: {audience_data.get('location', 'N/A')}")
            
            with col2:
                st.write("Behavior")
                st.write(f"- Peak Time: {audience_data.get('peak_time', 'N/A')}")
                st.write(f"- Device: {audience_data.get('device', 'N/A')}")
                st.write(f"- Platform: {audience_data.get('platform', 'N/A')}")
        
        # Create content insights section
        st.subheader("Content Insights")
        content_insights = performance_data.get('content_insights', {})
        
        if content_insights:
            st.write("Top Performing Elements")
            for element, score in content_insights.get('top_elements', {}).items():
                st.write(f"- {element}: {score}")
            
            st.write("Improvement Suggestions")
            for suggestion in content_insights.get('suggestions', []):
                st.write(f"- {suggestion}")
        
        logger.info(f"Performance insights rendered successfully for: {content_item.title}")
        
    except Exception as e:
        logger.error(f"Error rendering performance insights: {str(e)}", exc_info=True)
        st.error(f"Error rendering performance insights: {str(e)}") 