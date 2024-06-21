import os
import json
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st
import base64

# Load .env file
load_dotenv()

#from lib.chatbot_custom.chatbot_local_docqa import alwrity_chat_docqa
from lib.utils.alwrity_utils import (blog_from_keyword, ai_agents_team, 
        write_story, essay_writer, ai_news_writer,
        ai_finance_ta_writer, ai_social_writer,
        do_web_research, competitor_analysis,
        )



# Function to check if API keys are present and prompt user to input if not
def check_api_keys():
    api_keys = {
        "METAPHOR_API_KEY": "[Get Metaphor AI Key](https://dashboard.exa.ai/login)",
        "TAVILY_API_KEY": "[Get Tavily AI Key](https://tavily.com/#api)",
        "SERPER_API_KEY": "[Get Serper API Key](https://serper.dev/signup)",
        "STABILITY_API_KEY": "[Get Stability API Key Here](https://platform.stability.ai/)",
        "FIRECRAWL_API_KEY": "[Get Firecrawl API key Here](https://www.firecrawl.dev/account)"
    }
    missing_keys = []

    for key, description in api_keys.items():
        if os.getenv(key) is None:
            missing_keys.append((key, description))

    if missing_keys:
        st.error("🚨 Some API keys are missing! Please provide them below: 🚨")
        
        new_keys = []
        for key, description in missing_keys:
            api_key = st.text_input(f"Enter 🔏 {key}: 👉{description}👈", placeholder=description, help=description)
            if api_key:
                new_keys.append((key, api_key))
        
        if new_keys:
            with open(".env", "a") as env_file:
                for key, api_key in new_keys:
                    env_file.write(f"{key}={api_key}\n")
                    os.environ[key] = api_key
                    st.success(f"✅ {key} added successfully! Press Enter to continue.")
        
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


# Function to save configuration to a file
def save_config(config):
    with open(os.getenv("ALWRITY_CONFIG"), "w") as config_file:
        json.dump(config, config_file, indent=4)


# Sidebar configuration
def sidebar_configuration():
    st.sidebar.title("🛠️ Personalization 🏗️")

    with st.sidebar.expander("**👷 Content Personalization**"):
        blog_length = st.text_input("**Content Length**", value="2000", 
                          help="Length of blogs Or word count. Note: It won't be exact and depends on GPT providers and Max token count.")
        
        blog_tone_options = ["Casual", "Professional", "How-to", "Beginner", "Research", "Programming", "Social Media", "Customize"]
        blog_tone = st.selectbox("**Content Tone**",
                          options=blog_tone_options,
                          help="Choose the tone of the blog.")

        if blog_tone == "Customize":
            custom_tone = st.text_input("Enter the tone of your content", help="Specify the tone of your content.")
            if custom_tone:
                blog_tone = custom_tone
            else:
                st.warning("Please specify the tone of your content.")
        
        blog_demographic_options = ["Professional", "Gen-Z", "Tech-savvy", "Student", "Digital Marketing", "Customize"]
        
        blog_demographic = st.selectbox("Target Audience",
                                options=blog_demographic_options,
                                help="Choose the target audience.")
        if blog_demographic == "Customize":
            custom_demographic = st.text_input("Enter your target audience", 
                                help="Specify your target audience.",
                                placeholder="Eg. Domain expert, Content creator, Financial expert etc..")
            if custom_demographic:
                blog_demographic = custom_demographic
            else:
                st.warning("Please specify your target audience.")
        
        blog_type = st.selectbox("Content Type", 
                          options=["Informational", "Commercial", "Company", "News", "Finance", "Competitor", "Programming", "Scholar"], 
                          help="Choose the type of the blog.")

        blog_language = st.selectbox("Content Language", 
                          options=["English", "Spanish", "German", "Chinese", "Arabic", "Nepali", "Hindi", "Hindustani", "Customize"], 
                          help="Choose the language of the blog.")
        if blog_language == "Customize":
            custom_lang = st.text_input("Enter the language of your choice", help="Specify the content language.")
            if custom_lang:
                blog_language = custom_lang
            else:
                st.warning("Please specify the language of your content.")

        blog_output_format = st.selectbox("Content Output Format", 
                          options=["markdown", "HTML", "plaintext"], 
                          help="Choose the output format of the blog.")

    with st.sidebar.expander("**🩻 Images Personalization**"):
        image_generation_model = st.selectbox("Image Generation Model", 
                          options=["stable-diffusion", "dalle2", "dalle3"], 
                          help="Choose the image generation model.")
        number_of_blog_images = st.number_input("Number of Blog Images", value=1, help="Number of blog images to include.")

    with st.sidebar.expander("**🤖 LLM Personalization**"):
        gpt_provider = st.selectbox("GPT Provider", 
                          options=["google", "openai", "minstral"], 
                          help="Choose the GPT provider.")
        model = st.text_input("Model", value="gemini-1.5-flash-latest", help="Mention which model of the above provider to use.")
        temperature = st.slider(
            "Temperature",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.1,
            format="%.1f",
            help="""Temperature controls the 'creativity' or randomness of the text generated by GPT.
                Greater determinism with higher values indicating more randomness."""
        )

        top_p = st.slider(
            "Top-p",
            min_value=0.0,
            max_value=1.0,
            value=0.9,
            step=0.1,
            format="%.1f",
            help="Top-p sampling controls the level of diversity in the generated text."
        )

        # Selectbox for max tokens
        max_tokens_options = [500, 1000, 2000, 4000, 16000, 32000, 64000]
        max_tokens = st.selectbox(
            "Max Tokens",
            options=max_tokens_options,
            index=max_tokens_options.index(4000),
            help="Max tokens determine the maximum length of the output sequence generated by a model."
        )
        n = st.number_input("N", 
            value=1,
            min_value=1,
            max_value=10,
            help="Defines the number of words or characters grouped together in a sequence when analyzing text.")
        frequency_penalty = st.slider(
            "Frequency Penalty",
            min_value=0.0,
            max_value=2.0,
            value=1.0,
            step=0.1,
            format="%.1f",
            help="Influences word selection during text generation, promoting diversity with higher values."
        )

        presence_penalty = st.slider(
            "Presence Penalty",
            min_value=0.0,
            max_value=2.0,
            value=1.0,
            step=0.1,
            format="%.1f",
            help="Encourages the use of diverse words by discouraging repetition."
        )

    with st.sidebar.expander("**🕵️ Search Engine Personalization**"):
        geographic_location = st.selectbox("Geographic Location", 
                          options=["us", "in", "fr", "cn"], 
                          help="Choose the geo location for the web search.")
        search_language = st.selectbox("Search Language", 
                          options=["en", "zn-cn", "de", "hi"], 
                          help="Choose the language for search results.")
        number_of_results = st.number_input("Number of Results", 
                            value=10,
                            max_value=20,
                            min_value=1,
                            help="Number of Google search results to fetch.")
        time_range = st.selectbox("Time Range", 
                          options=["anytime", "past day", "past week", "past month", "past year"], 
                          help="Choose the time range for search results.")
        include_domains = st.text_input("Include Domains", value="", 
                          help="A list of domains to specifically include in the search results. Default is None, which includes all domains.")
        similar_url = st.text_input("Similar URL", value="", help="A single URL that instructs search engines to give results similar to the given URL.")

    # Storing collected inputs in a dictionary
    config = {
        "Blog Content Characteristics": {
            "Blog Length": blog_length,
            "Blog Tone": blog_tone,
            "Blog Demographic": blog_demographic,
            "Blog Type": blog_type,
            "Blog Language": blog_language,
            "Blog Output Format": blog_output_format
        },
        "Blog Images Details": {
            "Image Generation Model": image_generation_model,
            "Number of Blog Images": number_of_blog_images
        },
        "LLM Options": {
            "GPT Provider": gpt_provider,
            "Model": model,
            "Temperature": temperature,
            "Top-p": top_p,
            "Max Tokens": max_tokens,
            "N": n,
            "Frequency Penalty": frequency_penalty,
            "Presence Penalty": presence_penalty
        },
        "Search Engine Parameters": {
            "Geographic Location": geographic_location,
            "Search Language": search_language,
            "Number of Results": number_of_results,
            "Time Range": time_range,
            "Include Domains": include_domains,
            "Similar URL": similar_url
        }
    }

    # Writing the configuration to a file whenever a change is made
    save_config(config)



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

