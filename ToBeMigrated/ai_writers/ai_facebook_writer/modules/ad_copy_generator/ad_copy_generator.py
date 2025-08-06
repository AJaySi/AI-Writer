"""
Facebook Ad Copy Generator Module

This module provides functionality to generate high-converting ad copy for Facebook Ads.
It helps marketers create compelling ad content with targeting suggestions and
performance optimization features.
"""

import streamlit as st
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union, Tuple
from .....gpt_providers.text_generation.main_text_generation import llm_text_gen

# Set up logging
logger = logging.getLogger(__name__)

def write_fb_ad_copy():
    """
    Generate Facebook Ad copy with various customization options.
    
    This function provides a comprehensive interface for creating high-converting
    ad copy for Facebook Ads with features like:
    - Ad objective and format selection
    - Target audience configuration
    - Ad content customization
    - Call-to-action optimization
    - Preview and export options
    """
    
    st.title("Facebook Ad Copy Generator")
    st.markdown("""
    Create high-converting ad copy for your Facebook Ads with AI-powered suggestions
    and targeting recommendations.
    """)
    
    # Initialize session state for form data
    if 'ad_copy_data' not in st.session_state:
        st.session_state.ad_copy_data = {
            # Ad Objective & Format
            'objective': 'awareness',
            'format': 'single_image',
            'campaign_name': '',
            'budget_range': (100, 1000),
            'placements': ['feed'],
            
            # Target Audience
            'age_range': (18, 65),
            'gender': 'all',
            'location': '',
            'interests': [],
            'behaviors': [],
            'custom_audience': '',
            'lookalike_source': '',
            
            # Ad Content
            'primary_headline': '',
            'secondary_headline': '',
            'description': '',
            'link_description': '',
            'brand_voice': 'professional',
            'key_points': [],
            'usp': '',
            
            # Call-to-Action
            'cta_type': 'learn_more',
            'cta_text': '',
            'use_urgency': False,
            'offer_details': '',
            
            # Content Length
            'content_length': 'standard',
            
            # Generated Content
            'generated_content': '',
            'show_preview': False,
            'variations': []
        }
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Ad Objective & Format",
        "Target Audience",
        "Ad Content",
        "Call-to-Action",
        "Preview & Export"
    ])
    
    with tab1:
        render_objective_format_tab()
    
    with tab2:
        render_target_audience_tab()
    
    with tab3:
        render_ad_content_tab()
    
    with tab4:
        render_cta_tab()
    
    with tab5:
        render_preview_export_tab()
    
    # Generate button
    if st.button("Generate Ad Copy", type="primary"):
        if validate_ad_copy_fields():
            with st.spinner("Generating your ad copy..."):
                ad_content = generate_ad_copy()
                if ad_content:
                    st.session_state.ad_copy_data['generated_content'] = ad_content
                    st.success("Ad copy generated successfully!")
                    st.session_state.ad_copy_data['show_preview'] = True
                    # Generate variations for A/B testing
                    variations = generate_ad_variations()
                    if variations:
                        st.session_state.ad_copy_data['variations'] = variations
                    st.rerun()

