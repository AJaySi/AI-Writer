import re
import os
import PyPDF2
import openai
import streamlit as st
import tempfile
from loguru import logger


from lib.ai_writers.ai_news_article_writer import ai_news_generation
from lib.ai_writers.ai_finance_report_generator.ai_financial_dashboard import get_dashboard
from lib.ai_writers.ai_facebook_writer.facebook_ai_writer import facebook_main_menu
from lib.ai_writers.linkedin_writer.linkedin_ai_writer import linkedin_main_menu
from lib.ai_writers.twitter_writers.twitter_dashboard import run_dashboard
from lib.ai_writers.insta_ai_writer import insta_writer
from lib.ai_writers.youtube_writers.youtube_ai_writer import youtube_main_menu
from lib.ai_writers.ai_essay_writer import ai_essay_generator
from lib.gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image
#from lib.content_planning_calender.content_planning_agents_alwrity_crew import ai_agents_content_planner
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen


def ai_agents_team():
    # Define options for AI Content Teams
    st.title("🐲 Your AI Agents Teams")
    st.markdown("""Alwrity offers AI agents team for content creators to easily modify them for their needs.
                Abstracting tech & plumbing, easily define role, goal, task. Use different AI agents framework.""")
    
    options = [
        "AI Planning Team",
        "AI Content Creation Team"
    ]

    # Radio button for choosing an AI Content Team
    selected_team = st.radio("**Choose AI Agents Team:**", options)

    if selected_team == "AI Planning Team":
        st.title("AI Agents for Content Ideation")
        plan_keywords = st.text_input(
            "Enter Keywords to get 2 months content calendar:",
            placeholder="Enter keywords to generate AI content calendar:",
            help="Enter at least two words for better results."
        )
        if st.button("Get calendar"):
            if plan_keywords and len(plan_keywords.split()) >= 2:
                with st.spinner("Get Content Plan..."):
                    try:
                        #plan_content = ai_agents_content_planner(plan_keywords)
                        st.success(f"Coming soon: Content plan for: {plan_keywords}")
                        #st.markdown(plan_content)
                    except Exception as err:
                        st.error(f"Failed to generate content plan: {err}")
            else:
                st.error("🚫 Single keywords are just too vague. Try again.")
    elif selected_team == "AI Content Creation Team":
        content_agents()



def content_agents():
    st.markdown("AI Agents Team for Content Writing")
    content_keywords = st.text_input(
        "Enter Main Domain Keywords of your business:",
        placeholder="Better keywords, Better content. Get keywords from Google search",
        help="These keywords define your main business sector, blogging niche, Industry, domain etc"
    )

    if st.button("Start Writing"):
        if content_keywords and len(content_keywords.split()) >= 2:
            with st.spinner("Generating Content..."):
                try:
                    #calendar_content = ai_agents_writers(content_keywords)
                    st.success(f"🚫 Not implemented yet: {content_keywords}")
                    #st.markdown(calendar_content)
                except Exception as err:
                    st.error(f"🚫 Failed to generate content with AI Agents: {err}")
        else:
            st.error("🚫 Single keywords are just too vague. Try again.")



def essay_writer():
    st.title("AI Essay Writer 📝")
    st.write("Select your essay type, education level, and desired length, then let AI generate an essay for you. ✨")

    # Define essay types and education levels
    essay_types = [
        "📖 Argumentative - Forming an opinion via research. Building an evidence-based argument.",
        "📚 Expository - Knowledge of a topic. Communicating information clearly.",
        "✒️ Narrative - Creative language use. Presenting a compelling narrative.",
        "🎨 Descriptive - Creative language use. Describing sensory details."
    ]

    education_levels = [
        "🏫 Primary School",
        "🏫 High School",
        "🎓 College",
        "🎓 Graduate School"
    ]

    # Define the options for number of pages
    num_pages_options = [
        "📄 Short Form (1-2 pages)",
        "📄📄 Medium Form (3-5 pages)",
        "📄📄📄 Long Form (6+ pages)"
    ]

    # Create columns for input fields
    col1, col2 = st.columns(2)

    with col1:
        # Ask the user for the title of the essay
        essay_title = st.text_input("📝 Essay Title", placeholder="Enter the title of your essay", help="Provide a clear and concise title for your essay.")
        
        # Ask the user for type of essay
        selected_essay_type = st.selectbox("📚 Type of Essay", options=essay_types, help="Choose the type of essay you want to write.")

    with col2:
        # Ask the user for level of education
        selected_education_level = st.selectbox("🎓 Level of Education", options=education_levels, help="Choose your level of education.")
        
        # Ask the user for number of pages
        selected_num_pages = st.selectbox("📄 Number of Pages", options=num_pages_options, help="Select the length of your essay.")

    if st.button("🚀 Generate Essay"):
        if essay_title:
            st.success("Generating your essay... ✨")
            ai_essay_generator(essay_title, selected_essay_type, selected_education_level, selected_num_pages)
        else:
            st.error("Please enter a valid title for your essay. 🚫")


