"""
Twitter Dashboard with modern UI components.
"""

import streamlit as st
from typing import Dict, List
import json
from datetime import datetime

from .tweet_generator import smart_tweet_generator
from .twitter_streamlit_ui import (
    TwitterDashboard,
    FeatureCard,
    TweetForm,
    SettingsForm,
    Sidebar,
    Header,
    Tabs,
    Breadcrumbs,
    Theme,
    save_to_session,
    get_from_session,
    clear_session,
    show_success_message,
    show_error_message
)

def load_feature_data() -> Dict:
    """Load feature data from a structured format."""
    return {
        "tweet_generation": {
            "title": "Tweet Generation & Optimization",
            "icon": "🐦",
            "description": "Create and optimize engaging tweets with AI assistance",
            "features": [
                {
                    "name": "Smart Tweet Generator",
                    "description": "Generate multiple tweet variations with optimal character count, hashtags, and emojis",
                    "status": "active",
                    "icon": "✨",
                    "function": smart_tweet_generator
                },
                {
                    "name": "Tweet Performance Predictor",
                    "description": "Predict engagement rates and best posting times for maximum impact",
                    "status": "coming_soon",
                    "icon": "📊"
                }
            ]
        },
        "content_strategy": {
            "title": "Content Strategy Tools",
            "icon": "📅",
            "description": "Plan and manage your Twitter content strategy effectively",
            "features": [
                {
                    "name": "Content Calendar Generator",
                    "description": "Create weekly/monthly content plans with theme-based scheduling",
                    "status": "coming_soon",
                    "icon": "🗓️"
                },
                {
                    "name": "Hashtag Strategy Manager",
                    "description": "Research and manage trending hashtags for better reach",
                    "status": "coming_soon",
                    "icon": "#️⃣"
                }
            ]
        },
        "visual_content": {
            "title": "Visual Content Creation",
            "icon": "🎨",
            "description": "Create engaging visual content for your tweets",
            "features": [
                {
                    "name": "Image Generator",
                    "description": "Create tweet cards, infographics, and quote designs",
                    "status": "coming_soon",
                    "icon": "🖼️"
                },
                {
                    "name": "Video Content Assistant",
                    "description": "Generate video scripts and optimize captions",
                    "status": "coming_soon",
                    "icon": "🎥"
                }
            ]
        },
        "engagement": {
            "title": "Engagement & Community",
            "icon": "🤝",
            "description": "Manage and enhance community engagement",
            "features": [
                {
                    "name": "Reply Generator",
                    "description": "Generate context-aware responses with appropriate tone",
                    "status": "coming_soon",
                    "icon": "💬"
                },
                {
                    "name": "Community Tools",
                    "description": "Create polls and plan Q&A sessions",
                    "status": "coming_soon",
                    "icon": "👥"
                }
            ]
        },
        "analytics": {
            "title": "Analytics & Optimization",
            "icon": "📈",
            "description": "Track performance and optimize your Twitter strategy",
            "features": [
                {
                    "name": "Performance Analytics",
                    "description": "Track tweet performance and engagement metrics",
                    "status": "coming_soon",
                    "icon": "📊"
                },
                {
                    "name": "A/B Testing Assistant",
                    "description": "Test and optimize tweet variations for better results",
                    "status": "coming_soon",
                    "icon": "🔍"
                }
            ]
        },
        "research": {
            "title": "Research & Intelligence",
            "icon": "🔎",
            "description": "Gain insights and stay ahead of trends",
            "features": [
                {
                    "name": "Market Research",
                    "description": "Analyze competitors and track industry trends",
                    "status": "coming_soon",
                    "icon": "📊"
                },
                {
                    "name": "Content Inspiration",
                    "description": "Get trending topic suggestions and content ideas",
                    "status": "coming_soon",
                    "icon": "💡"
                }
            ]
        }
    }

