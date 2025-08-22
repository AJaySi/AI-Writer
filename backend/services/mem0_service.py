"""
Mem0 Service Integration for ALwrity
Handles storing and retrieving content strategy as memory
"""

import os
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from loguru import logger
from mem0 import Memory

class Mem0Service:
    """Service for integrating with mem0 AI memory platform"""
    
    def __init__(self):
        """Initialize mem0 service with API configuration"""
        self.api_key = os.getenv("MEM0_API_KEY")
        if not self.api_key:
            logger.warning("MEM0_API_KEY not found in environment variables. Mem0 functionality will be disabled.")
            self.memory = None
        else:
            try:
                # Initialize mem0 client
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
                logger.info("Mem0 service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize mem0 service: {e}")
                self.memory = None
    
    def is_available(self) -> bool:
        """Check if mem0 service is available"""
        return self.memory is not None
    
    async def store_content_strategy(self, 
                                   strategy_data: Dict[str, Any], 
                                   user_id: int, 
                                   strategy_id: int) -> bool:
        """
        Store content strategy as memory in mem0
        
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
            # Prepare memory content with structured information
            memory_content = self._prepare_strategy_memory_content(strategy_data, strategy_id)
            
            # Store in mem0 with user association
            result = self.memory.add(
                messages=[{"role": "user", "content": memory_content}],
                user_id=str(user_id),
                metadata={
                    "type": "content_strategy",
                    "strategy_id": strategy_id,
                    "activation_date": datetime.utcnow().isoformat(),
                    "source": "alwrity_strategy_activation"
                }
            )
            
            if result:
                logger.info(f"Successfully stored content strategy {strategy_id} in mem0 for user {user_id}")
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
            strategy_data: Raw strategy data
            strategy_id: Strategy ID
            
        Returns:
            str: Formatted memory content
        """
        try:
            # Extract key strategy components
            goals = strategy_data.get('goals', [])
            audience_personas = strategy_data.get('audience_personas', [])
            content_pillars = strategy_data.get('content_pillars', [])
            keywords = strategy_data.get('keywords', {})
            competitive_analysis = strategy_data.get('competitive_analysis', {})
            
            # Build structured memory content
            memory_parts = [
                f"Content Strategy #{strategy_id} - Activated on {datetime.utcnow().strftime('%Y-%m-%d')}",
                "",
                "STRATEGIC GOALS:"
            ]
            
            # Add goals
            for i, goal in enumerate(goals[:5], 1):  # Limit to top 5 goals
                if isinstance(goal, dict):
                    goal_text = goal.get('description', str(goal))
                else:
                    goal_text = str(goal)
                memory_parts.append(f"{i}. {goal_text}")
            
            memory_parts.append("\nTARGET AUDIENCE:")
            # Add audience personas
            for i, persona in enumerate(audience_personas[:3], 1):  # Limit to top 3 personas
                if isinstance(persona, dict):
                    persona_name = persona.get('name', f'Persona {i}')
                    persona_desc = persona.get('description', persona.get('demographics', ''))
                    memory_parts.append(f"{i}. {persona_name}: {persona_desc}")
                else:
                    memory_parts.append(f"{i}. {str(persona)}")
            
            memory_parts.append("\nCONTENT PILLARS:")
            # Add content pillars
            for i, pillar in enumerate(content_pillars[:5], 1):  # Limit to top 5 pillars
                if isinstance(pillar, dict):
                    pillar_text = pillar.get('title', pillar.get('name', str(pillar)))
                else:
                    pillar_text = str(pillar)
                memory_parts.append(f"{i}. {pillar_text}")
            
            # Add keywords if available
            if keywords:
                memory_parts.append("\nKEY KEYWORDS:")
                primary_keywords = keywords.get('primary', [])[:10]  # Limit to top 10
                if primary_keywords:
                    memory_parts.append(f"Primary: {', '.join(primary_keywords)}")
                
                secondary_keywords = keywords.get('secondary', [])[:10]  # Limit to top 10
                if secondary_keywords:
                    memory_parts.append(f"Secondary: {', '.join(secondary_keywords)}")
            
            # Add competitive insights if available
            if competitive_analysis:
                competitors = competitive_analysis.get('competitors', [])[:3]  # Top 3 competitors
                if competitors:
                    memory_parts.append("\nKEY COMPETITORS:")
                    for competitor in competitors:
                        if isinstance(competitor, dict):
                            comp_name = competitor.get('name', competitor.get('domain', 'Unknown'))
                            memory_parts.append(f"- {comp_name}")
                        else:
                            memory_parts.append(f"- {str(competitor)}")
            
            return "\n".join(memory_parts)
            
        except Exception as e:
            logger.error(f"Error preparing strategy memory content: {e}")
            # Fallback to basic JSON representation
            return f"Content Strategy #{strategy_id}: {json.dumps(strategy_data, indent=2)[:1000]}..."
    
    async def retrieve_strategy_memories(self, user_id: int, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve content strategy memories for a user
        
        Args:
            user_id: User ID to retrieve memories for
            query: Optional search query
            
        Returns:
            List of memory objects
        """
        if not self.is_available():
            logger.warning("Mem0 service not available")
            return []
        
        try:
            if query:
                # Search with specific query
                results = self.memory.search(
                    query=query,
                    user_id=str(user_id),
                    limit=10
                )
            else:
                # Get all strategy memories
                results = self.memory.get_all(
                    user_id=str(user_id)
                )
            
            # Filter for content strategy memories
            strategy_memories = []
            for memory in results:
                metadata = memory.get('metadata', {})
                if metadata.get('type') == 'content_strategy':
                    strategy_memories.append(memory)
            
            logger.info(f"Retrieved {len(strategy_memories)} strategy memories for user {user_id}")
            return strategy_memories
            
        except Exception as e:
            logger.error(f"Error retrieving strategy memories: {e}")
            return []
    
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