from typing import Dict, Any
from datetime import datetime

from ..integrations.platform_adapters import UnifiedPlatformAdapter

def create_platform_content(
    title: str,
    content: str,
    platforms: list,
    context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Create platform-specific content using the UnifiedPlatformAdapter.
    
    Args:
        title: The title of the content
        content: The main content to be adapted
        platforms: List of platforms to adapt content for
        context: Additional context for content adaptation
    
    Returns:
        Dict containing adapted content for each platform
    """
    # Initialize the platform adapter
    adapter = UnifiedPlatformAdapter()
    
    # Prepare base content
    base_content = {
        'title': title,
        'content': content,
        'keywords': ['content', 'marketing', 'social media'],
        'tone': 'professional',
        'cta': 'Learn More',
        'audience': 'For All',
        'language': 'English',
        'industry': 'technology',
        'word_count': 1000
    }
    
    # Adapt content for each platform
    adapted_content = {}
    for platform in platforms:
        try:
            platform_content = adapter.adapt_content(
                content=base_content,
                platform=platform,
                context=context
            )
            adapted_content[platform] = platform_content
        except Exception as e:
            print(f"Error adapting content for {platform}: {str(e)}")
            adapted_content[platform] = {'error': str(e)}
    
    return adapted_content

def main():
    """Example usage of platform content adaptation."""
    # Example content
    title = "The Future of AI in Content Marketing"
    content = """
    Artificial Intelligence is revolutionizing content marketing in unprecedented ways.
    From automated content generation to personalized user experiences, AI is becoming
    an indispensable tool for marketers. This article explores the latest trends and
    innovations in AI-powered content marketing.
    """
    
    # Example context
    context = {
        'target_audience': 'marketing professionals',
        'campaign_goals': ['awareness', 'engagement', 'lead generation'],
        'brand_voice': 'authoritative yet approachable',
        'content_theme': 'technology and innovation'
    }
    
    # Platforms to adapt content for
    platforms = ['instagram', 'twitter', 'linkedin', 'blog', 'facebook']
    
    # Generate platform-specific content
    adapted_content = create_platform_content(
        title=title,
        content=content,
        platforms=platforms,
        context=context
    )
    
    # Print results
    print("\nPlatform-Specific Content Adaptation Results:")
    print("=" * 50)
    
    for platform, content in adapted_content.items():
        print(f"\n{platform.upper()} Content:")
        print("-" * 30)
        
        if 'error' in content:
            print(f"Error: {content['error']}")
            continue
        
        # Print platform-specific content
        if platform == 'instagram':
            print("\nCaptions:")
            for caption in content['captions']:
                print(f"- {caption}")
            print("\nHashtags:")
            print(content['hashtags'])
        
        elif platform == 'twitter':
            print("\nTweets:")
            for tweet in content['tweets']:
                print(f"- {tweet}")
            print("\nThread Structure:")
            print(content['thread_structure'])
        
        elif platform == 'linkedin':
            print("\nPost:")
            print(content['post'])
            print("\nEngagement Optimization:")
            print(content['engagement_optimization'])
        
        elif platform == 'blog':
            print("\nPost:")
            print(content['post'])
            print("\nSEO Optimization:")
            print(content['seo_optimization'])
        
        elif platform == 'facebook':
            print("\nPost:")
            print(content['post'])
            print("\nEngagement Optimization:")
            print(content['engagement_optimization'])
        
        # Print media suggestions
        print("\nMedia Suggestions:")
        for media in content['media_suggestions']:
            print(f"- {media['type']}: {media['description']}")
        
        # Print platform-specific recommendations
        print("\nPlatform-Specific Recommendations:")
        for key, value in content['platform_specific'].items():
            print(f"- {key}: {value}")

if __name__ == '__main__':
    main() 