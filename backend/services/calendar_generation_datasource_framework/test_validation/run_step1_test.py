"""
Step 1 Test Execution Script
Runs comprehensive validation for Step 1 of the 12-step calendar generation process.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from loguru import logger

# Add the services directory to the path for proper imports
services_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)

try:
    from test_validation.step1_validator import Step1Validator
except ImportError as e:
    logger.error(f"Import error: {e}")
    raise ImportError("Step1Validator not available")


class Step1TestRunner:
    """
    Test runner for Step 1 validation with comprehensive logging and reporting.
    """
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.test_results = {}
        self.execution_summary = {}
        
    def _setup_logger(self):
        """Setup structured logging for test execution."""
        logger.remove()
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO"
        )
        return logger
    
    async def run_step1_validation_test(self, user_id: int = 1, strategy_id: int = 1):
        """Run comprehensive Step 1 validation test."""
        
        test_start = time.time()
        self.logger.info("🚀 Starting Step 1 Validation Test Suite")
        self.logger.info(f"📋 Test Parameters: user_id={user_id}, strategy_id={strategy_id}")
        
        try:
            # Initialize validator
            validator = Step1Validator()
            
            # Run validation
            validation_result = await validator.validate_step1(user_id, strategy_id)
            
            # Process results
            self._process_validation_results(validation_result)
            
            # Generate test summary
            test_summary = self._generate_test_summary(test_start)
            
            # Save results
            self._save_test_results(validation_result, test_summary)
            
            # Display results
            self._display_test_results(validation_result, test_summary)
            
            return {
                "validation_result": validation_result,
                "test_summary": test_summary,
                "status": "completed"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Test execution failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _process_validation_results(self, validation_result: dict):
        """Process and analyze validation results."""
        self.logger.info("📊 Processing validation results...")
        
        if "validation_report" in validation_result:
            report = validation_result["validation_report"]
            
            # Extract key metrics
            self.test_results["overall_status"] = report.get("overall_status", "unknown")
            self.test_results["execution_summary"] = report.get("execution_summary", {})
            self.test_results["quality_metrics"] = report.get("quality_metrics", {})
            self.test_results["performance_metrics"] = report.get("performance_metrics", {})
            self.test_results["recommendations"] = report.get("recommendations", [])
            
            # Analyze data flow trace
            self._analyze_data_flow_trace(report.get("data_flow_trace", []))
            
        else:
            self.logger.warning("⚠️ No validation report found in results")
    
    def _analyze_data_flow_trace(self, data_flow_trace: list):
        """Analyze data flow trace for insights."""
        self.logger.info("🔍 Analyzing data flow trace...")
        
        analysis = {
            "total_phases": len(data_flow_trace),
            "phase_analysis": {},
            "performance_insights": {},
            "quality_insights": {}
        }
        
        for i, phase in enumerate(data_flow_trace):
            phase_name = phase.get("phase", f"phase_{i}")
            results = phase.get("validation_results", {})
            
            # Phase performance analysis
            execution_time = results.get("execution_time", 0.0)
            analysis["phase_analysis"][phase_name] = {
                "execution_time": execution_time,
                "status": results.get("status", "unknown"),
                "data_completeness": results.get("data_completeness", 0.0) if "data_completeness" in results else None,
                "quality_score": results.get("data_quality_score", 0.0) if "data_quality_score" in results else None
            }
        
        # Performance insights
        execution_times = [phase.get("execution_time", 0.0) for phase in data_flow_trace]
        analysis["performance_insights"] = {
            "total_time": sum(execution_times),
            "average_time": sum(execution_times) / len(execution_times) if execution_times else 0.0,
            "slowest_phase": max(execution_times) if execution_times else 0.0,
            "fastest_phase": min(execution_times) if execution_times else 0.0
        }
        
        self.test_results["data_flow_analysis"] = analysis
    
    def _generate_test_summary(self, test_start: float) -> dict:
        """Generate comprehensive test summary."""
        test_time = time.time() - test_start
        
        summary = {
            "test_execution": {
                "timestamp": datetime.utcnow().isoformat(),
                "test_duration": test_time,
                "test_type": "step1_validation",
                "test_version": "1.0"
            },
            "overall_results": {
                "status": self.test_results.get("overall_status", "unknown"),
                "success_rate": self._calculate_success_rate(),
                "quality_score": self.test_results.get("quality_metrics", {}).get("overall_quality_score", 0.0),
                "performance_score": self.test_results.get("performance_metrics", {}).get("performance_score", 0.0)
            },
            "key_findings": self._extract_key_findings(),
            "recommendations": self.test_results.get("recommendations", [])
        }
        
        return summary
    
    def _calculate_success_rate(self) -> float:
        """Calculate overall success rate."""
        execution_summary = self.test_results.get("execution_summary", {})
        total_phases = execution_summary.get("total_phases", 0)
        successful_phases = execution_summary.get("successful_phases", 0)
        
        return (successful_phases / total_phases * 100) if total_phases > 0 else 0.0
    
    def _extract_key_findings(self) -> list:
        """Extract key findings from test results."""
        findings = []
        
        # Data utilization findings
        data_flow_analysis = self.test_results.get("data_flow_analysis", {})
        if data_flow_analysis:
            performance_insights = data_flow_analysis.get("performance_insights", {})
            findings.append(f"Total execution time: {performance_insights.get('total_time', 0.0):.2f}s")
            findings.append(f"Average phase time: {performance_insights.get('average_time', 0.0):.2f}s")
        
        # Quality findings
        quality_metrics = self.test_results.get("quality_metrics", {})
        if quality_metrics:
            findings.append(f"Overall quality score: {quality_metrics.get('overall_quality_score', 0.0):.1f}%")
            findings.append(f"Data completeness: {quality_metrics.get('data_completeness', 0.0):.1f}%")
        
        # Performance findings
        performance_metrics = self.test_results.get("performance_metrics", {})
        if performance_metrics:
            findings.append(f"Performance score: {performance_metrics.get('performance_score', 0.0):.1f}%")
        
        return findings
    
    def _save_test_results(self, validation_result: dict, test_summary: dict):
        """Save test results to file."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"step1_validation_results_{timestamp}.json"
        
        results_data = {
            "test_summary": test_summary,
            "validation_result": validation_result,
            "test_results": self.test_results
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(results_data, f, indent=2, default=str)
            
            self.logger.info(f"💾 Test results saved to: {filename}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to save test results: {str(e)}")
    
    def _display_test_results(self, validation_result: dict, test_summary: dict):
        """Display test results in a formatted way."""
        print("\n" + "="*80)
        print("🎯 STEP 1 VALIDATION TEST RESULTS")
        print("="*80)
        
        # Test Summary
        print(f"\n📋 Test Summary:")
        print(f"   Timestamp: {test_summary['test_execution']['timestamp']}")
        print(f"   Duration: {test_summary['test_execution']['test_duration']:.2f}s")
        print(f"   Status: {test_summary['overall_results']['status']}")
        print(f"   Success Rate: {test_summary['overall_results']['success_rate']:.1f}%")
        print(f"   Quality Score: {test_summary['overall_results']['quality_score']:.1f}%")
        print(f"   Performance Score: {test_summary['overall_results']['performance_score']:.1f}%")
        
        # Key Findings
        print(f"\n🔍 Key Findings:")
        for finding in test_summary['key_findings']:
            print(f"   • {finding}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        for recommendation in test_summary['recommendations']:
            print(f"   • {recommendation}")
        
        # Data Flow Analysis
        data_flow_analysis = self.test_results.get("data_flow_analysis", {})
        if data_flow_analysis:
            print(f"\n📊 Data Flow Analysis:")
            performance_insights = data_flow_analysis.get("performance_insights", {})
            print(f"   Total Phases: {data_flow_analysis.get('total_phases', 0)}")
            print(f"   Total Time: {performance_insights.get('total_time', 0.0):.2f}s")
            print(f"   Average Time: {performance_insights.get('average_time', 0.0):.2f}s")
            print(f"   Slowest Phase: {performance_insights.get('slowest_phase', 0.0):.2f}s")
            print(f"   Fastest Phase: {performance_insights.get('fastest_phase', 0.0):.2f}s")
        
        print("\n" + "="*80)
    
    async def run_multiple_tests(self, test_configs: list):
        """Run multiple tests with different configurations."""
        self.logger.info(f"🔄 Running {len(test_configs)} test configurations...")
        
        all_results = []
        
        for i, config in enumerate(test_configs):
            self.logger.info(f"🧪 Test {i+1}/{len(test_configs)}: {config}")
            
            try:
                result = await self.run_step1_validation_test(
                    user_id=config.get("user_id", 1),
                    strategy_id=config.get("strategy_id", 1)
                )
                all_results.append({
                    "config": config,
                    "result": result
                })
                
            except Exception as e:
                self.logger.error(f"❌ Test {i+1} failed: {str(e)}")
                all_results.append({
                    "config": config,
                    "result": {"status": "failed", "error": str(e)}
                })
        
        return all_results


# Test configurations
TEST_CONFIGURATIONS = [
    {"user_id": 1, "strategy_id": 1, "description": "Standard test"},
    {"user_id": 2, "strategy_id": 2, "description": "Alternative user test"},
    {"user_id": 1, "strategy_id": 3, "description": "Different strategy test"}
]


async def main():
    """Main test execution function."""
    print("🎯 Step 1 Validation Test Suite")
    print("=" * 50)
    
    # Initialize test runner
    test_runner = Step1TestRunner()
    
    # Run single test
    print("\n🧪 Running Single Test...")
    result = await test_runner.run_step1_validation_test()
    
    # Run multiple tests (optional)
    if len(sys.argv) > 1 and sys.argv[1] == "--multiple":
        print("\n🔄 Running Multiple Tests...")
        multiple_results = await test_runner.run_multiple_tests(TEST_CONFIGURATIONS)
        
        print(f"\n📊 Multiple Test Summary:")
        successful_tests = sum(1 for r in multiple_results if r["result"].get("status") == "completed")
        print(f"   Successful: {successful_tests}/{len(multiple_results)}")
    
    return result


if __name__ == "__main__":
    import time
    asyncio.run(main())
