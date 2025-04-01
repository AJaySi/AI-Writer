"""API key manager for handling various API keys."""

from typing import Dict, Any, Optional
from loguru import logger
import streamlit as st
import os
import json
import sys
from datetime import datetime
from dotenv import load_dotenv
from .components.website_setup import render_website_setup
from .components.ai_research_setup import render_ai_research_setup
from .components.ai_providers import render_ai_providers
from .components.final_setup import render_final_setup
from .components.personalization_setup import render_personalization_setup
from .components.alwrity_integrations import render_alwrity_integrations
from .components.base import render_navigation_buttons, render_step_indicator
from .wizard_state import initialize_wizard_state, get_current_step, next_step, previous_step
from .manager import APIKeyManager
from .validation import check_all_api_keys

# Configure logger to output to both file and stdout
logger.remove()  # Remove default handler
logger.add("logs/api_key_manager.log", 
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
           level="DEBUG")
logger.add(sys.stdout, 
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
           level="INFO")

def initialize_wizard_state():
    """Initialize or get the wizard state from session"""
    logger.debug("Initializing wizard state")
    if 'wizard_state' not in st.session_state:
        st.session_state.wizard_state = {
            'current_step': 0,
            'total_steps': 0,
            'completed_steps': set(),
            'api_keys_status': {},
            'setup_progress': 0
        }
        logger.info("Created new wizard state")

def update_progress():
    """Update the overall setup progress"""
    logger.debug("Updating setup progress")
    try:
        # Get the API key manager instance from session state
        api_key_manager = st.session_state.get('api_key_manager')
        if not api_key_manager:
            logger.warning("API key manager not found in session state")
            return
            
        total_keys = sum(len(keys) for keys in api_key_manager.api_key_groups.values())
        configured_keys = sum(1 for status in st.session_state.wizard_state['api_keys_status'].values() 
                            if status.get('configured', False))
        progress = (configured_keys / total_keys) * 100
        st.session_state.wizard_state['setup_progress'] = progress
        logger.info(f"Updated progress to {progress:.1f}%")
    except Exception as e:
        logger.error(f"Error updating progress: {str(e)}", exc_info=True)

def render(api_key_manager: APIKeyManager) -> Dict[str, Any]:
    """
    Render the API key manager interface.
    
    Returns:
        Dict[str, Any]: Current state
    """
    try:
        logger.info("[render] Rendering API key manager interface")
        
        # Initialize session state for current step if not exists
        if "current_step" not in st.session_state:
            st.session_state.current_step = 1
            logger.info("[render] Initialized current_step to 1")
        
        # Display step indicator
        render_step_indicator(st.session_state.current_step, 6)
        
        # Render appropriate step based on current_step
        if st.session_state.current_step == 1:
            logger.info("[render] Rendering AI providers setup")
            return render_ai_providers(api_key_manager)
        elif st.session_state.current_step == 2:
            logger.info("[render] Rendering website setup")
            return render_website_setup(api_key_manager)
        elif st.session_state.current_step == 3:
            logger.info("[render] Rendering AI Research setup")
            return render_ai_research_setup(api_key_manager)
        elif st.session_state.current_step == 4:
            logger.info("[render] Rendering personalization setup")
            return render_personalization_setup(api_key_manager)
        elif st.session_state.current_step == 5:
            logger.info("[render] Rendering ALwrity integrations setup")
            return render_alwrity_integrations(api_key_manager)
        elif st.session_state.current_step == 6:
            logger.info("[render] Rendering final setup")
            return render_final_setup(api_key_manager)
        
    except Exception as e:
        error_msg = f"Error in API key manager: {str(e)}"
        logger.error(f"[render] {error_msg}")
        st.error(error_msg)
        return {"current_step": st.session_state.current_step, "error": error_msg}

def render_navigation(self):
    """Render navigation buttons with proper state handling"""
    st.markdown("""
        <div class="nav-buttons">
    """, unsafe_allow_html=True)
    
    # Back button
    if self.current_step > 1:
        if st.button("← Back", key="back_button"):
            self.current_step -= 1
            st.rerun()
    
    # Next/Continue button
    if self.current_step < 3:
        if st.button("Continue →", key="next_button"):
            if self.current_step == 1:
                # Validate at least one provider is configured
                if not self.validate_providers():
                    st.error("Please configure at least one AI provider to continue.")
                    return
                
                # Store all API keys in session state
                st.session_state['api_keys'] = {
                    'openai': self.openai_key,
                    'google': self.google_key,
                    'anthropic': self.anthropic_key,
                    'mistral': self.mistral_key,
                    'serpapi': self.serpapi_key,
                    'google_search': self.google_search_key,
                    'google_search_cx': self.google_search_cx,
                    'bing_search': self.bing_search_key,
                    'tavily': self.tavily_key,
                    'metaphor': self.metaphor_key,
                    'wordpress': {
                        'url': self.wordpress_url,
                        'username': self.wordpress_username,
                        'password': self.wordpress_password,
                        'app_password': self.wordpress_app_password
                    }
                }
                self.current_step = 2
                st.rerun()
            elif self.current_step == 2:
                # Validate WordPress credentials
                if not self.validate_wordpress_credentials():
                    st.error("Please configure valid WordPress credentials to continue.")
                    return
                
                # Store WordPress credentials in session state
                st.session_state['wordpress_credentials'] = {
                    'url': self.wordpress_url,
                    'username': self.wordpress_username,
                    'password': self.wordpress_password,
                    'app_password': self.wordpress_app_password
                }
                self.current_step = 3
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
