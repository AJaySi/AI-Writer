"""
Personal Letters Module

This module provides a Streamlit interface for generating various types of personal letters
using AI assistance. It collects user inputs specific to the chosen personal letter subtype,
formats the data, generates a prompt for the AI, calls the AI for content generation,
and displays the formatted letter preview and analysis.
"""

import streamlit as st
import datetime
from typing import Dict, Any, List

# Assuming these modules and functions exist and are correctly imported in a real application.
# Placeholder functions are included below for demonstration purposes if actual imports are not available.
# from ..utils.letter_formatter import format_letter, get_letter_preview_html
# from ..utils.letter_analyzer import analyze_letter_tone, check_formality, get_readability_metrics, suggest_improvements
# from ..utils.letter_templates import get_template_by_type
# from ....gpt_providers.text_generation.main_text_generation import llm_text_gen

# --- Placeholder Functions (Replace with actual imports in a real app) ---
# These placeholders mimic the expected behavior of the imported functions
# to allow the rest of the code structure to be reviewed and run without dependencies.

def format_letter(content: str, metadata: Dict[str, Any], letter_type: str = "personal") -> str:
    """Placeholder: Returns the content as is."""
    return content

def get_letter_preview_html(content: str, metadata: Dict[str, Any], letter_type: str = "personal") -> str:
    """Placeholder: Generates a basic HTML preview for personal letters."""
    # Basic HTML structure with inline styles for a personal letter feel
    formatted_paragraphs = "".join(f"<p style='margin-bottom: 1em;'>{p.strip()}</p>" for p in content.split("\n\n") if p.strip())
    return f"""
    <div style="max-width: 700px; margin: 20px auto; padding: 30px; border: 1px solid #e0e0e0; border-radius: 8px; background-color: #ffffff; font-family: 'Georgia', serif; line-height: 1.7; color: #333;">
        <div style="text-align: right; margin-bottom: 30px; font-size: 0.9em; color: #555;">
            {metadata.get('date', 'Date')}
        </div>

        <div style="margin-bottom: 30px;">
             {formatted_paragraphs if formatted_paragraphs else "<p>Letter content goes here...</p>"}
        </div>

        <div style="margin-top: 40px;">
            <p style="margin-bottom: 0.5em;">{metadata.get('complimentary_close', 'Sincerely,')}</p>
            <p style="font-weight: bold; margin-top: 0;">{metadata.get('sender_name', 'Sender Name')}</p>
        </div>
    </div>
    """

def analyze_letter_tone(content: str) -> Dict[str, float]:
    """Placeholder: Returns dummy tone analysis."""
    # Returns scores between 0.0 and 1.0
    return {"warm": 0.9, "sincere": 0.8, "friendly": 0.7}

def check_formality(content: str) -> float:
    """Placeholder: Returns a dummy formality score (0.0 to 1.0)."""
    # Personal letters are typically less formal
    return 0.30 # Example: 30% formal

def get_readability_metrics(content: str) -> Dict[str, Any]:
    """Placeholder: Returns dummy readability metrics."""
    word_count = len(content.split())
    # Estimate reading time in seconds (assuming ~200 words per minute)
    reading_time_seconds = round((word_count / 200) * 60)
    return {
        "word_count": word_count,
        "sentence_count": max(1, content.count('. ') + content.count('! ') + content.count('? ')), # Simple sentence count
        "avg_words_per_sentence": round(word_count / max(1, content.count('. ') + content.count('! ') + content.count('? ')), 2),
        "flesch_reading_ease": 70.0, # Dummy score for personal letters
        "reading_level": "Easy", # Dummy level
        "reading_time_seconds": reading_time_seconds # Added reading time
    }

def suggest_improvements(content: str, letter_type: str) -> List[str]:
    """Placeholder: Returns dummy improvement suggestions."""
    if len(content) < 100:
        return ["Suggestion: The letter seems very brief. Consider adding more personal details or anecdotes."]
    elif "generic" in content.lower():
         return ["Suggestion: Try to make the language more specific and personal to your relationship."]
    else:
        return ["Suggestion: Read it aloud to check if it sounds like your natural voice."]

def get_template_by_type(letter_type: str, subtype: str = "default") -> Dict[str, Any]:
    """Placeholder: Returns a generic template."""
    # This should ideally come from the actual letter_templates module
    return {"structure": ["Greeting", "Body", "Closing"], "guidance": "Generic guidance for a personal letter."}

def llm_text_gen(prompt: str) -> str:
    """Placeholder: Simulates LLM text generation."""
    # In a real app, this would call the actual LLM API
    st.info(f"LLM Prompt:\n```\n{prompt}\n```") # Display prompt for debugging
    # Return a dummy generated letter based on the prompt
    return f"Hi [Generated Recipient Name],\n\nThis is a sample personal letter generated based on the following details:\n\n{prompt}\n\n[Generated content based on the prompt would go here, following the requested structure, tone, emotion, and style.]\n\nBest,\n[Generated Your Name]"

# --- End Placeholder Functions ---

