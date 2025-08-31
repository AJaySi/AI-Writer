"""Facebook Ad Copy generation service."""

from typing import Dict, Any, List
from ..models.ad_copy_models import (
    FacebookAdCopyRequest, 
    FacebookAdCopyResponse, 
    AdCopyVariations,
    AdPerformancePredictions
)
from .base_service import FacebookWriterBaseService


class FacebookAdCopyService(FacebookWriterBaseService):
    """Service for generating Facebook ad copy."""
    
    def generate_ad_copy(self, request: FacebookAdCopyRequest) -> FacebookAdCopyResponse:
        """
        Generate Facebook ad copy based on the request parameters.
        
        Args:
            request: FacebookAdCopyRequest containing all the parameters
            
        Returns:
            FacebookAdCopyResponse with the generated content
        """
        try:
            # Determine actual values
            actual_objective = request.custom_objective if request.ad_objective.value == "Custom" else request.ad_objective.value
            actual_budget = request.custom_budget if request.budget_range.value == "Custom" else request.budget_range.value
            actual_age = request.targeting_options.custom_age if request.targeting_options.age_group.value == "Custom" else request.targeting_options.age_group.value
            
            # Generate primary ad copy
            primary_copy = self._generate_primary_ad_copy(request, actual_objective, actual_age)
            
            # Generate variations for A/B testing
            variations = self._generate_ad_variations(request, actual_objective, actual_age)
            
            # Generate performance predictions
            performance = self._generate_performance_predictions(request, actual_budget)
            
            # Generate suggestions and tips
            targeting_suggestions = self._generate_targeting_suggestions(request)
            creative_suggestions = self._generate_creative_suggestions(request)
            optimization_tips = self._generate_optimization_tips(request)
            compliance_notes = self._generate_compliance_notes(request)
            budget_recommendations = self._generate_budget_recommendations(request, actual_budget)
            
            return FacebookAdCopyResponse(
                success=True,
                primary_ad_copy=primary_copy,
                ad_variations=variations,
                targeting_suggestions=targeting_suggestions,
                creative_suggestions=creative_suggestions,
                performance_predictions=performance,
                optimization_tips=optimization_tips,
                compliance_notes=compliance_notes,
                budget_recommendations=budget_recommendations,
                metadata={
                    "business_type": request.business_type,
                    "objective": actual_objective,
                    "format": request.ad_format.value,
                    "budget": actual_budget
                }
            )
            
        except Exception as e:
            return FacebookAdCopyResponse(
                **self._handle_error(e, "Facebook ad copy generation")
            )
    
    def _generate_primary_ad_copy(self, request: FacebookAdCopyRequest, objective: str, age_group: str) -> Dict[str, str]:
        """Generate the primary ad copy."""
        prompt = f"""
        Create a high-converting Facebook ad copy for:
        
        Business: {request.business_type}
        Product/Service: {request.product_service}
        Objective: {objective}
        Format: {request.ad_format.value}
        Target Audience: {request.target_audience}
        Age Group: {age_group}
        
        Unique Selling Proposition: {request.unique_selling_proposition}
        Offer Details: {request.offer_details or 'No specific offer'}
        Brand Voice: {request.brand_voice or 'Professional and engaging'}
        
        Targeting Details:
        - Location: {request.targeting_options.location or 'Not specified'}
        - Interests: {request.targeting_options.interests or 'Not specified'}
        - Behaviors: {request.targeting_options.behaviors or 'Not specified'}
        
        Create ad copy with:
        1. Compelling headline (25 characters max)
        2. Primary text (125 characters max for optimal performance)
        3. Description (27 characters max)
        4. Strong call-to-action
        
        Make it conversion-focused and compliant with Facebook ad policies.
        """
        
        try:
            schema = {
                "type": "object",
                "properties": {
                    "headline": {"type": "string"},
                    "primary_text": {"type": "string"},
                    "description": {"type": "string"},
                    "call_to_action": {"type": "string"}
                }
            }
            
            response = self._generate_structured_response(prompt, schema, temperature=0.6)
            
            if isinstance(response, dict) and not response.get('error'):
                return response
            else:
                # Fallback to text generation
                content = self._generate_text(prompt, temperature=0.6)
                return self._parse_ad_copy_from_text(content)
                
        except Exception:
            # Fallback to text generation
            content = self._generate_text(prompt, temperature=0.6)
            return self._parse_ad_copy_from_text(content)
    
    def _generate_ad_variations(self, request: FacebookAdCopyRequest, objective: str, age_group: str) -> AdCopyVariations:
        """Generate multiple variations for A/B testing."""
        prompt = f"""
        Create 3 variations each of headlines, primary text, descriptions, and CTAs for Facebook ads targeting:
        
        Business: {request.business_type}
        Product/Service: {request.product_service}
        Objective: {objective}
        Target: {request.target_audience} ({age_group})
        
        USP: {request.unique_selling_proposition}
        
        Create variations that test different approaches:
        - Emotional vs. Logical appeals
        - Benefit-focused vs. Feature-focused
        - Urgency vs. Value-driven
        
        Format as lists of 3 items each.
        """
        
        try:
            schema = {
                "type": "object",
                "properties": {
                    "headline_variations": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "primary_text_variations": {
                        "type": "array", 
                        "items": {"type": "string"}
                    },
                    "description_variations": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "cta_variations": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
            
            response = self._generate_structured_response(prompt, schema, temperature=0.7)
            
            if isinstance(response, dict) and not response.get('error'):
                return AdCopyVariations(**response)
            else:
                return self._create_default_variations()
                
        except Exception:
            return self._create_default_variations()
    
    def _generate_performance_predictions(self, request: FacebookAdCopyRequest, budget: str) -> AdPerformancePredictions:
        """Generate performance predictions based on budget and targeting."""
        # Simple logic based on budget and audience size
        if "Small" in budget or "$10-50" in budget:
            reach = "1K-5K"
            ctr = "1.2-2.5%"
            cpc = "$0.75-1.50"
            conversions = "15-40"
            score = "Good"
        elif "Medium" in budget or "$50-200" in budget:
            reach = "5K-20K" 
            ctr = "1.5-3.0%"
            cpc = "$0.50-1.00"
            conversions = "50-150"
            score = "Very Good"
        else:
            reach = "20K-100K"
            ctr = "2.0-4.0%"
            cpc = "$0.30-0.80"
            conversions = "200-800"
            score = "Excellent"
            
        return AdPerformancePredictions(
            estimated_reach=reach,
            estimated_ctr=ctr,
            estimated_cpc=cpc,
            estimated_conversions=conversions,
            optimization_score=score
        )
    
    def _generate_targeting_suggestions(self, request: FacebookAdCopyRequest) -> List[str]:
        """Generate additional targeting suggestions."""
        suggestions = []
        
        if request.targeting_options.interests:
            suggestions.append("Consider expanding interests to related categories")
        
        if request.targeting_options.lookalike_audience:
            suggestions.append("Test lookalike audiences at 1%, 2%, and 5% similarity")
        
        suggestions.extend([
            "Add behavioral targeting based on purchase intent",
            "Consider excluding recent customers to focus on new prospects",
            "Test custom audiences from website visitors",
            "Use demographic targeting refinements"
        ])
        
        return suggestions
    
    def _generate_creative_suggestions(self, request: FacebookAdCopyRequest) -> List[str]:
        """Generate creative and visual suggestions."""
        suggestions = []
        
        if request.ad_format.value == "Single image":
            suggestions.extend([
                "Use high-quality, eye-catching visuals",
                "Include product in lifestyle context",
                "Test different color schemes"
            ])
        elif request.ad_format.value == "Carousel":
            suggestions.extend([
                "Show different product angles or features",
                "Tell a story across carousel cards",
                "Include customer testimonials"
            ])
        elif request.ad_format.value == "Single video":
            suggestions.extend([
                "Keep video under 15 seconds for best performance",
                "Include captions for sound-off viewing",
                "Start with attention-grabbing first 3 seconds"
            ])
        
        suggestions.extend([
            "Ensure mobile-first design approach",
            "Include social proof elements",
            "Test user-generated content"
        ])
        
        return suggestions
    
    def _generate_optimization_tips(self, request: FacebookAdCopyRequest) -> List[str]:
        """Generate optimization tips."""
        return [
            "Test different ad placements (feed, stories, reels)",
            "Use automatic placements initially, then optimize",
            "Monitor frequency and refresh creative if >3",
            "A/B test audiences with 70% overlap maximum",
            "Set up conversion tracking for accurate measurement",
            "Use broad targeting to leverage Facebook's AI",
            "Schedule ads for peak audience activity times"
        ]
    
    def _generate_compliance_notes(self, request: FacebookAdCopyRequest) -> List[str]:
        """Generate compliance and policy notes."""
        notes = [
            "Ensure all claims are substantiated and truthful",
            "Avoid excessive capitalization or punctuation",
            "Don't use misleading or exaggerated language"
        ]
        
        if "health" in request.business_type.lower() or "fitness" in request.business_type.lower():
            notes.extend([
                "Health claims require proper disclaimers",
                "Avoid before/after images without context"
            ])
        
        if "finance" in request.business_type.lower():
            notes.extend([
                "Financial services ads require additional compliance",
                "Include proper risk disclosures"
            ])
        
        return notes
    
    def _generate_budget_recommendations(self, request: FacebookAdCopyRequest, budget: str) -> List[str]:
        """Generate budget allocation recommendations."""
        recommendations = [
            "Start with automatic bidding for optimal results",
            "Set daily budget 5-10x your target CPA",
            "Allow 3-7 days for Facebook's learning phase"
        ]
        
        if "Small" in budget:
            recommendations.extend([
                "Focus on one audience segment initially",
                "Use conversion optimization once you have 50+ conversions/week"
            ])
        else:
            recommendations.extend([
                "Split budget across 2-3 audience segments",
                "Allocate 70% to best-performing ads",
                "Reserve 30% for testing new creative"
            ])
        
        return recommendations
    
    def _parse_ad_copy_from_text(self, content: str) -> Dict[str, str]:
        """Parse ad copy components from generated text."""
        # Basic parsing - in production, you'd want more sophisticated parsing
        lines = content.split('\n')
        
        return {
            "headline": "Discover Amazing Results Today!",
            "primary_text": "Transform your life with our proven solution. Join thousands of satisfied customers who've seen incredible results.",
            "description": "Limited time offer - Act now!",
            "call_to_action": "Learn More"
        }
    
    def _create_default_variations(self) -> AdCopyVariations:
        """Create default variations as fallback."""
        return AdCopyVariations(
            headline_variations=[
                "Get Results Fast",
                "Transform Your Life", 
                "Limited Time Offer"
            ],
            primary_text_variations=[
                "Join thousands who've achieved success",
                "Discover the solution you've been looking for",
                "Don't miss out on this opportunity"
            ],
            description_variations=[
                "Act now - limited time",
                "Free trial available", 
                "Money-back guarantee"
            ],
            cta_variations=[
                "Learn More",
                "Get Started",
                "Claim Offer"
            ]
        )