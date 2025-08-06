"""
Comprehensive Functionality Test for Content Planning Module
Tests all existing endpoints and functionality to establish baseline before refactoring.
"""

import asyncio
import json
import time
from typing import Dict, Any, List
from datetime import datetime, timedelta
import requests
from loguru import logger

class ContentPlanningFunctionalityTest:
    """Comprehensive test suite for content planning functionality."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = {}
        self.baseline_data = {}
        self.session = requests.Session()
        
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all functionality tests and return results."""
        logger.info("🧪 Starting comprehensive functionality test suite")
        
        test_suites = [
            self.test_health_endpoints,
            self.test_strategy_endpoints,
            self.test_calendar_endpoints,
            self.test_gap_analysis_endpoints,
            self.test_ai_analytics_endpoints,
            self.test_calendar_generation_endpoints,
            self.test_content_optimization_endpoints,
            self.test_performance_prediction_endpoints,
            self.test_content_repurposing_endpoints,
            self.test_trending_topics_endpoints,
            self.test_comprehensive_user_data_endpoints,
            self.test_error_scenarios,
            self.test_data_validation,
            self.test_response_formats,
            self.test_performance_metrics
        ]
        
        for test_suite in test_suites:
            try:
                await test_suite()
            except Exception as e:
                logger.error(f"❌ Test suite {test_suite.__name__} failed: {str(e)}")
                self.test_results[test_suite.__name__] = {
                    "status": "failed",
                    "error": str(e)
                }
        
        logger.info("✅ Functionality test suite completed")
        return self.test_results
    
    async def test_health_endpoints(self):
        """Test health check endpoints."""
        logger.info("🔍 Testing health endpoints")
        
        endpoints = [
            "/api/content-planning/health",
            "/api/content-planning/database/health",
            "/api/content-planning/health/backend",
            "/api/content-planning/health/ai",
            "/api/content-planning/ai-analytics/health",
            "/api/content-planning/calendar-generation/health"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                self.test_results[f"health_{endpoint.split('/')[-1]}"] = {
                    "status": "passed" if response.status_code == 200 else "failed",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "response_data": response.json() if response.status_code == 200 else None
                }
                logger.info(f"✅ Health endpoint {endpoint}: {response.status_code}")
            except Exception as e:
                logger.error(f"❌ Health endpoint {endpoint} failed: {str(e)}")
                self.test_results[f"health_{endpoint.split('/')[-1]}"] = {
                    "status": "failed",
                    "error": str(e)
                }
    
    async def test_strategy_endpoints(self):
        """Test strategy CRUD endpoints."""
        logger.info("🔍 Testing strategy endpoints")
        
        # Test data
        strategy_data = {
            "user_id": 1,
            "name": "Test Strategy",
            "industry": "technology",
            "target_audience": {
                "age_range": "25-45",
                "interests": ["technology", "innovation"],
                "location": "global"
            },
            "content_pillars": [
                {"name": "Educational Content", "percentage": 40},
                {"name": "Thought Leadership", "percentage": 30},
                {"name": "Product Updates", "percentage": 30}
            ],
            "ai_recommendations": {
                "priority_topics": ["AI", "Machine Learning"],
                "content_frequency": "daily",
                "platform_focus": ["LinkedIn", "Website"]
            }
        }
        
        # Test CREATE strategy
        try:
            response = self.session.post(
                f"{self.base_url}/api/content-planning/strategies/",
                json=strategy_data
            )
            self.test_results["strategy_create"] = {
                "status": "passed" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code == 200 else None
            }
            
            if response.status_code == 200:
                strategy_id = response.json().get("id")
                self.baseline_data["strategy_id"] = strategy_id
                logger.info(f"✅ Strategy created with ID: {strategy_id}")
            else:
                logger.warning(f"⚠️ Strategy creation failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Strategy creation failed: {str(e)}")
            self.test_results["strategy_create"] = {
                "status": "failed",
                "error": str(e)
            }
        
        # Test GET strategies
        try:
            response = self.session.get(
                f"{self.base_url}/api/content-planning/strategies/?user_id=1"
            )
            self.test_results["strategy_get_all"] = {
                "status": "passed" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code == 200 else None
            }
            logger.info(f"✅ Get strategies: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Get strategies failed: {str(e)}")
            self.test_results["strategy_get_all"] = {
                "status": "failed",
                "error": str(e)
            }
        
        # Test GET specific strategy
        if self.baseline_data.get("strategy_id"):
            try:
                response = self.session.get(
                    f"{self.base_url}/api/content-planning/strategies/{self.baseline_data['strategy_id']}"
                )
                self.test_results["strategy_get_specific"] = {
                    "status": "passed" if response.status_code == 200 else "failed",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "response_data": response.json() if response.status_code == 200 else None
                }
                logger.info(f"✅ Get specific strategy: {response.status_code}")
            except Exception as e:
                logger.error(f"❌ Get specific strategy failed: {str(e)}")
                self.test_results["strategy_get_specific"] = {
                    "status": "failed",
                    "error": str(e)
                }
    
    async def test_calendar_endpoints(self):
        """Test calendar event endpoints."""
        logger.info("🔍 Testing calendar endpoints")
        
        # Test data
        event_data = {
            "strategy_id": self.baseline_data.get("strategy_id", 1),
            "title": "Test Calendar Event",
            "description": "This is a test calendar event for functionality testing",
            "content_type": "blog_post",
            "platform": "website",
            "scheduled_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "ai_recommendations": {
                "optimal_time": "09:00",
                "hashtags": ["#test", "#content"],
                "tone": "professional"
            }
        }
        
        # Test CREATE calendar event
        try:
            response = self.session.post(
                f"{self.base_url}/api/content-planning/calendar-events/",
                json=event_data
            )
            self.test_results["calendar_create"] = {
                "status": "passed" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code == 200 else None
            }
            
            if response.status_code == 200:
                event_id = response.json().get("id")
                self.baseline_data["event_id"] = event_id
                logger.info(f"✅ Calendar event created with ID: {event_id}")
            else:
                logger.warning(f"⚠️ Calendar event creation failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Calendar event creation failed: {str(e)}")
            self.test_results["calendar_create"] = {
                "status": "failed",
                "error": str(e)
            }
        
        # Test GET calendar events
        try:
            response = self.session.get(
                f"{self.base_url}/api/content-planning/calendar-events/?strategy_id={self.baseline_data.get('strategy_id', 1)}"
            )
            self.test_results["calendar_get_all"] = {
                "status": "passed" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code == 200 else None
            }
            logger.info(f"✅ Get calendar events: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Get calendar events failed: {str(e)}")
            self.test_results["calendar_get_all"] = {
                "status": "failed",
                "error": str(e)
            }
    
    async def test_gap_analysis_endpoints(self):
        """Test gap analysis endpoints."""
        logger.info("🔍 Testing gap analysis endpoints")
        
        # Test data
        gap_analysis_data = {
            "user_id": 1,
            "website_url": "https://example.com",
            "competitor_urls": ["https://competitor1.com", "https://competitor2.com"],
            "target_keywords": ["content marketing", "digital strategy"],
            "industry": "technology"
        }
        
        # Test CREATE gap analysis
        try:
            response = self.session.post(
                f"{self.base_url}/api/content-planning/gap-analysis/",
                json=gap_analysis_data
            )
            self.test_results["gap_analysis_create"] = {
                "status": "passed" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code == 200 else None
            }
            
            if response.status_code == 200:
                analysis_id = response.json().get("id")
                self.baseline_data["analysis_id"] = analysis_id
                logger.info(f"✅ Gap analysis created with ID: {analysis_id}")
            else:
                logger.warning(f"⚠️ Gap analysis creation failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Gap analysis creation failed: {str(e)}")
            self.test_results["gap_analysis_create"] = {
                "status": "failed",
                "error": str(e)
            }
        
        # Test GET gap analyses
        try:
            response = self.session.get(
                f"{self.base_url}/api/content-planning/gap-analysis/?user_id=1"
            )
            self.test_results["gap_analysis_get_all"] = {
                "status": "passed" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code == 200 else None
            }
            logger.info(f"✅ Get gap analyses: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Get gap analyses failed: {str(e)}")
            self.test_results["gap_analysis_get_all"] = {
                "status": "failed",
                "error": str(e)
            }
    
    async def test_ai_analytics_endpoints(self):
        """Test AI analytics endpoints."""
        logger.info("🔍 Testing AI analytics endpoints")
        
        # Test GET AI analytics
        try:
            response = self.session.get(
                f"{self.base_url}/api/content-planning/ai-analytics/?user_id=1"
            )
            self.test_results["ai_analytics_get"] = {
                "status": "passed" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code == 200 else None
            }
            logger.info(f"✅ Get AI analytics: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Get AI analytics failed: {str(e)}")
            self.test_results["ai_analytics_get"] = {
                "status": "failed",
                "error": str(e)
            }
        
        # Test content evolution analysis
        evolution_data = {
            "strategy_id": self.baseline_data.get("strategy_id", 1),
            "time_period": "30d"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/content-planning/ai-analytics/content-evolution",
                json=evolution_data
            )
            self.test_results["ai_analytics_evolution"] = {
                "status": "passed" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code == 200 else None
            }
            logger.info(f"✅ Content evolution analysis: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Content evolution analysis failed: {str(e)}")
            self.test_results["ai_analytics_evolution"] = {
                "status": "failed",
                "error": str(e)
            }
    
    async def test_calendar_generation_endpoints(self):
        """Test calendar generation endpoints."""
        logger.info("🔍 Testing calendar generation endpoints")
        
        # Test calendar generation
        calendar_data = {
            "user_id": 1,
            "strategy_id": self.baseline_data.get("strategy_id", 1),
            "calendar_type": "monthly",
            "industry": "technology",
            "business_size": "sme",
            "force_refresh": False
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/content-planning/generate-calendar",
                json=calendar_data
            )
            self.test_results["calendar_generation"] = {
                "status": "passed" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code == 200 else None
            }
            logger.info(f"✅ Calendar generation: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Calendar generation failed: {str(e)}")
            self.test_results["calendar_generation"] = {
                "status": "failed",
                "error": str(e)
            }
    
    async def test_content_optimization_endpoints(self):
        """Test content optimization endpoints."""
        logger.info("🔍 Testing content optimization endpoints")
        
        # Test content optimization
        optimization_data = {
            "user_id": 1,
            "title": "Test Content Title",
            "description": "This is test content for optimization",
            "content_type": "blog_post",
            "target_platform": "linkedin",
            "original_content": {
                "title": "Original Title",
                "content": "Original content text"
            }
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/content-planning/optimize-content",
                json=optimization_data
            )
            self.test_results["content_optimization"] = {
                "status": "passed" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code == 200 else None
            }
            logger.info(f"✅ Content optimization: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Content optimization failed: {str(e)}")
            self.test_results["content_optimization"] = {
                "status": "failed",
                "error": str(e)
            }
    
    async def test_performance_prediction_endpoints(self):
        """Test performance prediction endpoints."""
        logger.info("🔍 Testing performance prediction endpoints")
        
        # Test performance prediction
        prediction_data = {
            "user_id": 1,
            "strategy_id": self.baseline_data.get("strategy_id", 1),
            "content_type": "blog_post",
            "platform": "linkedin",
            "content_data": {
                "title": "Test Content",
                "description": "Test content description",
                "hashtags": ["#test", "#content"]
            }
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/content-planning/performance-predictions",
                json=prediction_data
            )
            self.test_results["performance_prediction"] = {
                "status": "passed" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code == 200 else None
            }
            logger.info(f"✅ Performance prediction: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Performance prediction failed: {str(e)}")
            self.test_results["performance_prediction"] = {
                "status": "failed",
                "error": str(e)
            }
    
    async def test_content_repurposing_endpoints(self):
        """Test content repurposing endpoints."""
        logger.info("🔍 Testing content repurposing endpoints")
        
        # Test content repurposing
        repurposing_data = {
            "user_id": 1,
            "strategy_id": self.baseline_data.get("strategy_id", 1),
            "original_content": {
                "title": "Original Content",
                "content": "Original content text",
                "platform": "website"
            },
            "target_platforms": ["linkedin", "twitter", "instagram"]
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/content-planning/repurpose-content",
                json=repurposing_data
            )
            self.test_results["content_repurposing"] = {
                "status": "passed" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code == 200 else None
            }
            logger.info(f"✅ Content repurposing: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Content repurposing failed: {str(e)}")
            self.test_results["content_repurposing"] = {
                "status": "failed",
                "error": str(e)
            }
    
    async def test_trending_topics_endpoints(self):
        """Test trending topics endpoints."""
        logger.info("🔍 Testing trending topics endpoints")
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/content-planning/trending-topics?user_id=1&industry=technology&limit=5"
            )
            self.test_results["trending_topics"] = {
                "status": "passed" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code == 200 else None
            }
            logger.info(f"✅ Trending topics: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Trending topics failed: {str(e)}")
            self.test_results["trending_topics"] = {
                "status": "failed",
                "error": str(e)
            }
    
    async def test_comprehensive_user_data_endpoints(self):
        """Test comprehensive user data endpoints."""
        logger.info("🔍 Testing comprehensive user data endpoints")
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/content-planning/comprehensive-user-data?user_id=1"
            )
            self.test_results["comprehensive_user_data"] = {
                "status": "passed" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code == 200 else None
            }
            logger.info(f"✅ Comprehensive user data: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Comprehensive user data failed: {str(e)}")
            self.test_results["comprehensive_user_data"] = {
                "status": "failed",
                "error": str(e)
            }
    
    async def test_error_scenarios(self):
        """Test error handling scenarios."""
        logger.info("🔍 Testing error scenarios")
        
        # Test invalid user ID
        try:
            response = self.session.get(
                f"{self.base_url}/api/content-planning/strategies/?user_id=999999"
            )
            self.test_results["error_invalid_user"] = {
                "status": "passed" if response.status_code in [404, 400] else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code != 200 else None
            }
            logger.info(f"✅ Error handling (invalid user): {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Error handling test failed: {str(e)}")
            self.test_results["error_invalid_user"] = {
                "status": "failed",
                "error": str(e)
            }
        
        # Test invalid strategy ID
        try:
            response = self.session.get(
                f"{self.base_url}/api/content-planning/strategies/999999"
            )
            self.test_results["error_invalid_strategy"] = {
                "status": "passed" if response.status_code in [404, 400] else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code != 200 else None
            }
            logger.info(f"✅ Error handling (invalid strategy): {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Error handling test failed: {str(e)}")
            self.test_results["error_invalid_strategy"] = {
                "status": "failed",
                "error": str(e)
            }
    
    async def test_data_validation(self):
        """Test data validation scenarios."""
        logger.info("🔍 Testing data validation")
        
        # Test invalid strategy data
        invalid_strategy_data = {
            "user_id": "invalid",  # Should be int
            "name": "",  # Should not be empty
            "industry": "invalid_industry"  # Should be valid industry
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/content-planning/strategies/",
                json=invalid_strategy_data
            )
            self.test_results["validation_invalid_strategy"] = {
                "status": "passed" if response.status_code in [422, 400] else "failed",
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "response_data": response.json() if response.status_code != 200 else None
            }
            logger.info(f"✅ Data validation (invalid strategy): {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Data validation test failed: {str(e)}")
            self.test_results["validation_invalid_strategy"] = {
                "status": "failed",
                "error": str(e)
            }
    
    async def test_response_formats(self):
        """Test response format consistency."""
        logger.info("🔍 Testing response formats")
        
        # Test strategy response format
        try:
            response = self.session.get(
                f"{self.base_url}/api/content-planning/strategies/?user_id=1"
            )
            if response.status_code == 200:
                data = response.json()
                has_required_fields = all(
                    field in data for field in ["strategies", "total_strategies"]
                )
                self.test_results["response_format_strategies"] = {
                    "status": "passed" if has_required_fields else "failed",
                    "has_required_fields": has_required_fields,
                    "response_structure": list(data.keys()) if isinstance(data, dict) else None
                }
                logger.info(f"✅ Response format (strategies): {has_required_fields}")
            else:
                self.test_results["response_format_strategies"] = {
                    "status": "failed",
                    "status_code": response.status_code
                }
        except Exception as e:
            logger.error(f"❌ Response format test failed: {str(e)}")
            self.test_results["response_format_strategies"] = {
                "status": "failed",
                "error": str(e)
            }
    
    async def test_performance_metrics(self):
        """Test performance metrics."""
        logger.info("🔍 Testing performance metrics")
        
        # Test response times for key endpoints
        endpoints_to_test = [
            "/api/content-planning/health",
            "/api/content-planning/strategies/?user_id=1",
            "/api/content-planning/calendar-events/?strategy_id=1",
            "/api/content-planning/gap-analysis/?user_id=1"
        ]
        
        performance_results = {}
        
        for endpoint in endpoints_to_test:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{endpoint}")
                end_time = time.time()
                
                response_time = end_time - start_time
                performance_results[endpoint] = {
                    "response_time": response_time,
                    "status_code": response.status_code,
                    "is_successful": response.status_code == 200
                }
                
                logger.info(f"✅ Performance test {endpoint}: {response_time:.3f}s")
                
            except Exception as e:
                logger.error(f"❌ Performance test failed for {endpoint}: {str(e)}")
                performance_results[endpoint] = {
                    "error": str(e),
                    "is_successful": False
                }
        
        self.test_results["performance_metrics"] = {
            "status": "completed",
            "results": performance_results,
            "summary": {
                "total_endpoints": len(endpoints_to_test),
                "successful_requests": sum(1 for r in performance_results.values() if r.get("is_successful")),
                "average_response_time": sum(r.get("response_time", 0) for r in performance_results.values()) / len(endpoints_to_test)
            }
        }

def run_functionality_test():
    """Run the comprehensive functionality test."""
    test = ContentPlanningFunctionalityTest()
    results = asyncio.run(test.run_all_tests())
    
    # Print summary
    print("\n" + "="*60)
    print("FUNCTIONALITY TEST RESULTS SUMMARY")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r.get("status") == "passed")
    failed_tests = total_tests - passed_tests
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests > 0:
        print("\nFailed Tests:")
        for test_name, result in results.items():
            if result.get("status") == "failed":
                print(f"  - {test_name}: {result.get('error', 'Unknown error')}")
    
    # Save results to file
    with open("functionality_test_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nDetailed results saved to: functionality_test_results.json")
    print("="*60)
    
    return results

if __name__ == "__main__":
    run_functionality_test() 