"""
Base platform adapter class.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime

class PlatformAdapter(ABC):
    """Base class for platform-specific adapters."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize platform adapter with configuration."""
        self.config = config
        self.platform_name = self.__class__.__name__.replace('Adapter', '').upper()
    
    @abstractmethod
    async def publish_content(
        self,
        content: Dict[str, Any],
        schedule_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Publish content to the platform."""
        pass
    
    @abstractmethod
    async def get_content_status(
        self,
        content_id: str
    ) -> Dict[str, Any]:
        """Get the status of published content."""
        pass
    
    @abstractmethod
    async def delete_content(
        self,
        content_id: str
    ) -> Dict[str, Any]:
        """Delete published content."""
        pass
    
    @abstractmethod
    async def update_content(
        self,
        content_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update published content."""
        pass
    
    @abstractmethod
    async def get_analytics(
        self,
        content_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get analytics for published content."""
        pass
    
    @abstractmethod
    async def validate_content(
        self,
        content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate content before publishing."""
        pass
    
    @abstractmethod
    async def get_optimal_publish_time(
        self,
        content_type: str,
        target_audience: Optional[Dict[str, Any]] = None
    ) -> datetime:
        """Get optimal publish time for content."""
        pass
    
    @abstractmethod
    async def get_platform_limits(
        self
    ) -> Dict[str, Any]:
        """Get platform-specific limits and constraints."""
        pass
    
    @abstractmethod
    async def get_supported_content_types(
        self
    ) -> List[str]:
        """Get list of supported content types."""
        pass
    
    @abstractmethod
    async def get_platform_metrics(
        self
    ) -> Dict[str, Any]:
        """Get platform-specific metrics and statistics."""
        pass
    
    def _format_error_response(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Format error response."""
        return {
            'success': False,
            'platform': self.platform_name,
            'error': str(error),
            'error_type': error.__class__.__name__,
            'context': context or {}
        }
    
    def _format_success_response(
        self,
        data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Format success response."""
        return {
            'success': True,
            'platform': self.platform_name,
            'data': data,
            'context': context or {}
        }
    
    def _validate_config(self) -> None:
        """Validate platform configuration."""
        required_fields = self.get_required_config_fields()
        missing_fields = [
            field for field in required_fields
            if field not in self.config
        ]
        
        if missing_fields:
            raise ValueError(
                f"Missing required configuration fields: {', '.join(missing_fields)}"
            )
    
    @classmethod
    def get_required_config_fields(cls) -> List[str]:
        """Get list of required configuration fields."""
        return []
    
    @classmethod
    def get_platform_name(cls) -> str:
        """Get platform name."""
        return cls.__name__.replace('Adapter', '').upper()
    
    @classmethod
    def get_platform_description(cls) -> str:
        """Get platform description."""
        return "Base platform adapter"
    
    @classmethod
    def get_platform_version(cls) -> str:
        """Get platform adapter version."""
        return "1.0.0" 