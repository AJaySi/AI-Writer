"""Web Crawler Logic Service for ALwrity Backend.

This service handles business logic for web crawling and content extraction,
migrated from the legacy web crawler functionality.
"""

from typing import Dict, Any, List, Optional
from loguru import logger
from datetime import datetime
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
import re

class WebCrawlerLogic:
    """Business logic for web crawling and content extraction."""
    
    def __init__(self):
        """Initialize the Web Crawler Logic service."""
        logger.info("[WebCrawlerLogic.__init__] Initializing web crawler service")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.timeout = 30
        self.max_content_length = 10000
    
    def _validate_url(self, url: str) -> bool:
        """
        Validate URL format and fix common formatting issues.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if URL is valid
        """
        try:
            # Clean and fix common URL issues
            cleaned_url = self._fix_url_format(url)
            
            result = urlparse(cleaned_url)
            
            # Check if we have both scheme and netloc
            if not all([result.scheme, result.netloc]):
                return False
            
            # Additional validation for domain format
            domain = result.netloc
            if '.' not in domain or len(domain.split('.')[-1]) < 2:
                return False
            
            return True
        except Exception as e:
            logger.error(f"[WebCrawlerLogic._validate_url] URL validation error: {str(e)}")
            return False
    
    def _fix_url_format(self, url: str) -> str:
        """
        Fix common URL formatting issues.
        
        Args:
            url (str): URL to fix
            
        Returns:
            str: Fixed URL
        """
        # Remove leading/trailing whitespace
        url = url.strip()
        
        # Check if URL already has a protocol but is missing slashes
        if url.startswith('https:/') and not url.startswith('https://'):
            url = url.replace('https:/', 'https://')
        elif url.startswith('http:/') and not url.startswith('http://'):
            url = url.replace('http:/', 'http://')
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Fix missing slash after protocol
        if '://' in url and not url.split('://')[1].startswith('/'):
            url = url.replace('://', ':///')
        
        # Ensure only two slashes after protocol
        if ':///' in url:
            url = url.replace(':///', '://')
        
        logger.debug(f"[WebCrawlerLogic._fix_url_format] Fixed URL: {url}")
        return url
    
    async def crawl_website(self, url: str) -> Dict[str, Any]:
        """
        Crawl a website and extract its content asynchronously with enhanced data extraction.
        
        Args:
            url (str): The URL to crawl
            
        Returns:
            Dict: Extracted website content and metadata
        """
        try:
            logger.info(f"[WebCrawlerLogic.crawl_website] Starting enhanced crawl for URL: {url}")
            
            # Fix URL format first
            fixed_url = self._fix_url_format(url)
            logger.info(f"[WebCrawlerLogic.crawl_website] Fixed URL: {fixed_url}")
            
            # Validate URL
            if not self._validate_url(fixed_url):
                error_msg = f"Invalid URL format: {url}"
                logger.error(f"[WebCrawlerLogic.crawl_website] {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }
            
            # Fetch the page content
            try:
                async with aiohttp.ClientSession(headers=self.headers, timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                    async with session.get(fixed_url) as response:
                        if response.status == 200:
                            html_content = await response.text()
                            logger.debug("[WebCrawlerLogic.crawl_website] Successfully fetched HTML content")
                        else:
                            error_msg = f"Failed to fetch content: Status code {response.status}"
                            logger.error(f"[WebCrawlerLogic.crawl_website] {error_msg}")
                            return {
                                'success': False,
                                'error': error_msg
                            }
            except Exception as e:
                error_msg = f"Failed to fetch content from {fixed_url}: {str(e)}"
                logger.error(f"[WebCrawlerLogic.crawl_website] {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }
            
            # Parse HTML with BeautifulSoup
            logger.debug("[WebCrawlerLogic.crawl_website] Parsing HTML content")
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract domain information
            domain_info = self._extract_domain_info(fixed_url, soup)
            
            # Extract enhanced main content
            main_content = self._extract_enhanced_content(soup)
            
            # Extract social media and brand information
            social_media = self._extract_social_media(soup)
            brand_info = self._extract_brand_information(soup)
            
            # Extract content structure and patterns
            content_structure = self._extract_content_structure(soup)
            
            # Extract content
            content = {
                'title': soup.title.string.strip() if soup.title else '',
                'description': soup.find('meta', {'name': 'description'}).get('content', '').strip() if soup.find('meta', {'name': 'description'}) else '',
                'main_content': main_content,
                'headings': [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
                'links': [{'text': a.get_text(strip=True), 'href': urljoin(fixed_url, a.get('href', ''))} for a in soup.find_all('a', href=True)],
                'images': [{'alt': img.get('alt', '').strip(), 'src': urljoin(fixed_url, img.get('src', ''))} for img in soup.find_all('img', src=True)],
                'meta_tags': {
                    meta.get('name', meta.get('property', '')): meta.get('content', '').strip()
                    for meta in soup.find_all('meta')
                    if (meta.get('name') or meta.get('property')) and meta.get('content')
                },
                'domain_info': domain_info,
                'social_media': social_media,
                'brand_info': brand_info,
                'content_structure': content_structure
            }
            
            logger.debug(f"[WebCrawlerLogic.crawl_website] Extracted {len(content['links'])} links, {len(content['images'])} images, and {len(social_media)} social media links")
            
            logger.info("[WebCrawlerLogic.crawl_website] Successfully completed enhanced website crawl")
            return {
                'success': True,
                'content': content,
                'url': fixed_url,
                'timestamp': datetime.now().isoformat()
            }
                
        except Exception as e:
            error_msg = f"Error crawling {url}: {str(e)}"
            logger.error(f"[WebCrawlerLogic.crawl_website] {error_msg}")
            return {
                'success': False,
                'error': str(e)
            }

    def _extract_domain_info(self, url: str, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract domain-specific information."""
        try:
            domain = urlparse(url).netloc
            return {
                'domain': domain,
                'domain_name': domain.replace('www.', ''),
                'is_blog': any(keyword in domain.lower() for keyword in ['blog', 'medium', 'substack', 'wordpress']),
                'is_ecommerce': any(keyword in domain.lower() for keyword in ['shop', 'store', 'cart', 'buy', 'amazon', 'ebay']),
                'is_corporate': any(keyword in domain.lower() for keyword in ['corp', 'inc', 'llc', 'company', 'business']),
                'has_blog_section': bool(soup.find('a', href=re.compile(r'blog|news|articles', re.I))),
                'has_about_page': bool(soup.find('a', href=re.compile(r'about|company|team', re.I))),
                'has_contact_page': bool(soup.find('a', href=re.compile(r'contact|support|help', re.I)))
            }
        except Exception as e:
            logger.error(f"[WebCrawlerLogic._extract_domain_info] Error: {str(e)}")
            return {}

    def _extract_enhanced_content(self, soup: BeautifulSoup) -> str:
        """Extract enhanced main content with better structure detection."""
        try:
            # Try to find main content areas
            main_content_elements = []
            
            # Look for semantic content containers
            semantic_selectors = [
                'article', 'main', '[role="main"]',
                '.content', '.main-content', '.article', '.post',
                '.entry', '.page-content', '.site-content'
            ]
            
            for selector in semantic_selectors:
                elements = soup.select(selector)
                if elements:
                    main_content_elements.extend(elements)
                    break
            
            # If no semantic containers found, look for content-rich divs
            if not main_content_elements:
                content_divs = soup.find_all('div', class_=re.compile(r'content|main|article|post|entry', re.I))
                main_content_elements = content_divs
            
            # If still no content, get all paragraph text
            if not main_content_elements:
                main_content_elements = soup.find_all(['p', 'article', 'section'])
            
            # Extract text with better formatting
            content_parts = []
            for elem in main_content_elements:
                text = elem.get_text(separator=' ', strip=True)
                if text and len(text) > 20:  # Only include substantial text
                    content_parts.append(text)
            
            main_content = ' '.join(content_parts)
            
            # Limit content length
            if len(main_content) > self.max_content_length:
                main_content = main_content[:self.max_content_length] + "..."
            
            return main_content
            
        except Exception as e:
            logger.error(f"[WebCrawlerLogic._extract_enhanced_content] Error: {str(e)}")
            return ''

    def _extract_social_media(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract social media links and handles."""
        social_media = {}
        try:
            # Common social media patterns
            social_patterns = {
                'facebook': r'facebook\.com|fb\.com',
                'twitter': r'twitter\.com|x\.com',
                'linkedin': r'linkedin\.com',
                'instagram': r'instagram\.com',
                'youtube': r'youtube\.com|youtu\.be',
                'tiktok': r'tiktok\.com',
                'pinterest': r'pinterest\.com',
                'github': r'github\.com'
            }
            
            # Find all links
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link.get('href', '').lower()
                for platform, pattern in social_patterns.items():
                    if re.search(pattern, href):
                        social_media[platform] = href
                        break
            
            # Also check for social media meta tags
            meta_social = {
                'og:site_name': 'site_name',
                'twitter:site': 'twitter',
                'twitter:creator': 'twitter_creator'
            }
            
            for meta in soup.find_all('meta', property=True):
                prop = meta.get('property', '')
                if prop in meta_social:
                    social_media[meta_social[prop]] = meta.get('content', '')
            
            return social_media
            
        except Exception as e:
            logger.error(f"[WebCrawlerLogic._extract_social_media] Error: {str(e)}")
            return {}

    def _extract_brand_information(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract brand and company information."""
        brand_info = {}
        try:
            # Extract logo information
            logos = soup.find_all('img', alt=re.compile(r'logo|brand', re.I))
            if logos:
                brand_info['logo_alt'] = [logo.get('alt', '') for logo in logos]
            
            # Extract company name from various sources
            company_name_selectors = [
                'h1', '.logo', '.brand', '.company-name',
                '[class*="logo"]', '[class*="brand"]'
            ]
            
            for selector in company_name_selectors:
                elements = soup.select(selector)
                if elements:
                    brand_info['company_name'] = elements[0].get_text(strip=True)
                    break
            
            # Extract taglines and slogans
            tagline_selectors = [
                '.tagline', '.slogan', '.motto',
                '[class*="tagline"]', '[class*="slogan"]'
            ]
            
            for selector in tagline_selectors:
                elements = soup.select(selector)
                if elements:
                    brand_info['tagline'] = elements[0].get_text(strip=True)
                    break
            
            # Extract contact information
            contact_info = {}
            contact_patterns = {
                'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                'phone': r'[\+]?[1-9][\d]{0,15}',
                'address': r'\d+\s+[a-zA-Z\s]+(?:street|st|avenue|ave|road|rd|boulevard|blvd)'
            }
            
            for info_type, pattern in contact_patterns.items():
                matches = re.findall(pattern, soup.get_text())
                if matches:
                    contact_info[info_type] = matches[:3]  # Limit to first 3 matches
            
            brand_info['contact_info'] = contact_info
            
            return brand_info
            
        except Exception as e:
            logger.error(f"[WebCrawlerLogic._extract_brand_information] Error: {str(e)}")
            return {}

    def _extract_content_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract content structure and patterns."""
        structure = {}
        try:
            # Count different content types
            structure['headings'] = {
                'h1': len(soup.find_all('h1')),
                'h2': len(soup.find_all('h2')),
                'h3': len(soup.find_all('h3')),
                'h4': len(soup.find_all('h4')),
                'h5': len(soup.find_all('h5')),
                'h6': len(soup.find_all('h6'))
            }
            
            structure['paragraphs'] = len(soup.find_all('p'))
            structure['lists'] = len(soup.find_all(['ul', 'ol']))
            structure['images'] = len(soup.find_all('img'))
            structure['links'] = len(soup.find_all('a'))
            
            # Analyze content sections
            sections = soup.find_all(['section', 'article', 'div'], class_=re.compile(r'section|article|content', re.I))
            structure['content_sections'] = len(sections)
            
            # Check for common content patterns
            structure['has_navigation'] = bool(soup.find(['nav', 'header']))
            structure['has_footer'] = bool(soup.find('footer'))
            structure['has_sidebar'] = bool(soup.find(class_=re.compile(r'sidebar|aside', re.I)))
            structure['has_call_to_action'] = bool(soup.find(text=re.compile(r'click|buy|sign|register|subscribe', re.I)))
            
            return structure
            
        except Exception as e:
            logger.error(f"[WebCrawlerLogic._extract_content_structure] Error: {str(e)}")
            return {}
    
    def extract_content_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extract content from provided text sample.
        
        Args:
            text (str): Text content to process
            
        Returns:
            Dict: Processed content with metadata
        """
        try:
            logger.info("[WebCrawlerLogic.extract_content_from_text] Processing text content")
            
            # Clean and process text
            cleaned_text = re.sub(r'\s+', ' ', text.strip())
            
            # Split into sentences for analysis
            sentences = [s.strip() for s in cleaned_text.split('.') if s.strip()]
            
            # Extract basic metrics
            words = cleaned_text.split()
            word_count = len(words)
            sentence_count = len(sentences)
            avg_sentence_length = word_count / max(sentence_count, 1)
            
            content = {
                'title': 'Text Sample',
                'description': 'Content provided as text sample',
                'main_content': cleaned_text,
                'headings': [],
                'links': [],
                'images': [],
                'meta_tags': {},
                'metrics': {
                    'word_count': word_count,
                    'sentence_count': sentence_count,
                    'avg_sentence_length': avg_sentence_length,
                    'unique_words': len(set(words)),
                    'content_length': len(cleaned_text)
                }
            }
            
            logger.info("[WebCrawlerLogic.extract_content_from_text] Successfully processed text content")
            return {
                'success': True,
                'content': content,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = f"Error processing text content: {str(e)}"
            logger.error(f"[WebCrawlerLogic.extract_content_from_text] {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
    
    def validate_crawl_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate web crawl request data.
        
        Args:
            request_data (Dict): Request data to validate
            
        Returns:
            Dict: Validation results
        """
        try:
            logger.info("[WebCrawlerLogic.validate_crawl_request] Validating request")
            
            errors = []
            
            # Check for required fields
            url = request_data.get('url', '')
            text_sample = request_data.get('text_sample', '')
            
            if not url and not text_sample:
                errors.append("Either URL or text sample is required")
            
            if url and not self._validate_url(url):
                errors.append("Invalid URL format")
            
            if text_sample and len(text_sample) < 50:
                errors.append("Text sample must be at least 50 characters")
            
            if text_sample and len(text_sample) > 10000:
                errors.append("Text sample is too long (max 10,000 characters)")
            
            if errors:
                return {
                    'valid': False,
                    'errors': errors
                }
            
            logger.info("[WebCrawlerLogic.validate_crawl_request] Request validation successful")
            return {
                'valid': True,
                'url': url,
                'text_sample': text_sample
            }
            
        except Exception as e:
            logger.error(f"[WebCrawlerLogic.validate_crawl_request] Validation error: {str(e)}")
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"]
            }
    
    def get_crawl_metrics(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate metrics for crawled content.
        
        Args:
            content (Dict): Content to analyze
            
        Returns:
            Dict: Content metrics
        """
        try:
            logger.info("[WebCrawlerLogic.get_crawl_metrics] Calculating content metrics")
            
            main_content = content.get('main_content', '')
            title = content.get('title', '')
            description = content.get('description', '')
            headings = content.get('headings', [])
            links = content.get('links', [])
            images = content.get('images', [])
            
            # Calculate metrics
            words = main_content.split()
            sentences = [s.strip() for s in main_content.split('.') if s.strip()]
            
            metrics = {
                'word_count': len(words),
                'sentence_count': len(sentences),
                'avg_sentence_length': len(words) / max(len(sentences), 1),
                'unique_words': len(set(words)),
                'content_length': len(main_content),
                'title_length': len(title),
                'description_length': len(description),
                'heading_count': len(headings),
                'link_count': len(links),
                'image_count': len(images),
                'readability_score': self._calculate_readability(main_content),
                'content_density': len(set(words)) / max(len(words), 1)
            }
            
            logger.info("[WebCrawlerLogic.get_crawl_metrics] Metrics calculated successfully")
            return {
                'success': True,
                'metrics': metrics
            }
            
        except Exception as e:
            logger.error(f"[WebCrawlerLogic.get_crawl_metrics] Error calculating metrics: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _calculate_readability(self, text: str) -> float:
        """
        Calculate a simple readability score.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            float: Readability score (0-1)
        """
        try:
            if not text:
                return 0.0
            
            words = text.split()
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            
            if not sentences:
                return 0.0
            
            # Simple Flesch Reading Ease approximation
            avg_sentence_length = len(words) / len(sentences)
            avg_word_length = sum(len(word) for word in words) / len(words)
            
            # Normalize to 0-1 scale
            readability = max(0, min(1, (100 - avg_sentence_length - avg_word_length) / 100))
            
            return round(readability, 2)
            
        except Exception as e:
            logger.error(f"[WebCrawlerLogic._calculate_readability] Error: {str(e)}")
            return 0.5 