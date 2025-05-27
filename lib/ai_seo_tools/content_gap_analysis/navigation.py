"""
Navigation component for Content Gap Analysis tool.
"""

import streamlit as st

def show_content_gap_analysis_nav():
    """Show navigation for Content Gap Analysis tool."""
    st.sidebar.title("Content Gap Analysis")
    st.sidebar.markdown("""
    Analyze your content strategy, identify gaps, and get AI-powered recommendations.
    """)
    
    # Navigation options
    nav_option = st.sidebar.radio(
        "Select Analysis Type",
        ["Website Analysis", "Competitor Analysis", "Keyword Research", "Recommendations"]
    )
    
    # Tool description
    st.sidebar.markdown("""
    ### Features
    - Website content analysis
    - Competitor content comparison
    - Keyword research and trends
    - AI-powered recommendations
    - Content gap identification
    - Implementation timeline
    """)
    
    # Help section
    with st.sidebar.expander("How to Use"):
        st.markdown("""
        1. Start with Website Analysis
        2. Add competitor URLs
        3. Research keywords
        4. Get recommendations
        5. Export results
        """)
    
    return nav_option 