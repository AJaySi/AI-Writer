"""AI research module for topic analysis and research."""

import asyncio
from typing import Dict, Any
from loguru import logger
import sys
from ..web_crawlers.async_web_crawler import AsyncWebCrawlerService
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen

# Configure logger
logger.remove()
logger.add(
    "logs/ai_research.log",
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

def research_topic(topic: str) -> Dict[str, Any]:
    """
    Research a topic using web crawling and AI analysis.
    
    Args:
        topic (str): The topic to research
        
    Returns:
        Dict[str, Any]: Research results including overview, findings, and recommendations
    """
    try:
        logger.info(f"[research_topic] Starting research for topic: {topic}")
        
        # Initialize web crawler
        async def analyze_topic():
            async with AsyncWebCrawlerService() as crawler:
                # Perform web research
                search_results = await crawler.crawl_website(topic)
                
                if not search_results.get('success'):
                    return {
                        'success': False,
                        'error': search_results.get('error', 'Research failed')
                    }
                
                # Analyze content with LLM
                analysis = await crawler.analyze_content_with_llm(
                    search_results['content'],
                    api_key=None,  # Should be passed from config
                    gpt_provider="google"  # Should be configurable
                )
                
                # Structure the response
                return {
                    'success': True,
                    'data': {
                        'research': {
                            'overview': {
                                'topic': topic,
                                'scope': analysis.get('topics', []),
                                'methodology': 'Web crawling and AI analysis'
                            },
                            'data_quality': {
                                'is_reliable': bool(analysis.get('seo_score', 0) > 0.7)
                            },
                            'analysis_quality': {
                                'is_thorough': bool(len(analysis.get('key_insights', [])) > 5)
                            },
                            'recommendations': analysis.get('recommendations', []),
                            'next_steps': analysis.get('priority_areas', [])
                        }
                    }
                }
        
        # Run the async analysis
        results = asyncio.run(analyze_topic())
        
        if not results.get('success'):
            error_msg = results.get('error', 'Research failed')
            logger.error(f"[research_topic] Research failed: {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
        
        logger.info("[research_topic] Research completed successfully")
        return results
        
    except Exception as e:
        error_msg = f"Research failed: {str(e)}"
        logger.error(f"[research_topic] {error_msg}")
        return {
            'success': False,
            'error': str(e)
        } 