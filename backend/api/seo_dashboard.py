"""SEO Dashboard API endpoints for ALwrity."""

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import os
from loguru import logger
import time

# Import existing services
from services.api_key_manager import APIKeyManager
from services.validation import check_all_api_keys
from services.seo_analyzer import ComprehensiveSEOAnalyzer, SEOAnalysisResult, SEOAnalysisService
from services.user_data_service import UserDataService
from services.database import get_db_session

# Initialize the SEO analyzer
seo_analyzer = ComprehensiveSEOAnalyzer()

# Pydantic models for SEO Dashboard
class SEOHealthScore(BaseModel):
    score: int
    change: int
    trend: str
    label: str
    color: str

class SEOMetric(BaseModel):
    value: float
    change: float
    trend: str
    description: str
    color: str

class PlatformStatus(BaseModel):
    status: str
    connected: bool
    last_sync: Optional[str] = None
    data_points: Optional[int] = None

class AIInsight(BaseModel):
    insight: str
    priority: str
    category: str
    action_required: bool
    tool_path: Optional[str] = None

class SEODashboardData(BaseModel):
    health_score: SEOHealthScore
    key_insight: str
    priority_alert: str
    metrics: Dict[str, SEOMetric]
    platforms: Dict[str, PlatformStatus]
    ai_insights: List[AIInsight]
    last_updated: str
    website_url: Optional[str] = None  # User's website URL from onboarding

# New models for comprehensive SEO analysis
class SEOAnalysisRequest(BaseModel):
    url: str
    target_keywords: Optional[List[str]] = None

class SEOAnalysisResponse(BaseModel):
    url: str
    timestamp: datetime
    overall_score: int
    health_status: str
    critical_issues: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    data: Dict[str, Any]
    success: bool
    message: str

class SEOMetricsResponse(BaseModel):
    metrics: Dict[str, Any]
    critical_issues: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    detailed_analysis: Dict[str, Any]
    timestamp: str
    url: str

# Mock data for Phase 1
def get_mock_seo_data() -> SEODashboardData:
    """Get mock SEO dashboard data for Phase 1."""
    # Try to get the user's website URL from the database
    website_url = None
    db_session = get_db_session()
    if db_session:
        try:
            user_data_service = UserDataService(db_session)
            website_url = user_data_service.get_user_website_url()
            logger.info(f"Retrieved website URL from database: {website_url}")
        except Exception as e:
            logger.error(f"Error fetching website URL from database: {e}")
        finally:
            db_session.close()
    
    return SEODashboardData(
        health_score=SEOHealthScore(
            score=78,
            change=12,
            trend="up",
            label="Good",
            color="#FF9800"
        ),
        key_insight="Your content strategy is working! Focus on technical SEO to reach 90+ score",
        priority_alert="Mobile speed needs attention - 2.8s load time",
        website_url=website_url,  # Include the user's website URL
        metrics={
            "traffic": SEOMetric(
                value=23450,
                change=23,
                trend="up",
                description="Strong growth!",
                color="#4CAF50"
            ),
            "rankings": SEOMetric(
                value=8,
                change=8,
                trend="up",
                description="Great work on content",
                color="#2196F3"
            ),
            "mobile": SEOMetric(
                value=2.8,
                change=-0.3,
                trend="down",
                description="Needs attention",
                color="#FF9800"
            ),
            "keywords": SEOMetric(
                value=156,
                change=5,
                trend="up",
                description="5 new opportunities",
                color="#9C27B0"
            )
        },
        platforms={
            "google_search_console": PlatformStatus(
                status="excellent",
                connected=True,
                last_sync="2024-01-15T10:30:00Z",
                data_points=1250
            ),
            "google_analytics": PlatformStatus(
                status="good",
                connected=True,
                last_sync="2024-01-15T10:25:00Z",
                data_points=890
            ),
            "bing_webmaster": PlatformStatus(
                status="needs_attention",
                connected=False,
                last_sync=None,
                data_points=0
            )
        },
        ai_insights=[
            AIInsight(
                insight="Your mobile page speed is 2.8s - optimize images and enable compression",
                priority="high",
                category="performance",
                action_required=True,
                tool_path="/seo-tools/page-speed-optimizer"
            ),
            AIInsight(
                insight="Add structured data to improve rich snippet opportunities",
                priority="medium",
                category="technical",
                action_required=False,
                tool_path="/seo-tools/schema-generator"
            ),
            AIInsight(
                insight="Content quality score improved by 15% - great work!",
                priority="low",
                category="content",
                action_required=False
            )
        ],
        last_updated="2024-01-15T10:30:00Z"
    )

