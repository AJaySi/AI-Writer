"""
Strategy Quality Assessment

Extracted from calendar_generator_service.py to improve maintainability
and align with 12-step implementation plan.
"""

from typing import Dict, Any, List
from loguru import logger


class StrategyQualityAssessor:
    """Assess strategy quality and prepare data for quality gates and prompt chaining."""
    
    async def analyze_strategy_completeness(self, strategy_dict: Dict[str, Any], enhanced_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze strategy completeness for quality assessment."""
        try:
            # Calculate completion percentage based on available data
            total_fields = 30  # Total strategic input fields
            filled_fields = 0
            
            # Count filled basic fields
            basic_fields = ['name', 'industry', 'target_audience', 'content_pillars', 'ai_recommendations']
            for field in basic_fields:
                if strategy_dict.get(field):
                    filled_fields += 1
            
            # Count filled enhanced fields
            enhanced_fields = [
                'business_objectives', 'target_metrics', 'content_budget', 'team_size',
                'implementation_timeline', 'market_share', 'competitive_position', 'performance_metrics',
                'content_preferences', 'consumption_patterns', 'audience_pain_points', 'buying_journey',
                'seasonal_trends', 'engagement_metrics', 'top_competitors', 'competitor_content_strategies',
                'market_gaps', 'industry_trends', 'emerging_trends', 'preferred_formats', 'content_mix',
                'content_frequency', 'optimal_timing', 'quality_metrics', 'editorial_guidelines', 'brand_voice',
                'traffic_sources', 'conversion_rates', 'content_roi_targets', 'ab_testing_capabilities'
            ]
            
            for field in enhanced_fields:
                if enhanced_data.get(field):
                    filled_fields += 1
            
            completion_percentage = (filled_fields / total_fields) * 100
            
            return {
                "completion_percentage": round(completion_percentage, 2),
                "filled_fields": filled_fields,
                "total_fields": total_fields,
                "missing_critical_fields": self._identify_missing_critical_fields(strategy_dict, enhanced_data),
                "data_quality_score": self._calculate_data_quality_score(strategy_dict, enhanced_data),
                "strategy_coherence": self._assess_strategy_coherence(strategy_dict, enhanced_data)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing strategy completeness: {str(e)}")
            return {"completion_percentage": 0, "filled_fields": 0, "total_fields": 30}
    
    async def calculate_strategy_quality_indicators(self, strategy_dict: Dict[str, Any], enhanced_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate quality indicators for strategy data."""
        try:
            quality_indicators = {
                "data_completeness": 0,
                "data_consistency": 0,
                "strategic_alignment": 0,
                "market_relevance": 0,
                "audience_alignment": 0,
                "content_strategy_coherence": 0,
                "competitive_positioning": 0,
                "performance_readiness": 0,
                "overall_quality_score": 0
            }
            
            # Calculate data completeness
            filled_fields = 0
            total_fields = 30
            for field in ['name', 'industry', 'target_audience', 'content_pillars']:
                if strategy_dict.get(field):
                    filled_fields += 1
            
            quality_indicators["data_completeness"] = (filled_fields / 4) * 100
            
            # Calculate strategic alignment
            if strategy_dict.get("content_pillars") and strategy_dict.get("target_audience"):
                quality_indicators["strategic_alignment"] = 85
            else:
                quality_indicators["strategic_alignment"] = 30
            
            # Calculate market relevance
            if strategy_dict.get("industry"):
                quality_indicators["market_relevance"] = 80
            else:
                quality_indicators["market_relevance"] = 40
            
            # Calculate audience alignment
            if strategy_dict.get("target_audience"):
                quality_indicators["audience_alignment"] = 75
            else:
                quality_indicators["audience_alignment"] = 25
            
            # Calculate content strategy coherence
            if strategy_dict.get("content_pillars") and len(strategy_dict.get("content_pillars", [])) >= 3:
                quality_indicators["content_strategy_coherence"] = 90
            else:
                quality_indicators["content_strategy_coherence"] = 50
            
            # Calculate overall quality score
            scores = [
                quality_indicators["data_completeness"],
                quality_indicators["strategic_alignment"],
                quality_indicators["market_relevance"],
                quality_indicators["audience_alignment"],
                quality_indicators["content_strategy_coherence"]
            ]
            quality_indicators["overall_quality_score"] = sum(scores) / len(scores)
            
            return quality_indicators
            
        except Exception as e:
            logger.error(f"Error calculating quality indicators: {str(e)}")
            return {"overall_quality_score": 0}
    
    async def calculate_data_completeness(self, strategy_dict: Dict[str, Any], enhanced_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate data completeness for quality gates."""
        try:
            completeness = {
                "business_context": 0,
                "audience_intelligence": 0,
                "competitive_intelligence": 0,
                "content_strategy": 0,
                "performance_analytics": 0,
                "overall_completeness": 0
            }
            
            # Business context completeness (8 fields)
            business_fields = ['business_objectives', 'target_metrics', 'content_budget', 'team_size',
                             'implementation_timeline', 'market_share', 'competitive_position', 'performance_metrics']
            filled_business = sum(1 for field in business_fields if enhanced_data.get(field))
            completeness["business_context"] = (filled_business / 8) * 100
            
            # Audience intelligence completeness (6 fields)
            audience_fields = ['content_preferences', 'consumption_patterns', 'audience_pain_points', 
                             'buying_journey', 'seasonal_trends', 'engagement_metrics']
            filled_audience = sum(1 for field in audience_fields if enhanced_data.get(field))
            completeness["audience_intelligence"] = (filled_audience / 6) * 100
            
            # Competitive intelligence completeness (5 fields)
            competitive_fields = ['top_competitors', 'competitor_content_strategies', 'market_gaps', 
                                'industry_trends', 'emerging_trends']
            filled_competitive = sum(1 for field in competitive_fields if enhanced_data.get(field))
            completeness["competitive_intelligence"] = (filled_competitive / 5) * 100
            
            # Content strategy completeness (7 fields)
            content_fields = ['preferred_formats', 'content_mix', 'content_frequency', 'optimal_timing', 
                            'quality_metrics', 'editorial_guidelines', 'brand_voice']
            filled_content = sum(1 for field in content_fields if enhanced_data.get(field))
            completeness["content_strategy"] = (filled_content / 7) * 100
            
            # Performance analytics completeness (4 fields)
            performance_fields = ['traffic_sources', 'conversion_rates', 'content_roi_targets', 'ab_testing_capabilities']
            filled_performance = sum(1 for field in performance_fields if enhanced_data.get(field))
            completeness["performance_analytics"] = (filled_performance / 4) * 100
            
            # Overall completeness
            total_filled = filled_business + filled_audience + filled_competitive + filled_content + filled_performance
            total_fields = 30
            completeness["overall_completeness"] = (total_filled / total_fields) * 100
            
            return completeness
            
        except Exception as e:
            logger.error(f"Error calculating data completeness: {str(e)}")
            return {"overall_completeness": 0}
    
    async def assess_strategic_alignment(self, strategy_dict: Dict[str, Any], enhanced_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess strategic alignment for quality gates."""
        try:
            alignment = {
                "business_objectives_alignment": 0,
                "audience_strategy_alignment": 0,
                "content_strategy_alignment": 0,
                "competitive_positioning_alignment": 0,
                "overall_alignment_score": 0
            }
            
            # Business objectives alignment
            if enhanced_data.get("business_objectives") and strategy_dict.get("content_pillars"):
                alignment["business_objectives_alignment"] = 85
            else:
                alignment["business_objectives_alignment"] = 40
            
            # Audience strategy alignment
            if strategy_dict.get("target_audience") and enhanced_data.get("audience_pain_points"):
                alignment["audience_strategy_alignment"] = 90
            else:
                alignment["audience_strategy_alignment"] = 50
            
            # Content strategy alignment
            if strategy_dict.get("content_pillars") and enhanced_data.get("content_mix"):
                alignment["content_strategy_alignment"] = 80
            else:
                alignment["content_strategy_alignment"] = 45
            
            # Competitive positioning alignment
            if enhanced_data.get("competitive_position") and enhanced_data.get("market_gaps"):
                alignment["competitive_positioning_alignment"] = 75
            else:
                alignment["competitive_positioning_alignment"] = 35
            
            # Overall alignment score
            scores = [
                alignment["business_objectives_alignment"],
                alignment["audience_strategy_alignment"],
                alignment["content_strategy_alignment"],
                alignment["competitive_positioning_alignment"]
            ]
            alignment["overall_alignment_score"] = sum(scores) / len(scores)
            
            return alignment
            
        except Exception as e:
            logger.error(f"Error assessing strategic alignment: {str(e)}")
            return {"overall_alignment_score": 0}
    
    async def prepare_quality_gate_data(self, strategy_dict: Dict[str, Any], enhanced_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for quality gates validation."""
        try:
            quality_gate_data = {
                "content_uniqueness": {
                    "strategy_pillars": strategy_dict.get("content_pillars", []),
                    "content_mix": enhanced_data.get("content_mix", {}),
                    "editorial_guidelines": enhanced_data.get("editorial_guidelines", {})
                },
                "content_mix": {
                    "preferred_formats": enhanced_data.get("preferred_formats", []),
                    "content_frequency": enhanced_data.get("content_frequency", ""),
                    "content_mix_ratios": enhanced_data.get("content_mix", {})
                },
                "chain_context": {
                    "strategy_completeness": await self.analyze_strategy_completeness(strategy_dict, enhanced_data),
                    "quality_indicators": await self.calculate_strategy_quality_indicators(strategy_dict, enhanced_data)
                },
                "calendar_structure": {
                    "implementation_timeline": enhanced_data.get("implementation_timeline", ""),
                    "content_frequency": enhanced_data.get("content_frequency", ""),
                    "optimal_timing": enhanced_data.get("optimal_timing", {})
                },
                "enterprise_standards": {
                    "brand_voice": enhanced_data.get("brand_voice", {}),
                    "editorial_guidelines": enhanced_data.get("editorial_guidelines", {}),
                    "quality_metrics": enhanced_data.get("quality_metrics", {})
                },
                "kpi_integration": {
                    "target_metrics": enhanced_data.get("target_metrics", []),
                    "content_roi_targets": enhanced_data.get("content_roi_targets", {}),
                    "performance_metrics": enhanced_data.get("performance_metrics", {})
                }
            }
            
            return quality_gate_data
            
        except Exception as e:
            logger.error(f"Error preparing quality gate data: {str(e)}")
            return {}
    
    async def prepare_prompt_chain_data(self, strategy_dict: Dict[str, Any], enhanced_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for 12-step prompt chaining."""
        try:
            prompt_chain_data = {
                "phase_1_foundation": {
                    "strategy_analysis": await self.analyze_strategy_completeness(strategy_dict, enhanced_data),
                    "gap_analysis": enhanced_data.get("market_gaps", []),
                    "audience_insights": enhanced_data.get("audience_pain_points", [])
                },
                "phase_2_structure": {
                    "content_pillars": strategy_dict.get("content_pillars", []),
                    "content_mix": enhanced_data.get("content_mix", {}),
                    "implementation_timeline": enhanced_data.get("implementation_timeline", "")
                },
                "phase_3_content": {
                    "preferred_formats": enhanced_data.get("preferred_formats", []),
                    "content_frequency": enhanced_data.get("content_frequency", ""),
                    "editorial_guidelines": enhanced_data.get("editorial_guidelines", {})
                },
                "phase_4_optimization": {
                    "quality_indicators": await self.calculate_strategy_quality_indicators(strategy_dict, enhanced_data),
                    "performance_metrics": enhanced_data.get("performance_metrics", {}),
                    "target_metrics": enhanced_data.get("target_metrics", [])
                }
            }
            
            return prompt_chain_data
            
        except Exception as e:
            logger.error(f"Error preparing prompt chain data: {str(e)}")
            return {}
    
    def _identify_missing_critical_fields(self, strategy_dict: Dict[str, Any], enhanced_data: Dict[str, Any]) -> List[str]:
        """Identify missing critical fields for strategy completion."""
        missing_fields = []
        
        # Critical basic fields
        critical_basic = ['name', 'industry', 'target_audience', 'content_pillars']
        for field in critical_basic:
            if not strategy_dict.get(field):
                missing_fields.append(f"basic_{field}")
        
        # Critical enhanced fields
        critical_enhanced = ['business_objectives', 'content_frequency', 'audience_pain_points']
        for field in critical_enhanced:
            if not enhanced_data.get(field):
                missing_fields.append(f"enhanced_{field}")
        
        return missing_fields
    
    def _calculate_data_quality_score(self, strategy_dict: Dict[str, Any], enhanced_data: Dict[str, Any]) -> float:
        """Calculate overall data quality score."""
        try:
            # Basic strategy quality (40% weight)
            basic_score = 0
            basic_fields = ['name', 'industry', 'target_audience', 'content_pillars', 'ai_recommendations']
            filled_basic = sum(1 for field in basic_fields if strategy_dict.get(field))
            basic_score = (filled_basic / len(basic_fields)) * 100
            
            # Enhanced strategy quality (60% weight)
            enhanced_score = 0
            enhanced_fields = ['business_objectives', 'content_frequency', 'audience_pain_points', 
                             'content_mix', 'editorial_guidelines', 'brand_voice']
            filled_enhanced = sum(1 for field in enhanced_fields if enhanced_data.get(field))
            enhanced_score = (filled_enhanced / len(enhanced_fields)) * 100
            
            # Weighted average
            overall_score = (basic_score * 0.4) + (enhanced_score * 0.6)
            return round(overall_score, 2)
            
        except Exception as e:
            logger.error(f"Error calculating data quality score: {str(e)}")
            return 0.0
    
    def _assess_strategy_coherence(self, strategy_dict: Dict[str, Any], enhanced_data: Dict[str, Any]) -> float:
        """Assess strategy coherence and consistency."""
        try:
            coherence_score = 0
            
            # Check if content pillars align with business objectives
            if strategy_dict.get("content_pillars") and enhanced_data.get("business_objectives"):
                coherence_score += 25
            
            # Check if target audience aligns with audience pain points
            if strategy_dict.get("target_audience") and enhanced_data.get("audience_pain_points"):
                coherence_score += 25
            
            # Check if content mix aligns with preferred formats
            if enhanced_data.get("content_mix") and enhanced_data.get("preferred_formats"):
                coherence_score += 25
            
            # Check if editorial guidelines align with brand voice
            if enhanced_data.get("editorial_guidelines") and enhanced_data.get("brand_voice"):
                coherence_score += 25
            
            return coherence_score
            
        except Exception as e:
            logger.error(f"Error assessing strategy coherence: {str(e)}")
            return 0.0
