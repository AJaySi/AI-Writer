import streamlit as st
from urllib.parse import urlparse


# Title and introduction
def show_title_and_intro():
    st.title("🌟 URL SEO Checkup: Your Link's Health Report 🌟")
    st.write("""
        Welcome to the URL SEO Checkup! This tool is like a doctor for your website links. 
        Just paste your URL, and we'll check if it's healthy and ready to climb the search engine ladder.
    """)


# Basic HTTPS Check
def check_https(url):
    st.subheader("The Basics - Are We Looking Good?")
    st.write("---")
    
    if url.startswith("https://"):
        st.success("✨ You're using HTTPS! This adds extra security, and Google rewards that with better rankings. Keep it up! ✨")
    else:
        st.warning("🚧 Heads Up! Your URL doesn't use 'https://'. This is a red flag for Google.")
        st.info("🔧 **How to fix:** Contact your hosting provider or website developer to install an SSL certificate. This will secure your site with HTTPS.")


# URL Length Check
def check_url_length(path):
    st.subheader("The Length Test - Keep it Short and Sweet!")
    st.write("---")
    
    if len(path) <= 50:
        st.success("🏆 Great! Your URL is short and user-friendly. Google loves short URLs! 🏆")
    else:
        st.warning("🧭 Tip: Try shortening your URL. Shorter URLs are easier to remember and better for SEO.")
        st.info("🔧 **How to fix:** Consider removing unnecessary words or folders in the URL. Aim for concise, descriptive URLs that are easy for users to read.")


# Hyphen Check
def check_hyphens(path):
    st.subheader("The Hyphen Check - Use Hyphens for Clear Separation!")
    st.write("---")
    
    if "-" in path:
        st.success("😎 You're on the right track! Using hyphens makes your URL more readable for both users and Google. 😎")
    else:
        st.warning("❓ Did you know? Using hyphens between words (like 'shoes-for-sale') helps Google understand your URL better!")
        st.info("🔧 **How to fix:** Update your URL to use hyphens (-) instead of spaces or underscores (_). For example, 'shoes-for-sale' instead of 'shoes_for_sale'.")


# File Extension Check
def check_file_extension(path):
    st.subheader("File Extension Check - Showing Your Files With Pride!")
    st.write("---")
    
    if "." in path:
        st.success("🥳 File Extension Check: Your URL includes a file extension like '.html', which helps Google categorize your page. Nice job! 🥳")
    else:
        st.warning("🤔 Your URL seems to be missing a file extension like '.html' or '.php'.")
        st.info("🔧 **How to fix:** While file extensions are not always required, adding them to static pages (like .html or .php) can improve clarity for search engines.")


# Keyword Insights
def show_keyword_insights(netloc, path):
    st.subheader("Bonus Insight - Let's Talk Keywords")
    st.write("---")
    
    st.info("Keywords are the words people use to search for information online. Your goal is to help Google understand what your page is about by using the right keywords in your URL!")
    
    st.markdown(f"""
        **Your Domain:** {netloc}  
        **Your URL Path:** {path}
        
        **Suggestion:** Consider adding a primary keyword to your URL if it aligns with your page content. But don't overdo it – too many keywords can hurt your SEO. Keep it natural!
    """)


# Main function to run the analysis
def run_analysis(url):
    # Parse the URL
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc  # Domain name
    path = parsed_url.path  # Path after the domain

    # Run checks
    check_https(url)
    check_url_length(path)
    check_hyphens(path)
    check_file_extension(path)
    show_keyword_insights(netloc, path)


# Display the app
def url_seo_checker():
    show_title_and_intro()

    # User input for URL
    url_input = st.text_input("Paste your URL here:", "https://www.example.com/")
    st.write(" ")  # Add spacing

    # When the analyze button is clicked
    if st.button("Let's Analyze!"):
        with st.spinner('Checking your link...'):
            url = url_input.strip()  # Clean up the input

            # Validate URL format
            if not url.startswith(("http://", "https://")):
                st.error("Oops! It seems like your URL needs 'http://' or 'https://' at the beginning. Please add it!")
                st.stop()

            # Run the analysis
            run_analysis(url)
