import streamlit as st
import os
import json
import base64
from datetime import datetime
import streamlit as st
from lib.utils.environment_utils import load_environment
from lib.utils.config_manager import save_config
from lib.utils.api_key_manager import check_api_keys, check_llm_environs
from lib.utils.content_generators import ai_writers, content_planning_tools, blog_from_keyword, story_input_section, essay_writer, ai_news_writer, ai_finance_ta_writer, write_ai_prod_desc, competitor_analysis, ai_agents_content_planner
from lib.utils.seo_tools import ai_seo_tools
from lib.utils.alwrity_utils import ai_agents_team, ai_social_writer
from lib.utils.file_processor import load_image, read_prompts, write_prompts
from lib.utils.voice_processing import record_voice

# Placeholder function definitions for missing functions
def blog_from_audio():
    """Placeholder for the blog_from_audio function."""
    st.write("This is a placeholder for the blog_from_audio function.")

def process_folder_for_rag(folder_path):
    """Placeholder for the process_folder_for_rag function."""
    st.write(f"This is a placeholder for processing the folder: {folder_path}")


@st.cache_data
def check_api_keys():
    """
    Checks if the required API keys are present in the environment variables.
    Prompts the user to enter missing keys and saves them in the .env file.
    """
    api_keys = {
        "METAPHOR_API_KEY": "https://dashboard.exa.ai/login",
        "TAVILY_API_KEY": "https://tavily.com/#api",
        "SERPER_API_KEY": "https://serper.dev/signup",
        "STABILITY_API_KEY": "https://platform.stability.ai/",
        "FIRECRAWL_API_KEY": "https://www.firecrawl.dev/account"
    }

    missing_keys = {
        key: url for key, url in api_keys.items() if os.getenv(key) is None
    }

    if missing_keys:
        st.error("🚨 Some API keys are missing! Please provide them below:")
        for key, url in missing_keys.items():
            api_key = st.text_input(f"Enter 🔏 {key}: 👉[Get it here]({url})👈")
            if api_key:
                os.environ[key] = api_key
                try:
                    with open(".env", "a") as env_file:
                        env_file.write(f"{key}={api_key}\n")
                except IOError as e:
                    st.error(f"Failed to write {key} to .env file: {e}")
                st.success(f"✅ {key} added successfully!")
        return False
    return True


@st.cache_data
def check_llm_environs():
    """
    Ensures that the LLM provider and corresponding API key are set.
    Prompts the user to select a provider and enter the API key if missing.
    """
    gpt_provider = os.getenv("GPT_PROVIDER")
    supported_providers = {
        'google': "GEMINI_API_KEY",
        'openai': "OPENAI_API_KEY",
        'mistralai': "MISTRAL_API_KEY"
    }

    if not gpt_provider or gpt_provider.lower() not in supported_providers:
        gpt_provider = st.selectbox(
            "Select your LLM Provider", options=list(supported_providers.keys())
        )
        os.environ["GPT_PROVIDER"] = gpt_provider
        try:
            with open(".env", "a") as env_file:
                env_file.write(f"GPT_PROVIDER={gpt_provider}\n")
        except IOError as e:
            st.error(f"Failed to write GPT_PROVIDER to .env file: {e}")
        st.success(f"GPT Provider set to {gpt_provider}")

    api_key_var = supported_providers[gpt_provider.lower()]
    if not os.getenv(api_key_var):
        api_key = st.text_input(f"Enter {api_key_var}:")
        if api_key:
            os.environ[api_key_var] = api_key
            with open(".env", "a") as env_file:
                env_file.write(f"{api_key_var}={api_key}\n")
            st.success(f"{api_key_var} added successfully!")
        return False
    return True


def save_config(config):
    """
    Saves the provided configuration dictionary to a JSON file specified by the environment variable.
    """
    try:
        with open(os.getenv("ALWRITY_CONFIG"), "w") as config_file:
            json.dump(config, config_file, indent=4)
    except Exception as e:
        st.error(f"An error occurred while saving the configuration: {e}")


