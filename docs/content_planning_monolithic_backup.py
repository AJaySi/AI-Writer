"""Content Planning API endpoints for ALwrity."""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import asyncio
from loguru import logger
from sqlalchemy.orm import Session
import time

# Import existing services
from services.api_key_manager import APIKeyManager
from services.validation import check_all_api_keys
from services.content_planning_service import ContentPlanningService
from services.user_data_service import UserDataService
from services.database import get_db_session, get_db

# Import database service
from services.content_planning_db import ContentPlanningDBService

# Import migrated content gap analysis services
from services.content_gap_analyzer.content_gap_analyzer import ContentGapAnalyzer
from services.content_gap_analyzer.competitor_analyzer import CompetitorAnalyzer
from services.content_gap_analyzer.keyword_researcher import KeywordResearcher
from services.content_gap_analyzer.ai_engine_service import AIEngineService
from services.content_gap_analyzer.website_analyzer import WebsiteAnalyzer

# Import new AI analytics service
from services.ai_analytics_service import AIAnalyticsService
from services.onboarding_data_service import OnboardingDataService

# Import new AI analysis database service
from services.ai_analysis_db_service import AIAnalysisDBService

# Import new calendar generator service
from services.calendar_generator_service import CalendarGeneratorService

# Initialize AI analysis database service
ai_analysis_db_service = AIAnalysisDBService()

# Initialize the content planning service
content_planning_service = ContentPlanningService()

# Initialize new calendar generator service
calendar_generator_service = CalendarGeneratorService()

# Initialize migrated services
content_gap_analyzer = ContentGapAnalyzer()
competitor_analyzer = CompetitorAnalyzer()
keyword_researcher = KeywordResearcher()
ai_engine_service = AIEngineService()
website_analyzer = WebsiteAnalyzer()

# Initialize new AI analytics service
ai_analytics_service = AIAnalyticsService()

# Pydantic models for Content Planning
class ContentStrategyRequest(BaseModel):
    industry: str
    target_audience: Dict[str, Any]
    business_goals: List[str]
    content_preferences: Dict[str, Any]
    competitor_urls: Optional[List[str]] = None

# New Pydantic models for database operations
class ContentStrategyCreate(BaseModel):
    user_id: int
    name: str
    industry: str
    target_audience: Dict[str, Any]
    content_pillars: Optional[List[Dict[str, Any]]] = None
    ai_recommendations: Optional[Dict[str, Any]] = None

class ContentStrategyResponse(BaseModel):
    id: int
    name: str
    industry: str
    target_audience: Dict[str, Any]
    content_pillars: List[Dict[str, Any]]
    ai_recommendations: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class CalendarEventCreate(BaseModel):
    strategy_id: int
    title: str
    description: str
    content_type: str
    platform: str
    scheduled_date: datetime
    ai_recommendations: Optional[Dict[str, Any]] = None

class CalendarEventResponse(BaseModel):
    id: int
    strategy_id: int
    title: str
    description: str
    content_type: str
    platform: str
    scheduled_date: datetime
    status: str
    ai_recommendations: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

class ContentGapAnalysisCreate(BaseModel):
    user_id: int
    website_url: str
    competitor_urls: List[str]
    target_keywords: Optional[List[str]] = None
    industry: Optional[str] = None
    analysis_results: Optional[Dict[str, Any]] = None
    recommendations: Optional[Dict[str, Any]] = None
    opportunities: Optional[Dict[str, Any]] = None

class ContentGapAnalysisResponse(BaseModel):
    id: int
    user_id: int
    website_url: str
    competitor_urls: List[str]
    target_keywords: Optional[List[str]] = None
    industry: Optional[str] = None
    analysis_results: Optional[Dict[str, Any]] = None
    recommendations: Optional[Dict[str, Any]] = None
    opportunities: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

class ContentGapAnalysisRequest(BaseModel):
    website_url: str
    competitor_urls: List[str]
    target_keywords: Optional[List[str]] = None
    industry: Optional[str] = None

class ContentGapAnalysisFullResponse(BaseModel):
    website_analysis: Dict[str, Any]
    competitor_analysis: Dict[str, Any]
    gap_analysis: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    opportunities: List[Dict[str, Any]]
    created_at: datetime

# New Pydantic models for AI Analytics
class ContentEvolutionRequest(BaseModel):
    strategy_id: int
    time_period: str = "30d"  # 7d, 30d, 90d, 1y

class PerformanceTrendsRequest(BaseModel):
    strategy_id: int
    metrics: Optional[List[str]] = None

class ContentPerformancePredictionRequest(BaseModel):
    strategy_id: int
    content_data: Dict[str, Any]

class StrategicIntelligenceRequest(BaseModel):
    strategy_id: int
    market_data: Optional[Dict[str, Any]] = None

class AIAnalyticsResponse(BaseModel):
    analysis_type: str
    strategy_id: int
    results: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    analysis_date: datetime

# New Pydantic models for Calendar Generation
class CalendarGenerationRequest(BaseModel):
    user_id: int
    strategy_id: Optional[int] = None
    calendar_type: str = Field("monthly", description="Type of calendar: monthly, weekly, custom")
    industry: Optional[str] = None
    business_size: str = Field("sme", description="Business size: startup, sme, enterprise")
    force_refresh: bool = Field(False, description="Force refresh calendar generation")

class CalendarGenerationResponse(BaseModel):
    user_id: int
    strategy_id: Optional[int]
    calendar_type: str
    industry: str
    business_size: str
    generated_at: datetime
    content_pillars: List[str]
    platform_strategies: Dict[str, Any]
    content_mix: Dict[str, float]
    daily_schedule: List[Dict[str, Any]]
    weekly_themes: List[Dict[str, Any]]
    content_recommendations: List[Dict[str, Any]]
    optimal_timing: Dict[str, Any]
    performance_predictions: Dict[str, Any]
    trending_topics: List[Dict[str, Any]]
    repurposing_opportunities: List[Dict[str, Any]]
    ai_insights: List[Dict[str, Any]]
    competitor_analysis: Dict[str, Any]
    gap_analysis_insights: Dict[str, Any]
    strategy_insights: Dict[str, Any]
    onboarding_insights: Dict[str, Any]
    processing_time: float
    ai_confidence: float

class ContentOptimizationRequest(BaseModel):
    user_id: int
    event_id: Optional[int] = None
    title: str
    description: str
    content_type: str
    target_platform: str
    original_content: Optional[Dict[str, Any]] = None

class ContentOptimizationResponse(BaseModel):
    user_id: int
    event_id: Optional[int]
    original_content: Dict[str, Any]
    optimized_content: Dict[str, Any]
    platform_adaptations: List[str]
    visual_recommendations: List[str]
    hashtag_suggestions: List[str]
    keyword_optimization: Dict[str, Any]
    tone_adjustments: Dict[str, Any]
    length_optimization: Dict[str, Any]
    performance_prediction: Dict[str, Any]
    optimization_score: float
    created_at: datetime

class PerformancePredictionRequest(BaseModel):
    user_id: int
    strategy_id: Optional[int] = None
    content_type: str
    platform: str
    content_data: Dict[str, Any]

class PerformancePredictionResponse(BaseModel):
    user_id: int
    strategy_id: Optional[int]
    content_type: str
    platform: str
    predicted_engagement_rate: float
    predicted_reach: int
    predicted_conversions: int
    predicted_roi: float
    confidence_score: float
    recommendations: List[str]
    created_at: datetime

class ContentRepurposingRequest(BaseModel):
    user_id: int
    strategy_id: Optional[int] = None
    original_content: Dict[str, Any]
    target_platforms: List[str]

class ContentRepurposingResponse(BaseModel):
    user_id: int
    strategy_id: Optional[int]
    original_content: Dict[str, Any]
    platform_adaptations: List[Dict[str, Any]]
    transformations: List[Dict[str, Any]]
    implementation_tips: List[str]
    gap_addresses: List[str]
    created_at: datetime

class TrendingTopicsRequest(BaseModel):
    user_id: int
    industry: str
    limit: int = Field(10, description="Number of trending topics to return")

class TrendingTopicsResponse(BaseModel):
    user_id: int
    industry: str
    trending_topics: List[Dict[str, Any]]
    gap_relevance_scores: Dict[str, float]
    audience_alignment_scores: Dict[str, float]
    created_at: datetime

# Create router
router = APIRouter(prefix="/api/content-planning", tags=["content-planning"])

