"""
Test runner script for easy test execution
Provides convenient methods to run different test suites
"""
import subprocess
import sys
import argparse
from datetime import datetime


class TestRunner:
    """Test runner for Playwright automation tests"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_path = f"reports/report_{self.timestamp}.html"
    
    def run_all_tests(self, browser="chromium", headed=False):
        """Run all tests"""
        print(f"Running all tests on {browser}...")
        cmd = [
            "pytest", "-v",
            f"--browser={browser}",
            f"--headed={'True' if headed else 'False'}",
            f"--html={self.report_path}",
            "--self-contained-html"
        ]
        return subprocess.run(cmd)
    
    def run_smoke_tests(self, browser="chromium", headed=False):
        """Run smoke tests only"""
        print(f"Running smoke tests on {browser}...")
        cmd = [
            "pytest", "-v",
            "-m", "smoke",
            f"--browser={browser}",
            f"--headed={'True' if headed else 'False'}",
            f"--html={self.report_path}",
            "--self-contained-html"
        ]
        return subprocess.run(cmd)
    
    def run_basic_search_tests(self, browser="chromium", headed=False):
        """Run basic search tests"""
        print(f"Running basic search tests on {browser}...")
        cmd = [
            "pytest", "-v",
            "-m", "basic_search",
            f"--browser={browser}",
            f"--headed={'True' if headed else 'False'}",
            f"--html={self.report_path}",
            "--self-contained-html"
        ]
        return subprocess.run(cmd)
    
    def run_t1_test(self, browser="chromium", headed=False):
        """Run T1 test only"""
        print(f"Running T1 test on {browser}...")
        cmd = [
            "pytest", "-v",
            "-m", "basic_search and one_way",
            f"--browser={browser}",
            f"--headed={'True' if headed else 'False'}",
            f"--html={self.report_path}",
            "--self-contained-html"
        ]
        return subprocess.run(cmd)
    
    def run_parallel_tests(self, workers=4):
        """Run tests in parallel"""
        print(f"Running tests in parallel with {workers} workers...")
        cmd = [
            "pytest", "-v",
            "-n", str(workers),
            f"--html={self.report_path}",
            "--self-contained-html"
        ]
        return subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(description="Run Playwright automation tests")
    parser.add_argument(
        "--suite",
        choices=["all", "smoke", "basic_search", "t1"],
        default="all",
        help="Test suite to run"
    )
    parser.add_argument(
        "--browser",
        choices=["chromium", "firefox", "webkit"],
        default="chromium",
        help="Browser to use"
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run tests in headed mode (show browser)"
    )
    parser.add_argument(
        "--parallel",
        type=int,
        metavar="N",
        help="Run tests in parallel with N workers"
    )
    
    args = parser.parse_args()
    runner = TestRunner()
    
    if args.parallel:
        result = runner.run_parallel_tests(args.parallel)
    elif args.suite == "smoke":
        result = runner.run_smoke_tests(args.browser, args.headed)
    elif args.suite == "basic_search":
        result = runner.run_basic_search_tests(args.browser, args.headed)
    elif args.suite == "t1":
        result = runner.run_t1_test(args.browser, args.headed)
    else:
        result = runner.run_all_tests(args.browser, args.headed)
    
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()