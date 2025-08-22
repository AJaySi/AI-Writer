"""
Content Mix Quality Gate

Validates content mix balance and distribution across different
content types and themes.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


class ContentMixGate:
    """Quality gate for content mix balance and distribution."""
    
    def __init__(self):
        self.name = "content_mix"
        self.description = "Validates content mix balance and distribution"
        self.pass_threshold = 0.8
        self.validation_criteria = [
            "Balanced content types",
            "Appropriate content mix ratios",
            "Theme distribution",
            "Content variety"
        ]
    
    async def validate(self, calendar_data: Dict[str, Any], step_name: str = None) -> Dict[str, Any]:
        """Validate content mix in calendar data."""
        try:
            logger.info(f"Validating content mix for step: {step_name or 'general'}")
            
            validation_result = {
                "gate_name": self.name,
                "passed": False,
                "score": 0.0,
                "issues": [],
                "recommendations": [],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            content_items = self._extract_content_items(calendar_data)
            
            if not content_items:
                validation_result["issues"].append("No content items found")
                return validation_result
            
            # Check content type balance
            type_balance_score = self._check_content_type_balance(content_items)
            
            # Check theme distribution
            theme_distribution_score = self._check_theme_distribution(content_items)
            
            # Check content variety
            variety_score = self._check_content_variety(content_items)
            
            # Calculate overall score
            overall_score = (type_balance_score + theme_distribution_score + variety_score) / 3
            validation_result["score"] = overall_score
            validation_result["passed"] = overall_score >= self.pass_threshold
            
            if not validation_result["passed"]:
                validation_result["recommendations"].extend([
                    "Balance content types across educational, thought leadership, and promotional",
                    "Ensure even distribution across content themes",
                    "Increase content variety and formats"
                ])
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error in content mix validation: {e}")
            return {
                "gate_name": self.name,
                "passed": False,
                "score": 0.0,
                "error": str(e),
                "recommendations": ["Fix content mix validation system"]
            }
    
    def _extract_content_items(self, calendar_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract content items from calendar data."""
        content_items = []
        
        if "daily_schedule" in calendar_data:
            for day_data in calendar_data["daily_schedule"].values():
                if isinstance(day_data, dict) and "content" in day_data:
                    content_items.extend(day_data["content"])
        
        return content_items
    
    def _check_content_type_balance(self, content_items: List[Dict[str, Any]]) -> float:
        """Check balance of content types."""
        type_counts = {"educational": 0, "thought_leadership": 0, "promotional": 0}
        
        for item in content_items:
            if isinstance(item, dict):
                content_type = item.get("type", "educational")
                type_counts[content_type] = type_counts.get(content_type, 0) + 1
        
        total = sum(type_counts.values())
        if total == 0:
            return 0.0
        
        # Ideal ratios: 40% educational, 30% thought leadership, 30% promotional
        ideal_ratios = {"educational": 0.4, "thought_leadership": 0.3, "promotional": 0.3}
        actual_ratios = {k: v/total for k, v in type_counts.items()}
        
        balance_score = 1.0
        for content_type, ideal_ratio in ideal_ratios.items():
            actual_ratio = actual_ratios.get(content_type, 0)
            deviation = abs(actual_ratio - ideal_ratio)
            balance_score -= deviation * 0.5  # Penalty for deviation
        
        return max(0.0, balance_score)
    
    def _check_theme_distribution(self, content_items: List[Dict[str, Any]]) -> float:
        """Check distribution of content themes."""
        theme_counts = {}
        
        for item in content_items:
            if isinstance(item, dict):
                theme = item.get("theme", "general")
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        if not theme_counts:
            return 0.0
        
        total = sum(theme_counts.values())
        max_count = max(theme_counts.values())
        
        # Calculate distribution evenness
        evenness = 1.0 - (max_count / total - 1/len(theme_counts))
        return max(0.0, evenness)
    
    def _check_content_variety(self, content_items: List[Dict[str, Any]]) -> float:
        """Check variety of content formats."""
        formats = set()
        
        for item in content_items:
            if isinstance(item, dict):
                format_type = item.get("format", "article")
                formats.add(format_type)
        
        # More formats = higher variety score
        variety_score = min(1.0, len(formats) / 5)  # Cap at 5 formats
        return variety_score
    
    def __str__(self) -> str:
        return f"ContentMixGate(threshold={self.pass_threshold})"
    
    def __repr__(self) -> str:
        return f"ContentMixGate(name={self.name}, threshold={self.pass_threshold})"
