"""AI research setup component for the API key manager."""

import streamlit as st
from loguru import logger
from typing import Dict, Any
from ..manager import APIKeyManager
from .base import render_navigation_buttons
import os
from dotenv import load_dotenv
import sys

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    "logs/ai_research_setup.log",
    rotation="500 MB",
    retention="10 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>"
)

def get_existing_api_key(key_name: str) -> str:
    """Get existing API key from environment or .env file.
    
    Args:
        key_name (str): Name of the API key to retrieve
        
    Returns:
        str: The API key value if found, empty string otherwise
    """
    # First try to get from environment
    api_key = os.getenv(key_name)
    
    # If not in environment, try to get from .env file
    if not api_key and os.path.exists('.env'):
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.strip().startswith(f"{key_name}="):
                        api_key = line.strip().split('=')[1]
                        break
        except Exception as e:
            logger.error(f"[get_existing_api_key] Failed to read {key_name} from .env: {str(e)}")
    
    return api_key if api_key else ""

def update_env_file(api_keys: Dict[str, str]) -> None:
    """Update the .env file with new API keys, avoiding duplicates.
    
    Args:
        api_keys (Dict[str, str]): Dictionary of API keys to update
    """
    try:
        # Read existing .env file content
        env_content = []
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                env_content = f.readlines()
        
        # Remove trailing newlines and empty lines
        env_content = [line.strip() for line in env_content if line.strip()]
        
        # Create a dictionary of existing variables
        env_dict = {}
        for line in env_content:
            if '=' in line:
                key, value = line.split('=', 1)
                env_dict[key.strip()] = value.strip()
        
        # Update with new values
        env_dict.update(api_keys)
        
        # Write back to .env file
        with open('.env', 'w') as f:
            for key, value in env_dict.items():
                f.write(f"{key}={value}\n")
        
        logger.info("[update_env_file] Successfully updated .env file with API keys")
    except Exception as e:
        logger.error(f"[update_env_file] Error updating .env file: {str(e)}")
        raise

