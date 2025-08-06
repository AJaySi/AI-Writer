"""Website and SEO analysis module."""

import asyncio
from typing import Dict, List, Optional, Tuple
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
from .models import (
    SEOAnalysisResult,
    MetaTagAnalysis,
    ContentAnalysis,
    SEORecommendation
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/website_analyzer.log')
    ]
)

# Create a logger for the website analyzer
logger = logging.getLogger(__name__)

# Create a separate logger for scraping operations
scraping_logger = logging.getLogger('website_analyzer.scraping')
scraping_logger.setLevel(logging.WARNING)

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
                error_msg = f"Invalid URL format: {url}"
                logger.error(error_msg)
                return {
                    "success": False,
                    "error": error_msg,
                    "error_details": {"stage": "url_validation"}
                }

            # Basic URL parsing
            parsed_url = urlparse(url)
            domain = parsed_url.netloc

            # Initialize results dictionary
            results = {
                "url": url,
                "domain": domain,
                "timestamp": datetime.now().isoformat(),
                "analysis": {}
            }

            # Perform various analyses
            with ThreadPoolExecutor(max_workers=4) as executor:
                logger.info("Starting parallel analysis tasks")
                
                # Basic website info
                logger.info("Starting basic info analysis")
                basic_info = executor.submit(self._get_basic_info, url).result()
                if "error" in basic_info:
                    error_msg = f"Basic info analysis failed: {basic_info['error']}"
                    logger.error(error_msg)
                    return {
                        "success": False,
                        "error": error_msg,
                        "error_details": {
                            "stage": "basic_info",
                            "details": basic_info.get("error_details", {})
                        }
                    }
                results["analysis"]["basic_info"] = basic_info

                # SSL/TLS info
                logger.info("Starting SSL analysis")
                ssl_info = executor.submit(self._check_ssl, domain).result()
                results["analysis"]["ssl_info"] = ssl_info

                # DNS info
                logger.info("Starting DNS analysis")
                dns_info = executor.submit(self._check_dns, domain).result()
                results["analysis"]["dns_info"] = dns_info

                # WHOIS info
                logger.info("Starting WHOIS analysis")
                whois_info = executor.submit(self._get_whois_info, domain).result()
                results["analysis"]["whois_info"] = whois_info

                # Content analysis
                logger.info("Starting content analysis")
                content_info = executor.submit(self._analyze_content, url).result()
                if "error" in content_info:
                    error_msg = f"Content analysis failed: {content_info['error']}"
                    logger.error(error_msg)
                    return {
                        "success": False,
                        "error": error_msg,
                        "error_details": {
                            "stage": "content_analysis",
                            "details": content_info.get("error_details", {})
                        }
                    }
                results["analysis"]["content_info"] = content_info

                # Performance metrics
                logger.info("Starting performance analysis")
                performance = executor.submit(self._check_performance, url).result()
                if "error" in performance:
                    error_msg = f"Performance analysis failed: {performance['error']}"
                    logger.error(error_msg)
                    return {
                        "success": False,
                        "error": error_msg,
                        "error_details": {
                            "stage": "performance_analysis",
                            "details": performance.get("error_details", {})
                        }
                    }
                results["analysis"]["performance"] = performance

                # SEO analysis
                logger.info("Starting SEO analysis")
                seo_analysis = executor.submit(self._analyze_seo, url).result()
                if "error" in seo_analysis:
                    error_msg = f"SEO analysis failed: {seo_analysis['error']}"
                    logger.error(error_msg)
                    return {
                        "success": False,
                        "error": error_msg,
                        "error_details": {
                            "stage": "seo_analysis",
                            "details": seo_analysis.get("error_details", {})
                        }
                    }
                results["analysis"]["seo_info"] = seo_analysis

            logger.info(f"Analysis completed successfully for {url}")
            logger.debug(f"Final results: {json.dumps(results, indent=2)}")
            return {
                "success": True,
                "data": results
            }

        except Exception as e:
            error_msg = f"Error during website analysis: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "success": False,
                "error": error_msg,
                "error_details": {
                    "type": type(e).__name__,
                    "traceback": str(e.__traceback__)
                }
            }

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
        scraping_logger.debug(f"Getting basic info for {url}")
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
        except requests.exceptions.RequestException as e:
            error_msg = f"Request error in basic info: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "error": error_msg,
                "error_details": {
                    "type": "RequestException",
                    "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None,
                    "url": url
                }
            }
        except Exception as e:
            error_msg = f"Error getting basic info: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "error": error_msg,
                "error_details": {
                    "type": type(e).__name__,
                    "traceback": str(e.__traceback__)
                }
            }

    def _check_ssl(self, domain: str) -> Dict:
        """Check SSL/TLS certificate information."""
        scraping_logger.debug(f"Checking SSL for {domain}")
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
        scraping_logger.debug(f"Checking DNS for {domain}")
        try:
            records = {}
            for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT']:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    records[record_type] = [str(rdata) for rdata in answers]
                except dns.resolver.NoAnswer:
                    records[record_type] = []
                except Exception as e:
                    scraping_logger.warning(f"Error resolving {record_type} record: {str(e)}")
                    records[record_type] = []
            return records
        except Exception as e:
            logger.error(f"DNS check error: {str(e)}", exc_info=True)
            return {"error": str(e)}

    def _get_whois_info(self, domain: str) -> Dict:
        """Get WHOIS information for a domain."""
        scraping_logger.debug(f"Getting WHOIS info for {domain}")
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
        scraping_logger.debug(f"Analyzing content for {url}")
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
            heading_counts = {
                'h1': len(soup.find_all('h1')),
                'h2': len(soup.find_all('h2')),
                'h3': len(soup.find_all('h3')),
                'h4': len(soup.find_all('h4')),
                'h5': len(soup.find_all('h5')),
                'h6': len(soup.find_all('h6'))
            }
            
            # Count images
            images = soup.find_all('img')
            
            # Count links
            links = soup.find_all('a')
            
            # Count paragraphs
            paragraphs = soup.find_all('p')
            
            return {
                "word_count": word_count,
                "heading_count": len(headings),
                "heading_structure": heading_counts,
                "image_count": len(images),
                "link_count": len(links),
                "paragraph_count": len(paragraphs),
                "has_meta_description": bool(self._get_meta_description(soup)),
                "has_robots_txt": bool(self._get_robots_txt(url)),
                "has_sitemap": bool(self._get_sitemap(url))
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error in content analysis: {str(e)}", exc_info=True)
            return {
                "word_count": 0,
                "heading_count": 0,
                "heading_structure": {'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0},
                "image_count": 0,
                "link_count": 0,
                "paragraph_count": 0,
                "has_meta_description": False,
                "has_robots_txt": False,
                "has_sitemap": False,
                "error": str(e)
            }
        except Exception as e:
            logger.error(f"Content analysis error: {str(e)}", exc_info=True)
            return {
                "word_count": 0,
                "heading_count": 0,
                "heading_structure": {'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0},
                "image_count": 0,
                "link_count": 0,
                "paragraph_count": 0,
                "has_meta_description": False,
                "has_robots_txt": False,
                "has_sitemap": False,
                "error": str(e)
            }

    def _check_performance(self, url: str) -> Dict:
        """Check website performance metrics."""
        scraping_logger.debug(f"Checking performance for {url}")
        try:
            start_time = datetime.now()
            response = self.session.get(url, timeout=10)
            end_time = datetime.now()
            
            load_time = (end_time - start_time).total_seconds()
            
            return {
                "load_time": load_time,
                "status_code": response.status_code,
                "content_length": len(response.content),
                "headers": dict(response.headers),
                "response_time": response.elapsed.total_seconds()
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error in performance check: {str(e)}", exc_info=True)
            return {
                "load_time": 0,
                "status_code": 0,
                "content_length": 0,
                "headers": {},
                "response_time": 0,
                "error": str(e)
            }
        except Exception as e:
            logger.error(f"Performance check error: {str(e)}", exc_info=True)
            return {
                "load_time": 0,
                "status_code": 0,
                "content_length": 0,
                "headers": {},
                "response_time": 0,
                "error": str(e)
            }

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
            scraping_logger.warning(f"Error fetching robots.txt: {str(e)}")
        return None

    def _get_sitemap(self, url: str) -> Optional[str]:
        """Get sitemap.xml content."""
        try:
            sitemap_url = f"{url.rstrip('/')}/sitemap.xml"
            response = self.session.get(sitemap_url, timeout=5)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            scraping_logger.warning(f"Error fetching sitemap.xml: {str(e)}")
        return None

    def _analyze_seo(self, url: str) -> Dict:
        """Analyze website SEO."""
        try:
            # Extract content
            content, soup, extract_errors = self._extract_content(url)
            if not content or not soup:
                return {
                    "error": "Failed to extract content",
                    "error_details": {"errors": extract_errors}
                }

            # Analyze meta tags
            meta_analysis = self._analyze_meta_tags(soup)
            
            # Analyze content with AI
            content_analysis, recommendations = self._analyze_content_with_ai(content)
            
            # Calculate overall score
            meta_score = sum([
                1 if meta_analysis.title['status'] == 'good' else 0,
                1 if meta_analysis.description['status'] == 'good' else 0,
                1 if meta_analysis.keywords['status'] == 'good' else 0,
                1 if meta_analysis.has_robots else 0,
                1 if meta_analysis.has_sitemap else 0
            ]) * 20  # Scale to 100

            overall_score = (
                meta_score * 0.3 +  # 30% weight for meta tags
                content_analysis.readability_score * 0.3 +  # 30% weight for readability
                content_analysis.content_quality_score * 0.4  # 40% weight for content quality
            )

            return {
                "overall_score": overall_score,
                "meta_tags": meta_analysis.__dict__,
                "content": content_analysis.__dict__,
                "recommendations": [rec.__dict__ for rec in recommendations]
            }

        except Exception as e:
            error_msg = f"Error in SEO analysis: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "error": error_msg,
                "error_details": {
                    "type": type(e).__name__,
                    "traceback": str(e.__traceback__)
                }
            }

    def _extract_content(self, url: str) -> Tuple[Optional[str], Optional[BeautifulSoup], List[str]]:
        """Extract content from URL."""
        errors = []
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return response.text, soup, errors
        except requests.RequestException as e:
            error_msg = f"Error fetching URL: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
            return None, None, errors

    def _analyze_meta_tags(self, soup: BeautifulSoup) -> MetaTagAnalysis:
        """Analyze meta tags using BeautifulSoup."""
        # Title analysis
        title = soup.title.string if soup.title else ""
        title_analysis = {
            'status': 'good' if title and 30 <= len(title) <= 60 else 'needs_improvement',
            'value': title,
            'recommendation': '' if title and 30 <= len(title) <= 60 else 'Title should be between 30-60 characters'
        }

        # Meta description analysis
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        desc = meta_desc.get('content', '') if meta_desc else ""
        desc_analysis = {
            'status': 'good' if desc and 120 <= len(desc) <= 160 else 'needs_improvement',
            'value': desc,
            'recommendation': '' if desc and 120 <= len(desc) <= 160 else 'Description should be between 120-160 characters'
        }

        # Keywords analysis
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        keywords = meta_keywords.get('content', '') if meta_keywords else ""
        keywords_analysis = {
            'status': 'good' if keywords else 'needs_improvement',
            'value': keywords,
            'recommendation': '' if keywords else 'Add relevant keywords meta tag'
        }

        return MetaTagAnalysis(
            title=title_analysis,
            description=desc_analysis,
            keywords=keywords_analysis,
            has_robots=bool(soup.find('meta', attrs={'name': 'robots'})),
            has_sitemap=bool(soup.find('link', attrs={'rel': 'sitemap'}))
        )

    def _analyze_content_with_ai(self, content: str) -> Tuple[ContentAnalysis, List[SEORecommendation]]:
        """Analyze content using AI."""
        try:
            # Prepare prompt for content analysis
            prompt = f"""Analyze the following webpage content for SEO and provide a structured analysis:
            Content: {content[:4000]}...  # Truncate to avoid token limits
            
            Provide analysis in the following format:
            1. Word count
            2. Heading structure analysis
            3. Keyword density for main topics
            4. Readability score (0-100)
            5. Content quality score (0-100)
            6. List of SEO recommendations with priority (high/medium/low), category, issue, recommendation, and impact
            
            Format the response as JSON."""

            try:
                # Get AI analysis using llm_text_gen
                analysis = llm_text_gen(
                    prompt=prompt,
                    system_prompt="You are an SEO expert analyzing website content.",
                    response_format="json_object"
                )
                
                if not analysis:
                    logger.error("Empty response from AI analysis")
                    return self._get_fallback_analysis(content)
                
                # Create ContentAnalysis object
                content_analysis = ContentAnalysis(
                    word_count=len(content.split()),
                    headings_structure=analysis.get('heading_structure', {}),
                    keyword_density=analysis.get('keyword_density', {}),
                    readability_score=analysis.get('readability_score', 0),
                    content_quality_score=analysis.get('content_quality_score', 0)
                )

                # Create recommendations
                recommendations = [
                    SEORecommendation(
                        priority=rec['priority'],
                        category=rec['category'],
                        issue=rec['issue'],
                        recommendation=rec['recommendation'],
                        impact=rec['impact']
                    )
                    for rec in analysis.get('recommendations', [])
                ]

                return content_analysis, recommendations

            except Exception as e:
                logger.error(f"Error in AI analysis: {str(e)}")
                return self._get_fallback_analysis(content)

        except Exception as e:
            logger.error(f"Error in AI analysis setup: {str(e)}")
            return self._get_fallback_analysis(content)

    def _get_fallback_analysis(self, content: str) -> Tuple[ContentAnalysis, List[SEORecommendation]]:
        """Provide fallback analysis when AI analysis is not available."""
        try:
            # Basic content analysis
            words = content.split()
            word_count = len(words)
            
            # Simple readability score based on word count
            readability_score = min(100, max(0, word_count / 10))
            
            # Basic content quality score
            content_quality_score = min(100, max(0, word_count / 20))
            
            # Create basic recommendations
            recommendations = [
                SEORecommendation(
                    priority="high",
                    category="content",
                    issue="AI analysis unavailable",
                    recommendation="Consider running the analysis again with a valid API key for more detailed insights",
                    impact="Limited analysis capabilities"
                )
            ]
            
            return ContentAnalysis(
                word_count=word_count,
                headings_structure={},
                keyword_density={},
                readability_score=readability_score,
                content_quality_score=content_quality_score
            ), recommendations
            
        except Exception as e:
            logger.error(f"Error in fallback analysis: {str(e)}")
            return ContentAnalysis(
                word_count=0,
                headings_structure={},
                keyword_density={},
                readability_score=0,
                content_quality_score=0
            ), []

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
            error_msg = f"Error in base analysis: {results['error']}"
            logger.error(error_msg)
            logger.error(f"Error details: {json.dumps(results.get('error_details', {}), indent=2)}")
            return {
                "success": False,
                "error": error_msg,
                "error_details": results.get("error_details", {})
            }
        
        # Add success status and wrap results
        logger.info("Analysis completed successfully")
        logger.debug(f"Analysis results: {json.dumps(results, indent=2)}")
        return {
            "success": True,
            "data": results
        }
    except Exception as e:
        error_msg = f"Error in analyze_website: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "success": False,
            "error": error_msg,
            "error_details": {
                "type": type(e).__name__,
                "traceback": str(e.__traceback__)
            }
        }