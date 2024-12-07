"""Build script for PepperPy monorepo"""

import subprocess
from collections.abc import Sequence
from pathlib import Path

PACKAGES: Sequence[str] = [
    "pepperpy-core",
    "pepperpy-ai",
    "pepperpy-console",
    "pepperpy-ui",
    "pepperpy-files",
    "pepperpy-codebase",
]


def build_package(package: str) -> bool:
    """Build a single package"""
    package_dir = Path("packages") / package

    try:
        # Install dependencies
        subprocess.run(["poetry", "install"], cwd=package_dir, check=True)

        # Run tests
        subprocess.run(["poetry", "run", "pytest"], cwd=package_dir, check=True)

        # Build package
        subprocess.run(["poetry", "build"], cwd=package_dir, check=True)

        return True

    except subprocess.CalledProcessError as e:
        print(f"Error building {package}: {e}")
        return False


def build_all() -> list[str]:
    """Build all packages"""
    failed: list[str] = []

    for package in PACKAGES:
        print(f"\nBuilding {package}...")
        if not build_package(package):
            failed.append(package)

    return failed


if __name__ == "__main__":
    failed = build_all()
    if failed:
        print(f"\nFailed packages: {", ".join(failed)}")
        exit(1)
    print("\nAll packages built successfully!")
