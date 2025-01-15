import streamlit as st
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from lib.utils.config_manager import save_config
from lib.utils.ui_setup import setup_ui, setup_tabs
from lib.utils.api_key_manager import check_all_api_keys
from lib.utils.file_processor import read_prompts, write_prompts

# Constants for various options
BLOG_TONE_OPTIONS = ["Casual", "Professional", "How-to", "Beginner", "Research", "Programming", "Social Media", "Customize"]
BLOG_DEMOGRAPHIC_OPTIONS = ["Professional", "Gen-Z", "Tech-savvy", "Student", "Digital Marketing", "Customize"]
BLOG_LANGUAGE_OPTIONS = ["English", "Spanish", "German", "Chinese", "Arabic", "Nepali", "Hindi", "Hindustani", "Customize"]
CONTENT_TYPE_OPTIONS = ["Informational", "Commercial", "Company", "News", "Finance", "Competitor", "Programming", "Scholar"]
OUTPUT_FORMAT_OPTIONS = ["markdown", "HTML", "plaintext"]
IMAGE_MODEL_OPTIONS = ["stable-diffusion", "dalle2", "dalle3"]
GPT_PROVIDER_OPTIONS = ["google", "openai", "minstral"]
GEOGRAPHIC_LOCATION_OPTIONS = ["us", "in", "fr", "cn"]
SEARCH_LANGUAGE_OPTIONS = ["en", "zn-cn", "de", "hi"]
TIME_RANGE_OPTIONS = ["anytime", "past day", "past week", "past month", "past year"]

def get_custom_input(label, options, help_text, placeholder=""):
    """
    Get custom input from the user.

    Parameters:
    - label (str): The label for the input field.
    - options (list): List of options for the select box.
    - help_text (str): Help text for the select box.
    - placeholder (str): Placeholder text for the custom input field.

    Returns:
    - str: The selected or custom input value.
    """
    selection = st.selectbox(f"**{label}**", options=options, help=help_text)
    if selection == "Customize":
        custom_input = st.text_input(f"Enter your {label.lower()}", help=f"Specify your {label.lower()}.", placeholder=placeholder)
        if custom_input:
            selection = custom_input
        else:
            st.warning(f"Please specify your {label.lower()}.")
    return selection

def content_personalization(sb):
    """
    Sidebar content personalization section.

    Parameters:
    - sb: The Streamlit sidebar object.

    Returns:
    - dict: Dictionary containing personalized content configuration.
    """
    with sb.expander("**👷 Content Personalization**"):
        blog_length = sb.text_input("**Content Length (words)**", value="2000", help="Approximate word count for blogs.")
        blog_tone = get_custom_input("Content Tone", BLOG_TONE_OPTIONS, "Select the desired tone for the blog content.")
        blog_demographic = get_custom_input("Target Audience", BLOG_DEMOGRAPHIC_OPTIONS, "Select the primary audience for the blog content.", "Eg. Domain expert, Content creator, Financial expert etc.")
        blog_type = sb.selectbox("**Content Type**", options=CONTENT_TYPE_OPTIONS, help="Select the category that best describes the blog content.")
        blog_language = get_custom_input("Content Language", BLOG_LANGUAGE_OPTIONS, "Select the language in which the blog will be written.")
        blog_output_format = sb.selectbox("**Content Output Format**", options=OUTPUT_FORMAT_OPTIONS, help="Select the format for the blog output.")
        return {
            "Blog Length": blog_length,
            "Blog Tone": blog_tone,
            "Blog Demographic": blog_demographic,
            "Blog Type": blog_type,
            "Blog Language": blog_language,
            "Blog Output Format": blog_output_format
        }

def images_personalization(sb):
    """
    Sidebar images personalization section.

    Parameters:
    - sb: The Streamlit sidebar object.

    Returns:
    - dict: Dictionary containing personalized images configuration.
    """
    with sb.expander("**🩻 Images Personalization**"):
        image_generation_model = sb.selectbox("**Image Generation Model**", options=IMAGE_MODEL_OPTIONS, help="Select the model to generate images for the blog.")
        number_of_blog_images = sb.number_input("**Number of Blog Images**", value=1, help="Specify the number of images to include in the blog.")
        return {
            "Image Generation Model": image_generation_model,
            "Number of Blog Images": number_of_blog_images
        }

