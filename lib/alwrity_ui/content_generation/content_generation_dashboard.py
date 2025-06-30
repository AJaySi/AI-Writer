import streamlit as st
from typing import Dict, List
from functools import lru_cache
from datetime import datetime
from loguru import logger

# Import all necessary AI writer functions
from lib.ai_writers.ai_blog_writer.ai_blog_generator import ai_blog_writer_page
from lib.ai_writers.ai_essay_writer import ai_essay_generator
from lib.ai_writers.ai_news_article_writer import ai_news_generation
from lib.utils.alwrity_utils import ai_news_writer, ai_finance_ta_writer, ai_social_writer, essay_writer
from lib.ai_writers.ai_facebook_writer.facebook_ai_writer import facebook_main_menu
from lib.ai_writers.linkedin_writer.linkedin_ai_writer import linkedin_main_menu
from lib.ai_writers.twitter_writers import run_dashboard as twitter_writer
from lib.ai_writers.insta_ai_writer import insta_writer
from lib.ai_writers.youtube_writers.youtube_ai_writer import youtube_main_menu
from lib.ai_writers.ai_agents_crew_writer import ai_agents_writers
from lib.utils.alwrity_utils import ai_agents_team

# Import SEO tools from ai_seo_tools
from lib.ai_seo_tools.on_page_seo_analyzer import analyze_onpage_seo
from lib.ai_seo_tools.weburl_seo_checker import url_seo_checker
from lib.ai_seo_tools.content_title_generator import ai_title_generator, generate_blog_titles
from lib.ai_seo_tools.meta_desc_generator import metadesc_generator_main
from lib.ai_seo_tools.seo_structured_data import ai_structured_data
from lib.ai_seo_tools.image_alt_text_generator import alt_text_gen
from lib.ai_seo_tools.opengraph_generator import og_tag_generator
from lib.ai_seo_tools.google_pagespeed_insights import google_pagespeed_insights
from lib.ai_seo_tools.sitemap_analysis import main as sitemap_analyzer
from lib.ai_seo_tools.twitter_tags_generator import display_app as twitter_tags_app
from lib.ai_seo_tools.enterprise_seo_suite import render_enterprise_seo_suite
from lib.alwrity_ui.seo_tools_dashboard import ai_seo_tools

@lru_cache(maxsize=None)
def get_tool_implementations() -> Dict[str, callable]:
    """
    Return a mapping of tool names to their implementation functions.
    Uses caching to avoid repeated imports.
    """
    tool_mapping = {
        # Text Generation Tools
        "AI Blog Writer": ai_blog_writer_page,
        "AI Essay Writer": essay_writer,
        "AI News Writer": ai_news_writer,
        "AI Content Team": ai_agents_team,
        
        # Business Content Tools
        "Financial TA Writer": ai_finance_ta_writer,
        "AI Social Media": ai_social_writer,
        
        # Social Media Specific Tools
        "Facebook Writer": facebook_main_menu,
        "LinkedIn Writer": linkedin_main_menu,
        "Twitter Writer": twitter_writer,
        "Instagram Writer": insta_writer,
        "YouTube Writer": youtube_main_menu,
        
        # SEO & Optimization Tools
        "SEO Dashboard": ai_seo_tools,
        "On-Page SEO Analyzer": analyze_onpage_seo,
        "URL SEO Checker": url_seo_checker,
        "AI Title Generator": lambda: _render_seo_tool("AI Title Generator", generate_blog_titles),
        "Meta Description Generator": metadesc_generator_main,
        "Structured Data Generator": ai_structured_data,
        "Alt Text Generator": alt_text_gen,
        "OpenGraph Tags": og_tag_generator,
        "Page Speed Insights": google_pagespeed_insights,
        "Sitemap Analyzer": sitemap_analyzer,
        "Twitter Cards Generator": twitter_tags_app,
        "Enterprise SEO Suite": render_enterprise_seo_suite,
        
        # Creative Content Tools - placeholder functions for now
        "Story Generator": lambda: st.info("Story Generator coming soon!"),
        "Poetry Writer": lambda: st.info("Poetry Writer coming soon!"),
        "Script Writer": lambda: st.info("Script Writer coming soon!"),
        "Email Templates": lambda: st.info("Email Templates coming soon!"),
        
        # Marketing Content Tools - placeholder functions
        "Ad Copy Generator": lambda: st.info("Ad Copy Generator coming soon!"),
        "Product Descriptions": lambda: st.info("Product Descriptions coming soon!"),
        "Press Releases": lambda: st.info("Press Releases coming soon!"),
        "Landing Page Copy": lambda: st.info("Landing Page Copy coming soon!"),
        
        # Educational Content Tools - placeholder functions
        "Course Content": lambda: st.info("Course Content coming soon!"),
        "Tutorial Writer": lambda: st.info("Tutorial Writer coming soon!"),
        "Quiz Generator": lambda: st.info("Quiz Generator coming soon!"),
        "Study Guides": lambda: st.info("Study Guides coming soon!")
    }
    
    # Handle import errors gracefully
    failed_imports = []
    working_tools = {}
    
    for tool_name, tool_func in tool_mapping.items():
        try:
            # Test if the function is callable
            if callable(tool_func):
                working_tools[tool_name] = tool_func
            else:
                failed_imports.append(tool_name)
        except Exception as e:
            logger.warning(f"Failed to load tool {tool_name}: {e}")
            failed_imports.append(tool_name)
    
    if failed_imports:
        logger.info(f"Some tools are not available: {failed_imports}")
    
    return working_tools

