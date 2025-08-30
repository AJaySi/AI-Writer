from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from services.database import get_db
from services.strategy_copilot_service import StrategyCopilotService

router = APIRouter(prefix="/api/content-planning/strategy", tags=["strategy-copilot"])

@router.post("/generate-category-data")
async def generate_category_data(
    request: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Generate data for a specific category based on user description."""
    try:
        service = StrategyCopilotService(db)
        result = await service.generate_category_data(
            category=request["category"],
            user_description=request["userDescription"],
            current_form_data=request["currentFormData"]
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate-field")
async def validate_field(
    request: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Validate a specific strategy field."""
    try:
        service = StrategyCopilotService(db)
        result = await service.validate_field(
            field_id=request["fieldId"],
            value=request["value"]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_strategy(
    request: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Analyze complete strategy for completeness and coherence."""
    try:
        service = StrategyCopilotService(db)
        result = await service.analyze_strategy(
            form_data=request["formData"]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-suggestions")
async def generate_suggestions(
    request: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Generate suggestions for a specific field."""
    try:
        service = StrategyCopilotService(db)
        result = await service.generate_field_suggestions(
            field_id=request["fieldId"],
            current_form_data=request["currentFormData"]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