# Database-integrated endpoints
@router.post("/strategies/", response_model=ContentStrategyResponse)
async def create_content_strategy(
    strategy: ContentStrategyCreate,
    db: Session = Depends(get_db)
):
    """Create a new content strategy."""
    try:
        logger.info(f"Creating content strategy: {strategy.name}")
        
        db_service = ContentPlanningDBService(db)
        strategy_data = strategy.dict()
        
        created_strategy = await db_service.create_content_strategy(strategy_data)
        
        if created_strategy:
            logger.info(f"Content strategy created successfully: {created_strategy.id}")
            return ContentStrategyResponse(**created_strategy.to_dict())
        else:
            raise HTTPException(status_code=500, detail="Failed to create content strategy")
            
    except Exception as e:
        logger.error(f"Error creating content strategy: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/strategies/", response_model=Dict[str, Any])
async def get_content_strategies(
    user_id: Optional[int] = Query(None, description="User ID"),
    strategy_id: Optional[int] = Query(None, description="Strategy ID")
):
    """
    Get content strategies with comprehensive logging for debugging.
    """
    try:
        logger.info(f"🚀 Starting content strategy analysis for user: {user_id}, strategy: {strategy_id}")
        
        # Check for existing strategy analysis in database
        logger.info(f"🔍 Checking database for existing strategy analysis for user {user_id or 'None'}")
        
        # Get latest AI analysis for strategic intelligence
        latest_analysis = await ai_analysis_db_service.get_latest_ai_analysis(
            user_id=user_id or 1, 
            analysis_type="strategic_intelligence"
        )
        
        if latest_analysis:
            logger.info(f"✅ Found existing strategy analysis in database: {latest_analysis.get('id', 'unknown')}")
            
            # Extract the actual strategic intelligence data from personalized_data_used
            # The strategic intelligence data is stored in personalized_data_used, not in results
            personalized_data = latest_analysis.get("personalized_data_used", {})
            
            # Generate strategic intelligence from the personalized data
            ai_analytics = AIAnalyticsService()
            strategic_intelligence = await ai_analytics.generate_strategic_intelligence(
                strategy_id=strategy_id or 1
            )
            
            logger.info("📊 CONTENT STRATEGY DATA BREAKDOWN:")
            logger.info(f"   - Strategy ID: {latest_analysis.get('id', 'N/A')}")
            logger.info(f"   - Analysis Date: {latest_analysis.get('analysis_date', 'N/A')}")
            logger.info(f"   - User ID: {latest_analysis.get('user_id', 'N/A')}")
            
            # Log strategic insights from the generated intelligence
            strategic_insights = strategic_intelligence.get("strategic_insights", [])
            logger.info(f"   - Strategic Insights Count: {len(strategic_insights)}")
            for i, insight in enumerate(strategic_insights[:3]):  # Log first 3 insights
                logger.info(f"     Insight {i+1}: {insight.get('insight', 'N/A')}")
                logger.info(f"       Type: {insight.get('type', 'N/A')}")
                logger.info(f"       Priority: {insight.get('priority', 'N/A')}")
                logger.info(f"       Impact: {insight.get('estimated_impact', 'N/A')}")
            
            # Log market positioning data
            market_positioning = strategic_intelligence.get("market_positioning", {})
            logger.info(f"   - Market Positioning: {market_positioning.get('industry_position', 'N/A')}")
            logger.info(f"   - Competitive Advantage: {market_positioning.get('competitive_advantage', 'N/A')}")
            logger.info(f"   - Market Share: {market_positioning.get('market_share', 'N/A')}")
            
            # Log strategic scores
            strategic_scores = strategic_intelligence.get("strategic_scores", {})
            logger.info(f"   - Strategic Scores:")
            for score_name, score_value in strategic_scores.items():
                logger.info(f"     {score_name}: {score_value}")
            
            # Log risk assessment
            risk_assessment = strategic_intelligence.get("risk_assessment", [])
            logger.info(f"   - Risk Assessment Count: {len(risk_assessment)}")
            for i, risk in enumerate(risk_assessment[:2]):  # Log first 2 risks
                logger.info(f"     Risk {i+1}: {risk.get('type', 'N/A')} - {risk.get('severity', 'N/A')}")
                logger.info(f"       Description: {risk.get('description', 'N/A')}")
            
            # Log opportunity analysis
            opportunity_analysis = strategic_intelligence.get("opportunity_analysis", [])
            logger.info(f"   - Opportunity Analysis Count: {len(opportunity_analysis)}")
            for i, opportunity in enumerate(opportunity_analysis[:2]):  # Log first 2 opportunities
                logger.info(f"     Opportunity {i+1}: {opportunity.get('title', 'N/A')}")
                logger.info(f"       Impact: {opportunity.get('estimated_impact', 'N/A')}")
            
            # Log recommendations
            recommendations = strategic_intelligence.get("recommendations", [])
            logger.info(f"   - Recommendations Count: {len(recommendations)}")
            for i, rec in enumerate(recommendations[:3]):  # Log first 3 recommendations
                logger.info(f"     Recommendation {i+1}: {rec.get('title', 'N/A')}")
                logger.info(f"       Priority: {rec.get('priority', 'N/A')}")
                logger.info(f"       Impact: {rec.get('estimated_impact', 'N/A')}")
            
            # Log the full strategy data structure
            logger.info("🔍 FULL STRATEGY DATA STRUCTURE:")
            logger.info(f"   - Strategic Intelligence Keys: {list(strategic_intelligence.keys())}")
            logger.info(f"   - Personalized Data Keys: {list(personalized_data.keys())}")
            
            return {
                "status": "success",
                "message": "Content strategy retrieved successfully",
                "data": {
                    "strategies": [strategic_intelligence],
                    "total_count": 1,
                    "user_id": user_id,
                    "analysis_date": latest_analysis.get("analysis_date"),
                    "strategic_insights": strategic_insights,
                    "market_positioning": market_positioning,
                    "strategic_scores": strategic_scores,
                    "risk_assessment": risk_assessment,
                    "opportunity_analysis": opportunity_analysis,
                    "recommendations": recommendations,
                    "personalized_data": personalized_data
                }
            }
        else:
            logger.warning("⚠️ No existing strategy analysis found in database")
            return {
                "status": "not_found",
                "message": "No content strategy found",
                "data": {
                    "strategies": [],
                    "total_count": 0,
                    "user_id": user_id
                }
            }
            
    except Exception as e:
        logger.error(f"❌ Error retrieving content strategies: {str(e)}")
        logger.error(f"Exception type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving content strategies: {str(e)}"
        )

