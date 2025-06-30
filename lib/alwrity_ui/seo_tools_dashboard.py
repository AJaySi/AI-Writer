import streamlit as st
from loguru import logger
from typing import List, Dict, Any, Callable

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

# Import new enterprise tools
from ..ai_seo_tools.google_search_console_integration import render_gsc_integration
from ..ai_seo_tools.ai_content_strategy import render_ai_content_strategy
from ..ai_seo_tools.enterprise_seo_suite import render_enterprise_seo_suite

from lib.alwrity_ui.dashboard_styles import apply_dashboard_style, render_dashboard_header, render_category_header, render_card


# ============================================================================
# TOOL CONFIGURATION FUNCTIONS
# ============================================================================

def get_enterprise_tools_config() -> List[Dict[str, Any]]:
    """Get configuration for enterprise tools."""
    return [
        {
            'name': '🎯 Enterprise SEO Suite',
            'description': 'Unified command center for comprehensive SEO management with AI-powered workflows',
            'function': render_enterprise_seo_suite,
            'features': ['Complete SEO audit workflows', 'AI-powered recommendations', 'Strategic planning', 'Performance tracking']
        },
        {
            'name': '📊 Google Search Console Intelligence',
            'description': 'AI-powered insights from Google Search Console data with content recommendations',
            'function': render_gsc_integration,
            'features': ['GSC data analysis', 'Content opportunities', 'Performance insights', 'Strategic recommendations']
        },
        {
            'name': '🧠 AI Content Strategy Generator',
            'description': 'Generate comprehensive content strategies using AI market intelligence',
            'function': render_ai_content_strategy,
            'features': ['Content pillar development', 'Topic cluster strategy', 'Content calendar planning', 'Distribution strategy']
        }
    ]

def get_analytics_tools_config() -> List[Dict[str, Any]]:
    """Get configuration for analytics tools."""
    return [
        {
            'name': '📊 Google Search Console Intelligence',
            'description': 'Deep analysis of GSC data with AI-powered content recommendations',
            'function': render_gsc_integration,
            'category': 'Search Analytics'
        },
        {
            'name': '🔍 Enhanced Content Gap Analysis',
            'description': 'Advanced competitor content analysis with AI insights',
            'function': lambda: render_enhanced_content_gap_analysis(),
            'category': 'Competitive Intelligence'
        },
        {
            'name': '📈 SEO Performance Tracker',
            'description': 'Track and analyze SEO performance with trend analysis',
            'function': lambda: st.info("SEO Performance Tracker - Coming soon with advanced metrics"),
            'category': 'Performance Analytics'
        }
    ]

def get_technical_tools_config() -> List[Dict[str, Any]]:
    """Get configuration for technical SEO tools."""
    return [
        {
            'name': '🔍 Technical SEO Crawler',
            'description': 'Comprehensive site-wide technical SEO analysis',
            'function': lambda: render_technical_seo_crawler(),
            'priority': 'High'
        },
        {
            'name': '📱 Mobile SEO Analyzer',
            'description': 'Mobile-specific SEO analysis and optimization',
            'function': lambda: st.info("Mobile SEO Analyzer - Advanced mobile optimization coming soon"),
            'priority': 'Medium'
        },
        {
            'name': '⚡ Core Web Vitals Optimizer',
            'description': 'Analyze and optimize Core Web Vitals performance',
            'function': lambda: st.info("Core Web Vitals Optimizer - Performance optimization coming soon"),
            'priority': 'High'
        },
        {
            'name': '🗺️ XML Sitemap Generator',
            'description': 'Generate and optimize XML sitemaps',
            'function': lambda: st.info("XML Sitemap Generator - Coming soon"),
            'priority': 'Medium'
        }
    ]

