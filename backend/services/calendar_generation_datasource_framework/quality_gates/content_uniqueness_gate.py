"""
Content Uniqueness Quality Gate

Validates content uniqueness and prevents duplicate content
in calendar generation.
"""

import logging
from typing import Dict, Any, List, Set
from datetime import datetime

logger = logging.getLogger(__name__)


class ContentUniquenessGate:
    """
    Quality gate for content uniqueness and duplicate prevention.
    """
    
    def __init__(self):
        self.name = "content_uniqueness"
        self.description = "Validates content uniqueness and prevents duplicate content"
        self.pass_threshold = 0.9
        self.validation_criteria = [
            "No duplicate content topics",
            "Unique content titles",
            "Diverse content themes",
            "No keyword cannibalization"
        ]
    
    async def validate(self, calendar_data: Dict[str, Any], step_name: str = None) -> Dict[str, Any]:
        """
        Validate content uniqueness in calendar data.
        
        Args:
            calendar_data: Calendar data to validate
            step_name: Optional step name for context
            
        Returns:
            Validation result
        """
        try:
            logger.info(f"Validating content uniqueness for step: {step_name or 'general'}")
            
            validation_result = {
                "gate_name": self.name,
                "passed": False,
                "score": 0.0,
                "issues": [],
                "recommendations": [],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Extract content items from calendar data
            content_items = self._extract_content_items(calendar_data)
            
            if not content_items:
                validation_result["issues"].append("No content items found for validation")
                validation_result["recommendations"].append("Ensure calendar contains content items")
                return validation_result
            
            # Check for duplicate topics
            duplicate_topics = self._check_duplicate_topics(content_items)
            if duplicate_topics:
                validation_result["issues"].extend(duplicate_topics)
            
            # Check for duplicate titles
            duplicate_titles = self._check_duplicate_titles(content_items)
            if duplicate_titles:
                validation_result["issues"].extend(duplicate_titles)
            
            # Check content diversity
            diversity_score = self._calculate_diversity_score(content_items)
            
            # Check keyword cannibalization
            keyword_issues = self._check_keyword_cannibalization(content_items)
            if keyword_issues:
                validation_result["issues"].extend(keyword_issues)
            
            # Calculate overall score
            base_score = 1.0
            penalty_per_issue = 0.1
            total_penalties = len(validation_result["issues"]) * penalty_per_issue
            final_score = max(0.0, base_score - total_penalties)
            
            # Apply diversity bonus
            final_score = (final_score + diversity_score) / 2
            
            validation_result["score"] = final_score
            validation_result["passed"] = final_score >= self.pass_threshold
            
            # Generate recommendations
            if not validation_result["passed"]:
                validation_result["recommendations"].extend([
                    "Review and remove duplicate content topics",
                    "Ensure unique content titles",
                    "Increase content theme diversity",
                    "Avoid keyword cannibalization"
                ])
            
            logger.info(f"Content uniqueness validation: {'PASSED' if validation_result['passed'] else 'FAILED'} (score: {final_score:.2f})")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error in content uniqueness validation: {e}")
            return {
                "gate_name": self.name,
                "passed": False,
                "score": 0.0,
                "error": str(e),
                "recommendations": ["Fix content uniqueness validation system"]
            }
    
    def _extract_content_items(self, calendar_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract content items from calendar data."""
        content_items = []
        
        # Extract from daily schedule
        if "daily_schedule" in calendar_data:
            for day_data in calendar_data["daily_schedule"].values():
                if isinstance(day_data, dict) and "content" in day_data:
                    content_items.extend(day_data["content"])
        
        # Extract from weekly themes
        if "weekly_themes" in calendar_data:
            for theme_data in calendar_data["weekly_themes"].values():
                if isinstance(theme_data, dict) and "content" in theme_data:
                    content_items.extend(theme_data["content"])
        
        # Extract from content recommendations
        if "content_recommendations" in calendar_data:
            content_items.extend(calendar_data["content_recommendations"])
        
        return content_items
    
    def _check_duplicate_topics(self, content_items: List[Dict[str, Any]]) -> List[str]:
        """Check for duplicate content topics."""
        issues = []
        topics = []
        
        for item in content_items:
            if isinstance(item, dict):
                topic = item.get("topic", item.get("title", ""))
                if topic:
                    topics.append(topic.lower().strip())
        
        # Find duplicates
        seen_topics = set()
        duplicate_topics = set()
        
        for topic in topics:
            if topic in seen_topics:
                duplicate_topics.add(topic)
            else:
                seen_topics.add(topic)
        
        for topic in duplicate_topics:
            issues.append(f"Duplicate topic found: {topic}")
        
        return issues
    
    def _check_duplicate_titles(self, content_items: List[Dict[str, Any]]) -> List[str]:
        """Check for duplicate content titles."""
        issues = []
        titles = []
        
        for item in content_items:
            if isinstance(item, dict):
                title = item.get("title", "")
                if title:
                    titles.append(title.lower().strip())
        
        # Find duplicates
        seen_titles = set()
        duplicate_titles = set()
        
        for title in titles:
            if title in seen_titles:
                duplicate_titles.add(title)
            else:
                seen_titles.add(title)
        
        for title in duplicate_titles:
            issues.append(f"Duplicate title found: {title}")
        
        return issues
    
    def _calculate_diversity_score(self, content_items: List[Dict[str, Any]]) -> float:
        """Calculate content diversity score."""
        if not content_items:
            return 0.0
        
        # Extract themes/categories
        themes = set()
        for item in content_items:
            if isinstance(item, dict):
                theme = item.get("theme", item.get("category", ""))
                if theme:
                    themes.add(theme.lower().strip())
        
        # Calculate diversity based on number of unique themes
        total_items = len(content_items)
        unique_themes = len(themes)
        
        if total_items == 0:
            return 0.0
        
        # Diversity score: more themes = higher score, but not too many
        diversity_ratio = unique_themes / total_items
        optimal_ratio = 0.3  # 30% unique themes is optimal
        
        if diversity_ratio <= optimal_ratio:
            return diversity_ratio / optimal_ratio
        else:
            # Penalize too much diversity (might indicate lack of focus)
            return max(0.0, 1.0 - (diversity_ratio - optimal_ratio))
    
    def _check_keyword_cannibalization(self, content_items: List[Dict[str, Any]]) -> List[str]:
        """Check for keyword cannibalization."""
        issues = []
        keywords = []
        
        for item in content_items:
            if isinstance(item, dict):
                item_keywords = item.get("keywords", [])
                if isinstance(item_keywords, list):
                    keywords.extend([kw.lower().strip() for kw in item_keywords])
        
        # Find keyword frequency
        keyword_freq = {}
        for keyword in keywords:
            keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
        
        # Check for overused keywords
        for keyword, frequency in keyword_freq.items():
            if frequency > 3:  # More than 3 uses of same keyword
                issues.append(f"Potential keyword cannibalization: '{keyword}' used {frequency} times")
        
        return issues
    
    def __str__(self) -> str:
        return f"ContentUniquenessGate(threshold={self.pass_threshold})"
    
    def __repr__(self) -> str:
        return f"ContentUniquenessGate(name={self.name}, threshold={self.pass_threshold}, criteria={len(self.validation_criteria)})"
