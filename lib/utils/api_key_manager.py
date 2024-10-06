import os
import streamlit as st
from dotenv import load_dotenv

import os
import streamlit as st

@st.cache_data
def check_api_keys():
    """Checks for API keys and prompts for input if not found."""
    required_keys = ["GOOGLE_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
    missing_keys = []
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)

    if missing_keys:
        st.warning(f"API keys not found: {', '.join(missing_keys)}. Please provide them below. Restart the app after saving the keys.")
        with st.form(key='api_keys_form'):
            for key in missing_keys:
                st.text_input(f"{key}:", type="password", key=key)
            if st.form_submit_button("Save Keys"):
                with open(".env", "a") as env_file:
                    for key in missing_keys:
                        key_value = st.session_state[key]
                        env_file.write(f"{key}={key_value}\n")
                st.success("API keys saved successfully! Please restart the application.")
        return False
    return True



