import streamlit as st
import importlib
import sys
import os
from pathlib import Path

# Add the parent directory to the path to allow importing from lib
current_dir = Path(__file__).parent
root_dir = current_dir.parent.parent.parent
sys.path.append(str(root_dir))

# Dictionary to store the input section functions
input_sections = {}

# List of copywriter modules to import
copywriter_modules = [
    "ai_emotional_copywriter",
    "acca_copywriter",
    "app_copywriter",
    "star_copywriter",
    "oath_copywriter",
    "quest_copywriter",
    "aidppc_copywriter",
    "aida_copywriter",
    "pas_copywriter",
    "fab_copywriter",
    "4c_copywriter",
    "4r_copywriter"
]

# Dynamically import all copywriter modules
for module_name in copywriter_modules:
    try:
        module_path = f"lib.ai_writers.ai_copywriter.{module_name}"
        module = importlib.import_module(module_path)
        if hasattr(module, "input_section"):
            input_sections[module_name] = module.input_section
    except Exception as e:
        st.write(f"Debug: Error importing {module_name}: {str(e)}")

def copywriter_dashboard():
    """
    Main function to display the copywriting dashboard.
    This function can be called from content_generator.py when the user selects "AI Copywriter".
    """
    
    # Define the copywriting formulas with their details
    copywriting_formulas = [
        {
            "name": "Emotional Copywriter",
            "icon": "🎭",
            "description": "Create copy that resonates with your audience's emotions and drives action.",
            "color": "#FF6B6B",
            "module": "ai_emotional_copywriter",
            "function": input_sections.get("ai_emotional_copywriter")
        },
        {
            "name": "ACCA Copywriter",
            "icon": "🎯",
            "description": "Use the ACCA (Attention, Context, Content, Action) framework to create compelling copy.",
            "color": "#4ECDC4",
            "module": "acca_copywriter",
            "function": input_sections.get("acca_copywriter")
        },
        {
            "name": "APP Copywriter",
            "icon": "🤝",
            "description": "Implement the APP (Agree, Promise, Preview) formula to create persuasive copy.",
            "color": "#45B7D1",
            "module": "app_copywriter",
            "function": input_sections.get("app_copywriter")
        },
        {
            "name": "STAR Copywriter",
            "icon": "⭐",
            "description": "Use the STAR (Situation, Task, Action, Result) framework to tell compelling stories.",
            "color": "#FFD166",
            "module": "star_copywriter",
            "function": input_sections.get("star_copywriter")
        },
        {
            "name": "OATH Copywriter",
            "icon": "📜",
            "description": "Apply the OATH (Oblivious, Apathetic, Thinking, Hurting) framework to target specific audience mindsets.",
            "color": "#06D6A0",
            "module": "oath_copywriter",
            "function": input_sections.get("oath_copywriter")
        },
        {
            "name": "QUEST Copywriter",
            "icon": "🔍",
            "description": "Use the QUEST (Question, Unpack, Emphasize, Solution, Transform) framework for narrative-driven copy.",
            "color": "#118AB2",
            "module": "quest_copywriter",
            "function": input_sections.get("quest_copywriter")
        },
        {
            "name": "AIDPPC Copywriter",
            "icon": "💰",
            "description": "Implement the AIDPPC (Attention, Interest, Desire, Proof, Persuasion, Call to Action) framework for PPC ads.",
            "color": "#073B4C",
            "module": "aidppc_copywriter",
            "function": input_sections.get("aidppc_copywriter")
        },
        {
            "name": "AIDA Copywriter",
            "icon": "🎬",
            "description": "Use the AIDA (Attention, Interest, Desire, Action) framework to guide customers through the sales funnel.",
            "color": "#EF476F",
            "module": "aida_copywriter",
            "function": input_sections.get("aida_copywriter")
        },
        {
            "name": "PAS Copywriter",
            "icon": "🔧",
            "description": "Apply the PAS (Problem, Agitate, Solution) formula to address pain points and offer solutions.",
            "color": "#7209B7",
            "module": "pas_copywriter",
            "function": input_sections.get("pas_copywriter")
        },
        {
            "name": "FAB Copywriter",
            "icon": "💎",
            "description": "Use the FAB (Features, Advantages, Benefits) framework to highlight product value.",
            "color": "#3A0CA3",
            "module": "fab_copywriter",
            "function": input_sections.get("fab_copywriter")
        },
        {
            "name": "4C Copywriter",
            "icon": "📝",
            "description": "Implement the 4C (Clear, Concise, Credible, Compelling) framework for effective messaging.",
            "color": "#4361EE",
            "module": "four_c_copywriter",
            "function": input_sections.get("four_c_copywriter")
        },
        {
            "name": "4R Copywriter",
            "icon": "🔄",
            "description": "Use the 4R (Relevance, Resonance, Response, Results) framework to connect with your audience.",
            "color": "#F72585",
            "module": "four_r_copywriter",
            "function": input_sections.get("four_r_copywriter")
        }
    ]
    
    # Create a container for the dashboard
    dashboard_container = st.container()
    
    # Create a container for the formula input section
    formula_container = st.container()
    
    # Initialize session state for selected formula if it doesn't exist
    if "selected_formula" not in st.session_state:
        st.session_state.selected_formula = None
    
    # If a formula is selected, show its input section
    if st.session_state.selected_formula is not None:
        with formula_container:
            # Display the selected formula's input section
            st.markdown("---")
            st.markdown(f"# {st.session_state.selected_formula['icon']} {st.session_state.selected_formula['name']}")
            
            # Add a back button
            if st.button("← Back to Dashboard", key="back_to_dashboard"):
                # Clear the selected formula from session state
                st.session_state.selected_formula = None
                st.rerun()
            
            # Call the input section function for the selected formula
            if st.session_state.selected_formula["function"]:
                st.session_state.selected_formula["function"]()
            else:
                st.error(f"The {st.session_state.selected_formula['name']} module is not available.")
    else:
        with dashboard_container:
            # Display the dashboard
            # Header
            st.markdown("""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h1 style='color: #1E88E5; text-align: center;'>✍️ AI Copywriting Tools</h1>
                <p style='text-align: center;'>Choose the perfect copywriting formula for your marketing needs</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Introduction
            st.markdown("""
            ## Welcome to the AI Copywriting Suite
            
            This dashboard provides access to a variety of copywriting formulas, each designed for specific marketing needs. 
            Select a formula below to get started with creating compelling copy for your brand.
            
            ### How to Use This Dashboard
            
            1. Browse the available copywriting formulas below
            2. Click on a formula card to access its specific tool
            3. Fill in the required information
            4. Generate high-quality copy tailored to your needs
            """)
            
            # Create a 3-column layout for the formula cards
            col1, col2, col3 = st.columns(3)
            
            # Display the formula cards
            for i, formula in enumerate(copywriting_formulas):
                # Skip formulas that don't have a function
                if formula["function"] is None:
                    continue
                    
                # Determine which column to use
                col = col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3
                
                with col:
                    # Create a card for each formula
                    st.markdown(f"""
                    <div style='background-color: {formula["color"]}; padding: 20px; border-radius: 10px; margin-bottom: 20px; color: white;'>
                        <h2 style='color: white;'>{formula["icon"]} {formula["name"]}</h2>
                        <p>{formula["description"]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add a button to access the formula
                    if st.button(f"Use {formula['name']}", key=f"btn_{i}"):
                        # Store the selected formula in session state
                        st.session_state.selected_formula = formula
                        st.rerun()

# For standalone execution
if __name__ == "__main__":
    st.set_page_config(
        page_title="AI Copywriting Tools",
        page_icon="✍️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    copywriter_dashboard()