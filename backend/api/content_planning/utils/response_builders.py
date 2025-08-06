"""
Response Builders for Content Planning API
Standardized response formatting utilities extracted from the main content_planning.py file.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from fastapi import status
import json

class ResponseBuilder:
    """Standardized response building utilities."""
    
    @staticmethod
    def create_success_response(
        data: Any,
        message: str = "Operation completed successfully",
        status_code: int = 200
    ) -> Dict[str, Any]:
        """Create a standardized success response."""
        return {
            "status": "success",
            "message": message,
            "data": data,
            "status_code": status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def create_error_response(
        message: str,
        error_type: str = "general",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a standardized error response."""
        response = {
            "status": "error",
            "error_type": error_type,
            "message": message,
            "status_code": status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if details:
            response["details"] = details
            
        return response
    
    @staticmethod
    def create_paginated_response(
        data: List[Any],
        total_count: int,
        page: int = 1,
        page_size: int = 10,
        message: str = "Data retrieved successfully"
    ) -> Dict[str, Any]:
        """Create a standardized paginated response."""
        return {
            "status": "success",
            "message": message,
            "data": data,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "total_pages": (total_count + page_size - 1) // page_size
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def create_health_response(
        service_name: str,
        status: str,
        services: Dict[str, Any],
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Create a standardized health check response."""
        return {
            "service": service_name,
            "status": status,
            "timestamp": (timestamp or datetime.utcnow()).isoformat(),
            "services": services
        }
    
    @staticmethod
    def create_ai_analytics_response(
        insights: List[Dict[str, Any]],
        recommendations: List[Dict[str, Any]],
        total_insights: int,
        total_recommendations: int,
        generated_at: datetime,
        ai_service_status: str = "operational",
        processing_time: Optional[float] = None,
        personalized_data_used: bool = True,
        data_source: str = "ai_analysis"
    ) -> Dict[str, Any]:
        """Create a standardized AI analytics response."""
        response = {
            "insights": insights,
            "recommendations": recommendations,
            "total_insights": total_insights,
            "total_recommendations": total_recommendations,
            "generated_at": generated_at.isoformat(),
            "ai_service_status": ai_service_status,
            "personalized_data_used": personalized_data_used,
            "data_source": data_source
        }
        
        if processing_time is not None:
            response["processing_time"] = f"{processing_time:.2f}s"
            
        return response
    
    @staticmethod
    def create_gap_analysis_response(
        gap_analyses: List[Dict[str, Any]],
        total_gaps: int,
        generated_at: datetime,
        ai_service_status: str = "operational",
        personalized_data_used: bool = True,
        data_source: str = "ai_analysis"
    ) -> Dict[str, Any]:
        """Create a standardized gap analysis response."""
        return {
            "gap_analyses": gap_analyses,
            "total_gaps": total_gaps,
            "generated_at": generated_at.isoformat(),
            "ai_service_status": ai_service_status,
            "personalized_data_used": personalized_data_used,
            "data_source": data_source
        }
    
    @staticmethod
    def create_strategy_response(
        strategies: List[Dict[str, Any]],
        total_count: int,
        user_id: Optional[int] = None,
        analysis_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Create a standardized strategy response."""
        response = {
            "status": "success",
            "message": "Content strategy retrieved successfully",
            "data": {
                "strategies": strategies,
                "total_count": total_count
            }
        }
        
        if user_id is not None:
            response["data"]["user_id"] = user_id
            
        if analysis_date is not None:
            response["data"]["analysis_date"] = analysis_date.isoformat()
            
        return response

# Common response patterns
RESPONSE_PATTERNS = {
    "success": {
        "status": "success",
        "message": "Operation completed successfully"
    },
    "error": {
        "status": "error",
        "message": "Operation failed"
    },
    "not_found": {
        "status": "error",
        "message": "Resource not found"
    },
    "validation_error": {
        "status": "error",
        "message": "Validation failed"
    }
}

# Response status codes
RESPONSE_STATUS_CODES = {
    "success": 200,
    "created": 201,
    "no_content": 204,
    "bad_request": 400,
    "unauthorized": 401,
    "forbidden": 403,
    "not_found": 404,
    "conflict": 409,
    "unprocessable_entity": 422,
    "internal_error": 500,
    "service_unavailable": 503
} 