from typing import Dict
import json

class ContentGapAnalyzer:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self, url: str) -> Dict:
        """
        Analyze content gaps for a given URL.
        
        Args:
            url (str): The URL to analyze
            
        Returns:
            Dict: Analysis results including content gaps and recommendations
        """
        try:
            # Get base analysis
            logger.info(f"Starting content gap analysis for URL: {url}")
            base_analysis = self.analyzer.analyze_website(url)
            
            # Check for errors in base analysis
            if not base_analysis.get("success", False):
                error_msg = base_analysis.get("error", "Unknown error in website analysis")
                error_details = base_analysis.get("error_details", {})
                logger.error(f"Base analysis failed: {error_msg}")
                logger.error(f"Error details: {json.dumps(error_details, indent=2)}")
                return {
                    "success": False,
                    "error": error_msg,
                    "error_details": error_details,
                    "stage": "base_analysis"
                }
            
            # Extract required sections
            analysis_data = base_analysis.get("data", {}).get("analysis", {})
            required_sections = ["content_info", "basic_info", "performance"]
            missing_sections = [section for section in required_sections if section not in analysis_data]
            
            if missing_sections:
                error_msg = f"Missing required analysis sections: {', '.join(missing_sections)}"
                logger.error(error_msg)
                logger.error(f"Available sections: {list(analysis_data.keys())}")
                return {
                    "success": False,
                    "error": error_msg,
                    "error_details": {
                        "missing_sections": missing_sections,
                        "available_sections": list(analysis_data.keys())
                    },
                    "stage": "section_validation"
                }
            
            # Extract content metrics
            try:
                content_info = analysis_data["content_info"]
                basic_info = analysis_data["basic_info"]
                performance = analysis_data["performance"]
            except KeyError as e:
                error_msg = f"Error extracting analysis section: {str(e)}"
                logger.error(error_msg)
                return {
                    "success": False,
                    "error": error_msg,
                    "error_details": {
                        "type": "KeyError",
                        "missing_key": str(e),
                        "available_keys": list(analysis_data.keys())
                    },
                    "stage": "data_extraction"
                }
            
            # Analyze content gaps
            try:
                gaps = self._analyze_content_gaps(content_info, basic_info, performance)
            except Exception as e:
                error_msg = f"Error analyzing content gaps: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return {
                    "success": False,
                    "error": error_msg,
                    "error_details": {
                        "type": type(e).__name__,
                        "traceback": str(e.__traceback__)
                    },
                    "stage": "gap_analysis"
                }
            
            # Generate recommendations
            try:
                recommendations = self._generate_recommendations(gaps)
            except Exception as e:
                error_msg = f"Error generating recommendations: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return {
                    "success": False,
                    "error": error_msg,
                    "error_details": {
                        "type": type(e).__name__,
                        "traceback": str(e.__traceback__)
                    },
                    "stage": "recommendation_generation"
                }
            
            return {
                "success": True,
                "data": {
                    "content_gaps": gaps,
                    "recommendations": recommendations,
                    "metrics": {
                        "word_count": content_info.get("word_count", 0),
                        "heading_count": content_info.get("heading_count", 0),
                        "image_count": content_info.get("image_count", 0),
                        "link_count": content_info.get("link_count", 0),
                        "paragraph_count": content_info.get("paragraph_count", 0),
                        "load_time": performance.get("load_time", 0),
                        "response_time": performance.get("response_time", 0)
                    }
                }
            }
            
        except Exception as e:
            error_msg = f"Error in content gap analysis: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "success": False,
                "error": error_msg,
                "error_details": {
                    "type": type(e).__name__,
                    "traceback": str(e.__traceback__)
                },
                "stage": "general"
            } 