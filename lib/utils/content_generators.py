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
        "📅 Content Calendar Ideator (Coming Soon)"
    ])
    
    # Keywords Researcher tab
    with tab_keywords:
        do_web_research()
        
    # Competitor Analysis tab
    with tab_competitor:
        competitor_analysis()
        
    # Content Calendar Ideator tab
    with tab_calendar:
        st.info("🚧 **Coming Soon!** This feature is currently under development and will be available in a future update.")
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
            <h3 style='margin-top: 0;'>📅 Content Calendar Ideator</h3>
            <p>The Content Calendar Ideator will help you:</p>
            <ul>
                <li>Generate months-long content calendars around your keywords</li>
                <li>Get AI-suggested blog titles and topics</li>
                <li>Plan your content strategy with data-driven insights</li>
                <li>Organize your content creation schedule</li>
            </ul>
            <p><strong>Stay tuned for updates!</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Keep the original functionality but hide it behind a "Preview" button
        with st.expander("Preview Feature (Under Development)", expanded=False):
            plan_keywords = st.text_input(
                "**Enter Your main Keywords to get 2 months content calendar:**",
                placeholder="Enter 2-3 main keywords to generate AI content calendar with keyword researched blog titles",
                help="The keywords are the ones where you would want to generate 50-60 blogs/articles on."
            )
            if st.button("**Ideate Content Calendar**"):
                if plan_keywords:
                    #ai_agents_content_planner(plan_keywords)
                    st.header("Coming Soon.")
                else:
                    st.error("Come on, really, Enter some keywords to plan on..")
