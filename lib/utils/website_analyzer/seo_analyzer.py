"""SEO analyzer module with AI integration."""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse
import openai
from loguru import logger
import os
from dotenv import load_dotenv
from .models import (
    SEOAnalysisResult,
    MetaTagAnalysis,
    ContentAnalysis,
    SEORecommendation
)

def extract_content(url: str) -> Tuple[Optional[str], Optional[BeautifulSoup], List[str]]:
    """Extract content from URL."""
    errors = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return response.text, soup, errors
    except requests.RequestException as e:
        error_msg = f"Error fetching URL: {str(e)}"
        logger.error(error_msg)
        errors.append(error_msg)
        return None, None, errors

def analyze_meta_tags(soup: BeautifulSoup) -> MetaTagAnalysis:
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

def analyze_content_with_ai(content: str) -> Tuple[ContentAnalysis, List[SEORecommendation]]:
    """Analyze content using AI."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
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

        # Get AI analysis
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an SEO expert analyzing website content."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        # Parse AI response
        analysis = response.choices[0].message.content
        
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
        return ContentAnalysis(
            word_count=len(content.split()),
            headings_structure={},
            keyword_density={},
            readability_score=0,
            content_quality_score=0
        ), []

def analyze_seo(url: str) -> SEOAnalysisResult:
    """Main function to analyze website SEO."""
    errors = []
    warnings = []
    
    # Validate URL
    try:
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            errors.append("Invalid URL format")
            raise ValueError("Invalid URL format")
    except Exception as e:
        errors.append(f"URL parsing error: {str(e)}")
        return SEOAnalysisResult(
            url=url,
            analyzed_at=datetime.now(),
            overall_score=0,
            meta_tags=None,
            content=None,
            recommendations=[],
            errors=errors,
            warnings=warnings,
            success=False
        )

    # Extract content
    content, soup, extract_errors = extract_content(url)
    errors.extend(extract_errors)
    
    if not content or not soup:
        return SEOAnalysisResult(
            url=url,
            analyzed_at=datetime.now(),
            overall_score=0,
            meta_tags=None,
            content=None,
            recommendations=[],
            errors=errors,
            warnings=warnings,
            success=False
        )

    try:
        # Analyze meta tags
        meta_analysis = analyze_meta_tags(soup)
        
        # Analyze content with AI
        content_analysis, recommendations = analyze_content_with_ai(content)
        
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

        return SEOAnalysisResult(
            url=url,
            analyzed_at=datetime.now(),
            overall_score=overall_score,
            meta_tags=meta_analysis,
            content=content_analysis,
            recommendations=recommendations,
            errors=errors,
            warnings=warnings,
            success=True
        )

    except Exception as e:
        error_msg = f"Error in SEO analysis: {str(e)}"
        logger.error(error_msg)
        errors.append(error_msg)
        return SEOAnalysisResult(
            url=url,
            analyzed_at=datetime.now(),
            overall_score=0,
            meta_tags=None,
            content=None,
            recommendations=[],
            errors=errors,
            warnings=warnings,
            success=False
        ) 