"""
FastAPI endpoint for the Comprehensive SEO Analyzer
Provides data for the React SEO Dashboard
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

from .comprehensive_seo_analyzer import ComprehensiveSEOAnalyzer, SEOAnalysisResult

app = FastAPI(
    title="Comprehensive SEO Analyzer API",
    description="API for analyzing website SEO performance with actionable insights",
    version="1.0.0"
)

# Initialize the analyzer
seo_analyzer = ComprehensiveSEOAnalyzer()

class SEOAnalysisRequest(BaseModel):
    url: HttpUrl
    target_keywords: Optional[List[str]] = None

class SEOAnalysisResponse(BaseModel):
    url: str
    timestamp: datetime
    overall_score: int
    health_status: str
    critical_issues: List[str]
    warnings: List[str]
    recommendations: List[str]
    data: Dict[str, Any]
    success: bool
    message: str

@app.post("/analyze-seo", response_model=SEOAnalysisResponse)
async def analyze_seo(request: SEOAnalysisRequest):
    """
    Analyze a URL for comprehensive SEO performance
    
    Args:
        request: SEOAnalysisRequest containing URL and optional target keywords
        
    Returns:
        SEOAnalysisResponse with detailed analysis results
    """
    try:
        # Convert URL to string
        url_str = str(request.url)
        
        # Perform analysis
        result = seo_analyzer.analyze_url(url_str, request.target_keywords)
        
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
            'message': f"SEO analysis completed successfully for {result.url}"
        }
        
        return SEOAnalysisResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing SEO: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "service": "Comprehensive SEO Analyzer API"
    }

@app.get("/analysis-summary/{url:path}")
async def get_analysis_summary(url: str):
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
        
        # Perform analysis
        result = seo_analyzer.analyze_url(url)
        
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
        
        return summary
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting analysis summary: {str(e)}"
        )

@app.get("/seo-metrics/{url:path}")
async def get_seo_metrics(url: str):
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
        
        # Perform analysis
        result = seo_analyzer.analyze_url(url)
        
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
        
        return dashboard_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting SEO metrics: {str(e)}"
        )

@app.post("/batch-analyze")
async def batch_analyze(urls: List[str]):
    """
    Analyze multiple URLs in batch
    
    Args:
        urls: List of URLs to analyze
        
    Returns:
        Batch analysis results
    """
    try:
        results = []
        
        for url in urls:
            try:
                # Ensure URL has protocol
                if not url.startswith(('http://', 'https://')):
                    url = f"https://{url}"
                
                # Perform analysis
                result = seo_analyzer.analyze_url(url)
                
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
        
        return {
            "total_urls": len(urls),
            "successful_analyses": len([r for r in results if r['success']]),
            "failed_analyses": len([r for r in results if not r['success']]),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in batch analysis: {str(e)}"
        )

# Enhanced prompts for better results
ENHANCED_PROMPTS = {
    "critical_issue": "🚨 CRITICAL: This issue is severely impacting your SEO performance and must be fixed immediately.",
    "warning": "⚠️ WARNING: This could be improved to boost your search rankings.",
    "recommendation": "💡 RECOMMENDATION: Implement this to improve your SEO score.",
    "excellent": "🎉 EXCELLENT: Your SEO is performing very well in this area!",
    "good": "✅ GOOD: Your SEO is performing well, with room for minor improvements.",
    "needs_improvement": "🔧 NEEDS IMPROVEMENT: Several areas need attention to boost your SEO.",
    "poor": "❌ POOR: Significant improvements needed across multiple areas."
}

def enhance_analysis_result(result: SEOAnalysisResult) -> SEOAnalysisResult:
    """
    Enhance analysis results with better prompts and user-friendly language
    """
    # Enhance critical issues
    enhanced_critical_issues = []
    for issue in result.critical_issues:
        enhanced_issue = f"{ENHANCED_PROMPTS['critical_issue']} {issue}"
        enhanced_critical_issues.append(enhanced_issue)
    
    # Enhance warnings
    enhanced_warnings = []
    for warning in result.warnings:
        enhanced_warning = f"{ENHANCED_PROMPTS['warning']} {warning}"
        enhanced_warnings.append(enhanced_warning)
    
    # Enhance recommendations
    enhanced_recommendations = []
    for rec in result.recommendations:
        enhanced_rec = f"{ENHANCED_PROMPTS['recommendation']} {rec}"
        enhanced_recommendations.append(enhanced_rec)
    
    # Create enhanced result
    enhanced_result = SEOAnalysisResult(
        url=result.url,
        timestamp=result.timestamp,
        overall_score=result.overall_score,
        health_status=result.health_status,
        critical_issues=enhanced_critical_issues,
        warnings=enhanced_warnings,
        recommendations=enhanced_recommendations,
        data=result.data
    )
    
    return enhanced_result

@app.post("/analyze-seo-enhanced", response_model=SEOAnalysisResponse)
async def analyze_seo_enhanced(request: SEOAnalysisRequest):
    """
    Analyze a URL with enhanced, user-friendly prompts
    
    Args:
        request: SEOAnalysisRequest containing URL and optional target keywords
        
    Returns:
        SEOAnalysisResponse with enhanced, user-friendly analysis results
    """
    try:
        # Convert URL to string
        url_str = str(request.url)
        
        # Perform analysis
        result = seo_analyzer.analyze_url(url_str, request.target_keywords)
        
        # Enhance results
        enhanced_result = enhance_analysis_result(result)
        
        # Convert to response format
        response_data = {
            'url': enhanced_result.url,
            'timestamp': enhanced_result.timestamp,
            'overall_score': enhanced_result.overall_score,
            'health_status': enhanced_result.health_status,
            'critical_issues': enhanced_result.critical_issues,
            'warnings': enhanced_result.warnings,
            'recommendations': enhanced_result.recommendations,
            'data': enhanced_result.data,
            'success': True,
            'message': f"Enhanced SEO analysis completed successfully for {enhanced_result.url}"
        }
        
        return SEOAnalysisResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing SEO: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 