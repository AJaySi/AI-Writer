"""AI providers setup component for API key manager."""

from typing import Dict, Any
from loguru import logger
import streamlit as st
import os
import sys

def render_ai_providers_setup(api_key_manager) -> Dict[str, Any]:
    """
    Render the AI providers setup component.
    
    Args:
        api_key_manager: API key manager instance
        
    Returns:
        Dict[str, Any]: Component state
    """
    try:
        logger.info("[render_ai_providers_setup] Rendering AI providers setup")
        
        # Display section header
        st.header("Step 1: Select AI Providers")
        st.markdown("""
        Configure your AI providers to enable advanced content generation capabilities.
        Choose and set up the AI services you want to use.
        """)
        
        # Create columns for different providers
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("OpenAI")
            st.markdown("""
            OpenAI's GPT models provide powerful natural language processing capabilities.
            
            Get your API key from: [OpenAI Dashboard](https://platform.openai.com/account/api-keys)
            """)
            
            openai_key = api_key_manager.get_api_key("openai")
            openai_input = st.text_input(
                "OpenAI API Key",
                value=openai_key if openai_key else "",
                type="password",
                key="openai_key_input"
            )
        
        with col2:
            st.subheader("Google Gemini")
            st.markdown("""
            Google's Gemini models offer advanced AI capabilities.
            
            Get your API key from: [Google AI Studio](https://makersuite.google.com/app/apikey)
            """)
            
            gemini_key = api_key_manager.get_api_key("gemini")
            gemini_input = st.text_input(
                "Gemini API Key",
                value=gemini_key if gemini_key else "",
                type="password",
                key="gemini_key_input"
            )
        
        # Optional AI Provider
        st.subheader("Additional AI Provider (Optional)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            Mistral AI provides an alternative model for content generation.
            
            Get your API key from: [Mistral Platform](https://console.mistral.ai/api-keys/)
            """)
            
            mistral_key = api_key_manager.get_api_key("mistral")
            mistral_input = st.text_input(
                "Mistral API Key (Optional)",
                value=mistral_key if mistral_key else "",
                type="password",
                key="mistral_key_input"
            )
        
        # Add a note about saving
        st.info("""
        Note: At least one AI provider (OpenAI or Google Gemini) is required.
        Click Continue to save your keys and proceed.
        """)
        
        # Save keys if they've changed when proceeding to next step
        if st.session_state.get('wizard_current_step', 1) > 1:
            if openai_input != openai_key:
                api_key_manager.save_api_key("openai", openai_input)
                logger.info("[render_ai_providers_setup] OpenAI API key saved")
            
            if gemini_input != gemini_key:
                api_key_manager.save_api_key("gemini", gemini_input)
                logger.info("[render_ai_providers_setup] Gemini API key saved")
            
            if mistral_input != mistral_key:
                api_key_manager.save_api_key("mistral", mistral_input)
                logger.info("[render_ai_providers_setup] Mistral API key saved")
            
            # Validate that at least one required provider is configured
            if not (openai_input or gemini_input):
                st.error("Please configure at least one AI provider (OpenAI or Google Gemini) to proceed.")
                return {"current_step": 1, "can_proceed": False}
        
        return {"current_step": 1, "can_proceed": bool(openai_input or gemini_input)}
        
    except Exception as e:
        error_msg = f"Error in AI providers setup: {str(e)}"
        logger.error(f"[render_ai_providers_setup] {error_msg}")
        st.error(error_msg)
        return {"current_step": 1, "error": error_msg}
