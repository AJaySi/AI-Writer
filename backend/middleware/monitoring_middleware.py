"""
Enhanced FastAPI Monitoring Middleware
Database-backed monitoring for API calls, errors, and performance metrics.
"""

from fastapi import Request, Response
from fastapi.responses import JSONResponse
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, deque
import asyncio
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from models.api_monitoring import APIRequest, APIEndpointStats, SystemHealth, CachePerformance
from services.database import get_db

class DatabaseAPIMonitor:
    """Database-backed API monitoring."""
    
    def __init__(self):
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'hit_rate': 0.0
        }
    
    async def add_request(self, db: Session, path: str, method: str, status_code: int, 
                         duration: float, user_id: str = None, cache_hit: bool = None,
                         request_size: int = None, response_size: int = None,
                         user_agent: str = None, ip_address: str = None):
        """Add a request to database monitoring."""
        try:
            # Store individual request
            api_request = APIRequest(
                path=path,
                method=method,
                status_code=status_code,
                duration=duration,
                user_id=user_id,
                cache_hit=cache_hit,
                request_size=request_size,
                response_size=response_size,
                user_agent=user_agent,
                ip_address=ip_address
            )
            db.add(api_request)
            
            # Update endpoint stats
            endpoint_key = f"{method} {path}"
            endpoint_stats = db.query(APIEndpointStats).filter(
                APIEndpointStats.endpoint == endpoint_key
            ).first()
            
            if not endpoint_stats:
                endpoint_stats = APIEndpointStats(endpoint=endpoint_key)
                db.add(endpoint_stats)
            
            # Update statistics - handle None values
            endpoint_stats.total_requests = (endpoint_stats.total_requests or 0) + 1
            endpoint_stats.total_duration = (endpoint_stats.total_duration or 0.0) + duration
            endpoint_stats.avg_duration = endpoint_stats.total_duration / endpoint_stats.total_requests
            endpoint_stats.last_called = datetime.utcnow()
            
            if status_code >= 400:
                endpoint_stats.total_errors = (endpoint_stats.total_errors or 0) + 1
            
            if cache_hit is not None:
                if cache_hit:
                    endpoint_stats.cache_hits = (endpoint_stats.cache_hits or 0) + 1
                else:
                    endpoint_stats.cache_misses = (endpoint_stats.cache_misses or 0) + 1
                
                total_cache_requests = endpoint_stats.cache_hits + endpoint_stats.cache_misses
                if total_cache_requests > 0:
                    endpoint_stats.cache_hit_rate = (endpoint_stats.cache_hits / total_cache_requests) * 100
            
            # Update min/max duration
            if endpoint_stats.min_duration is None or duration < endpoint_stats.min_duration:
                endpoint_stats.min_duration = duration
            if endpoint_stats.max_duration is None or duration > endpoint_stats.max_duration:
                endpoint_stats.max_duration = duration
            
            db.commit()
            
            # Update cache stats
            if cache_hit is not None:
                if cache_hit:
                    self.cache_stats['hits'] += 1
                else:
                    self.cache_stats['misses'] += 1
                
                total_cache_requests = self.cache_stats['hits'] + self.cache_stats['misses']
                if total_cache_requests > 0:
                    self.cache_stats['hit_rate'] = (self.cache_stats['hits'] / total_cache_requests) * 100
            
        except Exception as e:
            logger.error(f"❌ Error storing API request: {str(e)}")
            db.rollback()
    
    async def get_stats(self, db: Session, minutes: int = 5) -> Dict[str, Any]:
        """Get current monitoring statistics from database."""
        try:
            now = datetime.utcnow()
            since = now - timedelta(minutes=minutes)
            
            # Recent requests
            recent_requests = db.query(APIRequest).filter(
                APIRequest.timestamp >= since
            ).count()
            
            # Recent errors
            recent_errors = db.query(APIRequest).filter(
                and_(
                    APIRequest.timestamp >= since,
                    APIRequest.status_code >= 400
                )
            ).count()
            
            # Top endpoints
            top_endpoints = db.query(APIEndpointStats).order_by(
                APIEndpointStats.total_requests.desc()
            ).limit(10).all()
            
            # Recent errors details
            recent_error_details = db.query(APIRequest).filter(
                and_(
                    APIRequest.timestamp >= since,
                    APIRequest.status_code >= 400
                )
            ).order_by(APIRequest.timestamp.desc()).limit(10).all()
            
            # Overall stats
            total_requests = db.query(APIRequest).count()
            total_errors = db.query(APIRequest).filter(APIRequest.status_code >= 400).count()
            
            # Calculate error rate
            error_rate = (recent_errors / max(recent_requests, 1)) * 100
            
            return {
                'timestamp': now.isoformat(),
                'overview': {
                    'total_requests': total_requests,
                    'total_errors': total_errors,
                    'recent_requests': recent_requests,
                    'recent_errors': recent_errors
                },
                'cache_performance': self.cache_stats,
                'top_endpoints': [
                    {
                        'endpoint': endpoint.endpoint,
                        'count': endpoint.total_requests or 0,
                        'avg_time': round(endpoint.avg_duration or 0.0, 3),
                        'errors': endpoint.total_errors or 0,
                        'last_called': endpoint.last_called.isoformat() if endpoint.last_called else None,
                        'cache_hit_rate': round(endpoint.cache_hit_rate or 0.0, 2)
                    }
                    for endpoint in top_endpoints
                ],
                'recent_errors': [
                    {
                        'timestamp': error.timestamp.isoformat(),
                        'path': error.path,
                        'method': error.method,
                        'status_code': error.status_code,
                        'duration': error.duration
                    }
                    for error in recent_error_details
                ],
                'system_health': {
                    'status': 'healthy' if recent_errors < 5 else 'warning',
                    'error_rate': round(error_rate, 2)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting monitoring stats: {str(e)}")
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'error': str(e),
                'overview': {'total_requests': 0, 'total_errors': 0, 'recent_requests': 0, 'recent_errors': 0},
                'system_health': {'status': 'unknown', 'error_rate': 0.0}
            }
    
    async def get_lightweight_stats(self, db: Session) -> Dict[str, Any]:
        """Get lightweight stats for dashboard header."""
        try:
            now = datetime.utcnow()
            since = now - timedelta(minutes=5)
            
            # Quick stats for dashboard
            recent_requests = db.query(APIRequest).filter(
                APIRequest.timestamp >= since
            ).count()
            
            recent_errors = db.query(APIRequest).filter(
                and_(
                    APIRequest.timestamp >= since,
                    APIRequest.status_code >= 400
                )
            ).count()
            
            # Determine status
            if recent_errors == 0:
                status = "healthy"
                icon = "🟢"
            elif recent_errors < 3:
                status = "warning"
                icon = "🟡"
            else:
                status = "critical"
                icon = "🔴"
            
            return {
                'status': status,
                'icon': icon,
                'recent_requests': recent_requests,
                'recent_errors': recent_errors,
                'error_rate': round((recent_errors / max(recent_requests, 1)) * 100, 1),
                'timestamp': now.isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting lightweight stats: {str(e)}")
            return {
                'status': 'unknown',
                'icon': '⚪',
                'recent_requests': 0,
                'recent_errors': 0,
                'error_rate': 0.0,
                'timestamp': datetime.utcnow().isoformat()
            }

# Global monitor instance
api_monitor = DatabaseAPIMonitor()

# List of endpoints to exclude from monitoring
EXCLUDED_ENDPOINTS = [
    "/api/content-planning/monitoring/lightweight-stats",
    "/api/content-planning/monitoring/api-stats",
    "/api/content-planning/monitoring/cache-stats",
    "/api/content-planning/monitoring/health"
]

def should_monitor_endpoint(path: str) -> bool:
    """Check if an endpoint should be monitored."""
    return not any(path.endswith(excluded) for excluded in EXCLUDED_ENDPOINTS)

async def monitoring_middleware(request: Request, call_next):
    """Enhanced FastAPI middleware for monitoring API calls."""
    start_time = time.time()
    
    # Skip monitoring for excluded endpoints
    if not should_monitor_endpoint(request.url.path):
        response = await call_next(request)
        return response
    
    # Extract request details
    user_id = None
    try:
        if hasattr(request, 'query_params') and 'user_id' in request.query_params:
            user_id = request.query_params['user_id']
        elif hasattr(request, 'path_params') and 'user_id' in request.path_params:
            user_id = request.path_params['user_id']
    except:
        pass
    
    # Get database session
    db = next(get_db())
    
    try:
        response = await call_next(request)
        status_code = response.status_code
        duration = time.time() - start_time
        
        # Check for cache-related headers
        cache_hit = None
        if hasattr(response, 'headers'):
            cache_header = response.headers.get('x-cache-status')
            if cache_header:
                cache_hit = cache_header.lower() == 'hit'
        
        # Store in database
        await api_monitor.add_request(
            db=db,
            path=request.url.path,
            method=request.method,
            status_code=status_code,
            duration=duration,
            user_id=user_id,
            cache_hit=cache_hit,
            user_agent=request.headers.get('user-agent'),
            ip_address=request.client.host if request.client else None
        )
        
        # Add monitoring headers
        response.headers['x-response-time'] = f"{duration:.3f}s"
        response.headers['x-monitor-id'] = f"{int(time.time())}"
        
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        status_code = 500
        
        # Store error in database
        await api_monitor.add_request(
            db=db,
            path=request.url.path,
            method=request.method,
            status_code=status_code,
            duration=duration,
            user_id=user_id,
            cache_hit=False,
            user_agent=request.headers.get('user-agent'),
            ip_address=request.client.host if request.client else None
        )
        
        logger.error(f"❌ API Error: {request.method} {request.url.path} - {str(e)}")
        
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "monitor_id": int(time.time())}
        )
    finally:
        db.close()

async def get_monitoring_stats(minutes: int = 5) -> Dict[str, Any]:
    """Get current monitoring statistics."""
    db = next(get_db())
    try:
        return await api_monitor.get_stats(db, minutes)
    finally:
        db.close()

async def get_lightweight_stats() -> Dict[str, Any]:
    """Get lightweight stats for dashboard header."""
    db = next(get_db())
    try:
        return await api_monitor.get_lightweight_stats(db)
    finally:
        db.close()
