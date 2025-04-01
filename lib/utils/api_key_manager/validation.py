"""API key validation module."""

from typing import Dict, Any, List, Tuple
from loguru import logger
import os
from dotenv import load_dotenv
from .manager import APIKeyManager

def check_all_api_keys(api_key_manager: APIKeyManager) -> bool:
    """Check if minimum required API keys are present.
    
    Args:
        api_key_manager (APIKeyManager): The API key manager instance
        
    Returns:
        bool: True if minimum required keys are present (at least one AI provider and one research provider)
    """
    try:
        # Load environment variables
        logger.info("Starting API key validation process...")
        
        # Get the current working directory and .env file path
        current_dir = os.getcwd()
        env_path = os.path.join(current_dir, '.env')
        logger.info(f"Looking for .env file at: {env_path}")
        
        # Check if .env file exists
        if not os.path.exists(env_path):
            logger.error(f".env file not found at {env_path}")
            return False
            
        # Load environment variables
        load_dotenv(env_path)
        logger.debug("Environment variables loaded")
        
        # Log all environment variables (without their values)
        logger.debug("Available environment variables:")
        for key in os.environ.keys():
            if any(provider in key for provider in ['API_KEY', 'SERPAPI', 'TAVILY', 'METAPHOR', 'FIRECRAWL']):
                logger.debug(f"Found environment variable: {key}")
        
        # Step 1: Check for at least one AI provider
        logger.info("Checking AI provider API keys...")
        ai_providers = [
            'OPENAI_API_KEY',
            'GEMINI_API_KEY',
            'ANTHROPIC_API_KEY',
            'MISTRAL_API_KEY'
        ]
        
        # Log which AI providers are found
        for provider in ai_providers:
            value = os.getenv(provider)
            if value:
                logger.info(f"Found {provider} (length: {len(value)})")
            else:
                logger.debug(f"Missing {provider}")
        
        has_ai_provider = any(os.getenv(key) for key in ai_providers)
        if not has_ai_provider:
            logger.warning("No AI provider API key found")
            return False
        else:
            logger.success("✓ At least one AI provider key found")
        
        # Step 2: Check for at least one research provider
        logger.info("Checking research provider API keys...")
        research_providers = [
            'SERPAPI_KEY',
            'TAVILY_API_KEY',
            'METAPHOR_API_KEY',
            'FIRECRAWL_API_KEY'
        ]
        
        # Log which research providers are found
        for provider in research_providers:
            value = os.getenv(provider)
            if value:
                logger.info(f"Found {provider} (length: {len(value)})")
            else:
                logger.debug(f"Missing {provider}")
        
        has_research_provider = any(os.getenv(key) for key in research_providers)
        if not has_research_provider:
            logger.warning("No research provider API key found")
            return False
        else:
            logger.success("✓ At least one research provider key found")
        
        logger.success("All required API keys validated successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error checking API keys: {str(e)}", exc_info=True)
        return False 