"""
Content Quality Analyzer Service for ALwrity

This service provides comprehensive quality assessment for generated content,
evaluating factual accuracy, source verification, professional tone, and industry relevance.

Key Features:
- Factual accuracy scoring against source verification
- Professional tone analysis for enterprise content
- Industry relevance metrics and assessment
- Overall quality scoring and recommendations
- Content quality tracking over time

Dependencies:
- re (for pattern matching)
- typing (for type hints)
- logging (for debugging)

Author: ALwrity Team
Version: 1.0
Last Updated: January 2025
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from loguru import logger

class ContentQualityAnalyzer:
    """
    Service for analyzing and scoring content quality.
    
    This service evaluates content across multiple dimensions including
    factual accuracy, professional tone, industry relevance, and overall quality.
    """
    
    def __init__(self):
        """Initialize the Content Quality Analyzer."""
        # Professional tone indicators
        self.professional_indicators = [
            "research", "analysis", "insights", "trends", "strategies",
            "implementation", "optimization", "innovation", "development",
            "leadership", "expertise", "professional", "industry", "enterprise"
        ]
        
        # Unprofessional tone indicators
        self.unprofessional_indicators = [
            "awesome", "amazing", "incredible", "mind-blowing", "crazy",
            "totally", "absolutely", "literally", "basically", "actually",
            "you know", "like", "um", "uh", "lol", "omg"
        ]
        
        # Industry-specific terminology patterns
        self.industry_terminology = {
            "Technology": ["ai", "machine learning", "automation", "digital transformation", "cloud computing"],
            "Healthcare": ["patient care", "medical", "treatment", "diagnosis", "healthcare"],
            "Finance": ["investment", "market", "financial", "portfolio", "risk management"],
            "Marketing": ["brand", "campaign", "audience", "conversion", "engagement"],
            "Education": ["learning", "curriculum", "pedagogy", "student", "academic"]
        }
        
        logger.info("Content Quality Analyzer initialized successfully")
    
    def analyze_content_quality(
        self, 
        content: str, 
        sources: List[Dict[str, Any]], 
        industry: str = "general"
    ) -> Dict[str, Any]:
        """
        Analyze content quality across multiple dimensions.
        
        Args:
            content: The content to analyze
            sources: List of research sources used
            industry: The target industry for relevance assessment
            
        Returns:
            Comprehensive quality analysis results
        """
        try:
            # Analyze different quality aspects
            logger.info("🔍 [Quality Analysis] Starting content quality analysis")
            logger.info(f"🔍 [Quality Analysis] Content length: {len(content)} characters")
            logger.info(f"🔍 [Quality Analysis] Sources count: {len(sources)}")
            
            factual_accuracy = self._assess_factual_accuracy(content, sources)
            logger.info(f"🔍 [Quality Analysis] Factual accuracy score: {factual_accuracy}")
            
            source_verification = self._assess_source_verification(content, sources)
            logger.info(f"🔍 [Quality Analysis] Source verification score: {source_verification}")
            
            professional_tone = self._assess_professional_tone(content)
            logger.info(f"🔍 [Quality Analysis] Professional tone score: {professional_tone}")
            
            industry_relevance = self._assess_industry_relevance(content, industry)
            logger.info(f"🔍 [Quality Analysis] Industry relevance score: {industry_relevance}")
            
            citation_coverage = self._assess_citation_coverage(content, sources)
            logger.info(f"🔍 [Quality Analysis] Citation coverage score: {citation_coverage}")
            
            # Calculate overall quality score
            overall_score = self._calculate_overall_score({
                "factual_accuracy": factual_accuracy,
                "source_verification": source_verification,
                "professional_tone": professional_tone,
                "industry_relevance": industry_relevance,
                "citation_coverage": citation_coverage
            })
            logger.info(f"🔍 [Quality Analysis] Overall score calculated: {overall_score}")
            
            # Generate recommendations
            recommendations = self._generate_recommendations({
                "factual_accuracy": factual_accuracy,
                "source_verification": source_verification,
                "professional_tone": professional_tone,
                "industry_relevance": industry_relevance,
                "citation_coverage": citation_coverage
            })
            logger.info(f"🔍 [Quality Analysis] Generated {len(recommendations)} recommendations")
            
            result = {
                "overall_score": overall_score,
                "metrics": {
                    "factual_accuracy": factual_accuracy,
                    "source_verification": source_verification,
                    "professional_tone": professional_tone,
                    "industry_relevance": industry_relevance,
                    "citation_coverage": citation_coverage
                },
                "recommendations": recommendations,
                "content_length": len(content),
                "word_count": len(content.split()),
                "analysis_timestamp": self._get_timestamp()
            }
            
            logger.info(f"🔍 [Quality Analysis] Final result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Content quality analysis failed: {str(e)}")
            return {
                "overall_score": 0.0,
                "error": str(e),
                "metrics": {},
                "recommendations": ["Content quality analysis failed. Please try again."]
            }
    
    def _assess_factual_accuracy(self, content: str, sources: List[Dict[str, Any]]) -> float:
        """
        Assess factual accuracy based on source verification.
        
        Args:
            content: The content to analyze
            sources: Research sources used
            
        Returns:
            Factual accuracy score between 0.0 and 1.0
        """
        logger.info(f"🔍 [Factual Accuracy] Starting analysis with {len(sources)} sources")
        logger.info(f"🔍 [Factual Accuracy] Content length: {len(content)} characters")
        
        if not sources:
            logger.warning("🔍 [Factual Accuracy] No sources provided, returning 0.0")
            return 0.0
        
        # Look for factual indicators in the content
        factual_indicators = [
            r'\d+%', r'\d+ percent',  # Percentages
            r'\$\d+', r'\d+ dollars',  # Dollar amounts
            r'\d+ million', r'\d+ billion',  # Billions
            r'research shows', r'studies indicate', r'data reveals',
            r'experts say', r'according to', r'statistics show',
            r'\d{4}',  # Years
            r'\d+ organizations', r'\d+ companies', r'\d+ enterprises',
            r'AI', r'artificial intelligence', r'machine learning',  # Technology terms
            r'content creation', r'digital marketing', r'technology industry',  # Industry terms
            r'efficiency', r'innovation', r'development', r'growth',  # Business terms
            r'businesses', r'companies', r'organizations',  # Entity terms
            r'tools', r'platforms', r'systems', r'solutions'  # Product terms
        ]
        
        factual_claims = 0
        supported_claims = 0
        
        for pattern in factual_indicators:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                logger.info(f"🔍 [Factual Accuracy] Pattern {pattern} found {len(matches)} matches: {matches}")
            factual_claims += len(matches)
            
            # Check if claims are near citations
            for match in matches:
                if self._is_claim_supported(match, content, sources):
                    supported_claims += 1
        
        logger.info(f"🔍 [Factual Accuracy] Total factual claims: {factual_claims}")
        logger.info(f"🔍 [Factual Accuracy] Supported claims: {supported_claims}")
        
        # Calculate accuracy score - be more lenient
        if factual_claims == 0:
            logger.info("🔍 [Factual Accuracy] No factual claims to verify, returning 0.8")
            return 0.8  # No factual claims to verify
        
        # Base accuracy score
        accuracy_score = supported_claims / factual_claims
        logger.info(f"🔍 [Factual Accuracy] Base accuracy score: {accuracy_score}")
        
        # Boost score if we have good source quality
        if sources:
            avg_credibility = sum(
                (s.credibility_score or 0) if hasattr(s, 'credibility_score') else (s.get("credibility_score", 0) or 0)
                for s in sources
            ) / len(sources)
            
            logger.info(f"🔍 [Factual Accuracy] Average credibility: {avg_credibility}")
            
            # Boost accuracy if sources are credible
            if avg_credibility > 0.7:
                accuracy_score = min(accuracy_score * 1.3, 1.0)
                logger.info(f"🔍 [Factual Accuracy] Applied high credibility boost: {accuracy_score}")
            elif avg_credibility > 0.5:
                accuracy_score = min(accuracy_score * 1.1, 1.0)
                logger.info(f"🔍 [Factual Accuracy] Applied medium credibility boost: {accuracy_score}")
        
        # Boost score if we have multiple sources (diversity)
        if len(sources) >= 3:
            accuracy_score = min(accuracy_score * 1.2, 1.0)
            logger.info(f"🔍 [Factual Accuracy] Applied diversity boost: {accuracy_score}")
        
        final_score = round(min(accuracy_score, 1.0), 3)
        logger.info(f"🔍 [Factual Accuracy] Final accuracy score: {final_score}")
        return final_score
    
    def _assess_source_verification(self, content: str, sources: List[Dict[str, Any]]) -> float:
        """
        Assess source verification quality.
        
        Args:
            content: The content to analyze
            sources: Research sources used
            
        Returns:
            Source verification score between 0.0 and 1.0
        """
        if not sources:
            return 0.0
        
        # Calculate source quality metrics
        total_sources = len(sources)
        
        # Source credibility scores - handle both Dict and ResearchSource objects
        credibility_scores = []
        relevance_scores = []
        domain_scores = []
        source_types = set()
        
        for s in sources:
            if hasattr(s, 'credibility_score'):
                # ResearchSource Pydantic model
                credibility_scores.append(s.credibility_score or 0)
                relevance_scores.append(s.relevance_score or 0)
                domain_scores.append(s.domain_authority or 0)
                source_types.add(s.source_type or "general")
            else:
                # Dictionary object
                credibility_scores.append(s.get("credibility_score", 0))
                relevance_scores.append(s.get("relevance_score", 0))
                domain_scores.append(s.get("domain_authority", 0))
                source_types.add(s.get("source_type", "general"))
        
        avg_credibility = sum(credibility_scores) / len(credibility_scores) if credibility_scores else 0
        avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0
        avg_domain_authority = sum(domain_scores) / len(domain_scores) if domain_scores else 0
        diversity_score = min(len(source_types) / 3, 1.0)  # Normalize to 3+ types
        
        # Calculate verification score
        verification_score = (
            avg_credibility * 0.3 +
            avg_relevance * 0.3 +
            avg_domain_authority * 0.2 +
            diversity_score * 0.2
        )
        
        return round(verification_score, 3)
    
    def _assess_professional_tone(self, content: str) -> float:
        """
        Assess professional tone appropriateness.
        
        Args:
            content: The content to analyze
            
        Returns:
            Professional tone score between 0.0 and 1.0
        """
        content_lower = content.lower()
        
        # Count professional indicators
        professional_count = sum(1 for indicator in self.professional_indicators if indicator in content_lower)
        
        # Count unprofessional indicators
        unprofessional_count = sum(1 for indicator in self.unprofessional_indicators if indicator in content_lower)
        
        # Calculate tone score
        total_indicators = len(self.professional_indicators) + len(self.unprofessional_indicators)
        
        if total_indicators == 0:
            return 0.7  # Neutral score
        
        professional_score = professional_count / len(self.professional_indicators)
        unprofessional_penalty = unprofessional_count / len(self.unprofessional_indicators)
        
        tone_score = professional_score - unprofessional_penalty
        tone_score = max(0.0, min(1.0, tone_score))  # Clamp between 0 and 1
        
        return round(tone_score, 3)
    
    def _assess_industry_relevance(self, content: str, industry: str) -> float:
        """
        Assess industry relevance of the content.
        
        Args:
            content: The content to analyze
            industry: The target industry
            
        Returns:
            Industry relevance score between 0.0 and 1.0
        """
        if industry.lower() == "general":
            return 0.7  # Neutral score for general industry
        
        content_lower = content.lower()
        industry_lower = industry.lower()
        
        # Get industry-specific terminology
        industry_terms = self.industry_terminology.get(industry, [])
        
        # Count industry-specific terms
        industry_term_count = sum(1 for term in industry_terms if term in content_lower)
        
        # Count industry mentions
        industry_mentions = content_lower.count(industry_lower)
        
        # Calculate relevance score
        if not industry_terms:
            return 0.6  # Fallback score
        
        term_relevance = min(industry_term_count / len(industry_terms), 1.0)
        mention_relevance = min(industry_mentions / 3, 1.0)  # Normalize to 3+ mentions
        
        relevance_score = (term_relevance * 0.7) + (mention_relevance * 0.3)
        
        return round(relevance_score, 3)
    
    def _assess_citation_coverage(self, content: str, sources: List[Dict[str, Any]]) -> float:
        """
        Assess citation coverage in the content.
        
        Args:
            content: The content to analyze
            sources: Research sources used
            
        Returns:
            Citation coverage score between 0.0 and 1.0
        """
        logger.info(f"🔍 [Citation Coverage] Starting analysis with {len(sources)} sources")
        logger.info(f"🔍 [Citation Coverage] Content length: {len(content)} characters")
        
        # Debug: Show sample of content to see what we're analyzing
        content_sample = content[:500] + "..." if len(content) > 500 else content
        logger.info(f"🔍 [Citation Coverage] Content sample: {content_sample}")
        
        if not sources:
            logger.warning("🔍 [Citation Coverage] No sources provided, returning 0.0")
            return 0.0
        
        # Look for citation patterns - updated to match our actual citation format
        citation_patterns = [
            r'<sup class="liw-cite"[^>]*>\[(\d+)\]</sup>',  # HTML format - PRIORITY 1
            r'\[(\d+)\]',  # Our primary format: [1], [2], etc.
            r'\[Source (\d+)\]', r'\(Source (\d+)\)',
            r'\((\d+)\)', r'Source (\d+)', r'Ref\. (\d+)', r'Reference (\d+)'
        ]
        
        total_citations = 0
        for pattern in citation_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                logger.info(f"🔍 [Citation Coverage] Pattern {pattern} found {len(matches)} matches: {matches}")
            total_citations += len(matches)
        
        logger.info(f"🔍 [Citation Coverage] Total citations found: {total_citations}")
        
        # Calculate coverage score - be more lenient since we strategically place citations
        expected_citations = min(len(sources), len(sources) * 0.8)  # Allow 80% coverage
        if expected_citations == 0:
            logger.warning("🔍 [Citation Coverage] Expected citations is 0, returning 0.0")
            return 0.0
            
        coverage_score = min(total_citations / expected_citations, 1.0)
        logger.info(f"🔍 [Citation Coverage] Coverage score before boost: {coverage_score}")
        
        # Boost score if we have good source diversity
        if len(sources) >= 3:
            coverage_score = min(coverage_score * 1.2, 1.0)
            logger.info(f"🔍 [Citation Coverage] Applied diversity boost, final score: {coverage_score}")
        
        final_score = round(coverage_score, 3)
        logger.info(f"🔍 [Citation Coverage] Final coverage score: {final_score}")
        return final_score
    
    def _is_claim_supported(self, claim: str, content: str, sources: List[Dict[str, Any]]) -> bool:
        """
        Check if a factual claim is supported by nearby citations.
        
        Args:
            claim: The factual claim to check
            content: The content containing the claim
            sources: Research sources used
            
        Returns:
            True if the claim appears to be supported
        """
        # Find the position of the claim
        claim_pos = content.lower().find(claim.lower())
        if claim_pos == -1:
            return False
        
        # Look for citations within 300 characters of the claim (increased range)
        start_pos = max(0, claim_pos - 150)
        end_pos = min(len(content), claim_pos + len(claim) + 150)
        
        nearby_text = content[start_pos:end_pos]
        
        # Check for citation patterns - updated to match our actual format
        citation_patterns = [
            r'<sup class="liw-cite"[^>]*>\[(\d+)\]</sup>',  # HTML format - PRIORITY 1
            r'\[(\d+)\]',  # Our primary format: [1], [2], etc.
            r'\[Source (\d+)\]', r'\[(\d+)\]', r'\(Source (\d+)\)',
            r'\((\d+)\)', r'Source (\d+)', r'Ref\. (\d+)', r'Reference (\d+)'
        ]
        
        for pattern in citation_patterns:
            if re.search(pattern, nearby_text, re.IGNORECASE):
                return True
        
        return False
    
    def _calculate_overall_score(self, metrics: Dict[str, float]) -> float:
        """
        Calculate overall quality score from individual metrics.
        
        Args:
            metrics: Dictionary of quality metrics
            
        Returns:
            Overall quality score between 0.0 and 1.0
        """
        # Weighted scoring system
        weights = {
            "factual_accuracy": 0.25,
            "source_verification": 0.25,
            "professional_tone": 0.20,
            "industry_relevance": 0.15,
            "citation_coverage": 0.15
        }
        
        overall_score = 0.0
        total_weight = 0.0
        
        for metric_name, weight in weights.items():
            if metric_name in metrics:
                overall_score += metrics[metric_name] * weight
                total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        final_score = overall_score / total_weight
        return round(final_score, 3)
    
    def _generate_recommendations(self, metrics: Dict[str, float]) -> List[str]:
        """
        Generate improvement recommendations based on quality metrics.
        
        Args:
            metrics: Dictionary of quality metrics
            
        Returns:
            List of improvement recommendations
        """
        recommendations = []
        
        # Factual accuracy recommendations
        if metrics.get("factual_accuracy", 0) < 0.7:
            recommendations.append("Improve factual accuracy by ensuring all claims are properly supported by sources.")
        
        if metrics.get("factual_accuracy", 0) < 0.5:
            recommendations.append("Significant factual accuracy issues detected. Review and verify all claims against sources.")
        
        # Source verification recommendations
        if metrics.get("source_verification", 0) < 0.6:
            recommendations.append("Enhance source quality by using more credible and relevant sources.")
        
        if metrics.get("source_verification", 0) < 0.4:
            recommendations.append("Low source verification quality. Consider using more authoritative and recent sources.")
        
        # Professional tone recommendations
        if metrics.get("professional_tone", 0) < 0.7:
            recommendations.append("Improve professional tone by using more industry-appropriate language.")
        
        if metrics.get("professional_tone", 0) < 0.5:
            recommendations.append("Content tone needs significant improvement for professional audiences.")
        
        # Industry relevance recommendations
        if metrics.get("industry_relevance", 0) < 0.6:
            recommendations.append("Increase industry relevance by using more industry-specific terminology and examples.")
        
        if metrics.get("industry_relevance", 0) < 0.4:
            recommendations.append("Content lacks industry focus. Add more industry-specific content and context.")
        
        # Citation coverage recommendations
        if metrics.get("citation_coverage", 0) < 0.8:
            recommendations.append("Improve citation coverage by adding more inline citations throughout the content.")
        
        if metrics.get("citation_coverage", 0) < 0.5:
            recommendations.append("Low citation coverage. Add citations for all factual claims and data points.")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Content quality is good. Consider adding more specific examples or expanding on key points.")
        
        return recommendations
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for analysis tracking."""
        from datetime import datetime
        return datetime.utcnow().isoformat()
    
    def track_quality_over_time(
        self, 
        content_id: str, 
        quality_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Track content quality metrics over time for analysis.
        
        Args:
            content_id: Unique identifier for the content
            quality_metrics: Quality analysis results
            
        Returns:
            Tracking information and trends
        """
        # This would typically integrate with a database or analytics system
        # For now, we'll return the tracking structure
        
        tracking_data = {
            "content_id": content_id,
            "timestamp": quality_metrics.get("analysis_timestamp"),
            "overall_score": quality_metrics.get("overall_score", 0.0),
            "metrics": quality_metrics.get("metrics", {}),
            "content_length": quality_metrics.get("content_length", 0),
            "word_count": quality_metrics.get("word_count", 0)
        }
        
        logger.info(f"Quality metrics tracked for content {content_id}: {tracking_data['overall_score']}")
        
        return {
            "tracked": True,
            "tracking_data": tracking_data,
            "message": f"Quality metrics tracked for content {content_id}"
        }
    
    def compare_content_quality(
        self, 
        content_a: Dict[str, Any], 
        content_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compare quality between two pieces of content.
        
        Args:
            content_a: Quality metrics for first content piece
            content_b: Quality metrics for second content piece
            
        Returns:
            Comparison analysis and recommendations
        """
        comparison = {
            "content_a_score": content_a.get("overall_score", 0.0),
            "content_b_score": content_b.get("overall_score", 0.0),
            "score_difference": 0.0,
            "better_content": "content_a",
            "improvement_areas": [],
            "strength_areas": []
        }
        
        # Calculate score difference
        score_a = content_a.get("overall_score", 0.0)
        score_b = content_b.get("overall_score", 0.0)
        comparison["score_difference"] = round(abs(score_a - score_b), 3)
        
        # Determine better content
        if score_a > score_b:
            comparison["better_content"] = "content_a"
            better_metrics = content_a.get("metrics", {})
            worse_metrics = content_b.get("metrics", {})
        else:
            comparison["better_content"] = "content_b"
            better_metrics = content_b.get("metrics", {})
            worse_metrics = content_a.get("metrics", {})
        
        # Identify improvement areas
        for metric_name in better_metrics:
            if metric_name in worse_metrics:
                if worse_metrics[metric_name] < better_metrics[metric_name] - 0.2:
                    comparison["improvement_areas"].append(f"Improve {metric_name.replace('_', ' ')}")
        
        # Identify strength areas
        for metric_name in better_metrics:
            if better_metrics[metric_name] > 0.8:
                comparison["strength_areas"].append(f"Strong {metric_name.replace('_', ' ')}")
        
        return comparison
    
    def generate_quality_report(
        self, 
        content: str, 
        sources: List[Any], 
        industry: str = "general"
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive quality report for content.
        
        Args:
            content: The content to analyze
            sources: Research sources used (can be Dict or ResearchSource objects)
            industry: Target industry
            
        Returns:
            Comprehensive quality report
        """
        # Perform full quality analysis
        quality_analysis = self.analyze_content_quality(content, sources, industry)
        
        # Generate detailed report
        report = {
            "summary": {
                "overall_score": quality_analysis["overall_score"],
                "quality_level": self._get_quality_level(quality_analysis["overall_score"]),
                "content_length": quality_analysis["content_length"],
                "word_count": quality_analysis["word_count"]
            },
            "detailed_metrics": quality_analysis["metrics"],
            "recommendations": quality_analysis["recommendations"],
            "source_analysis": {
                "total_sources": len(sources),
                "source_types": self._extract_source_types(sources),
                "avg_credibility": self._calculate_avg_score(sources, "credibility_score"),
                "avg_relevance": self._calculate_avg_score(sources, "relevance_score")
            },
            "improvement_plan": self._generate_improvement_plan(quality_analysis["metrics"]),
            "analysis_timestamp": quality_analysis["analysis_timestamp"]
        }
        
        return report
    
    def _get_quality_level(self, score: float) -> str:
        """Convert numerical score to quality level description."""
        if score >= 0.9:
            return "Excellent"
        elif score >= 0.8:
            return "Very Good"
        elif score >= 0.7:
            return "Good"
        elif score >= 0.6:
            return "Fair"
        elif score >= 0.5:
            return "Below Average"
        else:
            return "Poor"
    
    def _generate_improvement_plan(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Generate a structured improvement plan based on quality metrics.
        
        Args:
            metrics: Quality metrics dictionary
            
        Returns:
            Structured improvement plan
        """
        improvement_plan = {
            "priority_high": [],
            "priority_medium": [],
            "priority_low": [],
            "estimated_effort": "medium"
        }
        
        # Categorize improvements by priority
        for metric_name, score in metrics.items():
            if score < 0.4:
                improvement_plan["priority_high"].append(f"Significantly improve {metric_name.replace('_', ' ')}")
            elif score < 0.6:
                improvement_plan["priority_medium"].append(f"Improve {metric_name.replace('_', ' ')}")
            elif score < 0.8:
                improvement_plan["priority_low"].append(f"Enhance {metric_name.replace('_', ' ')}")
        
        # Estimate effort based on number of high-priority items
        high_priority_count = len(improvement_plan["priority_high"])
        if high_priority_count >= 3:
            improvement_plan["estimated_effort"] = "high"
        elif high_priority_count >= 1:
            improvement_plan["estimated_effort"] = "medium"
        else:
            improvement_plan["estimated_effort"] = "low"
        
        return improvement_plan
    
    def _extract_source_types(self, sources: List[Any]) -> List[str]:
        """Extract source types from sources, handling both Dict and ResearchSource objects."""
        source_types = set()
        for s in sources:
            if hasattr(s, 'source_type'):
                # ResearchSource Pydantic model
                source_types.add(s.source_type or "general")
            else:
                # Dictionary object
                source_types.add(s.get("source_type", "general"))
        return list(source_types)
    
    def _calculate_avg_score(self, sources: List[Any], score_field: str) -> float:
        """Calculate average score from sources, handling both Dict and ResearchSource objects."""
        if not sources:
            return 0.0
        
        total_score = 0.0
        valid_sources = 0
        
        for s in sources:
            if hasattr(s, score_field):
                # ResearchSource Pydantic model
                score = getattr(s, score_field)
                if score is not None:
                    total_score += score
                    valid_sources += 1
            else:
                # Dictionary object
                score = s.get(score_field, 0)
                if score:
                    total_score += score
                    valid_sources += 1
        
        return total_score / valid_sources if valid_sources > 0 else 0.0
