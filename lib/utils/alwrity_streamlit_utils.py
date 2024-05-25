import os
import streamlit as st
from pathlib import Path
import configparser
from datetime import datetime

from rich import print
from lib.ai_web_researcher.gpt_online_researcher import gpt_web_researcher
from lib.ai_web_researcher.metaphor_basic_neural_web_search import metaphor_find_similar
from lib.ai_writers.keywords_to_blog_streamlit import write_blog_from_keywords
from lib.ai_writers.speech_to_blog.main_audio_to_blog import generate_audio_blog
from lib.ai_writers.long_form_ai_writer import long_form_generator
from lib.ai_writers.ai_news_article_writer import ai_news_generation
from lib.ai_writers.ai_agents_crew_writer import ai_agents_writers
from lib.ai_writers.ai_financial_writer import write_basic_ta_report
from lib.ai_writers.facebook_ai_writer import facebook_post_writer
from lib.ai_writers.linkedin_ai_writer import linked_post_writer
from lib.ai_writers.twitter_ai_writer import tweet_writer 
from lib.ai_writers.insta_ai_writer import insta_writer
from lib.ai_writers.youtube_ai_writer import write_yt_title, write_yt_description, write_yt_script
from lib.gpt_providers.text_generation.ai_story_writer import ai_story_generator
from lib.gpt_providers.text_generation.ai_essay_writer import ai_essay_generator
from lib.gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image
from lib.content_planning_calender.content_planning_agents_alwrity_crew import ai_agents_planner



def blog_from_keyword():
    """ Input blog keywords, research and write a factual blog."""
    st.markdown("<div class='sub-header'>Blog from Keywords</div>", unsafe_allow_html=True)

    content_keywords = st.text_input('Enter Keywords/Blog Title',
            help='Check your keywords against Google search, if you get good search results, you will get good content with Alwrity.',
            placeholder='Shit in, Shit Out; Better keywords, better research, hence better content.\n👋 :')

    if content_keywords and len(content_keywords.split()) < 2:
        st.error('🚫 Blog keywords should be at least two words long. Please try again.')

    content_type = st.selectbox("Select content type:", ["Normal-length content", "Long-form content", "Experimental - AI Agents team"])
    if st.button("Write Blog"):
        # Clear the previous results from the screen
        st.empty()
        if content_keywords and len(content_keywords.split()) >= 2:
            if content_type == "Normal-length content":
                try:
                    short_blog = write_blog_from_keywords(content_keywords)
                    st.markdown(short_blog)
                    st.success(f"Successfully wrote blog on: {content_keywords}")
                except Exception as err:
                    st.error(f"🚫 Failed to write blog on {content_keywords}, Error: {err}")
            elif content_type == "Long-form content":
                try:
                    st.empty()
                    long_form_generator(content_keywords)
                    st.success(f"Successfully wrote long-form blog on: {content_keywords}")
                except Exception as err:
                    st.error(f"🚫 Failed to write blog on {content_keywords}, Error: {err}")
            elif content_type == "Experimental - AI Agents team":
                try:
                    ai_agents_writers(content_keywords)
                    st.success(f"Successfully wrote content with AI agents on: {content_keywords}")
                except Exception as err:
                    st.error(f"🚫 Failed to Write content with AI agents: {err}")


def ai_agents_team():
    # Define options for AI Content Teams
    st.title("🧚🐲 AI Agents Content Teams")
    st.markdown("""Alwrity offers AI agents team for content creators to easily modify them for their needs.
                Abstracting tech & plumbing, easily define role, goal, task. Use different AI agents framework.""")
    options = [
        "AI Content Ideation & Planning Team",
        "AI Content Creation Team"
    ]

    # Selectbox for choosing an AI Content Team
    selected_team = st.selectbox("**Choose AI Agents Team:**", options)

    if selected_team == "AI Content Ideation & Planning Team":
        content_planning_agents()
    elif selected_team == "AI Content Creation Team":
        content_creation_agents()


