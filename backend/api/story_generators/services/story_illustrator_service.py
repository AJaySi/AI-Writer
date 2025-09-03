"""
AI Story Illustrator Service

This service provides functionality for generating illustrations for stories,
converted from the original Streamlit implementation to work with FastAPI.
"""

import asyncio
import time
import re
import tempfile
import zipfile
import os
import base64
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

from ..core.logging import get_logger
from ..core.exceptions import (
    IllustrationGenerationError,
    FileProcessingError,
    InvalidInputError
)
from .gemini_image_service import get_gemini_image_service

logger = get_logger(__name__)


class StoryIllustratorService:
    """Service for generating story illustrations using AI."""
    
    def __init__(self):
        """Initialize the story illustrator service."""
        self.logger = logger
        self.image_service = get_gemini_image_service()
        self.max_story_length = 10000
        self.min_segment_length = 100
        self.max_segments = 20
    
    async def generate_illustrations(
        self,
        story_input: Dict[str, Any],
        settings: Dict[str, Any],
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Generate illustrations for a story.
        
        Args:
            story_input: Story input data (text, url, or file)
            settings: Illustration generation settings
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary containing generated illustrations and metadata
        """
        try:
            logger.log_generation_start("story_illustrations", {
                "input_type": self._get_input_type(story_input),
                "style": settings.get("style", "digital art")
            })
            
            start_time = time.time()
            
            # Update progress
            if progress_callback:
                await progress_callback("Processing story input...", 5)
            
            # Extract story text
            story_text = await self._extract_story_text(story_input)
            
            if not story_text:
                raise InvalidInputError("No story text could be extracted from input")
            
            # Validate story length
            if len(story_text) > self.max_story_length:
                story_text = story_text[:self.max_story_length]
                logger.warning(f"Story truncated to {self.max_story_length} characters")
            
            # Update progress
            if progress_callback:
                await progress_callback("Segmenting story...", 15)
            
            # Segment the story
            segments = self._segment_story(
                story_text,
                settings.get("min_segment_length", self.min_segment_length),
                settings.get("max_illustrations", self.max_segments)
            )
            
            logger.info(f"Story segmented into {len(segments)} parts")
            
            # Update progress
            if progress_callback:
                await progress_callback("Generating illustrations...", 25)
            
            # Generate illustrations
            illustrations = await self._generate_illustrations_for_segments(
                segments,
                settings,
                progress_callback
            )
            
            # Update progress
            if progress_callback:
                await progress_callback("Creating download package...", 90)
            
            # Create download package
            download_url = await self._create_download_package(illustrations)
            
            duration = time.time() - start_time
            logger.log_generation_complete("story_illustrations", duration, True)
            
            # Update progress
            if progress_callback:
                await progress_callback("Illustrations generated successfully!", 100)
            
            return {
                "success": True,
                "story_title": self._extract_title(story_text),
                "story_segments": segments,
                "illustrations": illustrations,
                "total_illustrations": len(illustrations),
                "processing_time": duration,
                "download_url": download_url
            }
            
        except Exception as e:
            logger.error_with_context(e, {"input_type": self._get_input_type(story_input)})
            
            if isinstance(e, (IllustrationGenerationError, FileProcessingError, InvalidInputError)):
                raise e
            else:
                raise IllustrationGenerationError(f"Illustration generation failed: {str(e)}")
    
    async def _extract_story_text(self, story_input: Dict[str, Any]) -> str:
        """Extract story text from various input sources."""
        try:
            if story_input.get("text"):
                return story_input["text"]
            
            elif story_input.get("url"):
                return await self._extract_text_from_url(story_input["url"])
            
            elif story_input.get("file_content") and story_input.get("file_name"):
                return await self._extract_text_from_file(
                    story_input["file_content"],
                    story_input["file_name"]
                )
            
            else:
                raise InvalidInputError("No valid story input provided")
                
        except Exception as e:
            logger.error(f"Story text extraction failed: {str(e)}")
            raise FileProcessingError(f"Failed to extract story text: {str(e)}")
    
    async def _extract_text_from_url(self, url: str) -> str:
        """Extract text content from a URL."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = await asyncio.to_thread(
                requests.get, url, headers=headers, timeout=10
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            
            # Get text
            text = soup.get_text(separator='\\n')
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\\n'.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except Exception as e:
            logger.error(f"URL text extraction failed: {str(e)}")
            raise FileProcessingError(f"Failed to extract text from URL: {str(e)}")
    
    async def _extract_text_from_file(self, file_content: str, file_name: str) -> str:
        """Extract text from uploaded file content."""
        try:
            # Decode base64 content
            file_data = base64.b64decode(file_content)
            
            # Handle different file types
            file_ext = Path(file_name).suffix.lower()
            
            if file_ext in ['.txt', '.md']:
                return file_data.decode('utf-8')
            
            elif file_ext == '.pdf':
                # Would need additional PDF processing library
                raise FileProcessingError("PDF processing not yet implemented")
            
            elif file_ext in ['.doc', '.docx']:
                # Would need additional document processing library
                raise FileProcessingError("Document processing not yet implemented")
            
            else:
                # Try to decode as text
                try:
                    return file_data.decode('utf-8')
                except UnicodeDecodeError:
                    raise FileProcessingError(f"Unsupported file type: {file_ext}")
                    
        except Exception as e:
            logger.error(f"File text extraction failed: {str(e)}")
            raise FileProcessingError(f"Failed to extract text from file: {str(e)}")
    
    def _segment_story(
        self,
        story_text: str,
        min_segment_length: int,
        max_segments: int
    ) -> List[str]:
        """Segment a story into logical parts for illustration."""
        try:
            # Clean up the text
            story_text = story_text.strip()
            
            # Split by paragraphs first
            paragraphs = re.split(r'\\n\\s*\\n', story_text)
            
            # Initialize segments
            segments = []
            current_segment = ""
            
            for paragraph in paragraphs:
                # Skip empty paragraphs
                if not paragraph.strip():
                    continue
                
                # If adding this paragraph would make the segment too long, start a new segment
                if len(current_segment) + len(paragraph) > 1000:  # Limit segment size
                    if current_segment and len(current_segment) >= min_segment_length:
                        segments.append(current_segment.strip())
                    current_segment = paragraph
                else:
                    # Add paragraph to current segment
                    if current_segment:
                        current_segment += "\\n\\n" + paragraph
                    else:
                        current_segment = paragraph
                
                # Stop if we have enough segments
                if len(segments) >= max_segments:
                    break
            
            # Add the last segment if it's long enough
            if current_segment and len(current_segment) >= min_segment_length:
                segments.append(current_segment.strip())
            
            # If no segments were created, create segments from the whole text
            if not segments and story_text:
                # Split into chunks of reasonable size
                chunk_size = max(min_segment_length, len(story_text) // max_segments)
                for i in range(0, len(story_text), chunk_size):
                    chunk = story_text[i:i + chunk_size]
                    if len(chunk) >= min_segment_length:
                        segments.append(chunk)
                    if len(segments) >= max_segments:
                        break
            
            logger.info(f"Created {len(segments)} story segments")
            return segments[:max_segments]
            
        except Exception as e:
            logger.error(f"Story segmentation failed: {str(e)}")
            raise FileProcessingError(f"Failed to segment story: {str(e)}")
    
    async def _generate_illustrations_for_segments(
        self,
        segments: List[str],
        settings: Dict[str, Any],
        progress_callback: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """Generate illustrations for story segments."""
        try:
            illustrations = []
            total_segments = len(segments)
            
            for i, segment in enumerate(segments):
                # Update progress
                progress = 25 + (i / total_segments) * 60  # 25% to 85%
                if progress_callback:
                    await progress_callback(
                        f"Generating illustration {i+1} of {total_segments}...",
                        progress
                    )
                
                logger.info(f"Generating illustration for segment {i+1}/{total_segments}")
                
                try:
                    # Generate illustration for this segment
                    images = await self.image_service.generate_image(
                        segment,
                        style=settings.get("style", "digital art"),
                        aspect_ratio=settings.get("aspect_ratio", "16:9"),
                        quality=settings.get("quality", "high"),
                        num_images=1
                    )
                    
                    if images:
                        image_data = images[0]
                        illustrations.append({
                            "segment_text": segment,
                            "image_base64": image_data["image_data"],
                            "prompt_used": image_data["prompt"],
                            "segment_index": i,
                            "generation_time": image_data["metadata"].get("generation_time", 0)
                        })
                        
                        logger.info(f"Illustration {i+1} generated successfully")
                    else:
                        logger.warning(f"No illustration generated for segment {i+1}")
                
                except Exception as e:
                    logger.error(f"Failed to generate illustration for segment {i+1}: {str(e)}")
                    # Continue with other segments
                    continue
                
                # Add delay to avoid rate limiting
                if i < total_segments - 1:  # Don't delay after the last segment
                    await asyncio.sleep(2)
            
            logger.info(f"Generated {len(illustrations)} illustrations out of {total_segments} segments")
            return illustrations
            
        except Exception as e:
            logger.error(f"Illustration generation failed: {str(e)}")
            raise IllustrationGenerationError(f"Failed to generate illustrations: {str(e)}")
    
    async def _create_download_package(self, illustrations: List[Dict[str, Any]]) -> Optional[str]:
        """Create a ZIP package with all illustrations."""
        try:
            if not illustrations:
                return None
            
            # Create temporary directory
            temp_dir = tempfile.mkdtemp(prefix="story_illustrations_")
            zip_path = os.path.join(temp_dir, "story_illustrations.zip")
            
            with zipfile.ZipFile(zip_path, 'w') as zip_file:
                for i, illustration in enumerate(illustrations):
                    # Save image data to file
                    image_filename = f"illustration_{i+1:03d}.png"
                    image_data = base64.b64decode(illustration["image_base64"])
                    
                    # Add image to zip
                    zip_file.writestr(image_filename, image_data)
                    
                    # Create text file with segment and prompt
                    text_filename = f"illustration_{i+1:03d}_info.txt"
                    text_content = f"""Illustration {i+1}
Segment: {illustration['segment_text'][:200]}...
Prompt: {illustration['prompt_used']}
Generation Time: {illustration.get('generation_time', 'Unknown')} seconds
"""
                    zip_file.writestr(text_filename, text_content)
            
            # In a real implementation, you would upload this to a file storage service
            # and return the public URL. For now, we'll return the local path.
            logger.info(f"Created illustration package: {zip_path}")
            return zip_path
            
        except Exception as e:
            logger.error(f"Failed to create download package: {str(e)}")
            return None
    
    def _extract_title(self, story_text: str) -> str:
        """Extract or generate a title from the story text."""
        try:
            # Look for title patterns at the beginning
            lines = story_text.split('\\n')
            for line in lines[:5]:  # Check first 5 lines
                line = line.strip()
                if line and len(line) < 100:  # Reasonable title length
                    # Check if it looks like a title (short, no periods at end)
                    if not line.endswith('.') or len(line) < 50:
                        return line
            
            # Generate title from first sentence
            first_sentence = story_text.split('.')[0]
            if len(first_sentence) < 100:
                return first_sentence + "..."
            
            # Default title
            return "Generated Story"
            
        except Exception:
            return "Generated Story"
    
    def _get_input_type(self, story_input: Dict[str, Any]) -> str:
        """Get the type of story input."""
        if story_input.get("text"):
            return "text"
        elif story_input.get("url"):
            return "url"
        elif story_input.get("file_content"):
            return "file"
        else:
            return "unknown"


# Global service instance
_story_illustrator_service = None


def get_story_illustrator_service() -> StoryIllustratorService:
    """Get or create the story illustrator service instance."""
    global _story_illustrator_service
    if _story_illustrator_service is None:
        _story_illustrator_service = StoryIllustratorService()
    return _story_illustrator_service