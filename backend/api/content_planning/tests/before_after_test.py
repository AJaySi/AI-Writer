"""
Before/After Comparison Test for Content Planning Module
Automated comparison of API responses before and after refactoring.
"""

import asyncio
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
import requests
from loguru import logger
import difflib

class BeforeAfterComparisonTest:
    """Automated comparison of API responses before and after refactoring."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.baseline_responses = {}
        self.refactored_responses = {}
        self.comparison_results = {}
        self.session = requests.Session()
        
    def load_baseline_data(self, baseline_file: str = "functionality_test_results.json"):
        """Load baseline data from functionality test results."""
        try:
            with open(baseline_file, 'r') as f:
                baseline_data = json.load(f)
            
            # Extract response data from baseline
            for test_name, result in baseline_data.items():
                if result.get("status") == "passed" and result.get("response_data"):
                    self.baseline_responses[test_name] = result["response_data"]
            
            logger.info(f"✅ Loaded baseline data with {len(self.baseline_responses)} responses")
            return True
        except FileNotFoundError:
            logger.error(f"❌ Baseline file {baseline_file} not found")
            return False
        except Exception as e:
            logger.error(f"❌ Error loading baseline data: {str(e)}")
            return False
    
    async def capture_refactored_responses(self) -> Dict[str, Any]:
        """Capture responses from refactored API."""
        logger.info("🔍 Capturing responses from refactored API")
        
        # Define test scenarios
        test_scenarios = [
            {
                "name": "health_check",
                "method": "GET",
                "endpoint": "/api/content-planning/health",
                "data": None
            },
            {
                "name": "strategies_get",
                "method": "GET",
                "endpoint": "/api/content-planning/strategies/?user_id=1",
                "data": None
            },
            {
                "name": "calendar_events_get",
                "method": "GET",
                "endpoint": "/api/content-planning/calendar-events/?strategy_id=1",
                "data": None
            },
            {
                "name": "gap_analysis_get",
                "method": "GET",
                "endpoint": "/api/content-planning/gap-analysis/?user_id=1",
                "data": None
            },
            {
                "name": "ai_analytics_get",
                "method": "GET",
                "endpoint": "/api/content-planning/ai-analytics/?user_id=1",
                "data": None
            },
            {
                "name": "comprehensive_user_data",
                "method": "GET",
                "endpoint": "/api/content-planning/calendar-generation/comprehensive-user-data?user_id=1",
                "data": None
            },
            {
                "name": "strategy_create",
                "method": "POST",
                "endpoint": "/api/content-planning/strategies/",
                "data": {
                    "user_id": 1,
                    "name": "Comparison Test Strategy",
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
            },
            {
                "name": "calendar_generation",
                "method": "POST",
                "endpoint": "/api/content-planning/calendar-generation/generate-calendar",
                "data": {
                    "user_id": 1,
                    "strategy_id": 1,
                    "calendar_type": "monthly",
                    "industry": "technology",
                    "business_size": "sme",
                    "force_refresh": False
                }
            },
            {
                "name": "content_optimization",
                "method": "POST",
                "endpoint": "/api/content-planning/calendar-generation/optimize-content",
                "data": {
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
            },
            {
                "name": "trending_topics",
                "method": "GET",
                "endpoint": "/api/content-planning/calendar-generation/trending-topics?user_id=1&industry=technology&limit=5",
                "data": None
            }
        ]
        
        for scenario in test_scenarios:
            try:
                if scenario["method"] == "GET":
                    response = self.session.get(f"{self.base_url}{scenario['endpoint']}")
                elif scenario["method"] == "POST":
                    response = self.session.post(
                        f"{self.base_url}{scenario['endpoint']}",
                        json=scenario["data"]
                    )
                
                self.refactored_responses[scenario["name"]] = {
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "response_data": response.json() if response.status_code == 200 else None,
                    "headers": dict(response.headers)
                }
                
                logger.info(f"✅ Captured {scenario['name']}: {response.status_code}")
                
            except Exception as e:
                logger.error(f"❌ Failed to capture {scenario['name']}: {str(e)}")
                self.refactored_responses[scenario["name"]] = {
                    "error": str(e),
                    "status_code": None,
                    "response_data": None
                }
        
        return self.refactored_responses
    
    def compare_responses(self) -> Dict[str, Any]:
        """Compare baseline and refactored responses."""
        logger.info("🔍 Comparing baseline and refactored responses")
        
        comparison_results = {}
        
        for test_name in self.baseline_responses.keys():
            if test_name in self.refactored_responses:
                baseline = self.baseline_responses[test_name]
                refactored = self.refactored_responses[test_name]
                
                comparison = self._compare_single_response(test_name, baseline, refactored)
                comparison_results[test_name] = comparison
                
                if comparison["status"] == "passed":
                    logger.info(f"✅ {test_name}: Responses match")
                else:
                    logger.warning(f"⚠️ {test_name}: Responses differ")
            else:
                logger.warning(f"⚠️ {test_name}: No refactored response found")
                comparison_results[test_name] = {
                    "status": "failed",
                    "reason": "No refactored response found"
                }
        
        return comparison_results
    
    def _compare_single_response(self, test_name: str, baseline: Any, refactored: Any) -> Dict[str, Any]:
        """Compare a single response pair."""
        try:
            # Check if refactored response has error
            if isinstance(refactored, dict) and refactored.get("error"):
                return {
                    "status": "failed",
                    "reason": f"Refactored API error: {refactored['error']}",
                    "baseline": baseline,
                    "refactored": refactored
                }
            
            # Get response data
            baseline_data = baseline if isinstance(baseline, dict) else baseline
            refactored_data = refactored.get("response_data") if isinstance(refactored, dict) else refactored
            
            # Compare status codes
            baseline_status = 200  # Assume success for baseline
            refactored_status = refactored.get("status_code", 200) if isinstance(refactored, dict) else 200
            
            if baseline_status != refactored_status:
                return {
                    "status": "failed",
                    "reason": f"Status code mismatch: baseline={baseline_status}, refactored={refactored_status}",
                    "baseline_status": baseline_status,
                    "refactored_status": refactored_status,
                    "baseline": baseline_data,
                    "refactored": refactored_data
                }
            
            # Compare response structure
            structure_match = self._compare_structure(baseline_data, refactored_data)
            if not structure_match["match"]:
                return {
                    "status": "failed",
                    "reason": "Response structure mismatch",
                    "structure_diff": structure_match["differences"],
                    "baseline": baseline_data,
                    "refactored": refactored_data
                }
            
            # Compare response content
            content_match = self._compare_content(baseline_data, refactored_data)
            if not content_match["match"]:
                return {
                    "status": "failed",
                    "reason": "Response content mismatch",
                    "content_diff": content_match["differences"],
                    "baseline": baseline_data,
                    "refactored": refactored_data
                }
            
            # Compare performance
            performance_match = self._compare_performance(baseline, refactored)
            
            return {
                "status": "passed",
                "structure_match": structure_match,
                "content_match": content_match,
                "performance_match": performance_match,
                "baseline": baseline_data,
                "refactored": refactored_data
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "reason": f"Comparison error: {str(e)}",
                "baseline": baseline,
                "refactored": refactored
            }
    
    def _compare_structure(self, baseline: Any, refactored: Any) -> Dict[str, Any]:
        """Compare the structure of two responses."""
        try:
            if type(baseline) != type(refactored):
                return {
                    "match": False,
                    "differences": f"Type mismatch: baseline={type(baseline)}, refactored={type(refactored)}"
                }
            
            if isinstance(baseline, dict):
                baseline_keys = set(baseline.keys())
                refactored_keys = set(refactored.keys())
                
                missing_keys = baseline_keys - refactored_keys
                extra_keys = refactored_keys - baseline_keys
                
                if missing_keys or extra_keys:
                    return {
                        "match": False,
                        "differences": {
                            "missing_keys": list(missing_keys),
                            "extra_keys": list(extra_keys)
                        }
                    }
                
                # Recursively compare nested structures
                for key in baseline_keys:
                    nested_comparison = self._compare_structure(baseline[key], refactored[key])
                    if not nested_comparison["match"]:
                        return {
                            "match": False,
                            "differences": f"Nested structure mismatch at key '{key}': {nested_comparison['differences']}"
                        }
            
            elif isinstance(baseline, list):
                if len(baseline) != len(refactored):
                    return {
                        "match": False,
                        "differences": f"List length mismatch: baseline={len(baseline)}, refactored={len(refactored)}"
                    }
                
                # Compare list items (assuming order matters)
                for i, (baseline_item, refactored_item) in enumerate(zip(baseline, refactored)):
                    nested_comparison = self._compare_structure(baseline_item, refactored_item)
                    if not nested_comparison["match"]:
                        return {
                            "match": False,
                            "differences": f"List item mismatch at index {i}: {nested_comparison['differences']}"
                        }
            
            return {"match": True, "differences": None}
            
        except Exception as e:
            return {
                "match": False,
                "differences": f"Structure comparison error: {str(e)}"
            }
    
    def _compare_content(self, baseline: Any, refactored: Any) -> Dict[str, Any]:
        """Compare the content of two responses."""
        try:
            if baseline == refactored:
                return {"match": True, "differences": None}
            
            # For dictionaries, compare key values
            if isinstance(baseline, dict) and isinstance(refactored, dict):
                differences = {}
                for key in baseline.keys():
                    if key in refactored:
                        if baseline[key] != refactored[key]:
                            differences[key] = {
                                "baseline": baseline[key],
                                "refactored": refactored[key]
                            }
                    else:
                        differences[key] = {
                            "baseline": baseline[key],
                            "refactored": "missing"
                        }
                
                if differences:
                    return {
                        "match": False,
                        "differences": differences
                    }
                else:
                    return {"match": True, "differences": None}
            
            # For lists, compare items
            elif isinstance(baseline, list) and isinstance(refactored, list):
                if len(baseline) != len(refactored):
                    return {
                        "match": False,
                        "differences": f"List length mismatch: baseline={len(baseline)}, refactored={len(refactored)}"
                    }
                
                differences = []
                for i, (baseline_item, refactored_item) in enumerate(zip(baseline, refactored)):
                    if baseline_item != refactored_item:
                        differences.append({
                            "index": i,
                            "baseline": baseline_item,
                            "refactored": refactored_item
                        })
                
                if differences:
                    return {
                        "match": False,
                        "differences": differences
                    }
                else:
                    return {"match": True, "differences": None}
            
            # For other types, direct comparison
            else:
                return {
                    "match": baseline == refactored,
                    "differences": {
                        "baseline": baseline,
                        "refactored": refactored
                    } if baseline != refactored else None
                }
                
        except Exception as e:
            return {
                "match": False,
                "differences": f"Content comparison error: {str(e)}"
            }
    
    def _compare_performance(self, baseline: Any, refactored: Any) -> Dict[str, Any]:
        """Compare performance metrics."""
        try:
            baseline_time = baseline.get("response_time", 0) if isinstance(baseline, dict) else 0
            refactored_time = refactored.get("response_time", 0) if isinstance(refactored, dict) else 0
            
            time_diff = abs(refactored_time - baseline_time)
            time_diff_percentage = (time_diff / baseline_time * 100) if baseline_time > 0 else 0
            
            # Consider performance acceptable if within 50% of baseline
            is_acceptable = time_diff_percentage <= 50
            
            return {
                "baseline_time": baseline_time,
                "refactored_time": refactored_time,
                "time_difference": time_diff,
                "time_difference_percentage": time_diff_percentage,
                "is_acceptable": is_acceptable
            }
            
        except Exception as e:
            return {
                "error": f"Performance comparison error: {str(e)}",
                "is_acceptable": False
            }
    
    def generate_comparison_report(self) -> str:
        """Generate a detailed comparison report."""
        report = []
        report.append("=" * 80)
        report.append("BEFORE/AFTER COMPARISON REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("")
        
        total_tests = len(self.comparison_results)
        passed_tests = sum(1 for r in self.comparison_results.values() if r.get("status") == "passed")
        failed_tests = total_tests - passed_tests
        
        report.append(f"SUMMARY:")
        report.append(f"  Total Tests: {total_tests}")
        report.append(f"  Passed: {passed_tests}")
        report.append(f"  Failed: {failed_tests}")
        report.append(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        report.append("")
        
        if failed_tests > 0:
            report.append("FAILED TESTS:")
            report.append("-" * 40)
            for test_name, result in self.comparison_results.items():
                if result.get("status") == "failed":
                    report.append(f"  {test_name}:")
                    report.append(f"    Reason: {result.get('reason', 'Unknown')}")
                    if "structure_diff" in result:
                        report.append(f"    Structure Differences: {result['structure_diff']}")
                    if "content_diff" in result:
                        report.append(f"    Content Differences: {result['content_diff']}")
                    report.append("")
        
        report.append("DETAILED RESULTS:")
        report.append("-" * 40)
        for test_name, result in self.comparison_results.items():
            report.append(f"  {test_name}: {result.get('status', 'unknown')}")
            if result.get("status") == "passed":
                performance = result.get("performance_match", {})
                if performance.get("is_acceptable"):
                    report.append(f"    Performance: ✅ Acceptable")
                else:
                    report.append(f"    Performance: ⚠️ Degraded")
                report.append(f"    Response Time: {performance.get('refactored_time', 0):.3f}s")
            report.append("")
        
        return "\n".join(report)
    
    async def run_comparison(self, baseline_file: str = "functionality_test_results.json") -> Dict[str, Any]:
        """Run the complete before/after comparison."""
        logger.info("🧪 Starting before/after comparison test")
        
        # Load baseline data
        if not self.load_baseline_data(baseline_file):
            logger.error("❌ Failed to load baseline data")
            return {"status": "failed", "reason": "Baseline data not available"}
        
        # Capture refactored responses
        await self.capture_refactored_responses()
        
        # Compare responses
        self.comparison_results = self.compare_responses()
        
        # Generate report
        report = self.generate_comparison_report()
        print(report)
        
        # Save detailed results
        with open("before_after_comparison_results.json", "w") as f:
            json.dump({
                "comparison_results": self.comparison_results,
                "baseline_responses": self.baseline_responses,
                "refactored_responses": self.refactored_responses,
                "report": report
            }, f, indent=2, default=str)
        
        logger.info("✅ Before/after comparison completed")
        return self.comparison_results

def run_before_after_comparison():
    """Run the before/after comparison test."""
    test = BeforeAfterComparisonTest()
    results = asyncio.run(test.run_comparison())
    
    # Print summary
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r.get("status") == "passed")
    failed_tests = total_tests - passed_tests
    
    print(f"\nComparison Summary:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {failed_tests}")
    print(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests == 0:
        print("🎉 All tests passed! Refactoring maintains functionality.")
    else:
        print(f"⚠️ {failed_tests} tests failed. Review differences carefully.")
    
    return results

if __name__ == "__main__":
    run_before_after_comparison() 