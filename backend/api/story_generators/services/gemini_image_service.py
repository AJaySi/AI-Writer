"""
Enhanced Gemini Image Generation Service

This service provides enhanced image generation capabilities using the latest Gemini API,
specifically designed for story illustration with support for the new image generation features.

Based on: https://ai.google.dev/gemini-api/docs/image-generation
"""

import os
import sys
import time
import base64
import asyncio
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
from PIL import Image
from io import BytesIO
import tempfile
import uuid

try:
    import google.genai as genai
    from google.genai import types
except ImportError:
    genai = None

from ..core.logging import get_logger
from ..core.exceptions import (
    IllustrationGenerationError,
    ModelConnectionError,
    RateLimitError,
    InvalidInputError
)
from ...services.api_key_manager import APIKeyManager

logger = get_logger(__name__)


class EnhancedGeminiImageService:
    """Enhanced Gemini image generation service with latest API features."""
    
    def __init__(self):
        """Initialize the Gemini image service."""
        self.api_key_manager = APIKeyManager()
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Gemini client."""
        try:
            if genai is None:
                raise ModelConnectionError(
                    "Google genai library not available. Install with: pip install google-genai"
                )
            
            api_key = self.api_key_manager.get_api_key("GEMINI_API_KEY")
            if not api_key:
                raise ModelConnectionError("Gemini API key not found")
            
            genai.configure(api_key=api_key)
            logger.info("Gemini client initialized successfully")
            
        except Exception as e:
            logger.error_with_context(e, {"service": "gemini_image"})
            raise ModelConnectionError(f"Failed to initialize Gemini client: {str(e)}")
    
    async def generate_image(
        self,
        prompt: str,
        style: str = "digital art",
        aspect_ratio: str = "16:9",
        quality: str = "high",
        num_images: int = 1,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Generate images using Gemini's latest image generation capabilities.
        
        Args:
            prompt: Text description for image generation
            style: Art style for the image
            aspect_ratio: Aspect ratio (1:1, 16:9, 9:16, etc.)
            quality: Image quality (standard, high, ultra)
            num_images: Number of images to generate
            **kwargs: Additional parameters
            
        Returns:
            List of generated image data
        """
        try:
            logger.log_generation_start("image", {"prompt": prompt, "style": style})
            start_time = time.time()
            
            # Enhance prompt with style and quality parameters
            enhanced_prompt = self._enhance_prompt(prompt, style, aspect_ratio, quality)
            
            images = []
            for i in range(num_images):
                logger.log_generation_progress("image", (i / num_images) * 100, f"Generating image {i+1}/{num_images}")
                
                image_data = await self._generate_single_image(enhanced_prompt, aspect_ratio)
                if image_data:
                    images.append({
                        "index": i,
                        "prompt": enhanced_prompt,
                        "image_data": image_data,
                        "metadata": {
                            "style": style,
                            "aspect_ratio": aspect_ratio,
                            "quality": quality,
                            "generation_time": time.time() - start_time
                        }
                    })
            
            duration = time.time() - start_time
            logger.log_generation_complete("image", duration, len(images) > 0)
            logger.log_api_call("gemini", "imagen-3.0", None)
            
            return images
            
        except Exception as e:
            logger.error_with_context(e, {
                "prompt": prompt,
                "style": style,
                "aspect_ratio": aspect_ratio
            })
            raise IllustrationGenerationError(f"Image generation failed: {str(e)}")
    
    async def _generate_single_image(self, prompt: str, aspect_ratio: str) -> Optional[str]:
        """Generate a single image using Gemini API."""
        try:
            # Use the new Gemini 2.0 Flash Experimental model for image generation
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            # Configure generation parameters
            generation_config = types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=8192,
                response_modalities=["Text", "Image"]  # Required for image generation
            )
            
            # Generate content with image
            response = await asyncio.to_thread(
                model.generate_content,
                prompt,
                config=generation_config
            )
            
            # Extract image from response
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                
                # Look for image parts in the response
                for part in candidate.content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        # Convert image data to base64
                        image_data = part.inline_data.data
                        return base64.b64encode(image_data).decode('utf-8')
            
            return None
            
        except Exception as e:
            logger.error(f"Single image generation failed: {str(e)}")
            if "quota" in str(e).lower() or "rate" in str(e).lower():
                raise RateLimitError(f"Rate limit exceeded: {str(e)}")
            raise IllustrationGenerationError(f"Image generation failed: {str(e)}")
    
    def _enhance_prompt(self, prompt: str, style: str, aspect_ratio: str, quality: str) -> str:
        """Enhance the prompt with style and quality parameters."""
        # Style enhancements
        style_prompts = {
            "digital art": "digital artwork, highly detailed, vibrant colors",
            "watercolor": "watercolor painting, soft brushstrokes, flowing colors",
            "oil painting": "oil painting, rich textures, classical technique",
            "pencil sketch": "detailed pencil sketch, fine lines, artistic shading",
            "cartoon": "cartoon style, colorful, playful illustration",
            "anime": "anime style, detailed characters, dynamic composition",
            "realistic": "photorealistic, high detail, natural lighting",
            "fantasy": "fantasy art, magical elements, ethereal atmosphere",
            "children's book illustration": "children's book style, friendly, colorful, simple"
        }
        
        # Quality enhancements
        quality_prompts = {
            "standard": "good quality",
            "high": "high quality, detailed, professional",
            "ultra": "ultra high quality, masterpiece, award-winning, 4K resolution"
        }
        
        # Aspect ratio considerations
        aspect_prompts = {
            "16:9": "widescreen composition, cinematic framing",
            "9:16": "vertical composition, portrait orientation",
            "1:1": "square composition, balanced framing",
            "4:3": "classic composition, traditional framing"
        }
        
        # Build enhanced prompt
        enhanced = prompt
        
        if style in style_prompts:
            enhanced = f"{style_prompts[style]}, {enhanced}"
        
        if quality in quality_prompts:
            enhanced = f"{enhanced}, {quality_prompts[quality]}"
        
        if aspect_ratio in aspect_prompts:
            enhanced = f"{enhanced}, {aspect_prompts[aspect_ratio]}"
        
        return enhanced
    
    async def generate_story_illustrations(
        self,
        story_segments: List[str],
        style: str = "digital art",
        aspect_ratio: str = "16:9",
        max_illustrations: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Generate illustrations for multiple story segments.
        
        Args:
            story_segments: List of story text segments
            style: Art style for illustrations
            aspect_ratio: Image aspect ratio
            max_illustrations: Maximum number of illustrations to generate
            
        Returns:
            List of illustration data
        """
        try:
            logger.log_generation_start("story_illustrations", {
                "segments": len(story_segments),
                "style": style
            })
            
            # Limit segments if necessary
            segments_to_process = story_segments[:max_illustrations]
            illustrations = []
            
            for i, segment in enumerate(segments_to_process):
                logger.log_generation_progress(
                    "story_illustrations",
                    (i / len(segments_to_process)) * 100,
                    f"Processing segment {i+1}/{len(segments_to_process)}"
                )
                
                # Generate illustration prompt from story segment
                illustration_prompt = await self._create_illustration_prompt(segment)
                
                # Generate image
                images = await self.generate_image(
                    illustration_prompt,
                    style=style,
                    aspect_ratio=aspect_ratio,
                    num_images=1
                )
                
                if images:
                    illustrations.append({
                        "segment_index": i,
                        "segment_text": segment,
                        "illustration_prompt": illustration_prompt,
                        "image_data": images[0]["image_data"],
                        "metadata": images[0]["metadata"]
                    })
                
                # Add delay to avoid rate limiting
                await asyncio.sleep(1)
            
            logger.log_generation_complete("story_illustrations", time.time(), True)
            return illustrations
            
        except Exception as e:
            logger.error_with_context(e, {"segments_count": len(story_segments)})
            raise IllustrationGenerationError(f"Story illustration generation failed: {str(e)}")
    
    async def _create_illustration_prompt(self, story_segment: str) -> str:
        """Create an illustration prompt from a story segment using AI."""
        try:
            model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')
            
            prompt = f"""
            Based on this story segment, create a detailed visual description for an illustration:
            
            Story segment: "{story_segment}"
            
            Create a vivid, detailed description focusing on:
            - The main scene or setting
            - Key characters and their appearance
            - Important objects or elements
            - The mood and atmosphere
            - Visual composition
            
            Keep the description concise but detailed enough for image generation.
            """
            
            response = await asyncio.to_thread(model.generate_content, prompt)
            
            if response.text:
                return response.text.strip()
            else:
                # Fallback to simple extraction
                return self._extract_visual_elements(story_segment)
                
        except Exception as e:
            logger.warning(f"Failed to generate illustration prompt with AI: {str(e)}")
            return self._extract_visual_elements(story_segment)
    
    def _extract_visual_elements(self, text: str) -> str:
        """Extract visual elements from text as fallback."""
        # Simple extraction of potential visual elements
        words = text.split()
        
        # Look for visual descriptors
        visual_words = []
        for word in words:
            if any(keyword in word.lower() for keyword in [
                'color', 'light', 'dark', 'bright', 'shadow', 'sun', 'moon',
                'tree', 'house', 'mountain', 'river', 'forest', 'city',
                'character', 'person', 'man', 'woman', 'child'
            ]):
                visual_words.append(word)
        
        if visual_words:
            return f"Illustration showing {' '.join(visual_words[:10])}"
        else:
            return f"Illustration of the scene: {text[:100]}..."
    
    def save_image(self, image_data: str, filename: str, output_dir: str = None) -> str:
        """
        Save base64 image data to file.
        
        Args:
            image_data: Base64 encoded image data
            filename: Output filename
            output_dir: Output directory (optional)
            
        Returns:
            Path to saved file
        """
        try:
            # Create output directory if not specified
            if output_dir is None:
                output_dir = tempfile.mkdtemp(prefix="story_illustrations_")
            
            os.makedirs(output_dir, exist_ok=True)
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            
            # Save image
            output_path = os.path.join(output_dir, filename)
            image.save(output_path)
            
            logger.info(f"Image saved to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error_with_context(e, {"filename": filename})
            raise IllustrationGenerationError(f"Failed to save image: {str(e)}")


# Global service instance
_gemini_image_service = None


def get_gemini_image_service() -> EnhancedGeminiImageService:
    """Get or create the Gemini image service instance."""
    global _gemini_image_service
    if _gemini_image_service is None:
        _gemini_image_service = EnhancedGeminiImageService()
    return _gemini_image_service