def get_content_tools_config() -> List[Dict[str, Any]]:
    """Get configuration for content and strategy tools."""
    return [
        {
            'name': '🧠 AI Content Strategy Generator',
            'description': 'Comprehensive content strategy with AI market intelligence',
            'function': render_ai_content_strategy,
            'type': 'Enterprise'
        },
        {
            'name': '📅 Content Calendar Planner',
            'description': 'AI-powered content calendar with SEO optimization',
            'function': lambda: render_content_calendar(),
            'type': 'Professional'
        },
        {
            'name': '🎯 Topic Cluster Generator',
            'description': 'Generate SEO topic clusters for content dominance',
            'function': lambda: st.info("Topic Cluster Generator - Advanced clustering coming soon"),
            'type': 'Professional'
        },
        {
            'name': '📊 Content Performance Analyzer',
            'description': 'Analyze content performance and optimization opportunities',
            'function': lambda: st.info("Content Performance Analyzer - Coming soon"),
            'type': 'Standard'
        }
    ]

def get_basic_tools_config() -> List[Dict[str, Any]]:
    """Get configuration for basic SEO tools."""
    return [
        {
            'name': '📝 Meta Description Generator',
            'description': 'Generate SEO-optimized meta descriptions',
            'function': lambda: metadesc_generator_main(),
            'category': 'Metadata'
        },
        {
            'name': '🎯 Content Title Generator', 
            'description': 'Create compelling, SEO-friendly titles',
            'function': lambda: ai_title_generator(),
            'category': 'Content'
        },
        {
            'name': '🔗 OpenGraph Generator',
            'description': 'Generate social media OpenGraph tags',
            'function': lambda: og_tag_generator(),
            'category': 'Social'
        },
        {
            'name': '🖼️ Image Alt Text Generator',
            'description': 'Generate SEO-friendly image alt text',
            'function': lambda: alt_text_gen(),
            'category': 'Images'
        },
        {
            'name': '📋 Schema Markup Generator',
            'description': 'Generate structured data markup',
            'function': lambda: ai_structured_data(),
            'category': 'Technical'
        },
        {
            'name': '🔍 On-Page SEO Analyzer',
            'description': 'Comprehensive on-page SEO analysis',
            'function': lambda: analyze_onpage_seo(),
            'category': 'Analysis'
        },
        {
            'name': '🌐 URL SEO Checker',
            'description': 'Quick SEO check for any URL',
            'function': lambda: url_seo_checker(),
            'category': 'Analysis'
        }
    ]

def get_tool_functions_mapping() -> Dict[str, Callable]:
    """Get mapping of tool names to their functions for URL routing."""
    return {
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


# ============================================================================
# INDIVIDUAL TOOL RENDERING FUNCTIONS
# ============================================================================

def render_content_gap_analysis():
    """Render the content gap analysis workflow interface."""
    ui = ContentGapAnalysisUI()
    ui.run()

def render_enhanced_content_gap_analysis_ui():
    """Render the enhanced content gap analysis with advertools integration."""
    render_enhanced_content_gap_analysis()

def render_content_calendar():
    """Render the content calendar dashboard with proper error handling."""
    import logging
    import sys
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('content_calendar.log', mode='a')
        ]
    )
    calendar_logger = logging.getLogger('content_calendar')
    
    try:
        calendar_logger.info("Initializing Content Calendar Dashboard")
        dashboard = ContentCalendarDashboard()
        calendar_logger.info("Rendering Content Calendar Dashboard")
        dashboard.render()
        calendar_logger.info("Content Calendar Dashboard rendered successfully")
    except Exception as e:
        calendar_logger.error(f"Error rendering content calendar: {str(e)}", exc_info=True)
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
            _display_readability_metrics(text_input)
            _display_readability_recommendations()
        else:
            st.error("Please enter text to analyze.")

