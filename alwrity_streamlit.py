import os
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st

# Load .env file
load_dotenv()

from lib.utils.alwrity_streamlit_utils import (
        blog_from_keyword, ai_agents_team, 
        blog_from_audio, write_story,
        essay_writer, ai_news_writer,
        ai_finance_ta_writer, ai_social_writer
        )

# Custom CSS for styling
st.markdown(
    """
    <style>
    div.row-widget.stRadio > div {
        flex-direction: row;
        align-items: stretch;
    }

    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"]  {
        background-color: #9AC5F4;
        padding-right: 10px;
        padding-left: 4px;
        padding-bottom: 3px;
        margin: 4px;
    }
    body {
        background: #f9f9f9;
        background-image: linear-gradient(to bottom right, #f0f8ff, #e3f2fd);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #2196F3;
        margin-bottom: 10px;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    .stApp {
        margin-top: -80px;
    }
    .sub-header {
        font-size: 1.75em;
        font-weight: bold;
        color: #ff6347;
        margin-top: 40px;
        margin-bottom: 10px;
        text-align: center;
    }
    .option-box {
        border: 2px solid #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 12px #aaaaaa;
        background-color: #f5f5f5;
    }
    .button {
	    background: #ff6347; /* Orange */
	    color: white;
	    border: none;
	    padding: 10px 20px;
	    border-radius: 5px; /* Rounded corners */
	    text-align: center;
	    text-decoration: none;
	    display: inline-block;
	    font-size: 16px;
	    margin: 10px 2px;
	    cursor: pointer;
	    transition: background-color 0.3s ease; /* Smooth transition for hover effect */
	    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Add a subtle shadow */
	    font-weight: bold; /* Make the text bold */
    }

    .button:hover {
        background-color: #ff4d4d; /* Darker orange */
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3); /* Slightly larger shadow on hover */
    }
    .stTabs [role="tab"] {
        font-size: 1.2em;
        font-weight: bold;
        color: white;
        background: #673AB7;
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
        border: 2px solid #ddd;
        transition: background 0.3s ease;
    }
    .stTabs [role="tab"]:hover {
        background: #9575CD;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background: #D1C4E9;
        color: #333;
        border: 2px solid #673AB7;
    }
    .sidebar-header {
        font-size: 1.5em;
        font-weight: bold;
        color: #333;
        margin-bottom: 20px;
    }
    .sidebar-option {
        margin-bottom: 10px;
        font-size: 1.2em;
        color: #2196F3;
    }
    .content-section {
        padding: 20px;
        margin-bottom: 30px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px #ddd;
        background-color: #f8f8f8;
    }
    .content-title {
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 10px;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to check if API keys are present and prompt user to input if not
def check_api_keys():
    api_keys = {
        "METAPHOR_API_KEY": "Metaphor AI Key (Get it here: https://dashboard.exa.ai/login)",
        "TAVILY_API_KEY": "Tavily AI Key (Get it here: https://tavily.com/#api)",
        "SERPER_API_KEY": "Serper API Key (Get it here: https://serper.dev/signup)"
    }
    missing_keys = []

    for key, description in api_keys.items():
        if os.getenv(key) is None:
            missing_keys.append((key, description))

    if missing_keys:
        st.warning(f"API keys are missing. Please provide them below:{missing_keys}")
        for key, description in missing_keys:
            api_key = st.text_input(f"Enter {key}:", placeholder=description, help=description)
            if api_key:
                with open(".env", "a") as env_file:
                    env_file.write(f"{key}={api_key}\n")
                os.environ[key] = api_key
                st.success(f"{key} added successfully! Enter to Continue..")
        return False
    return True


# Function to check LLM provider and API key
def check_llm_environs():
    gpt_provider = os.getenv("GPT_PROVIDER")
    supported_providers = ['google', 'openai', 'mistralai']

    if gpt_provider is None or gpt_provider.lower() not in map(str.lower, supported_providers):
        gpt_provider = st.selectbox(
            "Select your LLM Provider",
            options=["google", "openai", "mistralai"],
            help="Select from 'google', 'openai', 'mistralai'"
        )
        os.environ["GPT_PROVIDER"] = gpt_provider
        with open(".env", "a") as env_file:
            env_file.write(f"GPT_PROVIDER={gpt_provider}\n")
        st.success(f"GPT Provider set to {gpt_provider}")

    api_key_var = ""
    if gpt_provider.lower() == "google":
        api_key_var = "GEMINI_API_KEY"
        missing_api_msg = "To get your Gemini API key, please visit: https://aistudio.google.com/app/apikey"
    elif gpt_provider.lower() == "openai":
        api_key_var = "OPENAI_API_KEY"
        missing_api_msg = "To get your OpenAI API key, please visit: https://openai.com/blog/openai-api"
    elif gpt_provider.lower() == "mistralai":
        api_key_var = "MISTRAL_API_KEY"
        missing_api_msg = "To get your MistralAI API key, please visit: https://mistralai.com/api"

    if os.getenv(api_key_var) is None:
        api_key = st.text_input(f"Enter {api_key_var}:", placeholder=missing_api_msg, help=missing_api_msg)
        if api_key:
            with open(".env", "a") as env_file:
                env_file.write(f"{api_key_var}={api_key}\n")
            os.environ[api_key_var] = api_key
            st.success(f"{api_key_var} added successfully! Enter to continue..")
        return False
    return True


# Sidebar configuration
def sidebar_configuration():
    st.sidebar.title("🛠️ Alwrity Configuration 🏗️")

    with st.sidebar.expander("👷 Blog Content Characteristics"):
        st.text_input("**Blog Length**", value="2000", 
                      help="Length of blogs Or word count. Note: It won't be exact and depends on GPT providers and Max token count.")
        st.text_input("**Blog Tone**", value="Casual", 
                      help="Professional, how-to, beginner, research, programming, casual, etc.")
        st.text_input("Blog Demographic", value="Content creators & Digital marketing", 
                      help="Target Audience, Gen-Z, Tech-savvy, Working professional, students, kids, etc.")
        st.text_input("Blog Type", value="Informational", 
                      help="Informational, commercial, company, news, finance, competitor, programming, scholar, etc.")
        st.text_input("Blog Language", value="English", 
                      help="Spanish, German, Chinese, Arabic, Nepali, Hindi, Hindustani, etc.")
        st.text_input("Blog Output Format", value="markdown", 
                      help="Specify the output format of the blog as: HTML, markdown, plaintext. Defaults to markdown.")

    with st.sidebar.expander("🩻 Blog Images Details"):
        st.text_input("Image Generation Model", value="stable-diffusion", help="Options are dalle2, dalle3, stable-diffusion.")
        st.number_input("Number of Blog Images", value=1, help="Number of blog images to include.")

    with st.sidebar.expander("🤖 LLM Options"):
        st.text_input("GPT Provider", value="google", help="Choose one of the following: Openai, Google, Minstral.")
        st.text_input("Model", value="gemini-1.5-flash-latest", help="Mention which model of the above provider to use.")
        st.number_input("Temperature", value=0.7, 
                        help="""Temperature controls the 'creativity' or randomness of the text generated by GPT. 
                        Greater determinism with higher values indicating more randomness.""")
        st.number_input("Top-p", value=0.9, help="Top-p sampling controls the level of diversity in the generated text.")
        st.number_input("Max Tokens", value=4096, help="Max tokens determine the maximum length of the output sequence generated by a model.")
        st.number_input("N", value=1, help="Defines the number of words or characters grouped together in a sequence when analyzing text.")
        st.number_input("Frequency Penalty", value=1, 
                        help="Influences word selection during text generation, promoting diversity with higher values.")
        st.number_input("Presence Penalty", value=1, help="Encourages the use of diverse words by discouraging repetition.")

    with st.sidebar.expander("🕵️ Search Engine Parameters"):
        st.text_input("Geographic Location", value="us", 
                      help="Geo location restricts the web search to a given country. Examples are us for United States, in for India, fr for France, cn for China, etc.")
        st.text_input("Search Language", value="en", 
                      help="Define the language you want search results in. Example: en for English, zn-cn for Chinese, de for German, hi for Hindi, etc.")
        st.number_input("Number of Results", value=10, help="Number of Google search results to fetch.")
        st.text_input("Time Range", value="anytime", 
                      help="Acceptable values: past day, past week, past month, past year. Limits the search results for a given time duration from today.")
        st.text_input("Include Domains", value="", 
                      help="A list of domains to specifically include in the search results. Default is None, which includes all domains.")
        st.text_input("Similar URL", value="", help="A single URL that instructs search engines to give results similar to the given URL.")

# Function to read prompts from the file
def read_prompts(file_path="prompt_llm.txt"):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            prompts = file.readlines()
        return [prompt.strip() for prompt in prompts]
    return []

# Function to write prompts to the file
def write_prompts(prompts, file_path="prompt_llm.txt"):
    with open(file_path, "w") as file:
        for prompt in prompts:
            file.write(f"{prompt}\n")

def main():
    st.markdown("<div class='main-header'>Welcome to Alwrity!</div>", unsafe_allow_html=True)
    # Export the paths and file names. Dont want alwrity to be chatty and prompt for inputs.
    os.environ["SEARCH_SAVE_FILE"] = os.path.join(os.getcwd(), "lib", "workspace", "web_research_report",
                                                  f"web_research_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
    os.environ["IMG_SAVE_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "generated_content")
    os.environ["CONTENT_SAVE_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "generated_content")
    os.environ["PROMPTS_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "prompts")

    # Check API keys and LLM environment settings
    api_keys_valid = check_api_keys()
    llm_environs_valid = check_llm_environs()

    if api_keys_valid and llm_environs_valid:
        # Clear previous messages and display the sidebar configuration
        sidebar_configuration()
    else:
        st.error("Error loading Environment variables.")
        st.stop()

    # Define the tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["AI Writers", "Content Planning", "Agents Content Teams", "Alwrity Brain", "Ask Alwrity"])
    with tab1:
        write_blog()

    with tab2:
        content_planning_tools()

    with tab3:
        ai_agents_team()

    with tab4:
        alwrity_brain()

    with tab5:
        st.title("🙎 Ask Alwrity 🤦")
        st.write("Oh, you decided to talk to a chatbot? I guess even Netflix can't... Shall we get this over with?")
    
    # Sidebar for prompt modification
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
def write_blog():
    options = [
        "Write from few keywords",
        "Write from audio files",
        "Story Writer",
        "Essay writer",
        "Write News reports",
        "Write Financial TA report",
        "AI Social writer (instagram, tweets, linkedin, facebook post)",
        "AI Copywriter",
        "Quit"
    ]
    choice = st.selectbox("**Select a content creation type:**", options, index=0, format_func=lambda x: f"📝 {x}")

    if choice == "Write from few keywords":
        blog_from_keyword()
    elif choice == "Write from audio files":
        blog_from_audio()
    elif choice == "Story Writer":
        write_story()
    elif choice == "Essay writer":
        essay_writer()
    elif choice == "Write News reports":
        ai_news_writer()
    elif choice == "Write Financial TA report":
        ai_finance_ta_writer()
    elif choice == "AI Social writer (instagram, tweets, linkedin, facebook post)":
        ai_social_writer()
    elif choice == "Quit":
        st.write("Exiting, Getting Lost. But.... I have nowhere to go 🥹🥹")


def content_planning_tools():
    st.markdown("<div class='sub-header'>Content Planning</div>", unsafe_allow_html=True)
    st.markdown("""**Alwrity content Ideation & Planning** : Provide few keywords to do comprehensive web research.
             Provide few keywords to get Google, Neural, pytrends analysis. Know keywords, blog titles to target.
             Generate months long content calender around given keywords.""")
    options = [
        "Keywords web research🤓",
        "Competitor Analysis🧐",
        "Give me content calendar 🥹🥹"
    ]
    choice = st.selectbox("Select a content planning tool:", options, index=0, format_func=lambda x: f"🔍 {x}")

    if st.button("Plan Content"):
        if choice == "Keywords web research🤓":
            do_web_research()
        elif choice == "Competitor Analysis🧐":
            competitor_analysis()
        elif choice == "Give me content calendar 🥹🥹":
            content_planning_agents()


def alwrity_brain():
    st.title("🖕 Alwrity Brain, Better than yours!")
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

