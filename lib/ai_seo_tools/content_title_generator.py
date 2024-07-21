import time #Iwish
import os
import json
import streamlit as st
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import google.generativeai as genai

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def ai_title_generator():
    """ Use AI to personalize content title generation """
    st.title("✍️ Alwrity - AI Blog Title Generator")

    # Input section
    with st.expander("**PRO-TIP** - Follow the steps below for best results.", expanded=True):
        col1, col2 = st.columns([5, 5])

        with col1:
            input_blog_keywords = st.text_input(
                '**🔑 Enter main keywords of your blog!**',
                placeholder="e.g., AI tools, digital marketing, SEO",
                help="Use 2-3 words that best describe the main topic of your blog."
            )
            input_blog_content = st.text_area(
                '**📄 Copy/Paste your entire blog content.** (Optional)',
                placeholder="e.g., Content about the importance of AI in digital marketing...",
                help="Paste your full blog content here for more accurate title suggestions. This is optional."
            )

        with col2:
            input_title_type = st.selectbox(
                '📝 Blog Type', 
                ('General', 'How-to Guides', 'Tutorials', 'Listicles', 'Newsworthy Posts', 'FAQs', 'Checklists/Cheat Sheets'),
                index=0
            )
            input_title_intent = st.selectbox(
                '🔍 Search Intent', 
                ('Informational Intent', 'Commercial Intent', 'Transactional Intent', 'Navigational Intent'), 
                index=0
            )
            language_options = ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Other"]
            input_language = st.selectbox(
                '🌐 Select Language', 
                options=language_options,
                index=0,
                help="Choose the language for your blog title."
            )
            if input_language == "Other":
                input_language = st.text_input(
                    'Specify Language', 
                    placeholder="e.g., Italian, Dutch",
                    help="Specify your preferred language."
                )

    # Generate Blog Title button
    if st.button('**Generate Blog Titles**'):
        with st.spinner("Generating blog titles..."):
            if input_blog_content == 'Optional':
                input_blog_content = None

            if not input_blog_keywords and not input_blog_content:
                st.error('**🫣 Provide Inputs to generate Blog Titles. Either Blog Keywords OR content is required!**')
            else:
                blog_titles = generate_blog_titles(input_blog_keywords, input_blog_content, input_title_type, input_title_intent, input_language)
                if blog_titles:
                    st.subheader('**👩🧕🔬 Go Rule search ranking with these Blog Titles!**')
                    with st.expander("**Final - Blog Titles Output 🎆🎇🎇**", expanded=True):
                        st.markdown(blog_titles)
                else:
                    st.error("💥 **Failed to generate blog titles. Please try again!**")


# Function to generate blog metadesc
def generate_blog_titles(input_blog_keywords, input_blog_content, input_title_type, input_title_intent, input_language):
    """ Function to call upon LLM to get the work done. """
    # If keywords and content both are given.
    if input_blog_content and input_blog_keywords:
        prompt = f"""As a SEO expert, I will provide you with main 'blog keywords' and 'blog content'.
        Your task is write 5 SEO optimised blog titles, from given blog keywords and content.

        Follow the below guidelines for generating the blog titles:
        1). As SEO expert, follow all best practises for SEO optimised blog titles.
        2). Your response should be optimised around given keywords and content.
        3). Optimise your response for web search intent {input_title_intent}.
        4). Optimise your response for blog type of {input_title_type}.
        5). Your blog titles should in {input_language} language.\n

        blog keywords: '{input_blog_keywords}'\n
        blog content: '{input_blog_content}'
        """
    elif input_blog_keywords and not input_blog_content:
        prompt = f"""As a SEO expert, I will provide you with main 'keywords' of a blog.
        Your task is write 5 SEO optimised blog titles from given blog keywords.

        Follow the below guidelines for generating the blog titles:
        1). As SEO expert, follow all best practises for SEO optimised blog titles.
        2). Your response should be optimised around given keywords and content.
        3). Optimise your response for web search intent {input_title_intent}.
        4). Optimise your response for blog type of {input_title_type}.
        5). Your blog titles should in {input_language} language.\n

        blog keywords: '{input_blog_keywords}'\n
        """
    elif input_blog_content and not input_blog_keywords:
        prompt = f"""As a SEO expert, I will provide you with a 'blog content'.
        Your task is write 5 SEO optimised blog titles from given blog content.

        Follow the below guidelines for generating the blog titles:
        1). As SEO expert, follow all best practises for SEO optimised blog titles.
        2). Your response should be optimised around given keywords and content.
        3). Optimise your response for web search intent {input_title_intent}.
        4). Optimise your response for blog type of {input_title_type}.
        5). Your blog titles should in {input_language} language.\n

        blog content: '{input_blog_content}'\n
        """

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
