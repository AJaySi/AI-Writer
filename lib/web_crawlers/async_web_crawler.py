"""Web crawler module using requests and BeautifulSoup."""

from typing import Dict, List, Optional
import json
from loguru import logger
import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pydantic import BaseModel, Field
import os
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen

class WebsiteContent(BaseModel):
    """Model for website content analysis."""
    title: str = Field("", description="Title of the webpage")
    description: str = Field("", description="Meta description of the webpage")
    main_content: str = Field("", description="Main content of the webpage")
    headings: List[str] = Field([], description="All headings on the page")
    links: List[Dict[str, str]] = Field([], description="All links on the page")
    images: List[Dict[str, str]] = Field([], description="All images on the page")
    meta_tags: Dict[str, str] = Field({}, description="Meta tags from the page")

class AsyncWebCrawlerService:
    """Service for crawling websites."""
    
    def __init__(self):
        """Initialize the crawler service."""
        logger.info("[AsyncWebCrawlerService.__init__] Initializing crawler service")
        self.visited_urls = set()
        self.base_url = None
        self.domain = None
        self.session = None
        self.max_pages = 10  # Limit the number of pages to crawl
        self.timeout = 30  # Timeout in seconds for requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def __aenter__(self):
        """Create aiohttp session when entering context."""
        logger.debug("[AsyncWebCrawlerService.__aenter__] Creating aiohttp session")
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close aiohttp session when exiting context."""
        logger.debug("[AsyncWebCrawlerService.__aexit__] Closing aiohttp session")
        if self.session:
            await self.session.close()
    
    async def fetch_url(self, url: str) -> str:
        """
        Fetch URL content asynchronously.
        
        Args:
            url (str): URL to fetch
            
        Returns:
            str: HTML content
        """
        logger.debug(f"[AsyncWebCrawlerService.fetch_url] Fetching URL: {url}")
        if not self.session:
            logger.debug("[AsyncWebCrawlerService.fetch_url] Creating new session")
            self.session = aiohttp.ClientSession(headers=self.headers)
            
        async with self.session.get(url) as response:
            if response.status == 200:
                logger.debug(f"[AsyncWebCrawlerService.fetch_url] Successfully fetched URL: {url}")
                return await response.text()
            else:
                error_msg = f"Failed to fetch URL: Status code {response.status}"
                logger.error(f"[AsyncWebCrawlerService.fetch_url] {error_msg}")
                raise Exception(error_msg)
    
    async def crawl_website(self, url: str) -> Dict:
        """
        Crawl a website and extract its content.
        
        Args:
            url (str): The URL to crawl
            
        Returns:
            Dict: Extracted website content and metadata
        """
        try:
            logger.info(f"[AsyncWebCrawlerService.crawl_website] Starting crawl for URL: {url}")
            
            # Fetch the page content
            try:
                html_content = await self.fetch_url(url)
                logger.debug("[AsyncWebCrawlerService.crawl_website] Successfully fetched HTML content")
            except Exception as e:
                error_msg = f"Failed to fetch content from {url}: {str(e)}"
                logger.error(f"[AsyncWebCrawlerService.crawl_website] {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }
            
            # Parse HTML with BeautifulSoup
            logger.debug("[AsyncWebCrawlerService.crawl_website] Parsing HTML content")
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract main content (focusing on article-like content)
            main_content_elements = soup.find_all(['article', 'main', 'div'], class_=['content', 'main-content', 'article', 'post'])
            if not main_content_elements:
                main_content_elements = soup.find_all(['p', 'article', 'section'])
            
            main_content = ' '.join([elem.get_text(strip=True) for elem in main_content_elements])
            
            # If still no content, get all paragraph text
            if not main_content:
                main_content = ' '.join([p.get_text(strip=True) for p in soup.find_all('p')])
            
            logger.debug(f"[AsyncWebCrawlerService.crawl_website] Extracted {len(main_content)} characters of main content")
            
            # Extract content
            content = {
                'title': soup.title.string.strip() if soup.title else '',
                'description': soup.find('meta', {'name': 'description'}).get('content', '').strip() if soup.find('meta', {'name': 'description'}) else '',
                'main_content': main_content,
                'headings': [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
                'links': [{'text': a.get_text(strip=True), 'href': urljoin(url, a.get('href', ''))} for a in soup.find_all('a', href=True)],
                'images': [{'alt': img.get('alt', '').strip(), 'src': urljoin(url, img.get('src', ''))} for img in soup.find_all('img', src=True)],
                'meta_tags': {
                    meta.get('name', meta.get('property', '')): meta.get('content', '').strip()
                    for meta in soup.find_all('meta')
                    if (meta.get('name') or meta.get('property')) and meta.get('content')
                }
            }
            
            logger.debug(f"[AsyncWebCrawlerService.crawl_website] Extracted {len(content['links'])} links and {len(content['images'])} images")
            
            # Close the session if it exists
            if self.session:
                logger.debug("[AsyncWebCrawlerService.crawl_website] Closing session")
                await self.session.close()
                self.session = None
            
            logger.info("[AsyncWebCrawlerService.crawl_website] Successfully completed website crawl")
            return {
                'success': True,
                'content': content,
                'url': url
            }
                
        except Exception as e:
            error_msg = f"Error crawling {url}: {str(e)}"
            logger.error(f"[AsyncWebCrawlerService.crawl_website] {error_msg}")
            # Ensure session is closed even if there's an error
            if self.session:
                logger.debug("[AsyncWebCrawlerService.crawl_website] Closing session after error")
                await self.session.close()
                self.session = None
            return {
                'success': False,
                'error': str(e)
            }
    
    async def analyze_content_with_llm(self, content: Dict, api_key: str, gpt_provider: str) -> Dict:
        """
        Analyze content using LLM.
        
        Args:
            content (Dict): Content to analyze
            api_key (str): API key for the LLM service
            gpt_provider (str): Provider to use (openai/google)
            
        Returns:
            Dict: Analysis results
        """
        try:
            logger.info(f"[AsyncWebCrawlerService.analyze_content_with_llm] Starting content analysis with {gpt_provider}")
            
            # Prepare the content for analysis
            main_content = content.get("main_content", "")
            if isinstance(main_content, dict):
                main_content = main_content.get("text", "")
            
            logger.debug(f"[AsyncWebCrawlerService.analyze_content_with_llm] Prepared {len(main_content)} characters for analysis")
            
            # Construct the prompt for analysis
            prompt = f"""Analyze the following website content and provide a comprehensive analysis:

