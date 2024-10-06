import os
import streamlit as st
from dotenv import load_dotenv


@st.cache_data
def check_all_api_keys():
    """
    Checks if all required API keys are present in the environment variables.
    Prompts the user to enter missing keys and saves them in the .env file.
    This includes general API keys and the LLM provider key.
    """
    api_keys = {
        "METAPHOR_API_KEY": "https://dashboard.exa.ai/login",
        "TAVILY_API_KEY": "https://tavily.com/#api",
        "SERPER_API_KEY": "https://serper.dev/signup",
        "STABILITY_API_KEY": "https://platform.stability.ai/",
        "FIRECRAWL_API_KEY": "https://www.firecrawl.dev/account"
    }

    missing_keys = {
        key: url for key, url in api_keys.items() if os.getenv(key) is None
    }

    gpt_provider = os.getenv("GPT_PROVIDER")
    supported_providers = {
        'google': "GEMINI_API_KEY",
        'openai': "OPENAI_API_KEY",
        'mistral': "MISTRAL_API_KEY"
    }
    if not gpt_provider or gpt_provider.lower() not in supported_providers:
        gpt_provider = st.selectbox(
            "Select your LLM Provider", options=list(supported_providers.keys())
        )
        os.environ["GPT_PROVIDER"] = gpt_provider
        try:
            with open(".env", "a") as env_file:
                env_file.write(f"GPT_PROVIDER={gpt_provider}\n")
        except IOError as e:
            st.error(f"Failed to write GPT_PROVIDER to .env file: {e}")
        st.success(f"GPT Provider set to {gpt_provider}")

    api_key_var = supported_providers[gpt_provider.lower()]
    if not os.getenv(api_key_var):
        missing_keys[api_key_var] = ''

    if missing_keys:
        st.warning(f"API keys not found: {', '.join(missing_keys)}. Please provide them below. Restart the app after saving the keys.")
        with st.form(key='api_keys_form'):
            for key, url in missing_keys.items():
                if url:
                    st.text_input(f"{key}: 👉[Get it here]({url})👈", type="password", key=key)
                else:
                    st.text_input(f"{key}:", type="password", key=key)
            if st.form_submit_button("Save Keys"):
                with open(".env", "a") as env_file:
                    for key in missing_keys:
                        key_value = st.session_state[key]
                        env_file.write(f"{key}={key_value}\n")
                st.success("API keys saved successfully! Please restart the application.")
                st.stop()
        return False
    return True
