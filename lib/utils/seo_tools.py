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


def ai_seo_tools():
    """
    A collection of AI-powered SEO tools for content creators, providing various options 
    such as generating structured data, optimizing images, checking page speed, 
    and analyzing on-page SEO.
    """
    st.markdown(
        """
        Welcome to your one-stop solution for AI-driven SEO optimization. Select a tool from the options below 
        to improve your website’s SEO with cutting-edge AI technology.
        """
    ) 
    # List of SEO tools with unique emojis for each option
    options = [
        "📝 Generate Structured Data - Rich Snippet",
        "✏️ Generate SEO Optimized Blog Titles",
        "📝 Generate Meta Description for SEO",
        "🖼️ Generate Image Alt Text",
        "📄 Generate OpenGraph Tags",
        "📉 Optimize/Resize Image",
        "⚡ Run Google PageSpeed Insights",
        "🔍 Analyze On-Page SEO",
        "🌐 URL SEO Checker",
        "🔗 AI Backlinking Tool"
    ]
    
    # User selection of SEO tools using radio buttons
    choice = st.radio(
        "**👇 Select an AI SEO Tool:**", 
        options, 
        index=0, 
        format_func=lambda x: x
    )
    
    # Call the respective functions based on the user selection
    if choice == "📝 Generate Structured Data - Rich Snippet":
        # Generate Structured Data for Rich Snippets
        ai_structured_data()

    elif choice == "📝 Generate Meta Description for SEO":
        # Generate SEO-optimized meta descriptions
        metadesc_generator_main()

    elif choice == "✏️ Generate SEO Optimized Blog Titles":
        # Generate SEO-friendly blog titles
        ai_title_generator()

    elif choice == "🖼️ Generate Image Alt Text":
        # Generate alternative text for images
        alt_text_gen()

    elif choice == "📄 Generate OpenGraph Tags":
        # Generate OpenGraph tags for social media sharing
        og_tag_generator()

    elif choice == "📉 Optimize/Resize Image":
        # Optimize images by resizing or compressing them
        main_img_optimizer()

    elif choice == "⚡ Run Google PageSpeed Insights":
        # Run Google PageSpeed Insights for performance analysis
        google_pagespeed_insights()

    elif choice == "🔍 Analyze On-Page SEO":
        # Analyze on-page SEO elements
        analyze_onpage_seo()

    elif choice == "🌐 URL SEO Checker":
        # Check SEO health of a specific URL
        url_seo_checker()

    elif choice == "🔗 AI Backlinking Tool":
        # Run AI Backlinking tool for link-building opportunities
        backlinking_ui()
