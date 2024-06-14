import time #Iwish
import os
import json
import requests
import streamlit as st


def generate_facebook_post(business_type, target_audience, post_goal, post_tone, include, avoid):
    """
    Generates a Facebook post prompt for an LLM based on user input.

    Args:
        business_type: The type of business, e.g., fashion retailer, fitness coach.
        target_audience: A description of the target audience.
        post_goal: The goal of the Facebook post.
        post_tone: The desired tone of the post.
        include: Elements to include in the post (e.g., images, videos, links).
        avoid: Elements to avoid in the post (e.g., long paragraphs, technical jargon).

    Returns:
        A string containing the LLM prompt.
    """
    prompt = f"""I am a {business_type}.

    Please help me write a detailed Facebook post that will engage my target audience, {target_audience}.

    Here are some additional details to consider:

    * **Post Goal:** {post_goal}
    * **Post Tone:** {post_tone}
    * **Include:** {include}
    * **Avoid:** {avoid}

    **Example Post Structure:**

    1. **Attention-Grabbing Opening:** Start with a question or a bold statement to capture attention.
    2. **Engaging Content:** Briefly describe the main message or offer, highlighting key benefits or features.
    3. **Call-to-Action (CTA):** Encourage the audience to take a specific action (e.g., visit a link, comment, share).
    4. **Multimedia:** Mention the types of multimedia elements to include (e.g., images, videos).
    5. **Hashtags:** Include relevant hashtags to increase post visibility.

    """
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"An error occurred while generating the prompt: {e}")
        return None


def facebook_post_writer():
    st.title("📱 Alwrity - Facebook Post Generator")
    st.markdown(
        """
        Facebook Post Generator will help you create a compelling Facebook post for your business.
        Please provide the following details to generate your post:
        """
    )

    try:
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
            business_type = st.text_input(
                "🏢 **What is your business type?**",
                placeholder="e.g., Fitness coach",
                help="Provide the type of your business. This will help tailor the post content."
            )

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

            avoid = st.text_input(
                "❌ **What elements do you want to avoid?**",
                placeholder="e.g., Long paragraphs",
                help="Specify any elements you want to avoid in the post (e.g., long paragraphs, technical jargon)."
            )

        if st.button("🚀 Generate Facebook Post"):
            if not business_type or not target_audience:
                st.error("🚫 Please provide the required inputs: Business Type and Target Audience.")
            else:
                generated_post = generate_facebook_post(
                    business_type, target_audience, post_goal, post_tone, include, avoid
                )
                if generated_post:
                    st.subheader("**🧕 Verify: Alwrity can make mistakes.**")
                    st.write("## 📄 Generated Facebook Post:")
                    st.write(generated_post)
                    st.markdown("---")
                else:
                    st.error("Error: Failed to generate Facebook Post.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
