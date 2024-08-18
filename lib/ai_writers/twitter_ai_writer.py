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
                label="**What's the tweet about? (Hook)**",
                placeholder="e.g., Discover the future of tech today!",
                help="Provide a compelling opening statement or question to grab attention."
            )

        with col2:
            target_audience = st.text_input(
                label="**Target Audience**",
                placeholder="e.g., technology enthusiasts, travel lovers",
                help="Describe the audience you want to target with this tweet."
            )

        col3, col4 = st.columns([5, 5])
        with col3:
            tweet_tone = st.selectbox(
                label="**Tweet Tone**",
                options=["Humorous", "Informative", "Inspirational", "Serious", "Casual"],
                help="Choose the tone you'd like the tweet to have."
            )

        with col4:
            cta = st.text_input(
                label="**Call to Action (Optional)**",
                placeholder="e.g., Retweet this if you agree! (Leave blank if not applicable)",
                help="Provide a call to action if you'd like to include one."
            )

        col5, col6 = st.columns([5, 5])
        with col5:
            keywords_hashtags = st.text_input(
                label="**Keywords/Hashtags**",
                placeholder="e.g., #AI #Innovation",
                help="Provide 2-3 relevant keywords or hashtags."
            )

        with col6:
            tweet_length = st.selectbox(
                "Tweet Length (Optional)",
                options=["Short (under 100 characters)", "Medium (100-200 characters)", "Long (200+ characters)"],
                help="Choose the desired tweet length.",
            )

    if st.button('**Write Tweets**'):
        if not target_audience or not hook:
            st.error("🚫 Please provide all required inputs.")
        else:
            with st.status("Assigning AI professional to write your tweets...", expanded=True) as status:
                response = tweet_generator(target_audience, hook, tweet_tone, cta, keywords_hashtags, tweet_length)
                if response:
                    st.subheader(f'**🧕👩: Your Tweets!**')
                    st.markdown(response)
                else:
                    st.error("💥**Failed to generate tweets. Please try again!**")


def tweet_generator(target_audience, hook, tone_style, cta, keywords_hashtags, tweet_length):
    """ Tweet Generator """

    prompt = f"""
	    You are a social media expert creating tweets for an audience interested in {target_audience}. 
	    Write 5 engaging, concise, and visually appealing tweets that each:
	
	    1. Start with a compelling hook based on the following input: "{hook}"
	    2. Include the following call to action: "{cta}" 
	    3. Use 2-3 relevant keywords/hashtags, including: "{keywords_hashtags}"
	    4. Adopt the following tone/style: "{tone_style}"
	    5. Adhere to the following length requirement: {tweet_length} 
	    
	    Make sure to keep the tone consistent with the selected style and platform context.
	
	    Here are some examples of call-to-actions to include (if no specific CTA was provided): 
	    - Retweet this if you agree!
	    - Share your thoughts in the comments!
	    - Learn more at [link] 
	    - Follow for more {target_audience} content.
	
	    Output each tweet separated by a newline.
	    """

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)
