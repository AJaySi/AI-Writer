"""
API endpoints for social media connections and OAuth management.
Handles authentication, connection management, and analytics fetching.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import logging

from services.database import get_db
from services.oauth_service import oauth_service
from services.gsc_analytics_service import gsc_analytics_service
from services.social_posting_service import social_posting_service
from models.social_connections import SocialConnection, SocialAnalytics, SocialPost

# Setup logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/social", tags=["social_connections"])

# Pydantic models
class ConnectionResponse(BaseModel):
    id: int
    platform: str
    platform_username: str
    connection_status: str
    auto_post_enabled: bool
    analytics_enabled: bool
    connected_at: str
    expires_at: Optional[str]
    profile_data: Dict

class AnalyticsResponse(BaseModel):
    connection_id: int
    metric_name: str
    metric_value: Dict
    date_range_start: Optional[str]
    date_range_end: Optional[str]
    fetched_at: str

class AuthUrlResponse(BaseModel):
    auth_url: str
    state_token: str
    platform: str

class PostContentRequest(BaseModel):
    content: str
    media_urls: Optional[List[str]] = None
    scheduled_at: Optional[str] = None

class PostResponse(BaseModel):
    success: bool
    message: str
    post_id: Optional[int] = None
    platform_post_id: Optional[str] = None
    platform_url: Optional[str] = None

# OAuth endpoints
@router.get("/auth/{platform}", response_model=AuthUrlResponse)
async def initiate_oauth(
    platform: str,
    user_id: int = Query(default=1),  # In production, get from authenticated user
    db: Session = Depends(get_db)
):
    """Initiate OAuth flow for a social media platform."""
    try:
        auth_url, state_token = oauth_service.generate_auth_url(platform, user_id)
        
        return AuthUrlResponse(
            auth_url=auth_url,
            state_token=state_token,
            platform=platform
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to initiate OAuth for {platform}: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate authentication")

@router.get("/oauth/callback/{platform}")
async def oauth_callback(
    platform: str,
    code: str = Query(...),
    state: str = Query(...),
    error: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Handle OAuth callback from social media platforms."""
    if error:
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
    
    try:
        # Handle the OAuth callback
        connection_data = await oauth_service.handle_oauth_callback(platform, code, state)
        
        # Save the connection to database
        connection = oauth_service.save_connection(connection_data, db)
        
        # Return success response (in production, redirect to frontend)
        return {
            "success": True,
            "message": f"Successfully connected {platform}",
            "connection": connection.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to handle OAuth callback for {platform}: {e}")
        raise HTTPException(status_code=500, detail="Failed to complete authentication")

# Connection management endpoints
@router.get("/connections", response_model=List[ConnectionResponse])
async def get_user_connections(
    user_id: int = Query(default=1),  # In production, get from authenticated user
    platform: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all social media connections for a user."""
    try:
        query = db.query(SocialConnection).filter(SocialConnection.user_id == user_id)
        
        if platform:
            query = query.filter(SocialConnection.platform == platform)
        
        connections = query.all()
        
        return [
            ConnectionResponse(
                id=conn.id,
                platform=conn.platform,
                platform_username=conn.platform_username or "",
                connection_status=conn.connection_status,
                auto_post_enabled=conn.auto_post_enabled,
                analytics_enabled=conn.analytics_enabled,
                connected_at=conn.connected_at.isoformat() if conn.connected_at else "",
                expires_at=conn.expires_at.isoformat() if conn.expires_at else None,
                profile_data=conn.profile_data or {}
            )
            for conn in connections
        ]
    except Exception as e:
        logger.error(f"Failed to get user connections: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve connections")

@router.get("/connections/{connection_id}", response_model=ConnectionResponse)
async def get_connection(
    connection_id: int,
    user_id: int = Query(default=1),  # In production, get from authenticated user
    db: Session = Depends(get_db)
):
    """Get a specific social media connection."""
    try:
        connection = db.query(SocialConnection).filter(
            SocialConnection.id == connection_id,
            SocialConnection.user_id == user_id
        ).first()
        
        if not connection:
            raise HTTPException(status_code=404, detail="Connection not found")
        
        return ConnectionResponse(
            id=connection.id,
            platform=connection.platform,
            platform_username=connection.platform_username or "",
            connection_status=connection.connection_status,
            auto_post_enabled=connection.auto_post_enabled,
            analytics_enabled=connection.analytics_enabled,
            connected_at=connection.connected_at.isoformat() if connection.connected_at else "",
            expires_at=connection.expires_at.isoformat() if connection.expires_at else None,
            profile_data=connection.profile_data or {}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get connection {connection_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve connection")

@router.delete("/connections/{connection_id}")
async def delete_connection(
    connection_id: int,
    user_id: int = Query(default=1),  # In production, get from authenticated user
    db: Session = Depends(get_db)
):
    """Delete a social media connection."""
    try:
        connection = db.query(SocialConnection).filter(
            SocialConnection.id == connection_id,
            SocialConnection.user_id == user_id
        ).first()
        
        if not connection:
            raise HTTPException(status_code=404, detail="Connection not found")
        
        db.delete(connection)
        db.commit()
        
        return {"success": True, "message": "Connection deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete connection {connection_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete connection")

@router.patch("/connections/{connection_id}/settings")
async def update_connection_settings(
    connection_id: int,
    auto_post_enabled: Optional[bool] = None,
    analytics_enabled: Optional[bool] = None,
    user_id: int = Query(default=1),  # In production, get from authenticated user
    db: Session = Depends(get_db)
):
    """Update connection settings."""
    try:
        connection = db.query(SocialConnection).filter(
            SocialConnection.id == connection_id,
            SocialConnection.user_id == user_id
        ).first()
        
        if not connection:
            raise HTTPException(status_code=404, detail="Connection not found")
        
        if auto_post_enabled is not None:
            connection.auto_post_enabled = auto_post_enabled
        
        if analytics_enabled is not None:
            connection.analytics_enabled = analytics_enabled
        
        db.commit()
        db.refresh(connection)
        
        return {"success": True, "message": "Settings updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update connection settings {connection_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update settings")

# Google Search Console specific endpoints
@router.get("/gsc/{connection_id}/sites")
async def get_gsc_sites(
    connection_id: int,
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """Get list of verified sites from Google Search Console."""
    try:
        connection = db.query(SocialConnection).filter(
            SocialConnection.id == connection_id,
            SocialConnection.user_id == user_id,
            SocialConnection.platform == 'google_search_console'
        ).first()
        
        if not connection:
            raise HTTPException(status_code=404, detail="GSC connection not found")
        
        sites = await gsc_analytics_service.fetch_site_list(connection, db)
        return {"success": True, "sites": sites}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get GSC sites for connection {connection_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve GSC sites")

@router.get("/gsc/{connection_id}/analytics/performance")
async def get_gsc_performance(
    connection_id: int,
    site_url: str = Query(...),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """Get performance summary from Google Search Console."""
    try:
        connection = db.query(SocialConnection).filter(
            SocialConnection.id == connection_id,
            SocialConnection.user_id == user_id,
            SocialConnection.platform == 'google_search_console'
        ).first()
        
        if not connection:
            raise HTTPException(status_code=404, detail="GSC connection not found")
        
        # Check for cached data first
        cached_data = gsc_analytics_service.get_cached_analytics(
            connection_id, 'performance_summary', db
        )
        
        if cached_data:
            return {"success": True, "data": cached_data, "cached": True}
        
        # Fetch fresh data
        performance_data = await gsc_analytics_service.fetch_performance_summary(
            connection, db, site_url, start_date, end_date
        )
        
        return {"success": True, "data": performance_data, "cached": False}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get GSC performance for connection {connection_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve GSC performance data")

@router.get("/gsc/{connection_id}/analytics/queries")
async def get_gsc_top_queries(
    connection_id: int,
    site_url: str = Query(...),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    limit: int = Query(100),
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """Get top queries from Google Search Console."""
    try:
        connection = db.query(SocialConnection).filter(
            SocialConnection.id == connection_id,
            SocialConnection.user_id == user_id,
            SocialConnection.platform == 'google_search_console'
        ).first()
        
        if not connection:
            raise HTTPException(status_code=404, detail="GSC connection not found")
        
        # Check for cached data first
        cached_data = gsc_analytics_service.get_cached_analytics(
            connection_id, 'top_queries', db
        )
        
        if cached_data:
            return {"success": True, "data": cached_data, "cached": True}
        
        # Fetch fresh data
        queries_data = await gsc_analytics_service.fetch_top_queries(
            connection, db, site_url, start_date, end_date, limit
        )
        
        return {"success": True, "data": queries_data, "cached": False}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get GSC queries for connection {connection_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve GSC queries data")

@router.get("/gsc/{connection_id}/analytics/pages")
async def get_gsc_top_pages(
    connection_id: int,
    site_url: str = Query(...),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    limit: int = Query(100),
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """Get top pages from Google Search Console."""
    try:
        connection = db.query(SocialConnection).filter(
            SocialConnection.id == connection_id,
            SocialConnection.user_id == user_id,
            SocialConnection.platform == 'google_search_console'
        ).first()
        
        if not connection:
            raise HTTPException(status_code=404, detail="GSC connection not found")
        
        # Check for cached data first
        cached_data = gsc_analytics_service.get_cached_analytics(
            connection_id, 'top_pages', db
        )
        
        if cached_data:
            return {"success": True, "data": cached_data, "cached": True}
        
        # Fetch fresh data
        pages_data = await gsc_analytics_service.fetch_top_pages(
            connection, db, site_url, start_date, end_date, limit
        )
        
        return {"success": True, "data": pages_data, "cached": False}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get GSC pages for connection {connection_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve GSC pages data")

# Analytics endpoints
@router.get("/analytics/{connection_id}", response_model=List[AnalyticsResponse])
async def get_connection_analytics(
    connection_id: int,
    metric_name: Optional[str] = Query(None),
    limit: int = Query(10),
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """Get analytics data for a connection."""
    try:
        # Verify connection belongs to user
        connection = db.query(SocialConnection).filter(
            SocialConnection.id == connection_id,
            SocialConnection.user_id == user_id
        ).first()
        
        if not connection:
            raise HTTPException(status_code=404, detail="Connection not found")
        
        query = db.query(SocialAnalytics).filter(
            SocialAnalytics.connection_id == connection_id
        )
        
        if metric_name:
            query = query.filter(SocialAnalytics.metric_name == metric_name)
        
        analytics = query.order_by(SocialAnalytics.fetched_at.desc()).limit(limit).all()
        
        return [
            AnalyticsResponse(
                connection_id=item.connection_id,
                metric_name=item.metric_name,
                metric_value=item.metric_value,
                date_range_start=item.date_range_start.isoformat() if item.date_range_start else None,
                date_range_end=item.date_range_end.isoformat() if item.date_range_end else None,
                fetched_at=item.fetched_at.isoformat() if item.fetched_at else ""
            )
            for item in analytics
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get analytics for connection {connection_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics data")

# Posting endpoints
@router.post("/connections/{connection_id}/post", response_model=PostResponse)
async def post_content(
    connection_id: int,
    post_data: PostContentRequest,
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """Post content to a connected social media platform."""
    try:
        # Verify connection belongs to user
        connection = db.query(SocialConnection).filter(
            SocialConnection.id == connection_id,
            SocialConnection.user_id == user_id
        ).first()
        
        if not connection:
            raise HTTPException(status_code=404, detail="Connection not found")
        
        # Parse scheduled_at if provided
        scheduled_at = None
        if post_data.scheduled_at:
            try:
                from datetime import datetime
                scheduled_at = datetime.fromisoformat(post_data.scheduled_at)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid scheduled_at format")
        
        # Post content
        result = await social_posting_service.post_content(
            connection_id=connection_id,
            content=post_data.content,
            media_urls=post_data.media_urls,
            scheduled_at=scheduled_at,
            db=db
        )
        
        return PostResponse(
            success=result['success'],
            message=result['message'],
            post_id=result.get('post_id'),
            platform_post_id=result.get('platform_post_id'),
            platform_url=result.get('platform_url')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to post content: {e}")
        raise HTTPException(status_code=500, detail="Failed to post content")

@router.get("/posts")
async def get_user_posts(
    user_id: int = Query(default=1),
    platform: Optional[str] = Query(None),
    limit: int = Query(50),
    db: Session = Depends(get_db)
):
    """Get posts for a user across all connected platforms."""
    try:
        posts = social_posting_service.get_user_posts(
            user_id=user_id,
            platform=platform,
            limit=limit,
            db=db
        )
        
        return {"success": True, "posts": posts}
        
    except Exception as e:
        logger.error(f"Failed to get user posts: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve posts")

@router.get("/posts/{post_id}")
async def get_post_analytics(
    post_id: int,
    user_id: int = Query(default=1),
    db: Session = Depends(get_db)
):
    """Get analytics for a specific post."""
    try:
        # Verify post belongs to user
        post = db.query(SocialPost).join(SocialConnection).filter(
            SocialPost.id == post_id,
            SocialConnection.user_id == user_id
        ).first()
        
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        analytics = social_posting_service.get_post_analytics(post_id, db)
        
        if analytics:
            return {"success": True, "analytics": analytics}
        else:
            raise HTTPException(status_code=404, detail="Analytics not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get post analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics")

# Test endpoint for development
@router.get("/test/platforms")
async def test_supported_platforms():
    """Get list of supported social media platforms."""
    return {
        "supported_platforms": [
            {
                "id": "google_search_console",
                "name": "Google Search Console",
                "description": "Connect GSC to fetch website analytics and search performance data",
                "features": ["Analytics", "Search Performance", "Index Status"]
            },
            {
                "id": "youtube",
                "name": "YouTube",
                "description": "Connect YouTube for video analytics and content management",
                "features": ["Video Analytics", "Channel Management", "Content Upload"]
            },
            {
                "id": "facebook",
                "name": "Facebook",
                "description": "Connect Facebook for page management and content posting",
                "features": ["Page Management", "Content Posting", "Analytics"]
            },
            {
                "id": "twitter",
                "name": "Twitter/X",
                "description": "Connect Twitter for tweet management and analytics",
                "features": ["Tweet Posting", "Analytics", "Trend Analysis"]
            },
            {
                "id": "linkedin",
                "name": "LinkedIn",
                "description": "Connect LinkedIn for professional content and networking",
                "features": ["Content Posting", "Professional Analytics", "Network Insights"]
            }
        ]
    }