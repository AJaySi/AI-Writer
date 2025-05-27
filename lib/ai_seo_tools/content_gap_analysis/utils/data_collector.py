"""
Data collector utility for content gap analysis.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Any

class DataCollector:
    """
    Collects and processes website data for analysis.
    """
    
    def __init__(self):
        """Initialize the data collector."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def collect(self, url: str) -> Dict[str, Any]:
        """
        Collect website data for analysis.
        
        Args:
            url (str): The URL to collect data from
            
        Returns:
            dict: Collected website data
        """
        try:
            # Fetch webpage content
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract relevant data
            data = {
                'url': url,
                'title': self._extract_title(soup),
                'meta_description': self._extract_meta_description(soup),
                'headings': self._extract_headings(soup),
                'content': self._extract_content(soup),
                'links': self._extract_links(soup),
                'images': self._extract_images(soup)
            }
            
            return data
            
        except Exception as e:
            return {
                'error': str(e),
                'url': url
            }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        title = soup.find('title')
        return title.text if title else ''
    
    def _extract_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description."""
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta.get('content', '') if meta else ''
    
    def _extract_headings(self, soup: BeautifulSoup) -> Dict[str, list]:
        """Extract all headings."""
        headings = {}
        for i in range(1, 7):
            tags = soup.find_all(f'h{i}')
            headings[f'h{i}'] = [tag.text.strip() for tag in tags]
        return headings
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content."""
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def _extract_links(self, soup: BeautifulSoup) -> list:
        """Extract all links."""
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                links.append({
                    'url': href,
                    'text': link.text.strip()
                })
        return links
    
    def _extract_images(self, soup: BeautifulSoup) -> list:
        """Extract all images."""
        images = []
        for img in soup.find_all('img'):
            images.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            })
        return images 