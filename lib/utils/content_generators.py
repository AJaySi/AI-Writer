import streamlit as st
from lib.utils.alwrity_utils import (
    blog_from_keyword, ai_agents_team, essay_writer, ai_news_writer,
    ai_finance_ta_writer, ai_social_writer, do_web_research, competitor_analysis
)
from lib.ai_writers.ai_story_writer.story_writer import story_input_section
from lib.ai_writers.ai_product_description_writer import write_ai_prod_desc
from lib.content_planning_calender.content_planning_agents_alwrity_crew import ai_agents_content_planner
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
    """Content planning tools with enhanced UI and styling"""
    
    # Apply custom CSS
    st.markdown(f'<style>{open("lib/workspace/alwrity_ui_styling.css").read()}</style>', unsafe_allow_html=True)
    
    # Header section with improved styling
    st.markdown("""
        <div class="content-header">
            <h2>🎯 Content Ideation & Planning</h2>
            <p class="subtitle">
                Comprehensive web research, keyword analysis, and content calendar generation tool.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different planning tools
    tabs = st.tabs([
        "🔍 Keywords Researcher",
        "📊 Competitor Analysis",
        "📅 Content Calendar"
    ])
    
    # Keywords Researcher Tab
    with tabs[0]:
        st.markdown("""
            <div class="tool-section">
                <h3>Keywords Research</h3>
                <p>Analyze keywords using Google Trends, Neural Analysis, and comprehensive web research.</p>
            </div>
        """, unsafe_allow_html=True)
        do_web_research()
    
    # Competitor Analysis Tab
    with tabs[1]:
        st.markdown("""
            <div class="tool-section">
                <h3>Competitor Analysis</h3>
                <p>Analyze competitor content and identify opportunities in your niche.</p>
            </div>
        """, unsafe_allow_html=True)
        competitor_analysis()
    
    # Content Calendar Tab
    with tabs[2]:
        st.markdown("""
            <div class="tool-section">
                <h3>Content Calendar Generator</h3>
                <p>Generate a 2-month content calendar with researched blog titles.</p>
            </div>
        """, unsafe_allow_html=True)
        
        plan_keywords = st.text_input(
            "**Enter Your main Keywords**",
            placeholder="Enter 2-3 main keywords for 50-60 blogs/articles",
            help="These keywords will be used to generate your content calendar"
        )
        
        if st.button("Generate Content Calendar", type="primary", use_container_width=True):
            if plan_keywords:
                ai_agents_content_planner(plan_keywords)
            else:
                st.error("Please enter some keywords to generate your content calendar.")