@router.get("/strategies/{strategy_id}", response_model=ContentStrategyResponse)
async def get_content_strategy(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific content strategy by ID."""
    try:
        logger.info(f"Fetching content strategy: {strategy_id}")
        
        db_service = ContentPlanningDBService(db)
        strategy = await db_service.get_content_strategy(strategy_id)
        
        if strategy:
            return ContentStrategyResponse(**strategy.to_dict())
        else:
            raise HTTPException(status_code=404, detail="Content strategy not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting content strategy: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/strategies/{strategy_id}", response_model=ContentStrategyResponse)
async def update_content_strategy(
    strategy_id: int,
    update_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update a content strategy."""
    try:
        logger.info(f"Updating content strategy: {strategy_id}")
        
        db_service = ContentPlanningDBService(db)
        updated_strategy = await db_service.update_content_strategy(strategy_id, update_data)
        
        if updated_strategy:
            return ContentStrategyResponse(**updated_strategy.to_dict())
        else:
            raise HTTPException(status_code=404, detail="Content strategy not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating content strategy: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/strategies/{strategy_id}")
async def delete_content_strategy(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Delete a content strategy."""
    try:
        logger.info(f"Deleting content strategy: {strategy_id}")
        
        db_service = ContentPlanningDBService(db)
        deleted = await db_service.delete_content_strategy(strategy_id)
        
        if deleted:
            return {"message": f"Content strategy {strategy_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Content strategy not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting content strategy: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/calendar-events/", response_model=CalendarEventResponse)
async def create_calendar_event(
    event: CalendarEventCreate,
    db: Session = Depends(get_db)
):
    """Create a new calendar event."""
    try:
        logger.info(f"Creating calendar event: {event.title}")
        
        db_service = ContentPlanningDBService(db)
        event_data = event.dict()
        
        created_event = await db_service.create_calendar_event(event_data)
        
        if created_event:
            logger.info(f"Calendar event created successfully: {created_event.id}")
            return CalendarEventResponse(**created_event.to_dict())
        else:
            raise HTTPException(status_code=500, detail="Failed to create calendar event")
            
    except Exception as e:
        logger.error(f"Error creating calendar event: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/calendar-events/", response_model=List[CalendarEventResponse])
async def get_calendar_events(
    strategy_id: Optional[int] = Query(None, description="Filter by strategy ID"),
    db: Session = Depends(get_db)
):
    """Get calendar events, optionally filtered by strategy."""
    try:
        logger.info("Fetching calendar events")
        
        db_service = ContentPlanningDBService(db)
        
        if strategy_id:
            events = await db_service.get_strategy_calendar_events(strategy_id)
        else:
            # TODO: Implement get_all_calendar_events method
            events = []
        
        return [CalendarEventResponse(**event.to_dict()) for event in events]
        
    except Exception as e:
        logger.error(f"Error getting calendar events: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/calendar-events/{event_id}", response_model=CalendarEventResponse)
async def get_calendar_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific calendar event by ID."""
    try:
        logger.info(f"Fetching calendar event: {event_id}")
        
        db_service = ContentPlanningDBService(db)
        event = await db_service.get_calendar_event(event_id)
        
        if event:
            return CalendarEventResponse(**event.to_dict())
        else:
            raise HTTPException(status_code=404, detail="Calendar event not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting calendar event: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/calendar-events/{event_id}", response_model=CalendarEventResponse)
async def update_calendar_event(
    event_id: int,
    update_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update a calendar event."""
    try:
        logger.info(f"Updating calendar event: {event_id}")
        
        db_service = ContentPlanningDBService(db)
        updated_event = await db_service.update_calendar_event(event_id, update_data)
        
        if updated_event:
            return CalendarEventResponse(**updated_event.to_dict())
        else:
            raise HTTPException(status_code=404, detail="Calendar event not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating calendar event: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/calendar-events/{event_id}")
async def delete_calendar_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Delete a calendar event."""
    try:
        logger.info(f"Deleting calendar event: {event_id}")
        
        db_service = ContentPlanningDBService(db)
        deleted = await db_service.delete_calendar_event(event_id)
        
        if deleted:
            return {"message": f"Calendar event {event_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Calendar event not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting calendar event: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/gap-analysis/", response_model=ContentGapAnalysisResponse)
async def create_content_gap_analysis(
    analysis: ContentGapAnalysisCreate,
    db: Session = Depends(get_db)
):
    """Create a new content gap analysis."""
    try:
        logger.info(f"Creating content gap analysis for: {analysis.website_url}")
        
        db_service = ContentPlanningDBService(db)
        analysis_data = analysis.dict()
        
        created_analysis = await db_service.create_content_gap_analysis(analysis_data)
        
        if created_analysis:
            logger.info(f"Content gap analysis created successfully: {created_analysis.id}")
            return ContentGapAnalysisResponse(**created_analysis.to_dict())
        else:
            raise HTTPException(status_code=500, detail="Failed to create content gap analysis")
            
    except Exception as e:
        logger.error(f"Error creating content gap analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/gap-analysis/", response_model=Dict[str, Any])
async def get_content_gap_analyses(
    user_id: Optional[int] = Query(None, description="User ID"),
    strategy_id: Optional[int] = Query(None, description="Strategy ID"),
    force_refresh: bool = Query(False, description="Force refresh gap analysis")
):
    """Get content gap analysis with real AI insights - Database first approach."""
    try:
        logger.info(f"🚀 Starting content gap analysis for user: {user_id}, strategy: {strategy_id}, force_refresh: {force_refresh}")
        
        # Use user_id or default to 1
        current_user_id = user_id or 1
        
        # Skip database check if force_refresh is True
        if not force_refresh:
            # First, try to get existing gap analysis from database
            logger.info(f"🔍 Checking database for existing gap analysis for user {current_user_id}")
            existing_analysis = await ai_analysis_db_service.get_latest_ai_analysis(
                user_id=current_user_id,
                analysis_type="gap_analysis",
                strategy_id=strategy_id,
                max_age_hours=24  # Use cached results up to 24 hours old
            )
            
            if existing_analysis:
                logger.info(f"✅ Found existing gap analysis in database: {existing_analysis.id}")
                
                # Return cached results
                return {
                    "gap_analyses": [{"recommendations": existing_analysis.recommendations or []}],
                    "total_gaps": len(existing_analysis.recommendations or []),
                    "generated_at": existing_analysis.created_at.isoformat(),
                    "ai_service_status": existing_analysis.ai_service_status,
                    "personalized_data_used": True if existing_analysis.personalized_data_used else False,
                    "data_source": "database_cache",
                    "cache_age_hours": (datetime.utcnow() - existing_analysis.created_at).total_seconds() / 3600
                }
        
        # No recent analysis found or force refresh requested, run new AI analysis
        logger.info(f"🔄 Running new gap analysis for user {current_user_id} (force_refresh: {force_refresh})")
        
        # Get personalized inputs from onboarding data
        onboarding_service = OnboardingDataService()
        personalized_inputs = onboarding_service.get_personalized_ai_inputs(current_user_id)
        
        logger.info(f"📊 Using personalized inputs: {json.dumps(personalized_inputs, indent=2)}")
        
        # Generate real AI-powered gap analysis
        ai_engine = AIEngineService()
        gap_analysis = await ai_engine.generate_content_recommendations(personalized_inputs)
        
        logger.info(f"✅ AI gap analysis completed: {len(gap_analysis)} recommendations")
        
        # Store results in database
        try:
            await ai_analysis_db_service.store_ai_analysis_result(
                user_id=current_user_id,
                analysis_type="gap_analysis",
                insights=[],
                recommendations=gap_analysis,
                personalized_data=personalized_inputs,
                strategy_id=strategy_id,
                ai_service_status="operational"
            )
            logger.info(f"💾 Gap analysis results stored in database for user {current_user_id}")
        except Exception as e:
            logger.error(f"❌ Failed to store gap analysis in database: {str(e)}")
        
        return {
            "gap_analyses": [{"recommendations": gap_analysis}],
            "total_gaps": len(gap_analysis),
            "generated_at": datetime.utcnow().isoformat(),
            "ai_service_status": "operational",
            "personalized_data_used": True,
            "data_source": "ai_analysis"
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating content gap analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating content gap analysis: {str(e)}")

@router.get("/gap-analysis/{analysis_id}", response_model=ContentGapAnalysisResponse)
async def get_content_gap_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific content gap analysis by ID."""
    try:
        logger.info(f"Fetching content gap analysis: {analysis_id}")
        
        db_service = ContentPlanningDBService(db)
        analysis = await db_service.get_content_gap_analysis(analysis_id)
        
        if analysis:
            return ContentGapAnalysisResponse(**analysis.to_dict())
        else:
            raise HTTPException(status_code=404, detail="Content gap analysis not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting content gap analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/gap-analysis/analyze", response_model=ContentGapAnalysisFullResponse)
async def analyze_content_gaps(request: ContentGapAnalysisRequest):
    """
    Analyze content gaps between your website and competitors.
    """
    try:
        logger.info(f"Starting content gap analysis for: {request.website_url}")
        
        # Use migrated services for actual analysis
        analysis_results = {}
        
        # 1. Website Analysis
        logger.info("Performing website analysis...")
        website_analysis = await website_analyzer.analyze_website_content(request.website_url)
        analysis_results['website_analysis'] = website_analysis
        
        # 2. Competitor Analysis
        logger.info("Performing competitor analysis...")
        competitor_analysis = await competitor_analyzer.analyze_competitors(request.competitor_urls)
        analysis_results['competitor_analysis'] = competitor_analysis
        
        # 3. Keyword Research
        logger.info("Performing keyword research...")
        keyword_analysis = await keyword_researcher.research_keywords(
            industry=request.industry,
            target_keywords=request.target_keywords
        )
        analysis_results['keyword_analysis'] = keyword_analysis
        
        # 4. Content Gap Analysis
        logger.info("Performing content gap analysis...")
        gap_analysis = await content_gap_analyzer.identify_content_gaps(
            website_url=request.website_url,
            competitor_urls=request.competitor_urls,
            keyword_data=keyword_analysis
        )
        analysis_results['gap_analysis'] = gap_analysis
        
        # 5. AI-Powered Recommendations
        logger.info("Generating AI recommendations...")
        recommendations = await ai_engine_service.generate_recommendations(
            website_analysis=website_analysis,
            competitor_analysis=competitor_analysis,
            gap_analysis=gap_analysis,
            keyword_analysis=keyword_analysis
        )
        analysis_results['recommendations'] = recommendations
        
        # 6. Strategic Opportunities
        logger.info("Identifying strategic opportunities...")
        opportunities = await ai_engine_service.identify_strategic_opportunities(
            gap_analysis=gap_analysis,
            competitor_analysis=competitor_analysis,
            keyword_analysis=keyword_analysis
        )
        analysis_results['opportunities'] = opportunities
        
        # Prepare response
        response_data = {
            'website_analysis': analysis_results['website_analysis'],
            'competitor_analysis': analysis_results['competitor_analysis'],
            'gap_analysis': analysis_results['gap_analysis'],
            'recommendations': analysis_results['recommendations'],
            'opportunities': analysis_results['opportunities'],
            'created_at': datetime.utcnow()
        }
        
        logger.info(f"Content gap analysis completed successfully")
        return ContentGapAnalysisFullResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error analyzing content gaps: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing content gaps: {str(e)}"
        )

@router.get("/health")
async def content_planning_health_check():
    """
    Health check for content planning services.
    """
    try:
        # Check all migrated services
        service_status = {}
        
        # Test content gap analyzer
        try:
            await content_gap_analyzer.health_check()
            service_status['content_gap_analyzer'] = 'operational'
        except Exception as e:
            service_status['content_gap_analyzer'] = f'error: {str(e)}'
        
        # Test competitor analyzer
        try:
            await competitor_analyzer.health_check()
            service_status['competitor_analyzer'] = 'operational'
        except Exception as e:
            service_status['competitor_analyzer'] = f'error: {str(e)}'
        
        # Test keyword researcher
        try:
            await keyword_researcher.health_check()
            service_status['keyword_researcher'] = 'operational'
        except Exception as e:
            service_status['keyword_researcher'] = f'error: {str(e)}'
        
        # Test AI engine service
        try:
            await ai_engine_service.health_check()
            service_status['ai_engine_service'] = 'operational'
        except Exception as e:
            service_status['ai_engine_service'] = f'error: {str(e)}'
        
        # Test website analyzer
        try:
            await website_analyzer.health_check()
            service_status['website_analyzer'] = 'operational'
        except Exception as e:
            service_status['website_analyzer'] = f'error: {str(e)}'
        
        # Determine overall status
        operational_services = sum(1 for status in service_status.values() if status == 'operational')
        total_services = len(service_status)
        
        overall_status = 'healthy' if operational_services == total_services else 'degraded'
        
        health_status = {
            'status': overall_status,
            'services': service_status,
            'operational_services': operational_services,
            'total_services': total_services,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )

@router.get("/database/health")
async def database_health_check(db: Session = Depends(get_db)):
    """
    Health check for database operations.
    """
    try:
        logger.info("Performing database health check")
        
        db_service = ContentPlanningDBService(db)
        health_status = await db_service.health_check()
        
        logger.info(f"Database health check completed: {health_status['status']}")
        return health_status
        
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database health check failed: {str(e)}"
        )

# New AI Analytics Endpoints
@router.post("/ai-analytics/content-evolution", response_model=AIAnalyticsResponse)
async def analyze_content_evolution(request: ContentEvolutionRequest):
    """
    Analyze content evolution over time for a specific strategy.
    """
    try:
        logger.info(f"Starting content evolution analysis for strategy {request.strategy_id}")
        
        # Perform content evolution analysis
        evolution_analysis = await ai_analytics_service.analyze_content_evolution(
            strategy_id=request.strategy_id,
            time_period=request.time_period
        )
        
        # Prepare response
        response_data = {
            'analysis_type': 'content_evolution',
            'strategy_id': request.strategy_id,
            'results': evolution_analysis,
            'recommendations': evolution_analysis.get('recommendations', []),
            'analysis_date': datetime.utcnow()
        }
        
        logger.info(f"Content evolution analysis completed for strategy {request.strategy_id}")
        return AIAnalyticsResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error analyzing content evolution: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing content evolution: {str(e)}"
        )

@router.post("/ai-analytics/performance-trends", response_model=AIAnalyticsResponse)
async def analyze_performance_trends(request: PerformanceTrendsRequest):
    """
    Analyze performance trends for content strategy.
    """
    try:
        logger.info(f"Starting performance trends analysis for strategy {request.strategy_id}")
        
        # Perform performance trends analysis
        trends_analysis = await ai_analytics_service.analyze_performance_trends(
            strategy_id=request.strategy_id,
            metrics=request.metrics
        )
        
        # Prepare response
        response_data = {
            'analysis_type': 'performance_trends',
            'strategy_id': request.strategy_id,
            'results': trends_analysis,
            'recommendations': trends_analysis.get('recommendations', []),
            'analysis_date': datetime.utcnow()
        }
        
        logger.info(f"Performance trends analysis completed for strategy {request.strategy_id}")
        return AIAnalyticsResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error analyzing performance trends: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing performance trends: {str(e)}"
        )

@router.post("/ai-analytics/predict-performance", response_model=AIAnalyticsResponse)
async def predict_content_performance(request: ContentPerformancePredictionRequest):
    """
    Predict content performance using AI models.
    """
    try:
        logger.info(f"Starting content performance prediction for strategy {request.strategy_id}")
        
        # Perform content performance prediction
        prediction_results = await ai_analytics_service.predict_content_performance(
            content_data=request.content_data,
            strategy_id=request.strategy_id
        )
        
        # Prepare response
        response_data = {
            'analysis_type': 'content_performance_prediction',
            'strategy_id': request.strategy_id,
            'results': prediction_results,
            'recommendations': prediction_results.get('optimization_recommendations', []),
            'analysis_date': datetime.utcnow()
        }
        
        logger.info(f"Content performance prediction completed for strategy {request.strategy_id}")
        return AIAnalyticsResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error predicting content performance: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error predicting content performance: {str(e)}"
        )

@router.post("/ai-analytics/strategic-intelligence", response_model=AIAnalyticsResponse)
async def generate_strategic_intelligence(request: StrategicIntelligenceRequest):
    """
    Generate strategic intelligence for content planning.
    """
    try:
        logger.info(f"Starting strategic intelligence generation for strategy {request.strategy_id}")
        
        # Generate strategic intelligence
        intelligence_results = await ai_analytics_service.generate_strategic_intelligence(
            strategy_id=request.strategy_id,
            market_data=request.market_data
        )
        
        # Prepare response
        response_data = {
            'analysis_type': 'strategic_intelligence',
            'strategy_id': request.strategy_id,
            'results': intelligence_results,
            'recommendations': [],  # Strategic intelligence includes its own recommendations
            'analysis_date': datetime.utcnow()
        }
        
        logger.info(f"Strategic intelligence generation completed for strategy {request.strategy_id}")
        return AIAnalyticsResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error generating strategic intelligence: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating strategic intelligence: {str(e)}"
        )

@router.get("/ai-analytics/health")
async def ai_analytics_health_check():
    """
    Health check for AI analytics services.
    """
    try:
        # Check AI analytics service
        service_status = {}
        
        # Test AI analytics service
        try:
            # Test with a simple operation that doesn't require data
            # Just check if the service can be instantiated
            test_service = AIAnalyticsService()
            service_status['ai_analytics_service'] = 'operational'
        except Exception as e:
            service_status['ai_analytics_service'] = f'error: {str(e)}'
        
        # Determine overall status
        operational_services = sum(1 for status in service_status.values() if status == 'operational')
        total_services = len(service_status)
        
        overall_status = 'healthy' if operational_services == total_services else 'degraded'
        
        health_status = {
            'status': overall_status,
            'services': service_status,
            'operational_services': operational_services,
            'total_services': total_services,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return health_status
        
    except Exception as e:
        logger.error(f"AI analytics health check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"AI analytics health check failed: {str(e)}"
        )

# Additional database-integrated endpoints
@router.get("/ai-analytics/", response_model=Dict[str, Any])
async def get_ai_analytics(
    user_id: Optional[int] = Query(None, description="User ID"),
    strategy_id: Optional[int] = Query(None, description="Strategy ID"),
    force_refresh: bool = Query(False, description="Force refresh AI analysis")
):
    """Get AI analytics with real personalized insights - Database first approach."""
    try:
        logger.info(f"🚀 Starting AI analytics for user: {user_id}, strategy: {strategy_id}, force_refresh: {force_refresh}")
        start_time = time.time()
        
        # Use user_id or default to 1
        current_user_id = user_id or 1
        
        # Skip database check if force_refresh is True
        if not force_refresh:
            # First, try to get existing AI analysis from database
            logger.info(f"🔍 Checking database for existing AI analysis for user {current_user_id}")
            existing_analysis = await ai_analysis_db_service.get_latest_ai_analysis(
                user_id=current_user_id,
                analysis_type="comprehensive_analysis",
                strategy_id=strategy_id,
                max_age_hours=24  # Use cached results up to 24 hours old
            )
            
            if existing_analysis:
                logger.info(f"✅ Found existing AI analysis in database: {existing_analysis.id}")
                
                # Return cached results
                return {
                    "insights": existing_analysis.insights or [],
                    "recommendations": existing_analysis.recommendations or [],
                    "total_insights": len(existing_analysis.insights or []),
                    "total_recommendations": len(existing_analysis.recommendations or []),
                    "generated_at": existing_analysis.created_at.isoformat(),
                    "ai_service_status": existing_analysis.ai_service_status,
                    "processing_time": f"{existing_analysis.processing_time:.2f}s" if existing_analysis.processing_time else "cached",
                    "personalized_data_used": True if existing_analysis.personalized_data_used else False,
                    "data_source": "database_cache",
                    "cache_age_hours": (datetime.utcnow() - existing_analysis.created_at).total_seconds() / 3600,
                    "user_profile": existing_analysis.personalized_data_used or {}
                }
        
        # No recent analysis found or force refresh requested, run new AI analysis
        logger.info(f"🔄 Running new AI analysis for user {current_user_id} (force_refresh: {force_refresh})")
        
        # Get personalized inputs from onboarding data
        onboarding_service = OnboardingDataService()
        personalized_inputs = onboarding_service.get_personalized_ai_inputs(current_user_id)
        
        logger.info(f"📊 Using personalized inputs: {json.dumps(personalized_inputs, indent=2)}")
        
        # Initialize AI services
        ai_analytics = AIAnalyticsService()
        ai_engine = AIEngineService()
        
        # Generate real AI insights using personalized data
        logger.info("🔍 Generating performance analysis...")
        performance_analysis = await ai_analytics.analyze_performance_trends(
            strategy_id=strategy_id or 1
        )
        
        logger.info("🧠 Generating strategic intelligence...")
        strategic_intelligence = await ai_analytics.generate_strategic_intelligence(
            strategy_id=strategy_id or 1
        )
        
        logger.info("📈 Analyzing content evolution...")
        evolution_analysis = await ai_analytics.analyze_content_evolution(
            strategy_id=strategy_id or 1
        )
        
        logger.info("🎯 Generating content recommendations...")
        content_recommendations = await ai_engine.generate_content_recommendations(
            personalized_inputs
        )
        
        # Combine all insights
        insights = []
        recommendations = []
        
        if performance_analysis:
            insights.extend(performance_analysis.get('insights', []))
        if strategic_intelligence:
            insights.extend(strategic_intelligence.get('insights', []))
        if evolution_analysis:
            insights.extend(evolution_analysis.get('insights', []))
        if content_recommendations:
            recommendations.extend(content_recommendations)  # content_recommendations is already a list
        
        total_time = time.time() - start_time
        logger.info(f"🎉 AI analytics completed in {total_time:.2f}s: {len(insights)} insights, {len(recommendations)} recommendations")
        
        # Store results in database
        try:
            await ai_analysis_db_service.store_ai_analysis_result(
                user_id=current_user_id,
                analysis_type="comprehensive_analysis",
                insights=insights,
                recommendations=recommendations,
                performance_metrics=performance_analysis,
                personalized_data=personalized_inputs,
                processing_time=total_time,
                strategy_id=strategy_id,
                ai_service_status="operational" if len(insights) > 0 else "fallback"
            )
            logger.info(f"💾 AI analysis results stored in database for user {current_user_id}")
        except Exception as e:
            logger.error(f"❌ Failed to store AI analysis in database: {str(e)}")
        
        return {
            "insights": insights,
            "recommendations": recommendations,
            "total_insights": len(insights),
            "total_recommendations": len(recommendations),
            "generated_at": datetime.utcnow().isoformat(),
            "ai_service_status": "operational" if len(insights) > 0 else "fallback",
            "processing_time": f"{total_time:.2f}s",
            "personalized_data_used": True,
            "data_source": "ai_analysis",
            "user_profile": {
                "website_url": personalized_inputs.get('website_analysis', {}).get('website_url', ''),
                "content_types": personalized_inputs.get('website_analysis', {}).get('content_types', []),
                "target_audience": personalized_inputs.get('website_analysis', {}).get('target_audience', []),
                "industry_focus": personalized_inputs.get('website_analysis', {}).get('industry_focus', 'general')
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating AI analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating AI analytics: {str(e)}")

@router.get("/strategies/{strategy_id}/analytics")
async def get_strategy_analytics(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Get analytics for a specific strategy."""
    try:
        logger.info(f"Fetching analytics for strategy: {strategy_id}")
        
        db_service = ContentPlanningDBService(db)
        analytics = await db_service.get_strategy_analytics(strategy_id)
        
        return {
            'strategy_id': strategy_id,
            'analytics_count': len(analytics),
            'analytics': [analytic.to_dict() for analytic in analytics]
        }
        
    except Exception as e:
        logger.error(f"Error getting strategy analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/strategies/{strategy_id}/events")
async def get_strategy_events(
    strategy_id: int,
    status: Optional[str] = Query(None, description="Filter by event status"),
    db: Session = Depends(get_db)
):
    """Get calendar events for a specific strategy."""
    try:
        logger.info(f"Fetching events for strategy: {strategy_id}")
        
        db_service = ContentPlanningDBService(db)
        
        if status:
            events = await db_service.get_events_by_status(strategy_id, status)
        else:
            events = await db_service.get_strategy_calendar_events(strategy_id)
        
        return {
            'strategy_id': strategy_id,
            'events_count': len(events),
            'events': [event.to_dict() for event in events]
        }
        
    except Exception as e:
        logger.error(f"Error getting strategy events: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/users/{user_id}/recommendations")
async def get_user_recommendations(
    user_id: int,
    priority: Optional[str] = Query(None, description="Filter by priority"),
    db: Session = Depends(get_db)
):
    """Get content recommendations for a user."""
    try:
        logger.info(f"Fetching recommendations for user: {user_id}")
        
        db_service = ContentPlanningDBService(db)
        
        if priority:
            recommendations = await db_service.get_recommendations_by_priority(user_id, priority)
        else:
            recommendations = await db_service.get_user_content_recommendations(user_id)
        
        return {
            'user_id': user_id,
            'recommendations_count': len(recommendations),
            'recommendations': [rec.to_dict() for rec in recommendations]
        }
        
    except Exception as e:
        logger.error(f"Error getting user recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/strategies/{strategy_id}/summary")
async def get_strategy_summary(
    strategy_id: int,
    db: Session = Depends(get_db)
):
    """Get a comprehensive summary of a strategy with analytics."""
    try:
        logger.info(f"Fetching strategy summary: {strategy_id}")
        
        db_service = ContentPlanningDBService(db)
        
        # Get strategy with analytics
        strategies_with_analytics = await db_service.get_strategies_with_analytics(strategy_id)
        
        if strategies_with_analytics:
            return strategies_with_analytics[0]
        else:
            raise HTTPException(status_code=404, detail="Strategy not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting strategy summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") 

@router.get("/health/backend", response_model=Dict[str, Any])
async def check_backend_health():
    """
    Check core backend health (independent of AI services)
    """
    try:
        # Check basic backend functionality
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "api_server": True,
                "database_connection": False,  # Will be updated below
                "file_system": True,
                "memory_usage": "normal"
            },
            "version": "1.0.0"
        }
        
        # Test database connection
        try:
            from sqlalchemy import text
            db_session = get_db_session()
            result = db_session.execute(text("SELECT 1"))
            result.fetchone()
            health_status["services"]["database_connection"] = True
        except Exception as e:
            logger.warning(f"Database health check failed: {str(e)}")
            health_status["services"]["database_connection"] = False
        
        # Determine overall status
        all_services_healthy = all(health_status["services"].values())
        health_status["status"] = "healthy" if all_services_healthy else "degraded"
        
        return health_status
    except Exception as e:
        logger.error(f"Backend health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
            "services": {
                "api_server": False,
                "database_connection": False,
                "file_system": False,
                "memory_usage": "unknown"
            }
        }

@router.get("/health/ai", response_model=Dict[str, Any])
async def check_ai_services_health():
    """
    Check AI services health separately
    """
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "gemini_provider": False,
                "ai_analytics_service": False,
                "ai_engine_service": False
            }
        }
        
        # Test Gemini provider
        try:
            from llm_providers.gemini_provider import get_gemini_api_key
            api_key = get_gemini_api_key()
            if api_key:
                health_status["services"]["gemini_provider"] = True
        except Exception as e:
            logger.warning(f"Gemini provider health check failed: {e}")
        
        # Test AI Analytics Service
        try:
            from services.ai_analytics_service import AIAnalyticsService
            ai_service = AIAnalyticsService()
            health_status["services"]["ai_analytics_service"] = True
        except Exception as e:
            logger.warning(f"AI Analytics Service health check failed: {e}")
        
        # Test AI Engine Service
        try:
            from services.content_gap_analyzer.ai_engine_service import AIEngineService
            ai_engine = AIEngineService()
            health_status["services"]["ai_engine_service"] = True
        except Exception as e:
            logger.warning(f"AI Engine Service health check failed: {e}")
        
        # Determine overall AI status
        ai_services_healthy = any(health_status["services"].values())
        health_status["status"] = "healthy" if ai_services_healthy else "unhealthy"
        
        return health_status
    except Exception as e:
        logger.error(f"AI services health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
            "services": {
                "gemini_provider": False,
                "ai_analytics_service": False,
                "ai_engine_service": False
            }
        } 

