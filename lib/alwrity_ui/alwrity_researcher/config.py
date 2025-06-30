import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_api_key(key_name):
    """Get API key from environment variables or Streamlit secrets"""
    # Try to get from environment variables first
    api_key = os.getenv(key_name)
    
    # If not found in environment, try Streamlit secrets
    if not api_key and key_name in st.secrets:
        api_key = st.secrets[key_name]
        
    return api_key

def check_api_configuration():
    """Check if all required API keys are configured"""
    api_status = {
        "SERPER_API_KEY": bool(get_api_key("SERPER_API_KEY")),
        "TAVILY_API_KEY": bool(get_api_key("TAVILY_API_KEY")),
        "METAPHOR_API_KEY": bool(get_api_key("METAPHOR_API_KEY")),
        "FIRECRAWL_API_KEY": bool(get_api_key("FIRECRAWL_API_KEY"))
    }
    
    return api_status

def display_api_configuration_status():
    """Display API configuration status in the sidebar with improved styling"""
    api_status = check_api_configuration()
    
    st.sidebar.markdown("<div class='api-status-container'>", unsafe_allow_html=True)
    st.sidebar.markdown("<div class='api-status-title'>API Configuration Status</div>", unsafe_allow_html=True)
    
    # Display API status with improved styling
    for api_name, is_configured in api_status.items():
        if is_configured:
            st.sidebar.markdown(
                f"<div class='api-status-item configured'>✅ {api_name}</div>", 
                unsafe_allow_html=True
            )
        else:
            st.sidebar.markdown(
                f"<div class='api-status-item not-configured'>❌ {api_name}</div>", 
                unsafe_allow_html=True
            )
    
    # Display instructions if any API key is missing with improved styling
    if not all(api_status.values()):
        with st.sidebar.expander("How to configure API keys"):
            st.markdown("""
            <div style="background-color: #f8fafc; padding: 12px; border-radius: 6px; border-left: 4px solid #3b82f6;">
                <p style="margin-bottom: 10px; font-weight: 500;">To configure missing API keys, create a <code>.env</code> file in the project root with the following format:</p>
                <pre style="background-color: #f1f5f9; padding: 10px; border-radius: 4px; overflow-x: auto; font-size: 0.9em;">
SERPER_API_KEY=your_serper_api_key
TAVILY_API_KEY=your_tavily_api_key
METAPHOR_API_KEY=your_metaphor_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
                </pre>
                <p style="margin-top: 10px;">Alternatively, you can set these as environment variables in your system.</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.sidebar.markdown("</div>", unsafe_allow_html=True)