#!/usr/bin/env python  # noqa: EXE001
"""Lint checker for the PepperPy project."""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def is_tool_available(tool: str) -> bool:
    """Check if a tool is available in the system PATH."""
    return shutil.which(tool) is not None


def run_command(cmd: list[str]) -> bool:
    """Execute a command and display detailed output for problematic files.

    Args:
        cmd (list[str]): Command to be executed.

    Returns:
        bool: True if command succeeds, False otherwise.
    """
    print(f"\nExecuting: {" ".join(cmd)}")
    try:
        # Execute command and capture output
        subprocess.run(
            cmd,
            check=True,
            cwd=ROOT_DIR,
            text=True,
            capture_output=True,
        )
        print(f"{cmd[0]} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        # Print detailed output from the linter
        print(f"{cmd[0]} encountered issues. Details below:\n")
        print(e.stdout or e.stderr)

        # Collect and print a summary of problematic files
        problematic_files = set()
        output = e.stdout.strip().splitlines() + e.stderr.strip().splitlines()
        for line in output:
            # Handle Ruff output
            if ":" in line:
                parts = line.split(":")
                filename = parts[0].strip()
                if (ROOT_DIR / filename).exists():
                    problematic_files.add(filename)

        if problematic_files:
            print("\nSummary of problematic files:")
            for filename in sorted(problematic_files):
                print(f"- {filename}")

        return False


def run_linters() -> bool:
    """Run all linters with auto-fix mode.

    Returns:
        bool: True if all linters are successful, False otherwise.
    """
    print("Running linters...")

    # Check if required tools are installed
    required_tools = ["ruff"]
    missing_tools = [tool for tool in required_tools if not is_tool_available(tool)]
    if missing_tools:
        print(f"Missing tools: {", ".join(missing_tools)}. Please install them and try again.")
        return False

    # List of linter commands to execute
    linters = [
        ["ruff", "check", "--fix", "."],
    ]

    success = True

    for cmd in linters:
        if not run_command(cmd):
            success = False

    if not success:
        print("\nSome linters failed. Please fix the issues above.")
    else:
        print("\nAll linters completed successfully!")

    return success


if __name__ == "__main__":
    sys.exit(0 if run_linters() else 1)