@router.get("/ai-analytics/stream")
async def stream_ai_analytics_progress(
    user_id: Optional[int] = Query(None, description="User ID"),
    strategy_id: Optional[int] = Query(None, description="Strategy ID")
):
    """
    Stream AI analytics progress in real-time using Server-Sent Events
    """
    async def generate_progress():
        try:
            # Send initial connection message
            yield f"data: {json.dumps({'type': 'connected', 'message': 'Starting AI analysis...'})}\n\n"
            
            ai_service = AIAnalyticsService()
            current_strategy_id = strategy_id or 1
            
            # Step 1: Performance Analysis
            yield f"data: {json.dumps({'type': 'progress', 'step': 'performance', 'message': 'Analyzing performance trends...', 'progress': 20})}\n\n"
            
            performance_start = time.time()
            performance_analysis = await ai_service.analyze_performance_trends(
                strategy_id=current_strategy_id, 
                metrics=['engagement_rate', 'reach', 'conversion_rate']
            )
            performance_time = time.time() - performance_start
            
            yield f"data: {json.dumps({'type': 'progress', 'step': 'performance', 'message': f'Performance analysis completed in {performance_time:.2f}s', 'progress': 40})}\n\n"
            
            # Step 2: Strategic Intelligence
            yield f"data: {json.dumps({'type': 'progress', 'step': 'strategic', 'message': 'Generating strategic intelligence...', 'progress': 60})}\n\n"
            
            strategic_start = time.time()
            strategic_intelligence = await ai_service.generate_strategic_intelligence(strategy_id=current_strategy_id)
            strategic_time = time.time() - strategic_start
            
            yield f"data: {json.dumps({'type': 'progress', 'step': 'strategic', 'message': f'Strategic intelligence completed in {strategic_time:.2f}s', 'progress': 80})}\n\n"
            
            # Step 3: Content Evolution
            yield f"data: {json.dumps({'type': 'progress', 'step': 'evolution', 'message': 'Analyzing content evolution...', 'progress': 90})}\n\n"
            
            evolution_start = time.time()
            evolution_analysis = await ai_service.analyze_content_evolution(strategy_id=current_strategy_id, time_period="30d")
            evolution_time = time.time() - evolution_start
            
            yield f"data: {json.dumps({'type': 'progress', 'step': 'evolution', 'message': f'Content evolution analysis completed in {evolution_time:.2f}s', 'progress': 95})}\n\n"
            
            # Step 4: AI Engine Recommendations
            yield f"data: {json.dumps({'type': 'progress', 'step': 'ai_engine', 'message': 'Generating AI recommendations...', 'progress': 98})}\n\n"
            
            engine_start = time.time()
            from services.content_gap_analyzer.ai_engine_service import AIEngineService
            ai_engine = AIEngineService()
            analysis_data = {
                "website_analysis": {"content_types": ["blog", "video", "social"]},
                "competitor_analysis": {"top_performers": ["competitor1.com", "competitor2.com"]},
                "gap_analysis": {"content_gaps": ["AI content", "Video tutorials", "Case studies"]},
                "keyword_analysis": {"high_value_keywords": ["AI marketing", "Content automation", "Digital strategy"]}
            }
            ai_recommendations = await ai_engine.generate_content_recommendations(analysis_data)
            engine_time = time.time() - engine_start
            
            yield f"data: {json.dumps({'type': 'progress', 'step': 'ai_engine', 'message': f'AI recommendations completed in {engine_time:.2f}s', 'progress': 100})}\n\n"
            
            # Compile final results
            insights = []
            recommendations = []
            
            # Extract insights from performance analysis
            if 'trend_analysis' in performance_analysis:
                for metric, trend_data in performance_analysis['trend_analysis'].items():
                    if isinstance(trend_data, dict):
                        trend_direction = trend_data.get('trend_direction', 'stable')
                        change_percentage = trend_data.get('change_percentage', 0)
                        if trend_direction == 'increasing':
                            insights.append({
                                "id": f"perf_{metric}", 
                                "type": "performance", 
                                "title": f"{metric.replace('_', ' ').title()} Improvement", 
                                "description": f"Your {metric.replace('_', ' ')} is showing positive trends with {change_percentage}% improvement.", 
                                "priority": "high" if change_percentage > 20 else "medium", 
                                "created_at": datetime.utcnow().isoformat()
                            })
            
            # Extract insights from strategic intelligence
            if 'market_positioning' in strategic_intelligence:
                market_data = strategic_intelligence['market_positioning']
                positioning_score = market_data.get('positioning_score', 0)
                if positioning_score < 5:
                    insights.append({
                        "id": "market_position", 
                        "type": "warning", 
                        "title": "Market Positioning Needs Improvement", 
                        "description": f"Your market positioning score is {positioning_score}/10. Consider strategic adjustments.", 
                        "priority": "high", 
                        "created_at": datetime.utcnow().isoformat()
                    })
            
            # Add AI-generated insights
            if ai_recommendations and len(ai_recommendations) > 0:
                for i, rec in enumerate(ai_recommendations[:2]):
                    insights.append({
                        "id": f"ai_gen_{i+1}", 
                        "type": "ai_generated", 
                        "title": rec.get('title', 'AI-Generated Insight'), 
                        "description": rec.get('description', 'AI-powered content recommendation'), 
                        "priority": "high", 
                        "created_at": datetime.utcnow().isoformat()
                    })
                    recommendations.append({
                        "id": f"ai_rec_{i+1}", 
                        "type": "ai_recommendation", 
                        "title": rec.get('title', 'AI Recommendation'), 
                        "description": rec.get('description', ''), 
                        "confidence": rec.get('confidence', 90), 
                        "reasoning": "Generated by AI analysis of content gaps and opportunities", 
                        "action_items": rec.get('action_items', []), 
                        "status": "pending"
                    })
            
            # Send final results
            total_time = time.time() - performance_start
            final_results = {
                "type": "complete",
                "insights": insights,
                "recommendations": recommendations,
                "total_insights": len(insights),
                "total_recommendations": len(recommendations),
                "processing_time": f"{total_time:.2f}s",
                "ai_service_status": "operational" if len(insights) > 0 else "fallback"
            }
            
            yield f"data: {json.dumps(final_results)}\n\n"
            
        except Exception as e:
            error_message = {
                "type": "error",
                "message": f"AI analysis failed: {str(e)}",
                "error": str(e)
            }
            yield f"data: {json.dumps(error_message)}\n\n"
    
    return StreamingResponse(
        generate_progress(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    ) 

@router.get("/ai-analytics/results/{user_id}")
async def get_user_ai_analysis_results(
    user_id: int,
    analysis_type: Optional[str] = Query(None, description="Filter by analysis type"),
    limit: int = Query(10, description="Number of results to return")
):
    """Get AI analysis results for a specific user."""
    try:
        logger.info(f"Fetching AI analysis results for user {user_id}")
        
        analysis_types = [analysis_type] if analysis_type else None
        results = await ai_analysis_db_service.get_user_ai_analyses(
            user_id=user_id,
            analysis_types=analysis_types,
            limit=limit
        )
        
        return {
            "user_id": user_id,
            "results": [result.to_dict() for result in results],
            "total_results": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error fetching AI analysis results: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/ai-analytics/refresh/{user_id}")
async def refresh_ai_analysis(
    user_id: int,
    analysis_type: str = Query(..., description="Type of analysis to refresh"),
    strategy_id: Optional[int] = Query(None, description="Strategy ID")
):
    """Force refresh of AI analysis for a user."""
    try:
        logger.info(f"Force refreshing AI analysis for user {user_id}, type: {analysis_type}")
        
        # Delete existing analysis to force refresh
        await ai_analysis_db_service.delete_old_ai_analyses(days_old=0)
        
        # Run new analysis based on type
        if analysis_type == "comprehensive_analysis":
            # This will trigger a new comprehensive analysis
            return {"message": f"AI analysis refresh initiated for user {user_id}"}
        elif analysis_type == "gap_analysis":
            # This will trigger a new gap analysis
            return {"message": f"Gap analysis refresh initiated for user {user_id}"}
        elif analysis_type == "strategic_intelligence":
            # This will trigger a new strategic intelligence analysis
            return {"message": f"Strategic intelligence refresh initiated for user {user_id}"}
        else:
            raise HTTPException(status_code=400, detail=f"Unknown analysis type: {analysis_type}")
        
    except Exception as e:
        logger.error(f"Error refreshing AI analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/ai-analytics/cache/{user_id}")
async def clear_ai_analysis_cache(
    user_id: int,
    analysis_type: Optional[str] = Query(None, description="Specific analysis type to clear")
):
    """Clear AI analysis cache for a user."""
    try:
        logger.info(f"Clearing AI analysis cache for user {user_id}")
        
        if analysis_type:
            # Clear specific analysis type
            deleted_count = await ai_analysis_db_service.delete_old_ai_analyses(days_old=0)
            return {"message": f"Cleared {deleted_count} cached results for user {user_id}"}
        else:
            # Clear all cached results
            deleted_count = await ai_analysis_db_service.delete_old_ai_analyses(days_old=0)
            return {"message": f"Cleared {deleted_count} cached results for user {user_id}"}
        
    except Exception as e:
        logger.error(f"Error clearing AI analysis cache: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/ai-analytics/statistics")
async def get_ai_analysis_statistics(
    user_id: Optional[int] = Query(None, description="User ID for user-specific stats")
):
    """Get AI analysis statistics."""
    try:
        logger.info(f"📊 Getting AI analysis statistics for user: {user_id}")
        
        if user_id:
            # Get user-specific statistics
            user_stats = await ai_analysis_db_service.get_analysis_statistics(user_id)
            return {
                "user_id": user_id,
                "statistics": user_stats,
                "message": "User-specific AI analysis statistics retrieved successfully"
            }
        else:
            # Get global statistics
            global_stats = await ai_analysis_db_service.get_analysis_statistics()
            return {
                "statistics": global_stats,
                "message": "Global AI analysis statistics retrieved successfully"
            }
            
    except Exception as e:
        logger.error(f"❌ Error getting AI analysis statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get AI analysis statistics: {str(e)}"
        )

# ============================================================================
# NEW CALENDAR GENERATION ENDPOINTS
# ============================================================================

@router.post("/generate-calendar", response_model=CalendarGenerationResponse)
async def generate_comprehensive_calendar(request: CalendarGenerationRequest):
    """
    Generate a comprehensive AI-powered content calendar using database insights.
    This endpoint uses advanced AI analysis and comprehensive user data.
    """
    try:
        logger.info(f"🎯 Generating comprehensive calendar for user {request.user_id}")
        start_time = time.time()
        
        # Generate calendar using advanced AI-powered method
        calendar_data = await calendar_generator_service.generate_ai_powered_calendar(
            user_id=request.user_id,
            strategy_id=request.strategy_id,
            calendar_type=request.calendar_type,
            industry=request.industry,
            business_size=request.business_size
        )
        
        processing_time = time.time() - start_time
        
        logger.info(f"✅ Calendar generated successfully in {processing_time:.2f}s")
        
        return CalendarGenerationResponse(
            user_id=calendar_data["user_id"],
            strategy_id=calendar_data["strategy_id"],
            calendar_type=calendar_data["calendar_type"],
            industry=calendar_data["industry"],
            business_size=calendar_data["business_size"],
            generated_at=datetime.fromisoformat(calendar_data["generated_at"]),
            content_pillars=calendar_data["content_pillars"],
            platform_strategies=calendar_data["platform_strategies"],
            content_mix=calendar_data["content_mix"],
            daily_schedule=calendar_data["daily_schedule"],
            weekly_themes=calendar_data["weekly_themes"],
            content_recommendations=calendar_data["content_recommendations"],
            optimal_timing=calendar_data["optimal_timing"],
            performance_predictions=calendar_data["performance_predictions"],
            trending_topics=calendar_data["trending_topics"],
            repurposing_opportunities=calendar_data["repurposing_opportunities"],
            ai_insights=calendar_data["ai_insights"],
            competitor_analysis=calendar_data["competitor_analysis"],
            gap_analysis_insights=calendar_data["gap_analysis_insights"],
            strategy_insights=calendar_data["strategy_insights"],
            onboarding_insights=calendar_data["onboarding_insights"],
            processing_time=calendar_data["processing_time"],
            ai_confidence=calendar_data["ai_confidence"]
        )
        
    except Exception as e:
        logger.error(f"❌ Error generating comprehensive calendar: {str(e)}")
        logger.error(f"Exception type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating comprehensive calendar: {str(e)}"
        )

@router.post("/optimize-content", response_model=ContentOptimizationResponse)
async def optimize_content_for_platform(request: ContentOptimizationRequest):
    """
    Optimize content for specific platforms using database insights.
    
    This endpoint optimizes content based on:
    - Historical performance data for the platform
    - Audience preferences from onboarding data
    - Gap analysis insights for content improvement
    - Competitor analysis for differentiation
    """
    try:
        logger.info(f"🔧 Starting content optimization for user {request.user_id}")
        
        # Validate API keys
        api_key_status = await check_all_api_keys()
        if not api_key_status["all_keys_present"]:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI services are not properly configured"
            )
        
        # Get user data for optimization
        user_data = await calendar_generator_service._get_comprehensive_user_data(
            request.user_id, 
            None  # No strategy_id for content optimization
        )
        
        # Create optimization request for AI
        optimization_prompt = f"""
        Optimize the following content for {request.target_platform}:
        
        Original Content:
        - Title: {request.title}
        - Description: {request.description}
        - Content Type: {request.content_type}
        - Platform: {request.target_platform}
        
        User Context:
        - Industry: {user_data.get('industry', 'technology')}
        - Target Audience: {user_data.get('target_audience', {})}
        - Performance Data: {user_data.get('performance_data', {})}
        - Gap Analysis: {user_data.get('gap_analysis', {})}
        
        Provide comprehensive optimization including:
        1. Platform-specific adaptations
        2. Visual recommendations
        3. Hashtag suggestions
        4. Keyword optimization
        5. Tone adjustments
        6. Length optimization
        7. Performance predictions
        """
        
        # Generate optimization using AI
        optimization_result = await calendar_generator_service.ai_engine.generate_structured_response(
            prompt=optimization_prompt,
            schema={
                "type": "object",
                "properties": {
                    "optimized_content": {"type": "object"},
                    "platform_adaptations": {"type": "array", "items": {"type": "string"}},
                    "visual_recommendations": {"type": "array", "items": {"type": "string"}},
                    "hashtag_suggestions": {"type": "array", "items": {"type": "string"}},
                    "keyword_optimization": {"type": "object"},
                    "tone_adjustments": {"type": "object"},
                    "length_optimization": {"type": "object"},
                    "performance_prediction": {"type": "object"},
                    "optimization_score": {"type": "number"}
                }
            }
        )
        
        # Prepare response
        response_data = {
            "user_id": request.user_id,
            "event_id": request.event_id,
            "original_content": {
                "title": request.title,
                "description": request.description,
                "content_type": request.content_type,
                "target_platform": request.target_platform
            },
            "optimized_content": optimization_result.get("optimized_content", {}),
            "platform_adaptations": optimization_result.get("platform_adaptations", []),
            "visual_recommendations": optimization_result.get("visual_recommendations", []),
            "hashtag_suggestions": optimization_result.get("hashtag_suggestions", []),
            "keyword_optimization": optimization_result.get("keyword_optimization", {}),
            "tone_adjustments": optimization_result.get("tone_adjustments", {}),
            "length_optimization": optimization_result.get("length_optimization", {}),
            "performance_prediction": optimization_result.get("performance_prediction", {}),
            "optimization_score": optimization_result.get("optimization_score", 0.8),
            "created_at": datetime.utcnow()
        }
        
        logger.info(f"✅ Content optimization completed for user {request.user_id}")
        return ContentOptimizationResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error optimizing content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to optimize content: {str(e)}"
        )

