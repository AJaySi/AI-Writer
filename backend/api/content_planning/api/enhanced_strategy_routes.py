"""
Enhanced Strategy API Routes
Handles API endpoints for enhanced content strategy functionality.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from loguru import logger
import json
import asyncio
from datetime import datetime
from collections import defaultdict
import time

# Import database
from services.database import get_db_session

# Import services
from ..services.enhanced_strategy_service import EnhancedStrategyService
from ..services.enhanced_strategy_db_service import EnhancedStrategyDBService

# Import models
from models.enhanced_strategy_models import EnhancedContentStrategy

# Import utilities
from ..utils.error_handlers import ContentPlanningErrorHandler
from ..utils.response_builders import ResponseBuilder
from ..utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES

router = APIRouter(tags=["Enhanced Strategy"])

# Cache for streaming endpoints (5 minutes cache)
streaming_cache = defaultdict(dict)
CACHE_DURATION = 300  # 5 minutes

def get_cached_data(cache_key: str) -> Optional[Dict[str, Any]]:
    """Get cached data if it exists and is not expired."""
    if cache_key in streaming_cache:
        cached_data = streaming_cache[cache_key]
        if time.time() - cached_data.get("timestamp", 0) < CACHE_DURATION:
            return cached_data.get("data")
    return None

def set_cached_data(cache_key: str, data: Dict[str, Any]):
    """Set cached data with timestamp."""
    streaming_cache[cache_key] = {
        "data": data,
        "timestamp": time.time()
    }

# Helper function to get database session
def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()

async def stream_data(data_generator):
    """Helper function to stream data as Server-Sent Events"""
    async for chunk in data_generator:
        if isinstance(chunk, dict):
            yield f"data: {json.dumps(chunk)}\n\n"
        else:
            yield f"data: {json.dumps({'message': str(chunk)})}\n\n"
        await asyncio.sleep(0.1)  # Small delay to prevent overwhelming

@router.get("/stream/strategies")
async def stream_enhanced_strategies(
    user_id: Optional[int] = Query(None, description="User ID to filter strategies"),
    strategy_id: Optional[int] = Query(None, description="Specific strategy ID"),
    db: Session = Depends(get_db)
):
    """Stream enhanced strategies with real-time updates."""
    
    async def strategy_generator():
        try:
            logger.info(f"🚀 Starting strategy stream for user: {user_id}, strategy: {strategy_id}")
            
            # Send initial status
            yield {"type": "status", "message": "Starting strategy retrieval...", "timestamp": datetime.utcnow().isoformat()}
            
            db_service = EnhancedStrategyDBService(db)
            enhanced_service = EnhancedStrategyService(db_service)
            
            # Send progress update
            yield {"type": "progress", "message": "Querying database...", "progress": 25}
            
            strategies_data = await enhanced_service.get_enhanced_strategies(user_id, strategy_id, db)
            
            # Send progress update
            yield {"type": "progress", "message": "Processing strategies...", "progress": 50}
            
            if strategies_data.get("status") == "not_found":
                yield {"type": "result", "status": "not_found", "data": strategies_data}
                return
            
            # Send progress update
            yield {"type": "progress", "message": "Finalizing data...", "progress": 75}
            
            # Send final result
            yield {"type": "result", "status": "success", "data": strategies_data, "progress": 100}
            
            logger.info(f"✅ Strategy stream completed for user: {user_id}")
            
        except Exception as e:
            logger.error(f"❌ Error in strategy stream: {str(e)}")
            yield {"type": "error", "message": str(e), "timestamp": datetime.utcnow().isoformat()}
    
    return StreamingResponse(
        stream_data(strategy_generator()),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Credentials": "true"
        }
    )

@router.get("/stream/strategic-intelligence")
async def stream_strategic_intelligence(
    user_id: Optional[int] = Query(None, description="User ID"),
    db: Session = Depends(get_db)
):
    """Stream strategic intelligence data with real-time updates."""
    
    async def intelligence_generator():
        try:
            logger.info(f"🚀 Starting strategic intelligence stream for user: {user_id}")
            
            # Check cache first
            cache_key = f"strategic_intelligence_{user_id}"
            cached_data = get_cached_data(cache_key)
            if cached_data:
                logger.info(f"✅ Returning cached strategic intelligence data for user: {user_id}")
                yield {"type": "result", "status": "success", "data": cached_data, "progress": 100}
                return
            
            # Send initial status
            yield {"type": "status", "message": "Loading strategic intelligence...", "timestamp": datetime.utcnow().isoformat()}
            
            db_service = EnhancedStrategyDBService(db)
            enhanced_service = EnhancedStrategyService(db_service)
            
            # Send progress update
            yield {"type": "progress", "message": "Retrieving strategies...", "progress": 20}
            
            strategies_data = await enhanced_service.get_enhanced_strategies(user_id, None, db)
            
            # Send progress update
            yield {"type": "progress", "message": "Analyzing market positioning...", "progress": 40}
            
            if strategies_data.get("status") == "not_found":
                # Send fallback data
                fallback_data = {
                    "market_positioning": {
                        "score": 75,
                        "strengths": ["Strong brand voice", "Consistent content quality"],
                        "weaknesses": ["Limited video content", "Slow content production"]
                    },
                    "competitive_advantages": [
                        {"advantage": "AI-powered content creation", "impact": "High", "implementation": "In Progress"},
                        {"advantage": "Data-driven strategy", "impact": "Medium", "implementation": "Complete"}
                    ],
                    "strategic_risks": [
                        {"risk": "Content saturation in market", "probability": "Medium", "impact": "High"},
                        {"risk": "Algorithm changes affecting reach", "probability": "High", "impact": "Medium"}
                    ]
                }
                # Cache the fallback data
                set_cached_data(cache_key, fallback_data)
                yield {"type": "result", "status": "success", "data": fallback_data, "progress": 100}
                return
            
            # Extract strategic intelligence from first strategy
            strategy = strategies_data.get("strategies", [{}])[0]
            
            # Parse ai_recommendations if it's a JSON string
            ai_recommendations = {}
            if strategy.get("ai_recommendations"):
                try:
                    if isinstance(strategy["ai_recommendations"], str):
                        ai_recommendations = json.loads(strategy["ai_recommendations"])
                    else:
                        ai_recommendations = strategy["ai_recommendations"]
                except (json.JSONDecodeError, TypeError):
                    ai_recommendations = {}
            
            # Send progress update
            yield {"type": "progress", "message": "Extracting competitive analysis...", "progress": 60}
            
            strategic_data = {
                "market_positioning": {
                    "score": ai_recommendations.get("market_positioning", {}).get("score", 75),
                    "strengths": ai_recommendations.get("market_positioning", {}).get("strengths", ["Strong brand voice", "Consistent content quality"]),
                    "weaknesses": ai_recommendations.get("market_positioning", {}).get("weaknesses", ["Limited video content", "Slow content production"])
                },
                "competitive_advantages": ai_recommendations.get("competitive_advantages", [
                    {"advantage": "AI-powered content creation", "impact": "High", "implementation": "In Progress"},
                    {"advantage": "Data-driven strategy", "impact": "Medium", "implementation": "Complete"}
                ]),
                "strategic_risks": ai_recommendations.get("strategic_risks", [
                    {"risk": "Content saturation in market", "probability": "Medium", "impact": "High"},
                    {"risk": "Algorithm changes affecting reach", "probability": "High", "impact": "Medium"}
                ])
            }
            
            # Cache the strategic data
            set_cached_data(cache_key, strategic_data)
            
            # Send progress update
            yield {"type": "progress", "message": "Finalizing intelligence data...", "progress": 80}
            
            # Send final result
            yield {"type": "result", "status": "success", "data": strategic_data, "progress": 100}
            
            logger.info(f"✅ Strategic intelligence stream completed for user: {user_id}")
            
        except Exception as e:
            logger.error(f"❌ Error in strategic intelligence stream: {str(e)}")
            yield {"type": "error", "message": str(e), "timestamp": datetime.utcnow().isoformat()}
    
    return StreamingResponse(
        stream_data(intelligence_generator()),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Credentials": "true"
        }
    )

@router.get("/stream/keyword-research")
async def stream_keyword_research(
    user_id: Optional[int] = Query(None, description="User ID"),
    db: Session = Depends(get_db)
):
    """Stream keyword research data with real-time updates."""
    
    async def keyword_generator():
        try:
            logger.info(f"🚀 Starting keyword research stream for user: {user_id}")
            
            # Check cache first
            cache_key = f"keyword_research_{user_id}"
            cached_data = get_cached_data(cache_key)
            if cached_data:
                logger.info(f"✅ Returning cached keyword research data for user: {user_id}")
                yield {"type": "result", "status": "success", "data": cached_data, "progress": 100}
                return
            
            # Send initial status
            yield {"type": "status", "message": "Loading keyword research...", "timestamp": datetime.utcnow().isoformat()}
            
            # Import gap analysis service
            from ..services.gap_analysis_service import GapAnalysisService
            
            # Send progress update
            yield {"type": "progress", "message": "Retrieving gap analyses...", "progress": 20}
            
            gap_service = GapAnalysisService()
            gap_analyses = await gap_service.get_gap_analyses(user_id)
            
            # Send progress update
            yield {"type": "progress", "message": "Analyzing keyword opportunities...", "progress": 40}
            
            # Handle case where gap_analyses is 0, None, or empty
            if not gap_analyses or gap_analyses == 0 or len(gap_analyses) == 0:
                # Send fallback data
                fallback_data = {
                    "trend_analysis": {
                        "high_volume_keywords": [
                            {"keyword": "AI marketing automation", "volume": "10K-100K", "difficulty": "Medium"},
                            {"keyword": "content strategy 2024", "volume": "1K-10K", "difficulty": "Low"},
                            {"keyword": "digital marketing trends", "volume": "10K-100K", "difficulty": "High"}
                        ],
                        "trending_keywords": [
                            {"keyword": "AI content generation", "growth": "+45%", "opportunity": "High"},
                            {"keyword": "voice search optimization", "growth": "+32%", "opportunity": "Medium"},
                            {"keyword": "video marketing strategy", "growth": "+28%", "opportunity": "High"}
                        ]
                    },
                    "intent_analysis": {
                        "informational": ["how to", "what is", "guide to"],
                        "navigational": ["company name", "brand name", "website"],
                        "transactional": ["buy", "purchase", "download", "sign up"]
                    },
                    "opportunities": [
                        {"keyword": "AI content tools", "search_volume": "5K-10K", "competition": "Low", "cpc": "$2.50"},
                        {"keyword": "content marketing ROI", "search_volume": "1K-5K", "competition": "Medium", "cpc": "$4.20"},
                        {"keyword": "social media strategy", "search_volume": "10K-50K", "competition": "High", "cpc": "$3.80"}
                    ]
                }
                # Cache the fallback data
                set_cached_data(cache_key, fallback_data)
                yield {"type": "result", "status": "success", "data": fallback_data, "progress": 100}
                return
            
            # Extract keyword data from first gap analysis
            gap_analysis = gap_analyses[0] if isinstance(gap_analyses, list) else gap_analyses
            
            # Parse analysis_results if it's a JSON string
            analysis_results = {}
            if gap_analysis.get("analysis_results"):
                try:
                    if isinstance(gap_analysis["analysis_results"], str):
                        analysis_results = json.loads(gap_analysis["analysis_results"])
                    else:
                        analysis_results = gap_analysis["analysis_results"]
                except (json.JSONDecodeError, TypeError):
                    analysis_results = {}
            
            # Send progress update
            yield {"type": "progress", "message": "Processing keyword data...", "progress": 60}
            
            keyword_data = {
                "trend_analysis": {
                    "high_volume_keywords": analysis_results.get("opportunities", [])[:3] or [
                        {"keyword": "AI marketing automation", "volume": "10K-100K", "difficulty": "Medium"},
                        {"keyword": "content strategy 2024", "volume": "1K-10K", "difficulty": "Low"},
                        {"keyword": "digital marketing trends", "volume": "10K-100K", "difficulty": "High"}
                    ],
                    "trending_keywords": [
                        {"keyword": "AI content generation", "growth": "+45%", "opportunity": "High"},
                        {"keyword": "voice search optimization", "growth": "+32%", "opportunity": "Medium"},
                        {"keyword": "video marketing strategy", "growth": "+28%", "opportunity": "High"}
                    ]
                },
                "intent_analysis": {
                    "informational": ["how to", "what is", "guide to"],
                    "navigational": ["company name", "brand name", "website"],
                    "transactional": ["buy", "purchase", "download", "sign up"]
                },
                "opportunities": analysis_results.get("opportunities", []) or [
                    {"keyword": "AI content tools", "search_volume": "5K-10K", "competition": "Low", "cpc": "$2.50"},
                    {"keyword": "content marketing ROI", "search_volume": "1K-5K", "competition": "Medium", "cpc": "$4.20"},
                    {"keyword": "social media strategy", "search_volume": "10K-50K", "competition": "High", "cpc": "$3.80"}
                ]
            }
            
            # Cache the keyword data
            set_cached_data(cache_key, keyword_data)
            
            # Send progress update
            yield {"type": "progress", "message": "Finalizing keyword research...", "progress": 80}
            
            # Send final result
            yield {"type": "result", "status": "success", "data": keyword_data, "progress": 100}
            
            logger.info(f"✅ Keyword research stream completed for user: {user_id}")
            
        except Exception as e:
            logger.error(f"❌ Error in keyword research stream: {str(e)}")
            yield {"type": "error", "message": str(e), "timestamp": datetime.utcnow().isoformat()}
    
    return StreamingResponse(
        stream_data(keyword_generator()),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Credentials": "true"
        }
    )

@router.post("/create")
async def create_enhanced_strategy(
    strategy_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Create a new enhanced content strategy with 30+ strategic inputs."""
    try:
        logger.info("🚀 Creating enhanced content strategy")
        
        # Validate required fields
        if not strategy_data.get('user_id'):
            raise HTTPException(status_code=400, detail="user_id is required")
        
        if not strategy_data.get('name'):
            raise HTTPException(status_code=400, detail="strategy name is required")
        
        # Create enhanced strategy
        db_service = EnhancedStrategyDBService(db)
        enhanced_service = EnhancedStrategyService(db_service)
        created_strategy = await enhanced_service.create_enhanced_strategy(strategy_data, db)
        
        logger.info(f"✅ Enhanced strategy created successfully: {created_strategy.get('id')}")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced content strategy created successfully",
            data=created_strategy
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error creating enhanced strategy: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "create_enhanced_strategy")

