import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import research modules (placeholder imports for now)
try:
    from ai_web_researcher import (
        google_serp_search,
        tavily_ai_search,
        metaphor_basic_neural_web_search,
        google_trends_researcher,
        firecrawl_web_crawler
    )
except ImportError:
    # For development/testing without actual modules
    pass

def load_css():
    """Load custom CSS"""
    css_file = Path(__file__).parent / "style.css"
    with open(css_file) as f:
        css_content = f.read()
        # Use session state to track if CSS has been loaded
        if 'css_loaded' not in st.session_state:
            st.session_state['css_loaded'] = False
        
        # Always apply CSS on each page load to ensure styles persist during navigation
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        st.session_state['css_loaded'] = True

def display_google_serp_results(results):
    """Display Google SERP search results"""
    # Check if results are available
    if not results:
        st.warning("No search results available. Please try a different query or check your API configuration.")
        return
        
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    # Display organic results
    st.markdown('<div class="category-header">Search Results</div>', unsafe_allow_html=True)
    
    # Display actual organic results
    organic_results = results.get('organic', [])
    if organic_results:
        for result in organic_results:
            st.markdown(f"""
            <div class="result-item">
                <div class="result-title">{result.get('title', 'No Title')}</div>
                <div class="result-url">{result.get('link', '#')}</div>
                <div class="result-snippet">{result.get('snippet', 'No description available.')}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No organic search results found.")
    
    # Display People Also Ask
    paa_results = results.get('peopleAlsoAsk', [])
    if paa_results:
        st.markdown('<div class="category-header">People Also Ask</div>', unsafe_allow_html=True)
        
        for question in paa_results:
            st.markdown(f"""
            <div class="result-item">
                <div class="result-title">{question.get('question', 'No Question')}</div>
                <div class="result-snippet">{question.get('snippet', 'No answer available.')}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Display Related Searches if available
    related_searches = results.get('relatedSearches', [])
    if related_searches:
        st.markdown('<div class="category-header">Related Searches</div>', unsafe_allow_html=True)
        
        for search in related_searches:
            st.markdown(f"""
            <div class="result-item">
                <div class="result-title">{search}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_tavily_results(results):
    """Display Tavily AI search results"""
    # Check if results are available
    if not results:
        st.warning("No Tavily search results available. Please try a different query or check your API configuration.")
        return
        
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    # Display answer if available
    answer = results.get('answer', '')
    if answer:
        st.markdown('<div class="category-header">Answer</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-item">
            <div class="result-snippet">{answer}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display search results
    search_results = results.get('results', [])
    if search_results:
        st.markdown('<div class="category-header">Search Results</div>', unsafe_allow_html=True)
        
        for result in search_results:
            st.markdown(f"""
            <div class="result-item">
                <div class="result-title">{result.get('title', 'No Title')}</div>
                <div class="result-url">{result.get('url', '#')}</div>
                <div class="result-snippet">{result.get('content', 'No content available.')}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No search results found.")
    
    # Display follow-up questions if available
    follow_up_questions = results.get('follow_up_questions', [])
    if follow_up_questions:
        st.markdown('<div class="category-header">Follow-up Questions</div>', unsafe_allow_html=True)
        
        for question in follow_up_questions:
            st.markdown(f"""
            <div class="result-item">
                <div class="result-title">{question}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_metaphor_results(results):
    """Display Metaphor Neural Search results"""
    # Check if results are available
    if not results:
        st.warning("No Metaphor search results available. Please try a different query or check your API configuration.")
        return
        
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    # Display search results
    st.markdown('<div class="category-header">Similar Content</div>', unsafe_allow_html=True)
    
    # Display actual results
    documents = results.get('documents', [])
    if documents:
        for doc in documents:
            title = doc.get('title', 'No Title')
            url = doc.get('url', '#')
            extract = doc.get('extract', 'No content available.')
            
            st.markdown(f"""
            <div class="result-item">
                <div class="result-title">{title}</div>
                <div class="result-url">{url}</div>
                <div class="result-snippet">{extract}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No similar content found.")
    
    # Display summary if available
    summary = results.get('summary', '')
    if summary:
        st.markdown('<div class="category-header">Content Summary</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-item">
            <div class="result-snippet">{summary}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_google_trends_results(results):
    """Display Google Trends results"""
    # Check if results are available
    if not results:
        st.warning("No Google Trends results available. Please try a different query or check your API configuration.")
        return
        
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    # Display interest over time chart if available
    interest_over_time = results.get('interest_over_time')
    if interest_over_time is not None and not interest_over_time.empty:
        st.markdown('<div class="category-header">Interest Over Time</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Search Interest Over Time</div>', unsafe_allow_html=True)
        
        # Convert to DataFrame if it's not already
        if not isinstance(interest_over_time, pd.DataFrame):
            interest_over_time = pd.DataFrame(interest_over_time)
        
        # Prepare data for visualization
        if 'date' in interest_over_time.columns:
            # Melt the DataFrame to get it in the right format for plotting
            terms = [col for col in interest_over_time.columns if col != 'date']
            df = interest_over_time.melt('date', value_vars=terms, var_name='Term', value_name='Interest')
            
            # Create and display the chart
            fig = px.line(df, x='date', y='Interest', color='Term', title='Search Interest Over Time')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Interest over time data is not in the expected format.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display related queries if available
    related_queries = results.get('related_queries', {})
    if related_queries:
        st.markdown('<div class="category-header">Related Queries</div>', unsafe_allow_html=True)
        
        # Display top related queries
        for term, queries in related_queries.items():
            if 'top' in queries:
                st.markdown(f'<div class="subcategory-header">Top queries for "{term}"</div>', unsafe_allow_html=True)
                for query in queries['top'].get('query', []):
                    st.markdown(f"""
                    <div class="result-item">
                        <div class="result-title">{query}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            if 'rising' in queries:
                st.markdown(f'<div class="subcategory-header">Rising queries for "{term}"</div>', unsafe_allow_html=True)
                for query in queries['rising'].get('query', []):
                    st.markdown(f"""
                    <div class="result-item">
                        <div class="result-title">{query}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Display related topics if available
    related_topics = results.get('related_topics', {})
    if related_topics:
        st.markdown('<div class="category-header">Related Topics</div>', unsafe_allow_html=True)
        
        # Display top related topics
        for term, topics in related_topics.items():
            if 'top' in topics:
                st.markdown(f'<div class="subcategory-header">Top topics for "{term}"</div>', unsafe_allow_html=True)
                for topic in topics['top'].get('topic', []):
                    st.markdown(f"""
                    <div class="result-item">
                        <div class="result-title">{topic}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_crawler_results(results):
    """Display Web Crawler results"""
    # Check if results are available
    if not results:
        st.warning("No web crawler results available. Please try a different URL or check your API configuration.")
        return
        
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    # Display crawled pages
    st.markdown('<div class="category-header">Crawled Pages</div>', unsafe_allow_html=True)
    
    # Handle different result formats
    if isinstance(results, dict):
        # Single page result
        page_data = results
        st.markdown(f"""
        <div class="result-item">
            <div class="result-title">{page_data.get('title', 'No Title')}</div>
            <div class="result-url">{page_data.get('url', '#')}</div>
            <div class="result-snippet">
                <b>Title:</b> {page_data.get('title', 'No Title')}<br>
                <b>Description:</b> {page_data.get('description', 'No description available.')}<br>
                <b>Word Count:</b> {page_data.get('word_count', 'Unknown')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display content sections if available
        content = page_data.get('content', [])
        if content:
            st.markdown('<div class="category-header">Page Content</div>', unsafe_allow_html=True)
            for section in content:
                if isinstance(section, dict):
                    section_type = section.get('type', '')
                    section_content = section.get('content', '')
                    if section_type and section_content:
                        st.markdown(f"""
                        <div class="result-item">
                            <div class="result-title">{section_type}</div>
                            <div class="result-snippet">{section_content}</div>
                        </div>
                        """, unsafe_allow_html=True)
    
    elif isinstance(results, list):
        # Multiple pages result
        for page_data in results:
            if isinstance(page_data, dict):
                st.markdown(f"""
                <div class="result-item">
                    <div class="result-title">{page_data.get('title', 'No Title')}</div>
                    <div class="result-url">{page_data.get('url', '#')}</div>
                    <div class="result-snippet">
                        <b>Title:</b> {page_data.get('title', 'No Title')}<br>
                        <b>Description:</b> {page_data.get('description', 'No description available.')}<br>
                        <b>Word Count:</b> {page_data.get('word_count', 'Unknown')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Display content structure
    st.markdown('<div class="category-header">Content Structure</div>', unsafe_allow_html=True)
    
    # Placeholder data for chart
    labels = ['Blog Posts', 'Product Pages', 'Category Pages', 'About Pages', 'Contact Pages']
    values = [38, 27, 18, 10, 7]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text='Content Type Distribution')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_analyzer_results(results):
    """Display Website Analyzer results"""
    # This is a placeholder function that will be implemented when integrated with actual modules
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    # Display content quality metrics
    st.markdown('<div class="category-header">Content Quality Metrics</div>', unsafe_allow_html=True)
    
    # Placeholder data for chart
    categories = ['Readability', 'Engagement', 'Relevance', 'Uniqueness', 'Comprehensiveness']
    values = [4.2, 3.8, 4.5, 3.9, 4.1]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Content Quality'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Display SEO recommendations
    st.markdown('<div class="category-header">SEO Recommendations</div>', unsafe_allow_html=True)
    
    # Placeholder data
    recommendations = [
        "Improve meta descriptions for better click-through rates",
        "Add more internal links to related content",
        "Optimize images with descriptive alt text",
        "Improve page loading speed by optimizing images",
        "Add structured data markup for better search visibility"
    ]
    
    for recommendation in recommendations:
        st.markdown(f"""
        <div class="result-item">
            <div class="result-title">{recommendation}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)