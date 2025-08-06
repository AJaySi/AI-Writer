"""
Facebook Group Post Generator Module

This module provides functionality to generate engaging posts for Facebook Groups.
It helps content creators create community-focused content that drives engagement
and fosters discussion within Facebook Groups.
"""

import streamlit as st
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union, Tuple
from .....gpt_providers.text_generation.main_text_generation import llm_text_gen

# Set up logging
logger = logging.getLogger(__name__)

def write_fb_group_post():
    """
    Generate a Facebook Group post with various customization options.
    
    This function provides a comprehensive interface for creating engaging
    Facebook Group posts with features like:
    - Content customization
    - Polls and questions
    - Announcements
    - Media attachments
    - Engagement prompts
    """
    
    st.title("Facebook Group Post Generator")
    st.markdown("""
    Create engaging posts for your Facebook Groups that drive discussion and community engagement.
    Customize your content, add interactive elements, and optimize for maximum impact.
    """)
    
    # Initialize session state for form data
    if 'group_post_data' not in st.session_state:
        st.session_state.group_post_data = {
            'post_type': 'discussion',
            'content': '',
            'media_type': 'none',
            'poll_options': [],
            'question': '',
            'is_announcement': False,
            'engagement_prompt': '',
            'hashtags': [],
            'target_audience': 'all',
            'post_tone': 'professional',
            'call_to_action': 'discuss'
        }
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "Content & Media", 
        "Interactive Elements", 
        "Engagement", 
        "Preview & Export"
    ])
    
    with tab1:
        render_content_media_tab()
    
    with tab2:
        render_interactive_elements_tab()
    
    with tab3:
        render_engagement_tab()
    
    with tab4:
        render_preview_export_tab()
    
    # Generate button
    if st.button("Generate Group Post", type="primary"):
        if validate_group_post_fields():
            with st.spinner("Generating your group post..."):
                post_content = generate_group_post()
                if post_content:
                    st.session_state.group_post_data['generated_content'] = post_content
                    st.success("Group post generated successfully!")
                    st.session_state.show_preview = True

def render_content_media_tab():
    """Render the content and media input fields."""
    
    st.header("Content & Media")
    
    # Post Type Selection
    post_type = st.selectbox(
        "Post Type",
        options=['discussion', 'question', 'announcement', 'resource', 'event'],
        index=['discussion', 'question', 'announcement', 'resource', 'event'].index(
            st.session_state.group_post_data['post_type']
        ),
        help="Choose the type of post you want to create"
    )
    st.session_state.group_post_data['post_type'] = post_type
    
    # Content Input
    content = st.text_area(
        "Post Content",
        value=st.session_state.group_post_data['content'],
        height=200,
        help="Write your post content or leave blank for AI generation"
    )
    st.session_state.group_post_data['content'] = content
    
    # Media Options
    media_type = st.selectbox(
        "Media Type",
        options=['none', 'image', 'video', 'document', 'link'],
        index=['none', 'image', 'video', 'document', 'link'].index(
            st.session_state.group_post_data['media_type']
        ),
        help="Add media to your post"
    )
    st.session_state.group_post_data['media_type'] = media_type
    
    if media_type != 'none':
        if media_type == 'image':
            st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])
        elif media_type == 'video':
            st.file_uploader("Upload Video", type=['mp4', 'mov'])
        elif media_type == 'document':
            st.file_uploader("Upload Document", type=['pdf', 'doc', 'docx'])
        elif media_type == 'link':
            st.text_input("Enter URL", help="Paste the URL you want to share")

def render_interactive_elements_tab():
    """Render the interactive elements options."""
    
    st.header("Interactive Elements")
    
    # Poll Creation
    if st.checkbox("Add Poll", help="Create a poll for group members"):
        poll_question = st.text_input("Poll Question")
        poll_options = []
        for i in range(4):
            option = st.text_input(f"Option {i+1}")
            if option:
                poll_options.append(option)
        st.session_state.group_post_data['poll_options'] = poll_options
    
    # Question Creation
    if st.checkbox("Add Question", help="Ask a question to group members"):
        question = st.text_input("Your Question")
        st.session_state.group_post_data['question'] = question
    
    # Announcement Toggle
    is_announcement = st.checkbox(
        "Mark as Announcement",
        value=st.session_state.group_post_data['is_announcement'],
        help="Pin this post as an announcement in the group"
    )
    st.session_state.group_post_data['is_announcement'] = is_announcement

