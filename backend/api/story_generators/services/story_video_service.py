"""
AI Story Video Generator Service

This service provides functionality for generating story videos,
converted from the original Streamlit implementation to work with FastAPI.

Note: This is a simplified version that focuses on scene generation and image creation.
Full video compilation would require additional video processing libraries.
"""

import asyncio
import time
import tempfile
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

from ..core.logging import get_logger
from ..core.exceptions import (
    VideoGenerationError,
    FileProcessingError,
    InvalidInputError
)
from .gemini_image_service import get_gemini_image_service

logger = get_logger(__name__)


class StoryVideoService:
    """Service for generating story videos using AI."""
    
    def __init__(self):
        """Initialize the story video service."""
        self.logger = logger
        self.image_service = get_gemini_image_service()
        self.max_story_length = 5000  # Shorter for video processing
        self.max_scenes = 15  # Limit scenes for video
    
    async def generate_video_scenes(
        self,
        story_text: str,
        title: Optional[str],
        video_settings: Dict[str, Any],
        audio_settings: Dict[str, Any],
        illustration_style: str = "digital art",
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Generate video scenes from a story.
        
        Args:
            story_text: The story text to convert to video
            title: Video title
            video_settings: Video generation settings
            audio_settings: Audio settings for the video
            illustration_style: Art style for scene illustrations
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary containing generated scenes and metadata
        """
        try:
            logger.log_generation_start("story_video", {
                "story_length": len(story_text),
                "style": illustration_style
            })
            
            start_time = time.time()
            
            # Update progress
            if progress_callback:
                await progress_callback("Processing story text...", 10)
            
            # Validate and prepare story
            if len(story_text) > self.max_story_length:
                story_text = story_text[:self.max_story_length]
                logger.warning(f"Story truncated to {self.max_story_length} characters")
            
            # Update progress
            if progress_callback:
                await progress_callback("Creating video scenes...", 20)
            
            # Segment story into scenes
            scenes = await self._create_video_scenes(
                story_text,
                video_settings.get("duration_per_scene", 5.0),
                self.max_scenes
            )
            
            logger.info(f"Created {len(scenes)} video scenes")
            
            # Update progress
            if progress_callback:
                await progress_callback("Generating scene illustrations...", 30)
            
            # Generate images for scenes
            scene_data = await self._generate_scene_images(
                scenes,
                illustration_style,
                video_settings.get("quality", "high"),
                progress_callback
            )
            
            # Update progress
            if progress_callback:
                await progress_callback("Processing audio settings...", 80)
            
            # Process audio if requested
            if audio_settings.get("include_narration", False):
                scene_data = await self._add_narration_data(scene_data, audio_settings)
            
            # Update progress
            if progress_callback:
                await progress_callback("Finalizing video data...", 95)
            
            # Calculate video metadata
            total_duration = sum(scene.get("duration", 5.0) for scene in scene_data)
            
            duration = time.time() - start_time
            logger.log_generation_complete("story_video", duration, True)
            
            # Update progress
            if progress_callback:
                await progress_callback("Video scenes generated successfully!", 100)
            
            return {
                "success": True,
                "video_url": None,  # Would be generated after video compilation
                "video_file_size": None,
                "video_duration": total_duration,
                "scenes": scene_data,
                "total_scenes": len(scene_data),
                "processing_time": duration,
                "thumbnail_url": scene_data[0].get("image_url") if scene_data else None,
                "metadata": {
                    "title": title or "Generated Story Video",
                    "story_length": len(story_text),
                    "illustration_style": illustration_style,
                    "video_settings": video_settings,
                    "audio_settings": audio_settings
                }
            }
            
        except Exception as e:
            logger.error_with_context(e, {
                "story_length": len(story_text),
                "style": illustration_style
            })
            
            if isinstance(e, (VideoGenerationError, FileProcessingError, InvalidInputError)):
                raise e
            else:
                raise VideoGenerationError(f"Video generation failed: {str(e)}")
    
    async def _create_video_scenes(
        self,
        story_text: str,
        duration_per_scene: float,
        max_scenes: int
    ) -> List[str]:
        """Create video scenes from story text."""
        try:
            # Simple scene segmentation based on paragraphs and sentence breaks
            # In a more advanced version, this could use AI to identify scene changes
            
            # Split by paragraphs first
            paragraphs = [p.strip() for p in story_text.split('\\n\\n') if p.strip()]
            
            # If we have too few paragraphs, split by sentences
            if len(paragraphs) < 3:
                sentences = [s.strip() for s in story_text.split('.') if s.strip()]
                # Group sentences into scenes
                scene_size = max(1, len(sentences) // max_scenes)
                scenes = []
                for i in range(0, len(sentences), scene_size):
                    scene_text = '. '.join(sentences[i:i + scene_size])
                    if scene_text:
                        scenes.append(scene_text + '.')
            else:
                # Use paragraphs as scenes, combining small ones
                scenes = []
                current_scene = ""
                
                for paragraph in paragraphs:
                    if len(current_scene) + len(paragraph) > 200:  # Max scene length
                        if current_scene:
                            scenes.append(current_scene)
                        current_scene = paragraph
                    else:
                        if current_scene:
                            current_scene += "\\n\\n" + paragraph
                        else:
                            current_scene = paragraph
                    
                    if len(scenes) >= max_scenes:
                        break
                
                if current_scene and len(scenes) < max_scenes:
                    scenes.append(current_scene)
            
            # Limit to max scenes
            scenes = scenes[:max_scenes]
            
            logger.info(f"Created {len(scenes)} scenes from story")
            return scenes
            
        except Exception as e:
            logger.error(f"Scene creation failed: {str(e)}")
            raise VideoGenerationError(f"Failed to create video scenes: {str(e)}")
    
    async def _generate_scene_images(
        self,
        scenes: List[str],
        illustration_style: str,
        quality: str,
        progress_callback: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """Generate images for video scenes."""
        try:
            scene_data = []
            total_scenes = len(scenes)
            
            for i, scene_text in enumerate(scenes):
                # Update progress
                progress = 30 + (i / total_scenes) * 45  # 30% to 75%
                if progress_callback:
                    await progress_callback(
                        f"Generating image for scene {i+1} of {total_scenes}...",
                        progress
                    )
                
                logger.info(f"Generating image for scene {i+1}/{total_scenes}")
                
                try:
                    # Generate image for this scene
                    images = await self.image_service.generate_image(
                        scene_text,
                        style=illustration_style,
                        aspect_ratio="16:9",  # Standard video aspect ratio
                        quality=quality,
                        num_images=1
                    )
                    
                    if images:
                        image_data = images[0]
                        scene_data.append({
                            "scene_text": scene_text,
                            "scene_index": i,
                            "image_prompt": image_data["prompt"],
                            "image_base64": image_data["image_data"],
                            "duration": 5.0,  # Default scene duration
                            "narration_text": scene_text if len(scene_text) < 200 else scene_text[:200] + "...",
                            "narration_audio_url": None  # Would be generated separately
                        })
                        
                        logger.info(f"Scene {i+1} image generated successfully")
                    else:
                        logger.warning(f"No image generated for scene {i+1}")
                        # Add scene without image
                        scene_data.append({
                            "scene_text": scene_text,
                            "scene_index": i,
                            "image_prompt": scene_text,
                            "image_base64": None,
                            "duration": 5.0,
                            "narration_text": scene_text if len(scene_text) < 200 else scene_text[:200] + "...",
                            "narration_audio_url": None
                        })
                
                except Exception as e:
                    logger.error(f"Failed to generate image for scene {i+1}: {str(e)}")
                    # Continue with other scenes
                    scene_data.append({
                        "scene_text": scene_text,
                        "scene_index": i,
                        "image_prompt": scene_text,
                        "image_base64": None,
                        "duration": 5.0,
                        "narration_text": scene_text if len(scene_text) < 200 else scene_text[:200] + "...",
                        "narration_audio_url": None
                    })
                
                # Add delay to avoid rate limiting
                if i < total_scenes - 1:
                    await asyncio.sleep(1)
            
            logger.info(f"Generated images for {len([s for s in scene_data if s['image_base64']])} out of {total_scenes} scenes")
            return scene_data
            
        except Exception as e:
            logger.error(f"Scene image generation failed: {str(e)}")
            raise VideoGenerationError(f"Failed to generate scene images: {str(e)}")
    
    async def _add_narration_data(
        self,
        scene_data: List[Dict[str, Any]],
        audio_settings: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Add narration data to scenes (placeholder for future audio generation)."""
        try:
            # This is a placeholder for future audio generation functionality
            # In a full implementation, this would:
            # 1. Generate speech from scene text using TTS
            # 2. Save audio files
            # 3. Add audio URLs to scene data
            
            logger.info("Narration data processing (placeholder)")
            
            for scene in scene_data:
                # For now, just add metadata about narration
                scene["narration_enabled"] = True
                scene["narration_voice"] = audio_settings.get("narration_voice", "neutral")
                scene["audio_volume"] = audio_settings.get("audio_volume", 0.7)
                # scene["narration_audio_url"] would be set after TTS generation
            
            return scene_data
            
        except Exception as e:
            logger.error(f"Narration processing failed: {str(e)}")
            return scene_data  # Return scenes without narration if it fails
    
    async def compile_video(
        self,
        scene_data: List[Dict[str, Any]],
        video_settings: Dict[str, Any],
        audio_settings: Dict[str, Any]
    ) -> Optional[str]:
        """
        Compile scenes into a video file.
        
        This is a placeholder for future video compilation functionality.
        In a full implementation, this would use video processing libraries
        like moviepy to create the final video.
        """
        try:
            logger.info("Video compilation (placeholder)")
            
            # This would involve:
            # 1. Loading scene images
            # 2. Creating video clips with specified duration
            # 3. Adding transitions between scenes
            # 4. Adding background music if specified
            # 5. Adding narration audio if available
            # 6. Rendering final video file
            
            # For now, return None to indicate compilation is not yet implemented
            return None
            
        except Exception as e:
            logger.error(f"Video compilation failed: {str(e)}")
            raise VideoGenerationError(f"Video compilation failed: {str(e)}")


# Global service instance
_story_video_service = None


def get_story_video_service() -> StoryVideoService:
    """Get or create the story video service instance."""
    global _story_video_service
    if _story_video_service is None:
        _story_video_service = StoryVideoService()
    return _story_video_service