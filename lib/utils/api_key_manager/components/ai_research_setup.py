"""AI research setup component for the API key manager."""

import streamlit as st
from loguru import logger
from typing import Dict, Any
from ..manager import APIKeyManager
# Removed import of render_navigation_buttons as it's handled in base
import os
from dotenv import load_dotenv # Keep if api_key_manager uses it
import sys
# Import test functions (adjust path if needed)
from ..api_key_tests import (
    test_serpapi_key,
    test_tavily_key,
    test_metaphor_key,
    test_firecrawl_key
    # Add others if needed later, e.g., test_bing_key, test_google_search_key
)

# Configure logger (assuming configured elsewhere or keep minimal here)
logger.add(sys.stderr, level="INFO") # Keep simple example if needed

# Helper function to validate a specific research provider's key
def _validate_research_key(provider_name: str, key_value: str) -> bool:
    """Validate the API key for a given research provider."""
    if not key_value:
        logger.debug(f"Validation: Key for {provider_name} is empty.")
        return False
    try:
        logger.debug(f"Validating key for {provider_name}...")
        if provider_name == "serpapi":
            is_valid = test_serpapi_key(key_value)
        elif provider_name == "tavily":
            is_valid = test_tavily_key(key_value)
        elif provider_name == "metaphor":
            is_valid = test_metaphor_key(key_value)
        elif provider_name == "firecrawl":
            is_valid = test_firecrawl_key(key_value)
        else:
            logger.warning(f"Validation not implemented for research provider: {provider_name}")
            return False # Default to False for unknown providers
        
        logger.info(f"Validation result for {provider_name}: {'Valid' if is_valid else 'Invalid'}")
        return is_valid
    except Exception as e:
        logger.error(f"Error validating key for {provider_name}: {e}", exc_info=True)
        return False

# Callback function for handling API key input changes
def _handle_research_key_change(provider_name: str, api_key_manager):
    """Save and validate research API key when input changes."""
    key_input_widget_key = f"{provider_name}_key_input"
    status_widget_key = f"{provider_name}_status"
    
    if key_input_widget_key not in st.session_state:
        logger.warning(f"Input widget key '{key_input_widget_key}' not found in session state.")
        return
        
    key_value = st.session_state[key_input_widget_key]
    current_status = st.session_state.get(status_widget_key)
    
    logger.debug(f"Handling research key change for {provider_name}. Key: {'***' if key_value else 'Empty'}. Current status: {current_status}")

    if not key_value:
        api_key_manager.save_api_key(provider_name, "")
        st.session_state[status_widget_key] = "unsaved"
        logger.info(f"Cleared API key for {provider_name}.")
        return

    st.session_state[status_widget_key] = "saving"
    st.rerun()
    
    try:
        logger.debug(f"Saving key for {provider_name}...")
        api_key_manager.save_api_key(provider_name, key_value)
        logger.info(f"Saved API key for {provider_name}.")

        is_valid = _validate_research_key(provider_name, key_value)

        if is_valid:
            st.session_state[status_widget_key] = "valid"
        else:
            st.session_state[status_widget_key] = "invalid"
            
    except Exception as e:
        logger.error(f"Error during saving/validation for {provider_name}: {e}", exc_info=True)
        st.session_state[status_widget_key] = "error"

