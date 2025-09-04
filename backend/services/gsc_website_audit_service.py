"""
Google Search Console Website Audit Service

A comprehensive, modular service for conducting data-driven website content audits
using Google Search Console APIs. This service provides deep insights into content
performance, identifies optimization opportunities, and delivers actionable recommendations.

Features:
- Core Performance Metrics Analysis (Impressions, Clicks, CTR, Position)
- Granular Page and Query Level Analysis
- Advanced Derived Metrics and Comparisons
- Technical Signals from Multiple GSC APIs
- Content Clustering and Topic Performance
- Automated Audit Report Generation
"""

import os
import asyncio
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import pandas as pd
import numpy as np
from collections import defaultdict
import logging

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from sqlalchemy.orm import Session
from models.social_connections import SocialConnection
from services.oauth_service import oauth_service
from services.logging_service import testing_logger
from services.google_trends_service import google_trends_service, TrendData, SeasonalInsight, TrendComparison
from services.ai_insights_service import ai_insights_service, CombinedAnalysis

logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Enumeration of available GSC metrics."""
    IMPRESSIONS = "impressions"
    CLICKS = "clicks"
    CTR = "ctr"
    POSITION = "position"

class DimensionType(Enum):
    """Enumeration of available GSC dimensions."""
    PAGE = "page"
    QUERY = "query"
    COUNTRY = "country"
    DEVICE = "device"
    DATE = "date"

class PerformanceCategory(Enum):
    """Content performance categories."""
    TOP_PERFORMER = "top_performer"
    HIGH_POTENTIAL = "high_potential"
    STRIKING_DISTANCE = "striking_distance"
    UNDERPERFORMER = "underperformer"
    LOW_HANGING_FRUIT = "low_hanging_fruit"
    CONTENT_DECAY = "content_decay"

@dataclass
class AuditMetrics:
    """Data class for core audit metrics."""
    impressions: int = 0
    clicks: int = 0
    ctr: float = 0.0
    position: float = 0.0
    
    def __post_init__(self):
        """Calculate CTR if not provided."""
        if self.ctr == 0.0 and self.impressions > 0:
            self.ctr = (self.clicks / self.impressions) * 100

@dataclass
class PagePerformance:
    """Data class for page-level performance data."""
    url: str
    metrics: AuditMetrics
    category: PerformanceCategory
    recommendations: List[str]
    queries: List[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'url': self.url,
            'metrics': asdict(self.metrics),
            'category': self.category.value,
            'recommendations': self.recommendations,
            'queries': self.queries or []
        }

@dataclass
class QueryPerformance:
    """Data class for query-level performance data."""
    query: str
    metrics: AuditMetrics
    pages: List[str]
    intent_type: str = "unknown"
    opportunity_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'query': self.query,
            'metrics': asdict(self.metrics),
            'pages': self.pages,
            'intent_type': self.intent_type,
            'opportunity_score': self.opportunity_score
        }

@dataclass
class ContentCluster:
    """Data class for content clustering analysis."""
    topic: str
    pages: List[str]
    total_metrics: AuditMetrics
    avg_metrics: AuditMetrics
    performance_score: float
    recommendations: List[str]

@dataclass
class AuditReport:
    """Comprehensive audit report data structure."""
    site_url: str
    audit_date: datetime
    date_range: Dict[str, str]
    
    # Summary metrics
    total_pages: int
    total_queries: int
    total_impressions: int
    total_clicks: int
    average_ctr: float
    average_position: float
    
    # Performance analysis
    top_performers: List[PagePerformance]
    underperformers: List[PagePerformance]
    low_hanging_fruit: List[PagePerformance]
    striking_distance: List[QueryPerformance]
    content_decay: List[PagePerformance]
    
    # Advanced insights
    query_opportunities: List[QueryPerformance]
    content_clusters: List[ContentCluster]
    technical_issues: Dict[str, Any]
    
    # Trends and comparisons
    performance_trends: Dict[str, Any]
    yoy_comparison: Optional[Dict[str, Any]] = None
    mom_comparison: Optional[Dict[str, Any]] = None
    
    # Enhanced with Google Trends and AI insights
    trends_data: List[TrendData] = None
    seasonal_insights: List[SeasonalInsight] = None
    trend_comparisons: List[TrendComparison] = None
    ai_analysis: Optional[CombinedAnalysis] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary for API response."""
        return {
            'site_url': self.site_url,
            'audit_date': self.audit_date.isoformat(),
            'date_range': self.date_range,
            'summary': {
                'total_pages': self.total_pages,
                'total_queries': self.total_queries,
                'total_impressions': self.total_impressions,
                'total_clicks': self.total_clicks,
                'average_ctr': self.average_ctr,
                'average_position': self.average_position
            },
            'performance_analysis': {
                'top_performers': [p.to_dict() for p in self.top_performers],
                'underperformers': [p.to_dict() for p in self.underperformers],
                'low_hanging_fruit': [p.to_dict() for p in self.low_hanging_fruit],
                'striking_distance': [q.to_dict() for q in self.striking_distance],
                'content_decay': [p.to_dict() for p in self.content_decay]
            },
            'advanced_insights': {
                'query_opportunities': [q.to_dict() for q in self.query_opportunities],
                'content_clusters': [asdict(c) for c in self.content_clusters],
                'technical_issues': self.technical_issues
            },
            'trends': {
                'performance_trends': self.performance_trends,
                'yoy_comparison': self.yoy_comparison,
                'mom_comparison': self.mom_comparison
            },
            'google_trends': {
                'trends_data': [t.to_dict() for t in self.trends_data] if self.trends_data else [],
                'seasonal_insights': [s.to_dict() for s in self.seasonal_insights] if self.seasonal_insights else [],
                'trend_comparisons': [c.to_dict() for c in self.trend_comparisons] if self.trend_comparisons else []
            },
            'ai_insights': self.ai_analysis.to_dict() if self.ai_analysis else None
        }