def render_objective_format_tab():
    """Render the ad objective and format selection fields."""
    
    st.header("Ad Objective & Format")
    
    # Ad Objective
    objective = st.selectbox(
        "Ad Objective",
        options=['awareness', 'traffic', 'engagement', 'leads', 'app_promotion', 'sales', 'conversions'],
        index=['awareness', 'traffic', 'engagement', 'leads', 'app_promotion', 'sales', 'conversions'].index(
            st.session_state.ad_copy_data['objective']
        ),
        help="Choose the main objective of your ad campaign"
    )
    st.session_state.ad_copy_data['objective'] = objective
    
    # Ad Format
    format_col1, format_col2 = st.columns(2)
    
    with format_col1:
        ad_format = st.selectbox(
            "Ad Format",
            options=['single_image', 'carousel', 'video', 'collection', 'instant_experience'],
            index=['single_image', 'carousel', 'video', 'collection', 'instant_experience'].index(
                st.session_state.ad_copy_data['format']
            ),
            help="Choose the format of your ad"
        )
        st.session_state.ad_copy_data['format'] = ad_format
    
    with format_col2:
        # Show format preview
        st.image(
            f"https://via.placeholder.com/600x300?text={ad_format.replace('_', ' ').title()}+Coming+Soon",
            caption=f"{ad_format.replace('_', ' ').title()} Format Example",
            use_container_width=True
        )
    
    # Campaign Setup
    st.subheader("Campaign Setup")
    
    campaign_name = st.text_input(
        "Campaign Name",
        value=st.session_state.ad_copy_data['campaign_name'],
        help="Enter a name for your ad campaign"
    )
    st.session_state.ad_copy_data['campaign_name'] = campaign_name
    
    # Budget Range
    budget_range = st.slider(
        "Budget Range ($)",
        min_value=1,
        max_value=10000,
        value=st.session_state.ad_copy_data['budget_range'],
        help="Set your campaign budget range"
    )
    st.session_state.ad_copy_data['budget_range'] = budget_range
    
    # Ad Placements
    placement_options = [
        'feed', 'stories', 'messenger', 'marketplace', 'video_feeds',
        'in_stream', 'search', 'instagram', 'audience_network'
    ]
    
    placements = st.multiselect(
        "Ad Placements",
        options=placement_options,
        default=st.session_state.ad_copy_data['placements'],
        help="Choose where your ad will appear"
    )
    st.session_state.ad_copy_data['placements'] = placements

def render_target_audience_tab():
    """Render the target audience configuration fields."""
    
    st.header("Target Audience")
    
    # Demographics
    st.subheader("Demographics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age_range = st.slider(
            "Age Range",
            min_value=13,
            max_value=65,
            value=st.session_state.ad_copy_data['age_range'],
            help="Select target age range"
        )
        st.session_state.ad_copy_data['age_range'] = age_range
    
    with col2:
        gender = st.selectbox(
            "Gender",
            options=['all', 'male', 'female'],
            index=['all', 'male', 'female'].index(
                st.session_state.ad_copy_data['gender']
            ),
            help="Select target gender"
        )
        st.session_state.ad_copy_data['gender'] = gender
    
    location = st.text_input(
        "Location",
        value=st.session_state.ad_copy_data['location'],
        help="Enter target location (city, state, country)"
    )
    st.session_state.ad_copy_data['location'] = location
    
    # Interests
    st.subheader("Interests")
    
    # Initialize interests in session state if not present
    if 'interests' not in st.session_state.ad_copy_data:
        st.session_state.ad_copy_data['interests'] = []
    
    # Add new interest
    new_interest = st.text_input("Add an interest", key="new_interest")
    if st.button("Add Interest") and new_interest:
        if new_interest not in st.session_state.ad_copy_data['interests']:
            st.session_state.ad_copy_data['interests'].append(new_interest)
            st.rerun()
    
    # Display and allow removal of existing interests
    if st.session_state.ad_copy_data['interests']:
        st.write("Current Interests:")
        for i, interest in enumerate(st.session_state.ad_copy_data['interests']):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{i+1}. {interest}")
            with col2:
                if st.button("Remove", key=f"remove_interest_{i}"):
                    st.session_state.ad_copy_data['interests'].pop(i)
                    st.rerun()
    
    # Behaviors
    st.subheader("Behaviors")
    
    behavior_options = [
        'engaged_shoppers',
        'frequent_travelers',
        'technology_early_adopters',
        'small_business_owners',
        'mobile_users',
        'luxury_shoppers'
    ]
    
    behaviors = st.multiselect(
        "Select Behaviors",
        options=behavior_options,
        default=st.session_state.ad_copy_data['behaviors'],
        help="Choose relevant user behaviors"
    )
    st.session_state.ad_copy_data['behaviors'] = behaviors
    
    # Custom & Lookalike Audiences
    st.subheader("Advanced Targeting")
    
    custom_audience = st.text_area(
        "Custom Audience Source",
        value=st.session_state.ad_copy_data['custom_audience'],
        help="Describe your custom audience source (e.g., email list, website visitors)",
        height=100
    )
    st.session_state.ad_copy_data['custom_audience'] = custom_audience
    
    lookalike_source = st.text_area(
        "Lookalike Audience Source",
        value=st.session_state.ad_copy_data['lookalike_source'],
        help="Describe your lookalike audience source",
        height=100
    )
    st.session_state.ad_copy_data['lookalike_source'] = lookalike_source

