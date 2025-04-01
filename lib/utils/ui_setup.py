import os
import streamlit as st
from lib.utils.file_processor import load_image
from lib.utils.content_generators import content_planning_tools, ai_writers
from lib.utils.alwrity_utils import ai_social_writer
from lib.utils.seo_tools import ai_seo_tools


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
        </style>
    """, unsafe_allow_html=True)

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
        #ai_agents_team()
        st.subheader("Agents Teams")
        
    with tab4:
        ai_seo_tools()

    with tab5:
        ai_social_writer()

    with tab6:
        st.subheader("Chat with your Data, Chat with any Data.. COMING SOON !")
        st.markdown("Create a collection by uploading files (PDF, MD, CSV, etc), or crawl a data source (Websites, more sources coming soon.")
        st.markdown("One can ask/chat, summarize and do semantic search over the uploaded data")
        # alwrity_chat_docqa()
