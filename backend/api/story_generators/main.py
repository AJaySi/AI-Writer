"""
Main integration module for Story Generators API.

This module provides the main FastAPI application integration for all story generators.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .routers import (
    story_writer,
    story_illustrator,
    story_video_generator
)
from .core.exceptions import (
    story_generator_exception_handler,
    http_exception_handler,
    general_exception_handler,
    StoryGeneratorException
)
from .core.logging import setup_logging, get_logger

logger = get_logger(__name__)


def create_story_generators_app() -> FastAPI:
    """
    Create and configure the Story Generators FastAPI application.
    
    Returns:
        Configured FastAPI application
    """
    # Setup logging
    setup_logging()
    
    # Create FastAPI app
    app = FastAPI(
        title="ALwrity Story Generators API",
        description="AI-powered story generation, illustration, and video creation",
        version="1.0.0",
        docs_url="/story-generators/docs",
        redoc_url="/story-generators/redoc",
        openapi_url="/story-generators/openapi.json"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add exception handlers
    app.add_exception_handler(StoryGeneratorException, story_generator_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    # Include routers
    app.include_router(story_writer.router)
    app.include_router(story_illustrator.router)
    app.include_router(story_video_generator.router)
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint for Story Generators API."""
        return {
            "message": "ALwrity Story Generators API",
            "version": "1.0.0",
            "services": [
                "Story Writer",
                "Story Illustrator", 
                "Story Video Generator"
            ],
            "endpoints": {
                "story_writer": "/story-writer",
                "story_illustrator": "/story-illustrator",
                "story_video_generator": "/story-video-generator"
            }
        }
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check for all story generator services."""
        try:
            from .services import (
                get_story_writer_service,
                get_story_illustrator_service,
                get_story_video_service,
                get_gemini_image_service
            )
            
            # Test all services
            services_status = {}
            
            try:
                get_story_writer_service()
                services_status["story_writer"] = "healthy"
            except Exception as e:
                services_status["story_writer"] = f"unhealthy: {str(e)}"
            
            try:
                get_story_illustrator_service()
                services_status["story_illustrator"] = "healthy"
            except Exception as e:
                services_status["story_illustrator"] = f"unhealthy: {str(e)}"
            
            try:
                get_story_video_service()
                services_status["story_video_generator"] = "healthy"
            except Exception as e:
                services_status["story_video_generator"] = f"unhealthy: {str(e)}"
            
            try:
                get_gemini_image_service()
                services_status["gemini_image_service"] = "healthy"
            except Exception as e:
                services_status["gemini_image_service"] = f"unhealthy: {str(e)}"
            
            overall_healthy = all("healthy" in status for status in services_status.values())
            
            return {
                "status": "healthy" if overall_healthy else "degraded",
                "services": services_status
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            raise HTTPException(status_code=503, detail="Health check failed")
    
    logger.info("Story Generators API application created successfully")
    return app


# Create the app instance
story_generators_app = create_story_generators_app()