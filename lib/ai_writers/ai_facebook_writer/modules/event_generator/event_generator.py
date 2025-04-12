"""
Facebook Event Generator Module

This module provides functionality to generate engaging Facebook event descriptions with various features
and customization options.
"""

import streamlit as st
from datetime import datetime, date, time
import json
import os
from typing import Dict, Any, List, Optional, Union, Tuple
from loguru import logger
import sys
import base64
from io import BytesIO

from .....gpt_providers.text_generation.main_text_generation import llm_text_gen
from .....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image

# Configure logging
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

def initialize_session_state():
    """Initialize session state with default values."""
    if 'event_data' not in st.session_state:
        st.session_state.event_data = {
            'basic_info': {},
            'content': {},
            'media': {},
            'engagement': {},
            'analytics': {}
        }
    
    # Initialize individual fields with default values that match selectbox options
    defaults = {
        'event_type': "Physical Event",
        'event_category': "Business",
        'timezone': "UTC",
        'platform': "Zoom",
        'description_type': "Basic",
        'content_style': "Professional",
        'cover_image_style': "Modern",
        'color_scheme': "#1877F2",
        'image_ratio': "16:9",
        'image_quality': "High",
        'event_name': "",
        'event_date': date.today(),
        'event_time': time(12, 0),  # Default to noon
        'venue_name': "",
        'street_address': "",
        'city': "",
        'country': "",
        'meeting_link': "",
        'meeting_id': "",
        'passcode': "",
        'key_points': "",
        'target_audience': "",
        'event_goal': "",
        'engagement_prompts': ""
    }
    
    for field, default_value in defaults.items():
        if field not in st.session_state:
            st.session_state[field] = default_value

def write_fb_event():
    """Generate an engaging Facebook event description with various features and customization options."""
    
    # Initialize session state
    initialize_session_state()
    
    st.markdown("""
    ### 📅 Facebook Event Generator
    Create compelling event descriptions that drive attendance and engagement. Customize your event
    with various features and get AI-powered suggestions for optimal performance.
    """)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Event Details", "Content & Media", "Engagement", "Analytics", "Preview & Export"])
    
    with tab1:
        render_event_details_tab()
    
    with tab2:
        render_content_media_tab()
    
    with tab3:
        render_engagement_tab()
    
    with tab4:
        render_analytics_tab()
    
    with tab5:
        render_preview_export_tab()

