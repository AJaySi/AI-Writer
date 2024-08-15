import time #Iwish
import os
import json
import requests
import streamlit as st

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def insta_writer():
    # Title and description
    st.title("✍️ Instagram Caption Writer")

    # Input section
    with st.expander("**PRO-TIP** - Read the instructions below.", expanded=True):
        input_insta_keywords = st.text_input('**Enter main keywords of Your instagram caption!**')
        col1, col2, space, col3, col4 = st.columns([5, 5, 0.5, 5, 5])
        with col1:
            input_insta_type = st.selectbox('Voice Tone', ('Neutral', 'Formal', 'Casual', 'Funny', 
                'Optimistic', 'Assertive', 'Friendly', 'Encouraging', 'Sarcastic'), index=0)
        with col2:
            input_insta_cta = st.selectbox('CTA (Call To Action)', ('Shop Now', 
                'Learn More', 'Swipe Up', 'Sign Up', 'Link in Bio', 'Sense of urgency'), index=0)
        with col3:
            input_insta_audience = st.selectbox('Choose Target Audience', ('For All', 
                'Age:18-24 (Gen Z)', 'Age:25-34 (Millennials)'), index=0)
        with col4:
            input_insta_language = st.selectbox('Choose Language', ('English', 'Hindustani',
                'Chinese', 'Hindi', 'Spanish'), index=0)

    
        # Generate Blog Title button
        if st.button('**Get Instagram Captions**'):
            with st.spinner():
                # Clicking without providing data, really ?
                if not input_insta_keywords:
                    st.error('** 🫣 P🫣   Provide Inputs to generate Blog Tescription.  Keywords, are required!**')
                elif input_insta_keywords:
                    insta_captions = generate_insta_captions(input_insta_keywords,
                            input_insta_type, 
                            input_insta_cta,
                            input_insta_audience,
                            input_insta_language
                            )
                    if insta_captions:
                        st.subheader('**👩👩🔬Go Viral, with these Instagram captions!🎆🎇 🎇**')
                        st.markdown(insta_captions)
                    else:
                        st.error("💥**Failed to generate instagram Captions. Please try again!**")


# Function to generate blog metadesc
def generate_insta_captions(input_insta_keywords, input_insta_type, input_insta_cta, input_insta_audience, input_insta_language):
    """ Function to call upon LLM to get the work done. """

    # If keywords and content both are given.
    if input_insta_keywords:
        prompt = f"""As an instagram expert and experienced content writer, 
        I will provide you with my 'instagram caption keywords', along with CTA, Target Audience & voice tone.
        Your task is to write 3 instagram captions.

        Follow below guidelines to generate instagram captions:
        1). Front-Loading: Capture attention by placing key info at the beginning of your captions.
        2). Optimise your captions for {input_insta_cta} Call-to-Action (CTA). 
        3). Hashtag Usage: Limit yourself to four relevant hashtags per caption.
        4). Brand Voice and Tone: Use and convey {input_insta_type} voice tone in your captions.
        5). Optimise your captions for {input_insta_audience} target audience.
        6). Emojis: Inject personality and emotion into your captions with emojis.
        7). Brevity: Keep your captions concise and to the point.
        8). Important: Your response should be in {input_insta_language} language.

        \nInstagram caption keywords: '{input_insta_keywords}'\n
        """

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)