def _display_readability_metrics(text: str):
    """Display readability metrics for the given text."""
    from textstat import textstat
    
    metrics = {
        "Flesch Reading Ease": textstat.flesch_reading_ease(text),
        "Flesch-Kincaid Grade Level": textstat.flesch_kincaid_grade(text),
        "Gunning Fog Index": textstat.gunning_fog(text),
        "SMOG Index": textstat.smog_index(text),
        "Automated Readability Index": textstat.automated_readability_index(text),
        "Coleman-Liau Index": textstat.coleman_liau_index(text),
        "Linsear Write Formula": textstat.linsear_write_formula(text),
        "Dale-Chall Readability Score": textstat.dale_chall_readability_score(text),
        "Readability Consensus": textstat.readability_consensus(text)
    }
    
    st.subheader("Text Analysis Results")
    for metric, value in metrics.items():
        st.metric(metric, f"{value:.2f}")

def _display_readability_recommendations():
    """Display readability recommendations."""
    st.subheader("Key Takeaways:")
    st.markdown("""
        * **Don't Be Afraid to Simplify!** Often, simpler language makes content more impactful and easier to digest.
        * **Aim for a Reading Level Appropriate for Your Audience:** Consider the education level, background, and familiarity of your readers.
        * **Use Short Sentences:** This makes your content more scannable and easier to read.
        * **Write for Everyone:** Accessibility should always be a priority. When in doubt, aim for clear, concise language!
    """)

def render_wordcloud_generator():
    """Render the word cloud generator."""
    st.title("☁️ Word Cloud Generator")
    st.write("Visualize the most important words in your content")
    
    text_input = st.text_area("Enter your text:", height=200)
    
    if st.button("Generate Word Cloud"):
        if text_input.strip():
            _generate_and_display_wordcloud(text_input)
            _display_text_statistics(text_input)
        else:
            st.error("Please enter text to generate a word cloud.")

def _generate_and_display_wordcloud(text: str):
    """Generate and display word cloud for the given text."""
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    
    # Create and generate a word cloud image
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    # Display the word cloud
    st.subheader("Word Cloud Visualization")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

def _display_text_statistics(text: str):
    """Display basic text statistics."""
    st.subheader("Text Statistics")
    words = text.split()
    unique_words = set(words)
    st.metric("Total Words", len(words))
    st.metric("Unique Words", len(unique_words))


# ============================================================================
# TAB RENDERING FUNCTIONS
# ============================================================================

def render_enterprise_tab():
    """Render the Enterprise Suite tab."""
    st.header("🏢 Enterprise SEO Command Center")
    st.markdown("**Unified SEO management for enterprise-level optimization**")
    
    enterprise_tools = get_enterprise_tools_config()
    
    # Display enterprise tools
    for tool in enterprise_tools:
        _render_enterprise_tool_card(tool)
    
    # Render selected enterprise tool
    _render_selected_enterprise_tool(enterprise_tools)

