import os
import streamlit as st
from dotenv import load_dotenv

import os
import streamlit as st

import os
import streamlit as st

def check_api_keys():
    """Checks for API keys and returns a list of missing keys."""
    required_keys = ["GOOGLE_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
    missing_keys = []
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    return missing_keys



