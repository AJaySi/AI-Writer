import streamlit as st
import os
import json
from pathlib import Path

st.set_page_config(
    page_title="Personalization Setup",
    page_icon="⚙️",
    layout="wide"
)

st.title("Personalization Setup")

# Initialize session state for active tab if not exists
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Writing Preferences"

# Create tabs for different sections
tab1, tab2 = st.tabs(["Writing Preferences", "AI Configuration"])

with tab1:
    st.write("""
    This section allows you to customize your AI writing experience.
    Configure your preferences and settings here.
    """)

    # Add your personalization options here
    st.subheader("Writing Style Preferences")
    tone = st.selectbox(
        "Select your preferred writing tone",
        ["Professional", "Casual", "Academic", "Creative"]
    )

    st.subheader("Content Preferences")
    content_type = st.multiselect(
        "Select your preferred content types",
        ["Blog Posts", "Articles", "Social Media", "Technical Writing", "Creative Writing"]
    )

    if st.button("Save Preferences"):
        st.success("Your preferences have been saved!")

with tab2:
    st.subheader("AI Configuration Settings")
    
    # Create a form for AI configuration
    with st.form("ai_config_form"):
        # API Keys
        st.text_input("OpenAI API Key", type="password", key="openai_key")
        st.text_input("Google API Key", type="password", key="google_key")
        st.text_input("SerpAPI Key", type="password", key="serpapi_key")
        
        # Model Selection
        st.selectbox("Select Model", ["gpt-3.5-turbo", "gpt-4"], key="model")
        
        # Temperature
        st.slider("Temperature", 0.0, 2.0, 0.7, 0.1, key="temperature")
        
        # Max Tokens
        st.number_input("Max Tokens", 100, 4000, 2000, 100, key="max_tokens")
        
        # Submit button
        submitted = st.form_submit_button("Save Configuration")
        
        if submitted:
            # Create config directory if it doesn't exist
            config_dir = Path("config")
            config_dir.mkdir(exist_ok=True)
            
            # Save configuration
            config = {
                "openai_key": st.session_state.openai_key,
                "google_key": st.session_state.google_key,
                "serpapi_key": st.session_state.serpapi_key,
                "model": st.session_state.model,
                "temperature": st.session_state.temperature,
                "max_tokens": st.session_state.max_tokens
            }
            
            config_file = config_dir / "test_config.json"
            with open(config_file, "w") as f:
                json.dump(config, f, indent=4)
            
            st.success("Configuration saved successfully!") 