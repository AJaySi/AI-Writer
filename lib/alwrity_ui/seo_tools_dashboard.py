import streamlit as st
from loguru import logger

from lib.ai_seo_tools.seo_structured_data import ai_structured_data
from lib.ai_seo_tools.content_title_generator import ai_title_generator
from lib.ai_seo_tools.meta_desc_generator import metadesc_generator_main
from lib.ai_seo_tools.image_alt_text_generator import alt_text_gen
from lib.ai_seo_tools.opengraph_generator import og_tag_generator
from lib.ai_seo_tools.optimize_images_for_upload import main_img_optimizer
from lib.ai_seo_tools.google_pagespeed_insights import google_pagespeed_insights
from lib.ai_seo_tools.on_page_seo_analyzer import analyze_onpage_seo
from lib.ai_seo_tools.weburl_seo_checker import url_seo_checker
from lib.ai_marketing_tools.ai_backlinker.backlinking_ui_streamlit import backlinking_ui
from lib.ai_seo_tools.content_gap_analysis.ui import ContentGapAnalysisUI
from lib.ai_seo_tools.content_calendar.ui.dashboard import ContentCalendarDashboard
from lib.alwrity_ui.dashboard_styles import apply_dashboard_style, render_dashboard_header, render_category_header, render_card

def render_content_gap_analysis():
    """Render the content gap analysis workflow interface."""
    from lib.ai_seo_tools.content_gap_analysis.ui import ContentGapAnalysisUI
    
    # Initialize and run the Content Gap Analysis UI
    ui = ContentGapAnalysisUI()
    ui.run()

def render_content_calendar():
    """Render the content calendar dashboard."""
    import logging
    import sys
    from datetime import datetime
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('content_calendar.log', mode='a')
        ]
    )
    logger = logging.getLogger('content_calendar')
    
    try:
        logger.info("Initializing Content Calendar Dashboard")
        dashboard = ContentCalendarDashboard()
        logger.info("Rendering Content Calendar Dashboard")
        dashboard.render()
        logger.info("Content Calendar Dashboard rendered successfully")
    except Exception as e:
        logger.error(f"Error rendering content calendar: {str(e)}", exc_info=True)
        st.error(f"An error occurred while loading the content calendar: {str(e)}")

