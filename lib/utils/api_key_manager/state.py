"""State management for the API key manager."""

import streamlit as st
from datetime import datetime

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

def update_progress(api_keys_config):
    """Update the overall setup progress."""
    total_keys = sum(len(keys) for keys in api_keys_config.values())
    configured_keys = sum(1 for status in st.session_state.wizard_state['api_keys_status'].values() 
                         if status.get('configured', False))
    st.session_state.wizard_state['setup_progress'] = (configured_keys / total_keys) * 100

def update_key_status(key):
    """Update the status of an API key in the wizard state."""
    st.session_state.wizard_state['api_keys_status'][key] = {
        'configured': True,
        'timestamp': datetime.now().isoformat()
    }

def get_key_status(key):
    """Get the current status of an API key."""
    return st.session_state.wizard_state['api_keys_status'].get(key, {})

def get_progress():
    """Get the current setup progress."""
    return st.session_state.wizard_state['setup_progress']