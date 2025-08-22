"""
Core Interfaces for Calendar Generation Data Source Framework

Defines the abstract interfaces and base classes for all data sources
in the calendar generation system.
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)


class DataSourceType(Enum):
    """Enumeration of data source types."""
    STRATEGY = "strategy"
    ANALYSIS = "analysis"
    RESEARCH = "research"
    PERFORMANCE = "performance"
    AI = "ai"
    CUSTOM = "custom"


class DataSourcePriority(Enum):
    """Enumeration of data source priorities."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    OPTIONAL = 5


class DataSourceInterface(ABC):
    """
    Abstract interface for all data sources in the calendar generation system.
    
    This interface provides a standardized way to implement data sources
    that can be dynamically registered, validated, and enhanced with AI insights.
    """
    
    def __init__(self, source_id: str, source_type: DataSourceType, priority: DataSourcePriority = DataSourcePriority.MEDIUM):
        """
        Initialize a data source.
        
        Args:
            source_id: Unique identifier for the data source
            source_type: Type of data source (strategy, analysis, research, etc.)
            priority: Priority level for data source processing
        """
        self.source_id = source_id
        self.source_type = source_type
        self.priority = priority
        self.is_active = True
        self.last_updated: Optional[datetime] = None
        self.data_quality_score: float = 0.0
        self.version: str = "1.0.0"
        self.metadata: Dict[str, Any] = {}
        
        logger.info(f"Initialized data source: {source_id} ({source_type.value})")
    
    @abstractmethod
    async def get_data(self, user_id: int, strategy_id: int) -> Dict[str, Any]:
        """
        Retrieve data from this source.
        
        Args:
            user_id: User identifier
            strategy_id: Strategy identifier
            
        Returns:
            Dictionary containing the retrieved data
        """
        raise NotImplementedError
    
    @abstractmethod
    async def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and score data quality.
        
        Args:
            data: Data to validate
            
        Returns:
            Dictionary containing validation results and quality score
        """
        raise NotImplementedError
    
    @abstractmethod
    async def enhance_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance data with AI insights.
        
        Args:
            data: Original data to enhance
            
        Returns:
            Enhanced data with AI insights
        """
        raise NotImplementedError
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get source metadata for quality gates and monitoring.
        
        Returns:
            Dictionary containing source metadata
        """
        return {
            "source_id": self.source_id,
            "source_type": self.source_type.value,
            "priority": self.priority.value,
            "is_active": self.is_active,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "data_quality_score": self.data_quality_score,
            "version": self.version,
            "metadata": self.metadata
        }
    
    def update_metadata(self, key: str, value: Any) -> None:
        """
        Update source metadata.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value
        logger.debug(f"Updated metadata for {self.source_id}: {key} = {value}")
    
    def set_active(self, active: bool) -> None:
        """
        Set the active status of the data source.
        
        Args:
            active: Whether the source should be active
        """
        self.is_active = active
        logger.info(f"Set {self.source_id} active status to: {active}")
    
    def update_quality_score(self, score: float) -> None:
        """
        Update the data quality score.
        
        Args:
            score: New quality score (0.0 to 1.0)
        """
        if 0.0 <= score <= 1.0:
            self.data_quality_score = score
            logger.debug(f"Updated quality score for {self.source_id}: {score}")
        else:
            logger.warning(f"Invalid quality score for {self.source_id}: {score} (must be 0.0-1.0)")
    
    def mark_updated(self) -> None:
        """Mark the data source as recently updated."""
        self.last_updated = datetime.utcnow()
        logger.debug(f"Marked {self.source_id} as updated at {self.last_updated}")
    
    def __str__(self) -> str:
        """String representation of the data source."""
        return f"DataSource({self.source_id}, {self.source_type.value}, priority={self.priority.value})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the data source."""
        return f"DataSource(source_id='{self.source_id}', source_type={self.source_type}, priority={self.priority}, is_active={self.is_active}, quality_score={self.data_quality_score})"


class DataSourceValidationResult:
    """
    Standardized validation result for data sources.
    """
    
    def __init__(self, is_valid: bool = True, quality_score: float = 0.0):
        self.is_valid = is_valid
        self.quality_score = quality_score
        self.missing_fields: List[str] = []
        self.recommendations: List[str] = []
        self.warnings: List[str] = []
        self.errors: List[str] = []
        self.metadata: Dict[str, Any] = {}
    
    def add_missing_field(self, field: str) -> None:
        """Add a missing field to the validation result."""
        self.missing_fields.append(field)
        self.is_valid = False
    
    def add_recommendation(self, recommendation: str) -> None:
        """Add a recommendation to the validation result."""
        self.recommendations.append(recommendation)
    
    def add_warning(self, warning: str) -> None:
        """Add a warning to the validation result."""
        self.warnings.append(warning)
    
    def add_error(self, error: str) -> None:
        """Add an error to the validation result."""
        self.errors.append(error)
        self.is_valid = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert validation result to dictionary."""
        return {
            "is_valid": self.is_valid,
            "quality_score": self.quality_score,
            "missing_fields": self.missing_fields,
            "recommendations": self.recommendations,
            "warnings": self.warnings,
            "errors": self.errors,
            "metadata": self.metadata
        }
    
    def __str__(self) -> str:
        """String representation of validation result."""
        status = "VALID" if self.is_valid else "INVALID"
        return f"ValidationResult({status}, score={self.quality_score:.2f}, missing={len(self.missing_fields)}, errors={len(self.errors)})"
