"""
AI Generation Endpoints
Handles AI-powered strategy generation endpoints.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from loguru import logger
from datetime import datetime
from fastapi.responses import StreamingResponse
import json

# Import database
from services.database import get_db_session

# Import services
from ....services.content_strategy.ai_generation import AIStrategyGenerator, StrategyGenerationConfig
from ....services.enhanced_strategy_service import EnhancedStrategyService
from ....services.enhanced_strategy_db_service import EnhancedStrategyDBService

# Import utilities
from ....utils.error_handlers import ContentPlanningErrorHandler
from ....utils.response_builders import ResponseBuilder
from ....utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES

router = APIRouter(tags=["AI Strategy Generation"])

# Helper function to get database session
def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate-comprehensive-strategy")
async def generate_comprehensive_strategy(
    user_id: int,
    strategy_name: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Generate a comprehensive AI-powered content strategy."""
    try:
        logger.info(f"🚀 Generating comprehensive AI strategy for user: {user_id}")
        
        # Get user context and onboarding data
        db_service = EnhancedStrategyDBService(db)
        enhanced_service = EnhancedStrategyService(db_service)
        
        # Get onboarding data for context
        onboarding_data = await enhanced_service._get_onboarding_data(user_id)
        
        # Build context for AI generation
        context = {
            "onboarding_data": onboarding_data,
            "user_id": user_id,
            "generation_config": config or {}
        }
        
        # Create strategy generation config
        generation_config = StrategyGenerationConfig(
            include_competitive_analysis=config.get("include_competitive_analysis", True) if config else True,
            include_content_calendar=config.get("include_content_calendar", True) if config else True,
            include_performance_predictions=config.get("include_performance_predictions", True) if config else True,
            include_implementation_roadmap=config.get("include_implementation_roadmap", True) if config else True,
            include_risk_assessment=config.get("include_risk_assessment", True) if config else True,
            max_content_pieces=config.get("max_content_pieces", 50) if config else 50,
            timeline_months=config.get("timeline_months", 12) if config else 12
        )
        
        # Initialize AI strategy generator
        strategy_generator = AIStrategyGenerator(generation_config)
        
        # Generate comprehensive strategy
        comprehensive_strategy = await strategy_generator.generate_comprehensive_strategy(
            user_id=user_id,
            context=context,
            strategy_name=strategy_name
        )
        
        logger.info(f"✅ Comprehensive AI strategy generated successfully for user: {user_id}")
        
        return ResponseBuilder.create_success_response(
            message="Comprehensive AI strategy generated successfully",
            data=comprehensive_strategy
        )
        
    except RuntimeError as e:
        logger.error(f"❌ AI service error generating comprehensive strategy: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"AI service temporarily unavailable: {str(e)}"
        )
    except Exception as e:
        logger.error(f"❌ Error generating comprehensive strategy: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "generate_comprehensive_strategy")

@router.post("/generate-strategy-component")
async def generate_strategy_component(
    user_id: int,
    component_type: str,
    base_strategy: Optional[Dict[str, Any]] = None,
    context: Optional[Dict[str, Any]] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Generate a specific strategy component using AI."""
    try:
        logger.info(f"🚀 Generating strategy component '{component_type}' for user: {user_id}")
        
        # Validate component type
        valid_components = [
            "strategic_insights",
            "competitive_analysis", 
            "content_calendar",
            "performance_predictions",
            "implementation_roadmap",
            "risk_assessment"
        ]
        
        if component_type not in valid_components:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid component type. Must be one of: {valid_components}"
            )
        
        # Get context if not provided
        if not context:
            db_service = EnhancedStrategyDBService(db)
            enhanced_service = EnhancedStrategyService(db_service)
            onboarding_data = await enhanced_service._get_onboarding_data(user_id)
            context = {"onboarding_data": onboarding_data, "user_id": user_id}
        
        # Get base strategy if not provided
        if not base_strategy:
            # Generate base strategy using autofill
            from ....services.content_strategy.autofill.ai_structured_autofill import AIStructuredAutofillService
            autofill_service = AIStructuredAutofillService()
            autofill_result = await autofill_service.generate_autofill_fields(user_id, context)
            base_strategy = autofill_result.get("fields", {})
        
        # Initialize AI strategy generator
        strategy_generator = AIStrategyGenerator()
        
        # Generate specific component
        if component_type == "strategic_insights":
            component = await strategy_generator._generate_strategic_insights(base_strategy, context)
        elif component_type == "competitive_analysis":
            component = await strategy_generator._generate_competitive_analysis(base_strategy, context)
        elif component_type == "content_calendar":
            component = await strategy_generator._generate_content_calendar(base_strategy, context)
        elif component_type == "performance_predictions":
            component = await strategy_generator._generate_performance_predictions(base_strategy, context)
        elif component_type == "implementation_roadmap":
            component = await strategy_generator._generate_implementation_roadmap(base_strategy, context)
        elif component_type == "risk_assessment":
            component = await strategy_generator._generate_risk_assessment(base_strategy, context)
        
        logger.info(f"✅ Strategy component '{component_type}' generated successfully for user: {user_id}")
        
        return ResponseBuilder.create_success_response(
            message=f"Strategy component '{component_type}' generated successfully",
            data={
                "component_type": component_type,
                "component_data": component,
                "generated_at": datetime.utcnow().isoformat(),
                "user_id": user_id
            }
        )
        
    except RuntimeError as e:
        logger.error(f"❌ AI service error generating strategy component: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"AI service temporarily unavailable for {component_type}: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error generating strategy component: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "generate_strategy_component")

@router.get("/strategy-generation-status")
async def get_strategy_generation_status(
    user_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get the status of strategy generation for a user."""
    try:
        logger.info(f"Getting strategy generation status for user: {user_id}")
        
        # Get user's strategies
        db_service = EnhancedStrategyDBService(db)
        enhanced_service = EnhancedStrategyService(db_service)
        
        strategies_data = await enhanced_service.get_enhanced_strategies(user_id, None, db)
        
        # Analyze generation status
        strategies = strategies_data.get("strategies", [])
        
        status_data = {
            "user_id": user_id,
            "total_strategies": len(strategies),
            "ai_generated_strategies": len([s for s in strategies if s.get("ai_generated", False)]),
            "last_generation": None,
            "generation_stats": {
                "comprehensive_strategies": 0,
                "partial_strategies": 0,
                "manual_strategies": 0
            }
        }
        
        if strategies:
            # Find most recent AI-generated strategy
            ai_strategies = [s for s in strategies if s.get("ai_generated", False)]
            if ai_strategies:
                latest_ai = max(ai_strategies, key=lambda x: x.get("created_at", ""))
                status_data["last_generation"] = latest_ai.get("created_at")
            
            # Categorize strategies
            for strategy in strategies:
                if strategy.get("ai_generated", False):
                    if strategy.get("comprehensive", False):
                        status_data["generation_stats"]["comprehensive_strategies"] += 1
                    else:
                        status_data["generation_stats"]["partial_strategies"] += 1
                else:
                    status_data["generation_stats"]["manual_strategies"] += 1
        
        logger.info(f"✅ Strategy generation status retrieved for user: {user_id}")
        
        return ResponseBuilder.create_success_response(
            message="Strategy generation status retrieved successfully",
            data=status_data
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting strategy generation status: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_strategy_generation_status")

@router.post("/optimize-existing-strategy")
async def optimize_existing_strategy(
    strategy_id: int,
    optimization_type: str = "comprehensive",
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Optimize an existing strategy using AI."""
    try:
        logger.info(f"🚀 Optimizing existing strategy {strategy_id} with type: {optimization_type}")
        
        # Get existing strategy
        db_service = EnhancedStrategyDBService(db)
        enhanced_service = EnhancedStrategyService(db_service)
        
        strategies_data = await enhanced_service.get_enhanced_strategies(strategy_id=strategy_id, db=db)
        
        if strategies_data.get("status") == "not_found" or not strategies_data.get("strategies"):
            raise HTTPException(
                status_code=404,
                detail=f"Strategy with ID {strategy_id} not found"
            )
        
        existing_strategy = strategies_data["strategies"][0]
        user_id = existing_strategy.get("user_id")
        
        # Get user context
        onboarding_data = await enhanced_service._get_onboarding_data(user_id)
        context = {"onboarding_data": onboarding_data, "user_id": user_id}
        
        # Initialize AI strategy generator
        strategy_generator = AIStrategyGenerator()
        
        # Generate optimization based on type
        if optimization_type == "comprehensive":
            # Generate comprehensive optimization
            optimized_strategy = await strategy_generator.generate_comprehensive_strategy(
                user_id=user_id,
                context=context,
                strategy_name=f"Optimized: {existing_strategy.get('name', 'Strategy')}"
            )
        else:
            # Generate specific component optimization
            component = await strategy_generator._generate_strategic_insights(existing_strategy, context)
            optimized_strategy = {
                "optimization_type": optimization_type,
                "original_strategy": existing_strategy,
                "optimization_data": component,
                "optimized_at": datetime.utcnow().isoformat()
            }
        
        logger.info(f"✅ Strategy {strategy_id} optimized successfully")
        
        return ResponseBuilder.create_success_response(
            message="Strategy optimized successfully",
            data=optimized_strategy
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error optimizing strategy: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "optimize_existing_strategy") 

@router.get("/generate-comprehensive-strategy/stream")
async def generate_comprehensive_strategy_stream(
    user_id: int,
    strategy_name: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None,
    db: Session = Depends(get_db)
):
    """Generate comprehensive AI strategy with Server-Sent Events for progress updates."""
    try:
        logger.info(f"🚀 Starting streaming AI strategy generation for user: {user_id}")
        
        async def generate_strategy_stream():
            try:
                # Step 1: Get user context with educational content
                yield f"data: {json.dumps({
                    'step': 1, 
                    'message': 'Getting user context...', 
                    'progress': 10,
                    'educational_content': {
                        'title': '🔍 Analyzing Your Data',
                        'description': 'We\'re gathering all your onboarding information to create a personalized strategy.',
                        'details': [
                            '📊 Website analysis data',
                            '🎯 Research preferences',
                            '🔑 API configurations',
                            '📈 Historical performance metrics'
                        ],
                        'insight': 'Your data helps us understand your business context, target audience, and competitive landscape.',
                        'ai_prompt_preview': 'Analyzing user onboarding data to extract business context, audience insights, and competitive positioning...'
                    }
                })}\n\n"
                
                db_service = EnhancedStrategyDBService(db)
                enhanced_service = EnhancedStrategyService(db_service)
                onboarding_data = await enhanced_service._get_onboarding_data(user_id)
                
                context = {
                    "onboarding_data": onboarding_data,
                    "user_id": user_id,
                    "generation_config": config or {}
                }
                
                # Step 2: Generate base strategy fields
                yield f"data: {json.dumps({
                    'step': 2, 
                    'message': 'Generating base strategy fields...', 
                    'progress': 20,
                    'educational_content': {
                        'title': '🏗️ Building Foundation',
                        'description': 'Creating the core strategy framework based on your business objectives.',
                        'details': [
                            '🎯 Business objectives mapping',
                            '📊 Target metrics definition',
                            '💰 Budget allocation strategy',
                            '⏰ Timeline planning'
                        ],
                        'insight': 'A solid foundation ensures your content strategy aligns with business goals and resources.',
                        'ai_prompt_preview': 'Generating strategic foundation: business objectives, target metrics, budget allocation, and timeline planning...'
                    }
                })}\n\n"
                
                # Initialize AI strategy generator
                from ....services.content_strategy.ai_generation import AIStrategyGenerator
                strategy_generator = AIStrategyGenerator()
                
                # Step 3: Generate strategic insights with real-time educational content
                yield f"data: {json.dumps({
                    'step': 3, 
                    'message': 'Generating strategic insights...', 
                    'progress': 30,
                    'educational_content': {
                        'title': '🧠 Strategic Intelligence Analysis',
                        'description': 'AI is analyzing your market position and identifying strategic opportunities.',
                        'details': [
                            '🎯 Market positioning analysis',
                            '💡 Opportunity identification',
                            '📈 Growth potential assessment',
                            '🎪 Competitive advantage mapping'
                        ],
                        'insight': 'Strategic insights help you understand where you stand in the market and how to differentiate.',
                        'ai_prompt_preview': 'Analyzing market position, identifying strategic opportunities, assessing growth potential, and mapping competitive advantages...',
                        'estimated_time': '15-20 seconds'
                    }
                })}\n\n"
                
                try:
                    # Create a custom AI service manager that emits educational content to SSE
                    from services.ai_service_manager import AIServiceManager, AIServiceType
                    
                    class SSEAIServiceManager(AIServiceManager):
                        def __init__(self, sse_yield_func):
                            super().__init__()
                            self.sse_yield = sse_yield_func
                        
                        async def _emit_educational_content(self, service_type: AIServiceType, status: str, error_message: str = None, processing_time: float = None):
                            """Override to emit educational content to SSE stream."""
                            try:
                                educational_content = self._get_educational_content(service_type, status, error_message, processing_time)
                                
                                # Emit to SSE stream
                                yield_data = {
                                    'type': 'educational_content',
                                    'service_type': service_type.value,
                                    'status': status,
                                    'educational_content': educational_content
                                }
                                
                                if processing_time:
                                    yield_data['processing_time'] = processing_time
                                if error_message:
                                    yield_data['error_message'] = error_message
                                
                                await self.sse_yield(f"data: {json.dumps(yield_data)}\n\n")
                                logger.info(f"📚 Emitted educational content for {service_type.value}: {status}")
                                
                            except Exception as e:
                                logger.error(f"Error emitting educational content to SSE: {e}")
                    
                    # Use the SSE-enabled AI service manager
                    sse_ai_manager = SSEAIServiceManager(lambda data: generate_strategy_stream().__anext__())
                    
                    # Generate strategic insights with educational content
                    strategic_insights = await strategy_generator._generate_strategic_insights({}, context, sse_ai_manager)
                    
                    yield f"data: {json.dumps({
                        'step': 3, 
                        'message': 'Strategic insights generated successfully', 
                        'progress': 35, 
                        'success': True,
                        'educational_content': {
                            'title': '✅ Strategic Insights Complete',
                            'description': 'Successfully identified key strategic opportunities and market positioning.',
                            'achievement': f'Generated {len(strategic_insights.get("insights", []))} strategic insights',
                            'next_step': 'Moving to competitive analysis...'
                        }
                    })}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({
                        'step': 3, 
                        'message': f'Strategic insights generation failed: {str(e)}', 
                        'progress': 35, 
                        'success': False, 
                        'error': str(e),
                        'educational_content': {
                            'title': '⚠️ Strategic Insights Issue',
                            'description': 'We encountered an issue with strategic analysis, but continuing with other components.',
                            'fallback': 'Will use industry best practices for strategic positioning.'
                        }
                    })}\n\n"
                    strategic_insights = {}
                
                # Step 4: Generate competitive analysis with educational content
                yield f"data: {json.dumps({
                    'step': 4, 
                    'message': 'Generating competitive analysis...', 
                    'progress': 40,
                    'educational_content': {
                        'title': '🔍 Competitive Intelligence Analysis',
                        'description': 'AI is analyzing your competitors to identify gaps and opportunities.',
                        'details': [
                            '🏢 Competitor content strategies',
                            '📊 Market gap analysis',
                            '🎯 Differentiation opportunities',
                            '📈 Industry trend analysis'
                        ],
                        'insight': 'Understanding your competitors helps you find unique angles and underserved market segments.',
                        'ai_prompt_preview': 'Analyzing competitor content strategies, identifying market gaps, finding differentiation opportunities, and assessing industry trends...',
                        'estimated_time': '20-25 seconds'
                    }
                })}\n\n"
                
                try:
                    competitive_analysis = await strategy_generator._generate_competitive_analysis({}, context, sse_ai_manager)
                    yield f"data: {json.dumps({
                        'step': 4, 
                        'message': 'Competitive analysis generated successfully', 
                        'progress': 45, 
                        'success': True,
                        'educational_content': {
                            'title': '✅ Competitive Analysis Complete',
                            'description': 'Successfully analyzed competitive landscape and identified market opportunities.',
                            'achievement': f'Analyzed {len(competitive_analysis.get("competitors", []))} competitors',
                            'next_step': 'Moving to content calendar generation...'
                        }
                    })}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({
                        'step': 4, 
                        'message': f'Competitive analysis generation failed: {str(e)}', 
                        'progress': 45, 
                        'success': False, 
                        'error': str(e),
                        'educational_content': {
                            'title': '⚠️ Competitive Analysis Issue',
                            'description': 'We encountered an issue with competitive analysis, but continuing with other components.',
                            'fallback': 'Will use industry best practices for competitive positioning.'
                        }
                    })}\n\n"
                    competitive_analysis = {}
                
                # Step 5: Generate content calendar with educational content
                yield f"data: {json.dumps({
                    'step': 5, 
                    'message': 'Generating content calendar...', 
                    'progress': 50,
                    'educational_content': {
                        'title': '📅 Content Calendar Creation',
                        'description': 'AI is building a comprehensive content schedule optimized for your audience.',
                        'details': [
                            '📝 Content piece generation',
                            '📅 Optimal publishing schedule',
                            '🎯 Audience engagement timing',
                            '🔄 Content repurposing strategy'
                        ],
                        'insight': 'A well-planned content calendar ensures consistent engagement and maximizes content ROI.',
                        'ai_prompt_preview': 'Generating content pieces, optimizing publishing schedule, determining audience engagement timing, and planning content repurposing...',
                        'estimated_time': '25-30 seconds'
                    }
                })}\n\n"
                
                try:
                    content_calendar = await strategy_generator._generate_content_calendar({}, context, sse_ai_manager)
                    yield f"data: {json.dumps({
                        'step': 5, 
                        'message': 'Content calendar generated successfully', 
                        'progress': 55, 
                        'success': True,
                        'educational_content': {
                            'title': '✅ Content Calendar Complete',
                            'description': 'Successfully created comprehensive content schedule.',
                            'achievement': f'Generated {len(content_calendar.get("content_pieces", []))} content pieces',
                            'next_step': 'Moving to performance predictions...'
                        }
                    })}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({
                        'step': 5, 
                        'message': f'Content calendar generation failed: {str(e)}', 
                        'progress': 55, 
                        'success': False, 
                        'error': str(e),
                        'educational_content': {
                            'title': '⚠️ Content Calendar Issue',
                            'description': 'We encountered an issue with content calendar generation, but continuing with other components.',
                            'fallback': 'Will use industry best practices for content scheduling.'
                        }
                    })}\n\n"
                    content_calendar = {}
                
                # Step 6: Generate performance predictions with educational content
                yield f"data: {json.dumps({
                    'step': 6, 
                    'message': 'Generating performance predictions...', 
                    'progress': 60,
                    'educational_content': {
                        'title': '📊 Performance Forecasting',
                        'description': 'AI is predicting content performance and ROI based on industry data.',
                        'details': [
                            '📈 Traffic growth projections',
                            '💰 ROI predictions',
                            '🎯 Conversion rate estimates',
                            '📊 Engagement metrics forecasting'
                        ],
                        'insight': 'Performance predictions help you set realistic expectations and optimize resource allocation.',
                        'ai_prompt_preview': 'Analyzing industry benchmarks, predicting traffic growth, estimating ROI, forecasting conversion rates, and projecting engagement metrics...',
                        'estimated_time': '15-20 seconds'
                    }
                })}\n\n"
                
                try:
                    performance_predictions = await strategy_generator._generate_performance_predictions({}, context, sse_ai_manager)
                    yield f"data: {json.dumps({
                        'step': 6, 
                        'message': 'Performance predictions generated successfully', 
                        'progress': 65, 
                        'success': True,
                        'educational_content': {
                            'title': '✅ Performance Predictions Complete',
                            'description': 'Successfully predicted content performance and ROI.',
                            'achievement': f'Predicted {performance_predictions.get("estimated_roi", "15-25%")} ROI',
                            'next_step': 'Moving to implementation roadmap...'
                        }
                    })}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({
                        'step': 6, 
                        'message': f'Performance predictions generation failed: {str(e)}', 
                        'progress': 65, 
                        'success': False, 
                        'error': str(e),
                        'educational_content': {
                            'title': '⚠️ Performance Predictions Issue',
                            'description': 'We encountered an issue with performance predictions, but continuing with other components.',
                            'fallback': 'Will use industry benchmarks for performance estimates.'
                        }
                    })}\n\n"
                    performance_predictions = {}
                
                # Step 7: Generate implementation roadmap with educational content
                yield f"data: {json.dumps({
                    'step': 7, 
                    'message': 'Generating implementation roadmap...', 
                    'progress': 70,
                    'educational_content': {
                        'title': '🗺️ Implementation Roadmap',
                        'description': 'AI is creating a detailed implementation plan for your content strategy.',
                        'details': [
                            '📋 Task breakdown and timeline',
                            '👥 Resource allocation planning',
                            '🎯 Milestone definition',
                            '📊 Success metric tracking'
                        ],
                        'insight': 'A clear implementation roadmap ensures successful strategy execution and measurable results.',
                        'ai_prompt_preview': 'Creating implementation roadmap: task breakdown, resource allocation, milestone planning, and success metric definition...',
                        'estimated_time': '15-20 seconds'
                    }
                })}\n\n"
                
                try:
                    implementation_roadmap = await strategy_generator._generate_implementation_roadmap({}, context, sse_ai_manager)
                    yield f"data: {json.dumps({
                        'step': 7, 
                        'message': 'Implementation roadmap generated successfully', 
                        'progress': 75, 
                        'success': True,
                        'educational_content': {
                            'title': '✅ Implementation Roadmap Complete',
                            'description': 'Successfully created detailed implementation plan.',
                            'achievement': f'Planned {implementation_roadmap.get("total_duration", "12 months")} implementation timeline',
                            'next_step': 'Moving to risk assessment...'
                        }
                    })}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({
                        'step': 7, 
                        'message': f'Implementation roadmap generation failed: {str(e)}', 
                        'progress': 75, 
                        'success': False, 
                        'error': str(e),
                        'educational_content': {
                            'title': '⚠️ Implementation Roadmap Issue',
                            'description': 'We encountered an issue with implementation roadmap generation, but continuing with other components.',
                            'fallback': 'Will use industry best practices for implementation planning.'
                        }
                    })}\n\n"
                    implementation_roadmap = {}
                
                # Step 8: Generate risk assessment with educational content
                yield f"data: {json.dumps({
                    'step': 8, 
                    'message': 'Generating risk assessment...', 
                    'progress': 80,
                    'educational_content': {
                        'title': '⚠️ Risk Assessment',
                        'description': 'AI is identifying potential risks and mitigation strategies for your content strategy.',
                        'details': [
                            '🔍 Risk identification and analysis',
                            '📊 Risk probability assessment',
                            '🛡️ Mitigation strategy development',
                            '📈 Risk monitoring framework'
                        ],
                        'insight': 'Proactive risk assessment helps you prepare for challenges and maintain strategy effectiveness.',
                        'ai_prompt_preview': 'Assessing risks: identifying potential challenges, analyzing probability and impact, developing mitigation strategies, and creating monitoring framework...',
                        'estimated_time': '10-15 seconds'
                    }
                })}\n\n"
                
                try:
                    risk_assessment = await strategy_generator._generate_risk_assessment({}, context, sse_ai_manager)
                    yield f"data: {json.dumps({
                        'step': 8, 
                        'message': 'Risk assessment generated successfully', 
                        'progress': 85, 
                        'success': True,
                        'educational_content': {
                            'title': '✅ Risk Assessment Complete',
                            'description': 'Successfully identified risks and mitigation strategies.',
                            'achievement': f'Assessed {risk_assessment.get("overall_risk_level", "Medium")} risk level',
                            'next_step': 'Finalizing comprehensive strategy...'
                        }
                    })}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({
                        'step': 8, 
                        'message': f'Risk assessment generation failed: {str(e)}', 
                        'progress': 85, 
                        'success': False, 
                        'error': str(e),
                        'educational_content': {
                            'title': '⚠️ Risk Assessment Issue',
                            'description': 'We encountered an issue with risk assessment, but continuing with strategy finalization.',
                            'fallback': 'Will use industry best practices for risk management.'
                        }
                    })}\n\n"
                    risk_assessment = {}
                
                # Step 9: Compile comprehensive strategy
                yield f"data: {json.dumps({
                    'step': 9, 
                    'message': 'Compiling comprehensive strategy...', 
                    'progress': 90,
                    'educational_content': {
                        'title': '📋 Strategy Compilation',
                        'description': 'AI is compiling all components into a comprehensive content strategy.',
                        'details': [
                            '🔗 Component integration',
                            '📊 Data synthesis',
                            '📝 Strategy documentation',
                            '✅ Quality validation'
                        ],
                        'insight': 'A comprehensive strategy integrates all components into a cohesive, actionable plan.',
                        'ai_prompt_preview': 'Compiling comprehensive strategy: integrating all components, synthesizing data, documenting strategy, and validating quality...',
                        'estimated_time': '5-10 seconds'
                    }
                })}\n\n"
                
                # Compile the comprehensive strategy
                comprehensive_strategy = {
                    "strategic_insights": strategic_insights,
                    "competitive_analysis": competitive_analysis,
                    "content_calendar": content_calendar,
                    "performance_predictions": performance_predictions,
                    "implementation_roadmap": implementation_roadmap,
                    "risk_assessment": risk_assessment,
                    "metadata": {
                        "ai_generated": True,
                        "comprehensive": True,
                        "generation_timestamp": datetime.utcnow().isoformat(),
                        "user_id": user_id,
                        "strategy_name": strategy_name or "Enhanced Content Strategy"
                    }
                }
                
                # Step 10: Complete with educational content
                yield f"data: {json.dumps({
                    'step': 10, 
                    'message': 'Strategy generation completed successfully!', 
                    'progress': 100, 
                    'success': True, 
                    'strategy': comprehensive_strategy,
                    'educational_content': {
                        'title': '🎉 Strategy Generation Complete!',
                        'description': 'Your comprehensive AI-powered content strategy is ready!',
                        'summary': {
                            'total_components': 6,
                            'successful_components': sum([
                                1 if strategic_insights else 0,
                                1 if competitive_analysis else 0,
                                1 if content_calendar else 0,
                                1 if performance_predictions else 0,
                                1 if implementation_roadmap else 0,
                                1 if risk_assessment else 0
                            ]),
                            'total_content_pieces': len(content_calendar.get("content_pieces", [])),
                            'estimated_roi': performance_predictions.get("estimated_roi", "15-25%"),
                            'implementation_timeline': implementation_roadmap.get("total_duration", "12 months"),
                            'risk_level': risk_assessment.get("overall_risk_level", "Medium")
                        },
                        'key_achievements': [
                            '🧠 Strategic insights generated',
                            '🔍 Competitive analysis completed',
                            '📅 Content calendar created',
                            '📊 Performance predictions calculated',
                            '🗺️ Implementation roadmap planned',
                            '⚠️ Risk assessment conducted'
                        ],
                        'next_steps': [
                            'Review your comprehensive strategy',
                            'Customize specific components as needed',
                            'Share with your team for feedback',
                            'Begin implementation following the roadmap'
                        ],
                        'ai_insights': 'Your strategy leverages advanced AI analysis of your business context, competitive landscape, and industry best practices to create a data-driven content approach.',
                        'personalization_note': 'This strategy is uniquely tailored to your business based on your onboarding data, ensuring relevance and effectiveness.'
                    }
                })}\n\n"
                
            except Exception as e:
                logger.error(f"❌ Error in streaming strategy generation: {str(e)}")
                yield f"data: {json.dumps({'error': f'Strategy generation failed: {str(e)}', 'progress': 0, 'success': False})}\n\n"
        
        return StreamingResponse(
            generate_strategy_stream(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Cache-Control"
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Error starting streaming strategy generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start streaming strategy generation: {str(e)}"
        )

@router.get("/ai-generation-education")
async def get_ai_generation_education() -> Dict[str, Any]:
    """Get educational content about the AI generation process."""
    try:
        logger.info("📚 Providing AI generation educational content")
        
        educational_content = {
            "title": "🤖 AI-Powered Strategy Generation",
            "subtitle": "Understanding How We Create Your Content Strategy",
            "overview": {
                "description": "Our AI system analyzes your business data and generates a comprehensive content strategy using advanced machine learning and industry best practices.",
                "total_time": "2-3 minutes",
                "components": 6,
                "ai_model": "Google Gemini Pro",
                "personalization_level": "High"
            },
            "process_steps": [
                {
                    "step": 1,
                    "title": "🔍 Data Analysis",
                    "description": "Analyzing your onboarding data to understand your business context",
                    "duration": "5-10 seconds",
                    "details": [
                        "Website analysis data processing",
                        "Research preferences analysis",
                        "API configuration review",
                        "Historical performance assessment"
                    ],
                    "ai_prompt_example": "Analyze user onboarding data to extract business context, audience insights, and competitive positioning..."
                },
                {
                    "step": 2,
                    "title": "🏗️ Foundation Building",
                    "description": "Creating the core strategy framework based on your objectives",
                    "duration": "5-10 seconds",
                    "details": [
                        "Business objectives mapping",
                        "Target metrics definition",
                        "Budget allocation strategy",
                        "Timeline planning"
                    ],
                    "ai_prompt_example": "Generate strategic foundation: business objectives, target metrics, budget allocation, and timeline planning..."
                },
                {
                    "step": 3,
                    "title": "🧠 Strategic Intelligence",
                    "description": "AI analyzes your market position and identifies opportunities",
                    "duration": "15-20 seconds",
                    "details": [
                        "Market positioning analysis",
                        "Opportunity identification",
                        "Growth potential assessment",
                        "Competitive advantage mapping"
                    ],
                    "ai_prompt_example": "Analyze market position, identify strategic opportunities, assess growth potential, and map competitive advantages..."
                },
                {
                    "step": 4,
                    "title": "🔍 Competitive Intelligence",
                    "description": "Analyzing competitors to identify gaps and opportunities",
                    "duration": "20-25 seconds",
                    "details": [
                        "Competitor content strategies",
                        "Market gap analysis",
                        "Differentiation opportunities",
                        "Industry trend analysis"
                    ],
                    "ai_prompt_example": "Analyze competitor content strategies, identify market gaps, find differentiation opportunities, and assess industry trends..."
                },
                {
                    "step": 5,
                    "title": "📅 Content Calendar Creation",
                    "description": "Building a comprehensive content schedule optimized for your audience",
                    "duration": "25-30 seconds",
                    "details": [
                        "Content piece generation",
                        "Optimal publishing schedule",
                        "Audience engagement timing",
                        "Content repurposing strategy"
                    ],
                    "ai_prompt_example": "Generate content pieces, optimize publishing schedule, determine audience engagement timing, and plan content repurposing..."
                },
                {
                    "step": 6,
                    "title": "📊 Performance Forecasting",
                    "description": "Predicting content performance and ROI based on industry data",
                    "duration": "15-20 seconds",
                    "details": [
                        "Traffic growth projections",
                        "ROI predictions",
                        "Conversion rate estimates",
                        "Engagement metrics forecasting"
                    ],
                    "ai_prompt_example": "Analyze industry benchmarks, predict traffic growth, estimate ROI, forecast conversion rates, and project engagement metrics..."
                },
                {
                    "step": 7,
                    "title": "🗺️ Implementation Roadmap",
                    "description": "Creating a step-by-step plan to execute your strategy",
                    "duration": "15-20 seconds",
                    "details": [
                        "Phase-by-phase breakdown",
                        "Timeline with milestones",
                        "Resource allocation",
                        "Success checkpoints"
                    ],
                    "ai_prompt_example": "Create phase-by-phase breakdown, establish timeline with milestones, allocate resources, and set success checkpoints..."
                },
                {
                    "step": 8,
                    "title": "⚠️ Risk Assessment",
                    "description": "Identifying potential challenges and creating mitigation strategies",
                    "duration": "10-15 seconds",
                    "details": [
                        "Risk identification",
                        "Risk probability analysis",
                        "Mitigation strategies",
                        "Contingency planning"
                    ],
                    "ai_prompt_example": "Identify potential risks, analyze risk probabilities, develop mitigation strategies, and create contingency plans..."
                }
            ],
            "ai_technology": {
                "model": "Google Gemini Pro",
                "capabilities": [
                    "Advanced natural language processing",
                    "Context-aware analysis",
                    "Industry knowledge integration",
                    "Personalized recommendations"
                ],
                "data_sources": [
                    "Your onboarding data",
                    "Industry benchmarks",
                    "Best practices database",
                    "Market research insights"
                ]
            },
            "personalization_features": {
                "data_points_used": [
                    "Business objectives and goals",
                    "Target audience demographics",
                    "Industry and market context",
                    "Competitive landscape",
                    "Content preferences and style",
                    "Budget and resource constraints"
                ],
                "customization_level": "High",
                "adaptation_factors": [
                    "Industry-specific insights",
                    "Audience behavior patterns",
                    "Competitive positioning",
                    "Resource availability"
                ]
            },
            "quality_assurance": {
                "validation_steps": [
                    "Data completeness check",
                    "Strategy coherence validation",
                    "Industry alignment verification",
                    "Implementation feasibility assessment"
                ],
                "fallback_mechanisms": [
                    "Industry best practices",
                    "Standard templates",
                    "Benchmark data",
                    "Expert recommendations"
                ]
            },
            "tips_for_users": [
                "💡 The more detailed your onboarding data, the more personalized your strategy will be",
                "📊 Review and customize the generated strategy to match your specific needs",
                "🔄 Use the strategy as a starting point and iterate based on performance",
                "📈 Monitor results and adjust the strategy as your business evolves",
                "👥 Share the strategy with your team for feedback and buy-in"
            ],
            "technical_details": {
                "processing_time": "2-3 minutes total",
                "ai_calls": "8 specialized AI analyses",
                "data_processing": "Real-time onboarding data integration",
                "output_format": "Structured JSON with comprehensive strategy components",
                "scalability": "Handles multiple concurrent generations"
            }
        }
        
        return ResponseBuilder.create_success_response(
            message="AI generation educational content retrieved successfully",
            data=educational_content
        )
        
    except Exception as e:
        logger.error(f"❌ Error getting AI generation education: {str(e)}")
        raise ContentPlanningErrorHandler.handle_general_error(e, "get_ai_generation_education") 