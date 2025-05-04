"""
Streamlit UI for FAQ Generator

This module provides a user-friendly interface for generating FAQs from various content sources.
"""

import streamlit as st
import asyncio
from pathlib import Path
from typing import Optional
import json
import requests
from bs4 import BeautifulSoup

from .faqs_generator_blog import FAQGenerator, FAQConfig, TargetAudience, FAQStyle, SearchDepth


def fetch_url_content(url):
    """Fetch and extract content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        st.error(f"Error fetching URL content: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="FAQ Generator",
        page_icon="❓",
        layout="wide"
    )
    
    st.title("FAQ Generator")
    st.markdown("Generate comprehensive FAQs from your content with research integration.")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Basic settings
        num_faqs = st.slider("Number of FAQs", 1, 20, 5)
        target_audience = st.selectbox(
            "Target Audience",
            [audience.value for audience in TargetAudience]
        )
        faq_style = st.selectbox(
            "FAQ Style",
            [style.value for style in FAQStyle]
        )
        
        # Advanced settings
        with st.expander("Advanced Settings"):
            include_emojis = st.checkbox("Include Emojis", value=True)
            include_code_examples = st.checkbox("Include Code Examples", value=True)
            include_references = st.checkbox("Include References", value=True)
            
            search_depth = st.selectbox(
                "Search Depth",
                [depth.value for depth in SearchDepth]
            )
            time_range = st.selectbox(
                "Time Range",
                ["last_month", "last_6_months", "last_year", "all_time"]
            )
            language = st.text_input("Language", value="English")
    
    # Main content area
    content_type = st.radio(
        "Content Source",
        ["Direct Input", "File Upload", "URL"]
    )
    
    content = ""
    if content_type == "Direct Input":
        content = st.text_area("Enter your content", height=300)
    
    elif content_type == "URL":
        url = st.text_input("Enter URL")
        if url:
            content = fetch_url_content(url)
            if content:
                st.text_area("Extracted Content", content, height=300)
    
    # Generate button
    if st.button("Generate FAQs") and content:
        try:
            # Create config
            config = FAQConfig(
                num_faqs=num_faqs,
                target_audience=TargetAudience(target_audience),
                faq_style=FAQStyle(faq_style),
                include_emojis=include_emojis,
                include_code_examples=include_code_examples,
                include_references=include_references,
                search_depth=SearchDepth(search_depth),
                time_range=time_range,
                language=language
            )
            
            # Initialize generator
            generator = FAQGenerator(config)
            
            # Generate FAQs
            with st.spinner("Generating FAQs..."):
                faqs = asyncio.run(generator.generate_faqs(content))
            
            # Display results
            st.success("FAQs generated successfully!")
            
            # Output format selection
            output_format = st.radio(
                "Output Format",
                ["Preview", "Markdown", "HTML", "JSON"]
            )
            
            if output_format == "Preview":
                for i, faq in enumerate(faqs, 1):
                    with st.expander(f"{i}. {faq.question}"):
                        st.markdown(faq.answer)
                        if faq.code_example:
                            st.code(faq.code_example)
                        if faq.references:
                            st.markdown("**References:**")
                            for ref in faq.references:
                                st.markdown(f"- [{ref['title']}]({ref['url']}) - {ref['source']} ({ref['date']})")
            
            elif output_format == "Markdown":
                st.code(generator.to_markdown(), language="markdown")
                st.download_button(
                    "Download Markdown",
                    generator.to_markdown(),
                    file_name="faqs.md",
                    mime="text/markdown"
                )
            
            elif output_format == "HTML":
                st.code(generator.to_html(), language="html")
                st.download_button(
                    "Download HTML",
                    generator.to_html(),
                    file_name="faqs.html",
                    mime="text/html"
                )
            
            elif output_format == "JSON":
                json_output = json.dumps([faq.__dict__ for faq in faqs], indent=2)
                st.code(json_output, language="json")
                st.download_button(
                    "Download JSON",
                    json_output,
                    file_name="faqs.json",
                    mime="application/json"
                )
        
        except Exception as e:
            st.error(f"Error generating FAQs: {str(e)}")

if __name__ == "__main__":
    main() 