"""API key manager class."""

from typing import Dict, Any, Optional
from loguru import logger
import streamlit as st
import os
import json
import sys
from datetime import datetime
from dotenv import load_dotenv

# Configure logger to output to both file and stdout
logger.remove()  # Remove default handler
logger.add("logs/api_key_manager.log", 
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
           level="DEBUG")
logger.add(sys.stdout, 
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
           level="INFO")

class APIKeyManager:
    """Manager for handling API keys."""
    
    def __init__(self):
        """Initialize the API key manager."""
        logger.info("[APIKeyManager.__init__] Initializing API key manager")
        self.api_keys = {}
        self.load_api_keys()
        self.api_key_groups = {
            "Create": {
                "GEMINI_API_KEY": {
                    "url": "https://makersuite.google.com/app/apikey",
                    "description": "Google's Gemini AI for content generation",
                    "setup_steps": [
                        "Visit Google AI Studio",
                        "Create a Google Cloud account",
                        "Enable Gemini API",
                        "Generate API key"
                    ]
                },
                "OPENAI_API_KEY": {
                    "url": "https://platform.openai.com/api-keys",
                    "description": "OpenAI's GPT models for content creation",
                    "setup_steps": [
                        "Go to OpenAI platform",
                        "Create an account",
                        "Navigate to API keys",
                        "Create new API key"
                    ]
                },
                "MISTRAL_API_KEY": {
                    "url": "https://console.mistral.ai/api-keys/",
                    "description": "Mistral AI for efficient content generation",
                    "setup_steps": [
                        "Visit Mistral AI website",
                        "Sign up for an account",
                        "Access API section",
                        "Generate API key"
                    ]
                }
            },
            "Research": {
                "TAVILY_API_KEY": {
                    "url": "https://tavily.com/#api",
                    "description": "Powers intelligent web research features",
                    "setup_steps": [
                        "Go to Tavily's website",
                        "Create an account",
                        "Access your API dashboard",
                        "Generate a new API key"
                    ]
                },
                "SERPER_API_KEY": {
                    "url": "https://serper.dev/signup",
                    "description": "Enables Google search functionality",
                    "setup_steps": [
                        "Visit Serper.dev",
                        "Sign up for an account",
                        "Go to API section",
                        "Create your API key"
                    ]
                }
            },
            "Deep Search": {
                "METAPHOR_API_KEY": {
                    "url": "https://dashboard.exa.ai/login",
                    "description": "Enables advanced web search capabilities",
                    "setup_steps": [
                        "Visit the Exa AI dashboard",
                        "Sign up for a free account",
                        "Navigate to API Keys section",
                        "Create a new API key"
                    ]
                },
                "FIRECRAWL_API_KEY": {
                    "url": "https://www.firecrawl.dev/account",
                    "description": "Enables web content extraction",
                    "setup_steps": [
                        "Visit Firecrawl website",
                        "Sign up for an account",
                        "Access API dashboard",
                        "Create your API key"
                    ]
                }
            },
            "Integrations": {
                "STABILITY_API_KEY": {
                    "url": "https://platform.stability.ai/",
                    "description": "Enables AI image generation",
                    "setup_steps": [
                        "Access Stability AI platform",
                        "Create an account",
                        "Navigate to API settings",
                        "Generate your API key"
                    ]
                }
            }
        }
    
    def load_api_keys(self):
        """Load API keys from environment variables."""
        try:
            logger.info("[APIKeyManager.load_api_keys] Loading API keys from environment")
            
            # Get the current working directory and .env file path
            current_dir = os.getcwd()
            env_path = os.path.join(current_dir, '.env')
            logger.info(f"[APIKeyManager.load_api_keys] Looking for .env file at: {env_path}")
            
            # Check if .env file exists
            if not os.path.exists(env_path):
                logger.warning(f"[APIKeyManager.load_api_keys] .env file not found at {env_path}")
                return
                
            # Load environment variables
            load_dotenv(env_path, override=True)
            logger.debug("[APIKeyManager.load_api_keys] Environment variables loaded")
            
            # Define all possible API key providers
            all_providers = [
                # AI Providers
                'OPENAI_API_KEY',
                'GEMINI_API_KEY',
                'ANTHROPIC_API_KEY',
                'MISTRAL_API_KEY',
                # Research Providers
                'SERPER_API_KEY',
                'TAVILY_API_KEY',
                'METAPHOR_API_KEY',
                'FIRECRAWL_API_KEY'
            ]
            
            # Load API keys from environment variables
            for provider in all_providers:
                value = os.getenv(provider)
                if value:
                    self.api_keys[provider] = value
                    logger.info(f"[APIKeyManager.load_api_keys] Loaded {provider} from environment")
                else:
                    logger.debug(f"[APIKeyManager.load_api_keys] {provider} not found in environment")
            
            logger.info(f"[APIKeyManager.load_api_keys] Loaded {len(self.api_keys)} API keys")
            
        except Exception as e:
            logger.error(f"[APIKeyManager.load_api_keys] Error loading API keys: {str(e)}")
    
    def save_api_key(self, provider: str, api_key: str) -> bool:
        """
        Save an API key for a provider.
        
        Args:
            provider: The provider name (e.g., 'openai', 'gemini')
            api_key: The API key value
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info(f"[APIKeyManager] Saving API key for {provider}")
            
            # Map provider to environment variable name
            env_var_map = {
                'openai': 'OPENAI_API_KEY',
                'gemini': 'GEMINI_API_KEY',
                'mistral': 'MISTRAL_API_KEY',
                'anthropic': 'ANTHROPIC_API_KEY',
                'serpapi': 'SERPAPI_API_KEY',
                'tavily': 'TAVILY_API_KEY',
                'metaphor': 'METAPHOR_API_KEY',
                'firecrawl': 'FIRECRAWL_API_KEY'
            }
            
            env_var = env_var_map.get(provider)
            if not env_var:
                logger.error(f"[APIKeyManager] Unknown provider: {provider}")
                return False
            
            # Update the in-memory dictionary
            self.api_keys[provider] = api_key
            
            # Update environment variable
            os.environ[env_var] = api_key
            
            # Read existing .env file content
            env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env')
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except FileNotFoundError:
                lines = []
            
            # Update or add the API key
            key_found = False
            updated_lines = []
            for line in lines:
                if line.startswith(f"{env_var}="):
                    updated_lines.append(f"{env_var}={api_key}\n")
                    key_found = True
                else:
                    updated_lines.append(line)
            
            if not key_found:
                updated_lines.append(f"{env_var}={api_key}\n")
            
            # Write back to .env file
            with open(env_path, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)
            
            logger.info(f"[APIKeyManager] Successfully saved API key for {provider}")
            return True
            
        except Exception as e:
            logger.error(f"[APIKeyManager] Error saving API key for {provider}: {str(e)}")
            return False
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """Get an API key."""
        return self.api_keys.get(provider) 