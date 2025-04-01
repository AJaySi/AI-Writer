"""Webpage content analysis tool."""

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from urllib.parse import urlparse

st.title("🧠 Web Content Analyzer: Uncover Hidden Insights with AI! 🧠")
st.write("""
        Welcome!  This tool leverages the power of AI to analyze your web page's content.  It goes beyond just keywords - 
        we'll use cutting-edge technology to uncover valuable insights and unlock new ways to boost your website! 
    """)

# --- User Input ---

url_input = st.text_input("Paste your URL here:", "https://www.example.com/")
language_input = st.selectbox("What language is your content?", ('English', 'Italian', 'Albanian'))
st.write("  ") 

# ---  AI Model Setup --- 

llm = OpenAI(temperature=0.7)
conversation_chain = ConversationChain(llm=llm)  

# --- Analyze Button & Processing --- 

if st.button("Analyze with AI!"):
    with st.spinner('Analyzing your content...'):
        url = url_input.strip()
        language = language_input.lower()

        if not url.startswith("http"):
            st.error("Oops! Looks like you forgot 'http://' or 'https://' at the beginning of your URL.  Please add it and try again! 😊")
            st.stop()

        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = "https://" + url
            
            # Fetch webpage content
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract content
            title = soup.title.string if soup.title else "No title found"
            meta_description = soup.find('meta', {'name': 'description'})
            description = meta_description['content'] if meta_description else "No description found"
            
            # Display results
            st.subheader("Page Analysis")
            st.metric("Title", title)
            st.metric("Description", description)
            
            # Content statistics
            text_content = soup.get_text()
            words = text_content.split()
            st.metric("Word Count", len(words))
            st.metric("Unique Words", len(set(words)))
            
            # Frequency analysis (same as before)
            freq = nltk.FreqDist(words)
            keywords = freq.most_common(10)  
            df_keywords = pd.DataFrame(keywords, columns=("Keyword", "Frequency"))

            # ---  AI-Powered Insights --- 
            st.subheader("AI Insights:")
            st.write("  ")

            st.markdown("**Main Theme:**")
            ai_theme = conversation_chain.run(f"What is the main theme or topic of this content? \n {text_content}")
            st.markdown(f"  {ai_theme}")

            st.write("  ")

            st.markdown("**Suggested Keywords:**")
            ai_keywords = conversation_chain.run(f"What other relevant keywords might be helpful to target for this content? \n {text_content}")
            st.markdown(f"  {ai_keywords}")

            st.write("  ")

            st.markdown("**Content Improvement:**")
            ai_improvement = conversation_chain.run(f"What could be done to improve this content for clarity, engagement, or SEO? \n {text_content}")
            st.markdown(f"  {ai_improvement}")

            # --- Display Frequency Results ---
            st.write("  ")

            st.subheader("Top Keywords:")
            st.write("  ")
            st.dataframe(df_keywords)

            st.subheader("What's the Value of This AI Analysis?")
            st.write("  ")
            
            st.markdown(""" 
            *  **Uncover Hidden Insights:**  AI can analyze your content in much more nuanced ways, helping you spot connections and trends you might have missed.
            *  **Go Beyond Keywords:**  AI can provide in-depth insights into your content's main themes, tone, and even suggest relevant topics to explore further.
            * **AI as a Partner:** Think of this AI as your content strategist, offering guidance and actionable steps to make your content even better.

            Ready to leverage the power of AI to optimize your content? Start putting the suggestions and insights you just received into practice. See what difference AI can make in your writing! 🚀
            """)
        except requests.exceptions.RequestException as e:
            st.error(f"Oops! Something went wrong fetching the URL.  Error: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
