#!/usr/bin/env python
"""Lint Checker for PepperPy"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def is_tool_available(tool: str) -> bool:
    """Check if a tool is available in the system PATH."""
    return shutil.which(tool) is not None


def run_command(cmd: list[str]) -> bool:
    """
    Run a command and display only problematic filenames.

    Args:
        cmd (list[str]): Command to execute.

    Returns:
        bool: True if the command succeeds, False otherwise.

    """
    print(f"\nRunning: {' '.join(cmd)}")
    try:
        # Run the command and capture output
        subprocess.run(
            cmd,
            check=True,
            cwd=ROOT_DIR,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"{cmd[0]} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        # Print full output for context
        print(f"{cmd[0]} found issues. Detailed output:")
        print(e.stdout)  # Output from the linter
        print(e.stderr)  # Error messages, if any

        # Filter and print only problematic filenames
        problematic_files = set()
        output = e.stdout.strip().splitlines() + e.stderr.strip().splitlines()
        for line in output:
            # Handle output from 'black'
            if cmd[0] == "black" and "would reformat" in line:
                problematic_files.add(line.split("would reformat")[1].strip())
            # Handle output from other tools (e.g., 'ruff')
            elif ":" in line:
                parts = line.split(":")
                filename = parts[0].strip()
                if (ROOT_DIR / filename).exists():
                    problematic_files.add(filename)

        print("\nSummary of problematic files:")
        for filename in sorted(problematic_files):
            print(f"- {filename}")

        return False


def run_linters() -> bool:
    """
    Run all linters without auto-fix mode.

    Returns:
        bool: True if all linters succeed, False otherwise.

    """
    print("Running linters...")

    # Check if required tools are installed
    required_tools = ["black", "ruff"]
    missing_tools = [tool for tool in required_tools if not is_tool_available(tool)]
    if missing_tools:
        print(
            f"Missing tools: {', '.join(missing_tools)}. Please install them and try again.",
        )
        return False

    linters = [
        ["black", "--check", "pepperpy", "tests", "examples"],
        ["ruff", "check", "pepperpy", "tests", "examples"],
    ]

    success = True
    for cmd in linters:
        if not run_command(cmd):
            success = False

    if not success:
        print("Some linters failed. Please fix the issues above.")
    else:
        print("All linters passed successfully!")

    return success


if __name__ == "__main__":
    sys.exit(0 if run_linters() else 1)
