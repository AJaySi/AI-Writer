import streamlit as st
import logging
from datetime import datetime
from typing import Dict, Optional, Any

# Configure module logger
logger = logging.getLogger(__name__)

def display_research_results(results: Dict[str, Any]) -> None:
    """
    Display research results in a structured format with tabs.
    
    Args:
        results (dict): Processed research results containing summary and data
    """
    if not results:
        st.warning("No results to display")
        return

    # Create tabs for different result sections
    tabs = st.tabs(["📊 Summary", "🔍 Results", "📈 Statistics"])
    
    with tabs[0]:
        display_summary_section(results)
    
    with tabs[1]:
        if results['source'] == 'gemini':
            display_gemini_results(results)
        else:
            display_serp_results(results)
    
    with tabs[2]:
        display_statistics(results)

def process_research_results(results: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Process and format research results."""
    logger.info("Processing research results")
    
    try:
        if not results:
            return None
            
        processed = {
            'timestamp': str(datetime.now()),
            'source': results.get('source', 'unknown'),
            'summary': {},
            'data': {}
        }
        
        if results.get('source') == 'gemini':
            processed.update(process_gemini_results(results))
        else:
            processed.update(process_serp_results(results))
        
        logger.info("Results processing completed")
        return processed
        
    except Exception as err:
        logger.error(f"Failed to process results: {err}", exc_info=True)
        return None

def process_search_results(search_results: Dict[str, Any], search_type: str = "general") -> Optional[Dict[str, Any]]:
    """Process search results and prepare for display."""
    logger.info(f"Processing {search_type} search results")
    
    try:
        if not search_results:
            return None
            
        processed = {
            'organic': process_organic_results(search_results.get('organic', [])),
            'peopleAlsoAsk': process_paa_results(search_results.get('peopleAlsoAsk', [])),
            'relatedSearches': process_related_searches(search_results.get('relatedSearches', [])),
            'metadata': {
                'timestamp': str(datetime.now()),
                'type': search_type
            }
        }
        
        return processed
        
    except Exception as err:
        logger.error(f"Error processing search results: {err}", exc_info=True)
        return None

# Helper functions for result processing
def process_organic_results(results):
    """Process organic search results."""
    return [{
        'title': result.get('title', 'No Title'),
        'link': result.get('link', '#'),
        'snippet': result.get('snippet', 'No snippet available'),
        'position': result.get('position', 'N/A')
    } for result in results]

def process_paa_results(results):
    """Process People Also Ask results."""
    return [{
        'question': result.get('title', ''),
        'answer': result.get('snippet', 'No answer available'),
        'link': result.get('link', '#')
    } for result in results]

def process_related_searches(results):
    """Process related searches."""
    return [query.get('query', '') for query in results]

def process_gemini_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process Gemini API research results.
    
    Args:
        results (dict): Raw Gemini research results
        
    Returns:
        dict: Processed results with summary and data
    """
    gemini_data = results.get('results', {})
    return {
        'summary': {
            'main_findings': gemini_data.get('main_response', ''),
            'sources': gemini_data.get('grounding_data', []),
            'processing_time': gemini_data.get('metadata', {}).get('timestamp'),
            'total_sources': len(gemini_data.get('grounding_data', [])),
            'model': gemini_data.get('metadata', {}).get('model', 'unknown')
        },
        'data': gemini_data
    }

def process_serp_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process SERP search results.
    
    Args:
        results (dict): Raw SERP results
        
    Returns:
        dict: Processed results with summary and data
    """
    organic_results = results.get('organic', [])
    paa_results = results.get('peopleAlsoAsk', [])
    related_searches = results.get('relatedSearches', [])
    
    return {
        'summary': {
            'total_results': len(organic_results),
            'sources': [result.get('link') for result in organic_results],
            'titles': [result.get('title') for result in organic_results],
            'total_questions': len(paa_results),
            'total_related': len(related_searches)
        },
        'data': {
            'organic': process_organic_results(organic_results),
            'peopleAlsoAsk': process_paa_results(paa_results),
            'relatedSearches': process_related_searches(related_searches)
        }
    }

# Display helper functions
def display_summary_section(results):
    """Display summary section of results."""
    st.markdown("### 📋 Research Summary")
    st.markdown(f"""
    - **Source**: {results['source'].title()}
    - **Time**: {results['timestamp']}
    - **Total Sources**: {len(results.get('summary', {}).get('sources', []))}
    """)

def display_gemini_results(results):
    """Display Gemini-specific results."""
    st.markdown("### 🤖 Gemini Research Findings")
    st.write(results['summary']['main_findings'])
    
    with st.expander("🌐 Sources and References", expanded=False):
        st.write(results['data'].get('grounding_data', 'No sources available'))

def display_serp_results(results):
    """Display SERP-specific results."""
    st.markdown("### 🔍 Search Results")
    
    for result in results['data'].get('organic', []):
        with st.expander(f"📄 {result['title']}", expanded=False):
            st.markdown(f"""
            **Rank:** {result['position']}
            
            **Link:** [{result['link']}]({result['link']})
            
            **Snippet:**
            {result['snippet']}
            """)

def display_statistics(results: Dict[str, Any]) -> None:
    """
    Display statistical information about search results.
    
    Args:
        results (dict): Processed research results
    """
    st.markdown("### 📈 Research Statistics")
    
    # Source-specific metrics
    if results['source'] == 'gemini':
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Sources Analyzed",
                results.get('summary', {}).get('total_sources', 0)
            )
        with col2:
            st.metric(
                "Model Used",
                results.get('summary', {}).get('model', 'Unknown')
            )
            
    else:  # SERP results
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Organic Results",
                results.get('summary', {}).get('total_results', 0)
            )
        with col2:
            st.metric(
                "Related Questions",
                results.get('summary', {}).get('total_questions', 0)
            )
        with col3:
            st.metric(
                "Related Searches",
                results.get('summary', {}).get('total_related', 0)
            )
    
    # Common metrics
    st.markdown("#### 🕒 Timing Information")
    st.info(f"Research completed at: {results['timestamp']}")
    
    # Display data quality metrics
    st.markdown("#### 📊 Data Quality")
    quality_metrics = calculate_quality_metrics(results)
    
    col1, col2 = st.columns(2)
    with col1:
        st.progress(quality_metrics['completeness'])
        st.caption("Data Completeness")
    with col2:
        st.progress(quality_metrics['relevance'])
        st.caption("Estimated Relevance")

def calculate_quality_metrics(results: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculate quality metrics for the research results.
    
    Args:
        results (dict): Processed research results
        
    Returns:
        dict: Quality metrics including completeness and relevance scores
    """
    try:
        if results['source'] == 'gemini':
            completeness = 1.0 if results['summary']['main_findings'] else 0.0
            relevance = 0.8 if results['summary']['sources'] else 0.4
        else:
            organic_results = results.get('summary', {}).get('total_results', 0)
            completeness = min(organic_results / 10, 1.0)  # Normalize to 0-1
            has_paa = bool(results.get('summary', {}).get('total_questions', 0))
            has_related = bool(results.get('summary', {}).get('total_related', 0))
            relevance = (0.6 + (0.2 if has_paa else 0) + (0.2 if has_related else 0))
        
        return {
            'completeness': completeness,
            'relevance': relevance
        }
        
    except Exception as err:
        logger.error(f"Error calculating quality metrics: {err}")
        return {'completeness': 0.0, 'relevance': 0.0}