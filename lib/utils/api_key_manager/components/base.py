"""Base components for the API key manager."""

import streamlit as st
from typing import Dict, Any
from loguru import logger
from ..styles import API_KEY_MANAGER_STYLES # Assuming styles are correctly imported
from ..wizard_state import (
    get_current_step, # Keep if used elsewhere
    next_step,        # Keep if used elsewhere
    previous_step,    # Keep if used elsewhere
    can_proceed_to_next_step # Keep if used elsewhere
)

def render_step_indicator(current_step: int, total_steps: int) -> None:
    """Render the step indicator."""
    # Existing step indicator code... (Keep as is)
    try:
        st.markdown("""
            <style>
                .step-indicator {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 2rem;
                    padding: 1rem;
                    background: #f0f2f6;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .step {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    padding: 0.5rem 1rem;
                    border-radius: 20px;
                    background: #ffffff;
                    transition: all 0.3s ease;
                }
                .step.active {
                    background: #1f77b4;
                    color: white;
                }
                .step.completed {
                    background: #2ecc71;
                    color: white;
                }
                .step-icon {
                    font-size: 1.2rem;
                }
                .step-number {
                    font-weight: bold;
                }
                .step-title {
                    font-size: 0.9rem;
                }
                .step-line {
                    flex: 1;
                    height: 2px;
                    background: #e0e0e0;
                    margin: 0 1rem;
                }
                .step-line.active {
                    background: #1f77b4;
                }
                .step-line.completed {
                    background: #2ecc71;
                }
            </style>
        """, unsafe_allow_html=True)

        steps = [
            ("🔑", "AI Providers", 1),
            ("🌐", "Website Setup", 2),
            ("🔍", "AI Research", 3),
            ("🎨", "Personalization", 4),
            ("🔗", "Integrations", 5),
            ("✅", "Complete", 6)
        ]

        html = '<div class="step-indicator">'
        for i, (icon, title, step) in enumerate(steps):
            step_class = "active" if step == current_step else "completed" if step < current_step else ""
            line_class = "active" if step == current_step else "completed" if step < current_step else ""
            
            html += f'''
                <div class="step {step_class}">
                    <span class="step-icon">{icon}</span>
                    <span class="step-number">{step}</span>
                    <span class="step-title">{title}</span>
                </div>
            '''
            if i < len(steps) - 1:
                html += f'<div class="step-line {line_class}"></div>'
        html += '</div>'
        
        st.markdown(html, unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"Error rendering step indicator: {str(e)}")
        st.error("Error displaying step indicator")

def render_navigation_buttons(current_step: int, total_steps: int) -> None:
    """Render the navigation buttons with validation logic for steps 1 and 3."""
    col1, col2, col3 = st.columns([1, 2, 1])
    proceed_error_placeholder = col2.empty() # Placeholder for error message

    with col1:
        if current_step > 1:
            if st.button("**← Back**", use_container_width=True, key="back_button"):
                st.session_state['current_step'] = current_step - 1
                st.rerun()
    
    with col3:
        if current_step < total_steps:
            next_text = "**Continue →**"
            button_disabled = False
            error_message = ""

            if current_step == 1:
                # --- Step 1 Specific Validation --- 
                openai_valid = st.session_state.get("openai_status") == "valid"
                gemini_valid = st.session_state.get("gemini_status") == "valid"
                if not (openai_valid or gemini_valid):
                    button_disabled = True
                    error_message = "Please ensure at least one required AI provider (OpenAI or Gemini) has a valid API key to continue."
                logger.debug(f"Step 1 validation: OpenAI Valid={openai_valid}, Gemini Valid={gemini_valid}, Proceed={not button_disabled}")
            
            elif current_step == 3:
                # --- Step 3 Specific Validation --- 
                research_providers = ["serpapi", "tavily", "metaphor", "firecrawl"]
                invalid_key_found = False
                for provider in research_providers:
                    status = st.session_state.get(f"{provider}_status")
                    # Disable if any *entered* key is invalid or in error state
                    if status in ["invalid", "error"]:
                        invalid_key_found = True
                        break
                if invalid_key_found:
                    button_disabled = True
                    error_message = f"Please ensure any entered research API keys are valid before continuing. Check {provider.capitalize()} key."
                logger.debug(f"Step 3 validation: Invalid Key Found={invalid_key_found}, Proceed={not button_disabled}")
            
            # --- Default Logic for Other Steps --- 
            # else: # No specific validation for other steps currently
            #     button_disabled = False 

            # --- Render Button --- 
            if st.button(next_text, use_container_width=True, disabled=button_disabled, key="next_button"):
                if button_disabled:
                     # Should not happen if disabled, but safeguard
                    proceed_error_placeholder.error(error_message if error_message else "Cannot proceed.", icon="⚠️")
                    logger.warning(f"Continue button clicked on Step {current_step} while disabled.")
                else:
                    # Proceed to next step
                    logger.info(f"Proceeding from step {current_step} to {current_step + 1}")
                    st.session_state['current_step'] = current_step + 1
                    st.rerun()
            
            # Show error persistently if button is disabled
            elif button_disabled:
                 proceed_error_placeholder.error(error_message, icon="⚠️")

        elif current_step == total_steps:
            # --- Final Step Logic --- 
            final_step_can_complete = True # Replace with actual final validation logic
            if st.button("**Complete Setup ✓**", use_container_width=True, type="primary", disabled=not final_step_can_complete, key="complete_button"):
                if final_step_can_complete:
                    logger.info("Setup completed successfully!")
                    st.session_state['setup_complete'] = True 
                    st.success("✅ Setup completed successfully!") 
                    st.balloons()
                    st.rerun() 
                else:
                    proceed_error_placeholder.error("Please complete all required steps before finishing.", icon="⚠️")
                    logger.warning("Complete Setup clicked but final validation failed.")
            elif not final_step_can_complete:
                 proceed_error_placeholder.error("Please complete all required steps before finishing.", icon="⚠️")

def render_tab_style() -> None:
    """Render enhanced tab styling."""
    # Existing tab style code... (Keep as is)
    st.markdown("""
        <style>
            .stTabs [data-baseweb="tab-list"] {
                gap: 2rem;
                background: #f8f9fa;
                padding: 0.5rem;
                border-radius: 10px;
                margin-bottom: 1rem;
            }
            .stTabs [data-baseweb="tab"] {
                padding: 0.75rem 1.5rem;
                border-radius: 25px;
                transition: all 0.3s ease;
                background: transparent;
                color: #495057;
                font-weight: 500;
            }
            .stTabs [data-baseweb="tab"]:hover {
                background: #e9ecef;
                color: #1f77b4;
            }
            .stTabs [aria-selected="true"] {
                background: #1f77b4 !important;
                color: white !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .stTabs [data-baseweb="tab-list"] button:nth-child(1) {
                margin-left: 0.5rem;
            }
            .stTabs [data-baseweb="tab-list"] button:nth-child(3) {
                margin-right: 0.5rem;
            }
            .tab-content {
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                margin-top: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

def render_success_message():
    """Render the success message with glassmorphic design."""
    # Existing success message code... (Keep as is)
    st.markdown("""
        <div class="success-message">
            <h3 style='color: white; margin-bottom: 12px; font-size: 1.4em;'>✅ API keys saved successfully!</h3>
            <p style='color: rgba(255,255,255,0.95); font-size: 1.1em;'>
                Please restart the application for the changes to take effect.
            </p>
        </div>
    """, unsafe_allow_html=True)