def render_ad_content_tab():
    """Render the ad content configuration fields."""
    
    st.header("Ad Content")
    
    # Headlines
    st.subheader("Headlines")
    
    primary_headline = st.text_input(
        "Primary Headline",
        value=st.session_state.ad_copy_data['primary_headline'],
        help="Enter your main headline (max 40 characters)",
        max_chars=40
    )
    st.session_state.ad_copy_data['primary_headline'] = primary_headline
    
    secondary_headline = st.text_input(
        "Secondary Headline (optional)",
        value=st.session_state.ad_copy_data['secondary_headline'],
        help="Enter a secondary headline (max 40 characters)",
        max_chars=40
    )
    st.session_state.ad_copy_data['secondary_headline'] = secondary_headline
    
    # Description
    description = st.text_area(
        "Ad Description",
        value=st.session_state.ad_copy_data['description'],
        help="Enter your ad description (max 125 characters)",
        max_chars=125,
        height=100
    )
    st.session_state.ad_copy_data['description'] = description
    
    # Link Description
    link_description = st.text_input(
        "Link Description",
        value=st.session_state.ad_copy_data['link_description'],
        help="Enter your link description (max 30 characters)",
        max_chars=30
    )
    st.session_state.ad_copy_data['link_description'] = link_description
    
    # Brand Voice
    brand_voice = st.selectbox(
        "Brand Voice",
        options=['professional', 'friendly', 'casual', 'formal', 'humorous'],
        index=['professional', 'friendly', 'casual', 'formal', 'humorous'].index(
            st.session_state.ad_copy_data['brand_voice']
        ),
        help="Choose the tone for your ad copy"
    )
    st.session_state.ad_copy_data['brand_voice'] = brand_voice
    
    # Key Points
    st.subheader("Key Points")
    
    # Initialize key_points in session state if not present
    if 'key_points' not in st.session_state.ad_copy_data:
        st.session_state.ad_copy_data['key_points'] = []
    
    # Add new key point
    new_point = st.text_input("Add a key point", key="new_key_point")
    if st.button("Add Point") and new_point:
        if new_point not in st.session_state.ad_copy_data['key_points']:
            st.session_state.ad_copy_data['key_points'].append(new_point)
            st.rerun()
    
    # Display and allow removal of existing key points
    if st.session_state.ad_copy_data['key_points']:
        st.write("Current Key Points:")
        for i, point in enumerate(st.session_state.ad_copy_data['key_points']):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{i+1}. {point}")
            with col2:
                if st.button("Remove", key=f"remove_point_{i}"):
                    st.session_state.ad_copy_data['key_points'].pop(i)
                    st.rerun()
    
    # Unique Selling Proposition
    usp = st.text_area(
        "Unique Selling Proposition",
        value=st.session_state.ad_copy_data['usp'],
        help="What makes your offer unique? (max 80 characters)",
        max_chars=80,
        height=100
    )
    st.session_state.ad_copy_data['usp'] = usp

