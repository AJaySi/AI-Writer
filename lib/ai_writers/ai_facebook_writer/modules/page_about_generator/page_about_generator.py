"""
Facebook Page About Generator Module

This module provides functionality to generate professional and engaging About sections
for Facebook Pages. It helps businesses create compelling content that effectively
communicates their brand identity, mission, and value proposition to visitors.
"""

import streamlit as st
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union, Tuple
from .....gpt_providers.text_generation.main_text_generation import llm_text_gen

# Set up logging
logger = logging.getLogger(__name__)

def write_fb_page_about():
    """
    Generate a Facebook Page About section with various customization options.
    
    This function provides a comprehensive interface for creating professional
    and engaging About sections for Facebook Pages with features like:
    - Basic information management
    - Brand voice and tone customization
    - Key sections configuration
    - Preview and export options
    """
    
    st.title("Facebook Page About Generator")
    st.markdown("""
    Create professional and engaging About sections for your Facebook Pages that effectively
    communicate your brand identity, mission, and value proposition to visitors.
    """)
    
    # Initialize session state for form data
    if 'page_about_data' not in st.session_state:
        st.session_state.page_about_data = {
            # Basic Information
            'business_name': '',
            'industry': '',
            'founded_date': '',
            'location': '',
            'website': '',
            'phone': '',
            'email': '',
            'address': '',
            'mission_statement': '',
            
            # Brand Voice & Tone
            'tone': 'professional',
            'brand_personality': [],
            'target_audience': '',
            'brand_values': [],
            
            # Key Sections
            'include_about_us': True,
            'about_us_content': '',
            'include_products': True,
            'products_content': '',
            'include_usp': True,
            'usp_content': '',
            'include_team': False,
            'team_content': '',
            'include_awards': False,
            'awards_content': '',
            'include_testimonials': False,
            'testimonials_content': '',
            'include_cta': True,
            'cta_content': '',
            
            # Content Length
            'content_length': 'standard',
            
            # Generated Content
            'generated_content': '',
            'show_preview': False
        }
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "Basic Information", 
        "Brand Voice & Tone", 
        "Key Sections", 
        "Preview & Export"
    ])
    
    with tab1:
        render_basic_info_tab()
    
    with tab2:
        render_brand_voice_tab()
    
    with tab3:
        render_key_sections_tab()
    
    with tab4:
        render_preview_export_tab()
    
    # Generate button
    if st.button("Generate About Section", type="primary"):
        if validate_page_about_fields():
            with st.spinner("Generating your About section..."):
                about_content = generate_page_about()
                if about_content:
                    st.session_state.page_about_data['generated_content'] = about_content
                    st.success("About section generated successfully!")
                    st.session_state.page_about_data['show_preview'] = True
                    st.rerun()

def render_basic_info_tab():
    """Render the basic information input fields."""
    
    st.header("Basic Information")
    
    # Business Name
    business_name = st.text_input(
        "Business/Organization Name",
        value=st.session_state.page_about_data['business_name'],
        help="Enter your business or organization name"
    )
    st.session_state.page_about_data['business_name'] = business_name
    
    # Industry
    industry = st.text_input(
        "Industry/Category",
        value=st.session_state.page_about_data['industry'],
        help="Enter your industry or business category"
    )
    st.session_state.page_about_data['industry'] = industry
    
    # Founded Date
    founded_date = st.text_input(
        "Founded Date",
        value=st.session_state.page_about_data['founded_date'],
        help="Enter when your business was founded (e.g., '2010' or 'January 2010')"
    )
    st.session_state.page_about_data['founded_date'] = founded_date
    
    # Location
    location = st.text_input(
        "Location",
        value=st.session_state.page_about_data['location'],
        help="Enter your business location (city, state, country)"
    )
    st.session_state.page_about_data['location'] = location
    
    # Website
    website = st.text_input(
        "Website URL",
        value=st.session_state.page_about_data['website'],
        help="Enter your website URL"
    )
    st.session_state.page_about_data['website'] = website
    
    # Contact Information
    st.subheader("Contact Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        phone = st.text_input(
            "Phone Number",
            value=st.session_state.page_about_data['phone'],
            help="Enter your business phone number"
        )
        st.session_state.page_about_data['phone'] = phone
        
        email = st.text_input(
            "Email Address",
            value=st.session_state.page_about_data['email'],
            help="Enter your business email address"
        )
        st.session_state.page_about_data['email'] = email
    
    with col2:
        address = st.text_area(
            "Physical Address",
            value=st.session_state.page_about_data['address'],
            help="Enter your business physical address",
            height=100
        )
        st.session_state.page_about_data['address'] = address
    
    # Mission Statement
    mission_statement = st.text_area(
        "Mission Statement",
        value=st.session_state.page_about_data['mission_statement'],
        help="Enter your business mission statement (1-2 sentences)",
        height=100
    )
    st.session_state.page_about_data['mission_statement'] = mission_statement

