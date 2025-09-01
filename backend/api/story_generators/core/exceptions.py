"""
Custom exceptions for story generators.
"""

from typing import Optional, Dict, Any
from fastapi import HTTPException, status


class StoryGeneratorException(Exception):
    """Base exception for story generators."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class StoryGenerationError(StoryGeneratorException):
    """Exception raised when story generation fails."""
    pass


class IllustrationGenerationError(StoryGeneratorException):
    """Exception raised when illustration generation fails."""
    pass


class VideoGenerationError(StoryGeneratorException):
    """Exception raised when video generation fails."""
    pass


class InvalidInputError(StoryGeneratorException):
    """Exception raised for invalid input data."""
    pass


class ModelConnectionError(StoryGeneratorException):
    """Exception raised when AI model connection fails."""
    pass


class FileProcessingError(StoryGeneratorException):
    """Exception raised when file processing fails."""
    pass


class RateLimitError(StoryGeneratorException):
    """Exception raised when API rate limits are exceeded."""
    pass


# HTTP Exception mappers
def map_to_http_exception(error: StoryGeneratorException) -> HTTPException:
    """Map custom exceptions to HTTP exceptions."""
    
    error_mappings = {
        InvalidInputError: status.HTTP_400_BAD_REQUEST,
        FileProcessingError: status.HTTP_400_BAD_REQUEST,
        ModelConnectionError: status.HTTP_503_SERVICE_UNAVAILABLE,
        RateLimitError: status.HTTP_429_TOO_MANY_REQUESTS,
        StoryGenerationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        IllustrationGenerationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        VideoGenerationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }
    
    status_code = error_mappings.get(type(error), status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return HTTPException(
        status_code=status_code,
        detail={
            "error": error.__class__.__name__,
            "message": error.message,
            "details": error.details
        }
    )


# Exception handlers
async def story_generator_exception_handler(request, exc: StoryGeneratorException):
    """Handle story generator exceptions."""
    http_exc = map_to_http_exception(exc)
    return await http_exception_handler(request, http_exc)


async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions with logging."""
    from .logging import get_logger
    
    logger = get_logger(__name__)
    logger.warning(
        f"HTTP Exception: {exc.status_code} - {exc.detail}",
        extra={
            "status_code": exc.status_code,
            "detail": exc.detail,
            "url": str(request.url),
            "method": request.method
        }
    )
    
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


async def general_exception_handler(request, exc: Exception):
    """Handle general exceptions with logging."""
    from .logging import get_logger
    
    logger = get_logger(__name__)
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={
            "exception_type": exc.__class__.__name__,
            "url": str(request.url),
            "method": request.method
        },
        exc_info=True
    )
    
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Internal server error",
                "type": "InternalServerError"
            }
        }
    )