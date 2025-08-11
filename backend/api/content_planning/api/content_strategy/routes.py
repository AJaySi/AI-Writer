"""
Content Strategy Routes
Main router that includes all content strategy endpoint modules.
"""

from fastapi import APIRouter

# Import endpoint modules
from .endpoints.strategy_crud import router as crud_router
from .endpoints.analytics_endpoints import router as analytics_router
from .endpoints.utility_endpoints import router as utility_router
from .endpoints.streaming_endpoints import router as streaming_router
from .endpoints.autofill_endpoints import router as autofill_router
from .endpoints.ai_generation_endpoints import router as ai_generation_router

# Create main router
router = APIRouter(prefix="/content-strategy", tags=["Content Strategy"])

# Include all endpoint routers
router.include_router(crud_router, prefix="/strategies")
router.include_router(analytics_router, prefix="/strategies")
router.include_router(utility_router, prefix="")
router.include_router(streaming_router, prefix="")
router.include_router(autofill_router, prefix="/strategies")
router.include_router(ai_generation_router, prefix="/ai-generation") 