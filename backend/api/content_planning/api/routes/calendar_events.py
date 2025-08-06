"""
Calendar Events Routes for Content Planning API
Extracted from the main content_planning.py file for better organization.
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger

# Import database service
from services.database import get_db_session, get_db
from services.content_planning_db import ContentPlanningDBService

# Import models
from ..models.requests import CalendarEventCreate
from ..models.responses import CalendarEventResponse

# Import utilities
from ...utils.error_handlers import ContentPlanningErrorHandler
from ...utils.response_builders import ResponseBuilder
from ...utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES

# Import services
from ...services.calendar_service import CalendarService

# Initialize services
calendar_service = CalendarService()

# Create router
router = APIRouter(prefix="/calendar-events", tags=["calendar-events"])

@router.post("/", response_model=CalendarEventResponse)
async def create_calendar_event(
    event: CalendarEventCreate,
    db: Session = Depends(get_db)
):
    """Create a new calendar event."""
    try:
        logger.info(f"Creating calendar event: {event.title}")
        
        event_data = event.dict()
        created_event = await calendar_service.create_calendar_event(event_data, db)
        
        return CalendarEventResponse(**created_event)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating calendar event: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "create_calendar_event")

@router.get("/", response_model=List[CalendarEventResponse])
async def get_calendar_events(
    strategy_id: Optional[int] = Query(None, description="Filter by strategy ID"),
    db: Session = Depends(get_db)
):
    """Get calendar events, optionally filtered by strategy."""
    try:
        logger.info("Fetching calendar events")
        
        events = await calendar_service.get_calendar_events(strategy_id, db)
        return [CalendarEventResponse(**event) for event in events]
        
    except Exception as e:
        logger.error(f"Error getting calendar events: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_calendar_events")

@router.get("/{event_id}", response_model=CalendarEventResponse)
async def get_calendar_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific calendar event by ID."""
    try:
        logger.info(f"Fetching calendar event: {event_id}")
        
        event = await calendar_service.get_calendar_event_by_id(event_id, db)
        return CalendarEventResponse(**event)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting calendar event: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_calendar_event")

@router.put("/{event_id}", response_model=CalendarEventResponse)
async def update_calendar_event(
    event_id: int,
    update_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update a calendar event."""
    try:
        logger.info(f"Updating calendar event: {event_id}")
        
        updated_event = await calendar_service.update_calendar_event(event_id, update_data, db)
        return CalendarEventResponse(**updated_event)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating calendar event: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "update_calendar_event")

@router.delete("/{event_id}")
async def delete_calendar_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Delete a calendar event."""
    try:
        logger.info(f"Deleting calendar event: {event_id}")
        
        deleted = await calendar_service.delete_calendar_event(event_id, db)
        
        if deleted:
            return {"message": f"Calendar event {event_id} deleted successfully"}
        else:
            raise ContentPlanningErrorHandler.handle_not_found_error("Calendar event", event_id)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting calendar event: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "delete_calendar_event")

@router.post("/schedule", response_model=Dict[str, Any])
async def schedule_calendar_event(
    event: CalendarEventCreate,
    db: Session = Depends(get_db)
):
    """Schedule a calendar event with conflict checking."""
    try:
        logger.info(f"Scheduling calendar event: {event.title}")
        
        event_data = event.dict()
        result = await calendar_service.schedule_event(event_data, db)
        return result
        
    except Exception as e:
        logger.error(f"Error scheduling calendar event: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "schedule_calendar_event")

@router.get("/strategy/{strategy_id}/events")
async def get_strategy_events(
    strategy_id: int,
    status: Optional[str] = Query(None, description="Filter by event status"),
    db: Session = Depends(get_db)
):
    """Get calendar events for a specific strategy."""
    try:
        logger.info(f"Fetching events for strategy: {strategy_id}")
        
        if status:
            events = await calendar_service.get_events_by_status(strategy_id, status, db)
            return {
                'strategy_id': strategy_id,
                'status': status,
                'events_count': len(events),
                'events': events
            }
        else:
            result = await calendar_service.get_strategy_events(strategy_id, db)
            return result
        
    except Exception as e:
        logger.error(f"Error getting strategy events: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") 