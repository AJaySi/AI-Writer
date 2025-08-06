"""
Cover Letters Module

This module provides a Streamlit interface for generating various types of cover letters
using AI assistance. It collects user inputs specific to the chosen cover letter subtype,
formats the data, generates a prompt for the AI, calls the AI for content generation,
and displays the formatted letter preview and analysis, including ATS compatibility.
"""

import streamlit as st
import datetime
import re # Import regex for ATS score calculation
from typing import Dict, Any, List
from collections import Counter # Import Counter for ATS keyword frequency

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
    """Placeholder: Generates a basic HTML preview."""
    # Basic HTML structure with inline styles for preview
    formatted_paragraphs = "".join(f"<p style='margin-bottom: 1em;'>{p.strip()}</p>" for p in content.split("\n\n") if p.strip())
    return f"""
    <div style="max-width: 800px; margin: 20px auto; padding: 30px; border: 1px solid #d0d0d0; border-radius: 8px; background-color: #ffffff; font-family: 'Arial', sans-serif; line-height: 1.6; color: #333;">
        <div style="text-align: right; margin-bottom: 20px;">{metadata.get('date', 'Date')}</div>
        <div style="margin-bottom: 20px; font-weight: bold;">Subject: Application for {metadata.get('job_title', 'Position')}</div>
        <div style="margin-bottom: 20px;">{metadata.get('salutation', 'Dear Hiring Manager,')}</div>
        <div style="margin-bottom: 20px;">{formatted_paragraphs if formatted_paragraphs else "<p>Letter content goes here...</p>"}</div>
        <div style="margin-top: 40px;">{metadata.get('complimentary_close', 'Sincerely,')}</div>
        <div>{metadata.get('sender_name', 'Your Name')}</div>
    </div>
    """

def analyze_letter_tone(content: str) -> Dict[str, float]:
    """Placeholder: Returns dummy tone analysis."""
    # Returns scores between 0.0 and 1.0
    return {"professional": 0.85, "enthusiastic": 0.7, "confident": 0.8}

def check_formality(content: str) -> float:
    """Placeholder: Returns a dummy formality score (0.0 to 1.0)."""
    return 0.90 # Example: 90% formal

def get_readability_metrics(content: str) -> Dict[str, Any]:
    """Placeholder: Returns dummy readability metrics."""
    word_count = len(content.split())
    # Estimate reading time in seconds (assuming ~200 words per minute)
    reading_time_seconds = round((word_count / 200) * 60)
    return {
        "word_count": word_count,
        "sentence_count": max(1, content.count('. ') + content.count('! ') + content.count('? ')), # Simple sentence count
        "avg_words_per_sentence": round(word_count / max(1, content.count('. ') + content.count('! ') + content.count('? ')), 2),
        "flesch_reading_ease": 55.0, # Dummy score
        "reading_level": "Fairly Difficult", # Dummy level
        "reading_time_seconds": reading_time_seconds # Added reading time
    }

def suggest_improvements(content: str, letter_type: str) -> List[str]:
    """Placeholder: Returns dummy improvement suggestions."""
    if len(content) < 150:
        return ["Suggestion: Your cover letter seems quite brief. Consider elaborating on your key qualifications."]
    elif "generic skill" in content.lower():
         return ["Suggestion: Replace generic skills with specific examples or achievements."]
    else:
        return ["Suggestion: Ensure your letter clearly matches the job description keywords."]

def get_template_by_type(letter_type: str, subtype: str = "default") -> Dict[str, Any]:
    """Placeholder: Returns a generic template."""
    # This should ideally come from the actual letter_templates module
    return {"structure": ["Introduction", "Body Paragraphs", "Closing"], "guidance": "Generic guidance for a cover letter."}

def llm_text_gen(prompt: str) -> str:
    """Placeholder: Simulates LLM text generation."""
    # In a real app, this would call the actual LLM API
    st.info(f"LLM Prompt:\n```\n{prompt}\n```") # Display prompt for debugging
    # Return a dummy generated letter based on the prompt
    return f"Subject: Application for [Generated Job Title] Position\n\nDear [Generated Hiring Manager Name],\n\nThis is a sample cover letter generated based on the following details:\n\n{prompt}\n\n[Generated content based on the prompt would go here, following the requested structure, tone, and focus area.]\n\nSincerely,\n[Generated Your Name]"

# --- End Placeholder Functions ---


def write_letter():
    """
    Main function for the Cover Letters interface. Sets up the Streamlit page
    and handles navigation between subtype selection and the letter form.
    """

    # Page title and description
    st.title("📄 Cover Letter Writer")
    st.markdown("""
    Create professional cover letters tailored to specific job applications. Select a cover letter type below to get started.
    """)

    # Initialize Streamlit session state variables specific to the cover letter module.
    # These variables persist across reruns and store the user's progress and data.
    if "cover_letter_subtype" not in st.session_state:
        st.session_state.cover_letter_subtype = None # Stores the ID of the selected cover letter type
    if "cover_letter_generated" not in st.session_state:
        st.session_state.cover_letter_generated = False # Flag to indicate if a letter has been generated
    if "cover_letter_content" not in st.session_state:
        st.session_state.cover_letter_content = None # Stores the generated letter content
    if "cover_letter_metadata" not in st.session_state:
        st.session_state.cover_letter_metadata = {} # Stores metadata like sender/recipient info
    if "cover_letter_form_data" not in st.session_state:
         st.session_state.cover_letter_form_data = {} # Stores the user's input from the form fields

    # Back button logic for subtypes. This button appears when a subtype is selected,
    # allowing the user to return to the subtype selection screen.
    if st.session_state.cover_letter_subtype is not None:
        if st.button("← Back to Cover Letter Types"):
            # Reset session state variables for this module to their initial state
            # This clears the current form data and generated letter.
            st.session_state.cover_letter_subtype = None
            st.session_state.cover_letter_generated = False
            st.session_state.cover_letter_content = None
            st.session_state.cover_letter_metadata = {}
            st.session_state.cover_letter_form_data = {}
            st.rerun() # Rerun the app to update the UI based on the changed state

    # Main navigation logic within the cover letter module.
    # If no subtype is selected, show the selection grid. Otherwise, show the form for the selected subtype.
    if st.session_state.cover_letter_subtype is None:
        # Display cover letter type selection if no subtype is selected
        display_cover_letter_types()
    else:
        # Display the interface form for the selected cover letter subtype
        display_cover_letter_form(st.session_state.cover_letter_subtype)