def content_creation_agents():
    st.markdown("<div class='sub-header'>AI Agents Team for Content Creation</div>", unsafe_allow_html=True)
    content_keywords = st.text_input(
        "Enter Main Domain Keywords of your business:",
        placeholder="Better keywords, Better content calendar:",
        help="These keywords define your main business sector, blogging niche, Industry, domain etc"
    )

    if st.button("Start Writing"):
        if content_keywords and len(content_keywords.split()) >= 2:
            with st.spinner("Generating Content..."):
                try:
                    calendar_content = ai_agents_writers(content_keywords)
                    st.success(f"Successfully generated content for: {content_keywords}")
                    st.markdown(calendar_content)
                except Exception as err:
                    st.error(f"Failed to generate content with AI Agents: {err}")
        else:
            st.error("🚫 Single keywords are just too vague. Try again.")


def content_planning_agents():
    st.markdown("<div class='sub-header'>AI Agents Team for Content Ideation</div>", unsafe_allow_html=True)
    content_keywords = st.text_input(
        "Enter Main Domain Keywords of your business:",
        placeholder="Better keywords will generate better content calendar:",
        help="Enter at least two words for better results."
    )

    if st.button("Generate Content Plan"):
        if content_keywords and len(content_keywords.split()) >= 2:
            with st.spinner("Generating Content Plan..."):
                try:
                    plan_content = ai_agents_planner(content_keywords)
                    st.success(f"Successfully generated content plan for: {content_keywords}")
                    st.markdown(plan_content)
                except Exception as err:
                    st.error(f"Failed to generate content plan: {err}")
        else:
            st.error("🚫 Single keywords are just too vague. Try again.")



def blog_from_audio():
    """
    Prompt the user to input either a YouTube URL, a file location, or keywords to search on YouTube.
    Validate the input and take appropriate actions based on the input type.
    """
    st.title("Audio Blog Generator 🎤📝")
    st.write("Generate a blog from an audio input. You can provide a YouTube URL or upload an audio file from your local folder.")

    # Toggle button to choose input method
    input_method = st.radio(
        "Choose input method:",
        ('YouTube URL', 'Upload Audio File')
    )

    if input_method == 'YouTube URL':
        youtube_url = st.text_input("Enter YouTube video URL", placeholder="https://www.youtube.com/...")
        if st.button("Generate Blog"):
            if youtube_url:
                if youtube_url.startswith("https://www.youtube.com/") or youtube_url.startswith("http://www.youtube.com/"):
                    st.success("Valid YouTube URL provided. Processing...")
                    generate_audio_blog(youtube_url)
                else:
                    st.error("Invalid YouTube URL. Please enter a valid URL.")
            else:
                st.error("Please enter a YouTube URL to generate a blog.")
    else:
        uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])
        if st.button("Generate Blog"):
            if uploaded_file:
                file_path = os.path.join("uploads", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"File {uploaded_file.name} uploaded successfully. Processing...")
                generate_audio_blog(file_path)
            else:
                st.error("Please upload an audio file to generate a blog.")

