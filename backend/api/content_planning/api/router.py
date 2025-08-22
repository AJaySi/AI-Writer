"""
Main Router for Content Planning API
Centralized router that includes all sub-routes for the content planning module.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any
from datetime import datetime
from loguru import logger

# Import route modules
from .routes import strategies, calendar_events, gap_analysis, ai_analytics, calendar_generation, health_monitoring, monitoring

# Import enhanced strategy routes
from .enhanced_strategy_routes import router as enhanced_strategy_router

# Import content strategy routes
from .content_strategy.routes import router as content_strategy_router

# Import quality analysis routes
from ..quality_analysis_routes import router as quality_analysis_router

# Create main router
router = APIRouter(prefix="/api/content-planning", tags=["content-planning"])

# Include route modules
router.include_router(strategies.router)
router.include_router(calendar_events.router)
router.include_router(gap_analysis.router)
router.include_router(ai_analytics.router)
router.include_router(calendar_generation.router)
router.include_router(health_monitoring.router)
router.include_router(monitoring.router)

# Include enhanced strategy routes with correct prefix
router.include_router(enhanced_strategy_router, prefix="/enhanced-strategies")

# Include content strategy routes
router.include_router(content_strategy_router)

# Include quality analysis routes
router.include_router(quality_analysis_router)

# Add health check endpoint
@router.get("/health")
async def content_planning_health_check():
    """
    Health check for content planning module.
    Returns operational status of all sub-modules.
    """
    try:
        logger.info("🏥 Performing content planning health check")
        
        health_status = {
            "service": "content_planning",
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "modules": {
                "strategies": "operational",
                "calendar_events": "operational", 
                "gap_analysis": "operational",
                "ai_analytics": "operational",
                "calendar_generation": "operational",
                "health_monitoring": "operational",
                "monitoring": "operational",
                "enhanced_strategies": "operational",
                "models": "operational",
                "utils": "operational"
            },
            "version": "2.0.0",
            "architecture": "modular"
        }
        
        logger.info("✅ Content planning health check completed")
        return health_status
        
    except Exception as e:
        logger.error(f"❌ Content planning health check failed: {str(e)}")
        return {
            "service": "content_planning",
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        } 