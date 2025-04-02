import streamlit as st
import os
import json
import base64
import logging
from datetime import datetime

# Set page config - must be the first Streamlit command
st.set_page_config(
    page_title="AI Writer - Content Generation Platform",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",  # Changed from collapsed to expanded
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Load and apply custom CSS
with open('lib/workspace/alwrity_ui_styling.css', 'r') as f:
    css = f.read()
    
st.markdown(f"""
    <style>
        /* Hide Streamlit header elements */
        header {{
            visibility: hidden !important;
            height: 0px !important;
        }}
        
        /* Hide Deploy button */
        .stDeployButton {{
            display: none !important;
        }}
        
        /* Adjust top padding since we removed the header */
        .main .block-container {{
            padding-top: 1rem !important;
        }}
        
        {css}
    </style>
""", unsafe_allow_html=True)

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

from lib.utils.ui_setup import setup_ui
from lib.utils.api_key_manager.api_key_manager import APIKeyManager, render
from lib.utils.api_key_manager.validation import check_all_api_keys
from dotenv import load_dotenv
from lib.utils.content_generators import blog_from_keyword, story_input_section, essay_writer, ai_news_writer, ai_finance_ta_writer, write_ai_prod_desc, do_web_research, competitor_analysis
from lib.utils.ui_setup import setup_ui, setup_alwrity_ui


def process_folder_for_rag(folder_path):
    """Placeholder for the process_folder_for_rag function."""
    logger.info(f"Processing folder for RAG: {folder_path}")
    st.write(f"This is a placeholder for processing the folder: {folder_path}")


def save_config(config):
    """
    Saves the provided configuration dictionary to a JSON file specified by the environment variable.
    """
    try:
        logger.debug(f"Saving configuration to {os.getenv('ALWRITY_CONFIG')}")
        with open(os.getenv("ALWRITY_CONFIG"), "w") as config_file:
            json.dump(config, config_file, indent=4)
        logger.info("Configuration saved successfully")
    except Exception as e:
        logger.error(f"Error saving configuration: {str(e)}", exc_info=True)
        st.error(f"An error occurred while saving the configuration: {e}")


def main():
    """Main application entry point."""
    # Initialize API key manager
    api_key_manager = APIKeyManager()
    
    # Setup UI
    setup_ui()
    #load_environment
    load_dotenv()
    logger.debug("Environment variables loaded")
    setup_environment_paths()
    logger.debug("Environment paths configured")
    
    # Check API keys and show setup if needed
    if not check_all_api_keys(api_key_manager):
        logger.info("API keys not verified")
        # Add CSS to hide sidebar during setup
        st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display:none;}
            /* Hide sidebar during setup */
            [data-testid="stSidebar"] {
                visibility: hidden !important;
                width: 0px !important;
                position: fixed !important;
            }
        </style>
        """, unsafe_allow_html=True)
        render(api_key_manager)
        return
    else:
        logger.info("All API keys verified")
        # Remove the CSS that hides the sidebar and ensure it's expanded
        st.markdown("""
            <style>
                #MainMenu {visibility: visible;}
                footer {visibility: visible;}
                .stDeployButton {display:block;}
                
                /* Sidebar styling */
                [data-testid="stSidebar"] {
                    visibility: visible !important;
                    position: relative !important;
                    transition: width 0.3s ease-in-out;
                }
                
                /* Expanded state */
                [data-testid="stSidebar"][aria-expanded="true"] {
                    width: 288px !important;
                    margin-left: 0 !important;
                }
                
                /* Collapsed state */
                [data-testid="stSidebar"][aria-expanded="false"] {
                    width: 0 !important;
                    margin-left: 0 !important;
                }
                
                /* Main content area adjustments */
                .main .block-container {
                    padding-left: 2rem !important;
                    padding-right: 2rem !important;
                    max-width: none;
                }
                
                /* Ensure content reflows when sidebar is collapsed */
                @media (max-width: 768px) {
                    .main .block-container {
                        padding-left: 1rem !important;
                        padding-right: 1rem !important;
                    }
                }
            </style>
            <script>
                // Force sidebar to be expanded initially
                document.addEventListener('DOMContentLoaded', function() {
                    const sidebar = document.querySelector('[data-testid="stSidebar"]');
                    if (sidebar) {
                        sidebar.setAttribute('aria-expanded', 'true');
                        sidebar.style.transition = 'width 0.3s ease-in-out';
                        
                        // Handle sidebar content
                        const sidebarContent = sidebar.querySelector('.css-1d391kg');
                        if (sidebarContent) {
                            sidebarContent.style.width = sidebar.getAttribute('aria-expanded') === 'true' ? '288px' : '0px';
                            sidebarContent.style.display = 'block';
                            sidebarContent.style.transition = 'width 0.3s ease-in-out';
                        }
                        
                        // Add event listener for sidebar toggle
                        const toggleButton = document.querySelector('button[kind="header"]');
                        if (toggleButton) {
                            toggleButton.addEventListener('click', function() {
                                const isExpanded = sidebar.getAttribute('aria-expanded') === 'true';
                                if (sidebarContent) {
                                    sidebarContent.style.width = isExpanded ? '0px' : '288px';
                                }
                            });
                        }
                    }
                });
            </script>
        """, unsafe_allow_html=True)
        
        # Set session state to ensure sidebar stays expanded
        if 'sidebar_expanded' not in st.session_state:
            st.session_state.sidebar_expanded = True
            
        # Force sidebar state
        st.sidebar.markdown("""
            <style>
                [data-testid="stSidebar"] {
                    width: 288px !important;
                }
            </style>
        """, unsafe_allow_html=True)
            
        setup_alwrity_ui()


def setup_environment_paths():
    """Sets up environment paths for saving files and configurations."""
    logger.debug("Setting up environment paths")
    try:
        os.environ["SEARCH_SAVE_FILE"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_web_research",
                                                  f"web_research_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
        os.environ["IMG_SAVE_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_content")
        os.environ["CONTENT_SAVE_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_content")
        os.environ["PROMPTS_DIR"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_prompts")
        os.environ["ALWRITY_CONFIG"] = os.path.join(os.getcwd(), "lib", "workspace", "alwrity_config", "main_config.json")
        logger.info("Environment paths configured successfully")
    except Exception as e:
        logger.error(f"Error setting up environment paths: {str(e)}", exc_info=True)
        raise


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