@router.post("/performance-predictions", response_model=PerformancePredictionResponse)
async def predict_content_performance(request: PerformancePredictionRequest):
    """
    Predict content performance using database insights.
    
    This endpoint predicts performance based on:
    - Historical performance data
    - Audience demographics and preferences
    - Content type and platform patterns
    - Gap analysis opportunities
    """
    try:
        logger.info(f"📊 Starting performance prediction for user {request.user_id}")
        
        # Get user data for prediction
        user_data = await calendar_generator_service._get_comprehensive_user_data(
            request.user_id, 
            request.strategy_id
        )
        
        # Generate performance prediction
        prediction_prompt = f"""
        Predict performance for the following content:
        
        Content Data:
        - Content Type: {request.content_type}
        - Platform: {request.platform}
        - Content Data: {request.content_data}
        
        User Context:
        - Industry: {user_data.get('industry', 'technology')}
        - Performance Data: {user_data.get('performance_data', {})}
        - Gap Analysis: {user_data.get('gap_analysis', {})}
        - Audience Insights: {user_data.get('onboarding_data', {}).get('target_audience', {})}
        
        Provide performance predictions including:
        1. Engagement rate
        2. Reach estimates
        3. Conversion predictions
        4. ROI estimates
        5. Confidence score
        6. Recommendations
        """
        
        # Generate prediction using AI
        prediction_result = await calendar_generator_service.ai_engine.generate_structured_response(
            prompt=prediction_prompt,
            schema={
                "type": "object",
                "properties": {
                    "predicted_engagement_rate": {"type": "number"},
                    "predicted_reach": {"type": "integer"},
                    "predicted_conversions": {"type": "integer"},
                    "predicted_roi": {"type": "number"},
                    "confidence_score": {"type": "number"},
                    "recommendations": {"type": "array", "items": {"type": "string"}}
                }
            }
        )
        
        # Prepare response
        response_data = {
            "user_id": request.user_id,
            "strategy_id": request.strategy_id,
            "content_type": request.content_type,
            "platform": request.platform,
            "predicted_engagement_rate": prediction_result.get("predicted_engagement_rate", 0.05),
            "predicted_reach": prediction_result.get("predicted_reach", 1000),
            "predicted_conversions": prediction_result.get("predicted_conversions", 10),
            "predicted_roi": prediction_result.get("predicted_roi", 2.5),
            "confidence_score": prediction_result.get("confidence_score", 0.75),
            "recommendations": prediction_result.get("recommendations", []),
            "created_at": datetime.utcnow()
        }
        
        logger.info(f"✅ Performance prediction completed for user {request.user_id}")
        return PerformancePredictionResponse(**response_data)
        
    except Exception as e:
        logger.error(f"❌ Error predicting content performance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to predict content performance: {str(e)}"
        )

