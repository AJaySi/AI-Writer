"""Page for AI Research Setup redirection."""

import streamlit as st
from loguru import logger
import sys
import os

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    "logs/ai_research_setup_page.log",
    rotation="500 MB",
    retention="10 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True
)
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>"
)

# Set page config
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

def render_ai_research_setup_page():
    """Render the AI Research Setup page."""
    try:
        logger.info("Starting AI Research Setup page")
        
        # Import and render the AI Research Setup component
        from lib.utils.api_key_manager.components.ai_research_setup import render_ai_research_setup
        render_ai_research_setup()
        
    except Exception as e:
        logger.error(f"Error in render_ai_research_setup_page: {str(e)}")
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    render_ai_research_setup_page() 