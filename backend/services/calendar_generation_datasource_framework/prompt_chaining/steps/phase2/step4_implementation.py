"""
Step 4 Implementation: Calendar Framework and Timeline

This module contains the implementation for Step 4 of the 12-step prompt chaining process.
It handles calendar structure analysis, timeline optimization, duration control, and strategic alignment.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from loguru import logger

from ..base_step import PromptStep
import sys
import os

# Add the services directory to the path for proper imports
services_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)

# Import data processing modules
try:
    from calendar_generation_datasource_framework.data_processing import (
        ComprehensiveUserDataProcessor,
        StrategyDataProcessor,
        GapAnalysisDataProcessor
    )
    from content_gap_analyzer.ai_engine_service import AIEngineService
    from content_gap_analyzer.keyword_researcher import KeywordResearcher
    from content_gap_analyzer.competitor_analyzer import CompetitorAnalyzer
except ImportError:
    # Fallback imports for testing
    ComprehensiveUserDataProcessor = None
    StrategyDataProcessor = None
    GapAnalysisDataProcessor = None
    AIEngineService = None
    KeywordResearcher = None
    CompetitorAnalyzer = None


class CalendarFrameworkStep(PromptStep):
    """
    Step 4: Calendar Framework and Timeline
    
    Data Sources: Calendar Configuration Data, Timeline Optimization Algorithms
    Context Focus: Calendar structure, timeline configuration, duration control, strategic alignment
    
    Quality Gates:
    - Calendar structure completeness validation
    - Timeline optimization effectiveness
    - Duration control accuracy
    - Strategic alignment verification
    """
    
    def __init__(self):
        super().__init__("Calendar Framework & Timeline", 4)
        # Initialize services if available
        if AIEngineService:
            self.ai_engine = AIEngineService()
        else:
            self.ai_engine = None
            
        if ComprehensiveUserDataProcessor:
            self.comprehensive_user_processor = ComprehensiveUserDataProcessor()
        else:
            self.comprehensive_user_processor = None
        
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute calendar framework and timeline step."""
        try:
            start_time = time.time()
            logger.info(f"🔄 Executing Step 4: Calendar Framework & Timeline")
            
            # Extract relevant data from context
            user_id = context.get("user_id")
            strategy_id = context.get("strategy_id")
            calendar_type = context.get("calendar_type", "monthly")
            industry = context.get("industry")
            business_size = context.get("business_size", "sme")
            
            # Get comprehensive user data
            if self.comprehensive_user_processor:
                user_data = await self.comprehensive_user_processor.get_comprehensive_user_data(user_id, strategy_id)
            else:
                # Fail gracefully - no fallback data
                logger.error("❌ ComprehensiveUserDataProcessor not available - Step 4 cannot proceed")
                raise RuntimeError("Required service ComprehensiveUserDataProcessor is not available. Step 4 cannot execute without real user data.")
            
            # Step 4.1: Calendar Structure Analysis
            calendar_structure = await self._analyze_calendar_structure(
                user_data, calendar_type, industry, business_size
            )
            
            # Step 4.2: Timeline Configuration and Optimization
            timeline_config = await self._optimize_timeline(
                calendar_structure, user_data, calendar_type
            )
            
            # Step 4.3: Duration Control and Accuracy Validation
            duration_control = await self._validate_duration_control(
                timeline_config, user_data
            )
            
            # Step 4.4: Strategic Alignment Verification
            strategic_alignment = await self._verify_strategic_alignment(
                calendar_structure, timeline_config, user_data
            )
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Generate step results
            step_results = {
                "stepNumber": 4,
                "stepName": "Calendar Framework & Timeline",
                "results": {
                    "calendarStructure": calendar_structure,
                    "timelineConfiguration": timeline_config,
                    "durationControl": duration_control,
                    "strategicAlignment": strategic_alignment
                },
                "qualityScore": self._calculate_quality_score(
                    calendar_structure, timeline_config, duration_control, strategic_alignment
                ),
                "executionTime": f"{execution_time:.1f}s",
                "dataSourcesUsed": ["Calendar Configuration", "Timeline Optimization", "Strategic Alignment"],
                "insights": [
                    f"Calendar structure optimized for {calendar_type} format",
                    f"Timeline configured with {timeline_config.get('total_weeks', 0)} weeks",
                    f"Duration control validated with {duration_control.get('accuracy_score', 0):.1%} accuracy",
                    f"Strategic alignment verified with {strategic_alignment.get('alignment_score', 0):.1%} score"
                ],
                "recommendations": [
                    "Optimize posting frequency based on audience engagement patterns",
                    "Adjust timeline duration for better content distribution",
                    "Enhance strategic alignment with business goals"
                ]
            }
            
            logger.info(f"✅ Step 4 completed with quality score: {step_results['qualityScore']:.2f}")
            return step_results
            
        except Exception as e:
            logger.error(f"❌ Error in Step 4: {str(e)}")
            raise
    
    async def _analyze_calendar_structure(self, user_data: Dict, calendar_type: str, industry: str, business_size: str) -> Dict[str, Any]:
        """Analyze calendar structure based on user data and requirements."""
        try:
            if not self.ai_engine:
                logger.error("❌ AIEngineService not available for calendar structure analysis")
                raise RuntimeError("Required service AIEngineService is not available for calendar structure analysis.")
            
            # Get posting preferences from user data
            posting_preferences = user_data.get("onboarding_data", {}).get("posting_preferences", {})
            posting_days = user_data.get("onboarding_data", {}).get("posting_days", [])
            
            if not posting_preferences or not posting_days:
                logger.error("❌ Missing posting preferences or posting days in user data")
                raise ValueError("Calendar structure analysis requires posting preferences and posting days from user data.")
            
            # Calculate total weeks based on calendar type
            if calendar_type == "monthly":
                total_weeks = 4
            elif calendar_type == "quarterly":
                total_weeks = 12
            elif calendar_type == "weekly":
                total_weeks = 1
            else:
                total_weeks = 4  # Default to monthly
            
            # Analyze posting frequency
            daily_posts = posting_preferences.get("daily", 0)
            weekly_posts = posting_preferences.get("weekly", 0)
            monthly_posts = posting_preferences.get("monthly", 0)
            
            return {
                "type": calendar_type,
                "total_weeks": total_weeks,
                "posting_frequency": {
                    "daily": daily_posts,
                    "weekly": weekly_posts,
                    "monthly": monthly_posts
                },
                "posting_days": posting_days,
                "industry": industry,
                "business_size": business_size
            }
            
        except Exception as e:
            logger.error(f"Error in calendar structure analysis: {str(e)}")
            raise
    
    async def _optimize_timeline(self, calendar_structure: Dict, user_data: Dict, calendar_type: str) -> Dict[str, Any]:
        """Optimize timeline configuration for the calendar."""
        try:
            if not self.ai_engine:
                logger.error("❌ AIEngineService not available for timeline optimization")
                raise RuntimeError("Required service AIEngineService is not available for timeline optimization.")
            
            total_weeks = calendar_structure.get("total_weeks", 4)
            posting_days = calendar_structure.get("posting_days", [])
            
            if not posting_days:
                logger.error("❌ Missing posting days for timeline optimization")
                raise ValueError("Timeline optimization requires posting days from calendar structure.")
            
            # Calculate total posting days
            total_days = total_weeks * len(posting_days)
            
            # Get optimal times from user data
            optimal_times = user_data.get("onboarding_data", {}).get("optimal_times", [])
            
            if not optimal_times:
                logger.error("❌ Missing optimal posting times for timeline optimization")
                raise ValueError("Timeline optimization requires optimal posting times from user data.")
            
            return {
                "total_weeks": total_weeks,
                "total_days": total_days,
                "posting_days": posting_days,
                "optimal_times": optimal_times,
                "calendar_type": calendar_type
            }
            
        except Exception as e:
            logger.error(f"Error in timeline optimization: {str(e)}")
            raise
    
    async def _validate_duration_control(self, timeline_config: Dict, user_data: Dict) -> Dict[str, Any]:
        """Validate duration control and accuracy."""
        try:
            if not self.ai_engine:
                logger.error("❌ AIEngineService not available for duration control validation")
                raise RuntimeError("Required service AIEngineService is not available for duration control validation.")
            
            total_weeks = timeline_config.get("total_weeks", 0)
            total_days = timeline_config.get("total_days", 0)
            
            if total_weeks <= 0 or total_days <= 0:
                logger.error("❌ Invalid timeline configuration for duration control validation")
                raise ValueError("Duration control validation requires valid timeline configuration.")
            
            # Validate against user preferences
            posting_preferences = user_data.get("onboarding_data", {}).get("posting_preferences", {})
            
            if not posting_preferences:
                logger.error("❌ Missing posting preferences for duration control validation")
                raise ValueError("Duration control validation requires posting preferences from user data.")
            
            # Calculate accuracy based on alignment with user preferences
            monthly_posts = posting_preferences.get("monthly", 0)
            expected_days = monthly_posts if timeline_config.get("calendar_type") == "monthly" else total_days
            
            accuracy_score = min(total_days / expected_days, 1.0) if expected_days > 0 else 0.0
            
            return {
                "accuracy_score": accuracy_score,
                "total_weeks": total_weeks,
                "total_days": total_days,
                "expected_days": expected_days,
                "validation_passed": accuracy_score >= 0.8
            }
            
        except Exception as e:
            logger.error(f"Error in duration control validation: {str(e)}")
            raise
    
    async def _verify_strategic_alignment(self, calendar_structure: Dict, timeline_config: Dict, user_data: Dict) -> Dict[str, Any]:
        """Verify strategic alignment of calendar framework."""
        try:
            if not self.ai_engine:
                logger.error("❌ AIEngineService not available for strategic alignment verification")
                raise RuntimeError("Required service AIEngineService is not available for strategic alignment verification.")
            
            # Get business goals and objectives from user data
            strategy_data = user_data.get("strategy_data", {})
            business_goals = strategy_data.get("business_goals", [])
            business_objectives = strategy_data.get("business_objectives", [])
            
            if not business_goals:
                logger.error("❌ Missing business goals for strategic alignment verification")
                raise ValueError("Strategic alignment verification requires business goals from user data.")
            
            # Get content pillars
            content_pillars = strategy_data.get("content_pillars", {})
            
            if not content_pillars:
                logger.error("❌ Missing content pillars for strategic alignment verification")
                raise ValueError("Strategic alignment verification requires content pillars from user data.")
            
            # Calculate alignment score based on how well the calendar supports business goals
            total_goals = len(business_goals)
            supported_goals = 0
            
            for goal in business_goals:
                if any(pillar in goal.lower() for pillar in content_pillars.keys()):
                    supported_goals += 1
            
            alignment_score = supported_goals / total_goals if total_goals > 0 else 0.0
            
            return {
                "alignment_score": alignment_score,
                "business_goals": business_goals,
                "business_objectives": business_objectives,
                "content_pillars": content_pillars,
                "supported_goals": supported_goals,
                "total_goals": total_goals,
                "alignment_passed": alignment_score >= 0.7
            }
            
        except Exception as e:
            logger.error(f"Error in strategic alignment verification: {str(e)}")
            raise
    
    def _calculate_quality_score(self, calendar_structure: Dict, timeline_config: Dict, duration_control: Dict, strategic_alignment: Dict) -> float:
        """Calculate quality score for Step 4."""
        try:
            # Extract individual scores
            duration_accuracy = duration_control.get("accuracy_score", 0.0)
            strategic_alignment_score = strategic_alignment.get("alignment_score", 0.0)
            
            # Validate that we have real data
            if duration_accuracy == 0.0 or strategic_alignment_score == 0.0:
                logger.error("❌ Missing quality metrics for score calculation")
                raise ValueError("Quality score calculation requires valid duration control and strategic alignment metrics.")
            
            # Weighted average based on importance
            quality_score = (
                duration_accuracy * 0.6 +
                strategic_alignment_score * 0.4
            )
            
            return min(quality_score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating quality score: {str(e)}")
            raise
    
    def get_prompt_template(self) -> str:
        """Get the AI prompt template for Step 4: Calendar Framework and Timeline."""
        return """
        You are an expert calendar strategist specializing in content calendar framework and timeline optimization.
        
        CONTEXT:
        - User Data: {user_data}
        - Calendar Type: {calendar_type}
        - Industry: {industry}
        - Business Size: {business_size}
        
        TASK:
        Analyze and optimize calendar framework and timeline:
        1. Analyze calendar structure based on user preferences and requirements
        2. Optimize timeline configuration for maximum effectiveness
        3. Validate duration control and accuracy
        4. Verify strategic alignment with business goals
        
        REQUIREMENTS:
        - Use real user data for all calculations
        - Ensure timeline optimization aligns with posting preferences
        - Validate duration control against user requirements
        - Verify strategic alignment with business objectives
        - Calculate quality scores based on real metrics
        
        OUTPUT FORMAT:
        Return structured analysis with:
        - Calendar structure analysis
        - Timeline configuration optimization
        - Duration control validation
        - Strategic alignment verification
        - Quality scores and recommendations
        """
    
    def validate_result(self, result: Dict[str, Any]) -> bool:
        """Validate the Step 4 result."""
        try:
            # Check required fields
            required_fields = [
                "stepNumber", "stepName", "results", "qualityScore", 
                "executionTime", "dataSourcesUsed", "insights", "recommendations"
            ]
            
            for field in required_fields:
                if field not in result:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Validate step number
            if result.get("stepNumber") != 4:
                logger.error(f"Invalid step number: {result.get('stepNumber')}")
                return False
            
            # Validate results structure
            results = result.get("results", {})
            required_results = ["calendarStructure", "timelineConfiguration", "durationControl", "strategicAlignment"]
            
            for result_field in required_results:
                if result_field not in results:
                    logger.error(f"Missing result field: {result_field}")
                    return False
            
            # Validate quality score is not mock data
            quality_score = result.get("qualityScore", 0)
            if quality_score == 0.9 or quality_score == 0.88:  # Common mock values
                logger.error("Quality score appears to be mock data")
                return False
            
            logger.info(f"✅ Step 4 result validation passed with quality score: {result.get('qualityScore', 0):.2f}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error validating Step 4 result: {str(e)}")
            return False
