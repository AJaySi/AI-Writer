"""
Formal Letters Module

This module provides a Streamlit interface for generating various types of formal letters
using AI assistance. It collects user inputs specific to the chosen formal letter subtype,
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
    """Placeholder: Generates a basic HTML preview for formal letters."""
    # Basic HTML structure with inline styles for preview
    formatted_paragraphs = "".join(f"<p style='margin-bottom: 1em;'>{p.strip()}</p>" for p in content.split("\n\n") if p.strip())
    return f"""
    <div style="max-width: 800px; margin: 20px auto; padding: 30px; border: 1px solid #d0d0d0; border-radius: 8px; background-color: #ffffff; font-family: 'Arial', sans-serif; line-height: 1.6; color: #333;">
        <div style="text-align: right; margin-bottom: 20px;">{metadata.get('date', 'Date')}</div>
        <div style="margin-bottom: 20px; font-weight: bold;">Subject: {metadata.get('subject', 'No Subject')}</div>
        <div style="margin-bottom: 20px;">{metadata.get('salutation', 'Dear Recipient,')}</div>
        <div style="margin-bottom: 20px;">{formatted_paragraphs if formatted_paragraphs else "<p>Letter content goes here...</p>"}</div>
        <div style="margin-top: 40px;">{metadata.get('complimentary_close', 'Sincerely,')}</div>
        <div>{metadata.get('sender_name', 'Sender Name')}</div>
        <div>{metadata.get('sender_title', 'Sender Title')}</div>
    </div>
    """

def analyze_letter_tone(content: str) -> Dict[str, float]:
    """Placeholder: Returns dummy tone analysis."""
    # Returns scores between 0.0 and 1.0
    return {"professional": 0.9, "formal": 0.85, "objective": 0.7}

def check_formality(content: str) -> float:
    """Placeholder: Returns a dummy formality score (0.0 to 1.0)."""
    return 0.88 # Example: 88% formal

def get_readability_metrics(content: str) -> Dict[str, Any]:
    """Placeholder: Returns dummy readability metrics."""
    word_count = len(content.split())
    # Estimate reading time in seconds (assuming ~200 words per minute)
    reading_time_seconds = round((word_count / 200) * 60)
    return {
        "word_count": word_count,
        "sentence_count": max(1, content.count('. ') + content.count('! ') + content.count('? ')), # Simple sentence count
        "avg_words_per_sentence": round(word_count / max(1, content.count('. ') + content.count('! ') + content.count('? ')), 2),
        "flesch_reading_ease": 45.0, # Dummy score for formal letters
        "reading_level": "Difficult", # Dummy level
        "reading_time_seconds": reading_time_seconds # Added reading time
    }

def suggest_improvements(content: str, letter_type: str) -> List[str]:
    """Placeholder: Returns dummy improvement suggestions."""
    if "passive voice" in content.lower():
        return ["Suggestion: Consider using more active voice for clarity and impact."]
    elif len(content.split('.')) < 5:
         return ["Suggestion: The letter seems very short. Ensure all necessary details are included."]
    else:
        return ["Suggestion: Double-check for any jargon that the recipient might not understand."]

def get_template_by_type(letter_type: str, subtype: str = "default") -> Dict[str, Any]:
    """Placeholder: Returns a generic template."""
    # This should ideally come from the actual letter_templates module
    return {"structure": ["Sender Info", "Date", "Recipient Info", "Subject", "Salutation", "Body", "Closing", "Signature"], "guidance": "Follow standard formal letter practices."}

def llm_text_gen(prompt: str) -> str:
    """Placeholder: Simulates LLM text generation."""
    # In a real app, this would call the actual LLM API
    st.info(f"LLM Prompt:\n```\n{prompt}\n```") # Display prompt for debugging
    # Return a dummy generated letter based on the prompt
    return f"Subject: Generated Formal Letter Preview\n\nDear [Generated Recipient Name],\n\nThis is a sample formal letter generated based on the following details:\n\n{prompt}\n\n[Generated content based on the prompt would go here, following the requested structure, formality, tone, and language complexity.]\n\nSincerely,\n[Generated Your Name]"

# --- End Placeholder Functions ---


def write_letter():
    """
    Main function for the Formal Letters interface. Sets up the Streamlit page
    and handles navigation between subtype selection and the letter form.
    """

    # Page title and description
    st.title("📝 Formal Letter Writer")
    st.markdown("""
    Create professional formal letters for business, academic, and official purposes. Select a letter type below to get started.
    """)

    # Initialize Streamlit session state variables specific to the formal module.
    # These variables persist across reruns and store the user's progress and data.
    if "formal_letter_subtype" not in st.session_state:
        st.session_state.formal_letter_subtype = None # Stores the ID of the selected formal letter type
    if "formal_letter_generated" not in st.session_state:
        st.session_state.formal_letter_generated = False # Flag to indicate if a letter has been generated
    if "formal_letter_content" not in st.session_state:
        st.session_state.formal_letter_content = None # Stores the generated letter content
    if "formal_letter_metadata" not in st.session_state:
        st.session_state.formal_letter_metadata = {} # Stores metadata like sender/recipient info
    if "formal_letter_form_data" not in st.session_state:
         st.session_state.formal_letter_form_data = {} # Stores the user's input from the form fields

    # Back button logic for subtypes. This button appears when a subtype is selected,
    # allowing the user to return to the subtype selection screen.
    if st.session_state.formal_letter_subtype is not None:
        if st.button("← Back to Formal Letter Types"):
            # Reset session state variables for this module to their initial state
            # This clears the current form data and generated letter.
            st.session_state.formal_letter_subtype = None
            st.session_state.formal_letter_generated = False
            st.session_state.formal_letter_content = None
            st.session_state.formal_letter_metadata = {}
            st.session_state.formal_letter_form_data = {}
            st.rerun() # Rerun the app to update the UI based on the changed state

    # Main navigation logic within the formal module.
    # If no subtype is selected, show the selection grid. Otherwise, show the form for the selected subtype.
    if st.session_state.formal_letter_subtype is None:
        # Display formal letter type selection if no subtype is selected
        display_formal_letter_types()
    else:
        # Display the interface form for the selected formal letter subtype
        display_formal_letter_form(st.session_state.formal_letter_subtype)


def display_formal_letter_types():
    """
    Displays the formal letter type selection interface using a grid of styled buttons.
    Each button represents a specific type of formal letter the user can choose to write.
    """

    st.markdown("## Select Formal Letter Type")

    # Define formal letter types with their details (ID, Name, Icon, Description, Color)
    # This list is used to generate the selection buttons.
    formal_letter_types = [
        {
            "id": "application",
            "name": "Application Letter",
            "icon": "📋",
            "description": "Apply for a job, program, or opportunity",
            "color": "#1976D2" # Blue
        },
        {
            "id": "complaint",
            "name": "Complaint Letter",
            "icon": "⚠️",
            "description": "Express dissatisfaction with a product or service",
            "color": "#D32F2F" # Red
        },
        {
            "id": "request",
            "name": "Request Letter",
            "icon": "🙋",
            "description": "Make a formal request for information or action",
            "color": "#388E3C" # Green
        },
        {
            "id": "recommendation",
            "name": "Recommendation Letter",
            "icon": "👍",
            "description": "Recommend someone for a position or opportunity",
            "color": "#7B1FA2" # Purple
        },
        {
            "id": "resignation",
            "name": "Resignation Letter",
            "icon": "🚪",
            "description": "Formally resign from a position",
            "color": "#455A64" # Blue Grey
        },
        {
            "id": "inquiry",
            "name": "Inquiry Letter",
            "icon": "❓",
            "description": "Request information about a product, service, or opportunity",
            "color": "#0097A7" # Teal
        },
        {
            "id": "authorization",
            "name": "Authorization Letter",
            "icon": "✅",
            "description": "Grant permission for someone to act on your behalf",
            "color": "#FF5722" # Deep Orange
        },
        {
            "id": "appeal",
            "name": "Appeal Letter",
            "icon": "🔄",
            "description": "Appeal a decision or request reconsideration",
            "color": "#FFA000" # Amber
        },
        {
            "id": "introduction",
            "name": "Introduction Letter",
            "icon": "🤝",
            "description": "Introduce yourself or your organization",
            "color": "#5D4037" # Brown
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
    for i, letter_type_config in enumerate(formal_letter_types):
        with cols[i % 3]: # Place buttons in columns, wrapping every 3
            # Use a unique key for each button based on its ID
            # The button label uses markdown and HTML for icon, name, and description
            if st.button(
                f"### {letter_type_config['icon']} {letter_type_config['name']}\n\n<p>{letter_type_config['description']}</p>",
                key=f"btn_formal_select_{letter_type_config['id']}", # Unique key for each button
                unsafe_allow_html=True # Allow markdown and HTML in the button label
            ):
                # When a button is clicked, update the session state to the selected subtype ID
                st.session_state.formal_letter_subtype = letter_type_config['id']
                # Clear previous data related to letter generation when selecting a new type
                st.session_state.formal_letter_generated = False
                st.session_state.formal_letter_content = None
                st.session_state.formal_letter_metadata = {}
                st.session_state.formal_letter_form_data = {} # Clear previous form data
                st.rerun() # Rerun the app to switch to the form for the selected subtype

    # Apply specific background colors to buttons using their keys and custom CSS
    # This requires injecting CSS after the buttons are rendered.
    # Note: This is a common Streamlit workaround for styling individual buttons dynamically.
    button_styles = ""
    for letter_type_config in formal_letter_types:
        button_styles += f"""
        div.stButton > button[data-testid="stButton"][kind="primary"][sf-key*="btn_formal_select_{letter_type_config['id']}"] {{
            background-color: {letter_type_config['color']};
        }}
         div.stButton > button[data-testid="stButton"][kind="primary"][sf-key*="btn_formal_select_{letter_type_config['id']}"]:hover {{
            background-color: {letter_type_config['color']}D9; /* Slightly darker on hover */
        }}
        """
    st.markdown(f"<style>{button_styles}</style>", unsafe_allow_html=True)


def display_formal_letter_form(subtype: str):
    """
    Displays the form for the selected formal letter subtype. This includes
    input fields specific to the subtype, contact information fields,
    tone and style options, and tabs for previewing and analyzing the generated letter.

    Args:
        subtype: The ID string of the selected formal letter subtype.
    """

    # Get the template for the selected subtype from the templates module.
    # This provides structural guidance and general advice for the LLM.
    template = get_template_by_type("formal", subtype)

    # Display the form title, icon, description, and guidance.
    st.markdown(f"## {get_icon_for_subtype(subtype)} {get_name_for_subtype(subtype)}")
    st.markdown(f"*{get_description_for_subtype(subtype)}*")
    st.info(f"**Guidance:** {template.get('guidance', 'No specific guidance available.')}")

    # Use a Streamlit form to group inputs. This helps manage state and
    # prevents the app from rerunning every time a single input widget changes,
    # improving performance for forms with many inputs.
    with st.form(key=f"formal_letter_form_{subtype}"):
        # Create tabs to organize the form sections.
        tab1, tab2, tab3 = st.tabs(["Letter Details", "Contact Information", "Preview & Export"])

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
                default_value = st.session_state.formal_letter_form_data.get(field["id"], "")

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
                     default_slider_value = st.session_state.formal_letter_form_data.get(field["id"], field.get("default", (field["min"] + field["max"]) / 2)) # Fallback to midpoint if no default specified
                     form_data[field["id"]] = st.slider(field["label"], field["min"], field["max"], default_slider_value, help=field.get("help", ""), key=f"{subtype}_{field['id']}")
                elif field["type"] == "number":
                    # Use the default value from session state or the field config's min value
                    default_number_value = st.session_state.formal_letter_form_data.get(field["id"], field.get("min", 0))
                    form_data[field["id"]] = st.number_input(field["label"], min_value=field.get("min", 0), value=default_number_value, help=field.get("help", ""), key=f"{subtype}_{field['id']}")


            # Section for selecting letter tone and style characteristics.
            st.markdown("### Tone and Style")
            col1, col2 = st.columns(2)

            with col1:
                # Slider for Formality Level, using session state default.
                formality_options = ["Standard Formal", "Very Formal", "Extremely Formal"]
                default_formality_level = st.session_state.formal_letter_form_data.get("formality_level", "Standard Formal")
                form_data["formality_level"] = st.select_slider(
                    "Formality Level",
                    options=formality_options,
                    value=default_formality_level,
                    help="Select the desired level of formality for your letter.",
                    key=f"{subtype}_formality_level"
                )

                # Selectbox for Tone, using subtype-specific tones and session state default.
                tone_options = get_tones_for_subtype(subtype)
                default_tone = st.session_state.formal_letter_form_data.get("tone", tone_options[0] if tone_options else "Professional")
                form_data["tone"] = st.selectbox(
                    "Tone",
                    tone_options,
                    index=tone_options.index(default_tone) if default_tone in tone_options else 0,
                    help="Select the overall tone for your letter.",
                    key=f"{subtype}_tone"
                )

            with col2:
                # Slider for Length, using session state default.
                length_options = ["Brief", "Standard", "Detailed"]
                default_length = st.session_state.formal_letter_form_data.get("length", "Standard")
                form_data["length"] = st.select_slider(
                    "Length",
                    options=length_options,
                    value=default_length,
                    help="Select the desired length of your letter.",
                    key=f"{subtype}_length"
                )

                # Slider for Language Complexity, using session state default.
                complexity_options = ["Simple", "Moderate", "Advanced"]
                default_language_complexity = st.session_state.formal_letter_form_data.get("language_complexity", "Moderate")
                form_data["language_complexity"] = st.select_slider(
                    "Language Complexity",
                    options=complexity_options,
                    value=default_language_complexity,
                    help="Select the complexity level of language used in the letter.",
                    key=f"{subtype}_language_complexity"
                )

            # Section for adding additional options like references.
            st.markdown("### Additional Options")

            # Checkbox and textarea for including references.
            default_include_references = st.session_state.formal_letter_form_data.get("include_references", True)
            include_references = st.checkbox("Include references to relevant documents, policies, or previous communications", value=default_include_references, help="Check to include specific references.", key=f"{subtype}_include_references")
            form_data["references"] = None # Initialize to None
            if include_references:
                default_references = st.session_state.formal_letter_form_data.get("references", "")
                form_data["references"] = st.text_area(
                    "References Details",
                    value=default_references,
                    height=100,
                    help="Mention any relevant documents, policies, or previous communications.",
                    placeholder="e.g., Regarding your email dated June 15, 2023, about the project timeline...",
                    key=f"{subtype}_references"
                )

            # Advanced options expander for legal/confidentiality notices.
            with st.expander("Advanced Options"):
                # Checkbox and textarea for including a legal disclaimer.
                default_include_legal_disclaimer = st.session_state.formal_letter_form_data.get("include_legal_disclaimer", False)
                include_legal_disclaimer = st.checkbox("Include legal disclaimer", value=default_include_legal_disclaimer, help="Add a legal disclaimer to your letter.", key=f"{subtype}_include_legal_disclaimer")
                form_data["legal_disclaimer"] = None # Initialize to None
                if include_legal_disclaimer:
                    default_legal_disclaimer = st.session_state.formal_letter_form_data.get("legal_disclaimer", "")
                    form_data["legal_disclaimer"] = st.text_area(
                        "Legal Disclaimer Text",
                        value=default_legal_disclaimer,
                        height=100,
                        help="Enter the text for the legal disclaimer.",
                        placeholder="e.g., This letter is without prejudice to any rights or remedies available to [Company Name]...",
                        key=f"{subtype}_legal_disclaimer"
                    )

                # Checkbox and textarea for including a confidentiality notice.
                default_include_confidentiality_notice = st.session_state.formal_letter_form_data.get("include_confidentiality_notice", False)
                include_confidentiality_notice = st.checkbox("Include confidentiality notice", value=default_include_confidentiality_notice, help="Add a confidentiality notice to your letter.", key=f"{subtype}_include_confidentiality_notice")
                form_data["confidentiality_notice"] = None # Initialize to None
                if include_confidentiality_notice:
                    default_confidentiality_notice = st.session_state.formal_letter_form_data.get("confidentiality_notice", "")
                    form_data["confidentiality_notice"] = st.text_area(
                        "Confidentiality Notice Text",
                        value=default_confidentiality_notice,
                        height=100,
                        help="Enter the text for the confidentiality notice.",
                        placeholder="e.g., The information contained in this letter is confidential and intended only for the recipient...",
                        key=f"{subtype}_confidentiality_notice"
                    )


        # --- Tab 2: Contact Information ---
        with tab2:
            # Section for sender and recipient contact information.
            col3, col4 = st.columns(2)

            with col3:
                st.markdown("### Sender Information")
                # Input fields for sender's contact details, populated from session state.
                form_data["sender_name"] = st.text_input("Your Full Name", value=st.session_state.formal_letter_form_data.get("sender_name", ""), help="Your full name as the sender.", key=f"{subtype}_sender_name")
                form_data["sender_title"] = st.text_input("Your Title/Position", value=st.session_state.formal_letter_form_data.get("sender_title", ""), help="Your job title or position.", key=f"{subtype}_sender_title")
                form_data["sender_organization"] = st.text_input("Your Organization/Company (Optional)", value=st.session_state.formal_letter_form_data.get("sender_organization", ""), help="The name of your organization or company, if applicable.", key=f"{subtype}_sender_organization")
                form_data["sender_address"] = st.text_area("Your Address", value=st.session_state.formal_letter_form_data.get("sender_address", ""), height=100, help="Your full mailing address.", key=f"{subtype}_sender_address")
                form_data["sender_phone"] = st.text_input("Your Phone Number (Optional)", value=st.session_state.formal_letter_form_data.get("sender_phone", ""), help="Your contact phone number.", key=f"{subtype}_sender_phone")
                form_data["sender_email"] = st.text_input("Your Email Address (Optional)", value=st.session_state.formal_letter_form_data.get("sender_email", ""), help="Your contact email address.", key=f"{subtype}_sender_email")

            with col4:
                st.markdown("### Recipient Information")
                # Input fields for recipient's contact details, populated from session state.
                form_data["recipient_name"] = st.text_input("Recipient's Full Name", value=st.session_state.formal_letter_form_data.get("recipient_name", ""), help="The full name of the recipient (if known).", key=f"{subtype}_recipient_name")
                form_data["recipient_title"] = st.text_input("Recipient's Title/Position (Optional)", value=st.session_state.formal_letter_form_data.get("recipient_title", ""), help="The recipient's job title or position (if known).", key=f"{subtype}_recipient_title")
                form_data["recipient_organization"] = st.text_input("Recipient's Organization/Company", value=st.session_state.formal_letter_form_data.get("recipient_organization", ""), help="The name of the recipient's organization or company.", key=f"{subtype}_recipient_organization")
                form_data["recipient_address"] = st.text_area("Recipient's Address", value=st.session_state.formal_letter_form_data.get("recipient_address", ""), height=100, help="The recipient's full mailing address.", key=f"{subtype}_recipient_address")

                # Optional recipient contact information in an expander.
                with st.expander("Additional Recipient Information (Optional)"):
                    form_data["recipient_phone"] = st.text_input("Recipient's Phone Number (Optional)", value=st.session_state.formal_letter_form_data.get("recipient_phone", ""), help="Recipient's contact phone number.", key=f"{subtype}_recipient_phone")
                    form_data["recipient_email"] = st.text_input("Recipient's Email Address (Optional)", value=st.session_state.formal_letter_form_data.get("recipient_email", ""), help="Recipient's contact email address.", key=f"{subtype}_recipient_email")

            # Section for letter formatting options.
            st.markdown("### Letter Format")
            format_options = ["Full Block", "Modified Block", "Semi-Block"]
            default_letter_format = st.session_state.formal_letter_form_data.get("letter_format", "Full Block")
            form_data["letter_format"] = st.selectbox(
                "Format Style",
                format_options,
                index=format_options.index(default_letter_format) if default_letter_format in format_options else 0,
                help="Select the standard formal letter format style.",
                key=f"{subtype}_letter_format"
            )

            default_include_subject_line = st.session_state.formal_letter_form_data.get("include_subject_line", True)
            include_subject_line = st.checkbox("Include subject line", value=default_include_subject_line, help="Include a clear subject line.", key=f"{subtype}_include_subject_line")
            form_data["subject_line"] = None # Initialize to None
            if include_subject_line:
                default_subject_line = st.session_state.formal_letter_form_data.get("subject_line", "")
                form_data["subject_line"] = st.text_input(
                    "Subject Line Text",
                    value=default_subject_line,
                    help="Enter the text for the subject line.",
                    placeholder="e.g., Application for Marketing Manager Position (Ref: JOB-2023-45)",
                    key=f"{subtype}_subject_line"
                )

            default_include_reference_number = st.session_state.formal_letter_form_data.get("include_reference_number", False)
            include_reference_number = st.checkbox("Include reference number", value=default_include_reference_number, help="Include a reference number for tracking.", key=f"{subtype}_include_reference_number")
            form_data["reference_number"] = None # Initialize to None
            if include_reference_number:
                default_reference_number = st.session_state.formal_letter_form_data.get("reference_number", "")
                form_data["reference_number"] = st.text_input(
                    "Reference Number Text",
                    value=default_reference_number,
                    help="Enter the reference number.",
                    placeholder="e.g., REF-2023-123",
                    key=f"{subtype}_reference_number"
                )

        # --- Tab 3: Preview & Export ---
        with tab3:
            # Instructions for the user before generation.
            if not st.session_state.formal_letter_generated:
                st.info("Complete the letter details and click 'Generate Letter' to preview your letter.")

            # The Generate button is placed inside the form. Clicking it submits the form
            # and triggers the code block below it to run.
            generate_button = st.form_submit_button("Generate Letter", type="primary")

            if generate_button:
                # Action to perform when the form is submitted via the Generate button.

                # Store the current state of all form inputs in session state.
                # This allows retaining user inputs even after generation or regeneration.
                st.session_state.formal_letter_form_data = form_data.copy()

                # Prepare metadata specifically for the formatter and analysis functions.
                # This includes structured contact info, dates, subject, etc.
                metadata = {
                    "sender_name": form_data.get("sender_name", ""),
                    "sender_title": form_data.get("sender_title", ""),
                    "sender_organization": form_data.get("sender_organization", ""),
                    "sender_address": form_data.get("sender_address", ""),
                    "sender_phone": form_data.get("sender_phone", ""),
                    "sender_email": form_data.get("sender_email", ""),
                    "recipient_name": form_data.get("recipient_name", ""),
                    "recipient_title": form_data.get("recipient_title", ""),
                    "recipient_organization": form_data.get("recipient_organization", ""),
                    "recipient_address": form_data.get("recipient_address", ""),
                    "recipient_phone": form_data.get("recipient_phone", ""),
                    "recipient_email": form_data.get("recipient_email", ""),
                    "date": datetime.datetime.now().strftime("%B %d, %Y"), # Use current date for the letter
                    "letter_format": form_data.get("letter_format", "Full Block"),
                    "subject": form_data.get('subject_line') if form_data.get('include_subject_line') else "", # Include subject in metadata for formatter
                    "reference_number": form_data.get('reference_number') if form_data.get('include_reference_number') else "", # Include reference in metadata
                }
                 # Determine salutation based on recipient name/title preference
                recipient_display_name = metadata.get("recipient_name")
                recipient_display_title = metadata.get("recipient_title")
                if recipient_display_name and recipient_display_title:
                     metadata["salutation"] = f"Dear {recipient_display_title} {recipient_display_name}:"
                elif recipient_display_name:
                     metadata["salutation"] = f"Dear {recipient_display_name}:"
                else:
                     metadata["salutation"] = "Dear Sir/Madam:" # Fallback salutation

                # Determine complimentary close based on formality
                metadata["complimentary_close"] = "Sincerely," # Standard formal close


                st.session_state.formal_letter_metadata = metadata.copy()


                # --- Letter Generation Logic ---
                # Check for minimal required fields before attempting generation.
                if not form_data.get("sender_name") or not form_data.get("recipient_name") or not form_data.get("recipient_organization"):
                    st.error("Please provide at least your name, the recipient's name, and the recipient's organization.")
                else:
                    # Display a spinner while the AI generates the letter.
                    with st.spinner("Generating your formal letter..."):
                        # Combine all necessary data into a single dictionary for the generation function.
                        # This includes both form data and metadata.
                        # Note: formality_level, tone, length, language_complexity are already in form_data
                        generation_data = {
                            "subtype": subtype,
                            **form_data, # Includes all collected form inputs
                            **metadata # Includes structured sender/recipient/date/format info
                        }

                        # Call the letter generation function with the combined data.
                        letter_content = generate_formal_letter(generation_data)

                        # Store the generated letter content and update the generated flag.
                        st.session_state.formal_letter_content = letter_content
                        st.session_state.formal_letter_generated = True

                        # Rerun the app to exit the form block and display the generated letter section.
                        # This rerun happens automatically on form submission, but explicit state updates
                        # ensure the display logic reacts correctly.
                        # st.rerun() # Rerun is handled by form submission

        # --- Display Generated Letter and Analysis ---
        # This block executes if a letter has been generated and stored in session state.
        if st.session_state.formal_letter_generated and st.session_state.formal_letter_content is not None:
            letter_content = st.session_state.formal_letter_content
            metadata = st.session_state.formal_letter_metadata

            # Create tabs for different views of the generated letter.
            preview_tab1, preview_tab2, preview_tab3 = st.tabs(["Formatted Preview", "Plain Text", "Analysis"])

            with preview_tab1:
                st.markdown("### Letter Preview")
                # Generate and display the HTML preview of the letter using the formatter utility.
                # Pass letter_type="formal" to the formatter.
                html_preview = get_letter_preview_html(letter_content, metadata, letter_type="formal")
                st.markdown(html_preview, unsafe_allow_html=True)

                # Download button for the plain text version of the letter.
                file_name_suffix = metadata.get('recipient_organization', 'formal').replace(' ', '_').lower()
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
                improvement_suggestions = suggest_improvements(letter_content, "formal") # Pass "formal" as letter_type

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
                st.session_state.formal_letter_generated = False
                st.session_state.formal_letter_content = None # Clear generated content
                # st.session_state.formal_letter_form_data is already populated from the form submit
                st.rerun() # Rerun to show the form with previous inputs


def generate_formal_letter(data: Dict[str, Any]) -> str:
    """
    Generates a formal letter using the LLM by constructing a detailed prompt
    based on the collected user inputs and metadata.

    Args:
        data: A dictionary containing all collected user inputs and metadata
              (from the form and session state).

    Returns:
        The generated letter content as a string, or an error message if generation fails.
    """

    # Extract key generation parameters from the data dictionary.
    subtype = data.get("subtype", "default")
    formality_level = data.get("formality_level", "Standard Formal")
    tone = data.get("tone", "Professional")
    length = data.get("length", "Standard")
    language_complexity = data.get("language_complexity", "Moderate")

    # Get template guidance and structure to include in the prompt.
    template = get_template_by_type("formal", subtype)
    template_guidance = template.get("guidance", "Follow standard formal letter practices.")
    template_structure = template.get("structure", ["Sender Info", "Date", "Recipient Info", "Subject", "Salutation", "Body", "Closing", "Signature"])


    # Build the prompt string step-by-step, including all relevant details
    # from the user's input and selected options.
    prompt_parts = [
        f"Write a {length.lower()}, {formality_level.lower()} {get_name_for_subtype(subtype)} letter with a {tone.lower()} tone using {language_complexity.lower()} language complexity.",
        f"Purpose: {get_description_for_subtype(subtype)}",
        f"Recipient: {data.get('recipient_name', '')}, {data.get('recipient_title', '')} at {data.get('recipient_organization', '')}",
        f"Sender: {data.get('sender_name', '')}, {data.get('sender_title', '')} at {data.get('sender_organization', '')}",
        f"Date: {data.get('date', '')}",
        f"Desired Format Style: {data.get('letter_format', 'Full Block')}",
    ]

    # Add subject line if provided
    if data.get('include_subject_line') and data.get('subject_line'):
        prompt_parts.append(f"Subject: {data['subject_line']}")

    # Add reference number if provided
    if data.get('include_reference_number') and data.get('reference_number'):
        prompt_parts.append(f"Reference Number: {data['reference_number']}")


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


    # Add additional options if included.
    if data.get('include_references') and data.get('references'):
        prompt_parts.append(f"Include references: {data['references']}")

    if data.get('include_legal_disclaimer') and data.get('legal_disclaimer'):
        prompt_parts.append(f"Include legal disclaimer: {data['legal_disclaimer']}")

    if data.get('include_confidentiality_notice') and data.get('confidentiality_notice'):
        prompt_parts.append(f"Include confidentiality notice: {data['confidentiality_notice']}")

    # Add the template structure and overall guidance to the prompt.
    # This helps the LLM understand the desired layout and writing style.
    prompt_parts.append("\nFollow this general structure:")
    for i, section in enumerate(template_structure):
        prompt_parts.append(f"{i+1}. {section}")
    prompt_parts.append(f"\nOverall Writing Guidance: {template_guidance}")

    # Add final instructions for the LLM.
    prompt_parts.append("\nMake the letter professional, clear, and appropriate for the formal context.")


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
    """Maps a formal letter subtype ID to a relevant emoji icon."""
    icons = {
        "application": "📋",
        "complaint": "⚠️",
        "request": "🙋",
        "recommendation": "👍",
        "resignation": "🚪",
        "inquiry": "❓",
        "authorization": "✅",
        "appeal": "🔄",
        "introduction": "🤝"
    }
    return icons.get(subtype, "📝") # Default icon

def get_name_for_subtype(subtype: str) -> str:
    """Maps a formal letter subtype ID to its display name."""
    names = {
        "application": "Application Letter",
        "complaint": "Complaint Letter",
        "request": "Request Letter",
        "recommendation": "Recommendation Letter",
        "resignation": "Resignation Letter",
        "inquiry": "Inquiry Letter",
        "authorization": "Authorization Letter",
        "appeal": "Appeal Letter",
        "introduction": "Introduction Letter"
    }
    return names.get(subtype, "Formal Letter") # Default name

def get_description_for_subtype(subtype: str) -> str:
    """Maps a formal letter subtype ID to a brief description."""
    descriptions = {
        "application": "Apply for a job, program, or opportunity with a professional application letter.",
        "complaint": "Express dissatisfaction with a product or service in a formal and effective manner.",
        "request": "Make a formal request for information, assistance, or action.",
        "recommendation": "Recommend someone for a position or opportunity with a professional endorsement.",
        "resignation": "Formally resign from a position while maintaining professional relationships.",
        "inquiry": "Request information about a product, service, or opportunity in a formal manner.",
        "authorization": "Grant permission for someone to act on your behalf with a formal authorization.",
        "appeal": "Appeal a decision or request reconsideration with a persuasive formal letter.",
        "introduction": "Introduce yourself or your organization with a professional introduction letter."
    }
    return descriptions.get(subtype, "Create a formal letter for your specific needs.") # Default description

def get_fields_for_subtype(subtype: str) -> List[Dict[str, Any]]:
    """
    Provides a list of input field configurations specific to each formal letter subtype.
    Each dictionary in the list defines a form input field, including its ID, label,
    type, and optional properties like help text, options (for select/slider),
    min/max values (for slider/number), and a default value.
    """

    # Define subtype-specific fields.
    if subtype == "application":
        return [
            {
                "id": "position",
                "label": "Position/Opportunity",
                "type": "text",
                "help": "What specific position, program, or opportunity are you applying for?"
            },
            {
                "id": "source",
                "label": "Where You Found the Opportunity (Optional)",
                "type": "text",
                "help": "Where did you learn about this opportunity? (e.g., company website, job board, referral)"
            },
            {
                "id": "qualifications",
                "label": "Key Qualifications",
                "type": "textarea",
                "help": "List your key qualifications and skills that match the requirements of this position."
            },
            {
                "id": "experience",
                "label": "Relevant Experience",
                "type": "textarea",
                "help": "Describe your relevant work experience, projects, or academic background."
            }
        ]
    elif subtype == "complaint":
        return [
            {
                "id": "product_service",
                "label": "Product or Service Involved",
                "type": "text",
                "help": "What product or service is the subject of your complaint?"
            },
            {
                "id": "date_of_incident",
                "label": "Date of Purchase or Incident",
                "type": "date", # Using date type for date input
                "help": "When did you purchase the product or when did the incident occur?"
            },
            {
                "id": "order_reference",
                "label": "Order/Reference Number (Optional)",
                "type": "text",
                "help": "Include any relevant order numbers, account numbers, or reference IDs."
            },
            {
                "id": "complaint_nature",
                "label": "Nature of Complaint",
                "type": "textarea",
                "help": "Describe the issue clearly, factually, and in detail. Include specific dates, times, and names if applicable."
            },
            {
                "id": "desired_resolution",
                "label": "Desired Resolution",
                "type": "textarea",
                "help": "Clearly state what outcome you are seeking to resolve this complaint (e.g., full refund, replacement, repair, specific action)."
            }
        ]
    elif subtype == "request":
        return [
            {
                "id": "request_type",
                "label": "Type of Request",
                "type": "text",
                "help": "What type of formal request are you making? (e.g., Request for Information, Request for Meeting, Request for Document)"
            },
            {
                "id": "request_details",
                "label": "Specific Request Details",
                "type": "textarea",
                "help": "Provide all necessary details about what you are requesting."
            },
            {
                "id": "request_reason",
                "label": "Reason or Justification for Request",
                "type": "textarea",
                "help": "Clearly explain why you are making this request and its importance."
            },
            {
                "id": "deadline",
                "label": "Deadline for Response/Action (if applicable)",
                "type": "date", # Using date type for date input
                "help": "Is there a specific date by which you need a response or action?"
            }
        ]
    elif subtype == "recommendation":
        return [
            {
                "id": "recommendee",
                "label": "Person Being Recommended (Full Name)",
                "type": "text",
                "help": "Enter the full name of the person you are recommending."
            },
            {
                "id": "position",
                "label": "Position/Opportunity Being Recommended For",
                "type": "text",
                "help": "What specific position, program, or opportunity are you recommending them for?"
            },
            {
                "id": "relationship",
                "label": "Your Relationship to the Recommendee",
                "type": "text",
                "help": "Describe your professional or academic relationship (e.g., former manager, professor, colleague)."
            },
            {
                "id": "relationship_duration",
                "label": "Duration of Relationship",
                "type": "text",
                "help": "How long have you known the person in this capacity? (e.g., 3 years, from 2018 to 2022)"
            },
            {
                "id": "strengths",
                "label": "Key Strengths and Qualities",
                "type": "textarea",
                "help": "Highlight the most relevant strengths and qualities of the person being recommended."
            },
            {
                "id": "achievements",
                "label": "Specific Achievements or Contributions",
                "type": "textarea",
                "help": "Provide concrete examples of their achievements, contributions, or performance."
            }
        ]
    elif subtype == "resignation":
        return [
            {
                "id": "current_position",
                "label": "Your Current Position",
                "type": "text",
                "help": "What is your current job title?"
            },
            {
                "id": "last_day",
                "label": "Your Last Working Day",
                "type": "date", # Using date type for date input
                "help": "Specify your intended last day of employment."
            },
            {
                "id": "resignation_reason",
                "label": "Reason for Resignation (Optional)",
                "type": "textarea",
                "help": "You may choose to provide a brief, professional reason for leaving (e.g., pursuing a new opportunity, personal reasons)."
            },
            {
                "id": "transition_plan",
                "label": "Offer of Assistance with Transition (Optional)",
                "type": "textarea",
                "help": "Offer to assist with the transition of your responsibilities."
            },
             {
                "id": "gratitude",
                "label": "Express Gratitude (Optional)",
                "type": "textarea",
                "help": "Express thanks for the opportunity and experience gained."
            }
        ]
    elif subtype == "inquiry":
        return [
            {
                "id": "inquiry_subject",
                "label": "Inquiry Subject",
                "type": "text",
                "help": "What is the main subject of your inquiry?"
            },
            {
                "id": "background_info",
                "label": "Relevant Background Information (Optional)",
                "type": "textarea",
                "help": "Provide any necessary context for your inquiry."
            },
            {
                "id": "specific_questions",
                "label": "Specific Questions",
                "type": "textarea",
                "help": "List your questions clearly and concisely, perhaps using bullet points."
            },
            {
                "id": "response_deadline",
                "label": "Deadline for Response (if applicable)",
                "type": "date", # Using date type for date input
                "help": "By when do you need the information?"
            }
        ]
    elif subtype == "authorization":
        return [
            {
                "id": "authorized_person",
                "label": "Person Being Authorized (Full Name)",
                "type": "text",
                "help": "Enter the full name of the person you are authorizing."
            },
            {
                "id": "authorized_person_id",
                "label": "Authorized Person's Identification (Optional)",
                "type": "text",
                "help": "Include any identification details if necessary (e.g., ID number, employee ID)."
            },
            {
                "id": "authorization_purpose",
                "label": "Purpose and Scope of Authorization",
                "type": "textarea",
                "help": "Clearly and precisely state what you are authorizing them to do on your behalf."
            },
            {
                "id": "authorization_duration",
                "label": "Duration of Authorization",
                "type": "text", # Using text for flexibility (e.g., "from date to date", "until revoked")
                "help": "Specify how long this authorization is valid (e.g., 'from [Start Date] to [End Date]', 'until revoked in writing')."
            },
            {
                "id": "authorization_limitations",
                "label": "Limitations or Restrictions (Optional)",
                "type": "textarea",
                "help": "Specify any limitations or restrictions on the authorized person's actions."
            }
        ]
    elif subtype == "appeal":
        return [
            {
                "id": "appealed_decision",
                "label": "Decision Being Appealed",
                "type": "text",
                "help": "Clearly identify the specific decision you are appealing."
            },
            {
                "id": "decision_date",
                "label": "Date of Original Decision",
                "type": "date", # Using date type for date input
                "help": "When was the original decision made?"
            },
            {
                "id": "appeal_grounds",
                "label": "Grounds for Appeal",
                "type": "textarea",
                "help": "Explain the specific reasons or arguments why you believe the decision should be overturned or reconsidered. Reference relevant policies or facts."
            },
            {
                "id": "supporting_evidence",
                "label": "Supporting Evidence (Optional)",
                "type": "textarea",
                "help": "Mention any supporting documents or evidence you are providing."
            },
            {
                "id": "requested_outcome",
                "label": "Requested Outcome",
                "type": "textarea",
                "help": "Clearly state what resolution you are seeking from this appeal."
            }
        ]
    elif subtype == "introduction":
        return [
            {
                "id": "introduction_purpose",
                "label": "Purpose of Introduction",
                "type": "text",
                "help": "Why are you introducing yourself or your organization to this recipient?"
            },
            {
                "id": "key_information",
                "label": "Key Information About Yourself/Organization",
                "type": "textarea",
                "help": "Highlight relevant background, expertise, or services."
            },
            {
                "id": "collaboration_areas",
                "label": "Potential Areas of Collaboration or Mutual Interest (Optional)",
                "type": "textarea",
                "help": "Suggest ways you could potentially collaborate or areas of shared interest."
            },
            {
                "id": "call_to_action",
                "label": "Call to Action",
                "type": "textarea",
                "help": "What specific action would you like the recipient to take after reading your introduction? (e.g., schedule a meeting, visit website)"
            }
        ]

    # Default fields if subtype is not recognized or no specific fields are defined.
    # This provides a basic textarea for general content.
    return [
        {
            "id": "main_content",
            "label": "Main Content",
            "type": "textarea",
            "help": "Enter the main content you want to include in your formal letter."
        }
    ]

def get_tones_for_subtype(subtype: str) -> List[str]:
    """Maps a formal letter subtype ID to a list of suggested tones."""
    tones = {
        "application": ["Professional", "Confident", "Enthusiastic", "Respectful", "Formal"],
        "complaint": ["Firm", "Respectful", "Direct", "Objective", "Assertive"],
        "request": ["Polite", "Clear", "Respectful", "Direct", "Appreciative"],
        "recommendation": ["Supportive", "Positive", "Professional", "Enthusiastic", "Confident"],
        "resignation": ["Professional", "Appreciative", "Respectful", "Positive", "Formal"],
        "inquiry": ["Curious", "Professional", "Respectful", "Clear", "Formal"],
        "authorization": ["Clear", "Precise", "Formal", "Direct", "Authoritative"],
        "appeal": ["Persuasive", "Respectful", "Objective", "Confident", "Diplomatic"],
        "introduction": ["Friendly", "Professional", "Enthusiastic", "Informative", "Engaging"]
    }
    # Return the list of tones for the subtype, or a default list if not found.
    return tones.get(subtype, ["Professional", "Formal", "Respectful", "Clear", "Direct"])

# Example of how to run the app (for local development using `streamlit run your_script_name.py`)
# Uncomment the lines below to make this script directly executable.
# if __name__ == "__main__":
#     write_letter()
