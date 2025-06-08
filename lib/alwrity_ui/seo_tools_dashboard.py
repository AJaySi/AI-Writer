import streamlit as st
from loguru import logger

# Import existing tools
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
from lib.ai_seo_tools.content_gap_analysis.enhanced_ui import render_enhanced_content_gap_analysis
from lib.ai_seo_tools.content_calendar.ui.dashboard import ContentCalendarDashboard
from lib.ai_seo_tools.technical_seo_crawler import render_technical_seo_crawler

# Import additional tools
from lib.ai_seo_tools.twitter_tags_generator import display_app as twitter_tags_app
from lib.ai_seo_tools.sitemap_analysis import main as sitemap_analyzer
from lib.ai_seo_tools.textstaty import analyze_text as readability_analyzer
from lib.ai_seo_tools.wordcloud import generate_wordcloud

from lib.alwrity_ui.dashboard_styles import apply_dashboard_style, render_dashboard_header, render_category_header, render_card

def render_content_gap_analysis():
    """Render the content gap analysis workflow interface."""
    from lib.ai_seo_tools.content_gap_analysis.ui import ContentGapAnalysisUI
    
    # Initialize and run the Content Gap Analysis UI
    ui = ContentGapAnalysisUI()
    ui.run()

def render_enhanced_content_gap_analysis_ui():
    """Render the enhanced content gap analysis with advertools integration."""
    render_enhanced_content_gap_analysis()

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

def render_twitter_tags():
    """Render the Twitter tags generator."""
    twitter_tags_app()

def render_readability_analyzer():
    """Render the text readability analyzer."""
    st.title("📖 Text Readability Analyzer")
    st.write("Making Your Content Easy to Read")
    
    text_input = st.text_area("Paste your text here:", height=200)
    
    if st.button("Analyze Readability"):
        if text_input.strip():
            from textstat import textstat
            
            # Calculate various metrics
            metrics = {
                "Flesch Reading Ease": textstat.flesch_reading_ease(text_input),
                "Flesch-Kincaid Grade Level": textstat.flesch_kincaid_grade(text_input),
                "Gunning Fog Index": textstat.gunning_fog(text_input),
                "SMOG Index": textstat.smog_index(text_input),
                "Automated Readability Index": textstat.automated_readability_index(text_input),
                "Coleman-Liau Index": textstat.coleman_liau_index(text_input),
                "Linsear Write Formula": textstat.linsear_write_formula(text_input),
                "Dale-Chall Readability Score": textstat.dale_chall_readability_score(text_input),
                "Readability Consensus": textstat.readability_consensus(text_input)
            }
            
            # Display metrics
            st.subheader("Text Analysis Results")
            for metric, value in metrics.items():
                st.metric(metric, f"{value:.2f}")
            
            # Add recommendations
            st.subheader("Key Takeaways:")
            st.markdown("""
                * **Don't Be Afraid to Simplify!** Often, simpler language makes content more impactful and easier to digest.
                * **Aim for a Reading Level Appropriate for Your Audience:** Consider the education level, background, and familiarity of your readers.
                * **Use Short Sentences:** This makes your content more scannable and easier to read.
                * **Write for Everyone:** Accessibility should always be a priority. When in doubt, aim for clear, concise language!
            """)
        else:
            st.error("Please enter text to analyze.")

def render_wordcloud_generator():
    """Render the word cloud generator."""
    st.title("☁️ Word Cloud Generator")
    st.write("Visualize the most important words in your content")
    
    text_input = st.text_area("Enter your text:", height=200)
    
    if st.button("Generate Word Cloud"):
        if text_input.strip():
            from wordcloud import WordCloud
            import matplotlib.pyplot as plt
            
            # Create and generate a word cloud image
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_input)
            
            # Display the word cloud
            st.subheader("Word Cloud Visualization")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
            
            # Add some statistics
            st.subheader("Text Statistics")
            words = text_input.split()
            unique_words = set(words)
            st.metric("Total Words", len(words))
            st.metric("Unique Words", len(unique_words))
        else:
            st.error("Please enter text to generate a word cloud.")

