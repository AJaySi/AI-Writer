import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, List
import json
import base64

from .tweet_generator import smart_tweet_generator

def add_bg_from_base64(base64_string):
    """Add background image using base64 string."""
    return f'''
    <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* Enhanced styling for containers */
        .element-container, .stMarkdown, .stButton {{
            background-color: rgba(0, 0, 0, 0.7);
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            backdrop-filter: blur(10px);
        }}
        
        /* Typography enhancements */
        h1, h2, h3 {{
            color: #ffffff !important;
            font-family: 'Helvetica Neue', sans-serif;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}
        
        p, li {{
            color: #e0e0e0 !important;
            font-family: 'Helvetica Neue', sans-serif;
        }}
        
        /* Button styling */
        .stButton > button {{
            background: linear-gradient(45deg, #1DA1F2, #0C85D0);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
        }}
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: rgba(0, 0, 0, 0.6);
            padding: 10px;
            border-radius: 10px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: transparent;
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            background-color: rgba(29, 161, 242, 0.2);
        }}
        
        /* Feature card styling */
        .feature-card {{
            background: linear-gradient(135deg, rgba(29, 161, 242, 0.1), rgba(0, 0, 0, 0.3));
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            transition: transform 0.3s ease;
        }}
        
        .feature-card:hover {{
            transform: translateY(-5px);
        }}
        
        /* Status badge styling */
        .status-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        
        .status-active {{
            background: linear-gradient(45deg, #00C853, #69F0AE);
            color: #000000;
        }}
        
        .status-coming-soon {{
            background: linear-gradient(45deg, #FFD700, #FFA000);
            color: #000000;
        }}
    </style>
    '''

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
    status_class = "status-active" if feature['status'] == 'active' else "status-coming-soon"
    with st.container():
        st.markdown(f"""
            <div class='feature-card'>
                <h3 style='color: #ffffff; margin: 0;'>{feature['icon']} {feature['name']}</h3>
                <p style='color: #e0e0e0; margin: 10px 0;'>{feature['description']}</p>
                <span class='status-badge {status_class}'>
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

def get_space_background() -> str:
    """Return base64 encoded space-themed background."""
    return """iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mN8/+F9PQAJYgN4hWvGzQAAAABJRU5ErkJggg==""" # This is a placeholder. You'll need to replace with actual base64 image

def run_dashboard():
    """Main function to run the Twitter dashboard."""
    # Add space-themed background
    st.markdown(add_bg_from_base64(get_space_background()), unsafe_allow_html=True)
    
    # Enhanced Header with gradient text
    st.markdown("""
        <div style='text-align: center; padding: 40px 0;'>
            <h1 style='
                font-size: 3em;
                background: linear-gradient(45deg, #1DA1F2, #ffffff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
            '>🐦 Twitter AI Writer</h1>
            <p style='
                font-size: 1.2em;
                color: #e0e0e0;
                max-width: 600px;
                margin: 0 auto;
            '>Your all-in-one Twitter content creation and management platform. 
            Harness the power of AI to enhance your Twitter marketing strategy.</p>
        </div>
    """, unsafe_allow_html=True)

    # Load feature data
    features = load_feature_data()

    # Create tabs with enhanced styling
    tab1, tab2, tab3 = st.tabs(["🎯 Quick Actions", "📊 Analytics", "⚙️ Settings"])

    with tab1:
        st.markdown("<h2 style='color: #ffffff;'>🚀 Quick Actions</h2>", unsafe_allow_html=True)
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

    # Enhanced Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(0, 0, 0, 0.5); border-radius: 10px;'>
            <p style='color: #ffffff; margin-bottom: 10px;'>Need assistance? We're here to help!</p>
            <div style='display: flex; justify-content: center; gap: 20px;'>
                <a href='#' style='
                    text-decoration: none;
                    color: #1DA1F2;
                    background: rgba(255, 255, 255, 0.1);
                    padding: 8px 20px;
                    border-radius: 20px;
                    transition: all 0.3s ease;
                '>📚 Documentation</a>
                <a href='#' style='
                    text-decoration: none;
                    color: #1DA1F2;
                    background: rgba(255, 255, 255, 0.1);
                    padding: 8px 20px;
                    border-radius: 20px;
                    transition: all 0.3s ease;
                '>💬 Contact Support</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    run_dashboard() 