def _render_enterprise_tool_card(tool: Dict[str, Any]):
    """Render an individual enterprise tool card."""
    with st.expander(f"{tool['name']} - {tool['description']}", expanded=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Key Features:**")
            for feature in tool['features']:
                st.write(f"• {feature}")
        
        with col2:
            if st.button(f"Launch {tool['name'].split()[1]}", key=f"enterprise_{tool['name']}", use_container_width=True):
                st.session_state.selected_enterprise_tool = tool['name']
                tool['function']()

def _render_selected_enterprise_tool(enterprise_tools: List[Dict[str, Any]]):
    """Render the selected enterprise tool if any."""
    if 'selected_enterprise_tool' in st.session_state:
        selected_tool = next((tool for tool in enterprise_tools if tool['name'] == st.session_state.selected_enterprise_tool), None)
        if selected_tool:
            st.markdown("---")
            selected_tool['function']()

def render_analytics_tab():
    """Render the Analytics & Intelligence tab."""
    st.header("📊 Analytics & Intelligence")
    st.markdown("**Advanced analytics and competitive intelligence tools**")
    
    analytics_tools = get_analytics_tools_config()
    
    # Group tools by category
    categories = _group_tools_by_category(analytics_tools)
    
    for category, tools in categories.items():
        st.subheader(f"📊 {category}")
        
        for tool in tools:
            _render_analytics_tool_row(tool)

def _group_tools_by_category(tools: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group tools by their category."""
    categories = {}
    for tool in tools:
        category = tool['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(tool)
    return categories

def _render_analytics_tool_row(tool: Dict[str, Any]):
    """Render an analytics tool row."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**{tool['name']}**")
        st.write(tool['description'])
    
    with col2:
        if st.button("Launch", key=f"analytics_{tool['name']}", use_container_width=True):
            tool['function']()

def render_technical_tab():
    """Render the Technical SEO tab."""
    st.header("🔧 Technical SEO")
    st.markdown("**Advanced technical SEO analysis and optimization tools**")
    
    technical_tools = get_technical_tools_config()
    
    # Display technical tools with priority indicators
    for tool in technical_tools:
        _render_technical_tool_row(tool)

def _render_technical_tool_row(tool: Dict[str, Any]):
    """Render a technical tool row with priority indicator."""
    priority_color = "🔴" if tool['priority'] == 'High' else "🟡"
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**{tool['name']}** {priority_color}")
        st.write(tool['description'])
    
    with col2:
        st.write(f"**Priority:** {tool['priority']}")
    
    with col3:
        if st.button("Launch", key=f"technical_{tool['name']}", use_container_width=True):
            tool['function']()

def render_content_tab():
    """Render the Content & Strategy tab."""
    st.header("📝 Content & Strategy")
    st.markdown("**AI-powered content creation and strategy tools**")
    
    content_tools = get_content_tools_config()
    
    # Group by tool type
    tool_types = _group_tools_by_type(content_tools)
    
    for tool_type, tools in tool_types.items():
        _render_content_tool_section(tool_type, tools)

def _group_tools_by_type(tools: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group tools by their type."""
    tool_types = {}
    for tool in tools:
        tool_type = tool['type']
        if tool_type not in tool_types:
            tool_types[tool_type] = []
        tool_types[tool_type].append(tool)
    return tool_types

def _render_content_tool_section(tool_type: str, tools: List[Dict[str, Any]]):
    """Render a content tool section."""
    type_color = {"Enterprise": "🏢", "Professional": "💼", "Standard": "📋"}
    st.subheader(f"{type_color.get(tool_type, '📋')} {tool_type} Tools")
    
    for tool in tools:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{tool['name']}**")
            st.write(tool['description'])
        
        with col2:
            if st.button("Launch", key=f"content_{tool['name']}", use_container_width=True):
                tool['function']()

def render_basic_tools_tab():
    """Render the Basic Tools tab."""
    st.header("🎯 Basic SEO Tools")
    st.markdown("**Essential SEO tools for quick optimization tasks**")
    
    basic_tools = get_basic_tools_config()
    
    # Group basic tools by category
    basic_categories = _group_tools_by_category(basic_tools)
    
    # Display in columns for better layout
    _render_basic_tools_in_columns(basic_categories)

def _render_basic_tools_in_columns(basic_categories: Dict[str, List[Dict[str, Any]]]):
    """Render basic tools in two columns."""
    col1, col2 = st.columns(2)
    
    categories_list = list(basic_categories.items())
    mid_point = len(categories_list) // 2
    
    with col1:
        for category, tools in categories_list[:mid_point]:
            _render_basic_tool_category(category, tools)
    
    with col2:
        for category, tools in categories_list[mid_point:]:
            _render_basic_tool_category(category, tools)

def _render_basic_tool_category(category: str, tools: List[Dict[str, Any]]):
    """Render a basic tool category."""
    st.subheader(f"📂 {category}")
    for tool in tools:
        if st.button(f"{tool['name']}", key=f"basic_{tool['name']}", use_container_width=True):
            tool['function']()
        st.caption(tool['description'])
        st.markdown("---")

def render_enterprise_features_footer():
    """Render the enterprise features footer."""
    st.markdown("---")
    st.markdown("### 🚀 Enterprise SEO Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **🏢 Enterprise Suite**
        - Unified SEO workflows
        - AI-powered insights
        - Strategic planning
        - Performance tracking
        """)
    
    with col2:
        st.info("""
        **📊 Advanced Analytics**
        - GSC integration
        - Competitive intelligence
        - Content gap analysis
        - Performance insights
        """)
    
    with col3:
        st.info("""
        **🧠 AI Strategy**
        - Content strategy generation
        - Topic cluster planning
        - Distribution optimization
        - Market intelligence
        """)


# ============================================================================
# MAIN DASHBOARD FUNCTIONS
# ============================================================================

def render_seo_tools_dashboard():
    """Render comprehensive SEO tools dashboard with enterprise features."""
    st.title("🚀 Alwrity AI SEO Tools")
    st.markdown("**Enterprise-level SEO tools powered by artificial intelligence**")
    
    # Create tabs for different tool categories
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏢 Enterprise Suite",
        "📊 Analytics & Intelligence", 
        "🔧 Technical SEO",
        "📝 Content & Strategy",
        "🎯 Basic Tools"
    ])
    
    with tab1:
        render_enterprise_tab()
    
    with tab2:
        render_analytics_tab()
    
    with tab3:
        render_technical_tab()
    
    with tab4:
        render_content_tab()
    
    with tab5:
        render_basic_tools_tab()
    
    # Add footer with enterprise features highlight
    render_enterprise_features_footer()

