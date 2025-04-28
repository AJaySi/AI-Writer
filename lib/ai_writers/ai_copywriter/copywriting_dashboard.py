import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, List, Any
import json
import os

from ...gpt_providers.text_generation.main_text_generation import llm_text_gen
from ...gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image

# Import formula modules as they're created
from .formulas.aida_formula import generate_aida_copy
from .formulas.pas_formula import generate_pas_copy
from .formulas.bab_formula import generate_bab_copy
# Additional imports will be added as more formula modules are created

def load_formula_data() -> Dict:
    """Load copywriting formula data."""
    return {
        "attention_formulas": {
            "title": "Attention-Grabbing Formulas",
            "icon": "🔍",
            "description": "Formulas designed to capture attention and generate interest",
            "formulas": [
                {
                    "name": "AIDA",
                    "full_name": "Attention, Interest, Desire, Action",
                    "description": "The classic marketing formula that guides prospects through a purchase decision",
                    "status": "active",
                    "icon": "🎯",
                    "function": generate_aida_copy,
                    "best_for": ["Landing Pages", "Sales Emails", "Product Descriptions"]
                },
                {
                    "name": "PAS",
                    "full_name": "Problem, Agitation, Solution",
                    "description": "Identify a problem, agitate it, then present your solution",
                    "status": "active",
                    "icon": "🔧",
                    "function": generate_pas_copy,
                    "best_for": ["Social Ads", "Blog Intros", "Sales Pages"]
                }
            ]
        },
        "storytelling_formulas": {
            "title": "Storytelling Formulas",
            "icon": "📚",
            "description": "Formulas that use narrative techniques to engage and persuade",
            "formulas": [
                {
                    "name": "BAB",
                    "full_name": "Before, After, Bridge",
                    "description": "Show the current state, desired state, and how to get there",
                    "status": "active",
                    "icon": "🌉",
                    "function": generate_bab_copy,
                    "best_for": ["Case Studies", "Testimonials", "Video Scripts"]
                },
                {
                    "name": "Hero's Journey",
                    "full_name": "Hero's Journey Adaptation",
                    "description": "Adapt the classic storytelling structure for marketing",
                    "status": "coming_soon",
                    "icon": "🦸",
                    "best_for": ["Brand Stories", "About Pages", "Long-form Content"]
                }
            ]
        },
        "persuasion_formulas": {
            "title": "Persuasion Formulas",
            "icon": "⚡",
            "description": "Formulas focused on convincing and converting",
            "formulas": [
                {
                    "name": "4Ps",
                    "full_name": "Promise, Picture, Proof, Push",
                    "description": "Make a promise, paint a picture, provide proof, push for action",
                    "status": "coming_soon",
                    "icon": "🏆",
                    "best_for": ["Sales Pages", "Webinar Scripts", "Video Sales Letters"]
                },
                {
                    "name": "FAB",
                    "full_name": "Features, Advantages, Benefits",
                    "description": "Connect product features to customer benefits",
                    "status": "coming_soon",
                    "icon": "✨",
                    "best_for": ["Product Pages", "Brochures", "Sales Presentations"]
                }
            ]
        },
        "specialized_formulas": {
            "title": "Specialized Formulas",
            "icon": "🔬",
            "description": "Formulas for specific marketing contexts and goals",
            "formulas": [
                {
                    "name": "PASTOR",
                    "full_name": "Problem, Amplify, Story, Transformation, Offer, Response",
                    "description": "Comprehensive formula for long-form sales copy",
                    "status": "coming_soon",
                    "icon": "📝",
                    "best_for": ["Long Sales Letters", "Webinar Scripts", "Launch Sequences"]
                },
                {
                    "name": "QUEST",
                    "full_name": "Qualify, Understand, Educate, Stimulate, Transition",
                    "description": "Formula designed for B2B marketing and complex sales",
                    "status": "coming_soon",
                    "icon": "🏢",
                    "best_for": ["B2B Emails", "White Papers", "Case Studies"]
                }
            ]
        }
    }

