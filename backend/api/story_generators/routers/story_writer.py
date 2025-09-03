"""
FastAPI router for AI Story Writer endpoints.
"""

import asyncio
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.responses import StreamingResponse
import json
import uuid
from datetime import datetime

from ..schemas import (
    StoryWriterRequest,
    StoryWriterResponse,
    StoryGenerationStatus
)
from ..services.story_writer_service import get_story_writer_service
from ..core.logging import get_logger
from ..core.exceptions import (
    StoryGenerationError,
    ModelConnectionError,
    InvalidInputError,
    map_to_http_exception
)

router = APIRouter(prefix="/story-writer", tags=["Story Writer"])
logger = get_logger(__name__)

# In-memory storage for generation jobs (in production, use Redis or database)
generation_jobs: Dict[str, Dict[str, Any]] = {}


@router.post("/generate", response_model=StoryWriterResponse)
async def generate_story(
    request: StoryWriterRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate a complete story using AI with prompt chaining.
    
    This endpoint creates a story generation job and returns the job ID.
    Use the /status/{job_id} endpoint to check progress and get the final result.
    """
    try:
        # Create job ID
        job_id = str(uuid.uuid4())
        
        # Initialize job status
        generation_jobs[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "progress": 0.0,
            "current_step": "Initializing...",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "request_data": request.dict(),
            "result": None,
            "error": None
        }
        
        # Start background task for story generation
        background_tasks.add_task(
            _generate_story_background,
            job_id,
            request
        )
        
        logger.info(f"Story generation job created: {job_id}")
        
        return StoryWriterResponse(
            success=True,
            story=None,
            premise=None,
            outline=None,
            word_count=None,
            character_count=None,
            error_message=None
        )
        
    except Exception as e:
        logger.error_with_context(e, {"request": request.dict()})
        raise map_to_http_exception(
            StoryGenerationError(f"Failed to start story generation: {str(e)}")
        )


@router.get("/generate-sync", response_model=StoryWriterResponse)
async def generate_story_sync(
    persona: str,
    story_setting: str,
    character_input: str,
    plot_elements: str,
    writing_style: str,
    story_tone: str,
    narrative_pov: str,
    audience_age_group: str,
    content_rating: str,
    ending_preference: str
):
    """
    Generate a story synchronously (for smaller stories or testing).
    
    This endpoint will block until the story is generated and return the complete result.
    Use this for testing or when you need immediate results.
    """
    try:
        request = StoryWriterRequest(
            persona=persona,
            story_setting=story_setting,
            character_input=character_input,
            plot_elements=plot_elements,
            writing_style=writing_style,
            story_tone=story_tone,
            narrative_pov=narrative_pov,
            audience_age_group=audience_age_group,
            content_rating=content_rating,
            ending_preference=ending_preference
        )
        
        service = get_story_writer_service()
        
        result = await service.generate_story(
            persona=request.persona,
            story_setting=request.story_setting,
            character_input=request.character_input,
            plot_elements=request.plot_elements,
            writing_style=request.writing_style,
            story_tone=request.story_tone,
            narrative_pov=request.narrative_pov,
            audience_age_group=request.audience_age_group,
            content_rating=request.content_rating,
            ending_preference=request.ending_preference
        )
        
        return StoryWriterResponse(
            success=result["success"],
            story=result.get("story"),
            premise=result.get("premise"),
            outline=result.get("outline"),
            word_count=result.get("word_count"),
            character_count=result.get("character_count"),
            error_message=None
        )
        
    except Exception as e:
        logger.error_with_context(e, {"request_params": locals()})
        
        if isinstance(e, (StoryGenerationError, ModelConnectionError, InvalidInputError)):
            raise map_to_http_exception(e)
        else:
            raise map_to_http_exception(
                StoryGenerationError(f"Story generation failed: {str(e)}")
            )


@router.get("/status/{job_id}")
async def get_generation_status(job_id: str):
    """
    Get the status of a story generation job.
    
    Returns the current progress, status, and result (if completed).
    """
    try:
        if job_id not in generation_jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job = generation_jobs[job_id]
        
        return {
            "job_id": job_id,
            "status": job["status"],
            "progress": job["progress"],
            "current_step": job["current_step"],
            "created_at": job["created_at"],
            "updated_at": job["updated_at"],
            "result": job.get("result"),
            "error": job.get("error")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get job status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get job status")


@router.get("/stream/{job_id}")
async def stream_generation_progress(job_id: str):
    """
    Stream real-time progress updates for a story generation job.
    
    Returns a Server-Sent Events (SSE) stream with progress updates.
    """
    async def generate_progress_stream():
        """Generate progress updates as SSE stream."""
        try:
            while job_id in generation_jobs:
                job = generation_jobs[job_id]
                
                # Send current status
                yield f"data: {json.dumps(job)}\\n\\n"
                
                # If job is completed or failed, end stream
                if job["status"] in ["completed", "failed"]:
                    break
                
                # Wait before next update
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Stream generation failed: {str(e)}")
            yield f"data: {json.dumps({'error': str(e)})}\\n\\n"
    
    return StreamingResponse(
        generate_progress_stream(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache"}
    )


@router.delete("/jobs/{job_id}")
async def cancel_generation_job(job_id: str):
    """
    Cancel a story generation job.
    
    This will stop the generation process and clean up resources.
    """
    try:
        if job_id not in generation_jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job = generation_jobs[job_id]
        
        if job["status"] in ["completed", "failed"]:
            raise HTTPException(status_code=400, detail="Job already completed")
        
        # Mark job as cancelled
        job["status"] = "cancelled"
        job["updated_at"] = datetime.utcnow().isoformat()
        
        logger.info(f"Story generation job cancelled: {job_id}")
        
        return {"message": "Job cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to cancel job: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cancel job")


@router.get("/jobs")
async def list_generation_jobs():
    """
    List all story generation jobs.
    
    Returns a list of all jobs with their current status.
    """
    try:
        jobs = []
        for job_id, job_data in generation_jobs.items():
            jobs.append({
                "job_id": job_id,
                "status": job_data["status"],
                "progress": job_data["progress"],
                "created_at": job_data["created_at"],
                "updated_at": job_data["updated_at"]
            })
        
        return {"jobs": jobs}
        
    except Exception as e:
        logger.error(f"Failed to list jobs: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list jobs")


async def _generate_story_background(job_id: str, request: StoryWriterRequest):
    """Background task for story generation."""
    try:
        # Update job status
        generation_jobs[job_id]["status"] = "running"
        generation_jobs[job_id]["current_step"] = "Starting story generation..."
        generation_jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()
        
        # Progress callback
        async def progress_callback(step: str, progress: float):
            if job_id in generation_jobs:
                generation_jobs[job_id]["progress"] = progress
                generation_jobs[job_id]["current_step"] = step
                generation_jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()
        
        # Check if job was cancelled
        if generation_jobs[job_id]["status"] == "cancelled":
            return
        
        # Generate story
        service = get_story_writer_service()
        result = await service.generate_story(
            persona=request.persona,
            story_setting=request.story_setting,
            character_input=request.character_input,
            plot_elements=request.plot_elements,
            writing_style=request.writing_style,
            story_tone=request.story_tone,
            narrative_pov=request.narrative_pov,
            audience_age_group=request.audience_age_group,
            content_rating=request.content_rating,
            ending_preference=request.ending_preference,
            progress_callback=progress_callback
        )
        
        # Update job with result
        if job_id in generation_jobs:
            generation_jobs[job_id]["status"] = "completed"
            generation_jobs[job_id]["progress"] = 100.0
            generation_jobs[job_id]["current_step"] = "Story generation completed!"
            generation_jobs[job_id]["result"] = StoryWriterResponse(
                success=result["success"],
                story=result.get("story"),
                premise=result.get("premise"),
                outline=result.get("outline"),
                word_count=result.get("word_count"),
                character_count=result.get("character_count"),
                error_message=None
            ).dict()
            generation_jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()
        
        logger.info(f"Story generation job completed: {job_id}")
        
    except Exception as e:
        logger.error_with_context(e, {"job_id": job_id})
        
        # Update job with error
        if job_id in generation_jobs:
            generation_jobs[job_id]["status"] = "failed"
            generation_jobs[job_id]["error"] = str(e)
            generation_jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()


@router.get("/health")
async def health_check():
    """Health check endpoint for the story writer service."""
    try:
        service = get_story_writer_service()
        return {
            "status": "healthy",
            "service": "story_writer",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")