import time #Iwish
import os
import json
import requests
import streamlit as st

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen
from ..ai_web_researcher.gpt_online_researcher import do_google_serp_search


def linked_post_writer():
    # Title and description
    st.title("✍️ Alwrity - AI Linkedin Blog Post Generator")

    # Input section
    with st.expander("**PRO-TIP** - Read the instructions below.", expanded=True):
        input_blog_keywords = st.text_input('**Enter main keywords of your Post!** (2-3 words that defines your blog)')
        col1, col2, space, col3 = st.columns([5, 5, 0.5, 5])
        with col1:
            input_linkedin_type = st.selectbox('Post Type', ('General', 'How-to Guides', 'Polls', 'Listicles', 
                'Reality check posts', 'Job Posts', 'FAQs', 'Checklists/Cheat Sheets'), index=0)
        with col2:
            input_linkedin_length = st.selectbox('Post Length', ('1000 words', 'Long Form', 'Short form'), index=0)
        with col3:
            input_linkedin_language = st.selectbox('Choose Language', ('English', 'Vietnamese',
                'Chinese', 'Hindi', 'Spanish'), index=0)
        # Generate Blog FAQ button
        if st.button('**Get LinkedIn Post**'):
            with st.spinner():
                # Clicking without providing data, really ?
                if not input_blog_keywords:
                    st.error('** 🫣Provide Inputs to generate Blinkedin Post. Keywords, required!**')
                elif input_blog_keywords:
                    linkedin_post = generate_linkedin_post(input_blog_keywords, input_linkedin_type, 
                            input_linkedin_length, input_linkedin_language)
                    if linkedin_post:
                        st.subheader('**🧕🔬👩 Go Rule LinkedIn with this Blog Post!**')
                        st.write(linkedin_post)
                        st.write("\n\n\n")
                    else:
                        st.error("💥**Failed to generate linkedin Post. Please try again!**")


# Function to generate blog metadesc
def generate_linkedin_post(input_blog_keywords, input_linkedin_type, input_linkedin_length, input_linkedin_language):
    """ Function to call upon LLM to get the work done. """

    # Fetch SERP results & PAA questions for FAQ.
    serp_results, people_also_ask = do_google_serp_search(input_blog_keywords)

    # If keywords and content both are given.
    if serp_results:
        prompt = f"""As an Experienced, industry veteran and experienced linkedin content writer, 
        I will provide you with my 'blog keywords' and 'google serp results' done for the keywords.
        Your task is to write a detailed linkedin post, using given keywords and search results.

        Follow below guidelines for generating the linkedin post:
        1). Write a title, introduction, sections, faqs and a conclusion for the post.
        2). Your FAQ should be based on 'People also ask' and 'Related Queries' from given serp results.
        3). Maintain consistent voice of tone, keep the sentence short and simple.
        4). Make sure to include important results from the given google serp results.
        5). Optimise your response for blog type of {input_linkedin_type}.
        6). Important to provide your response in {input_linkedin_language} language.\n

        Your final response should demostrate Experience, Expertise, Authoritativeness, and Trustworthiness.

        blog keywords: \'\'\'{input_blog_keywords}\'\'\'
        google serp results: \'\'\'{serp_results}\'\'\'
        """

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        st.error(f"Failed to generate Open Graph tags: {err}")
        return None
