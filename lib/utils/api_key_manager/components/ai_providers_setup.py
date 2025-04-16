"""AI providers setup component for API key manager."""

from typing import Dict, Any
from loguru import logger
import streamlit as st
import os
import sys
# Corrected import: Assuming validation functions are in validation.py in the parent directory
from ..validation import (
    test_openai_api_key,
    test_gemini_api_key,
    # test_anthropic_api_key, # Keep commented if not used or add if needed
    # test_deepseek_api_key,  # Keep commented if not used or add if needed
    test_mistral_api_key
)

# Helper function to validate a specific provider's key
def _validate_provider_key(provider_name: str, key_value: str) -> bool:
    """Validate the API key for a given provider."""
    if not key_value:
        logger.debug(f"Validation: Key for {provider_name} is empty.")
        return False
    try:
        logger.debug(f"Validating key for {provider_name}...")
        if provider_name == "openai":
            # Ensure the function exists in validation.py
            if callable(getattr(sys.modules[__name__], 'test_openai_api_key', None)):
                 is_valid = test_openai_api_key(key_value)
            else:
                 logger.error("test_openai_api_key not found in validation module")
                 is_valid = False # Assume invalid if test func missing
        elif provider_name == "gemini":
            if callable(getattr(sys.modules[__name__], 'test_gemini_api_key', None)):
                 is_valid = test_gemini_api_key(key_value)
            else:
                 logger.error("test_gemini_api_key not found in validation module")
                 is_valid = False
        elif provider_name == "mistral":
            if callable(getattr(sys.modules[__name__], 'test_mistral_api_key', None)):
                 is_valid = test_mistral_api_key(key_value)
            else:
                 logger.error("test_mistral_api_key not found in validation module")
                 is_valid = False
        else:
            logger.warning(f"Validation not implemented for provider: {provider_name}")
            return False # Or True if unknown providers are allowed without validation
        
        logger.info(f"Validation result for {provider_name}: {'Valid' if is_valid else 'Invalid'}")
        return is_valid
    except Exception as e:
        logger.error(f"Error validating key for {provider_name}: {e}", exc_info=True)
        return False

# Callback function for handling API key input changes
def _handle_api_key_change(provider_name: str, api_key_manager):
    """Save and validate API key when input changes."""
    key_input_widget_key = f"{provider_name}_key_input"
    status_widget_key = f"{provider_name}_status"
    
    # Check if the input widget key exists in session state
    if key_input_widget_key not in st.session_state:
        logger.warning(f"Input widget key '{key_input_widget_key}' not found in session state.")
        return
        
    key_value = st.session_state[key_input_widget_key]
    current_status = st.session_state.get(status_widget_key)
    
    logger.debug(f"Handling change for {provider_name}. Key: {'***' if key_value else 'Empty'}. Current status: {current_status}")

    # If key is empty, reset status
    if not key_value:
        api_key_manager.save_api_key(provider_name, "") # Ensure empty key is saved
        st.session_state[status_widget_key] = "unsaved"
        logger.info(f"Cleared API key for {provider_name}.")
        return

    # Set status to saving/validating
    st.session_state[status_widget_key] = "saving"
    st.rerun() # Rerun to show the spinner immediately
    
    try:
        # Save the key using the manager
        logger.debug(f"Saving key for {provider_name}...")
        api_key_manager.save_api_key(provider_name, key_value)
        logger.info(f"Saved API key for {provider_name}.")

        # Validate the key
        is_valid = _validate_provider_key(provider_name, key_value)

        # Update status based on validation result
        if is_valid:
            st.session_state[status_widget_key] = "valid"
        else:
            st.session_state[status_widget_key] = "invalid"
            
    except Exception as e:
        logger.error(f"Error during saving/validation for {provider_name}: {e}", exc_info=True)
        st.session_state[status_widget_key] = "error"

