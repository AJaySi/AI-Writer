"""
Test Runner for Content Planning Module
Simple script to run functionality tests and establish baseline.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import the test modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from functionality_test import run_functionality_test
from before_after_test import run_before_after_comparison
from test_data import TestData

def run_baseline_test():
    """Run the baseline functionality test to establish current state."""
    print("🧪 Running baseline functionality test...")
    print("=" * 60)
    
    try:
        results = run_functionality_test()
        
        # Print summary
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get("status") == "passed")
        failed_tests = total_tests - passed_tests
        
        print(f"\nBaseline Test Summary:")
        print(f"  Total Tests: {total_tests}")
        print(f"  Passed: {passed_tests}")
        print(f"  Failed: {failed_tests}")
        print(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            print("🎉 All baseline tests passed!")
            return True
        else:
            print(f"⚠️ {failed_tests} baseline tests failed.")
            return False
            
    except Exception as e:
        print(f"❌ Baseline test failed: {str(e)}")
        return False

def run_comparison_test():
    """Run the before/after comparison test."""
    print("\n🔄 Running before/after comparison test...")
    print("=" * 60)
    
    try:
        results = run_before_after_comparison()
        
        # Print summary
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get("status") == "passed")
        failed_tests = total_tests - passed_tests
        
        print(f"\nComparison Test Summary:")
        print(f"  Total Tests: {total_tests}")
        print(f"  Passed: {passed_tests}")
        print(f"  Failed: {failed_tests}")
        print(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            print("🎉 All comparison tests passed! Refactoring maintains functionality.")
            return True
        else:
            print(f"⚠️ {failed_tests} comparison tests failed. Review differences carefully.")
            return False
            
    except Exception as e:
        print(f"❌ Comparison test failed: {str(e)}")
        return False

def main():
    """Main test runner function."""
    print("🚀 Content Planning Module Test Runner")
    print("=" * 60)
    
    # Check if baseline file exists
    baseline_file = "functionality_test_results.json"
    baseline_exists = os.path.exists(baseline_file)
    
    if not baseline_exists:
        print("📋 No baseline found. Running baseline test first...")
        baseline_success = run_baseline_test()
        
        if not baseline_success:
            print("❌ Baseline test failed. Cannot proceed with comparison.")
            return False
    else:
        print("✅ Baseline file found. Skipping baseline test.")
    
    # Run comparison test
    comparison_success = run_comparison_test()
    
    if comparison_success:
        print("\n🎉 All tests completed successfully!")
        return True
    else:
        print("\n❌ Some tests failed. Please review the results.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 