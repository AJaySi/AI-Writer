"""
UI setup module for ALwrity application.
Provides consistent navigation and layout structure.
"""

import os
import streamlit as st
from lib.utils.file_processor import load_image
from lib.utils.content_generators import content_planning_tools
from lib.utils.alwrity_utils import ai_social_writer
from lib.utils.seo_tools import ai_seo_tools
from lib.utils.settings_page import render_settings_page
from loguru import logger

# Import social media writer functions
from lib.ai_writers.ai_facebook_writer.facebook_ai_writer import facebook_main_menu
from lib.ai_writers.linkedin_writer.linkedin_ai_writer import linkedin_main_menu
from lib.ai_writers.twitter_writers import run_dashboard
from lib.ai_writers.insta_ai_writer import insta_writer
from lib.ai_writers.youtube_writers.youtube_ai_writer import youtube_main_menu
from lib.ai_writers.ai_writer_dashboard import get_ai_writers, list_ai_writers
from lib.chatbot_custom.enhanced_alwrity_chatbot import run_enhanced_chatbot

def render_social_tools_dashboard():
    """Render a modern dashboard for social media tools."""
    st.markdown("""
        <style>
            .social-card {
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
                height: 100%;
            }
            .social-card:hover {
                transform: translateY(-5px);
            }
            .social-icon {
                font-size: 2.5rem;
                margin-bottom: 15px;
            }
            .social-title {
                font-size: 1.2rem;
                font-weight: 600;
                margin-bottom: 10px;
            }
            .social-description {
                color: #666;
                font-size: 0.9rem;
                margin-bottom: 15px;
            }
            .social-button {
                width: 100%;
                padding: 8px 16px;
                border-radius: 5px;
                border: none;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
            }
        </style>
    """, unsafe_allow_html=True)

    # Define social tools with their details and paths
    social_tools = {
        "Facebook": {
            "icon": "📘",
            "description": "Create engaging Facebook posts and manage your content strategy",
            "color": "#4267B2",
            "path": "facebook"
        },
        "LinkedIn": {
            "icon": "💼",
            "description": "Generate professional LinkedIn content and optimize your profile",
            "color": "#0077B5",
            "path": "linkedin"
        },
        "Twitter": {
            "icon": "🐦",
            "description": "Craft viral tweets and manage your Twitter presence",
            "color": "#1DA1F2",
            "path": "twitter"
        },
        "Instagram": {
            "icon": "📸",
            "description": "Create Instagram captions and plan your visual content",
            "color": "#E1306C",
            "path": "instagram"
        },
        "YouTube": {
            "icon": "🎥",
            "description": "Generate video scripts and optimize your YouTube content",
            "color": "#FF0000",
            "path": "youtube"
        }
    }

    # Create a grid of cards
    cols = st.columns(3)
    for idx, (platform, details) in enumerate(social_tools.items()):
        with cols[idx % 3]:
            st.markdown(f"""
                <div class="social-card">
                    <div class="social-icon">{details['icon']}</div>
                    <div class="social-title">{platform}</div>
                    <div class="social-description">{details['description']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Open {platform}", key=f"btn_{platform}", 
                        help=f"Launch {platform} tools",
                        use_container_width=True):
                # Set query parameters to redirect to the specific tool
                st.query_params["tool"] = details["path"]
                st.rerun()

def setup_ui():
    """Set up the UI with custom styling."""
    # Add custom CSS
    st.markdown("""
        <style>
            /* Main app styling */
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            }
            
            /* Compact layout styling with zero top padding when sub-tab selected */
            .main .block-container {
                padding-top: 0 !important;  /* Remove all top padding */
                padding-bottom: 0;
                max-width: 100%;
            }
            
            /* Remove extra padding and margins */
            .stMarkdown {
                margin: 0;
                padding: 0;
            }
            
            /* Header styling with zero margins when in sub-tab */
            .sub-tab-active h1, .sub-tab-active h2, .sub-tab-active h3 {
                display: none;  /* Hide headers in sub-tab mode */
            }
            
            /* Remove extra padding in containers */
            .stMarkdown {
                margin-bottom: 0;
            }
            
            /* Header styling */
            h1, h2, h3 {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-weight: 600;
                margin-top: 0;
                margin-bottom: 0.5rem;  /* Reduced from 1rem */
                padding-top: 0;
            }
            
            /* Reduce spacing between elements */
            .element-container {
                margin-bottom: 0.5rem;  /* Reduced from 1rem */
            }
            
            /* Button styling */
            .stButton > button {
                border-radius: 8px;
                font-weight: 500;
                transition: all 0.3s ease;
                margin-bottom: 0.25rem;  /* Reduced from 0.5rem */
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            
            /* Input field styling */
            .stTextInput > div > div > input {
                border-radius: 8px;
                border: 1px solid rgba(0,0,0,0.1);
                padding: 0.5rem 1rem;
            }
            
            /* Checkbox styling */
            .stCheckbox > label {
                font-weight: 500;
            }
            
            /* Expander styling */
            .streamlit-expanderHeader {
                font-weight: 500;
                color: #2c3e50;
                margin-bottom: 0.5rem;
            }
            
            /* Success message styling */
            .stSuccess {
                background: linear-gradient(135deg, #43c6ac 0%, #191654 100%);
                padding: 0.75rem;
                border-radius: 8px;
                color: white;
                margin-bottom: 1rem;
            }
            
            /* Error message styling */
            .stError {
                background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
                padding: 0.75rem;
                border-radius: 8px;
                color: white;
                margin-bottom: 1rem;
            }
            
            /* Info message styling */
            .stInfo {
                padding: 0.75rem;
                margin-bottom: 1rem;
            }

            /* Sidebar navigation styling */
            .sidebar-nav {
                padding: 0.5rem 0;
            }
            
            .nav-button {
                width: 100%;
                text-align: left;
                padding: 0.5rem 1rem;
                background: transparent;
                border: none;
                color: #2c3e50;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                margin: 0.2rem 0;
                border-radius: 4px;
            }
            
            .nav-button:hover {
                background: rgba(0,0,0,0.05);
                padding-left: 0.5rem;
            }
            
            .nav-button.active {
                background: #1565C0;
                color: white;
            }
            
            /* Enhanced Sub-menu styling with minimal spacing */
            .sub-menu {
                padding-left: 1rem;
                margin: 0;
                border-left: 2px solid rgba(21, 101, 192, 0.3);
                background: rgba(255, 255, 255, 0.05);
                border-radius: 0 8px 8px 0;
                padding-top: 0;
                padding-bottom: 0;
            }
            
            /* Sub-menu button styling with minimal gaps */
            .sub-menu .stButton > button {
                font-size: 0.9rem;
                text-align: left;
                padding: 0.4rem 0.8rem;
                background: transparent;
                border: none;
                color: #2c3e50;
                font-weight: 500;
                transition: all 0.2s ease;
                margin: 0;
                border-radius: 4px;
                min-height: 0;
                height: auto;
                line-height: 1.2;
                width: 100%;
            }
            
            /* Platform-specific button styles */
            .facebook-button .stButton > button {
                color: #4267B2;
                background: rgba(66, 103, 178, 0.1);
            }
            
            .linkedin-button .stButton > button {
                color: #0077B5;
                background: rgba(0, 119, 181, 0.1);
            }
            
            .twitter-button .stButton > button {
                color: #1DA1F2;
                background: rgba(29, 161, 242, 0.1);
            }
            
            .instagram-button .stButton > button {
                color: #E1306C;
                background: rgba(225, 48, 108, 0.1);
            }
            
            .youtube-button .stButton > button {
                color: #FF0000;
                background: rgba(255, 0, 0, 0.1);
            }
            
            /* Platform-specific hover states */
            .facebook-button .stButton > button:hover {
                background: rgba(66, 103, 178, 0.2) !important;
                color: #4267B2 !important;
            }
            
            .linkedin-button .stButton > button:hover {
                background: rgba(0, 119, 181, 0.2) !important;
                color: #0077B5 !important;
            }
            
            .twitter-button .stButton > button:hover {
                background: rgba(29, 161, 242, 0.2) !important;
                color: #1DA1F2 !important;
            }
            
            .instagram-button .stButton > button:hover {
                background: rgba(225, 48, 108, 0.2) !important;
                color: #E1306C !important;
            }
            
            .youtube-button .stButton > button:hover {
                background: rgba(255, 0, 0, 0.2) !important;
                color: #FF0000 !important;
            }
            
            /* Platform-specific active states */
            .facebook-button.active .stButton > button {
                background: #4267B2 !important;
                color: white !important;
            }
            
            .linkedin-button.active .stButton > button {
                background: #0077B5 !important;
                color: white !important;
            }
            
            .twitter-button.active .stButton > button {
                background: #1DA1F2 !important;
                color: white !important;
            }
            
            .instagram-button.active .stButton > button {
                background: #E1306C !important;
                color: white !important;
            }
            
            .youtube-button.active .stButton > button {
                background: #FF0000 !important;
                color: white !important;
            }

            /* Remove any extra spacing from button containers */
            .sub-menu .stButton {
                margin: 0;
                padding: 0;
            }
            
            .sub-menu > div {
                margin: 0;
                padding: 0;
            }
            
            .sub-menu .element-container {
                margin: 0;
                padding: 0;
            }
            
            /* Ensure minimal gaps between elements */
            .sub-menu > div:not(:last-child) {
                margin-bottom: 1px;
            }

            /* Sidebar icon styling */
            .sidebar-icon {
                padding: 1rem;
                text-align: center;
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
            }
            
            .sidebar-icon img {
                width: 80px !important;
                height: auto !important;
                margin: 0 auto;
            }
        </style>
    """, unsafe_allow_html=True)


def setup_alwrity_ui():
    """Sets up the main navigation in the sidebar."""
    logger.info("Setting up ALwrity UI")
    
    # Initialize session state for active tab if not exists
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Content Planning"
        logger.info(f"Initialized active_tab to: {st.session_state.active_tab}")
    
    # Initialize session state for active sub-tab if not exists
    if 'active_sub_tab' not in st.session_state:
        st.session_state.active_sub_tab = None
        logger.info("Initialized active_sub_tab to None")

    # Define the navigation items with their icons and functions
    nav_items = {
        "AI Writers": ("📝", get_ai_writers),
        "Content Planning": ("📅", content_planning_tools),
        "AI SEO Tools": ("🔍", ai_seo_tools),
        "AI Social Tools": ("📱", render_social_tools_dashboard),
        "ALwrity Assistant": ("🤖", run_enhanced_chatbot),
        "ALwrity Settings": ("⚙️", render_settings_page),
        "Agents Teams(TBD)": ("🤝", lambda: st.subheader("Agents Teams - Coming Soon!"))
    }
    
    logger.info(f"Defined {len(nav_items)} navigation items")

    # Create sidebar navigation
    st.sidebar.markdown("### ALwrity Options")
    st.sidebar.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)

    # Create navigation buttons
    for name, (icon, func) in nav_items.items():
        button_class = "nav-button active" if st.session_state.active_tab == name else "nav-button"
        
        if st.sidebar.button(f"{icon} {name}", key=f"nav_{name}", 
                           help=f"Navigate to {name}", use_container_width=True):
            st.session_state.active_tab = name
            # Reset sub-tab when main tab changes
            st.session_state.active_sub_tab = None
            logger.info(f"Selected main tab: {name}")

    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Add the AskAlwrity icon at the bottom of sidebar
    st.sidebar.markdown('<div class="sidebar-icon">', unsafe_allow_html=True)
    icon_path = os.path.join("lib", "workspace", "AskAlwrity-min.ico")
    if os.path.exists(icon_path):
        st.sidebar.image(icon_path, use_container_width=False)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Display content based on active tab and tool selection
    if st.session_state.active_tab == "AI Social Tools":
        # Check if a specific tool is selected
        selected_tool = st.query_params.get("tool")
        if selected_tool:
            # Add a back button at the top
            if st.button("← Back to Social Tools Dashboard", key=f"back_to_dashboard_{selected_tool}"):
                # Clear the tool query parameter
                st.query_params.clear()
                st.rerun()
            
            # Map tool paths to their respective functions
            tool_functions = {
                "facebook": facebook_main_menu,
                "linkedin": linkedin_main_menu,
                "twitter": run_dashboard,
                "instagram": insta_writer,
                "youtube": youtube_main_menu
            }
            
            if selected_tool in tool_functions:
                # Clear any existing content
                st.empty()
                # Execute the selected tool's function
                tool_functions[selected_tool]()
            else:
                st.error(f"Invalid tool selected: {selected_tool}")
                render_social_tools_dashboard()
        else:
            # Show the dashboard if no tool is selected
            st.markdown("""
                <style>
                    .main .block-container {
                        padding-top: 0.25rem !important;
                    }
                </style>
            """, unsafe_allow_html=True)
            st.title(f"{nav_items[st.session_state.active_tab][0]} {st.session_state.active_tab}")
            render_social_tools_dashboard()
    else:
        # Handle other tabs as before
        if st.session_state.active_tab == "AI Writers":
            writer = st.query_params.get("writer")
            logger.info(f"Current writer from query params: {writer}")
            
            if writer:
                writers = list_ai_writers()
                logger.info(f"Found {len(writers)} writers")
                
                writer_found = False
                for w in writers:
                    logger.info(f"Checking writer: {w['name']} with path: {w['path']}")
                    if w["path"] == writer:
                        writer_found = True
                        logger.info(f"Found matching writer: {w['name']}, executing function")
                        st.empty()
                        w["function"]()
                        break
                
                if not writer_found:
                    logger.error(f"No writer found with path: {writer}")
                    st.error(f"No writer found with path: {writer}")
            else:
                logger.info("No writer selected, showing dashboard")
                get_ai_writers()
        else:
            st.markdown("""
                <style>
                    .main .block-container {
                        padding-top: 0.25rem !important;
                        padding-bottom: 0;
                    }
                </style>
            """, unsafe_allow_html=True)
            st.title(f"{nav_items[st.session_state.active_tab][0]} {st.session_state.active_tab}")
            nav_items[st.session_state.active_tab][1]()
    
    logger.info("Finished setting up ALwrity UI")