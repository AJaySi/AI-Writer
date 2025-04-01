import streamlit as st
import logging

from .config_manager import save_config

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to console
        #logging.FileHandler('alwrity.log')  # Output to file
    ]
)
logger = logging.getLogger(__name__)

# Sidebar configuration
def sidebar_configuration():
    """Configure the sidebar with all necessary options."""
    try:
        # Configure sidebar styling
        st.sidebar.markdown("""
            <style>
                [data-testid="stSidebar"] {
                    min-width: 250px !important;
                    max-width: 250px !important;
                    visibility: visible !important;
                    position: relative !important;
                    transform: translateX(0) !important;
                }
                [data-testid="stSidebar"][aria-expanded="true"] {
                    min-width: 250px !important;
                    max-width: 250px !important;
                    transform: translateX(0) !important;
                }
                [data-testid="stSidebar"][aria-expanded="false"] {
                    min-width: 250px !important;
                    max-width: 250px !important;
                    transform: translateX(0) !important;
                }
                .stSidebar .element-container {
                    padding: 0.5rem;
                }
                .stSidebar .stMarkdown {
                    padding: 0.5rem;
                }
                .stSidebar .stSelectbox {
                    padding: 0.5rem;
                }
                .stSidebar .stTextInput {
                    padding: 0.5rem;
                }
                .stSidebar .stNumberInput {
                    padding: 0.5rem;
                }
                .stSidebar .stSlider {
                    padding: 0.5rem;
                }
                /* Ensure sidebar is visible */
                section[data-testid="stSidebar"] {
                    visibility: visible !important;
                    transform: translateX(0) !important;
                }
            </style>
        """, unsafe_allow_html=True)
        
        logger.info("Initializing sidebar configuration")
        st.sidebar.title("🛠️ Personalization & Settings 🏗️")

        with st.sidebar.expander("**👷 Content Personalization**"):
            logger.debug("Setting up content personalization options")
            blog_length = st.text_input("**Content Length (words)**", value="2000", 
                              help="Approximate word count for blogs. Note: Actual length may vary based on GPT provider and max token count.")
            
            blog_tone_options = ["Casual", "Professional", "How-to", "Beginner", "Research", "Programming", "Social Media", "Customize"]
            blog_tone = st.selectbox("**Content Tone**",
                              options=blog_tone_options,
                              help="Select the desired tone for the blog content.")
            logger.debug(f"Selected blog tone: {blog_tone}")

            if blog_tone == "Customize":
                custom_tone = st.text_input("Enter the tone of your content", help="Specify the tone of your content.")
                if custom_tone:
                    blog_tone = custom_tone
                    logger.debug(f"Custom tone set to: {custom_tone}")
                else:
                    logger.warning("Custom tone not specified")
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
    except Exception as e:
        logger.error(f"Error configuring sidebar: {str(e)}")
        st.error(f"Error configuring sidebar: {str(e)}")