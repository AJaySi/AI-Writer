import streamlit as st
from lib.utils.alwrity_utils import (essay_writer, ai_news_writer, ai_finance_ta_writer)

from lib.ai_writers.ai_story_writer.story_writer import story_input_section
from lib.ai_writers.ai_product_description_writer import write_ai_prod_desc
from lib.ai_writers.ai_copywriter.copywriter_dashboard import copywriter_dashboard
from lib.ai_writers.linkedin_writer import LinkedInAIWriter
from lib.ai_writers.blog_rewriter_updater.ai_blog_rewriter import write_blog_rewriter
from lib.ai_writers.ai_blog_faqs_writer.faqs_ui import main as faqs_generator
from lib.ai_writers.ai_blog_writer.ai_blog_generator import ai_blog_writer_page
from lib.ai_writers.ai_outline_writer.outline_ui import main as outline_generator
from lib.alwrity_ui.dashboard_styles import apply_dashboard_style, render_dashboard_header, render_category_header, render_card
from loguru import logger

# Try to import AI Content Performance Predictor (AI-first approach)
try:
    from lib.content_performance_predictor.ai_performance_predictor import render_ai_predictor_ui as render_content_performance_predictor
    AI_PREDICTOR_AVAILABLE = True
    logger.info("AI Content Performance Predictor loaded successfully")
except ImportError:
    logger.warning("AI Content Performance Predictor not available")
    render_content_performance_predictor = None
    AI_PREDICTOR_AVAILABLE = False

# Try to import Bootstrap AI Competitive Suite
try:
    from lib.ai_competitive_suite.bootstrap_ai_suite import render_bootstrap_ai_suite
    BOOTSTRAP_SUITE_AVAILABLE = True
    logger.info("Bootstrap AI Competitive Suite loaded successfully")
except ImportError:
    logger.warning("Bootstrap AI Competitive Suite not available")
    render_bootstrap_ai_suite = None
    BOOTSTRAP_SUITE_AVAILABLE = False

def list_ai_writers():
    """Return a list of available AI writers with their metadata (no UI rendering)."""
    writers = []
    
    # Add Content Performance Predictor if available
    if render_content_performance_predictor:
        # AI-first approach description
        if AI_PREDICTOR_AVAILABLE:
            description = "🎯 AI-powered content performance prediction with competitive intelligence - perfect for solo entrepreneurs"
            name = "AI Content Performance Predictor"
        else:
            description = "Predict content success before publishing with AI-powered performance analysis"
            name = "Content Performance Predictor"
        
        writers.append({
            "name": name,
            "icon": "🎯",
            "description": description,
            "category": "⭐ Featured",
            "function": render_content_performance_predictor,
            "path": "performance_predictor",
            "featured": True
        })
    
    # Add Bootstrap AI Competitive Suite if available
    if render_bootstrap_ai_suite:
        writers.append({
            "name": "Bootstrap AI Competitive Suite",
            "icon": "🚀",
            "description": "🥷 Complete AI-powered competitive toolkit: content performance prediction + competitive intelligence for solo entrepreneurs",
            "category": "⭐ Featured",
            "function": render_bootstrap_ai_suite,
            "path": "bootstrap_ai_suite",
            "featured": True
        })
    
    # Add existing writers
    writers.extend([
        {
            "name": "AI Blog Writer",
            "icon": "📝",
            "description": "Generate comprehensive blog posts from keywords, URLs, or uploaded content",
            "category": "Content Creation",
            "function": ai_blog_writer_page,
            "path": "ai_blog_writer"
        },
        {
            "name": "AI Blog Rewriter",
            "icon": "🔄",
            "description": "Rewrite and update existing blog content with improved quality and SEO optimization",
            "category": "Content Creation",
            "function": write_blog_rewriter,
            "path": "blog_rewriter"
        },
        {
            "name": "Story Writer",
            "icon": "📚",
            "description": "Create engaging stories and narratives with AI assistance",
            "category": "Creative Writing",
            "function": story_input_section,
            "path": "story_writer"
        },
        {
            "name": "Essay writer",
            "icon": "✍️",
            "description": "Generate well-structured essays on any topic",
            "category": "Academic",
            "function": essay_writer,
            "path": "essay_writer"
        },
        {
            "name": "Write News reports",
            "icon": "📰",
            "description": "Create professional news articles and reports",
            "category": "Journalism",
            "function": ai_news_writer,
            "path": "news_writer"
        },
        {
            "name": "Write Financial TA report",
            "icon": "📊",
            "description": "Generate technical analysis reports for financial markets",
            "category": "Finance",
            "function": ai_finance_ta_writer,
            "path": "financial_writer"
        },
        {
            "name": "AI Product Description Writer",
            "icon": "🛍️",
            "description": "Create compelling product descriptions that drive sales",
            "category": "E-commerce",
            "function": write_ai_prod_desc,
            "path": "product_writer"
        },
        {
            "name": "AI Copywriter",
            "icon": "✒️",
            "description": "Generate persuasive copy for marketing and advertising",
            "category": "Marketing",
            "function": copywriter_dashboard,
            "path": "copywriter"
        },
        {
            "name": "LinkedIn AI Writer",
            "icon": "💼",
            "description": "Create professional LinkedIn content that engages your network",
            "category": "Professional",
            "function": lambda: LinkedInAIWriter().run(),
            "path": "linkedin_writer"
        },
        {
            "name": "FAQ Generator",
            "icon": "❓",
            "description": "Generate comprehensive, well-researched FAQs from any content source with customizable options",
            "category": "Content Creation",
            "function": faqs_generator,
            "path": "faqs_generator"
        },
        {
            "name": "Blog Outline Generator",
            "icon": "📋",
            "description": "Create detailed blog outlines with AI-powered content generation and image integration",
            "category": "Content Creation",
            "function": outline_generator,
            "path": "outline_generator"
        }
    ])
    
    return writers

def get_ai_writers():
    """Main function to display AI writers dashboard with premium glassmorphic design."""
    logger.info("Starting AI Writers Dashboard")
    
    # Apply common dashboard styling
    apply_dashboard_style()
    
    # Render dashboard header
    render_dashboard_header(
        "🤖 AI Content Writers",
        "Choose from our collection of specialized AI writers, each designed for specific content types and industries. Create engaging, high-quality content with just a few clicks."
    )

    writers = list_ai_writers()
    logger.info(f"Found {len(writers)} AI writers")

    # Group writers by category for better organization
    categories = {}
    for writer in writers:
        category = writer["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(writer)

    # Render writers by category with common cards
    for category_name, category_writers in categories.items():
        render_category_header(category_name)
        
        # Create columns for this category
        cols = st.columns(min(len(category_writers), 3))
        
        for idx, writer in enumerate(category_writers):
            with cols[idx % 3]:
                # Use the common card renderer
                if render_card(
                    icon=writer['icon'],
                    title=writer['name'],
                    description=writer['description'],
                    category=writer['category'],
                    key_suffix=f"{writer['path']}_{category_name}",
                    help_text=f"Launch {writer['name']} - {writer['description']}"
                ):
                    logger.info(f"Selected writer: {writer['name']} with path: {writer['path']}")
                    st.session_state.selected_writer = writer
                    st.query_params["writer"] = writer['path']
                    logger.info(f"Updated query params with writer: {writer['path']}")
                    st.rerun()
        
        # Add spacing between categories
        st.markdown('<div class="category-spacer"></div>', unsafe_allow_html=True)

    logger.info("Finished rendering AI Writers Dashboard")
    
    return writers

# Remove the old ai_writers function since it's now integrated into get_ai_writers