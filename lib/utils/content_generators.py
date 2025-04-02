import streamlit as st
from lib.utils.alwrity_utils import (
    blog_from_keyword, ai_agents_team, essay_writer, ai_news_writer,
    ai_finance_ta_writer, ai_social_writer, do_web_research, competitor_analysis
)
from lib.ai_writers.ai_story_writer.story_writer import story_input_section
from lib.ai_writers.ai_product_description_writer import write_ai_prod_desc
#from lib.content_planning_calender.content_planning_agents_alwrity_crew import ai_agents_content_planner
from lib.utils.seo_tools import ai_seo_tools


def ai_writers():
    options = [
        "AI Blog Writer",
        "Story Writer",
        "Essay writer",
        "Write News reports",
        "Write Financial TA report",
        "AI Product Description Writer",
        "AI Copywriter",
        "Quit"
    ]
    choice = st.selectbox("**👇Select a content creation type:**", options, index=0, format_func=lambda x: f"📝 {x}")

    if choice == "AI Blog Writer":
        blog_from_keyword()
    elif choice == "Story Writer":
        story_input_section()
    elif choice == "Essay writer":
        essay_writer()
    elif choice == "Write News reports":
        ai_news_writer()
    elif choice == "Write Financial TA report":
        ai_finance_ta_writer()
    elif choice == "AI Product Description Writer":
        write_ai_prod_desc()
    elif choice == "Quit":
        st.subheader("Exiting, Getting Lost. But.... I have nowhere to go 🥹🥹")


def content_planning_tools():
    # Add custom CSS for compact layout
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
