import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import utils module
from utils import (
    load_css,
    display_google_serp_results,
    display_tavily_results,
    display_metaphor_results,
    display_google_trends_results,
    display_crawler_results,
    display_analyzer_results
)

# Configure Streamlit page settings
st.set_page_config(
    page_title="AI Web Researcher Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS immediately
st.markdown("""
<style>
.main-header {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
}
.category-header {
    font-size: 20px;
    font-weight: bold;
    margin: 15px 0;
    color: #0066cc;
}
/* Make the dashboard responsive */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
    white-space: pre-wrap;
    min-width: fit-content;
    font-size: 14px;
    padding: 8px 16px;
}
/* Adjust container width */
.block-container {
    max-width: 95% !important;
    padding: 1rem 1rem 10rem !important;
}
/* Additional styling for better visibility */
.stApp {
    background-color: #f8f9fa;
}
.stTabs [data-baseweb="tab"] [data-testid="stMarkdownContainer"] p {
    font-size: 14px !important;
    margin-bottom: 0px !important;
}
.stTabs [data-baseweb="tab-list"] button {
    background-color: #ffffff;
    border: 1px solid #e9ecef;
    border-radius: 4px;
    margin: 2px;
}
.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    background-color: #e7f1ff;
    border-color: #b8daff;
}
</style>
""", unsafe_allow_html=True)

# CSS is now loaded at the top of the file

# Initialize session state variables
def init_session_state():
    if 'current_section' not in st.session_state:
        st.session_state['current_section'] = 'Dashboard Home'

# Initialize session state at startup
init_session_state()

def main():
    # Initialize session state before accessing it
    init_session_state()
    
    # Main navigation header
    st.markdown('<div class="main-nav-header">AI Web Researcher</div>', unsafe_allow_html=True)
    
    # Create tabs for navigation
    selected_section = st.tabs([
        "🏠 Dashboard Home",
        "🔍 Search Tools",
        "🧠 Neural Search",
        "📈 Trend Analysis",
        "🕸️ Web Crawling",
        "📚 Academic Research",
        "📋 Research Workflows"
    ])
    
    # Display appropriate section based on selected tab
    with selected_section[0]:
        display_home()
    with selected_section[1]:
        display_search_tools()
    with selected_section[2]:
        display_neural_search()
    with selected_section[3]:
        display_trend_analysis()
    with selected_section[4]:
        display_web_crawling()
    with selected_section[5]:
        display_academic_research()
    with selected_section[6]:
        display_research_workflows()
    
    # Ensure CSS is consistently applied
    load_css()

def display_home():
    
    # Main header with improved styling
    st.markdown('<div class="main-header">AI Web Researcher Dashboard</div>', unsafe_allow_html=True)
    
    # Introduction with better formatting
    st.markdown("""
    <div class="intro-container">
        <p class="intro-text">Welcome to the <span class="intro-highlight">AI Web Researcher Dashboard</span>, a comprehensive suite of research tools designed 
        specifically for content creators and digital marketing professionals. This dashboard integrates 
        various web research modules to streamline your content research process, enhance content quality, 
        and improve workflow efficiency.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick access to tool categories with improved header
    st.markdown('<div class="category-header">Research Tool Categories</div>', unsafe_allow_html=True)
    
    # Use 2 columns with equal width for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-title">🔍 Search Engine Research</div>
            <div class="tool-description">Powerful search tools to understand search intent, identify content gaps, and discover high-performing content in your niche</div>
            <div class="tool-features"><b>Includes:</b> Google SERP Search • Tavily AI Search</div>
            <div class="tool-features"><b>Use cases:</b> Keyword research, competitor analysis, content planning, identifying user questions</div>
            <div style="margin-top: 12px;">
                <span class="tool-badge">SERP Analysis</span>
                <span class="tool-badge ai-powered">AI-Powered</span>
            </div>
        </div>
        
        <div class="tool-card">
            <div class="tool-title">🧠 Neural Search</div>
            <div class="tool-description">Advanced semantic search technology that understands concepts rather than just keywords to find truly relevant content</div>
            <div class="tool-features"><b>Includes:</b> Metaphor Neural Search</div>
            <div class="tool-features"><b>Use cases:</b> Finding conceptually similar articles, discovering unique content angles, competitive research</div>
            <div style="margin-top: 12px;">
                <span class="tool-badge semantic">Semantic</span>
                <span class="tool-badge deep-learning">Deep Learning</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-title">📈 Trend Analysis</div>
            <div class="tool-description">Comprehensive trend analysis tools that track search term popularity over time to identify seasonal patterns and emerging topics</div>
            <div class="tool-features"><b>Includes:</b> Google Trends Researcher</div>
            <div class="tool-features"><b>Use cases:</b> Seasonal content planning, topic validation, identifying rising trends, content calendar optimization</div>
            <div style="margin-top: 12px;">
                <span class="tool-badge time-series">Time Series</span>
                <span class="tool-badge forecasting">Forecasting</span>
            </div>
        </div>
        
        <div class="tool-card">
            <div class="tool-title">🕸️ Web Crawling & Analysis</div>
            <div class="tool-description">Powerful web extraction tools that gather and structure content from websites for in-depth analysis and insights</div>
            <div class="tool-features"><b>Includes:</b> Async Web Crawler • Firecrawl Web Crawler • Website Analyzer</div>
            <div class="tool-features"><b>Use cases:</b> Content auditing, competitor analysis, data extraction, market research, content aggregation</div>
            <div style="margin-top: 12px;">
                <span class="tool-badge content-extraction">Content Extraction</span>
                <span class="tool-badge data-analysis">Data Analysis</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Featured workflow with improved header
    st.markdown('<div class="category-header">Featured Research Workflow</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="workflow-card">
        <div class="workflow-title">Comprehensive Topic Research Workflow</div>
        <p style="color: #4b5563; margin-bottom: 1.25rem;">Follow this proven research workflow to develop comprehensive, data-driven content that resonates with your audience and performs well in search.</p>
        <div class="workflow-step-container">
            <div class="workflow-step-number">1</div>
            <div class="workflow-step-content">
                <div class="step-title">Initial Exploration</div>
                <div class="workflow-step-description">Use Google SERP Search to understand the search landscape, identify user intent, and discover what content currently ranks well. Analyze People Also Ask questions to identify key user concerns.</div>
            </div>
        </div>
        <div class="workflow-step-container">
            <div class="workflow-step-number">2</div>
            <div class="workflow-step-content">
                <div class="step-title">In-depth Research</div>
                <div class="workflow-step-description">Use Tavily AI Search for deeper research on identified subtopics. The AI-powered search provides more contextual information and helps uncover expert insights that might be missed in traditional searches.</div>
            </div>
        </div>
        <div class="workflow-step-container">
            <div class="workflow-step-number">3</div>
            <div class="workflow-step-content">
                <div class="step-title">Competitive Analysis</div>
                <div class="workflow-step-description">Use Metaphor Neural Search to find conceptually similar content from competitors. Analyze their approach, identify content gaps, and discover unique angles that differentiate your content.</div>
            </div>
        </div>
        <div class="workflow-step-container">
            <div class="workflow-step-number">4</div>
            <div class="workflow-step-content">
                <div class="step-title">Trend Validation</div>
                <div class="workflow-step-description">Use Google Trends Researcher to verify topic popularity, identify seasonal patterns, and discover related trending topics. This ensures your content is timely and aligned with current audience interests.</div>
            </div>
        </div>
        <div class="workflow-step-container">
            <div class="workflow-step-number">5</div>
            <div class="workflow-step-content">
                <div class="step-title">Content Extraction</div>
                <div class="workflow-step-description">Use Web Crawling tools to extract specific content from top-performing pages for detailed analysis. This helps identify content structure, depth, and formatting approaches that resonate with your audience.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_search_tools():
    
    st.markdown('<div class="main-header">Search Engine Research Tools</div>', unsafe_allow_html=True)
    
    # Google SERP Search
    st.markdown('<div class="category-header">Google SERP Search</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">Google SERP Search</div>
        <div class="tool-description">Retrieves organic search results, People Also Ask questions, and related searches</div>
        <div class="tool-features">
            <b>Best for:</b> Initial topic research, understanding search intent, and identifying content gaps<br>
            <b>Key features:</b> Comprehensive search results with structured data extraction
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input form for Google SERP Search
    with st.form("google_serp_search_form"):
        search_query = st.text_input("Enter your search query")
        col1, col2 = st.columns(2)
        with col1:
            num_results = st.slider("Number of results", 5, 30, 10)
        with col2:
            include_paa = st.checkbox("Include People Also Ask", value=True)
        
        submitted = st.form_submit_button("Search")
        if submitted and search_query:
            try:
                with st.spinner("Searching Google SERP..."):
                    # Import the actual module
                    from ai_web_researcher.google_serp_search import google_search
                    
                    # Call the actual implementation
                    results = google_search(search_query)
                    
                    # Display the results
                    if results:
                        display_google_serp_results(results)
                    else:
                        st.error("No results found. Please try a different query.")
            except Exception as e:
                st.error(f"Error performing Google SERP search: {str(e)}")
                st.info("Please check your API configuration in the .env file.")
                st.info("Required API: SERPER_API_KEY for Google SERP Search")
                display_google_serp_results(None)
    
    # Tavily AI Search
    st.markdown('<div class="category-header">Tavily AI Search</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">Tavily AI Search</div>
        <div class="tool-description">Advanced AI-powered search with semantic understanding</div>
        <div class="tool-features">
            <b>Best for:</b> In-depth research requiring contextual understanding<br>
            <b>Key features:</b> Provides direct answers to questions and follow-up question suggestions
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input form for Tavily AI Search
    with st.form("tavily_ai_search_form"):
        search_query = st.text_input("Enter your search query or question")
        search_depth = st.select_slider("Search depth", options=["basic", "medium", "deep"], value="medium")
        
        submitted = st.form_submit_button("Search with Tavily AI")
        if submitted and search_query:
            try:
                with st.spinner("Searching with Tavily AI..."):
                    # Import the actual module
                    from ai_web_researcher.tavily_ai_search import do_tavily_ai_search
                    
                    # Call the actual implementation
                    results = do_tavily_ai_search(search_query, search_depth=search_depth)
                    
                    # Display the results
                    if results:
                        display_tavily_results(results)
                    else:
                        st.error("No results found. Please try a different query.")
            except Exception as e:
                st.error(f"Error performing Tavily AI search: {str(e)}")
                st.info("Please check your API configuration in the .env file.")
                st.info("Required API: TAVILY_API_KEY for Tavily AI Search")
                display_tavily_results(None)

def display_neural_search():
    
    st.markdown('<div class="main-header">Neural Search Tools</div>', unsafe_allow_html=True)
    
    # Metaphor Neural Search
    st.markdown('<div class="category-header">Metaphor Neural Search</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">Metaphor Neural Search</div>
        <div class="tool-description">Semantic search technology for finding related content</div>
        <div class="tool-features">
            <b>Best for:</b> Discovering content based on conceptual similarity rather than keyword matching<br>
            <b>Key features:</b> Find similar articles, competitor analysis, and content inspiration
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input form for Metaphor Neural Search
    with st.form("metaphor_search_form"):
        st.markdown("**Search by keyword or find similar content to a URL**")
        search_type = st.radio("Search type", ["Keyword Search", "Similar Content Search"])
        
        if search_type == "Keyword Search":
            search_query = st.text_input("Enter your search query")
            url_input = ""
        else:
            search_query = ""
            url_input = st.text_input("Enter a URL to find similar content")
        
        num_results = st.slider("Number of results", 3, 20, 5)
        
        submitted = st.form_submit_button("Search with Metaphor")
        if submitted and (search_query or url_input):
            try:
                with st.spinner("Searching with Metaphor Neural Search..."):
                    # Import the actual module
                    from ai_web_researcher.metaphor_basic_neural_web_search import metaphor_search_articles, metaphor_find_similar
                    
                    # Call the actual implementation
                    if search_query:
                        results = metaphor_search_articles(search_query, num_results=num_results)
                    else:
                        results = metaphor_find_similar(url_input, num_results=num_results)
                    
                    # Display the results
                    if results:
                        display_metaphor_results(results)
                    else:
                        st.error("No results found. Please try a different query.")
            except Exception as e:
                st.error(f"Error performing Metaphor Neural search: {str(e)}")
                st.info("Please check your API configuration in the .env file.")
                st.info("Required API: METAPHOR_API_KEY for Metaphor Neural Search")
                display_metaphor_results(None)

def display_trend_analysis():
    
    st.markdown('<div class="main-header">Trend Analysis Tools</div>', unsafe_allow_html=True)
    
    # Google Trends Researcher
    st.markdown('<div class="category-header">Google Trends Researcher</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">Google Trends Researcher</div>
        <div class="tool-description">Analyze search term popularity and related queries</div>
        <div class="tool-features">
            <b>Best for:</b> Content planning, trend forecasting, and seasonal content optimization<br>
            <b>Key features:</b> Interest over time charts, related queries, and regional interest data
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input form for Google Trends Researcher
    with st.form("google_trends_form"):
        search_terms = st.text_area("Enter search terms (one per line)")
        col1, col2 = st.columns(2)
        with col1:
            time_frame = st.select_slider("Time range", options=["past_hour", "past_day", "past_week", "past_month", "past_90_days", "past_12_months", "past_5_years"], value="past_12_months")
        with col2:
            geo = st.text_input("Geographic region (ISO country code, e.g., 'US')", value="US")
        
        submitted = st.form_submit_button("Analyze Trends")
        if submitted and search_terms:
            try:
                with st.spinner("Analyzing Google Trends..."):
                    # Import the actual module
                    from ai_web_researcher.google_trends_researcher import do_google_trends_analysis
                    
                    # Call the actual implementation
                    search_terms_list = [term.strip() for term in search_terms.split('\n') if term.strip()]
                    results = do_google_trends_analysis(search_terms_list, time_frame=time_frame, geo=geo)
                    
                    # Display the results
                    if results:
                        display_google_trends_results(results)
                    else:
                        st.error("No trend data found. Please try different search terms.")
            except Exception as e:
                st.error(f"Error analyzing Google Trends: {str(e)}")
                st.info("Google Trends analysis doesn't require an API key, but there might be rate limiting or network issues.")
                display_google_trends_results(None)

def display_web_crawling():
    
    st.markdown('<div class="main-header">Web Crawling & Analysis Tools</div>', unsafe_allow_html=True)
    
    # Create tabs for different crawling tools
    tab1, tab2, tab3 = st.tabs(["Firecrawl Web Crawler", "Website Analyzer", "Async Web Crawler"])
    
    with tab1:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-title">Firecrawl Web Crawler</div>
            <div class="tool-description">Extract structured content from websites</div>
            <div class="tool-features">
                <b>Best for:</b> Content extraction, competitor analysis, and website auditing<br>
                <b>Key features:</b> Extracts titles, descriptions, headings, and content from web pages
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Input form for Firecrawl Web Crawler
        with st.form("firecrawl_form"):
            website_url = st.text_input("Enter website URL")
            depth = st.slider("Crawl depth", 1, 5, 1)
            max_pages = st.slider("Maximum pages", 1, 50, 10)
            
            submitted = st.form_submit_button("Crawl Website")
            if submitted and website_url:
                try:
                    with st.spinner("Crawling website..."):
                        # Import the actual module
                        from ai_web_researcher.firecrawl_web_crawler import scrape_website
                        
                        # Call the actual implementation
                        results = scrape_website(website_url, depth=depth, max_pages=max_pages)
                        
                        # Display the results
                        if results:
                            display_crawler_results(results)
                        else:
                            st.error("No crawler results found. Please try a different URL.")
                except Exception as e:
                    st.error(f"Error crawling website: {str(e)}")
                    st.info("Please check your API configuration in the .env file.")
                    st.info("Required API: FIRECRAWL_API_KEY for Web Crawler")
                    display_crawler_results(None)
    
    with tab2:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-title">Website Analyzer</div>
            <div class="tool-description">Analyze website content and structure</div>
            <div class="tool-features">
                <b>Best for:</b> Content analysis, SEO auditing, and competitor research<br>
                <b>Key features:</b> Content analysis, keyword extraction, and readability metrics
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Input form for Website Analyzer
        with st.form("website_analyzer_form"):
            website_url = st.text_input("Enter website URL")
            analyze_type = st.selectbox("Analysis type", ["Basic Analysis", "SEO Analysis", "Content Analysis", "Competitor Analysis"])
            
            submitted = st.form_submit_button("Analyze Website")
            if submitted and website_url:
                st.info("Website Analyzer is coming soon. This feature is under development.")
    
    with tab3:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-title">Async Web Crawler</div>
            <div class="tool-description">High-performance asynchronous web crawler</div>
            <div class="tool-features">
                <b>Best for:</b> Large-scale crawling, data extraction, and content aggregation<br>
                <b>Key features:</b> Fast, efficient crawling with customizable extraction rules
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Input form for Async Web Crawler
        with st.form("async_crawler_form"):
            website_url = st.text_input("Enter website URL")
            max_urls = st.slider("Maximum URLs to crawl", 10, 100, 30)
            
            submitted = st.form_submit_button("Start Crawling")
            if submitted and website_url:
                st.info("Async Web Crawler is coming soon. This feature is under development.")

def display_academic_research():
    
    st.markdown('<div class="main-header">Academic Research Tools</div>', unsafe_allow_html=True)
    
    # ArXiv Search Section
    st.markdown('<div class="category-header">ArXiv Scholarly Search</div>', unsafe_allow_html=True)
    
    # Search Parameters
    search_col1, search_col2 = st.columns([2, 1])
    with search_col1:
        search_query = st.text_input("🔍 Enter research topic or keywords", key="arxiv_search")
    with search_col2:
        max_results = st.number_input("Maximum Results", min_value=1, max_value=50, value=10)
    
    # Search Button
    if st.button("🔎 Search ArXiv", key="arxiv_search_button"):
        if search_query:
            with st.spinner("Searching ArXiv database..."):
                try:
                    # Import arxiv search function
                    from ai_web_researcher.arxiv_schlorly_research import fetch_arxiv_data, create_dataframe
                    
                    # Fetch results
                    results = fetch_arxiv_data(search_query, max_results)
                    
                    if results:
                        # Create DataFrame
                        df = create_dataframe(results, ["Title", "Published Date", "ArXiv ID", "Summary", "PDF URL"])
                        
                        # Display results in an expander
                        with st.expander("📚 Search Results", expanded=True):
                            # Display each paper with options to view abstract and download
                            for idx, row in df.iterrows():
                                st.markdown(f"### {row['Title']}")
                                st.markdown(f"*Published: {row['Published Date']}*")
                                
                                # Create columns for buttons
                                btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
                                
                                with btn_col1:
                                    if st.button(f"📄 View Abstract #{idx}"):
                                        st.markdown(f"**Abstract:**\n{row['Summary']}")
                                
                                with btn_col2:
                                    st.markdown(f"[📥 Download PDF]({row['PDF URL']})")
                                    if st.button(f"📝 Summarize #{idx}"):
                                        with st.spinner("Generating summary..."):
                                            try:
                                                from ai_web_researcher.gpt_summarize_web_content import summarize_web_content
                                                summary = summarize_web_content(row['PDF URL'])
                                                if summary:
                                                    st.markdown("### GPT Summary")
                                                    st.markdown(summary)
                                                    # Add export option for the summary
                                                    st.download_button(
                                                        label="📥 Export Summary",
                                                        data=summary,
                                                        file_name=f"summary_{row['ArXiv ID']}.txt",
                                                        mime="text/plain"
                                                    )
                                            except Exception as e:
                                                st.error(f"Error generating summary: {str(e)}")
                                
                                with btn_col3:
                                    if st.button(f"🔍 Related Web Content #{idx}"):
                                        # Use Google SERP to find related content
                                        from ai_web_researcher.google_serp_search import google_search
                                        web_results = google_search(row['Title'])
                                        if web_results:
                                            st.markdown("### Related Web Content")
                                            for result in web_results['organic'][:3]:
                                                st.markdown(f"- [{result['title']}]({result['link']})\n  {result['snippet']}")
                                
                                st.markdown("---")
                    else:
                        st.warning("No results found. Try modifying your search terms.")
                except Exception as e:
                    st.error(f"An error occurred while searching: {str(e)}")
        else:
            st.warning("Please enter a search query.")
    
    # Research Notes Section
    st.markdown('<div class="category-header">Research Notes</div>', unsafe_allow_html=True)
    
    # Initialize session state for notes if not exists
    if 'research_notes' not in st.session_state:
        st.session_state.research_notes = {}
    
    notes_col1, notes_col2 = st.columns([2, 1])
    
    with notes_col1:
        paper_id = st.text_input("ArXiv ID or Paper Title", key="notes_paper_id")
        notes_content = st.text_area("Research Notes", height=200, key="notes_content")
        
        if st.button("Save Notes"):
            if paper_id:
                st.session_state.research_notes[paper_id] = notes_content
                st.success("Notes saved successfully!")
            else:
                st.warning("Please enter a paper identifier.")
    
    with notes_col2:
        st.markdown("### Saved Notes")
        for paper_id, notes in st.session_state.research_notes.items():
            with st.expander(f"📝 {paper_id}"):
                st.text_area("Saved Notes", value=notes, height=150, key=f"saved_{paper_id}", disabled=True)
                if st.button("Export Notes", key=f"export_{paper_id}"):
                    notes_export = f"Research Notes for {paper_id}\n\n{notes}"
                    st.download_button(
                        label="📥 Download Notes",
                        data=notes_export,
                        file_name=f"research_notes_{paper_id}.txt",
                        mime="text/plain"
                    )
    
    # Citation Management Section
    st.markdown('<div class="category-header">Citation Management</div>', unsafe_allow_html=True)
    
    # BibTeX Export
    st.markdown("### Export Citations")
    arxiv_id = st.text_input("Enter ArXiv ID for citation export")
    if arxiv_id and st.button("Generate BibTeX"):
        try:
            from ai_web_researcher.arxiv_schlorly_research import arxiv_bibtex
            bibtex = arxiv_bibtex(arxiv_id)
            if bibtex:
                st.code(bibtex, language="bibtex")
                st.download_button(
                    label="📥 Download BibTeX",
                    data=bibtex,
                    file_name=f"citation_{arxiv_id}.bib",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"Error generating citation: {str(e)}")

def display_research_workflows():
    
    st.markdown('<div class="main-header">Research Workflows</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="workflow-description">
        Research workflows combine multiple research tools to provide comprehensive insights for specific content creation tasks.
        Select a workflow to get started.
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different workflows
    tab1, tab2, tab3 = st.tabs(["Topic Research", "Competitor Analysis", "Trend Discovery"])
    
    with tab1:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-title">Comprehensive Topic Research</div>
            <div class="workflow-description">
                This workflow helps you thoroughly research a topic for content creation by combining search results, 
                semantic understanding, and trend analysis.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Input form for Topic Research workflow
        with st.form("topic_research_form"):
            topic = st.text_input("Enter your topic")
            include_trends = st.checkbox("Include trend analysis", value=True)
            include_competitors = st.checkbox("Include competitor analysis", value=True)
            
            submitted = st.form_submit_button("Start Research Workflow")
            if submitted and topic:
                st.info("Research workflows are coming soon. This feature is under development.")
    
    with tab2:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-title">Competitor Content Analysis</div>
            <div class="workflow-description">
                This workflow analyzes your competitors' content to identify gaps and opportunities for your own content strategy.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Input form for Competitor Analysis workflow
        with st.form("competitor_analysis_form"):
            competitor_urls = st.text_area("Enter competitor URLs (one per line)")
            topic_focus = st.text_input("Topic focus (optional)")
            
            submitted = st.form_submit_button("Start Competitor Analysis")
            if submitted and competitor_urls:
                st.info("Research workflows are coming soon. This feature is under development.")
    
    with tab3:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-title">Trend Discovery & Content Planning</div>
            <div class="workflow-description">
                This workflow identifies trending topics in your niche and helps you plan content around them.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Input form for Trend Discovery workflow
        with st.form("trend_discovery_form"):
            niche = st.text_input("Enter your niche or industry")
            time_period = st.select_slider("Time period", options=["past_week", "past_month", "past_90_days", "past_12_months"], value="past_month")
            
            submitted = st.form_submit_button("Discover Trends")
            if submitted and niche:
                st.info("Research workflows are coming soon. This feature is under development.")