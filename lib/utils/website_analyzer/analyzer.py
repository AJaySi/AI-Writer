"""Website scraping and AI analysis module."""

import asyncio
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import streamlit as st
import re
from loguru import logger
from ...web_crawlers.async_web_crawler import AsyncWebCrawlerService
from ...gpt_providers.text_generation.main_text_generation import llm_text_gen
import os
import sys
import logging
import json
from datetime import datetime
import requests
import ssl
import socket
import whois
import dns.resolver
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/website_analyzer.log')
    ]
)
logger = logging.getLogger(__name__)

def analyze_website(url: str) -> Dict:
    """
    Analyze a website and return comprehensive results.
    
    Args:
        url (str): The URL to analyze
        
    Returns:
        Dict: Analysis results including various metrics and checks
    """
    logger.info(f"Starting website analysis for URL: {url}")
    try:
        analyzer = WebsiteAnalyzer()
        results = analyzer.analyze_website(url)
        
        # Add success status to results
        if "error" in results:
            return {
                "success": False,
                "error": results["error"]
            }
        
        # Add success status and wrap results
        return {
            "success": True,
            "data": results
        }
    except Exception as e:
        logger.error(f"Error in analyze_website: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }

class WebsiteAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        logger.info("WebsiteAnalyzer initialized")

    def analyze_website(self, url: str) -> Dict:
        """
        Perform comprehensive analysis of a website.
        
        Args:
            url (str): The URL to analyze
            
        Returns:
            Dict: Analysis results including various metrics and checks
        """
        logger.info(f"Starting analysis for URL: {url}")
        try:
            # Validate URL
            if not self._validate_url(url):
                logger.error(f"Invalid URL format: {url}")
                return {"error": "Invalid URL format"}

            # Basic URL parsing
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            logger.debug(f"Parsed domain: {domain}")

            # Initialize results dictionary
            results = {
                "url": url,
                "domain": domain,
                "timestamp": datetime.now().isoformat(),
                "analysis": {}
            }

            # Perform various analyses
            with ThreadPoolExecutor(max_workers=4) as executor:
                # Basic website info
                basic_info = executor.submit(self._get_basic_info, url).result()
                results["analysis"]["basic_info"] = basic_info

                # SSL/TLS info
                ssl_info = executor.submit(self._check_ssl, domain).result()
                results["analysis"]["ssl_info"] = ssl_info

                # DNS info
                dns_info = executor.submit(self._check_dns, domain).result()
                results["analysis"]["dns_info"] = dns_info

                # WHOIS info
                whois_info = executor.submit(self._get_whois_info, domain).result()
                results["analysis"]["whois_info"] = whois_info

                # Content analysis
                content_info = executor.submit(self._analyze_content, url).result()
                results["analysis"]["content_info"] = content_info

                # Performance metrics
                performance = executor.submit(self._check_performance, url).result()
                results["analysis"]["performance"] = performance

            logger.info(f"Analysis completed successfully for {url}")
            return results

        except Exception as e:
            logger.error(f"Error during website analysis: {str(e)}", exc_info=True)
            return {"error": str(e)}

    def _validate_url(self, url: str) -> bool:
        """Validate URL format."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception as e:
            logger.error(f"URL validation error: {str(e)}")
            return False

    def _get_basic_info(self, url: str) -> Dict:
        """Get basic website information."""
        logger.debug(f"Getting basic info for {url}")
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return {
                "status_code": response.status_code,
                "content_type": response.headers.get('content-type', ''),
                "title": soup.title.string if soup.title else '',
                "meta_description": self._get_meta_description(soup),
                "headers": dict(response.headers),
                "robots_txt": self._get_robots_txt(url),
                "sitemap": self._get_sitemap(url)
            }
        except Exception as e:
            logger.error(f"Error getting basic info: {str(e)}", exc_info=True)
            return {"error": str(e)}

    def _check_ssl(self, domain: str) -> Dict:
        """Check SSL/TLS certificate information."""
        logger.debug(f"Checking SSL for {domain}")
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        "has_ssl": True,
                        "issuer": dict(x[0] for x in cert['issuer']),
                        "expiry": datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').isoformat(),
                        "version": cert['version'],
                        "subject": dict(x[0] for x in cert['subject'])
                    }
        except Exception as e:
            logger.error(f"SSL check error: {str(e)}", exc_info=True)
            return {"has_ssl": False, "error": str(e)}

    def _check_dns(self, domain: str) -> Dict:
        """Check DNS records."""
        logger.debug(f"Checking DNS for {domain}")
        try:
            records = {}
            for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT']:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    records[record_type] = [str(rdata) for rdata in answers]
                except dns.resolver.NoAnswer:
                    records[record_type] = []
                except Exception as e:
                    logger.warning(f"Error resolving {record_type} record: {str(e)}")
                    records[record_type] = []
            return records
        except Exception as e:
            logger.error(f"DNS check error: {str(e)}", exc_info=True)
            return {"error": str(e)}

    def _get_whois_info(self, domain: str) -> Dict:
        """Get WHOIS information for a domain."""
        try:
            w = whois.whois(domain)
            
            def format_date(date_value):
                if isinstance(date_value, list):
                    return date_value[0].isoformat() if date_value else 'Unknown'
                return date_value.isoformat() if date_value else 'Unknown'
            
            return {
                'registrar': w.registrar if hasattr(w, 'registrar') else 'Unknown',
                'creation_date': format_date(w.creation_date),
                'expiration_date': format_date(w.expiration_date),
                'updated_date': format_date(w.updated_date) if hasattr(w, 'updated_date') else 'Unknown',
                'name_servers': w.name_servers if hasattr(w, 'name_servers') else [],
                'domain_name': w.domain_name if hasattr(w, 'domain_name') else domain,
                'text': w.text if hasattr(w, 'text') else ''
            }
        except Exception as e:
            logger.error(f"WHOIS check error: {str(e)}")
            return {
                'registrar': 'Unknown',
                'creation_date': 'Unknown',
                'expiration_date': 'Unknown',
                'updated_date': 'Unknown',
                'name_servers': [],
                'domain_name': domain,
                'text': ''
            }

    def _analyze_content(self, url: str) -> Dict:
        """Analyze website content."""
        logger.debug(f"Analyzing content for {url}")
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get all text content
            text_content = soup.get_text()
            
            # Count words
            words = re.findall(r'\w+', text_content.lower())
            word_count = len(words)
            
            # Count headings
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            
            # Count images
            images = soup.find_all('img')
            
            # Count links
            links = soup.find_all('a')
            
            return {
                "word_count": word_count,
                "heading_count": len(headings),
                "image_count": len(images),
                "link_count": len(links),
                "has_meta_description": bool(self._get_meta_description(soup)),
                "has_robots_txt": bool(self._get_robots_txt(url)),
                "has_sitemap": bool(self._get_sitemap(url))
            }
        except Exception as e:
            logger.error(f"Content analysis error: {str(e)}", exc_info=True)
            return {"error": str(e)}

    def _check_performance(self, url: str) -> Dict:
        """Check website performance metrics."""
        logger.debug(f"Checking performance for {url}")
        try:
            start_time = datetime.now()
            response = self.session.get(url, timeout=10)
            end_time = datetime.now()
            
            load_time = (end_time - start_time).total_seconds()
            
            return {
                "load_time": load_time,
                "status_code": response.status_code,
                "content_length": len(response.content),
                "headers": dict(response.headers)
            }
        except Exception as e:
            logger.error(f"Performance check error: {str(e)}", exc_info=True)
            return {"error": str(e)}

    def _get_meta_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract meta description from HTML."""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        return meta_desc.get('content') if meta_desc else None

    def _get_robots_txt(self, url: str) -> Optional[str]:
        """Get robots.txt content."""
        try:
            robots_url = f"{url.rstrip('/')}/robots.txt"
            response = self.session.get(robots_url, timeout=5)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            logger.warning(f"Error fetching robots.txt: {str(e)}")
        return None

    def _get_sitemap(self, url: str) -> Optional[str]:
        """Get sitemap.xml content."""
        try:
            sitemap_url = f"{url.rstrip('/')}/sitemap.xml"
            response = self.session.get(sitemap_url, timeout=5)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            logger.warning(f"Error fetching sitemap.xml: {str(e)}")
        return None