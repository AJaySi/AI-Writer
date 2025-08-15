"""
Transparency Service for Autofill Process
Generates educational content and transparency messages for the strategy inputs autofill process.
"""

from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from loguru import logger
import json
from datetime import datetime

class AutofillTransparencyService:
    """Service for generating educational content and transparency messages during autofill process."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_field_confidence_score(self, field_id: str, data_source: str, input_data: Any) -> float:
        """Calculate confidence score for a specific field based on data quality and completeness."""
        
        # Base confidence scores by data source
        source_confidence = {
            'website_analysis': 0.85,
            'research_preferences': 0.92,
            'api_keys': 0.78,
            'onboarding_session': 0.88,
            'unknown': 0.70
        }
        
        base_confidence = source_confidence.get(data_source, 0.70)
        
        # Adjust based on data completeness
        completeness_score = self._calculate_data_completeness(input_data)
        
        # Adjust based on data freshness (if applicable)
        freshness_score = self._calculate_data_freshness(data_source)
        
        # Adjust based on field-specific factors
        field_factor = self._get_field_specific_factor(field_id)
        
        # Calculate final confidence score
        final_confidence = base_confidence * completeness_score * freshness_score * field_factor
        
        # Ensure confidence is between 0.5 and 1.0
        return max(0.5, min(1.0, final_confidence))
    
    def calculate_field_data_quality(self, field_id: str, data_source: str, input_data: Any) -> float:
        """Calculate data quality score for a specific field."""
        
        # Base quality scores by data source
        source_quality = {
            'website_analysis': 0.88,
            'research_preferences': 0.94,
            'api_keys': 0.82,
            'onboarding_session': 0.90,
            'unknown': 0.75
        }
        
        base_quality = source_quality.get(data_source, 0.75)
        
        # Adjust based on data structure and format
        structure_score = self._calculate_data_structure_quality(input_data)
        
        # Adjust based on data consistency
        consistency_score = self._calculate_data_consistency(field_id, input_data)
        
        # Adjust based on field-specific quality factors
        field_quality_factor = self._get_field_quality_factor(field_id)
        
        # Calculate final quality score
        final_quality = base_quality * structure_score * consistency_score * field_quality_factor
        
        # Ensure quality is between 0.6 and 1.0
        return max(0.6, min(1.0, final_quality))
    
    def _calculate_data_completeness(self, input_data: Any) -> float:
        """Calculate data completeness score."""
        if input_data is None:
            return 0.3
        
        if isinstance(input_data, str):
            return 0.8 if len(input_data.strip()) > 10 else 0.5
        
        if isinstance(input_data, (list, tuple)):
            return 0.9 if len(input_data) > 0 else 0.4
        
        if isinstance(input_data, dict):
            # Check if dict has meaningful content
            if len(input_data) == 0:
                return 0.4
            # Check if values are not empty
            non_empty_values = sum(1 for v in input_data.values() if v and str(v).strip())
            return 0.7 + (0.2 * (non_empty_values / len(input_data)))
        
        return 0.8
    
    def _calculate_data_freshness(self, data_source: str) -> float:
        """Calculate data freshness score."""
        # Mock freshness calculation - in real implementation, this would check timestamps
        freshness_scores = {
            'website_analysis': 0.95,  # Usually recent
            'research_preferences': 0.90,  # User-provided, recent
            'api_keys': 0.85,  # Configuration data
            'onboarding_session': 0.92,  # Recent user input
            'unknown': 0.80
        }
        return freshness_scores.get(data_source, 0.80)
    
    def _calculate_data_structure_quality(self, input_data: Any) -> float:
        """Calculate data structure quality score."""
        if input_data is None:
            return 0.5
        
        if isinstance(input_data, str):
            # Check if string is well-formed
            if len(input_data.strip()) > 0:
                return 0.9
            return 0.6
        
        if isinstance(input_data, (list, tuple)):
            # Check if list has proper structure
            if len(input_data) > 0:
                return 0.95
            return 0.7
        
        if isinstance(input_data, dict):
            # Check if dict has proper structure
            if len(input_data) > 0:
                return 0.92
            return 0.6
        
        return 0.8
    
    def _calculate_data_consistency(self, field_id: str, input_data: Any) -> float:
        """Calculate data consistency score."""
        # Mock consistency calculation - in real implementation, this would check against expected formats
        if input_data is None:
            return 0.6
        
        # Field-specific consistency checks
        consistency_factors = {
            'business_objectives': 0.95,
            'target_metrics': 0.92,
            'content_budget': 0.88,
            'team_size': 0.90,
            'implementation_timeline': 0.85,
            'market_share': 0.87,
            'competitive_position': 0.89,
            'performance_metrics': 0.91,
            'content_preferences': 0.93,
            'consumption_patterns': 0.90,
            'audience_pain_points': 0.88,
            'buying_journey': 0.89,
            'seasonal_trends': 0.86,
            'engagement_metrics': 0.92,
            'top_competitors': 0.90,
            'competitor_content_strategies': 0.87,
            'market_gaps': 0.85,
            'industry_trends': 0.88,
            'emerging_trends': 0.84,
            'preferred_formats': 0.93,
            'content_mix': 0.89,
            'content_frequency': 0.91,
            'optimal_timing': 0.88,
            'quality_metrics': 0.90,
            'editorial_guidelines': 0.87,
            'brand_voice': 0.89,
            'traffic_sources': 0.92,
            'conversion_rates': 0.88,
            'content_roi_targets': 0.86,
            'ab_testing_capabilities': 0.90
        }
        
        return consistency_factors.get(field_id, 0.85)
    
    def _get_field_specific_factor(self, field_id: str) -> float:
        """Get field-specific confidence factor."""
        # Some fields are inherently more reliable than others
        field_factors = {
            'business_objectives': 1.0,  # High confidence
            'target_metrics': 0.95,
            'content_budget': 0.90,
            'team_size': 0.92,
            'implementation_timeline': 0.88,
            'market_share': 0.85,
            'competitive_position': 0.87,
            'performance_metrics': 0.93,
            'content_preferences': 0.96,  # User-provided, high confidence
            'consumption_patterns': 0.89,
            'audience_pain_points': 0.86,
            'buying_journey': 0.88,
            'seasonal_trends': 0.84,
            'engagement_metrics': 0.91,
            'top_competitors': 0.89,
            'competitor_content_strategies': 0.85,
            'market_gaps': 0.83,
            'industry_trends': 0.87,
            'emerging_trends': 0.82,
            'preferred_formats': 0.94,
            'content_mix': 0.88,
            'content_frequency': 0.90,
            'optimal_timing': 0.86,
            'quality_metrics': 0.89,
            'editorial_guidelines': 0.85,
            'brand_voice': 0.87,
            'traffic_sources': 0.91,
            'conversion_rates': 0.88,
            'content_roi_targets': 0.85,
            'ab_testing_capabilities': 0.89
        }
        
        return field_factors.get(field_id, 0.85)
    
    def _get_field_quality_factor(self, field_id: str) -> float:
        """Get field-specific quality factor."""
        # Quality factors based on data complexity and reliability
        quality_factors = {
            'business_objectives': 0.95,
            'target_metrics': 0.93,
            'content_budget': 0.90,
            'team_size': 0.92,
            'implementation_timeline': 0.88,
            'market_share': 0.86,
            'competitive_position': 0.89,
            'performance_metrics': 0.94,
            'content_preferences': 0.96,
            'consumption_patterns': 0.91,
            'audience_pain_points': 0.87,
            'buying_journey': 0.89,
            'seasonal_trends': 0.85,
            'engagement_metrics': 0.93,
            'top_competitors': 0.90,
            'competitor_content_strategies': 0.86,
            'market_gaps': 0.84,
            'industry_trends': 0.88,
            'emerging_trends': 0.83,
            'preferred_formats': 0.95,
            'content_mix': 0.89,
            'content_frequency': 0.91,
            'optimal_timing': 0.87,
            'quality_metrics': 0.92,
            'editorial_guidelines': 0.86,
            'brand_voice': 0.88,
            'traffic_sources': 0.93,
            'conversion_rates': 0.89,
            'content_roi_targets': 0.86,
            'ab_testing_capabilities': 0.90
        }
        
        return quality_factors.get(field_id, 0.87)
    
    def get_field_mapping_with_metrics(self, auto_populated_fields: Dict[str, Any], data_sources: Dict[str, str], input_data_points: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get field mapping with confidence scores and data quality metrics."""
        
        field_categories = {
            'Business Context': [
                'business_objectives', 'target_metrics', 'content_budget', 'team_size',
                'implementation_timeline', 'market_share', 'competitive_position', 'performance_metrics'
            ],
            'Audience Intelligence': [
                'content_preferences', 'consumption_patterns', 'audience_pain_points',
                'buying_journey', 'seasonal_trends', 'engagement_metrics'
            ],
            'Competitive Intelligence': [
                'top_competitors', 'competitor_content_strategies', 'market_gaps',
                'industry_trends', 'emerging_trends'
            ],
            'Content Strategy': [
                'preferred_formats', 'content_mix', 'content_frequency', 'optimal_timing',
                'quality_metrics', 'editorial_guidelines', 'brand_voice'
            ],
            'Performance & Analytics': [
                'traffic_sources', 'conversion_rates', 'content_roi_targets', 'ab_testing_capabilities'
            ]
        }
        
        result = []
        
        for category_name, field_ids in field_categories.items():
            category_fields = []
            
            for field_id in field_ids:
                data_source = data_sources.get(field_id, 'unknown')
                input_data = input_data_points.get(field_id)
                field_value = auto_populated_fields.get(field_id)
                
                # Calculate real confidence and quality scores
                confidence_score = self.calculate_field_confidence_score(field_id, data_source, input_data)
                data_quality_score = self.calculate_field_data_quality(field_id, data_source, input_data)
                
                category_fields.append({
                    'fieldId': field_id,
                    'label': field_id.replace('_', ' ').title(),
                    'source': data_source,
                    'value': field_value,
                    'confidence': confidence_score,
                    'dataQuality': data_quality_score,
                    'inputData': input_data
                })
            
            result.append({
                'category': category_name,
                'fields': category_fields
            })
        
        return result

    def get_phase_educational_content(self, phase: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate educational content for a specific phase of the autofill process."""
        
        educational_content = {
            'title': '',
            'description': '',
            'points': [],
            'tips': [],
            'phase': phase,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if phase == 'autofill_initialization':
            educational_content.update({
                'title': 'Initializing Strategy Inputs Generation',
                'description': 'We\'re preparing to analyze your data and generate personalized strategy inputs.',
                'points': [
                    'Analyzing your business context and industry data',
                    'Preparing AI models for strategy input generation',
                    'Setting up data quality assessment frameworks',
                    'Initializing transparency and educational content systems'
                ],
                'tips': [
                    'This phase ensures all systems are ready for optimal generation',
                    'The initialization process adapts to your specific business context',
                    'We\'ll provide real-time transparency throughout the entire process'
                ]
            })
            
        elif phase == 'autofill_data_collection':
            educational_content.update({
                'title': 'Collecting and Analyzing Data Sources',
                'description': 'We\'re gathering and analyzing all available data sources to inform your strategy inputs.',
                'points': [
                    'Retrieving your website analysis and content insights',
                    'Analyzing competitor data and market positioning',
                    'Processing research preferences and target audience data',
                    'Integrating API configurations and external data sources'
                ],
                'tips': [
                    'More comprehensive data leads to more accurate strategy inputs',
                    'We prioritize data quality over quantity for better results',
                    'All data sources are analyzed for relevance and reliability'
                ]
            })
            
        elif phase == 'autofill_data_quality':
            educational_content.update({
                'title': 'Assessing Data Quality and Completeness',
                'description': 'We\'re evaluating the quality and completeness of your data to ensure optimal strategy generation.',
                'points': [
                    'Evaluating data freshness and relevance',
                    'Assessing completeness of business context information',
                    'Analyzing data consistency across different sources',
                    'Identifying potential data gaps and opportunities'
                ],
                'tips': [
                    'High-quality data ensures more accurate and actionable strategy inputs',
                    'We\'ll highlight any data gaps that could impact strategy quality',
                    'Data quality scores help you understand confidence levels'
                ]
            })
            
        elif phase == 'autofill_context_analysis':
            educational_content.update({
                'title': 'Analyzing Business Context and Strategic Framework',
                'description': 'We\'re analyzing your business context to create a strategic framework for content planning.',
                'points': [
                    'Understanding your business objectives and goals',
                    'Analyzing market position and competitive landscape',
                    'Evaluating target audience and customer journey',
                    'Identifying content opportunities and strategic priorities'
                ],
                'tips': [
                    'This analysis forms the foundation for all strategy inputs',
                    'We consider both internal and external factors',
                    'The framework adapts to your specific industry and business model'
                ]
            })
            
        elif phase == 'autofill_strategy_generation':
            educational_content.update({
                'title': 'Generating Strategic Insights and Recommendations',
                'description': 'We\'re generating strategic insights and recommendations based on your data analysis.',
                'points': [
                    'Creating strategic insights from analyzed data',
                    'Generating actionable recommendations for content strategy',
                    'Identifying key opportunities and competitive advantages',
                    'Developing strategic priorities and focus areas'
                ],
                'tips': [
                    'Strategic insights are tailored to your specific business context',
                    'Recommendations are actionable and measurable',
                    'We focus on opportunities that align with your business objectives'
                ]
            })
            
        elif phase == 'autofill_field_generation':
            educational_content.update({
                'title': 'Generating Individual Strategy Input Fields',
                'description': 'We\'re generating specific strategy input fields based on your data and strategic analysis.',
                'points': [
                    'Generating business context and objectives',
                    'Creating audience intelligence and insights',
                    'Developing competitive intelligence and positioning',
                    'Formulating content strategy and performance metrics'
                ],
                'tips': [
                    'Each field is generated with confidence scores and quality metrics',
                    'Fields are validated for consistency and alignment',
                    'You can review and modify any generated field'
                ]
            })
            
        elif phase == 'autofill_quality_validation':
            educational_content.update({
                'title': 'Validating Generated Strategy Inputs',
                'description': 'We\'re validating all generated strategy inputs for quality, consistency, and alignment.',
                'points': [
                    'Checking data quality and completeness',
                    'Validating field consistency and alignment',
                    'Ensuring strategic coherence across all inputs',
                    'Identifying any potential issues or improvements'
                ],
                'tips': [
                    'Quality validation ensures reliable and actionable strategy inputs',
                    'We check for consistency across all generated fields',
                    'Any issues are flagged for your review and consideration'
                ]
            })
            
        elif phase == 'autofill_alignment_check':
            educational_content.update({
                'title': 'Checking Strategy Alignment and Consistency',
                'description': 'We\'re ensuring all strategy inputs are aligned and consistent with your business objectives.',
                'points': [
                    'Verifying alignment with business objectives',
                    'Checking consistency across strategic inputs',
                    'Ensuring coherence with market positioning',
                    'Validating strategic priorities and focus areas'
                ],
                'tips': [
                    'Alignment ensures all strategy inputs work together effectively',
                    'Consistency prevents conflicting strategic directions',
                    'Strategic coherence maximizes the impact of your content strategy'
                ]
            })
            
        elif phase == 'autofill_final_review':
            educational_content.update({
                'title': 'Performing Final Review and Optimization',
                'description': 'We\'re conducting a final review and optimization of all strategy inputs.',
                'points': [
                    'Reviewing all generated strategy inputs',
                    'Optimizing for maximum strategic impact',
                    'Ensuring all inputs are actionable and measurable',
                    'Preparing final strategy input recommendations'
                ],
                'tips': [
                    'Final review ensures optimal quality and strategic value',
                    'Optimization maximizes the effectiveness of your strategy',
                    'All inputs are ready for immediate implementation'
                ]
            })
            
        elif phase == 'autofill_complete':
            educational_content.update({
                'title': 'Strategy Inputs Generation Completed Successfully',
                'description': 'Your strategy inputs have been generated successfully with comprehensive transparency and quality assurance.',
                'points': [
                    'All 30 strategy input fields have been generated',
                    'Quality validation and alignment checks completed',
                    'Confidence scores and data quality metrics provided',
                    'Strategy inputs ready for implementation and review'
                ],
                'tips': [
                    'Review the generated inputs and modify as needed',
                    'Use confidence scores to prioritize high-quality inputs',
                    'The transparency data helps you understand data source influence'
                ]
            })
        
        return educational_content

    def get_transparency_message(self, phase: str, context: Dict[str, Any] = None) -> str:
        """Generate a transparency message for a specific phase."""
        
        messages = {
            'autofill_initialization': 'Starting strategy inputs generation process...',
            'autofill_data_collection': 'Collecting and analyzing data sources from your onboarding and research...',
            'autofill_data_quality': 'Assessing data quality and completeness for optimal strategy generation...',
            'autofill_context_analysis': 'Analyzing your business context and creating strategic framework...',
            'autofill_strategy_generation': 'Generating strategic insights and recommendations using AI...',
            'autofill_field_generation': 'Generating individual strategy input fields based on your data...',
            'autofill_quality_validation': 'Validating generated strategy inputs for quality and consistency...',
            'autofill_alignment_check': 'Checking strategy alignment and consistency across all inputs...',
            'autofill_final_review': 'Performing final review and optimization of strategy inputs...',
            'autofill_complete': 'Strategy inputs generation completed successfully!'
        }
        
        base_message = messages.get(phase, f'Processing phase: {phase}')
        
        # Add context-specific details if available
        if context and 'data_sources' in context:
            data_sources = context['data_sources']
            if data_sources:
                source_count = len(data_sources)
                base_message += f' (Analyzing {source_count} data sources)'
        
        return base_message

    def get_data_source_summary(self, base_context: Dict[str, Any]) -> Dict[str, List[str]]:
        """Get a summary of data sources and their associated fields."""
        
        # Extract data sources from base context
        data_sources = {}
        
        # Website analysis fields
        website_fields = ['business_objectives', 'target_metrics', 'content_budget', 'team_size',
                         'implementation_timeline', 'market_share', 'competitive_position',
                         'performance_metrics', 'engagement_metrics', 'top_competitors',
                         'competitor_content_strategies', 'market_gaps', 'industry_trends',
                         'emerging_trends', 'traffic_sources', 'conversion_rates', 'content_roi_targets']
        
        # Research preferences fields
        research_fields = ['content_preferences', 'consumption_patterns', 'audience_pain_points',
                          'buying_journey', 'seasonal_trends', 'preferred_formats', 'content_mix',
                          'content_frequency', 'optimal_timing', 'quality_metrics', 'editorial_guidelines',
                          'brand_voice']
        
        # API configuration fields
        api_fields = ['ab_testing_capabilities']
        
        # Onboarding session fields (fallback for any remaining fields)
        onboarding_fields = []
        
        # Map fields to data sources
        for field in website_fields:
            data_sources[field] = 'website_analysis'
        
        for field in research_fields:
            data_sources[field] = 'research_preferences'
        
        for field in api_fields:
            data_sources[field] = 'api_keys'
        
        # Group fields by data source
        source_summary = {}
        for field, source in data_sources.items():
            if source not in source_summary:
                source_summary[source] = []
            source_summary[source].append(field)
        
        return source_summary

    def generate_phase_message(self, phase: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate a complete phase message with transparency information."""
        
        message = self.get_transparency_message(phase, context)
        educational_content = self.get_phase_educational_content(phase, context)
        
        return {
            'type': phase,
            'message': message,
            'educational_content': educational_content,
            'timestamp': datetime.utcnow().isoformat(),
            'context': context or {}
        }
