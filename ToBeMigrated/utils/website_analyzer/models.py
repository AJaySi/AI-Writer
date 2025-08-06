"""Data models for website analysis results."""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class SEORecommendation:
    """A single SEO recommendation."""
    priority: str  # 'high', 'medium', 'low'
    category: str  # 'content', 'technical', 'meta', etc.
    issue: str
    recommendation: str
    impact: str

@dataclass
class MetaTagAnalysis:
    """Analysis of meta tags."""
    title: Dict[str, str]  # {'status': 'good', 'value': 'actual title', 'recommendation': 'suggestion'}
    description: Dict[str, str]
    keywords: Dict[str, str]
    has_robots: bool
    has_sitemap: bool

@dataclass
class ContentAnalysis:
    """Analysis of page content."""
    word_count: int
    headings_structure: Dict[str, int]  # {'h1': 1, 'h2': 3, etc}
    keyword_density: Dict[str, float]
    readability_score: float
    content_quality_score: float

@dataclass
class SEOAnalysisResult:
    """Complete SEO analysis result."""
    url: str
    analyzed_at: datetime
    overall_score: float  # 0-100
    meta_tags: MetaTagAnalysis
    content: ContentAnalysis
    recommendations: List[SEORecommendation]
    errors: List[str]
    warnings: List[str]
    success: bool 