Content:
{main_content[:4000]}  # Limit content length for API

Please provide analysis in the following JSON format:
{{
    "topics": ["topic1", "topic2", ...],
    "key_insights": ["insight1", "insight2", ...],
    "content_quality": {{
        "readability": "score",
        "engagement": "score",
        "completeness": "score"
    }},
    "recommendations": ["rec1", "rec2", ...],
    "seo_score": "score",
    "content_gaps": ["gap1", "gap2", ...],
    "opportunities": ["opp1", "opp2", ...],
    "priority_areas": ["area1", "area2", ...]
}}

Ensure the response is valid JSON."""

            # Call the LLM function
            logger.debug("[AsyncWebCrawlerService.analyze_content_with_llm] Calling llm_text_gen with prompt")
            response = llm_text_gen(prompt)
            
            if not response:
                logger.error("[AsyncWebCrawlerService.analyze_content_with_llm] No response from LLM")
                return {}
            
            # Clean up the response before parsing
            logger.debug("[AsyncWebCrawlerService.analyze_content_with_llm] Cleaning response for JSON parsing")
            try:
                # Remove any leading/trailing whitespace
                cleaned_response = response.strip()
                
                # If response starts with a newline or other characters before {, clean it
                start_idx = cleaned_response.find('{')
                end_idx = cleaned_response.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    cleaned_response = cleaned_response[start_idx:end_idx + 1]
                
                # Fix any line breaks within strings
                cleaned_response = cleaned_response.replace('\n', ' ')
                
                logger.debug(f"[AsyncWebCrawlerService.analyze_content_with_llm] Attempting to parse cleaned response: {cleaned_response[:100]}...")
                
                # Parse the cleaned response
                analysis_result = json.loads(cleaned_response)
                logger.info("[AsyncWebCrawlerService.analyze_content_with_llm] Successfully parsed LLM response")
                logger.debug(f"[AsyncWebCrawlerService.analyze_content_with_llm] Analysis result keys: {analysis_result.keys()}")
                return analysis_result
                
            except json.JSONDecodeError as e:
                logger.error(f"[AsyncWebCrawlerService.analyze_content_with_llm] Failed to parse LLM response as JSON: {str(e)}")
                logger.debug(f"[AsyncWebCrawlerService.analyze_content_with_llm] Raw response: {response[:100]}...")
                return {}
                
        except Exception as e:
            logger.error(f"[AsyncWebCrawlerService.analyze_content_with_llm] Error analyzing content with LLM: {str(e)}")
            return {}