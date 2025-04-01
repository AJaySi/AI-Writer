"""Web crawler for ALwrity style analysis."""

import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from loguru import logger

async def analyze_website_style(url: str, sample_text: str = None) -> dict:
    """
    Analyze website content or sample text for style analysis.
    
    Args:
        url: Website URL to analyze
        sample_text: Optional sample text to analyze instead of website
        
    Returns:
        dict: Analysis results including content style metrics
    """
    try:
        if sample_text:
            # Analyze sample text directly
            return {
                "success": True,
                "content": sample_text,
                "metrics": {
                    "word_count": len(sample_text.split()),
                    "sentence_count": len(sample_text.split('.')),
                    "avg_sentence_length": len(sample_text.split()) / max(len(sample_text.split('.')), 1)
                }
            }
        browser_config = BrowserConfig()  # Default browser configuration
        run_config = CrawlerRunConfig()   # Default crawl run configuration
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url=url,
                config=run_config
            )
            print(result.markdown)  # Print clean markdown content

            logger.debug(f"Crawl result: {result}")
            if result.success:
                # Process content for style analysis
                content = result.markdown
                sentences = [s.strip() for s in content.split('.') if s.strip()]
                
                return {
                    "success": True,
                    "content": content,
                    "metrics": {
                        "word_count": len(content.split()),
                        "sentence_count": len(sentences),
                        "avg_sentence_length": len(content.split()) / max(len(sentences), 1),
                        "internal_links": len(result.links["internal"]),
                        "images": len(result.media["images"])
                    }
                }
            else:
                return {
                    "success": False,
                    "error": result.error_message
                }

    except Exception as e:
        logger.error(f"Error in style analysis: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def analyze_style(url: str = None, sample_text: str = None) -> dict:
    """
    Synchronous wrapper for style analysis.
    
    Args:
        url: Website URL to analyze
        sample_text: Optional sample text to analyze
        
    Returns:
        dict: Analysis results
    """
    return asyncio.run(analyze_website_style(url, sample_text))


# Deep Crawling
# One of Crawl4AI's most powerful features is its ability to perform 
# configurable deep crawling that can explore websites beyond a single page.
#  With fine-tuned control over crawl depth, domain boundaries,
#  and content filtering, Crawl4AI gives you the tools to extract precisely the content you need.
# 
#
#
#
#