def display_cover_letter_types():
    """
    Displays the cover letter type selection interface using a grid of styled buttons.
    Each button represents a specific type of cover letter the user can choose to write.
    """

    st.markdown("## Select Cover Letter Type")

    # Define cover letter types with their details (ID, Name, Icon, Description, Color)
    # This list is used to generate the selection buttons.
    cover_letter_types = [
        {
            "id": "standard",
            "name": "Standard Cover Letter",
            "icon": "📝",
            "description": "General purpose cover letter for most job applications",
            "color": "#1976D2" # Blue
        },
        {
            "id": "career_change",
            "name": "Career Change",
            "icon": "🔄",
            "description": "Highlight transferable skills when changing careers",
            "color": "#388E3C" # Green
        },
        {
            "id": "entry_level",
            "name": "Entry Level",
            "icon": "🌱",
            "description": "For recent graduates or those with limited experience",
            "color": "#FFA000" # Orange
        },
        {
            "id": "executive",
            "name": "Executive",
            "icon": "👔",
            "description": "For senior management and executive positions",
            "color": "#5D4037" # Brown
        },
        {
            "id": "creative",
            "name": "Creative",
            "icon": "🎨",
            "description": "For creative industries like design, writing, or marketing",
            "color": "#7B1FA2" # Purple
        },
        {
            "id": "technical",
            "name": "Technical",
            "icon": "💻",
            "description": "For IT, engineering, and other technical roles",
            "color": "#0097A7" # Teal
        },
        {
            "id": "academic",
            "name": "Academic",
            "icon": "🎓",
            "description": "For positions in education and research",
            "color": "#D32F2F" # Red
        },
        {
            "id": "remote",
            "name": "Remote Position",
            "icon": "🏠",
            "description": "Emphasize skills for working remotely",
            "color": "#455A64" # Blue Grey
        },
        {
            "id": "referral",
            "name": "Referral",
            "icon": "👥",
            "description": "Mention a referral or connection at the company",
            "color": "#FF5722" # Deep Orange
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
    for i, letter_type_config in enumerate(cover_letter_types):
        with cols[i % 3]: # Place buttons in columns, wrapping every 3
            # Use a unique key for each button based on its ID
            # The button label uses markdown and HTML for icon, name, and description
            if st.button(
                f"### {letter_type_config['icon']} {letter_type_config['name']}\n\n<p>{letter_type_config['description']}</p>",
                key=f"btn_cover_select_{letter_type_config['id']}", # Unique key for each button
                unsafe_allow_html=True # Allow markdown and HTML in the button label
            ):
                # When a button is clicked, update the session state to the selected subtype ID
                st.session_state.cover_letter_subtype = letter_type_config['id']
                # Clear previous data related to letter generation when selecting a new type
                st.session_state.cover_letter_generated = False
                st.session_state.cover_letter_content = None
                st.session_state.cover_letter_metadata = {}
                st.session_state.cover_letter_form_data = {} # Clear previous form data
                st.rerun() # Rerun the app to switch to the form for the selected subtype

    # Apply specific background colors to buttons using their keys and custom CSS
    # This requires injecting CSS after the buttons are rendered.
    # Note: This is a common Streamlit workaround for styling individual buttons dynamically.
    button_styles = ""
    for letter_type_config in cover_letter_types:
        button_styles += f"""
        div.stButton > button[data-testid="stButton"][kind="primary"][sf-key*="btn_cover_select_{letter_type_config['id']}"] {{
            background-color: {letter_type_config['color']};
        }}
         div.stButton > button[data-testid="stButton"][kind="primary"][sf-key*="btn_cover_select_{letter_type_config['id']}"]:hover {{
            background-color: {letter_type_config['color']}D9; /* Slightly darker on hover */
        }}
        """
    st.markdown(f"<style>{button_styles}</style>", unsafe_allow_html=True)


def display_cover_letter_form(subtype: str):
    """
    Displays the form for the selected cover letter subtype. This includes
    input fields specific to the subtype, personal profile information,
    skills and experience fields, customization options, and tabs for
    previewing and analyzing the generated letter.

    Args:
        subtype: The ID string of the selected cover letter subtype.
    """

    # Get the template for the selected subtype from the templates module.
    # This provides structural guidance and general advice for the LLM.
    template = get_template_by_type("cover", subtype)

    # Display the form title, icon, description, and guidance.
    st.markdown(f"## {get_icon_for_subtype(subtype)} {get_name_for_subtype(subtype)}")
    st.markdown(f"*{get_description_for_subtype(subtype)}*")
    st.info(f"**Guidance:** {template.get('guidance', 'No specific guidance available.')}")

    # Use a Streamlit form to group inputs. This helps manage state and
    # prevents the app from rerunning every time a single input widget changes,
    # improving performance for forms with many inputs.
    with st.form(key=f"cover_letter_form_{subtype}"):
        # Create tabs to organize the form sections.
        tab1, tab2, tab3, tab4 = st.tabs(["Job Details", "Your Profile", "Skills & Experience", "Preview & Export"])

        # Dictionary to store form data collected from all tabs
        form_data = {}

        # --- Tab 1: Job Details ---
        with tab1:
            st.markdown("### Job Information")

            # Input fields for job details, populated from session state.
            form_data["job_title"] = st.text_input("Job Title", value=st.session_state.cover_letter_form_data.get("job_title", ""), help="The exact title of the position you're applying for.", key=f"{subtype}_job_title")
            form_data["company_name"] = st.text_input("Company Name", value=st.session_state.cover_letter_form_data.get("company_name", ""), help="The full name of the company you're applying to.", key=f"{subtype}_company_name")
            form_data["job_posting_url"] = st.text_input("Job Posting URL (Optional)", value=st.session_state.cover_letter_form_data.get("job_posting_url", ""), help="Provide the URL of the job posting if available. This helps tailor the letter.", key=f"{subtype}_job_posting_url")

            # Job description text area. Crucial for ATS analysis and tailoring.
            form_data["job_description"] = st.text_area(
                "Job Description",
                value=st.session_state.cover_letter_form_data.get("job_description", ""),
                height=200,
                help="Copy and paste the full job description or list the key requirements and responsibilities.",
                key=f"{subtype}_job_description"
            )

            # Optional fields for department and hiring manager.
            col1, col2 = st.columns(2)
            with col1:
                form_data["department"] = st.text_input("Department (Optional)", value=st.session_state.cover_letter_form_data.get("department", ""), help="The specific department you are applying to, if known.", key=f"{subtype}_department")
            with col2:
                form_data["hiring_manager"] = st.text_input("Hiring Manager's Name (Optional)", value=st.session_state.cover_letter_form_data.get("hiring_manager", ""), help="The name of the hiring manager or recruiter if known. Using a name is highly recommended.", key=f"{subtype}_hiring_manager")

            # Application details section.
            st.markdown("### Application Details")
            application_methods = ["Online Application", "Email", "Company Website", "Job Board", "Referral", "Other"]
            default_app_method = st.session_state.cover_letter_form_data.get("application_method", "Online Application")
            form_data["application_method"] = st.selectbox(
                "How are you applying?",
                application_methods,
                index=application_methods.index(default_app_method) if default_app_method in application_methods else 0,
                help="Select the primary method you will use to submit this cover letter.",
                key=f"{subtype}_application_method"
            )

            # Conditional fields for referral method.
            if form_data["application_method"] == "Referral":
                form_data["referral_name"] = st.text_input(
                    "Referral's Name",
                    value=st.session_state.cover_letter_form_data.get("referral_name", ""),
                    help="The full name of the person who referred you.",
                    key=f"{subtype}_referral_name"
                )
                form_data["referral_relationship"] = st.text_input(
                    "Relationship to Referral",
                    value=st.session_state.cover_letter_form_data.get("referral_relationship", ""),
                    help="Briefly describe your relationship with the referrer (e.g., former colleague, friend, mentor).",
                    key=f"{subtype}_referral_relationship"
                )
            else:
                 # Ensure referral fields are not in form_data if not selected
                 form_data["referral_name"] = None
                 form_data["referral_relationship"] = None


            # Company research and interest sections.
            st.markdown("### Company Research")
            form_data["company_research"] = st.text_area(
                "Company Research (Optional)",
                value=st.session_state.cover_letter_form_data.get("company_research", ""),
                height=150,
                help="Share specific details you know about the company (e.g., mission, values, recent projects, news). This shows you've done your research.",
                placeholder="e.g., I was impressed by your company's recent sustainability initiative and your commitment to innovation in the field of...",
                key=f"{subtype}_company_research"
            )

            form_data["why_interested"] = st.text_area(
                "Why You're Interested (Optional)",
                value=st.session_state.cover_letter_form_data.get("why_interested", ""),
                height=150,
                help="Explain your genuine interest in this specific role and company. Connect it to your career goals or values.",
                placeholder="e.g., I'm particularly drawn to this role because it aligns with my passion for...",
                key=f"{subtype}_why_interested"
            )

        # --- Tab 2: Your Profile ---
        with tab2:
            st.markdown("### Personal Information")

            # Input fields for personal contact information.
            col3, col4 = st.columns(2)
            with col3:
                form_data["full_name"] = st.text_input("Your Full Name", value=st.session_state.cover_letter_form_data.get("full_name", ""), help="Your full name as you want it to appear on the letter.", key=f"{subtype}_full_name")
                form_data["email"] = st.text_input("Email Address", value=st.session_state.cover_letter_form_data.get("email", ""), help="Your professional email address.", key=f"{subtype}_email")
                form_data["phone"] = st.text_input("Phone Number", value=st.session_state.cover_letter_form_data.get("phone", ""), help="Your primary contact phone number.", key=f"{subtype}_phone")

            with col4:
                form_data["location"] = st.text_input("Location", value=st.session_state.cover_letter_form_data.get("location", ""), help="Your current city and state/country.", key=f"{subtype}_location")
                form_data["linkedin"] = st.text_input("LinkedIn Profile URL (Optional)", value=st.session_state.cover_letter_form_data.get("linkedin", ""), help="Your LinkedIn profile URL.", key=f"{subtype}_linkedin")
                form_data["portfolio"] = st.text_input("Portfolio/Website URL (Optional)", value=st.session_state.cover_letter_form_data.get("portfolio", ""), help="Your online portfolio or personal website URL.", key=f"{subtype}_portfolio")

            # Professional summary section.
            st.markdown("### Professional Summary")
            form_data["current_title"] = st.text_input("Current or Most Recent Job Title", value=st.session_state.cover_letter_form_data.get("current_title", ""), help="Your current or most recent job title.", key=f"{subtype}_current_title")
            form_data["years_experience"] = st.number_input("Years of Relevant Experience", min_value=0, max_value=50, value=st.session_state.cover_letter_form_data.get("years_experience", 0), help="Total years of experience relevant to the target position.", key=f"{subtype}_years_experience")

            form_data["professional_summary"] = st.text_area(
                "Professional Summary",
                value=st.session_state.cover_letter_form_data.get("professional_summary", ""),
                height=150,
                help="A brief (2-3 sentence) summary highlighting your key qualifications and career goals. This is often at the top of a resume.",
                placeholder="e.g., Results-driven marketing professional with 5+ years of experience in digital marketing strategies...",
                key=f"{subtype}_professional_summary"
            )

            # Education section.
            st.markdown("### Education")
            degrees = ["High School", "Associate's", "Bachelor's", "Master's", "PhD", "Other", "None"]
            default_degree = st.session_state.cover_letter_form_data.get("highest_degree", "Bachelor's")
            form_data["highest_degree"] = st.selectbox(
                "Highest Degree",
                degrees,
                index=degrees.index(default_degree) if default_degree in degrees else 0,
                help="Your highest level of education achieved or in progress.",
                key=f"{subtype}_highest_degree"
            )

            # Conditional education fields based on degree selection.
            if form_data["highest_degree"] != "None":
                form_data["field_of_study"] = st.text_input("Field of Study", value=st.session_state.cover_letter_form_data.get("field_of_study", ""), help="Your major or primary field of study.", key=f"{subtype}_field_of_study")
                form_data["institution"] = st.text_input("Institution", value=st.session_state.cover_letter_form_data.get("institution", ""), help="Name of the school, college, or university.", key=f"{subtype}_institution")
                # Set a reasonable default for graduation year, e.g., current year or a recent past year.
                current_year = datetime.date.today().year
                default_grad_year = st.session_state.cover_letter_form_data.get("graduation_year", current_year)
                form_data["graduation_year"] = st.number_input("Graduation Year", min_value=1950, max_value=current_year + 5, value=default_grad_year, help="Year you graduated or expect to graduate.", key=f"{subtype}_graduation_year")
            else:
                 form_data["field_of_study"] = None
                 form_data["institution"] = None
                 form_data["graduation_year"] = None


        # --- Tab 3: Skills & Experience ---
        with tab3:
            st.markdown("### Key Skills")

            # Input fields for skills.
            form_data["technical_skills"] = st.text_area(
                "Technical Skills",
                value=st.session_state.cover_letter_form_data.get("technical_skills", ""),
                height=100,
                help="List your technical skills relevant to the position, separated by commas or bullet points.",
                placeholder="e.g., Python, SQL, Adobe Creative Suite, Financial Modeling, Project Management",
                key=f"{subtype}_technical_skills"
            )

            form_data["soft_skills"] = st.text_area(
                "Soft Skills",
                value=st.session_state.cover_letter_form_data.get("soft_skills", ""),
                height=100,
                help="List your soft skills relevant to the position, separated by commas or bullet points.",
                placeholder="e.g., Leadership, Communication, Problem-solving, Teamwork, Adaptability",
                key=f"{subtype}_soft_skills"
            )

            form_data["certifications"] = st.text_area(
                "Certifications (Optional)",
                value=st.session_state.cover_letter_form_data.get("certifications", ""),
                height=100,
                help="List any relevant certifications you hold, separated by commas or bullet points.",
                placeholder="e.g., PMP, CPA, AWS Certified Solutions Architect",
                key=f"{subtype}_certifications"
            )

            # Work experience and achievements section.
            st.markdown("### Relevant Experience")

            # Most relevant achievement field. Encourage metrics.
            form_data["most_relevant_achievement"] = st.text_area(
                "Most Relevant Achievement",
                value=st.session_state.cover_letter_form_data.get("most_relevant_achievement", ""),
                height=150,
                help="Describe your single most impactful achievement that is highly relevant to this position. Use the STAR method (Situation, Task, Action, Result) and include metrics if possible.",
                placeholder="e.g., Led a team of 5 to increase website conversion rates by 35% through A/B testing and UX improvements",
                key=f"{subtype}_most_relevant_achievement"
            )

            # Additional achievements field.
            form_data["additional_achievements"] = st.text_area(
                "Additional Achievements (Optional)",
                value=st.session_state.cover_letter_form_data.get("additional_achievements", ""),
                height=150,
                help="List 2-3 other significant achievements relevant to the position, using bullet points.",
                placeholder="e.g., Reduced customer churn by 20% through implementation of new retention strategies\nManaged a $500K budget for marketing campaigns that generated $2.5M in revenue",
                key=f"{subtype}_additional_achievements"
            )

            # Cover letter customization options.
            st.markdown("### Cover Letter Customization")

            # Tone and style selection.
            col5, col6 = st.columns(2)
            with col5:
                tones = get_tones_for_subtype(subtype)
                default_tone = st.session_state.cover_letter_form_data.get("tone", tones[0] if tones else "Professional")
                form_data["tone"] = st.selectbox(
                    "Tone",
                    tones,
                    index=tones.index(default_tone) if default_tone in tones else 0,
                    help="Select the desired tone for your cover letter.",
                    key=f"{subtype}_tone"
                )

                lengths = ["Brief", "Standard", "Detailed"]
                default_length = st.session_state.cover_letter_form_data.get("length", "Standard")
                form_data["length"] = st.select_slider(
                    "Length",
                    options=lengths,
                    value=default_length,
                    help="Select the desired length of your cover letter.",
                    key=f"{subtype}_length"
                )

            with col6:
                focus_areas = ["Balanced", "Skills-focused", "Experience-focused", "Culture fit-focused", "Achievement-focused"]
                default_focus = st.session_state.cover_letter_form_data.get("focus_area", "Balanced")
                form_data["focus_area"] = st.selectbox(
                    "Focus Area",
                    focus_areas,
                    index=focus_areas.index(default_focus) if default_focus in focus_areas else 0,
                    help="Choose the main area you want the cover letter to emphasize.",
                    key=f"{subtype}_focus_area"
                )

            # Optional sections like salary expectations, availability, relocation, custom closing.
            default_include_salary = st.session_state.cover_letter_form_data.get("include_salary", False)
            include_salary = st.checkbox("Include salary expectations", value=default_include_salary, help="Check to include your salary expectations in the letter.", key=f"{subtype}_include_salary")
            form_data["salary_expectations"] = None # Initialize to None
            if include_salary:
                default_salary = st.session_state.cover_letter_form_data.get("salary_expectations", "")
                form_data["salary_expectations"] = st.text_input(
                    "Salary Expectations",
                    value=default_salary,
                    help="Your salary expectations (e.g., $70,000-$80,000 annually, Negotiable).",
                    placeholder="e.g., $70,000-$80,000 annually",
                    key=f"{subtype}_salary_expectations"
                )

            with st.expander("Additional Customization"):
                default_include_availability = st.session_state.cover_letter_form_data.get("include_availability", False)
                include_availability = st.checkbox("Include availability information", value=default_include_availability, help="Mention your availability to start or for interviews.", key=f"{subtype}_include_availability")
                form_data["availability"] = None # Initialize to None
                if include_availability:
                    default_availability = st.session_state.cover_letter_form_data.get("availability", "")
                    form_data["availability"] = st.text_input(
                        "Availability Details",
                        value=default_availability,
                        help="When you can start or your availability for interviews.",
                        placeholder="e.g., Available to start immediately or Available for interviews on weekdays after 3 PM",
                        key=f"{subtype}_availability"
                    )

                default_include_relocation = st.session_state.cover_letter_form_data.get("include_relocation", False)
                include_relocation = st.checkbox("Include relocation information", value=default_include_relocation, help="Specify your willingness to relocate or remote work preference.", key=f"{subtype}_include_relocation")
                form_data["relocation_info"] = None # Initialize to None
                if include_relocation:
                    default_relocation = st.session_state.cover_letter_form_data.get("relocation_info", "")
                    form_data["relocation_info"] = st.text_input(
                        "Relocation Information Details",
                        value=default_relocation,
                        help="Your willingness to relocate or remote work preferences.",
                        placeholder="e.g., Willing to relocate to Seattle area or Currently based in Chicago but open to remote work",
                        key=f"{subtype}_relocation_info"
                    )

                default_include_closing = st.session_state.cover_letter_form_data.get("include_closing", False)
                include_closing = st.checkbox("Include custom closing statement", value=default_include_closing, help="Provide a specific sentence or two for the letter's closing.", key=f"{subtype}_include_closing")
                form_data["closing_statement"] = None # Initialize to None
                if include_closing:
                    default_closing = st.session_state.cover_letter_form_data.get("closing_statement", "")
                    form_data["closing_statement"] = st.text_area(
                        "Custom Closing Statement Text",
                        value=default_closing,
                        height=100,
                        help="Enter your custom closing statement.",
                        placeholder="e.g., I would welcome the opportunity to discuss how my background and skills would be a good match for the [Job Title] position. Thank you for your consideration.",
                        key=f"{subtype}_closing_statement"
                    )


        # --- Tab 4: Preview & Export ---
        with tab4:
            # Instructions for the user before generation.
            if not st.session_state.cover_letter_generated:
                st.info("Complete the letter details and click 'Generate Cover Letter' to preview your letter.")

            # The Generate button is placed inside the form. Clicking it submits the form
            # and triggers the code block below it to run.
            generate_button = st.form_submit_button("Generate Cover Letter", type="primary")

            if generate_button:
                # Action to perform when the form is submitted via the Generate button.

                # Store the current state of all form inputs in session state.
                # This allows retaining user inputs even after generation or regeneration.
                st.session_state.cover_letter_form_data = form_data.copy()

                # Prepare metadata specifically for the formatter and analysis functions.
                # This includes structured contact info, dates, subject, etc.
                metadata = {
                    "sender_name": form_data.get("full_name", ""),
                    "sender_email": form_data.get("email", ""),
                    "sender_phone": form_data.get("phone", ""),
                    "sender_location": form_data.get("location", ""),
                    "sender_linkedin": form_data.get("linkedin", ""),
                    "sender_portfolio": form_data.get("portfolio", ""),
                    "recipient_name": form_data.get("hiring_manager", "Hiring Manager"), # Default to "Hiring Manager" if name is not provided
                    "recipient_title": "", # Cover letters typically don't include recipient title here
                    "recipient_company": form_data.get("company_name", ""),
                    "recipient_department": form_data.get("department", ""),
                    "recipient_address": "", # Address is often omitted in modern cover letters unless specified
                    "date": datetime.datetime.now().strftime("%B %d, %Y"), # Use current date for the letter
                    "job_title": form_data.get("job_title", "") # Include job title in metadata for subject line
                }
                # Add salutation and complimentary close to metadata for the formatter
                # These could be made configurable in the future
                metadata["salutation"] = f"Dear {metadata['recipient_name']}," if metadata["recipient_name"] != "Hiring Manager" else "Dear Hiring Manager,"
                metadata["complimentary_close"] = "Sincerely,"

                st.session_state.cover_letter_metadata = metadata.copy()


                # --- Letter Generation Logic ---
                # Check for minimal required fields before attempting generation.
                if not form_data.get("job_title") or not form_data.get("company_name") or not form_data.get("full_name"):
                    st.error("Please provide at least the job title, company name, and your full name.")
                else:
                    # Display a spinner while the AI generates the letter.
                    with st.spinner("Generating your cover letter..."):
                        # Call the letter generation function with the collected form data.
                        cover_letter_content = generate_cover_letter(subtype, form_data)

                        # Store the generated letter content and update the generated flag.
                        st.session_state.cover_letter_content = cover_letter_content
                        st.session_state.cover_letter_generated = True

                        # Rerun the app to exit the form block and display the generated letter section.
                        # This rerun happens automatically on form submission, but explicit state updates
                        # ensure the display logic reacts correctly.
                        # st.rerun() # Rerun is handled by form submission

        # --- Display Generated Letter and Analysis ---
        # This block executes if a letter has been generated and stored in session state.
        if st.session_state.cover_letter_generated and st.session_state.cover_letter_content is not None:
            cover_letter_content = st.session_state.cover_letter_content
            metadata = st.session_state.cover_letter_metadata
            job_description = st.session_state.cover_letter_form_data.get("job_description", "") # Get job description for ATS analysis

            # Create tabs for different views of the generated letter.
            preview_tab1, preview_tab2, preview_tab3 = st.tabs(["Formatted Preview", "Plain Text", "Analysis"])

            with preview_tab1:
                st.markdown("### Cover Letter Preview")
                # Generate and display the HTML preview of the letter using the formatter utility.
                # Pass letter_type="cover" to the formatter.
                html_preview = get_letter_preview_html(cover_letter_content, metadata, letter_type="cover")
                st.markdown(html_preview, unsafe_allow_html=True)

                # Download button for the plain text version of the letter.
                # Use job title in the filename for better organization.
                file_name_job_title = metadata.get('job_title', 'cover_letter').replace(' ', '_').lower()
                st.download_button(
                    label="Download as Text",
                    data=cover_letter_content,
                    file_name=f"{file_name_job_title}_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )

            with preview_tab2:
                st.markdown("### Plain Text Content")
                # Display the raw generated letter content in a text area.
                st.text_area("Cover Letter Content", cover_letter_content, height=400, key=f"{subtype}_plain_text_display")

                # Button to copy the plain text content to the clipboard.
                st.button("Copy Plain Text (Manual Copy from above)", help="Select and copy the text from the box above.", key=f"{subtype}_copy_plain_text_instruction")


            with preview_tab3:
                st.markdown("### Cover Letter Analysis")
                # Perform and display analysis of the generated letter using utility functions.

                # Analyze tone, formality, and readability.
                tone_analysis = analyze_letter_tone(cover_letter_content)
                formality_score = check_formality(cover_letter_content) # Returns score between 0.0 and 1.0
                readability_metrics = get_readability_metrics(cover_letter_content)
                # Get improvement suggestions, passing the letter type for context.
                improvement_suggestions = suggest_improvements(cover_letter_content, "cover") # Pass "cover" as letter_type

                # Display analysis results in two columns.
                col7, col8 = st.columns(2)

                with col7:
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


                with col8:
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

                # ATS compatibility analysis section.
                st.markdown("#### ATS Compatibility")

                # Calculate ATS score based on keyword matching with the job description.
                ats_score = calculate_ats_score(cover_letter_content, job_description)

                st.progress(ats_score / 100.0) # Progress bar expects 0.0 to 1.0
                st.write(f"ATS Compatibility Score: {ats_score}/100")

                # Provide feedback based on the ATS score.
                if ats_score < 60:
                    st.warning("Your cover letter may not be well-optimized for Applicant Tracking Systems (ATS). Consider incorporating more keywords and phrases directly from the job description.")
                elif ats_score < 80:
                    st.info("Your cover letter has a good ATS compatibility score. Review the job description and consider adding a few more relevant keywords if possible.")
                else:
                    st.success("Your cover letter appears to be well-optimized for Applicant Tracking Systems (ATS).")

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
            if st.button("Regenerate Cover Letter", key=f"{subtype}_regenerate_button"):
                # Reset the generated state and content to allow the form to be displayed again.
                st.session_state.cover_letter_generated = False
                st.session_state.cover_letter_content = None # Clear generated content
                # st.session_state.cover_letter_form_data is already populated from the form submit
                st.rerun() # Rerun to show the form with previous inputs


def generate_cover_letter(subtype: str, data: Dict[str, Any]) -> str:
    """
    Generates a cover letter using the LLM by constructing a detailed prompt
    based on the collected user inputs and metadata.

    Args:
        subtype: The ID string of the cover letter subtype.
        data: A dictionary containing all collected user inputs and metadata
              (from the form and session state).

    Returns:
        The generated letter content as a string, or an error message if generation fails.
    """

    # Extract key generation parameters from the data dictionary.
    tone = data.get("tone", "Professional")
    length = data.get("length", "Standard")
    focus_area = data.get("focus_area", "Balanced")

    # Get template guidance and structure to include in the prompt.
    template = get_template_by_type("cover", subtype)
    template_guidance = template.get("guidance", "Follow standard cover letter practices.")
    template_structure = template.get("structure", ["Introduction", "Body Paragraphs", "Closing"])

    # Build the prompt string step-by-step, including all relevant details
    # from the user's input and selected options.
    prompt_parts = [
        f"Write a {length.lower()} cover letter for a {get_name_for_subtype(subtype)} position with a {tone.lower()} tone.",
        f"The letter should primarily focus on {focus_area.lower()} aspects.",
        f"Applicant Name: {data.get('full_name', '')}",
        f"Target Job Title: {data.get('job_title', '')}",
        f"Target Company: {data.get('company_name', '')}",
        f"Hiring Manager (if known): {data.get('hiring_manager', 'Not specified')}",
        f"Application Method: {data.get('application_method', 'Not specified')}",
    ]

    # Add job description if provided, as it's crucial for tailoring.
    if data.get('job_description'):
        prompt_parts.append(f"\nJob Description/Key Requirements:\n{data['job_description']}")

    # Add applicant's professional profile details.
    prompt_parts.append("\nApplicant Profile:")
    prompt_parts.append(f"- Current/Most Recent Title: {data.get('current_title', 'Not specified')}")
    prompt_parts.append(f"- Years of Relevant Experience: {data.get('years_experience', 'Not specified')}")
    if data.get('professional_summary'):
        prompt_parts.append(f"- Professional Summary: {data['professional_summary']}")

    # Add education details if applicable.
    if data.get('highest_degree') and data['highest_degree'] != "None":
        education_details = f"{data['highest_degree']}"
        if data.get('field_of_study'):
            education_details += f" in {data['field_of_study']}"
        if data.get('institution'):
            education_details += f" from {data['institution']}"
        if data.get('graduation_year'):
            education_details += f" ({data['graduation_year']})"
        prompt_parts.append(f"- Education: {education_details}")
    else:
        prompt_parts.append("- Education: Not specified")


    # Add skills and experience details.
    prompt_parts.append("\nSkills and Experience:")
    if data.get('technical_skills'):
        prompt_parts.append(f"- Technical Skills: {data['technical_skills']}")
    if data.get('soft_skills'):
        prompt_parts.append(f"- Soft Skills: {data['soft_skills']}")
    if data.get('certifications'):
        prompt_parts.append(f"- Certifications: {data['certifications']}")
    if data.get('most_relevant_achievement'):
        prompt_parts.append(f"- Most Relevant Achievement: {data['most_relevant_achievement']}")
    if data.get('additional_achievements'):
        prompt_parts.append(f"- Additional Achievements:\n{data['additional_achievements']}")

    # Add company research and interest if provided.
    if data.get('company_research'):
        prompt_parts.append(f"\nCompany Research/Understanding:\n{data['company_research']}")
    if data.get('why_interested'):
        prompt_parts.append(f"\nReason for Interest in Role/Company:\n{data['why_interested']}")

    # Add conditional information based on application method or additional options.
    if data.get('application_method') == "Referral" and data.get('referral_name'):
        prompt_parts.append(f"\nReferral: Referred by {data['referral_name']}{' (' + data['referral_relationship'] + ')' if data.get('referral_relationship') else ''}")

    if data.get('include_salary') and data.get('salary_expectations'):
        prompt_parts.append(f"\nSalary Expectations: {data['salary_expectations']}")

    if data.get('include_availability') and data.get('availability'):
        prompt_parts.append(f"\nAvailability: {data['availability']}")

    if data.get('include_relocation') and data.get('relocation_info'):
        prompt_parts.append(f"\nRelocation Information: {data['relocation_info']}")

    if data.get('include_closing') and data.get('closing_statement'):
        prompt_parts.append(f"\nCustom Closing Statement: {data['closing_statement']}")


    # Add specific instructions based on cover letter subtype.
    # These instructions guide the LLM on the specific focus for this type of letter.
    if subtype == "standard":
        prompt_parts.append("\nInstruction: This is a standard cover letter. Focus on clearly matching the applicant's qualifications to the job requirements in a professional manner.")
    elif subtype == "career_change":
        prompt_parts.append("\nInstruction: This is a career change cover letter. Emphasize transferable skills from previous roles and explain the motivation for this career transition. Clearly connect past experience and new skills to the requirements of the target role.")
    elif subtype == "entry_level":
        prompt_parts.append("\nInstruction: This is an entry-level cover letter. Focus on relevant education, coursework, projects, internships, and transferable skills. Emphasize enthusiasm, eagerness to learn, and potential for growth.")
    elif subtype == "executive":
        prompt_parts.append("\nInstruction: This is an executive-level cover letter. Emphasize strategic leadership experience, significant achievements with measurable results, and industry expertise. Use a confident, authoritative, and forward-looking tone.")
    elif subtype == "creative":
        prompt_parts.append("\nInstruction: This is a cover letter for a creative position. Use a more engaging and expressive style appropriate for a creative role while maintaining professionalism. Highlight specific creative achievements and link to the applicant's portfolio.")
    elif subtype == "technical":
        prompt_parts.append("\nInstruction: This is a cover letter for a technical position. Focus on specific technical skills, relevant projects, and problem-solving abilities. Use appropriate technical terminology accurately.")
    elif subtype == "academic":
        prompt_parts.append("\nInstruction: This is a cover letter for an academic position. Focus on research experience, teaching philosophy, publications, and contributions to the field. Use a scholarly and professional tone suitable for academia.")
    elif subtype == "remote":
        prompt_parts.append("\nInstruction: This is a cover letter for a remote position. Emphasize self-motivation, excellent communication skills (especially written), time management, and any prior experience working independently or in remote teams. Address how the applicant succeeds in a remote environment.")
    elif subtype == "referral":
        prompt_parts.append("\nInstruction: This is a referral cover letter. Mention the referral prominently and early in the letter. Explain the connection and how it aligns with the applicant's interest in the role. Still, ensure you highlight the applicant's own qualifications.")


    # Add the template structure and overall guidance to the prompt.
    # This helps the LLM understand the desired layout and writing style.
    prompt_parts.append("\nFollow this general structure:")
    for i, section in enumerate(template_structure):
        prompt_parts.append(f"{i+1}. {section}")
    prompt_parts.append(f"\nOverall Writing Guidance: {template_guidance}")

    # Add final instructions for the LLM.
    prompt_parts.append("\nMake the letter professional, concise, and tailored to the specific job and company. Avoid generic language and clichés. Focus on what the applicant can offer the employer.")


    # Combine all prompt parts into a single string.
    final_prompt = "\n".join(prompt_parts)

    # Call the LLM text generation function with the constructed prompt.
    try:
        cover_letter_content = llm_text_gen(final_prompt)
        return cover_letter_content
    except Exception as e:
        # Catch any errors during LLM generation and display an error message.
        st.error(f"Error generating cover letter: {str(e)}")
        return "Error generating cover letter. Please try again."

def calculate_ats_score(cover_letter: str, job_description: str) -> int:
    """
    Calculate a basic ATS compatibility score based on keyword matching
    between the cover letter and the job description.

    Args:
        cover_letter: The content of the cover letter.
        job_description: The content of the job description.

    Returns:
        An estimated ATS compatibility score between 0 and 100.
    """
    if not job_description or not cover_letter:
        # Return a neutral score if either is empty
        return 50

    # Convert to lowercase for case-insensitive matching
    cover_letter_lower = cover_letter.lower()
    job_description_lower = job_description.lower()

    # Define common words and punctuation to remove
    common_words = {"and", "the", "a", "an", "in", "on", "at", "to", "for", "with", "by", "of", "or", "is", "are", "be", "will", "have", "has", "had", "as", "you", "we", "they", "it", "this", "that", "these", "those", "our", "your", "their", "its", "his", "her", "him", "she", "he", "them", "us", "me", "my", "mine", "yours", "theirs", "ours", "from", "about", "which", "what", "where", "when", "how", "who", "whom", "whose", "can", "could", "would", "should", "may", "might", "must", "get", "go", "do", "does", "did", "am", "is", "are", "was", "were", "been", "being", "have", "has", "had", "do", "did", "done", "say", "says", "said", "see", "sees", "saw", "seen", "make", "makes", "made", "go", "goes", "went", "gone", "come", "comes", "came", "come", "take", "takes", "took", "taken", "give", "gives", "gave", "given", "find", "finds", "found", "get", "gets", "got", "gotten", "know", "knows", "knew", "known", "think", "thinks", "thought", "take", "takes", "took", "taken", "want", "wants", "wanted", "look", "looks", "looked", "tell", "tells", "told", "use", "uses", "used", "find", "finds", "found", "ask", "asks", "asked", "work", "works", "worked", "seem", "seems", "seemed", "feel", "feels", "felt", "become", "becomes", "became", "become", "leave", "leaves", "left", "put", "puts", "put", "bring", "brings", "brought", "begin", "begins", "began", "begun", "show", "shows", "showed", "shown", "hear", "hears", "heard", "play", "plays", "played", "run", "runs", "ran", "run", "move", "moves", "moved", "like", "likes", "liked", "believe", "believes", "believed", "hold", "holds", "held", "happen", "happens", "happened", "write", "writes", "wrote", "written", "provide", "provides", "provided", "sit", "sits", "sat", "stand", "stands", "stood", "lose", "loses", "lost", "pay", "pays", "paid", "meet", "meets", "met", "include", "includes", "included", "continue", "continues", "continued", "set", "sets", "set", "learn", "learns", "learned", "change", "changes", "changed", "lead", "leads", "led", "understand", "understands", "understood", "watch", "watches", "watched", "follow", "follows", "followed", "stop", "stops", "stopped", "create", "creates", "created", "speak", "speaks", "spoke", "spoken", "read", "reads", "read", "allow", "allows", "allowed", "add", "adds", "added", "spend", "spends", "spent", "grow", "grows", "grew", "grown", "open", "opens", "opened", "walk", "walks", "walked", "win", "wins", "won", "offer", "offers", "offered", "remember", "remembers", "remembered", "love", "loves", "loved", "consider", "considers", "considered", "appear", "appears", "appeared", "buy", "buys", "bought", "wait", "waits", "waited", "serve", "serves", "served", "die", "dies", "died", "send", "sends", "sent", "build", "builds", "built", "stay", "stays", "stayed", "fall", "falls", "fell", "fallen", "cut", "cuts", "cut", "reach", "reaches", "reached", "kill", "kills", "killed", "remain", "remains", "remained"} # Expanded list

    # Extract words from job description, filter out short and common words
    job_words = re.findall(r'\b[a-zA-Z]{3,}\b', job_description_lower)
    job_words = [word for word in job_words if word not in common_words]

    # Count frequency of each word in job description
    word_freq = Counter(job_words)

    # Get the most common words as potential keywords (top N, excluding very common words)
    # Adjust N (e.g., 30) based on typical job description length
    potential_keywords = [word for word, count in word_freq.most_common(40) if count > 1] # Increased N

    if not potential_keywords:
        # If no meaningful keywords extracted, return a neutral score
        return 50

    # Check how many potential keywords are present in the cover letter
    matches = 0
    for keyword in potential_keywords:
        # Use regex to match whole words to avoid partial matches
        if re.search(r'\b' + re.escape(keyword) + r'\b', cover_letter_lower):
            matches += 1

    # Calculate initial score based on percentage of keywords matched
    score = (matches / len(potential_keywords)) * 100

    # Adjust score based on other factors relevant to ATS:

    # Length factor (ATS prefers concise but not too short)
    word_count = len(cover_letter.split())
    if word_count < 150: # Too short
        score -= 15
    elif word_count > 500: # Potentially too long
        score -= 10
    # Add a bonus for being within a good range (e.g., 200-400 words)
    elif 200 <= word_count <= 400:
        score += 5


    # Contact information factor (essential for ATS)
    # Check for presence of key contact info indicators
    contact_indicators = ["phone", "email", "linkedin"]
    contact_score_bonus = 0
    for indicator in contact_indicators:
        if indicator in cover_letter_lower or any(indicator in val.lower() for key, val in metadata.items() if isinstance(val, str)): # Check metadata too
            contact_score_bonus += 5
    score += min(contact_score_bonus, 15) # Cap the contact bonus


    # Formatting factor (simple check for standard elements)
    # Check for salutation and closing
    if re.search(r'\bdear\b', cover_letter_lower[:100]) and re.search(r'\b(sincerely|regards)\b', cover_letter_lower[-100:]):
        score += 5

    # Check for subject line presence (important for email applications)
    if "subject:" in cover_letter_lower[:50]:
         score += 3


    # Cap the score between 0 and 100
    score = max(0, min(score, 100))

    return round(score)


def get_icon_for_subtype(subtype: str) -> str:
    """Maps a cover letter subtype ID to a relevant emoji icon."""
    icons = {
        "standard": "📝",
        "career_change": "🔄",
        "entry_level": "🌱",
        "executive": "👔",
        "creative": "🎨",
        "technical": "💻",
        "academic": "🎓",
        "remote": "🏠",
        "referral": "👥"
    }
    return icons.get(subtype, "📄") # Default icon

def get_name_for_subtype(subtype: str) -> str:
    """Maps a cover letter subtype ID to its display name."""
    names = {
        "standard": "Standard Cover Letter",
        "career_change": "Career Change Cover Letter",
        "entry_level": "Entry Level Cover Letter",
        "executive": "Executive Cover Letter",
        "creative": "Creative Cover Letter",
        "technical": "Technical Cover Letter",
        "academic": "Academic Cover Letter",
        "remote": "Remote Position Cover Letter",
        "referral": "Referral Cover Letter"
    }
    return names.get(subtype, "Cover Letter") # Default name

def get_description_for_subtype(subtype: str) -> str:
    """Maps a cover letter subtype ID to a brief description."""
    descriptions = {
        "standard": "A general purpose cover letter suitable for most job applications.",
        "career_change": "Highlight transferable skills and explain your career transition.",
        "entry_level": "Emphasize education, internships, and potential for recent graduates or those with limited experience.",
        "executive": "Showcase leadership experience and strategic vision for senior management positions.",
        "creative": "Express your creative abilities while maintaining professionalism for design, writing, or marketing roles.",
        "technical": "Demonstrate technical expertise and problem-solving abilities for IT, engineering, and other technical roles.",
        "academic": "Highlight research experience, teaching philosophy, and scholarly contributions for positions in education and research.",
        "remote": "Emphasize self-motivation, communication skills, and ability to work independently for remote positions.",
        "referral": "Leverage your connection at the company and explain how it relates to your interest in the position."
    }
    return descriptions.get(subtype, "Create a tailored cover letter for your job application.") # Default description

def get_fields_for_subtype(subtype: str) -> List[Dict[str, Any]]:
    """
    Provides a list of input field configurations specific to each cover letter subtype.
    Each dictionary in the list defines a form input field, including its ID, label,
    type, and optional properties like help text, options (for select/slider),
    min/max values (for slider/number), and a default value.
    """

    # Define subtype-specific fields.
    # Note: Many fields are common across subtypes but their *emphasis* in the prompt changes.
    # This function defines the *inputs* available on the form.
    common_fields = [] # No fields are strictly *only* common, all can be emphasized differently

    if subtype == "standard":
        return common_fields # Standard uses the general fields available in the form structure

    elif subtype == "career_change":
        # No specific *extra* fields needed, but the prompt emphasizes transferable skills and transition explanation.
        return common_fields

    elif subtype == "entry_level":
         # No specific *extra* fields needed, but the prompt emphasizes education, projects, and potential.
        return common_fields

    elif subtype == "executive":
         # No specific *extra* fields needed, but the prompt emphasizes leadership and strategic achievements.
        return common_fields

    elif subtype == "creative":
         # No specific *extra* fields needed, but the prompt emphasizes portfolio and creative process.
        return common_fields

    elif subtype == "technical":
         # No specific *extra* fields needed, but the prompt emphasizes technical skills and projects.
        return common_fields

    elif subtype == "academic":
         # No specific *extra* fields needed, but the prompt emphasizes research, teaching, and publications.
        return common_fields

    elif subtype == "remote":
         # No specific *extra* fields needed, but the prompt emphasizes remote work skills.
        return common_fields

    elif subtype == "referral":
         # No specific *extra* fields needed, but the prompt emphasizes the referral.
        return common_fields

    # Default fields if subtype is not recognized or no specific fields are defined.
    # In this cover letter module, the main form structure already defines the core fields,
    # so this fallback is less critical but included for robustness.
    return [] # Returning an empty list means no extra fields are added dynamically


def get_tones_for_subtype(subtype: str) -> List[str]:
    """Maps a cover letter subtype ID to a list of suggested tones."""
    tones = {
        "standard": ["Professional", "Confident", "Enthusiastic", "Formal"],
        "career_change": ["Professional", "Confident", "Determined", "Enthusiastic"],
        "entry_level": ["Enthusiastic", "Eager", "Professional", "Confident"],
        "executive": ["Confident", "Authoritative", "Strategic", "Professional"],
        "creative": ["Enthusiastic", "Expressive", "Professional", "Passionate"],
        "technical": ["Professional", "Analytical", "Precise", "Confident"],
        "academic": ["Scholarly", "Professional", "Analytical", "Clear"],
        "remote": ["Professional", "Self-motivated", "Communicative", "Reliable"],
        "referral": ["Professional", "Enthusiastic", "Connected", "Confident"]
    }
    # Return the list of tones for the subtype, or a default list if not found.
    return tones.get(subtype, ["Professional", "Confident", "Enthusiastic"])

# Example of how to run the app (for local development using `streamlit run your_script_name.py`)
# Uncomment the lines below to make this script directly executable.
# if __name__ == "__main__":
#     write_letter()