def calculate_health_score(metrics: Dict[str, Any]) -> SEOHealthScore:
    """Calculate SEO health score based on metrics."""
    # This would be replaced with actual calculation logic
    base_score = 75
    change = 12
    trend = "up"
    label = "Good"
    color = "#FF9800"
    
    return SEOHealthScore(
        score=base_score,
        change=change,
        trend=trend,
        label=label,
        color=color
    )

def generate_ai_insights(metrics: Dict[str, Any], platforms: Dict[str, Any]) -> List[AIInsight]:
    """Generate AI-powered insights based on metrics and platform data."""
    insights = []
    
    # Performance insights
    if metrics.get("mobile", {}).get("value", 0) > 2.5:
        insights.append(AIInsight(
            insight="Mobile page speed needs optimization - aim for under 2 seconds",
            priority="high",
            category="performance",
            action_required=True,
            tool_path="/seo-tools/page-speed-optimizer"
        ))
    
    # Technical insights
    if not platforms.get("google_search_console", {}).get("connected", False):
        insights.append(AIInsight(
            insight="Connect Google Search Console for better SEO monitoring",
            priority="medium",
            category="technical",
            action_required=True,
            tool_path="/seo-tools/search-console-setup"
        ))
    
    # Content insights
    if metrics.get("rankings", {}).get("change", 0) > 0:
        insights.append(AIInsight(
            insight="Rankings are improving - continue with current content strategy",
            priority="low",
            category="content",
            action_required=False
        ))
    
    return insights

# API Endpoints
async def get_seo_dashboard_data() -> SEODashboardData:
    """Get comprehensive SEO dashboard data."""
    try:
        # For now, return mock data
        # In production, this would fetch real data from database
        return get_mock_seo_data()
    except Exception as e:
        logger.error(f"Error getting SEO dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Failed to get SEO dashboard data")

async def get_seo_health_score() -> SEOHealthScore:
    """Get current SEO health score."""
    try:
        mock_data = get_mock_seo_data()
        return mock_data.health_score
    except Exception as e:
        logger.error(f"Error getting SEO health score: {e}")
        raise HTTPException(status_code=500, detail="Failed to get SEO health score")

async def get_seo_metrics() -> Dict[str, SEOMetric]:
    """Get SEO metrics."""
    try:
        mock_data = get_mock_seo_data()
        return mock_data.metrics
    except Exception as e:
        logger.error(f"Error getting SEO metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get SEO metrics")

async def get_platform_status() -> Dict[str, PlatformStatus]:
    """Get platform connection status."""
    try:
        mock_data = get_mock_seo_data()
        return mock_data.platforms
    except Exception as e:
        logger.error(f"Error getting platform status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get platform status")

async def get_ai_insights() -> List[AIInsight]:
    """Get AI-generated insights."""
    try:
        mock_data = get_mock_seo_data()
        return mock_data.ai_insights
    except Exception as e:
        logger.error(f"Error getting AI insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to get AI insights")

async def seo_dashboard_health_check():
    """Health check for SEO dashboard."""
    return {"status": "healthy", "service": "SEO Dashboard API"}

