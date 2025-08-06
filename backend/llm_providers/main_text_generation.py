"""Main Text Generation Service for ALwrity Backend.

This service provides the main LLM text generation functionality,
migrated from the legacy lib/gpt_providers/text_generation/main_text_generation.py
"""

import os
import json
from typing import Optional, Dict, Any
from loguru import logger
from services.api_key_manager import APIKeyManager

from .openai_provider import openai_chatgpt
from .gemini_provider import gemini_text_response, gemini_structured_json_response
from .anthropic_provider import anthropic_text_response
from .deepseek_provider import deepseek_text_response

def llm_text_gen(prompt: str, system_prompt: Optional[str] = None, json_struct: Optional[Dict[str, Any]] = None) -> str:
    """
    Generate text using Language Model (LLM) based on the provided prompt.
    
    Args:
        prompt (str): The prompt to generate text from.
        system_prompt (str, optional): Custom system prompt to use instead of the default one.
        json_struct (dict, optional): JSON schema structure for structured responses.
        
    Returns:
        str: Generated text based on the prompt.
    """
    try:
        logger.info("[llm_text_gen] Starting text generation")
        logger.debug(f"[llm_text_gen] Prompt length: {len(prompt)} characters")
        
        # Initialize API key manager
        api_key_manager = APIKeyManager()
        
        # Set default values for LLM parameters
        gpt_provider = "google"  # Default to Google Gemini
        model = "models/gemini-2.0-flash"
        temperature = 0.7
        max_tokens = 4000
        top_p = 0.9
        n = 1
        fp = 16
        frequency_penalty = 0.0
        presence_penalty = 0.0
        
        # Default blog characteristics
        blog_tone = "Professional"
        blog_demographic = "Professional"
        blog_type = "Informational"
        blog_language = "English"
        blog_output_format = "markdown"
        blog_length = 2000
        
        # Try to get provider from environment or config
        try:
            # Check which providers have API keys available
            available_providers = []
            if api_key_manager.get_api_key("openai"):
                available_providers.append("openai")
            if api_key_manager.get_api_key("gemini"):
                available_providers.append("google")
            if api_key_manager.get_api_key("anthropic"):
                available_providers.append("anthropic")
            if api_key_manager.get_api_key("deepseek"):
                available_providers.append("deepseek")
            
            # Prefer Google Gemini if available, otherwise use first available
            if "google" in available_providers:
                gpt_provider = "google"
                model = "models/gemini-2.0-flash"
            elif available_providers:
                gpt_provider = available_providers[0]
                if gpt_provider == "openai":
                    model = "gpt-4o"
                elif gpt_provider == "anthropic":
                    model = "claude-3-5-sonnet-20241022"
                elif gpt_provider == "deepseek":
                    model = "deepseek-chat"
            else:
                logger.warning("[llm_text_gen] No API keys found, using mock response")
                return _get_mock_response(prompt)
                
            logger.debug(f"[llm_text_gen] Using provider: {gpt_provider}, model: {model}")
            
        except Exception as err:
            logger.warning(f"[llm_text_gen] Error determining provider, using defaults: {err}")
            gpt_provider = "google"
            model = "models/gemini-2.0-flash"

        # Construct the system prompt if not provided
        if system_prompt is None:
            system_instructions = f"""You are a highly skilled content writer with a knack for creating engaging and informative content. 
                Your expertise spans various writing styles and formats.

                Writing Style Guidelines:
                - Tone: {blog_tone}
                - Target Audience: {blog_demographic}
                - Content Type: {blog_type}
                - Language: {blog_language}
                - Output Format: {blog_output_format}
                - Target Length: {blog_length} words

                Please provide responses that are:
                - Well-structured and easy to read
                - Engaging and informative
                - Tailored to the specified tone and audience
                - Professional yet accessible
                - Optimized for the target content type
            """
        else:
            system_instructions = system_prompt

        # Generate response based on provider
        if gpt_provider == "openai":
            return openai_chatgpt(
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                n=n,
                fp=fp,
                system_prompt=system_instructions
            )
        elif gpt_provider == "google":
            if json_struct:
                return gemini_structured_json_response(
                    prompt=prompt,
                    schema=json_struct,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=n,
                    max_tokens=max_tokens,
                    system_prompt=system_instructions
                )
            else:
                return gemini_text_response(
                    prompt=prompt,
                    temperature=temperature,
                    top_p=top_p,
                    n=n,
                    max_tokens=max_tokens,
                    system_prompt=system_instructions
                )
        elif gpt_provider == "anthropic":
            return anthropic_text_response(
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                system_prompt=system_instructions
            )
        elif gpt_provider == "deepseek":
            return deepseek_text_response(
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                system_prompt=system_instructions
            )
        else:
            logger.error(f"[llm_text_gen] Unknown provider: {gpt_provider}")
            return _get_mock_response(prompt)

    except Exception as e:
        logger.error(f"[llm_text_gen] Error during text generation: {str(e)}")
        return _get_mock_response(prompt)

def _get_mock_response(prompt: str) -> str:
    """Get a mock response when no API keys are available."""
    logger.warning("[llm_text_gen] Using mock response - no API keys configured")
    
    # Return a structured mock response for style detection
    if "style analysis" in prompt.lower() or "writing style" in prompt.lower():
        return json.dumps({
            "writing_style": {
                "tone": "professional",
                "voice": "active",
                "complexity": "moderate",
                "engagement_level": "high"
            },
            "content_characteristics": {
                "sentence_structure": "well-structured",
                "vocabulary_level": "intermediate",
                "paragraph_organization": "logical flow",
                "content_flow": "smooth transitions"
            },
            "target_audience": {
                "demographics": ["professionals", "business users"],
                "expertise_level": "intermediate",
                "industry_focus": "technology",
                "geographic_focus": "global"
            },
            "content_type": {
                "primary_type": "blog",
                "secondary_types": ["article", "guide"],
                "purpose": "inform",
                "call_to_action": "moderate"
            },
            "recommended_settings": {
                "writing_tone": "professional",
                "target_audience": "business professionals",
                "content_type": "blog",
                "creativity_level": "medium",
                "geographic_location": "global"
            }
        })
    
    # Generic mock response
    return "This is a mock response. Please configure API keys for real content generation."

def check_gpt_provider(gpt_provider: str) -> bool:
    """Check if the specified GPT provider is supported."""
    supported_providers = ["openai", "google", "anthropic", "deepseek"]
    return gpt_provider in supported_providers

def get_api_key(gpt_provider: str) -> Optional[str]:
    """Get API key for the specified provider."""
    try:
        api_key_manager = APIKeyManager()
        provider_mapping = {
            "openai": "openai",
            "google": "gemini",
            "anthropic": "anthropic",
            "deepseek": "deepseek"
        }
        
        mapped_provider = provider_mapping.get(gpt_provider, gpt_provider)
        return api_key_manager.get_api_key(mapped_provider)
    except Exception as e:
        logger.error(f"[get_api_key] Error getting API key for {gpt_provider}: {str(e)}")
        return None 