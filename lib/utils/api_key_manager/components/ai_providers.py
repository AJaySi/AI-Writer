"""AI providers setup component."""

import streamlit as st
from loguru import logger
from typing import Dict, Any
from ..manager import APIKeyManager
from .base import render_navigation_buttons, render_step_indicator, render_tab_style
from ..wizard_state import next_step, update_progress
from datetime import datetime
import os
from dotenv import load_dotenv

def validate_api_key(key: str) -> bool:
    """Validate if an API key is properly formatted."""
    if not key:
        return False
    # Basic validation - check if key is not empty and has minimum length
    return len(key.strip()) > 0

def save_to_env_file(key_name: str, key_value: str) -> bool:
    """Save API key to .env file."""
    try:
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), '.env')
        
        # Read existing .env file
        env_contents = []
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                env_contents = f.readlines()
        
        # Check if key already exists
        key_exists = False
        for i, line in enumerate(env_contents):
            if line.startswith(f"{key_name}="):
                env_contents[i] = f"{key_name}={key_value}\n"
                key_exists = True
                break
        
        # Add new key if it doesn't exist
        if not key_exists:
            env_contents.append(f"{key_name}={key_value}\n")
        
        # Write back to .env file
        with open(env_path, 'w') as f:
            f.writelines(env_contents)
        
        # Reload environment variables to ensure consistency
        load_dotenv(override=True)
        
        logger.info(f"[save_to_env_file] Successfully saved {key_name} to .env file")
        return True
    except Exception as e:
        logger.error(f"[save_to_env_file] Error saving to .env file: {str(e)}")
        return False

