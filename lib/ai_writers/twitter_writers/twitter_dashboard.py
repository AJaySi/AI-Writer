import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, List
import json

from .tweet_generator import smart_tweet_generator

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

def render_feature_card(feature: Dict) -> None:
    """Render a single feature card with its details."""
    with st.container():
        st.markdown(f"""
            <div style='padding: 20px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 20px;'>
                <h3 style='margin: 0;'>{feature['icon']} {feature['name']}</h3>
                <p style='margin: 10px 0;'>{feature['description']}</p>
                <span style='background-color: {'#4CAF50' if feature['status'] == 'active' else '#ffd700'}; 
                            padding: 5px 10px; border-radius: 15px; font-size: 0.8em;'>
                    {feature['status'].title()}
                </span>
            </div>
        """, unsafe_allow_html=True)

def render_category_section(category: Dict) -> None:
    """Render a category section with all its features."""
    st.markdown(f"### {category['icon']} {category['title']}")
    st.markdown(f"*{category['description']}*")
    
    col1, col2 = st.columns(2)
    with col1:
        render_feature_card(category['features'][0])
    with col2:
        render_feature_card(category['features'][1])

def run_dashboard():
    """Main function to run the Twitter dashboard."""
    # Header
    st.title("🐦 Twitter AI Writer Dashboard")
    st.markdown("""
        Welcome to your all-in-one Twitter content creation and management platform. 
        Explore our AI-powered tools to enhance your Twitter marketing strategy.
    """)

    # Load feature data
    features = load_feature_data()

    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🎯 Quick Actions", "📊 Analytics", "⚙️ Settings"])

    with tab1:
        st.markdown("### 🚀 Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📝 Create New Tweet", use_container_width=True):
                # Call the Smart Tweet Generator
                smart_tweet_generator()
        with col2:
            st.button("📅 Schedule Content", use_container_width=True)
        with col3:
            st.button("📊 View Analytics", use_container_width=True)

    with tab2:
        st.markdown("### 📈 Analytics Dashboard")
        st.info("Analytics features coming soon! Stay tuned for detailed insights and performance metrics.")

    with tab3:
        st.markdown("### ⚙️ Settings")
        st.info("Settings and configuration options coming soon!")

    # Main content area
    st.markdown("## 🛠️ Available Tools")
    
    # Render each category
    for category in features.values():
        render_category_section(category)
        
        # If this is the tweet generation category and the Smart Tweet Generator is active,
        # add a button to launch it
        if category["title"] == "Tweet Generation & Optimization" and category["features"][0]["status"] == "active":
            if st.button(f"🚀 Launch {category['features'][0]['name']}", use_container_width=True):
                category["features"][0]["function"]()

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center;'>
            <p>Need help? Check out our <a href='#'>documentation</a> or <a href='#'>contact support</a></p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    run_dashboard() 