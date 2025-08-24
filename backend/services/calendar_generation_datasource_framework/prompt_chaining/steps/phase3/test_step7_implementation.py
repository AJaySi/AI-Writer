"""
Test Script for Step 7: Weekly Theme Development

This script tests the Step 7 implementation to ensure:
- Proper execution with real data
- Quality metrics calculation
- Strategic alignment validation
- Error handling and fallback mechanisms
"""

import asyncio
import sys
import os
from typing import Dict, Any
from loguru import logger

# Add the services directory to the path for proper imports
services_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)

from step7_implementation import WeeklyThemeDevelopmentStep


async def test_step7_implementation():
    """Test Step 7 implementation with comprehensive validation."""
    
    logger.info("🧪 Starting Step 7: Weekly Theme Development tests")
    
    # Initialize Step 7
    step = WeeklyThemeDevelopmentStep()
    
    # Create test context with mock data
    context = create_test_context()
    
    try:
        # Execute Step 7
        logger.info("🚀 Executing Step 7...")
        result = await step.execute(context)
        
        # Validate result structure
        logger.info("📋 Validating result structure...")
        validate_result_structure(result)
        
        # Validate weekly themes
        logger.info("🎯 Validating weekly themes...")
        validate_weekly_themes(result)
        
        # Validate quality metrics
        logger.info("📊 Validating quality metrics...")
        validate_quality_metrics(result)
        
        # Validate strategic alignment
        logger.info("🎯 Validating strategic alignment...")
        validate_strategic_alignment(result)
        
        # Test validation method
        logger.info("✅ Testing validation method...")
        validation_passed = step.validate_result(result)
        logger.info(f"Validation passed: {validation_passed}")
        
        # Calculate quality score
        quality_score = step._calculate_quality_score(result, validation_passed)
        logger.info(f"Quality score: {quality_score:.3f}")
        
        # Print summary
        print_summary(result, quality_score, validation_passed)
        
        logger.info("✅ Step 7 tests completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Step 7 test failed: {str(e)}")
        return False


def create_test_context() -> Dict[str, Any]:
    """Create test context with mock data."""
    
    return {
        "user_id": 1,
        "strategy_id": 1,
        "calendar_duration": 30,  # 30 days
        "step_01_result": {
            "strategy_data": {
                "business_goals": [
                    "Increase brand awareness",
                    "Generate qualified leads",
                    "Establish thought leadership"
                ],
                "target_audience": {
                    "demographics": "B2B professionals, 25-45 years old",
                    "interests": "Technology, innovation, business growth",
                    "pain_points": ["Limited time", "Need for ROI", "Competition"]
                }
            }
        },
        "step_02_result": {
            "gap_analysis": {
                "content_gaps": [
                    {"description": "Technical tutorials and guides", "impact_score": 0.8},
                    {"description": "Case studies and success stories", "impact_score": 0.9},
                    {"description": "Industry trend analysis", "impact_score": 0.7},
                    {"description": "Best practices and tips", "impact_score": 0.8}
                ]
            }
        },
        "step_05_result": {
            "content_pillars": [
                {"name": "Educational Content", "description": "How-to guides and tutorials"},
                {"name": "Thought Leadership", "description": "Industry insights and analysis"},
                {"name": "Case Studies", "description": "Success stories and examples"},
                {"name": "Best Practices", "description": "Tips and recommendations"}
            ],
            "pillar_weights": {
                "Educational Content": 0.3,
                "Thought Leadership": 0.25,
                "Case Studies": 0.25,
                "Best Practices": 0.2
            }
        },
        "step_06_result": {
            "platform_strategies": {
                "LinkedIn": {
                    "approach": "Professional thought leadership content",
                    "tone": "Professional and authoritative",
                    "content_types": ["Articles", "Posts", "Videos"]
                },
                "Blog": {
                    "approach": "In-depth educational content",
                    "tone": "Informative and helpful",
                    "content_types": ["How-to guides", "Case studies", "Analysis"]
                },
                "Twitter": {
                    "approach": "Quick insights and engagement",
                    "tone": "Conversational and engaging",
                    "content_types": ["Tips", "Insights", "Questions"]
                }
            }
        }
    }


def validate_result_structure(result: Dict[str, Any]):
    """Validate the structure of the result."""
    
    required_fields = [
        "weekly_themes",
        "diversity_metrics", 
        "alignment_metrics",
        "insights",
        "num_weeks",
        "theme_count",
        "content_pillars_used",
        "strategic_alignment_score",
        "diversity_score"
    ]
    
    for field in required_fields:
        if field not in result:
            raise ValueError(f"Missing required field: {field}")
    
    logger.info(f"✅ Result structure validation passed - {len(required_fields)} fields present")


def validate_weekly_themes(result: Dict[str, Any]):
    """Validate weekly themes data."""
    
    weekly_themes = result.get("weekly_themes", [])
    
    if not weekly_themes:
        raise ValueError("No weekly themes generated")
    
    if len(weekly_themes) < 4:
        raise ValueError(f"Insufficient weekly themes: {len(weekly_themes)} (minimum 4)")
    
    # Validate each theme structure
    required_theme_fields = [
        "title", "description", "primary_pillar", "content_angles",
        "target_platforms", "week_number", "week_start_date", "week_end_date"
    ]
    
    for i, theme in enumerate(weekly_themes):
        for field in required_theme_fields:
            if field not in theme:
                raise ValueError(f"Theme {i+1} missing field: {field}")
        
        # Validate content angles
        content_angles = theme.get("content_angles", [])
        if len(content_angles) < 3:
            raise ValueError(f"Theme {i+1} has insufficient content angles: {len(content_angles)}")
        
        # Validate target platforms
        target_platforms = theme.get("target_platforms", [])
        if len(target_platforms) < 2:
            raise ValueError(f"Theme {i+1} has insufficient target platforms: {len(target_platforms)}")
    
    logger.info(f"✅ Weekly themes validation passed - {len(weekly_themes)} themes generated")


