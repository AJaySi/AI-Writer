"""
AI Letter Writer - Main Module

This module provides a comprehensive interface for generating various types of letters
using AI assistance. It supports multiple letter formats, styles, and use cases.
It uses Streamlit for the user interface.
"""

import streamlit as st
# Assuming these modules exist in a package structure
from .letter_types import (
    business_letters,
    personal_letters,
    formal_letters,
    cover_letters,
    recommendation_letters,
    complaint_letters,
    thank_you_letters,
    invitation_letters
)
# Assuming these utility functions exist
from .utils.letter_formatter import format_letter
from .utils.letter_analyzer import analyze_letter_tone, check_formality
from .utils.letter_templates import get_template_by_type

# Define the letter types and their properties
LETTER_TYPES_CONFIG = [
    {
        "id": "business",
        "name": "Business Letters",
        "icon": "💼",
        "description": "Professional correspondence for business contexts.",
        "color": "#1E88E5", # Blue 600
        "module": business_letters
    },
    {
        "id": "personal",
        "name": "Personal Letters",
        "icon": "💌",
        "description": "Heartfelt messages for friends and family.",
        "color": "#43A047", # Green 600
        "module": personal_letters
    },
    {
        "id": "formal",
        "name": "Formal Letters",
        "icon": "📜",
        "description": "Official correspondence for institutions and authorities.",
        "color": "#5E35B1", # Deep Purple 600
        "module": formal_letters
    },
    {
        "id": "cover",
        "name": "Cover Letters",
        "icon": "📋",
        "description": "Job application letters to showcase your qualifications.",
        "color": "#FB8C00", # Orange 600
        "module": cover_letters
    },
    {
        "id": "recommendation",
        "name": "Recommendation Letters",
        "icon": "👍",
        "description": "Endorse colleagues, students, or employees.",
        "color": "#00ACC1", # Cyan 600
        "module": recommendation_letters
    },
    {
        "id": "complaint",
        "name": "Complaint Letters",
        "icon": "⚠️",
        "description": "Address issues with products, services, or situations.",
        "color": "#E53935", # Red 600
        "module": complaint_letters
    },
    {
        "id": "thank_you",
        "name": "Thank You Letters",
        "icon": "🙏",
        "description": "Express gratitude for various occasions.",
        "color": "#8E24AA", # Purple 600
        "module": thank_you_letters
    },
    {
        "id": "invitation",
        "name": "Invitation Letters",
        "icon": "🎉",
        "description": "Invite people to events, interviews, or gatherings.",
        "color": "#FFB300", # Amber 600
        "module": invitation_letters
    }
]

# Map letter type IDs to their modules for easy access
LETTER_MODULES_MAP = {config["id"]: config["module"] for config in LETTER_TYPES_CONFIG}


def initialize_session_state() -> None:
    """Initializes necessary Streamlit session state variables."""
    if "letter_type" not in st.session_state:
        st.session_state.letter_type = None
    if "letter_subtype" not in st.session_state:
        st.session_state.letter_subtype = None # Useful if a letter type has subtypes
    if "generated_letter" not in st.session_state:
        st.session_state.generated_letter = None
    if "letter_metadata" not in st.session_state:
        # Store information like sender, recipient, date, subject, tone, etc.
        st.session_state.letter_metadata = {}
    if "letter_input_data" not in st.session_state:
         # Store user inputs for letter generation
         st.session_state.letter_input_data = {}


def display_letter_type_selection() -> None:
    """Displays the letter type selection interface using a grid of styled containers with buttons."""

    st.markdown("## Select Letter Type")

    # Create a grid layout for the cards (3 columns)
    cols = st.columns(3)

    # Display each letter type as a card with a button below it
    for i, letter_type_config in enumerate(LETTER_TYPES_CONFIG):
        with cols[i % 3]:
            # Use markdown to create a styled container for the card appearance
            st.markdown(
                f"""
                <div style="
                    background-color: {letter_type_config['color']};
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 10px; /* Space between card content and button */
                    color: white;
                    min-height: 180px; /* Ensure consistent minimum height */
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between; /* Distribute space within the card */
                ">
                    <h3 style="margin-top: 0; color: white;">{letter_type_config['icon']} {letter_type_config['name']}</h3>
                    <p style="color: white;">{letter_type_config['description']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Place the Streamlit button below the styled container
            # Make the button expand to the width of the column for better alignment with the card
            if st.button(
                f"Select {letter_type_config['name']}",
                key=f"btn_select_{letter_type_config['id']}", # Unique key for each button
                use_container_width=True
            ):
                st.session_state.letter_type = letter_type_config['id']
                # Clear previous state data when selecting a new type
                st.session_state.letter_subtype = None
                st.session_state.generated_letter = None
                st.session_state.letter_metadata = {}
                st.session_state.letter_input_data = {}
                st.rerun()


def display_letter_interface(letter_type_id: str) -> None:
    """
    Displays the interface for the selected letter type by calling the
    appropriate module's write function.

    Args:
        letter_type_id: The ID string of the selected letter type.
    """
    module = LETTER_MODULES_MAP.get(letter_type_id)

    if module:
        try:
            # Call the main function (e.g., write_letter or main) from the selected module
            # Assuming the module has a function that renders its UI and handles generation
            module.write_letter() # Assuming the function is named 'write_letter'
        except AttributeError:
             st.error(f"Module for '{letter_type_id}' does not have a 'write_letter' function.")
        except Exception as e:
             st.error(f"An error occurred while loading the interface for '{letter_type_id}': {e}")
    else:
        st.error(f"Letter type module '{letter_type_id}' not found in map.")


def write_letter() -> None:
    """Main function for the AI Letter Writer interface."""

    # Page title and description
    st.title("✉️ AI Letter Writer")
    st.markdown("""
    Create professional, personalized letters for any occasion. Select a letter type below to get started.
    Our AI will help you craft the perfect letter with the right tone, structure, and content.
    """)

    # Initialize session state on first run
    initialize_session_state()

    # Back button logic - only show if a letter type is selected
    if st.session_state.letter_type is not None:
        if st.button("← Back to Letter Types"):
            # Reset session state to return to selection
            st.session_state.letter_type = None
            st.session_state.letter_subtype = None
            st.session_state.generated_letter = None
            st.session_state.letter_metadata = {}
            st.session_state.letter_input_data = {}
            st.rerun() # Rerun to show the selection page

    # Main navigation logic
    if st.session_state.letter_type is None:
        # Display letter type selection if no type is selected
        display_letter_type_selection()
    else:
        # Display the interface for the selected letter type
        display_letter_interface(st.session_state.letter_type)

    # --- Placeholder for displaying generated letter and actions ---
    # This part would typically be handled within the specific letter type modules
    # after the letter is generated. However, if a common display is needed
    # after returning from the module function, it would go here, but this
    # requires the module function to somehow signal completion or store
    # the generated letter in session state. The current structure expects
    # the module's write_letter() to handle its entire lifecycle.

    # Example of potentially displaying a generated letter after returning
    # (This assumes the module updates st.session_state.generated_letter)
    # if st.session_state.generated_letter:
    #     st.subheader("Generated Letter Preview")
    #     st.text_area("Your Letter", st.session_state.generated_letter, height=400)
    #     # Add options like copy, download, analyze, edit, etc.


if __name__ == "__main__":
    # Run the main letter writing function when the script is executed
    write_letter()