def llm_personalization(sb):
    """
    Sidebar LLM personalization section.

    Parameters:
    - sb: The Streamlit sidebar object.

    Returns:
    - dict: Dictionary containing personalized LLM configuration.
    """
    with sb.expander("**🤖 LLM Personalization**"):
        gpt_provider = sb.selectbox("**GPT Provider**", options=GPT_PROVIDER_OPTIONS, help="Select the provider for the GPT model.")
        model = sb.text_input("**Model**", value="gemini-1.5-flash-latest", help="Specify the model version to use from the selected provider.")
        temperature = sb.slider("Temperature", min_value=0.1, max_value=1.0, value=0.7, step=0.1, format="%.1f", help="Controls the 'creativity' or randomness of the text generated.")
        top_p = sb.slider("Top-p", min_value=0.0, max_value=1.0, value=0.9, step=0.1, format="%.1f", help="Controls the level of diversity in the generated text.")
        max_tokens = sb.selectbox("Max Tokens", options=[500, 1000, 2000, 4000, 16000, 32000, 64000], index=3, help="Maximum length of the output sequence generated by a model.")
        n = sb.number_input("N", value=1, min_value=1, max_value=10, help="Defines the number of words or characters grouped together in a sequence.")
        frequency_penalty = sb.slider("Frequency Penalty", min_value=0.0, max_value=2.0, value=1.0, step=0.1, format="%.1f", help="Promotes diversity with higher values.")
        presence_penalty = sb.slider("Presence Penalty", min_value=0.0, max_value=2.0, value=1.0, step=0.1, format="%.1f", help="Encourages the use of diverse words by discouraging repetition.")
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

def search_engine_personalization(sb):
    """
    Sidebar search engine personalization section.

    Parameters:
    - sb: The Streamlit sidebar object.

    Returns:
    - dict: Dictionary containing personalized search engine configuration.
    """
    with sb.expander("**🕵️ Search Engine Personalization**"):
        geographic_location = sb.selectbox("**Geographic Location**", options=GEOGRAPHIC_LOCATION_OPTIONS, help="Select the geographic location for tailoring search results.")
        search_language = sb.selectbox("**Search Language**", options=SEARCH_LANGUAGE_OPTIONS, help="Select the language for the search results.")
        number_of_results = sb.number_input("**Number of Results**", value=10, min_value=1, max_value=20, help="Specify the number of search results to retrieve.")
        time_range = sb.selectbox("**Time Range**", options=TIME_RANGE_OPTIONS, help="Select the time range for filtering search results.")
        include_domains = sb.text_input("**Include Domains**", value="", help="List specific domains to include in search results.")
        similar_url = sb.text_input("**Similar URL**", value="", help="Provide a URL to find similar results.")
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
    Sidebar configuration for personalization and settings.
    This function consolidates various personalization settings into the sidebar.
    """
    sb = st.sidebar
    sb.title("🛠️ Personalization & Settings 🏗️")
    
    content_config = content_personalization(sb)
    images_config = images_personalization(sb)
    llm_config = llm_personalization(sb)
    search_config = search_engine_personalization(sb)

    config = {
        "Blog Content Characteristics": content_config,
        "Blog Images Details": images_config,
        "LLM Options": llm_config,
        "Search Engine Parameters": search_config
    }

    # Save the configuration to a file whenever a change is made
    save_config(config)

def setup_environment_paths():
    """
    Sets up environment paths for saving files and configurations.
    """
    os.environ["SEARCH_SAVE_FILE"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_web_research",
                                                  f"web_research_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
    os.environ["IMG_SAVE_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_content")
    os.environ["CONTENT_SAVE_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_content")
    os.environ["PROMPTS_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_prompts")
    os.environ["ALWRITY_CONFIG"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_config", "main_config.json")

def modify_prompts_sidebar():
    """
    Provides a sidebar for modifying prompts.
    """
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

def main():
    """
    Main function to run the Streamlit app.
    Initializes the environment, checks API keys, sets up paths, and configures the UI.
    """
    load_dotenv()
    setup_ui()

    if check_all_api_keys():
        setup_environment_paths()
        sidebar_configuration()
        setup_tabs()
        modify_prompts_sidebar()

if __name__ == "__main__":
    main()

