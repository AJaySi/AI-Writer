"""
Gap Analysis Data Processor

Extracted from calendar_generator_service.py to improve maintainability
and align with 12-step implementation plan.
"""

from typing import Dict, Any
from loguru import logger


class GapAnalysisDataProcessor:
    """Process gap analysis data from database."""
    
    def __init__(self):
        self.content_planning_db_service = None  # Will be injected
    
    async def get_gap_analysis_data(self, user_id: int) -> Dict[str, Any]:
        """Get gap analysis data from database."""
        try:
            # Check if database service is available
            if self.content_planning_db_service is None:
                logger.warning("ContentPlanningDBService not available, returning empty gap analysis data")
                return {}
            
            # Get latest gap analysis results using the correct method name
            gap_analyses = await self.content_planning_db_service.get_user_content_gap_analyses(user_id)
            
            if gap_analyses:
                latest_analysis = gap_analyses[0]  # Get most recent
                return {
                    "content_gaps": latest_analysis.get("analysis_results", {}).get("content_gaps", []),
                    "keyword_opportunities": latest_analysis.get("analysis_results", {}).get("keyword_opportunities", []),
                    "competitor_insights": latest_analysis.get("analysis_results", {}).get("competitor_insights", []),
                    "recommendations": latest_analysis.get("recommendations", []),
                    "opportunities": latest_analysis.get("opportunities", [])
                }
            return {}
            
        except Exception as e:
            logger.warning(f"Could not get gap analysis data: {str(e)}")
            return {}
