import os
import time
import logging
import streamlit as st
from datetime import datetime

from lib.ai_web_researcher.gpt_online_researcher import gpt_web_researcher
from lib.utils.read_main_config_params import read_return_config_section

# Configure module-level logging
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

def reload_env_variables():
    """Reload environment variables from .env file."""
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
        return True
    except Exception as e:
        logger.error(f"Failed to reload environment variables: {str(e)}")
        return False

def save_api_key_to_env(key_name, key_value):
    """Save API key to .env file."""
    try:
        env_path = os.path.join(os.getcwd(), '.env')
        
        # Read existing .env content
        existing_content = {}
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        existing_content[key] = value
        
        # Update or add new key
        existing_content[key_name] = key_value
        
        # Write back to .env
        with open(env_path, 'w') as f:
            for key, value in existing_content.items():
                f.write(f"{key}={value}\n")
        
        # Update environment variable and reload all env vars
        os.environ[key_name] = key_value
        if reload_env_variables():
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to save API key to .env: {str(e)}")
        return False

def validate_api_keys():
    """Validate required API keys and return their status."""
    
    logger.info("Validating API keys")
    
    # Get API keys
    api_keys = {
        'SERPER_API_KEY': os.getenv('SERPER_API_KEY'),
        'METAPHOR_API_KEY': os.getenv('METAPHOR_API_KEY'),
        'TAVILY_API_KEY': os.getenv('TAVILY_API_KEY'),
        'FIRECRAWL_API_KEY': os.getenv('FIRECRAWL_API_KEY')
    }
    
    # Test SERPER_API_KEY validity
    if api_keys['SERPER_API_KEY']:
        try:
            # Make a test request
            import requests
            test_url = "https://google.serper.dev/search"
            headers = {
                'X-API-KEY': api_keys['SERPER_API_KEY'],
                'Content-Type': 'application/json'
            }
            test_payload = {"q": "test", "gl": "us", "hl": "en", "num": 1}
            
            response = requests.post(test_url, headers=headers, json=test_payload)
            api_keys['SERPER_API_KEY_VALID'] = response.status_code == 200
            
            if not api_keys['SERPER_API_KEY_VALID']:
                logger.error(f"SERPER_API_KEY validation failed: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error validating SERPER_API_KEY: {str(e)}")
            api_keys['SERPER_API_KEY_VALID'] = False
    else:
        api_keys['SERPER_API_KEY_VALID'] = False

    return api_keys

