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
from ...gpt_providers.text_generation.main_text_generation import llm_text_gen
from .modules.post_generator import write_fb_post
from .modules.story_generator import write_fb_story
#from .modules.reel_generator import write_fb_reel
#from .modules.carousel_generator import write_fb_carousel
#from .modules.event_generator import write_fb_event
#from .modules.group_post_generator import write_fb_group_post
#from .modules.page_about_generator import write_fb_page_about
#from .modules.ad_copy_generator import write_fb_ad_copy
#from .modules.hashtag_generator import write_fb_hashtags
#from .modules.engagement_analyzer import analyze_fb_engagement

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
            # Display the selected tool's input section
            st.markdown("---")
            st.markdown(f"# {st.session_state.selected_tool['icon']} {st.session_state.selected_tool['name']}")
            
            # Add a back button
            if st.button("← Back to Dashboard", key="back_to_dashboard"):
                # Clear the selected tool from session state
                st.session_state.selected_tool = None
                st.rerun()
            
            # Call the function for the selected tool
            if st.session_state.selected_tool["function"]:
                st.session_state.selected_tool["function"]()
            else:
                # Display coming soon or future tool information
                st.info(f"**{st.session_state.selected_tool['status'].replace('_', ' ').title()}!**")
                st.write(st.session_state.selected_tool["description"])
                st.image(f"https://via.placeholder.com/600x300?text={st.session_state.selected_tool['name']}+Coming+Soon", use_column_width=True)
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


if __name__ == "__main__":
    facebook_main_menu()