def render_seo_tools_dashboard():
    """Render a modern dashboard for SEO tools with premium glassmorphic design."""
    
    # Apply common dashboard styling
    apply_dashboard_style()

    # Enhanced dashboard header with modern design
    render_dashboard_header(
        "🚀 SEO AI Power Suite",
        "Dominate search rankings with our comprehensive AI-powered SEO toolkit. From keyword research to content optimization, master every aspect of search engine optimization."
    )

    # Define SEO tools organized by category
    seo_tools = {
        "Research & Strategy": {
            "Color Analysis": {
                "icon": "🎨",
                "description": "Analyze website color schemes for optimal user experience and SEO performance",
                "category": "Analysis",
                "path": "color_analysis",
                "features": ["Color Psychology", "Accessibility Check", "Brand Analysis", "Conversion Optimization"]
            },
            "Keyword Research": {
                "icon": "🔑", 
                "description": "Discover high-impact keywords with advanced AI-powered research and competition analysis",
                "category": "Research",
                "path": "keyword_research",
                "features": ["Keyword Discovery", "Competition Analysis", "Search Volume", "Difficulty Scoring"]
            },
            "SEO Audit": {
                "icon": "🔍",
                "description": "Comprehensive website analysis with actionable insights for improving search rankings",
                "category": "Analysis",
                "path": "seo_audit",
                "features": ["Technical SEO", "Content Analysis", "Performance Check", "Mobile Optimization"]
            }
        },
        "Content Optimization": {
            "Content Optimizer": {
                "icon": "📝",
                "description": "Transform your content with AI-driven SEO optimization for maximum search visibility",
                "category": "Optimization",
                "path": "content_optimizer",
                "features": ["Content Analysis", "SEO Scoring", "Readability Check", "Meta Optimization"]
            },
            "Meta Generator": {
                "icon": "🏷️",
                "description": "Create compelling meta titles and descriptions that boost click-through rates",
                "category": "Optimization",
                "path": "meta_generator",
                "features": ["Title Generation", "Description Writing", "Character Optimization", "SERP Preview"]
            },
            "Schema Markup": {
                "icon": "🏗️",
                "description": "Generate structured data markup to enhance search result appearance",
                "category": "Technical",
                "path": "schema_markup",
                "features": ["Rich Snippets", "Local SEO", "Product Markup", "FAQ Schema"]
            }
        },
        "Analysis & Tracking": {
            "Rank Tracker": {
                "icon": "📊",
                "description": "Monitor keyword rankings and track your SEO progress with detailed analytics",
                "category": "Analytics",
                "path": "rank_tracker",
                "features": ["Position Tracking", "Progress Analytics", "Competitor Monitoring", "Ranking Reports"]
            },
            "Backlink Analyzer": {
                "icon": "🔗",
                "description": "Analyze your backlink profile and discover new link building opportunities",
                "category": "Analysis",
                "path": "backlink_analyzer",
                "features": ["Link Analysis", "Authority Metrics", "Anchor Text Analysis", "Toxic Link Detection"]
            },
            "Site Speed Test": {
                "icon": "⚡",
                "description": "Evaluate website performance and get optimization recommendations",
                "category": "Performance",
                "path": "speed_test",
                "features": ["Speed Analysis", "Core Web Vitals", "Optimization Tips", "Mobile Performance"]
            }
        }
    }

    # Render categories and tools
    for category, tools in seo_tools.items():
        # Render category header
        render_category_header(category)
        
        # Create responsive grid for tools in this category
        cols = st.columns(3)
        for idx, (tool_name, details) in enumerate(tools.items()):
            with cols[idx % 3]:
                # Use the common card renderer
                if render_card(
                    icon=details['icon'],
                    title=tool_name,
                    description=details['description'],
                    category=details['category'],
                    key_suffix=f"seo_{tool_name.replace(' ', '_')}",
                    help_text=f"Open {tool_name} - {details['description'][:50]}..."
                ):
                    # Set query parameters to redirect to the specific tool
                    st.query_params["tool"] = details["path"]
                    st.rerun()

    # Add SEO insights section
    st.markdown("""
        <div style="margin-top: 3rem;">
            <div class="dashboard-header" style="margin-bottom: 2rem;">
                <h1 style="font-size: 2.2em;">🎯 SEO Success Features</h1>
                <p>Comprehensive tools designed to boost your search engine rankings and drive organic traffic growth.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # SEO insights grid
    insight_cols = st.columns(2)
    insights = [
        {
            "title": "🤖 AI-Powered Analysis",
            "description": "Advanced machine learning algorithms analyze your content and provide data-driven optimization recommendations."
        },
        {
            "title": "📈 Real-Time Tracking",
            "description": "Monitor your SEO performance with live ranking updates and comprehensive progress analytics."
        },
        {
            "title": "🎯 Competitor Intelligence",
            "description": "Stay ahead of the competition with detailed analysis of competitor strategies and opportunities."
        },
        {
            "title": "🚀 Technical Excellence",
            "description": "Comprehensive technical SEO analysis covering Core Web Vitals, mobile optimization, and site architecture."
        }
    ]

    for idx, insight in enumerate(insights):
        with insight_cols[idx % 2]:
            st.markdown(f"""
                <div class="premium-card" style="min-height: 160px; cursor: default;">
                    <div class="card-glow"></div>
                    <div class="card-content">
                        <div class="card-title" style="margin-bottom: 0.8rem;">{insight['title']}</div>
                        <div class="card-description" style="margin-bottom: 0;">{insight['description']}</div>
                    </div>
                    <div class="card-shine"></div>
                </div>
            """, unsafe_allow_html=True)
    
    # Close dashboard container
    st.markdown('</div>', unsafe_allow_html=True)

def ai_seo_tools():
    """Render the SEO tools dashboard with premium glassmorphic design."""
    logger.info("Starting SEO Tools Dashboard")
    
    # Apply common dashboard styling
    apply_dashboard_style()

    # Check if a specific tool is selected
    selected_tool = st.query_params.get("tool")
    
    if selected_tool:
        # Map tool paths to their respective functions
        tool_functions = {
            # Individual tools
            "structured_data": ai_structured_data,
            "blog_title": ai_title_generator,
            "meta_description": metadesc_generator_main,
            "alt_text": alt_text_gen,
            "opengraph": og_tag_generator,
            "image_optimizer": main_img_optimizer,
            "pagespeed": google_pagespeed_insights,
            "onpage_seo": analyze_onpage_seo,
            "url_checker": url_seo_checker,
            "backlinking": backlinking_ui,
            
            # Tool combinations
            "content_optimization": lambda: run_tool_combination([
                ai_title_generator,
                metadesc_generator_main,
                ai_structured_data
            ], "Content Optimization Suite"),
            "technical_audit": lambda: run_tool_combination([
                google_pagespeed_insights,
                analyze_onpage_seo,
                url_seo_checker
            ], "Technical SEO Audit"),
            "image_optimization": lambda: run_tool_combination([
                alt_text_gen,
                main_img_optimizer
            ], "Image Optimization Suite"),
            "social_optimization": lambda: run_tool_combination([
                og_tag_generator,
                backlinking_ui
            ], "Social Media Optimization"),
            
            # Add Content Gap Analysis and Content Calendar
            "content_gap_analysis": render_content_gap_analysis,
            "content_calendar": render_content_calendar
        }
        
        if selected_tool in tool_functions:
            # Clear any existing content
            st.empty()
            # Execute the selected tool's function
            tool_functions[selected_tool]()
        else:
            st.error(f"Invalid tool selected: {selected_tool}")
            render_seo_tools_dashboard()
    else:
        # Show the dashboard if no tool is selected
        render_seo_tools_dashboard()

def run_tool_combination(tools, combination_name):
    """Run a combination of tools and provide cross-tool analysis."""
    st.markdown(f"# {combination_name}")
    st.markdown("Running comprehensive analysis...")
    
    # Create tabs for each tool in the combination
    tabs = st.tabs([f"Step {i+1}" for i in range(len(tools))])
    
    # Run each tool in its own tab
    for i, (tab, tool) in enumerate(zip(tabs, tools)):
        with tab:
            st.markdown(f"### Step {i+1}")
            tool()
    
    # Add cross-tool analysis section
    st.markdown("## 📊 Cross-Tool Analysis")
    st.markdown("Analyzing results across all tools...")
    
    # Add recommendations based on combined results
    st.markdown("## 💡 Recommendations")
    st.markdown("Based on the combined analysis, here are the key recommendations:")
    
    # Add a button to export the complete analysis
    if st.button("📥 Export Complete Analysis", use_container_width=True):
        st.info("Analysis export functionality coming soon!")