@router.post("/repurpose-content", response_model=ContentRepurposingResponse)
async def repurpose_content_across_platforms(request: ContentRepurposingRequest):
    """
    Repurpose content across different platforms using database insights.
    
    This endpoint suggests content repurposing based on:
    - Existing content and strategy data
    - Gap analysis opportunities
    - Platform-specific requirements
    - Audience preferences
    """
    try:
        logger.info(f"🔄 Starting content repurposing for user {request.user_id}")
        
        # Get user data for repurposing
        user_data = await calendar_generator_service._get_comprehensive_user_data(
            request.user_id, 
            request.strategy_id
        )
        
        # Generate repurposing suggestions
        repurposing_prompt = f"""
        Repurpose the following content for multiple platforms:
        
        Original Content:
        {request.original_content}
        
        Target Platforms:
        {request.target_platforms}
        
        User Context:
        - Gap Analysis: {user_data.get('gap_analysis', {})}
        - Strategy Data: {user_data.get('strategy_data', {})}
        - Recommendations: {user_data.get('recommendations_data', [])}
        
        Provide repurposing suggestions including:
        1. Platform-specific adaptations
        2. Content transformations
        3. Implementation tips
        4. Gap addressing opportunities
        """
        
        # Generate repurposing suggestions using AI
        repurposing_result = await calendar_generator_service.ai_engine.generate_structured_response(
            prompt=repurposing_prompt,
            schema={
                "type": "object",
                "properties": {
                    "platform_adaptations": {"type": "array", "items": {"type": "object"}},
                    "transformations": {"type": "array", "items": {"type": "object"}},
                    "implementation_tips": {"type": "array", "items": {"type": "string"}},
                    "gap_addresses": {"type": "array", "items": {"type": "string"}}
                }
            }
        )
        
        # Prepare response
        response_data = {
            "user_id": request.user_id,
            "strategy_id": request.strategy_id,
            "original_content": request.original_content,
            "platform_adaptations": repurposing_result.get("platform_adaptations", []),
            "transformations": repurposing_result.get("transformations", []),
            "implementation_tips": repurposing_result.get("implementation_tips", []),
            "gap_addresses": repurposing_result.get("gap_addresses", []),
            "created_at": datetime.utcnow()
        }
        
        logger.info(f"✅ Content repurposing completed for user {request.user_id}")
        return ContentRepurposingResponse(**response_data)
        
    except Exception as e:
        logger.error(f"❌ Error repurposing content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to repurpose content: {str(e)}"
        )