def do_web_research():
    """Main function to perform web research based on user input."""
    
    # Reset session state variables for this research operation
    if 'metaphor_results_displayed' in st.session_state:
        del st.session_state.metaphor_results_displayed
    
    logger.info("Starting do_web_research function")
    
    try:
        # Get API keys without validation
        api_keys = {
            'SERPER_API_KEY': os.getenv('SERPER_API_KEY'),
            'METAPHOR_API_KEY': os.getenv('METAPHOR_API_KEY'),
            'TAVILY_API_KEY': os.getenv('TAVILY_API_KEY'),
            'FIRECRAWL_API_KEY': os.getenv('FIRECRAWL_API_KEY')
        }
        
        if not api_keys['SERPER_API_KEY']:
            st.error("""
            🚫 SERPER_API_KEY is missing. Please configure your API key.
            """)
            with st.popover("⚙️ Configure API Keys"):
                st.markdown("""
                ### API Key Configuration
                Enter your API keys below to enable research features.
                """)
                
                # SERPER API Key
                serper_col1, serper_col2 = st.columns([3, 1])
                with serper_col1:
                    serper_key = st.text_input(
                        "Serper API Key",
                        type="password",
                        placeholder="Enter your Serper API key",
                        help="Get your key at https://serper.dev"
                    )
                    test_key = st.checkbox("Test API key before saving", value=False, help="Validate the API key before saving", key="test_serper_key")
                with serper_col2:
                    if st.button("Save Serper", use_container_width=True):
                        if serper_key:
                            if test_key:
                                # Test the API key
                                try:
                                    import requests
                                    test_url = "https://google.serper.dev/search"
                                    headers = {
                                        'X-API-KEY': serper_key,
                                        'Content-Type': 'application/json'
                                    }
                                    test_payload = {"q": "test", "gl": "us", "hl": "en", "num": 1}
                                    response = requests.post(test_url, headers=headers, json=test_payload)
                                    
                                    if response.status_code == 200:
                                        if save_api_key_to_env('SERPER_API_KEY', serper_key):
                                            st.success("✅ Serper API key validated and saved!")
                                            st.rerun()
                                        else:
                                            st.error("Failed to save API key")
                                    else:
                                        st.error(f"API key validation failed: {response.status_code} - {response.text}")
                                except Exception as e:
                                    st.error(f"Error validating API key: {str(e)}")
                            else:
                                # Skip validation and save directly
                                if save_api_key_to_env('SERPER_API_KEY', serper_key):
                                    st.success("✅ Serper API key saved!")
                                    time.sleep(0.5)  # Small delay to ensure the key is saved
                                    st.rerun()
                                else:
                                    st.error("Failed to save API key")
                
                # METAPHOR API Key
                if not api_keys.get('METAPHOR_API_KEY'):
                    metaphor_col1, metaphor_col2 = st.columns([3, 1])
                    with metaphor_col1:
                        metaphor_key = st.text_input(
                            "Metaphor API Key",
                            type="password",
                            placeholder="Enter your Metaphor API key",
                            help="Get your key at https://metaphor.systems"
                        )
                        test_metaphor = st.checkbox("Test API key before saving", value=False, help="Validate the API key before saving", key="test_metaphor_key")
                    with metaphor_col2:
                        if st.button("Save Metaphor", use_container_width=True):
                            if metaphor_key:
                                if test_metaphor:
                                    # Test the API key
                                    try:
                                        import requests
                                        test_url = "https://api.metaphor.systems/v1/search"
                                        headers = {
                                            'Authorization': f'Bearer {metaphor_key}',
                                            'Content-Type': 'application/json'
                                        }
                                        test_payload = {"query": "test", "numResults": 1}
                                        response = requests.post(test_url, headers=headers, json=test_payload)
                                        
                                        if response.status_code == 200:
                                            if save_api_key_to_env('METAPHOR_API_KEY', metaphor_key):
                                                st.success("✅ Metaphor API key validated and saved!")
                                                st.rerun()
                                            else:
                                                st.error("Failed to save API key")
                                        else:
                                            st.error(f"API key validation failed: {response.status_code} - {response.text}")
                                    except Exception as e:
                                        st.error(f"Error validating API key: {str(e)}")
                                else:
                                    # Skip validation and save directly
                                    if save_api_key_to_env('METAPHOR_API_KEY', metaphor_key):
                                        st.success("✅ Metaphor API key saved!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to save API key")
                
                # TAVILY API Key
                if not api_keys.get('TAVILY_API_KEY'):
                    tavily_col1, tavily_col2 = st.columns([3, 1])
                    with tavily_col1:
                        tavily_key = st.text_input(
                            "Tavily API Key",
                            type="password",
                            placeholder="Enter your Tavily API key",
                            help="Get your key at https://tavily.com"
                        )
                        test_tavily = st.checkbox("Test API key before saving", value=False, help="Validate the API key before saving", key="test_tavily_key")
                    with tavily_col2:
                        if st.button("Save Tavily", use_container_width=True):
                            if tavily_key:
                                if test_tavily:
                                    # Test the API key
                                    try:
                                        import requests
                                        test_url = "https://api.tavily.com/v1/search"
                                        headers = {
                                            'Authorization': f'Bearer {tavily_key}',
                                            'Content-Type': 'application/json'
                                        }
                                        test_payload = {"query": "test", "max_results": 1}
                                        response = requests.post(test_url, headers=headers, json=test_payload)
                                        
                                        if response.status_code == 200:
                                            if save_api_key_to_env('TAVILY_API_KEY', tavily_key):
                                                st.success("✅ Tavily API key validated and saved!")
                                                st.rerun()
                                            else:
                                                st.error("Failed to save API key")
                                        else:
                                            st.error(f"API key validation failed: {response.status_code} - {response.text}")
                                    except Exception as e:
                                        st.error(f"Error validating API key: {str(e)}")
                                else:
                                    # Skip validation and save directly
                                    if save_api_key_to_env('TAVILY_API_KEY', tavily_key):
                                        st.success("✅ Tavily API key saved!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to save API key")
                
                # FIRECRAWL API Key
                if not api_keys.get('FIRECRAWL_API_KEY'):
                    firecrawl_col1, firecrawl_col2 = st.columns([3, 1])
                    with firecrawl_col1:
                        firecrawl_key = st.text_input(
                            "Firecrawl API Key",
                            type="password",
                            placeholder="Enter your Firecrawl API key",
                            help="Get your key at https://firecrawl.co"
                        )
                        test_firecrawl = st.checkbox("Test API key before saving", value=False, help="Validate the API key before saving", key="test_firecrawl_key")
                    with firecrawl_col2:
                        if st.button("Save Firecrawl", use_container_width=True):
                            if firecrawl_key:
                                if test_firecrawl:
                                    # Test the API key
                                    try:
                                        import requests
                                        test_url = "https://api.firecrawl.co/v1/search"
                                        headers = {
                                            'Authorization': f'Bearer {firecrawl_key}',
                                            'Content-Type': 'application/json'
                                        }
                                        test_payload = {"query": "test", "limit": 1}
                                        response = requests.post(test_url, headers=headers, json=test_payload)
                                        
                                        if response.status_code == 200:
                                            if save_api_key_to_env('FIRECRAWL_API_KEY', firecrawl_key):
                                                st.success("✅ Firecrawl API key validated and saved!")
                                                st.rerun()
                                            else:
                                                st.error("Failed to save API key")
                                        else:
                                            st.error(f"API key validation failed: {response.status_code} - {response.text}")
                                    except Exception as e:
                                        st.error(f"Error validating API key: {str(e)}")
                                else:
                                    # Skip validation and save directly
                                    if save_api_key_to_env('FIRECRAWL_API_KEY', firecrawl_key):
                                        st.success("✅ Firecrawl API key saved!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to save API key")
                
                st.markdown("""
                ---
                ### Need Help?
                1. Click the links above to get your API keys
                2. Enter the keys in the fields above
                3. Click Save to store them securely
                4. The app will refresh automatically
                """)
            return

        # Initialize session state for research options
        if "research_options" not in st.session_state:
            st.session_state.research_options = {
                "primary_keywords": "",
                "related_keywords": "",
                "target_audience": ["General"],
                "content_type": ["Blog Posts"],
                "search_depth": 3,
                "geo_location": "us",
                "search_language": "en",
                "num_results": 10,
                "time_range": "past month",
                "include_domains": "",
                "similar_url": "",
                "search_mode": "google"  # Default search mode
            }

        # Define the research options dialog function
        @st.dialog("🔍 Research Options", width="large")
        def show_research_options():
            tab1, tab2 = st.tabs(["Basic", "Advanced"])
            
            with tab1:
                st.session_state.research_options["related_keywords"] = st.text_input(
                    "Related Keywords",
                    value=st.session_state.research_options["related_keywords"],
                    placeholder="Enter related terms...",
                    help="Additional keywords to provide context and expand research"
                )
                
                st.session_state.research_options["target_audience"] = st.multiselect(
                    "Target Audience",
                    ["General", "Technical", "Business", "Academic", "Youth", "Senior"],
                    default=st.session_state.research_options["target_audience"],
                    help="Select your target audience to focus research"
                )
                
                st.session_state.research_options["content_type"] = st.multiselect(
                    "Content Type",
                    ["Blog Posts", "Articles", "Social Media", "Whitepapers", "Tutorials", "Videos"],
                    default=st.session_state.research_options["content_type"],
                    help="Select content types to tailor research results"
                )
                
                st.session_state.research_options["search_depth"] = st.slider(
                    "Search Depth",
                    min_value=1,
                    max_value=5,
                    value=st.session_state.research_options["search_depth"],
                    help="Higher depth means more comprehensive but slower research"
                )

            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    st.session_state.research_options["geo_location"] = st.selectbox(
                        "Geographic Location",
                        options=["us", "in", "uk", "fr", "de", "jp", "custom"],
                        index=["us", "in", "uk", "fr", "de", "jp"].index(st.session_state.research_options["geo_location"]),
                        help="Target specific geographic region for research"
                    )
                    
                    st.session_state.research_options["num_results"] = st.number_input(
                        "Number of Results",
                        min_value=1,
                        max_value=100,
                        value=st.session_state.research_options["num_results"],
                        help="Number of results to analyze"
                    )
                
                with col2:
                    st.session_state.research_options["search_language"] = st.selectbox(
                        "Search Language",
                        options=["en", "hi", "fr", "de", "es", "custom"],
                        index=["en", "hi", "fr", "de", "es"].index(st.session_state.research_options["search_language"]),
                        help="Primary language for search results"
                    )
                    
                    st.session_state.research_options["time_range"] = st.selectbox(
                        "Time Range",
                        options=["past day", "past week", "past month", "past year", "anytime"],
                        index=["past day", "past week", "past month", "past year", "anytime"].index(st.session_state.research_options["time_range"]),
                        help="Time period for research results"
                    )

                # Add the technical options to the Advanced tab
                st.markdown("---")
                st.markdown("### Advanced Search Parameters")
                
                st.session_state.research_options["include_domains"] = st.text_input(
                    "Include Domains",
                    value=st.session_state.research_options["include_domains"],
                    placeholder="example.com, another.com",
                    help="Specific domains to include in research"
                )
                
                st.session_state.research_options["similar_url"] = st.text_input(
                    "Similar URL",
                    value=st.session_state.research_options["similar_url"],
                    placeholder="https://example.com/page",
                    help="Find content similar to this URL"
                )

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Apply", use_container_width=True, type="primary"):
                    st.session_state.show_options_dialog = False
                    st.rerun()
            with col2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.show_options_dialog = False
                    st.rerun()

        # Main interface
        st.title("ALwrity Web Researcher")
        
        # Primary search area with help popover
        with st.popover("ℹ️ Keyword Research Tips"):
            st.markdown("""
                ### How to Get Better Results
                1. **Primary Keywords**: Your main topic or focus
                2. **Related Keywords**: Supporting terms that add context
                3. **Search Depth**: Higher depth = more comprehensive but slower
                4. **Target Audience**: Affects content recommendations
                5. **Content Type**: Influences research focus
                6. **Search Mode**: Choose between traditional web research(Google), AI-powered search(Tavily and Metaphor) and Deep Researcher
            """)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.session_state.research_options["primary_keywords"] = st.text_input(
                "Primary Keywords", 
                value=st.session_state.research_options["primary_keywords"],
                placeholder="Enter main keywords for research...",
                help="Enter your main topic or focus keywords"
            )
        with col2:
            if st.button("Research Options", use_container_width=True):
                show_research_options()

        # Research method selection in main container
        st.markdown("### Select Research Method")
        search_options = [
            ("google", "🔍 Google Search", "Traditional web research with AI analysis", bool(api_keys['SERPER_API_KEY'])),
            ("ai", "🤖 AI Search", "Neural search with semantic analysis", bool(api_keys['METAPHOR_API_KEY'] and api_keys['TAVILY_API_KEY'])),
            ("deep", "🔬 Deep Search (Beta)", "Advanced deep web analysis", bool(all(api_keys.values())))
        ]
        
        enabled_options = [opt[1] for opt in search_options if opt[3]]
        if enabled_options:
            selected_option = st.radio(
                "Search Method",
                options=enabled_options,
                horizontal=True,
                help="Choose your preferred research method"
            )
            
            # Map the selected option to the search_mode value
            for mode, label, _, _ in search_options:
                if label == selected_option:
                    st.session_state.research_options["search_mode"] = mode
                    break
        else:
            st.warning("No search methods available. Please configure API keys.")

        # Execute search button
        if st.button("🔍 Start Research", type="primary", use_container_width=True):
            if not st.session_state.research_options["primary_keywords"]:
                st.warning("⚠️ Please enter primary keywords for research")
                return
            
            try:
                # Create compact progress display
                progress_container = st.container()
                with progress_container:
                    status_col, progress_col = st.columns([3, 1])
                    with status_col:
                        status_display = st.empty()
                        status_display.info("🚀 Initializing research...")
                    with progress_col:
                        progress_bar = st.progress(0)

                def update_progress(message, progress=None, level="info"):
                    """Update progress bar and status display.
                    
                    Args:
                        message (str): The message to display
                        progress (float, optional): Progress value between 0 and 100. Will be converted to 0.0-1.0
                        level (str, optional): Message level (info, warning, error, success)
                    """
                    if progress is not None:
                        # Convert percentage to decimal (0.0-1.0)
                        progress = float(progress) / 100.0
                        # Ensure progress stays within bounds
                        progress = max(0.0, min(1.0, progress))
                        progress_bar.progress(progress)
                    
                    if level == "error":
                        status_display.error(f"🚫 {message}")
                    elif level == "warning":
                        status_display.warning(f"⚠️ {message}")
                    elif level == "success":
                        status_display.success(f"✨ {message}")
                    else:
                        status_display.info(f"🔄 {message}")
                    logger.debug(f"Progress update [{level}]: {message}")

                # Execute search with all parameters
                try:
                    update_progress("Starting search...", 0.25)
                    logger.info(f"Executing web research with mode: {st.session_state.research_options['search_mode']}")
                    
                    # Create base parameters
                    research_params = {
                        "search_keywords": st.session_state.research_options["primary_keywords"],
                        "search_mode": st.session_state.research_options["search_mode"],
                        "related_keywords": st.session_state.research_options["related_keywords"],
                        "target_audience": st.session_state.research_options["target_audience"],
                        "content_type": st.session_state.research_options["content_type"],
                        "search_depth": st.session_state.research_options["search_depth"],
                        "geo_location": st.session_state.research_options["geo_location"],
                        "search_language": st.session_state.research_options["search_language"],
                        "num_results": st.session_state.research_options["num_results"],
                        "time_range": st.session_state.research_options["time_range"],
                        "include_domains": st.session_state.research_options["include_domains"],
                        "similar_url": st.session_state.research_options["similar_url"]
                    }
                    
                    # Add UI-specific parameters
                    research_params.update({
                        "status_container": status_display,
                        "update_progress": update_progress
                    })

                    # For AI search mode, ensure search_keywords is passed correctly
                    if st.session_state.research_options["search_mode"] == "ai":
                        research_params["tavily_params"] = {
                            "max_results": st.session_state.research_options["num_results"],
                            "search_depth": "advanced" if st.session_state.research_options["search_depth"] > 2 else "basic",
                            "time_range": st.session_state.research_options["time_range"],
                            "include_domains": st.session_state.research_options["include_domains"].split(",") if st.session_state.research_options["include_domains"] else [""]
                        }
                        # Pass search_keywords as a positional argument
                        research_params["tavily_search_keywords"] = st.session_state.research_options["primary_keywords"]
                    
                    # Execute the research
                    web_research_result = gpt_web_researcher(**research_params)
                    
                    if web_research_result:
                        status_display.success("✨ Research completed!")
                        
                        # Display results in an organized way
                        with st.expander("📊 Research Results", expanded=False):
                            st.write(web_research_result)
                    else:
                        st.warning("No results found for your search")
                        
                except Exception as e:
                    error_msg = f"Research failed: {str(e)}"
                    logger.error(error_msg, exc_info=True)
                    st.error(f"🚫 Research failed: {error_msg}")
                
            except Exception as e:
                logger.error(f"Unexpected error in web research: {e}", exc_info=True)
                st.error("🚫 An unexpected error occurred. Please try again.")
    except Exception as e:
        logger.error(f"Unexpected error in web research: {e}", exc_info=True)
        st.error("🚫 An unexpected error occurred. Please try again.")