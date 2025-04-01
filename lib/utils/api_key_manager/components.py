"""API key manager components."""

import asyncio
import streamlit as st
import os
from loguru import logger
from .styles import API_KEY_MANAGER_STYLES
from .config import FEATURE_PREVIEWS, API_KEY_CONFIGS
from .wizard_state import (
    get_current_step,
    next_step,
    previous_step,
    set_selected_providers,
    get_selected_providers,
    set_website_url,
    get_website_url,
    set_api_key,
    get_api_key,
    can_proceed_to_next_step,
    get_api_keys
)
from .health_monitor import APIKeyHealthMonitor
from .key_rotation import KeyRotationManager
from ...utils.website_analyzer import analyze_website
from .api_key_tests import (
    test_openai_api_key,
    test_gemini_api_key,
    test_anthropic_api_key,
    test_deepseek_api_key,
    test_mistral_api_key
)
from .components.base import render_step_indicator, render_navigation_buttons, render_success_message
from .components import (
    render_ai_providers,
    render_website_setup,
    render_health_monitoring,
    render_ai_research_setup,
    render_final_setup
)

def render_wizard():
    """Render the main wizard interface."""
    st.title("API Key Setup Wizard")
    
    # Get current step
    current_step = get_current_step()
    
    # Render step indicator
    render_step_indicator()
    
    # Render current step content
    if current_step == 1:
        render_ai_providers()
    elif current_step == 2:
        render_website_setup()
    elif current_step == 3:
        render_ai_research_setup()
    elif current_step == 4:
        render_final_setup()
    elif current_step == 5:
        render_health_monitoring()
    
    # Render navigation buttons
    render_navigation_buttons()

__all__ = [
    'render_wizard',
    'render_step_indicator',
    'render_navigation_buttons',
    'render_success_message',
    'render_ai_providers',
    'render_website_setup',
    'render_ai_research_setup',
    'render_health_monitoring',
    'render_final_setup'
]