def render_ai_providers(api_key_manager: APIKeyManager) -> Dict[str, Any]:
    """Render the AI providers setup step."""
    logger.info("[render_ai_providers] Starting AI providers setup")
    try:
        # Load environment variables
        load_dotenv(override=True)
        
        # Get existing API keys from .env
        openai_key = os.getenv('OPENAI_API_KEY', '')
        gemini_key = os.getenv('GEMINI_API_KEY', '')
        
        # Initialize wizard state if not already initialized
        if 'wizard_state' not in st.session_state:
            st.session_state.wizard_state = {
                'current_step': 1,
                'total_steps': 6,
                'progress': 0,
                'completed_steps': set(),
                'last_updated': datetime.now()
            }
            logger.info("[render_ai_providers] Initialized wizard state")
        
        # Store API key manager in session state for update_progress
        st.session_state['api_key_manager'] = api_key_manager
        
        # Main content
        st.markdown("""
            <div class='setup-header'><h2>🤖 AI LLM Providers Setup</h2></div>
        """, unsafe_allow_html=True)
        
        # Create tabs for different AI providers
        tabs = st.tabs(["Primary Providers", "Additional Providers"])
        
        # Track if any changes were made
        changes_made = False
        has_valid_key = False
        validation_message = ""
        
        with tabs[0]:
            st.markdown("### Primary AI Providers")
            
            # Create a grid layout for AI provider cards
            col1, col2 = st.columns(2)
            
            with col1:
                # OpenAI Card
                with st.container():
                    openai_input = st.text_input(
                        "OpenAI API Key",
                        value=openai_key,
                        type="password",
                        key="openai_key",
                        help="Enter your OpenAI API key",
                        placeholder="Power your content generation with GPT-4 AI models"
                    )
                    
                    if openai_key:
                        st.success("✅ OpenAI API key found in environment")
                    elif openai_input:
                        if validate_api_key(openai_input):
                            st.markdown("""
                                <div class="ai-provider-status status-valid">
                                    ✓ API key configured
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                                <div class="ai-provider-status status-invalid">
                                    ⚠️ Invalid API key format
                                </div>
                            """, unsafe_allow_html=True)
                    
                    with st.expander("📋 How to get your OpenAI API key", expanded=False):
                        st.markdown("""
                            **Step-by-step guide:**
                            1. Go to [OpenAI's website](https://platform.openai.com)
                            2. Sign up or log in to your account
                            3. Navigate to the API section
                            4. Click "Create new secret key"
                            5. Copy the generated key and paste it here
                            
                            **Note:** Keep your API key secure and never share it publicly.
                        """)
            
            with col2:
                # Google Card
                with st.container():
                    gemini_input = st.text_input(
                        "Google Gemini API Key",
                        value=gemini_key,
                        type="password",
                        key="google_key",
                        help="Enter your Google API key",
                        placeholder="Power your content generation with Gemini AI models"
                    )
                    
                    if gemini_key:
                        st.success("✅ Gemini API key found in environment")
                    elif gemini_input:
                        if validate_api_key(gemini_input):
                            st.markdown("""
                                <div class="ai-provider-status status-valid">
                                    ✓ API key configured
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                                <div class="ai-provider-status status-invalid">
                                    ⚠️ Invalid API key format
                                </div>
                            """, unsafe_allow_html=True)
                    
                    with st.expander("📋 How to get your Google API key", expanded=False):
                        st.markdown("""
                            **Step-by-step guide:**
                            1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
                            2. Sign in with your Google account
                            3. Click "Create API key"
                            4. Copy the generated key and paste it here
                            
                            **Note:** Make sure to enable the Gemini API in your Google Cloud Console.
                        """)
        
        with tabs[1]:
            st.markdown("### Additional AI Providers")
            st.markdown("Configure additional AI providers for enhanced capabilities")
            
            # Create a grid layout for additional provider cards
            col1, col2 = st.columns(2)
            
            with col1:
                # Anthropic Card (Coming Soon)
                with st.container():
                    st.markdown("""
                        <div class="ai-provider-card disabled">
                            <div class="ai-provider-header">
                                <div class="ai-provider-icon">🧠</div>
                                <div class="ai-provider-title">Anthropic <span class="coming-soon-badge">Coming Soon</span></div>
                            </div>
                            <div class="ai-provider-content">
                                <p>Access Claude for advanced content generation</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.info("Anthropic integration will be available in the next update")
            
            with col2:
                # Mistral Card (Coming Soon)
                with st.container():
                    st.markdown("""
                        <div class="ai-provider-card disabled">
                            <div class="ai-provider-header">
                                <div class="ai-provider-icon">⚡</div>
                                <div class="ai-provider-title">Mistral <span class="coming-soon-badge">Coming Soon</span></div>
                            </div>
                            <div class="ai-provider-content">
                                <p>Use Mistral's efficient language models</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.info("Mistral integration will be available in the next update")
        
        # Track changes and validate keys
        if any([openai_input, gemini_input]):
            changes_made = True
            # Check if at least one valid API key is provided
            if validate_api_key(openai_input) or validate_api_key(gemini_input):
                has_valid_key = True
                validation_message = "✅ At least one AI provider configured successfully"
            else:
                validation_message = "⚠️ Please provide at least one valid API key"
        else:
            validation_message = "⚠️ Please configure at least one AI provider to continue"
        
        # Display validation message
        if validation_message:
            if "✅" in validation_message:
                st.success(validation_message)
            else:
                st.warning(validation_message)
        
        # Navigation buttons
        if render_navigation_buttons(1, 6, changes_made):
            if has_valid_key:
                # Save API keys to .env file
                if validate_api_key(openai_input):
                    if save_to_env_file("OPENAI_API_KEY", openai_input):
                        logger.info("[render_ai_providers] OpenAI API key saved to .env file")
                    else:
                        st.error("Failed to save OpenAI API key to .env file")
                        return {"current_step": 1, "error": "Failed to save OpenAI API key"}
                
                if validate_api_key(gemini_input):
                    if save_to_env_file("GEMINI_API_KEY", gemini_input):
                        logger.info("[render_ai_providers] Google Gemini API key saved to .env file")
                    else:
                        st.error("Failed to save Gemini API key to .env file")
                        return {"current_step": 1, "error": "Failed to save Gemini API key"}
                
                # Reload environment variables to ensure consistency
                load_dotenv(override=True)
                
                # Get updated API keys from environment
                updated_openai_key = os.getenv('OPENAI_API_KEY', '')
                updated_gemini_key = os.getenv('GEMINI_API_KEY', '')
                
                # Store the API keys in session state
                st.session_state['api_keys'] = {
                    'openai': updated_openai_key,
                    'google': updated_gemini_key
                }
                
                # Update progress and move to next step
                st.session_state['current_step'] = 2  # Set the next step explicitly
                update_progress()
                st.rerun()  # Rerun to apply the changes
            else:
                st.error("Please configure at least one valid AI provider to continue")
        
        return {"current_step": 1, "changes_made": changes_made}
        
    except Exception as e:
        error_msg = f"Error in AI providers setup: {str(e)}"
        logger.error(f"[render_ai_providers] {error_msg}")
        st.error(error_msg)
        return {"current_step": 1, "error": error_msg} 