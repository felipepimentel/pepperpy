"""CI/CD management utilities"""

import subprocess
from pathlib import Path


class CIManager:
    """Manages CI/CD operations"""

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.packages_dir = root_dir / "packages"

    def validate_all(self) -> bool:
        """Run all validations"""
        checks = [
            self.check_formatting(),
            self.check_types(),
            self.run_tests(),
            self.check_dependencies(),
            self.validate_docker(),
        ]
        return all(checks)

    def check_formatting(self) -> bool:
        """Check code formatting"""
        try:
            subprocess.run(["ruff", "check", "."], check=True)
            subprocess.run(["black", "--check", "."], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def check_types(self) -> bool:
        """Check type annotations"""
        try:
            subprocess.run(["mypy", "."], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def run_tests(self) -> bool:
        """Run test suite"""
        try:
            subprocess.run(["pytest", "tests/"], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def check_dependencies(self) -> bool:
        """Check project dependencies"""
        try:
            subprocess.run(["poetry", "check"], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def validate_docker(self) -> bool:
        """Validate Docker configuration"""
        try:
            if (self.root_dir / "Dockerfile").exists():
                subprocess.run(["docker", "build", "-t", "pepperpy-test", "."], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