def _render_seo_tool(tool_name: str, tool_function):
    """Render SEO tools with consistent styling and handle errors."""
    st.markdown(f"## 🔍 {tool_name}")
    st.markdown("---")
    
    # Handle AI Title Generator specifically
    if "Title Generator" in tool_name:
        _render_title_generator_ui()
    else:
        # For other SEO tools, call them directly
        try:
            if callable(tool_function):
                tool_function()
            else:
                st.warning(f"Tool '{tool_name}' is not properly configured.")
        except Exception as e:
            st.error(f"Error loading tool: {str(e)}")
            logger.error(f"Error in SEO tool {tool_name}: {str(e)}")

def _render_title_generator_ui():
    """Render a custom UI for the AI Title Generator."""
    st.markdown("### Generate SEO-Optimized Titles")
    
    # Input form
    with st.form("title_generator_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            keywords = st.text_input(
                "Blog Keywords",
                placeholder="Enter your main keywords (comma-separated)",
                help="Primary keywords for your content"
            )
            
            title_type = st.selectbox(
                "Content Type",
                ["How-to Guide", "Listicle", "News Article", "Product Review", "Tutorial", "Case Study", "Opinion", "Research"]
            )
        
        with col2:
            content = st.text_area(
                "Blog Content (Optional)",
                placeholder="Paste your blog content here for more targeted titles...",
                height=100,
                help="Optional: Paste existing content for more relevant titles"
            )
            
            title_intent = st.selectbox(
                "Search Intent",
                ["Informational", "Commercial", "Transactional", "Navigational"]
            )
        
        language = st.selectbox(
            "Language",
            ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Hindi"]
        )
        
        submitted = st.form_submit_button("🚀 Generate Titles", use_container_width=True)
    
    if submitted:
        if not keywords:
            st.warning("Please enter at least some keywords to generate titles.")
            return
        
        with st.spinner("🎯 Generating SEO-optimized titles..."):
            try:
                # Import and call the title generation function
                from lib.ai_seo_tools.content_title_generator import generate_blog_titles
                
                result = generate_blog_titles(
                    input_blog_keywords=keywords,
                    input_blog_content=content if content else None,
                    input_title_type=title_type,
                    input_title_intent=title_intent,
                    input_language=language
                )
                
                if result:
                    st.success("✅ Titles generated successfully!")
                    st.markdown("### 🎯 Your SEO-Optimized Titles:")
                    
                    # Display the result in a nice format
                    st.markdown(f"```\n{result}\n```")
                    
                    # Add copy buttons or additional features
                    if st.button("📋 Copy All Titles"):
                        st.success("Titles copied to clipboard! (Feature coming soon)")
                else:
                    st.error("Failed to generate titles. Please try again.")
                    
            except Exception as e:
                st.error(f"Error generating titles: {str(e)}")
                logger.error(f"Title generation error: {str(e)}")

