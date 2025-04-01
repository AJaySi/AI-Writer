"""Health monitoring component for the API key manager."""

import streamlit as st
from loguru import logger
from ..health_monitor import APIKeyHealthMonitor
from ..key_rotation import KeyRotationManager
from ..wizard_state import get_api_keys

def render_health_monitoring():
    """Render the API key health monitoring dashboard."""
    st.header("API Key Health & Rotation")
    
    # Initialize managers
    health_monitor = APIKeyHealthMonitor()
    rotation_manager = KeyRotationManager()
    
    # Create tabs for different views
    health_tab, rotation_tab = st.tabs(["Health Monitor", "Key Rotation"])
    
    with health_tab:
        health_monitor.get_health_dashboard()
    
    with rotation_tab:
        rotation_manager.display_rotation_dashboard()
        
        # Manual rotation controls
        st.subheader("Manual Controls")
        key_type = st.selectbox(
            "Select Key Type",
            options=[k.split('_')[0] for k in get_api_keys()]
        )
        
        if key_type:
            if st.button("Force Rotation"):
                new_key = rotation_manager.rotate_if_needed(key_type)
                if new_key:
                    st.success(f"Rotated to new key: {new_key}")
                else:
                    st.warning("No suitable key available for rotation")
