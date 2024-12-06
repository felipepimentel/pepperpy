"""Validate migration status for monorepo transition"""

import json
import sys
from pathlib import Path


class MigrationValidator:
    """Validates the migration status from monolithic to monorepo structure"""

    # Mapping of source directories to target packages
    PACKAGE_MAPPING = {
        "core": "pepperpy-core",
        "ai": "pepperpy-ai",
        "console": "pepperpy-console",
        "ui": "pepperpy-ui",
        "files": "pepperpy-files",
        "codebase": "pepperpy-codebase",
        "db": "pepperpy-core/db",  # DB functionality moves to core
    }

    def __init__(self):
        self.pepperpy_dir = Path("pepperpy")
        self.packages_dir = Path("packages")
        self.results: dict[str, dict] = {}
        self.missing_packages: list[str] = []

    def validate_migration(self) -> tuple[bool, dict]:
        """
        Validates the migration status and returns a detailed report.

        Returns:
            Tuple[bool, Dict]: Success status and detailed report
        """
        try:
            self._check_directory_structure()
            self._validate_package_migrations()
            self._validate_dependencies()
            return self._generate_report()
        except Exception as e:
            report = {
                "status": "error",
                "error": str(e),
                "missing_packages": self.missing_packages,
                "packages": {},
                "summary": {
                    "total_pending_files": 0,
                    "total_missing_tests": 0,
                    "total_missing_docs": 0,
                },
            }
            return False, report

    def _check_directory_structure(self) -> None:
        """Validates the basic directory structure"""
        if not self.packages_dir.exists():
            self.packages_dir.mkdir(parents=True)
            print(f"Created missing directory: {self.packages_dir}")

        for package in self.PACKAGE_MAPPING.values():
            package_path = self.packages_dir / package.split("/")[0]
            if not package_path.exists():
                self.missing_packages.append(package)
                print(f"Warning: Package directory not found: {package_path}")

    def _validate_package_migrations(self) -> None:
        """Validates migration status for each package"""
        for src_dir, target_package in self.PACKAGE_MAPPING.items():
            # Skip packages that don't exist yet
            if target_package.split("/")[0] in [p.split("/")[0] for p in self.missing_packages]:
                continue

            source_path = self.pepperpy_dir / src_dir
            if not source_path.exists():
                continue

            package_base = target_package.split("/")[0]
            target_path = self.packages_dir / package_base

            self.results[target_package] = {
                "pending_files": [],
                "modified_files": [],
                "missing_tests": [],
                "missing_docs": [],
            }

            self._check_pending_files(source_path, target_path, target_package)
            self._check_test_coverage(target_path, target_package)
            self._check_documentation(target_path, target_package)

    def _check_pending_files(self, source: Path, target: Path, package: str) -> None:
        """Checks for files that haven't been migrated"""
        if not source.exists():
            return

        for src_file in source.rglob("*.py"):
            rel_path = src_file.relative_to(source)
            dest_file = target / "pepperpy_" / package.split("-")[1] / rel_path

            if not dest_file.exists():
                self.results[package]["pending_files"].append(str(rel_path))

    def _check_test_coverage(self, package_path: Path, package: str) -> None:
        """Validates test coverage for migrated files"""
        tests_path = package_path / "tests"
        if not tests_path.exists():
            self.results[package]["missing_tests"].append("No tests directory found")
            return

        src_files = set()
        test_files = set()

        for py_file in (package_path / "pepperpy_" / package.split("-")[1]).rglob("*.py"):
            if py_file.name != "__init__.py":
                src_files.add(py_file.stem)

        for test_file in tests_path.rglob("test_*.py"):
            test_files.add(test_file.stem[5:])  # Remove 'test_' prefix

        missing_tests = src_files - test_files
        if missing_tests:
            self.results[package]["missing_tests"].extend(list(missing_tests))

    def _check_documentation(self, package_path: Path, package: str) -> None:
        """Validates documentation coverage"""
        docs_path = package_path / "docs"
        if not docs_path.exists():
            self.results[package]["missing_docs"].append("No documentation directory found")
            return

        # Check for README and API documentation
        required_docs = ["README.md", "API.md"]
        for doc in required_docs:
            if not (docs_path / doc).exists():
                self.results[package]["missing_docs"].append(f"Missing {doc}")

    def _validate_dependencies(self) -> None:
        """Validates package dependencies and cross-references"""
        for package_dir in self.packages_dir.iterdir():
            if not package_dir.is_dir():
                continue

            pyproject_path = package_dir / "pyproject.toml"
            if not pyproject_path.exists():
                self.results[package_dir.name]["missing_docs"].append("Missing pyproject.toml")
                continue

    def _generate_report(self) -> tuple[bool, dict]:
        """Generates a detailed migration report"""
        has_issues = bool(self.missing_packages)
        report = {
            "status": "incomplete" if has_issues else "success",
            "missing_packages": self.missing_packages,
            "packages": {},
            "summary": {
                "total_pending_files": 0,
                "total_missing_tests": 0,
                "total_missing_docs": 0,
                "total_missing_packages": len(self.missing_packages),
            },
        }

        for package, results in self.results.items():
            package_report = {
                "status": "complete" if not any(results.values()) else "incomplete",
                **results,
            }

            report["packages"][package] = package_report

            # Update summary
            report["summary"]["total_pending_files"] += len(results["pending_files"])
            report["summary"]["total_missing_tests"] += len(results["missing_tests"])
            report["summary"]["total_missing_docs"] += len(results["missing_docs"])

            if package_report["status"] == "incomplete":
                has_issues = True

        report["status"] = "incomplete" if has_issues else "complete"
        return not has_issues, report


def main() -> int:
    """Main entry point"""
    validator = MigrationValidator()
    success, report = validator.validate_migration()

    # Print report in a readable format
    print("\nMigration Validation Report")
    print("==========================")
    print(f"\nOverall Status: {report['status'].upper()}")

    if report.get("error"):
        print(f"\nError: {report['error']}")

    if report.get("missing_packages"):
        print("\nMissing Packages:")
        for package in report["missing_packages"]:
            print(f"  - {package}")

    print("\nSummary:")
    summary = report["summary"]
    print(f"- Total Missing Packages: {summary['total_missing_packages']}")
    print(f"- Total Pending Files: {summary['total_pending_files']}")
    print(f"- Total Missing Tests: {summary['total_missing_tests']}")
    print(f"- Total Missing Docs: {summary['total_missing_docs']}")

    if report["packages"]:
        print("\nDetailed Package Report:")
        for package, details in report["packages"].items():
            print(f"\n{package}:")
            print(f"  Status: {details['status']}")
            if details["pending_files"]:
                print("  Pending Files:")
                for file in details["pending_files"]:
                    print(f"    - {file}")
            if details["missing_tests"]:
                print("  Missing Tests:")
                for test in details["missing_tests"]:
                    print(f"    - {test}")
            if details["missing_docs"]:
                print("  Missing Documentation:")
                for doc in details["missing_docs"]:
                    print(f"    - {doc}")

    # Save report to file
    with open("migration_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\nDetailed report saved to migration_report.json")
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