def write_story():
    """ Alwrity AI Story Writer """

    personas = [
        "Award-Winning Science Fiction Author",
        "Historical Fiction Author",
        "Fantasy World Builder",
        "Mystery Novelist",
        "Romantic Poet",
        "Thriller Writer",
        "Children's Book Author",
        "Satirical Humorist",
        "Biographical Writer",
        "Dystopian Visionary",
        "Magical Realism Author"
    ]

    persona_descriptions = {
        "Award-Winning Science Fiction Author": "You are an award-winning science fiction author with a penchant for expansive, intricately woven stories. Your ultimate goal is to write the next award-winning sci-fi novel.",
        "Historical Fiction Author": "You are a seasoned historical fiction author, meticulously researching past eras to weave captivating narratives. Your goal is to transport readers to different times and places through your vivid storytelling.",
        "Fantasy World Builder": "You are a world-building enthusiast, crafting intricate realms filled with magic, mythical creatures, and epic quests. Your ambition is to create the next immersive fantasy saga that captivates readers' imaginations.",
        "Mystery Novelist": "You are a master of suspense and intrigue, intricately plotting out mysteries with unexpected twists and turns. Your aim is to keep readers on the edge of their seats, eagerly turning pages to unravel the truth.",
        "Romantic Poet": "You are a romantic at heart, composing verses that capture the essence of love, longing, and human connections. Your dream is to write the next timeless love story that leaves readers swooning.",
        "Thriller Writer": "You are a thrill-seeker, crafting adrenaline-pumping tales of danger, suspense, and high-stakes action. Your mission is to keep readers hooked from start to finish with heart-pounding thrills and unexpected twists.",
        "Children's Book Author": "You are a storyteller for the young and young at heart, creating whimsical worlds and lovable characters that inspire imagination and wonder. Your goal is to spark joy and curiosity in young readers with enchanting tales.",
        "Satirical Humorist": "You are a keen observer of society, using humor and wit to satirize the absurdities of everyday life. Your aim is to entertain and provoke thought, delivering biting social commentary through clever and humorous storytelling.",
        "Biographical Writer": "You are a chronicler of lives, delving into the stories of real people and events to illuminate the human experience. Your passion is to bring history to life through richly detailed biographies that resonate with readers.",
        "Dystopian Visionary": "You are a visionary writer, exploring dark and dystopian futures that reflect contemporary fears and anxieties. Your vision is to challenge societal norms and provoke reflection on the path humanity is heading.",
        "Magical Realism Author": "You are a purveyor of magical realism, blending the ordinary with the extraordinary to create enchanting and thought-provoking tales. Your goal is to blur the lines between reality and fantasy, leaving readers enchanted and introspective."
    }

    st.title("Alwrity AI Story Writer ✍️")
    st.write("Select your story writing persona or book genre and let AI help you craft an amazing story. 🌟")

    # Select persona
    selected_persona_name = st.selectbox(
        "Select Your Story Writing Persona or Book Genre:",
        options=personas,
        help="Choose a persona that resonates with the style you want the AI Story Writer to adopt."
    )

    # Display persona description
    if selected_persona_name:
        st.info(persona_descriptions[selected_persona_name])

    # Combined input for characters and plot details
    story_details_input = st.text_area(
        "Enter characters and plot details for your story:",
        placeholder="E.g., Characters: John, Alice, Dragon, Detective\nPlot: A detective is trying to solve a mystery in a small town...",
        help="Provide a list of characters and a brief outline of the plot for your story."
    )

    # Generate story button
    if st.button("Generate Story"):
        if selected_persona_name and story_details_input:
            st.success(f"Generating story for {selected_persona_name} with the provided details.")
            ai_story_generator(selected_persona_name, persona_descriptions[selected_persona_name], story_details_input)
        else:
            st.error("Please select a persona and enter the story details to generate a story.")



def essay_writer():
    st.title("AI Essay Writer 📝")
    st.write("Select your essay type, education level, and desired length, then let AI generate an essay for you. ✨")

    # Define essay types and education levels
    essay_types = [
        "Argumentative - Forming an opinion via research. Building an evidence-based argument.",
        "Expository - Knowledge of a topic. Communicating information clearly.",
        "Narrative - Creative language use. Presenting a compelling narrative.",
        "Descriptive - Creative language use. Describing sensory details."
    ]

    education_levels = [
        "Primary School",
        "High School",
        "College",
        "Graduate School"
    ]

    # Define the options for number of pages
    num_pages_options = [
        "Short Form (1-2 pages)",
        "Medium Form (3-5 pages)",
        "Long Form (6+ pages)"
    ]

    # Create columns for inputs
    col1, col2, = st.columns(2)

    with col1:
        # Ask the user for the title of the essay
        essay_title = st.text_input("Essay Title", placeholder="Enter the title of your essay", help="Provide a clear and concise title for your essay.")

    with col2:
        # Ask the user for type of essay
        selected_essay_type = st.selectbox("Type of Essay", options=essay_types, help="Choose the type of essay you want to write.")

    # Create another row for number of pages
    col3, col4 = st.columns(2)
    with col3:
        # Ask the user for level of education
        selected_education_level = st.selectbox("Level of Education", options=education_levels, help="Choose your level of education.")

    with col4:
        # Prompt the user to select the length of the essay
        selected_num_pages = st.selectbox("Number of Pages", options=num_pages_options, help="Select the length of your essay.")

    st.markdown("### Generate Your Essay")

    if st.button("Generate Essay"):
        if essay_title:
            st.success("Generating your essay...")
            ai_essay_generator(essay_title, selected_essay_type, selected_education_level, selected_num_pages)
        else:
            st.error("Please enter a valid title for your essay.")