def write_letter():
    """
    Main function for the Personal Letters interface. Sets up the Streamlit page
    and handles navigation between subtype selection and the letter form.
    """

    # Page title and description
    st.title("💌 Personal Letter Writer")
    st.markdown("""
    Create heartfelt personal letters for friends, family, and loved ones. Select a letter type below to get started.
    """)

    # Initialize Streamlit session state variables specific to the personal module.
    # These variables persist across reruns and store the user's progress and data.
    if "personal_letter_subtype" not in st.session_state:
        st.session_state.personal_letter_subtype = None # Stores the ID of the selected personal letter type
    if "personal_letter_generated" not in st.session_state:
        st.session_state.personal_letter_generated = False # Flag to indicate if a letter has been generated
    if "personal_letter_content" not in st.session_state:
        st.session_state.personal_letter_content = None # Stores the generated letter content
    if "personal_letter_metadata" not in st.session_state:
        st.session_state.personal_letter_metadata = {} # Stores metadata like sender/recipient info
    if "personal_letter_form_data" not in st.session_state:
         st.session_state.personal_letter_form_data = {} # Stores the user's input from the form fields


    # Back button logic for subtypes. This button appears when a subtype is selected,
    # allowing the user to return to the subtype selection screen.
    if st.session_state.personal_letter_subtype is not None:
        if st.button("← Back to Personal Letter Types"):
            # Reset session state variables for this module to their initial state
            # This clears the current form data and generated letter.
            st.session_state.personal_letter_subtype = None
            st.session_state.personal_letter_generated = False
            st.session_state.personal_letter_content = None
            st.session_state.personal_letter_metadata = {}
            st.session_state.personal_letter_form_data = {}
            st.rerun() # Rerun the app to update the UI based on the changed state

    # Main navigation logic within the personal module.
    # If no subtype is selected, show the selection grid. Otherwise, show the form for the selected subtype.
    if st.session_state.personal_letter_subtype is None:
        # Display personal letter type selection if no subtype is selected
        display_personal_letter_types()
    else:
        # Display the interface form for the selected personal letter subtype
        display_personal_letter_form(st.session_state.personal_letter_subtype)


def display_personal_letter_types():
    """
    Displays the personal letter type selection interface using a grid of styled buttons.
    Each button represents a specific type of personal letter the user can choose to write.
    """

    st.markdown("## Select Personal Letter Type")

    # Define personal letter types with their details (ID, Name, Icon, Description, Color)
    # This list is used to generate the selection buttons.
    personal_letter_types = [
        {
            "id": "congratulations",
            "name": "Congratulations",
            "icon": "🎉",
            "description": "Celebrate achievements and milestones",
            "color": "#43A047" # Green
        },
        {
            "id": "thank_you",
            "name": "Thank You",
            "icon": "🙏",
            "description": "Express gratitude for gifts, help, or support",
            "color": "#1E88E5" # Blue
        },
        {
            "id": "sympathy",
            "name": "Sympathy",
            "icon": "💐",
            "description": "Offer comfort during difficult times",
            "color": "#5E35B1" # Deep Purple
        },
        {
            "id": "apology",
            "name": "Apology",
            "icon": "🙇",
            "description": "Say sorry and make amends",
            "color": "#FB8C00" # Orange
        },
        {
            "id": "invitation",
            "name": "Invitation",
            "icon": "✉️",
            "description": "Invite someone to an event or gathering",
            "color": "#EC407A" # Pink
        },
        {
            "id": "friendship",
            "name": "Friendship",
            "icon": "👫",
            "description": "Nurture and celebrate friendships",
            "color": "#00ACC1" # Cyan
        },
        {
            "id": "love",
            "name": "Love Letter",
            "icon": "❤️",
            "description": "Express romantic feelings and affection",
            "color": "#E53935" # Red
        },
        {
            "id": "encouragement",
            "name": "Encouragement",
            "icon": "🌟",
            "description": "Offer support and motivation",
            "color": "#FFB300" # Amber
        },
        {
            "id": "farewell",
            "name": "Farewell",
            "icon": "👋",
            "description": "Say goodbye to friends or colleagues",
            "color": "#8E24AA" # Purple
        }
    ]

    # Inject custom CSS to style the Streamlit buttons to look like cards.
    # This provides a visually appealing selection grid.
    st.markdown("""
        <style>
        /* Target Streamlit buttons and apply card-like styling */
        div.stButton > button {
            width: 100%; /* Make buttons fill their column */
            height: 200px; /* Fixed height for consistent grid */
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px; /* Space between rows */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            font-size: 16px;
            border: none;
            cursor: pointer;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            color: white !important; /* Ensure text is white */
        }
        /* Hover effect */
        div.stButton > button:hover {
            transform: translateY(-5px); /* Lift effect */
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }
        /* Style for the text inside the button */
        div.stButton > button h3 {
            color: white !important; /* Ensure icon/title is white */
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 1.2em; /* Adjust title size */
        }
         div.stButton > button p {
            color: white !important; /* Ensure description is white */
            font-size: 0.9em; /* Adjust description size */
            margin: 0;
        }
        </style>
        """, unsafe_allow_html=True)


    # Create a grid layout for the buttons using Streamlit columns (3 columns per row).
    cols = st.columns(3)

    # Display each letter type as a button.
    for i, letter_type_config in enumerate(personal_letter_types):
        with cols[i % 3]: # Place buttons in columns, wrapping every 3
            # Use a unique key for each button based on its ID
            # The button label uses markdown and HTML for icon, name, and description
            if st.button(
                f"### {letter_type_config['icon']} {letter_type_config['name']}\n\n<p>{letter_type_config['description']}</p>",
                key=f"btn_personal_select_{letter_type_config['id']}", # Unique key for each button
                unsafe_allow_html=True # Allow markdown and HTML in the button label
            ):
                # When a button is clicked, update the session state to the selected subtype ID
                st.session_state.personal_letter_subtype = letter_type_config['id']
                # Clear previous data related to letter generation when selecting a new type
                st.session_state.personal_letter_generated = False
                st.session_state.personal_letter_content = None
                st.session_state.personal_letter_metadata = {}
                st.session_state.personal_letter_form_data = {} # Clear previous form data
                st.rerun() # Rerun the app to switch to the form for the selected subtype

    # Apply specific background colors to buttons using their keys and custom CSS
    # This requires injecting CSS after the buttons are rendered.
    # Note: This is a common Streamlit workaround for styling individual buttons dynamically.
    button_styles = ""
    for letter_type_config in personal_letter_types:
        button_styles += f"""
        div.stButton > button[data-testid="stButton"][kind="primary"][sf-key*="btn_personal_select_{letter_type_config['id']}"] {{
            background-color: {letter_type_config['color']};
        }}
         div.stButton > button[data-testid="stButton"][kind="primary"][sf-key*="btn_personal_select_{letter_type_config['id']}"]:hover {{
            background-color: {letter_type_config['color']}D9; /* Slightly darker on hover */
        }}
        """
    st.markdown(f"<style>{button_styles}</style>", unsafe_allow_html=True)


