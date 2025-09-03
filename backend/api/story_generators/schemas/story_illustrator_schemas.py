"""
Pydantic schemas for AI Story Illustrator endpoints.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum


class IllustrationStyle(str, Enum):
    DIGITAL_ART = "digital art"
    WATERCOLOR = "watercolor"
    OIL_PAINTING = "oil painting"
    PENCIL_SKETCH = "pencil sketch"
    CARTOON = "cartoon"
    ANIME = "anime"
    REALISTIC = "realistic"
    FANTASY = "fantasy"
    CHILDREN_BOOK = "children's book illustration"


class AspectRatio(str, Enum):
    SQUARE = "1:1"
    LANDSCAPE = "16:9"
    PORTRAIT = "9:16"
    CLASSIC = "4:3"
    WIDE = "21:9"


class ImageQuality(str, Enum):
    STANDARD = "standard"
    HIGH = "high"
    ULTRA = "ultra"


class StoryInput(BaseModel):
    """Schema for story input methods."""
    
    text: Optional[str] = Field(None, description="Direct text input of the story")
    url: Optional[HttpUrl] = Field(None, description="URL to extract story text from")
    file_content: Optional[str] = Field(None, description="Base64 encoded file content")
    file_name: Optional[str] = Field(None, description="Original filename")


class IllustrationSettings(BaseModel):
    """Settings for illustration generation."""
    
    style: IllustrationStyle = Field(
        default=IllustrationStyle.DIGITAL_ART,
        description="Art style for illustrations"
    )
    aspect_ratio: AspectRatio = Field(
        default=AspectRatio.LANDSCAPE,
        description="Aspect ratio for generated images"
    )
    quality: ImageQuality = Field(
        default=ImageQuality.HIGH,
        description="Quality level for generated images"
    )
    max_illustrations: int = Field(
        default=10,
        ge=1,
        le=20,
        description="Maximum number of illustrations to generate"
    )
    min_segment_length: int = Field(
        default=100,
        ge=50,
        le=500,
        description="Minimum length of story segment for illustration"
    )


class StoryIllustratorRequest(BaseModel):
    """Request schema for story illustration."""
    
    story_input: StoryInput = Field(..., description="Story input data")
    settings: IllustrationSettings = Field(
        default_factory=IllustrationSettings,
        description="Illustration generation settings"
    )


class IllustrationData(BaseModel):
    """Data for a single illustration."""
    
    segment_text: str = Field(..., description="Story segment that was illustrated")
    image_url: Optional[str] = Field(None, description="URL to the generated image")
    image_base64: Optional[str] = Field(None, description="Base64 encoded image data")
    prompt_used: str = Field(..., description="Prompt used to generate the illustration")
    segment_index: int = Field(..., description="Index of the story segment")
    generation_time: Optional[float] = Field(None, description="Time taken to generate this illustration")


class StoryIllustratorResponse(BaseModel):
    """Response schema for story illustration."""
    
    success: bool = Field(..., description="Whether the illustration generation was successful")
    story_title: Optional[str] = Field(None, description="Extracted or generated story title")
    story_segments: List[str] = Field(default_factory=list, description="Story segments that were processed")
    illustrations: List[IllustrationData] = Field(default_factory=list, description="Generated illustrations")
    total_illustrations: int = Field(default=0, description="Total number of illustrations generated")
    processing_time: Optional[float] = Field(None, description="Total processing time in seconds")
    download_url: Optional[str] = Field(None, description="URL to download all illustrations as a ZIP file")
    error_message: Optional[str] = Field(None, description="Error message if generation failed")


class IllustrationProgress(BaseModel):
    """Schema for illustration generation progress updates."""
    
    status: str = Field(..., description="Current status of illustration generation")
    progress: float = Field(..., description="Progress percentage (0-100)")
    current_step: str = Field(..., description="Current step in the generation process")
    segments_processed: int = Field(default=0, description="Number of segments processed")
    total_segments: int = Field(default=0, description="Total number of segments to process")
    illustrations_generated: int = Field(default=0, description="Number of illustrations generated")
    estimated_completion_time: Optional[int] = Field(None, description="Estimated completion time in seconds")