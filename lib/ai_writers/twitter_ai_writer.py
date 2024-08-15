import time #Iwish
import os
import json
import requests
import streamlit as st

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def tweet_writer():
    """ AI Tweet Generator """
    with st.expander("**PRO-TIP** - Read the instructions below.", expanded=True):
        col1, col2 = st.columns([5, 5])
        with col1:
            hook = st.text_input(
                    label="What's the tweet about:(Hook)",
                    placeholder="e.g., Discover the future of tech today!",
                    help="Provide a compelling opening statement or question to grab attention."
            )

        with col2:
            # Collect user inputs with placeholders and help text
            target_audience = st.text_input(
                label="Target Audience",
                placeholder="e.g., technology enthusiasts, travel lovers",
                help="Describe the audience you want to target with this tweet."
            )

    if st.button('**Write Tweets**'):
        if not target_audience or not hook:
            st.error("🚫 Please provide all required inputs.")
        else:
            with st.status("Assigning AI professional to write your Google Ads copy..", expanded=True) as status:
                response = tweet_generator(target_audience, hook)
                if response:
                    st.subheader(f'**🧕👩: Your Tweets!**')
                    st.markdown(response)
                else:
                    st.error("💥**Failed to write Letter. Please try again!**")


def tweet_generator(target_audience, hook):
    """ Email project_update_writer """

    prompt = f"""
    You are a social media expert creating tweets for an audience interested in {target_audience}. 
    Write 5 engaging, concise, and visually appealing tweets that each:

    1. Start with a compelling hook based on the following keywords: "{hook}"
    2. Include a compelling call to action.
    3. Use 2-3 relevant hashtags. 
    4. Adopt a tone that matches the following options: 
        - Humorous 
        - Informative 
        - Inspirational 
        - Serious 
        - Casual
    5. Be under 100 characters (including spaces and punctuation). 

    Here are some examples of call-to-actions to include:
    - Retweet this if you agree!
    - Share your thoughts in the comments!
    - Learn more at [link] 
    - Follow for more [topic] content
    - Like if you're excited about [topic]

    Output each tweet separated by a newline.
    """

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)