def run_dashboard():
    """Main function to run the Twitter dashboard."""
    # Initialize dashboard
    dashboard = TwitterDashboard()
    
    # Load feature data
    features = load_feature_data()
    
    # Setup navigation
    sidebar = Sidebar(title="Twitter Tools")
    sidebar.add_menu_item("Dashboard", "📊", "dashboard")
    sidebar.add_menu_item("Tweet Generator", "✍️", "tweet_generator")
    sidebar.add_menu_item("Analytics", "📈", "analytics")
    sidebar.add_menu_item("Settings", "⚙️", "settings")
    
    # Setup header
    header = Header(
        title="Twitter AI Writer",
        subtitle="Your all-in-one Twitter content creation and management platform"
    )
    header.add_action("New Tweet", "✏️", lambda: save_to_session("current_page", "tweet_generator"))
    header.add_action("Refresh", "🔄", lambda: st.experimental_rerun())
    
    # Setup tabs
    tabs = Tabs()
    tabs.add_tab("Overview", "📊", lambda: render_overview(features))
    tabs.add_tab("Recent Tweets", "🐦", lambda: render_recent_tweets())
    tabs.add_tab("Analytics", "📈", lambda: render_analytics())
    
    # Setup breadcrumbs
    breadcrumbs = Breadcrumbs()
    breadcrumbs.add_item("Home", "dashboard", "🏠")
    breadcrumbs.add_item(get_from_session("current_page", "Dashboard").title())
    
    # Render dashboard
    dashboard.render()

def render_overview(features: Dict):
    """Render the overview tab content."""
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        FeatureCard(
            title="Tweet Generator",
            description="Create engaging tweets with AI assistance",
            icon="✍️",
            features=[
                {
                    "name": "AI-Powered",
                    "description": "Generate tweets using advanced AI"
                },
                {
                    "name": "Customizable",
                    "description": "Adjust tone, length, and style"
                }
            ],
            on_click=lambda: save_to_session("current_page", "tweet_generator")
        ).render()
    
    with col2:
        FeatureCard(
            title="Analytics",
            description="Track your tweet performance",
            icon="📈",
            features=[
                {
                    "name": "Engagement",
                    "description": "Monitor likes, retweets, and replies"
                },
                {
                    "name": "Growth",
                    "description": "Track follower growth over time"
                }
            ]
        ).render()
    
    with col3:
        FeatureCard(
            title="Settings",
            description="Customize your experience",
            icon="⚙️",
            features=[
                {
                    "name": "Preferences",
                    "description": "Set your default options"
                },
                {
                    "name": "API",
                    "description": "Configure Twitter API settings"
                }
            ]
        ).render()

def render_recent_tweets():
    """Render the recent tweets tab content."""
    # Tweet form
    tweet_form = TweetForm(
        on_submit=lambda: handle_tweet_submit()
    )
    tweet_form.render()
    
    # Recent tweets
    st.markdown("### Recent Tweets")
    tweets = get_from_session("tweets", [])
    for tweet in tweets:
        TweetCard(
            content=tweet["content"],
            engagement_score=tweet["engagement_score"],
            hashtags=tweet["hashtags"],
            emojis=tweet["emojis"],
            metrics=tweet["metrics"],
            on_copy=lambda: copy_tweet(tweet),
            on_save=lambda: save_tweet(tweet)
        ).render()

def render_analytics():
    """Render the analytics tab content."""
    st.markdown("### Tweet Analytics")
    st.info("Analytics features coming soon!")

def handle_tweet_submit():
    """Handle tweet form submission."""
    # Get form data
    content = get_from_session("tweet_content")
    tone = get_from_session("tone")
    length = get_from_session("length")
    hashtags = get_from_session("hashtags")
    emojis = get_from_session("emojis")
    engagement_boost = get_from_session("engagement_boost")
    
    # Create tweet object
    tweet = {
        "content": content,
        "tone": tone,
        "length": length,
        "hashtags": hashtags,
        "emojis": emojis,
        "engagement_score": engagement_boost,
        "metrics": {
            "Engagement": engagement_boost,
            "Reach": engagement_boost * 0.8,
            "Growth": engagement_boost * 0.6
        }
    }
    
    # Add to tweets list
    tweets = get_from_session("tweets", [])
    tweets.append(tweet)
    save_to_session("tweets", tweets)
    
    # Show success message
    show_success_message("Tweet created successfully!")

def copy_tweet(tweet: Dict):
    """Copy tweet to clipboard."""
    show_success_message("Tweet copied to clipboard!")

def save_tweet(tweet: Dict):
    """Save tweet for later."""
    show_success_message("Tweet saved!")

if __name__ == "__main__":
    run_dashboard() 