def ai_seo_tools():
    """Main entry point for SEO tools dashboard with premium glassmorphic design."""
    logger.info("Starting SEO Tools Dashboard")
    
    # Apply common dashboard styling
    apply_dashboard_style()

    # Check if a specific tool is selected
    selected_tool = st.query_params.get("tool")
    
    if selected_tool:
        _handle_selected_tool(selected_tool)
    else:
        # Show the dashboard if no tool is selected
        render_seo_tools_dashboard()

def _handle_selected_tool(selected_tool: str):
    """Handle rendering of a specific selected tool."""
    tool_functions = get_tool_functions_mapping()
    
    if selected_tool in tool_functions:
        # Clear any existing content
        st.empty()
        # Execute the selected tool's function
        tool_functions[selected_tool]()
    else:
        st.error(f"Tool '{selected_tool}' is not available or under development.")
        st.info("Please select a different tool from the dashboard.")
        render_seo_tools_dashboard()

def run_tool_combination(tools: List[Callable], combination_name: str):
    """Run a combination of tools and provide cross-tool analysis."""
    st.markdown(f"# {combination_name}")
    st.markdown("Comprehensive SEO analysis workflow")
    
    # Create tabs for each tool in the combination
    tab_names = _generate_tab_names(tools)
    tabs = st.tabs(tab_names)
    
    # Run each tool in its own tab
    _execute_tools_in_tabs(tabs, tools)
    
    # Add cross-tool analysis section
    _render_analysis_summary()

def _generate_tab_names(tools: List[Callable]) -> List[str]:
    """Generate tab names for tool combination."""
    tab_names = []
    for i, tool in enumerate(tools):
        if hasattr(tool, '__name__'):
            tab_names.append(tool.__name__.replace('_', ' ').title())
        else:
            tab_names.append(f"Step {i+1}")
    return tab_names

def _execute_tools_in_tabs(tabs: List, tools: List[Callable]):
    """Execute tools in their respective tabs."""
    for tab, tool in zip(tabs, tools):
        with tab:
            try:
                tool()
            except Exception as e:
                st.error(f"Error running tool: {str(e)}")
                logger.error(f"Error in tool combination: {str(e)}")

def _render_analysis_summary():
    """Render the analysis summary section."""
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