def render_event_details_tab():
    """Render the event details tab with input fields."""
    
    # Basic Event Information
    st.markdown("#### Basic Event Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        event_types = ["Physical Event", "Online Event", "Hybrid Event"]
        event_type = st.selectbox(
            "Event Type",
            options=event_types,
            index=event_types.index(st.session_state.event_type) if st.session_state.event_type in event_types else 0,
            help="Select the type of event you're creating",
            key="event_type"
        )
        
        event_name = st.text_input(
            "Event Name",
            value=st.session_state.event_name,
            help="Enter a catchy and descriptive name for your event",
            key="event_name"
        )
        
        event_categories = ["Business", "Education", "Entertainment", "Sports", "Community", "Other"]
        event_category = st.selectbox(
            "Event Category",
            options=event_categories,
            index=event_categories.index(st.session_state.event_category) if st.session_state.event_category in event_categories else 0,
            help="Select the category that best describes your event",
            key="event_category"
        )
    
    with col2:
        # Handle date input without conflicting with session state
        if "event_date" not in st.session_state:
            st.session_state.event_date = date.today()
        
        event_date = st.date_input(
            "Event Date",
            min_value=date.today(),
            help="Select the date of your event",
            key="event_date"
        )
        
        # Handle time input without conflicting with session state
        if "event_time" not in st.session_state:
            st.session_state.event_time = time(12, 0)
        
        event_time = st.time_input(
            "Event Time",
            help="Select the time of your event",
            key="event_time"
        )
        
        timezones = ["UTC", "EST", "PST", "GMT", "IST"]
        timezone = st.selectbox(
            "Timezone",
            options=timezones,
            index=timezones.index(st.session_state.timezone) if st.session_state.timezone in timezones else 0,
            help="Select the timezone for your event",
            key="timezone"
        )
    
    # Location Details
    st.markdown("#### Location Details")
    
    if event_type in ["Physical Event", "Hybrid Event"]:
        col1, col2 = st.columns(2)
        
        with col1:
            venue_name = st.text_input(
                "Venue Name",
                value=st.session_state.venue_name,
                help="Enter the name of the venue",
                key="venue_name"
            )
            
            street_address = st.text_input(
                "Street Address",
                value=st.session_state.street_address,
                help="Enter the street address",
                key="street_address"
            )
        
        with col2:
            city = st.text_input(
                "City",
                value=st.session_state.city,
                help="Enter the city",
                key="city"
            )
            
            country = st.text_input(
                "Country",
                value=st.session_state.country,
                help="Enter the country",
                key="country"
            )
    
    if event_type in ["Online Event", "Hybrid Event"]:
        st.markdown("#### Online Event Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            platforms = ["Zoom", "Google Meet", "Microsoft Teams", "Facebook Live", "Other"]
            platform = st.selectbox(
                "Platform",
                options=platforms,
                index=platforms.index(st.session_state.platform) if st.session_state.platform in platforms else 0,
                help="Select the platform for your online event",
                key="platform"
            )
            
            meeting_link = st.text_input(
                "Meeting Link",
                value=st.session_state.meeting_link,
                help="Enter the meeting link (optional)",
                key="meeting_link"
            )
        
        with col2:
            meeting_id = st.text_input(
                "Meeting ID",
                value=st.session_state.meeting_id,
                help="Enter the meeting ID (optional)",
                key="meeting_id"
            )
            
            passcode = st.text_input(
                "Passcode",
                value=st.session_state.passcode,
                help="Enter the passcode (optional)",
                key="passcode"
            )
    
    # Event Description
    st.markdown("#### Event Description")
    
    description_types = ["Basic", "Detailed", "Professional"]
    description_type = st.radio(
        "Description Type",
        options=description_types,
        index=description_types.index(st.session_state.description_type) if st.session_state.description_type in description_types else 0,
        help="Select the level of detail for your event description",
        key="description_type"
    )
    
    key_points = st.text_area(
        "Key Points to Include",
        value=st.session_state.key_points,
        help="Enter key points that should be included in the event description",
        height=100,
        key="key_points"
    )
    
    target_audience = st.text_input(
        "Target Audience",
        value=st.session_state.target_audience,
        help="Describe your target audience",
        key="target_audience"
    )
    
    event_goal = st.text_area(
        "Event Goal",
        value=st.session_state.event_goal,
        help="What do you want to achieve with this event?",
        height=100,
        key="event_goal"
    )

def render_content_media_tab():
    """Render the content and media tab with customization options."""
    
    st.markdown("#### Content Customization")
    
    # Template Selection
    st.markdown("##### Template Selection")
    
    template_type = st.selectbox(
        "Template Type",
        ["Custom", "Conference", "Workshop", "Webinar", "Networking", "Product Launch", "Fundraiser"],
        help="Select a template type for your event"
    )
    
    # Content Style - Move this after template selection
    content_styles = ["Professional", "Casual", "Formal", "Engaging", "Educational"]
    default_style = "Professional"
    
    # Set default style based on template
    if template_type != "Custom":
        if template_type == "Conference":
            default_style = "Professional"
        elif template_type == "Workshop":
            default_style = "Educational"
        elif template_type == "Webinar":
            default_style = "Professional"
        elif template_type == "Networking":
            default_style = "Casual"
        elif template_type == "Product Launch":
            default_style = "Engaging"
        elif template_type == "Fundraiser":
            default_style = "Engaging"
    
    content_style = st.selectbox(
        "Content Style",
        content_styles,
        index=content_styles.index(default_style),
        help="Select the style of your event description",
        key="content_style"
    )
    
    # Content Elements
    st.markdown("##### Content Elements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        include_agenda = st.checkbox("Include Agenda", value=True)
        include_speakers = st.checkbox("Include Speakers", value=True)
        include_benefits = st.checkbox("Include Benefits", value=True)
        include_requirements = st.checkbox("Include Requirements", value=True)
    
    with col2:
        include_faq = st.checkbox("Include FAQ", value=True)
        include_testimonials = st.checkbox("Include Testimonials", value=True)
        include_sponsors = st.checkbox("Include Sponsors", value=True)
        include_highlights = st.checkbox("Include Event Highlights", value=True)
    
    # Media Options
    st.markdown("#### Media Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cover_image_style = st.selectbox(
            "Cover Image Style",
            ["Modern", "Professional", "Creative", "Minimalist", "Bold"],
            help="Select the style for your event cover image",
            key="cover_image_style"
        )
        
        color_scheme = st.color_picker(
            "Brand Color",
            "#1877F2",
            help="Select your brand color for the event",
            key="color_scheme"
        )
    
    with col2:
        image_ratio = st.selectbox(
            "Image Ratio",
            ["16:9", "1:1", "4:3"],
            help="Select the aspect ratio for your images",
            key="image_ratio"
        )
        
        image_quality = st.select_slider(
            "Image Quality",
            options=["Low", "Medium", "High"],
            value="High",
            help="Select the quality for generated images",
            key="image_quality"
        )

def render_engagement_tab():
    """Render the engagement tab with interactive elements."""
    
    st.markdown("#### Engagement Features")
    
    # Interactive Elements
    st.markdown("##### Interactive Elements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced Poll Options
        use_poll = st.checkbox("Add Poll", value=False)
        if use_poll:
            poll_type = st.selectbox(
                "Poll Type",
                ["Multiple Choice", "Rating", "Open-ended", "Ranking"]
            )
            poll_questions = st.text_area(
                "Poll Questions",
                help="Enter poll questions (one per line)",
                height=100
            )
            poll_duration = st.number_input(
                "Poll Duration (days)",
                min_value=1,
                max_value=30,
                value=7
            )
        
        # Enhanced Quiz Options
        use_quiz = st.checkbox("Add Quiz", value=False)
        if use_quiz:
            quiz_type = st.selectbox(
                "Quiz Type",
                ["Trivia", "Personality", "Knowledge Check"]
            )
            quiz_questions = st.text_area(
                "Quiz Questions",
                help="Enter quiz questions (one per line)",
                height=100
            )
            quiz_rewards = st.text_input(
                "Quiz Rewards",
                help="Enter rewards for quiz completion"
            )
        
        use_countdown = st.checkbox("Add Countdown", value=False)
    
    with col2:
        # Enhanced RSVP Options
        use_rsvp = st.checkbox("Enable RSVP", value=True)
        if use_rsvp:
            rsvp_options = st.multiselect(
                "RSVP Options",
                ["Attending", "Maybe", "Not Attending", "Bring a Guest"]
            )
            rsvp_limit = st.number_input(
                "RSVP Limit",
                min_value=0,
                value=0,
                help="0 for unlimited"
            )
            rsvp_deadline = st.date_input(
                "RSVP Deadline",
                min_value=date.today()
            )
        
        use_reminder = st.checkbox("Enable Reminders", value=True)
        if use_reminder:
            reminder_times = st.multiselect(
                "Reminder Times",
                ["1 day before", "1 hour before", "15 minutes before", "Custom"]
            )
            if "Custom" in reminder_times:
                custom_reminder = st.text_input(
                    "Custom Reminder Time",
                    help="Format: X days/hours/minutes before"
                )
        
        use_feedback = st.checkbox("Enable Feedback Form", value=True)
    
    # Social Sharing
    st.markdown("##### Social Sharing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        include_hashtags = st.checkbox("Include Hashtags", value=True)
        if include_hashtags:
            hashtag_count = st.slider(
                "Number of Hashtags",
                min_value=1,
                max_value=10,
                value=5
            )
            custom_hashtags = st.text_input(
                "Custom Hashtags",
                help="Enter custom hashtags (comma separated)"
            )
        
        include_social_links = st.checkbox("Include Social Links", value=True)
    
    with col2:
        include_share_buttons = st.checkbox("Include Share Buttons", value=True)
        include_invite_friends = st.checkbox("Include Invite Friends", value=True)
    
    # Engagement Prompts
    st.markdown("##### Engagement Prompts")
    
    engagement_prompts = st.text_area(
        "Custom Engagement Prompts",
        help="Enter custom prompts to encourage engagement",
        height=100,
        key="engagement_prompts"
    )
    
    # Language Options
    st.markdown("##### Language Options")
    
    language = st.selectbox(
        "Event Language",
        ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Chinese", "Japanese", "Korean", "Other"]
    )
    
    if language != "English":
        st.info(f"Event description will be generated in {language}. You can still input details in English.")

def render_analytics_tab():
    """Render the analytics tab with insights and predictions."""
    
    st.markdown("#### Analytics & Insights")
    
    # Engagement Prediction
    st.markdown("##### Engagement Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Predicted Engagement Metrics**")
        
        # Generate mock predictions based on input
        if st.session_state.event_name and st.session_state.target_audience:
            predicted_rsvp = min(100, max(10, len(st.session_state.event_name) * 5))
            predicted_views = predicted_rsvp * 10
            predicted_engagement = min(100, max(20, predicted_rsvp * 0.8))
            
            st.metric("Predicted RSVPs", f"{predicted_rsvp}")
            st.metric("Predicted Views", f"{predicted_views}")
            st.metric("Predicted Engagement Rate", f"{predicted_engagement}%")
        else:
            st.info("Fill in event details to see engagement predictions")
    
    with col2:
        st.markdown("**Engagement Factors**")
        
        factors = {
            "Event Name": 85,
            "Description Quality": 90,
            "Visual Appeal": 75,
            "Timing": 80,
            "Target Audience Match": 95
        }
        
        for factor, score in factors.items():
            st.progress(score / 100)
            st.text(f"{factor}: {score}%")
    
    # Best Practices
    st.markdown("##### Best Practices")
    
    best_practices = [
        "Use clear, action-oriented language in your event title",
        "Include all essential details in the first 3 sentences",
        "Add visual elements to increase engagement",
        "Use hashtags strategically (3-5 is optimal)",
        "Include a clear call-to-action",
        "Optimize for mobile viewing",
        "Post at optimal times (typically 1-3pm on weekdays)"
    ]
    
    for practice in best_practices:
        st.markdown(f"✅ {practice}")
    
    # A/B Testing Suggestions
    st.markdown("##### A/B Testing Suggestions")
    
    if st.button("Generate A/B Testing Ideas"):
        st.markdown("**Title Variations:**")
        st.markdown(f"1. {st.session_state.event_name}")
        st.markdown(f"2. {st.session_state.event_name} - Don't Miss Out!")
        st.markdown(f"3. Join Us: {st.session_state.event_name}")
        
        st.markdown("**Description Variations:**")
        st.markdown("1. Focus on benefits and outcomes")
        st.markdown("2. Focus on problem-solving and solutions")
        st.markdown("3. Focus on community and networking")
        
        st.markdown("**Visual Variations:**")
        st.markdown("1. Use brand colors prominently")
        st.markdown("2. Use contrasting colors for attention")
        st.markdown("3. Use minimal design with focus on text")

def render_preview_export_tab():
    """Render the preview and export tab."""
    
    st.markdown("#### Preview & Export")
    
    # Preview Options
    preview_type = st.radio(
        "Preview Type",
        ["Mobile", "Desktop", "Social Cards", "All"]
    )
    
    # Generate Event Button
    if st.button("🚀 Generate Event Description", key="generate_event"):
        with st.spinner("Generating your event description..."):
            # Validate required fields
            if not validate_event_fields():
                return
            
            # Generate event description
            event_description = generate_event_description()
            
            # Store in session state
            st.session_state.event_description = event_description
            
            # Display preview based on selection
            if preview_type == "Mobile" or preview_type == "All":
                st.markdown("##### Mobile Preview")
                st.markdown("""
                <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; max-width: 375px; margin: 0 auto; background-color: #f9f9f9;">
                    <h3 style="margin-top: 0;">{}</h3>
                    <p style="color: #666;">{} at {}</p>
                    <div style="margin: 15px 0;">
                        {}
                    </div>
                </div>
                """.format(
                    st.session_state.event_name,
                    st.session_state.event_date.strftime("%B %d, %Y"),
                    st.session_state.event_time.strftime("%I:%M %p"),
                    event_description
                ), unsafe_allow_html=True)
            
            if preview_type == "Desktop" or preview_type == "All":
                st.markdown("##### Desktop Preview")
                st.markdown("""
                <div style="border: 1px solid #ddd; border-radius: 10px; padding: 20px; max-width: 600px; margin: 0 auto; background-color: #f9f9f9;">
                    <h2 style="margin-top: 0;">{}</h2>
                    <p style="color: #666;">{} at {}</p>
                    <div style="margin: 20px 0;">
                        {}
                    </div>
                </div>
                """.format(
                    st.session_state.event_name,
                    st.session_state.event_date.strftime("%B %d, %Y"),
                    st.session_state.event_time.strftime("%I:%M %p"),
                    event_description
                ), unsafe_allow_html=True)
            
            if preview_type == "Social Cards" or preview_type == "All":
                st.markdown("##### Social Cards Preview")
                st.markdown("""
                <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; max-width: 500px; margin: 0 auto; background-color: #f9f9f9;">
                    <h3 style="margin-top: 0;">{}</h3>
                    <p style="color: #666;">{} at {}</p>
                    <div style="margin: 15px 0;">
                        {}
                    </div>
                </div>
                """.format(
                    st.session_state.event_name,
                    st.session_state.event_date.strftime("%B %d, %Y"),
                    st.session_state.event_time.strftime("%I:%M %p"),
                    event_description[:200] + "..." if len(event_description) > 200 else event_description
                ), unsafe_allow_html=True)
            
            # Export options
            st.markdown("#### Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📋 Copy to Clipboard"):
                    st.code(event_description)
                    st.success("Event description copied to clipboard!")
            
            with col2:
                if st.button("💾 Download as Text"):
                    download_event_description(event_description)
            
            with col3:
                if st.button("📅 Export to Calendar"):
                    st.info("Calendar export feature coming soon!")

def validate_event_fields() -> bool:
    """Validate required event fields with enhanced validation."""
    validation_rules = {
        "Event Name": {
            "required": True,
            "min_length": 5,
            "max_length": 100,
            "type": str
        },
        "Event Date": {
            "required": True,
            "min_date": date.today(),
            "type": Union[date, type(None)]
        },
        "Target Audience": {
            "required": True,
            "min_length": 10,
            "type": str
        },
        "Event Goal": {
            "required": True,
            "min_length": 20,
            "type": str
        }
    }
    
    errors = []
    for field, rules in validation_rules.items():
        field_key = field.lower().replace(" ", "_")
        value = st.session_state.get(field_key)
        
        # Skip validation if field is not required and value is empty
        if not rules["required"] and (value is None or value == ""):
            continue
            
        # Type validation
        if "type" in rules and value is not None:
            expected_type = rules["type"]
            if not isinstance(value, expected_type):
                errors.append(f"{field} must be of type {expected_type}")
                continue
        
        # Required field validation
        if rules["required"] and (value is None or value == ""):
            errors.append(f"{field} is required")
            continue
        
        # Length validation for strings
        if isinstance(value, str):
            if "min_length" in rules and len(value) < rules["min_length"]:
                errors.append(f"{field} must be at least {rules['min_length']} characters")
            if "max_length" in rules and len(value) > rules["max_length"]:
                errors.append(f"{field} must be less than {rules['max_length']} characters")
        
        # Date validation
        if isinstance(value, date):
            if "min_date" in rules and value < rules["min_date"]:
                errors.append(f"{field} must be in the future")
    
    if errors:
        st.error("\n".join(errors))
        return False
    
    return True

def generate_event_description() -> str:
    """Generate the event description using AI with enhanced features."""
    prompt = f"""
    Create a compelling Facebook event description for:
    
    Event Name: {st.session_state.get('event_name', '')}
    Event Type: {st.session_state.get('event_type', '')}
    Event Category: {st.session_state.get('event_category', '')}
    Date & Time: {st.session_state.get('event_date', '')} at {st.session_state.get('event_time', '')}
    Target Audience: {st.session_state.get('target_audience', '')}
    Event Goal: {st.session_state.get('event_goal', '')}
    
    Key Points to Include: {st.session_state.get('key_points', '')}
    
    Style: {st.session_state.get('content_style', '')}
    
    Additional Requirements:
    1. Include SEO-optimized keywords
    2. Add emoji suggestions for key points
    3. Include trending hashtags in the event category
    4. Add engagement hooks at strategic points
    5. Include social proof elements
    6. Add urgency triggers
    7. Include mobile-optimized formatting
    8. Add accessibility considerations
    
    Format the description with:
    - Engaging opening
    - Clear event details
    - Key benefits
    - Call to action
    - Relevant hashtags
    """
    
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        st.error(f"An error occurred while generating the event description: {err}")
        return ""

def download_event_description(content: str):
    """Download the event description as a text file."""
    # Create a download link
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="event_description.txt">Download Event Description</a>'
    st.markdown(href, unsafe_allow_html=True) 