"""
Mem0 Service Integration for ALwrity
Handles storing and retrieving content strategy as memory with intelligent categorization
"""

import os
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from loguru import logger
from mem0 import Memory

class Mem0Service:
    """Service for integrating with mem0 AI memory platform with intelligent categorization"""
    
    # Intelligent categories for different user types
    CONTENT_CREATOR_CATEGORIES = [
        "creative_strategy", "content_pillars", "audience_engagement", 
        "brand_voice", "content_formats", "seasonal_content"
    ]
    
    DIGITAL_MARKETER_CATEGORIES = [
        "marketing_strategy", "conversion_optimization", "competitive_analysis",
        "performance_metrics", "roi_tracking", "campaign_strategy"
    ]
    
    INDUSTRY_CATEGORIES = [
        "technology", "healthcare", "finance", "retail", "education", 
        "manufacturing", "services", "nonprofit", "entertainment"
    ]
    
    def __init__(self):
        """Initialize mem0 service with API configuration"""
        self.api_key = os.getenv("MEM0_API_KEY")
        if not self.api_key:
            logger.warning("MEM0_API_KEY not found in environment variables. Mem0 functionality will be disabled.")
            self.memory = None
        else:
            try:
                # Initialize mem0 client with advanced configuration
                config = {
                    "vector_store": {
                        "provider": "qdrant",
                        "config": {
                            "collection_name": "alwrity_strategies",
                            "embedding_model_dims": 1536,
                        }
                    }
                }
                self.memory = Memory.from_config(config)
                logger.info("Mem0 service initialized successfully with intelligent categorization")
            except Exception as e:
                logger.error(f"Failed to initialize mem0 service: {e}")
                self.memory = None
    
    def is_available(self) -> bool:
        """Check if mem0 service is available"""
        return self.memory is not None
    
    def _determine_user_type(self, strategy_data: Dict[str, Any]) -> str:
        """Determine user type based on strategy data for intelligent categorization"""
        if not strategy_data or not isinstance(strategy_data, dict):
            return "content_creator"  # Safe default
        
        try:
            # Check for digital marketer indicators
            if any(key in strategy_data for key in ['conversion_rates', 'traffic_sources', 'content_roi_targets', 'performance_metrics']):
                return "digital_marketer"
            
            # Check for content creator indicators
            if any(key in strategy_data for key in ['brand_voice', 'editorial_guidelines', 'content_mix', 'preferred_formats']):
                return "content_creator"
            
            # Default to content creator
            return "content_creator"
        except Exception as e:
            logger.warning(f"Error determining user type: {e}, defaulting to content_creator")
            return "content_creator"
    
    def _categorize_strategy(self, strategy_data: Dict[str, Any], user_type: str) -> List[str]:
        """Intelligently categorize strategy based on content and user type"""
        if not strategy_data or not isinstance(strategy_data, dict):
            return ["general"]  # Safe default
        
        try:
            categories = []
            
            # Add industry category
            industry = str(strategy_data.get('industry', '')).lower().strip()
            if industry in self.INDUSTRY_CATEGORIES:
                categories.append(industry)
            elif industry:
                categories.append("other_industry")
            
            # Add user-type specific categories
            if user_type == "digital_marketer":
                if strategy_data.get('top_competitors') or strategy_data.get('competitor_content_strategies'):
                    categories.append("competitive_analysis")
                if strategy_data.get('conversion_rates') or strategy_data.get('content_roi_targets'):
                    categories.append("conversion_optimization")
                if strategy_data.get('performance_metrics') or strategy_data.get('traffic_sources'):
                    categories.append("performance_metrics")
                categories.append("marketing_strategy")
            else:  # content_creator
                if strategy_data.get('content_pillars'):
                    categories.append("content_pillars")
                if strategy_data.get('brand_voice') or strategy_data.get('editorial_guidelines'):
                    categories.append("brand_voice")
                if strategy_data.get('preferred_formats') or strategy_data.get('content_mix'):
                    categories.append("content_formats")
                categories.append("creative_strategy")
            
            # Add seasonal category if seasonal trends exist
            if strategy_data.get('seasonal_trends'):
                categories.append("seasonal_content")
            
            # Ensure we always have at least one category
            if not categories:
                categories = ["general"]
            
            return categories
        except Exception as e:
            logger.warning(f"Error categorizing strategy: {e}, returning default category")
            return ["general"]

    async def store_content_strategy(self, 
                                   strategy_data: Dict[str, Any], 
                                   user_id: int, 
                                   strategy_id: int) -> bool:
        """
        Store content strategy as memory in mem0 with intelligent categorization
        
        Args:
            strategy_data: The complete strategy data to store
            user_id: User ID for memory association
            strategy_id: Strategy ID for reference
            
        Returns:
            bool: Success status
        """
        if not self.is_available():
            logger.warning("Mem0 service not available, skipping memory storage")
            return False
        
        try:
            # Determine user type and categories
            user_type = self._determine_user_type(strategy_data)
            categories = self._categorize_strategy(strategy_data, user_type)
            
            # Prepare memory content with structured information
            memory_content = self._prepare_strategy_memory_content(strategy_data, strategy_id)
            
            # Enhanced metadata for advanced search operations
            metadata = {
                "type": "content_strategy",
                "strategy_id": strategy_id,
                "activation_date": datetime.utcnow().isoformat(),
                "source": "alwrity_strategy_activation",
                "user_type": user_type,
                "categories": categories,
                "industry": strategy_data.get('industry', 'general'),
                "strategy_name": strategy_data.get('name', f'Strategy {strategy_id}'),
                "has_competitors": bool(strategy_data.get('top_competitors')),
                "has_metrics": bool(strategy_data.get('performance_metrics')),
                "content_pillar_count": len(strategy_data.get('content_pillars', [])),
                "target_audience_defined": bool(strategy_data.get('target_audience'))
            }
            
            # Store in mem0 with advanced configuration
            result = self.memory.add(
                messages=[{"role": "user", "content": memory_content}],
                user_id=str(user_id),
                metadata=metadata,
                filters={
                    "categories": {"in": categories},
                    "user_type": user_type,
                    "industry": strategy_data.get('industry', 'general')
                }
            )
            
            if result:
                logger.info(f"Successfully stored content strategy {strategy_id} in mem0 for user {user_id} with categories: {categories}")
                return True
            else:
                logger.error(f"Failed to store content strategy {strategy_id} in mem0")
                return False
                
        except Exception as e:
            logger.error(f"Error storing content strategy in mem0: {e}")
            return False
    
    def _prepare_strategy_memory_content(self, strategy_data: Dict[str, Any], strategy_id: int) -> str:
        """
        Prepare strategy data for memory storage in a readable format
        
        Args:
            strategy_data: Raw strategy data from database model
            strategy_id: Strategy ID
            
        Returns:
            str: Formatted memory content
        """
        try:
            # Extract key strategy components using correct field names from database model
            # Handle both legacy field names and new database model field names
            business_goals = strategy_data.get('business_objectives', strategy_data.get('business_goals', []))
            target_audience = strategy_data.get('target_audience', {})
            content_pillars = strategy_data.get('content_pillars', [])
            top_competitors = strategy_data.get('top_competitors', [])
            competitive_analysis = strategy_data.get('competitor_content_strategies', strategy_data.get('competitive_analysis', {}))
            
            # Build structured memory content with enhanced categorization
            strategy_name = strategy_data.get('name', f'Strategy {strategy_id}')
            industry = strategy_data.get('industry', 'General')
            
            memory_parts = [
                f"Content Strategy: {strategy_name} (ID: {strategy_id})",
                f"Industry: {industry}",
                f"Activated: {datetime.utcnow().strftime('%Y-%m-%d')}",
                "",
                "BUSINESS OBJECTIVES:"
            ]
            
            # Add business goals/objectives
            if isinstance(business_goals, list):
                for i, goal in enumerate(business_goals[:5], 1):  # Limit to top 5 goals
                    if isinstance(goal, dict):
                        goal_text = goal.get('description', goal.get('objective', str(goal)))
                    else:
                        goal_text = str(goal)
                    memory_parts.append(f"{i}. {goal_text}")
            elif business_goals:
                memory_parts.append(f"1. {str(business_goals)}")
            
            memory_parts.append("\nTARGET AUDIENCE:")
            # Handle target_audience as object (not array)
            if isinstance(target_audience, dict):
                demographics = target_audience.get('demographics', '')
                if demographics:
                    memory_parts.append(f"Demographics: {demographics}")
                
                age_range = target_audience.get('age_range', '')
                if age_range:
                    memory_parts.append(f"Age Range: {age_range}")
                
                interests = target_audience.get('interests', [])
                if interests:
                    if isinstance(interests, list):
                        memory_parts.append(f"Interests: {', '.join(interests[:5])}")
                    else:
                        memory_parts.append(f"Interests: {interests}")
                
                # Handle additional audience fields from database model
                consumption_patterns = strategy_data.get('consumption_patterns', {})
                if consumption_patterns:
                    memory_parts.append(f"Content Consumption: {consumption_patterns}")
                
            elif target_audience:
                memory_parts.append(f"Target Audience: {str(target_audience)}")
            
            memory_parts.append("\nCONTENT STRATEGY:")
            # Add content pillars
            if content_pillars:
                memory_parts.append("Content Pillars:")
                for i, pillar in enumerate(content_pillars[:5], 1):  # Limit to top 5 pillars
                    if isinstance(pillar, dict):
                        pillar_text = pillar.get('title', pillar.get('name', str(pillar)))
                    else:
                        pillar_text = str(pillar)
                    memory_parts.append(f"  {i}. {pillar_text}")
            
            # Add content preferences and formats
            preferred_formats = strategy_data.get('preferred_formats', [])
            if preferred_formats:
                memory_parts.append(f"Preferred Formats: {', '.join(preferred_formats[:5])}")
            
            content_frequency = strategy_data.get('content_frequency')
            if content_frequency:
                memory_parts.append(f"Publishing Frequency: {content_frequency}")
            
            # Add brand voice if available
            brand_voice = strategy_data.get('brand_voice', {})
            if brand_voice:
                memory_parts.append(f"Brand Voice: {brand_voice}")
            
            # Add competitive analysis
            if top_competitors or competitive_analysis:
                memory_parts.append("\nCOMPETITIVE LANDSCAPE:")
                
                # Handle top_competitors list
                if top_competitors:
                    memory_parts.append("Key Competitors:")
                    for i, competitor in enumerate(top_competitors[:3], 1):  # Top 3 competitors
                        if isinstance(competitor, dict):
                            comp_name = competitor.get('name', competitor.get('domain', f'Competitor {i}'))
                            memory_parts.append(f"  {i}. {comp_name}")
                        else:
                            memory_parts.append(f"  {i}. {str(competitor)}")
                
                # Handle competitive analysis data
                if competitive_analysis:
                    memory_parts.append("Competitive Insights:")
                    if isinstance(competitive_analysis, dict):
                        for key, value in list(competitive_analysis.items())[:3]:
                            memory_parts.append(f"  - {key}: {value}")
                    else:
                        memory_parts.append(f"  - {str(competitive_analysis)}")
            
            # Add performance metrics if available
            performance_metrics = strategy_data.get('performance_metrics', {})
            if performance_metrics:
                memory_parts.append("\nPERFORMANCE TARGETS:")
                if isinstance(performance_metrics, dict):
                    for metric, value in list(performance_metrics.items())[:3]:
                        memory_parts.append(f"  - {metric}: {value}")
            
            # Add market positioning
            market_positioning = strategy_data.get('market_positioning', {})
            if market_positioning:
                memory_parts.append(f"\nMarket Position: {market_positioning}")
            
            return "\n".join(memory_parts)
            
        except Exception as e:
            logger.error(f"Error preparing strategy memory content: {e}")
            # Fallback to basic JSON representation
            return f"Content Strategy #{strategy_id}: {json.dumps(strategy_data, indent=2)[:1000]}..."
    
    async def retrieve_strategy_memories(self, 
                                       user_id: int, 
                                       query: Optional[str] = None,
                                       user_type: Optional[str] = None,
                                       industry: Optional[str] = None,
                                       categories: Optional[List[str]] = None,
                                       limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve content strategy memories with advanced filtering
        
        Args:
            user_id: User ID to retrieve memories for
            query: Optional search query
            user_type: Filter by user type (content_creator, digital_marketer)
            industry: Filter by industry
            categories: Filter by specific categories
            limit: Maximum number of results
            
        Returns:
            List of memory objects
        """
        if not self.is_available():
            logger.warning("Mem0 service not available")
            return []
        
        try:
            # Build advanced filters
            filters = {
                "AND": [
                    {"metadata.type": "content_strategy"}
                ]
            }
            
            if user_type:
                filters["AND"].append({"metadata.user_type": user_type})
            
            if industry:
                filters["AND"].append({"metadata.industry": industry})
            
            if categories:
                filters["AND"].append({"metadata.categories": {"in": categories}})
            
            if query:
                # Advanced search with filters
                results = self.memory.search(
                    query=query,
                    user_id=str(user_id),
                    filters=filters,
                    limit=limit
                )
            else:
                # Get all strategy memories with filters
                results = self.memory.get_all(
                    user_id=str(user_id),
                    filters=filters,
                    limit=limit
                )
            
            # Ensure we only return strategy memories
            strategy_memories = []
            for memory in results:
                metadata = memory.get('metadata', {})
                if metadata.get('type') == 'content_strategy':
                    strategy_memories.append(memory)
            
            logger.info(f"Retrieved {len(strategy_memories)} strategy memories for user {user_id} with filters: user_type={user_type}, industry={industry}, categories={categories}")
            return strategy_memories
            
        except Exception as e:
            logger.error(f"Error retrieving strategy memories: {e}")
            return []
    
    async def search_strategies_by_category(self, 
                                          user_id: int, 
                                          category: str, 
                                          limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search strategies by specific category for content creators and digital marketers
        
        Args:
            user_id: User ID
            category: Category to search for
            limit: Maximum results
            
        Returns:
            List of matching strategies
        """
        return await self.retrieve_strategy_memories(
            user_id=user_id,
            categories=[category],
            limit=limit
        )
    
    async def get_user_type_strategies(self, 
                                     user_id: int, 
                                     user_type: str, 
                                     limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get strategies filtered by user type (content_creator or digital_marketer)
        
        Args:
            user_id: User ID
            user_type: Type of user (content_creator, digital_marketer)
            limit: Maximum results
            
        Returns:
            List of strategies for the user type
        """
        return await self.retrieve_strategy_memories(
            user_id=user_id,
            user_type=user_type,
            limit=limit
        )
    
    async def get_industry_strategies(self, 
                                    user_id: int, 
                                    industry: str, 
                                    limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get strategies filtered by industry
        
        Args:
            user_id: User ID
            industry: Industry to filter by
            limit: Maximum results
            
        Returns:
            List of industry-specific strategies
        """
        return await self.retrieve_strategy_memories(
            user_id=user_id,
            industry=industry,
            limit=limit
        )
    
    async def delete_strategy_memory(self, user_id: int, strategy_id: int) -> bool:
        """
        Delete a specific strategy memory
        
        Args:
            user_id: User ID
            strategy_id: Strategy ID to delete
            
        Returns:
            bool: Success status
        """
        if not self.is_available():
            logger.warning("Mem0 service not available")
            return False
        
        try:
            # Get all memories and find the one matching the strategy_id
            memories = await self.retrieve_strategy_memories(user_id)
            
            for memory in memories:
                metadata = memory.get('metadata', {})
                if metadata.get('strategy_id') == strategy_id:
                    memory_id = memory.get('id')
                    if memory_id:
                        self.memory.delete(memory_id)
                        logger.info(f"Deleted strategy memory {strategy_id} for user {user_id}")
                        return True
            
            logger.warning(f"Strategy memory {strategy_id} not found for user {user_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error deleting strategy memory: {e}")
            return False
    
    async def update_strategy_memory(self, 
                                   user_id: int, 
                                   strategy_id: int, 
                                   updated_strategy_data: Dict[str, Any]) -> bool:
        """
        Update an existing strategy memory
        
        Args:
            user_id: User ID
            strategy_id: Strategy ID to update
            updated_strategy_data: New strategy data
            
        Returns:
            bool: Success status
        """
        if not self.is_available():
            logger.warning("Mem0 service not available")
            return False
        
        try:
            # Delete old memory and create new one
            await self.delete_strategy_memory(user_id, strategy_id)
            return await self.store_content_strategy(updated_strategy_data, user_id, strategy_id)
            
        except Exception as e:
            logger.error(f"Error updating strategy memory: {e}")
            return False
    
    async def get_memory_statistics(self, user_id: int) -> Dict[str, Any]:
        """
        Get comprehensive memory statistics for user dashboard
        
        Args:
            user_id: User ID
            
        Returns:
            Dict containing memory statistics
        """
        if not self.is_available():
            return {
                "total_memories": 0,
                "categories": {},
                "user_types": {},
                "industries": {},
                "recent_memories": 0,
                "api_calls_today": 0,
                "available": False
            }
        
        try:
            # Get all user memories
            all_memories = await self.retrieve_strategy_memories(user_id=user_id, limit=1000)
            
            stats = {
                "total_memories": len(all_memories),
                "categories": {},
                "user_types": {},
                "industries": {},
                "recent_memories": 0,
                "api_calls_today": 0,  # This would need to be tracked separately
                "available": True,
                "last_updated": datetime.utcnow().isoformat()
            }
            
            # Analyze memories
            for memory in all_memories:
                metadata = memory.get('metadata', {})
                
                # Count categories
                categories = metadata.get('categories', [])
                for category in categories:
                    stats["categories"][category] = stats["categories"].get(category, 0) + 1
                
                # Count user types
                user_type = metadata.get('user_type', 'unknown')
                stats["user_types"][user_type] = stats["user_types"].get(user_type, 0) + 1
                
                # Count industries
                industry = metadata.get('industry', 'unknown')
                stats["industries"][industry] = stats["industries"].get(industry, 0) + 1
                
                # Count recent memories (last 7 days)
                activation_date = metadata.get('activation_date')
                if activation_date:
                    try:
                        from datetime import datetime, timedelta
                        memory_date = datetime.fromisoformat(activation_date.replace('Z', '+00:00'))
                        if memory_date > datetime.now() - timedelta(days=7):
                            stats["recent_memories"] += 1
                    except:
                        pass
            
            logger.info(f"Retrieved memory statistics for user {user_id}: {stats['total_memories']} memories")
            return stats
            
        except Exception as e:
            logger.error(f"Error getting memory statistics: {e}")
            return {
                "total_memories": 0,
                "categories": {},
                "user_types": {},
                "industries": {},
                "recent_memories": 0,
                "api_calls_today": 0,
                "available": False,
                "error": str(e)
            }
    
    async def search_memories_with_query(self, user_id: int, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search memories using natural language query for chat interface
        
        Args:
            user_id: User ID
            query: Natural language search query
            limit: Maximum results
            
        Returns:
            List of relevant memories
        """
        if not self.is_available():
            logger.warning("Mem0 service not available for search")
            return []
        
        try:
            results = await self.retrieve_strategy_memories(
                user_id=user_id,
                query=query,
                limit=limit
            )
            
            # Enhance results with formatted content for chat
            enhanced_results = []
            for result in results:
                metadata = result.get('metadata', {})
                enhanced_result = {
                    "id": result.get('id'),
                    "strategy_name": metadata.get('strategy_name', 'Unknown Strategy'),
                    "strategy_id": metadata.get('strategy_id'),
                    "industry": metadata.get('industry', 'General'),
                    "user_type": metadata.get('user_type', 'unknown'),
                    "categories": metadata.get('categories', []),
                    "activation_date": metadata.get('activation_date'),
                    "content": result.get('content', ''),
                    "relevance_score": result.get('score', 0)
                }
                enhanced_results.append(enhanced_result)
            
            logger.info(f"Found {len(enhanced_results)} memories for query: {query}")
            return enhanced_results
            
        except Exception as e:
            logger.error(f"Error searching memories with query '{query}': {e}")
            return []