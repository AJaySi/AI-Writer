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

def render_ai_research_setup(api_key_manager: APIKeyManager) -> Dict[str, Any]:
    """Render the AI research setup step."""
    logger.info("[render_ai_research_setup] Rendering AI research setup component")
    
    st.markdown("""
        <div class='setup-header'>
            <h2>🔍 AI Research Setup</h2>
            <p>Configure your AI research providers for content analysis and research</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for different search types
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### The Usual")
        
        # SerpAPI Card
        st.markdown("""
            <div class="ai-provider-card">
                <div class="ai-provider-header">
                    <div class="ai-provider-icon">🔎</div>
                    <div class="ai-provider-title">SerpAPI</div>
                </div>
                <div class="ai-provider-description">
                    Access search engine results for research
                </div>
                <div class="ai-provider-input">
        """, unsafe_allow_html=True)
        
        serpapi_key = st.text_input(
            "SerpAPI Key",
            type="password",
            key="serpapi_key",
            help="Enter your SerpAPI key"
        )
        
        if serpapi_key:
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

        # Firecrawl Card
        st.markdown("""
            <div class="ai-provider-card">
                <div class="ai-provider-header">
                    <div class="ai-provider-icon">🕷️</div>
                    <div class="ai-provider-title">Firecrawl</div>
                </div>
                <div class="ai-provider-description">
                    Web content extraction and analysis
                </div>
                <div class="ai-provider-input">
        """, unsafe_allow_html=True)
        
        firecrawl_key = st.text_input(
            "Firecrawl API Key",
            type="password",
            key="firecrawl_key",
            help="Enter your Firecrawl API key"
        )
        
        if firecrawl_key:
            st.markdown("""
                <div class="ai-provider-status status-valid">
                    ✓ API key configured
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
        
        # Tavily Card
        st.markdown("""
            <div class="ai-provider-card">
                <div class="ai-provider-header">
                    <div class="ai-provider-icon">🤖</div>
                    <div class="ai-provider-title">Tavily AI</div>
                </div>
                <div class="ai-provider-description">
                    AI-powered search with semantic understanding
                </div>
                <div class="ai-provider-input">
        """, unsafe_allow_html=True)
        
        tavily_key = st.text_input(
            "Tavily API Key",
            type="password",
            key="tavily_key",
            help="Enter your Tavily API key"
        )
        
        if tavily_key:
            st.markdown("""
                <div class="ai-provider-status status-valid">
                    ✓ API key configured
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
        
        # Metaphor/Exa Card
        st.markdown("""
            <div class="ai-provider-card">
                <div class="ai-provider-header">
                    <div class="ai-provider-icon">🧠</div>
                    <div class="ai-provider-title">Metaphor/Exa</div>
                </div>
                <div class="ai-provider-description">
                    Neural search engine for deep research
                </div>
                <div class="ai-provider-input">
        """, unsafe_allow_html=True)
        
        metaphor_key = st.text_input(
            "Metaphor/Exa API Key",
            type="password",
            key="metaphor_key",
            help="Enter your Metaphor/Exa API key"
        )
        
        if metaphor_key:
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
    
    # Disabled Options Expander
    with st.expander("🔜 Coming Soon - More Search Options", expanded=False):
        st.markdown("""
            <div style='opacity: 0.7;'>
                <h4>Bing Search API</h4>
                <p>Microsoft's powerful search API with web, news, and image search capabilities.</p>
                
                <h4>Google Search API</h4>
                <p>Google's programmable search engine with customizable search parameters.</p>
                
                <p><em>These integrations are under development and will be available soon!</em></p>
            </div>
        """, unsafe_allow_html=True)
    
    # Track changes
    changes_made = bool(serpapi_key or tavily_key or metaphor_key or firecrawl_key)
    
    # Navigation buttons with correct arguments
    if render_navigation_buttons(3, 5, changes_made):
        if changes_made:
            try:
                # Load existing .env file if it exists
                load_dotenv()
                
                # Create or update .env file with new API keys
                with open('.env', 'a') as f:
                    if serpapi_key:
                        f.write(f"\nSERPAPI_KEY={serpapi_key}")
                        logger.info("[render_ai_research_setup] Saved SerpAPI key")
                    if tavily_key:
                        f.write(f"\nTAVILY_API_KEY={tavily_key}")
                        logger.info("[render_ai_research_setup] Saved Tavily API key")
                    if metaphor_key:
                        f.write(f"\nMETAPHOR_API_KEY={metaphor_key}")
                        logger.info("[render_ai_research_setup] Saved Metaphor API key")
                    if firecrawl_key:
                        f.write(f"\nFIRECRAWL_API_KEY={firecrawl_key}")
                        logger.info("[render_ai_research_setup] Saved Firecrawl API key")
                
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
    st.markdown("""
    ---
    ### Understanding Your Research Options
    
    #### The Usual: Traditional Search
    **SerpAPI**
    - Real-time search results from multiple search engines
    - Access to structured data from search results
    - Great for gathering general information and market research
    - Includes features like:
        - Web search results
        - News articles
        - Knowledge graphs
        - Related questions
    
    #### AI Deep Research: Advanced Search Capabilities
    
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
    
    #### Choosing the Right Tool
    
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
    
    return {"current_step": 3, "changes_made": changes_made}
