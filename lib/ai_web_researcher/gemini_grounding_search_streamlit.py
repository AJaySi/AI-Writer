import os
import streamlit as st
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

# Set page config
st.set_page_config(
    page_title="Gemini Grounding Search",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
.container {
    align-items: center;
    border-radius: 8px;
    display: flex;
    font-family: Google Sans, Roboto, sans-serif;
    font-size: 14px;
    line-height: 20px;
    padding: 8px 12px;
    background-color: #fafafa;
    box-shadow: 0 0 0 1px #0000000f;
    margin-top: 20px;
}
.chip {
    display: inline-block;
    border: solid 1px;
    border-radius: 16px;
    min-width: 14px;
    padding: 5px 16px;
    text-align: center;
    user-select: none;
    margin: 0 8px;
    background-color: #ffffff;
    border-color: #d2d2d2;
    color: #5e5e5e;
    text-decoration: none;
}
.chip:hover {
    background-color: #f2f2f2;
}
.carousel {
    overflow: auto;
    scrollbar-width: none;
    white-space: nowrap;
    margin-right: -12px;
    display: flex;
    align-items: center;
}
.headline {
    display: flex;
    margin-right: 4px;
    align-items: center;
}
.gradient-container {
    position: relative;
}
.gradient {
    position: absolute;
    transform: translate(3px, -9px);
    height: 36px;
    width: 9px;
    background: linear-gradient(90deg, #fafafa 15%, #fafafa00 100%);
}
.result-text {
    font-size: 16px;
    line-height: 1.6;
    color: #202124;
    margin: 20px 0;
    white-space: pre-wrap;
}
@media (prefers-color-scheme: dark) {
    .container {
        background-color: #1f1f1f;
        box-shadow: 0 0 0 1px #ffffff26;
    }
    .headline-label {
        color: #fff;
    }
    .chip {
        background-color: #2c2c2c;
        border-color: #3c4043;
        color: #fff;
    }
    .chip:hover {
        background-color: #353536;
    }
    .gradient {
        background: linear-gradient(90deg, #1f1f1f 15%, #1f1f1f00 100%);
    }
    .result-text {
        color: #e8eaed;
    }
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("Gemini Grounding Search")

# Initialize Gemini client
if 'GEMINI_API_KEY' not in os.environ:
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    if api_key:
        os.environ['GEMINI_API_KEY'] = api_key

# Search input
search_query = st.text_input("Enter your search query:", "When is the next total solar eclipse in the United States?")

if st.button("Search"):
    if 'GEMINI_API_KEY' not in os.environ:
        st.error("Please enter your Gemini API Key first!")
    else:
        try:
            client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
            model_id = "gemini-2.0-flash"

            google_search_tool = Tool(
                google_search = GoogleSearch()
            )

            with st.spinner("Searching..."):
                response = client.models.generate_content(
                    model=model_id,
                    contents=search_query,
                    config=GenerateContentConfig(
                        tools=[google_search_tool],
                        response_modalities=["TEXT"],
                    )
                )

                # Display search results header
                st.header("Search Results")
                
                # Display the response text
                if response.candidates[0].content.parts:
                    st.markdown('<div class="result-text">' + 
                              response.candidates[0].content.parts[0].text.replace('\n', '<br>') + 
                              '</div>', 
                              unsafe_allow_html=True)

                # Display the grounding metadata
                if hasattr(response.candidates[0], 'grounding_metadata') and \
                   hasattr(response.candidates[0].grounding_metadata, 'search_entry_point') and \
                   hasattr(response.candidates[0].grounding_metadata.search_entry_point, 'rendered_content'):
                    
                    st.header("Related Searches")
                    rendered_content = response.candidates[0].grounding_metadata.search_entry_point.rendered_content
                    st.markdown(rendered_content, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}") 