# Function to load and encode the image file
def load_image(image_path):
    with open(image_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    return b64_string


def main():
    # Use the encoded image in HTML
    # Load and encode the image
    try:
        # Read the CSS file content
        css_file_path = os.path.join('lib', 'workspace', 'alwrity_ui_styling.css')
        with open(css_file_path) as f:
            custom_css = f.read()
        # Set the page configuration
        st.set_page_config(page_title="Alwrity", layout="wide")
        # Inject custom CSS into the Streamlit app
        st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)
    except Exception as err:
        st.error(f"Failed in setting up Alwrity Streamlit UI: {err}")

    image_base64 = load_image("lib/workspace/alwrity_logo.png")
    st.markdown(f"""
    <div class='main-header'>
        <img src='data:image/png;base64,{image_base64}' alt='Alwrity Logo' style='height: 50px; margin-right: 10px; vertical-align: middle;'>
        Welcome to Alwrity!
    </div>
    """, unsafe_allow_html=True)
    
    # Export the paths and file names. Dont want alwrity to be chatty and prompt for inputs.
    os.environ["SEARCH_SAVE_FILE"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_web_research",
                                                  f"web_research_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
    os.environ["IMG_SAVE_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_content")
    os.environ["CONTENT_SAVE_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_content")
    os.environ["PROMPTS_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_prompts")
    os.environ["ALWRITY_CONFIG"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_config", "main_config.json")

    # Check API keys and LLM environment settings
    api_keys_valid = check_api_keys()
    llm_environs_valid = check_llm_environs()

    if api_keys_valid and llm_environs_valid:
        # Clear previous messages and display the sidebar configuration
        sidebar_configuration()

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
            st.info("Chatbot")
            st.markdown("Create a collection by uploading files (PDF, MD, CSV, etc), or crawl a data source (Websites, more sources coming soon.")
            st.markdown("One can ask/chat, summarize and do semantic search over the uploaded data")
            #alwrity_chat_docqa()
    
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
        "AI Blog Writer",
        "Story Writer",
        "Essay writer",
        "Write News reports",
        "Write Financial TA report",
        "AI Social writer (instagram, tweets, linkedin, facebook post)",
        "AI Copywriter",
        "Quit"
    ]
    choice = st.selectbox("**👇Select a content creation type:**", options, index=0, format_func=lambda x: f"📝 {x}")

    if choice == "AI Blog Writer":
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
    st.markdown("""**Alwrity content Ideation & Planning** : Provide few keywords to do comprehensive web research.
             Provide few keywords to get Google, Neural, pytrends analysis. Know keywords, blog titles to target.
             Generate months long content calendar around given keywords.""")
    
    options = [
        "Keywords Researcher",
        "Competitor Analysis",
        "Get Content Calender"
    ]
    choice = st.radio("Select a content planning tool:", options, index=0, format_func=lambda x: f"🔍 {x}")
    
    if choice == "Keywords Researcher":
        do_web_research()
    elif choice == "Competitor Analysis":
        competitor_analysis()
    elif choice == "Get Content Calender":
        planning_agents()


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

