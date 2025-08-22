"""
Real Services Integration Test for 12-Step Prompt Chaining Framework

This script tests the complete integration using real AI services and database connections.
This test should be run from the backend/services directory or with proper PYTHONPATH setup.
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional

# Add the backend directory to Python path for proper imports
backend_dir = os.path.dirname(os.path.dirname(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

services_dir = os.path.dirname(__file__)
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)


async def test_real_ai_engine_service():
    """Test real AI Engine Service with proper error handling."""
    print("🤖 Testing Real AI Engine Service")
    print("=" * 40)
    
    try:
        from content_gap_analyzer.ai_engine_service import AIEngineService
        ai_engine = AIEngineService()
        
        # Test strategic insights generation
        print("🎯 Testing strategic insights generation...")
        try:
            result = await ai_engine.generate_strategic_insights(
                strategy_data={
                    "content_pillars": ["AI", "Technology", "Innovation"],
                    "target_audience": {"demographics": {"age": "25-35", "industry": "technology"}},
                    "business_goals": ["Increase brand awareness", "Generate leads"]
                },
                onboarding_data={
                    "website_analysis": {
                        "industry": "technology",
                        "target_audience": ["developers", "tech enthusiasts"],
                        "content_focus": ["tutorials", "industry insights"]
                    }
                },
                industry="technology",
                business_size="sme"
            )
            
            if result and isinstance(result, dict):
                print(f"✅ Strategic insights generation: SUCCESS")
                print(f"   - Result keys: {list(result.keys())}")
                if "strategic_insights" in result:
                    print(f"   - Insights count: {len(result['strategic_insights'])}")
                return True, result
            else:
                print(f"⚠️ Strategic insights generation: Empty result")
                return False, None
                
        except Exception as e:
            print(f"❌ Strategic insights generation failed: {str(e)}")
            return False, None
            
    except ImportError as e:
        print(f"❌ AI Engine Service not available: {e}")
        return False, None


async def test_real_keyword_researcher():
    """Test real Keyword Researcher service."""
    print("\n🔍 Testing Real Keyword Researcher")
    print("=" * 40)
    
    try:
        from content_gap_analyzer.keyword_researcher import KeywordResearcher
        keyword_researcher = KeywordResearcher()
        
        # Test keyword analysis
        print("🎯 Testing keyword analysis...")
        try:
            result = await keyword_researcher.analyze_keywords(
                target_keywords=["artificial intelligence", "machine learning", "automation", "AI tools"],
                industry="technology"
            )
            
            if result and isinstance(result, dict):
                print(f"✅ Keyword analysis: SUCCESS")
                print(f"   - Result keys: {list(result.keys())}")
                if "high_value_keywords" in result:
                    print(f"   - High-value keywords: {len(result['high_value_keywords'])}")
                return True, result
            else:
                print(f"⚠️ Keyword analysis: Empty result")
                return False, None
                
        except Exception as e:
            print(f"❌ Keyword analysis failed: {str(e)}")
            return False, None
            
    except ImportError as e:
        print(f"❌ Keyword Researcher not available: {e}")
        return False, None


async def test_real_onboarding_service():
    """Test real Onboarding Data Service."""
    print("\n👤 Testing Real Onboarding Data Service")
    print("=" * 40)
    
    try:
        from onboarding_data_service import OnboardingDataService
        onboarding_service = OnboardingDataService()
        
        # Test get personalized inputs
        print("🎯 Testing get personalized AI inputs...")
        try:
            result = onboarding_service.get_personalized_ai_inputs(1)
            
            if result and isinstance(result, dict):
                print(f"✅ Get personalized AI inputs: SUCCESS")
                print(f"   - Result keys: {list(result.keys())}")
                if "website_analysis" in result:
                    print(f"   - Website analysis available")
                if "keyword_analysis" in result:
                    print(f"   - Keyword analysis available")
                return True, result
            else:
                print(f"⚠️ Get personalized AI inputs: Empty result")
                return False, None
                
        except Exception as e:
            print(f"❌ Get personalized AI inputs failed: {str(e)}")
            return False, None
            
    except ImportError as e:
        print(f"❌ Onboarding Data Service not available: {e}")
        return False, None


async def test_real_data_processing():
    """Test real data processing modules."""
    print("\n💾 Testing Real Data Processing Modules")
    print("=" * 40)
    
    try:
        from calendar_generation_datasource_framework.data_processing import (
            ComprehensiveUserDataProcessor,
            StrategyDataProcessor,
            GapAnalysisDataProcessor
        )
        
        # Test comprehensive user data processor
        print("🎯 Testing ComprehensiveUserDataProcessor...")
        try:
            processor = ComprehensiveUserDataProcessor()
            result = await processor.get_comprehensive_user_data(1, 1)
            
            if result and isinstance(result, dict):
                print(f"✅ ComprehensiveUserDataProcessor: SUCCESS")
                print(f"   - Result keys: {list(result.keys())}")
                return True, result
            else:
                print(f"⚠️ ComprehensiveUserDataProcessor: Empty result")
                return False, None
                
        except Exception as e:
            print(f"❌ ComprehensiveUserDataProcessor failed: {str(e)}")
            return False, None
            
    except ImportError as e:
        print(f"❌ Data Processing modules not available: {e}")
        return False, None


async def test_phase1_with_real_services():
    """Test Phase 1 steps with real service integration."""
    print("\n🎯 Testing Phase 1 Steps with Real Services")
    print("=" * 50)
    
    try:
        from calendar_generation_datasource_framework.prompt_chaining.steps.phase1_steps import (
            ContentStrategyAnalysisStep,
            GapAnalysisStep,
            AudiencePlatformStrategyStep
        )
        
        # Get real data
        real_context = {
            "user_id": 1,
            "strategy_id": 1,
            "calendar_type": "monthly",
            "industry": "technology",
            "business_size": "sme",
            "user_data": {
                "strategy_data": {
                    "content_pillars": ["AI", "Technology", "Innovation", "Tutorials"],
                    "target_audience": {
                        "demographics": {"age": "25-35", "location": "US", "industry": "technology"},
                        "interests": ["AI", "machine learning", "programming", "tech trends"]
                    },
                    "business_goals": ["Increase brand awareness", "Generate leads", "Establish thought leadership"],
                    "success_metrics": ["Website traffic", "Social engagement", "Lead generation"]
                },
                "onboarding_data": {
                    "website_analysis": {
                        "industry": "technology",
                        "target_audience": ["developers", "tech enthusiasts", "AI researchers"],
                        "content_focus": ["tutorials", "industry insights", "product reviews"],
                        "competitive_landscape": ["competitor1.com", "competitor2.com"]
                    },
                    "competitor_analysis": {
                        "top_performers": ["OpenAI Blog", "Google AI Blog", "MIT Technology Review"],
                        "content_types": ["research papers", "tutorials", "industry news"]
                    },
                    "keyword_analysis": {
                        "high_value_keywords": ["artificial intelligence", "machine learning", "AI tools", "automation"],
                        "search_volume": {"artificial intelligence": 100000, "machine learning": 80000}
                    }
                },
                "gap_analysis": {
                    "content_gaps": ["Video tutorials", "Interactive demos", "Case studies", "Beginner guides"],
                    "keyword_opportunities": ["AI for beginners", "machine learning tutorial", "AI tools comparison"],
                    "implementation_priority": {"high": ["Video tutorials"], "medium": ["Case studies"]}
                },
                "performance_data": {
                    "engagement_metrics": {"average_engagement": 0.05, "peak_engagement_time": "9am-11am"},
                    "best_performing_content": ["How-to guides", "Industry insights", "Product comparisons"],
                    "platform_performance": {"linkedin": 0.08, "twitter": 0.03, "blog": 0.12}
                },
                "competitor_data": {
                    "competitor_urls": ["https://openai.com/blog", "https://ai.googleblog.com"],
                    "analysis_date": datetime.now().isoformat()
                }
            },
            "step_results": {},
            "quality_scores": {},
            "current_step": 0,
            "phase": "initialization"
        }
        
        phase1_results = {}
        total_execution_time = 0
        
        # Test Step 1: Content Strategy Analysis with real services
        print("🎯 Testing Step 1: Content Strategy Analysis with Real Services")
        try:
            step1 = ContentStrategyAnalysisStep()
            result1 = await step1.run(real_context)
            phase1_results["step_01"] = result1
            total_execution_time += result1.get('execution_time', 0.0)
            
            print(f"✅ Step 1 Status: {result1.get('status', 'unknown')}")
            print(f"📊 Step 1 Quality: {result1.get('quality_score', 0.0):.2f}")
            print(f"⏱️ Step 1 Time: {result1.get('execution_time', 0.0):.2f}s")
            
            # Check if real services were used
            step_result = result1.get('result', {})
            strategy_summary = step_result.get('content_strategy_summary', {})
            if strategy_summary.get('content_pillars'):
                print(f"   ✅ Real strategy data processed: {len(strategy_summary['content_pillars'])} pillars")
            
        except Exception as e:
            print(f"❌ Step 1 failed: {str(e)}")
            
        # Test Step 2: Gap Analysis with real services
        print("\n🎯 Testing Step 2: Gap Analysis & Opportunity Identification with Real Services")
        try:
            step2 = GapAnalysisStep()
            result2 = await step2.run(real_context)
            phase1_results["step_02"] = result2
            total_execution_time += result2.get('execution_time', 0.0)
            
            print(f"✅ Step 2 Status: {result2.get('status', 'unknown')}")
            print(f"📊 Step 2 Quality: {result2.get('quality_score', 0.0):.2f}")
            print(f"⏱️ Step 2 Time: {result2.get('execution_time', 0.0):.2f}s")
            
            # Check if real services were used
            step_result = result2.get('result', {})
            gap_analysis = step_result.get('prioritized_gaps', {})
            if gap_analysis.get('content_gaps'):
                print(f"   ✅ Real gap data processed: {len(gap_analysis['content_gaps'])} gaps")
            
        except Exception as e:
            print(f"❌ Step 2 failed: {str(e)}")
            
        # Test Step 3: Audience & Platform Strategy with real services
        print("\n🎯 Testing Step 3: Audience & Platform Strategy with Real Services")
        try:
            step3 = AudiencePlatformStrategyStep()
            result3 = await step3.run(real_context)
            phase1_results["step_03"] = result3
            total_execution_time += result3.get('execution_time', 0.0)
            
            print(f"✅ Step 3 Status: {result3.get('status', 'unknown')}")
            print(f"📊 Step 3 Quality: {result3.get('quality_score', 0.0):.2f}")
            print(f"⏱️ Step 3 Time: {result3.get('execution_time', 0.0):.2f}s")
            
            # Check if real services were used
            step_result = result3.get('result', {})
            audience_personas = step_result.get('audience_personas', {})
            if audience_personas.get('demographics'):
                print(f"   ✅ Real audience data processed")
            
        except Exception as e:
            print(f"❌ Step 3 failed: {str(e)}")
        
        # Calculate overall metrics
        completed_steps = len([r for r in phase1_results.values() if r.get('status') == 'completed'])
        total_quality = sum(r.get('quality_score', 0.0) for r in phase1_results.values())
        avg_quality = total_quality / len(phase1_results) if phase1_results else 0.0
        
        print(f"\n📋 Phase 1 Real Services Integration Summary")
        print("=" * 50)
        print(f"✅ Completed Steps: {completed_steps}/3")
        print(f"📊 Average Quality: {avg_quality:.2f}")
        print(f"⏱️ Total Time: {total_execution_time:.2f}s")
        
        return completed_steps == 3, phase1_results
        
    except ImportError as e:
        print(f"❌ Phase 1 steps not available: {e}")
        return False, {}


async def test_end_to_end_calendar_generation():
    """Test complete end-to-end calendar generation with real services."""
    print("\n🚀 Testing End-to-End Calendar Generation with Real Services")
    print("=" * 60)
    
    try:
        from calendar_generation_datasource_framework.prompt_chaining import PromptChainOrchestrator
        
        # Initialize orchestrator
        print("📋 Initializing Prompt Chain Orchestrator...")
        orchestrator = PromptChainOrchestrator()
        
        # Test full calendar generation
        print("🎯 Testing complete calendar generation...")
        
        try:
            result = await orchestrator.generate_calendar(
                user_id=1,
                strategy_id=1,
                calendar_type="monthly",
                industry="technology",
                business_size="sme"
            )
            
            print("✅ End-to-end calendar generation completed!")
            
            # Analyze result quality
            quality_score = result.get('quality_score', 0.0)
            ai_confidence = result.get('ai_confidence', 0.0)
            processing_time = result.get('processing_time', 0.0)
            
            print(f"📊 Quality Score: {quality_score:.2f}")
            print(f"🤖 AI Confidence: {ai_confidence:.2f}")
            print(f"⏱️ Processing Time: {processing_time:.2f}s")
            print(f"🎯 Framework Version: {result.get('framework_version', 'unknown')}")
            
            # Check calendar content completeness
            calendar_fields = [
                'daily_schedule', 'weekly_themes', 'content_recommendations',
                'optimal_timing', 'performance_predictions', 'trending_topics',
                'content_pillars', 'platform_strategies', 'gap_analysis_insights'
            ]
            
            present_fields = [field for field in calendar_fields if field in result and result[field]]
            completeness_score = len(present_fields) / len(calendar_fields) * 100
            
            print(f"📋 Content Completeness: {completeness_score:.1f}% ({len(present_fields)}/{len(calendar_fields)} fields)")
            
            # Check step results
            step_results = result.get('step_results_summary', {})
            completed_steps = len([s for s in step_results.values() if s.get('status') == 'completed'])
            
            print(f"🎯 Steps Completed: {completed_steps}/12")
            
            return True, {
                'quality_score': quality_score,
                'ai_confidence': ai_confidence,
                'processing_time': processing_time,
                'completeness_score': completeness_score,
                'completed_steps': completed_steps
            }
            
        except Exception as e:
            print(f"❌ End-to-end calendar generation failed: {str(e)}")
            return False, None
            
    except ImportError as e:
        print(f"❌ Prompt Chain Orchestrator not available: {e}")
        return False, None


async def generate_real_services_report(test_results: Dict[str, Any]):
    """Generate comprehensive real services integration report."""
    print("\n📋 Real Services Integration Report")
    print("=" * 60)
    
    # Service connectivity
    services_tested = 0
    services_working = 0
    
    for test_name, (success, data) in test_results.items():
        services_tested += 1
        if success:
            services_working += 1
            print(f"✅ {test_name}: SUCCESS")
        else:
            print(f"❌ {test_name}: FAILED")
    
    connectivity_score = services_working / services_tested * 100 if services_tested > 0 else 0
    print(f"\n🔧 Service Connectivity: {services_working}/{services_tested} ({connectivity_score:.1f}%)")
    
    # Phase 1 integration analysis
    if 'phase1_real_services' in test_results:
        phase1_success, phase1_data = test_results['phase1_real_services']
        if phase1_success:
            avg_quality = sum(r.get('quality_score', 0.0) for r in phase1_data.values()) / len(phase1_data)
            total_time = sum(r.get('execution_time', 0.0) for r in phase1_data.values())
            print(f"🎯 Phase 1 Quality: {avg_quality:.2f}")
            print(f"⏱️ Phase 1 Time: {total_time:.2f}s")
    
    # End-to-end analysis
    if 'e2e_calendar_generation' in test_results:
        e2e_success, e2e_data = test_results['e2e_calendar_generation']
        if e2e_success and e2e_data:
            print(f"🚀 E2E Quality: {e2e_data['quality_score']:.2f}")
            print(f"🤖 E2E Confidence: {e2e_data['ai_confidence']:.2f}")
            print(f"📋 E2E Completeness: {e2e_data['completeness_score']:.1f}%")
    
    # Overall assessment
    if connectivity_score >= 80:
        print(f"\n🎉 EXCELLENT: Real services integration ready for production!")
    elif connectivity_score >= 60:
        print(f"\n✅ GOOD: Most services working, minor issues to resolve")
    elif connectivity_score >= 40:
        print(f"\n⚠️ FAIR: Some services working, significant improvements needed")
    else:
        print(f"\n❌ POOR: Major service integration issues, requires attention")
    
    # Save detailed report
    report = {
        "timestamp": datetime.now().isoformat(),
        "service_connectivity": {
            "working": services_working,
            "tested": services_tested,
            "percentage": connectivity_score
        },
        "test_results": test_results,
        "overall_status": "excellent" if connectivity_score >= 80 else "good" if connectivity_score >= 60 else "fair" if connectivity_score >= 40 else "poor"
    }
    
    with open("real_services_integration_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n💾 Detailed report saved to: real_services_integration_report.json")


async def main():
    """Main real services integration test function."""
    print("🧪 Real Services Integration Test Suite")
    print("=" * 60)
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_results = {}
    
    # Test individual real services
    test_results['ai_engine'] = await test_real_ai_engine_service()
    test_results['keyword_researcher'] = await test_real_keyword_researcher()
    test_results['onboarding_service'] = await test_real_onboarding_service()
    test_results['data_processing'] = await test_real_data_processing()
    
    # Test Phase 1 with real services
    test_results['phase1_real_services'] = await test_phase1_with_real_services()
    
    # Test end-to-end calendar generation
    test_results['e2e_calendar_generation'] = await test_end_to_end_calendar_generation()
    
    # Generate comprehensive report
    await generate_real_services_report(test_results)
    
    print(f"\n🏁 Real services integration test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(main())
