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

def ai_seo_tools():
    """ Collection SEO tools for content creators. """
    options = [
        "Generate Structured Data - Rich Snippet",
        "Generate SEO optimized Blog Titles",
        "Generate Meta Description for SEO",
        "Generate Image Alt Text",
        "Generate OpenGraph Tags",
        "Optimize/Resize Image",
        "Run Google PageSpeed Insights",
        "Analyze On Page SEO",
        "URL SEO Checker"
    ]
    
    # Using st.radio instead of st.selectbox
    choice = st.radio("**👇 Select AI SEO Tool:**", options, index=0, format_func=lambda x: f"📝 {x}")
    
    # Handle choices based on the selected option
    if choice == "Generate Structured Data - Rich Snippet":
        ai_structured_data()
    elif choice == "Generate Meta Description for SEO":
        metadesc_generator_main()
    elif choice == "Generate SEO optimized Blog Titles":
        ai_title_generator()
    elif choice == "Generate Image Alt Text":
        alt_text_gen()
    elif choice == "Generate OpenGraph Tags":
        og_tag_generator()
    elif choice == "Optimize/Resize Image":
        main_img_optimizer()
    elif choice == "Run Google PageSpeed Insights":
        google_pagespeed_insights()
    elif choice == "Analyze On Page SEO":
        analyze_onpage_seo()
    elif choice == "URL SEO Checker":
        url_seo_checker()
