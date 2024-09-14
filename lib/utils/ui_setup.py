import os
import streamlit as st
from .file_processor import load_image

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