def render_ai_research_setup(api_key_manager: APIKeyManager) -> Dict[str, Any]:
    """Render the AI research setup step."""
    logger.info("[render_ai_research_setup] Rendering AI research setup component")
    
    st.markdown("""
        <div class='setup-header'><h2>🔍 AI Web Research API Setup</h2></div>
    """, unsafe_allow_html=True)
    
    # Create two columns for different search types
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### The Usual")
        
        # Get existing API keys
        existing_serpapi_key = get_existing_api_key("SERPAPI_KEY")
        existing_firecrawl_key = get_existing_api_key("FIRECRAWL_API_KEY")
        
        serpapi_key = st.text_input(
            "## Enter 🔎 SerpAPI",
            value=existing_serpapi_key,
            type="password",
            key="serpapi_key",
            help="Enter your SerpAPI key",
            placeholder="Access search engine results for research"
        )
        
        if serpapi_key or existing_serpapi_key:
            st.markdown("""
                <div class="ai-provider-status status-valid">
                    ✓ API key configured
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="api-info-section">
                <details>
                    <summary>📋 How to get your SerpAPI key</summary>
                    <div class="api-info-content">
                        <p><strong>Step-by-step guide:</strong></p>
                        <ol>
                            <li>Visit <a href="https://serpapi.com" target="_blank">SerpAPI</a></li>
                            <li>Create an account</li>
                            <li>Go to your dashboard</li>
                            <li>Copy your API key</li>
                            <li>Paste it here</li>
                        </ol>
                        <p><strong>Note:</strong> SerpAPI provides real-time search results from multiple engines.</p>
                    </div>
                </details>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        firecrawl_key = st.text_input(
            "Enter 🕷️ Firecrawl API Key",
            value=existing_firecrawl_key,
            type="password",
            key="firecrawl_key",
            help="Enter your Firecrawl API key",
            placeholder="Web content extraction and analysis"
        )
        
        if firecrawl_key or existing_firecrawl_key:
            st.markdown("""
                <div class="ai-provider-status status-valid">
                    ✓ Firecrawl API key configured
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="api-info-section">
                <details>
                    <summary>📋 How to get your Firecrawl API key</summary>
                    <div class="api-info-content">
                        <p><strong>Step-by-step guide:</strong></p>
                        <ol>
                            <li>Visit <a href="https://www.firecrawl.dev/account" target="_blank">Firecrawl</a></li>
                            <li>Create an account</li>
                            <li>Go to your dashboard</li>
                            <li>Generate your API key</li>
                            <li>Copy and paste it here</li>
                        </ol>
                        <p><strong>Note:</strong> Firecrawl provides powerful web content extraction and analysis capabilities.</p>
                    </div>
                </details>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### AI Deep Research")
        
        # Get existing API keys
        existing_tavily_key = get_existing_api_key("TAVILY_API_KEY")
        existing_metaphor_key = get_existing_api_key("METAPHOR_API_KEY")
        
        tavily_key = st.text_input(
            "Enter 🤖 Tavily API Key",
            value=existing_tavily_key,
            type="password",
            key="tavily_key",
            help="Enter your Tavily API key",
            placeholder="AI-powered search with semantic understanding"
        )
        
        if tavily_key or existing_tavily_key:
            st.markdown("""
                <div class="ai-provider-status status-valid">
                    ✓ Tavily API key configured
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="api-info-section">
                <details>
                    <summary>📋 How to get your Tavily API key</summary>
                    <div class="api-info-content">
                        <p><strong>Step-by-step guide:</strong></p>
                        <ol>
                            <li>Visit <a href="https://tavily.com" target="_blank">Tavily</a></li>
                            <li>Create an account</li>
                            <li>Go to API settings</li>
                            <li>Generate a new API key</li>
                            <li>Copy and paste it here</li>
                        </ol>
                        <p><strong>Note:</strong> Tavily provides AI-powered semantic search capabilities.</p>
                    </div>
                </details>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        metaphor_key = st.text_input(
            "Enter 🧠 Metaphor/Exa API Key",
            value=existing_metaphor_key,
            type="password",
            key="metaphor_key",
            help="Enter your Metaphor/Exa API key",
            placeholder="Neural search engine for deep research"
        )
        
        if metaphor_key or existing_metaphor_key:
            st.markdown("""
                <div class="ai-provider-status status-valid">
                    ✓ API key configured
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="api-info-section">
                <details>
                    <summary>📋 How to get your Metaphor/Exa API key</summary>
                    <div class="api-info-content">
                        <p><strong>Step-by-step guide:</strong></p>
                        <ol>
                            <li>Visit <a href="https://metaphor.systems" target="_blank">Metaphor/Exa</a></li>
                            <li>Create an account</li>
                            <li>Navigate to API settings</li>
                            <li>Generate your API key</li>
                            <li>Copy and paste it here</li>
                        </ol>
                        <p><strong>Note:</strong> Metaphor/Exa provides neural search capabilities for deep research.</p>
                    </div>
                </details>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    
    
    # Track changes
    changes_made = bool(serpapi_key or tavily_key or metaphor_key or firecrawl_key)
    
    # Navigation buttons with correct arguments
    if render_navigation_buttons(3, 5, changes_made):
        if changes_made:
            try:
                # Prepare API keys dictionary with only non-empty values
                api_keys = {}
                if serpapi_key:
                    api_keys['SERPAPI_KEY'] = serpapi_key
                if tavily_key:
                    api_keys['TAVILY_API_KEY'] = tavily_key
                if metaphor_key:
                    api_keys['METAPHOR_API_KEY'] = metaphor_key
                if firecrawl_key:
                    api_keys['FIRECRAWL_API_KEY'] = firecrawl_key
                
                # Update .env file with new API keys
                update_env_file(api_keys)
                
                # Update environment variables
                for key, value in api_keys.items():
                    os.environ[key] = value
                
                # Store the API keys in session state
                st.session_state['api_keys'] = {
                    'serpapi': serpapi_key,
                    'tavily': tavily_key,
                    'metaphor': metaphor_key,
                    'firecrawl': firecrawl_key
                }
                
                # Update progress and move to next step
                st.session_state['current_step'] = 4
                st.rerun()
            except Exception as e:
                error_msg = f"Error saving API keys: {str(e)}"
                logger.error(f"[render_ai_research_setup] {error_msg}")
                st.error(error_msg)
        else:
            st.error("Please configure at least one research provider to continue")
    
    # Detailed Information Section
    st.markdown("---")
    st.markdown("### Understanding Your Research Options")
    
    # Create four columns for the information popovers
    info_col1, info_col2, info_col3, info_col4 = st.columns(4)
    
    # The Usual: Traditional Search Popover
    with info_col1:
        with st.popover("#### The Usual: Traditional Search"):
            st.markdown("""
            **SerpAPI**
            - Real-time search results from multiple search engines
            - Access to structured data from search results
            - Great for gathering general information and market research
            - Includes features like:
                - Web search results
                - News articles
                - Knowledge graphs
                - Related questions
            """)
    
    # AI Deep Research Popover
    with info_col2:
        with st.popover("#### AI Deep Research: Advanced Search Capabilities"):
            st.markdown("""
            **Tavily AI**
            - AI-powered search with semantic understanding
            - Automatically summarizes and analyzes search results
            - Perfect for:
                - Deep research tasks
                - Academic research
                - Fact-checking
                - Real-time information gathering
            
            **Metaphor/Exa**
            - Neural search engine that understands context and meaning
            - Specialized in finding highly relevant content
            - Ideal for:
                - Technical research
                - Finding similar content
                - Discovering patterns in research
                - Understanding topic landscapes
            """)
    
    # Choosing the Right Tool Popover
    with info_col3:
        with st.popover("#### Choosing the Right Tool"):
            st.markdown("""
            1. **For General Research:**
               - Start with SerpAPI for broad coverage and structured data
            
            2. **For Deep Analysis:**
               - Use Tavily AI when you need AI-powered insights
               - Choose Metaphor/Exa for neural search and pattern discovery
            
            3. **For Comprehensive Research:**
               - Combine multiple tools to get the most complete picture
               - Use SerpAPI for initial research
               - Follow up with AI tools for deeper insights
            
            > **Pro Tip:** Configure multiple providers to ensure you have backup options and can cross-reference results for better accuracy.
            """)
    
    # Coming Soon Popover
    with info_col4:
        with st.popover("#### 🔜 Coming Soon - More Search Options"):
            st.markdown("""
            **Bing Search API**
            - Microsoft's powerful search API with comprehensive capabilities
            - Features include:
                - Web search with advanced filtering
                - News articles with sentiment analysis
                - Image search with visual recognition
                - Video search with content understanding
                - Custom search parameters for targeted results
            
            **Google Search API**
            - Google's programmable search engine with extensive features
            - Capabilities include:
                - Custom search engine creation
                - Site-specific search
                - Image and video search
                - News search with time-based filtering
                - Knowledge graph integration
            
            **Additional Planned Integrations:**
            - **DuckDuckGo API**: Privacy-focused search with no tracking
            - **Brave Search API**: Independent search engine with unique features
            - **Perplexity API**: AI-powered research assistant with real-time data
            
            > **Note:** These integrations are under active development and will be available in future updates.
            """)
    
    return {"current_step": 3, "changes_made": changes_made}
