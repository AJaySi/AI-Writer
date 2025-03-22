import os
import streamlit as st
from .file_processor import load_image
from .content_generators import content_planning_tools, ai_writers
from .alwrity_utils import ai_agents_team, ai_social_writer
from .seo_tools import ai_seo_tools


def setup_ui():
    """Sets up the Streamlit UI with custom CSS and logo."""
    try:
        css_file_path = os.path.join('lib', 'workspace', 'alwrity_ui_styling.css')
        with open(css_file_path) as f:
            custom_css = f.read()
        st.set_page_config(page_title="ALwrity", layout="wide")
        st.markdown(f'<style>{open("lib/workspace/alwrity_ui_styling.css").read()}</style>', unsafe_allow_html=True)
    except Exception as err:
        st.error(f"Failed in setting up Alwrity Streamlit UI: {err}")

    image_base64 = load_image("lib/workspace/alwrity_logo.png")
    st.markdown(f"""
    <div class='main-header'>
        <img src='data:image/png;base64,{image_base64}' alt='Alwrity Logo' style='height: 50px; margin-right: 10px; vertical-align: middle;'>
        Welcome to ALwrity!
    </div>
    """, unsafe_allow_html=True)


def sidebar_configuration():
    """Sets up the sidebar for personalization and settings."""
    if st.sidebar.button("⚙️ Settings", use_container_width=True):
        # Store the current page in session state
        st.session_state['current_page'] = 'settings'
        # Force a rerun to switch to settings page
        st.rerun()


def setup_sidebar_navigation():
    """Sets up the sidebar navigation for the main tabs."""
    st.sidebar.title("📂 Navigation")

    # Create a navigation menu in the sidebar
    selected_tab = st.sidebar.radio(
        "Navigate",
        options=[
            "📅 Content Planning",
            "📝 AI Writers",
            "🤝 Agents Teams",
            "🛠️ AI SEO Tools",
            "📱 AI Social Tools",
            "💬 Ask Alwrity"
        ],
        label_visibility="collapsed"
    )

    # Render the content based on the selected tab
    if selected_tab == "📅 Content Planning":
        content_planning_tools()
    elif selected_tab == "📝 AI Writers":
        ai_writers()
    elif selected_tab == "🤝 Agents Teams":
        ai_agents_team()
    elif selected_tab == "🛠️ AI SEO Tools":
        ai_seo_tools()
    elif selected_tab == "📱 AI Social Tools":
        ai_social_writer()
    elif selected_tab == "💬 Ask Alwrity":
        st.subheader("Chat with your Data, Chat with any Data.. COMING SOON!")
        st.markdown("""
            Create a collection by uploading files (PDF, MD, CSV, etc), 
            or crawl a data source (Websites, more sources coming soon).
            
            One can ask/chat, summarize and do semantic search over the uploaded data.
        """)