@router.get("/")
async def get_enhanced_strategies(
    user_id: Optional[int] = Query(None, description="User ID to filter strategies"),
    strategy_id: Optional[int] = Query(None, description="Specific strategy ID"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get enhanced content strategies with comprehensive data and AI recommendations."""
    try:
        logger.info(f"🚀 Getting enhanced strategies for user: {user_id}, strategy: {strategy_id}")
        
        db_service = EnhancedStrategyDBService(db)
        enhanced_service = EnhancedStrategyService(db_service)
        strategies_data = await enhanced_service.get_enhanced_strategies(user_id, strategy_id, db)
        
        if strategies_data.get("status") == "not_found":
            return ResponseBuilder.create_not_found_response(
                message="No enhanced content strategies found",
                data=strategies_data
            )
        
        logger.info(f"✅ Retrieved {strategies_data.get('total_count', 0)} enhanced strategies")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced content strategies retrieved successfully",
            data=strategies_data
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting enhanced strategies: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategies")

@router.get("/onboarding-data")
async def get_onboarding_data(
    user_id: Optional[int] = Query(None, description="User ID to get onboarding data for"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get onboarding data for enhanced strategy auto-population."""
    try:
        logger.info(f"🚀 Getting onboarding data for user: {user_id}")
        
        db_service = EnhancedStrategyDBService(db)
        enhanced_service = EnhancedStrategyService(db_service)
        
        # Ensure we have a valid user_id
        actual_user_id = user_id or 1
        onboarding_data = await enhanced_service._get_onboarding_data(actual_user_id)
        
        logger.info(f"✅ Onboarding data retrieved successfully for user: {actual_user_id}")
        
        return ResponseBuilder.create_success_response(
            message="Onboarding data retrieved successfully",
            data=onboarding_data
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting onboarding data: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_onboarding_data")

@router.get("/tooltips")
async def get_enhanced_strategy_tooltips() -> Dict[str, Any]:
    """Get tooltip data for enhanced strategy fields."""
    try:
        logger.info("🚀 Getting enhanced strategy tooltips")
        
        # Mock tooltip data - in real implementation, this would come from a database
        tooltip_data = {
            "business_objectives": {
                "title": "Business Objectives",
                "description": "Define your primary and secondary business goals that content will support.",
                "examples": ["Increase brand awareness by 25%", "Generate 100 qualified leads per month"],
                "best_practices": ["Be specific and measurable", "Align with overall business strategy"]
            },
            "target_metrics": {
                "title": "Target Metrics",
                "description": "Specify the KPIs that will measure content strategy success.",
                "examples": ["Traffic growth: 30%", "Engagement rate: 5%", "Conversion rate: 2%"],
                "best_practices": ["Set realistic targets", "Track both leading and lagging indicators"]
            }
        }
        
        logger.info("✅ Enhanced strategy tooltips retrieved successfully")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced strategy tooltips retrieved successfully",
            data=tooltip_data
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting enhanced strategy tooltips: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategy_tooltips")

@router.get("/disclosure-steps")
async def get_enhanced_strategy_disclosure_steps() -> Dict[str, Any]:
    """Get progressive disclosure steps for enhanced strategy."""
    try:
        logger.info("🚀 Getting enhanced strategy disclosure steps")
        
        # Progressive disclosure steps configuration
        disclosure_steps = [
            {
                "id": "business_context",
                "title": "Business Context",
                "description": "Define your business objectives and context",
                "fields": ["business_objectives", "target_metrics", "content_budget", "team_size", "implementation_timeline", "market_share", "competitive_position", "performance_metrics"],
                "is_complete": False,
                "is_visible": True,
                "dependencies": []
            },
            {
                "id": "audience_intelligence",
                "title": "Audience Intelligence",
                "description": "Understand your target audience",
                "fields": ["content_preferences", "consumption_patterns", "audience_pain_points", "buying_journey", "seasonal_trends", "engagement_metrics"],
                "is_complete": False,
                "is_visible": False,
                "dependencies": ["business_context"]
            },
            {
                "id": "competitive_intelligence",
                "title": "Competitive Intelligence",
                "description": "Analyze your competitive landscape",
                "fields": ["top_competitors", "competitor_content_strategies", "market_gaps", "industry_trends", "emerging_trends"],
                "is_complete": False,
                "is_visible": False,
                "dependencies": ["audience_intelligence"]
            },
            {
                "id": "content_strategy",
                "title": "Content Strategy",
                "description": "Define your content approach",
                "fields": ["preferred_formats", "content_mix", "content_frequency", "optimal_timing", "quality_metrics", "editorial_guidelines", "brand_voice"],
                "is_complete": False,
                "is_visible": False,
                "dependencies": ["competitive_intelligence"]
            },
            {
                "id": "performance_analytics",
                "title": "Performance & Analytics",
                "description": "Set up measurement and optimization",
                "fields": ["traffic_sources", "conversion_rates", "content_roi_targets", "ab_testing_capabilities"],
                "is_complete": False,
                "is_visible": False,
                "dependencies": ["content_strategy"]
            }
        ]
        
        logger.info("✅ Enhanced strategy disclosure steps retrieved successfully")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced strategy disclosure steps retrieved successfully",
            data=disclosure_steps
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting enhanced strategy disclosure steps: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategy_disclosure_steps")

@router.get("/{strategy_id}")
async def get_enhanced_strategy_by_id(
    strategy_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get a specific enhanced content strategy by ID."""
    try:
        logger.info(f"🚀 Getting enhanced strategy: {strategy_id}")
        
        db_service = EnhancedStrategyDBService(db)
        strategy = await db_service.get_enhanced_strategy(strategy_id)
        
        if not strategy:
            raise ContentPlanningErrorHandler.handle_not_found_error("Enhanced strategy", strategy_id)
        
        # Get comprehensive data
        enhanced_service = EnhancedStrategyService(db_service)
        comprehensive_data = await enhanced_service.get_enhanced_strategies(
            strategy_id=strategy_id
        )
        
        logger.info(f"✅ Enhanced strategy retrieved successfully: {strategy_id}")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced content strategy retrieved successfully",
            data=comprehensive_data.get("strategies", [{}])[0] if comprehensive_data.get("strategies") else {}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting enhanced strategy: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategy_by_id")

@router.put("/{strategy_id}")
async def update_enhanced_strategy(
    strategy_id: int,
    update_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update an enhanced content strategy."""
    try:
        logger.info(f"🚀 Updating enhanced strategy: {strategy_id}")
        
        db_service = EnhancedStrategyDBService(db)
        updated_strategy = await db_service.update_enhanced_strategy(strategy_id, update_data)
        
        if not updated_strategy:
            raise ContentPlanningErrorHandler.handle_not_found_error("Enhanced strategy", strategy_id)
        
        logger.info(f"✅ Enhanced strategy updated successfully: {strategy_id}")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced content strategy updated successfully",
            data=updated_strategy.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error updating enhanced strategy: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "update_enhanced_strategy")

@router.delete("/{strategy_id}")
async def delete_enhanced_strategy(
    strategy_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Delete an enhanced content strategy."""
    try:
        logger.info(f"🚀 Deleting enhanced strategy: {strategy_id}")
        
        db_service = EnhancedStrategyDBService(db)
        deleted = await db_service.delete_enhanced_strategy(strategy_id)
        
        if not deleted:
            raise ContentPlanningErrorHandler.handle_not_found_error("Enhanced strategy", strategy_id)
        
        logger.info(f"✅ Enhanced strategy deleted successfully: {strategy_id}")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced content strategy deleted successfully",
            data={"strategy_id": strategy_id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting enhanced strategy: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "delete_enhanced_strategy")

@router.get("/{strategy_id}/analytics")
async def get_enhanced_strategy_analytics(
    strategy_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get comprehensive analytics for an enhanced strategy."""
    try:
        logger.info(f"🚀 Getting analytics for enhanced strategy: {strategy_id}")
        
        db_service = EnhancedStrategyDBService(db)
        
        # Get strategy with analytics
        strategies_with_analytics = await db_service.get_enhanced_strategies_with_analytics(
            strategy_id=strategy_id
        )
        
        if not strategies_with_analytics:
            raise ContentPlanningErrorHandler.handle_not_found_error("Enhanced strategy", strategy_id)
        
        strategy_analytics = strategies_with_analytics[0]
        
        logger.info(f"✅ Enhanced strategy analytics retrieved successfully: {strategy_id}")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced strategy analytics retrieved successfully",
            data=strategy_analytics
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting enhanced strategy analytics: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategy_analytics")

@router.get("/{strategy_id}/ai-analyses")
async def get_enhanced_strategy_ai_analysis(
    strategy_id: int,
    limit: int = Query(10, description="Number of AI analysis results to return"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get AI analysis history for an enhanced strategy."""
    try:
        logger.info(f"🚀 Getting AI analysis for enhanced strategy: {strategy_id}")
        
        db_service = EnhancedStrategyDBService(db)
        
        # Verify strategy exists
        strategy = await db_service.get_enhanced_strategy(strategy_id)
        if not strategy:
            raise ContentPlanningErrorHandler.handle_not_found_error("Enhanced strategy", strategy_id)
        
        # Get AI analysis history
        ai_analysis_history = await db_service.get_ai_analysis_history(strategy_id, limit)
        
        logger.info(f"✅ AI analysis history retrieved successfully: {strategy_id}")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced strategy AI analysis retrieved successfully",
            data={
                "strategy_id": strategy_id,
                "ai_analysis_history": ai_analysis_history,
                "total_analyses": len(ai_analysis_history)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting enhanced strategy AI analysis: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategy_ai_analysis")

@router.get("/{strategy_id}/completion")
async def get_enhanced_strategy_completion_stats(
    strategy_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get completion statistics for an enhanced strategy."""
    try:
        logger.info(f"🚀 Getting completion stats for enhanced strategy: {strategy_id}")
        
        db_service = EnhancedStrategyDBService(db)
        
        # Get strategy
        strategy = await db_service.get_enhanced_strategy(strategy_id)
        if not strategy:
            raise ContentPlanningErrorHandler.handle_not_found_error("Enhanced strategy", strategy_id)
        
        # Calculate completion stats
        completion_stats = {
            "strategy_id": strategy_id,
            "completion_percentage": strategy.completion_percentage,
            "total_fields": 30,  # 30+ strategic inputs
            "filled_fields": len([f for f in strategy.__dict__.keys() if getattr(strategy, f) is not None]),
            "missing_fields": 30 - len([f for f in strategy.__dict__.keys() if getattr(strategy, f) is not None]),
            "last_updated": strategy.updated_at.isoformat() if strategy.updated_at else None
        }
        
        logger.info(f"✅ Completion stats retrieved successfully: {strategy_id}")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced strategy completion stats retrieved successfully",
            data=completion_stats
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting enhanced strategy completion stats: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategy_completion_stats")

@router.get("/{strategy_id}/onboarding-integration")
async def get_enhanced_strategy_onboarding_integration(
    strategy_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get onboarding data integration for an enhanced strategy."""
    try:
        logger.info(f"🚀 Getting onboarding integration for enhanced strategy: {strategy_id}")
        
        db_service = EnhancedStrategyDBService(db)
        onboarding_integration = await db_service.get_onboarding_integration(strategy_id)
        
        if not onboarding_integration:
            return ResponseBuilder.create_not_found_response(
                message="No onboarding integration found for this strategy",
                data={"strategy_id": strategy_id}
            )
        
        logger.info(f"✅ Onboarding integration retrieved successfully: {strategy_id}")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced strategy onboarding integration retrieved successfully",
            data=onboarding_integration
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting onboarding integration: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_enhanced_strategy_onboarding_integration")

@router.post("/cache/clear")
async def clear_streaming_cache(
    user_id: Optional[int] = Query(None, description="User ID to clear cache for")
):
    """Clear streaming cache for a specific user or all users."""
    try:
        logger.info(f"🚀 Clearing streaming cache for user: {user_id}")
        
        if user_id:
            # Clear cache for specific user
            cache_keys_to_remove = [
                f"strategic_intelligence_{user_id}",
                f"keyword_research_{user_id}"
            ]
            for key in cache_keys_to_remove:
                if key in streaming_cache:
                    del streaming_cache[key]
                    logger.info(f"✅ Cleared cache for key: {key}")
        else:
            # Clear all cache
            streaming_cache.clear()
            logger.info("✅ Cleared all streaming cache")
        
        return ResponseBuilder.create_success_response(
            message="Streaming cache cleared successfully",
            data={"cleared_for_user": user_id}
        )
        
    except Exception as e:
        logger.error(f"❌ Error clearing streaming cache: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "clear_streaming_cache")

@router.post("/{strategy_id}/ai-recommendations")
async def generate_enhanced_ai_recommendations(
    strategy_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Generate AI recommendations for an enhanced strategy."""
    try:
        logger.info(f"🚀 Generating AI recommendations for enhanced strategy: {strategy_id}")
        
        # Get strategy
        db_service = EnhancedStrategyDBService(db)
        strategy = await db_service.get_enhanced_strategy(strategy_id)
        
        if not strategy:
            raise ContentPlanningErrorHandler.handle_not_found_error("Enhanced strategy", strategy_id)
        
        # Generate AI recommendations
        enhanced_service = EnhancedStrategyService(db_service)
        await enhanced_service._generate_comprehensive_ai_recommendations(strategy, db)
        
        # Get updated strategy data
        updated_strategy = await db_service.get_enhanced_strategy(strategy_id)
        
        logger.info(f"✅ AI recommendations generated successfully: {strategy_id}")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced strategy AI recommendations generated successfully",
            data=updated_strategy.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error generating AI recommendations: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "generate_enhanced_ai_recommendations")

@router.post("/{strategy_id}/ai-analysis/regenerate")
async def regenerate_enhanced_strategy_ai_analysis(
    strategy_id: int,
    analysis_type: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Regenerate AI analysis for an enhanced strategy."""
    try:
        logger.info(f"🚀 Regenerating AI analysis for enhanced strategy: {strategy_id}, type: {analysis_type}")
        
        # Get strategy
        db_service = EnhancedStrategyDBService(db)
        strategy = await db_service.get_enhanced_strategy(strategy_id)
        
        if not strategy:
            raise ContentPlanningErrorHandler.handle_not_found_error("Enhanced strategy", strategy_id)
        
        # Regenerate AI analysis
        enhanced_service = EnhancedStrategyService(db_service)
        await enhanced_service._generate_specialized_recommendations(strategy, analysis_type, db)
        
        # Get updated strategy data
        updated_strategy = await db_service.get_enhanced_strategy(strategy_id)
        
        logger.info(f"✅ AI analysis regenerated successfully: {strategy_id}")
        
        return ResponseBuilder.create_success_response(
            message="Enhanced strategy AI analysis regenerated successfully",
            data=updated_strategy.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error regenerating AI analysis: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "regenerate_enhanced_strategy_ai_analysis") 