# New comprehensive SEO analysis endpoints
async def analyze_seo_comprehensive(request: SEOAnalysisRequest) -> SEOAnalysisResponse:
    """
    Analyze a URL for comprehensive SEO performance (progressive mode)
    
    Args:
        request: SEOAnalysisRequest containing URL and optional target keywords
        
    Returns:
        SEOAnalysisResponse with detailed analysis results
    """
    try:
        logger.info(f"Starting progressive SEO analysis for URL: {request.url}")
        
        # Use progressive analysis for comprehensive results with timeout handling
        result = seo_analyzer.analyze_url_progressive(request.url, request.target_keywords)
        
        # Store result in database
        db_session = get_db_session()
        if db_session:
            try:
                seo_service = SEOAnalysisService(db_session)
                stored_analysis = seo_service.store_analysis_result(result)
                if stored_analysis:
                    logger.info(f"Stored progressive SEO analysis in database with ID: {stored_analysis.id}")
                else:
                    logger.warning("Failed to store SEO analysis in database")
            except Exception as db_error:
                logger.error(f"Database error during analysis storage: {str(db_error)}")
            finally:
                db_session.close()
        
        # Convert to response format
        response_data = {
            'url': result.url,
            'timestamp': result.timestamp,
            'overall_score': result.overall_score,
            'health_status': result.health_status,
            'critical_issues': result.critical_issues,
            'warnings': result.warnings,
            'recommendations': result.recommendations,
            'data': result.data,
            'success': True,
            'message': f"Progressive SEO analysis completed successfully for {result.url}"
        }
        
        logger.info(f"Progressive SEO analysis completed for {request.url}. Overall score: {result.overall_score}")
        return SEOAnalysisResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error analyzing SEO for {request.url}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing SEO: {str(e)}"
        )

async def analyze_seo_full(request: SEOAnalysisRequest) -> SEOAnalysisResponse:
    """
    Analyze a URL for comprehensive SEO performance (full analysis)
    
    Args:
        request: SEOAnalysisRequest containing URL and optional target keywords
        
    Returns:
        SEOAnalysisResponse with detailed analysis results
    """
    try:
        logger.info(f"Starting full SEO analysis for URL: {request.url}")
        
        # Use progressive analysis for comprehensive results
        result = seo_analyzer.analyze_url_progressive(request.url, request.target_keywords)
        
        # Store result in database
        db_session = get_db_session()
        if db_session:
            try:
                seo_service = SEOAnalysisService(db_session)
                stored_analysis = seo_service.store_analysis_result(result)
                if stored_analysis:
                    logger.info(f"Stored full SEO analysis in database with ID: {stored_analysis.id}")
                else:
                    logger.warning("Failed to store SEO analysis in database")
            except Exception as db_error:
                logger.error(f"Database error during analysis storage: {str(db_error)}")
            finally:
                db_session.close()
        
        # Convert to response format
        response_data = {
            'url': result.url,
            'timestamp': result.timestamp,
            'overall_score': result.overall_score,
            'health_status': result.health_status,
            'critical_issues': result.critical_issues,
            'warnings': result.warnings,
            'recommendations': result.recommendations,
            'data': result.data,
            'success': True,
            'message': f"Full SEO analysis completed successfully for {result.url}"
        }
        
        logger.info(f"Full SEO analysis completed for {request.url}. Overall score: {result.overall_score}")
        return SEOAnalysisResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error in full SEO analysis for {request.url}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error in full SEO analysis: {str(e)}"
        )

