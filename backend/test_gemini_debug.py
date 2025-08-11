#!/usr/bin/env python3
"""
Debug script to test Gemini API and identify the empty response issue.
"""

import os
import sys
import asyncio
import logging

# Add current directory to path
sys.path.append('.')

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_gemini_api():
    """Test Gemini API to identify the issue."""
    
    # Check if API key is set
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        logger.error("❌ GEMINI_API_KEY environment variable not set")
        return False
    
    logger.info(f"🔑 Found Gemini API key: {api_key[:10]}...")
    
    try:
        # Test basic API connectivity
        from services.llm_providers.gemini_provider import test_gemini_api_key
        is_valid, message = await test_gemini_api_key(api_key)
        
        if is_valid:
            logger.info(f"✅ {message}")
        else:
            logger.error(f"❌ {message}")
            return False
        
        # Test simple text generation
        from services.llm_providers.gemini_provider import gemini_pro_text_gen
        simple_response = gemini_pro_text_gen("Hello, this is a test. Please respond with 'Test successful'.")
        logger.info(f"📝 Simple text response: {simple_response}")
        
        # Test structured JSON generation with a simple schema
        from services.llm_providers.gemini_provider import gemini_structured_json_response
        
        simple_schema = {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "status": {"type": "string"}
            }
        }
        
        simple_prompt = "Generate a simple JSON response with a message and status."
        
        logger.info("🧪 Testing structured JSON generation...")
        structured_response = gemini_structured_json_response(simple_prompt, simple_schema)
        logger.info(f"📋 Structured response: {structured_response}")
        
        # Test with the actual autofill schema
        from api.content_planning.services.content_strategy.autofill.ai_structured_autofill import AIStructuredAutofillService
        
        autofill_service = AIStructuredAutofillService()
        schema = autofill_service._build_schema()
        
        logger.info(f"🔧 Autofill schema has {len(schema.get('properties', {}))} properties")
        
        # Test with a minimal context
        test_context = {
            'user_id': 1,
            'website_analysis': {
                'url': 'https://test.com',
                'industry': 'Technology'
            }
        }
        
        context_summary = autofill_service._build_context_summary(test_context)
        prompt = autofill_service._build_prompt(context_summary)
        
        logger.info(f"📝 Autofill prompt length: {len(prompt)}")
        logger.info(f"📝 Autofill prompt preview: {prompt[:200]}...")
        
        # Test the actual autofill call
        logger.info("🧪 Testing actual autofill generation...")
        autofill_result = await autofill_service.generate_autofill_fields(1, test_context)
        logger.info(f"📋 Autofill result: {autofill_result}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing Gemini API: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_gemini_api())
    if success:
        logger.info("✅ Gemini API test completed successfully")
    else:
        logger.error("❌ Gemini API test failed")
        sys.exit(1) 