def render_cta_tab():
    """Render the call-to-action configuration fields."""
    
    st.header("Call-to-Action")
    
    # CTA Type
    cta_options = {
        'learn_more': 'Learn More',
        'shop_now': 'Shop Now',
        'sign_up': 'Sign Up',
        'book_now': 'Book Now',
        'contact_us': 'Contact Us',
        'download': 'Download',
        'get_offer': 'Get Offer',
        'watch_more': 'Watch More',
        'subscribe': 'Subscribe',
        'custom': 'Custom'
    }
    
    cta_type = st.selectbox(
        "CTA Button Type",
        options=list(cta_options.keys()),
        index=list(cta_options.keys()).index(
            st.session_state.ad_copy_data['cta_type']
        ),
        format_func=lambda x: cta_options[x],
        help="Choose your call-to-action button type"
    )
    st.session_state.ad_copy_data['cta_type'] = cta_type
    
    # Custom CTA Text (if custom selected)
    if cta_type == 'custom':
        cta_text = st.text_input(
            "Custom CTA Text",
            value=st.session_state.ad_copy_data['cta_text'],
            help="Enter your custom call-to-action text (max 20 characters)",
            max_chars=20
        )
        st.session_state.ad_copy_data['cta_text'] = cta_text
    
    # Urgency Elements
    st.subheader("Urgency Elements")
    
    use_urgency = st.checkbox(
        "Add Urgency",
        value=st.session_state.ad_copy_data['use_urgency'],
        help="Add time-sensitive elements to your ad"
    )
    st.session_state.ad_copy_data['use_urgency'] = use_urgency
    
    if use_urgency:
        offer_details = st.text_area(
            "Offer Details",
            value=st.session_state.ad_copy_data['offer_details'],
            help="Enter time-sensitive offer details (e.g., 'Limited time offer - 24 hours only!')",
            height=100
        )
        st.session_state.ad_copy_data['offer_details'] = offer_details

