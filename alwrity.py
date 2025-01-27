import streamlit as st
import os
import json
import base64
from datetime import datetime

from lib.utils.config_manager import save_config
from lib.utils.ui_setup import setup_ui
from lib.utils.api_key_manager import check_all_api_keys
from dotenv import load_dotenv
from lib.utils.content_generators import ai_writers, content_planning_tools, blog_from_keyword, story_input_section, essay_writer, ai_news_writer, ai_finance_ta_writer, write_ai_prod_desc, do_web_research, competitor_analysis, ai_agents_content_planner
from lib.utils.seo_tools import ai_seo_tools
from lib.utils.ui_setup import setup_ui, setup_tabs
from lib.utils.alwrity_utils import ai_agents_team, ai_social_writer
from lib.utils.file_processor import load_image, read_prompts, write_prompts
from lib.utils.voice_processing import record_voice

# Constants for hardcoded values
BLOG_TONE_OPTIONS = ["Casual", "Professional", "How-to", "Beginner", "Research", "Programming", "Social Media", "Customize"]
BLOG_DEMOGRAPHIC_OPTIONS = ["Professional", "Gen-Z", "Tech-savvy", "Student", "Digital Marketing", "Customize"]
BLOG_TYPE_OPTIONS = ["Informational", "Commercial", "Company", "News", "Finance", "Competitor", "Programming", "Scholar"]
BLOG_LANGUAGE_OPTIONS = ["English", "Spanish", "German", "Chinese", "Arabic", "Nepali", "Hindi", "Hindustani", "Customize"]
BLOG_OUTPUT_FORMAT_OPTIONS = ["markdown", "HTML", "plaintext"]
IMAGE_GENERATION_MODEL_OPTIONS = ["stable-diffusion", "dalle2", "dalle3"]
GPT_PROVIDER_OPTIONS = ["google", "openai", "minstral", "deepseek"]
MAX_TOKENS_OPTIONS = [500, 1000, 2000, 4000, 16000, 32000, 64000]
GEOGRAPHIC_LOCATION_OPTIONS = ["us", "in", "fr", "cn"]
SEARCH_LANGUAGE_OPTIONS = ["en", "zn-cn", "de", "hi"]
TIME_RANGE_OPTIONS = ["anytime", "past day", "past week", "past month", "past year"]


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


def handle_custom_input(label, default_options, help_text):
    """
    Handles custom user input for selectbox options.
    
    Args:
        label (str): The label for the selectbox.
        default_options (list): The default options for the selectbox.
        help_text (str): The help text for the selectbox.

    Returns:
        str: The selected or custom input value.
    """
    selected_option = st.selectbox(f"**{label}**", options=default_options, help=help_text)
    if selected_option == "Customize":
        custom_option = st.text_input(f"Enter your {label.lower()}", help=f"Specify your {label.lower()}.")
        if custom_option:
            return custom_option
        else:
            st.warning(f"Please specify your {label.lower()}.")
    return selected_option

def configure_content_personalization():
    """
    Configures the content personalization settings in the sidebar.
    
    Returns:
        dict: A dictionary containing the blog content characteristics.
    """
    st.sidebar.expander("**👷 Content Personalization**")
    blog_length = st.text_input("**Content Length (words)**", value="2000", help="Approximate word count for blogs. Note: Actual length may vary based on GPT provider and max token count.")
    blog_tone = handle_custom_input("Content Tone", BLOG_TONE_OPTIONS, "Select the desired tone for the blog content.")
    blog_demographic = handle_custom_input("Target Audience", BLOG_DEMOGRAPHIC_OPTIONS, "Select the primary audience for the blog content.")
    blog_type = st.selectbox("**Content Type**", options=BLOG_TYPE_OPTIONS, help="Select the category that best describes the blog content.")
    blog_language = handle_custom_input("Content Language", BLOG_LANGUAGE_OPTIONS, "Select the language in which the blog will be written.")
    blog_output_format = st.selectbox("**Content Output Format**", options=BLOG_OUTPUT_FORMAT_OPTIONS, help="Select the format for the blog output.")
    return {
        "Blog Length": blog_length,
        "Blog Tone": blog_tone,
        "Blog Demographic": blog_demographic,
        "Blog Type": blog_type,
        "Blog Language": blog_language,
        "Blog Output Format": blog_output_format
    }

def configure_images_personalization():
    """
    Configures the image personalization settings in the sidebar.
    
    Returns:
        dict: A dictionary containing the blog image details.
    """
    st.sidebar.expander("**🩻 Images Personalization**")
    image_generation_model = st.selectbox("**Image Generation Model**", options=IMAGE_GENERATION_MODEL_OPTIONS, help="Select the model to generate images for the blog.")
    number_of_blog_images = st.number_input("**Number of Blog Images**", value=1, help="Specify the number of images to include in the blog.")
    return {
        "Image Generation Model": image_generation_model,
        "Number of Blog Images": number_of_blog_images
    }