@router.get("/trending-topics", response_model=TrendingTopicsResponse)
async def get_trending_topics(
    user_id: int = Query(..., description="User ID"),
    industry: str = Query(..., description="Industry for trending topics"),
    limit: int = Query(10, description="Number of trending topics to return")
):
    """
    Get trending topics relevant to the user's industry and content gaps.
    
    This endpoint provides trending topics based on:
    - Industry-specific trends
    - Gap analysis keyword opportunities
    - Audience alignment assessment
    - Competitor analysis insights
    """
    try:
        logger.info(f"📈 Getting trending topics for user {user_id} in {industry}")
        
        # Get user data for trending topics
        user_data = await calendar_generator_service._get_comprehensive_user_data(user_id, None)
        
        # Get trending topics with database insights
        trending_topics = await calendar_generator_service._get_trending_topics_from_db(industry, user_data)
        
        # Limit results
        limited_topics = trending_topics[:limit]
        
        # Calculate relevance scores
        gap_relevance_scores = {}
        audience_alignment_scores = {}
        
        for topic in limited_topics:
            topic_key = topic.get("keyword", "")
            gap_relevance_scores[topic_key] = calendar_generator_service._assess_gap_relevance(topic, user_data.get("gap_analysis", {}))
            audience_alignment_scores[topic_key] = calendar_generator_service._assess_audience_alignment(topic, user_data.get("onboarding_data", {}))
        
        # Prepare response
        response_data = {
            "user_id": user_id,
            "industry": industry,
            "trending_topics": limited_topics,
            "gap_relevance_scores": gap_relevance_scores,
            "audience_alignment_scores": audience_alignment_scores,
            "created_at": datetime.utcnow()
        }
        
        logger.info(f"✅ Trending topics retrieved for user {user_id}")
        return TrendingTopicsResponse(**response_data)
        
    except Exception as e:
        logger.error(f"❌ Error getting trending topics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get trending topics: {str(e)}"
        )

