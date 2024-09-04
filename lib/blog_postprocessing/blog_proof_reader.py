import os
import sys
import configparser

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def blog_proof_editor(blog_content):
    """ Helper for blog proof reading. """

    try:
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'main_config'))
        config = configparser.ConfigParser()
        #config = configparser.RawConfigParser()
        config.read(config_path, encoding='utf-8')
    except Exception as err:
        print(f"ProofReader: Failed to read values from config: {err}")

    prompt = f"""As an expert content writer and editor, I will provide you with 'my blog' content.
        Your task is to rewrite my blog, by following the guidelines below.
        
        Below are the guidelines to follow:

        1). You must respond in {config.get('blog_characteristics', 'blog_language')} language.
        2). Vocabulary and Grammar Enhancement: Directly correct any grammatical errors and upgrade the 
        vocabulary for better readability.
        3). Improve Sentence Structure: Enhance sentence construction for better clarity and conversational flow.
        4). Tone and Brand Alignment: Adjust tone, voice, personality for {config.get('blog_characteristics', 'blog_tone')} audience.
        5). Optimize Content Structure: Reorganize content for more impactful presentation, including better paragraphing & transitions.
        6). Simplify content: Simplify concepts and replace overly complex words. Use simple english words.
        7). Make sure your response content length is of {config.get('blog_characteristics', 'blog_length')} words.

        \n\nMy Blog: '{blog_content}'. """

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Error Blog Proof Reading: {err}")

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from langchain.llms import OpenAI
from langchain.chains import ConversationChain

# ... (rest of your code)

    if st.button("Analyze with AI!"):
        # ... (fetch and process content as before)

        with st.spinner('Analyzing your content...'):
            st.subheader("AI Insights:")
            st.write("  ")

            #  1. Overall Critique 
            st.markdown("**Overall Evaluation:**")
            ai_overall = conversation_chain.run(f"""Analyze the provided article and give a constructive critique, focusing on its strengths and weaknesses regarding:
            * Informativeness: Does it offer valuable information the reader might not know, or strengthen their understanding?
            * Authority: Does the author demonstrate expertise and credibility, backing up claims with evidence?
            * Captivatingness:  Does it effectively engage the reader, capture attention, and make them want to continue reading? 

            Provide specific examples to support your evaluation.
            """)
            st.markdown(f"  {ai_overall}")
            st.write("  ")

            # 2. Structure & Organization
            st.markdown("**Structure and Organization:**")
            ai_structure = conversation_chain.run(f"""Analyze the structure and organization of the provided article. 
            * Does it flow logically, with a clear beginning, middle, and end?
            * Are subheadings effectively used to break down the content and guide the reader?
            * Is the writing style consistent throughout the article?

            Suggest improvements for clarity and readability.
            """)
            st.markdown(f"  {ai_structure}")
            st.write("  ")

            # 3.  Content Quality
            st.markdown("**Content Quality:**")
            ai_content = conversation_chain.run(f"""Critique the content of the article, considering:
            * Is the value of the article clear? 
            * Does it address a pain point or a need for the target audience?
            * Are the arguments compelling and supported by evidence or examples? 
            *  Are any technical terms explained well?

            Identify areas where the content could be strengthened or improved.
            """)
            st.markdown(f"  {ai_content}")
            st.write("  ")

            # 4.  Call to Action & Headline 
            st.markdown("**Headline and Call to Action:**")
            ai_headline = conversation_chain.run(f"""Evaluate the effectiveness of the headline and call to action (CTA) in the provided article.
            * Does the headline accurately and compellingly summarize the article's content? 
            * Is the CTA clear, actionable, and positioned well within the text?

            Provide suggestions for improving the headline and CTA.
            """)
            st.markdown(f"  {ai_headline}")
            st.write("  ")

            # 5.  Writing Style & Tone 
            st.markdown("**Writing Style and Tone:**")
            ai_style = conversation_chain.run(f"""Assess the overall writing style and tone of the article.
            * Does it use jargon or overly technical language that might be inaccessible to the target audience?
            * Is the tone appropriate for the topic and target audience (e.g., professional, conversational, humorous)?
            *  Is the writing clear, concise, and engaging? 

            Suggest ways to improve the writing style and make the article more accessible and compelling for the intended reader.
            """)
            st.markdown(f"  {ai_style}")

            #  ---  Display Keyword Results (same as before) --- 
        # ... (rest of your code)