def render_brand_voice_tab():
    """Render the brand voice and tone selection fields."""
    
    st.header("Brand Voice & Tone")
    
    # Tone Selection
    tone = st.selectbox(
        "Select Tone",
        options=['professional', 'friendly', 'casual', 'formal', 'humorous'],
        index=['professional', 'friendly', 'casual', 'formal', 'humorous'].index(
            st.session_state.page_about_data['tone']
        ),
        help="Choose the tone for your About section"
    )
    st.session_state.page_about_data['tone'] = tone
    
    # Brand Personality Traits
    st.subheader("Brand Personality Traits")
    
    personality_options = [
        'Innovative', 'Reliable', 'Creative', 'Professional', 'Friendly',
        'Authoritative', 'Empathetic', 'Ambitious', 'Authentic', 'Dynamic',
        'Trustworthy', 'Passionate', 'Efficient', 'Eco-friendly', 'Luxurious'
    ]
    
    # Initialize brand_personality in session state if not present
    if 'brand_personality' not in st.session_state.page_about_data:
        st.session_state.page_about_data['brand_personality'] = []
    
    # Create a multi-select for brand personality traits
    selected_traits = st.multiselect(
        "Select Brand Personality Traits (up to 5)",
        options=personality_options,
        default=st.session_state.page_about_data['brand_personality'],
        help="Choose up to 5 traits that best describe your brand personality"
    )
    
    # Limit to 5 traits
    if len(selected_traits) > 5:
        st.warning("You can only select up to 5 traits. The first 5 will be used.")
        selected_traits = selected_traits[:5]
    
    st.session_state.page_about_data['brand_personality'] = selected_traits
    
    # Target Audience
    target_audience = st.text_area(
        "Target Audience",
        value=st.session_state.page_about_data['target_audience'],
        help="Describe your target audience (demographics, interests, needs)",
        height=100
    )
    st.session_state.page_about_data['target_audience'] = target_audience
    
    # Brand Values
    st.subheader("Brand Values")
    
    # Initialize brand_values in session state if not present
    if 'brand_values' not in st.session_state.page_about_data:
        st.session_state.page_about_data['brand_values'] = []
    
    # Create a dynamic list for brand values
    brand_values = st.session_state.page_about_data['brand_values']
    
    # Add new value
    new_value = st.text_input("Add a brand value", key="new_brand_value")
    if st.button("Add Value") and new_value:
        if new_value not in brand_values:
            brand_values.append(new_value)
            st.session_state.page_about_data['brand_values'] = brand_values
            st.rerun()
    
    # Display and allow removal of existing values
    if brand_values:
        st.write("Current Brand Values:")
        for i, value in enumerate(brand_values):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{i+1}. {value}")
            with col2:
                if st.button("Remove", key=f"remove_value_{i}"):
                    brand_values.pop(i)
                    st.session_state.page_about_data['brand_values'] = brand_values
                    st.rerun()
    else:
        st.info("No brand values added yet. Add at least one brand value.")

