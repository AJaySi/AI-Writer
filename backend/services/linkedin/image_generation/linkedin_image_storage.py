"""
LinkedIn Image Storage Service

This service handles image storage, retrieval, and management for LinkedIn image generation.
It provides secure storage, efficient retrieval, and metadata management for generated images.
"""

import os
import hashlib
import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image
from io import BytesIO
from loguru import logger

# Import existing infrastructure
from ...api_key_manager import APIKeyManager


class LinkedInImageStorage:
    """
    Handles storage and management of LinkedIn generated images.
    
    This service provides secure storage, efficient retrieval, metadata management,
    and cleanup functionality for LinkedIn image generation.
    """
    
    def __init__(self, storage_path: Optional[str] = None, api_key_manager: Optional[APIKeyManager] = None):
        """
        Initialize the LinkedIn Image Storage service.
        
        Args:
            storage_path: Base path for image storage
            api_key_manager: API key manager for authentication
        """
        self.api_key_manager = api_key_manager or APIKeyManager()
        
        # Set up storage paths
        if storage_path:
            self.base_storage_path = Path(storage_path)
        else:
            # Default to project-relative path
            self.base_storage_path = Path(__file__).parent.parent.parent.parent / "linkedin_images"
        
        # Create storage directories
        self.images_path = self.base_storage_path / "images"
        self.metadata_path = self.base_storage_path / "metadata"
        self.temp_path = self.base_storage_path / "temp"
        
        # Ensure directories exist
        self._create_storage_directories()
        
        # Storage configuration
        self.max_storage_size_gb = 10  # Maximum storage size in GB
        self.image_retention_days = 30  # Days to keep images
        self.max_image_size_mb = 10    # Maximum individual image size in MB
        
        logger.info(f"LinkedIn Image Storage initialized at {self.base_storage_path}")
    
    def _create_storage_directories(self):
        """Create necessary storage directories."""
        try:
            self.images_path.mkdir(parents=True, exist_ok=True)
            self.metadata_path.mkdir(parents=True, exist_ok=True)
            self.temp_path.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories for organization
            (self.images_path / "posts").mkdir(exist_ok=True)
            (self.images_path / "articles").mkdir(exist_ok=True)
            (self.images_path / "carousels").mkdir(exist_ok=True)
            (self.images_path / "video_scripts").mkdir(exist_ok=True)
            
            logger.info("Storage directories created successfully")
            
        except Exception as e:
            logger.error(f"Error creating storage directories: {str(e)}")
            raise
    
    async def store_image(
        self, 
        image_data: bytes, 
        metadata: Dict[str, Any],
        content_type: str = "post"
    ) -> Dict[str, Any]:
        """
        Store generated image with metadata.
        
        Args:
            image_data: Image data in bytes
            image_metadata: Image metadata and context
            content_type: Type of LinkedIn content (post, article, carousel, video_script)
            
        Returns:
            Dict containing storage result and image ID
        """
        try:
            start_time = datetime.now()
            
            # Generate unique image ID
            image_id = self._generate_image_id(image_data, metadata)
            
            # Validate image data
            validation_result = await self._validate_image_for_storage(image_data)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'error': f"Image validation failed: {validation_result['error']}"
                }
            
            # Determine storage path based on content type
            storage_path = self._get_storage_path(content_type, image_id)
            
            # Store image file
            image_stored = await self._store_image_file(image_data, storage_path)
            if not image_stored:
                return {
                    'success': False,
                    'error': 'Failed to store image file'
                }
            
            # Store metadata
            metadata_stored = await self._store_metadata(image_id, metadata, storage_path)
            if not metadata_stored:
                # Clean up image file if metadata storage fails
                await self._cleanup_failed_storage(storage_path)
                return {
                    'success': False,
                    'error': 'Failed to store image metadata'
                }
            
            # Update storage statistics
            await self._update_storage_stats()
            
            storage_time = (datetime.now() - start_time).total_seconds()
            
            return {
                'success': True,
                'image_id': image_id,
                'storage_path': str(storage_path),
                'metadata': {
                    'stored_at': datetime.now().isoformat(),
                    'storage_time': storage_time,
                    'file_size': len(image_data),
                    'content_type': content_type
                }
            }
            
        except Exception as e:
            logger.error(f"Error storing LinkedIn image: {str(e)}")
            return {
                'success': False,
                'error': f"Image storage failed: {str(e)}"
            }
    
    async def retrieve_image(self, image_id: str) -> Dict[str, Any]:
        """
        Retrieve stored image by ID.
        
        Args:
            image_id: Unique image identifier
            
        Returns:
            Dict containing image data and metadata
        """
        try:
            # Find image file
            image_path = await self._find_image_by_id(image_id)
            if not image_path:
                return {
                    'success': False,
                    'error': f'Image not found: {image_id}'
                }
            
            # Load metadata
            metadata = await self._load_metadata(image_id)
            if not metadata:
                return {
                    'success': False,
                    'error': f'Metadata not found for image: {image_id}'
                }
            
            # Read image data
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            return {
                'success': True,
                'image_data': image_data,
                'metadata': metadata,
                'image_path': str(image_path)
            }
            
        except Exception as e:
            logger.error(f"Error retrieving LinkedIn image {image_id}: {str(e)}")
            return {
                'success': False,
                'error': f"Image retrieval failed: {str(e)}"
            }
    
    async def delete_image(self, image_id: str) -> Dict[str, Any]:
        """
        Delete stored image and metadata.
        
        Args:
            image_id: Unique image identifier
            
        Returns:
            Dict containing deletion result
        """
        try:
            # Find image file
            image_path = await self._find_image_by_id(image_id)
            if not image_path:
                return {
                    'success': False,
                    'error': f'Image not found: {image_id}'
                }
            
            # Delete image file
            if image_path.exists():
                image_path.unlink()
                logger.info(f"Deleted image file: {image_path}")
            
            # Delete metadata
            metadata_path = self.metadata_path / f"{image_id}.json"
            if metadata_path.exists():
                metadata_path.unlink()
                logger.info(f"Deleted metadata file: {metadata_path}")
            
            # Update storage statistics
            await self._update_storage_stats()
            
            return {
                'success': True,
                'message': f'Image {image_id} deleted successfully'
            }
            
        except Exception as e:
            logger.error(f"Error deleting LinkedIn image {image_id}: {str(e)}")
            return {
                'success': False,
                'error': f"Image deletion failed: {str(e)}"
            }
    
    async def list_images(
        self, 
        content_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        List stored images with optional filtering.
        
        Args:
            content_type: Filter by content type
            limit: Maximum number of images to return
            offset: Number of images to skip
            
        Returns:
            Dict containing list of images and metadata
        """
        try:
            images = []
            
            # Scan metadata directory
            metadata_files = list(self.metadata_path.glob("*.json"))
            
            for metadata_file in metadata_files[offset:offset + limit]:
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    
                    # Apply content type filter
                    if content_type and metadata.get('content_type') != content_type:
                        continue
                    
                    # Check if image file still exists
                    image_id = metadata_file.stem
                    image_path = await self._find_image_by_id(image_id)
                    
                    if image_path and image_path.exists():
                        # Add file size and last modified info
                        stat = image_path.stat()
                        metadata['file_size'] = stat.st_size
                        metadata['last_modified'] = datetime.fromtimestamp(stat.st_mtime).isoformat()
                        
                        images.append(metadata)
                    
                except Exception as e:
                    logger.warning(f"Error reading metadata file {metadata_file}: {str(e)}")
                    continue
            
            return {
                'success': True,
                'images': images,
                'total_count': len(images),
                'limit': limit,
                'offset': offset
            }
            
        except Exception as e:
            logger.error(f"Error listing LinkedIn images: {str(e)}")
            return {
                'success': False,
                'error': f"Image listing failed: {str(e)}"
            }
    
    async def cleanup_old_images(self, days_old: Optional[int] = None) -> Dict[str, Any]:
        """
        Clean up old images based on retention policy.
        
        Args:
            days_old: Minimum age in days for cleanup (defaults to retention policy)
            
        Returns:
            Dict containing cleanup results
        """
        try:
            if days_old is None:
                days_old = self.image_retention_days
            
            cutoff_date = datetime.now() - timedelta(days=days_old)
            deleted_count = 0
            errors = []
            
            # Scan metadata directory
            metadata_files = list(self.metadata_path.glob("*.json"))
            
            for metadata_file in metadata_files:
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    
                    # Check creation date
                    created_at = metadata.get('stored_at')
                    if created_at:
                        created_date = datetime.fromisoformat(created_at)
                        if created_date < cutoff_date:
                            # Delete old image
                            image_id = metadata_file.stem
                            delete_result = await self.delete_image(image_id)
                            
                            if delete_result['success']:
                                deleted_count += 1
                            else:
                                errors.append(f"Failed to delete {image_id}: {delete_result['error']}")
                    
                except Exception as e:
                    logger.warning(f"Error processing metadata file {metadata_file}: {str(e)}")
                    continue
            
            return {
                'success': True,
                'deleted_count': deleted_count,
                'errors': errors,
                'cutoff_date': cutoff_date.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error cleaning up old LinkedIn images: {str(e)}")
            return {
                'success': False,
                'error': f"Cleanup failed: {str(e)}"
            }
    
    async def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics and usage information.
        
        Returns:
            Dict containing storage statistics
        """
        try:
            total_size = 0
            total_files = 0
            content_type_counts = {}
            
            # Calculate storage usage
            for content_type_dir in self.images_path.iterdir():
                if content_type_dir.is_dir():
                    content_type = content_type_dir.name
                    content_type_counts[content_type] = 0
                    
                    for image_file in content_type_dir.glob("*"):
                        if image_file.is_file():
                            total_size += image_file.stat().st_size
                            total_files += 1
                            content_type_counts[content_type] += 1
            
            # Check storage limits
            total_size_gb = total_size / (1024 ** 3)
            storage_limit_exceeded = total_size_gb > self.max_storage_size_gb
            
            return {
                'success': True,
                'total_size_bytes': total_size,
                'total_size_gb': round(total_size_gb, 2),
                'total_files': total_files,
                'content_type_counts': content_type_counts,
                'storage_limit_gb': self.max_storage_size_gb,
                'storage_limit_exceeded': storage_limit_exceeded,
                'retention_days': self.image_retention_days
            }
            
        except Exception as e:
            logger.error(f"Error getting storage stats: {str(e)}")
            return {
                'success': False,
                'error': f"Failed to get storage stats: {str(e)}"
            }
    
    def _generate_image_id(self, image_data: bytes, metadata: Dict[str, Any]) -> str:
        """Generate unique image ID based on content and metadata."""
        # Create hash from image data and key metadata
        hash_input = f"{image_data[:1000]}{metadata.get('topic', '')}{metadata.get('industry', '')}{datetime.now().isoformat()}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    async def _validate_image_for_storage(self, image_data: bytes) -> Dict[str, Any]:
        """Validate image data before storage."""
        try:
            # Check file size
            if len(image_data) > self.max_image_size_mb * 1024 * 1024:
                return {
                    'valid': False,
                    'error': f'Image size {len(image_data) / (1024*1024):.2f}MB exceeds maximum {self.max_image_size_mb}MB'
                }
            
            # Validate image format
            try:
                image = Image.open(BytesIO(image_data))
                if image.format not in ['PNG', 'JPEG', 'JPG']:
                    return {
                        'valid': False,
                        'error': f'Unsupported image format: {image.format}'
                    }
            except Exception as e:
                return {
                    'valid': False,
                    'error': f'Invalid image data: {str(e)}'
                }
            
            return {'valid': True}
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Validation error: {str(e)}'
            }
    
    def _get_storage_path(self, content_type: str, image_id: str) -> Path:
        """Get storage path for image based on content type."""
        # Map content types to directory names
        content_type_map = {
            'post': 'posts',
            'article': 'articles',
            'carousel': 'carousels',
            'video_script': 'video_scripts'
        }
        
        directory = content_type_map.get(content_type, 'posts')
        return self.images_path / directory / f"{image_id}.png"
    
    async def _store_image_file(self, image_data: bytes, storage_path: Path) -> bool:
        """Store image file to disk."""
        try:
            # Ensure directory exists
            storage_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write image data
            with open(storage_path, 'wb') as f:
                f.write(image_data)
            
            logger.info(f"Stored image file: {storage_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing image file: {str(e)}")
            return False
    
    async def _store_metadata(self, image_id: str, metadata: Dict[str, Any], storage_path: Path) -> bool:
        """Store image metadata to JSON file."""
        try:
            # Add storage metadata
            metadata['image_id'] = image_id
            metadata['storage_path'] = str(storage_path)
            metadata['stored_at'] = datetime.now().isoformat()
            
            # Write metadata file
            metadata_path = self.metadata_path / f"{image_id}.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            logger.info(f"Stored metadata: {metadata_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing metadata: {str(e)}")
            return False
    
    async def _find_image_by_id(self, image_id: str) -> Optional[Path]:
        """Find image file by ID across all content type directories."""
        for content_dir in self.images_path.iterdir():
            if content_dir.is_dir():
                image_path = content_dir / f"{image_id}.png"
                if image_path.exists():
                    return image_path
        
        return None
    
    async def _load_metadata(self, image_id: str) -> Optional[Dict[str, Any]]:
        """Load metadata for image ID."""
        try:
            metadata_path = self.metadata_path / f"{image_id}.json"
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading metadata for {image_id}: {str(e)}")
        
        return None
    
    async def _cleanup_failed_storage(self, storage_path: Path):
        """Clean up files if storage operation fails."""
        try:
            if storage_path.exists():
                storage_path.unlink()
                logger.info(f"Cleaned up failed storage: {storage_path}")
        except Exception as e:
            logger.error(f"Error cleaning up failed storage: {str(e)}")
    
    async def _update_storage_stats(self):
        """Update storage statistics (placeholder for future implementation)."""
        # This could be implemented to track storage usage over time
        pass
