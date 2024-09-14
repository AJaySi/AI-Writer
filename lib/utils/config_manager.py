import json
import os
import streamlit as st

def save_config(config):
    """
    Saves the provided configuration dictionary to a JSON file specified by the environment variable.
    """
    try:
        with open(os.getenv("ALWRITY_CONFIG"), "w") as config_file:
            json.dump(config, config_file, indent=4)
    except Exception as e:
        st.error(f"An error occurred while saving the configuration: {e}")
