#!/usr/bin/env python3
"""
Final test to verify real AI integration is working.
"""

import requests
import json
import sys

def test_ai_analytics_real_data():
    """Test that AI analytics endpoint returns real AI insights."""
    try:
        print("🧪 Testing AI Analytics Real Data")
        print("=" * 40)
        
        response = requests.get("http://localhost:8000/api/content-planning/ai-analytics/", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ AI Analytics endpoint: PASSED")
            print(f"   - Status: {response.status_code}")
            print(f"   - AI Service Status: {data.get('ai_service_status', 'unknown')}")
            print(f"   - Total Insights: {data.get('total_insights', 0)}")
            print(f"   - Total Recommendations: {data.get('total_recommendations', 0)}")
            
            # Check if we have real AI insights
            insights = data.get('insights', [])
            if len(insights) > 0:
                print(f"   - Real AI Insights Found: {len(insights)}")
                for i, insight in enumerate(insights[:2]):  # Show first 2 insights
                    print(f"     {i+1}. {insight.get('title', 'No title')} ({insight.get('type', 'unknown')})")
                    print(f"        Priority: {insight.get('priority', 'unknown')}")
                    print(f"        Description: {insight.get('description', 'No description')[:80]}...")
            else:
                print("   - No insights found")
            
            # Check recommendations
            recommendations = data.get('recommendations', [])
            if len(recommendations) > 0:
                print(f"   - Real AI Recommendations Found: {len(recommendations)}")
                for i, rec in enumerate(recommendations[:2]):  # Show first 2 recommendations
                    print(f"     {i+1}. {rec.get('title', 'No title')} (Confidence: {rec.get('confidence', 0)}%)")
            else:
                print("   - No recommendations found")
            
            # Verify it's not mock data
            if data.get('ai_service_status') == 'operational':
                print("✅ Real AI Integration: CONFIRMED")
                return True
            else:
                print("❌ Still using fallback/mock data")
                return False
                
        else:
            print(f"❌ AI Analytics endpoint: FAILED (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ AI Analytics test failed: {e}")
        return False

def test_strategies_endpoint():
    """Test that strategies endpoint works without user_id."""
    try:
        print("\n🧪 Testing Strategies Endpoint")
        print("=" * 35)
        
        response = requests.get("http://localhost:8000/api/content-planning/strategies/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Strategies endpoint: PASSED")
            print(f"   - Status: {response.status_code}")
            print(f"   - Strategies found: {len(data)}")
            
            if len(data) > 0:
                strategy = data[0]
                print(f"   - Strategy name: {strategy.get('name', 'Unknown')}")
                print(f"   - Industry: {strategy.get('industry', 'Unknown')}")
                print(f"   - Content pillars: {len(strategy.get('content_pillars', []))}")
            
            return True
        else:
            print(f"❌ Strategies endpoint: FAILED (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Strategies test failed: {e}")
        return False

def test_gap_analysis_endpoint():
    """Test that gap analysis endpoint works without user_id."""
    try:
        print("\n🧪 Testing Gap Analysis Endpoint")
        print("=" * 35)
        
        response = requests.get("http://localhost:8000/api/content-planning/gap-analysis/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Gap analysis endpoint: PASSED")
            print(f"   - Status: {response.status_code}")
            print(f"   - Analyses found: {len(data)}")
            
            if len(data) > 0:
                analysis = data[0]
                print(f"   - Website: {analysis.get('website_url', 'Unknown')}")
                print(f"   - Competitors: {len(analysis.get('competitor_urls', []))}")
                print(f"   - Keywords: {len(analysis.get('target_keywords', []))}")
            
            return True
        else:
            print(f"❌ Gap analysis endpoint: FAILED (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Gap analysis test failed: {e}")
        return False

def main():
    """Run all final tests."""
    print("🧪 Final AI Integration Test")
    print("=" * 50)
    
    tests = [
        test_ai_analytics_real_data,
        test_strategies_endpoint,
        test_gap_analysis_endpoint
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Final Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 SUCCESS: All endpoints working with real AI integration!")
        print("✅ 422 errors fixed")
        print("✅ Real AI insights being generated")
        print("✅ UI should now show real data instead of mock data")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 