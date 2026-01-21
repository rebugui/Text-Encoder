#!/usr/bin/env python3
"""Run all tests and display summary."""
import subprocess
import sys

def main():
    print("Running all tests...")
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', 'tests/', '-q', '--tb=no'],
        capture_output=True,
        text=True
    )

    # Print the output
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    print(f"\nExit code: {result.returncode}")

    # Parse output for summary
    lines = result.stdout.strip().split('\n')
    for line in reversed(lines):
        if 'passed' in line.lower():
            print(f"\n{line}")
            break

    return result.returncode

if __name__ == '__main__':
    sys.exit(main())
