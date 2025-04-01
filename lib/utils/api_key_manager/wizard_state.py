"""Wizard state management for the API key manager."""

import streamlit as st
from loguru import logger

def initialize_wizard_state():
    """Initialize or get the wizard state from session."""
    if 'wizard_state' not in st.session_state:
        st.session_state.wizard_state = {
            'current_step': 0,
            'total_steps': 0,
            'completed_steps': set(),
            'api_keys_status': {},
            'setup_progress': 0
        }
        logger.info("Initialized wizard state")

def get_current_step():
    """Get the current step from the wizard state."""
    return st.session_state.wizard_state.get('current_step', 0)

def next_step():
    """Move to the next step in the wizard."""
    current_step = get_current_step()
    st.session_state.wizard_state['current_step'] = current_step + 1
    st.session_state.wizard_state['completed_steps'].add(current_step)
    logger.info(f"Moving to next step: {current_step + 1}")

def previous_step():
    """Move to the previous step in the wizard."""
    current_step = get_current_step()
    if current_step > 0:
        st.session_state.wizard_state['current_step'] = current_step - 1
        st.session_state.wizard_state['completed_steps'].discard(current_step - 1)
        logger.info(f"Moving to previous step: {current_step - 1}")

def update_progress():
    """Update the overall setup progress."""
    total_steps = st.session_state.wizard_state.get('total_steps', 0)
    completed_steps = len(st.session_state.wizard_state.get('completed_steps', set()))
    if total_steps > 0:
        progress = (completed_steps / total_steps) * 100
        st.session_state.wizard_state['setup_progress'] = progress
        logger.info(f"Updated progress: {progress:.1f}%")

def is_step_completed(step):
    """Check if a specific step is completed."""
    return step in st.session_state.wizard_state.get('completed_steps', set())

def get_step_status(step):
    """Get the status of a specific step."""
    current_step = get_current_step()
    if step < current_step:
        return "completed"
    elif step == current_step:
        return "current"
    else:
        return "pending"

def can_proceed_to_next_step():
    """Check if the user can proceed to the next step."""
    current_step = get_current_step()
    
    if current_step == 1:
        # Get selected providers
        selected_providers = get_selected_providers()
        
        # If no providers are selected, cannot proceed
        if not selected_providers:
            return False
        
        # Check if at least one selected provider has a valid API key
        for provider in selected_providers:
            validation_status = get_validation_status(provider)
            if validation_status and validation_status.get('is_valid', False):
                return True
        
        return False
    
    elif current_step == 2:
        # Website URL is now optional
        return True
    
    elif current_step == 3:
        # AI Research setup - both Tavily and Metaphor are optional
        return True
    
    elif current_step == 4:
        # Final setup - always allow proceeding
        return True
    
    return False
