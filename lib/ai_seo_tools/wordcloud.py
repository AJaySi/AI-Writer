import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

st.set_page_config(layout="wide", page_title="Web Content Analyzer - Dive Into Your Words!", page_icon=":mag:")

st.title("🔎 Web Content Analyzer:  Uncover Your Words' Power! 🔎")
st.write("""
        Welcome!  This tool helps you understand the words that drive your website content.  Just paste in your web page's 
        URL, and we'll give you insights you can use to improve your content and reach more people! 
    """)

url_input = st.text_input("Paste your URL here:", "https://www.example.com/")
language_input = st.selectbox("What language is your content?", ('English', 'Italian', 'Albanian'))
num_results_input = st.slider("How many top words/phrases should we show?", min_value=10, max_value=150, value=50)
st.write("  ") 

authorized_domains = ["example.com", "another-example.com"]

if st.button("Analyze Your Content!"):
    with st.spinner('Analyzing your content...'):
        url = url_input.strip()
        language = language_input.lower()
        num_results = num_results_input

        if not url.startswith("http"):
            st.error("Oops! Looks like you forgot 'http://' or 'https://' at the beginning of your URL.  Please add it and try again! 😊")
            st.stop()

        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        if parsed_url.netloc not in authorized_domains:
            st.error("The domain of the provided URL is not authorized. Please use an authorized domain.")
            st.stop()

        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for errors

            soup = BeautifulSoup(response.content, 'html.parser')
            body_txt = soup.find('body').text

            words = [w.lower() for w in word_tokenize(body_txt)]
            stopw = nltk.corpus.stopwords.words(language)

            final_words = [w for w in words if w not in stopw and w.isalpha()]

            # Frequency analysis
            freq = nltk.FreqDist(final_words)
            keywords = freq.most_common(num_results)
            
            bigrams = ngrams(final_words, 2)
            freq_bigrams = nltk.FreqDist(bigrams)
            bigrams_freq = freq_bigrams.most_common(num_results)

            # Create DataFrames for Display
            df_keywords = pd.DataFrame(keywords, columns=("Keyword", "Frequency"))
            df_bigrams = pd.DataFrame(bigrams_freq, columns=("Bigram", "Frequency"))

            st.subheader("Top Keywords and Phrases:")
            st.write("  ")
            st.dataframe(df_keywords)

            st.write("  ")

            st.subheader("Top Two-Word Phrases:")
            st.write("  ")
            st.dataframe(df_bigrams)

            st.write("  ")
            st.subheader("What's the Value of This Analysis?")
            st.write("  ")

            st.markdown(""" 
            *  **See What Resonates:** Discover the most popular words and phrases used on your website. This can reveal themes and topics that your audience is interested in.
            *  **Find Keywords for SEO:** The analysis helps identify relevant keywords you could use for your website content and marketing efforts. 
            *  **Improve Your Content:**  You can understand how people might search for similar content and ensure you're providing the right keywords.
            * **Stand Out:**  Compare your results to other websites or competitors to understand how you can differentiate your content.  

            Ready to dive deeper into your content's vocabulary? Start by making some of the keywords you just discovered the stars of your next blog post or social media message. You might be surprised at the impact! 🚀
            """)
        
        except requests.exceptions.RequestException as e:
            st.error(f"Oops! Something went wrong fetching the URL.  Error: {e}")
