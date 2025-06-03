#!/usr/bin/env python3
"""
Smart Content Repurposing Engine Demo

This script demonstrates the capabilities of the Smart Content Repurposing Engine
by showing how a single piece of content can be transformed into multiple 
platform-optimized variations.

Usage:
    python demo_smart_repurposing.py
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from lib.database.models import ContentItem, ContentType, Platform, SEOData
from lib.ai_seo_tools.content_calendar.core.content_repurposer import SmartContentRepurposingEngine
from lib.ai_seo_tools.content_calendar.core.content_generator import ContentGenerator

def create_sample_content() -> ContentItem:
    """Create a sample blog post for demonstration."""
    
    sample_content = """
    The Future of AI in Content Creation: 5 Game-Changing Trends
    
    Artificial Intelligence is revolutionizing how we create, optimize, and distribute content. 
    According to recent studies, 73% of marketers are already using AI tools for content creation, 
    and this number is expected to reach 95% by 2025.
    
    Here are the top 5 trends shaping the future:
    
    1. Automated Content Generation
    AI can now generate high-quality blog posts, social media content, and even video scripts. 
    Tools like GPT-4 and Claude are producing content that's increasingly indistinguishable 
    from human-written text. Companies using AI content generation report 40% faster 
    content production and 25% cost reduction.
    
    2. Personalized Content at Scale
    AI enables hyper-personalization by analyzing user behavior, preferences, and engagement 
    patterns. Netflix's recommendation algorithm is a prime example, driving 80% of viewer 
    engagement through personalized content suggestions.
    
    3. Real-time Content Optimization
    Machine learning algorithms can analyze content performance in real-time and suggest 
    optimizations. This includes headline testing, image selection, and even optimal 
    posting times. Brands using AI optimization see 35% higher engagement rates.
    
    4. Voice and Visual Content Creation
    AI is expanding beyond text to create voice content, images, and videos. Tools like 
    DALL-E and Midjourney are democratizing visual content creation, while voice synthesis 
    technology enables podcast and audio content generation.
    
    5. Predictive Content Strategy
    AI can predict trending topics, optimal content formats, and audience preferences 
    before they become mainstream. This predictive capability gives content creators 
    a significant competitive advantage.
    
    The key to success in this AI-driven landscape is not to replace human creativity 
    but to augment it. The most successful content strategies will combine AI efficiency 
    with human insight and emotional intelligence.
    
    What's your experience with AI content tools? Have you noticed improvements in 
    your content performance? Share your thoughts in the comments below.
    """
    
    return ContentItem(
        title="The Future of AI in Content Creation: 5 Game-Changing Trends",
        description=sample_content.strip(),
        content_type=ContentType.BLOG_POST,
        platforms=[Platform.WEBSITE],
        publish_date=datetime.now(),
        status="draft",
        author="AI Content Strategist",
        tags=["AI", "content creation", "marketing", "technology", "trends"],
        notes="Comprehensive guide on AI trends in content creation",
        seo_data=SEOData(
            title="The Future of AI in Content Creation: 5 Game-Changing Trends",
            meta_description="Discover the top 5 AI trends revolutionizing content creation. Learn how 73% of marketers are using AI tools and what's coming next.",
            keywords=["AI content creation", "artificial intelligence marketing", "content automation", "AI trends", "content strategy"],
            structured_data={}
        )
    )

def demonstrate_content_analysis(engine: SmartContentRepurposingEngine, content: ContentItem):
    """Demonstrate content analysis capabilities."""
    print("🔍 CONTENT ANALYSIS DEMONSTRATION")
    print("=" * 50)
    
    # Analyze content atoms
    content_text = content.description
    atoms = engine.analyze_content_atoms(content_text, content.title)
    
    print(f"📊 Content Analysis for: '{content.title}'")
    print(f"📝 Word Count: {len(content_text.split())}")
    print()
    
    print("🔬 Content Atoms Extracted:")
    for atom_type, atom_list in atoms.items():
        if atom_list:
            print(f"\n{atom_type.upper()}:")
            for i, atom in enumerate(atom_list[:3], 1):  # Show first 3
                print(f"  {i}. {atom}")
            if len(atom_list) > 3:
                print(f"  ... and {len(atom_list) - 3} more")
    
    print("\n" + "=" * 50)

def demonstrate_single_content_repurposing(generator: ContentGenerator, content: ContentItem):
    """Demonstrate single content repurposing."""
    print("\n📝 SINGLE CONTENT REPURPOSING DEMONSTRATION")
    print("=" * 50)
    
    target_platforms = [Platform.TWITTER, Platform.LINKEDIN, Platform.INSTAGRAM]
    
    print(f"🎯 Repurposing for platforms: {[p.name for p in target_platforms]}")
    print("⏳ Generating repurposed content...")
    
    try:
        repurposed_content = generator.repurpose_content_for_platforms(
            content_item=content,
            target_platforms=target_platforms,
            strategy='adaptive'
        )
        
        if repurposed_content:
            print(f"✅ Successfully created {len(repurposed_content)} repurposed pieces!")
            
            for i, repurposed in enumerate(repurposed_content, 1):
                platform = repurposed.platforms[0].name
                print(f"\n📱 {i}. {platform.upper()} VERSION:")
                print(f"Title: {repurposed.title}")
                print(f"Content Preview: {repurposed.description[:200]}...")
                print(f"Tags: {', '.join(repurposed.tags)}")
        else:
            print("❌ No repurposed content was generated.")
            
    except Exception as e:
        print(f"❌ Error during repurposing: {str(e)}")
    
    print("\n" + "=" * 50)

def demonstrate_content_series_creation(generator: ContentGenerator, content: ContentItem):
    """Demonstrate cross-platform content series creation."""
    print("\n📚 CONTENT SERIES CREATION DEMONSTRATION")
    print("=" * 50)
    
    platforms = [Platform.TWITTER, Platform.LINKEDIN, Platform.WEBSITE]
    
    print(f"🌐 Creating progressive disclosure series for: {[p.name for p in platforms]}")
    print("⏳ Generating content series...")
    
    try:
        series_content = generator.create_content_series_across_platforms(
            source_content=content,
            platforms=platforms,
            series_type='progressive_disclosure'
        )
        
        if series_content:
            total_pieces = sum(len(pieces) for pieces in series_content.values())
            print(f"✅ Successfully created series with {total_pieces} pieces across {len(series_content)} platforms!")
            
            for platform_name, content_pieces in series_content.items():
                print(f"\n📱 {platform_name.upper()} SERIES ({len(content_pieces)} pieces):")
                for i, piece in enumerate(content_pieces, 1):
                    print(f"  {i}. {piece.title}")
                    print(f"     Preview: {piece.description[:150]}...")
        else:
            print("❌ No content series was generated.")
            
    except Exception as e:
        print(f"❌ Error creating series: {str(e)}")
    
    print("\n" + "=" * 50)

def demonstrate_repurposing_analysis(generator: ContentGenerator, content: ContentItem):
    """Demonstrate content repurposing analysis."""
    print("\n🔍 REPURPOSING ANALYSIS DEMONSTRATION")
    print("=" * 50)
    
    available_platforms = [Platform.TWITTER, Platform.LINKEDIN, Platform.INSTAGRAM, Platform.FACEBOOK, Platform.WEBSITE]
    
    print("📊 Analyzing content for repurposing potential...")
    
    try:
        analysis = generator.analyze_content_for_repurposing(
            content_item=content,
            available_platforms=available_platforms
        )
        
        if analysis:
            content_analysis = analysis.get('content_analysis', {})
            
            print(f"📈 ANALYSIS RESULTS:")
            print(f"  Word Count: {content_analysis.get('word_count', 0)}")
            print(f"  Content Richness: {content_analysis.get('content_richness', 'Unknown')}")
            print(f"  Repurposing Potential: {content_analysis.get('repurposing_potential', 'Unknown')}")
            
            print(f"\n🎯 RECOMMENDED PLATFORMS:")
            for platform in analysis.get('platform_suggestions', []):
                print(f"  • {platform.name}")
            
            print(f"\n💡 SUGGESTED STRATEGIES:")
            for strategy in analysis.get('strategy_suggestions', []):
                print(f"  • {strategy.replace('_', ' ').title()}")
            
            estimated = analysis.get('estimated_output', {})
            if estimated:
                print(f"\n📊 ESTIMATED OUTPUT:")
                print(f"  Total Pieces: {estimated.get('total_pieces', 0)}")
                print(f"  Time Savings: {estimated.get('time_savings', '0 hours')}")
                print(f"  Content Multiplication: {estimated.get('content_multiplication', '1x')}")
        else:
            print("❌ No analysis results generated.")
            
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
    
    print("\n" + "=" * 50)

def demonstrate_comprehensive_workflow(generator: ContentGenerator, content: ContentItem):
    """Demonstrate the comprehensive content generation with repurposing plan."""
    print("\n🚀 COMPREHENSIVE WORKFLOW DEMONSTRATION")
    print("=" * 50)
    
    target_platforms = [Platform.TWITTER, Platform.LINKEDIN, Platform.INSTAGRAM]
    
    print("🎯 Generating content with integrated repurposing plan...")
    
    try:
        # Create a context for content generation (simplified for demo)
        context = {
            'target_audience': 'Content creators and marketers',
            'content_goals': ['educate', 'engage', 'convert'],
            'keywords': ['AI', 'content creation', 'marketing automation']
        }
        
        result = generator.generate_content_with_repurposing_plan(
            content_item=content,
            context=context,
            target_platforms=target_platforms
        )
        
        if result:
            print("✅ Successfully generated comprehensive content plan!")
            
            # Display content structure
            content_data = result.get('content', {})
            outline = content_data.get('outline', {})
            
            print(f"\n📋 CONTENT STRUCTURE:")
            headings = outline.get('headings', [])
            if headings:
                print(f"  Main Headings: {len(headings)} generated")
            
            key_points = outline.get('key_points', [])
            if key_points:
                print(f"  Key Points: {len(key_points)} identified")
            
            # Display repurposing plan
            repurposing_plan = result.get('repurposing_plan', {})
            if repurposing_plan:
                print(f"\n🔄 REPURPOSING PLAN:")
                
                analysis = repurposing_plan.get('analysis', {})
                if analysis:
                    estimated = analysis.get('estimated_output', {})
                    print(f"  Estimated Pieces: {estimated.get('total_pieces', 0)}")
                    print(f"  Time Savings: {estimated.get('time_savings', '0 hours')}")
                
                strategy = repurposing_plan.get('recommended_strategy', 'adaptive')
                print(f"  Recommended Strategy: {strategy}")
                
                roadmap = repurposing_plan.get('platform_roadmap', {})
                timeline = roadmap.get('timeline', {})
                if timeline:
                    print(f"  Platform Timeline:")
                    for platform, details in timeline.items():
                        print(f"    • {platform}: {details.get('release_date', 'TBD')}")
        else:
            print("❌ No comprehensive plan generated.")
            
    except Exception as e:
        print(f"❌ Error generating comprehensive workflow: {str(e)}")
    
    print("\n" + "=" * 50)

def main():
    """Main demonstration function."""
    print("🔄 SMART CONTENT REPURPOSING ENGINE DEMO")
    print("=" * 50)
    print("This demo shows how one piece of content can be transformed")
    print("into multiple platform-optimized variations using AI.")
    print("=" * 50)
    
    # Initialize the engines
    print("🚀 Initializing Smart Content Repurposing Engine...")
    repurposing_engine = SmartContentRepurposingEngine()
    content_generator = ContentGenerator()
    
    # Create sample content
    print("📝 Creating sample content...")
    sample_content = create_sample_content()
    
    print(f"✅ Sample content created: '{sample_content.title}'")
    print(f"📊 Content length: {len(sample_content.description.split())} words")
    
    # Run demonstrations
    try:
        # 1. Content Analysis
        demonstrate_content_analysis(repurposing_engine, sample_content)
        
        # 2. Single Content Repurposing
        demonstrate_single_content_repurposing(content_generator, sample_content)
        
        # 3. Content Series Creation
        demonstrate_content_series_creation(content_generator, sample_content)
        
        # 4. Repurposing Analysis
        demonstrate_repurposing_analysis(content_generator, sample_content)
        
        # 5. Comprehensive Workflow
        demonstrate_comprehensive_workflow(content_generator, sample_content)
        
    except Exception as e:
        print(f"❌ Demo error: {str(e)}")
        print("This is expected if AI services are not configured.")
    
    print("\n🎉 DEMO COMPLETE!")
    print("=" * 50)
    print("Key Features Demonstrated:")
    print("✅ Content atomization and analysis")
    print("✅ Platform-specific content repurposing")
    print("✅ Cross-platform content series creation")
    print("✅ AI-powered repurposing recommendations")
    print("✅ Comprehensive content planning workflow")
    print("\nThe Smart Content Repurposing Engine is ready to transform")
    print("your content creation process!")

if __name__ == "__main__":
    main()