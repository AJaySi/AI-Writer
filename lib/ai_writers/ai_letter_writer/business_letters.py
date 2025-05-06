"""
Business Letters Module

This module provides a Streamlit interface for generating various types of business letters
using AI assistance. It collects user inputs specific to the chosen business letter subtype,
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
    """Placeholder: Generates a basic HTML preview for business letters."""
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
    return {"professional": 0.9, "persuasive": 0.75, "confident": 0.8}

def check_formality(content: str) -> float:
    """Placeholder: Returns a dummy formality score (0.0 to 1.0)."""
    return 0.85 # Example: 85% formal

def get_readability_metrics(content: str) -> Dict[str, Any]:
    """Placeholder: Returns dummy readability metrics."""
    word_count = len(content.split())
    # Estimate reading time in seconds (assuming ~200 words per minute)
    reading_time_seconds = round((word_count / 200) * 60)
    return {
        "word_count": word_count,
        "sentence_count": max(1, content.count('. ') + content.count('! ') + content.count('? ')), # Simple sentence count
        "avg_words_per_sentence": round(word_count / max(1, content.count('. ') + content.count('! ') + content.count('? ')), 2),
        "flesch_reading_ease": 50.0, # Dummy score for business letters
        "reading_level": "Fairly Difficult", # Dummy level
        "reading_time_seconds": reading_time_seconds # Added reading time
    }

def suggest_improvements(content: str, letter_type: str) -> List[str]:
    """Placeholder: Returns dummy improvement suggestions."""
    if "jargon" in content.lower():
        return ["Suggestion: Avoid excessive jargon unless appropriate for the recipient."]
    elif "passive voice" in content.lower():
         return ["Suggestion: Consider using more active voice for clarity and impact."]
    else:
        return ["Suggestion: Ensure your call to action is clear and prominent."]

def get_template_by_type(letter_type: str, subtype: str = "default") -> Dict[str, Any]:
    """Placeholder: Returns a generic template."""
    # This should ideally come from the actual letter_templates module
    return {"structure": ["Introduction", "Body", "Call to Action", "Closing"], "guidance": "Follow standard business letter practices."}

def llm_text_gen(prompt: str) -> str:
    """Placeholder: Simulates LLM text generation."""
    # In a real app, this would call the actual LLM API
    st.info(f"LLM Prompt:\n```\n{prompt}\n```") # Display prompt for debugging
    # Return a dummy generated letter based on the prompt
    return f"Subject: Generated Business Letter Preview\n\nDear [Generated Recipient Name],\n\nThis is a sample business letter generated based on the following details:\n\n{prompt}\n\n[Generated content based on the prompt would go here, following the requested structure, tone, persuasion level, length, and formality.]\n\nSincerely,\n[Generated Your Name]"

# --- End Placeholder Functions ---


def write_letter():
    """
    Main function for the Business Letters interface. Sets up the Streamlit page
    and handles navigation between subtype selection and the letter form.
    """

    # Page title and description
    st.title("💼 Business Letter Writer")
    st.markdown("""
    Create professional business letters for various purposes. Select a letter type below to get started.
    """)

    # Initialize Streamlit session state variables specific to the business module.
    # These variables persist across reruns and store the user's progress and data.
    if "business_letter_subtype" not in st.session_state:
        st.session_state.business_letter_subtype = None # Stores the ID of the selected business letter type
    if "business_letter_generated" not in st.session_state:
        st.session_state.business_letter_generated = False # Flag to indicate if a letter has been generated
    if "business_letter_content" not in st.session_state:
        st.session_state.business_letter_content = None # Stores the generated letter content
    if "business_letter_metadata" not in st.session_state:
        st.session_state.business_letter_metadata = {} # Stores metadata like sender/recipient info
    if "business_letter_form_data" not in st.session_state:
         st.session_state.business_letter_form_data = {} # Stores the user's input from the form fields

    # Back button logic for subtypes. This button appears when a subtype is selected,
    # allowing the user to return to the subtype selection screen.
    if st.session_state.business_letter_subtype is not None:
        if st.button("← Back to Business Letter Types"):
            # Reset session state variables for this module to their initial state
            # This clears the current form data and generated letter.
            st.session_state.business_letter_subtype = None
            st.session_state.business_letter_generated = False
            st.session_state.business_letter_content = None
            st.session_state.business_letter_metadata = {}
            st.session_state.business_letter_form_data = {}
            st.rerun() # Rerun the app to update the UI based on the changed state

    # Main navigation logic within the business module.
    # If no subtype is selected, show the selection grid. Otherwise, show the form for the selected subtype.
    if st.session_state.business_letter_subtype is None:
        # Display business letter type selection if no subtype is selected
        display_business_letter_types()
    else:
        # Display the interface form for the selected business letter subtype
        display_business_letter_form(st.session_state.business_letter_subtype)


def display_business_letter_types():
    """
    Displays the business letter type selection interface using a grid of styled buttons.
    Each button represents a specific type of business letter the user can choose to write.
    """

    st.markdown("## Select Business Letter Type")

    # Define business letter types with their details (ID, Name, Icon, Description, Color)
    # This list is used to generate the selection buttons.
    business_letter_types = [
        {
            "id": "sales",
            "name": "Sales Letter",
            "icon": "💰",
            "description": "Promote products or services to potential customers",
            "color": "#4CAF50" # Green
        },
        {
            "id": "proposal",
            "name": "Business Proposal",
            "icon": "📊",
            "description": "Present a business idea or solution",
            "color": "#2196F3" # Blue
        },
        {
            "id": "order",
            "name": "Order Letter",
            "icon": "🛒",
            "description": "Place an order for products or services",
            "color": "#FF9800" # Orange
        },
        {
            "id": "quotation",
            "name": "Quotation Letter",
            "icon": "💲",
            "description": "Provide pricing information for products or services",
            "color": "#9C27B0" # Purple
        },
        {
            "id": "acknowledgment",
            "name": "Acknowledgment Letter",
            "icon": "✅",
            "description": "Confirm receipt of payment, order, or documents",
            "color": "#607D8B" # Blue Grey
        },
        {
            "id": "collection",
            "name": "Collection Letter",
            "icon": "💵",
            "description": "Request payment for overdue accounts",
            "color": "#F44336" # Red
        },
        {
            "id": "adjustment",
            "name": "Adjustment Letter",
            "icon": "🔧",
            "description": "Respond to customer complaints or requests",
            "color": "#795548" # Brown
        },
        {
            "id": "credit",
            "name": "Credit Letter",
            "icon": "💳",
            "description": "Extend credit to customers or respond to credit requests",
            "color": "#009688" # Teal
        },
        {
            "id": "follow_up",
            "name": "Follow-up Letter",
            "icon": "🔄",
            "description": "Follow up on previous communication or meetings",
            "color": "#673AB7" # Deep Purple
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
    for i, letter_type_config in enumerate(business_letter_types):
        with cols[i % 3]: # Place buttons in columns, wrapping every 3
            # Use a unique key for each button based on its ID
            # The button label uses markdown and HTML for icon, name, and description
            if st.button(
                f"### {letter_type_config['icon']} {letter_type_config['name']}\n\n<p>{letter_type_config['description']}</p>",
                key=f"btn_business_select_{letter_type_config['id']}", # Unique key for each button
                unsafe_allow_html=True # Allow markdown and HTML in the button label
            ):
                # When a button is clicked, update the session state to the selected subtype ID
                st.session_state.business_letter_subtype = letter_type_config['id']
                # Clear previous data related to letter generation when selecting a new type
                st.session_state.business_letter_generated = False
                st.session_state.business_letter_content = None
                st.session_state.business_letter_metadata = {}
                st.session_state.business_letter_form_data = {} # Clear previous form data
                st.rerun() # Rerun the app to switch to the form for the selected subtype

    # Apply specific background colors to buttons using their keys and custom CSS
    # This requires injecting CSS after the buttons are rendered.
    # Note: This is a common Streamlit workaround for styling individual buttons dynamically.
    button_styles = ""
    for letter_type_config in business_letter_types:
        button_styles += f"""
        div.stButton > button[data-testid="stButton"][kind="primary"][sf-key*="btn_business_select_{letter_type_config['id']}"] {{
            background-color: {letter_type_config['color']};
        }}
        div.stButton > button[data-testid="stButton"][kind="primary"][sf-key*="btn_business_select_{letter_type_config['id']}"]:hover {{
            background-color: {letter_type_config['color']}D9; /* Slightly darker on hover */
        }}
        """
    st.markdown(f"<style>{button_styles}</style>", unsafe_allow_html=True)


def display_business_letter_form(subtype: str):
    """
    Displays the form for the selected business letter subtype. This includes
    input fields specific to the subtype, general business information fields,
    tone and style options, and tabs for previewing and analyzing the generated letter.

    Args:
        subtype: The ID string of the selected business letter subtype.
    """

    # Get the template for the selected subtype from the templates module.
    # This provides structural guidance and general advice for the LLM.
    template = get_template_by_type("business", subtype)

    # Display the form title, icon, description, and guidance.
    st.markdown(f"## {get_icon_for_subtype(subtype)} {get_name_for_subtype(subtype)}")
    st.markdown(f"*{get_description_for_subtype(subtype)}*")
    st.info(f"**Guidance:** {template.get('guidance', 'No specific guidance available.')}")


    # Use a Streamlit form to group inputs. This helps manage state and
    # prevents the app from rerunning every time a single input widget changes,
    # improving performance for forms with many inputs.
    with st.form(key=f"business_letter_form_{subtype}"):
        # Create tabs to organize the form sections.
        tab1, tab2, tab3 = st.tabs(["Letter Details", "Business Information", "Preview & Export"])

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
                default_value = st.session_state.business_letter_form_data.get(field["id"], "")

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
                     default_slider_value = st.session_state.business_letter_form_data.get(field["id"], field.get("default", (field["min"] + field["max"]) / 2)) # Fallback to midpoint if no default specified
                     form_data[field["id"]] = st.slider(field["label"], field["min"], field["max"], default_slider_value, help=field.get("help", ""), key=f"{subtype}_{field['id']}")
                elif field["type"] == "number":
                    # Use the default value from session state or the field config's min value
                    default_number_value = st.session_state.business_letter_form_data.get(field["id"], field.get("min", 0))
                    form_data[field["id"]] = st.number_input(field["label"], min_value=field.get("min", 0), value=default_number_value, help=field.get("help", ""), key=f"{subtype}_{field['id']}")


            # Section for selecting letter tone and style characteristics.
            st.markdown("### Tone and Style")
            col1, col2 = st.columns(2)

            with col1:
                # Selectbox for Tone, using subtype-specific tones and session state default.
                tone_options = get_tones_for_subtype(subtype)
                default_tone = st.session_state.business_letter_form_data.get("tone", tone_options[0] if tone_options else "Professional")
                form_data["tone"] = st.selectbox(
                    "Tone",
                    tone_options,
                    index=tone_options.index(default_tone) if default_tone in tone_options else 0, # Set index based on default value
                    help="Select the overall tone for your letter (e.g., Friendly, Formal, Assertive).",
                    key=f"{subtype}_tone"
                )

                # Slider for Persuasion Level, using session state default.
                persuasion_options = ["Subtle", "Moderate", "Strong"]
                default_persuasion = st.session_state.business_letter_form_data.get("persuasion_level", "Moderate")
                form_data["persuasion_level"] = st.select_slider(
                    "Persuasion Level",
                    options=persuasion_options,
                    value=default_persuasion,
                    help="Select how persuasive you want your letter to be.",
                    key=f"{subtype}_persuasion"
                )

            with col2:
                # Slider for Length, using session state default.
                length_options = ["Brief", "Standard", "Detailed"]
                default_length = st.session_state.business_letter_form_data.get("length", "Standard")
                form_data["length"] = st.select_slider(
                    "Length",
                    options=length_options,
                    value=default_length,
                    help="Select the desired length of your letter.",
                    key=f"{subtype}_length"
                )

                # Slider for Formality, using session state default.
                formality_options = ["Conversational", "Professional", "Formal"]
                default_formality = st.session_state.business_letter_form_data.get("formality", "Professional")
                form_data["formality"] = st.select_slider(
                    "Formality",
                    options=formality_options,
                    value=default_formality,
                    help="Select the formality level of your letter.",
                    key=f"{subtype}_formality"
                )

            # Section for defining a Call to Action.
            st.markdown("### Call to Action")
            default_include_cta = st.session_state.business_letter_form_data.get("include_cta", True)
            include_cta = st.checkbox("Include a call to action", value=default_include_cta, help="Check to include a clear call to action in your letter.", key=f"{subtype}_include_cta")

            cta_type = None
            custom_cta = None
            form_data["cta_type"] = None # Initialize to None
            form_data["custom_cta"] = None # Initialize to None
            if include_cta:
                default_cta_type = st.session_state.business_letter_form_data.get("cta_type", "Request a Meeting")
                cta_options = ["Request a Meeting", "Place an Order", "Contact for More Information", "Visit Website", "Call", "Email", "Custom"]
                cta_type = st.selectbox(
                    "Call to Action Type",
                    cta_options,
                    index=cta_options.index(default_cta_type) if default_cta_type in cta_options else 0,
                    help="Select the type of call to action you want to include, or choose 'Custom'.",
                    key=f"{subtype}_cta_type"
                )
                form_data["cta_type"] = cta_type # Add selected CTA type to form_data for prompt

                if cta_type == "Custom":
                    default_custom_cta = st.session_state.business_letter_form_data.get("custom_cta", "")
                    custom_cta = st.text_input(
                        "Custom Call to Action",
                        value=default_custom_cta,
                        help="Enter your custom call to action phrase.",
                        placeholder="e.g., Register for our upcoming webinar",
                        key=f"{subtype}_custom_cta"
                    )
                    form_data["custom_cta"] = custom_cta # Add to form_data for prompt


            # Section for adding additional persuasive elements like offers, testimonials, or urgency.
            with st.expander("Additional Options"):
                default_include_special_offer = st.session_state.business_letter_form_data.get("include_special_offer", False)
                include_special_offer = st.checkbox("Include a special offer or incentive", value=default_include_special_offer, help="Add a specific offer to encourage action.", key=f"{subtype}_include_special_offer")
                form_data["special_offer"] = None # Initialize to None
                if include_special_offer:
                    default_special_offer = st.session_state.business_letter_form_data.get("special_offer", "")
                    form_data["special_offer"] = st.text_area(
                        "Special Offer/Incentive Details",
                        value=default_special_offer,
                        height=100,
                        help="Describe the special offer or incentive.",
                        placeholder="e.g., 15% discount for orders placed before June 30",
                        key=f"{subtype}_special_offer"
                    )

                default_include_testimonial = st.session_state.business_letter_form_data.get("include_testimonial", False)
                include_testimonial = st.checkbox("Include a testimonial or social proof", value=default_include_testimonial, help="Add a quote from a satisfied customer or relevant statistic.", key=f"{subtype}_include_testimonial")
                form_data["testimonial"] = None # Initialize to None
                if include_testimonial:
                    default_testimonial = st.session_state.business_letter_form_data.get("testimonial", "")
                    form_data["testimonial"] = st.text_area(
                        "Testimonial/Social Proof Details",
                        value=default_testimonial,
                        height=100,
                        help="Add a testimonial or social proof to strengthen your message.",
                        placeholder="e.g., 'ABC Company helped us increase our revenue by 30% in just three months.' - John Smith, CEO of XYZ Corp",
                        key=f"{subtype}_testimonial"
                    )

                default_include_urgency = st.session_state.business_letter_form_data.get("include_urgency", False)
                include_urgency = st.checkbox("Include urgency or scarcity elements", value=default_include_urgency, help="Add elements that encourage prompt action.", key=f"{subtype}_include_urgency")
                form_data["urgency"] = None # Initialize to None
                if include_urgency:
                    default_urgency = st.session_state.business_letter_form_data.get("urgency", "")
                    form_data["urgency"] = st.text_area(
                        "Urgency/Scarcity Details",
                        value=default_urgency,
                        height=100,
                        help="Add elements that create a sense of urgency or scarcity.",
                        placeholder="e.g., Limited time offer - only 10 spots available",
                        key=f"{subtype}_urgency"
                    )

        # --- Tab 2: Business Information ---
        with tab2:
            # Section for sender and recipient business information.
            col3, col4 = st.columns(2)

            with col3:
                st.markdown("### Your Company Information")
                # Input fields for sender's business details, populated from session state.
                form_data["sender_company"] = st.text_input("Your Company Name", value=st.session_state.business_letter_form_data.get("sender_company", ""), help="Your company's full legal name.", key=f"{subtype}_sender_company")
                form_data["sender_name"] = st.text_input("Your Name", value=st.session_state.business_letter_form_data.get("sender_name", ""), help="Your full name as the sender.", key=f"{subtype}_sender_name")
                form_data["sender_title"] = st.text_input("Your Title/Position", value=st.session_state.business_letter_form_data.get("sender_title", ""), help="Your job title or position within the company.", key=f"{subtype}_sender_title")
                form_data["sender_address"] = st.text_area("Your Company Address", value=st.session_state.business_letter_form_data.get("sender_address", ""), height=100, help="Full mailing address of your company.", key=f"{subtype}_sender_address")
                form_data["sender_phone"] = st.text_input("Your Phone Number (Optional)", value=st.session_state.business_letter_form_data.get("sender_phone", ""), help="Your contact phone number.", key=f"{subtype}_sender_phone")
                form_data["sender_email"] = st.text_input("Your Email Address (Optional)", value=st.session_state.business_letter_form_data.get("sender_email", ""), help="Your contact email address.", key=f"{subtype}_sender_email")
                form_data["sender_website"] = st.text_input("Your Website (Optional)", value=st.session_state.business_letter_form_data.get("sender_website", ""), help="Your company website URL.", key=f"{subtype}_sender_website")

            with col4:
                st.markdown("### Recipient Information")
                # Input fields for recipient's business details, populated from session state.
                form_data["recipient_company"] = st.text_input("Recipient Company Name", value=st.session_state.business_letter_form_data.get("recipient_company", ""), help="The name of the company you are writing to.", key=f"{subtype}_recipient_company")
                form_data["recipient_name"] = st.text_input("Recipient Name (Optional)", value=st.session_state.business_letter_form_data.get("recipient_name", ""), help="The name of the specific person you are writing to (if known).", key=f"{subtype}_recipient_name")
                form_data["recipient_title"] = st.text_input("Recipient Title/Position (Optional)", value=st.session_state.business_letter_form_data.get("recipient_title", ""), help="The recipient's job title or position (if known).", key=f"{subtype}_recipient_title")
                form_data["recipient_address"] = st.text_area("Recipient Address", value=st.session_state.business_letter_form_data.get("recipient_address", ""), height=100, help="Full mailing address of the recipient's company.", key=f"{subtype}_recipient_address")

                # Optional recipient contact information in an expander.
                with st.expander("Additional Recipient Information (Optional)"):
                    form_data["recipient_phone"] = st.text_input("Recipient Phone Number (Optional)", value=st.session_state.business_letter_form_data.get("recipient_phone", ""), help="Recipient's contact phone number.", key=f"{subtype}_recipient_phone")
                    form_data["recipient_email"] = st.text_input("Recipient Email Address (Optional)", value=st.session_state.business_letter_form_data.get("recipient_email", ""), help="Recipient's contact email address.", key=f"{subtype}_recipient_email")

            # Section for defining the business relationship.
            st.markdown("### Business Relationship")
            relationship_options = ["New Prospect", "Existing Customer", "Former Customer", "Partner/Vendor", "Other"]
            default_relationship_type = st.session_state.business_letter_form_data.get("relationship_type", "New Prospect")
            form_data["relationship_type"] = st.selectbox(
                "Relationship with Recipient",
                relationship_options,
                 index=relationship_options.index(default_relationship_type) if default_relationship_type in relationship_options else 0,
                help="Select your current business relationship with the recipient.",
                key=f"{subtype}_relationship_type"
            )

            form_data["relationship_duration"] = None # Initialize to None
            if form_data["relationship_type"] == "Existing Customer":
                default_relationship_duration = st.session_state.business_letter_form_data.get("relationship_duration", "")
                form_data["relationship_duration"] = st.text_input(
                    "Relationship Duration",
                    value=default_relationship_duration,
                    help="How long have you been doing business with this customer? (e.g., 3 years, since 2020)",
                    placeholder="e.g., 3 years",
                    key=f"{subtype}_relationship_duration"
                )

            # Section for letter formatting options.
            st.markdown("### Letter Format")
            format_options = ["Full Block", "Modified Block", "Semi-Block"]
            default_letter_format = st.session_state.business_letter_form_data.get("letter_format", "Full Block")
            form_data["letter_format"] = st.selectbox(
                "Format Style",
                format_options,
                index=format_options.index(default_letter_format) if default_letter_format in format_options else 0,
                help="Select the standard business letter format style.",
                key=f"{subtype}_letter_format"
            )

            default_include_letterhead = st.session_state.business_letter_form_data.get("include_letterhead", True)
            form_data["include_letterhead"] = st.checkbox("Include letterhead", value=default_include_letterhead, help="Include your company's letterhead information at the top.", key=f"{subtype}_include_letterhead")

            default_include_subject_line = st.session_state.business_letter_form_data.get("include_subject_line", True)
            include_subject_line = st.checkbox("Include subject line", value=default_include_subject_line, help="Include a clear subject line.", key=f"{subtype}_include_subject_line")
            form_data["subject_line"] = None # Initialize to None
            form_data["include_subject_line"] = include_subject_line # Store checkbox state
            if include_subject_line:
                default_subject_line = st.session_state.business_letter_form_data.get("subject_line", "")
                form_data["subject_line"] = st.text_input(
                    "Subject Line Text",
                    value=default_subject_line,
                    help="Enter the text for the subject line.",
                    placeholder="e.g., Special Offer for Premium Customers",
                    key=f"{subtype}_subject_line"
                )

            default_include_reference_number = st.session_state.business_letter_form_data.get("include_reference_number", False)
            include_reference_number = st.checkbox("Include reference number", value=default_include_reference_number, help="Include a reference number for tracking.", key=f"{subtype}_include_reference_number")
            form_data["reference_number"] = None # Initialize to None
            form_data["include_reference_number"] = include_reference_number # Store checkbox state
            if include_reference_number:
                default_reference_number = st.session_state.business_letter_form_data.get("reference_number", "")
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
            if not st.session_state.business_letter_generated:
                st.info("Complete the letter details and click 'Generate Letter' to preview your letter.")

            # The Generate button is placed inside the form. Clicking it submits the form
            # and triggers the code block below it to run.
            generate_button = st.form_submit_button("Generate Letter", type="primary")

            if generate_button:
                # Action to perform when the form is submitted via the Generate button.

                # Store the current state of all form inputs in session state.
                # This allows retaining user inputs even after generation or regeneration.
                st.session_state.business_letter_form_data = form_data.copy()

                # Prepare metadata specifically for the formatter and analysis functions.
                # This includes structured contact info, dates, subject, etc.
                metadata = {
                    "sender_company": form_data.get("sender_company", ""),
                    "sender_name": form_data.get("sender_name", ""),
                    "sender_title": form_data.get("sender_title", ""),
                    "sender_address": form_data.get("sender_address", ""),
                    "sender_phone": form_data.get("sender_phone", ""),
                    "sender_email": form_data.get("sender_email", ""),
                    "sender_website": form_data.get("sender_website", ""),
                    "recipient_company": form_data.get("recipient_company", ""),
                    "recipient_name": form_data.get("recipient_name", ""),
                    "recipient_title": form_data.get("recipient_title", ""),
                    "recipient_address": form_data.get("recipient_address", ""),
                    "recipient_phone": form_data.get("recipient_phone", ""),
                    "recipient_email": form_data.get("recipient_email", ""),
                    "relationship_type": form_data.get("relationship_type", ""),
                    "date": datetime.datetime.now().strftime("%B %d, %Y"), # Use current date for the letter
                    "letter_format": form_data.get("letter_format", "Full Block"),
                    "include_letterhead": form_data.get("include_letterhead", True),
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
                metadata["complimentary_close"] = "Sincerely," # Standard business close


                st.session_state.business_letter_metadata = metadata.copy()


                # --- Letter Generation Logic ---
                # Check for minimal required fields before attempting generation.
                if not form_data.get("sender_company") or not form_data.get("recipient_company"):
                    st.error("Please provide at least your company name and the recipient's company name.")
                else:
                    # Display a spinner while the AI generates the letter.
                    with st.spinner("Generating your business letter..."):
                        # Combine all necessary data into a single dictionary for the generation function.
                        # This includes both form data and metadata.
                        # Note: tone, persuasion_level, length, formality are already in form_data
                        generation_data = {
                            "subtype": subtype,
                            **form_data, # Includes all collected form inputs
                            **metadata # Includes structured sender/recipient/date/format info
                        }

                        # Call the letter generation function with the combined data.
                        letter_content = generate_business_letter(generation_data)

                        # Store the generated letter content and update the generated flag.
                        st.session_state.business_letter_content = letter_content
                        st.session_state.business_letter_generated = True

                        # Rerun the app to exit the form block and display the generated letter section.
                        # This rerun happens automatically on form submission, but explicit state updates
                        # ensure the display logic reacts correctly.
                        # st.rerun() # Rerun is handled by form submission

        # --- Display Generated Letter and Analysis ---
        # This block executes if a letter has been generated and stored in session state.
        if st.session_state.business_letter_generated and st.session_state.business_letter_content is not None:
            letter_content = st.session_state.business_letter_content
            metadata = st.session_state.business_letter_metadata

            # Create tabs for different views of the generated letter.
            preview_tab1, preview_tab2, preview_tab3 = st.tabs(["Formatted Preview", "Plain Text", "Analysis"])

            with preview_tab1:
                st.markdown("### Letter Preview")
                # Generate and display the HTML preview of the letter using the formatter utility.
                # Pass letter_type="business" to the formatter.
                html_preview = get_letter_preview_html(letter_content, metadata, letter_type="business")
                st.markdown(html_preview, unsafe_allow_html=True)

                # Download button for the plain text version of the letter.
                file_name_suffix = metadata.get('recipient_company', 'business').replace(' ', '_').lower()
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
                improvement_suggestions = suggest_improvements(letter_content, "business") # Pass "business" as letter_type

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
                st.session_state.business_letter_generated = False
                st.session_state.business_letter_content = None # Clear generated content
                # st.session_state.business_letter_form_data is already populated from the form submit
                st.rerun() # Rerun to show the form with previous inputs


def generate_business_letter(data: Dict[str, Any]) -> str:
    """
    Generates a business letter using the LLM by constructing a detailed prompt
    based on the collected user inputs and metadata.

    Args:
        data: A dictionary containing all collected user inputs and metadata
              (from the form and session state).

    Returns:
        The generated letter content as a string, or an error message if generation fails.
    """

    # Extract key generation parameters from the data dictionary.
    subtype = data.get("subtype", "default")
    tone = data.get("tone", "Professional")
    persuasion_level = data.get("persuasion_level", "Moderate")
    length = data.get("length", "Standard")
    formality = data.get("formality", "Professional")

    # Get template guidance and structure to include in the prompt.
    template = get_template_by_type("business", subtype)
    template_guidance = template.get("guidance", "Follow standard business letter practices.")
    template_structure = template.get("structure", ["Introduction", "Body", "Call to Action", "Closing"])


    # Build the prompt string step-by-step, including all relevant details
    # from the user's input and selected options.
    prompt_parts = [
        f"Write a {length.lower()}, {formality.lower()} business {get_name_for_subtype(subtype)} letter with a {tone.lower()} tone and {persuasion_level.lower()} persuasion level.",
        f"Purpose: {get_description_for_subtype(subtype)}",
        f"Recipient: {data.get('recipient_name', '')}, {data.get('recipient_title', '')} at {data.get('recipient_company', '')}",
        f"Sender: {data.get('sender_name', '')}, {data.get('sender_title', '')} at {data.get('sender_company', '')}",
        f"Relationship: {data.get('relationship_type', 'Not specified')}{' for ' + data.get('relationship_duration', '') if data.get('relationship_duration') else ''}",
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


    # Add additional persuasive options if included.
    if data.get('include_cta') and data.get('cta_type'):
        cta_text = data.get('custom_cta') if data.get('cta_type') == "Custom" else data['cta_type']
        if cta_text:
            prompt_parts.append(f"Include a clear Call to Action: {cta_text}")

    if data.get('include_special_offer') and data.get('special_offer'):
        prompt_parts.append(f"Include this Special Offer/Incentive: {data['special_offer']}")

    if data.get('include_testimonial') and data.get('testimonial'):
        prompt_parts.append(f"Include this Testimonial/Social Proof: {data['testimonial']}")

    if data.get('include_urgency') and data.get('urgency'):
        prompt_parts.append(f"Include Urgency/Scarcity Elements: {data['urgency']}")

    # Add the template structure and overall guidance to the prompt.
    # This helps the LLM understand the desired layout and writing style.
    prompt_parts.append("\nFollow this general structure:")
    for i, section in enumerate(template_structure):
        prompt_parts.append(f"{i+1}. {section}")
    prompt_parts.append(f"\nOverall Writing Guidance: {template_guidance}")

    # Add final instructions for the LLM.
    prompt_parts.append("\nMake the letter professional, persuasive, and appropriate for business communication.")


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
    """Maps a business letter subtype ID to a relevant emoji icon."""
    icons = {
        "sales": "💰",
        "proposal": "📊",
        "order": "🛒",
        "quotation": "💲",
        "acknowledgment": "✅",
        "collection": "💵",
        "adjustment": "🔧",
        "credit": "💳",
        "follow_up": "🔄"
    }
    return icons.get(subtype, "📝") # Default icon

def get_name_for_subtype(subtype: str) -> str:
    """Maps a business letter subtype ID to its display name."""
    names = {
        "sales": "Sales Letter",
        "proposal": "Business Proposal",
        "order": "Order Letter",
        "quotation": "Quotation Letter",
        "acknowledgment": "Acknowledgment Letter",
        "collection": "Collection Letter",
        "adjustment": "Adjustment Letter",
        "credit": "Credit Letter",
        "follow_up": "Follow-up Letter"
    }
    return names.get(subtype, "Business Letter") # Default name

def get_description_for_subtype(subtype: str) -> str:
    """Maps a business letter subtype ID to a brief description."""
    descriptions = {
        "sales": "Promote products or services to potential customers with a persuasive sales letter.",
        "proposal": "Present a business idea or solution with a comprehensive business proposal.",
        "order": "Place an order for products or services with a clear and detailed order letter.",
        "quotation": "Provide pricing information for products or services with a professional quotation letter.",
        "acknowledgment": "Confirm receipt of payment, order, or documents with an acknowledgment letter.",
        "collection": "Request payment for overdue accounts with a firm but professional collection letter.",
        "adjustment": "Respond to customer complaints or requests with a solution-oriented adjustment letter.",
        "credit": "Extend credit to customers or respond to credit requests with a clear credit letter.",
        "follow_up": "Follow up on previous communication or meetings with a purposeful follow-up letter."
    }
    return descriptions.get(subtype, "Create a business letter for your specific needs.") # Default description

def get_fields_for_subtype(subtype: str) -> List[Dict[str, Any]]:
    """
    Provides a list of input field configurations specific to each business letter subtype.
    Each dictionary in the list defines a form input field, including its ID, label,
    type, and optional properties like help text, options (for select/slider),
    min/max values (for slider/number), and a default value.
    """

    # Define subtype-specific fields.
    if subtype == "sales":
        return [
            {
                "id": "product_service",
                "label": "Product/Service",
                "type": "text",
                "help": "What specific product or service are you promoting?"
            },
            {
                "id": "benefits",
                "label": "Key Benefits",
                "type": "textarea",
                "help": "List the main benefits your product or service offers to the recipient."
            },
            {
                "id": "usp",
                "label": "Unique Selling Points",
                "type": "textarea",
                "help": "What makes your product or service stand out from competitors?"
            },
            {
                "id": "pricing",
                "label": "Pricing Information",
                "type": "textarea",
                "help": "Include relevant pricing details or a call to action to learn about pricing. (optional)"
            }
        ]
    elif subtype == "proposal":
        return [
            {
                "id": "proposal_type",
                "label": "Proposal Type",
                "type": "text",
                "help": "What type of proposal is this? (e.g., service proposal, partnership proposal)"
            },
            {
                "id": "problem",
                "label": "Problem Statement",
                "type": "textarea",
                "help": "What problem or need does your proposal address?"
            },
            {
                "id": "solution",
                "label": "Proposed Solution",
                "type": "textarea",
                "help": "What solution are you proposing?"
            },
            {
                "id": "implementation",
                "label": "Implementation Plan",
                "type": "textarea",
                "help": "How will your solution be implemented?"
            },
            {
                "id": "cost_timeline",
                "label": "Cost and Timeline Summary",
                "type": "textarea",
                "help": "Provide a summary of the costs involved and the overall timeline."
            }
        ]
    elif subtype == "order":
        return [
            {
                "id": "ordered_items",
                "label": "Products/Services Ordered",
                "type": "textarea",
                "help": "List the products or services you are ordering, including quantities, model numbers, and any specific details."
            },
            {
                "id": "delivery",
                "label": "Delivery Details",
                "type": "textarea",
                "help": "Specify delivery requirements: requested date, shipping address (if different from recipient address), shipping method, and any special instructions."
            },
            {
                "id": "payment_terms",
                "label": "Payment Terms",
                "type": "text",
                "help": "State the agreed-upon payment terms for this order (e.g., Net 30, Payment in Advance)."
            },
            {
                 "id": "po_number",
                 "label": "Purchase Order Number",
                 "type": "text",
                 "help": "Enter the Purchase Order number if applicable for tracking."
            }
        ]
    elif subtype == "quotation":
        return [
            {
                "id": "quoted_items",
                "label": "Products/Services Quoted",
                "type": "textarea",
                "help": "List the products or services you are providing a quote for, including brief descriptions and specifications."
            },
            {
                "id": "pricing_details",
                "label": "Pricing Details",
                "type": "textarea",
                "help": "Provide a breakdown of pricing for each item or service, including unit price, quantity, and line total. Mention taxes or fees separately."
            },
            {
                "id": "validity",
                "label": "Validity Period",
                "type": "text",
                "help": "How long is this quotation valid for?"
            },
            {
                "id": "terms",
                "label": "Terms and Conditions",
                "type": "textarea",
                "help": "Include any relevant terms and conditions related to this quotation. (optional)"
            }
        ]
    elif subtype == "acknowledgment":
        return [
            {
                "id": "acknowledging",
                "label": "Acknowledging",
                "type": "text",
                "help": "What specific item, payment, order, or document are you acknowledging receipt of?"
            },
            {
                "id": "date_received",
                "label": "Date Received",
                "type": "date", # Using date type for date input
                "help": "When was the item, payment, order, or document received?"
            },
            {
                "id": "reference_info",
                "label": "Reference Information",
                "type": "text",
                "help": "Include any relevant reference numbers (e.g., Order ID, Invoice #, Case Number)."
            },
            {
                "id": "next_steps",
                "label": "Next Steps",
                "type": "textarea",
                "help": "Outline the next steps or actions that will be taken regarding this item (e.g., 'Your order is being processed', 'Your payment has been applied'). (optional)"
            }
        ]
    elif subtype == "collection":
        return [
            {
                "id": "invoice_number",
                "label": "Invoice Number",
                "type": "text",
                "help": "What is the invoice number for the overdue payment?"
            },
            {
                "id": "amount_due",
                "label": "Amount Due",
                "type": "text", # Using text to allow currency symbols like $ or €
                "help": "What is the total outstanding amount due?"
            },
            {
                "id": "due_date",
                "label": "Original Due Date",
                "type": "date", # Using date type for date input
                "help": "When was the payment originally due?"
            },
            {
                "id": "days_overdue",
                "label": "Days Overdue",
                "type": "number",
                "min": 0, # Minimum value is 0 days overdue
                "help": "How many days is the payment currently overdue?"
            },
            {
                "id": "payment_history",
                "label": "Payment History Summary",
                "type": "textarea",
                "help": "Briefly summarize previous attempts to collect payment or communication about the invoice. (optional)"
            },
             {
                "id": "consequences",
                "label": "Consequences of Non-Payment",
                "type": "textarea",
                "help": "Clearly state the consequences of continued non-payment (e.g., late fees, referral to collections, legal action). Tailor the severity to the stage of collection. (optional)"
            }
        ]
    elif subtype == "adjustment":
        return [
            {
                "id": "customer_name_adj", # Added suffix to avoid potential ID clashes with recipient_name
                "label": "Customer Name",
                "type": "text",
                "help": "Name of the customer who submitted the complaint or request."
            },
            {
                "id": "complaint_request",
                "label": "Customer Complaint/Request Summary",
                "type": "textarea",
                "help": "Provide a brief summary of the customer's complaint or request."
            },
            {
                "id": "date_of_issue",
                "label": "Date of Issue/Complaint",
                "type": "date", # Using date type for date input
                "help": "When did the issue occur or when was the complaint/request received?"
            },
            {
                "id": "findings",
                "label": "Investigation Findings",
                "type": "textarea",
                "help": "Describe what your investigation found regarding the customer's issue."
            },
            {
                "id": "adjustment",
                "label": "Adjustment Offered",
                "type": "textarea",
                "help": "Clearly describe the specific adjustment you are offering to resolve the issue (e.g., full refund, partial refund, replacement product, service credit)."
            },
            {
                "id": "preventive_measures",
                "label": "Preventive Measures",
                "type": "textarea",
                "help": "What measures will be taken to prevent similar issues from happening in the future? (optional)"
            }
        ]
    elif subtype == "credit":
        return [
            {
                "id": "credit_request_type",
                "label": "Credit Request Type",
                "type": "select",
                "options": ["New Credit Application", "Credit Limit Increase Request", "Credit Terms Adjustment Request", "Response to Credit Inquiry"],
                "help": "What type of credit-related request or response is this letter for?"
            },
            {
                "id": "applicant_name",
                "label": "Applicant Name",
                "type": "text",
                "help": "Name of the individual or company applying for or receiving credit."
            },
            {
                "id": "credit_decision",
                "label": "Credit Decision",
                "type": "select",
                "options": ["Approved", "Denied", "Conditionally Approved", "Under Review", "Information Required"],
                "help": "What is the outcome or status of the credit application/request?"
            },
            {
                "id": "credit_terms",
                "label": "Credit Terms",
                "type": "textarea",
                "help": "Describe the credit terms being extended or requested (e.g., Net 30, 2% 10 Net 30, interest rate, payment schedule). (Required if Approved/Conditionally Approved)"
            },
            {
                "id": "credit_limit",
                "label": "Credit Limit",
                "type": "text", # Using text to allow for "N/A" or specific amounts
                "help": "What is the approved credit limit? (Required if Approved/Conditionally Approved)"
            },
            {
                "id": "requirements",
                "label": "Requirements/Conditions",
                "type": "textarea",
                "help": "List any specific requirements or conditions that must be met for the credit. (Optional)"
            },
            {
                "id": "reason_for_decision",
                "label": "Reason for Decision (if Denied/Conditional/Info Required)",
                "type": "textarea",
                "help": "Clearly explain the reason for the credit decision or why more information is needed. (Required if not Approved)"
            }
        ]
    elif subtype == "follow_up":
        return [
            {
                "id": "previous_communication_type",
                "label": "Previous Communication Type",
                "type": "select",
                "options": ["Meeting", "Phone Call", "Email", "Proposal Submission", "Interview", "Networking Event", "Other"],
                "help": "What type of previous interaction are you following up on?"
            },
            {
                "id": "previous_date",
                "label": "Date of Previous Contact",
                "type": "date", # Using date type for date input
                "help": "When was the previous communication or meeting?"
            },
            {
                "id": "previous_topic",
                "label": "Topic of Previous Contact",
                "type": "text",
                "help": "What was the main subject or topic discussed during the previous interaction?"
            },
            {
                "id": "follow_up_purpose",
                "label": "Purpose of Follow-up",
                "type": "textarea",
                "help": "Why are you following up now? What is the specific goal of this letter?"
            },
            {
                "id": "action_items",
                "label": "Proposed Next Steps/Action Items",
                "type": "textarea",
                "help": "What actions or next steps are you proposing or inquiring about as a result of this follow-up? (optional)"
            }
        ]

    # Default fields if subtype is not recognized or no specific fields are defined.
    # This provides a basic textarea for general content.
    return [
        {
            "id": "main_content",
            "label": "Main Content",
            "type": "textarea",
            "help": "Enter the main content you want to include in your business letter."
        }
    ]

def get_tones_for_subtype(subtype: str) -> List[str]:
    """Maps a business letter subtype ID to a list of suggested tones."""
    tones = {
        "sales": ["Enthusiastic", "Confident", "Friendly", "Professional", "Persuasive"],
        "proposal": ["Professional", "Confident", "Collaborative", "Solution-oriented", "Authoritative"],
        "order": ["Clear", "Direct", "Professional", "Courteous", "Precise"],
        "quotation": ["Professional", "Helpful", "Informative", "Precise", "Courteous"],
        "acknowledgment": ["Appreciative", "Professional", "Courteous", "Helpful", "Prompt"],
        "collection": ["Firm", "Professional", "Respectful", "Direct", "Urgent"],
        "adjustment": ["Empathetic", "Professional", "Solution-oriented", "Apologetic", "Helpful"],
        "credit": ["Professional", "Helpful", "Informative", "Trustworthy", "Clear"],
        "follow_up": ["Friendly", "Professional", "Persistent", "Helpful", "Courteous"]
    }
    # Return the list of tones for the subtype, or a default list if not found.
    return tones.get(subtype, ["Professional", "Courteous", "Clear", "Helpful", "Friendly"])

# Example of how to run the app (for local development using `streamlit run your_script_name.py`)
# Uncomment the lines below to make this script directly executable.
# if __name__ == "__main__":
#     write_letter()