async def get_seo_metrics_detailed(url: str) -> SEOMetricsResponse:
    """
    Get detailed SEO metrics for dashboard display
    
    Args:
        url: The URL to analyze
        
    Returns:
        Detailed SEO metrics for React dashboard
    """
    try:
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        
        logger.info(f"Getting detailed SEO metrics for URL: {url}")
        
        # Perform analysis
        result = seo_analyzer.analyze_url_progressive(url)
        
        # Extract metrics for dashboard
        metrics = {
            "overall_score": result.overall_score,
            "health_status": result.health_status,
            "url_structure_score": result.data.get('url_structure', {}).get('score', 0),
            "meta_data_score": result.data.get('meta_data', {}).get('score', 0),
            "content_score": result.data.get('content_analysis', {}).get('score', 0),
            "technical_score": result.data.get('technical_seo', {}).get('score', 0),
            "performance_score": result.data.get('performance', {}).get('score', 0),
            "accessibility_score": result.data.get('accessibility', {}).get('score', 0),
            "user_experience_score": result.data.get('user_experience', {}).get('score', 0),
            "security_score": result.data.get('security_headers', {}).get('score', 0)
        }
        
        # Add detailed data for each category
        dashboard_data = {
            "metrics": metrics,
            "critical_issues": result.critical_issues,
            "warnings": result.warnings,
            "recommendations": result.recommendations,
            "detailed_analysis": {
                "url_structure": result.data.get('url_structure', {}),
                "meta_data": result.data.get('meta_data', {}),
                "content_analysis": result.data.get('content_analysis', {}),
                "technical_seo": result.data.get('technical_seo', {}),
                "performance": result.data.get('performance', {}),
                "accessibility": result.data.get('accessibility', {}),
                "user_experience": result.data.get('user_experience', {}),
                "security_headers": result.data.get('security_headers', {}),
                "keyword_analysis": result.data.get('keyword_analysis', {})
            },
            "timestamp": result.timestamp.isoformat(),
            "url": result.url
        }
        
        logger.info(f"Detailed SEO metrics retrieved for {url}")
        return SEOMetricsResponse(**dashboard_data)
        
    except Exception as e:
        logger.error(f"Error getting SEO metrics for {url}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting SEO metrics: {str(e)}"
        )

async def get_analysis_summary(url: str) -> Dict[str, Any]:
    """
    Get a quick summary of SEO analysis for a URL
    
    Args:
        url: The URL to analyze
        
    Returns:
        Summary of SEO analysis
    """
    try:
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        
        logger.info(f"Getting analysis summary for URL: {url}")
        
        # Perform analysis
        result = seo_analyzer.analyze_url_progressive(url)
        
        # Create summary
        summary = {
            "url": result.url,
            "overall_score": result.overall_score,
            "health_status": result.health_status,
            "critical_issues_count": len(result.critical_issues),
            "warnings_count": len(result.warnings),
            "recommendations_count": len(result.recommendations),
            "top_issues": result.critical_issues[:3],
            "top_recommendations": result.recommendations[:3],
            "analysis_timestamp": result.timestamp.isoformat()
        }
        
        logger.info(f"Analysis summary retrieved for {url}")
        return summary
        
    except Exception as e:
        logger.error(f"Error getting analysis summary for {url}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting analysis summary: {str(e)}"
        )

async def batch_analyze_urls(urls: List[str]) -> Dict[str, Any]:
    """
    Analyze multiple URLs in batch
    
    Args:
        urls: List of URLs to analyze
        
    Returns:
        Batch analysis results
    """
    try:
        logger.info(f"Starting batch analysis for {len(urls)} URLs")
        
        results = []
        
        for url in urls:
            try:
                # Ensure URL has protocol
                if not url.startswith(('http://', 'https://')):
                    url = f"https://{url}"
                
                # Perform analysis
                result = seo_analyzer.analyze_url_progressive(url)
                
                # Add to results
                results.append({
                    "url": result.url,
                    "overall_score": result.overall_score,
                    "health_status": result.health_status,
                    "critical_issues_count": len(result.critical_issues),
                    "warnings_count": len(result.warnings),
                    "success": True
                })
                
            except Exception as e:
                # Add error result
                results.append({
                    "url": url,
                    "overall_score": 0,
                    "health_status": "error",
                    "critical_issues_count": 0,
                    "warnings_count": 0,
                    "success": False,
                    "error": str(e)
                })
        
        batch_result = {
            "total_urls": len(urls),
            "successful_analyses": len([r for r in results if r['success']]),
            "failed_analyses": len([r for r in results if not r['success']]),
            "results": results
        }
        
        logger.info(f"Batch analysis completed. Success: {batch_result['successful_analyses']}/{len(urls)}")
        return batch_result
        
    except Exception as e:
        logger.error(f"Error in batch analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error in batch analysis: {str(e)}"
        ) 