# Sidebar configuration
def sidebar_configuration():
    st.sidebar.title("🛠️ Personalization & Settings 🏗️")

    with st.sidebar.expander("**👷 Content Personalization**"):
        blog_length = st.text_input("**Content Length (words)**", value="2000", 
                          help="Approximate word count for blogs. Note: Actual length may vary based on GPT provider and max token count.")
        
        blog_tone_options = ["Casual", "Professional", "How-to", "Beginner", "Research", "Programming", "Social Media", "Customize"]
        blog_tone = st.selectbox("**Content Tone**",
                          options=blog_tone_options,
                          help="Select the desired tone for the blog content.")

        if blog_tone == "Customize":
            custom_tone = st.text_input("Enter the tone of your content", help="Specify the tone of your content.")
            if custom_tone:
                blog_tone = custom_tone
            else:
                st.warning("Please specify the tone of your content.")
        
        blog_demographic_options = ["Professional", "Gen-Z", "Tech-savvy", "Student", "Digital Marketing", "Customize"]
        
        blog_demographic = st.selectbox("**Target Audience**",
                                options=blog_demographic_options,
                                help="Select the primary audience for the blog content.")
        if blog_demographic == "Customize":
            custom_demographic = st.text_input("Enter your target audience", 
                                help="Specify your target audience.",
                                placeholder="Eg. Domain expert, Content creator, Financial expert etc..")
            if custom_demographic:
                blog_demographic = custom_demographic
            else:
                st.warning("Please specify your target audience.")
        
        blog_type = st.selectbox("**Content Type**", 
                          options=["Informational", "Commercial", "Company", "News", "Finance", "Competitor", "Programming", "Scholar"], 
                          help="Select the category that best describes the blog content.")

        blog_language = st.selectbox("**Content Language**", 
                          options=["English", "Spanish", "German", "Chinese", "Arabic", "Nepali", "Hindi", "Hindustani", "Customize"], 
                          help="Select the language in which the blog will be written.")
        if blog_language == "Customize":
            custom_lang = st.text_input("Enter the language of your choice", help="Specify the content language.")
            if custom_lang:
                blog_language = custom_lang
            else:
                st.warning("Please specify the language of your content.")

        blog_output_format = st.selectbox("**Content Output Format**", 
                          options=["markdown", "HTML", "plaintext"], 
                          help="Select the format for the blog output.")

    with st.sidebar.expander("**🩻 Images Personalization**"):
        image_generation_model = st.selectbox("**Image Generation Model**", 
                          options=["stable-diffusion", "dalle2", "dalle3"], 
                          help="Select the model to generate images for the blog.")
        number_of_blog_images = st.number_input("**Number of Blog Images**", value=1, help="Specify the number of images to include in the blog.")

    with st.sidebar.expander("**🤖 LLM Personalization**"):
        gpt_provider = st.selectbox("**GPT Provider**", 
                          options=["google", "openai", "minstral"], 
                          help="Select the provider for the GPT model.")
        model = st.text_input("**Model**", value="gemini-1.5-flash-latest", help="Specify the model version to use from the selected provider.")
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
        geographic_location = st.selectbox("**Geographic Location**", 
                          options=["us", "in", "fr", "cn"], 
                          help="Select the geographic location for tailoring search results.")
        search_language = st.selectbox("**Search Language**", 
                          options=["en", "zn-cn", "de", "hi"], 
                          help="Select the language for the search results.")
        number_of_results = st.number_input("**Number of Results**", 
                            value=10,
                            max_value=20,
                            min_value=1,
                            help="Specify the number of search results to retrieve.")
        time_range = st.selectbox("**Time Range**", 
                          options=["anytime", "past day", "past week", "past month", "past year"], 
                          help="Select the time range for filtering search results.")
        include_domains = st.text_input("**Include Domains**", value="", 
                          help="List specific domains to include in search results. Leave blank to include all domains.")
        similar_url = st.text_input("**Similar URL**", value="", help="Provide a URL to find similar results. Leave blank if not needed.")

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
@st.cache_data
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
    load_environment()
    setup_ui()
    setup_environment_paths()
    sidebar_configuration()

    if check_api_keys() and check_llm_environs():
        setup_tabs()
        modify_prompts_sidebar()


