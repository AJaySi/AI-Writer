import streamlit as st

from lib.alwrity_ui.similar_analysis import competitor_analysis
from lib.alwrity_ui.keyword_web_researcher import do_web_research


def content_planning_tools():
    # A custom CSS for compact layout
    st.markdown("""
        <style>
            /* Reduce top padding of main container */
            .main .block-container {
                padding-top: 0rem !important;
                padding-bottom: 1rem !important;
            }
            
            /* Reduce spacing between elements */
            .stTabs {
                margin-top: 0.5rem !important;
            }
            
            /* Make markdown text more compact */
            .element-container {
                margin-bottom: 0.5rem !important;
            }
            
            /* Adjust subheader margins */
            .stMarkdown h3 {
                margin-top: 0 !important;
                margin-bottom: 0.5rem !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Make description more compact using a smaller font
    st.markdown("""
        <div style='font-size: 0.9em; margin-bottom: 0.5rem;'>
            <strong>Alwrity content Ideation & Planning</strong>: Provide few keywords to do comprehensive web research.
            Provide few keywords to get Google, Neural, pytrends analysis. Know keywords, blog titles to target.
            Generate months long content calendar around given keywords.
        </div>
    """, unsafe_allow_html=True)
    
    # Create tabs with reduced spacing
    tab_keywords, tab_competitor, tab_calendar = st.tabs([
        "🔍 Keywords Researcher",
        "📊 Competitor Analysis",
        "📅 Content Calendar Ideator"
    ])
    
    # Keywords Researcher tab
    with tab_keywords:
        do_web_research()
        
    # Competitor Analysis tab
    with tab_competitor:
        competitor_analysis()
        
    # Content Calendar Ideator tab
    with tab_calendar:
        st.info("🚧 **Content Calendar & Planning Dashboard**")
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
            <h3 style='margin-top: 0;'>📅 Content Calendar & Planning Dashboard</h3>
            <p>The Content Calendar Dashboard provides:</p>
            <ul>
                <li>AI-powered content planning and generation</li>
                <li>Multi-platform content scheduling</li>
                <li>Content optimization tools</li>
                <li>A/B testing capabilities</li>
                <li>Performance analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize and render the dashboard directly
        from lib.ai_seo_tools.content_calendar.ui.dashboard import ContentCalendarDashboard
        dashboard = ContentCalendarDashboard()
        dashboard.render()
