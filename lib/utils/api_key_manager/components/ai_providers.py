"""AI providers setup component - Wrapper for the actual setup UI."""

import streamlit as st
from loguru import logger
from typing import Dict, Any
from ..manager import APIKeyManager
from .ai_providers_setup import render_ai_providers_setup # Import the refactored setup UI

def render_ai_providers(api_key_manager: APIKeyManager) -> Dict[str, Any]:
    """Renders the AI providers setup step by calling the dedicated setup function."""
    logger.debug("[render_ai_providers] Calling render_ai_providers_setup")
    try:
        # The actual UI, saving, validation, and feedback are now handled within render_ai_providers_setup
        # This function acts primarily as a placeholder in the step sequence if needed,
        # or can be bypassed entirely if the main wizard calls render_ai_providers_setup directly.
        
        # Store the manager instance if needed by other potential logic (unlikely now)
        if 'api_key_manager' not in st.session_state:
             st.session_state['api_key_manager'] = api_key_manager
             
        # Call the function that now contains all the rendering and logic for this step
        component_state = render_ai_providers_setup(api_key_manager)
        
        # Return the state from the setup function, although it might not be used directly
        return component_state

    except Exception as e:
        error_msg = f"Error calling AI providers setup: {str(e)}"
        logger.error(f"[render_ai_providers] {error_msg}", exc_info=True)
        st.error("An error occurred while setting up AI providers.")
        # Ensure consistency in error return format if expected by the caller
        return {"error": error_msg}
