"""
UI setup module for ALwrity application.
Provides consistent navigation and layout structure.
"""

import os
import streamlit as st
from lib.utils.file_processor import load_image
from lib.utils.content_generators import content_planning_tools
from lib.utils.alwrity_utils import ai_social_writer
from lib.alwrity_ui.seo_tools_dashboard import ai_seo_tools
from lib.alwrity_ui.settings_page import render_settings_page
from lib.alwrity_ui.navigation_styles import apply_navigation_styles, apply_compact_layout
from lib.alwrity_ui.content_generation.content_generation_dashboard import render_content_generation_dashboard
from loguru import logger

# Import social media writer functions
from lib.ai_writers.ai_facebook_writer.facebook_ai_writer import facebook_main_menu
from lib.ai_writers.linkedin_writer.linkedin_ai_writer import linkedin_main_menu
from lib.ai_writers.twitter_writers import run_dashboard
from lib.ai_writers.insta_ai_writer import insta_writer
from lib.ai_writers.youtube_writers.youtube_ai_writer import youtube_main_menu
from lib.ai_writers.ai_writer_dashboard import get_ai_writers, list_ai_writers
from lib.chatbot_custom.enhanced_alwrity_chatbot import run_enhanced_chatbot
from lib.alwrity_ui.social_media_dashboard import render_social_tools_dashboard


def setup_ui():
    """Set up the UI with custom styling."""
    # Apply navigation-specific styling
    apply_navigation_styles()


def setup_alwrity_ui():
    """Sets up the main navigation in the sidebar."""
    logger.info("Setting up ALwrity UI")
    
    # Initialize session state for active tab if not exists
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Content Generation"
        logger.info(f"Initialized active_tab to: {st.session_state.active_tab}")
    
    # Initialize session state for active sub-tab if not exists
    if 'active_sub_tab' not in st.session_state:
        st.session_state.active_sub_tab = None
        logger.info("Initialized active_sub_tab to None")

    # Define the navigation items with their icons and functions
    nav_items = {
        "Content Generation": ("🎯", render_content_generation_dashboard),
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
            apply_compact_layout()
            logger.info(f"{nav_items[st.session_state.active_tab][0]} {st.session_state.active_tab}")
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
            apply_compact_layout()
            logger.info(f"{nav_items[st.session_state.active_tab][0]} {st.session_state.active_tab}")
            nav_items[st.session_state.active_tab][1]()
    
    logger.info("Finished setting up ALwrity UI")