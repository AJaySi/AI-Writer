import streamlit as st
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
    """Render a modern dashboard for SEO tools with improved UI and navigation."""
    selected_section = st.session_state.get('seo_dashboard_section', 'combinations')

    # Define card gradients at the top so it's available in all sections
    card_gradients = {
        "Content Optimization Suite": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "Technical SEO Audit": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "Image Optimization Suite": "linear-gradient(135deg, #f7971e 0%, #ffd200 100%)",
        "Social Media Optimization": "linear-gradient(135deg, #f953c6 0%, #b91d73 100%)",
        "Content Gap Analysis": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "Content Calendar": "linear-gradient(135deg, #4CAF50 0%, #2196F3 100%)",
        "Structured Data Generator": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "Blog Title Generator": "linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%)",
        "Meta Description Generator": "linear-gradient(135deg, #f7971e 0%, #ffd200 100%)",
        "Image Alt Text Generator": "linear-gradient(135deg, #f953c6 0%, #b91d73 100%)",
        "OpenGraph Tags Generator": "linear-gradient(135deg, #f857a6 0%, #ff5858 100%)",
        "Image Optimizer": "linear-gradient(135deg, #43cea2 0%, #185a9d 100%)",
        "PageSpeed Insights": "linear-gradient(135deg, #ff9966 0%, #ff5e62 100%)",
        "On-Page SEO Analyzer": "linear-gradient(135deg, #56ab2f 0%, #a8e063 100%)",
        "URL SEO Checker": "linear-gradient(135deg, #3a7bd5 0%, #00d2ff 100%)",
        "AI Backlinking Tool": "linear-gradient(135deg, #e96443 0%, #904e95 100%)"
    }

    # Navigation bar only (no dashboard title/description)
    nav_cols = st.columns([1,1,1,1])
    nav_labels = ["Tool Combos", "Advanced", "Individual", "About"]
    nav_keys = ["combinations", "advanced", "individual", "about"]
    for i, label in enumerate(nav_labels):
        if nav_cols[i].button(label, key=f"nav_{label}"):
            st.session_state['seo_dashboard_section'] = nav_keys[i]
            selected_section = nav_keys[i]

    st.markdown("<hr style='margin:1.5rem 0;'>", unsafe_allow_html=True)

    # Define tool combinations for cross-tool analysis
    tool_combinations = {
        "Content Optimization Suite": {
            "icon": "📊",
            "description": "Comprehensive content optimization combining title generation, meta descriptions, and structured data.",
            "tools": ["Blog Title Generator", "Meta Description Generator", "Structured Data Generator"],
            "path": "content_optimization",
            "color": "#4CAF50"
        },
        "Technical SEO Audit": {
            "icon": "🔧",
            "description": "Complete technical SEO analysis including page speed, on-page SEO, and URL structure.",
            "tools": ["PageSpeed Insights", "On-Page SEO Analyzer", "URL SEO Checker"],
            "path": "technical_audit",
            "color": "#2196F3"
        },
        "Image Optimization Suite": {
            "icon": "🖼️",
            "description": "End-to-end image optimization with alt text generation and performance optimization.",
            "tools": ["Image Alt Text Generator", "Image Optimizer"],
            "path": "image_optimization",
            "color": "#FF9800"
        },
        "Social Media Optimization": {
            "icon": "📱",
            "description": "Enhance social media presence with OpenGraph tags and backlink analysis.",
            "tools": ["OpenGraph Tags Generator", "AI Backlinking Tool"],
            "path": "social_optimization",
            "color": "#9C27B0"
        }
    }

    # Define individual SEO tools
    seo_tools = {
        "Structured Data Generator": {
            "icon": "📋",
            "description": "Generate structured data (Rich Snippets) to enhance your search results with additional information.",
            "color": "#4CAF50",
            "path": "structured_data",
            "status": "active"
        },
        "Blog Title Generator": {
            "icon": "✏️",
            "description": "Create SEO-optimized blog titles that attract clicks and improve search rankings.",
            "color": "#2196F3",
            "path": "blog_title",
            "status": "active"
        },
        "Meta Description Generator": {
            "icon": "📝",
            "description": "Generate compelling meta descriptions that improve click-through rates from search results.",
            "color": "#FF9800",
            "path": "meta_description",
            "status": "active"
        },
        "Image Alt Text Generator": {
            "icon": "🖼️",
            "description": "Create descriptive alt text for images to improve accessibility and image SEO.",
            "color": "#9C27B0",
            "path": "alt_text",
            "status": "active"
        },
        "OpenGraph Tags Generator": {
            "icon": "📱",
            "description": "Generate OpenGraph tags for better social media sharing and visibility.",
            "color": "#F44336",
            "path": "opengraph",
            "status": "active"
        },
        "Image Optimizer": {
            "icon": "📉",
            "description": "Optimize and resize images for better website performance and SEO.",
            "color": "#607D8B",
            "path": "image_optimizer",
            "status": "active"
        },
        "PageSpeed Insights": {
            "icon": "⚡",
            "description": "Analyze your website's performance using Google PageSpeed Insights.",
            "color": "#795548",
            "path": "pagespeed",
            "status": "active"
        },
        "On-Page SEO Analyzer": {
            "icon": "🔍",
            "description": "Analyze and optimize your webpage's SEO elements and content.",
            "color": "#009688",
            "path": "onpage_seo",
            "status": "active"
        },
        "URL SEO Checker": {
            "icon": "🌐",
            "description": "Check the SEO health of specific URLs and get improvement suggestions.",
            "color": "#3F51B5",
            "path": "url_checker",
            "status": "active"
        },
        "AI Backlinking Tool": {
            "icon": "🔗",
            "description": "Discover and analyze backlink opportunities using AI-powered insights.",
            "color": "#E91E63",
            "path": "backlinking",
            "status": "active"
        }
    }

    # --- Tool Combinations Section ---
    if selected_section == 'combinations':
        combo_cols = st.columns(2)
        for idx, (combo_name, details) in enumerate(tool_combinations.items()):
            gradient = card_gradients.get(combo_name, "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)")
            with combo_cols[idx % 2]:
                st.markdown(f"""
                    <div class="seo-card" style="background: {gradient}; position: relative; overflow: hidden;">
                        <div class="seo-card-overlay"></div>
                        <div class="seo-icon">{details['icon']}</div>
                        <div class="seo-title">{combo_name}</div>
                        <div class="seo-description">{details['description']}</div>
                        <div>
                            {''.join([f'<span class="tool-badge">{tool}</span>' for tool in details['tools']])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Launch {combo_name}", key=f"combo_{combo_name}", use_container_width=True):
                    st.query_params["tool"] = details["path"]
                    st.rerun()

    # --- Advanced Features Section ---
    elif selected_section == 'advanced':
        adv_cols = st.columns(2)
        adv_features = [
            {
                "name": "Content Gap Analysis",
                "icon": "🎯",
                "description": "Identify content opportunities and optimize your content strategy with AI-powered insights.",
                "badges": ["Website Analysis", "Competitor Research", "Keyword Opportunities", "AI Recommendations"],
                "gradient": card_gradients["Content Gap Analysis"],
                "button": "Start Content Gap Analysis",
                "key": "content_gap_analysis",
                "path": "content_gap_analysis"
            },
            {
                "name": "Content Calendar",
                "icon": "📅",
                "description": "Plan, schedule, and manage your content strategy with our AI-powered content calendar.",
                "badges": ["Content Planning", "Scheduling", "Performance Tracking", "AI Insights"],
                "gradient": card_gradients["Content Calendar"],
                "button": "Open Content Calendar",
                "key": "content_calendar",
                "path": "content_calendar"
            }
        ]
        for idx, feature in enumerate(adv_features):
            with adv_cols[idx % 2]:
                st.markdown(f"""
                    <div class="seo-card" style="background: {feature['gradient']}; position: relative; overflow: hidden;">
                        <div class="seo-card-overlay"></div>
                        <div class="seo-icon">{feature['icon']}</div>
                        <div class="seo-title">{feature['name']}</div>
                        <div class="seo-description">{feature['description']}</div>
                        <div>
                            {''.join([f'<span class="tool-badge">{badge}</span>' for badge in feature['badges']])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(feature['button'], key=feature['key'], use_container_width=True):
                    st.query_params["tool"] = feature["path"]
                    st.rerun()

    # --- Individual Tools Section ---
    elif selected_section == 'individual':
        cols = st.columns(3)
        for idx, (tool_name, details) in enumerate(seo_tools.items()):
            gradient = card_gradients.get(tool_name, "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)")
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="seo-card" style="background: {gradient}; position: relative; overflow: hidden;">
                        <div class="seo-card-overlay"></div>
                        <div class="seo-icon">{details['icon']}</div>
                        <div class="seo-title">{tool_name}</div>
                        <div class="seo-description">{details['description']}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Use {tool_name}", key=f"btn_{tool_name}", use_container_width=True):
                    st.query_params["tool"] = details["path"]
                    st.rerun()

    # --- About Section ---
    elif selected_section == 'about':
        st.markdown("""
            <div style='text-align: center; margin: 2rem 0;'>
                <h2>About This Dashboard</h2>
                <p style='color: #666;'>This dashboard brings together powerful AI-driven SEO tools and workflows to help you optimize your website and content strategy. Use the navigation above to explore combinations, advanced features, or individual tools.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            .seo-card {
                border-radius: 14px;
                padding: 24px;
                margin-bottom: 24px;
                box-shadow: 0 4px 16px rgba(44, 62, 80, 0.10), 0 1.5px 4px rgba(44,62,80,0.06);
                transition: transform 0.2s cubic-bezier(.4,2,.6,1), box-shadow 0.2s;
                height: 100%;
                border: 1.5px solid #e3e8ee;
                position: relative;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            .seo-card-overlay {
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(255,255,255,0.72);
                z-index: 1;
                pointer-events: none;
                border-radius: 14px;
                box-shadow: 0 2px 8px rgba(44,62,80,0.08);
            }
            .seo-card:hover {
                transform: translateY(-6px) scale(1.025);
                box-shadow: 0 8px 32px rgba(44, 62, 80, 0.18), 0 2px 8px rgba(44,62,80,0.10);
                border-color: #4CAF50;
            }
            .seo-icon {
                font-size: 2.7rem;
                margin-bottom: 18px;
                z-index: 2;
                position: relative;
                text-shadow: 0 2px 8px rgba(44,62,80,0.10);
            }
            .seo-title {
                font-size: 1.25rem;
                font-weight: 800;
                margin-bottom: 12px;
                color: #222b45;
                z-index: 2;
                position: relative;
                text-shadow: 0 2px 8px rgba(44,62,80,0.10);
                letter-spacing: 0.01em;
            }
            .seo-description {
                color: #34495e;
                font-size: 1.08rem;
                margin-bottom: 15px;
                z-index: 2;
                position: relative;
                text-align: center;
                line-height: 1.5;
                text-shadow: 0 1px 4px rgba(44,62,80,0.08);
            }
            .tool-badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 0.9rem;
                margin-right: 8px;
                margin-bottom: 8px;
                background: rgba(255, 255, 255, 0.95);
                color: #2196F3;
                font-weight: 600;
                border: 1px solid #e3e8ee;
            }
        </style>
    """, unsafe_allow_html=True)

def ai_seo_tools():
    """
    A collection of AI-powered SEO tools for content creators, providing various options 
    such as generating structured data, optimizing images, checking page speed, 
    and analyzing on-page SEO.
    """
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
