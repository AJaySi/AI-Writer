"""AI Research setup component."""

import streamlit as st
from typing import Dict, Any
from loguru import logger
from ..manager import APIKeyManager
from .base import render_navigation_buttons, render_step_indicator

def render_ai_research(api_key_manager: APIKeyManager) -> Dict[str, Any]:
    """Render the AI Research setup step."""
    try:
        st.markdown("""
            <div class='setup-header'>
                <h2>🔍 AI Research Configuration</h2>
                <p>Configure your research preferences and provide user information</p>
            </div>
        """, unsafe_allow_html=True)

        # Create tabs for different sections
        tabs = st.tabs(["User Information", "Research Preferences"])

        changes_made = False
        has_valid_info = False
        validation_message = ""

        with tabs[0]:
            st.markdown("### User Information")
            st.markdown("Please provide your details for personalized research experience")

            # User Information Card
            with st.container():
                st.markdown("""
                    <div class="user-info-card">
                        <div class="user-info-header">
                            <div class="user-info-icon">👤</div>
                            <div class="user-info-title">Personal Details</div>
                        </div>
                        <div class="user-info-content">
                            <p>Your information helps us customize the research experience.</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # User Input Fields with Streamlit Components
                full_name = st.text_input("Full Name", key="full_name",
                    help="Enter your full name as you'd like it to appear")
                
                email = st.text_input("Email Address", key="email",
                    help="Enter your business email address")
                
                company = st.text_input("Company/Organization", key="company",
                    help="Enter your company or organization name")
                
                role = st.selectbox("Role",
                    ["Content Creator", "Marketing Manager", "Business Owner", "Other"],
                    help="Select your primary role")

        with tabs[1]:
            st.markdown("### Research Preferences")
            st.markdown("Configure how AI assists with your research")

            # Research Preferences Card
            with st.container():
                st.markdown("""
                    <div class="research-prefs-card">
                        <div class="research-prefs-header">
                            <div class="research-prefs-icon">🎯</div>
                            <div class="research-prefs-title">Research Settings</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Research Preferences Settings
                research_depth = st.select_slider(
                    "Research Depth",
                    options=["Basic", "Standard", "Deep", "Comprehensive"],
                    value="Standard",
                    help="Choose how detailed you want the AI research to be"
                )

                st.markdown("#### Content Types")
                content_types = st.multiselect(
                    "Select content types to focus on",
                    ["Blog Posts", "Social Media", "Technical Articles", "News", "Academic Papers"],
                    default=["Blog Posts", "Social Media"],
                    help="Choose what types of content you want to research"
                )

                auto_research = st.toggle(
                    "Enable Automated Research",
                    help="Automatically start research when content topics are added"
                )

        # Validate inputs
        if all([full_name, email, company]):
            changes_made = True
            has_valid_info = True
            validation_message = "✅ User information completed successfully"
        else:
            validation_message = "⚠️ Please fill in all required fields to continue"

        # Display validation message
        if validation_message:
            if "✅" in validation_message:
                st.success(validation_message)
            else:
                st.warning(validation_message)

        # Navigation buttons
        if render_navigation_buttons(3, 6, changes_made):
            if has_valid_info:
                # Store user information in session state
                st.session_state['user_info'] = {
                    'full_name': full_name,
                    'email': email,
                    'company': company,
                    'role': role,
                    'research_preferences': {
                        'depth': research_depth,
                        'content_types': content_types,
                        'auto_research': auto_research
                    }
                }
                
                # Update progress and move to next step
                st.session_state['current_step'] = 4
                st.rerun()
            else:
                st.error("Please complete all required fields to continue")

        return {"current_step": 3, "changes_made": changes_made}

    except Exception as e:
        error_msg = f"Error in AI research setup: {str(e)}"
        logger.error(f"[render_ai_research] {error_msg}")
        st.error(error_msg)
        return {"current_step": 3, "error": error_msg} 