def render_formula_card(formula: Dict) -> None:
    """Render a single formula card with its details."""
    status_color = "#4CAF50" if formula['status'] == 'active' else "#FFA500"
    
    with st.container():
        st.markdown(f"""
            <div style='padding: 20px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 20px;'>
                <h3 style='margin: 0;'>{formula['icon']} {formula['name']}</h3>
                <p style='font-size: 0.9em; color: #666;'>{formula['full_name']}</p>
                <p style='margin: 10px 0;'>{formula['description']}</p>
                <div style='margin: 10px 0;'>
                    <span style='font-size: 0.9em; font-weight: bold;'>Best for: </span>
                    {', '.join(formula.get('best_for', ['General Copy']))}
                </div>
                <span style='background-color: {status_color}; 
                            padding: 5px 10px; border-radius: 15px; font-size: 0.8em; color: white;'>
                    {formula['status'].replace('_', ' ').title()}
                </span>
            </div>
        """, unsafe_allow_html=True)

def render_category_section(category: Dict) -> None:
    """Render a category section with all its formulas."""
    st.markdown(f"### {category['icon']} {category['title']}")
    st.markdown(f"*{category['description']}*")
    
    # Create two columns for the formulas
    col1, col2 = st.columns(2)
    
    # Render formulas in the columns
    for i, formula in enumerate(category['formulas']):
        with col1 if i % 2 == 0 else col2:
            render_formula_card(formula)
            if formula['status'] == 'active':
                if st.button(f"Use {formula['name']} Formula", key=f"use_{formula['name']}"):
                    st.session_state.selected_formula = formula
                    st.session_state.show_formula_generator = True

def formula_selector_view():
    """Display the formula selection view."""
    st.title("AI Copywriting Formula Generator")
    st.write("Select a proven copywriting formula to create persuasive, high-converting copy.")
    
    # Load formula data
    formula_data = load_formula_data()
    
    # Create tabs for different categories
    tab1, tab2, tab3, tab4 = st.tabs([
        f"{formula_data['attention_formulas']['icon']} Attention",
        f"{formula_data['storytelling_formulas']['icon']} Storytelling",
        f"{formula_data['persuasion_formulas']['icon']} Persuasion",
        f"{formula_data['specialized_formulas']['icon']} Specialized"
    ])
    
    with tab1:
        render_category_section(formula_data['attention_formulas'])
    
    with tab2:
        render_category_section(formula_data['storytelling_formulas'])
    
    with tab3:
        render_category_section(formula_data['persuasion_formulas'])
    
    with tab4:
        render_category_section(formula_data['specialized_formulas'])

def formula_generator_view(formula: Dict):
    """Display the formula generator view for the selected formula."""
    st.title(f"{formula['icon']} {formula['name']} Formula Generator")
    st.write(f"Create persuasive copy using the {formula['full_name']} formula.")
    
    # Back button
    if st.button("← Back to Formula Selection"):
        st.session_state.show_formula_generator = False
        st.session_state.selected_formula = None
        st.rerun()
    
    # Call the specific formula function
    if 'function' in formula and formula['status'] == 'active':
        formula['function']()
    else:
        st.info(f"The {formula['name']} formula generator is coming soon!")

def write_ai_copywriter():
    """Main function to run the AI Copywriter dashboard."""
    # Initialize session state
    if 'show_formula_generator' not in st.session_state:
        st.session_state.show_formula_generator = False
    if 'selected_formula' not in st.session_state:
        st.session_state.selected_formula = None
    
    # Display appropriate view based on session state
    if st.session_state.show_formula_generator and st.session_state.selected_formula:
        formula_generator_view(st.session_state.selected_formula)
    else:
        formula_selector_view()
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center;'>
            <p>Powered by AI-Writer | <a href='#'>Learn more about copywriting formulas</a></p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    write_ai_copywriter()