"""
Calendar Generation Service for Content Planning API
Extracted business logic from the calendar generation route for better separation of concerns.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger
from sqlalchemy.orm import Session
import time

# Import database service
from services.content_planning_db import ContentPlanningDBService

# Import calendar generator service
from services.calendar_generator_service import CalendarGeneratorService

# Import validation service
from services.validation import check_all_api_keys

# Import utilities
from ..utils.error_handlers import ContentPlanningErrorHandler
from ..utils.response_builders import ResponseBuilder
from ..utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES

class CalendarGenerationService:
    """Service class for calendar generation operations."""
    
    def __init__(self):
        self.calendar_generator_service = CalendarGeneratorService()
    
    async def generate_comprehensive_calendar(self, user_id: int, strategy_id: Optional[int] = None, 
                                           calendar_type: str = "monthly", industry: Optional[str] = None, 
                                           business_size: str = "sme") -> Dict[str, Any]:
        """Generate a comprehensive AI-powered content calendar using database insights."""
        try:
            logger.info(f"🎯 Generating comprehensive calendar for user {user_id}")
            start_time = time.time()
            
            # Generate calendar using advanced AI-powered method
            calendar_data = await self.calendar_generator_service.generate_ai_powered_calendar(
                user_id=user_id,
                strategy_id=strategy_id,
                calendar_type=calendar_type,
                industry=industry,
                business_size=business_size
            )
            
            processing_time = time.time() - start_time
            
            logger.info(f"✅ Calendar generated successfully in {processing_time:.2f}s")
            return calendar_data
            
        except Exception as e:
            logger.error(f"❌ Error generating comprehensive calendar: {str(e)}")
            logger.error(f"Exception type: {type(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise ContentPlanningErrorHandler.handle_general_error(e, "generate_comprehensive_calendar")
    
    async def optimize_content_for_platform(self, user_id: int, title: str, description: str, 
                                         content_type: str, target_platform: str, event_id: Optional[int] = None) -> Dict[str, Any]:
        """Optimize content for specific platforms using database insights."""
        try:
            logger.info(f"🔧 Starting content optimization for user {user_id}")
            
            # Validate API keys - temporarily disabled for testing
            # from services.api_key_manager import APIKeyManager
            # api_manager = APIKeyManager()
            # api_key_status = check_all_api_keys(api_manager)
            # if not api_key_status.get("all_valid", False):
            #     raise Exception("AI services are not properly configured")
            
            # Get user data for optimization
            user_data = await self.calendar_generator_service._get_comprehensive_user_data(
                user_id, 
                None  # No strategy_id for content optimization
            )
            
            # Create optimization request for AI
            optimization_prompt = f"""
            Optimize the following content for {target_platform}:
            
            Original Content:
            - Title: {title}
            - Description: {description}
            - Content Type: {content_type}
            - Platform: {target_platform}
            
            User Context:
            - Industry: {user_data.get('industry', 'technology')}
            - Target Audience: {user_data.get('target_audience', {})}
            - Performance Data: {user_data.get('performance_data', {})}
            - Gap Analysis: {user_data.get('gap_analysis', {})}
            
            Provide comprehensive optimization including:
            1. Platform-specific adaptations
            2. Visual recommendations
            3. Hashtag suggestions
            4. Keyword optimization
            5. Tone adjustments
            6. Length optimization
            7. Performance predictions
            """
            
            # Generate optimization using AI
            optimization_result = await self.calendar_generator_service.ai_engine.generate_content_recommendations(
                analysis_data={
                    "original_content": {
                        "title": title,
                        "description": description,
                        "content_type": content_type,
                        "target_platform": target_platform
                    },
                    "user_context": {
                        "industry": user_data.get('industry', 'technology'),
                        "target_audience": user_data.get('target_audience', {}),
                        "performance_data": user_data.get('performance_data', {}),
                        "gap_analysis": user_data.get('gap_analysis', {})
                    }
                }
            )
            
            # Prepare response
            response_data = {
                "user_id": user_id,
                "event_id": event_id,
                "original_content": {
                    "title": title,
                    "description": description,
                    "content_type": content_type,
                    "target_platform": target_platform
                },
                "optimized_content": {
                    "title": title,
                    "description": description,
                    "content_type": content_type,
                    "target_platform": target_platform
                },
                "platform_adaptations": [rec.get('description', '') for rec in optimization_result[:3]],
                "visual_recommendations": ["Use engaging visuals", "Include relevant images", "Optimize for mobile"],
                "hashtag_suggestions": ["#content", "#marketing", "#digital"],
                "keyword_optimization": {"primary": "content", "secondary": ["marketing", "digital"]},
                "tone_adjustments": {"tone": "professional", "style": "informative"},
                "length_optimization": {"optimal_length": "150-300 words", "format": "paragraphs"},
                "performance_prediction": {"engagement_rate": 0.05, "reach": 1000},
                "optimization_score": 0.8,
                "created_at": datetime.utcnow()
            }
            
            logger.info(f"✅ Content optimization completed for user {user_id}")
            return response_data
            
        except Exception as e:
            logger.error(f"❌ Error optimizing content: {str(e)}")
            raise ContentPlanningErrorHandler.handle_general_error(e, "optimize_content_for_platform")
    
    async def predict_content_performance(self, user_id: int, content_type: str, platform: str, 
                                       content_data: Dict[str, Any], strategy_id: Optional[int] = None) -> Dict[str, Any]:
        """Predict content performance using database insights."""
        try:
            logger.info(f"📊 Starting performance prediction for user {user_id}")
            
            # Get user data for prediction
            user_data = await self.calendar_generator_service._get_comprehensive_user_data(
                user_id, 
                strategy_id
            )
            
            # Generate performance prediction
            prediction_prompt = f"""
            Predict performance for the following content:
            
            Content Data:
            - Content Type: {content_type}
            - Platform: {platform}
            - Content Data: {content_data}
            
            User Context:
            - Industry: {user_data.get('industry', 'technology')}
            - Performance Data: {user_data.get('performance_data', {})}
            - Gap Analysis: {user_data.get('gap_analysis', {})}
            - Audience Insights: {user_data.get('onboarding_data', {}).get('target_audience', {})}
            
            Provide performance predictions including:
            1. Engagement rate
            2. Reach estimates
            3. Conversion predictions
            4. ROI estimates
            5. Confidence score
            6. Recommendations
            """
            
            # Generate prediction using AI
            prediction_result = await self.calendar_generator_service.ai_engine.generate_structured_response(
                prompt=prediction_prompt,
                schema={
                    "type": "object",
                    "properties": {
                        "predicted_engagement_rate": {"type": "number"},
                        "predicted_reach": {"type": "integer"},
                        "predicted_conversions": {"type": "integer"},
                        "predicted_roi": {"type": "number"},
                        "confidence_score": {"type": "number"},
                        "recommendations": {"type": "array", "items": {"type": "string"}}
                    }
                }
            )
            
            # Prepare response
            response_data = {
                "user_id": user_id,
                "strategy_id": strategy_id,
                "content_type": content_type,
                "platform": platform,
                "predicted_engagement_rate": prediction_result.get("predicted_engagement_rate", 0.05),
                "predicted_reach": prediction_result.get("predicted_reach", 1000),
                "predicted_conversions": prediction_result.get("predicted_conversions", 10),
                "predicted_roi": prediction_result.get("predicted_roi", 2.5),
                "confidence_score": prediction_result.get("confidence_score", 0.75),
                "recommendations": prediction_result.get("recommendations", []),
                "created_at": datetime.utcnow()
            }
            
            logger.info(f"✅ Performance prediction completed for user {user_id}")
            return response_data
            
        except Exception as e:
            logger.error(f"❌ Error predicting content performance: {str(e)}")
            raise ContentPlanningErrorHandler.handle_general_error(e, "predict_content_performance")
    
    async def repurpose_content_across_platforms(self, user_id: int, original_content: Dict[str, Any], 
                                               target_platforms: List[str], strategy_id: Optional[int] = None) -> Dict[str, Any]:
        """Repurpose content across different platforms using database insights."""
        try:
            logger.info(f"🔄 Starting content repurposing for user {user_id}")
            
            # Get user data for repurposing
            user_data = await self.calendar_generator_service._get_comprehensive_user_data(
                user_id, 
                strategy_id
            )
            
            # Generate repurposing suggestions
            repurposing_prompt = f"""
            Repurpose the following content for multiple platforms:
            
            Original Content:
            {original_content}
            
            Target Platforms:
            {target_platforms}
            
            User Context:
            - Gap Analysis: {user_data.get('gap_analysis', {})}
            - Strategy Data: {user_data.get('strategy_data', {})}
            - Recommendations: {user_data.get('recommendations_data', [])}
            
            Provide repurposing suggestions including:
            1. Platform-specific adaptations
            2. Content transformations
            3. Implementation tips
            4. Gap addressing opportunities
            """
            
            # Generate repurposing suggestions using AI
            repurposing_result = await self.calendar_generator_service.ai_engine.generate_structured_response(
                prompt=repurposing_prompt,
                schema={
                    "type": "object",
                    "properties": {
                        "platform_adaptations": {"type": "array", "items": {"type": "object"}},
                        "transformations": {"type": "array", "items": {"type": "object"}},
                        "implementation_tips": {"type": "array", "items": {"type": "string"}},
                        "gap_addresses": {"type": "array", "items": {"type": "string"}}
                    }
                }
            )
            
            # Prepare response
            response_data = {
                "user_id": user_id,
                "strategy_id": strategy_id,
                "original_content": original_content,
                "platform_adaptations": repurposing_result.get("platform_adaptations", []),
                "transformations": repurposing_result.get("transformations", []),
                "implementation_tips": repurposing_result.get("implementation_tips", []),
                "gap_addresses": repurposing_result.get("gap_addresses", []),
                "created_at": datetime.utcnow()
            }
            
            logger.info(f"✅ Content repurposing completed for user {user_id}")
            return response_data
            
        except Exception as e:
            logger.error(f"❌ Error repurposing content: {str(e)}")
            raise ContentPlanningErrorHandler.handle_general_error(e, "repurpose_content_across_platforms")
    
    async def get_trending_topics(self, user_id: int, industry: str, limit: int = 10) -> Dict[str, Any]:
        """Get trending topics relevant to the user's industry and content gaps."""
        try:
            logger.info(f"📈 Getting trending topics for user {user_id} in {industry}")
            
            # Get user data for trending topics
            user_data = await self.calendar_generator_service._get_comprehensive_user_data(user_id, None)
            
            # Get trending topics with database insights
            trending_topics = await self.calendar_generator_service._get_trending_topics_from_db(industry, user_data)
            
            # Limit results
            limited_topics = trending_topics[:limit]
            
            # Calculate relevance scores
            gap_relevance_scores = {}
            audience_alignment_scores = {}
            
            for topic in limited_topics:
                topic_key = topic.get("keyword", "")
                gap_relevance_scores[topic_key] = self.calendar_generator_service._assess_gap_relevance(topic, user_data.get("gap_analysis", {}))
                audience_alignment_scores[topic_key] = self.calendar_generator_service._assess_audience_alignment(topic, user_data.get("onboarding_data", {}))
            
            # Prepare response
            response_data = {
                "user_id": user_id,
                "industry": industry,
                "trending_topics": limited_topics,
                "gap_relevance_scores": gap_relevance_scores,
                "audience_alignment_scores": audience_alignment_scores,
                "created_at": datetime.utcnow()
            }
            
            logger.info(f"✅ Trending topics retrieved for user {user_id}")
            return response_data
            
        except Exception as e:
            logger.error(f"❌ Error getting trending topics: {str(e)}")
            raise ContentPlanningErrorHandler.handle_general_error(e, "get_trending_topics")
    
    async def get_comprehensive_user_data(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive user data for calendar generation."""
        try:
            logger.info(f"Getting comprehensive user data for user_id: {user_id}")
            
            # Get comprehensive data using the calendar generator service
            logger.info("Calling calendar generator service...")
            comprehensive_data = await self.calendar_generator_service._get_comprehensive_user_data(user_id, None)
            logger.info(f"Calendar generator service returned: {type(comprehensive_data)}")
            
            logger.info(f"Successfully retrieved comprehensive user data for user_id: {user_id}")
            
            return {
                "status": "success",
                "data": comprehensive_data,
                "message": "Comprehensive user data retrieved successfully",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting comprehensive user data for user_id {user_id}: {str(e)}")
            logger.error(f"Exception type: {type(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise ContentPlanningErrorHandler.handle_general_error(e, "get_comprehensive_user_data")
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for calendar generation services."""
        try:
            logger.info("🏥 Performing calendar generation health check")
            
            # Check AI services
            from services.api_key_manager import APIKeyManager
            api_manager = APIKeyManager()
            api_key_status = check_all_api_keys(api_manager)
            
            # Check database connectivity
            db_status = "healthy"
            try:
                # Test database connection - only if calendar generator service is properly initialized
                if hasattr(self.calendar_generator_service, 'content_planning_db_service') and self.calendar_generator_service.content_planning_db_service is not None:
                    await self.calendar_generator_service.content_planning_db_service.get_user_content_gap_analyses(1)
                else:
                    db_status = "not_initialized"
            except Exception as e:
                db_status = f"error: {str(e)}"
            
            health_status = {
                "service": "calendar_generation",
                "status": "healthy" if api_key_status.get("all_valid", False) and db_status == "healthy" else "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "components": {
                    "ai_services": "healthy" if api_key_status.get("all_valid", False) else "unhealthy",
                    "database": db_status,
                    "calendar_generator": "healthy"
                },
                "api_keys": api_key_status
            }
            
            logger.info("✅ Calendar generation health check completed")
            return health_status
            
        except Exception as e:
            logger.error(f"❌ Calendar generation health check failed: {str(e)}")
            return {
                "service": "calendar_generation",
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            }
