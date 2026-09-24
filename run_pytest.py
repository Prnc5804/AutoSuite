"""
Test Runner Script - PyTest
Run all pytest-based tests with HTML report generation.
"""

import subprocess
import sys
import os
from datetime import datetime


def run_pytest_suite():
    """Run all pytest test cases and generate an HTML report."""

    # Create reports directory
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    os.makedirs(reports_dir, exist_ok=True)

    # Generate timestamp for report filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(reports_dir, f"pytest_report_{timestamp}.html")

    print("=" * 70)
    print("SELENIUM AUTOMATION FRAMEWORK - PYTEST TEST RUNNER")
    print(f"HTML Report: {report_file}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Build pytest command
    pytest_args = [
        sys.executable, "-m", "pytest",
        "tests/test_login_pytest.py",
        "tests/test_search_pytest.py",
        "-v",
        "--tb=short",
        f"--html={report_file}",
        "--self-contained-html",
    ]

    print(f"\nRunning: {' '.join(pytest_args)}\n")

    # Run pytest as subprocess
    result = subprocess.run(pytest_args, cwd=os.path.dirname(os.path.abspath(__file__)))

    print(f"\nHTML Report saved to: {report_file}")
    return result.returncode


def run_pytest_by_marker(marker):
    """
    Run pytest tests filtered by marker.

    Args:
        marker (str): Marker name (e.g., 'smoke', 'regression', 'login', 'search').
    """
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    os.makedirs(reports_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(reports_dir, f"pytest_{marker}_report_{timestamp}.html")

    print(f"Running tests with marker: {marker}")

    pytest_args = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "-m", marker,
        f"--html={report_file}",
        "--self-contained-html",
    ]

    result = subprocess.run(pytest_args, cwd=os.path.dirname(os.path.abspath(__file__)))
    print(f"Report saved to: {report_file}")
    return result.returncode


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run by marker if provided (e.g., python run_pytest.py smoke)
        marker_name = sys.argv[1]
        run_pytest_by_marker(marker_name)
    else:
        run_pytest_suite()
