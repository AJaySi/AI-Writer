"""API Key Rotation Manager."""

from datetime import datetime
from typing import Dict, Optional, List
import streamlit as st
from .health_monitor import APIKeyHealthMonitor
from .wizard_state import get_api_keys, set_api_key

class KeyRotationManager:
    """Manages automatic rotation of API keys based on health metrics."""

    def __init__(self):
        """Initialize the key rotation manager."""
        self.health_monitor = APIKeyHealthMonitor()
        if 'active_keys' not in st.session_state:
            st.session_state.active_keys = {}

    def get_active_key(self, key_type: str) -> str:
        """Get the currently active key for a given type."""
        return st.session_state.active_keys.get(key_type)

    def set_active_key(self, key_type: str, key_name: str) -> None:
        """Set the active key for a given type."""
        st.session_state.active_keys[key_type] = key_name

    def rotate_if_needed(self, key_type: str) -> Optional[str]:
        """Check and rotate key if needed based on health metrics."""
        current_key = self.get_active_key(key_type)
        
        # If no current key or current key needs rotation
        if not current_key or self.health_monitor.should_rotate_key(current_key):
            new_key = self.health_monitor.get_best_available_key(key_type)
            
            if new_key and new_key != current_key:
                # Set cooldown on the old key if it exists
                if current_key:
                    self.health_monitor.set_cooldown(current_key, duration_minutes=30)
                
                # Update the active key
                self.set_active_key(key_type, new_key)
                return new_key
        
        return current_key

    def get_rotation_status(self) -> Dict[str, Dict]:
        """Get rotation status for all key types."""
        status = {}
        api_keys = get_api_keys()
        
        for key_name in api_keys:
            key_type = key_name.split('_')[0]  # e.g., OPENAI from OPENAI_API_KEY
            
            active_key = self.get_active_key(key_type)
            health = self.health_monitor.get_key_health(key_name)
            
            if key_type not in status:
                status[key_type] = {
                    'active_key': active_key,
                    'available_keys': [],
                    'cooldown_keys': []
                }
            
            if health and health['in_cooldown']:
                status[key_type]['cooldown_keys'].append(key_name)
            else:
                status[key_type]['available_keys'].append(key_name)

        return status

    def display_rotation_dashboard(self) -> None:
        """Display the key rotation dashboard."""
        st.subheader("🔄 API Key Rotation Status")
        
        rotation_status = self.get_rotation_status()
        if not rotation_status:
            st.info("No API keys configured for rotation.")
            return

        for key_type, status in rotation_status.items():
            with st.expander(f"{key_type} Rotation Status"):
                # Active Key
                st.write("**Active Key:**")
                if status['active_key']:
                    st.success(status['active_key'])
                else:
                    st.warning("No active key")

                # Available Keys
                st.write("**Available Keys:**")
                if status['available_keys']:
                    for key in status['available_keys']:
                        st.write(f"- {key}")
                else:
                    st.warning("No available keys")

                # Cooldown Keys
                if status['cooldown_keys']:
                    st.write("**Keys in Cooldown:**")
                    for key in status['cooldown_keys']:
                        health = self.health_monitor.get_key_health(key)
                        if health and health['cooldown_until']:
                            time_left = (health['cooldown_until'] - datetime.now())
                            minutes_left = int(time_left.total_seconds() / 60)
                            st.info(f"- {key} (Cooldown: {minutes_left} minutes remaining)")

    def initialize_rotation(self) -> None:
        """Initialize key rotation for all API key types."""
        api_keys = get_api_keys()
        key_types = set()
        
        # Get unique key types
        for key_name in api_keys:
            key_type = key_name.split('_')[0]
            key_types.add(key_type)
        
        # Initialize rotation for each key type
        for key_type in key_types:
            if not self.get_active_key(key_type):
                best_key = self.health_monitor.get_best_available_key(key_type)
                if best_key:
                    self.set_active_key(key_type, best_key)