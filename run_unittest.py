"""
Test Runner Script - Unittest
Run all unittest-based tests with HTMLTestRunner report generation.
"""

import unittest
import os
import sys
from datetime import datetime

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.test_login import TestLogin, TestLoginDataDriven
from tests.test_search import TestProductSearch, TestSearchDataDriven


def run_unittest_suite():
    """Run all unittest test cases and generate an HTML report."""

    # Create reports directory
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    os.makedirs(reports_dir, exist_ok=True)

    # Create test suite
    suite = unittest.TestSuite()

    # Add Login Tests
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLogin))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLoginDataDriven))

    # Add Search Tests
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestProductSearch))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSearchDataDriven))

    # Generate timestamp for report filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(reports_dir, f"unittest_report_{timestamp}.txt")

    print("=" * 70)
    print("SELENIUM AUTOMATION FRAMEWORK - UNITTEST TEST RUNNER")
    print(f"Report: {report_file}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    class DualStream:
        """Stream that writes to both console and report file."""
        def __init__(self, *streams):
            self.streams = streams
        def write(self, data):
            for s in self.streams:
                s.write(data)
                s.flush()
        def flush(self):
            for s in self.streams:
                s.flush()

    with open(report_file, "w", encoding="utf-8") as f:
        dual_stream = DualStream(sys.stdout, f)
        runner = unittest.TextTestRunner(stream=dual_stream, verbosity=2)
        result = runner.run(suite)

    # Summary
    print(f"\n======================================================================")
    print(f"Total tests: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print(f"======================================================================")
    print(f"Report saved to: {report_file}")

    return result


if __name__ == "__main__":
    run_unittest_suite()