def display_personal_letter_form(subtype: str):
    """
    Displays the form for the selected personal letter subtype. This includes
    input fields specific to the subtype, personal information fields,
    tone and style options, and tabs for previewing and analyzing the generated letter.

    Args:
        subtype: The ID string of the selected personal letter subtype.
    """

    # Get the template for the selected subtype from the templates module.
    # This provides structural guidance and general advice for the LLM.
    template = get_template_by_type("personal", subtype)

    # Display the form title, icon, description, and guidance.
    st.markdown(f"## {get_icon_for_subtype(subtype)} {get_name_for_subtype(subtype)}")
    st.markdown(f"*{get_description_for_subtype(subtype)}*")
    st.info(f"**Guidance:** {template.get('guidance', 'No specific guidance available.')}")

    # Use a Streamlit form to group inputs. This helps manage state and
    # prevents the app from rerunning every time a single input widget changes,
    # improving performance for forms with many inputs.
    with st.form(key=f"personal_letter_form_{subtype}"):
        # Create tabs to organize the form sections.
        tab1, tab2, tab3 = st.tabs(["Letter Details", "Personal Info", "Preview & Export"])

        # Dictionary to store form data collected from all tabs
        form_data = {}

        # --- Tab 1: Letter Details ---
        with tab1:
            st.markdown("### Letter Content Details")

            # Get the configuration for subtype-specific input fields.
            fields = get_fields_for_subtype(subtype)

            # Create form fields dynamically based on the subtype configuration.
            # Populate default values from session state to retain user input across reruns.
            for field in fields:
                # Retrieve default value from session state, falling back to empty string or specific defaults
                default_value = st.session_state.personal_letter_form_data.get(field["id"], "")

                # Create the appropriate Streamlit input widget based on the field type.
                # Use a unique key for each widget to ensure state is managed correctly.
                if field["type"] == "text":
                    form_data[field["id"]] = st.text_input(field["label"], value=default_value, help=field.get("help", ""), key=f"{subtype}_{field['id']}")
                elif field["type"] == "textarea":
                    form_data[field["id"]] = st.text_area(field["label"], value=default_value, help=field.get("help", ""), height=150, key=f"{subtype}_{field['id']}")
                elif field["type"] == "date":
                    # Handle date input default value: use stored value if valid, otherwise use today's date.
                    try:
                        # Attempt to parse stored value as date, fallback to today if unsuccessful
                        default_date = datetime.datetime.strptime(str(default_value), "%Y-%m-%d").date() if default_value else datetime.date.today()
                    except (ValueError, TypeError):
                         default_date = datetime.date.today() # Fallback to today's date
                    form_data[field["id"]] = st.date_input(field["label"], value=default_date, help=field.get("help", ""), key=f"{subtype}_{field['id']}")
                elif field["type"] == "select":
                    # Determine the index of the default value in the options list.
                    try:
                        default_index = field["options"].index(default_value) if default_value in field["options"] else 0
                    except ValueError:
                        default_index = 0 # Default to the first option if the stored value is not valid
                    form_data[field["id"]] = st.selectbox(field["label"], field["options"], index=default_index, help=field.get("help", ""), key=f"{subtype}_{field['id']}")
                elif field["type"] == "slider":
                     # Use the default value from session state or the field config's default
                     default_slider_value = st.session_state.personal_letter_form_data.get(field["id"], field.get("default", (field["min"] + field["max"]) / 2)) # Fallback to midpoint if no default specified
                     form_data[field["id"]] = st.slider(field["label"], field["min"], field["max"], default_slider_value, help=field.get("help", ""), key=f"{subtype}_{field['id']}")


            # Section for selecting letter tone and style characteristics.
            st.markdown("### Tone and Style")
            col1, col2 = st.columns(2)

            with col1:
                # Selectbox for Tone, using subtype-specific tones and session state default.
                tone_options = ["Formal", "Warm", "Casual", "Intimate", "Playful"]
                default_tone = st.session_state.personal_letter_form_data.get("tone", get_default_tone_for_subtype(subtype))
                form_data["tone"] = st.select_slider(
                    "Tone",
                    options=tone_options,
                    value=default_tone, # select_slider uses value directly
                    help="Select the overall tone for your letter.",
                    key=f"{subtype}_tone"
                )

                # Selectbox for Emotional Tone, using subtype-specific emotions and session state default.
                emotion_options = get_emotions_for_subtype(subtype)
                default_emotion = st.session_state.personal_letter_form_data.get("emotion", emotion_options[0] if emotion_options else "Sincere")
                form_data["emotion"] = st.selectbox(
                    "Emotional Tone",
                    emotion_options,
                    index=emotion_options.index(default_emotion) if default_emotion in emotion_options else 0,
                    help="Select the primary emotional tone for your letter.",
                    key=f"{subtype}_emotion"
                )

            with col2:
                # Slider for Length, using session state default.
                length_options = ["Brief", "Standard", "Detailed", "Extensive"]
                default_length = st.session_state.personal_letter_form_data.get("length", "Standard")
                form_data["length"] = st.select_slider(
                    "Length",
                    options=length_options,
                    value=default_length,
                    help="Select the desired length of your letter.",
                    key=f"{subtype}_length"
                )

                # Selectbox for Writing Style, using session state default.
                style_options = ["Straightforward", "Descriptive", "Reflective", "Poetic", "Conversational"]
                default_style = st.session_state.personal_letter_form_data.get("style", "Conversational")
                form_data["style"] = st.selectbox(
                    "Writing Style",
                    style_options,
                    index=style_options.index(default_style) if default_style in style_options else 0,
                    help="Select the overall writing style for your letter.",
                    key=f"{subtype}_style"
                )

            # Section for adding personal touches.
            st.markdown("### Personal Touches")

            # Checkbox and textarea for including a shared memory.
            default_include_memory = st.session_state.personal_letter_form_data.get("include_memory", True)
            include_memory = st.checkbox("Include a shared memory", value=default_include_memory, help="Include a specific memory you share with the recipient.", key=f"{subtype}_include_memory")
            form_data["shared_memory"] = None # Initialize to None
            if include_memory:
                default_shared_memory = st.session_state.personal_letter_form_data.get("shared_memory", "")
                form_data["shared_memory"] = st.text_area(
                    "Shared Memory Details",
                    value=default_shared_memory,
                    height=100,
                    help="Describe the shared memory.",
                    placeholder="e.g., Remember when we went hiking last summer and got caught in the rain?",
                    key=f"{subtype}_shared_memory"
                )

            # Checkbox and textarea for including future plans/wishes.
            default_include_future = st.session_state.personal_letter_form_data.get("include_future", True)
            include_future = st.checkbox("Include future plans or wishes", value=default_include_future, help="Mention upcoming plans or express wishes for their future.", key=f"{subtype}_include_future")
            form_data["future_plans"] = None # Initialize to None
            if include_future:
                default_future_plans = st.session_state.personal_letter_form_data.get("future_plans", "")
                form_data["future_plans"] = st.text_area(
                    "Future Plans or Wishes Details",
                    value=default_future_plans,
                    height=100,
                    help="Describe the future plans or wishes.",
                    placeholder="e.g., I'm looking forward to seeing you at the family reunion next month.",
                    key=f"{subtype}_future_plans"
                )

            # Advanced options expander for less common personal touches.
            with st.expander("Advanced Options"):
                # Checkbox and text input for including a quote.
                default_include_quote = st.session_state.personal_letter_form_data.get("include_quote", False)
                include_quote = st.checkbox("Include a quote or saying", value=default_include_quote, help="Add a relevant quote, saying, or verse.", key=f"{subtype}_include_quote")
                form_data["quote"] = None # Initialize to None
                if include_quote:
                    default_quote = st.session_state.personal_letter_form_data.get("quote", "")
                    form_data["quote"] = st.text_input(
                        "Quote or Saying Text",
                        value=default_quote,
                        help="Enter the quote or saying.",
                        placeholder="e.g., 'True friendship is a plant of slow growth.' - George Washington",
                        key=f"{subtype}_quote"
                    )

                # Checkbox and text input for including an inside joke.
                default_include_inside_joke = st.session_state.personal_letter_form_data.get("include_inside_joke", False)
                include_inside_joke = st.checkbox("Include an inside joke", value=default_include_inside_joke, help="Add a reference only you and the recipient will understand.", key=f"{subtype}_include_inside_joke")
                form_data["inside_joke"] = None # Initialize to None
                if include_inside_joke:
                    default_inside_joke = st.session_state.personal_letter_form_data.get("inside_joke", "")
                    form_data["inside_joke"] = st.text_input(
                        "Inside Joke Details",
                        value=default_inside_joke,
                        help="Describe the inside joke.",
                        placeholder="e.g., Don't worry, I won't bring up the 'flamingo incident' again!",
                        key=f"{subtype}_inside_joke"
                    )


        # --- Tab 2: Personal Info ---
        with tab2:
            # Section for sender and recipient personal information.
            col3, col4 = st.columns(2)

            with col3:
                st.markdown("### Your Information")
                # Input fields for sender's personal details, populated from session state.
                form_data["sender_name"] = st.text_input("Your Name", value=st.session_state.personal_letter_form_data.get("sender_name", ""), help="Your full name or how you sign your letters.", key=f"{subtype}_sender_name")
                form_data["sender_nickname"] = st.text_input("Your Nickname (Optional)", value=st.session_state.personal_letter_form_data.get("sender_nickname", ""), help="A nickname you use with the recipient, if applicable.", key=f"{subtype}_sender_nickname")
                form_data["relationship"] = st.text_input("Your Relationship to Recipient", value=st.session_state.personal_letter_form_data.get("relationship", ""), help="Describe your relationship (e.g., Friend, Sister, Uncle, Partner).", key=f"{subtype}_relationship")

                # Selectbox for relationship duration.
                relationship_durations = ["Less than a year", "1-5 years", "5-10 years", "10+ years", "Lifelong"]
                default_relationship_duration = st.session_state.personal_letter_form_data.get("relationship_duration", "1-5 years")
                form_data["relationship_duration"] = st.selectbox(
                    "How long have you known the recipient?",
                    relationship_durations,
                    index=relationship_durations.index(default_relationship_duration) if default_relationship_duration in relationship_durations else 0,
                    help="Select the approximate duration of your relationship.",
                    key=f"{subtype}_relationship_duration"
                )

            with col4:
                st.markdown("### Recipient Information")
                # Input fields for recipient's personal details, populated from session state.
                form_data["recipient_name"] = st.text_input("Recipient's Name", value=st.session_state.personal_letter_form_data.get("recipient_name", ""), help="The recipient's full name or how you address them.", key=f"{subtype}_recipient_name")
                form_data["recipient_nickname"] = st.text_input("Recipient's Nickname (Optional)", value=st.session_state.personal_letter_form_data.get("recipient_nickname", ""), help="A nickname you use for the recipient, if applicable.", key=f"{subtype}_recipient_nickname")

                # Multiselect for recipient characteristics.
                recipient_traits_options = ["Funny", "Serious", "Creative", "Practical", "Emotional", "Reserved", "Outgoing", "Thoughtful", "Adventurous", "Kind", "Intelligent", "Quiet", "Loud", "Supportive", "Independent"] # Expanded options
                default_recipient_traits = st.session_state.personal_letter_form_data.get("recipient_traits", []) # Default to empty list
                # Ensure default_recipient_traits is a list for multiselect
                if isinstance(default_recipient_traits, str):
                    default_recipient_traits = [trait.strip() for trait in default_recipient_traits.split(',') if trait.strip()]

                form_data["recipient_traits"] = st.multiselect(
                    "Recipient's Characteristics",
                    recipient_traits_options,
                    default=default_recipient_traits,
                    help="Select traits that describe the recipient. This helps tailor the language.",
                    key=f"{subtype}_recipient_traits"
                )

                # Text area for special considerations.
                form_data["special_considerations"] = st.text_area(
                    "Special Considerations (Optional)",
                    value=st.session_state.personal_letter_form_data.get("special_considerations", ""),
                    height=100,
                    help="Mention any sensitive topics to avoid or specific circumstances to acknowledge (e.g., they recently lost a pet, celebrating sobriety).",
                    placeholder="e.g., Recently lost a job, celebrating sobriety milestone",
                    key=f"{subtype}_special_considerations"
                )


        # --- Tab 3: Preview & Export ---
        with tab3:
            # Instructions for the user before generation.
            if not st.session_state.personal_letter_generated:
                st.info("Complete the letter details and click 'Generate Letter' to preview your letter.")

            # The Generate button is placed inside the form. Clicking it submits the form
            # and triggers the code block below it to run.
            generate_button = st.form_submit_button("Generate Letter", type="primary")

            if generate_button:
                # Action to perform when the form is submitted via the Generate button.

                # Store the current state of all form inputs in session state.
                # This allows retaining user inputs even after generation or regeneration.
                st.session_state.personal_letter_form_data = form_data.copy()

                # Prepare metadata specifically for the formatter and analysis functions.
                # This includes structured contact info, dates, salutation, etc.
                metadata = {
                    "sender_name": form_data.get("sender_name", ""),
                    "sender_nickname": form_data.get("sender_nickname", ""),
                    "recipient_name": form_data.get("recipient_name", ""),
                    "recipient_nickname": form_data.get("recipient_nickname", ""),
                    "relationship": form_data.get("relationship", ""),
                    "relationship_duration": form_data.get("relationship_duration", ""),
                    # Convert list of traits back to a string for metadata if needed by formatter/analyzer
                    "recipient_traits": ", ".join(form_data.get("recipient_traits", [])) if form_data.get("recipient_traits") else "",
                    "special_considerations": form_data.get("special_considerations", ""),
                    "date": datetime.datetime.now().strftime("%B %d, %Y"), # Use current date for the letter
                }
                # Determine salutation based on nickname preference
                recipient_display_name = metadata["recipient_nickname"] if metadata.get("recipient_nickname") else metadata["recipient_name"]
                metadata["salutation"] = f"Dear {recipient_display_name}," if recipient_display_name else "Dear Friend," # Fallback salutation
                # Determine complimentary close based on tone/formality - simple logic for now
                metadata["complimentary_close"] = "Warmly," if form_data.get("tone") in ["Warm", "Intimate", "Playful"] else "Sincerely,"


                st.session_state.personal_letter_metadata = metadata.copy()


                # --- Letter Generation Logic ---
                # Check for minimal required fields before attempting generation.
                if not form_data.get("sender_name") or not form_data.get("recipient_name"):
                    st.error("Please provide at least your name and the recipient's name.")
                else:
                    # Display a spinner while the AI generates the letter.
                    with st.spinner("Generating your personal letter..."):
                        # Combine all necessary data into a single dictionary for the generation function.
                        # This includes both form data and metadata.
                        # Note: tone, emotion, length, style are already in form_data
                        generation_data = {
                            "subtype": subtype,
                            **form_data, # Includes all collected form inputs
                            **metadata # Includes structured sender/recipient/date/relationship info
                        }

                        # Call the letter generation function with the combined data.
                        letter_content = generate_personal_letter(generation_data)

                        # Store the generated letter content and update the generated flag.
                        st.session_state.personal_letter_content = letter_content
                        st.session_state.personal_letter_generated = True

                        # Rerun the app to exit the form block and display the generated letter section.
                        # This rerun happens automatically on form submission, but explicit state updates
                        # ensure the display logic reacts correctly.
                        # st.rerun() # Rerun is handled by form submission

        # --- Display Generated Letter and Analysis ---
        # This block executes if a letter has been generated and stored in session state.
        if st.session_state.personal_letter_generated and st.session_state.personal_letter_content is not None:
            letter_content = st.session_state.personal_letter_content
            metadata = st.session_state.personal_letter_metadata

            # Create tabs for different views of the generated letter.
            preview_tab1, preview_tab2, preview_tab3 = st.tabs(["Formatted Preview", "Plain Text", "Analysis"])

            with preview_tab1:
                st.markdown("### Letter Preview")
                # Generate and display the HTML preview of the letter using the formatter utility.
                # Pass letter_type="personal" to the formatter.
                html_preview = get_letter_preview_html(letter_content, metadata, letter_type="personal")
                st.markdown(html_preview, unsafe_allow_html=True)

                # Download button for the plain text version of the letter.
                file_name_suffix = metadata.get('recipient_name', 'personal').replace(' ', '_').lower()
                st.download_button(
                    label="Download as Text",
                    data=letter_content,
                    file_name=f"{subtype}_letter_to_{file_name_suffix}_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )

            with preview_tab2:
                st.markdown("### Plain Text Content")
                # Display the raw generated letter content in a text area.
                st.text_area("Letter Content", letter_content, height=400, key=f"{subtype}_plain_text_display")

                # Button to copy the plain text content to the clipboard.
                st.button("Copy Plain Text (Manual Copy from above)", help="Select and copy the text from the box above.", key=f"{subtype}_copy_plain_text_instruction")


            with preview_tab3:
                st.markdown("### Letter Analysis")
                # Perform and display analysis of the generated letter using utility functions.

                # Analyze tone, formality, and readability.
                tone_analysis = analyze_letter_tone(letter_content)
                formality_score = check_formality(letter_content) # Returns score between 0.0 and 1.0
                readability_metrics = get_readability_metrics(letter_content)
                # Get improvement suggestions, passing the letter type for context.
                improvement_suggestions = suggest_improvements(letter_content, "personal") # Pass "personal" as letter_type

                # Display analysis results in two columns.
                col5, col6 = st.columns(2)

                with col5:
                    st.markdown("#### Tone Analysis")
                    # Display each tone score.
                    if tone_analysis:
                        for tone, score in tone_analysis.items():
                            st.write(f"- **{tone.capitalize()}:** {score:.2f}")
                    else:
                        st.info("Tone analysis not available.")


                    st.markdown("#### Formality")
                    # Display formality score as a percentage and a progress bar.
                    st.progress(formality_score) # Progress bar expects a value between 0.0 and 1.0
                    st.write(f"Formality Score: {formality_score * 100:.0f}/100") # Display as a percentage (0-100)


                with col6:
                    st.markdown("#### Readability Metrics")
                    # Display various readability metrics.
                    if readability_metrics:
                        st.write(f"**Word Count:** {readability_metrics.get('word_count', 'N/A')} words")
                        st.write(f"**Sentence Count:** {readability_metrics.get('sentence_count', 'N/A')} sentences")
                        st.write(f"**Avg Words per Sentence:** {readability_metrics.get('avg_words_per_sentence', 'N/A')}")
                        st.write(f"**Flesch Reading Ease:** {readability_metrics.get('flesch_reading_ease', 'N/A')}")
                        st.write(f"**Reading Level:** {readability_metrics.get('reading_level', 'N/A')}")
                        # Display estimated reading time.
                        st.write(f"**Estimated Reading Time:** {readability_metrics.get('reading_time_seconds', 'N/A')} seconds")
                    else:
                        st.info("Readability metrics not available.")

                st.markdown("#### Suggestions for Improvement")
                # Display improvement suggestions.
                if improvement_suggestions:
                    # Iterate through the list and display each suggestion as a list item.
                    for suggestion in improvement_suggestions:
                        st.markdown(f"- {suggestion}")
                else:
                    st.info("No specific suggestions for improvement found.")

            # Button to regenerate the letter. Placed outside the form so it's always visible
            # after generation, without needing to resubmit the form first.
            # Keep the form data in session state so the user's inputs are retained.
            if st.button("Regenerate Letter", key=f"{subtype}_regenerate_button"):
                # Reset the generated state and content to allow the form to be displayed again.
                st.session_state.personal_letter_generated = False
                st.session_state.personal_letter_content = None # Clear generated content
                # st.session_state.personal_letter_form_data is already populated from the form submit
                st.rerun() # Rerun to show the form with previous inputs


def generate_personal_letter(data: Dict[str, Any]) -> str:
    """
    Generates a personal letter using the LLM by constructing a detailed prompt
    based on the collected user inputs and metadata.

    Args:
        data: A dictionary containing all collected user inputs and metadata
              (from the form and session state).

    Returns:
        The generated letter content as a string, or an error message if generation fails.
    """

    # Extract key generation parameters from the data dictionary.
    subtype = data.get("subtype", "default")
    tone = data.get("tone", "Warm")
    emotion = data.get("emotion", "Sincere")
    length = data.get("length", "Standard")
    style = data.get("style", "Conversational")

    # Get template guidance and structure to include in the prompt.
    template = get_template_by_type("personal", subtype)
    template_guidance = template.get("guidance", "Follow standard personal letter practices.")
    template_structure = template.get("structure", ["Greeting", "Body", "Closing"])

    # Build the prompt string step-by-step, including all relevant details
    # from the user's input and selected options.
    prompt_parts = [
        f"Write a {length.lower()} personal {get_name_for_subtype(subtype)} letter with a {tone.lower()}, {emotion.lower()} tone and {style.lower()} writing style.",
        f"Purpose: {get_description_for_subtype(subtype)}",
        f"Recipient: {data.get('recipient_name', '')} ({data.get('recipient_nickname', '') if data.get('recipient_nickname') else 'no nickname'})",
        f"Sender: {data.get('sender_name', '')} ({data.get('sender_nickname', '') if data.get('sender_nickname') else 'no nickname'})",
        f"Relationship: {data.get('relationship', 'Not specified')} for {data.get('relationship_duration', 'Not specified')}",
    ]

    # Add recipient traits if provided.
    if data.get('recipient_traits'):
        # Ensure traits are listed nicely in the prompt
        traits_list = ", ".join(data['recipient_traits']) if isinstance(data['recipient_traits'], list) else data['recipient_traits']
        if traits_list:
            prompt_parts.append(f"Recipient's Characteristics: {traits_list}")

    # Add subtype-specific details from the collected form data.
    subtype_fields = get_fields_for_subtype(subtype)
    if subtype_fields:
        prompt_parts.append("\nKey Details to Include:")
        for field in subtype_fields:
            field_value = data.get(field["id"])
            # Include the field's label and value in the prompt only if the value is not empty.
            if field_value:
                 # Format date fields nicely for the prompt if they are date objects.
                if field["type"] == "date":
                     try:
                         field_value_str = field_value.strftime("%B %d, %Y")
                     except AttributeError:
                         field_value_str = str(field_value) # Fallback if not a date object
                else:
                    field_value_str = str(field_value)

                prompt_parts.append(f"- {field['label']}: {field_value_str}")


    # Add personal touches if included.
    if data.get('include_memory') and data.get('shared_memory'):
        prompt_parts.append(f"Include this shared memory: {data['shared_memory']}")

    if data.get('include_future') and data.get('future_plans'):
        prompt_parts.append(f"Include these future plans or wishes: {data['future_plans']}")

    if data.get('include_quote') and data.get('quote'):
        prompt_parts.append(f"Include this quote: {data['quote']}")

    if data.get('include_inside_joke') and data.get('inside_joke'):
        prompt_parts.append(f"Include this inside joke: {data['inside_joke']}")

    # Add special considerations if provided.
    if data.get('special_considerations'):
        prompt_parts.append(f"\nSpecial considerations: {data['special_considerations']}")

    # Add the template structure and overall guidance to the prompt.
    # This helps the LLM understand the desired layout and writing style.
    prompt_parts.append("\nFollow this general structure:")
    for i, section in enumerate(template_structure):
        prompt_parts.append(f"{i+1}. {section}")
    prompt_parts.append(f"\nOverall Writing Guidance: {template_guidance}")

    # Add final instructions for the LLM.
    prompt_parts.append("\nMake the letter personal, authentic, and appropriate for the relationship described. Use natural language that sounds like it was written by a real person, not AI.")


    # Combine all prompt parts into a single string.
    final_prompt = "\n".join(prompt_parts)

    # Call the LLM text generation function with the constructed prompt.
    try:
        letter_content = llm_text_gen(final_prompt)
        return letter_content
    except Exception as e:
        # Catch any errors during LLM generation and display an error message.
        st.error(f"Error generating letter: {str(e)}")
        return "Error generating letter. Please try again."


# --- Helper functions (from original code, slightly enhanced) ---

def get_icon_for_subtype(subtype: str) -> str:
    """Maps a personal letter subtype ID to a relevant emoji icon."""
    icons = {
        "congratulations": "🎉",
        "thank_you": "🙏",
        "sympathy": "💐",
        "apology": "🙇",
        "invitation": "✉️",
        "friendship": "👫",
        "love": "❤️",
        "encouragement": "🌟",
        "farewell": "👋"
    }
    return icons.get(subtype, "📝") # Default icon

def get_name_for_subtype(subtype: str) -> str:
    """Maps a personal letter subtype ID to its display name."""
    names = {
        "congratulations": "Congratulations Letter",
        "thank_you": "Thank You Letter",
        "sympathy": "Sympathy Letter",
        "apology": "Apology Letter",
        "invitation": "Invitation Letter",
        "friendship": "Friendship Letter",
        "love": "Love Letter",
        "encouragement": "Encouragement Letter",
        "farewell": "Farewell Letter"
    }
    return names.get(subtype, "Personal Letter") # Default name

def get_description_for_subtype(subtype: str) -> str:
    """Maps a personal letter subtype ID to a brief description."""
    descriptions = {
        "congratulations": "Celebrate achievements and milestones with a heartfelt congratulations letter.",
        "thank_you": "Express gratitude for gifts, help, or support with a sincere thank you letter.",
        "sympathy": "Offer comfort and support during difficult times with a thoughtful sympathy letter.",
        "apology": "Say sorry and make amends with a sincere apology letter.",
        "invitation": "Invite someone to an event or gathering with a personal invitation letter.",
        "friendship": "Nurture and celebrate friendships with a meaningful letter.",
        "love": "Express romantic feelings and affection with a heartfelt love letter.",
        "encouragement": "Offer support and motivation with an uplifting encouragement letter.",
        "farewell": "Say goodbye to friends or colleagues with a touching farewell letter."
    }
    return descriptions.get(subtype, "Create a personalized letter for your specific needs.") # Default description

def get_fields_for_subtype(subtype: str) -> List[Dict[str, Any]]:
    """
    Provides a list of input field configurations specific to each personal letter subtype.
    Each dictionary in the list defines a form input field, including its ID, label,
    type, and optional properties like help text, options (for select/slider),
    min/max values (for slider/number), and a default value.
    """

    # Define subtype-specific fields.
    if subtype == "congratulations":
        return [
            {
                "id": "achievement",
                "label": "Achievement Being Celebrated",
                "type": "text",
                "help": "What specific achievement or milestone are you congratulating them for? Be as specific as possible."
            },
            {
                "id": "significance",
                "label": "Significance of Achievement",
                "type": "textarea",
                "help": "Explain why this achievement is significant to you or to them. How does it make you feel?"
            }
        ]
    elif subtype == "thank_you":
        return [
            {
                "id": "reason",
                "label": "Reason for Thanks",
                "type": "text",
                "help": "What specific gift, act of kindness, or support are you thanking them for?"
            },
            {
                "id": "impact",
                "label": "Impact of Their Action",
                "type": "textarea",
                "help": "Explain how their action or gift specifically helped or affected you. Be sincere."
            }
        ]
    elif subtype == "sympathy":
        return [
            {
                "id": "reason",
                "label": "Reason for Sympathy",
                "type": "text",
                "help": "What loss or difficult situation are you expressing sympathy for? (e.g., Loss of a loved one, difficult time)"
            },
            {
                "id": "relationship_to_affected",
                "label": "Recipient's Relationship to the Deceased/Affected (Optional)",
                "type": "text",
                "help": "What was the recipient's relationship to the person who passed away or is affected, if applicable? (e.g., Their mother, their pet)"
            },
             {
                "id": "positive_memory",
                "label": "Share a Positive Memory (Optional)",
                "type": "textarea",
                "help": "If appropriate, share a brief, positive memory of the person who was lost or the situation."
            },
            {
                "id": "offer_of_support",
                "label": "Offer of Support (Optional)",
                "type": "textarea",
                "help": "Offer specific ways you can provide support (e.g., 'I'm here to listen anytime', 'I can help with meals')."
            }
        ]
    elif subtype == "apology":
        return [
            {
                "id": "reason",
                "label": "What You Are Apologizing For",
                "type": "textarea",
                "help": "Clearly and specifically state what you are apologizing for. Take responsibility."
            },
            {
                "id": "impact",
                "label": "Acknowledge Impact of Actions",
                "type": "textarea",
                "help": "Show that you understand how your actions affected the recipient and acknowledge their feelings."
            },
            {
                "id": "amends",
                "label": "Proposed Amends or How You Will Make Things Right (Optional)",
                "type": "textarea",
                "help": "Suggest ways you can make amends or explain what you will do to prevent it from happening again."
            }
        ]
    elif subtype == "invitation":
        return [
            {
                "id": "event",
                "label": "Event Name",
                "type": "text",
                "help": "What is the name or type of event? (e.g., Birthday Party, Dinner Gathering, Wedding)"
            },
            {
                "id": "date_time",
                "label": "Date and Time",
                "type": "text", # Using text for flexibility (e.g., "Saturday, November 18th at 7:00 PM")
                "help": "When is the event taking place? Include day, date, and time."
            },
            {
                "id": "location",
                "label": "Location",
                "type": "text",
                "help": "Where is the event taking place? Include the full address if necessary."
            },
            {
                "id": "purpose_theme",
                "label": "Purpose or Theme (Optional)",
                "type": "text",
                "help": "Briefly mention the purpose or theme of the event."
            },
            {
                "id": "rsvp_details",
                "label": "RSVP Details",
                "type": "textarea",
                "help": "Specify how and by when they should RSVP (e.g., 'Please RSVP by November 10th to [Your Email/Phone]')."
            }
        ]
    elif subtype == "friendship":
        return [
            {
                "id": "occasion",
                "label": "Occasion for Writing (Optional)",
                "type": "text",
                "help": "Is there a specific reason for writing? (e.g., friendship anniversary, just thinking of you)"
            },
            {
                "id": "valued_aspects",
                "label": "Valued Aspects of Friendship",
                "type": "textarea",
                "help": "What specific qualities or moments do you value most about your friendship with this person?"
            },
             {
                "id": "recent_update",
                "label": "Recent Update or Shared Experience (Optional)",
                "type": "textarea",
                "help": "Mention something recent you've shared or an update in your life."
            }
        ]
    elif subtype == "love":
        return [
            {
                "id": "occasion",
                "label": "Occasion for Writing (Optional)",
                "type": "text",
                "help": "Is there a specific reason for writing? (e.g., anniversary, Valentine's Day, just because)"
            },
            {
                "id": "feelings",
                "label": "Feelings to Express",
                "type": "textarea",
                "help": "Describe the depth and nature of your feelings for your loved one."
            },
            {
                "id": "special_memories_love", # Added suffix
                "label": "Special Memories",
                "type": "textarea",
                "help": "Recall and describe cherished memories you share."
            },
             {
                "id": "qualities_loved",
                "label": "Qualities You Love and Appreciate",
                "type": "textarea",
                "help": "Mention specific qualities you adore about them."
            }
        ]
    elif subtype == "encouragement":
        return [
            {
                "id": "situation",
                "label": "Situation Requiring Encouragement",
                "type": "textarea",
                "help": "Describe the specific challenge or situation the recipient is facing."
            },
            {
                "id": "strengths",
                "label": "Strengths and Abilities to Highlight",
                "type": "textarea",
                "help": "Remind them of their strengths, resilience, or past successes that will help them through this."
            },
             {
                "id": "belief_statement",
                "label": "Statement of Belief in Them",
                "type": "textarea",
                "help": "Clearly state your confidence in their ability to overcome the challenge."
            }
        ]
    elif subtype == "farewell":
        return [
            {
                "id": "reason",
                "label": "Reason for Farewell",
                "type": "text",
                "help": "Why are you or the recipient saying goodbye? (e.g., Moving away, new job, retirement)"
            },
            {
                "id": "memories_farewell", # Added suffix
                "label": "Memories to Mention",
                "type": "textarea",
                "help": "Share positive memories you have with the recipient."
            },
            {
                "id": "wishes",
                "label": "Future Wishes",
                "type": "textarea",
                "help": "Express your sincere good wishes for their future endeavors."
            },
             {
                "id": "stay_in_touch",
                "label": "How to Stay in Touch (Optional)",
                "type": "textarea",
                "help": "Suggest ways to keep in touch (e.g., 'Let's connect on LinkedIn', 'I'll visit when I can')."
            }
        ]

    # Default fields if subtype is not recognized or no specific fields are defined.
    # This provides a basic textarea for general content.
    return [
        {
            "id": "main_content",
            "label": "Main Content",
            "type": "textarea",
            "help": "Enter the main content you want to include in your personal letter."
        }
    ]

def get_default_tone_for_subtype(subtype: str) -> str:
    """Maps a personal letter subtype ID to a suggested default tone."""
    tones = {
        "congratulations": "Warm",
        "thank_you": "Warm",
        "sympathy": "Warm",
        "apology": "Formal", # Apologies often require a more formal/serious tone initially
        "invitation": "Casual",
        "friendship": "Casual",
        "love": "Intimate",
        "encouragement": "Warm",
        "farewell": "Warm"
    }
    return tones.get(subtype, "Warm") # Default tone

def get_emotions_for_subtype(subtype: str) -> List[str]:
    """Maps a personal letter subtype ID to a list of suggested emotional tones."""
    emotions = {
        "congratulations": ["Joyful", "Proud", "Excited", "Impressed", "Inspired", "Happy"],
        "thank_you": ["Grateful", "Appreciative", "Touched", "Moved", "Thankful", "Humbled"],
        "sympathy": ["Compassionate", "Caring", "Supportive", "Empathetic", "Gentle", "Sorrowful"],
        "apology": ["Remorseful", "Sincere", "Humble", "Regretful", "Honest", "Contrite"],
        "invitation": ["Excited", "Welcoming", "Enthusiastic", "Anticipatory", "Cheerful", "Friendly"],
        "friendship": ["Appreciative", "Affectionate", "Nostalgic", "Grateful", "Warm", "Loyal"],
        "love": ["Passionate", "Devoted", "Adoring", "Tender", "Affectionate", "Romantic"],
        "encouragement": ["Supportive", "Optimistic", "Confident", "Reassuring", "Inspiring", "Hopeful"],
        "farewell": ["Nostalgic", "Hopeful", "Bittersweet", "Appreciative", "Reflective", "Fond"]
    }
    # Return the list of emotions for the subtype, or a default list if not found.
    return emotions.get(subtype, ["Sincere", "Warm", "Friendly", "Genuine", "Thoughtful"])

# Example of how to run the app (for local development using `streamlit run your_script_name.py`)
# Uncomment the lines below to make this script directly executable.
# if __name__ == "__main__":
#     write_letter()
