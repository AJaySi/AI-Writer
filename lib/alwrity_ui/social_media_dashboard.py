import streamlit as st
from lib.alwrity_ui.dashboard_styles import apply_dashboard_style, render_dashboard_header, render_card
from loguru import logger

def render_social_tools_dashboard():
    """Render the social media tools dashboard with premium glassmorphic design."""
    logger.info("Starting Social Media Tools Dashboard")
    
    # Apply common dashboard styling
    apply_dashboard_style()
    
    # Render dashboard header
    render_dashboard_header(
        "📱 AI Social Media Tools",
        "Create engaging social media content across all major platforms with our specialized AI writers. From viral posts to professional updates, we've got you covered."
    )

    # Define social tools with enhanced details and platform-specific styling
    social_tools = {
        "Facebook": {
            "icon": "📘",
            "description": "Create engaging Facebook posts, stories, and ads that drive meaningful interactions and build community",
            "category": "Social Network",
            "path": "facebook",
            "features": ["Post Generation", "Story Creation", "Ad Copy", "Community Management"]
        },
        "LinkedIn": {
            "icon": "💼",
            "description": "Generate professional LinkedIn content, articles, and networking posts that enhance your career presence",
            "category": "Professional",
            "path": "linkedin",
            "features": ["Professional Posts", "Article Writing", "Network Building", "Career Content"]
        },
        "Twitter": {
            "icon": "🐦",
            "description": "Craft viral tweets, threads, and engaging content that sparks conversations and grows your following",
            "category": "Microblogging",
            "path": "twitter",
            "features": ["Tweet Generation", "Thread Creation", "Hashtag Strategy", "Viral Content"]
        },
        "Instagram": {
            "icon": "📸",
            "description": "Create captivating Instagram captions, stories, and content that showcases your brand beautifully",
            "category": "Visual Content",
            "path": "instagram",
            "features": ["Caption Writing", "Story Content", "Hashtag Research", "Visual Strategy"]
        },
        "YouTube": {
            "icon": "🎥",
            "description": "Generate compelling video scripts, descriptions, and content strategies for your YouTube channel",
            "category": "Video Content",
            "path": "youtube",
            "features": ["Script Writing", "Video Descriptions", "SEO Optimization", "Content Planning"]
        }
    }

    # Create a responsive grid of premium cards
    cols = st.columns(3)
    for idx, (platform, details) in enumerate(social_tools.items()):
        with cols[idx % 3]:
            # Use the common card renderer
            if render_card(
                icon=details['icon'],
                title=platform,
                description=details['description'],
                category=details['category'],
                key_suffix=f"social_{platform}",
                help_text=f"Open {platform} content creation tools - {details['description'][:50]}..."
            ):
                # Set query parameters to redirect to the specific tool
                st.query_params["tool"] = details["path"]
                st.rerun()

    # Add feature showcase section
    st.markdown("""
        <div style="margin-top: 3rem;">
            <div class="dashboard-header" style="margin-bottom: 2rem;">
                <h1 style="font-size: 2.2em;">✨ Platform Features</h1>
                <p>Each platform comes with specialized AI tools designed for optimal engagement and growth.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Feature grid
    feature_cols = st.columns(2)
    features = [
        {
            "title": "🎯 Smart Content Generation",
            "description": "AI-powered content creation tailored to each platform's unique audience and format requirements."
        },
        {
            "title": "📊 Engagement Optimization",
            "description": "Data-driven insights and suggestions to maximize likes, shares, comments, and overall engagement."
        },
        {
            "title": "🕒 Optimal Timing",
            "description": "AI recommendations for the best times to post based on your audience's activity patterns."
        },
        {
            "title": "🔍 Hashtag Intelligence",
            "description": "Smart hashtag suggestions and trending topic analysis to increase your content's discoverability."
        }
    ]

    for idx, feature in enumerate(features):
        with feature_cols[idx % 2]:
            st.markdown(f"""
                <div class="premium-card" style="min-height: 160px; cursor: default;">
                    <div class="card-glow"></div>
                    <div class="card-content">
                        <div class="card-title" style="margin-bottom: 0.8rem;">{feature['title']}</div>
                        <div class="card-description" style="margin-bottom: 0;">{feature['description']}</div>
                    </div>
                    <div class="card-shine"></div>
                </div>
            """, unsafe_allow_html=True)