@router.get("/comprehensive-user-data")
async def get_comprehensive_user_data(
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get comprehensive user data for calendar generation.
    This endpoint aggregates all data points needed for the calendar wizard.
    """
    try:
        logger.info(f"Getting comprehensive user data for user_id: {user_id}")
        
        # Get comprehensive data using the calendar generator service
        logger.info("Calling calendar generator service...")
        comprehensive_data = await calendar_generator_service._get_comprehensive_user_data(user_id, None)
        logger.info(f"Calendar generator service returned: {type(comprehensive_data)}")
        
        logger.info(f"Successfully retrieved comprehensive user data for user_id: {user_id}")
        
        return {
            "status": "success",
            "data": comprehensive_data,
            "message": "Comprehensive user data retrieved successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting comprehensive user data for user_id {user_id}: {str(e)}")
        logger.error(f"Exception type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving comprehensive user data: {str(e)}"
        )

@router.get("/calendar-generation/health")
async def calendar_generation_health_check():
    """
    Health check for calendar generation services.
    """
    try:
        logger.info("🏥 Performing calendar generation health check")
        
        # Check AI services
        api_key_status = await check_all_api_keys()
        
        # Check database connectivity
        db_status = "healthy"
        try:
            # Test database connection - only if calendar generator service is properly initialized
            if hasattr(calendar_generator_service, 'content_planning_db_service') and calendar_generator_service.content_planning_db_service is not None:
                await calendar_generator_service.content_planning_db_service.get_user_content_gap_analyses(1)
            else:
                db_status = "not_initialized"
        except Exception as e:
            db_status = f"error: {str(e)}"
        
        health_status = {
            "service": "calendar_generation",
            "status": "healthy" if api_key_status["all_keys_present"] and db_status == "healthy" else "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "ai_services": "healthy" if api_key_status["all_keys_present"] else "unhealthy",
                "database": db_status,
                "calendar_generator": "healthy"
            },
            "api_keys": api_key_status
        }
        
        logger.info("✅ Calendar generation health check completed")
        return health_status
        
    except Exception as e:
        logger.error(f"❌ Calendar generation health check failed: {str(e)}")
        return {
            "service": "calendar_generation",
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        } 

@router.get("/debug/strategies/{user_id}")
async def debug_content_strategies(user_id: int):
    """
    Debug endpoint to print content strategy data directly.
    """
    try:
        logger.info(f"🔍 DEBUG: Getting content strategy data for user {user_id}")
        
        # Get latest AI analysis
        latest_analysis = await ai_analysis_db_service.get_latest_ai_analysis(
            user_id=user_id, 
            analysis_type="strategic_intelligence"
        )
        
        if latest_analysis:
            logger.info("📊 DEBUG: Content Strategy Data Found")
            logger.info("=" * 50)
            logger.info("FULL CONTENT STRATEGY DATA:")
            logger.info("=" * 50)
            
            # Print the entire data structure
            import json
            logger.info(json.dumps(latest_analysis, indent=2, default=str))
            
            return {
                "status": "success",
                "message": "Content strategy data printed to logs",
                "data": latest_analysis
            }
        else:
            logger.warning("⚠️ DEBUG: No content strategy data found")
            return {
                "status": "not_found",
                "message": "No content strategy data found",
                "data": None
            }
            
    except Exception as e:
        logger.error(f"❌ DEBUG: Error getting content strategy data: {str(e)}")
        import traceback
        logger.error(f"DEBUG Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Debug error: {str(e)}"
        )