def render_seo_tools_dashboard():
    """Render a modern dashboard for SEO tools with premium glassmorphic design."""
    
    # Apply common dashboard styling
    apply_dashboard_style()

    # Enhanced dashboard header with modern design
    render_dashboard_header(
        "🚀 SEO AI Power Suite",
        "Dominate search rankings with our comprehensive AI-powered SEO toolkit. From keyword research to content optimization, master every aspect of search engine optimization."
    )

    # Define SEO tools organized by real use cases and existing functionality
    seo_tools = {
        "Content Creation & Optimization": {
            "Content Title Generator": {
                "icon": "📝",
                "description": "Create attention-grabbing, SEO-optimized titles that resonate with your audience",
                "category": "Content",
                "path": "blog_title",
                "features": ["Keyword Optimization", "Title Variations", "CTR Enhancement", "SEO Best Practices"]
            },
            "Meta Description Generator": {
                "icon": "🏷️",
                "description": "Generate compelling meta descriptions that boost click-through rates from search results",
                "category": "Meta Tags",
                "path": "meta_description",
                "features": ["SERP Optimization", "Character Limits", "Keyword Integration", "CTR Improvement"]
            },
            "Structured Data Generator": {
                "icon": "🏗️",
                "description": "Create schema markup to enhance search result appearance with rich snippets",
                "category": "Technical",
                "path": "structured_data",
                "features": ["Rich Snippets", "Schema Markup", "Search Enhancement", "SERP Features"]
            }
        },
        "Image & Media Optimization": {
            "Image Alt Text Generator": {
                "icon": "🖼️",
                "description": "Generate SEO-friendly alt text for images to improve accessibility and search visibility",
                "category": "Images",
                "path": "alt_text",
                "features": ["Accessibility", "Image SEO", "Screen Reader Support", "Search Discovery"]
            },
            "Image Optimizer": {
                "icon": "🎯",
                "description": "Optimize images for web performance and faster loading times",
                "category": "Performance",
                "path": "image_optimizer",
                "features": ["File Compression", "Format Optimization", "Performance Boost", "Web Standards"]
            }
        },
        "Social Media Optimization": {
            "OpenGraph Generator": {
                "icon": "📱",
                "description": "Create OpenGraph tags for beautiful social media sharing experiences",
                "category": "Social",
                "path": "opengraph",
                "features": ["Social Sharing", "Visual Appeal", "Engagement Boost", "Platform Optimization"]
            },
            "Twitter Tags Generator": {
                "icon": "🐦",
                "description": "Generate trending and relevant Twitter hashtags for maximum engagement",
                "category": "Social",
                "path": "twitter_tags",
                "features": ["Hashtag Research", "Trend Analysis", "Engagement Boost", "Content Discovery"]
            }
        },
        "Technical SEO Analysis": {
            "Technical SEO Crawler": {
                "icon": "🔧",
                "description": "Comprehensive site-wide technical SEO analysis with AI-powered recommendations. Identify and fix technical issues that impact your search rankings.",
                "category": "Technical",
                "path": "technical_seo_crawler",
                "features": ["Site-wide Crawling", "Technical Issues Detection", "Performance Analysis", "AI Recommendations"]
            },
            "On-Page SEO Analyzer": {
                "icon": "🔍",
                "description": "Comprehensive analysis of on-page SEO factors with actionable recommendations",
                "category": "Analysis",
                "path": "onpage_seo",
                "features": ["Content Analysis", "SEO Scoring", "Recommendations", "Best Practices"]
            },
            "Website Speed Insights": {
                "icon": "⚡",
                "description": "Analyze website performance using Google PageSpeed Insights",
                "category": "Performance",
                "path": "pagespeed",
                "features": ["Core Web Vitals", "Performance Metrics", "Optimization Tips", "Mobile Analysis"]
            },
            "URL SEO Checker": {
                "icon": "🌐",
                "description": "Analyze URL structure and SEO factors for better search rankings",
                "category": "Technical",
                "path": "url_checker",
                "features": ["URL Analysis", "SEO Factors", "Technical Issues", "Optimization Tips"]
            },
            "Sitemap Analyzer": {
                "icon": "🗺️",
                "description": "Analyze website sitemaps to understand content structure and publishing trends",
                "category": "Technical",
                "path": "sitemap_analysis",
                "features": ["Content Structure", "Publishing Trends", "URL Analysis", "Site Architecture"]
            }
        },
        "Content Analysis & Research": {
            "Content Gap Analysis": {
                "icon": "📊",
                "description": "Identify content opportunities and gaps in your SEO strategy",
                "category": "Research",
                "path": "content_gap_analysis",
                "features": ["Competitor Analysis", "Keyword Gaps", "Content Opportunities", "Strategic Insights"]
            },
            "Enhanced Content Gap Analysis": {
                "icon": "🎯",
                "description": "Advanced content gap analysis with SERP intelligence, competitor crawling, and AI insights using advertools",
                "category": "Research",
                "path": "enhanced_content_gap_analysis",
                "features": ["SERP Analysis", "Competitor Intelligence", "Keyword Expansion", "AI Strategic Insights"]
            },
            "Text Readability Analyzer": {
                "icon": "📖",
                "description": "Analyze text readability and get suggestions for content improvement",
                "category": "Content",
                "path": "readability_analyzer",
                "features": ["Reading Level", "Clarity Score", "Improvement Tips", "Audience Targeting"]
            },
            "Word Cloud Generator": {
                "icon": "☁️",
                "description": "Visualize the most important words and terms in your content",
                "category": "Visualization",
                "path": "wordcloud_generator",
                "features": ["Content Visualization", "Keyword Analysis", "Theme Identification", "Text Statistics"]
            }
        },
        "Strategy & Planning": {
            "Content Calendar": {
                "icon": "📅",
                "description": "Plan and organize your content strategy with AI-powered scheduling",
                "category": "Planning",
                "path": "content_calendar",
                "features": ["Content Planning", "Publishing Schedule", "Strategy Management", "Team Collaboration"]
            },
            "Backlink Analysis": {
                "icon": "🔗",
                "description": "Analyze backlink opportunities and develop link building strategies",
                "category": "Link Building",
                "path": "backlinking",
                "features": ["Link Analysis", "Opportunity Discovery", "Authority Building", "Outreach Planning"]
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
                <h1 style="font-size: 2.2em;">🎯 Why Choose Our SEO Tools?</h1>
                <p>Real tools, real results. Each tool is designed to solve specific SEO challenges and drive measurable improvements.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # SEO insights grid
    insight_cols = st.columns(2)
    insights = [
        {
            "title": "🤖 AI-Powered Analysis",
            "description": "Advanced algorithms analyze your content and provide data-driven optimization recommendations for better rankings."
        },
        {
            "title": "📈 Actionable Insights",
            "description": "Get specific, implementable suggestions that directly impact your search engine visibility and traffic."
        },
        {
            "title": "🎯 Comprehensive Coverage",
            "description": "From technical SEO to content optimization, our tools cover every aspect of search engine optimization."
        },
        {
            "title": "🚀 Proven Results",
            "description": "Based on industry best practices and proven SEO strategies that deliver measurable improvements."
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
        # Map tool paths to their respective functions - ONLY existing, working tools
        tool_functions = {
            # Core content tools
            "structured_data": ai_structured_data,
            "blog_title": ai_title_generator,
            "meta_description": metadesc_generator_main,
            "alt_text": alt_text_gen,
            "opengraph": og_tag_generator,
            "image_optimizer": main_img_optimizer,
            
            # Technical analysis tools
            "technical_seo_crawler": render_technical_seo_crawler,
            "pagespeed": google_pagespeed_insights,
            "onpage_seo": analyze_onpage_seo,
            "url_checker": url_seo_checker,
            "sitemap_analysis": sitemap_analyzer,
            
            # Social media tools
            "twitter_tags": render_twitter_tags,
            
            # Content analysis tools
            "readability_analyzer": render_readability_analyzer,
            "wordcloud_generator": render_wordcloud_generator,
            
            # Advanced tools
            "backlinking": backlinking_ui,
            "content_gap_analysis": render_content_gap_analysis,
            "enhanced_content_gap_analysis": render_enhanced_content_gap_analysis_ui,
            "content_calendar": render_content_calendar,
            
            # Tool combinations for workflow efficiency
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
                render_twitter_tags
            ], "Social Media Optimization")
        }
        
        if selected_tool in tool_functions:
            # Clear any existing content
            st.empty()
            # Execute the selected tool's function
            tool_functions[selected_tool]()
        else:
            st.error(f"Tool '{selected_tool}' is not available or under development.")
            st.info("Please select a different tool from the dashboard.")
            render_seo_tools_dashboard()
    else:
        # Show the dashboard if no tool is selected
        render_seo_tools_dashboard()

def run_tool_combination(tools, combination_name):
    """Run a combination of tools and provide cross-tool analysis."""
    st.markdown(f"# {combination_name}")
    st.markdown("Comprehensive SEO analysis workflow")
    
    # Create tabs for each tool in the combination
    tab_names = []
    for i, tool in enumerate(tools):
        if hasattr(tool, '__name__'):
            tab_names.append(tool.__name__.replace('_', ' ').title())
        else:
            tab_names.append(f"Step {i+1}")
    
    tabs = st.tabs(tab_names)
    
    # Run each tool in its own tab
    for tab, tool in zip(tabs, tools):
        with tab:
            try:
                tool()
            except Exception as e:
                st.error(f"Error running tool: {str(e)}")
                logger.error(f"Error in tool combination: {str(e)}")
    
    # Add cross-tool analysis section
    with st.expander("📊 Analysis Summary", expanded=True):
        st.markdown("""
        ### Key Recommendations:
        1. **Content Optimization**: Ensure your titles and meta descriptions are keyword-optimized
        2. **Technical Performance**: Address any speed or technical issues identified
        3. **Structured Data**: Implement schema markup for better search visibility
        4. **Social Optimization**: Optimize social sharing tags for better engagement
        
        ### Next Steps:
        - Implement the recommendations from each tool
        - Monitor your rankings and traffic after changes
        - Regularly audit your content using these tools
        """)
    
    # Add export functionality placeholder
    if st.button("📥 Export Analysis Report", use_container_width=True):
        st.info("Export functionality is being developed. Save your results manually for now.")
