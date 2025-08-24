"""
Memory Management API Routes
Handles ALwrity memory statistics, search, and CRUD operations
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from services.mem0_service import Mem0Service
from loguru import logger

router = APIRouter(prefix="/memory", tags=["memory"])

# Pydantic models for request/response
class MemorySearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10
    user_type: Optional[str] = None
    industry: Optional[str] = None
    categories: Optional[List[str]] = None

class MemoryUpdateRequest(BaseModel):
    strategy_data: Dict[str, Any]

class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class MemoryDeleteRequest(BaseModel):
    memory_ids: List[str]

# Initialize service
def get_mem0_service():
    return Mem0Service()

@router.get("/statistics/{user_id}")
async def get_memory_statistics(
    user_id: int,
    mem0_service: Mem0Service = Depends(get_mem0_service)
) -> Dict[str, Any]:
    """
    Get comprehensive memory statistics for the mind icon
    
    Returns:
        - Total memories count
        - Categories breakdown
        - User types distribution
        - Industries representation
        - Recent activity
        - API usage stats
    """
    try:
        stats = await mem0_service.get_memory_statistics(user_id)
        
        # Add some additional UI-friendly formatting
        stats["formatted_categories"] = [
            {"name": category, "count": count, "percentage": round((count / max(stats["total_memories"], 1)) * 100, 1)}
            for category, count in stats["categories"].items()
        ]
        
        stats["status_message"] = f"ALwrity has stored {stats['total_memories']} strategic memories for you"
        
        return {
            "success": True,
            "data": stats
        }
        
    except Exception as e:
        logger.error(f"Error getting memory statistics for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve memory statistics: {str(e)}")

@router.post("/search/{user_id}")
async def search_memories(
    user_id: int,
    search_request: MemorySearchRequest,
    mem0_service: Mem0Service = Depends(get_mem0_service)
) -> Dict[str, Any]:
    """
    Search memories using advanced filtering and natural language queries
    """
    try:
        results = await mem0_service.retrieve_strategy_memories(
            user_id=user_id,
            query=search_request.query if search_request.query.strip() else None,
            user_type=search_request.user_type,
            industry=search_request.industry,
            categories=search_request.categories,
            limit=search_request.limit
        )
        
        return {
            "success": True,
            "data": {
                "memories": results,
                "total_found": len(results),
                "query": search_request.query,
                "filters_applied": {
                    "user_type": search_request.user_type,
                    "industry": search_request.industry,
                    "categories": search_request.categories
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Error searching memories for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Memory search failed: {str(e)}")

@router.post("/chat/{user_id}")
async def chat_with_memories(
    user_id: int,
    chat_message: ChatMessage,
    mem0_service: Mem0Service = Depends(get_mem0_service)
) -> Dict[str, Any]:
    """
    Chat interface for querying memories with natural language
    """
    try:
        # Search relevant memories based on the chat message
        relevant_memories = await mem0_service.search_memories_with_query(
            user_id=user_id,
            query=chat_message.message,
            limit=5
        )
        
        # Prepare context for chat response
        memory_context = []
        for memory in relevant_memories:
            memory_context.append({
                "strategy_name": memory["strategy_name"],
                "industry": memory["industry"],
                "categories": memory["categories"],
                "summary": memory["content"][:200] + "..." if len(memory["content"]) > 200 else memory["content"]
            })
        
        response = {
            "success": True,
            "data": {
                "relevant_memories": relevant_memories,
                "memory_context": memory_context,
                "total_memories_searched": len(relevant_memories),
                "chat_ready": True,
                "suggested_questions": [
                    "What content strategies have worked best for my industry?",
                    "Show me my most recent marketing campaigns",
                    "What are my top performing content pillars?",
                    "How have my strategies evolved over time?"
                ]
            }
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Error in chat with memories for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Chat query failed: {str(e)}")

@router.get("/all/{user_id}")
async def get_all_memories(
    user_id: int,
    limit: int = Query(50, description="Maximum number of memories to return"),
    user_type: Optional[str] = Query(None, description="Filter by user type"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    mem0_service: Mem0Service = Depends(get_mem0_service)
) -> Dict[str, Any]:
    """
    Get all memories for a user with optional filtering
    """
    try:
        memories = await mem0_service.retrieve_strategy_memories(
            user_id=user_id,
            user_type=user_type,
            industry=industry,
            limit=limit
        )
        
        return {
            "success": True,
            "data": {
                "memories": memories,
                "total": len(memories),
                "filters": {
                    "user_type": user_type,
                    "industry": industry,
                    "limit": limit
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting all memories for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve memories: {str(e)}")

@router.delete("/delete/{user_id}/{strategy_id}")
async def delete_memory(
    user_id: int,
    strategy_id: int,
    mem0_service: Mem0Service = Depends(get_mem0_service)
) -> Dict[str, Any]:
    """
    Delete a specific memory by strategy ID
    """
    try:
        success = await mem0_service.delete_strategy_memory(user_id, strategy_id)
        
        if success:
            return {
                "success": True,
                "message": f"Memory for strategy {strategy_id} deleted successfully"
            }
        else:
            raise HTTPException(status_code=404, detail=f"Memory for strategy {strategy_id} not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting memory for user {user_id}, strategy {strategy_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete memory: {str(e)}")

@router.put("/update/{user_id}/{strategy_id}")
async def update_memory(
    user_id: int,
    strategy_id: int,
    update_request: MemoryUpdateRequest,
    mem0_service: Mem0Service = Depends(get_mem0_service)
) -> Dict[str, Any]:
    """
    Update an existing memory with new strategy data
    """
    try:
        success = await mem0_service.update_strategy_memory(
            user_id=user_id,
            strategy_id=strategy_id,
            updated_strategy_data=update_request.strategy_data
        )
        
        if success:
            return {
                "success": True,
                "message": f"Memory for strategy {strategy_id} updated successfully"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to update memory")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating memory for user {user_id}, strategy {strategy_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update memory: {str(e)}")

@router.get("/categories/{user_id}")
async def get_user_categories(
    user_id: int,
    mem0_service: Mem0Service = Depends(get_mem0_service)
) -> Dict[str, Any]:
    """
    Get all available categories for the user for filtering purposes
    """
    try:
        stats = await mem0_service.get_memory_statistics(user_id)
        
        categories = list(stats.get("categories", {}).keys())
        industries = list(stats.get("industries", {}).keys())
        user_types = list(stats.get("user_types", {}).keys())
        
        return {
            "success": True,
            "data": {
                "categories": categories,
                "industries": industries,
                "user_types": user_types,
                "available_filters": {
                    "categories": mem0_service.CONTENT_CREATOR_CATEGORIES + mem0_service.DIGITAL_MARKETER_CATEGORIES,
                    "industries": mem0_service.INDUSTRY_CATEGORIES
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting categories for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve categories: {str(e)}")

@router.get("/health")
async def memory_health_check(
    mem0_service: Mem0Service = Depends(get_mem0_service)
) -> Dict[str, Any]:
    """
    Check if memory service is available and healthy
    """
    return {
        "success": True,
        "data": {
            "mem0_available": mem0_service.is_available(),
            "service_status": "healthy" if mem0_service.is_available() else "unavailable",
            "features": {
                "storage": mem0_service.is_available(),
                "search": mem0_service.is_available(),
                "categorization": True,
                "chat_interface": mem0_service.is_available()
            }
        }
    }