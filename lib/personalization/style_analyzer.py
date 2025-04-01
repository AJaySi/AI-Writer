"""Style analyzer module for analyzing content style using LLM."""

from typing import Dict, List, Optional
from loguru import logger
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen
import json
import re

class StyleAnalyzer:
    """Analyzer for content style using LLM."""
    
    def __init__(self):
        """Initialize the style analyzer."""
        logger.info("[StyleAnalyzer.__init__] Initializing style analyzer")
        
    def _clean_json_response(self, text: str) -> str:
        """
        Clean the LLM response to extract valid JSON.
        
        Args:
            text (str): Raw response from LLM
            
        Returns:
            str: Cleaned JSON string
        """
        try:
            # Remove markdown code block markers
            cleaned_string = text.replace("```json", "").replace("```", "").strip()
            
            # Log the cleaned JSON for debugging
            logger.debug(f"[StyleAnalyzer._clean_json_response] Cleaned JSON: {cleaned_string}")
            
            return cleaned_string
            
        except Exception as e:
            logger.error(f"[StyleAnalyzer._clean_json_response] Error cleaning response: {str(e)}")
            return ""
        
    def analyze_content_style(self, content: Dict) -> Dict:
        """
        Analyze the style of the provided content.
        
        Args:
            content (Dict): Content to analyze, containing main_content, title, etc.
            
        Returns:
            Dict: Analysis results
        """
        try:
            logger.info("[StyleAnalyzer.analyze_content_style] Starting content style analysis")
            
            # Prepare content for analysis
            main_content = content.get("main_content", "")
            title = content.get("title", "")
            description = content.get("description", "")
            
            # Construct the analysis prompt
            prompt = f"""Analyze the following content and provide a comprehensive writing style analysis.
            Focus on identifying the writing style, tone, and characteristics that make this content unique.

            Title: {title}
            Description: {description}
            Content: {main_content[:4000]}  # Limit content length for API

            IMPORTANT: Respond ONLY with a JSON object in the following format. Do not include any additional text, explanations, or markdown formatting:
            {{
                "writing_style": {{
                    "tone": "formal/casual/technical/etc",
                    "voice": "active/passive",
                    "complexity": "simple/moderate/complex",
                    "engagement_level": "low/medium/high"
                }},
                "content_characteristics": {{
                    "sentence_structure": "description",
                    "vocabulary_level": "basic/intermediate/advanced",
                    "paragraph_organization": "description",
                    "content_flow": "description"
                }},
                "target_audience": {{
                    "demographics": ["list"],
                    "expertise_level": "beginner/intermediate/advanced",
                    "industry_focus": "primary industry",
                    "geographic_focus": "primary region"
                }},
                "content_type": {{
                    "primary_type": "blog/article/product/etc",
                    "secondary_types": ["list"],
                    "purpose": "inform/entertain/persuade/etc",
                    "call_to_action": "type and frequency"
                }},
                "recommended_settings": {{
                    "writing_tone": "recommended tone",
                    "target_audience": "recommended audience",
                    "content_type": "recommended type",
                    "creativity_level": "low/medium/high",
                    "geographic_location": "recommended location"
                }}
            }}"""
            
            # Get analysis from LLM
            logger.debug("[StyleAnalyzer.analyze_content_style] Sending prompt to LLM")
            analysis_text = llm_text_gen(prompt)
            
            try:
                # Clean and parse the JSON response
                cleaned_json = self._clean_json_response(analysis_text)
                if not cleaned_json:
                    raise ValueError("No valid JSON found in response")
                    
                # Log the cleaned JSON for debugging
                logger.debug(f"[StyleAnalyzer.analyze_content_style] Cleaned JSON: {cleaned_json}")
                
                # Try to parse the cleaned JSON
                try:
                    analysis = json.loads(cleaned_json)
                except json.JSONDecodeError as e:
                    # If parsing fails, try to fix common JSON issues
                    logger.warning(f"[StyleAnalyzer.analyze_content_style] Initial JSON parsing failed: {e}")
                    
                    # Fix any remaining issues
                    cleaned_json = re.sub(r'([^"\\])\n', r'\1 ', cleaned_json)
                    cleaned_json = re.sub(r'\\n', ' ', cleaned_json)
                    
                    # Try parsing again
                    analysis = json.loads(cleaned_json)
                
                logger.info("[StyleAnalyzer.analyze_content_style] Successfully parsed analysis results")
                return analysis
                
            except json.JSONDecodeError as e:
                logger.error(f"[StyleAnalyzer.analyze_content_style] Failed to parse JSON response: {e}")
                logger.debug(f"[StyleAnalyzer.analyze_content_style] Raw response: {analysis_text}")
                return {
                    "error": "Failed to parse analysis results",
                    "raw_response": analysis_text
                }
                
        except Exception as e:
            logger.error(f"[StyleAnalyzer.analyze_content_style] Error during analysis: {str(e)}")
            return {
                "error": str(e),
                "success": False
            }
    
    def analyze_style_patterns(self, content: Dict) -> Dict:
        """
        Analyze specific writing style patterns in the content.
        
        Args:
            content (Dict): Content to analyze
            
        Returns:
            Dict: Pattern analysis results
        """
        try:
            main_content = content.get("main_content", "")
            
            prompt = f"""Analyze the following content for specific writing style patterns.
            Focus on identifying recurring patterns in sentence structure, word choice, and rhetorical devices.

            Content: {main_content[:4000]}

            IMPORTANT: Respond ONLY with a JSON object in the following format. Do not include any additional text, explanations, or markdown formatting:
            {{
                "sentence_patterns": {{
                    "structure": ["list of patterns"],
                    "length": "short/medium/long",
                    "complexity": "simple/moderate/complex"
                }},
                "word_patterns": {{
                    "vocabulary": ["list of patterns"],
                    "frequency": "low/medium/high",
                    "diversity": "low/medium/high"
                }},
                "rhetorical_devices": {{
                    "types": ["list of devices"],
                    "frequency": "low/medium/high",
                    "effectiveness": "low/medium/high"
                }}
            }}"""
            
            analysis_text = llm_text_gen(prompt)
            
            try:
                cleaned_json = self._clean_json_response(analysis_text)
                if not cleaned_json:
                    raise ValueError("No valid JSON found in response")
                    
                analysis = json.loads(cleaned_json)
                return analysis
            except json.JSONDecodeError as e:
                logger.error(f"[StyleAnalyzer.analyze_style_patterns] Failed to parse JSON response: {e}")
                return {
                    "error": "Failed to parse pattern analysis results",
                    "raw_response": analysis_text
                }
                
        except Exception as e:
            logger.error(f"[StyleAnalyzer.analyze_style_patterns] Error during analysis: {str(e)}")
            return {
                "error": str(e),
                "success": False
            } 