def setup_ui():
    """Sets up the Streamlit UI with custom CSS and logo."""
    try:
        css_file_path = os.path.join('lib', 'workspace', 'alwrity_ui_styling.css')
        with open(css_file_path) as f:
            custom_css = f.read()
        st.set_page_config(page_title="Alwrity", layout="wide")
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


def setup_environment_paths():
    """Sets up environment paths for saving files and configurations."""
    os.environ["SEARCH_SAVE_FILE"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_web_research",
                                                  f"web_research_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
    os.environ["IMG_SAVE_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_content")
    os.environ["CONTENT_SAVE_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_content")
    os.environ["PROMPTS_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_prompts")
    os.environ["ALWRITY_CONFIG"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_config", "main_config.json")


def setup_tabs():
    """Sets up the main tabs in the Streamlit app."""
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["📅Content Planning", " 📝🤖AI Writers", "🤝🤖Agents Teams", "🛠️🔍AI SEO tools", "📱AI Social Tools", " 💬Ask Alwrity"])
    with tab1:
        content_planning_tools()

    with tab2:
        ai_writers()

    with tab3:
        ai_agents_team()

    with tab4:
        ai_seo_tools()

    with tab5:
        ai_social_writer()

    with tab6:
        st.subheader("Chat with your Data, Chat with any Data.. COMING SOON !")
        st.markdown("Create a collection by uploading files (PDF, MD, CSV, etc), or crawl a data source (Websites, more sources coming soon.")
        st.markdown("One can ask/chat, summarize and do semantic search over the uploaded data")
        # alwrity_chat_docqa()


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
    elif choice == "Write from audio files":
        blog_from_audio()
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
        st.title("Web Research Assistant")
        st.write("Enter keywords for web research. The keywords should be at least three words long.")
        
        search_keywords = st.text_input("Search Keywords", placeholder="Enter keywords for web research...")
        if st.button("Start Web Research"):
            if search_keywords and len(search_keywords.split()) >= 3:
                try:
                    st.info(f"Starting web research on given keywords: {search_keywords}")
                    with st.spinner("Performing web research..."):
                        # Fetch and display multirange interest over time
                        st.subheader("Multirange Interest Over Time")
                        multirange_data = fetch_multirange_interest_over_time([search_keywords], ['today 3-m', 'today 1-m'])
                        st.dataframe(multirange_data)

                        # Fetch and display historical hourly interest
                        st.subheader("Historical Hourly Interest")
                        hourly_data = fetch_historical_hourly_interest([search_keywords], '2023-01-01', '2023-01-31')
                        st.dataframe(hourly_data)

                        # Fetch and display trending searches
                        st.subheader("Trending Searches")
                        trending_data = fetch_trending_searches()
                        st.dataframe(trending_data)

                        # Fetch and display realtime search trends
                        st.subheader("Realtime Search Trends")
                        realtime_data = fetch_realtime_search_trends()
                        st.dataframe(realtime_data)

                        # Fetch and display top charts
                        st.subheader("Top Charts")
                        top_charts_data = fetch_top_charts(2023)
                        st.dataframe(top_charts_data)

                        # Fetch and display suggestions
                        st.subheader("Suggestions")
                        suggestions = fetch_suggestions(search_keywords)
                        st.dataframe(pd.DataFrame(suggestions))

                        # Example of plotting with Matplotlib
                        st.subheader("Interest Over Time Plot")
                        plt.figure(figsize=(10, 6))
                        plt.plot(multirange_data['date'], multirange_data[search_keywords], label=search_keywords)
                        plt.title(f'Interest Over Time for "{search_keywords}"')
                        plt.xlabel('Date')
                        plt.ylabel('Interest')
                        plt.legend()
                        st.pyplot(plt)

                    st.success("Web research completed successfully!")
                except Exception as err:
                    st.error(f"ERROR: Failed to do web research: {err}")
            else:
                st.warning("Search keywords should be at least three words long. Please try again.")
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