def render_ai_research_setup(api_key_manager: APIKeyManager) -> Dict[str, Any]:
    """Render the AI research setup step with immediate feedback."""
    logger.info("[render_ai_research_setup] Rendering AI research setup component")
    
    research_providers = ["serpapi", "tavily", "metaphor", "firecrawl"]
    
    # Initialize statuses
    for provider in research_providers:
        status_key = f"{provider}_status"
        if status_key not in st.session_state:
            existing_key = api_key_manager.get_api_key(provider)
            if existing_key:
                if _validate_research_key(provider, existing_key):
                    st.session_state[status_key] = "valid"
                else:
                     st.session_state[status_key] = "invalid" 
            else:
                 st.session_state[status_key] = "unsaved"

    st.markdown("""
        <div class='setup-header'>
            <h2>Step 3: Configure AI Research Tools (Optional)</h2>
            <p>Set up API keys for enhanced web research, crawling, and analysis. These are optional but recommended.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # --- SerpAPI --- 
    with col1:
        st.subheader("SerpAPI")
        st.markdown("Access real-time search engine results. Get key: [SerpAPI](https://serpapi.com)")
        serpapi_key_val = api_key_manager.get_api_key("serpapi")
        st.text_input(
            "SerpAPI Key",
            value=serpapi_key_val if serpapi_key_val else "",
            type="password",
            key="serpapi_key_input",
            on_change=_handle_research_key_change,
            args=("serpapi", api_key_manager)
        )
        # Feedback Area
        serpapi_status = st.session_state.get("serpapi_status", "unsaved")
        feedback_placeholder_serpapi = st.empty()
        if serpapi_status == "saving":
            feedback_placeholder_serpapi.info("Validating SerpAPI key...", icon="⏳")
        elif serpapi_status == "valid":
            feedback_placeholder_serpapi.success("SerpAPI key saved and valid!", icon="✅")
        elif serpapi_status == "invalid":
            feedback_placeholder_serpapi.error("Invalid SerpAPI key.", icon="❌")
        elif serpapi_status == "error":
            feedback_placeholder_serpapi.error("Error saving/validating SerpAPI key.", icon="⚠️")

    # --- Firecrawl --- 
    with col1:
        st.subheader("Firecrawl")
        st.markdown("Web content extraction and crawling. Get key: [Firecrawl](https://www.firecrawl.dev/account)")
        firecrawl_key_val = api_key_manager.get_api_key("firecrawl")
        st.text_input(
            "Firecrawl API Key",
            value=firecrawl_key_val if firecrawl_key_val else "",
            type="password",
            key="firecrawl_key_input",
            on_change=_handle_research_key_change,
            args=("firecrawl", api_key_manager)
        )
        # Feedback Area
        firecrawl_status = st.session_state.get("firecrawl_status", "unsaved")
        feedback_placeholder_firecrawl = st.empty()
        if firecrawl_status == "saving":
            feedback_placeholder_firecrawl.info("Validating Firecrawl key...", icon="⏳")
        elif firecrawl_status == "valid":
            feedback_placeholder_firecrawl.success("Firecrawl key saved and valid!", icon="✅")
        elif firecrawl_status == "invalid":
            feedback_placeholder_firecrawl.error("Invalid Firecrawl key.", icon="❌")
        elif firecrawl_status == "error":
            feedback_placeholder_firecrawl.error("Error saving/validating Firecrawl key.", icon="⚠️")
            
    # --- Tavily --- 
    with col2:
        st.subheader("Tavily AI")
        st.markdown("AI-powered search & summarization. Get key: [Tavily](https://tavily.com)")
        tavily_key_val = api_key_manager.get_api_key("tavily")
        st.text_input(
            "Tavily API Key",
            value=tavily_key_val if tavily_key_val else "",
            type="password",
            key="tavily_key_input",
            on_change=_handle_research_key_change,
            args=("tavily", api_key_manager)
        )
        # Feedback Area
        tavily_status = st.session_state.get("tavily_status", "unsaved")
        feedback_placeholder_tavily = st.empty()
        if tavily_status == "saving":
            feedback_placeholder_tavily.info("Validating Tavily key...", icon="⏳")
        elif tavily_status == "valid":
            feedback_placeholder_tavily.success("Tavily key saved and valid!", icon="✅")
        elif tavily_status == "invalid":
            feedback_placeholder_tavily.error("Invalid Tavily key.", icon="❌")
        elif tavily_status == "error":
            feedback_placeholder_tavily.error("Error saving/validating Tavily key.", icon="⚠️")

    # --- Metaphor/Exa --- 
    with col2:
        st.subheader("Metaphor/Exa")
        st.markdown("Neural search for deep research. Get key: [Metaphor/Exa](https://metaphor.systems)")
        metaphor_key_val = api_key_manager.get_api_key("metaphor")
        st.text_input(
            "Metaphor/Exa API Key",
            value=metaphor_key_val if metaphor_key_val else "",
            type="password",
            key="metaphor_key_input",
            on_change=_handle_research_key_change,
            args=("metaphor", api_key_manager)
        )
        # Feedback Area
        metaphor_status = st.session_state.get("metaphor_status", "unsaved")
        feedback_placeholder_metaphor = st.empty()
        if metaphor_status == "saving":
            feedback_placeholder_metaphor.info("Validating Metaphor/Exa key...", icon="⏳")
        elif metaphor_status == "valid":
            feedback_placeholder_metaphor.success("Metaphor/Exa key saved and valid!", icon="✅")
        elif metaphor_status == "invalid":
            feedback_placeholder_metaphor.error("Invalid Metaphor/Exa key.", icon="❌")
        elif metaphor_status == "error":
            feedback_placeholder_metaphor.error("Error saving/validating Metaphor/Exa key.", icon="⚠️")

    # --- Coming Soon --- 
    with st.expander("🔜 Coming Soon - More Search Options", expanded=False):
        st.info("Integrations for Bing Search and Google Search APIs are planned.")

    st.info("You can skip this step if you don't need these research tools. Click Continue to proceed.")
    
    # Removed the old saving logic block here
    
    return {}