def render_key_sections_tab():
    """Render the key sections configuration fields."""
    
    st.header("Key Sections")
    
    # Content Length
    content_length = st.selectbox(
        "Content Length",
        options=['brief', 'standard', 'detailed'],
        index=['brief', 'standard', 'detailed'].index(
            st.session_state.page_about_data['content_length']
        ),
        help="Choose the length of the generated content"
    )
    st.session_state.page_about_data['content_length'] = content_length
    
    # About Us Section
    st.subheader("About Us/Our Story")
    include_about_us = st.checkbox(
        "Include About Us Section",
        value=st.session_state.page_about_data['include_about_us'],
        help="Include a section about your company's history and journey"
    )
    st.session_state.page_about_data['include_about_us'] = include_about_us
    
    if include_about_us:
        about_us_content = st.text_area(
            "Custom About Us Content (optional)",
            value=st.session_state.page_about_data['about_us_content'],
            help="Enter custom content or leave blank for AI generation",
            height=150
        )
        st.session_state.page_about_data['about_us_content'] = about_us_content
    
    # Products/Services Section
    st.subheader("Products/Services")
    include_products = st.checkbox(
        "Include Products/Services Section",
        value=st.session_state.page_about_data['include_products'],
        help="Include a section about your products or services"
    )
    st.session_state.page_about_data['include_products'] = include_products
    
    if include_products:
        products_content = st.text_area(
            "Custom Products/Services Content (optional)",
            value=st.session_state.page_about_data['products_content'],
            help="Enter custom content or leave blank for AI generation",
            height=150
        )
        st.session_state.page_about_data['products_content'] = products_content
    
    # Unique Selling Proposition Section
    st.subheader("Unique Selling Proposition")
    include_usp = st.checkbox(
        "Include USP Section",
        value=st.session_state.page_about_data['include_usp'],
        help="Include a section highlighting what sets you apart"
    )
    st.session_state.page_about_data['include_usp'] = include_usp
    
    if include_usp:
        usp_content = st.text_area(
            "Custom USP Content (optional)",
            value=st.session_state.page_about_data['usp_content'],
            help="Enter custom content or leave blank for AI generation",
            height=150
        )
        st.session_state.page_about_data['usp_content'] = usp_content
    
    # Team/Leadership Section
    st.subheader("Team/Leadership")
    include_team = st.checkbox(
        "Include Team/Leadership Section",
        value=st.session_state.page_about_data['include_team'],
        help="Include a section about your team or leadership"
    )
    st.session_state.page_about_data['include_team'] = include_team
    
    if include_team:
        team_content = st.text_area(
            "Custom Team/Leadership Content (optional)",
            value=st.session_state.page_about_data['team_content'],
            help="Enter custom content or leave blank for AI generation",
            height=150
        )
        st.session_state.page_about_data['team_content'] = team_content
    
    # Awards/Recognition Section
    st.subheader("Awards/Recognition")
    include_awards = st.checkbox(
        "Include Awards/Recognition Section",
        value=st.session_state.page_about_data['include_awards'],
        help="Include a section about your awards and recognition"
    )
    st.session_state.page_about_data['include_awards'] = include_awards
    
    if include_awards:
        awards_content = st.text_area(
            "Custom Awards/Recognition Content (optional)",
            value=st.session_state.page_about_data['awards_content'],
            help="Enter custom content or leave blank for AI generation",
            height=150
        )
        st.session_state.page_about_data['awards_content'] = awards_content
    
    # Customer Testimonials Section
    st.subheader("Customer Testimonials")
    include_testimonials = st.checkbox(
        "Include Customer Testimonials Section",
        value=st.session_state.page_about_data['include_testimonials'],
        help="Include a section with customer testimonials"
    )
    st.session_state.page_about_data['include_testimonials'] = include_testimonials
    
    if include_testimonials:
        testimonials_content = st.text_area(
            "Custom Testimonials Content (optional)",
            value=st.session_state.page_about_data['testimonials_content'],
            help="Enter custom content or leave blank for AI generation",
            height=150
        )
        st.session_state.page_about_data['testimonials_content'] = testimonials_content
    
    # Call-to-Action Section
    st.subheader("Call-to-Action")
    include_cta = st.checkbox(
        "Include Call-to-Action Section",
        value=st.session_state.page_about_data['include_cta'],
        help="Include a call-to-action to encourage visitors to take specific actions"
    )
    st.session_state.page_about_data['include_cta'] = include_cta
    
    if include_cta:
        cta_content = st.text_area(
            "Custom Call-to-Action Content (optional)",
            value=st.session_state.page_about_data['cta_content'],
            help="Enter custom content or leave blank for AI generation",
            height=150
        )
        st.session_state.page_about_data['cta_content'] = cta_content

