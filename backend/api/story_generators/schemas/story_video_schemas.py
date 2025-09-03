"""
Pydantic schemas for AI Story Video Generator endpoints.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum


class VideoFormat(str, Enum):
    MP4 = "mp4"
    AVI = "avi"
    MOV = "mov"
    WEBM = "webm"


class VideoQuality(str, Enum):
    LOW = "480p"
    MEDIUM = "720p"
    HIGH = "1080p"
    ULTRA = "4K"


class TransitionType(str, Enum):
    FADE = "fade"
    SLIDE = "slide"
    ZOOM = "zoom"
    DISSOLVE = "dissolve"
    NONE = "none"


class AudioSettings(BaseModel):
    """Settings for video audio."""
    
    include_narration: bool = Field(default=False, description="Include AI-generated narration")
    background_music: bool = Field(default=True, description="Include background music")
    music_url: Optional[HttpUrl] = Field(None, description="URL to custom background music")
    narration_voice: str = Field(default="neutral", description="Voice type for narration")
    audio_volume: float = Field(default=0.7, ge=0.0, le=1.0, description="Audio volume level")


class VideoSettings(BaseModel):
    """Settings for video generation."""
    
    fps: int = Field(default=24, ge=1, le=60, description="Frames per second")
    duration_per_scene: float = Field(default=5.0, ge=1.0, le=30.0, description="Duration per scene in seconds")
    video_format: VideoFormat = Field(default=VideoFormat.MP4, description="Output video format")
    quality: VideoQuality = Field(default=VideoQuality.HIGH, description="Video quality")
    transition_type: TransitionType = Field(default=TransitionType.FADE, description="Transition effect between scenes")
    transition_duration: float = Field(default=1.0, ge=0.1, le=5.0, description="Transition duration in seconds")
    include_subtitles: bool = Field(default=True, description="Include subtitles/captions")
    subtitle_style: Dict[str, Any] = Field(
        default_factory=lambda: {
            "font_size": 24,
            "font_color": "white",
            "background_color": "black",
            "position": "bottom"
        },
        description="Subtitle styling options"
    )


class StoryVideoRequest(BaseModel):
    """Request schema for story video generation."""
    
    story_text: str = Field(..., description="The story text to convert to video")
    title: Optional[str] = Field(None, description="Video title")
    video_settings: VideoSettings = Field(
        default_factory=VideoSettings,
        description="Video generation settings"
    )
    audio_settings: AudioSettings = Field(
        default_factory=AudioSettings,
        description="Audio settings for the video"
    )
    illustration_style: str = Field(
        default="digital art",
        description="Art style for scene illustrations"
    )


class SceneData(BaseModel):
    """Data for a single video scene."""
    
    scene_text: str = Field(..., description="Text content for this scene")
    scene_index: int = Field(..., description="Index of the scene in the video")
    image_prompt: str = Field(..., description="Prompt used to generate the scene image")
    image_url: Optional[str] = Field(None, description="URL to the generated scene image")
    image_base64: Optional[str] = Field(None, description="Base64 encoded scene image")
    duration: float = Field(..., description="Duration of this scene in seconds")
    narration_text: Optional[str] = Field(None, description="Narration text for this scene")
    narration_audio_url: Optional[str] = Field(None, description="URL to narration audio file")


class StoryVideoResponse(BaseModel):
    """Response schema for story video generation."""
    
    success: bool = Field(..., description="Whether the video generation was successful")
    video_url: Optional[str] = Field(None, description="URL to the generated video file")
    video_file_size: Optional[int] = Field(None, description="Size of the video file in bytes")
    video_duration: Optional[float] = Field(None, description="Duration of the video in seconds")
    scenes: List[SceneData] = Field(default_factory=list, description="Data for each scene in the video")
    total_scenes: int = Field(default=0, description="Total number of scenes in the video")
    processing_time: Optional[float] = Field(None, description="Total processing time in seconds")
    thumbnail_url: Optional[str] = Field(None, description="URL to video thumbnail image")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional video metadata"
    )
    error_message: Optional[str] = Field(None, description="Error message if generation failed")


class VideoGenerationProgress(BaseModel):
    """Schema for video generation progress updates."""
    
    status: str = Field(..., description="Current status of video generation")
    progress: float = Field(..., description="Progress percentage (0-100)")
    current_step: str = Field(..., description="Current step in the generation process")
    scenes_processed: int = Field(default=0, description="Number of scenes processed")
    total_scenes: int = Field(default=0, description="Total number of scenes")
    current_scene_progress: float = Field(default=0.0, description="Progress of current scene (0-100)")
    estimated_completion_time: Optional[int] = Field(None, description="Estimated completion time in seconds")
    current_operation: str = Field(default="", description="Current operation being performed")


class VideoGenerationJob(BaseModel):
    """Schema for video generation job tracking."""
    
    job_id: str = Field(..., description="Unique identifier for the generation job")
    status: str = Field(..., description="Current job status")
    created_at: str = Field(..., description="Job creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
    progress: VideoGenerationProgress = Field(..., description="Current progress information")
    result: Optional[StoryVideoResponse] = Field(None, description="Final result if completed")