def render_preview_export_tab():
    """Render the preview and export options."""
    
    st.header("Preview & Export")
    
    # Show preview if content has been generated
    if st.session_state.ad_copy_data['show_preview'] and st.session_state.ad_copy_data['generated_content']:
        st.subheader("Preview")
        
        # Toggle between mobile and desktop view
        view_mode = st.radio("View Mode", ["Desktop", "Mobile"])
        
        if view_mode == "Desktop":
            st.markdown("""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
                <h2 style='color: #1877F2;'>Ad Preview</h2>
                <div style='white-space: pre-wrap;'>
            """, unsafe_allow_html=True)
            st.write(st.session_state.ad_copy_data['generated_content'])
            st.markdown("</div></div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='max-width: 375px; margin: 0 auto; background-color: #f0f2f6; padding: 15px; border-radius: 10px;'>
                <h2 style='color: #1877F2; font-size: 18px;'>Ad Preview</h2>
                <div style='white-space: pre-wrap; font-size: 14px;'>
            """, unsafe_allow_html=True)
            st.write(st.session_state.ad_copy_data['generated_content'])
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        # A/B Testing Variations
        if st.session_state.ad_copy_data['variations']:
            st.subheader("A/B Testing Variations")
            for i, variation in enumerate(st.session_state.ad_copy_data['variations']):
                with st.expander(f"Variation {i+1}"):
                    st.write(variation)
        
        # Export options
        st.subheader("Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Copy to Clipboard"):
                st.code(st.session_state.ad_copy_data['generated_content'], language=None)
                st.success("Content copied to clipboard!")
        
        with col2:
            if st.button("Download as Text"):
                download_ad_copy(st.session_state.ad_copy_data['generated_content'])
        
        with col3:
            if st.button("Export as JSON"):
                export_ad_copy_json()
    else:
        st.info("Generate your ad copy to see a preview and export options.")

def validate_ad_copy_fields() -> bool:
    """Validate the required fields for the ad copy generator."""
    
    data = st.session_state.ad_copy_data
    
    # Check required fields
    if not data['campaign_name']:
        st.error("Campaign Name is required.")
        return False
    
    if not data['location']:
        st.error("Location is required.")
        return False
    
    if not data['primary_headline']:
        st.error("Primary Headline is required.")
        return False
    
    if not data['description']:
        st.error("Ad Description is required.")
        return False
    
    if not data['key_points']:
        st.error("At least one Key Point is required.")
        return False
    
    if not data['usp']:
        st.error("Unique Selling Proposition is required.")
        return False
    
    if data['cta_type'] == 'custom' and not data['cta_text']:
        st.error("Custom CTA Text is required when using a custom CTA.")
        return False
    
    return True

def generate_ad_copy() -> Optional[str]:
    """Generate the ad copy content using AI."""
    
    try:
        data = st.session_state.ad_copy_data
        
        # Prepare the prompt for the LLM
        prompt = f"""
        Create a Facebook Ad with the following specifications:
        
        Campaign Details:
        - Name: {data['campaign_name']}
        - Objective: {data['objective']}
        - Format: {data['format']}
        - Placements: {', '.join(data['placements'])}
        
        Target Audience:
        - Age: {data['age_range'][0]}-{data['age_range'][1]}
        - Gender: {data['gender']}
        - Location: {data['location']}
        - Interests: {', '.join(data['interests'])}
        - Behaviors: {', '.join(data['behaviors'])}
        
        Ad Content:
        - Primary Headline: {data['primary_headline']}
        - Secondary Headline: {data['secondary_headline']}
        - Description: {data['description']}
        - Link Description: {data['link_description']}
        - Brand Voice: {data['brand_voice']}
        - Key Points: {', '.join(data['key_points'])}
        - USP: {data['usp']}
        
        Call-to-Action:
        - Type: {data['cta_type']}
        - Custom Text: {data['cta_text'] if data['cta_type'] == 'custom' else 'N/A'}
        - Urgency: {data['offer_details'] if data['use_urgency'] else 'No urgency element'}
        
        The ad copy should be engaging, persuasive, and optimized for the selected objective.
        Use appropriate formatting and ensure the tone matches the selected brand voice.
        Include all key points and USP in a natural way.
        Make the call-to-action compelling and relevant to the objective.
        """
        
        # Get response from LLM
        response = llm_text_gen(prompt)
        
        if response:
            return response
        else:
            st.error("Failed to generate ad copy content. Please try again.")
            return None
            
    except Exception as e:
        logger.error(f"Error generating ad copy: {str(e)}")
        st.error("An error occurred while generating the ad copy. Please try again.")
        return None

def generate_ad_variations() -> Optional[List[str]]:
    """Generate variations of the ad copy for A/B testing."""
    
    try:
        data = st.session_state.ad_copy_data
        
        # Prepare the prompt for variations
        prompt = f"""
        Create 2 variations of the following Facebook Ad copy for A/B testing.
        Keep the core message and USP but vary the:
        1. Headline approach
        2. Description structure
        3. Call-to-action phrasing
        
        Original Ad Copy:
        {data['generated_content']}
        
        Make each variation unique while maintaining the brand voice ({data['brand_voice']})
        and focusing on the main objective ({data['objective']}).
        """
        
        # Get response from LLM
        response = llm_text_gen(prompt)
        
        if response:
            # Split the response into variations
            variations = response.split('\n\nVariation')
            return variations[1:] if len(variations) > 1 else []
        else:
            st.warning("Failed to generate ad variations. Using original copy only.")
            return None
            
    except Exception as e:
        logger.error(f"Error generating ad variations: {str(e)}")
        st.warning("Failed to generate ad variations. Using original copy only.")
        return None

def download_ad_copy(content: str):
    """Download the ad copy content as a text file."""
    
    try:
        # Create a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"facebook_ad_copy_{timestamp}.txt"
        
        # Create a download button
        st.download_button(
            label="Download Text File",
            data=content,
            file_name=filename,
            mime="text/plain"
        )
        
    except Exception as e:
        logger.error(f"Error downloading ad copy: {str(e)}")
        st.error("An error occurred while downloading the ad copy. Please try again.")

def export_ad_copy_json():
    """Export the ad copy data as a JSON file."""
    
    try:
        data = st.session_state.ad_copy_data
        
        # Create a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"facebook_ad_copy_{timestamp}.json"
        
        # Convert data to JSON
        json_data = json.dumps(data, indent=2)
        
        # Create a download button
        st.download_button(
            label="Download JSON File",
            data=json_data,
            file_name=filename,
            mime="application/json"
        )
        
    except Exception as e:
        logger.error(f"Error exporting ad copy JSON: {str(e)}")
        st.error("An error occurred while exporting the ad copy data. Please try again.") 