import time
import os
import json
import requests
import streamlit as st

from streamlit_quill import st_quill
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def generate_facebook_post(business_type, target_audience, post_goal, post_tone, include, avoid):
    """
    Generates a Facebook post prompt for an LLM based on user input.
    """
    prompt = f"""
        I am a {business_type} looking to engage my target audience, {target_audience}, on Facebook.

        My goal for this detailed post is: {post_goal}. The tone should be {post_tone}.

        Here are some additional preferences:
        - **Include:** {include}
        - **Avoid:** {avoid}

        Please write a well-structured Facebook post with:
        1. A **catchy opening** to grab attention.
        2. Detailed **Engaging content** that highlights key benefits or features.
        3. A **strong call-to-action** (CTA) encouraging my audience to take action.
        4. If applicable, suggest **multimedia** (images, videos, etc.).
        5. Include **relevant hashtags** for visibility.

        """
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        st.error(f"An error occurred while generating the prompt: {err}")
        return None


def facebook_post_writer():
    st.title("📱 Alwrity - Facebook Post Generator")
    st.markdown(
        """
        Facebook Post Generator will help you create a compelling Facebook post for your business.
        Please provide the following details to generate your post:
        """
    )

    # Inputs for the Facebook post generator
    col1, col2 = st.columns(2)

    with col1:
        post_goal_options = ["Promote a new product", "Share valuable content", "Increase engagement", "Customize"]
        post_goal = st.selectbox(
            "🎯 **What is the goal of your post?**",
            post_goal_options,
            index=2,
            help="Select the main goal of your post."
        )

        if post_goal == "Customize":
            post_goal = st.text_input(
                "🎯 **Customize your goal:**",
                placeholder="e.g., Announce an event",
                help="Provide a specific goal if you selected 'Customize'."
            )
        target_audience = st.text_input(
            "👥 **Describe your target audience:**",
            placeholder="e.g., Fitness enthusiasts",
            help="Describe the audience you are targeting with this post."
        )
        include = st.text_input(
            "📷 **What elements do you want to include?**",
            placeholder="e.g., Short video with a sneak peek of the challenge",
            help="Specify any elements you want to include in the post (e.g., images, videos, links, hashtags, questions)."
        )

    with col2:
        post_tone_options = ["Informative", "Humorous", "Inspirational", "Upbeat", "Casual", "Customize"]
        post_tone = st.selectbox(
            "🎨 **What tone do you want to use?**",
            post_tone_options,
            index=3,
            help="Choose the tone you want to use for the post."
        )

        if post_tone == "Customize":
            post_tone = st.text_input(
                "🎨 **Customize your tone:**",
                placeholder="e.g., Professional",
                help="Provide a specific tone if you selected 'Customize'."
            )

        business_type = st.text_input(
            "🏢 **What is your business type?**",
            placeholder="e.g., Fitness coach",
            help="Provide the type of your business. This will help tailor the post content."
        )

        avoid = st.text_input(
            "❌ **What elements do you want to avoid?**",
            placeholder="e.g., Long paragraphs",
            help="Specify any elements you want to avoid in the post (e.g., long paragraphs, technical jargon)."
        )

    # Handle the generation button
    if st.button("🚀 Generate Facebook Post"):
        with st.spinner():
            if not business_type or not target_audience:
                st.error("🚫 Please provide the required inputs: Business Type and Target Audience.")
            else:
                generated_post = generate_facebook_post(
                    business_type, target_audience, post_goal, post_tone, include, avoid
                )

                if generated_post:
                    st.markdown(generated_post)
                else:
                    st.error("Error: Failed to generate Facebook Post.")
