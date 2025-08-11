"""
Strategy Endpoints Module
CRUD, analytics, utility, streaming, autofill, and AI generation endpoints for content strategies.
"""

from .strategy_crud import router as crud_router
from .analytics_endpoints import router as analytics_router
from .utility_endpoints import router as utility_router
from .streaming_endpoints import router as streaming_router
from .autofill_endpoints import router as autofill_router
from .ai_generation_endpoints import router as ai_generation_router

__all__ = ["crud_router", "analytics_router", "utility_router", "streaming_router", "autofill_router", "ai_generation_router"] 