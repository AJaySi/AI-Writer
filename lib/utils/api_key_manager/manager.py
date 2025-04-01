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
        logger.info("[APIKeyManager.load_api_keys] Loading API keys from environment")
        try:
            # Load from environment variables
            self.api_keys = {
                "openai": os.getenv("OPENAI_API_KEY", ""),
                "google": os.getenv("GOOGLE_API_KEY", ""),
                "tavily": os.getenv("TAVILY_API_KEY", ""),
                "metaphor": os.getenv("METAPHOR_API_KEY", ""),
                "mistral": os.getenv("MISTRAL_API_KEY", "")
            }
            logger.info("[APIKeyManager.load_api_keys] Successfully loaded API keys")
        except Exception as e:
            logger.error(f"[APIKeyManager.load_api_keys] Error loading API keys: {str(e)}")
    
    def save_api_key(self, provider: str, key: str):
        """Save an API key."""
        logger.info(f"[APIKeyManager.save_api_key] Saving API key for provider: {provider}")
        try:
            self.api_keys[provider] = key
            # Save to environment variable
            os.environ[f"{provider.upper()}_API_KEY"] = key
            logger.info(f"[APIKeyManager.save_api_key] Successfully saved API key for {provider}")
        except Exception as e:
            logger.error(f"[APIKeyManager.save_api_key] Error saving API key: {str(e)}")
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """Get an API key."""
        return self.api_keys.get(provider) 