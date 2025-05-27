"""
Facebook AI Writer

This module provides a comprehensive suite of tools for generating Facebook content.
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

from ...gpt_providers.text_generation.main_text_generation import llm_text_gen
from .modules.post_generator import write_fb_post
from .modules.story_generator import write_fb_story
from .modules.facebook_reel.reel_generator import write_fb_reel
from .modules.facebook_carousel.carousel_generator import write_fb_carousel
from .modules.event_generator import write_fb_event
from .modules.hashtag_generator import write_fb_hashtags
from .modules.engagement_analyzer import analyze_fb_engagement
from .modules.group_post_generator import write_fb_group_post
from .modules.page_about_generator import write_fb_page_about
from .modules.ad_copy_generator import write_fb_ad_copy

#from streamlit_quill import st_quill


def generate_facebook_post(business_type, target_audience, post_goal, post_tone, include, avoid):
    """
    Generates a Facebook post prompt for an LLM based on user input.
    """
    prompt = f"""
        I am a {business_type} looking to engage my target audience, {target_audience}, on Facebook.

        My goal for this detailed post is: {post_goal}. The tone should be {post_tone}.

        Here are some additional preferences:
        - **Include:** {include}
        - **Avoid:** {avoid}

        Please write a well-structured Facebook post with:
        1. A **catchy opening** to grab attention.
        2. Detailed **Engaging content** that highlights key benefits or features.
        3. A **strong call-to-action** (CTA) encouraging my audience to take action.
        4. If applicable, suggest **multimedia** (images, videos, etc.).
        5. Include **relevant hashtags** for visibility.

        """
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        st.error(f"An error occurred while generating the prompt: {err}")
        return None


def facebook_main_menu():
    """Main function for the Facebook AI Writer."""
    
    # Initialize session state for selected tool if it doesn't exist
    if "selected_tool" not in st.session_state:
        st.session_state.selected_tool = None
    
    # Define the Facebook tools with their details
    facebook_tools = [
        # Content Creation Tools
        {
            "name": "FB Post Generator",
            "icon": "📝",
            "description": "Create engaging Facebook posts that drive engagement and reach.",
            "color": "#1877F2",  # Facebook blue
            "category": "Content Creation",
            "function": write_fb_post,
            "status": "active"
        },
        {
            "name": "FB Story Generator",
            "icon": "📱",
            "description": "Generate creative Facebook Stories with text overlays and engagement elements.",
            "color": "#1877F2",
            "category": "Content Creation",
            "function": write_fb_story,
            "status": "active"
        },
        {
            "name": "FB Reel Generator",
            "icon": "🎥",
            "description": "Create engaging Facebook Reels scripts with trending music suggestions.",
            "color": "#1877F2",
            "category": "Content Creation",
            "function": write_fb_reel,
            "status": "active"
        },
        {
            "name": "Carousel Generator",
            "icon": "🔄",
            "description": "Generate multi-image carousel posts with engaging captions for each slide.",
            "color": "#1877F2",
            "category": "Content Creation",
            "function": write_fb_carousel,
            "status": "active"
        },
        
        # Business Tools
        {
            "name": "Event Description Generator",
            "icon": "📅",
            "description": "Create compelling event descriptions that drive attendance and engagement.",
            "color": "#1877F2",
            "category": "Business Tools",
            "function": write_fb_event,
            "status": "active"
        },
        {
            "name": "Group Post Generator",
            "icon": "👥",
            "description": "Generate engaging posts for Facebook Groups with community-focused content.",
            "color": "#1877F2",
            "category": "Business Tools",
            "function": write_fb_group_post,
            "status": "active"
        },
        {
            "name": "Page About Generator",
            "icon": "ℹ️",
            "description": "Create professional and engaging About sections for your Facebook Page.",
            "color": "#1877F2",
            "category": "Business Tools",
            "function": write_fb_page_about,
            "status": "active"
        },
        
        # Marketing Tools
        {
            "name": "Ad Copy Generator",
            "icon": "💰",
            "description": "Generate high-converting ad copy for Facebook Ads with targeting suggestions.",
            "color": "#1877F2",
            "category": "Marketing Tools",
            "function": write_fb_ad_copy,
            "status": "active"
        },
        {
            "name": "Hashtag Generator",
            "icon": "#️⃣",
            "description": "Generate trending and relevant hashtags for your Facebook content.",
            "color": "#1877F2",
            "category": "Marketing Tools",
            "function": write_fb_hashtags,
            "status": "active"
        },
        {
            "name": "Engagement Analyzer",
            "icon": "📊",
            "description": "Analyze your content performance and get AI-powered improvement suggestions.",
            "color": "#1877F2",
            "category": "Marketing Tools",
            "function": analyze_fb_engagement,
            "status": "active"
        },
        
        # Future Tools
        {
            "name": "Content Calendar",
            "icon": "📅",
            "description": "Plan and organize your Facebook content with AI-powered scheduling suggestions.",
            "color": "#1877F2",
            "category": "Future Tools",
            "function": None,
            "status": "future"
        },
        {
            "name": "Live Stream Script",
            "icon": "🎥",
            "description": "Generate engaging scripts for Facebook Live streams with audience interaction points.",
            "color": "#1877F2",
            "category": "Future Tools",
            "function": None,
            "status": "future"
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
            if st.button("← Back to Dashboard", key="back_to_facebook_dashboard"):
                st.session_state.selected_tool = None
                st.rerun()
            
            # Display the tool header with card layout
            st.markdown(f"""
                <div style='
                    background: linear-gradient(145deg, #ffffff 0%, #f0f7ff 50%, #e6f0ff 100%);
                    padding: 2.5rem;
                    border-radius: 16px;
                    box-shadow: 0 10px 25px rgba(24, 119, 242, 0.08);
                    margin: 1rem 0 2.5rem 0;
                    border: 1px solid rgba(24, 119, 242, 0.1);
                '>
                    <div style='
                        display: flex;
                        align-items: center;
                        margin-bottom: 1.2rem;
                        background: rgba(255, 255, 255, 0.8);
                        padding: 1rem 1.5rem;
                        border-radius: 12px;
                        box-shadow: 0 4px 15px rgba(24, 119, 242, 0.05);
                    '>
                        <div style='
                            font-size: 2.5rem;
                            margin-right: 1rem;
                            color: #1877F2;
                        '>{st.session_state.selected_tool['icon']}</div>
                        <div>
                            <h1 style='
                                margin: 0;
                                color: #1877F2;
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
            
            # Call the function for the selected tool
            if st.session_state.selected_tool["function"]:
                st.session_state.selected_tool["function"]()
            else:
                # Display coming soon or future tool information
                st.info(f"**{st.session_state.selected_tool['status'].replace('_', ' ').title()}!**")
                st.write(st.session_state.selected_tool["description"])
                st.image(f"https://via.placeholder.com/600x300?text={st.session_state.selected_tool['name']}+Coming+Soon", use_container_width=True)
    else:
        with dashboard_container:
            # Display the dashboard
            # Header
            st.markdown("""
            <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                <h1 style='color: #1877F2; text-align: center;'>📱 Facebook AI Writer</h1>
                <p style='text-align: center;'>Generate professional Facebook content with ALwrity's AI-powered tools</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Group tools by category
            categories = {}
            for tool in facebook_tools:
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
                        
                        st.markdown(f"""
                        <div style='background-color: {tool["color"]}; padding: 20px; border-radius: 10px; margin-bottom: 20px; color: white;'>
                            <h2 style='color: white;'>{tool["icon"]} {tool["name"]} {status_badge}</h2>
                            <p>{tool["description"]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add a button to access the tool
                        if st.button(f"Use {tool['name']}", key=f"btn_{tool['name']}"):
                            # Store the selected tool in session state
                            st.session_state.selected_tool = tool
                            st.rerun()


class FacebookAIWriter:
    """
    AI-powered content generator for Facebook marketing and communication.
    
    This class provides various tools for generating Facebook content including:
    - Posts and updates
    - Page About sections
    - Event descriptions
    - Ad copy
    """
    
    def __init__(self):
        """Initialize the Facebook AI Writer."""
        pass
    
    def generate_post(self, **kwargs) -> str:
        """Generate a Facebook post."""
        return write_fb_post(**kwargs)
    
    def generate_page_about(self, **kwargs) -> str:
        """Generate a Facebook Page About section."""
        return write_fb_page_about(**kwargs)
    
    def generate_event(self, **kwargs) -> str:
        """Generate a Facebook Event description."""
        return write_fb_event(**kwargs)
    
    def generate_ad_copy(self, **kwargs) -> Dict[str, Union[str, List[str]]]:
        """
        Generate Facebook Ad copy with variations.
        
        Returns:
            Dict containing the generated ad copy and its variations.
        """
        return write_fb_ad_copy(**kwargs)

# List of available tools
AVAILABLE_TOOLS = [
    'Post Generator',
    'Page About Generator',
    'Event Generator',
    'Ad Copy Generator'
]

# Coming soon features
COMING_SOON = [
    'Story Generator',
    'Poll Generator',
    'Group Post Generator',
    'Carousel Post Generator',
    'Comment Response Generator'
]

if __name__ == "__main__":
    facebook_main_menu()
