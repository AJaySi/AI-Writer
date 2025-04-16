"""
LinkedIn AI Writer

This module provides a comprehensive suite of tools for generating LinkedIn content.
"""

import time
import os
import json
import requests
import streamlit as st
import importlib
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union
from loguru import logger

# Import AI text generation
from ...gpt_providers.text_generation.main_text_generation import llm_text_gen

# Import web research tools
from ...ai_web_researcher.gpt_online_researcher import do_google_serp_search
from ...ai_web_researcher.metaphor_basic_neural_web_search import metaphor_search_articles, streamlit_display_metaphor_results
from ...ai_web_researcher.tavily_ai_search import do_tavily_ai_search, streamlit_display_results

# Import LinkedIn content generators
from .modules.post_generator.linkedin_post_generator import linkedin_post_generator_ui
from .modules.article_generator.linkedin_article_generator import linkedin_article_generator_ui
from .modules.carousel_generator.linkedin_carousel_generator import linkedin_carousel_generator_ui
from .modules.video_script_generator.linkedin_video_script_generator import linkedin_video_script_generator_ui
from .modules.comment_response_generator.linkedin_comment_response_generator_ui import linkedin_comment_response_generator_ui
from .modules.profile_optimizer.linkedin_profile_optimizer_ui import linkedin_profile_optimizer_ui
from .modules.poll_generator import linkedin_poll_generator_ui
from .modules.company_page_generator import linkedin_company_page_generator_ui

# Import image generation
from ...gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image

# Create a wrapper for the async profile optimizer UI
def linkedin_profile_optimizer_ui_wrapper():
    """Wrapper function to call the async LinkedIn Profile Optimizer UI."""
    import asyncio
    asyncio.run(linkedin_profile_optimizer_ui())

# Create a wrapper for the async company page generator UI
def linkedin_company_page_generator_ui_wrapper():
    """Wrapper function to call the async LinkedIn Company Page Generator UI."""
    import asyncio
    asyncio.run(linkedin_company_page_generator_ui())

