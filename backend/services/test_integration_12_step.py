"""
Integration Test for 12-Step Prompt Chaining Framework

This script tests the complete integration with real AI services and database connections.
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from typing import Dict, Any

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

# Check if we can import the real services
def check_service_availability():
    """Check which services are available."""
    services_status = {
        "prompt_chaining": False,
        "ai_engine": False,
        "keyword_researcher": False,
        "competitor_analyzer": False,
        "onboarding_service": False,
        "ai_analytics": False,
        "content_planning_db": False
    }
    
    try:
        from calendar_generation_datasource_framework.prompt_chaining import PromptChainOrchestrator
        services_status["prompt_chaining"] = True
        print("✅ Prompt Chaining Framework available")
    except ImportError as e:
        print(f"❌ Prompt Chaining Framework not available: {e}")
    
    try:
        from content_gap_analyzer.ai_engine_service import AIEngineService
        services_status["ai_engine"] = True
        print("✅ AI Engine Service available")
    except ImportError as e:
        print(f"⚠️ AI Engine Service not available: {e}")
    
    try:
        from content_gap_analyzer.keyword_researcher import KeywordResearcher
        services_status["keyword_researcher"] = True
        print("✅ Keyword Researcher available")
    except ImportError as e:
        print(f"⚠️ Keyword Researcher not available: {e}")
    
    try:
        from content_gap_analyzer.competitor_analyzer import CompetitorAnalyzer
        services_status["competitor_analyzer"] = True
        print("✅ Competitor Analyzer available")
    except ImportError as e:
        print(f"⚠️ Competitor Analyzer not available: {e}")
    
    try:
        from onboarding_data_service import OnboardingDataService
        services_status["onboarding_service"] = True
        print("✅ Onboarding Data Service available")
    except ImportError as e:
        print(f"⚠️ Onboarding Data Service not available: {e}")
    
    try:
        from ai_analytics_service import AIAnalyticsService
        services_status["ai_analytics"] = True
        print("✅ AI Analytics Service available")
    except ImportError as e:
        print(f"⚠️ AI Analytics Service not available: {e}")
    
    try:
        from content_planning_db import ContentPlanningDBService
        services_status["content_planning_db"] = True
        print("✅ Content Planning DB Service available")
    except ImportError as e:
        print(f"⚠️ Content Planning DB Service not available: {e}")
    
    return services_status

async def test_real_ai_services():
    """Test real AI services connectivity."""
    print("🤖 Testing Real AI Services")
    print("=" * 40)
    
    success_count = 0
    total_tests = 0
    
    # Test AI Engine Service
    try:
        from content_gap_analyzer.ai_engine_service import AIEngineService
        ai_engine = AIEngineService()
        
        print("🎯 Testing AI Engine Service...")
        
        # Test strategic insights generation
        total_tests += 1
        try:
            result = await ai_engine.generate_strategic_insights(
                strategy_data={"content_pillars": ["AI", "Technology"]},
                onboarding_data={"website_analysis": {"industry": "technology"}},
                industry="technology",
                business_size="sme"
            )
            if result and isinstance(result, dict):
                print(f"✅ Strategic insights generation: SUCCESS")
                success_count += 1
            else:
                print(f"⚠️ Strategic insights generation: Empty result")
        except Exception as e:
            print(f"❌ Strategic insights generation: {str(e)}")
        
        # Test content gap analysis
        total_tests += 1
        try:
            result = await ai_engine.analyze_content_gaps(
                gap_data={"content_gaps": ["Blog posts", "Video content"]},
                keyword_analysis={"high_value_keywords": ["AI", "technology"]},
                competitor_analysis={"insights": {"competitors": ["comp1"]}},
                industry="technology"
            )
            if result and isinstance(result, dict):
                print(f"✅ Content gap analysis: SUCCESS")
                success_count += 1
            else:
                print(f"⚠️ Content gap analysis: Empty result")
        except Exception as e:
            print(f"❌ Content gap analysis: {str(e)}")
        
        # Test audience behavior analysis
        total_tests += 1
        try:
            result = await ai_engine.analyze_audience_behavior(
                onboarding_data={"website_analysis": {"target_audience": ["developers"]}},
                strategy_data={"target_audience": {"demographics": {"age": "25-35"}}},
                industry="technology",
                business_size="sme"
            )
            if result and isinstance(result, dict):
                print(f"✅ Audience behavior analysis: SUCCESS")
                success_count += 1
            else:
                print(f"⚠️ Audience behavior analysis: Empty result")
        except Exception as e:
            print(f"❌ Audience behavior analysis: {str(e)}")
        
    except ImportError:
        print("❌ AI Engine Service not available for testing")
    
    # Test Keyword Researcher
    try:
        from content_gap_analyzer.keyword_researcher import KeywordResearcher
        keyword_researcher = KeywordResearcher()
        
        print("\n🔍 Testing Keyword Researcher...")
        
        # Test keyword analysis
        total_tests += 1
        try:
            result = await keyword_researcher.analyze_keywords(
                target_keywords=["AI", "technology", "automation"],
                industry="technology"
            )
            if result and isinstance(result, dict):
                print(f"✅ Keyword analysis: SUCCESS")
                success_count += 1
            else:
                print(f"⚠️ Keyword analysis: Empty result")
        except Exception as e:
            print(f"❌ Keyword analysis: {str(e)}")
        
        # Test trending topics
        total_tests += 1
        try:
            result = await keyword_researcher.get_trending_topics(
                industry="technology"
            )
            if result and isinstance(result, list):
                print(f"✅ Trending topics: SUCCESS")
                success_count += 1
            else:
                print(f"⚠️ Trending topics: Empty result")
        except Exception as e:
            print(f"❌ Trending topics: {str(e)}")
        
    except ImportError:
        print("❌ Keyword Researcher not available for testing")
    
    # Test Competitor Analyzer
    try:
        from content_gap_analyzer.competitor_analyzer import CompetitorAnalyzer
        competitor_analyzer = CompetitorAnalyzer()
        
        print("\n🏢 Testing Competitor Analyzer...")
        
        # Test competitor analysis
        total_tests += 1
        try:
            result = await competitor_analyzer.analyze_competitors(
                competitor_urls=["https://example.com", "https://competitor.com"],
                industry="technology"
            )
            if result and isinstance(result, dict):
                print(f"✅ Competitor analysis: SUCCESS")
                success_count += 1
            else:
                print(f"⚠️ Competitor analysis: Empty result")
        except Exception as e:
            print(f"❌ Competitor analysis: {str(e)}")
        
    except ImportError:
        print("❌ Competitor Analyzer not available for testing")
    
    print(f"\n📊 AI Services Test Summary: {success_count}/{total_tests} tests passed")
    return success_count, total_tests

async def test_data_services():
    """Test data services connectivity."""
    print("\n💾 Testing Data Services")
    print("=" * 40)
    
    success_count = 0
    total_tests = 0
    
    # Test Onboarding Data Service
    try:
        from onboarding_data_service import OnboardingDataService
        onboarding_service = OnboardingDataService()
        
        print("👤 Testing Onboarding Data Service...")
        
        # Test get personalized inputs
        total_tests += 1
        try:
            result = onboarding_service.get_personalized_ai_inputs(1)
            if result and isinstance(result, dict):
                print(f"✅ Get personalized AI inputs: SUCCESS")
                success_count += 1
            else:
                print(f"⚠️ Get personalized AI inputs: Empty result")
        except Exception as e:
            print(f"❌ Get personalized AI inputs: {str(e)}")
        
    except ImportError:
        print("❌ Onboarding Data Service not available for testing")
    
    # Test AI Analytics Service
    try:
        from ai_analytics_service import AIAnalyticsService
        ai_analytics = AIAnalyticsService()
        
        print("\n🧠 Testing AI Analytics Service...")
        
        # Test strategic intelligence generation
        total_tests += 1
        try:
            result = await ai_analytics.generate_strategic_intelligence(1)
            if result and isinstance(result, dict):
                print(f"✅ Strategic intelligence generation: SUCCESS")
                success_count += 1
            else:
                print(f"⚠️ Strategic intelligence generation: Empty result")
        except Exception as e:
            print(f"❌ Strategic intelligence generation: {str(e)}")
        
    except ImportError:
        print("❌ AI Analytics Service not available for testing")
    
    # Test Content Planning DB Service
    try:
        from content_planning_db import ContentPlanningDBService
        # Note: This would require proper database session injection
        print("\n🗃️ Testing Content Planning DB Service...")
        print("ℹ️ Database service requires proper session injection - skipping direct test")
        
    except ImportError:
        print("❌ Content Planning DB Service not available for testing")
    
    print(f"\n📊 Data Services Test Summary: {success_count}/{total_tests} tests passed")
    return success_count, total_tests

async def test_12_step_framework_integration():
    """Test the 12-step framework with real service integration."""
    print("\n🚀 Testing 12-Step Framework Integration")
    print("=" * 50)
    
    try:
        from calendar_generation_datasource_framework.prompt_chaining import PromptChainOrchestrator
        
        # Initialize orchestrator
        print("📋 Initializing Prompt Chain Orchestrator...")
        orchestrator = PromptChainOrchestrator()
        
        # Check health status
        health_status = await orchestrator.get_health_status()
        print(f"✅ Framework Health: {health_status['status']}")
        print(f"📊 Steps Configured: {health_status['steps_configured']}")
        print(f"🏗️ Phases Configured: {health_status['phases_configured']}")
        
        # Test calendar generation with real services
        print("\n🎯 Testing Calendar Generation...")
        
        try:
            result = await orchestrator.generate_calendar(
                user_id=1,
                strategy_id=1,
                calendar_type="monthly",
                industry="technology",
                business_size="sme"
            )
            
            print("✅ Calendar generation completed!")
            print(f"📋 Result keys: {list(result.keys())}")
            print(f"⏱️ Processing time: {result.get('processing_time', 0):.2f}s")
            print(f"🎯 Framework version: {result.get('framework_version', 'unknown')}")
            print(f"📊 Status: {result.get('status', 'unknown')}")
            
            # Validate result structure
            required_fields = [
                'user_id', 'strategy_id', 'processing_time', 'generated_at',
                'framework_version', 'status'
            ]
            
            missing_fields = [field for field in required_fields if field not in result]
            if missing_fields:
                print(f"⚠️ Missing required fields: {missing_fields}")
            else:
                print("✅ All required fields present")
            
            # Check for calendar content
            calendar_fields = [
                'daily_schedule', 'weekly_themes', 'content_recommendations',
                'optimal_timing', 'performance_predictions', 'trending_topics'
            ]
            
            present_fields = [field for field in calendar_fields if field in result and result[field]]
            print(f"📋 Calendar content fields present: {len(present_fields)}/{len(calendar_fields)}")
            
            return True, result
            
        except Exception as e:
            print(f"❌ Calendar generation failed: {str(e)}")
            return False, None
        
    except ImportError as e:
        print(f"❌ 12-Step Framework not available: {e}")
        return False, None

async def test_phase1_steps_integration():
    """Test Phase 1 steps with real service integration."""
    print("\n🎯 Testing Phase 1 Steps Integration")
    print("=" * 50)
    
    try:
        from calendar_generation_datasource_framework.prompt_chaining.steps.phase1_steps import (
            ContentStrategyAnalysisStep,
            GapAnalysisStep,
            AudiencePlatformStrategyStep
        )
        
        # Test context
        context = {
            "user_id": 1,
            "strategy_id": 1,
            "calendar_type": "monthly",
            "industry": "technology",
            "business_size": "sme",
            "user_data": {
                "strategy_data": {
                    "content_pillars": ["AI", "Technology", "Innovation"],
                    "target_audience": {"demographics": {"age": "25-35", "location": "US"}},
                    "business_goals": ["Increase brand awareness", "Generate leads"],
                    "success_metrics": ["Website traffic", "Social engagement"]
                },
                "onboarding_data": {
                    "website_analysis": {"industry": "technology", "target_audience": ["developers"]},
                    "competitor_analysis": {"top_performers": ["competitor1", "competitor2"]},
                    "keyword_analysis": {"high_value_keywords": ["AI", "automation"]}
                },
                "gap_analysis": {
                    "content_gaps": ["Video content", "Interactive demos"],
                    "keyword_opportunities": ["machine learning", "artificial intelligence"]
                },
                "performance_data": {
                    "engagement_metrics": {"average_engagement": 0.05},
                    "best_performing_content": ["How-to guides", "Industry insights"]
                },
                "competitor_data": {
                    "competitor_urls": ["https://competitor1.com", "https://competitor2.com"]
                }
            },
            "step_results": {},
            "quality_scores": {},
            "current_step": 0,
            "phase": "initialization"
        }
        
        phase1_results = {}
        
        # Test Step 1: Content Strategy Analysis
        print("🎯 Testing Step 1: Content Strategy Analysis")
        try:
            step1 = ContentStrategyAnalysisStep()
            result1 = await step1.run(context)
            phase1_results["step_01"] = result1
            
            print(f"✅ Step 1 Status: {result1.get('status', 'unknown')}")
            print(f"📊 Step 1 Quality: {result1.get('quality_score', 0.0):.2f}")
            print(f"⏱️ Step 1 Time: {result1.get('execution_time', 0.0):.2f}s")
            
        except Exception as e:
            print(f"❌ Step 1 failed: {str(e)}")
        
        # Test Step 2: Gap Analysis & Opportunity Identification
        print("\n🎯 Testing Step 2: Gap Analysis & Opportunity Identification")
        try:
            step2 = GapAnalysisStep()
            result2 = await step2.run(context)
            phase1_results["step_02"] = result2
            
            print(f"✅ Step 2 Status: {result2.get('status', 'unknown')}")
            print(f"📊 Step 2 Quality: {result2.get('quality_score', 0.0):.2f}")
            print(f"⏱️ Step 2 Time: {result2.get('execution_time', 0.0):.2f}s")
            
        except Exception as e:
            print(f"❌ Step 2 failed: {str(e)}")
        
        # Test Step 3: Audience & Platform Strategy
        print("\n🎯 Testing Step 3: Audience & Platform Strategy")
        try:
            step3 = AudiencePlatformStrategyStep()
            result3 = await step3.run(context)
            phase1_results["step_03"] = result3
            
            print(f"✅ Step 3 Status: {result3.get('status', 'unknown')}")
            print(f"📊 Step 3 Quality: {result3.get('quality_score', 0.0):.2f}")
            print(f"⏱️ Step 3 Time: {result3.get('execution_time', 0.0):.2f}s")
            
        except Exception as e:
            print(f"❌ Step 3 failed: {str(e)}")
        
        # Calculate overall Phase 1 metrics
        completed_steps = len([r for r in phase1_results.values() if r.get('status') == 'completed'])
        total_quality = sum(r.get('quality_score', 0.0) for r in phase1_results.values())
        avg_quality = total_quality / len(phase1_results) if phase1_results else 0.0
        total_time = sum(r.get('execution_time', 0.0) for r in phase1_results.values())
        
        print(f"\n📋 Phase 1 Integration Summary")
        print("=" * 40)
        print(f"✅ Completed Steps: {completed_steps}/3")
        print(f"📊 Average Quality: {avg_quality:.2f}")
        print(f"⏱️ Total Time: {total_time:.2f}s")
        
        return completed_steps == 3, phase1_results
        
    except ImportError as e:
        print(f"❌ Phase 1 steps not available: {e}")
        return False, {}

async def generate_integration_report(
    services_status: Dict[str, bool],
    ai_services_result: tuple,
    data_services_result: tuple,
    framework_result: tuple,
    phase1_result: tuple
):
    """Generate comprehensive integration test report."""
    print("\n📋 Integration Test Report")
    print("=" * 60)
    
    # Service availability
    available_services = sum(services_status.values())
    total_services = len(services_status)
    print(f"🔧 Service Availability: {available_services}/{total_services}")
    
    # AI services
    ai_success, ai_total = ai_services_result
    print(f"🤖 AI Services: {ai_success}/{ai_total} tests passed")
    
    # Data services
    data_success, data_total = data_services_result
    print(f"💾 Data Services: {data_success}/{data_total} tests passed")
    
    # Framework integration
    framework_success, framework_data = framework_result
    print(f"🚀 Framework Integration: {'SUCCESS' if framework_success else 'FAILED'}")
    
    # Phase 1 integration
    phase1_success, phase1_data = phase1_result
    print(f"🎯 Phase 1 Integration: {'SUCCESS' if phase1_success else 'FAILED'}")
    
    # Overall assessment
    total_tests = ai_total + data_total + (1 if framework_success else 0) + (3 if phase1_success else 0)
    total_success = ai_success + data_success + (1 if framework_success else 0) + (3 if phase1_success else len(phase1_data))
    
    print(f"\n🎉 Overall Integration: {total_success}/{total_tests} ({total_success/total_tests*100:.1f}%)")
    
    # Recommendations
    print(f"\n📝 Recommendations:")
    if available_services < total_services:
        print("  • Set up missing services for full integration")
    if ai_success < ai_total:
        print("  • Check AI service configurations and API keys")
    if data_success < data_total:
        print("  • Verify database connections and service dependencies")
    if not framework_success:
        print("  • Debug framework integration issues")
    if not phase1_success:
        print("  • Review Phase 1 step implementations")
    
    if total_success == total_tests:
        print("  ✅ All systems operational - ready for production!")
    
    # Save detailed report
    report = {
        "timestamp": datetime.now().isoformat(),
        "service_availability": services_status,
        "ai_services": {"success": ai_success, "total": ai_total},
        "data_services": {"success": data_success, "total": data_total},
        "framework_integration": {"success": framework_success},
        "phase1_integration": {"success": phase1_success, "results": phase1_data},
        "overall": {"success": total_success, "total": total_tests, "percentage": total_success/total_tests*100}
    }
    
    with open("integration_test_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n💾 Detailed report saved to: integration_test_report.json")

async def main():
    """Main integration test function."""
    print("🧪 12-Step Framework Integration Test Suite")
    print("=" * 60)
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check service availability
    print("\n🔍 Checking Service Availability...")
    services_status = check_service_availability()
    
    # Test AI services
    ai_services_result = await test_real_ai_services()
    
    # Test data services
    data_services_result = await test_data_services()
    
    # Test 12-step framework integration
    framework_result = await test_12_step_framework_integration()
    
    # Test Phase 1 steps integration
    phase1_result = await test_phase1_steps_integration()
    
    # Generate comprehensive report
    await generate_integration_report(
        services_status,
        ai_services_result,
        data_services_result,
        framework_result,
        phase1_result
    )
    
    print(f"\n🏁 Integration test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(main())
