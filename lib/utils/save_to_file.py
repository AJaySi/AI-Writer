"""
Utility module for saving generated content to files.
Handles saving various types of content to the workspace directory.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Union, Dict, List, Any

# Define the workspace directory
WORKSPACE_DIR = Path(__file__).parent.parent.parent / "workspace" / "alwrity_content"

def ensure_directory_exists(directory: Union[str, Path]) -> None:
    """Ensure the specified directory exists."""
    os.makedirs(directory, exist_ok=True)

def save_to_file(
    content: Union[str, Dict, List, Any],
    filename: str,
    content_type: str = "text",
    subdirectory: str = None
) -> str:
    """
    Save content to a file in the workspace directory.
    
    Args:
        content: The content to save (string, dict, list, or any serializable object)
        filename: Name of the file to save
        content_type: Type of content ('text', 'json', 'audio', 'image')
        subdirectory: Optional subdirectory within the workspace
    
    Returns:
        str: Path to the saved file
    """
    # Create timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"{timestamp}_{filename}"
    
    # Determine the target directory
    target_dir = WORKSPACE_DIR
    if subdirectory:
        target_dir = target_dir / subdirectory
    
    # Ensure directory exists
    ensure_directory_exists(target_dir)
    
    # Determine file extension and format content
    if content_type == "json":
        file_path = target_dir / f"{base_filename}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
    elif content_type == "audio":
        file_path = target_dir / f"{base_filename}.mp3"
        with open(file_path, "wb") as f:
            f.write(content)
    elif content_type == "image":
        file_path = target_dir / f"{base_filename}.png"
        with open(file_path, "wb") as f:
            f.write(content)
    else:  # text
        file_path = target_dir / f"{base_filename}.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(content))
    
    return str(file_path)

def save_audio(audio_bytes: bytes, filename: str, subdirectory: str = "audio") -> str:
    """Save audio content to a file."""
    return save_to_file(audio_bytes, filename, "audio", subdirectory)

def save_image(image_bytes: bytes, filename: str, subdirectory: str = "images") -> str:
    """Save image content to a file."""
    return save_to_file(image_bytes, filename, "image", subdirectory)

def save_json(data: Union[Dict, List], filename: str, subdirectory: str = "json") -> str:
    """Save JSON content to a file."""
    return save_to_file(data, filename, "json", subdirectory)

def save_text(text: str, filename: str, subdirectory: str = "text") -> str:
    """Save text content to a file."""
    return save_to_file(text, filename, "text", subdirectory) 