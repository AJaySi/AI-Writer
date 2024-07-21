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


def metadesc_generator_main():

    # Title and description
    st.title("✍️ Alwrity - AI Blog Meta Description Generator")
    
    # Input section
    with st.expander("**PRO-TIP** - Read the instructions below. 🚀", expanded=True):
        col1, col2, space = st.columns([5, 5, 0.5])
        with col1:
            keywords = st.text_input("🔑 Target Keywords (comma-separated):",
                                     placeholder="e.g., content marketing, SEO, social media, online business",
                                     help="Enter your target keywords, separated by commas. 📝")
            
            tone_options = ["Informative", "Engaging", "Humorous", "Intriguing", "Playful"]
            tone = st.selectbox("🎨 Desired Tone (optional):",
                                options=["General"] + tone_options,
                                help="Choose the overall tone you want for your meta description. 🎭")
        with col2:
            search_type = st.selectbox('🔍 Search Intent:', 
                                       ('Informational Intent', 'Commercial Intent', 'Transactional Intent', 'Navigational Intent'), 
                                       index=0)
            
            language_options = ["English", "Spanish", "French", "German", "Other"]
            language_choice = st.selectbox("🌐 Preferred Language:", 
                                           options=language_options,
                                           help="Select the language for your meta description. 🗣️")
            if language_choice == "Other":
                language = st.text_input("Specify Other Language:",
                                         placeholder="e.g., Italian, Chinese",
                                         help="Enter your preferred language. 🌍")
            else:
                language = language_choice

    # Generate Blog Title button
    if st.button('**✨ Generate Meta Description ✨**'):
        with st.spinner("Crafting your Meta descriptions... ⏳"):

            # Validate input fields
            if not keywords:
                st.error('**🫣 Blog Keywords are required!**')
            else:
                blog_metadesc = generate_blog_metadesc(keywords, tone, search_type, language)
                if blog_metadesc:
                    st.subheader('**🎉 Your SEO-Boosting Blog Meta Descriptions! 🚀**')
                    with st.expander("**Final - Blog Meta Description Output 🎆🎇**", expanded=True):
                        st.markdown(blog_metadesc)
                else:
                    st.error("💥 **Failed to generate blog meta description. Please try again!**")


# Function to generate blog metadesc
def generate_blog_metadesc(keywords, tone, search_type, language):
    """ Function to call upon LLM to get the work done. """
    prompt = f"""
        Craft 3 engaging and SEO-friendly meta descriptions for a blog post based on the following details:

        Blog Post Keywords: {keywords}
        Search Intent Type: {search_type}
        Desired Tone: {tone}
        Preferred Language: {language}

        Output Format:

        Respond with 3 compelling and concise meta descriptions, approximately 155-160 characters long, that incorporate the target keywords, reflect the blog post content, resonate with the target audience, and entice users to click through to read the full article.
    """
    with st.spinner("Calling Gemini to craft 3 Meta descriptions for you... 💫"):
        try:    
            response = llm_text_gen(prompt)
            return response
        except Exception as err:
            st.error(f"Exit: Failed to get response from LLM: {err}")
