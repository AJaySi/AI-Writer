"""
SEO analyzer utility for content gap analysis.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
from typing import Dict, Any, List, Optional
from ....utils.website_analyzer.analyzer import WebsiteAnalyzer

def analyze_onpage_seo(url: str) -> Dict[str, Any]:
    """
    Analyze on-page SEO elements of a website.
    
    Args:
        url: The URL to analyze
        
    Returns:
        Dictionary containing SEO analysis results
    """
    try:
        # Use the combined website analyzer
        analyzer = WebsiteAnalyzer()
        analysis = analyzer.analyze_website(url)
        
        if not analysis.get('success', False):
            return {
                'error': analysis.get('error', 'Unknown error in SEO analysis'),
                'meta_title': '',
                'meta_description': '',
                'has_robots_txt': False,
                'has_sitemap': False,
                'mobile_friendly': False,
                'load_time': 0
            }
        
        # Extract relevant information from the analysis
        seo_info = analysis['data']['analysis']['seo_info']
        basic_info = analysis['data']['analysis']['basic_info']
        performance = analysis['data']['analysis']['performance']
        
        return {
            'meta_tags': seo_info.get('meta_tags', {}),
            'content': seo_info.get('content', {}),
            'meta_title': basic_info.get('title', ''),
            'meta_description': basic_info.get('meta_description', ''),
            'has_robots_txt': bool(basic_info.get('robots_txt')),
            'has_sitemap': bool(basic_info.get('sitemap')),
            'mobile_friendly': True,  # This would need to be implemented separately
            'load_time': performance.get('load_time', 0)
        }
    except Exception as e:
        return {
            'error': str(e),
            'meta_title': '',
            'meta_description': '',
            'has_robots_txt': False,
            'has_sitemap': False,
            'mobile_friendly': False,
            'load_time': 0
        }

def _analyze_meta_tags(soup: BeautifulSoup) -> Dict[str, Any]:
    """Analyze meta tags of the webpage."""
    meta_tags = {}
    
    # Title tag
    title_tag = soup.find('title')
    if title_tag:
        meta_tags['title'] = title_tag.string.strip()
    
    # Meta description
    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc:
        meta_tags['description'] = meta_desc.get('content', '').strip()
    
    # Meta keywords
    meta_keywords = soup.find('meta', {'name': 'keywords'})
    if meta_keywords:
        meta_tags['keywords'] = meta_keywords.get('content', '').strip()
    
    # Open Graph tags
    og_tags = {}
    for tag in soup.find_all('meta', property=re.compile(r'^og:')):
        og_tags[tag['property']] = tag.get('content', '')
    meta_tags['og_tags'] = og_tags
    
    # Twitter Card tags
    twitter_tags = {}
    for tag in soup.find_all('meta', name=re.compile(r'^twitter:')):
        twitter_tags[tag['name']] = tag.get('content', '')
    meta_tags['twitter_tags'] = twitter_tags
    
    return meta_tags

def _analyze_headings(soup: BeautifulSoup) -> Dict[str, Any]:
    """Analyze heading structure of the webpage."""
    headings = {
        'h1': [],
        'h2': [],
        'h3': [],
        'h4': [],
        'h5': [],
        'h6': []
    }
    
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        for heading in soup.find_all(tag):
            headings[tag].append(heading.get_text().strip())
    
    return headings

def _analyze_content(soup: BeautifulSoup) -> Dict[str, Any]:
    """Analyze main content of the webpage."""
    # Find main content
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|article'))
    
    if not main_content:
        return {
            'word_count': 0,
            'paragraph_count': 0,
            'content': ''
        }
    
    # Get text content
    content = main_content.get_text()
    
    # Count words and paragraphs
    words = content.split()
    paragraphs = main_content.find_all('p')
    
    return {
        'word_count': len(words),
        'paragraph_count': len(paragraphs),
        'content': content
    }

def _analyze_links(soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
    """Analyze links on the webpage."""
    links = {
        'internal': [],
        'external': [],
        'broken': []
    }
    
    base_domain = urlparse(base_url).netloc
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        
        # Handle relative URLs
        if not href.startswith(('http://', 'https://')):
            href = urljoin(base_url, href)
        
        # Categorize link
        if urlparse(href).netloc == base_domain:
            links['internal'].append({
                'url': href,
                'text': link.get_text().strip(),
                'title': link.get('title', '')
            })
        else:
            links['external'].append({
                'url': href,
                'text': link.get_text().strip(),
                'title': link.get('title', '')
            })
    
    return links

def _analyze_images(soup: BeautifulSoup) -> Dict[str, Any]:
    """Analyze images on the webpage."""
    images = []
    
    for img in soup.find_all('img'):
        image_data = {
            'src': img.get('src', ''),
            'alt': img.get('alt', ''),
            'title': img.get('title', ''),
            'width': img.get('width', ''),
            'height': img.get('height', ''),
            'has_alt': bool(img.get('alt')),
            'has_title': bool(img.get('title')),
            'has_dimensions': bool(img.get('width') and img.get('height'))
        }
        images.append(image_data)
    
    return {
        'total': len(images),
        'with_alt': sum(1 for img in images if img['has_alt']),
        'with_title': sum(1 for img in images if img['has_title']),
        'with_dimensions': sum(1 for img in images if img['has_dimensions']),
        'images': images
    }

def _check_technical_elements(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """Check technical SEO elements."""
    base_url = urlparse(url)
    domain = base_url.netloc
    
    # Check robots.txt
    robots_url = f"{base_url.scheme}://{domain}/robots.txt"
    try:
        robots_response = requests.get(robots_url, timeout=5)
        has_robots_txt = robots_response.status_code == 200
    except:
        has_robots_txt = False
    
    # Check sitemap
    sitemap_url = f"{base_url.scheme}://{domain}/sitemap.xml"
    try:
        sitemap_response = requests.get(sitemap_url, timeout=5)
        has_sitemap = sitemap_response.status_code == 200
    except:
        has_sitemap = False
    
    # Check mobile friendliness
    viewport = soup.find('meta', {'name': 'viewport'})
    has_viewport = bool(viewport)
    
    # Check canonical URL
    canonical = soup.find('link', {'rel': 'canonical'})
    has_canonical = bool(canonical)
    
    # Check language
    html_lang = soup.find('html').get('lang', '')
    has_language = bool(html_lang)
    
    return {
        'has_robots_txt': has_robots_txt,
        'has_sitemap': has_sitemap,
        'mobile_friendly': has_viewport,
        'has_canonical': has_canonical,
        'has_language': has_language,
        'language': html_lang
    } 