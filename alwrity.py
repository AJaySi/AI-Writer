import streamlit as st
import os
import json
import base64
import logging
from datetime import datetime

# Set page config with favicon
favicon_path = os.path.join("lib", "workspace", "alwrity_logo.png")
if os.path.exists(favicon_path):
    st.set_page_config(
        page_title="ALwrity - AI Content Creation Platform",
        page_icon=favicon_path,
        layout="wide",
        initial_sidebar_state="expanded",  # Changed from collapsed to expanded
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    )
else:
    st.set_page_config(
        page_title="ALwrity - AI Content Creation Platform",
        layout="wide",
        initial_sidebar_state="expanded"
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

import os
import json
import base64
import logging
import logging
from datetime import datetime
import os
import json
import base64
import logging
from datetime import datetime

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

from lib.utils.api_key_manager.api_key_manager import APIKeyManager, render
from lib.utils.api_key_manager.validation import check_all_api_keys
from dotenv import load_dotenv
from lib.utils.ui_setup import setup_ui, setup_alwrity_ui


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


if __name__ == "__main__":
    main()