import os
import streamlit as st
from dotenv import load_dotenv


@st.cache_data
def check_api_keys():
    """
    Checks if the required API keys are present in the environment variables.
    Prompts the user to enter missing keys and saves them in the .env file.
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
    if missing_keys:
        st.error("🚨 Some API keys are missing! Please provide them below:")
        for key, url in missing_keys.items():
            api_key = st.text_input(f"Enter 🔏 {key}: 👉[Get it here]({url})👈")
            if api_key:
                os.environ[key] = api_key
                try:
                    with open(".env", "a") as env_file:
                        env_file.write(f"{key}={api_key}\n")
                except IOError as e:
                    st.error(f"Failed to write {key} to .env file: {e}")
                st.success(f"✅ {key} added successfully!")
        return False
    return True
@st.cache_data
def check_llm_environs():
    """
    Ensures that the LLM provider and corresponding API key are set.
    Prompts the user to select a provider and enter the API key if missing.
    """
    gpt_provider = os.getenv("GPT_PROVIDER")
    supported_providers = {
        'google': "GEMINI_API_KEY",
        'openai': "OPENAI_API_KEY",
        'mistralai': "MISTRAL_API_KEY"
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
        api_key = st.text_input(f"Enter {api_key_var}:")
        if api_key:
            os.environ[api_key_var] = api_key
            with open(".env", "a") as env_file:
                env_file.write(f"{api_key_var}={api_key}\n")
            st.success(f"{api_key_var} added successfully!")
        return False
    return True




