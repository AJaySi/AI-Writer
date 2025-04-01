"""AI providers setup component."""

import streamlit as st
from loguru import logger
from typing import Dict, Any
from ..manager import APIKeyManager
from .base import render_navigation_buttons, render_step_indicator, render_tab_style
from ..wizard_state import next_step, update_progress
from datetime import datetime

def validate_api_key(key: str) -> bool:
    """Validate if an API key is properly formatted."""
    if not key:
        return False
    # Basic validation - check if key is not empty and has minimum length
    return len(key.strip()) > 0

def render_ai_providers(api_key_manager: APIKeyManager) -> Dict[str, Any]:
    """Render the AI providers setup step."""
    logger.info("[render_ai_providers] Starting AI providers setup")
    try:
        # Store API key manager in session state for update_progress
        st.session_state['api_key_manager'] = api_key_manager
        
        # Main content
        st.markdown("""
            <div class='setup-header'>
                <h2>🤖 AI Providers Setup</h2>
                <p>Configure your AI service providers for content generation</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for different AI providers
        tabs = st.tabs(["Primary Providers", "Additional Providers"])
        
        # Track if any changes were made
        changes_made = False
        has_valid_key = False
        validation_message = ""
        
        with tabs[0]:
            st.markdown("### Primary AI Providers")
            st.markdown("Configure the main AI providers for content creation")
            
            # Create a grid layout for AI provider cards
            col1, col2 = st.columns(2)
            
            with col1:
                # OpenAI Card
                with st.container():
                    st.markdown("""
                        <div class="ai-provider-card">
                            <div class="ai-provider-header">
                                <div class="ai-provider-icon">🤖</div>
                                <div class="ai-provider-title">OpenAI</div>
                            </div>
                            <div class="ai-provider-content">
                                <p>Power your content with GPT-4 and GPT-3.5 models</p>
                                <div class="ai-provider-input">
                    """, unsafe_allow_html=True)
                    
                    openai_key = st.text_input(
                        "OpenAI API Key",
                        type="password",
                        key="openai_key",
                        help="Enter your OpenAI API key"
                    )
                    
                    if openai_key:
                        if validate_api_key(openai_key):
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
                    
                    st.markdown("</div></div></div>", unsafe_allow_html=True)
            
            with col2:
                # Google Card
                with st.container():
                    st.markdown("""
                        <div class="ai-provider-card">
                            <div class="ai-provider-header">
                                <div class="ai-provider-icon">🔍</div>
                                <div class="ai-provider-title">Google Gemini</div>
                            </div>
                            <div class="ai-provider-content">
                                <p>Leverage Google's powerful Gemini models</p>
                                <div class="ai-provider-input">
                    """, unsafe_allow_html=True)
                    
                    google_key = st.text_input(
                        "Google API Key",
                        type="password",
                        key="google_key",
                        help="Enter your Google API key"
                    )
                    
                    if google_key:
                        if validate_api_key(google_key):
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
                    
                    st.markdown("</div></div></div>", unsafe_allow_html=True)
        
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
        if any([openai_key, google_key]):
            changes_made = True
            # Check if at least one valid API key is provided
            if validate_api_key(openai_key) or validate_api_key(google_key):
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
                # Store the API keys in a separate session state key
                st.session_state['api_keys'] = {
                    'openai': openai_key if validate_api_key(openai_key) else None,
                    'google': google_key if validate_api_key(google_key) else None
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