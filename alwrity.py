import streamlit as st
import os
import json
import base64
from datetime import datetime

from lib.utils.config_manager import save_config
from lib.utils.ui_setup import setup_ui, sidebar_configuration, setup_sidebar_navigation
from lib.utils.api_key_manager import check_all_api_keys
from dotenv import load_dotenv
from lib.utils.content_generators import ai_writers, content_planning_tools, blog_from_keyword, story_input_section, essay_writer, ai_news_writer, ai_finance_ta_writer, write_ai_prod_desc, do_web_research, competitor_analysis, ai_agents_content_planner
from lib.utils.seo_tools import ai_seo_tools
from lib.utils.alwrity_utils import ai_agents_team, ai_social_writer
from lib.utils.file_processor import load_image, read_prompts, write_prompts
from lib.utils.voice_processing import record_voice
from lib.utils.settings_page import render_settings_page



def process_folder_for_rag(folder_path):
    """Placeholder for the process_folder_for_rag function."""
    st.write(f"This is a placeholder for processing the folder: {folder_path}")


def save_config(config):
    """
    Saves the provided configuration dictionary to a JSON file specified by the environment variable.
    """
    try:
        with open(os.getenv("ALWRITY_CONFIG"), "w") as config_file:
            json.dump(config, config_file, indent=4)
    except Exception as e:
        st.error(f"An error occurred while saving the configuration: {e}")



def main():
    # Initialize session state for page navigation if not exists
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'main'

    # Load environment variables and setup UI
    load_dotenv()
    setup_ui()

    if check_all_api_keys():
        if st.session_state['current_page'] == 'settings':
            # Render settings page
            render_settings_page()
            
            # Add back button
            if st.sidebar.button("← Back to Main", use_container_width=True):
                st.session_state['current_page'] = 'main'
                st.rerun()
        else:
            # Render main app
            setup_environment_paths()
            setup_sidebar_navigation()
            sidebar_configuration()  # This now contains just the settings button
            modify_prompts_sidebar()


def setup_environment_paths():
    """Sets up environment paths for saving files and configurations."""
    os.environ["SEARCH_SAVE_FILE"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_web_research",
                                                  f"web_research_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
    os.environ["IMG_SAVE_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_content")
    os.environ["CONTENT_SAVE_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_content")
    os.environ["PROMPTS_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_prompts")
    os.environ["ALWRITY_CONFIG"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_config", "main_config.json")


def modify_prompts_sidebar():
    """Provides a sidebar for modifying prompts."""
    st.sidebar.title("📝 Modify Prompts")
    prompts = read_prompts()

    if prompts:
        edited_prompts = []
        for i, prompt in enumerate(prompts):
            edited_prompt = st.sidebar.text_area(f"Prompt {i+1}", prompt)
            edited_prompts.append(edited_prompt)

        if st.sidebar.button("Save Prompts"):
            write_prompts(edited_prompts)
            st.sidebar.success("Prompts saved successfully!")
    else:
        st.sidebar.warning("No prompts found in the file.")


# Functions for the main options
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
    st.markdown("""**Alwrity content Ideation & Planning** : Provide few keywords to do comprehensive web research.
             Provide few keywords to get Google, Neural, pytrends analysis. Know keywords, blog titles to target.
             Generate months long content calendar around given keywords.""")
    
    options = [
        "Keywords Researcher",
        "Competitor Analysis",
        "Content Calender Ideator"
    ]
    choice = st.radio("Select a content planning tool:", options, index=0, format_func=lambda x: f"🔍 {x}")
    
    if choice == "Keywords Researcher":
        do_web_research()
    elif choice == "Competitor Analysis":
        competitor_analysis()
    elif choice == "Content Calender Ideator":
        plan_keywords = st.text_input(
            "**Enter Your main Keywords to get 2 months content calendar:**",
            placeholder="Enter 2-3 main keywords to generate AI content calendar with keyword researched blog titles",
            help="The keywords are the ones where you would want to generate 50-60 blogs/articles on."
        )
        if st.button("**Ideate Content Calender**"):
            if plan_keywords:
                ai_agents_content_planner(plan_keywords)
            else:
                st.error("Come on, really, Enter some keywords to plan on..")


def alwrity_brain():
    st.title("🧠 Alwrity Brain, Better than yours!")
    st.write("Choose a folder to write content on. Alwrity will do RAG on these documents. The documents can of any type, pdf, pptx, docs, txt, cs etc. Video files and Audio files are also permitted.")

    folder_path = st.text_input("**Enter folder path:**")
    if st.button("**Process Folder**"):
        if folder_path:
            try:
                process_folder_for_rag(folder_path)
                st.success("Folder processed successfully!")
            except Exception as e:
                st.error(f"Error processing folder: {e}")
        else:
            st.warning("Please enter a valid folder path.")


if __name__ == "__main__":
    main()
