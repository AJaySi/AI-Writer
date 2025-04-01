"""Configuration management for GPT providers."""

import os
import json
from loguru import logger
import sys

# Configure logger to output to both file and stdout
logger.remove()  # Remove default handler
logger.add(
    "logs/config.log",
    rotation="500 MB",
    retention="10 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>"
)

def load_config() -> Optional[Dict]:
    """
    Load configuration from environment or config file.
    
    Returns:
        Optional[Dict]: Configuration dictionary or None if loading fails
    """
    try:
        logger.info("[load_config] Starting configuration load")
        
        # First try to load from environment variable
        config_str = os.getenv('ALWRITY_CONFIG')
        if config_str:
            logger.debug("[load_config] Found configuration in environment variable")
            try:
                config = json.loads(config_str)
                logger.info("[load_config] Successfully loaded configuration from environment")
                return config
            except json.JSONDecodeError as e:
                logger.error(f"[load_config] Failed to parse environment config: {str(e)}")
        
        # If no environment variable, try to load from file
        config_path = os.getenv('ALWRITY_CONFIG', 'config.json')
        logger.debug(f"[load_config] Attempting to load config from file: {config_path}")
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                logger.info("[load_config] Successfully loaded configuration from file")
                return config
            except json.JSONDecodeError as e:
                logger.error(f"[load_config] Failed to parse config file: {str(e)}")
            except Exception as e:
                logger.error(f"[load_config] Error reading config file: {str(e)}")
        else:
            logger.error(f"[load_config] Config file not found: {config_path}")
        
        return None
        
    except Exception as e:
        logger.error(f"[load_config] Unexpected error loading configuration: {str(e)}")
        return None

def read_return_config_section(section: str) -> tuple:
    """
    Read a specific section from the configuration.
    
    Args:
        section (str): The section to read
        
    Returns:
        tuple: Configuration values
    """
    try:
        logger.info(f"[read_return_config_section] Reading section: {section}")
        
        config = load_config()
        if not config:
            logger.error("[read_return_config_section] No configuration available")
            return None, None, None, None, None, None, None
            
        section_config = config.get(section, {})
        logger.debug(f"[read_return_config_section] Section config: {section_config}")
        
        # Extract values with defaults
        gpt_provider = section_config.get('gpt_provider', 'openai')
        model = section_config.get('model', 'gpt-3.5-turbo')
        temperature = float(section_config.get('temperature', 0.7))
        max_tokens = int(section_config.get('max_tokens', 2000))
        top_p = float(section_config.get('top_p', 1.0))
        n = int(section_config.get('n', 1))
        fp = section_config.get('fp', 'json')
        
        logger.info(f"[read_return_config_section] Successfully read configuration for {section}")
        logger.debug(f"[read_return_config_section] Values: provider={gpt_provider}, model={model}, "
                    f"temperature={temperature}, max_tokens={max_tokens}")
        
        return gpt_provider, model, temperature, max_tokens, top_p, n, fp
        
    except Exception as e:
        logger.error(f"[read_return_config_section] Error reading configuration section: {str(e)}")
        return None, None, None, None, None, None, None 