def essay_writerrererr():
    st.title("AI Essay Writer 📝")
    st.write("Select your essay type, education level, and desired length, then let AI generate an essay for you. ✨")

    # Define essay types and education levels
    essay_types = [
        "Argumentative - Forming an opinion via research. Building an evidence-based argument.",
        "Expository - Knowledge of a topic. Communicating information clearly.",
        "Narrative - Creative language use. Presenting a compelling narrative.",
        "Descriptive - Creative language use. Describing sensory details."
    ]

    education_levels = [
        "Primary School",
        "High School",
        "College",
        "Graduate School"
    ]

    # Define the options for number of pages
    num_pages_options = [
        "Short Form (1-2 pages)",
        "Medium Form (3-5 pages)",
        "Long Form (6+ pages)"
    ]

    # Ask the user for the title of the essay
    essay_title = st.text_input("Essay Title", placeholder="Enter the title of your essay", help="Provide a clear and concise title for your essay.")

    # Ask the user for type of essay, level of education, and number of pages
    selected_essay_type = st.selectbox("Type of Essay", options=essay_types, help="Choose the type of essay you want to write.")
    selected_education_level = st.selectbox("Level of Education", options=education_levels, help="Choose your level of education.")
    selected_num_pages = st.selectbox("Number of Pages", options=num_pages_options, help="Select the length of your essay.")

    if st.button("Generate Essay"):
        if essay_title:
            st.success("Generating your essay...")
            ai_essay_generator(essay_title, selected_essay_type, selected_education_level, selected_num_pages)
        else:
            st.error("Please enter a valid title for your essay.")


def ai_news_writer():
    """ AI News Writer """
    st.markdown("<div class='sub-header'>AI News Writer</div>", unsafe_allow_html=True)

    news_keywords = st.text_input(
        "Enter Keywords from News Headlines:",
        placeholder="Describe the News article in 3-5 words. Enter main keywords describing the News Event:",
        help="Enter at least two words for better results."
    )

    if news_keywords and len(news_keywords.split()) <= 2:
        st.error("🚫 News keywords should be at least two words long. Least, you can do..")

    # Selectbox for country
    countries = [
        ("es", "Spain"),
        ("vn", "Vietnam"),
        ("pk", "Pakistan"),
        ("in", "India"),
        ("de", "Germany"),
        ("cn", "China")
    ]

    # Selectbox for language
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
        news_country = st.selectbox("Select Origin Country of News Event:", countries, format_func=lambda x: x[1])
    with col2:
        news_language = st.selectbox("Select News Article Language to search for:", languages, format_func=lambda x: x[1])

    if st.button("Generate News Report"):
        with st.spinner("Generating News Report..."):
            try:
                news_report = ai_news_generation(news_keywords, news_country, news_language)
                st.success(f"Successfully generated news report on: {news_keywords}")
                st.markdown(news_report)
            except Exception as err:
                st.error(f"Failed to generate news report: {err}")


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
                    ta_report = write_basic_ta_report(ticker_symbol)
                    st.success(f"Successfully generated TA report for: {ticker_symbol}")
                    st.markdown(ta_report)
                except Exception as err:
                    st.error(f"🚫 Check ticker symbol: Failed to write Financial Technical Analysis. Error: {err}")
        else:
            st.error("🚫 Provide a valid Ticker Symbol. Don't waste my time.")

def ai_social_writer():
    st.write("Welcome!  Let's craft some engaging content for your social media.  Choose a platform and let the AI do the rest.")

    # Define social media platforms as radio buttons
    social_media_options = [
        ("facebook", "Facebook"),
        ("linkedin", "LinkedIn"),
        ("twitter", "Twitter"),
        ("instagram", "Instagram"),
        ("youtube", "YouTube")  # Add YouTube
    ]

    # Selectbox for choosing a platform
    selected_platform = st.selectbox("Choose a Social Media Platform:", social_media_options, format_func=lambda x: x[1])
    if "facebook" in selected_platform:
        facebook_post_writer()
    elif "linkedin" in selected_platform:
        linked_post_writer()
    elif "twitter" in selected_platform:
        tweet_writer()
    elif "instagram" in selected_platform:
        insta_writer()
#    elif "youtube" in selected_platform:
#        options = ["Write YT Description", "Write YT Title", "Write YT Script"]
#        selected_option = st.radio("", options)
#
#        if selected_option == "Write YT Description":
#            write_yt_description()
#        elif selected_option == "Write YT Title":
#            write_yt_title()
#        elif selected_option == "Write YT Script":
#            write_yt_script()
