import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from langchain.llms import OpenAI
from langchain.chains import ConversationChain

st.set_page_config(layout="wide", page_title="Web Content Analyzer - Dive Deep with AI!", page_icon=":mag_right:")

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

authorized_domains = ["example.com", "another-example.com"]

if st.button("Analyze with AI!"):
    with st.spinner('Analyzing your content...'):
        url = url_input.strip()
        language = language_input.lower()

        if not url.startswith("http"):
            st.error("Oops! Looks like you forgot 'http://' or 'https://' at the beginning of your URL.  Please add it and try again! 😊")
            st.stop()

        domain = url.split("//")[-1].split("/")[0]
        if not any(domain.endswith(auth_domain) for auth_domain in authorized_domains):
            st.error("The provided URL is not authorized. Please use a URL from an authorized domain.")
            st.stop()

        try:
            response = requests.get(url)
            response.raise_for_status()  

            soup = BeautifulSoup(response.content, 'html.parser')
            body_txt = soup.find('body').text

            words = [w.lower() for w in word_tokenize(body_txt)]
            stopw = nltk.corpus.stopwords.words(language)

            final_words = [w for w in words if w not in stopw and w.isalpha()]

            # Frequency analysis (same as before)
            freq = nltk.FreqDist(final_words)
            keywords = freq.most_common(10)  
            df_keywords = pd.DataFrame(keywords, columns=("Keyword", "Frequency"))

            # ---  AI-Powered Insights --- 
            st.subheader("AI Insights:")
            st.write("  ")

            st.markdown("**Main Theme:**")
            ai_theme = conversation_chain.run(f"What is the main theme or topic of this content? \n {body_txt}")
            st.markdown(f"  {ai_theme}")

            st.write("  ")

            st.markdown("**Suggested Keywords:**")
            ai_keywords = conversation_chain.run(f"What other relevant keywords might be helpful to target for this content? \n {body_txt}")
            st.markdown(f"  {ai_keywords}")

            st.write("  ")

            st.markdown("**Content Improvement:**")
            ai_improvement = conversation_chain.run(f"What could be done to improve this content for clarity, engagement, or SEO? \n {body_txt}")
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
