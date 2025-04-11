import os
import json
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_random_exponential
from loguru import logger
import sys

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def metadesc_generator_main():
    """
    Streamlit app for generating SEO-optimized blog meta descriptions.
    """
    st.title("✍️ Alwrity - AI Blog Meta Description Generator")
    st.markdown(
        "Create compelling, SEO-optimized meta descriptions in just a few clicks. Perfect for enhancing your blog's click-through rates!"
    )

    # Input section
    with st.expander("**PRO-TIP** - Read the instructions below. 🚀", expanded=True):
        col1, col2, _ = st.columns([5, 5, 0.5])

        # Column 1: Keywords and Tone
        with col1:
            keywords = st.text_input(
                "🔑 Target Keywords (comma-separated):",
                placeholder="e.g., content marketing, SEO, social media, online business",
                help="Enter your target keywords, separated by commas. 📝",
            )

            tone_options = ["General", "Informative", "Engaging", "Humorous", "Intriguing", "Playful"]
            tone = st.selectbox(
                "🎨 Desired Tone (optional):",
                options=tone_options,
                help="Choose the overall tone you want for your meta description. 🎭",
            )

        # Column 2: Search Intent and Language
        with col2:
            search_type = st.selectbox(
                "🔍 Search Intent:",
                ("Informational Intent", "Commercial Intent", "Transactional Intent", "Navigational Intent"),
                index=0,
            )

            language_options = ["English", "Spanish", "French", "German", "Other"]
            language_choice = st.selectbox(
                "🌐 Preferred Language:",
                options=language_options,
                help="Select the language for your meta description. 🗣️",
            )

            language = (
                st.text_input(
                    "Specify Other Language:",
                    placeholder="e.g., Italian, Chinese",
                    help="Enter your preferred language. 🌍",
                )
                if language_choice == "Other"
                else language_choice
            )

    # Generate Meta Description button
    if st.button("**✨ Generate Meta Description ✨**"):
        if not keywords.strip():
            st.error("**🫣 Target Keywords are required! Please provide at least one keyword.**")
            return

        with st.spinner("Crafting your Meta descriptions... ⏳"):
            blog_metadesc = generate_blog_metadesc(keywords, tone, search_type, language)
            if blog_metadesc:
                st.success("**🎉 Meta Descriptions Generated Successfully! 🚀**")
                with st.expander("**Your SEO-Boosting Blog Meta Descriptions 🎆🎇**", expanded=True):
                    st.markdown(blog_metadesc)
            else:
                st.error("💥 **Failed to generate blog meta description. Please try again!**")


def generate_blog_metadesc(keywords, tone, search_type, language):
    """
    Generate blog meta descriptions using LLM.

    Args:
        keywords (str): Comma-separated target keywords.
        tone (str): Desired tone for the meta description.
        search_type (str): Search intent type.
        language (str): Preferred language for the description.

    Returns:
        str: Generated meta descriptions or error message.
    """
    prompt = f"""
        Craft 3 engaging and SEO-friendly meta descriptions for a blog post based on the following details:

        Blog Post Keywords: {keywords}
        Search Intent Type: {search_type}
        Desired Tone: {tone}
        Preferred Language: {language}

        Output Format:

        Respond with 3 compelling and concise meta descriptions, approximately 155-160 characters long, that incorporate the target keywords, reflect the blog post content, resonate with the target audience, and entice users to click through to read the full article.
    """
    try:
        return llm_text_gen(prompt)
    except Exception as err:
        logger.error(f"Error generating meta description: {err}")
        st.error(f"💥 Error: Failed to generate response from LLM: {err}")
        return None
