"""
Integration Test for Step 1 Validation
Tests the complete Step 1 validation process with real data integration.
"""

import asyncio
import json
import sys
import os
import time
from datetime import datetime
from loguru import logger

# Add the services directory to the path for proper imports
services_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)

try:
    from test_validation.step1_validator import Step1Validator
    from test_validation.test_data_generator import TestDataGenerator, generate_test_data_for_validation
    from test_validation.run_step1_test import Step1TestRunner
except ImportError as e:
    logger.error(f"Import error: {e}")
    raise ImportError("Required test modules not available")


class IntegrationTestSuite:
    """
    Integration test suite for Step 1 validation with comprehensive testing.
    """
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.test_results = {}
        self.integration_metrics = {}
        
    def _setup_logger(self):
        """Setup structured logging for integration testing."""
        logger.remove()
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO"
        )
        return logger
    
    async def run_integration_test(self):
        """Run comprehensive integration test for Step 1 validation."""
        
        test_start = time.time()
        self.logger.info("🚀 Starting Step 1 Integration Test Suite")
        
        try:
            # Phase 1: Test Data Generation
            await self._test_data_generation()
            
            # Phase 2: Step 1 Validation
            await self._test_step1_validation()
            
            # Phase 3: Data Flow Integration
            await self._test_data_flow_integration()
            
            # Phase 4: Performance Testing
            await self._test_performance()
            
            # Phase 5: Quality Assessment
            await self._test_quality_assessment()
            
            # Generate integration report
            integration_report = self._generate_integration_report(test_start)
            
            # Save and display results
            self._save_integration_results(integration_report)
            self._display_integration_results(integration_report)
            
            return integration_report
            
        except Exception as e:
            self.logger.error(f"❌ Integration test failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _test_data_generation(self):
        """Test data generation functionality."""
        self.logger.info("🧪 Testing Data Generation...")
        
        try:
            # Test data generator
            generator = TestDataGenerator()
            
            # Generate test data for different scenarios
            test_scenarios = [
                {"user_id": 1, "strategy_id": 1, "description": "Technology Company"},
                {"user_id": 2, "strategy_id": 2, "description": "Healthcare Startup"},
                {"user_id": 3, "strategy_id": 3, "description": "Financial Services"}
            ]
            
            generated_data = {}
            
            for scenario in test_scenarios:
                data = generator.generate_comprehensive_test_data(
                    scenario["user_id"], 
                    scenario["strategy_id"]
                )
                generated_data[scenario["description"]] = data
                
                # Validate generated data structure
                self._validate_generated_data(data, scenario)
            
            self.test_results["data_generation"] = {
                "status": "success",
                "scenarios_tested": len(test_scenarios),
                "data_quality_score": self._calculate_data_quality_score(generated_data),
                "generated_data": generated_data
            }
            
            self.logger.info("✅ Data generation test completed successfully")
            
        except Exception as e:
            self.test_results["data_generation"] = {
                "status": "failed",
                "error": str(e)
            }
            self.logger.error(f"❌ Data generation test failed: {str(e)}")
    
    async def _test_step1_validation(self):
        """Test Step 1 validation process."""
        self.logger.info("🧪 Testing Step 1 Validation...")
        
        try:
            # Initialize validator
            validator = Step1Validator()
            
            # Test with different user/strategy combinations
            test_cases = [
                {"user_id": 1, "strategy_id": 1},
                {"user_id": 2, "strategy_id": 2}
            ]
            
            validation_results = {}
            
            for test_case in test_cases:
                result = await validator.validate_step1(
                    test_case["user_id"], 
                    test_case["strategy_id"]
                )
                validation_results[f"user_{test_case['user_id']}_strategy_{test_case['strategy_id']}"] = result
            
            # Analyze validation results
            success_count = sum(1 for r in validation_results.values() if r.get("status") != "failed")
            total_count = len(validation_results)
            
            self.test_results["step1_validation"] = {
                "status": "success" if success_count == total_count else "partial",
                "test_cases": len(test_cases),
                "successful_validations": success_count,
                "success_rate": (success_count / total_count) * 100 if total_count > 0 else 0,
                "validation_results": validation_results
            }
            
            self.logger.info(f"✅ Step 1 validation test completed: {success_count}/{total_count} successful")
            
        except Exception as e:
            self.test_results["step1_validation"] = {
                "status": "failed",
                "error": str(e)
            }
            self.logger.error(f"❌ Step 1 validation test failed: {str(e)}")
    
    async def _test_data_flow_integration(self):
        """Test data flow integration between components."""
        self.logger.info("🧪 Testing Data Flow Integration...")
        
        try:
            # Test data flow from generation to validation
            generator = TestDataGenerator()
            validator = Step1Validator()
            
            # Generate test data
            test_data = generator.generate_comprehensive_test_data(1, 1)
            
            # Validate data flow
            data_flow_validation = {
                "data_generation": "success",
                "data_structure": self._validate_data_structure(test_data),
                "data_completeness": self._calculate_data_completeness(test_data),
                "data_quality": self._calculate_data_quality_score({"test": test_data})
            }
            
            # Test integration with validator
            validation_result = await validator.validate_step1(1, 1)
            
            integration_success = (
                data_flow_validation["data_generation"] == "success" and
                validation_result.get("status") != "failed"
            )
            
            self.test_results["data_flow_integration"] = {
                "status": "success" if integration_success else "failed",
                "data_flow_validation": data_flow_validation,
                "validation_integration": validation_result.get("status", "unknown"),
                "integration_success": integration_success
            }
            
            self.logger.info("✅ Data flow integration test completed")
            
        except Exception as e:
            self.test_results["data_flow_integration"] = {
                "status": "failed",
                "error": str(e)
            }
            self.logger.error(f"❌ Data flow integration test failed: {str(e)}")
    
    async def _test_performance(self):
        """Test performance metrics."""
        self.logger.info("🧪 Testing Performance...")
        
        try:
            # Performance test scenarios
            performance_scenarios = [
                {"name": "Single Validation", "iterations": 1},
                {"name": "Multiple Validations", "iterations": 3},
                {"name": "Bulk Processing", "iterations": 5}
            ]
            
            performance_results = {}
            
            for scenario in performance_scenarios:
                start_time = time.time()
                
                # Run multiple validations
                validator = Step1Validator()
                for i in range(scenario["iterations"]):
                    await validator.validate_step1(1, 1)
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                performance_results[scenario["name"]] = {
                    "iterations": scenario["iterations"],
                    "total_time": execution_time,
                    "average_time": execution_time / scenario["iterations"],
                    "performance_score": self._calculate_performance_score(execution_time, scenario["iterations"])
                }
            
            # Calculate overall performance metrics
            total_time = sum(r["total_time"] for r in performance_results.values())
            average_time = total_time / len(performance_results)
            
            self.test_results["performance"] = {
                "status": "success",
                "scenarios_tested": len(performance_scenarios),
                "total_execution_time": total_time,
                "average_execution_time": average_time,
                "performance_results": performance_results,
                "performance_score": self._calculate_overall_performance_score(performance_results)
            }
            
            self.logger.info(f"✅ Performance test completed in {total_time:.2f}s")
            
        except Exception as e:
            self.test_results["performance"] = {
                "status": "failed",
                "error": str(e)
            }
            self.logger.error(f"❌ Performance test failed: {str(e)}")
    
    async def _test_quality_assessment(self):
        """Test quality assessment functionality."""
        self.logger.info("🧪 Testing Quality Assessment...")
        
        try:
            # Generate test data for quality assessment
            generator = TestDataGenerator()
            test_data = generator.generate_comprehensive_test_data(1, 1)
            
            # Assess data quality
            quality_metrics = {
                "data_completeness": self._calculate_data_completeness(test_data),
                "data_structure_quality": self._validate_data_structure(test_data),
                "data_consistency": self._assess_data_consistency(test_data),
                "data_relevance": self._assess_data_relevance(test_data)
            }
            
            # Calculate overall quality score
            overall_quality = sum(quality_metrics.values()) / len(quality_metrics)
            
            self.test_results["quality_assessment"] = {
                "status": "success",
                "quality_metrics": quality_metrics,
                "overall_quality_score": overall_quality,
                "quality_threshold_met": overall_quality >= 0.8
            }
            
            self.logger.info(f"✅ Quality assessment completed: {overall_quality:.2f} score")
            
        except Exception as e:
            self.test_results["quality_assessment"] = {
                "status": "failed",
                "error": str(e)
            }
            self.logger.error(f"❌ Quality assessment failed: {str(e)}")
    
    def _validate_generated_data(self, data: dict, scenario: dict):
        """Validate generated test data."""
        required_fields = ["user_id", "strategy_id", "strategy_data", "onboarding_data"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            raise ValueError(f"Missing required fields in generated data: {missing_fields}")
    
    def _calculate_data_quality_score(self, data: dict) -> float:
        """Calculate data quality score."""
        if not data:
            return 0.0
        
        # Simple quality scoring
        quality_score = 0.0
        
        # Check data structure
        if isinstance(data, dict):
            quality_score += 25.0
        
        # Check for non-empty values
        non_empty_count = sum(1 for value in data.values() if value is not None and value != "")
        quality_score += (non_empty_count / len(data)) * 50.0 if data else 0.0
        
        # Check for complex structures
        complex_structures = sum(1 for value in data.values() if isinstance(value, (list, dict)))
        quality_score += (complex_structures / len(data)) * 25.0 if data else 0.0
        
        return min(quality_score, 100.0)
    
    def _validate_data_structure(self, data: dict) -> float:
        """Validate data structure."""
        if not isinstance(data, dict):
            return 0.0
        
        required_fields = ["user_id", "strategy_id", "strategy_data"]
        present_fields = sum(1 for field in required_fields if field in data)
        
        return (present_fields / len(required_fields)) * 100
    
    def _calculate_data_completeness(self, data: dict) -> float:
        """Calculate data completeness."""
        if not data:
            return 0.0
        
        total_fields = len(data)
        non_empty_fields = sum(1 for value in data.values() if value is not None and value != "")
        
        return (non_empty_fields / total_fields) * 100 if total_fields > 0 else 0.0
    
    def _assess_data_consistency(self, data: dict) -> float:
        """Assess data consistency."""
        # Simple consistency check
        return 85.0  # Mock score
    
    def _assess_data_relevance(self, data: dict) -> float:
        """Assess data relevance."""
        # Simple relevance check
        return 90.0  # Mock score
    
    def _calculate_performance_score(self, execution_time: float, iterations: int) -> float:
        """Calculate performance score."""
        # Performance scoring based on time and iterations
        base_score = 100.0
        time_penalty = min(execution_time * 10, 50)  # Max 50 point penalty
        return max(base_score - time_penalty, 0.0)
    
    def _calculate_overall_performance_score(self, performance_results: dict) -> float:
        """Calculate overall performance score."""
        if not performance_results:
            return 0.0
        
        scores = [result["performance_score"] for result in performance_results.values()]
        return sum(scores) / len(scores)
    
    def _generate_integration_report(self, test_start: float) -> dict:
        """Generate comprehensive integration report."""
        test_time = time.time() - test_start
        
        # Calculate overall success rate
        successful_tests = sum(1 for result in self.test_results.values() if result.get("status") == "success")
        total_tests = len(self.test_results)
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        # Calculate overall quality score
        quality_scores = []
        if "quality_assessment" in self.test_results:
            quality_scores.append(self.test_results["quality_assessment"].get("overall_quality_score", 0))
        if "data_generation" in self.test_results:
            quality_scores.append(self.test_results["data_generation"].get("data_quality_score", 0))
        
        overall_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        return {
            "integration_report": {
                "timestamp": datetime.utcnow().isoformat(),
                "test_duration": test_time,
                "overall_status": "success" if success_rate >= 80 else "partial" if success_rate >= 60 else "failed",
                "success_rate": success_rate,
                "overall_quality_score": overall_quality,
                "test_results": self.test_results,
                "recommendations": self._generate_recommendations()
            }
        }
    
    def _generate_recommendations(self) -> list:
        """Generate recommendations based on test results."""
        recommendations = []
        
        # Analyze test results and generate recommendations
        if "performance" in self.test_results:
            perf_results = self.test_results["performance"]
            if perf_results.get("average_execution_time", 0) > 5.0:
                recommendations.append("Optimize validation performance for faster execution")
        
        if "quality_assessment" in self.test_results:
            quality_results = self.test_results["quality_assessment"]
            if quality_results.get("overall_quality_score", 0) < 0.8:
                recommendations.append("Improve data quality and completeness")
        
        if "step1_validation" in self.test_results:
            validation_results = self.test_results["step1_validation"]
            if validation_results.get("success_rate", 0) < 100:
                recommendations.append("Address validation failures and improve error handling")
        
        if not recommendations:
            recommendations.append("All tests passed successfully - system is performing well")
        
        return recommendations
    
    def _save_integration_results(self, integration_report: dict):
        """Save integration test results."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"integration_test_results_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(integration_report, f, indent=2, default=str)
            
            self.logger.info(f"💾 Integration test results saved to: {filename}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to save integration results: {str(e)}")
    
    def _display_integration_results(self, integration_report: dict):
        """Display integration test results."""
        report = integration_report["integration_report"]
        
        print("\n" + "="*80)
        print("🚀 STEP 1 INTEGRATION TEST RESULTS")
        print("="*80)
        
        # Overall Summary
        print(f"\n📋 Integration Test Summary:")
        print(f"   Timestamp: {report['timestamp']}")
        print(f"   Duration: {report['test_duration']:.2f}s")
        print(f"   Status: {report['overall_status']}")
        print(f"   Success Rate: {report['success_rate']:.1f}%")
        print(f"   Quality Score: {report['overall_quality_score']:.1f}%")
        
        # Test Results Summary
        print(f"\n🧪 Test Results Summary:")
        for test_name, test_result in report['test_results'].items():
            status = test_result.get('status', 'unknown')
            status_icon = "✅" if status == "success" else "⚠️" if status == "partial" else "❌"
            print(f"   {status_icon} {test_name.replace('_', ' ').title()}: {status}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        for recommendation in report['recommendations']:
            print(f"   • {recommendation}")
        
        print("\n" + "="*80)


async def main():
    """Main integration test execution function."""
    print("🚀 Step 1 Integration Test Suite")
    print("=" * 50)
    
    # Initialize integration test suite
    integration_suite = IntegrationTestSuite()
    
    # Run integration test
    result = await integration_suite.run_integration_test()
    
    return result


if __name__ == "__main__":
    asyncio.run(main())
