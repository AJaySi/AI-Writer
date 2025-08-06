"""API Key Manager package for ALwrity."""

from .manager import APIKeyManager
from .api_key_manager import render, check_onboarding_completion, get_onboarding_status, reset_onboarding
from .onboarding_progress import (
    OnboardingProgress, 
    get_onboarding_progress, 
    render_progress_indicator, 
    render_resume_message,
    StepStatus,
    StepData
)
from .validation import check_all_api_keys
from .components.base import (
    render_step_indicator,
    render_navigation_buttons,
    render_step_validation,
    render_resume_options
)

# Export all public components
__all__ = [
    # Main classes
    'APIKeyManager',
    'OnboardingProgress',
    'StepStatus',
    'StepData',
    
    # Main functions
    'render',
    'check_onboarding_completion',
    'get_onboarding_status',
    'reset_onboarding',
    'get_onboarding_progress',
    
    # UI components
    'render_progress_indicator',
    'render_resume_message',
    'render_step_indicator',
    'render_navigation_buttons',
    'render_step_validation',
    'render_resume_options',
    
    # Validation
    'check_all_api_keys'
]

# Version information
__version__ = "2.0.0"
__author__ = "ALwrity Team"
__description__ = "Comprehensive API key management and onboarding system for ALwrity"

# Note: FastAPI endpoints have been moved to the backend/ directory
# for better separation of concerns and enterprise architecture. 