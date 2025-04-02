import os
import streamlit as st
from lib.utils.file_processor import load_image
from lib.utils.content_generators import content_planning_tools, ai_writers
from lib.utils.alwrity_utils import ai_social_writer
from lib.utils.seo_tools import ai_seo_tools
from lib.utils.settings_page import render_settings_page


def setup_ui():
    """Set up the UI with custom styling."""
    # Add custom CSS
    st.markdown("""
        <style>
            /* Main app styling */
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            }
            
            /* Header styling */
            h1, h2, h3 {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-weight: 600;
            }
            
            /* Button styling */
            .stButton > button {
                border-radius: 8px;
                font-weight: 500;
                transition: all 0.3s ease;
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
            }
            
            /* Success message styling */
            .stSuccess {
                background: linear-gradient(135deg, #43c6ac 0%, #191654 100%);
                padding: 1rem;
                border-radius: 8px;
                color: white;
            }
            
            /* Error message styling */
            .stError {
                background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
                padding: 1rem;
                border-radius: 8px;
                color: white;
            }

            /* Sidebar navigation styling */
            .sidebar-nav {
                padding: 1rem 0;
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
                padding-left: 1.5rem;
            }
            
            .nav-button.active {
                background: #1565C0;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)


def setup_alwrity_ui():
    """Sets up the main navigation in the sidebar."""
    # Initialize session state for active tab if not exists
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Content Planning"

    # Define the navigation items with their icons and functions
    nav_items = {
        "Content Planning": ("📅", content_planning_tools),
        "AI Writers": ("📝", ai_writers),
        "Agents Teams": ("🤝", lambda: st.subheader("Agents Teams - Coming Soon!")),
        "AI SEO Tools": ("🔍", ai_seo_tools),
        "AI Social Tools": ("📱", ai_social_writer),
        "Ask Alwrity": ("💬", lambda: (
            st.subheader("Chat with your Data, Chat with any Data.. COMING SOON !"),
            st.markdown("Create a collection by uploading files (PDF, MD, CSV, etc), or crawl a data source (Websites, more sources coming soon."),
            st.markdown("One can ask/chat, summarize and do semantic search over the uploaded data")
        )),
        "ALwrity Settings": ("⚙️", render_settings_page)
    }

    # Create sidebar navigation
    st.sidebar.markdown("### ALwrity Options")
    st.sidebar.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)

    # Create navigation buttons
    for name, (icon, func) in nav_items.items():
        button_class = "nav-button active" if st.session_state.active_tab == name else "nav-button"
        if st.sidebar.button(f"{icon} {name}", key=f"nav_{name}", 
                           help=f"Navigate to {name}", use_container_width=True):
            st.session_state.active_tab = name

    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Display content based on active tab
    st.title(f"{nav_items[st.session_state.active_tab][0]} {st.session_state.active_tab}")
    nav_items[st.session_state.active_tab][1]()