def render_preview_export_tab():
    """Render the preview and export options."""
    
    st.header("Preview & Export")
    
    # Show preview if content has been generated
    if st.session_state.page_about_data['show_preview'] and st.session_state.page_about_data['generated_content']:
        st.subheader("Preview")
        
        # Toggle between mobile and desktop view
        view_mode = st.radio("View Mode", ["Desktop", "Mobile"])
        
        if view_mode == "Desktop":
            st.markdown("""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
                <h2 style='color: #1877F2;'>About</h2>
                <div style='white-space: pre-wrap;'>
            """, unsafe_allow_html=True)
            st.write(st.session_state.page_about_data['generated_content'])
            st.markdown("</div></div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='max-width: 375px; margin: 0 auto; background-color: #f0f2f6; padding: 15px; border-radius: 10px;'>
                <h2 style='color: #1877F2; font-size: 18px;'>About</h2>
                <div style='white-space: pre-wrap; font-size: 14px;'>
            """, unsafe_allow_html=True)
            st.write(st.session_state.page_about_data['generated_content'])
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        # SEO Score
        seo_score = calculate_seo_score(st.session_state.page_about_data['generated_content'])
        st.subheader(f"SEO Score: {seo_score}/10")
        
        if seo_score < 7:
            st.warning("Your About section could benefit from SEO improvements. Consider adding more keywords and optimizing your content.")
        
        # Export options
        st.subheader("Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Copy to Clipboard"):
                st.code(st.session_state.page_about_data['generated_content'], language=None)
                st.success("Content copied to clipboard!")
        
        with col2:
            if st.button("Download as Text"):
                download_page_about(st.session_state.page_about_data['generated_content'])
    else:
        st.info("Generate your About section to see a preview and export options.")

def validate_page_about_fields() -> bool:
    """Validate the required fields for the page about generator."""
    
    data = st.session_state.page_about_data
    
    # Check required fields
    if not data['business_name']:
        st.error("Business/Organization Name is required.")
        return False
    
    if not data['industry']:
        st.error("Industry/Category is required.")
        return False
    
    if not data['mission_statement']:
        st.error("Mission Statement is required.")
        return False
    
    if not data['target_audience']:
        st.error("Target Audience is required.")
        return False
    
    if not data['brand_personality']:
        st.error("At least one Brand Personality Trait is required.")
        return False
    
    if not data['brand_values']:
        st.error("At least one Brand Value is required.")
        return False
    
    # Check if at least one section is included
    sections_included = (
        data['include_about_us'] or 
        data['include_products'] or 
        data['include_usp'] or 
        data['include_team'] or 
        data['include_awards'] or 
        data['include_testimonials'] or 
        data['include_cta']
    )
    
    if not sections_included:
        st.error("At least one section must be included.")
        return False
    
    return True

def generate_page_about() -> Optional[str]:
    """Generate the page about content using AI."""
    
    try:
        data = st.session_state.page_about_data
        
        # Prepare the prompt for the LLM
        prompt = f"""
        Create a Facebook Page About section for {data['business_name']}, a {data['industry']} business.
        
        Basic Information:
        - Founded: {data['founded_date']}
        - Location: {data['location']}
        - Website: {data['website']}
        - Mission Statement: {data['mission_statement']}
        
        Brand Voice & Tone:
        - Tone: {data['tone']}
        - Brand Personality Traits: {', '.join(data['brand_personality'])}
        - Target Audience: {data['target_audience']}
        - Brand Values: {', '.join(data['brand_values'])}
        
        Content Length: {data['content_length']}
        
        Include the following sections:
        """
        
        # Add sections to include
        if data['include_about_us']:
            prompt += f"""
            - About Us/Our Story: {data['about_us_content'] if data['about_us_content'] else 'Generate engaging content about the company history and journey'}
            """
        
        if data['include_products']:
            prompt += f"""
            - Products/Services: {data['products_content'] if data['products_content'] else 'Generate engaging content about the products or services offered'}
            """
        
        if data['include_usp']:
            prompt += f"""
            - Unique Selling Proposition: {data['usp_content'] if data['usp_content'] else 'Generate engaging content about what sets the business apart'}
            """
        
        if data['include_team']:
            prompt += f"""
            - Team/Leadership: {data['team_content'] if data['team_content'] else 'Generate engaging content about the team or leadership'}
            """
        
        if data['include_awards']:
            prompt += f"""
            - Awards/Recognition: {data['awards_content'] if data['awards_content'] else 'Generate engaging content about awards and recognition'}
            """
        
        if data['include_testimonials']:
            prompt += f"""
            - Customer Testimonials: {data['testimonials_content'] if data['testimonials_content'] else 'Generate engaging content with customer testimonials'}
            """
        
        if data['include_cta']:
            prompt += f"""
            - Call-to-Action: {data['cta_content'] if data['cta_content'] else 'Generate an engaging call-to-action'}
            """
        
        prompt += """
        The About section should be well-structured, engaging, and optimized for Facebook.
        Use appropriate formatting, emojis, and line breaks for better readability.
        Make sure the tone is consistent with the selected brand voice.
        Include relevant keywords for SEO optimization.
        """
        
        # Get response from LLM
        response = llm_text_gen(prompt)
        
        if response:
            return response
        else:
            st.error("Failed to generate About section content. Please try again.")
            return None
            
    except Exception as e:
        logger.error(f"Error generating About section: {str(e)}")
        st.error("An error occurred while generating the About section. Please try again.")
        return None

def calculate_seo_score(content: str) -> int:
    """Calculate a simple SEO score for the content."""
    
    score = 5  # Start with a base score
    
    # Check for keywords (simple implementation)
    keywords = ['about', 'mission', 'vision', 'values', 'services', 'products', 'team', 'contact']
    for keyword in keywords:
        if keyword.lower() in content.lower():
            score += 0.5
    
    # Check for formatting
    if '\n\n' in content:  # Paragraph breaks
        score += 1
    
    if '*' in content or '_' in content:  # Bold or italic formatting
        score += 1
    
    # Check for length
    if len(content) > 500:
        score += 1
    
    # Cap the score at 10
    return min(score, 10)

def download_page_about(content: str):
    """Download the About section content as a text file."""
    
    try:
        # Create a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"facebook_page_about_{timestamp}.txt"
        
        # Create a download button
        st.download_button(
            label="Download Text File",
            data=content,
            file_name=filename,
            mime="text/plain"
        )
        
    except Exception as e:
        logger.error(f"Error downloading About section: {str(e)}")
        st.error("An error occurred while downloading the About section. Please try again.") 