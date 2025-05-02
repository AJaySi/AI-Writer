import streamlit as st
from lib.ai_web_researcher.metaphor_basic_neural_web_search import metaphor_find_similar
from datetime import datetime, timedelta
import re
import urllib.parse
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler if it doesn't exist
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

def is_valid_url(url):
    """
    Check if the provided string is a valid URL.
    
    Args:
        url (str): The URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        result = urllib.parse.urlparse(url)
        is_valid = all([result.scheme, result.netloc])
        logger.debug(f"URL validation for {url}: {is_valid}")
        return is_valid
    except Exception as e:
        logger.error(f"URL validation error for {url}: {str(e)}")
        return False

def competitor_analysis():
    logger.info("Starting competitor analysis")
    
    # Initialize session state for progress bar visibility
    if 'show_progress' not in st.session_state:
        st.session_state.show_progress = True
        logger.debug("Initialized show_progress session state")
        
    st.title("Competitor Analysis")
    st.markdown("""**Use Cases:**
        - Know similar companies and alternatives for the given URL.
        - Write listicles, similar companies, Top tools, alternative-to, similar products, similar websites, etc.
        [Read More Here](https://docs.exa.ai/reference/company-analyst)
    """)

    # URL input with validation
    similar_url = st.text_input(
        "👋 Enter a single valid URL for web analysis:",
        placeholder="https://example.com",
        help="Enter a complete URL including http:// or https://"
    )
    
    # Validate URL
    url_valid = is_valid_url(similar_url) if similar_url else False
    if similar_url and not url_valid:
        logger.warning(f"Invalid URL provided: {similar_url}")
        st.error("⚠️ Please enter a valid URL including http:// or https://")
    
    # Usecase selection with improved help
    usecase = st.selectbox(
        "Select Usecase", 
        ["similar companies", "listicles", "Top tools", "alternative-to", "similar products", "similar websites"],
        help="Choose the type of analysis you want to perform"
    )
    logger.debug(f"Selected usecase: {usecase}")
    
    # Default summary query based on usecase
    default_summary_queries = {
        "similar companies": "Find companies similar to this one, focusing on their business model, target audience, and market position",
        "listicles": "Find similar listicle articles about this topic, focusing on the structure and content",
        "Top tools": "Find top tools similar to this one, focusing on features, pricing, and user reviews",
        "alternative-to": "Find alternatives to this product or service, focusing on comparable features and pricing",
        "similar products": "Find products similar to this one, focusing on features, specifications, and use cases",
        "similar websites": "Find websites similar to this one, focusing on design, content, and functionality"
    }
    
    # Advanced options using a modal dialog
    show_advanced = st.checkbox("Show Advanced Options", help="Configure additional search parameters")
    logger.debug(f"Advanced options shown: {show_advanced}")
    
    # Initialize default values
    num_results = 5
    time_range = "Anytime"
    include_domains = []
    exclude_domains = []
    include_text = None
    exclude_text = None
    summary_query = default_summary_queries.get(usecase, "")
    
    # Add custom CSS for card styling
    st.markdown("""
    <style>
    .card {
        background: linear-gradient(to right, #f0f8ff, #e6f3ff);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border-left: 4px solid #4a90e2;
    }
    .card-title {
        color: #2c5282;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Advanced options section
    if show_advanced:
        logger.debug("Processing advanced options")
        st.markdown("### 🔧 Advanced Search Options")
        
        # Summary query with improved help in a card
        st.markdown('<div class="card"><div class="card-title">📝 Summary Query</div></div>', unsafe_allow_html=True)
        summary_query = st.text_area(
            "Customize the summary query", 
            value=summary_query,
            placeholder="Enter a custom query for summarization based on your usecase",
            help="This query will be used to generate summaries of the similar content. Be specific about what you want to know."
        )
        
        # Number of results with improved help in a card
        st.markdown('<div class="card"><div class="card-title">🔢 Number of Results</div></div>', unsafe_allow_html=True)
        num_results = st.slider(
            "How many results would you like?", 
            min_value=1, 
            max_value=20, 
            value=5, 
            step=1,
            help="How many similar results would you like to see?"
        )
        
        # Progress bar visibility toggle
        st.markdown('<div class="card"><div class="card-title">🔄 Progress Display</div></div>', unsafe_allow_html=True)
        st.session_state.show_progress = st.toggle(
            "Show detailed progress bars",
            value=st.session_state.show_progress,
            help="Toggle to show or hide detailed progress bars during analysis"
        )
        
        # Time range selection with improved styling in a card
        st.markdown('<div class="card"><div class="card-title">⏱️ Time Range</div></div>', unsafe_allow_html=True)
        time_range = st.radio(
            "Select time range for results",
            options=["Past Week", "Past Month", "Past Year", "Anytime"],
            index=3,
            horizontal=True,
            help="Filter results by when they were published"
        )
        
        # Domain filters with improved styling in a card
        st.markdown('<div class="card"><div class="card-title">🌐 Domain Filters</div></div>', unsafe_allow_html=True)
        domain_filter_type = st.radio(
            "Domain Filter Type",
            options=["Include Domains", "Exclude Domains", "None"],
            index=2,
            horizontal=True,
            help="Include or exclude specific domains from search results"
        )
        
        if domain_filter_type == "Include Domains":
            include_domains_input = st.text_input(
                "Include Domains (comma-separated)",
                placeholder="example.com, another-example.com",
                help="Only results from these domains will be included. Example: arxiv.org, paperswithcode.com"
            )
            if include_domains_input:
                include_domains = [domain.strip() for domain in include_domains_input.split(",")]
        
        elif domain_filter_type == "Exclude Domains":
            exclude_domains_input = st.text_input(
                "Exclude Domains (comma-separated)",
                placeholder="example.com, another-example.com",
                help="Results from these domains will be excluded from search results"
            )
            if exclude_domains_input:
                exclude_domains = [domain.strip() for domain in exclude_domains_input.split(",")]
        
        # Text filters with improved styling in a card
        st.markdown('<div class="card"><div class="card-title">📝 Text Filters</div></div>', unsafe_allow_html=True)
        text_filter_type = st.radio(
            "Text Filter Type",
            options=["Include Text", "Exclude Text", "None"],
            index=2,
            horizontal=True,
            help="Include or exclude results containing specific text"
        )
        
        if text_filter_type == "Include Text":
            include_text = st.text_input(
                "Include Text",
                placeholder="large language model",
                help="Only results containing this phrase will be included (up to 5 words)"
            )
        
        elif text_filter_type == "Exclude Text":
            exclude_text = st.text_input(
                "Exclude Text",
                placeholder="course",
                help="Results containing this phrase will be excluded (up to 5 words)"
            )
    
    # Analyze button with validation
    if st.button("Analyze", disabled=not url_valid if similar_url else False):
        if similar_url and url_valid:
            try:
                logger.info(f"Starting analysis for URL: {similar_url}")
                logger.debug(f"Analysis parameters - Usecase: {usecase}, Num Results: {num_results}, Time Range: {time_range}")
                
                # Create a progress container
                progress_container = st.empty()
                status_container = st.empty()
                results_container = st.empty()
                
                # Display initial status
                status_container.info(f"Starting analysis for the URL: {similar_url}")
                
                # Create a progress bar
                progress_bar = progress_container.progress(0.1)
                logger.debug("Initialized progress bar and status containers")
                
                # Calculate date range based on selection
                start_date = None
                end_date = None
                
                if time_range != "Anytime":
                    end_date = datetime.now()
                    if time_range == "Past Week":
                        start_date = end_date - timedelta(days=7)
                    elif time_range == "Past Month":
                        start_date = end_date - timedelta(days=30)
                    elif time_range == "Past Year":
                        start_date = end_date - timedelta(days=365)
                    logger.debug(f"Date range: {start_date} to {end_date}")
                
                # Format dates for API if they exist
                start_published_date = start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z") if start_date else None
                end_published_date = end_date.strftime("%Y-%m-%dT%H:%M:%S.999Z") if end_date else None
                
                # Prepare summary query
                summary_query_param = None
                if summary_query:
                    summary_query_param = {"query": summary_query}
                    logger.debug(f"Summary query: {summary_query}")
                
                # Update progress
                progress_bar.progress(0.2)
                status_container.info("Searching for similar content...")
                logger.info("Initiating similar content search")
                
                # Call the metaphor_find_similar function with all parameters
                with st.spinner("Performing competitor analysis..."):
                    logger.debug("Calling metaphor_find_similar API")
                    try:
                        df, search_response = metaphor_find_similar(
                            similar_url=similar_url,
                            usecase=usecase,
                            num_results=num_results,
                            start_published_date=start_published_date,
                            end_published_date=end_published_date,
                            include_domains=include_domains,
                            exclude_domains=exclude_domains,
                            include_text=include_text,
                            exclude_text=exclude_text,
                            summary_query=summary_query_param
                        )
                        logger.info(f"API call successful. Found {len(df) if not df.empty else 0} results")
                        
                        # Update progress
                        progress_bar.progress(0.7)
                        status_container.info("Processing and analyzing results...")
                        logger.debug("Processing search results")
                        
                        # Update progress to complete
                        progress_bar.progress(1.0)
                        status_container.success("Analysis completed successfully!")
                        logger.info("Analysis completed successfully")
                        
                    except Exception as api_error:
                        logger.error(f"API call failed: {str(api_error)}", exc_info=True)
                        raise
                
                # Display results
                if not df.empty:
                    logger.debug(f"Displaying {len(df)} results")
                    st.subheader("📊 Competitor Analysis Results")
                    
                    # Add a download button for the results
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"competitor_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                    )
                    
                    # Display the data editor
                    st.data_editor(
                        df,
                        column_config={
                            "Title": st.column_config.TextColumn(
                                "Title",
                                help="Title of the similar content",
                                width="large",
                            ),
                            "URL": st.column_config.LinkColumn(
                                "URL",
                                help="Link to the similar content",
                                width="medium",
                                display_text="Visit Website",
                            ),
                            "Content Summary": st.column_config.TextColumn(
                                "Content Summary",
                                help="Summary of the similar content",
                                width="large",
                            ),
                        },
                        hide_index=True,
                        use_container_width=True,
                    )
                    
                    # Display additional insights
                    st.subheader("🔍 Analysis Insights")
                    
                    # Create columns for metrics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Results", len(df))
                    
                    with col2:
                        # Calculate average content length
                        avg_content_length = df["Content Summary"].str.len().mean()
                        st.metric("Avg. Content Length", f"{avg_content_length:.0f} chars")
                    
                    with col3:
                        # Calculate unique domains
                        unique_domains = len(set([url.split('/')[2] for url in df["URL"]]))
                        st.metric("Unique Domains", unique_domains)
                    
                    # Display full summaries in expanders
                    st.subheader("📝 Detailed Competitor Summaries")
                    
                    if 'competitor_summaries' in st.session_state and st.session_state.competitor_summaries:
                        for url, data in st.session_state.competitor_summaries.items():
                            with st.expander(f"📊 {data['title']}", expanded=False):
                                st.markdown("### 📝 Detailed Competitor Analysis")
                                st.markdown(data['summary'])
                    
                    # Display raw data in an expander
                    with st.expander("View Raw Data"):
                        st.json(search_response)
                else:
                    logger.warning("No results found for the given URL and parameters")
                    st.warning("No results found for the given URL and parameters.")
                    
            except Exception as err:
                logger.error(f"Analysis failed: {str(err)}", exc_info=True)
                st.error(f"✖ 🚫 Failed to do similar search.\nError: {err}")
        else:
            logger.warning("Analysis attempted without valid URL")
            st.error("Please enter a valid URL.")