class GSCWebsiteAuditService:
    """
    Comprehensive Google Search Console Website Audit Service.
    
    This service provides modular, data-driven website content auditing
    capabilities using Google Search Console APIs.
    """
    
    def __init__(self):
        self.row_limit = 25000  # GSC API limit
        self.performance_thresholds = {
            'high_ctr': 5.0,
            'low_ctr': 2.0,
            'high_position': 3.0,
            'striking_distance_start': 11,
            'striking_distance_end': 20,
            'low_impressions': 10,
            'min_clicks_top_performer': 50
        }
        
    async def conduct_comprehensive_audit(
        self,
        connection: SocialConnection,
        site_url: str,
        start_date: str,
        end_date: str,
        db: Session,
        include_comparisons: bool = True,
        include_trends: bool = True,
        include_ai_insights: bool = True
    ) -> AuditReport:
        """
        Conduct a comprehensive website audit using GSC data.
        
        Args:
            connection: GSC connection object
            site_url: Website URL to audit
            start_date: Start date for analysis (YYYY-MM-DD)
            end_date: End date for analysis (YYYY-MM-DD)
            db: Database session
            include_comparisons: Whether to include YoY/MoM comparisons
            include_trends: Whether to include Google Trends analysis
            include_ai_insights: Whether to include AI-generated insights
            
        Returns:
            Complete audit report with all insights and recommendations
        """
        logger.info(f"Starting comprehensive audit for {site_url}")
        testing_logger.info_connection_event(
            "audit_started", "google_search_console", connection.user_id,
            {"site_url": site_url, "date_range": f"{start_date} to {end_date}"}
        )
        
        try:
            # Get GSC service
            service = await self._get_gsc_service(connection, db)
            
            # Core data collection
            logger.info("Collecting core performance data...")
            page_data = await self._get_page_performance_data(
                service, site_url, start_date, end_date
            )
            query_data = await self._get_query_performance_data(
                service, site_url, start_date, end_date
            )
            
            # Advanced analysis
            logger.info("Performing advanced analysis...")
            page_analysis = await self._analyze_page_performance(page_data, query_data)
            query_analysis = await self._analyze_query_opportunities(query_data, page_data)
            content_clusters = await self._analyze_content_clusters(page_data, site_url)
            
            # Technical signals
            logger.info("Collecting technical signals...")
            technical_issues = await self._get_technical_signals(service, site_url)
            
            # Performance trends
            logger.info("Analyzing performance trends...")
            trends = await self._analyze_performance_trends(
                service, site_url, start_date, end_date
            )
            
            # Comparisons (if requested)
            yoy_comparison = None
            mom_comparison = None
            if include_comparisons:
                logger.info("Generating comparison data...")
                yoy_comparison = await self._get_yoy_comparison(
                    service, site_url, start_date, end_date
                )
                mom_comparison = await self._get_mom_comparison(
                    service, site_url, start_date, end_date
                )
            
            # Calculate summary metrics
            summary_metrics = self._calculate_summary_metrics(page_data, query_data)
            
            # Enhanced Google Trends Analysis
            trends_data = []
            seasonal_insights = []
            trend_comparisons = []
            ai_analysis = None
            
            if include_trends:
                logger.info("Collecting Google Trends data...")
                trends_data, seasonal_insights, trend_comparisons = await self._get_trends_analysis(
                    query_analysis['all_queries'][:20], page_analysis['all_pages'][:20]
                )
            
            # AI-powered insights
            if include_ai_insights and (trends_data or not include_trends):
                logger.info("Generating AI insights...")
                try:
                    # Create a temporary report for AI analysis
                    temp_report = AuditReport(
                        site_url=site_url,
                        audit_date=datetime.utcnow(),
                        date_range={"start": start_date, "end": end_date},
                        total_pages=len(page_analysis['all_pages']),
                        total_queries=len(query_analysis['all_queries']),
                        total_impressions=summary_metrics['total_impressions'],
                        total_clicks=summary_metrics['total_clicks'],
                        average_ctr=summary_metrics['average_ctr'],
                        average_position=summary_metrics['average_position'],
                        top_performers=page_analysis['top_performers'],
                        underperformers=page_analysis['underperformers'],
                        low_hanging_fruit=page_analysis['low_hanging_fruit'],
                        striking_distance=query_analysis['striking_distance'],
                        content_decay=page_analysis['content_decay'],
                        query_opportunities=query_analysis['opportunities'],
                        content_clusters=content_clusters,
                        technical_issues=technical_issues,
                        performance_trends=trends,
                        yoy_comparison=yoy_comparison,
                        mom_comparison=mom_comparison
                    )
                    
                    ai_analysis = await ai_insights_service.generate_comprehensive_insights(
                        gsc_report=temp_report,
                        trends_data=trends_data,
                        seasonal_insights=seasonal_insights,
                        trend_comparisons=trend_comparisons
                    )
                except Exception as e:
                    logger.warning(f"AI insights generation failed: {e}")
                    ai_analysis = None
            
            # Generate comprehensive report
            report = AuditReport(
                site_url=site_url,
                audit_date=datetime.utcnow(),
                date_range={"start": start_date, "end": end_date},
                
                # Summary
                total_pages=len(page_analysis['all_pages']),
                total_queries=len(query_analysis['all_queries']),
                total_impressions=summary_metrics['total_impressions'],
                total_clicks=summary_metrics['total_clicks'],
                average_ctr=summary_metrics['average_ctr'],
                average_position=summary_metrics['average_position'],
                
                # Performance categories
                top_performers=page_analysis['top_performers'],
                underperformers=page_analysis['underperformers'],
                low_hanging_fruit=page_analysis['low_hanging_fruit'],
                striking_distance=query_analysis['striking_distance'],
                content_decay=page_analysis['content_decay'],
                
                # Advanced insights
                query_opportunities=query_analysis['opportunities'],
                content_clusters=content_clusters,
                technical_issues=technical_issues,
                
                # Trends and comparisons
                performance_trends=trends,
                yoy_comparison=yoy_comparison,
                mom_comparison=mom_comparison,
                
                # Enhanced insights
                trends_data=trends_data,
                seasonal_insights=seasonal_insights,
                trend_comparisons=trend_comparisons,
                ai_analysis=ai_analysis
            )
            
            logger.info(f"Audit completed successfully for {site_url}")
            testing_logger.info_connection_event(
                "audit_completed", "google_search_console", connection.user_id,
                {"site_url": site_url, "total_pages": report.total_pages}
            )
            
            return report
            
        except Exception as e:
            logger.error(f"Audit failed for {site_url}: {str(e)}")
            testing_logger.error_platform_api(
                "google_search_console", "audit", e,
                {"site_url": site_url, "user_id": connection.user_id}
            )
            raise

    async def _get_gsc_service(self, connection: SocialConnection, db: Session):
        """Get authenticated GSC service client."""
        access_token = oauth_service.get_valid_token(connection, db)
        if not access_token:
            raise ValueError("No valid access token available for GSC")
        
        credentials = Credentials(
            token=access_token,
            refresh_token=oauth_service.decrypt_token(connection.refresh_token) if connection.refresh_token else None,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            client_secret=os.getenv('GOOGLE_CLIENT_SECRET')
        )
        
        return build('searchconsole', 'v1', credentials=credentials)

    async def _get_page_performance_data(
        self,
        service,
        site_url: str,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve page-level performance data from GSC.
        
        Returns:
            List of page performance dictionaries
        """
        logger.debug(f"Fetching page performance data for {site_url}")
        
        request_body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['page'],
            'rowLimit': self.row_limit
        }
        
        try:
            response = service.searchanalytics().query(
                siteUrl=site_url,
                body=request_body
            ).execute()
            
            pages_data = []
            for row in response.get('rows', []):
                pages_data.append({
                    'page': row['keys'][0],
                    'impressions': row.get('impressions', 0),
                    'clicks': row.get('clicks', 0),
                    'ctr': row.get('ctr', 0) * 100,  # Convert to percentage
                    'position': row.get('position', 0)
                })
            
            logger.debug(f"Retrieved {len(pages_data)} pages")
            return pages_data
            
        except HttpError as e:
            logger.error(f"Error fetching page data: {e}")
            raise

    async def _get_query_performance_data(
        self,
        service,
        site_url: str,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Retrieve query-level performance data from GSC.
        
        Returns:
            List of query performance dictionaries
        """
        logger.debug(f"Fetching query performance data for {site_url}")
        
        request_body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['query'],
            'rowLimit': self.row_limit
        }
        
        try:
            response = service.searchanalytics().query(
                siteUrl=site_url,
                body=request_body
            ).execute()
            
            queries_data = []
            for row in response.get('rows', []):
                queries_data.append({
                    'query': row['keys'][0],
                    'impressions': row.get('impressions', 0),
                    'clicks': row.get('clicks', 0),
                    'ctr': row.get('ctr', 0) * 100,
                    'position': row.get('position', 0)
                })
            
            logger.debug(f"Retrieved {len(queries_data)} queries")
            return queries_data
            
        except HttpError as e:
            logger.error(f"Error fetching query data: {e}")
            raise

    async def _get_query_page_mapping(
        self,
        service,
        site_url: str,
        start_date: str,
        end_date: str
    ) -> Dict[str, List[str]]:
        """
        Get mapping between queries and pages.
        
        Returns:
            Dictionary mapping queries to their associated pages
        """
        logger.debug("Fetching query-page mapping")
        
        request_body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['query', 'page'],
            'rowLimit': self.row_limit
        }
        
        try:
            response = service.searchanalytics().query(
                siteUrl=site_url,
                body=request_body
            ).execute()
            
            query_page_map = defaultdict(list)
            for row in response.get('rows', []):
                query = row['keys'][0]
                page = row['keys'][1]
                query_page_map[query].append(page)
            
            return dict(query_page_map)
            
        except HttpError as e:
            logger.error(f"Error fetching query-page mapping: {e}")
            return {}

    async def _analyze_page_performance(
        self,
        page_data: List[Dict[str, Any]],
        query_data: List[Dict[str, Any]]
    ) -> Dict[str, List[PagePerformance]]:
        """
        Analyze page performance and categorize pages.
        
        Returns:
            Dictionary with categorized page performance data
        """
        logger.debug("Analyzing page performance")
        
        all_pages = []
        top_performers = []
        underperformers = []
        low_hanging_fruit = []
        content_decay = []
        
        # Sort pages by clicks for analysis
        sorted_pages = sorted(page_data, key=lambda x: x['clicks'], reverse=True)
        
        for page_info in sorted_pages:
            metrics = AuditMetrics(
                impressions=page_info['impressions'],
                clicks=page_info['clicks'],
                ctr=page_info['ctr'],
                position=page_info['position']
            )
            
            # Categorize page performance
            category, recommendations = self._categorize_page_performance(metrics)
            
            page_performance = PagePerformance(
                url=page_info['page'],
                metrics=metrics,
                category=category,
                recommendations=recommendations
            )
            
            all_pages.append(page_performance)
            
            # Add to specific categories
            if category == PerformanceCategory.TOP_PERFORMER:
                top_performers.append(page_performance)
            elif category == PerformanceCategory.UNDERPERFORMER:
                underperformers.append(page_performance)
            elif category == PerformanceCategory.LOW_HANGING_FRUIT:
                low_hanging_fruit.append(page_performance)
            elif category == PerformanceCategory.CONTENT_DECAY:
                content_decay.append(page_performance)
        
        return {
            'all_pages': all_pages,
            'top_performers': top_performers[:20],  # Top 20
            'underperformers': underperformers[:50],  # Bottom 50
            'low_hanging_fruit': low_hanging_fruit[:30],  # Top 30 opportunities
            'content_decay': content_decay[:25]  # Top 25 decay candidates
        }

    def _categorize_page_performance(
        self,
        metrics: AuditMetrics
    ) -> Tuple[PerformanceCategory, List[str]]:
        """
        Categorize a page's performance and generate recommendations.
        
        Returns:
            Tuple of (category, recommendations)
        """
        recommendations = []
        
        # Top Performer: High clicks and good position
        if (metrics.clicks >= self.performance_thresholds['min_clicks_top_performer'] and
            metrics.position <= self.performance_thresholds['high_position']):
            recommendations.extend([
                "Monitor for content decay and maintain freshness",
                "Consider expanding content to capture more related queries",
                "Use as template for other content creation"
            ])
            return PerformanceCategory.TOP_PERFORMER, recommendations
        
        # Low Hanging Fruit: High impressions but low CTR
        if (metrics.impressions > 100 and
            metrics.ctr < self.performance_thresholds['low_ctr']):
            recommendations.extend([
                "Optimize title tag to be more compelling",
                "Improve meta description to increase click appeal",
                "Consider adding structured data for rich snippets",
                "Test different SERP snippet approaches"
            ])
            return PerformanceCategory.LOW_HANGING_FRUIT, recommendations
        
        # Underperformer: Low impressions and clicks
        if (metrics.impressions < self.performance_thresholds['low_impressions'] and
            metrics.clicks < 5):
            recommendations.extend([
                "Review keyword targeting and content relevance",
                "Check for technical SEO issues (indexing, crawlability)",
                "Consider content consolidation or removal",
                "Improve internal linking to this page"
            ])
            return PerformanceCategory.UNDERPERFORMER, recommendations
        
        # High Potential: Good impressions, room for improvement
        if metrics.impressions > 500 and metrics.position > 10:
            recommendations.extend([
                "Optimize content for target keywords",
                "Improve content depth and quality",
                "Build more high-quality backlinks",
                "Enhance user experience signals"
            ])
            return PerformanceCategory.HIGH_POTENTIAL, recommendations
        
        # Default recommendations
        recommendations.extend([
            "Monitor performance trends",
            "Continue standard SEO best practices"
        ])
        
        return PerformanceCategory.HIGH_POTENTIAL, recommendations

    async def _analyze_query_opportunities(
        self,
        query_data: List[Dict[str, Any]],
        page_data: List[Dict[str, Any]]
    ) -> Dict[str, List[QueryPerformance]]:
        """
        Analyze query performance for optimization opportunities.
        
        Returns:
            Dictionary with categorized query opportunities
        """
        logger.debug("Analyzing query opportunities")
        
        all_queries = []
        striking_distance = []
        opportunities = []
        
        for query_info in query_data:
            metrics = AuditMetrics(
                impressions=query_info['impressions'],
                clicks=query_info['clicks'],
                ctr=query_info['ctr'],
                position=query_info['position']
            )
            
            # Calculate opportunity score
            opportunity_score = self._calculate_opportunity_score(metrics)
            
            # Determine intent type
            intent_type = self._classify_query_intent(query_info['query'])
            
            query_performance = QueryPerformance(
                query=query_info['query'],
                metrics=metrics,
                pages=[],  # Will be populated if needed
                intent_type=intent_type,
                opportunity_score=opportunity_score
            )
            
            all_queries.append(query_performance)
            
            # Striking distance: positions 11-20
            if (self.performance_thresholds['striking_distance_start'] <= 
                metrics.position <= self.performance_thresholds['striking_distance_end']):
                striking_distance.append(query_performance)
            
            # High opportunity queries
            if opportunity_score > 7.0:
                opportunities.append(query_performance)
        
        # Sort by opportunity score
        opportunities.sort(key=lambda x: x.opportunity_score, reverse=True)
        striking_distance.sort(key=lambda x: x.metrics.impressions, reverse=True)
        
        return {
            'all_queries': all_queries,
            'striking_distance': striking_distance[:50],
            'opportunities': opportunities[:30]
        }

    def _calculate_opportunity_score(self, metrics: AuditMetrics) -> float:
        """
        Calculate an opportunity score for a query (0-10 scale).
        
        Higher scores indicate better optimization opportunities.
        """
        score = 0.0
        
        # High impressions indicate relevance
        if metrics.impressions > 1000:
            score += 3.0
        elif metrics.impressions > 100:
            score += 2.0
        elif metrics.impressions > 10:
            score += 1.0
        
        # Position indicates potential for improvement
        if 11 <= metrics.position <= 20:
            score += 4.0  # Striking distance
        elif 4 <= metrics.position <= 10:
            score += 3.0  # First page but not top
        elif metrics.position > 20:
            score += 1.0  # Long-term opportunity
        
        # CTR vs expected CTR for position
        expected_ctr = self._get_expected_ctr_for_position(metrics.position)
        if metrics.ctr < expected_ctr * 0.7:  # Significantly below expected
            score += 2.0
        
        return min(score, 10.0)

    def _get_expected_ctr_for_position(self, position: float) -> float:
        """Get expected CTR based on average position."""
        # Based on industry averages
        ctr_by_position = {
            1: 28.5, 2: 15.7, 3: 11.0, 4: 8.0, 5: 7.2,
            6: 5.1, 7: 4.0, 8: 3.2, 9: 2.8, 10: 2.5
        }
        
        if position <= 10:
            return ctr_by_position.get(int(position), 2.0)
        elif position <= 20:
            return 1.5
        else:
            return 0.5

    def _classify_query_intent(self, query: str) -> str:
        """
        Classify the search intent of a query.
        
        Returns:
            Intent type: informational, navigational, transactional, commercial
        """
        query_lower = query.lower()
        
        # Transactional intent
        transactional_keywords = [
            'buy', 'purchase', 'order', 'shop', 'cart', 'checkout',
            'price', 'cost', 'deal', 'discount', 'sale'
        ]
        if any(keyword in query_lower for keyword in transactional_keywords):
            return 'transactional'
        
        # Commercial intent
        commercial_keywords = [
            'best', 'top', 'review', 'compare', 'vs', 'alternative',
            'recommendation', 'which', 'should i'
        ]
        if any(keyword in query_lower for keyword in commercial_keywords):
            return 'commercial'
        
        # Navigational intent
        navigational_keywords = [
            'login', 'sign in', 'account', 'dashboard', 'contact',
            'about', 'careers', 'support'
        ]
        if any(keyword in query_lower for keyword in navigational_keywords):
            return 'navigational'
        
        # Default to informational
        return 'informational'

    async def _analyze_content_clusters(
        self,
        page_data: List[Dict[str, Any]],
        site_url: str
    ) -> List[ContentCluster]:
        """
        Analyze content clusters by topic/subdirectory.
        
        Returns:
            List of content clusters with performance data
        """
        logger.debug("Analyzing content clusters")
        
        # Group pages by subdirectory/topic
        clusters = defaultdict(list)
        
        for page_info in page_data:
            # Extract topic from URL path
            topic = self._extract_topic_from_url(page_info['page'], site_url)
            clusters[topic].append(page_info)
        
        content_clusters = []
        
        for topic, pages in clusters.items():
            if len(pages) < 2:  # Skip single-page "clusters"
                continue
            
            # Calculate cluster metrics
            total_impressions = sum(p['impressions'] for p in pages)
            total_clicks = sum(p['clicks'] for p in pages)
            avg_position = np.mean([p['position'] for p in pages])
            avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            
            total_metrics = AuditMetrics(
                impressions=total_impressions,
                clicks=total_clicks,
                ctr=avg_ctr,
                position=avg_position
            )
            
            avg_metrics = AuditMetrics(
                impressions=int(total_impressions / len(pages)),
                clicks=int(total_clicks / len(pages)),
                ctr=avg_ctr,
                position=avg_position
            )
            
            # Calculate performance score
            performance_score = self._calculate_cluster_performance_score(
                total_metrics, len(pages)
            )
            
            # Generate recommendations
            recommendations = self._generate_cluster_recommendations(
                total_metrics, len(pages), performance_score
            )
            
            cluster = ContentCluster(
                topic=topic,
                pages=[p['page'] for p in pages],
                total_metrics=total_metrics,
                avg_metrics=avg_metrics,
                performance_score=performance_score,
                recommendations=recommendations
            )
            
            content_clusters.append(cluster)
        
        # Sort by performance score
        content_clusters.sort(key=lambda x: x.performance_score, reverse=True)
        
        return content_clusters[:20]  # Top 20 clusters

    def _extract_topic_from_url(self, url: str, site_url: str) -> str:
        """Extract topic/category from URL path."""
        try:
            # Remove site URL and get path
            path = url.replace(site_url, '').strip('/')
            
            # Get first directory level as topic
            if '/' in path:
                topic = path.split('/')[0]
            else:
                topic = 'homepage'
            
            return topic or 'root'
            
        except Exception:
            return 'unknown'

    def _calculate_cluster_performance_score(
        self,
        metrics: AuditMetrics,
        page_count: int
    ) -> float:
        """Calculate performance score for a content cluster."""
        score = 0.0
        
        # Traffic contribution
        if metrics.clicks > 1000:
            score += 4.0
        elif metrics.clicks > 500:
            score += 3.0
        elif metrics.clicks > 100:
            score += 2.0
        
        # Average position
        if metrics.position <= 5:
            score += 3.0
        elif metrics.position <= 10:
            score += 2.0
        elif metrics.position <= 20:
            score += 1.0
        
        # CTR performance
        expected_ctr = self._get_expected_ctr_for_position(metrics.position)
        if metrics.ctr >= expected_ctr:
            score += 2.0
        elif metrics.ctr >= expected_ctr * 0.8:
            score += 1.0
        
        # Content depth (more pages = more comprehensive)
        if page_count > 10:
            score += 1.0
        elif page_count > 5:
            score += 0.5
        
        return min(score, 10.0)

    def _generate_cluster_recommendations(
        self,
        metrics: AuditMetrics,
        page_count: int,
        performance_score: float
    ) -> List[str]:
        """Generate recommendations for a content cluster."""
        recommendations = []
        
        if performance_score >= 8.0:
            recommendations.extend([
                "Excellent cluster performance - maintain and expand",
                "Consider creating more content in this topic area",
                "Use as a template for other content clusters"
            ])
        elif performance_score >= 6.0:
            recommendations.extend([
                "Good performance with room for improvement",
                "Optimize individual pages within the cluster",
                "Consider internal linking improvements"
            ])
        elif performance_score >= 4.0:
            recommendations.extend([
                "Moderate performance - focus on content quality",
                "Review keyword targeting across cluster pages",
                "Consider consolidating similar pages"
            ])
        else:
            recommendations.extend([
                "Underperforming cluster - needs significant attention",
                "Audit content quality and relevance",
                "Consider major content restructuring or removal"
            ])
        
        # Specific recommendations based on metrics
        if metrics.ctr < 3.0:
            recommendations.append("Improve title tags and meta descriptions across cluster")
        
        if metrics.position > 15:
            recommendations.append("Focus on improving content depth and authority")
        
        if page_count > 20:
            recommendations.append("Consider content consolidation to avoid cannibalization")
        
        return recommendations

    async def _get_technical_signals(
        self,
        service,
        site_url: str
    ) -> Dict[str, Any]:
        """
        Get technical signals from other GSC APIs.
        
        Returns:
            Dictionary with technical insights
        """
        logger.debug("Collecting technical signals")
        
        technical_data = {
            'sitemaps': {},
            'indexing_status': {},
            'mobile_usability': {},
            'coverage_issues': {}
        }
        
        try:
            # Get sitemaps data
            sitemaps_response = service.sitemaps().list(siteUrl=site_url).execute()
            technical_data['sitemaps'] = {
                'total_sitemaps': len(sitemaps_response.get('sitemap', [])),
                'sitemaps': sitemaps_response.get('sitemap', [])
            }
            
        except HttpError as e:
            logger.warning(f"Could not fetch sitemaps data: {e}")
            technical_data['sitemaps'] = {'error': str(e)}
        
        # Note: URL Inspection API has usage limits, so we'll focus on aggregate data
        # In a production environment, you might sample a subset of important URLs
        
        return technical_data

    async def _analyze_performance_trends(
        self,
        service,
        site_url: str,
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """
        Analyze performance trends over the date range.
        
        Returns:
            Dictionary with trend analysis
        """
        logger.debug("Analyzing performance trends")
        
        # Get daily performance data
        request_body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['date'],
            'rowLimit': 500
        }
        
        try:
            response = service.searchanalytics().query(
                siteUrl=site_url,
                body=request_body
            ).execute()
            
            daily_data = []
            for row in response.get('rows', []):
                daily_data.append({
                    'date': row['keys'][0],
                    'impressions': row.get('impressions', 0),
                    'clicks': row.get('clicks', 0),
                    'ctr': row.get('ctr', 0) * 100,
                    'position': row.get('position', 0)
                })
            
            # Analyze trends
            df = pd.DataFrame(daily_data)
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
                
                trends = {
                    'total_days': len(df),
                    'clicks_trend': self._calculate_trend(df['clicks'].tolist()),
                    'impressions_trend': self._calculate_trend(df['impressions'].tolist()),
                    'ctr_trend': self._calculate_trend(df['ctr'].tolist()),
                    'position_trend': self._calculate_trend(df['position'].tolist()),
                    'best_day': df.loc[df['clicks'].idxmax()].to_dict() if len(df) > 0 else {},
                    'worst_day': df.loc[df['clicks'].idxmin()].to_dict() if len(df) > 0 else {}
                }
                
                return trends
            
        except HttpError as e:
            logger.warning(f"Could not fetch trend data: {e}")
        
        return {'error': 'Could not analyze trends'}

    def _calculate_trend(self, values: List[float]) -> Dict[str, Any]:
        """Calculate trend direction and strength for a metric."""
        if len(values) < 2:
            return {'direction': 'stable', 'strength': 0, 'change_percent': 0}
        
        # Calculate linear regression slope
        x = np.arange(len(values))
        slope, _ = np.polyfit(x, values, 1)
        
        # Calculate percentage change
        start_val = values[0] if values[0] != 0 else 1
        end_val = values[-1]
        change_percent = ((end_val - start_val) / start_val) * 100
        
        # Determine direction and strength
        if abs(change_percent) < 5:
            direction = 'stable'
            strength = abs(change_percent)
        elif change_percent > 0:
            direction = 'increasing'
            strength = change_percent
        else:
            direction = 'decreasing'
            strength = abs(change_percent)
        
        return {
            'direction': direction,
            'strength': round(strength, 2),
            'change_percent': round(change_percent, 2),
            'slope': round(slope, 4)
        }

    async def _get_yoy_comparison(
        self,
        service,
        site_url: str,
        start_date: str,
        end_date: str
    ) -> Optional[Dict[str, Any]]:
        """Get year-over-year comparison data."""
        try:
            # Calculate previous year dates
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            prev_start = (start_dt - timedelta(days=365)).strftime('%Y-%m-%d')
            prev_end = (end_dt - timedelta(days=365)).strftime('%Y-%m-%d')
            
            # Get current and previous period data
            current_data = await self._get_aggregate_metrics(service, site_url, start_date, end_date)
            previous_data = await self._get_aggregate_metrics(service, site_url, prev_start, prev_end)
            
            if current_data and previous_data:
                return self._calculate_comparison_metrics(current_data, previous_data, 'YoY')
                
        except Exception as e:
            logger.warning(f"Could not calculate YoY comparison: {e}")
        
        return None

    async def _get_mom_comparison(
        self,
        service,
        site_url: str,
        start_date: str,
        end_date: str
    ) -> Optional[Dict[str, Any]]:
        """Get month-over-month comparison data."""
        try:
            # Calculate previous month dates
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Calculate days in current period
            period_days = (end_dt - start_dt).days + 1
            
            prev_end = start_dt - timedelta(days=1)
            prev_start = prev_end - timedelta(days=period_days - 1)
            
            prev_start_str = prev_start.strftime('%Y-%m-%d')
            prev_end_str = prev_end.strftime('%Y-%m-%d')
            
            # Get current and previous period data
            current_data = await self._get_aggregate_metrics(service, site_url, start_date, end_date)
            previous_data = await self._get_aggregate_metrics(service, site_url, prev_start_str, prev_end_str)
            
            if current_data and previous_data:
                return self._calculate_comparison_metrics(current_data, previous_data, 'MoM')
                
        except Exception as e:
            logger.warning(f"Could not calculate MoM comparison: {e}")
        
        return None

    async def _get_aggregate_metrics(
        self,
        service,
        site_url: str,
        start_date: str,
        end_date: str
    ) -> Optional[Dict[str, Any]]:
        """Get aggregate metrics for a date range."""
        request_body = {
            'startDate': start_date,
            'endDate': end_date
        }
        
        try:
            response = service.searchanalytics().query(
                siteUrl=site_url,
                body=request_body
            ).execute()
            
            if response.get('rows'):
                row = response['rows'][0]
                return {
                    'impressions': row.get('impressions', 0),
                    'clicks': row.get('clicks', 0),
                    'ctr': row.get('ctr', 0) * 100,
                    'position': row.get('position', 0)
                }
        except HttpError as e:
            logger.warning(f"Could not fetch aggregate metrics: {e}")
        
        return None

    def _calculate_comparison_metrics(
        self,
        current: Dict[str, Any],
        previous: Dict[str, Any],
        comparison_type: str
    ) -> Dict[str, Any]:
        """Calculate comparison metrics between two periods."""
        comparison = {
            'comparison_type': comparison_type,
            'current_period': current,
            'previous_period': previous,
            'changes': {}
        }
        
        for metric in ['impressions', 'clicks', 'ctr', 'position']:
            current_val = current.get(metric, 0)
            previous_val = previous.get(metric, 0)
            
            if previous_val != 0:
                change_percent = ((current_val - previous_val) / previous_val) * 100
            else:
                change_percent = 100 if current_val > 0 else 0
            
            comparison['changes'][metric] = {
                'absolute_change': current_val - previous_val,
                'percent_change': round(change_percent, 2),
                'direction': 'increase' if change_percent > 0 else 'decrease' if change_percent < 0 else 'stable'
            }
        
        return comparison

    def _calculate_summary_metrics(
        self,
        page_data: List[Dict[str, Any]],
        query_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate summary metrics from page and query data."""
        total_impressions = sum(p['impressions'] for p in page_data)
        total_clicks = sum(p['clicks'] for p in page_data)
        
        # Calculate weighted averages
        if total_impressions > 0:
            avg_ctr = (total_clicks / total_impressions) * 100
            avg_position = sum(p['position'] * p['impressions'] for p in page_data) / total_impressions
        else:
            avg_ctr = 0
            avg_position = 0
        
        return {
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'average_ctr': round(avg_ctr, 2),
            'average_position': round(avg_position, 1)
        }

    async def _get_trends_analysis(
        self,
        top_queries: List[QueryPerformance],
        top_pages: List[PagePerformance]
    ) -> Tuple[List[TrendData], List[SeasonalInsight], List[TrendComparison]]:
        """
        Get comprehensive Google Trends analysis for top queries.
        
        Args:
            top_queries: Top performing queries from GSC
            top_pages: Top performing pages from GSC
            
        Returns:
            Tuple of (trends_data, seasonal_insights, trend_comparisons)
        """
        try:
            # Extract queries for trends analysis
            query_strings = [q.query for q in top_queries[:15]]  # Limit for API efficiency
            
            if not query_strings:
                return [], [], []
            
            # Get trends data for individual queries
            logger.info(f"Analyzing trends for {len(query_strings)} queries")
            trends_data = await google_trends_service.get_trends_for_queries(
                queries=query_strings,
                timeframe='today 12-m'
            )
            
            # Get seasonal insights (longer timeframe)
            seasonal_insights = await google_trends_service.get_seasonal_insights(
                queries=query_strings[:10],  # Limit for seasonal analysis
                timeframe='today 5-y'
            )
            
            # Compare top queries
            trend_comparisons = []
            if len(query_strings) >= 2:
                # Compare top 5 queries in batches
                for i in range(0, min(len(query_strings), 10), 5):
                    batch = query_strings[i:i+5]
                    if len(batch) >= 2:
                        comparison = await google_trends_service.compare_queries(
                            queries=batch,
                            timeframe='today 12-m'
                        )
                        if comparison:
                            trend_comparisons.append(comparison)
            
            logger.info(f"Trends analysis completed: {len(trends_data)} trends, {len(seasonal_insights)} seasonal patterns, {len(trend_comparisons)} comparisons")
            
            return trends_data, seasonal_insights, trend_comparisons
            
        except Exception as e:
            logger.error(f"Error in trends analysis: {e}")
            testing_logger.error_platform_api(
                "google_trends", "trends_analysis", e,
                {"queries_count": len(top_queries)}
            )
            return [], [], []

    async def conduct_enhanced_audit(
        self,
        connection: SocialConnection,
        site_url: str,
        start_date: str,
        end_date: str,
        db: Session,
        analysis_type: str = "comprehensive"
    ) -> AuditReport:
        """
        Conduct an enhanced audit with configurable analysis depth.
        
        Args:
            connection: GSC connection object
            site_url: Website URL to audit
            start_date: Start date for analysis
            end_date: End date for analysis
            db: Database session
            analysis_type: Type of analysis ('basic', 'trends', 'comprehensive')
            
        Returns:
            Enhanced audit report with appropriate level of analysis
        """
        include_comparisons = analysis_type in ['trends', 'comprehensive']
        include_trends = analysis_type in ['trends', 'comprehensive']
        include_ai_insights = analysis_type == 'comprehensive'
        
        return await self.conduct_comprehensive_audit(
            connection=connection,
            site_url=site_url,
            start_date=start_date,
            end_date=end_date,
            db=db,
            include_comparisons=include_comparisons,
            include_trends=include_trends,
            include_ai_insights=include_ai_insights
        )

# Global service instance
gsc_audit_service = GSCWebsiteAuditService()