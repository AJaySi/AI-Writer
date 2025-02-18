import os
import json
import requests
import streamlit as st
DATAFORSEO_USERNAME = os.getenv('DATAFORSEO_USERNAME', 'your_username')
DATAFORSEO_PASSWORD = os.getenv('DATAFORSEO_PASSWORD', 'your_password')
BASE_URL = "https://api.dataforseo.com/v3/"

def _make_dataforseo_request(endpoint, payload):
    """Helper function to make DataForSEO API requests"""
    try:
        response = requests.post(
            f"{BASE_URL}{endpoint}",
            auth=(DATAFORSEO_USERNAME, DATAFORSEO_PASSWORD),
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"DataForSEO API Error: {str(e)}")
        return None

def dataforseo_keyword_research():
    """Perform AI-powered keyword research using DataForSEO API"""
    st.header("🔍 DataForSEO Keyword Research")
    with st.form("keyword_research_form"):
        keyword = st.text_input("Seed Keyword", help="Enter primary keyword to research")
        location = st.text_input("Location", value="United States", help="Target geographic location")
        language = st.text_input("Language", value="en", help="Target language code")
        depth = st.slider("Research Depth", 1, 5, 3, help="Depth of keyword analysis")
        
        if st.form_submit_button("Run Keyword Research"):
            with st.spinner("Analyzing keyword opportunities..."):
                payload = [{
                    "keyword": keyword,
                    "location_name": location,
                    "language_name": language,
                    "depth": depth
                }]
                
                response = _make_dataforseo_request("dataforseo_labs/google/keywords_for_keywords/live", payload)
                if response:
                    st.success("Keyword research completed!")
                    st.json(response.get('tasks', [{}])[0].get('result', []))

def dataforseo_rank_tracking():
    """Track keyword rankings using DataForSEO"""
    st.header("📊 DataForSEO Rank Tracking")
    with st.form("rank_tracking_form"):
        domain = st.text_input("Domain to Track", help="Enter domain to monitor rankings")
        keywords = st.text_area("Keywords to Track", help="One keyword per line")
        location = st.text_input("Location", value="United States")
        
        if st.form_submit_button("Start Tracking"):
            with st.spinner("Setting up rank tracking..."):
                # Placeholder for API implementation
                st.success(f"Rank tracking started for {domain}")
                st.write("Implement rank tracking API integration here")

def dataforseo_competitor_analysis():
    """Analyze competitor SEO strategies"""
    st.header("📈 DataForSEO Competitor Analysis")
    with st.form("competitor_analysis_form"):
        target_domain = st.text_input("Competitor Domain", help="Domain to analyze")
        my_domain = st.text_input("Your Domain", help="Your domain for comparison")
        analysis_type = st.selectbox("Analysis Type", 
            ["Backlinks", "Keywords", "Content", "Technical SEO"])
        
        if st.form_submit_button("Run Analysis"):
            with st.spinner("Analyzing competitor strategies..."):
                # Placeholder for API implementation
                st.success(f"Competitor analysis completed for {target_domain}")
                st.write("Implement competitor analysis API integration here")