import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List

from ..integrations.integration_manager import IntegrationManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_cross_platform_content(
    title: str,
    content: str,
    platforms: List[str],
    content_type: str,
    target_audience: Dict[str, Any],
    industry: str,
    keywords: List[str]
) -> Dict[str, Any]:
    """Create and optimize content for multiple platforms."""
    try:
        # Initialize integration manager
        integration_manager = IntegrationManager()
        
        # Prepare content item
        content_item = {
            'title': title,
            'content': content,
            'content_type': content_type,
            'keywords': keywords,
            'target_audience': target_audience,
            'industry': industry
        }
        
        # Get platform suggestions
        suggestions = integration_manager.get_platform_suggestions(
            content=content_item,
            platforms=platforms
        )
        
        # Validate content for each platform
        validation_results = {}
        for platform in platforms:
            validation = integration_manager.validate_platform_content(
                content=content_item,
                platform=platform
            )
            validation_results[platform] = validation
        
        # Optimize content for each platform
        optimized_content = integration_manager.optimize_cross_platform_content(
            content=content_item,
            platforms=platforms
        )
        
        return {
            'original_content': content_item,
            'platform_suggestions': suggestions,
            'validation_results': validation_results,
            'optimized_content': optimized_content
        }
        
    except Exception as e:
        logger.error(f"Error creating cross-platform content: {str(e)}")
        return {
            'error': str(e)
        }

def create_content_calendar(
    start_date: datetime,
    end_date: datetime,
    platforms: List[str],
    content_types: List[str],
    target_audience: Dict[str, Any],
    industry: str,
    keywords: List[str]
) -> Dict[str, Any]:
    """Create a cross-platform content calendar."""
    try:
        # Initialize integration manager
        integration_manager = IntegrationManager()
        
        # Create calendar
        calendar = integration_manager.create_cross_platform_calendar(
            start_date=start_date,
            end_date=end_date,
            platforms=platforms,
            content_types=content_types,
            target_audience=target_audience,
            industry=industry,
            keywords=keywords
        )
        
        return calendar
        
    except Exception as e:
        logger.error(f"Error creating content calendar: {str(e)}")
        return {
            'error': str(e)
        }

def main():
    """Main function to demonstrate integration manager usage."""
    # Example content details
    title = "The Future of AI in Content Marketing"
    content = """
    Artificial Intelligence is revolutionizing the way we approach content marketing.
    From automated content generation to personalized recommendations, AI tools are
    helping marketers create more engaging and effective content strategies.
    
    Key points:
    1. AI-powered content generation
    2. Personalized content recommendations
    3. Automated content optimization
    4. Data-driven content strategy
    5. Future trends in AI marketing
    """
    
    # Platform and content settings
    platforms = ['instagram', 'twitter', 'linkedin', 'blog', 'facebook']
    content_type = 'article'
    target_audience = {
        'age_range': '25-34',
        'interests': ['technology', 'marketing', 'AI'],
        'location': 'global',
        'profession': 'marketing professionals'
    }
    industry = 'technology'
    keywords = ['AI', 'content marketing', 'automation', 'personalization']
    
    # Create cross-platform content
    logger.info("Creating cross-platform content...")
    content_result = create_cross_platform_content(
        title=title,
        content=content,
        platforms=platforms,
        content_type=content_type,
        target_audience=target_audience,
        industry=industry,
        keywords=keywords
    )
    
    # Print content results
    logger.info("\nCross-Platform Content Results:")
    logger.info("===============================")
    
    # Print platform suggestions
    logger.info("\nPlatform Suggestions:")
    for platform, suggestions in content_result['platform_suggestions'].items():
        logger.info(f"\n{platform.upper()}:")
        for key, value in suggestions.items():
            logger.info(f"  {key}: {value}")
    
    # Print validation results
    logger.info("\nValidation Results:")
    for platform, validation in content_result['validation_results'].items():
        logger.info(f"\n{platform.upper()}:")
        logger.info(f"  Valid: {validation['is_valid']}")
        if not validation['is_valid']:
            logger.info(f"  Error: {validation.get('error', 'N/A')}")
    
    # Print optimized content
    logger.info("\nOptimized Content:")
    for platform, optimized in content_result['optimized_content'].items():
        logger.info(f"\n{platform.upper()}:")
        for key, value in optimized.items():
            logger.info(f"  {key}: {value}")
    
    # Create content calendar
    logger.info("\nCreating content calendar...")
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)
    calendar_result = create_content_calendar(
        start_date=start_date,
        end_date=end_date,
        platforms=platforms,
        content_types=[content_type],
        target_audience=target_audience,
        industry=industry,
        keywords=keywords
    )
    
    # Print calendar results
    logger.info("\nContent Calendar Results:")
    logger.info("========================")
    
    # Print platform calendars
    logger.info("\nPlatform Calendars:")
    for platform, calendar in calendar_result['platform_calendars'].items():
        logger.info(f"\n{platform.upper()}:")
        logger.info(f"  Content Items: {len(calendar['content_items'])}")
        for item in calendar['content_items']:
            logger.info(f"  - {item['original_item']['title']}")

if __name__ == '__main__':
    main() 