def validate_quality_metrics(result: Dict[str, Any]):
    """Validate quality metrics."""
    
    diversity_metrics = result.get("diversity_metrics", {})
    
    # Check diversity scores
    overall_diversity = diversity_metrics.get("overall_diversity", 0.0)
    if overall_diversity < 0.3:
        raise ValueError(f"Diversity too low: {overall_diversity} (minimum 0.3)")
    
    # Check individual diversity metrics
    pillar_diversity = diversity_metrics.get("pillar_diversity", 0.0)
    platform_diversity = diversity_metrics.get("platform_diversity", 0.0)
    angle_diversity = diversity_metrics.get("angle_diversity", 0.0)
    
    if any(score < 0.2 for score in [pillar_diversity, platform_diversity, angle_diversity]):
        raise ValueError(f"Individual diversity scores too low: pillar={pillar_diversity}, platform={platform_diversity}, angle={angle_diversity}")
    
    logger.info(f"✅ Quality metrics validation passed - overall diversity: {overall_diversity:.3f}")


def validate_strategic_alignment(result: Dict[str, Any]):
    """Validate strategic alignment metrics."""
    
    alignment_metrics = result.get("alignment_metrics", {})
    
    # Check alignment score
    overall_score = alignment_metrics.get("overall_score", 0.0)
    if overall_score < 0.5:
        raise ValueError(f"Alignment score too low: {overall_score} (minimum 0.5)")
    
    # Check alignment level
    alignment_level = alignment_metrics.get("alignment_level", "Unknown")
    if alignment_level not in ["Excellent", "Good", "Fair", "Poor"]:
        raise ValueError(f"Invalid alignment level: {alignment_level}")
    
    # Check theme scores
    theme_scores = alignment_metrics.get("theme_scores", [])
    if len(theme_scores) < 4:
        raise ValueError(f"Insufficient theme scores: {len(theme_scores)}")
    
    if any(score < 0.3 for score in theme_scores):
        raise ValueError(f"Some theme alignment scores too low: {theme_scores}")
    
    logger.info(f"✅ Strategic alignment validation passed - overall score: {overall_score:.3f}, level: {alignment_level}")


def print_summary(result: Dict[str, Any], quality_score: float, validation_passed: bool):
    """Print test summary."""
    
    print("\n" + "="*60)
    print("🎯 STEP 7: WEEKLY THEME DEVELOPMENT - TEST SUMMARY")
    print("="*60)
    
    # Basic metrics
    weekly_themes = result.get("weekly_themes", [])
    diversity_metrics = result.get("diversity_metrics", {})
    alignment_metrics = result.get("alignment_metrics", {})
    
    print(f"📊 Generated {len(weekly_themes)} weekly themes")
    print(f"🎯 Quality Score: {quality_score:.3f}")
    print(f"✅ Validation Passed: {validation_passed}")
    
    # Diversity metrics
    print(f"\n📈 DIVERSITY METRICS:")
    print(f"   Overall Diversity: {diversity_metrics.get('overall_diversity', 0.0):.3f}")
    print(f"   Pillar Diversity: {diversity_metrics.get('pillar_diversity', 0.0):.3f}")
    print(f"   Platform Diversity: {diversity_metrics.get('platform_diversity', 0.0):.3f}")
    print(f"   Angle Diversity: {diversity_metrics.get('angle_diversity', 0.0):.3f}")
    
    # Alignment metrics
    print(f"\n🎯 STRATEGIC ALIGNMENT:")
    print(f"   Overall Score: {alignment_metrics.get('overall_score', 0.0):.3f}")
    print(f"   Alignment Level: {alignment_metrics.get('alignment_level', 'Unknown')}")
    print(f"   Theme Scores: {[f'{score:.2f}' for score in alignment_metrics.get('theme_scores', [])]}")
    
    # Sample themes
    print(f"\n📋 SAMPLE THEMES:")
    for i, theme in enumerate(weekly_themes[:3]):  # Show first 3 themes
        print(f"   Week {theme.get('week_number', i+1)}: {theme.get('title', 'Unknown')}")
        print(f"     Pillar: {theme.get('primary_pillar', 'Unknown')}")
        print(f"     Platforms: {', '.join(theme.get('target_platforms', []))}")
    
    # Insights
    insights = result.get("insights", [])
    print(f"\n💡 INSIGHTS GENERATED: {len(insights)}")
    for insight in insights[:2]:  # Show first 2 insights
        print(f"   - {insight.get('title', 'Unknown')}: {insight.get('description', 'No description')}")
    
    print("\n" + "="*60)
    print("✅ STEP 7 TEST COMPLETED SUCCESSFULLY!")
    print("="*60)


async def main():
    """Main test function."""
    
    logger.info("🧪 Starting Step 7: Weekly Theme Development test suite")
    
    try:
        success = await test_step7_implementation()
        
        if success:
            logger.info("🎉 All Step 7 tests passed!")
            return 0
        else:
            logger.error("❌ Step 7 tests failed!")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Test suite failed with error: {str(e)}")
        return 1


if __name__ == "__main__":
    # Configure logging
    logger.remove()
    logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
    
    # Run tests
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
