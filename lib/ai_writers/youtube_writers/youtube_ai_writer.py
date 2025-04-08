"""
YouTube AI Writer

This module provides a comprehensive suite of tools for generating YouTube content.
"""

import streamlit as st
import importlib
import sys
import os
from pathlib import Path
from .modules.title_generator import write_yt_title
from .modules.description_generator import write_yt_description
from .modules.script_generator import write_yt_script
from .modules.thumbnail_generator import write_yt_thumbnail
from .modules.end_screen_generator import write_yt_end_screen


def youtube_main_menu():
    """Main function for the YouTube AI Writer."""
    
    # Initialize session state for selected tool if it doesn't exist
    if "selected_tool" not in st.session_state:
        st.session_state.selected_tool = None
    
    # Define the YouTube tools with their details
    youtube_tools = [
        # Content Creation Tools
        {
            "name": "YT Title Generator",
            "icon": "📝",
            "description": "Create engaging YouTube video titles that drive clicks and views.",
            "color": "#FF0000",  # YouTube red
            "category": "Content Creation",
            "function": write_yt_title,
            "status": "active"
        },
        {
            "name": "YT Description Generator",
            "icon": "📄",
            "description": "Generate SEO-optimized descriptions for your YouTube videos.",
            "color": "#FF0000",  # YouTube red
            "category": "Content Creation",
            "function": write_yt_description,
            "status": "active"
        },
        {
            "name": "YT Script Generator",
            "icon": "🎬",
            "description": "Create professional YouTube scripts with optimized structures for engagement.",
            "color": "#FF0000",  # YouTube red
            "category": "Content Creation",
            "function": write_yt_script,
            "status": "active"
        },
        
        # Optimization Tools
        {
            "name": "Thumbnail Generator",
            "icon": "🎨",
            "description": "Create engaging thumbnail ideas and descriptions with color scheme suggestions based on your brand.",
            "color": "#FF0000",  # YouTube red
            "category": "Optimization",
            "function": write_yt_thumbnail,
            "status": "active"
        },
        {
            "name": "Tags Generator",
            "icon": "🏷️",
            "description": "Generate optimized tags for your videos with trending tag suggestions to improve discoverability.",
            "color": "#CC0000",  # Darker red for coming soon
            "category": "Optimization",
            "function": None,
            "status": "coming_soon"
        },
        
        # Engagement Tools (Coming Soon)
        {
            "name": "End Screen Generator",
            "icon": "🎬",
            "description": "Create effective end screen content and CTAs with template suggestions based on video type.",
            "color": "#FF0000",  # YouTube red
            "category": "Engagement",
            "function": write_yt_end_screen,
            "status": "active"
        },
        {
            "name": "Playlist Description Generator",
            "icon": "📚",
            "description": "Generate SEO-optimized descriptions for your playlists with organization suggestions.",
            "color": "#CC0000",  # Darker red for coming soon
            "category": "Engagement",
            "function": None,
            "status": "coming_soon"
        },
        
        # Future Tools (Coming Soon)
        {
            "name": "Analytics Insights",
            "icon": "📊",
            "description": "Get AI-powered insights and recommendations based on your channel analytics.",
            "color": "#990000",  # Even darker red for future
            "category": "Future Tools",
            "function": None,
            "status": "future"
        },
        {
            "name": "Channel Trailer Generator",
            "icon": "🎥",
            "description": "Create compelling channel trailers that convert visitors into subscribers.",
            "color": "#990000",  # Even darker red for future
            "category": "Future Tools",
            "function": None,
            "status": "future"
        },
        {
            "name": "Video Series Planner",
            "icon": "📅",
            "description": "Plan and organize your video series with content calendars and topic ideas.",
            "color": "#990000",  # Even darker red for future
            "category": "Future Tools",
            "function": None,
            "status": "future"
        },
        {
            "name": "Shorts Script Generator",
            "icon": "📱",
            "description": "Create engaging scripts optimized for YouTube Shorts format.",
            "color": "#990000",  # Even darker red for future
            "category": "Future Tools",
            "function": None,
            "status": "future"
        },
        {
            "name": "Community Post Generator",
            "icon": "💬",
            "description": "Generate engaging community posts to keep your audience active between videos.",
            "color": "#990000",  # Even darker red for future
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
                # Directly call the function instead of using it as a reference
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
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h1 style='color: #FF0000; text-align: center;'>🎥 YouTube AI Writer</h1>
                <p style='text-align: center;'>Generate professional YouTube content with AI-powered tools</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Introduction
            st.markdown("""
            ## Welcome to the YouTube AI Writer Suite
            
            This dashboard provides access to a variety of tools for creating and optimizing YouTube content. 
            Select a tool below to get started with generating professional content for your channel.
            
            ### How to Use This Dashboard
            
            1. Browse the available tools below
            2. Click on a tool card to access its specific functionality
            3. Fill in the required information
            4. Generate high-quality content for your YouTube channel
            """)
            
            # Group tools by category
            categories = {}
            for tool in youtube_tools:
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
    youtube_ai_writer()