def render_ai_providers_setup(api_key_manager) -> Dict[str, Any]:
    """
    Render the AI providers setup component with immediate feedback.
    
    Args:
        api_key_manager: API key manager instance
        
    Returns:
        Dict[str, Any]: Component state (not directly used here, handled by state manager)
    """
    try:
        logger.info("[render_ai_providers_setup] Rendering AI providers setup")
        
        # Initialize status in session state if not present
        for provider in ["openai", "gemini", "mistral"]:
            status_key = f"{provider}_status"
            if status_key not in st.session_state:
                # Check if a key exists and try to validate it on first load
                existing_key = api_key_manager.get_api_key(provider)
                if existing_key:
                    if _validate_provider_key(provider, existing_key):
                        st.session_state[status_key] = "valid"
                    else:
                        # Keep it unsaved/invalid on load if pre-existing key is bad
                        # Or maybe set to invalid? Let's choose unsaved for now.
                         st.session_state[status_key] = "invalid" 
                else:
                     st.session_state[status_key] = "unsaved"

        # Display section header
        st.header("Step 1: Configure AI Providers")
        st.markdown("""
        Configure your AI providers to enable advanced content generation capabilities.
        Enter your API keys below. They will be validated automatically.
        """)
        
        # --- OpenAI --- 
        st.subheader("OpenAI (Required)")
        st.markdown("Get your API key from: [OpenAI Dashboard](https://platform.openai.com/account/api-keys)")
        openai_key = api_key_manager.get_api_key("openai")
        st.text_input(
            "OpenAI API Key",
            value=openai_key if openai_key else "",
            type="password",
            key="openai_key_input",
            on_change=_handle_api_key_change,
            args=("openai", api_key_manager)
        )
        # Feedback Area for OpenAI
        openai_status = st.session_state.get("openai_status", "unsaved")
        feedback_placeholder_openai = st.empty()
        if openai_status == "saving":
            feedback_placeholder_openai.info("Validating OpenAI key...", icon="⏳")
        elif openai_status == "valid":
            feedback_placeholder_openai.success("OpenAI key saved and valid!", icon="✅")
        elif openai_status == "invalid":
            feedback_placeholder_openai.error("Invalid OpenAI key. Please check and try again.", icon="❌")
        elif openai_status == "error":
            feedback_placeholder_openai.error("Error saving/validating OpenAI key.", icon="⚠️")
        
        # --- Google Gemini --- 
        st.subheader("Google Gemini (Required)")
        st.markdown("Get your API key from: [Google AI Studio](https://makersuite.google.com/app/apikey)")
        gemini_key = api_key_manager.get_api_key("gemini")
        st.text_input(
            "Gemini API Key",
            value=gemini_key if gemini_key else "",
            type="password",
            key="gemini_key_input",
            on_change=_handle_api_key_change,
            args=("gemini", api_key_manager)
        )
        # Feedback Area for Gemini
        gemini_status = st.session_state.get("gemini_status", "unsaved")
        feedback_placeholder_gemini = st.empty()
        if gemini_status == "saving":
            feedback_placeholder_gemini.info("Validating Gemini key...", icon="⏳")
        elif gemini_status == "valid":
            feedback_placeholder_gemini.success("Gemini key saved and valid!", icon="✅")
        elif gemini_status == "invalid":
            feedback_placeholder_gemini.error("Invalid Gemini key. Please check and try again.", icon="❌")
        elif gemini_status == "error":
            feedback_placeholder_gemini.error("Error saving/validating Gemini key.", icon="⚠️")

        # --- Mistral AI (Optional) ---
        st.subheader("Mistral AI (Optional)")
        st.markdown("Get your API key from: [Mistral Platform](https://console.mistral.ai/api-keys/)")
        mistral_key = api_key_manager.get_api_key("mistral")
        st.text_input(
            "Mistral API Key",
            value=mistral_key if mistral_key else "",
            type="password",
            key="mistral_key_input",
            on_change=_handle_api_key_change,
            args=("mistral", api_key_manager)
        )
        # Feedback Area for Mistral
        mistral_status = st.session_state.get("mistral_status", "unsaved")
        feedback_placeholder_mistral = st.empty()
        if mistral_status == "saving":
            feedback_placeholder_mistral.info("Validating Mistral key...", icon="⏳")
        elif mistral_status == "valid":
            feedback_placeholder_mistral.success("Mistral key saved and valid!", icon="✅")
        elif mistral_status == "invalid":
            feedback_placeholder_mistral.error("Invalid Mistral key. Please check and try again.", icon="❌")
        elif mistral_status == "error":
            feedback_placeholder_mistral.error("Error saving/validating Mistral key.", icon="⚠️")

        # --- Final Notes --- 
        st.info("Note: At least one AI provider (OpenAI or Google Gemini) must have a valid API key to proceed.")
        
        # Return value is not strictly needed if navigation relies on session state status
        return {}

    except Exception as e:
        error_msg = f"Error rendering AI providers setup: {str(e)}"
        logger.error(f"[render_ai_providers_setup] {error_msg}", exc_info=True)
        st.error(error_msg)
        return {"error": error_msg}
