"""FastAPI router for Facebook Writer endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging

from ..models import *
from ..services import *

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/facebook-writer",
    tags=["Facebook Writer"],
    responses={404: {"description": "Not found"}},
)

# Initialize services
post_service = FacebookPostService()
story_service = FacebookStoryService()
reel_service = FacebookReelService()
carousel_service = FacebookCarouselService()
event_service = FacebookEventService()
hashtag_service = FacebookHashtagService()
engagement_service = FacebookEngagementService()
group_post_service = FacebookGroupPostService()
page_about_service = FacebookPageAboutService()
ad_copy_service = FacebookAdCopyService()


@router.get("/health")
async def health_check():
    """Health check endpoint for Facebook Writer API."""
    return {"status": "healthy", "service": "Facebook Writer API"}


@router.get("/tools")
async def get_available_tools():
    """Get list of available Facebook Writer tools."""
    tools = [
        {
            "name": "FB Post Generator",
            "endpoint": "/post/generate",
            "description": "Create engaging Facebook posts that drive engagement and reach",
            "icon": "📝",
            "category": "Content Creation"
        },
        {
            "name": "FB Story Generator", 
            "endpoint": "/story/generate",
            "description": "Generate creative Facebook Stories with text overlays and engagement elements",
            "icon": "📱",
            "category": "Content Creation"
        },
        {
            "name": "FB Reel Generator",
            "endpoint": "/reel/generate", 
            "description": "Create engaging Facebook Reels scripts with trending music suggestions",
            "icon": "🎥",
            "category": "Content Creation"
        },
        {
            "name": "Carousel Generator",
            "endpoint": "/carousel/generate",
            "description": "Generate multi-image carousel posts with engaging captions for each slide",
            "icon": "🔄",
            "category": "Content Creation"
        },
        {
            "name": "Event Description Generator",
            "endpoint": "/event/generate",
            "description": "Create compelling event descriptions that drive attendance and engagement",
            "icon": "📅",
            "category": "Business Tools"
        },
        {
            "name": "Group Post Generator",
            "endpoint": "/group-post/generate",
            "description": "Generate engaging posts for Facebook Groups with community-focused content",
            "icon": "👥",
            "category": "Business Tools"
        },
        {
            "name": "Page About Generator",
            "endpoint": "/page-about/generate",
            "description": "Create professional and engaging About sections for your Facebook Page",
            "icon": "ℹ️",
            "category": "Business Tools"
        },
        {
            "name": "Ad Copy Generator",
            "endpoint": "/ad-copy/generate",
            "description": "Generate high-converting ad copy for Facebook Ads with targeting suggestions",
            "icon": "💰",
            "category": "Marketing Tools"
        },
        {
            "name": "Hashtag Generator",
            "endpoint": "/hashtags/generate",
            "description": "Generate trending and relevant hashtags for your Facebook content",
            "icon": "#️⃣",
            "category": "Marketing Tools"
        },
        {
            "name": "Engagement Analyzer",
            "endpoint": "/engagement/analyze",
            "description": "Analyze your content performance and get AI-powered improvement suggestions",
            "icon": "📊",
            "category": "Marketing Tools"
        }
    ]
    
    return {"tools": tools, "total_count": len(tools)}


# Content Creation Endpoints
@router.post("/post/generate", response_model=FacebookPostResponse)
async def generate_facebook_post(request: FacebookPostRequest):
    """Generate a Facebook post with engagement optimization."""
    try:
        logger.info(f"Generating Facebook post for business: {request.business_type}")
        response = post_service.generate_post(request)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating Facebook post: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/story/generate", response_model=FacebookStoryResponse)
async def generate_facebook_story(request: FacebookStoryRequest):
    """Generate a Facebook story with visual suggestions."""
    try:
        logger.info(f"Generating Facebook story for business: {request.business_type}")
        response = story_service.generate_story(request)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating Facebook story: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/reel/generate", response_model=FacebookReelResponse)
async def generate_facebook_reel(request: FacebookReelRequest):
    """Generate a Facebook reel script with music suggestions."""
    try:
        logger.info(f"Generating Facebook reel for business: {request.business_type}")
        response = reel_service.generate_reel(request)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating Facebook reel: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/carousel/generate", response_model=FacebookCarouselResponse)
async def generate_facebook_carousel(request: FacebookCarouselRequest):
    """Generate a Facebook carousel post with multiple slides."""
    try:
        logger.info(f"Generating Facebook carousel for business: {request.business_type}")
        response = carousel_service.generate_carousel(request)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating Facebook carousel: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Business Tools Endpoints
@router.post("/event/generate", response_model=FacebookEventResponse)
async def generate_facebook_event(request: FacebookEventRequest):
    """Generate a Facebook event description."""
    try:
        logger.info(f"Generating Facebook event: {request.event_name}")
        response = event_service.generate_event(request)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating Facebook event: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/group-post/generate", response_model=FacebookGroupPostResponse)
async def generate_facebook_group_post(request: FacebookGroupPostRequest):
    """Generate a Facebook group post following community guidelines."""
    try:
        logger.info(f"Generating Facebook group post for: {request.group_name}")
        response = group_post_service.generate_group_post(request)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating Facebook group post: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/page-about/generate", response_model=FacebookPageAboutResponse)
async def generate_facebook_page_about(request: FacebookPageAboutRequest):
    """Generate a Facebook page about section."""
    try:
        logger.info(f"Generating Facebook page about for: {request.business_name}")
        response = page_about_service.generate_page_about(request)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating Facebook page about: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Marketing Tools Endpoints
@router.post("/ad-copy/generate", response_model=FacebookAdCopyResponse)
async def generate_facebook_ad_copy(request: FacebookAdCopyRequest):
    """Generate Facebook ad copy with targeting suggestions."""
    try:
        logger.info(f"Generating Facebook ad copy for: {request.business_type}")
        response = ad_copy_service.generate_ad_copy(request)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating Facebook ad copy: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/hashtags/generate", response_model=FacebookHashtagResponse)
async def generate_facebook_hashtags(request: FacebookHashtagRequest):
    """Generate relevant hashtags for Facebook content."""
    try:
        logger.info(f"Generating Facebook hashtags for: {request.content_topic}")
        response = hashtag_service.generate_hashtags(request)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating Facebook hashtags: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/engagement/analyze", response_model=FacebookEngagementResponse)
async def analyze_facebook_engagement(request: FacebookEngagementRequest):
    """Analyze Facebook content for engagement optimization."""
    try:
        logger.info(f"Analyzing Facebook engagement for {request.content_type.value}")
        response = engagement_service.analyze_engagement(request)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return response
        
    except Exception as e:
        logger.error(f"Error analyzing Facebook engagement: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Utility Endpoints
@router.get("/post/templates")
async def get_post_templates():
    """Get predefined post templates."""
    templates = [
        {
            "name": "Product Launch",
            "description": "Template for announcing new products",
            "goal": "Promote a product/service",
            "tone": "Upbeat",
            "structure": "Hook + Features + Benefits + CTA"
        },
        {
            "name": "Educational Content",
            "description": "Template for sharing knowledge",
            "goal": "Share valuable content", 
            "tone": "Informative",
            "structure": "Problem + Solution + Tips + Engagement Question"
        },
        {
            "name": "Community Engagement",
            "description": "Template for building community",
            "goal": "Increase engagement",
            "tone": "Conversational",
            "structure": "Question + Context + Personal Experience + Call for Comments"
        }
    ]
    return {"templates": templates}


@router.get("/analytics/benchmarks")
async def get_analytics_benchmarks():
    """Get Facebook analytics benchmarks by industry."""
    benchmarks = {
        "general": {
            "average_engagement_rate": "3.91%",
            "average_reach": "5.5%",
            "best_posting_times": ["1 PM - 3 PM", "3 PM - 4 PM"]
        },
        "retail": {
            "average_engagement_rate": "4.2%",
            "average_reach": "6.1%",
            "best_posting_times": ["12 PM - 2 PM", "5 PM - 7 PM"]
        },
        "health_fitness": {
            "average_engagement_rate": "5.1%",
            "average_reach": "7.2%",
            "best_posting_times": ["6 AM - 8 AM", "6 PM - 8 PM"]
        }
    }
    return {"benchmarks": benchmarks}


@router.get("/compliance/guidelines")
async def get_compliance_guidelines():
    """Get Facebook content compliance guidelines."""
    guidelines = {
        "general": [
            "Avoid misleading or false information",
            "Don't use excessive capitalization",
            "Ensure claims are substantiated",
            "Respect intellectual property rights"
        ],
        "advertising": [
            "Include required disclaimers",
            "Avoid prohibited content categories",
            "Use appropriate targeting",
            "Follow industry-specific regulations"
        ],
        "community": [
            "Respect community standards",
            "Avoid spam or repetitive content",
            "Don't engage in artificial engagement",
            "Report violations appropriately"
        ]
    }
    return {"guidelines": guidelines}