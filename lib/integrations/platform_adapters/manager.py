"""
Platform manager for handling multiple platform adapters.
"""

import logging
from typing import Dict, Any, List, Optional, Type
from datetime import datetime

from .base import PlatformAdapter
from .twitter import TwitterAdapter
from .wix import WixAdapter

logger = logging.getLogger(__name__)

class PlatformManager:
    """Manages multiple platform adapters."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize platform manager with configuration."""
        self.config = config
        self.adapters: Dict[str, PlatformAdapter] = {}
        self._initialize_adapters()
    
    def _initialize_adapters(self) -> None:
        """Initialize platform adapters based on configuration."""
        platform_configs = self.config.get('platforms', {})
        
        for platform, config in platform_configs.items():
            try:
                adapter = self._create_adapter(platform, config)
                if adapter:
                    self.adapters[platform] = adapter
                    logger.info(f"Initialized {platform} adapter")
            except Exception as e:
                logger.error(f"Failed to initialize {platform} adapter: {str(e)}")
    
    def _create_adapter(
        self,
        platform: str,
        config: Dict[str, Any]
    ) -> Optional[PlatformAdapter]:
        """Create platform adapter instance."""
        adapter_map: Dict[str, Type[PlatformAdapter]] = {
            'TWITTER': TwitterAdapter,
            'WIX': WixAdapter,
            # Add other platform adapters here
        }
        
        adapter_class = adapter_map.get(platform.upper())
        if not adapter_class:
            logger.warning(f"Unsupported platform: {platform}")
            return None
        
        try:
            return adapter_class(config)
        except Exception as e:
            raise Exception(
                f"Failed to create {platform} adapter: {str(e)}"
            )
    
    async def publish_content(
        self,
        content: Dict[str, Any],
        platforms: List[str],
        schedule_time: Optional[datetime] = None
    ) -> Dict[str, Dict[str, Any]]:
        """Publish content to multiple platforms."""
        results = {}
        
        for platform in platforms:
            if platform not in self.adapters:
                results[platform] = {
                    'success': False,
                    'error': f"Platform adapter not found: {platform}"
                }
                continue
            
            try:
                result = await self.adapters[platform].publish_content(
                    content,
                    schedule_time
                )
                results[platform] = result
            except Exception as e:
                results[platform] = {
                    'success': False,
                    'error': str(e)
                }
        
        return results
    
    async def get_content_status(
        self,
        content_id: str,
        platform: str
    ) -> Dict[str, Any]:
        """Get content status from a specific platform."""
        if platform not in self.adapters:
            return {
                'success': False,
                'error': f"Platform adapter not found: {platform}"
            }
        
        try:
            return await self.adapters[platform].get_content_status(content_id)
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def delete_content(
        self,
        content_id: str,
        platform: str
    ) -> Dict[str, Any]:
        """Delete content from a specific platform."""
        if platform not in self.adapters:
            return {
                'success': False,
                'error': f"Platform adapter not found: {platform}"
            }
        
        try:
            return await self.adapters[platform].delete_content(content_id)
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def update_content(
        self,
        content_id: str,
        updates: Dict[str, Any],
        platform: str
    ) -> Dict[str, Any]:
        """Update content on a specific platform."""
        if platform not in self.adapters:
            return {
                'success': False,
                'error': f"Platform adapter not found: {platform}"
            }
        
        try:
            return await self.adapters[platform].update_content(
                content_id,
                updates
            )
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_analytics(
        self,
        content_id: str,
        platform: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get analytics from a specific platform."""
        if platform not in self.adapters:
            return {
                'success': False,
                'error': f"Platform adapter not found: {platform}"
            }
        
        try:
            return await self.adapters[platform].get_analytics(
                content_id,
                start_date,
                end_date
            )
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def validate_content(
        self,
        content: Dict[str, Any],
        platform: str
    ) -> Dict[str, Any]:
        """Validate content for a specific platform."""
        if platform not in self.adapters:
            return {
                'success': False,
                'error': f"Platform adapter not found: {platform}"
            }
        
        try:
            return await self.adapters[platform].validate_content(content)
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_optimal_publish_time(
        self,
        content_type: str,
        platform: str,
        target_audience: Optional[Dict[str, Any]] = None
    ) -> datetime:
        """Get optimal publish time for a specific platform."""
        if platform not in self.adapters:
            raise Exception(f"Platform adapter not found: {platform}")
        
        return await self.adapters[platform].get_optimal_publish_time(
            content_type,
            target_audience
        )
    
    async def get_platform_limits(
        self,
        platform: str
    ) -> Dict[str, Any]:
        """Get platform limits for a specific platform."""
        if platform not in self.adapters:
            return {
                'success': False,
                'error': f"Platform adapter not found: {platform}"
            }
        
        try:
            return await self.adapters[platform].get_platform_limits()
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_supported_content_types(
        self,
        platform: str
    ) -> List[str]:
        """Get supported content types for a specific platform."""
        if platform not in self.adapters:
            raise Exception(f"Platform adapter not found: {platform}")
        
        return await self.adapters[platform].get_supported_content_types()
    
    async def get_platform_metrics(
        self,
        platform: str
    ) -> Dict[str, Any]:
        """Get platform metrics for a specific platform."""
        if platform not in self.adapters:
            return {
                'success': False,
                'error': f"Platform adapter not found: {platform}"
            }
        
        try:
            return await self.adapters[platform].get_platform_metrics()
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_available_platforms(self) -> List[str]:
        """Get list of available platform adapters."""
        return list(self.adapters.keys())
    
    def get_platform_info(self, platform: str) -> Dict[str, Any]:
        """Get information about a specific platform."""
        if platform not in self.adapters:
            return {
                'success': False,
                'error': f"Platform adapter not found: {platform}"
            }
        
        adapter = self.adapters[platform]
        return {
            'success': True,
            'name': adapter.get_platform_name(),
            'description': adapter.get_platform_description(),
            'version': adapter.get_platform_version(),
            'required_config': adapter.get_required_config_fields()
        } 