def render_engagement_tab():
    """Render the engagement options."""
    
    st.header("Engagement Settings")
    
    # Engagement Prompt
    engagement_prompt = st.text_area(
        "Engagement Prompt",
        value=st.session_state.group_post_data['engagement_prompt'],
        help="Add a prompt to encourage comments and discussion"
    )
    st.session_state.group_post_data['engagement_prompt'] = engagement_prompt
    
    # Target Audience
    target_audience = st.selectbox(
        "Target Audience",
        options=['all', 'new_members', 'active_members', 'specific_role'],
        index=['all', 'new_members', 'active_members', 'specific_role'].index(
            st.session_state.group_post_data['target_audience']
        ),
        help="Select who this post is primarily for"
    )
    st.session_state.group_post_data['target_audience'] = target_audience
    
    # Post Tone
    post_tone = st.selectbox(
        "Post Tone",
        options=['professional', 'casual', 'friendly', 'formal', 'humorous'],
        index=['professional', 'casual', 'friendly', 'formal', 'humorous'].index(
            st.session_state.group_post_data['post_tone']
        ),
        help="Choose the tone for your post"
    )
    st.session_state.group_post_data['post_tone'] = post_tone
    
    # Call to Action
    call_to_action = st.selectbox(
        "Call to Action",
        options=['discuss', 'share', 'learn', 'participate', 'feedback'],
        index=['discuss', 'share', 'learn', 'participate', 'feedback'].index(
            st.session_state.group_post_data['call_to_action']
        ),
        help="What action do you want members to take?"
    )
    st.session_state.group_post_data['call_to_action'] = call_to_action

def render_preview_export_tab():
    """Render the preview and export options."""
    
    st.header("Preview & Export")
    
    if 'generated_content' in st.session_state.group_post_data:
        st.subheader("Generated Post")
        st.markdown(st.session_state.group_post_data['generated_content'])
        
        # Export options
        st.subheader("Export Options")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Copy to Clipboard"):
                st.code(st.session_state.group_post_data['generated_content'])
        
        with col2:
            if st.button("Download as Text"):
                download_group_post(st.session_state.group_post_data['generated_content'])

def validate_group_post_fields() -> bool:
    """Validate the group post fields."""
    
    data = st.session_state.group_post_data
    
    # Basic validation rules
    validation_rules = {
        'post_type': {'required': True, 'type': str},
        'content': {'required': False, 'type': str},
        'media_type': {'required': True, 'type': str},
        'poll_options': {'required': False, 'type': list},
        'question': {'required': False, 'type': str},
        'is_announcement': {'required': True, 'type': bool},
        'engagement_prompt': {'required': False, 'type': str},
        'target_audience': {'required': True, 'type': str},
        'post_tone': {'required': True, 'type': str},
        'call_to_action': {'required': True, 'type': str}
    }
    
    errors = []
    
    for field, rules in validation_rules.items():
        value = data.get(field)
        
        # Skip validation for optional fields if empty
        if not rules['required'] and not value:
            continue
            
        # Type validation
        if value and not isinstance(value, rules['type']):
            errors.append(f"{field.replace('_', ' ').title()} must be of type {rules['type'].__name__}")
            continue
            
        # Required field validation
        if rules['required'] and not value:
            errors.append(f"{field.replace('_', ' ').title()} is required")
    
    if errors:
        for error in errors:
            st.error(error)
        return False
    
    return True

def generate_group_post() -> Optional[str]:
    """Generate the group post content using AI."""
    
    try:
        data = st.session_state.group_post_data
        
        # Prepare the prompt for the LLM
        prompt = f"""
        Create a Facebook Group post with the following specifications:
        
        Post Type: {data['post_type']}
        Content: {data['content'] if data['content'] else 'Generate engaging content'}
        Media Type: {data['media_type']}
        Target Audience: {data['target_audience']}
        Post Tone: {data['post_tone']}
        Call to Action: {data['call_to_action']}
        
        Additional Elements:
        - Poll Options: {', '.join(data['poll_options']) if data['poll_options'] else 'None'}
        - Question: {data['question'] if data['question'] else 'None'}
        - Is Announcement: {data['is_announcement']}
        - Engagement Prompt: {data['engagement_prompt'] if data['engagement_prompt'] else 'None'}
        
        The post should be engaging, community-focused, and encourage discussion.
        Include appropriate formatting, emojis, and hashtags where relevant.
        """
        
        # Get response from LLM
        response = llm_text_gen(prompt)
        
        if response:
            return response
        else:
            st.error("Failed to generate group post content. Please try again.")
            return None
            
    except Exception as e:
        logger.error(f"Error generating group post: {str(e)}")
        st.error("An error occurred while generating the group post. Please try again.")
        return None

def download_group_post(content: str):
    """Download the generated group post as a text file."""
    
    try:
        # Create a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"facebook_group_post_{timestamp}.txt"
        
        # Create the download button
        st.download_button(
            label="Download Post",
            data=content,
            file_name=filename,
            mime="text/plain"
        )
    except Exception as e:
        logger.error(f"Error downloading group post: {str(e)}")
        st.error("An error occurred while downloading the post. Please try again.") 