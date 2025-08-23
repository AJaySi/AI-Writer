"""
Google Search Console Website Audit API Endpoints

Comprehensive API endpoints for conducting data-driven website content audits
using Google Search Console APIs. Provides access to all audit functionality
including performance analysis, content clustering, and optimization recommendations.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import logging

from services.database import get_db
from services.gsc_website_audit_service import gsc_audit_service
from services.oauth_service import oauth_service
from services.logging_service import api_logger
from models.social_connections import SocialConnection

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/gsc-audit", tags=["GSC Website Audit"])

# Pydantic models for request/response validation
class AuditRequest(BaseModel):
    """Request model for starting a website audit."""
    site_url: str = Field(..., description="Website URL to audit")
    start_date: str = Field(..., description="Start date for analysis (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date for analysis (YYYY-MM-DD)")
    include_comparisons: bool = Field(True, description="Include YoY/MoM comparisons")
    include_trends: bool = Field(True, description="Include Google Trends analysis")
    include_ai_insights: bool = Field(True, description="Include AI-generated insights")
    
    class Config:
        schema_extra = {
            "example": {
                "site_url": "https://example.com/",
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "include_comparisons": True,
                "include_trends": True,
                "include_ai_insights": True
            }
        }

class QuickAuditRequest(BaseModel):
    """Request model for quick audit with preset date ranges."""
    site_url: str = Field(..., description="Website URL to audit")
    date_range: str = Field("last_30_days", description="Preset date range")
    analysis_type: str = Field("comprehensive", description="Analysis depth: 'basic', 'trends', 'comprehensive'")
    
    class Config:
        schema_extra = {
            "example": {
                "site_url": "https://example.com/",
                "date_range": "last_30_days",
                "analysis_type": "comprehensive"
            }
        }

class PageAnalysisRequest(BaseModel):
    """Request model for individual page analysis."""
    site_url: str = Field(..., description="Website URL")
    page_url: str = Field(..., description="Specific page URL to analyze")
    start_date: str = Field(..., description="Start date for analysis")
    end_date: str = Field(..., description="End date for analysis")

class QueryAnalysisRequest(BaseModel):
    """Request model for query-specific analysis."""
    site_url: str = Field(..., description="Website URL")
    query: str = Field(..., description="Specific query to analyze")
    start_date: str = Field(..., description="Start date for analysis")
    end_date: str = Field(..., description="End date for analysis")

class AuditResponse(BaseModel):
    """Response model for audit results."""
    success: bool
    message: str
    audit_id: Optional[str] = None
    report: Optional[Dict[str, Any]] = None
    
class AuditStatus(BaseModel):
    """Response model for audit status."""
    audit_id: str
    status: str
    progress: int
    message: str
    started_at: datetime
    estimated_completion: Optional[datetime] = None

# Main audit endpoints
@router.post("/start-audit", response_model=AuditResponse)
async def start_comprehensive_audit(
    audit_request: AuditRequest,
    background_tasks: BackgroundTasks,
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """
    Start a comprehensive website audit using GSC data.
    
    This endpoint initiates a full content audit including:
    - Core performance metrics analysis
    - Page and query level insights
    - Content clustering and topic performance
    - Technical signals and recommendations
    - YoY/MoM comparisons (if requested)
    """
    try:
        api_logger.info_connection_event(
            "audit_requested", "google_search_console", user_id,
            {"site_url": audit_request.site_url, "date_range": f"{audit_request.start_date} to {audit_request.end_date}"}
        )
        
        # Validate user has GSC connection
        connection = db.query(SocialConnection).filter(
            SocialConnection.user_id == user_id,
            SocialConnection.platform == 'google_search_console',
            SocialConnection.connection_status == 'active'
        ).first()
        
        if not connection:
            raise HTTPException(
                status_code=404,
                detail="No active Google Search Console connection found. Please connect GSC first."
            )
        
        # Validate date range
        start_date = datetime.strptime(audit_request.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(audit_request.end_date, '%Y-%m-%d')
        
        if start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail="Start date must be before end date"
            )
        
        if (datetime.now() - start_date).days > 365:
            raise HTTPException(
                status_code=400,
                detail="Start date cannot be more than 365 days ago"
            )
        
        # Conduct audit
        report = await gsc_audit_service.conduct_comprehensive_audit(
            connection=connection,
            site_url=audit_request.site_url,
            start_date=audit_request.start_date,
            end_date=audit_request.end_date,
            db=db,
            include_comparisons=audit_request.include_comparisons,
            include_trends=audit_request.include_trends,
            include_ai_insights=audit_request.include_ai_insights
        )
        
        api_logger.info_connection_event(
            "audit_completed", "google_search_console", user_id,
            {"site_url": audit_request.site_url, "total_pages": report.total_pages}
        )
        
        return AuditResponse(
            success=True,
            message="Audit completed successfully",
            report=report.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error_platform_api(
            "google_search_console", "comprehensive_audit", e,
            {"site_url": audit_request.site_url, "user_id": user_id}
        )
        raise HTTPException(
            status_code=500,
            detail=f"Audit failed: {str(e)}"
        )

@router.post("/quick-audit", response_model=AuditResponse)
async def quick_website_audit(
    audit_request: QuickAuditRequest,
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """
    Perform a quick website audit with preset date ranges.
    
    Available date ranges:
    - last_7_days: Last 7 days
    - last_30_days: Last 30 days (default)
    - last_90_days: Last 90 days
    - last_6_months: Last 6 months
    - last_year: Last 12 months
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        
        date_ranges = {
            'last_7_days': 7,
            'last_30_days': 30,
            'last_90_days': 90,
            'last_6_months': 180,
            'last_year': 365
        }
        
        if audit_request.date_range not in date_ranges:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid date range. Available options: {list(date_ranges.keys())}"
            )
        
        days_back = date_ranges[audit_request.date_range]
        start_date = end_date - timedelta(days=days_back)
        
        # Use the enhanced audit method
        connection = await _get_gsc_connection(user_id, db)
        
        report = await gsc_audit_service.conduct_enhanced_audit(
            connection=connection,
            site_url=audit_request.site_url,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            db=db,
            analysis_type=audit_request.analysis_type
        )
        
        return AuditResponse(
            success=True,
            message="Quick audit completed successfully",
            report=report.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Quick audit failed: {str(e)}"
        )

