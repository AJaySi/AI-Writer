"""Base components for the API key manager."""

import streamlit as st
from typing import Dict, Any
from loguru import logger
from ..styles import API_KEY_MANAGER_STYLES

def render_step_indicator(current_step: int, total_steps: int) -> None:
    """Render the step indicator."""
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
            ("🔑", "AI LLM", 1),
            ("🔍", "Website Analysis", 2),
            ("👤", "AI Research", 3),
            ("🎨", "Personalization", 4),
            ("🔄", "Integrations", 5),
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

def render_navigation_buttons(current_step: int, total_steps: int, changes_made: bool = True) -> bool:
    """Render the navigation buttons with modern glassmorphic styling.
    
    Args:
        current_step (int): Current step number
        total_steps (int): Total number of steps
        changes_made (bool): Whether changes were made in the current step
        
    Returns:
        bool: True if next/complete button was clicked, False otherwise
    """
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_step > 1:
            if st.button("**← Back**", use_container_width=True, key="back_button"):
                from ..wizard_state import previous_step
                previous_step()
                st.rerun()
    
    with col3:
        if current_step < total_steps:
            next_text = "**Continue →**"
            if st.button(next_text, use_container_width=True, disabled=not changes_made, key="next_button"):
                # Don't call next_step() here, let the component handle it
                return True
        else:
            if st.button("**Complete Setup ✓**", use_container_width=True, type="primary", key="complete_button"):
                # Save the configuration
                st.success("✅ Setup completed successfully!")
                return True
    
    return False

def render_tab_style() -> None:
    """Render enhanced tab styling."""
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
    st.markdown("""
        <div class="success-message">
            <h3 style='color: white; margin-bottom: 12px; font-size: 1.4em;'>✅ API keys saved successfully!</h3>
            <p style='color: rgba(255,255,255,0.95); font-size: 1.1em;'>
                Please restart the application for the changes to take effect.
            </p>
        </div>
    """, unsafe_allow_html=True)
