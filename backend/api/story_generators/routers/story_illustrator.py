"""
FastAPI router for AI Story Illustrator endpoints.
"""

import asyncio
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, BackgroundTasks, File, UploadFile, Form
from fastapi.responses import StreamingResponse, FileResponse
import json
import uuid
import base64
from datetime import datetime
from pathlib import Path

from ..schemas import (
    StoryIllustratorRequest,
    StoryIllustratorResponse,
    IllustrationProgress,
    StoryInput,
    IllustrationSettings
)
from ..services.story_illustrator_service import get_story_illustrator_service
from ..core.logging import get_logger
from ..core.exceptions import (
    IllustrationGenerationError,
    FileProcessingError,
    InvalidInputError,
    map_to_http_exception
)

router = APIRouter(prefix="/story-illustrator", tags=["Story Illustrator"])
logger = get_logger(__name__)

# In-memory storage for illustration jobs
illustration_jobs: Dict[str, Dict[str, Any]] = {}


@router.post("/generate", response_model=StoryIllustratorResponse)
async def generate_illustrations(
    request: StoryIllustratorRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate illustrations for a story using AI.
    
    This endpoint creates an illustration generation job and returns the job ID.
    Use the /status/{job_id} endpoint to check progress and get the final result.
    """
    try:
        # Validate input
        if not any([
            request.story_input.text,
            request.story_input.url,
            request.story_input.file_content
        ]):
            raise InvalidInputError("No story input provided")
        
        # Create job ID
        job_id = str(uuid.uuid4())
        
        # Initialize job status
        illustration_jobs[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "progress": 0.0,
            "current_step": "Initializing...",
            "segments_processed": 0,
            "total_segments": 0,
            "illustrations_generated": 0,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "request_data": request.dict(),
            "result": None,
            "error": None
        }
        
        # Start background task for illustration generation
        background_tasks.add_task(
            _generate_illustrations_background,
            job_id,
            request
        )
        
        logger.info(f"Illustration generation job created: {job_id}")
        
        return StoryIllustratorResponse(
            success=True,
            story_title=None,
            story_segments=[],
            illustrations=[],
            total_illustrations=0,
            processing_time=None,
            download_url=None,
            error_message=None
        )
        
    except Exception as e:
        logger.error_with_context(e, {"request": request.dict()})
        raise map_to_http_exception(
            IllustrationGenerationError(f"Failed to start illustration generation: {str(e)}")
        )


@router.post("/upload-file")
async def upload_story_file(
    file: UploadFile = File(...),
    style: str = Form("digital art"),
    aspect_ratio: str = Form("16:9"),
    quality: str = Form("high"),
    max_illustrations: int = Form(10),
    min_segment_length: int = Form(100)
):
    """
    Upload a story file and generate illustrations.
    
    Supports text files (.txt, .md) and will support PDF and Word documents in the future.
    """
    try:
        # Read file content
        file_content = await file.read()
        file_base64 = base64.b64encode(file_content).decode('utf-8')
        
        # Create request
        request = StoryIllustratorRequest(
            story_input=StoryInput(
                file_content=file_base64,
                file_name=file.filename
            ),
            settings=IllustrationSettings(
                style=style,
                aspect_ratio=aspect_ratio,
                quality=quality,
                max_illustrations=max_illustrations,
                min_segment_length=min_segment_length
            )
        )
        
        # Create job ID
        job_id = str(uuid.uuid4())
        
        # Initialize job status
        illustration_jobs[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "progress": 0.0,
            "current_step": "Processing uploaded file...",
            "segments_processed": 0,
            "total_segments": 0,
            "illustrations_generated": 0,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "request_data": request.dict(),
            "result": None,
            "error": None
        }
        
        # Start background task
        asyncio.create_task(
            _generate_illustrations_background(job_id, request)
        )
        
        return {"job_id": job_id, "message": "File uploaded and processing started"}
        
    except Exception as e:
        logger.error_with_context(e, {"filename": file.filename})
        raise map_to_http_exception(
            FileProcessingError(f"File upload failed: {str(e)}")
        )


@router.get("/generate-from-url")
async def generate_from_url(
    url: str,
    style: str = "digital art",
    aspect_ratio: str = "16:9",
    quality: str = "high",
    max_illustrations: int = 10,
    min_segment_length: int = 100,
    background_tasks: BackgroundTasks = None
):
    """
    Generate illustrations from a story URL.
    
    Extracts text content from the provided URL and generates illustrations.
    """
    try:
        # Create request
        request = StoryIllustratorRequest(
            story_input=StoryInput(url=url),
            settings=IllustrationSettings(
                style=style,
                aspect_ratio=aspect_ratio,
                quality=quality,
                max_illustrations=max_illustrations,
                min_segment_length=min_segment_length
            )
        )
        
        # Create job ID
        job_id = str(uuid.uuid4())
        
        # Initialize job status
        illustration_jobs[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "progress": 0.0,
            "current_step": "Extracting text from URL...",
            "segments_processed": 0,
            "total_segments": 0,
            "illustrations_generated": 0,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "request_data": request.dict(),
            "result": None,
            "error": None
        }
        
        # Start background task
        background_tasks.add_task(
            _generate_illustrations_background,
            job_id,
            request
        )
        
        return {"job_id": job_id, "message": "URL processing started"}
        
    except Exception as e:
        logger.error_with_context(e, {"url": url})
        raise map_to_http_exception(
            FileProcessingError(f"URL processing failed: {str(e)}")
        )


@router.get("/status/{job_id}")
async def get_illustration_status(job_id: str):
    """
    Get the status of an illustration generation job.
    
    Returns the current progress, status, and result (if completed).
    """
    try:
        if job_id not in illustration_jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job = illustration_jobs[job_id]
        
        return {
            "job_id": job_id,
            "status": job["status"],
            "progress": job["progress"],
            "current_step": job["current_step"],
            "segments_processed": job["segments_processed"],
            "total_segments": job["total_segments"],
            "illustrations_generated": job["illustrations_generated"],
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
async def stream_illustration_progress(job_id: str):
    """
    Stream real-time progress updates for an illustration generation job.
    
    Returns a Server-Sent Events (SSE) stream with progress updates.
    """
    async def generate_progress_stream():
        """Generate progress updates as SSE stream."""
        try:
            while job_id in illustration_jobs:
                job = illustration_jobs[job_id]
                
                # Send current status
                yield f"data: {json.dumps(job)}\\n\\n"
                
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


@router.get("/download/{job_id}")
async def download_illustrations(job_id: str):
    """
    Download all illustrations for a completed job as a ZIP file.
    
    Returns the ZIP file containing all generated illustrations and metadata.
    """
    try:
        if job_id not in illustration_jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job = illustration_jobs[job_id]
        
        if job["status"] != "completed":
            raise HTTPException(status_code=400, detail="Job not completed")
        
        result = job.get("result")
        if not result or not result.get("download_url"):
            raise HTTPException(status_code=404, detail="Download file not found")
        
        download_path = result["download_url"]
        
        if not Path(download_path).exists():
            raise HTTPException(status_code=404, detail="Download file not found")
        
        return FileResponse(
            path=download_path,
            filename=f"story_illustrations_{job_id}.zip",
            media_type="application/zip"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Download failed")


@router.get("/illustration/{job_id}/{index}")
async def get_single_illustration(job_id: str, index: int):
    """
    Get a single illustration from a completed job.
    
    Returns the illustration image and metadata.
    """
    try:
        if job_id not in illustration_jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job = illustration_jobs[job_id]
        
        if job["status"] != "completed":
            raise HTTPException(status_code=400, detail="Job not completed")
        
        result = job.get("result")
        if not result or not result.get("illustrations"):
            raise HTTPException(status_code=404, detail="No illustrations found")
        
        illustrations = result["illustrations"]
        
        if index < 0 or index >= len(illustrations):
            raise HTTPException(status_code=404, detail="Illustration not found")
        
        illustration = illustrations[index]
        
        return {
            "illustration": illustration,
            "index": index,
            "total": len(illustrations)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get illustration: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get illustration")


@router.delete("/jobs/{job_id}")
async def cancel_illustration_job(job_id: str):
    """
    Cancel an illustration generation job.
    
    This will stop the generation process and clean up resources.
    """
    try:
        if job_id not in illustration_jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job = illustration_jobs[job_id]
        
        if job["status"] in ["completed", "failed"]:
            raise HTTPException(status_code=400, detail="Job already completed")
        
        # Mark job as cancelled
        job["status"] = "cancelled"
        job["updated_at"] = datetime.utcnow().isoformat()
        
        logger.info(f"Illustration generation job cancelled: {job_id}")
        
        return {"message": "Job cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to cancel job: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cancel job")


@router.get("/jobs")
async def list_illustration_jobs():
    """
    List all illustration generation jobs.
    
    Returns a list of all jobs with their current status.
    """
    try:
        jobs = []
        for job_id, job_data in illustration_jobs.items():
            jobs.append({
                "job_id": job_id,
                "status": job_data["status"],
                "progress": job_data["progress"],
                "illustrations_generated": job_data["illustrations_generated"],
                "created_at": job_data["created_at"],
                "updated_at": job_data["updated_at"]
            })
        
        return {"jobs": jobs}
        
    except Exception as e:
        logger.error(f"Failed to list jobs: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list jobs")


async def _generate_illustrations_background(job_id: str, request: StoryIllustratorRequest):
    """Background task for illustration generation."""
    try:
        # Update job status
        illustration_jobs[job_id]["status"] = "running"
        illustration_jobs[job_id]["current_step"] = "Starting illustration generation..."
        illustration_jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()
        
        # Progress callback
        async def progress_callback(step: str, progress: float):
            if job_id in illustration_jobs:
                illustration_jobs[job_id]["progress"] = progress
                illustration_jobs[job_id]["current_step"] = step
                illustration_jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()
        
        # Check if job was cancelled
        if illustration_jobs[job_id]["status"] == "cancelled":
            return
        
        # Generate illustrations
        service = get_story_illustrator_service()
        result = await service.generate_illustrations(
            story_input=request.story_input.dict(),
            settings=request.settings.dict(),
            progress_callback=progress_callback
        )
        
        # Update job with result
        if job_id in illustration_jobs:
            illustration_jobs[job_id]["status"] = "completed"
            illustration_jobs[job_id]["progress"] = 100.0
            illustration_jobs[job_id]["current_step"] = "Illustration generation completed!"
            illustration_jobs[job_id]["total_segments"] = len(result.get("story_segments", []))
            illustration_jobs[job_id]["illustrations_generated"] = result.get("total_illustrations", 0)
            illustration_jobs[job_id]["result"] = StoryIllustratorResponse(
                success=result["success"],
                story_title=result.get("story_title"),
                story_segments=result.get("story_segments", []),
                illustrations=result.get("illustrations", []),
                total_illustrations=result.get("total_illustrations", 0),
                processing_time=result.get("processing_time"),
                download_url=result.get("download_url"),
                error_message=None
            ).dict()
            illustration_jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()
        
        logger.info(f"Illustration generation job completed: {job_id}")
        
    except Exception as e:
        logger.error_with_context(e, {"job_id": job_id})
        
        # Update job with error
        if job_id in illustration_jobs:
            illustration_jobs[job_id]["status"] = "failed"
            illustration_jobs[job_id]["error"] = str(e)
            illustration_jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()


@router.get("/health")
async def health_check():
    """Health check endpoint for the story illustrator service."""
    try:
        service = get_story_illustrator_service()
        return {
            "status": "healthy",
            "service": "story_illustrator",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")