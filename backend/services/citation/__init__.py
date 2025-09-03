"""
Citation Services Module for ALwrity

This module provides citation management capabilities for grounded content generation,
ensuring proper source attribution and citation validation.

Available Services:
- CitationManager: Handles inline citations, validation, and source attribution
- Citation pattern recognition and analysis
- Citation quality assessment and improvement suggestions
- Export formatting for different content types

Author: ALwrity Team
Version: 1.0
Last Updated: January 2025
"""

from services.citation.citation_manager import CitationManager

__all__ = [
    "CitationManager"
]