def configure_llm_personalization():
    """
    Configures the LLM (Language Learning Model) personalization settings in the sidebar.
    
    Returns:
        dict: A dictionary containing the LLM options.
    """
    st.sidebar.expander("**🤖 LLM Personalization**")
    gpt_provider = st.selectbox("**GPT Provider**", options=GPT_PROVIDER_OPTIONS, help="Select the provider for the GPT model.")
    model = st.text_input("**Model**", value="gemini-1.5-flash-latest", help="Specify the model version to use from the selected provider.")
    temperature = st.slider("Temperature", min_value=0.1, max_value=1.0, value=0.7, step=0.1, format="%.1f", help="Temperature controls the 'creativity' or randomness of the text generated by GPT.")
    top_p = st.slider("Top-p", min_value=0.0, max_value=1.0, value=0.9, step=0.1, format="%.1f", help="Top-p sampling controls the level of diversity in the generated text.")
    max_tokens = st.selectbox("Max Tokens", options=MAX_TOKENS_OPTIONS, index=MAX_TOKENS_OPTIONS.index(4000), help="Max tokens determine the maximum length of the output sequence generated by a model.")
    n = st.number_input("N", value=1, min_value=1, max_value=10, help="Defines the number of words or characters grouped together in a sequence when analyzing text.")
    frequency_penalty = st.slider("Frequency Penalty", min_value=0.0, max_value=2.0, value=1.0, step=0.1, format="%.1f", help="Influences word selection during text generation, promoting diversity with higher values.")
    presence_penalty = st.slider("Presence Penalty", min_value=0.0, max_value=2.0, value=1.0, step=0.1, format="%.1f", help="Encourages the use of diverse words by discouraging repetition.")
    return {
        "GPT Provider": gpt_provider,
        "Model": model,
        "Temperature": temperature,
        "Top-p": top_p,
        "Max Tokens": max_tokens,
        "N": n,
        "Frequency Penalty": frequency_penalty,
        "Presence Penalty": presence_penalty
    }

def configure_search_engine_personalization():
    """
    Configures the search engine personalization settings in the sidebar.
    
    Returns:
        dict: A dictionary containing the search engine parameters.
    """
    st.sidebar.expander("**🕵️ Search Engine Personalization**")
    geographic_location = st.selectbox("**Geographic Location**", options=GEOGRAPHIC_LOCATION_OPTIONS, help="Select the geographic location for tailoring search results.")
    search_language = st.selectbox("**Search Language**", options=SEARCH_LANGUAGE_OPTIONS, help="Select the language for the search results.")
    number_of_results = st.number_input("**Number of Results**", value=10, max_value=20, min_value=1, help="Specify the number of search results to retrieve.")
    time_range = st.selectbox("**Time Range**", options=TIME_RANGE_OPTIONS, help="Select the time range for filtering search results.")
    include_domains = st.text_input("**Include Domains**", value="", help="List specific domains to include in search results. Leave blank to include all domains.")
    similar_url = st.text_input("**Similar URL**", value="", help="Provide a URL to find similar results. Leave blank if not needed.")
    return {
        "Geographic Location": geographic_location,
        "Search Language": search_language,
        "Number of Results": number_of_results,
        "Time Range": time_range,
        "Include Domains": include_domains,
        "Similar URL": similar_url
    }

def sidebar_configuration():
    """
    Configures the sidebar with various personalization and settings options for the AI Writer application.
    
    The function includes configurations for:
    - Content Personalization
    - Images Personalization
    - LLM Personalization
    - Search Engine Personalization

    The collected inputs are stored in a dictionary and saved to a configuration file.
    """
    st.sidebar.title("🛠️ Personalization & Settings 🏗️")
    
    # Configure content personalization settings
    blog_content_config = configure_content_personalization()
    
    # Configure image personalization settings
    blog_images_config = configure_images_personalization()
    
    # Configure LLM personalization settings
    llm_config = configure_llm_personalization()
    
    # Configure search engine personalization settings
    search_engine_config = configure_search_engine_personalization()

    # Combine all configurations into a dictionary
    config = {
        "Blog Content Characteristics": blog_content_config,
        "Blog Images Details": blog_images_config,
        "LLM Options": llm_config,
        "Search Engine Parameters": search_engine_config
    }

    # Save the configuration whenever a change is made
    save_config(config)


def main():
    #load_environment
    load_dotenv()
    setup_ui()

    if check_all_api_keys():
        setup_environment_paths()
        sidebar_configuration()
        setup_tabs()
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