def linkedin_main_menu():
    """Main function for the LinkedIn AI Writer."""
    
    # Initialize session state for selected tool if it doesn't exist
    if "selected_tool" not in st.session_state:
        st.session_state.selected_tool = None
    
    # Define the LinkedIn tools with their details
    linkedin_tools = [
        # Content Creation Tools
        {
            "name": "LinkedIn Post Generator",
            "icon": "📝",
            "description": "Create engaging, professional posts that drive engagement and establish thought leadership.",
            "color": "#0A66C2",  # LinkedIn blue
            "category": "Content Creation",
            "function": linkedin_post_generator_ui,
            "status": "active",
            "features": [
                "Professional tone customization",
                "Industry-specific terminology",
                "Hashtag optimization",
                "Formatting options",
                "Character count optimization",
                "Call-to-action suggestions",
                "Engagement prediction",
                "Visual content recommendations",
                "Poll creation",
                "Best posting time suggestions",
                "Research-backed content",
                "Reference tracking"
            ]
        },
        {
            "name": "LinkedIn Article Generator",
            "icon": "📄",
            "description": "Generate long-form professional articles that showcase expertise and drive traffic.",
            "color": "#0A66C2",
            "category": "Content Creation",
            "function": linkedin_article_generator_ui,
            "status": "active",
            "features": [
                "Topic research and outline generation",
                "SEO optimization for LinkedIn articles",
                "Professional writing style adaptation",
                "Section structuring",
                "Citation and reference formatting",
                "Image placement suggestions",
                "Headline optimization",
                "Meta description generation",
                "Reading time estimation",
                "Internal linking suggestions",
                "Multiple research sources (Metaphor, Google, Tavily)",
                "AI-generated section images"
            ]
        },
        {
            "name": "LinkedIn Carousel Post Generator",
            "icon": "🔄",
            "description": "Create engaging carousel posts that showcase information in a visually appealing way.",
            "color": "#0A66C2",
            "category": "Content Creation",
            "function": linkedin_carousel_generator_ui,
            "status": "active",
            "features": [
                "Slide content generation",
                "Visual hierarchy optimization",
                "Story arc development",
                "Call-to-action placement",
                "Brand consistency maintenance",
                "Engagement element integration",
                "Professional design suggestions",
                "Content distribution strategy",
                "Analytics integration",
                "A/B testing variations"
            ]
        },
        {
            "name": "LinkedIn Video Script Generator",
            "icon": "🎥",
            "description": "Create scripts for LinkedIn videos that drive engagement.",
            "color": "#0A66C2",
            "category": "Content Creation",
            "function": linkedin_video_script_generator_ui,
            "status": "active",
            "features": [
                "Hook generation",
                "Story structure development",
                "Professional speaking points",
                "Visual cue suggestions",
                "Call-to-action optimization",
                "Engagement prompt integration",
                "Caption generation",
                "Thumbnail text suggestions",
                "Video description optimization",
                "Hashtag strategy"
            ]
        },
        {
            "name": "LinkedIn Comment Response Generator",
            "icon": "💬",
            "description": "Generate professional and engaging responses to LinkedIn comments with AI-powered analysis and optimization.",
            "color": "#0A66C2",
            "category": "Engagement",
            "function": linkedin_comment_response_generator_ui,
            "status": "active",
            "features": [
                "Comment analysis and categorization",
                "Multiple response types (general, disagreement, value-add)",
                "Brand voice customization",
                "Engagement goal targeting",
                "Resource suggestion generation",
                "Follow-up question generation",
                "Tone optimization",
                "Response strategy recommendations",
                "Context-aware responses",
                "Professional formatting"
            ]
        },
        
        # Profile & Personal Branding Tools
        {
            "name": "LinkedIn Profile Optimizer",
            "icon": "👤",
            "description": "Enhance LinkedIn profiles to improve visibility and professional appeal.",
            "color": "#0A66C2",
            "category": "Profile & Personal Branding",
            "function": linkedin_profile_optimizer_ui_wrapper,
            "status": "active",
            "features": [
                "Headline optimization",
                "About section generation",
                "Experience description enhancement",
                "Skills recommendation",
                "Project highlight creation",
                "Endorsement request generation",
                "Profile strength analysis",
                "Keyword optimization",
                "Professional summary generation",
                "Custom URL suggestions"
            ]
        },
        {
            "name": "LinkedIn Poll Generator",
            "icon": "📊",
            "description": "Create engaging polls that drive interaction and gather insights.",
            "color": "#0A66C2",
            "category": "Profile & Personal Branding",
            "function": linkedin_poll_generator_ui,
            "status": "active",
            "features": [
                "Question formulation optimization",
                "Option generation based on topic",
                "Industry-specific poll templates",
                "Engagement prediction",
                "Result analysis suggestions",
                "Follow-up content recommendations",
                "Trending topic integration",
                "Professional tone maintenance",
                "Data visualization suggestions",
                "Poll scheduling optimization"
            ]
        },
        
        # Business & Marketing Tools
        {
            "name": "LinkedIn Company Page Content Generator",
            "icon": "🏢",
            "description": "Create content for company pages that builds brand awareness and engagement.",
            "color": "#0A66C2",
            "category": "Business & Marketing",
            "function": linkedin_company_page_generator_ui_wrapper,
            "status": "active",
            "features": [
                "Company culture post generation",
                "Product/service announcement templates",
                "Employee spotlight content",
                "Company milestone celebrations",
                "Industry insights sharing",
                "Event promotion content",
                "Job posting templates",
                "Company news updates",
                "Brand voice consistency",
                "Engagement metrics optimization"
            ]
        },
        {
            "name": "LinkedIn Newsletter Generator",
            "icon": "📰",
            "description": "Create professional newsletters that establish thought leadership and drive engagement.",
            "color": "#0A66C2",
            "category": "Business & Marketing",
            "function": None,
            "status": "coming_soon",
            "features": [
                "Newsletter structure templates",
                "Topic clustering and organization",
                "Professional introduction and conclusion",
                "Industry trend analysis integration",
                "Expert quote suggestions",
                "Visual content recommendations",
                "Call-to-action optimization",
                "Subscriber engagement prompts",
                "Consistency maintenance",
                "Analytics integration suggestions"
            ]
        },
        {
            "name": "LinkedIn Job Description Generator",
            "icon": "💼",
            "description": "Create compelling job descriptions that attract qualified candidates.",
            "color": "#0A66C2",
            "category": "Business & Marketing",
            "function": None,
            "status": "coming_soon",
            "features": [
                "Role-specific templates",
                "Skills and qualifications optimization",
                "Company culture integration",
                "Benefits and perks highlighting",
                "Inclusive language checker",
                "Keyword optimization",
                "Application process clarity",
                "Remote/hybrid work policy integration",
                "Diversity and inclusion statements",
                "A/B testing variations"
            ]
        },
        
        # Sales & Networking Tools
        {
            "name": "LinkedIn Sales Navigator Content Generator",
            "icon": "💰",
            "description": "Create personalized outreach content for sales professionals.",
            "color": "#0A66C2",
            "category": "Sales & Networking",
            "function": None,
            "status": "coming_soon",
            "features": [
                "Prospect research integration",
                "Industry-specific messaging",
                "Personalization tokens",
                "Connection request templates",
                "Follow-up message sequences",
                "Value proposition highlighting",
                "Objection handling responses",
                "Meeting request templates",
                "Industry pain point addressing",
                "ROI demonstration content"
            ]
        },
        {
            "name": "LinkedIn InMail Generator",
            "icon": "✉️",
            "description": "Create personalized and effective InMail messages.",
            "color": "#0A66C2",
            "category": "Sales & Networking",
            "function": None,
            "status": "coming_soon",
            "features": [
                "Prospect research integration",
                "Personalization token usage",
                "Value proposition highlighting",
                "Call-to-action optimization",
                "Follow-up sequence generation",
                "Objection handling preparation",
                "Industry-specific messaging",
                "A/B testing variations",
                "Compliance checking",
                "Engagement tracking suggestions"
            ]
        },
        
        # Learning & Education Tools
        {
            "name": "LinkedIn Learning Course Description Generator",
            "icon": "📚",
            "description": "Create compelling descriptions for LinkedIn Learning courses.",
            "color": "#0A66C2",
            "category": "Learning & Education",
            "function": None,
            "status": "coming_soon",
            "features": [
                "Course objective optimization",
                "Learning outcome generation",
                "Prerequisite suggestions",
                "Target audience definition",
                "Skill tag recommendations",
                "Course structure outline",
                "Engagement element suggestions",
                "Completion certificate highlighting",
                "Industry relevance emphasis",
                "Career path integration"
            ]
        },
        {
            "name": "LinkedIn Event Description Generator",
            "icon": "📅",
            "description": "Create compelling event descriptions that drive attendance and engagement.",
            "color": "#0A66C2",
            "category": "Learning & Education",
            "function": None,
            "status": "coming_soon",
            "features": [
                "Event objective highlighting",
                "Speaker bio generation",
                "Agenda formatting",
                "Registration incentive suggestions",
                "Networking opportunity emphasis",
                "Industry relevance integration",
                "Visual content recommendations",
                "Engagement element suggestions",
                "Post-event follow-up content",
                "Attendance tracking integration"
            ]
        },
        
        # Community & Engagement Tools
        {
            "name": "LinkedIn Group Post Generator",
            "icon": "👥",
            "description": "Create content specifically optimized for LinkedIn Groups.",
            "color": "#0A66C2",
            "category": "Community & Engagement",
            "function": None,
            "status": "coming_soon",
            "features": [
                "Group-specific content adaptation",
                "Discussion prompt generation",
                "Community guideline compliance",
                "Engagement optimization",
                "Moderation suggestion",
                "Topic relevance checking",
                "Member value highlighting",
                "Cross-promotion opportunities",
                "Group culture adaptation",
                "Content scheduling"
            ]
        },
        {
            "name": "LinkedIn Comment Response Generator",
            "icon": "💬",
            "description": "Create professional and engaging responses to comments on LinkedIn posts.",
            "color": "#0A66C2",
            "category": "Community & Engagement",
            "function": None,
            "status": "coming_soon",
            "features": [
                "Tone adaptation based on comment",
                "Professional disagreement handling",
                "Question answering optimization",
                "Engagement continuation prompts",
                "Value-add response generation",
                "Community building suggestions",
                "Moderation guidance",
                "Follow-up question generation",
                "Resource sharing suggestions",
                "Relationship building strategies"
            ]
        }
    ]
    
    # Create a container for the dashboard
    dashboard_container = st.container()
    
    # Create a container for the tool input section
    tool_container = st.container()
    
    # If a tool is selected, show its input section
    if st.session_state.selected_tool is not None:
        with tool_container:
            # Add a back button at the top
            if st.button("← Back to Dashboard", key="back_to_dashboard"):
                st.session_state.selected_tool = None
                st.rerun()
            
            # Display the tool header with card layout
            st.markdown(f"""
                <div style='
                    background: linear-gradient(145deg, #ffffff 0%, #f0f7ff 50%, #e6f0ff 100%);
                    padding: 2.5rem;
                    border-radius: 16px;
                    box-shadow: 0 10px 25px rgba(10, 102, 194, 0.08);
                    margin: 1rem 0 2.5rem 0;
                    border: 1px solid rgba(10, 102, 194, 0.1);
                '>
                    <div style='
                        display: flex;
                        align-items: center;
                        margin-bottom: 1.2rem;
                        background: rgba(255, 255, 255, 0.8);
                        padding: 1rem 1.5rem;
                        border-radius: 12px;
                        box-shadow: 0 4px 15px rgba(10, 102, 194, 0.05);
                    '>
                        <div style='
                            font-size: 2.5rem;
                            margin-right: 1rem;
                            color: #0A66C2;
                        '>{st.session_state.selected_tool['icon']}</div>
                        <div>
                            <h1 style='
                                margin: 0;
                                color: #0A66C2;
                                font-size: 2.2rem;
                                font-weight: 600;
                            '>{st.session_state.selected_tool['name']}</h1>
                            <p style='
                                color: #666;
                                margin: 0.5rem 0 0 0;
                                font-size: 1.1rem;
                                line-height: 1.5;
                            '>{st.session_state.selected_tool['description']}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Call the tool's function if it exists
            if st.session_state.selected_tool["function"] is not None:
                st.session_state.selected_tool["function"]()
            else:
                # Display coming soon information
                st.info(f"**{st.session_state.selected_tool['status'].replace('_', ' ').title()}!**")
                st.write(st.session_state.selected_tool["description"])
                
                # Display features
                st.subheader("Features")
                for feature in st.session_state.selected_tool["features"]:
                    st.markdown(f"- {feature}")
                
                # Display placeholder image
                st.image(f"https://via.placeholder.com/600x300?text={st.session_state.selected_tool['name']}+Coming+Soon", use_container_width=True)
    else:
        with dashboard_container:
            # Display the dashboard
            # Header
            st.markdown("""
            <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                <h1 style='color: #0A66C2; text-align: center;'>💼 LinkedIn AI Writer</h1>
                <p style='text-align: center;'>Generate professional LinkedIn content with ALwrity's AI-powered tools</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Group tools by category
            categories = {}
            for tool in linkedin_tools:
                category = tool["category"]
                if category not in categories:
                    categories[category] = []
                categories[category].append(tool)
            
            # Display tools by category
            for category, tools in categories.items():
                st.markdown(f"## {category}")
                
                # Create a 3-column layout for the tool cards
                cols = st.columns(3)
                
                # Display the tool cards
                for i, tool in enumerate(tools):
                    # Determine which column to use
                    col = cols[i % 3]
                    
                    with col:
                        # Create a card for each tool
                        status_badge = ""
                        if tool["status"] == "coming_soon":
                            status_badge = "<span style='background-color: #FFA500; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;'>Coming Soon</span>"
                        elif tool["status"] == "future":
                            status_badge = "<span style='background-color: #808080; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;'>Future</span>"
                        elif tool["status"] == "active":
                            status_badge = "<span style='background-color: #4CAF50; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;'>Active</span>"
                        
                        st.markdown(f"""
                        <div style='background-color: {tool["color"]}; padding: 20px; border-radius: 10px; margin-bottom: 20px; color: white;'>
                            <h2 style='color: white;'>{tool["icon"]} {tool["name"]} {status_badge}</h2>
                            <p>{tool["description"]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add a button to access the tool
                        if st.button(f"Use {tool['name']}", key=f"btn_{tool['category']}_{tool['name']}"):
                            # Store the selected tool in session state
                            st.session_state.selected_tool = tool
                            st.rerun()


class LinkedInAIWriter:
    """
    AI-powered content generator for LinkedIn marketing and communication.
    
    This class provides various tools for generating LinkedIn content including:
    - Posts and articles
    - Profile optimization
    - Company page content
    - Sales and networking content
    - Learning and education content
    - Community and engagement content
    """
    
    def __init__(self):
        """Initialize the LinkedIn AI Writer."""
        pass
    
    # Methods will be implemented in future iterations
    # Each method will correspond to a specific LinkedIn content generation tool


# List of available tools
AVAILABLE_TOOLS = [
    'Post Generator',
    'Article Generator',
    'Carousel Post Generator',
    'Video Script Generator',
    'Profile Optimizer',
    'Poll Generator',
    'Company Page Content Generator',
    'Newsletter Generator',
    'Job Description Generator',
    'Sales Navigator Content Generator',
    'InMail Generator',
    'Learning Course Description Generator',
    'Event Description Generator',
    'Group Post Generator',
    'Comment Response Generator'
]

if __name__ == "__main__":
    linkedin_main_menu()
