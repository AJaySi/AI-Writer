"""
Data Source Registry for Calendar Generation Framework

Central registry for managing all data sources with dependency management,
validation, and monitoring capabilities.
"""

import logging
from typing import Dict, Any, Optional, List, Set
from datetime import datetime

from .interfaces import DataSourceInterface, DataSourceValidationResult

logger = logging.getLogger(__name__)


class DataSourceRegistry:
    """
    Central registry for managing all data sources in the calendar generation system.
    
    Provides centralized management, dependency handling, validation, and monitoring
    for all registered data sources.
    """
    
    def __init__(self):
        """Initialize the data source registry."""
        self._sources: Dict[str, DataSourceInterface] = {}
        self._source_configs: Dict[str, Dict[str, Any]] = {}
        self._dependencies: Dict[str, List[str]] = {}
        self._reverse_dependencies: Dict[str, Set[str]] = {}
        self._registry_metadata: Dict[str, Any] = {
            "created_at": datetime.utcnow(),
            "total_sources": 0,
            "active_sources": 0,
            "last_updated": None
        }
        
        logger.info("Initialized DataSourceRegistry")
    
    def register_source(self, source: DataSourceInterface, config: Dict[str, Any] = None) -> bool:
        """
        Register a new data source.
        
        Args:
            source: Data source to register
            config: Optional configuration for the source
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            if source.source_id in self._sources:
                logger.warning(f"Data source already registered: {source.source_id}")
                return False
            
            self._sources[source.source_id] = source
            self._source_configs[source.source_id] = config or {}
            self._reverse_dependencies[source.source_id] = set()
            
            self._registry_metadata["total_sources"] += 1
            if source.is_active:
                self._registry_metadata["active_sources"] += 1
            
            self._update_registry_metadata()
            
            logger.info(f"✅ Registered data source: {source.source_id} ({source.source_type.value})")
            return True
            
        except Exception as e:
            logger.error(f"Error registering data source {source.source_id}: {e}")
            return False
    
    def unregister_source(self, source_id: str) -> bool:
        """
        Unregister a data source.
        
        Args:
            source_id: ID of the source to unregister
            
        Returns:
            True if unregistration successful, False otherwise
        """
        try:
            if source_id not in self._sources:
                logger.warning(f"Data source not found for unregistration: {source_id}")
                return False
            
            # Remove from main sources
            source = self._sources.pop(source_id)
            
            # Update metadata
            self._registry_metadata["total_sources"] -= 1
            if source.is_active:
                self._registry_metadata["active_sources"] -= 1
            
            # Remove from configurations
            self._source_configs.pop(source_id, None)
            
            # Remove dependencies
            self._dependencies.pop(source_id, None)
            self._reverse_dependencies.pop(source_id, None)
            
            # Remove from reverse dependencies
            for dep_id in list(self._reverse_dependencies.keys()):
                self._reverse_dependencies[dep_id].discard(source_id)
            
            self._update_registry_metadata()
            
            logger.info(f"❌ Unregistered data source: {source_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error unregistering data source {source_id}: {e}")
            return False
    
    def get_source(self, source_id: str) -> Optional[DataSourceInterface]:
        """
        Get a specific data source.
        
        Args:
            source_id: ID of the source to retrieve
            
        Returns:
            Data source if found, None otherwise
        """
        return self._sources.get(source_id)
    
    def get_all_sources(self) -> Dict[str, DataSourceInterface]:
        """
        Get all registered data sources.
        
        Returns:
            Dictionary of all registered sources
        """
        return self._sources.copy()
    
    def get_active_sources(self) -> Dict[str, DataSourceInterface]:
        """
        Get all active data sources.
        
        Returns:
            Dictionary of active sources only
        """
        return {k: v for k, v in self._sources.items() if v.is_active}
    
    def get_sources_by_type(self, source_type: str) -> Dict[str, DataSourceInterface]:
        """
        Get all sources of a specific type.
        
        Args:
            source_type: Type of sources to retrieve
            
        Returns:
            Dictionary of sources of the specified type
        """
        return {k: v for k, v in self._sources.items() if v.source_type.value == source_type}
    
    def get_sources_by_priority(self, priority: int) -> Dict[str, DataSourceInterface]:
        """
        Get all sources with a specific priority.
        
        Args:
            priority: Priority level to filter by
            
        Returns:
            Dictionary of sources with the specified priority
        """
        return {k: v for k, v in self._sources.items() if v.priority.value == priority}
    
    def set_dependencies(self, source_id: str, dependencies: List[str]) -> bool:
        """
        Set dependencies for a data source.
        
        Args:
            source_id: ID of the source
            dependencies: List of dependency source IDs
            
        Returns:
            True if dependencies set successfully, False otherwise
        """
        try:
            if source_id not in self._sources:
                logger.error(f"Data source not found for dependency setting: {source_id}")
                return False
            
            # Validate dependencies exist
            for dep_id in dependencies:
                if dep_id not in self._sources:
                    logger.error(f"Dependency not found: {dep_id}")
                    return False
            
            # Set dependencies
            self._dependencies[source_id] = dependencies.copy()
            
            # Update reverse dependencies
            for dep_id in dependencies:
                if dep_id not in self._reverse_dependencies:
                    self._reverse_dependencies[dep_id] = set()
                self._reverse_dependencies[dep_id].add(source_id)
            
            logger.info(f"Set dependencies for {source_id}: {dependencies}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting dependencies for {source_id}: {e}")
            return False
    
    def get_dependencies(self, source_id: str) -> List[str]:
        """
        Get dependencies for a data source.
        
        Args:
            source_id: ID of the source
            
        Returns:
            List of dependency source IDs
        """
        return self._dependencies.get(source_id, [])
    
    def get_dependents(self, source_id: str) -> List[str]:
        """
        Get sources that depend on this source.
        
        Args:
            source_id: ID of the source
            
        Returns:
            List of dependent source IDs
        """
        return list(self._reverse_dependencies.get(source_id, set()))
    
    async def get_data_with_dependencies(self, source_id: str, user_id: int, strategy_id: int) -> Dict[str, Any]:
        """
        Get data from a source and its dependencies.
        
        Args:
            source_id: ID of the source
            user_id: User identifier
            strategy_id: Strategy identifier
            
        Returns:
            Dictionary containing source data and dependencies
        """
        source = self.get_source(source_id)
        if not source:
            raise ValueError(f"Data source not found: {source_id}")
        
        try:
            # Get dependency data first
            dependency_data = {}
            for dep_id in self._dependencies.get(source_id, []):
                dep_source = self.get_source(dep_id)
                if dep_source and dep_source.is_active:
                    try:
                        dep_data = await dep_source.get_data(user_id, strategy_id)
                        dependency_data[dep_id] = dep_data
                        logger.debug(f"Retrieved dependency data from {dep_id}")
                    except Exception as e:
                        logger.warning(f"Error getting dependency data from {dep_id}: {e}")
                        dependency_data[dep_id] = {}
            
            # Get main source data
            main_data = await source.get_data(user_id, strategy_id)
            
            # Enhance with dependencies
            enhanced_data = await source.enhance_data(main_data)
            enhanced_data["dependencies"] = dependency_data
            enhanced_data["source_metadata"] = source.get_metadata()
            
            logger.info(f"Retrieved data with dependencies from {source_id}")
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error getting data with dependencies from {source_id}: {e}")
            raise
    
    async def validate_all_sources(self) -> Dict[str, DataSourceValidationResult]:
        """
        Validate all registered data sources.
        
        Returns:
            Dictionary of validation results for all sources
        """
        validation_results = {}
        
        for source_id, source in self._sources.items():
            try:
                # Get sample data for validation
                sample_data = await source.get_data(1, 1)  # Use sample IDs
                validation_result = await source.validate_data(sample_data)
                
                # Convert to DataSourceValidationResult if needed
                if isinstance(validation_result, dict):
                    result = DataSourceValidationResult(
                        is_valid=validation_result.get("is_valid", True),
                        quality_score=validation_result.get("quality_score", 0.0)
                    )
                    result.missing_fields = validation_result.get("missing_fields", [])
                    result.recommendations = validation_result.get("recommendations", [])
                    result.warnings = validation_result.get("warnings", [])
                    result.errors = validation_result.get("errors", [])
                    validation_results[source_id] = result
                else:
                    validation_results[source_id] = validation_result
                
                # Update source quality score
                source.update_quality_score(validation_results[source_id].quality_score)
                
            except Exception as e:
                logger.error(f"Error validating source {source_id}: {e}")
                result = DataSourceValidationResult(is_valid=False, quality_score=0.0)
                result.add_error(f"Validation failed: {str(e)}")
                validation_results[source_id] = result
        
        return validation_results
    
    def get_registry_status(self) -> Dict[str, Any]:
        """
        Get comprehensive registry status.
        
        Returns:
            Dictionary containing registry status information
        """
        active_sources = self.get_active_sources()
        
        status = {
            "registry_metadata": self._registry_metadata.copy(),
            "total_sources": len(self._sources),
            "active_sources": len(active_sources),
            "source_types": {},
            "priority_distribution": {},
            "dependency_graph": self._dependencies.copy(),
            "source_metadata": {}
        }
        
        # Count by type
        for source in self._sources.values():
            source_type = source.source_type.value
            status["source_types"][source_type] = status["source_types"].get(source_type, 0) + 1
        
        # Count by priority
        for source in self._sources.values():
            priority = source.priority.value
            status["priority_distribution"][priority] = status["priority_distribution"].get(priority, 0) + 1
        
        # Get metadata for all sources
        for source_id, source in self._sources.items():
            status["source_metadata"][source_id] = source.get_metadata()
        
        return status
    
    def _update_registry_metadata(self) -> None:
        """Update registry metadata."""
        self._registry_metadata["last_updated"] = datetime.utcnow()
        self._registry_metadata["total_sources"] = len(self._sources)
        self._registry_metadata["active_sources"] = len(self.get_active_sources())
    
    def __str__(self) -> str:
        """String representation of the registry."""
        return f"DataSourceRegistry(total={len(self._sources)}, active={len(self.get_active_sources())})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the registry."""
        return f"DataSourceRegistry(sources={list(self._sources.keys())}, active={list(self.get_active_sources().keys())})"
