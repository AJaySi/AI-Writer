#!/usr/bin/env python3
"""
Test script for the persona generation system.
Tests the complete flow from onboarding data to persona creation.
"""

import sys
import os
import json
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from loguru import logger

def test_persona_system():
    """Test the complete persona generation system."""
    
    logger.info("🧪 Testing Persona Generation System")
    
    try:
        # Test 1: Check database models
        logger.info("📊 Test 1: Checking database models...")
        from models.persona_models import WritingPersona, PlatformPersona, PersonaAnalysisResult
        logger.info("✅ Persona models imported successfully")
        
        # Test 2: Check service initialization
        logger.info("🔧 Test 2: Testing service initialization...")
        from services.persona_analysis_service import PersonaAnalysisService
        persona_service = PersonaAnalysisService()
        logger.info("✅ PersonaAnalysisService initialized successfully")
        
        # Test 3: Create sample onboarding data
        logger.info("📝 Test 3: Creating sample onboarding data...")
        sample_onboarding_data = create_sample_onboarding_data()
        logger.info("✅ Sample onboarding data created")
        
        # Test 4: Test core persona generation
        logger.info("🤖 Test 4: Testing core persona generation...")
        core_persona = persona_service._generate_core_persona(sample_onboarding_data)
        
        if "error" in core_persona:
            logger.error(f"❌ Core persona generation failed: {core_persona['error']}")
            return False
        else:
            logger.info("✅ Core persona generated successfully")
            logger.info(f"   Persona Name: {core_persona.get('identity', {}).get('persona_name', 'N/A')}")
            logger.info(f"   Archetype: {core_persona.get('identity', {}).get('archetype', 'N/A')}")
            logger.info(f"   Confidence: {core_persona.get('confidence_score', 0)}%")
        
        # Test 5: Test platform adaptations
        logger.info("📱 Test 5: Testing platform adaptations...")
        platforms = ["twitter", "linkedin", "blog"]
        
        for platform in platforms:
            platform_persona = persona_service._generate_single_platform_persona(
                core_persona, platform, sample_onboarding_data
            )
            
            if "error" in platform_persona:
                logger.warning(f"⚠️ {platform} persona generation failed: {platform_persona['error']}")
            else:
                logger.info(f"✅ {platform} persona generated successfully")
        
        # Test 6: Test data sufficiency calculation
        logger.info("📊 Test 6: Testing data sufficiency calculation...")
        data_sufficiency = persona_service._calculate_data_sufficiency(sample_onboarding_data)
        logger.info(f"✅ Data sufficiency calculated: {data_sufficiency}%")
        
        logger.info("🎉 All persona system tests completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Persona system test failed: {str(e)}")
        return False

def create_sample_onboarding_data():
    """Create realistic sample onboarding data for testing."""
    
    return {
        "session_info": {
            "session_id": 1,
            "current_step": 6,
            "progress": 100.0,
            "started_at": datetime.utcnow().isoformat()
        },
        "website_analysis": {
            "id": 1,
            "website_url": "https://techstartup.example.com",
            "writing_style": {
                "tone": "professional",
                "voice": "authoritative",
                "complexity": "intermediate",
                "engagement_level": "high"
            },
            "content_characteristics": {
                "sentence_structure": "varied",
                "vocabulary": "technical",
                "paragraph_organization": "logical",
                "average_sentence_length": 15.2
            },
            "target_audience": {
                "demographics": ["startup founders", "tech professionals", "investors"],
                "expertise_level": "intermediate",
                "industry_focus": "technology"
            },
            "content_type": {
                "primary_type": "blog",
                "secondary_types": ["case_study", "tutorial"],
                "purpose": "educational"
            },
            "style_patterns": {
                "common_phrases": ["let's dive in", "the key insight", "bottom line"],
                "sentence_starters": ["Here's the thing:", "The reality is", "Consider this:"],
                "rhetorical_devices": ["metaphors", "data_points", "examples"]
            },
            "style_guidelines": {
                "tone_guidelines": "Maintain professional but approachable tone",
                "structure_guidelines": "Use clear headings and bullet points",
                "voice_guidelines": "Confident and knowledgeable without being condescending"
            },
            "status": "completed"
        },
        "research_preferences": {
            "id": 1,
            "research_depth": "Comprehensive",
            "content_types": ["blog", "case_study", "whitepaper"],
            "auto_research": True,
            "factual_content": True,
            "writing_style": {
                "tone": "professional",
                "voice": "authoritative",
                "complexity": "intermediate"
            }
        }
    }

def test_gemini_structured_response():
    """Test Gemini structured response functionality."""
    
    logger.info("🔬 Testing Gemini Structured Response")
    
    try:
        from services.llm_providers.gemini_provider import gemini_structured_json_response
        
        # Simple test schema
        test_schema = {
            "type": "object",
            "properties": {
                "test_field": {"type": "string"},
                "confidence": {"type": "number"}
            },
            "required": ["test_field", "confidence"]
        }
        
        test_prompt = "Generate a test response with test_field='Hello World' and confidence=95.5"
        
        response = gemini_structured_json_response(
            prompt=test_prompt,
            schema=test_schema,
            temperature=0.1,
            max_tokens=1024
        )
        
        if "error" in response:
            logger.error(f"❌ Gemini test failed: {response['error']}")
            return False
        else:
            logger.info(f"✅ Gemini structured response test successful: {response}")
            return True
            
    except Exception as e:
        logger.error(f"❌ Gemini test error: {str(e)}")
        return False

def run_comprehensive_test():
    """Run comprehensive test of the persona system."""
    
    logger.info("🚀 Starting Comprehensive Persona System Test")
    
    # Test 1: Gemini functionality
    gemini_works = test_gemini_structured_response()
    
    # Test 2: Persona system
    persona_works = test_persona_system()
    
    # Summary
    logger.info("📋 Test Summary:")
    logger.info(f"   Gemini Structured Response: {'✅ PASS' if gemini_works else '❌ FAIL'}")
    logger.info(f"   Persona Generation System: {'✅ PASS' if persona_works else '❌ FAIL'}")
    
    if gemini_works and persona_works:
        logger.info("🎉 All tests passed! Persona system is ready for production.")
        return True
    else:
        logger.error("❌ Some tests failed. Please check the logs and fix issues.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)