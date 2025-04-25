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
    
    st.markdown("### Step 6: Final Setup & Validation")
    
    # Load main config
    main_config = load_main_config()
    
    # Create tabs for each step
    tabs = st.tabs([
        "Step 1: AI LLM Setup", 
        "Step 2: Website Analysis", 
        "Step 3: AI Research", 
        "Step 4: Personalization", 
        "Step 5: Integrations"
    ])
    
    # Step 1: AI LLM Setup
    with tabs[0]:
        st.markdown("#### AI LLM Configuration")
        
        # Get API keys from environment
        openai_key = os.getenv('OPENAI_API_KEY', 'Not configured')
        gemini_key = os.getenv('GEMINI_API_KEY', 'Not configured')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY', 'Not configured')
        mistral_key = os.getenv('MISTRAL_API_KEY', 'Not configured')
        
        # Display API keys (masked)
        st.markdown("##### API Keys")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**OpenAI API Key:** {'*' * 8}{openai_key[-4:] if openai_key != 'Not configured' else ''}")
            st.markdown(f"**Google Gemini API Key:** {'*' * 8}{gemini_key[-4:] if gemini_key != 'Not configured' else ''}")
        
        with col2:
            st.markdown(f"**Anthropic API Key:** {'*' * 8}{anthropic_key[-4:] if anthropic_key != 'Not configured' else ''}")
            st.markdown(f"**Mistral API Key:** {'*' * 8}{mistral_key[-4:] if mistral_key != 'Not configured' else ''}")
    
    # Step 2: Website Analysis
    with tabs[1]:
        st.markdown("#### Website Analysis Configuration")
        
        # Get website URL from environment
        website_url = os.getenv('WEBSITE_URL', 'Not configured')
        
        # Display website URL
        st.markdown("##### Website URL")
        st.markdown(f"**Website URL:** {website_url}")
        
        # Display website analysis settings
        st.markdown("##### Analysis Settings")
        st.markdown("Website analysis settings will be used to understand your content style and preferences.")
    
    # Step 3: AI Research
    with tabs[2]:
        st.markdown("#### AI Research Configuration")
        
        # Get research API keys from environment
        serpapi_key = os.getenv('SERPAPI_KEY', 'Not configured')
        tavily_key = os.getenv('TAVILY_API_KEY', 'Not configured')
        metaphor_key = os.getenv('METAPHOR_API_KEY', 'Not configured')
        firecrawl_key = os.getenv('FIRECRAWL_API_KEY', 'Not configured')
        
        # Display API keys (masked)
        st.markdown("##### Research API Keys")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**SerpAPI Key:** {'*' * 8}{serpapi_key[-4:] if serpapi_key != 'Not configured' else ''}")
            st.markdown(f"**Tavily API Key:** {'*' * 8}{tavily_key[-4:] if tavily_key != 'Not configured' else ''}")
        
        with col2:
            st.markdown(f"**Metaphor API Key:** {'*' * 8}{metaphor_key[-4:] if metaphor_key != 'Not configured' else ''}")
            st.markdown(f"**Firecrawl API Key:** {'*' * 8}{firecrawl_key[-4:] if firecrawl_key != 'Not configured' else ''}")
    
    # Step 4: Personalization
    with tabs[3]:
        st.markdown("#### Personalization Configuration")
        
        # Display personalization settings from main config
        with st.popover("Blog Content Characteristics", help="Click to see details about blog content settings"):
            st.markdown("##### Blog Content Characteristics")
            blog_settings = main_config.get("Blog Content Characteristics", {})
            st.write(f"- Blog Length: {blog_settings.get('Blog Length', '2000')}")
            st.write(f"- Blog Tone: {blog_settings.get('Blog Tone', 'Professional')}")
            st.write(f"- Blog Demographic: {blog_settings.get('Blog Demographic', 'Professional')}")
            st.write(f"- Blog Type: {blog_settings.get('Blog Type', 'Informational')}")
            st.write(f"- Blog Language: {blog_settings.get('Blog Language', 'English')}")
            st.write(f"- Blog Output Format: {blog_settings.get('Blog Output Format', 'markdown')}")
            st.markdown("These settings define the overall structure and style of your blog content.")
        
        with st.popover("Blog Images Details", help="Click to see details about image generation settings"):
            st.markdown("##### Blog Images Details")
            image_settings = main_config.get("Blog Images Details", {})
            st.write(f"- Image Generation Model: {image_settings.get('Image Generation Model', 'stable-diffusion')}")
            st.write(f"- Number of Blog Images: {image_settings.get('Number of Blog Images', 1)}")
            st.markdown("These settings control how images are generated for your blog posts.")
        
        with st.popover("LLM Options", help="Click to see details about language model settings"):
            st.markdown("##### LLM Options")
            llm_settings = main_config.get("LLM Options", {})
            st.write(f"- GPT Provider: {llm_settings.get('GPT Provider', 'google')}")
            st.write(f"- Model: {llm_settings.get('Model', 'gemini-1.5-flash-latest')}")
            st.write(f"- Temperature: {llm_settings.get('Temperature', 0.7)}")
            st.write(f"- Top-p: {llm_settings.get('Top-p', 0.9)}")
            st.write(f"- Max Tokens: {llm_settings.get('Max Tokens', 4000)}")
            st.write(f"- Frequency Penalty: {llm_settings.get('Frequency Penalty', 1.0)}")
            st.write(f"- Presence Penalty: {llm_settings.get('Presence Penalty', 1.0)}")
            st.markdown("These settings control the behavior of the language model used for content generation.")
        
        with st.popover("Search Engine Parameters", help="Click to see details about search engine settings"):
            st.markdown("##### Search Engine Parameters")
            search_settings = main_config.get("Search Engine Parameters", {})
            st.write(f"- Geographic Location: {search_settings.get('Geographic Location', 'us')}")
            st.write(f"- Search Language: {search_settings.get('Search Language', 'en')}")
            st.write(f"- Number of Results: {search_settings.get('Number of Results', 10)}")
            st.write(f"- Time Range: {search_settings.get('Time Range', 'anytime')}")
            st.markdown("These settings control how search engines are used for research and content creation.")
    
    # Step 5: Integrations
    with tabs[4]:
        st.markdown("#### ALwrity Integrations Configuration")
        
        # Display integrations settings
        st.markdown("##### Website Platforms")
        st.info("WordPress integration will be available in the next update")
        st.info("Wix integration will be available in the next update")
        
        st.markdown("##### Social Media")
        st.info("Facebook integration will be available in the next update")
        st.info("Instagram integration will be available in the next update")
        
        st.markdown("##### Analytics Tools")
        st.info("Google Search Console integration will be available in the next update")

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
                # First set FINAL_SETUP_COMPLETE to True
                try:
                    # Read existing .env content
                    env_lines = []
                    if os.path.exists('.env'):
                        with open('.env', 'r') as f:
                            env_lines = f.readlines()
                    
                    # Remove any existing FINAL_SETUP_COMPLETE entries
                    env_lines = [line for line in env_lines if not line.startswith('FINAL_SETUP_COMPLETE=')]
                    
                    # Add the new FINAL_SETUP_COMPLETE entry
                    env_lines.append("FINAL_SETUP_COMPLETE=True\n")
                    
                    # Write back to .env file
                    with open('.env', 'w') as f:
                        f.writelines(env_lines)
                    
                    # Set environment variable
                    os.environ['FINAL_SETUP_COMPLETE'] = "True"
                    logger.info("[render_final_setup] Set FINAL_SETUP_COMPLETE=True")
                except Exception as e:
                    logger.error(f"[render_final_setup] Error setting FINAL_SETUP_COMPLETE: {str(e)}")
                    st.error("Error updating setup status. Please try again.")
                    return {"current_step": 6, "changes_made": False}

                # Now validate all steps
                validation_result = check_all_api_keys(api_key_manager)
                if not validation_result:
                    # If validation fails, revert FINAL_SETUP_COMPLETE
                    try:
                        env_lines = [line for line in env_lines if not line.startswith('FINAL_SETUP_COMPLETE=')]
                        env_lines.append("FINAL_SETUP_COMPLETE=False\n")
                        with open('.env', 'w') as f:
                            f.writelines(env_lines)
                        os.environ['FINAL_SETUP_COMPLETE'] = "False"
                    except Exception:
                        pass  # Ignore reversion errors
                    
                    st.error("Setup validation failed. Please ensure all required steps are completed.")
                    logger.error("[render_final_setup] Validation failed")
                    return {"current_step": 6, "changes_made": False}

                # Log the current API keys in the manager
                logger.info("[render_final_setup] Current API keys in manager:")
                for key, value in api_key_manager.api_keys.items():
                    if value:
                        logger.info(f"  - {key}: {'*' * 8}{value[-4:]}")
                    else:
                        logger.info(f"  - {key}: Not set")
                
                # Save main configuration
                config_path = os.path.join("lib", "workspace", "alwrity_config", "main_config.json")
                with open(config_path, 'w') as f:
                    json.dump(main_config, f, indent=4)
                logger.info("[render_final_setup] Saved main configuration")
                
                # Show success message
                st.success("✅ Setup completed successfully! Redirecting to main application...")
                
                # Set setup completion flag in session state
                st.session_state['setup_completed'] = True
                st.session_state['redirect_to_main'] = True
                
                # Clear the current step to ensure proper redirection
                if 'current_step' in st.session_state:
                    del st.session_state['current_step']
                
                # Rerun to trigger redirection
                st.rerun()
                
            except Exception as e:
                error_msg = f"Error completing setup: {str(e)}"
                logger.error(f"[render_final_setup] {error_msg}")
                st.error(error_msg)
                return {"current_step": 6, "changes_made": False}
    
    return {"current_step": 6, "changes_made": True}