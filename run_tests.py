#!/usr/bin/env python3
"""
Main test runner script to execute all tests and confirm they pass.
"""
import subprocess
import sys

if __name__ == "__main__":
    print("=" * 70)
    print("Running all tests...")
    print("=" * 70)
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        cwd=".",
    )
    
    print("\n" + "=" * 70)
    if result.returncode == 0:
        print("✓ All tests passed successfully!")
    else:
        print("✗ Some tests failed. Please review the output above.")
    print("=" * 70)
    
    sys.exit(result.returncode)
