"""Final setup component for the API key manager."""

import streamlit as st
from loguru import logger
import sys
import json
import os
from typing import Dict, Any
from ..manager import APIKeyManager
from ..validation import check_all_api_keys

# Configure logger to output to both file and stdout
logger.remove()  # Remove default handler
logger.add(
    "logs/final_setup.log",
    rotation="500 MB",
    retention="10 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>"
)

def load_main_config() -> Dict[str, Any]:
    """Load the main configuration file."""
    config_path = os.path.join("lib", "workspace", "alwrity_config", "main_config.json")
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading main_config.json: {str(e)}")
        return {}

def render_final_setup(api_key_manager: APIKeyManager) -> Dict[str, Any]:
    """Render the final setup step.
    
    Args:
        api_key_manager (APIKeyManager): The API key manager instance
        
    Returns:
        Dict[str, Any]: Current state
    """
    logger.info("[render_final_setup] Rendering final setup component")
    
    st.markdown("### Step 5: Final Setup")
    
    # Load main config
    main_config = load_main_config()
    
    # Display configuration summary
    st.markdown("#### Configuration Summary")
    
    # Blog Content Characteristics
    st.markdown("##### Blog Content Characteristics")
    blog_settings = main_config.get("Blog Content Characteristics", {})
    st.write(f"- Blog Length: {blog_settings.get('Blog Length', '2000')}")
    st.write(f"- Blog Tone: {blog_settings.get('Blog Tone', 'Professional')}")
    st.write(f"- Blog Demographic: {blog_settings.get('Blog Demographic', 'Professional')}")
    st.write(f"- Blog Type: {blog_settings.get('Blog Type', 'Informational')}")
    
    # LLM Options
    st.markdown("##### LLM Options")
    llm_settings = main_config.get("LLM Options", {})
    st.write(f"- GPT Provider: {llm_settings.get('GPT Provider', 'google')}")
    st.write(f"- Model: {llm_settings.get('Model', 'gemini-1.5-flash-latest')}")
    st.write(f"- Temperature: {llm_settings.get('Temperature', 0.7)}")
    st.write(f"- Max Tokens: {llm_settings.get('Max Tokens', 4000)}")
    
    # Personalization Settings
    st.markdown("##### Personalization Settings")
    personalization = main_config.get("personalization", {})
    st.write(f"- Writing Tone: {personalization.get('writing_tone', 'Professional')}")
    st.write(f"- Target Audience: {personalization.get('target_audience', 'General')}")
    st.write(f"- Content Type: {personalization.get('content_type', 'Blog Posts')}")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back to Personalization"):
            logger.info("[render_final_setup] User clicked back to personalization")
            st.session_state.current_step = 4
            st.session_state.next_step = "personalization_setup"
            st.rerun()
    
    with col2:
        if st.button("Complete Setup →"):
            logger.info("[render_final_setup] User clicked complete setup")
            try:
                # Verify all required API keys are present and valid
                is_valid = check_all_api_keys(api_key_manager)
                
                if not is_valid:
                    st.error("⚠️ Some required API keys are missing")
                    st.markdown("### Missing API Keys and Impact")
                    
                    # Display impact messages
                    st.warning("⚠️ Missing AI Provider: At least one AI provider (OpenAI, Google Gemini, Anthropic Claude, or Mistral) is required.")
                    st.warning("⚠️ Missing Research Provider: At least one research provider (SerpAPI, Tavily, Metaphor, or Firecrawl) is required.")
                    
                    st.markdown("""
                        <div style='background-color: #fff3cd; color: #856404; padding: 1rem; border-radius: 0.25rem; margin-top: 1rem;'>
                            <h4 style='margin: 0;'>Required Keys:</h4>
                            <ul style='margin: 0.5rem 0 0;'>
                                <li>At least one AI provider (OpenAI, Google Gemini, Anthropic Claude, or Mistral)</li>
                                <li>At least one research provider (SerpAPI, Tavily, Metaphor, or Firecrawl)</li>
                            </ul>
                            <p style='margin: 0.5rem 0 0;'>Please configure the required keys before proceeding.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    return {"current_step": 6, "changes_made": True}

                # Save final configuration
                if not os.path.exists("lib/workspace/alwrity_config"):
                    os.makedirs("lib/workspace/alwrity_config")
                
                config_path = os.path.join("lib", "workspace", "alwrity_config", "main_config.json")
                with open(config_path, 'w') as f:
                    json.dump(main_config, f, indent=4)
                
                # Show success message with HTML formatting
                st.markdown("""
                    <div style='background-color: #d4edda; color: #155724; padding: 1rem; border-radius: 0.25rem;'>
                        <h4 style='margin: 0;'>✅ Setup Completed Successfully!</h4>
                        <p style='margin: 0.5rem 0 0;'>Your configuration has been saved and you're ready to use ALwrity.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Set setup completion flag in session state
                st.session_state['setup_completed'] = True
                
                # Redirect to main application
                st.switch_page("alwrity.py")
                
            except Exception as e:
                error_msg = f"Error completing setup: {str(e)}"
                logger.error(f"[render_final_setup] {error_msg}")
                st.error(error_msg)
    
    return {"current_step": 5, "changes_made": True}
