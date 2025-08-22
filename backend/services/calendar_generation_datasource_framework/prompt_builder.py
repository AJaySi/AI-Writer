"""
Strategy-Aware Prompt Builder for Calendar Generation Framework

Builds AI prompts with full strategy context integration for the 12-step
prompt chaining architecture.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from .registry import DataSourceRegistry

logger = logging.getLogger(__name__)


class StrategyAwarePromptBuilder:
    """
    Builds AI prompts with full strategy context integration.
    
    Provides comprehensive prompt templates for all 12 steps of the
    calendar generation process with strategy-aware data context.
    """
    
    def __init__(self, data_source_registry: DataSourceRegistry):
        """
        Initialize the strategy-aware prompt builder.
        
        Args:
            data_source_registry: Registry containing all data sources
        """
        self.registry = data_source_registry
        self.prompt_templates = self._load_prompt_templates()
        self.step_dependencies = self._load_step_dependencies()
        
        logger.info("Initialized StrategyAwarePromptBuilder")
    
    def _load_prompt_templates(self) -> Dict[str, str]:
        """
        Load prompt templates for different steps.
        
        Returns:
            Dictionary of prompt templates for all 12 steps
        """
        return {
            "step_1_content_strategy_analysis": """
            Analyze the following content strategy data and provide comprehensive insights for calendar generation:
            
            STRATEGY DATA:
            {content_strategy_data}
            
            QUALITY INDICATORS:
            {content_strategy_validation}
            
            BUSINESS CONTEXT:
            {business_context}
            
            Generate a detailed analysis covering:
            1. Strategy completeness and coherence assessment
            2. Target audience alignment and segmentation
            3. Content pillar effectiveness and optimization opportunities
            4. Business objective alignment and KPI mapping
            5. Competitive positioning and differentiation strategy
            6. Content opportunities and strategic gaps identification
            7. Brand voice consistency and editorial guidelines assessment
            8. Content frequency and format optimization recommendations
            
            Provide actionable insights that will inform the subsequent calendar generation steps.
            """,
            
            "step_2_gap_analysis": """
            Conduct comprehensive gap analysis using the following data sources:
            
            GAP ANALYSIS DATA:
            {gap_analysis_data}
            
            STRATEGY CONTEXT:
            {content_strategy_data}
            
            KEYWORDS DATA:
            {keywords_data}
            
            AI ANALYSIS DATA:
            {ai_analysis_data}
            
            Generate gap analysis covering:
            1. Content gaps identification and prioritization
            2. Keyword opportunities and search intent mapping
            3. Competitor analysis insights and differentiation opportunities
            4. Market positioning opportunities and trend alignment
            5. Content recommendation priorities and impact assessment
            6. Audience need identification and content opportunity mapping
            7. Performance gap analysis and optimization opportunities
            8. Strategic content opportunity scoring and prioritization
            
            Focus on actionable insights that will drive high-quality calendar generation.
            """,
            
            "step_3_audience_platform_strategy": """
            Develop comprehensive audience and platform strategy using:
            
            STRATEGY DATA:
            {content_strategy_data}
            
            GAP ANALYSIS:
            {gap_analysis_data}
            
            KEYWORDS DATA:
            {keywords_data}
            
            AI ANALYSIS:
            {ai_analysis_data}
            
            Generate audience and platform strategy covering:
            1. Target audience segmentation and persona development
            2. Platform-specific strategy and content adaptation
            3. Audience behavior analysis and content preference mapping
            4. Platform performance optimization and engagement strategies
            5. Cross-platform content strategy and consistency planning
            6. Audience journey mapping and touchpoint optimization
            7. Platform-specific content format and timing optimization
            8. Audience engagement and interaction strategy development
            
            Provide platform-specific insights for optimal calendar generation.
            """,
            
            "step_4_calendar_framework_timeline": """
            Create comprehensive calendar framework and timeline using:
            
            STRATEGY FOUNDATION:
            {content_strategy_data}
            
            GAP ANALYSIS:
            {gap_analysis_data}
            
            AUDIENCE STRATEGY:
            {audience_platform_data}
            
            PERFORMANCE DATA:
            {performance_data}
            
            Generate calendar framework covering:
            1. Calendar timeline structure and duration optimization
            2. Content frequency planning and posting schedule optimization
            3. Seasonal and trend-based content planning
            4. Campaign integration and promotional content scheduling
            5. Content theme development and weekly/monthly planning
            6. Platform-specific timing and frequency optimization
            7. Content mix distribution and balance planning
            8. Calendar flexibility and adaptation strategy
            
            Focus on creating a robust framework for detailed content planning.
            """,
            
            "step_5_content_pillar_distribution": """
            Develop content pillar distribution strategy using:
            
            CONTENT PILLARS DATA:
            {content_pillars_data}
            
            STRATEGY ALIGNMENT:
            {content_strategy_data}
            
            GAP ANALYSIS:
            {gap_analysis_data}
            
            KEYWORDS DATA:
            {keywords_data}
            
            Generate pillar distribution covering:
            1. Content pillar prioritization and weighting
            2. Pillar-specific content planning and topic development
            3. Pillar balance and variety optimization
            4. Pillar-specific keyword integration and optimization
            5. Pillar performance tracking and optimization planning
            6. Pillar audience alignment and engagement strategy
            7. Pillar content format and platform optimization
            8. Pillar evolution and adaptation strategy
            
            Ensure optimal pillar distribution for comprehensive calendar coverage.
            """,
            
            "step_6_platform_specific_strategy": """
            Develop platform-specific content strategy using:
            
            AUDIENCE STRATEGY:
            {audience_platform_data}
            
            CONTENT PILLARS:
            {content_pillars_data}
            
            PERFORMANCE DATA:
            {performance_data}
            
            AI ANALYSIS:
            {ai_analysis_data}
            
            Generate platform strategy covering:
            1. Platform-specific content format optimization
            2. Platform-specific posting frequency and timing
            3. Platform-specific audience targeting and engagement
            4. Platform-specific content adaptation and optimization
            5. Cross-platform content consistency and brand alignment
            6. Platform-specific performance tracking and optimization
            7. Platform-specific content mix and variety planning
            8. Platform-specific trend integration and adaptation
            
            Optimize for platform-specific success and engagement.
            """,
            
            "step_7_weekly_theme_development": """
            Develop comprehensive weekly themes using:
            
            CALENDAR FRAMEWORK:
            {calendar_framework_data}
            
            CONTENT PILLARS:
            {content_pillars_data}
            
            PLATFORM STRATEGY:
            {platform_strategy_data}
            
            GAP ANALYSIS:
            {gap_analysis_data}
            
            Generate weekly themes covering:
            1. Weekly theme development and topic planning
            2. Theme-specific content variety and balance
            3. Theme audience alignment and engagement optimization
            4. Theme keyword integration and SEO optimization
            5. Theme platform adaptation and format optimization
            6. Theme performance tracking and optimization planning
            7. Theme trend integration and seasonal adaptation
            8. Theme brand alignment and consistency planning
            
            Create engaging and strategic weekly themes for calendar execution.
            """,
            
            "step_8_daily_content_planning": """
            Develop detailed daily content planning using:
            
            WEEKLY THEMES:
            {weekly_themes_data}
            
            PLATFORM STRATEGY:
            {platform_strategy_data}
            
            KEYWORDS DATA:
            {keywords_data}
            
            PERFORMANCE DATA:
            {performance_data}
            
            Generate daily content planning covering:
            1. Daily content topic development and optimization
            2. Daily content format and platform optimization
            3. Daily content timing and frequency optimization
            4. Daily content audience targeting and engagement
            5. Daily content keyword integration and SEO optimization
            6. Daily content performance tracking and optimization
            7. Daily content brand alignment and consistency
            8. Daily content variety and balance optimization
            
            Create detailed, actionable daily content plans for calendar execution.
            """,
            
            "step_9_content_recommendations": """
            Generate comprehensive content recommendations using:
            
            GAP ANALYSIS:
            {gap_analysis_data}
            
            KEYWORDS DATA:
            {keywords_data}
            
            AI ANALYSIS:
            {ai_analysis_data}
            
            PERFORMANCE DATA:
            {performance_data}
            
            Generate content recommendations covering:
            1. High-priority content opportunity identification
            2. Keyword-driven content topic recommendations
            3. Trend-based content opportunity development
            4. Performance-optimized content strategy recommendations
            5. Audience-driven content opportunity identification
            6. Competitive content opportunity analysis
            7. Seasonal and event-based content recommendations
            8. Content optimization and improvement recommendations
            
            Provide actionable content recommendations for calendar enhancement.
            """,
            
            "step_10_performance_optimization": """
            Develop performance optimization strategy using:
            
            PERFORMANCE DATA:
            {performance_data}
            
            AI ANALYSIS:
            {ai_analysis_data}
            
            CALENDAR FRAMEWORK:
            {calendar_framework_data}
            
            CONTENT RECOMMENDATIONS:
            {content_recommendations_data}
            
            Generate performance optimization covering:
            1. Performance metric tracking and optimization planning
            2. Content performance analysis and improvement strategies
            3. Engagement optimization and audience interaction planning
            4. Conversion optimization and goal achievement strategies
            5. ROI optimization and measurement planning
            6. Performance-based content adaptation and optimization
            7. A/B testing strategy and optimization planning
            8. Performance forecasting and predictive optimization
            
            Optimize calendar for maximum performance and ROI achievement.
            """,
            
            "step_11_strategy_alignment_validation": """
            Validate comprehensive strategy alignment using:
            
            CONTENT STRATEGY:
            {content_strategy_data}
            
            CALENDAR FRAMEWORK:
            {calendar_framework_data}
            
            WEEKLY THEMES:
            {weekly_themes_data}
            
            DAILY CONTENT:
            {daily_content_data}
            
            PERFORMANCE OPTIMIZATION:
            {performance_optimization_data}
            
            Generate strategy alignment validation covering:
            1. Business objective alignment and KPI mapping validation
            2. Target audience alignment and engagement validation
            3. Content pillar alignment and distribution validation
            4. Brand voice and editorial guideline compliance validation
            5. Platform strategy alignment and optimization validation
            6. Content quality and consistency validation
            7. Performance optimization alignment validation
            8. Strategic goal achievement validation
            
            Ensure comprehensive alignment with original strategy objectives.
            """,
            
            "step_12_final_calendar_assembly": """
            Perform final calendar assembly and optimization using:
            
            ALL PREVIOUS STEPS DATA:
            {all_steps_data}
            
            STRATEGY ALIGNMENT:
            {strategy_alignment_data}
            
            QUALITY VALIDATION:
            {quality_validation_data}
            
            Generate final calendar assembly covering:
            1. Comprehensive calendar structure and organization
            2. Content quality assurance and optimization
            3. Strategic alignment validation and optimization
            4. Performance optimization and measurement planning
            5. Calendar flexibility and adaptation planning
            6. Quality gate validation and compliance assurance
            7. Calendar execution and monitoring planning
            8. Success metrics and ROI measurement planning
            
            Create the final, optimized calendar ready for execution.
            """
        }
    
    def _load_step_dependencies(self) -> Dict[str, List[str]]:
        """
        Load step dependencies for data context.
        
        Returns:
            Dictionary of step dependencies
        """
        return {
            "step_1_content_strategy_analysis": ["content_strategy"],
            "step_2_gap_analysis": ["content_strategy", "gap_analysis", "keywords", "ai_analysis"],
            "step_3_audience_platform_strategy": ["content_strategy", "gap_analysis", "keywords", "ai_analysis"],
            "step_4_calendar_framework_timeline": ["content_strategy", "gap_analysis", "audience_platform", "performance_data"],
            "step_5_content_pillar_distribution": ["content_pillars", "content_strategy", "gap_analysis", "keywords"],
            "step_6_platform_specific_strategy": ["audience_platform", "content_pillars", "performance_data", "ai_analysis"],
            "step_7_weekly_theme_development": ["calendar_framework", "content_pillars", "platform_strategy", "gap_analysis"],
            "step_8_daily_content_planning": ["weekly_themes", "platform_strategy", "keywords", "performance_data"],
            "step_9_content_recommendations": ["gap_analysis", "keywords", "ai_analysis", "performance_data"],
            "step_10_performance_optimization": ["performance_data", "ai_analysis", "calendar_framework", "content_recommendations"],
            "step_11_strategy_alignment_validation": ["content_strategy", "calendar_framework", "weekly_themes", "daily_content", "performance_optimization"],
            "step_12_final_calendar_assembly": ["all_steps", "strategy_alignment", "quality_validation"]
        }
    
    async def build_prompt(self, step_name: str, user_id: int, strategy_id: int) -> str:
        """
        Build a strategy-aware prompt for a specific step.
        
        Args:
            step_name: Name of the step (e.g., "step_1_content_strategy_analysis")
            user_id: User identifier
            strategy_id: Strategy identifier
            
        Returns:
            Formatted prompt string with data context
        """
        template = self.prompt_templates.get(step_name)
        if not template:
            raise ValueError(f"Prompt template not found for step: {step_name}")
        
        try:
            # Get relevant data context for the step
            data_context = await self._get_data_context(user_id, strategy_id, step_name)
            
            # Format the prompt with data context
            formatted_prompt = template.format(**data_context)
            
            logger.info(f"Built strategy-aware prompt for {step_name}")
            return formatted_prompt
            
        except Exception as e:
            logger.error(f"Error building prompt for {step_name}: {e}")
            raise
    
    async def _get_data_context(self, user_id: int, strategy_id: int, step_name: str) -> Dict[str, Any]:
        """
        Get relevant data context for a specific step.
        
        Args:
            user_id: User identifier
            strategy_id: Strategy identifier
            step_name: Name of the step
            
        Returns:
            Dictionary containing data context for the step
        """
        data_context = {}
        
        # Get dependencies for this step
        dependencies = self.step_dependencies.get(step_name, [])
        
        # Get data from all active sources
        active_sources = self.registry.get_active_sources()
        
        for source_id, source in active_sources.items():
            try:
                # Check if this source is needed for this step
                if source_id in dependencies or "all_steps" in dependencies:
                    source_data = await source.get_data(user_id, strategy_id)
                    data_context[f"{source_id}_data"] = source_data
                    
                    # Add validation results
                    validation = await source.validate_data(source_data)
                    data_context[f"{source_id}_validation"] = validation
                    
                    logger.debug(f"Retrieved data from {source_id} for {step_name}")
                    
            except Exception as e:
                logger.warning(f"Error getting data from {source_id} for {step_name}: {e}")
                data_context[f"{source_id}_data"] = {}
                data_context[f"{source_id}_validation"] = {"is_valid": False, "quality_score": 0.0}
        
        # Add step-specific context
        data_context["step_name"] = step_name
        data_context["user_id"] = user_id
        data_context["strategy_id"] = strategy_id
        data_context["generation_timestamp"] = datetime.utcnow().isoformat()
        
        return data_context
    
    def get_available_steps(self) -> List[str]:
        """
        Get list of available steps.
        
        Returns:
            List of available step names
        """
        return list(self.prompt_templates.keys())
    
    def get_step_dependencies(self, step_name: str) -> List[str]:
        """
        Get dependencies for a specific step.
        
        Args:
            step_name: Name of the step
            
        Returns:
            List of data source dependencies
        """
        return self.step_dependencies.get(step_name, [])
    
    def validate_step_requirements(self, step_name: str) -> Dict[str, Any]:
        """
        Validate requirements for a specific step.
        
        Args:
            step_name: Name of the step
            
        Returns:
            Validation result dictionary
        """
        validation_result = {
            "step_name": step_name,
            "has_template": step_name in self.prompt_templates,
            "dependencies": self.get_step_dependencies(step_name),
            "available_sources": list(self.registry.get_active_sources().keys()),
            "missing_sources": []
        }
        
        # Check for missing data sources
        required_sources = self.get_step_dependencies(step_name)
        available_sources = list(self.registry.get_active_sources().keys())
        
        for source in required_sources:
            if source not in available_sources and source != "all_steps":
                validation_result["missing_sources"].append(source)
        
        validation_result["is_ready"] = (
            validation_result["has_template"] and 
            len(validation_result["missing_sources"]) == 0
        )
        
        return validation_result
    
    def __str__(self) -> str:
        """String representation of the prompt builder."""
        return f"StrategyAwarePromptBuilder(steps={len(self.prompt_templates)}, registry={self.registry})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the prompt builder."""
        return f"StrategyAwarePromptBuilder(steps={list(self.prompt_templates.keys())}, dependencies={self.step_dependencies})"
