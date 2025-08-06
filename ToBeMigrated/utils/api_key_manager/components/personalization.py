"""Personalization setup component."""

import streamlit as st
from typing import Dict, Any
from loguru import logger
from ..manager import APIKeyManager
from .base import render_navigation_buttons, render_step_indicator

def render_personalization(api_key_manager: APIKeyManager) -> Dict[str, Any]:
    """Render the personalization setup step."""
    try:
        st.markdown("""
            <div class='setup-header'>
                <h2>🎨 Personalization Settings</h2>
                <p>Customize your content generation experience</p>
            </div>
        """, unsafe_allow_html=True)

        # Create tabs for different sections
        tabs = st.tabs(["Content Style", "Brand Voice", "Advanced Settings"])

        changes_made = False
        has_valid_settings = False
        validation_message = ""

        with tabs[0]:
            st.markdown("### Content Style")
            st.markdown("Define your preferred content style and tone")

            # Content Style Card
            with st.container():
                st.markdown("""
                    <div class="style-card">
                        <div class="style-header">
                            <div class="style-icon">✨</div>
                            <div class="style-title">Writing Style</div>
                        </div>
                        <div class="style-content">
                            <p>Choose how you want your content to be written.</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Style Settings
                writing_style = st.selectbox(
                    "Writing Style",
                    ["Professional", "Casual", "Technical", "Conversational", "Academic"],
                    help="Select your preferred writing style"
                )

                tone = st.select_slider(
                    "Content Tone",
                    options=["Formal", "Semi-Formal", "Neutral", "Friendly", "Humorous"],
                    value="Neutral",
                    help="Choose the tone for your content"
                )

                content_length = st.select_slider(
                    "Content Length",
                    options=["Concise", "Standard", "Detailed", "Comprehensive"],
                    value="Standard",
                    help="Select your preferred content length"
                )

        with tabs[1]:
            st.markdown("### Brand Voice")
            st.markdown("Configure your brand's unique voice and personality")

            # Brand Voice Card
            with st.container():
                st.markdown("""
                    <div class="brand-card">
                        <div class="brand-header">
                            <div class="brand-icon">🎯</div>
                            <div class="brand-title">Brand Identity</div>
                        </div>
                        <div class="brand-content">
                            <p>Define your brand's personality and voice.</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Brand Settings
                brand_personality = st.multiselect(
                    "Brand Personality Traits",
                    ["Professional", "Innovative", "Friendly", "Trustworthy", "Creative", "Expert"],
                    default=["Professional", "Trustworthy"],
                    help="Select traits that best describe your brand"
                )

                brand_voice = st.text_area(
                    "Brand Voice Description",
                    help="Describe how your brand should sound in content"
                )

                keywords = st.text_input(
                    "Brand Keywords",
                    help="Enter key terms that should be used in your content"
                )

        with tabs[2]:
            st.markdown("### Advanced Settings")
            st.markdown("Fine-tune your content generation preferences")

            # Advanced Settings Card
            with st.container():
                st.markdown("""
                    <div class="advanced-card">
                        <div class="advanced-header">
                            <div class="advanced-icon">⚙️</div>
                            <div class="advanced-title">Advanced Options</div>
                        </div>
                        <div class="advanced-content">
                            <p>Configure advanced content generation settings.</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Advanced Settings
                seo_optimization = st.toggle(
                    "Enable SEO Optimization",
                    help="Automatically optimize content for search engines"
                )

                readability_level = st.select_slider(
                    "Readability Level",
                    options=["Simple", "Standard", "Advanced", "Expert"],
                    value="Standard",
                    help="Choose the complexity level of your content"
                )

                content_structure = st.multiselect(
                    "Content Structure",
                    ["Introduction", "Key Points", "Examples", "Conclusion", "Call-to-Action"],
                    default=["Introduction", "Key Points", "Conclusion"],
                    help="Select required content sections"
                )

        # Validate settings
        if all([writing_style, tone, content_length, brand_personality]):
            changes_made = True
            has_valid_settings = True
            validation_message = "✅ Personalization settings completed successfully"
        else:
            validation_message = "⚠️ Please complete all required settings to continue"

        # Display validation message
        if validation_message:
            if "✅" in validation_message:
                st.success(validation_message)
            else:
                st.warning(validation_message)

        # Navigation buttons
        if render_navigation_buttons(4, 6, changes_made):
            if has_valid_settings:
                # Store personalization settings in session state
                st.session_state['personalization'] = {
                    'content_style': {
                        'writing_style': writing_style,
                        'tone': tone,
                        'content_length': content_length
                    },
                    'brand_voice': {
                        'personality': brand_personality,
                        'voice_description': brand_voice,
                        'keywords': keywords
                    },
                    'advanced_settings': {
                        'seo_optimization': seo_optimization,
                        'readability_level': readability_level,
                        'content_structure': content_structure
                    }
                }
                
                # Update progress and move to next step
                st.session_state['current_step'] = 5
                st.rerun()
            else:
                st.error("Please complete all required settings to continue")

        return {"current_step": 4, "changes_made": changes_made}

    except Exception as e:
        error_msg = f"Error in personalization setup: {str(e)}"
        logger.error(f"[render_personalization] {error_msg}")
        st.error(error_msg)
        return {"current_step": 4, "error": error_msg} 