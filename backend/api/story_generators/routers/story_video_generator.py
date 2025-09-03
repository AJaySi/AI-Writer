"""
FastAPI router for AI Story Video Generator endpoints.
"""

import asyncio
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
import json
import uuid
from datetime import datetime

from ..schemas import (
    StoryVideoRequest,
    StoryVideoResponse,
    VideoGenerationProgress,
    VideoGenerationJob
)
from ..services.story_video_service import get_story_video_service
from ..core.logging import get_logger
from ..core.exceptions import (
    VideoGenerationError,
    InvalidInputError,
    map_to_http_exception
)

router = APIRouter(prefix="/story-video-generator", tags=["Story Video Generator"])
logger = get_logger(__name__)

# In-memory storage for video generation jobs
video_jobs: Dict[str, Dict[str, Any]] = {}


@router.post("/generate", response_model=StoryVideoResponse)
async def generate_story_video(
    request: StoryVideoRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate a story video using AI.
    
    This endpoint creates a video generation job and returns the job ID.
    Use the /status/{job_id} endpoint to check progress and get the final result.
    
    Note: This version generates video scenes and images. Full video compilation
    requires additional video processing libraries.
    """
    try:
        # Validate input
        if not request.story_text or len(request.story_text.strip()) < 50:
            raise InvalidInputError("Story text must be at least 50 characters long")
        
        # Create job ID
        job_id = str(uuid.uuid4())
        
        # Initialize job status
        video_jobs[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "progress": 0.0,
            "current_step": "Initializing...",
            "scenes_processed": 0,
            "total_scenes": 0,
            "current_scene_progress": 0.0,
            "current_operation": "Preparing",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "request_data": request.dict(),
            "result": None,
            "error": None
        }
        
        # Start background task for video generation
        background_tasks.add_task(
            _generate_video_background,
            job_id,
            request
        )
        
        logger.info(f"Video generation job created: {job_id}")
        
        return StoryVideoResponse(
            success=True,
            video_url=None,
            video_file_size=None,
            video_duration=None,
            scenes=[],
            total_scenes=0,
            processing_time=None,
            thumbnail_url=None,
            metadata={},
            error_message=None
        )
        
    except Exception as e:
        logger.error_with_context(e, {"request": request.dict()})
        raise map_to_http_exception(
            VideoGenerationError(f"Failed to start video generation: {str(e)}")
        )


@router.get("/generate-scenes-only")
async def generate_scenes_only(
    story_text: str,
    title: str = None,
    illustration_style: str = "digital art",
    max_scenes: int = 10,
    duration_per_scene: float = 5.0,
    quality: str = "high"
):
    """
    Generate only video scenes without full video compilation.
    
    This is useful for preview purposes or when you only need the scene data.
    """
    try:
        service = get_story_video_service()
        
        video_settings = {
            "duration_per_scene": duration_per_scene,
            "quality": quality,
            "max_scenes": max_scenes
        }
        
        audio_settings = {
            "include_narration": False,
            "background_music": False
        }
        
        result = await service.generate_video_scenes(
            story_text=story_text,
            title=title,
            video_settings=video_settings,
            audio_settings=audio_settings,
            illustration_style=illustration_style
        )
        
        return StoryVideoResponse(
            success=result["success"],
            video_url=result.get("video_url"),
            video_file_size=result.get("video_file_size"),
            video_duration=result.get("video_duration"),
            scenes=result.get("scenes", []),
            total_scenes=result.get("total_scenes", 0),
            processing_time=result.get("processing_time"),
            thumbnail_url=result.get("thumbnail_url"),
            metadata=result.get("metadata", {}),
            error_message=None
        )
        
    except Exception as e:
        logger.error_with_context(e, {"story_length": len(story_text)})
        
        if isinstance(e, (VideoGenerationError, InvalidInputError)):
            raise map_to_http_exception(e)
        else:
            raise map_to_http_exception(
                VideoGenerationError(f"Scene generation failed: {str(e)}")
            )


@router.get("/status/{job_id}")
async def get_video_status(job_id: str):
    """
    Get the status of a video generation job.
    
    Returns the current progress, status, and result (if completed).
    """
    try:
        if job_id not in video_jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job = video_jobs[job_id]
        
        return VideoGenerationJob(
            job_id=job_id,
            status=job["status"],
            created_at=job["created_at"],
            updated_at=job["updated_at"],
            progress=VideoGenerationProgress(
                status=job["status"],
                progress=job["progress"],
                current_step=job["current_step"],
                scenes_processed=job["scenes_processed"],
                total_scenes=job["total_scenes"],
                current_scene_progress=job["current_scene_progress"],
                current_operation=job["current_operation"]
            ),
            result=job.get("result")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get job status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get job status")


@router.get("/stream/{job_id}")
async def stream_video_progress(job_id: str):
    """
    Stream real-time progress updates for a video generation job.
    
    Returns a Server-Sent Events (SSE) stream with progress updates.
    """
    async def generate_progress_stream():
        """Generate progress updates as SSE stream."""
        try:
            while job_id in video_jobs:
                job = video_jobs[job_id]
                
                # Create progress object
                progress_data = {
                    "job_id": job_id,
                    "status": job["status"],
                    "progress": job["progress"],
                    "current_step": job["current_step"],
                    "scenes_processed": job["scenes_processed"],
                    "total_scenes": job["total_scenes"],
                    "current_scene_progress": job["current_scene_progress"],
                    "current_operation": job["current_operation"],
                    "updated_at": job["updated_at"]
                }
                
                # Send current status
                yield f"data: {json.dumps(progress_data)}\\n\\n"
                
                # If job is completed or failed, end stream
                if job["status"] in ["completed", "failed", "cancelled"]:
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


@router.get("/scene/{job_id}/{scene_index}")
async def get_video_scene(job_id: str, scene_index: int):
    """
    Get a specific scene from a completed video generation job.
    
    Returns the scene data including image and metadata.
    """
    try:
        if job_id not in video_jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job = video_jobs[job_id]
        
        if job["status"] != "completed":
            raise HTTPException(status_code=400, detail="Job not completed")
        
        result = job.get("result")
        if not result or not result.get("scenes"):
            raise HTTPException(status_code=404, detail="No scenes found")
        
        scenes = result["scenes"]
        
        if scene_index < 0 or scene_index >= len(scenes):
            raise HTTPException(status_code=404, detail="Scene not found")
        
        scene = scenes[scene_index]
        
        return {
            "scene": scene,
            "scene_index": scene_index,
            "total_scenes": len(scenes)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get scene: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get scene")


@router.delete("/jobs/{job_id}")
async def cancel_video_job(job_id: str):
    """
    Cancel a video generation job.
    
    This will stop the generation process and clean up resources.
    """
    try:
        if job_id not in video_jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job = video_jobs[job_id]
        
        if job["status"] in ["completed", "failed"]:
            raise HTTPException(status_code=400, detail="Job already completed")
        
        # Mark job as cancelled
        job["status"] = "cancelled"
        job["updated_at"] = datetime.utcnow().isoformat()
        
        logger.info(f"Video generation job cancelled: {job_id}")
        
        return {"message": "Job cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to cancel job: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cancel job")


@router.get("/jobs")
async def list_video_jobs():
    """
    List all video generation jobs.
    
    Returns a list of all jobs with their current status.
    """
    try:
        jobs = []
        for job_id, job_data in video_jobs.items():
            jobs.append({
                "job_id": job_id,
                "status": job_data["status"],
                "progress": job_data["progress"],
                "scenes_processed": job_data["scenes_processed"],
                "total_scenes": job_data["total_scenes"],
                "created_at": job_data["created_at"],
                "updated_at": job_data["updated_at"]
            })
        
        return {"jobs": jobs}
        
    except Exception as e:
        logger.error(f"Failed to list jobs: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list jobs")


async def _generate_video_background(job_id: str, request: StoryVideoRequest):
    """Background task for video generation."""
    try:
        # Update job status
        video_jobs[job_id]["status"] = "running"
        video_jobs[job_id]["current_step"] = "Starting video generation..."
        video_jobs[job_id]["current_operation"] = "Initializing"
        video_jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()
        
        # Progress callback
        async def progress_callback(step: str, progress: float):
            if job_id in video_jobs:
                video_jobs[job_id]["progress"] = progress
                video_jobs[job_id]["current_step"] = step
                video_jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()
        
        # Check if job was cancelled
        if video_jobs[job_id]["status"] == "cancelled":
            return
        
        # Generate video scenes
        service = get_story_video_service()
        result = await service.generate_video_scenes(
            story_text=request.story_text,
            title=request.title,
            video_settings=request.video_settings.dict(),
            audio_settings=request.audio_settings.dict(),
            illustration_style=request.illustration_style,
            progress_callback=progress_callback
        )
        
        # Update job with result
        if job_id in video_jobs:
            video_jobs[job_id]["status"] = "completed"
            video_jobs[job_id]["progress"] = 100.0
            video_jobs[job_id]["current_step"] = "Video generation completed!"
            video_jobs[job_id]["current_operation"] = "Finished"
            video_jobs[job_id]["total_scenes"] = result.get("total_scenes", 0)
            video_jobs[job_id]["scenes_processed"] = result.get("total_scenes", 0)
            video_jobs[job_id]["result"] = StoryVideoResponse(
                success=result["success"],
                video_url=result.get("video_url"),
                video_file_size=result.get("video_file_size"),
                video_duration=result.get("video_duration"),
                scenes=result.get("scenes", []),
                total_scenes=result.get("total_scenes", 0),
                processing_time=result.get("processing_time"),
                thumbnail_url=result.get("thumbnail_url"),
                metadata=result.get("metadata", {}),
                error_message=None
            ).dict()
            video_jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()
        
        logger.info(f"Video generation job completed: {job_id}")
        
    except Exception as e:
        logger.error_with_context(e, {"job_id": job_id})
        
        # Update job with error
        if job_id in video_jobs:
            video_jobs[job_id]["status"] = "failed"
            video_jobs[job_id]["error"] = str(e)
            video_jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()


@router.get("/health")
async def health_check():
    """Health check endpoint for the story video generator service."""
    try:
        service = get_story_video_service()
        return {
            "status": "healthy",
            "service": "story_video_generator",
            "timestamp": datetime.utcnow().isoformat(),
            "note": "Video compilation requires additional libraries"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")