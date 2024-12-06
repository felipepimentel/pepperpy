#!/usr/bin/env python  # noqa: EXE001
"""Lint checker and project status report generator for the PepperPy project."""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
REPORT_FILE = ROOT_DIR / "project_status_report.txt"


def is_tool_available(tool: str) -> bool:
    """Check if a tool is available in the system PATH."""
    return shutil.which(tool) is not None


def run_command(cmd: list[str]) -> subprocess.CompletedProcess:
    """Execute a command and capture its output.

    Args:
        cmd (list[str]): Command to be executed.

    Returns:
        subprocess.CompletedProcess: Result of the command execution.
    """
    print(f"\nRunning: {" ".join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            check=True,
            cwd=ROOT_DIR,
            text=True,
            capture_output=True,
        )
        print(f"{cmd[0]} completed successfully!")
        return result
    except subprocess.CalledProcessError as e:
        print(f"{cmd[0]} encountered issues. Details below:\n")
        print(e.stdout or e.stderr)

        # Create a dummy CompletedProcess object for consistency
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=e.returncode,
            stdout=e.stdout,
            stderr=e.stderr,
        )


def run_linters() -> dict:
    """Run all linters and capture the results.

    Returns:
        dict: Summary of linter results.
    """
    print("Running linters...")

    required_tools = ["ruff"]
    missing_tools = [tool for tool in required_tools if not is_tool_available(tool)]
    if missing_tools:
        print(f"Missing tools: {", ".join(missing_tools)}. Please install them.")
        return {"success": False, "details": {}}

    cmd = ["ruff", "check", "--fix", "."]
    result = run_command(cmd)

    success = result.returncode == 0
    return {
        "success": success,
        "details": {
            "stdout": result.stdout,
            "stderr": result.stderr,
        },
    }


def run_tests() -> dict:
    """Run unit tests and capture the results.

    Returns:
        dict: Summary of test results.
    """
    print("Running unit tests...")
    cmd = ["pytest", "--maxfail=1", "--disable-warnings"]
    result = run_command(cmd)

    success = result.returncode == 0
    return {
        "success": success,
        "details": {
            "stdout": result.stdout,
            "stderr": result.stderr,
        },
    }


def generate_report(lint_results: dict, test_results: dict) -> None:
    """Generate a plain text report for project status."""
    print("Generating project status report...")
    with REPORT_FILE.open("w") as report:
        report.write("Project Status Report\n")
        report.write("=" * 30 + "\n\n")

        # Linter results
        report.write("Linters:\n")
        if lint_results["success"]:
            report.write("  - Status: Pass\n")
        else:
            report.write("  - Status: Fail\n")
            report.write("  - Details:\n")
            report.write(f'{lint_results["details"]["stderr"]}\n\n')

        # Test results
        report.write("Unit Tests:\n")
        if test_results["success"]:
            report.write("  - Status: Pass\n")
        else:
            report.write("  - Status: Fail\n")
            report.write("  - Details:\n")
            report.write(f'{test_results["details"]["stderr"]}\n\n')

    print(f"Report generated: {REPORT_FILE}")


if __name__ == "__main__":
    lint_results = run_linters()
    test_results = run_tests()

    generate_report(lint_results, test_results)

    # Exit with appropriate status
    success = lint_results["success"] and test_results["success"]
    sys.exit(0 if success else 1)