# Specialized analysis endpoints
@router.post("/analyze-page")
async def analyze_specific_page(
    analysis_request: PageAnalysisRequest,
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """
    Analyze a specific page's performance in detail.
    
    Returns detailed metrics, recommendations, and queries driving traffic
    to the specified page.
    """
    try:
        connection = db.query(SocialConnection).filter(
            SocialConnection.user_id == user_id,
            SocialConnection.platform == 'google_search_console',
            SocialConnection.connection_status == 'active'
        ).first()
        
        if not connection:
            raise HTTPException(status_code=404, detail="No active GSC connection found")
        
        # Get GSC service
        service = await gsc_audit_service._get_gsc_service(connection, db)
        
        # Get page-specific data
        request_body = {
            'startDate': analysis_request.start_date,
            'endDate': analysis_request.end_date,
            'dimensions': ['page', 'query'],
            'dimensionFilterGroups': [{
                'filters': [{
                    'dimension': 'page',
                    'operator': 'equals',
                    'expression': analysis_request.page_url
                }]
            }],
            'rowLimit': 1000
        }
        
        response = service.searchanalytics().query(
            siteUrl=analysis_request.site_url,
            body=request_body
        ).execute()
        
        # Process results
        page_queries = []
        total_impressions = 0
        total_clicks = 0
        
        for row in response.get('rows', []):
            page_url = row['keys'][0]
            query = row['keys'][1]
            impressions = row.get('impressions', 0)
            clicks = row.get('clicks', 0)
            ctr = row.get('ctr', 0) * 100
            position = row.get('position', 0)
            
            total_impressions += impressions
            total_clicks += clicks
            
            page_queries.append({
                'query': query,
                'impressions': impressions,
                'clicks': clicks,
                'ctr': round(ctr, 2),
                'position': round(position, 1),
                'intent_type': gsc_audit_service._classify_query_intent(query)
            })
        
        # Sort by impressions
        page_queries.sort(key=lambda x: x['impressions'], reverse=True)
        
        # Calculate overall metrics
        overall_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        avg_position = sum(q['position'] * q['impressions'] for q in page_queries) / total_impressions if total_impressions > 0 else 0
        
        # Generate recommendations
        recommendations = []
        if overall_ctr < 3.0:
            recommendations.append("Optimize title tag and meta description to improve click-through rate")
        if avg_position > 10:
            recommendations.append("Focus on improving content quality and relevance for target keywords")
        if total_clicks < 50:
            recommendations.append("Consider expanding keyword targeting or improving content promotion")
        
        return {
            'success': True,
            'page_url': analysis_request.page_url,
            'date_range': {
                'start': analysis_request.start_date,
                'end': analysis_request.end_date
            },
            'overall_metrics': {
                'total_impressions': total_impressions,
                'total_clicks': total_clicks,
                'average_ctr': round(overall_ctr, 2),
                'average_position': round(avg_position, 1)
            },
            'top_queries': page_queries[:20],
            'recommendations': recommendations,
            'query_count': len(page_queries)
        }
        
    except Exception as e:
        api_logger.error_platform_api(
            "google_search_console", "page_analysis", e,
            {"page_url": analysis_request.page_url, "user_id": user_id}
        )
        raise HTTPException(status_code=500, detail=f"Page analysis failed: {str(e)}")

@router.post("/analyze-query")
async def analyze_specific_query(
    analysis_request: QueryAnalysisRequest,
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """
    Analyze a specific query's performance across all pages.
    
    Returns detailed metrics showing which pages rank for the query
    and optimization opportunities.
    """
    try:
        connection = db.query(SocialConnection).filter(
            SocialConnection.user_id == user_id,
            SocialConnection.platform == 'google_search_console',
            SocialConnection.connection_status == 'active'
        ).first()
        
        if not connection:
            raise HTTPException(status_code=404, detail="No active GSC connection found")
        
        # Get GSC service
        service = await gsc_audit_service._get_gsc_service(connection, db)
        
        # Get query-specific data
        request_body = {
            'startDate': analysis_request.start_date,
            'endDate': analysis_request.end_date,
            'dimensions': ['query', 'page'],
            'dimensionFilterGroups': [{
                'filters': [{
                    'dimension': 'query',
                    'operator': 'equals',
                    'expression': analysis_request.query
                }]
            }],
            'rowLimit': 1000
        }
        
        response = service.searchanalytics().query(
            siteUrl=analysis_request.site_url,
            body=request_body
        ).execute()
        
        # Process results
        query_pages = []
        total_impressions = 0
        total_clicks = 0
        
        for row in response.get('rows', []):
            query = row['keys'][0]
            page_url = row['keys'][1]
            impressions = row.get('impressions', 0)
            clicks = row.get('clicks', 0)
            ctr = row.get('ctr', 0) * 100
            position = row.get('position', 0)
            
            total_impressions += impressions
            total_clicks += clicks
            
            query_pages.append({
                'page_url': page_url,
                'impressions': impressions,
                'clicks': clicks,
                'ctr': round(ctr, 2),
                'position': round(position, 1)
            })
        
        # Sort by impressions
        query_pages.sort(key=lambda x: x['impressions'], reverse=True)
        
        # Calculate metrics
        overall_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        avg_position = sum(p['position'] * p['impressions'] for p in query_pages) / total_impressions if total_impressions > 0 else 0
        
        # Analyze intent and opportunity
        intent_type = gsc_audit_service._classify_query_intent(analysis_request.query)
        
        from services.gsc_website_audit_service import AuditMetrics
        metrics = AuditMetrics(
            impressions=total_impressions,
            clicks=total_clicks,
            ctr=overall_ctr,
            position=avg_position
        )
        opportunity_score = gsc_audit_service._calculate_opportunity_score(metrics)
        
        # Generate recommendations
        recommendations = []
        if len(query_pages) > 1:
            recommendations.append("Multiple pages competing for this query - consider content consolidation")
        if avg_position > 10:
            recommendations.append("Query is in striking distance - focus on content optimization")
        if overall_ctr < 3.0:
            recommendations.append("Low CTR for this query - optimize SERP snippets")
        
        return {
            'success': True,
            'query': analysis_request.query,
            'date_range': {
                'start': analysis_request.start_date,
                'end': analysis_request.end_date
            },
            'overall_metrics': {
                'total_impressions': total_impressions,
                'total_clicks': total_clicks,
                'average_ctr': round(overall_ctr, 2),
                'average_position': round(avg_position, 1)
            },
            'query_analysis': {
                'intent_type': intent_type,
                'opportunity_score': round(opportunity_score, 1),
                'competing_pages': len(query_pages)
            },
            'ranking_pages': query_pages[:10],
            'recommendations': recommendations
        }
        
    except Exception as e:
        api_logger.error_platform_api(
            "google_search_console", "query_analysis", e,
            {"query": analysis_request.query, "user_id": user_id}
        )
        raise HTTPException(status_code=500, detail=f"Query analysis failed: {str(e)}")

# Quick insights endpoints
@router.get("/top-performing-pages")
async def get_top_performing_pages(
    site_url: str = Query(..., description="Website URL"),
    days: int = Query(30, description="Number of days to analyze"),
    limit: int = Query(20, description="Number of pages to return"),
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """Get top performing pages by clicks."""
    try:
        connection = await _get_gsc_connection(user_id, db)
        service = await gsc_audit_service._get_gsc_service(connection, db)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get page data
        page_data = await gsc_audit_service._get_page_performance_data(
            service, site_url, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
        )
        
        # Sort by clicks and limit
        top_pages = sorted(page_data, key=lambda x: x['clicks'], reverse=True)[:limit]
        
        return {
            'success': True,
            'site_url': site_url,
            'date_range': f"Last {days} days",
            'total_pages_analyzed': len(page_data),
            'top_performing_pages': top_pages
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get top pages: {str(e)}")

@router.get("/low-hanging-fruit")
async def get_low_hanging_fruit(
    site_url: str = Query(..., description="Website URL"),
    days: int = Query(30, description="Number of days to analyze"),
    limit: int = Query(20, description="Number of opportunities to return"),
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """Get low hanging fruit opportunities (high impressions, low CTR)."""
    try:
        connection = await _get_gsc_connection(user_id, db)
        service = await gsc_audit_service._get_gsc_service(connection, db)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get page data
        page_data = await gsc_audit_service._get_page_performance_data(
            service, site_url, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
        )
        
        # Filter for low hanging fruit
        opportunities = []
        for page in page_data:
            if page['impressions'] > 100 and page['ctr'] < 3.0:
                opportunities.append({
                    **page,
                    'opportunity_score': page['impressions'] / page['ctr'] if page['ctr'] > 0 else 0
                })
        
        # Sort by opportunity score
        opportunities.sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        return {
            'success': True,
            'site_url': site_url,
            'date_range': f"Last {days} days",
            'total_opportunities': len(opportunities),
            'top_opportunities': opportunities[:limit],
            'criteria': {
                'min_impressions': 100,
                'max_ctr': 3.0
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get opportunities: {str(e)}")

@router.get("/striking-distance-queries")
async def get_striking_distance_queries(
    site_url: str = Query(..., description="Website URL"),
    days: int = Query(30, description="Number of days to analyze"),
    limit: int = Query(30, description="Number of queries to return"),
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """Get queries in striking distance (positions 11-20)."""
    try:
        connection = await _get_gsc_connection(user_id, db)
        service = await gsc_audit_service._get_gsc_service(connection, db)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get query data
        query_data = await gsc_audit_service._get_query_performance_data(
            service, site_url, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
        )
        
        # Filter for striking distance
        striking_distance = []
        for query in query_data:
            if 11 <= query['position'] <= 20 and query['impressions'] > 10:
                striking_distance.append({
                    **query,
                    'intent_type': gsc_audit_service._classify_query_intent(query['query'])
                })
        
        # Sort by impressions
        striking_distance.sort(key=lambda x: x['impressions'], reverse=True)
        
        return {
            'success': True,
            'site_url': site_url,
            'date_range': f"Last {days} days",
            'total_striking_distance': len(striking_distance),
            'top_opportunities': striking_distance[:limit],
            'criteria': {
                'position_range': '11-20',
                'min_impressions': 10
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get striking distance queries: {str(e)}")

@router.get("/content-clusters")
async def get_content_clusters(
    site_url: str = Query(..., description="Website URL"),
    days: int = Query(30, description="Number of days to analyze"),
    limit: int = Query(15, description="Number of clusters to return"),
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """Get content clusters analysis by topic/subdirectory."""
    try:
        connection = await _get_gsc_connection(user_id, db)
        service = await gsc_audit_service._get_gsc_service(connection, db)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get page data
        page_data = await gsc_audit_service._get_page_performance_data(
            service, site_url, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
        )
        
        # Analyze content clusters
        clusters = await gsc_audit_service._analyze_content_clusters(page_data, site_url)
        
        return {
            'success': True,
            'site_url': site_url,
            'date_range': f"Last {days} days",
            'total_clusters': len(clusters),
            'content_clusters': [
                {
                    'topic': cluster.topic,
                    'page_count': len(cluster.pages),
                    'total_clicks': cluster.total_metrics.clicks,
                    'total_impressions': cluster.total_metrics.impressions,
                    'average_ctr': round(cluster.total_metrics.ctr, 2),
                    'average_position': round(cluster.total_metrics.position, 1),
                    'performance_score': round(cluster.performance_score, 1),
                    'top_recommendations': cluster.recommendations[:3]
                }
                for cluster in clusters[:limit]
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get content clusters: {str(e)}")

# Utility functions
async def _get_gsc_connection(user_id: int, db: Session) -> SocialConnection:
    """Get active GSC connection for user."""
    connection = db.query(SocialConnection).filter(
        SocialConnection.user_id == user_id,
        SocialConnection.platform == 'google_search_console',
        SocialConnection.connection_status == 'active'
    ).first()
    
    if not connection:
        raise HTTPException(
            status_code=404,
            detail="No active Google Search Console connection found"
        )
    
    return connection

@router.post("/ai-insights")
async def get_ai_insights(
    audit_request: AuditRequest,
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered insights for a website using combined GSC and Google Trends data.
    
    This endpoint provides intelligent analysis including:
    - Strategic content recommendations
    - Trend-based optimization opportunities
    - Performance forecasting
    - Risk assessment
    - Actionable improvement plans
    """
    try:
        connection = await _get_gsc_connection(user_id, db)
        
        # Conduct comprehensive audit with AI insights
        report = await gsc_audit_service.conduct_comprehensive_audit(
            connection=connection,
            site_url=audit_request.site_url,
            start_date=audit_request.start_date,
            end_date=audit_request.end_date,
            db=db,
            include_comparisons=True,
            include_trends=True,
            include_ai_insights=True
        )
        
        if not report.ai_analysis:
            raise HTTPException(
                status_code=500,
                detail="AI analysis could not be generated"
            )
        
        return {
            'success': True,
            'site_url': audit_request.site_url,
            'ai_insights': report.ai_analysis.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI insights generation failed: {str(e)}"
        )

@router.post("/trends-analysis")
async def get_trends_analysis(
    site_url: str = Query(..., description="Website URL"),
    queries: List[str] = Query(..., description="Queries to analyze"),
    timeframe: str = Query("today 12-m", description="Analysis timeframe"),
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """
    Get Google Trends analysis for specific queries.
    
    Provides detailed trends analysis including:
    - Search interest over time
    - Related and rising queries
    - Seasonal patterns
    - Geographic distribution
    - Query comparisons
    """
    try:
        from services.google_trends_service import google_trends_service
        
        # Validate connection
        await _get_gsc_connection(user_id, db)
        
        # Get trends data
        trends_data = await google_trends_service.get_trends_for_queries(
            queries=queries,
            timeframe=timeframe
        )
        
        # Get seasonal insights
        seasonal_insights = await google_trends_service.get_seasonal_insights(
            queries=queries[:5],  # Limit for efficiency
            timeframe='today 5-y'
        )
        
        # Get query comparisons
        comparison = None
        if len(queries) >= 2:
            comparison = await google_trends_service.compare_queries(
                queries=queries[:5],  # Limit to 5 for comparison
                timeframe=timeframe
            )
        
        return {
            'success': True,
            'site_url': site_url,
            'timeframe': timeframe,
            'trends_data': [trend.to_dict() for trend in trends_data],
            'seasonal_insights': [insight.to_dict() for insight in seasonal_insights],
            'query_comparison': comparison.to_dict() if comparison else None,
            'analysis_summary': {
                'queries_analyzed': len(queries),
                'trends_found': len(trends_data),
                'seasonal_patterns': len(seasonal_insights),
                'rising_opportunities': sum(len(trend.rising_queries) for trend in trends_data)
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Trends analysis failed: {str(e)}"
        )

@router.get("/trending-topics")
async def get_trending_topics(
    geo: str = Query("US", description="Geographic region"),
    category: str = Query("all", description="Trend category"),
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """Get current trending topics and searches from Google Trends."""
    try:
        from services.google_trends_service import google_trends_service
        
        # Validate connection
        await _get_gsc_connection(user_id, db)
        
        trending_topics = await google_trends_service.get_trending_topics(
            geo=geo,
            category=category
        )
        
        return {
            'success': True,
            'region': geo,
            'category': category,
            'trending_topics': trending_topics,
            'total_topics': len(trending_topics),
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not fetch trending topics: {str(e)}"
        )

# Health check endpoint
@router.get("/health")
async def audit_service_health():
    """Check the health of the audit service."""
    return {
        'service': 'GSC Website Audit Enhanced',
        'status': 'operational',
        'version': '2.0.0',
        'features': [
            'Comprehensive website audits',
            'Page-level analysis',
            'Query-level analysis',
            'Content clustering',
            'Performance trends',
            'YoY/MoM comparisons',
            'Technical signals',
            'Google Trends integration',
            'AI-powered insights',
            'Seasonal pattern analysis',
            'Query trend comparisons',
            'Performance forecasting',
            'Strategic content recommendations'
        ],
        'ai_capabilities': [
            'Gemini-powered analysis',
            'Structured JSON responses',
            'Content strategy generation',
            'Performance forecasting',
            'Risk assessment',
            'Action plan prioritization'
        ]
    }