def ai_news_writer():
    """ AI News Writer """
    st.markdown("<h1>📰 AI News Writer 🗞️ </h1>", unsafe_allow_html=True)

    # Input for news keywords
    news_keywords = st.text_input(
        "**🔑 Enter Keywords from News Headlines:**",
        placeholder="Describe the News article in 3-5 words. Enter main keywords describing the News Event:",
        help="Enter at least two words for better results."
    )

    if news_keywords and len(news_keywords.split()) < 2:
        st.error("🚫 News keywords should be at least two words long. Least, you can do..")

    # Selectbox for country and language
    countries = [
        ("es", "Spain"),
        ("vn", "Vietnam"),
        ("pk", "Pakistan"),
        ("in", "India"),
        ("de", "Germany"),
        ("cn", "China")
    ]

    languages = [
        ("en", "English"),
        ("es", "Spanish"),
        ("vi", "Vietnamese"),
        ("ar", "Arabic"),
        ("hi", "Hindi"),
        ("de", "German"),
        ("zh-cn", "Chinese")
    ]

    col1, col2 = st.columns(2)
    with col1:
        news_country = st.selectbox("**🌍 Select Origin Country of News Event:**", 
                        countries, format_func=lambda x: x[1], help="Which country did the NEWS originate from ?")
    with col2:
        news_language = st.selectbox("**🗣️ Select News Article Language to Search For:**", 
                        languages, format_func=lambda x: x[1], help="Language to output News Article in ?")

    if st.button("📰 Generate News Report"):
        if news_keywords and len(news_keywords.split()) >= 2:
            with st.spinner("Generating News Report... ⏳"):
                try:
                    news_report = ai_news_generation(news_keywords, news_country, news_language)
                    st.success(f"Successfully generated news report on: {news_keywords} 🎉")
                    st.markdown(news_report)
                except Exception as err:
                    st.error(f"Failed to generate news report: {err} ❌")
        else:
            st.error("Please enter valid keywords for the news report. 🚫")


def ai_finance_ta_writer():
    st.markdown("<div class='sub-header'>AI Financial Technical Analysis Writer</div>", unsafe_allow_html=True)

    ticker_symbol = st.text_input(
        "Enter Ticker Symbol for TA:",
        placeholder="Enter a valid Ticker Symbol (Examples: IBM, BABA, HDFCBANK.NS, TATAMOTORS.NS etc)",
        help="Be sure of the ticker symbol. Double-check it! Examples: IBM, BABA, HDFCBANK.NS, TATAMOTORS.NS"
    )

    if st.button("Generate TA Report"):
        if ticker_symbol:
            with st.spinner("Generating TA Report..."):
                try:
                    # Get dashboard instance and generate technical analysis
                    dashboard = get_dashboard()
                    ta_report = dashboard.generate_technical_analysis(ticker_symbol)
                    st.success(f"Successfully generated TA report for: {ticker_symbol}")
                    st.markdown(ta_report)
                except Exception as err:
                    st.error(f"🚫 Check ticker symbol: Failed to write Financial Technical Analysis. Error: {err}")
        else:
            st.error("🚫 Provide a valid Ticker Symbol. Don't waste my time.")

def ai_social_writer():
    # Define social media platforms as radio buttons
    social_media_options = [
        ("facebook", "Facebook"),
        ("linkedin", "LinkedIn"),
        ("twitter", "Twitter"),
        ("instagram", "Instagram"),
        ("youtube", "YouTube")
    ]

    # Selectbox for choosing a platform
    selected_platform = st.radio("Choose a Social Media Platform:", social_media_options, format_func=lambda x: x[1])
    if "facebook" in selected_platform:
        facebook_main_menu()
    elif "linkedin" in selected_platform:
        linkedin_main_menu()
    elif "twitter" in selected_platform:
        run_dashboard()
    elif "instagram" in selected_platform:
        insta_writer()
    elif "youtube" in selected_platform:
        youtube_main_menu()