def render_content_generation_dashboard():
    """Main function to render the content generation dashboard."""
    # Initialize dashboard state
    dashboard_state = DashboardState()
    
    # Apply modern CSS
    apply_modern_css()
    
    # Main dashboard header
    st.markdown("""
    <div class="main-dashboard">
        <div class="dashboard-title">🚀 Alwrity Content Hub</div>
        <div class="dashboard-subtitle">
            Complete AI-powered content creation and SEO optimization suite. From writing to ranking - everything you need in one place.
        </div>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem; flex-wrap: wrap;">
            <div style="text-align: center;">
                <div style="font-size: 2rem;">✍️</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">AI Writing</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">🔍</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">SEO Tools</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">📱</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Social Media</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">📊</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Analytics</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick access section
    st.markdown("""
    <div class="quick-access">
        <div class="section-title">⚡ Quick Access</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Recent tools
    if st.session_state.get('recent_tools'):
        st.markdown("### 📝 Recently Used")
        cols = st.columns(min(len(st.session_state.recent_tools), 5))
        for idx, tool in enumerate(st.session_state.recent_tools[:5]):
            with cols[idx]:
                if st.button(f"🔄 {tool}", key=f"recent_{tool}_{idx}"):
                    handle_tool_selection(tool, dashboard_state)
    
    # Popular tools
    popular_tools = ToolAnalytics.get_popular_tools()
    if popular_tools:
        st.markdown("### 🔥 Popular Tools")
        cols = st.columns(min(len(popular_tools), 5))
        for idx, tool in enumerate(popular_tools[:5]):
            with cols[idx]:
                if st.button(f"⭐ {tool}", key=f"popular_{tool}_{idx}"):
                    handle_tool_selection(tool, dashboard_state)
    
    # Content tools by category
    content_tools = {
        "Text Generation": {
            "tools": [
                {"name": "AI Blog Writer", "icon": "✍️", "desc": "Create SEO-optimized blog posts with AI assistance"},
                {"name": "AI Essay Writer", "icon": "📝", "desc": "Generate academic essays and research papers"},
                {"name": "AI News Writer", "icon": "📰", "desc": "Write breaking news articles and reports"},
                {"name": "AI Content Team", "icon": "👥", "desc": "Collaborative AI writing team for complex projects"}
            ]
        },
        "SEO & Optimization": {
            "tools": [
                {"name": "SEO Dashboard", "icon": "🔍", "desc": "Comprehensive SEO tools and analytics dashboard"},
                {"name": "On-Page SEO Analyzer", "icon": "📊", "desc": "Analyze and optimize individual page SEO elements"},
                {"name": "AI Title Generator", "icon": "🏷️", "desc": "Generate SEO-optimized titles for better rankings"},
                {"name": "Meta Description Generator", "icon": "📄", "desc": "Create compelling meta descriptions that drive clicks"},
                {"name": "Structured Data Generator", "icon": "🏗️", "desc": "Generate schema markup for rich search results"},
                {"name": "Page Speed Insights", "icon": "⚡", "desc": "Analyze and improve website performance metrics"},
                {"name": "Enterprise SEO Suite", "icon": "🏢", "desc": "Advanced SEO workflows for enterprise needs"}
            ]
        },
        "Business Content": {
            "tools": [
                {"name": "Financial TA Writer", "icon": "📊", "desc": "Generate technical analysis reports for stocks"},
                {"name": "Email Templates", "icon": "📧", "desc": "Professional email templates for business"},
                {"name": "Press Releases", "icon": "📢", "desc": "Company announcements and press releases"},
                {"name": "Landing Page Copy", "icon": "🌐", "desc": "High-converting landing page content"}
            ]
        },
        "Social Media": {
            "tools": [
                {"name": "Facebook Writer", "icon": "📘", "desc": "Facebook posts, ads, and content strategies"},
                {"name": "LinkedIn Writer", "icon": "💼", "desc": "Professional LinkedIn articles and posts"},
                {"name": "Twitter Writer", "icon": "🐦", "desc": "Engaging tweets and Twitter threads"},
                {"name": "Instagram Writer", "icon": "📷", "desc": "Instagram captions and story content"},
                {"name": "YouTube Writer", "icon": "🎬", "desc": "YouTube descriptions and video scripts"},
                {"name": "OpenGraph Tags", "icon": "🔗", "desc": "Optimize social media sharing with Open Graph tags"},
                {"name": "Twitter Cards Generator", "icon": "🐦", "desc": "Create Twitter Card markup for rich previews"}
            ]
        },
        "Creative Content": {
            "tools": [
                {"name": "Story Generator", "icon": "📚", "desc": "Creative short stories and narratives"},
                {"name": "Poetry Writer", "icon": "🎭", "desc": "Beautiful poems and verses"},
                {"name": "Script Writer", "icon": "🎬", "desc": "Scripts for videos, plays, and presentations"},
                {"name": "Song Lyrics", "icon": "🎵", "desc": "Original song lyrics and musical content"}
            ]
        }
    }
    
    # Render categories
    for category, category_data in content_tools.items():
        st.markdown(f"""
        <div class="category-section">
            <div class="category-header">{category}</div>
            <div class="category-grid">
        """, unsafe_allow_html=True)
        
        # Create columns for tools in this category
        tools = category_data["tools"]
        cols = st.columns(min(len(tools), 3))
        
        for idx, tool in enumerate(tools):
            col_idx = idx % 3
            with cols[col_idx]:
                # Create tool card with button
                if st.button(
                    f"{tool['icon']} {tool['name']}\n{tool['desc']}", 
                    key=f"tool_{tool['name']}_{category}",
                    help=tool['desc']
                ):
                    handle_tool_selection(tool['name'], dashboard_state)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Footer with statistics
    st.markdown("---")
    st.markdown("### 📈 Alwrity Analytics")
    col1, col2, col3, col4 = st.columns(4)
    
    total_tools = len(get_tool_implementations())
    seo_tools_count = len([tool for category in content_tools.values() for tool in category["tools"] if "SEO" in category.get("name", "") or any(seo_keyword in tool["name"] for seo_keyword in ["SEO", "Meta", "Title", "Structured", "Speed", "OpenGraph"])])
    
    with col1:
        st.metric("🛠️ Total Tools", total_tools)
    with col2:
        st.metric("🔍 SEO Tools", 12)  # Based on our SEO tool count
    with col3:
        st.metric("📝 Recent Tools", len(st.session_state.get('recent_tools', [])))
    with col4:
        st.metric("⭐ Favorites", len(st.session_state.get('favorite_tools', [])))
    
    # Add capability showcase
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
        <h4 style="color: #2c3e50; margin-bottom: 1rem;">✨ Why Choose Alwrity?</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
            <div>
                <strong>🎯 All-in-One Solution</strong><br>
                <small>Content creation, SEO optimization, and social media management in one platform</small>
            </div>
            <div>
                <strong>🤖 AI-Powered Intelligence</strong><br>
                <small>Advanced AI models for content generation and SEO analysis</small>
            </div>
            <div>
                <strong>📊 Enterprise-Ready</strong><br>
                <small>Scalable tools designed for teams and enterprise workflows</small>
            </div>
            <div>
                <strong>🚀 Continuously Updated</strong><br>
                <small>Regular updates with new tools and enhanced capabilities</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

class DashboardState:
    """Manage dashboard state and user preferences."""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables."""
        if 'recent_tools' not in st.session_state:
            st.session_state.recent_tools = []
        if 'favorite_tools' not in st.session_state:
            st.session_state.favorite_tools = []
        if 'tool_usage_count' not in st.session_state:
            st.session_state.tool_usage_count = {}
    
    def add_recent_tool(self, tool_name: str):
        """Add a tool to recent tools list."""
        if tool_name in st.session_state.recent_tools:
            st.session_state.recent_tools.remove(tool_name)
        st.session_state.recent_tools.insert(0, tool_name)
        # Keep only last 5 recent tools
        st.session_state.recent_tools = st.session_state.recent_tools[:5]
    
    def toggle_favorite(self, tool_name: str):
        """Toggle tool favorite status."""
        if tool_name in st.session_state.favorite_tools:
            st.session_state.favorite_tools.remove(tool_name)
        else:
            st.session_state.favorite_tools.append(tool_name)
    
    def increment_usage(self, tool_name: str):
        """Increment tool usage count."""
        st.session_state.tool_usage_count[tool_name] = st.session_state.tool_usage_count.get(tool_name, 0) + 1

class ToolAnalytics:
    """Analytics for tool usage and recommendations."""
    
    @staticmethod
    def get_popular_tools(limit: int = 5) -> List[str]:
        """Get most popular tools based on usage."""
        usage_count = st.session_state.get('tool_usage_count', {})
        if not usage_count:
            # Return default popular tools showcasing Alwrity's key capabilities
            return ["AI Blog Writer", "SEO Dashboard", "AI Title Generator", "Meta Description Generator", "On-Page SEO Analyzer"]
        
        sorted_tools = sorted(usage_count.items(), key=lambda x: x[1], reverse=True)
        return [tool[0] for tool in sorted_tools[:limit]]

def apply_modern_css():
    """Apply modern CSS styling to the dashboard."""
    st.markdown("""
    <style>
    /* Main dashboard styling */
    .main-dashboard {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .dashboard-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .dashboard-subtitle {
        font-size: 1.2rem;
        text-align: center;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    
    /* Tool cards */
    .tool-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        border: 2px solid transparent;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .tool-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border-color: #667eea;
    }
    
    .tool-icon {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .tool-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .tool-description {
        font-size: 0.9rem;
        color: #666;
        text-align: center;
        line-height: 1.4;
    }
    
    /* Quick access section */
    .quick-access {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Recent tools styling */
    .recent-tool {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.25rem;
        font-weight: 500;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .recent-tool:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
    }
    
    /* Category sections */
    .category-section {
        margin-bottom: 3rem;
    }
    
    .category-header {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px 10px 0 0;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 0 0 10px 10px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .dashboard-title {
            font-size: 2rem;
        }
        .category-grid {
            grid-template-columns: 1fr;
        }
        .tool-card {
            height: auto;
            min-height: 150px;
        }
    }
    
    /* Success and info messages */
    .success-message {
        background: linear-gradient(135deg, #56ab2f, #a8e6cf);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .info-message {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def handle_tool_selection(tool_name: str, dashboard_state: DashboardState):
    """Handle tool selection and navigation."""
    try:
        # Update usage statistics
        dashboard_state.add_recent_tool(tool_name)
        dashboard_state.increment_usage(tool_name)
        
        # Get tool implementations
        tools = get_tool_implementations()
        
        if tool_name in tools:
            st.markdown(f"<div class='success-message'>🚀 Launching {tool_name}...</div>", unsafe_allow_html=True)
            
            # Show loading state
            with st.spinner(f"Loading {tool_name}..."):
                try:
                    # Execute the tool function
                    tools[tool_name]()
                    logger.info(f"Successfully launched tool: {tool_name}")
                except Exception as e:
                    st.error(f"Error running {tool_name}: {str(e)}")
                    logger.error(f"Error running tool {tool_name}: {e}")
        else:
            st.warning(f"Tool '{tool_name}' is not available yet.")
            
    except ImportError as e:
        st.error(f"Unable to load {tool_name}. Some dependencies may be missing.")
        logger.error(f"Import error for {tool_name}: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        logger.error(f"Unexpected error in tool selection: {e}")

# Main entry point
if __name__ == "__main__":
    render_content_generation_dashboard()