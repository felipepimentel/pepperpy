"""Migration script for transitioning to monorepo structure"""

import asyncio
import shutil
import subprocess
import sys
from pathlib import Path

import toml


class MonorepoMigrator:
    """Handles migration to monorepo structure"""

    PACKAGE_MAPPING = {
        "core": {
            "name": "pepperpy-core",
            "description": "Core functionality for PepperPy framework",
            "dependencies": [
                "pydantic",
                "asyncpg",
                "typing-extensions",
                "python-jose[cryptography]",
            ],
            "modules": ["config", "db", "module", "registry", "validation"],
        },
        "ai": {
            "name": "pepperpy-ai",
            "description": "AI integration module for PepperPy framework",
            "dependencies": ["pepperpy-core", "openai", "aiohttp", "tenacity"],
            "modules": ["agents", "chat", "providers"],
        },
        "console": {
            "name": "pepperpy-console",
            "description": "Terminal interface components for PepperPy framework",
            "dependencies": ["pepperpy-core", "rich", "prompt-toolkit"],
            "modules": ["components", "app", "terminal"],
        },
        "files": {
            "name": "pepperpy-files",
            "description": "File handling operations for PepperPy framework",
            "dependencies": ["pepperpy-core", "aiofiles"],
            "modules": ["handlers", "parsers", "watchers"],
        },
        "codebase": {
            "name": "pepperpy-codebase",
            "description": "Code analysis and manipulation for PepperPy framework",
            "dependencies": ["pepperpy-core", "libcst", "astroid"],
            "modules": ["analysis", "transforms", "metrics"],
        },
        "ui": {
            "name": "pepperpy-ui",
            "description": "User interface components for PepperPy framework",
            "dependencies": ["pepperpy-core", "textual"],
            "modules": ["components", "layouts", "themes"],
        },
    }

    def __init__(self):
        self.root_dir = Path.cwd()
        self.source_dir = self.root_dir / "pepperpy"
        self.packages_dir = self.root_dir / "packages"
        self.migrated_files: set[Path] = set()
        self.unmigrated_files: set[Path] = set()

    def _scan_source_directory(self) -> set[Path]:
        """Scan source directory for all Python files and directories"""
        all_files = set()
        for item in self.source_dir.rglob("*"):
            if item.is_file() and item.suffix == ".py":
                all_files.add(item)
            elif item.is_dir() and not item.name.startswith("."):
                all_files.add(item)
        return all_files

    def _map_file_to_package(self, file_path: Path) -> str:
        """Map a file to its target package based on its path"""
        relative_path = file_path.relative_to(self.source_dir)
        parts = relative_path.parts

        # Direct module mapping
        if parts[0] in self.PACKAGE_MAPPING:
            return self.PACKAGE_MAPPING[parts[0]]["name"]

        # Special cases and patterns
        if parts[0] == "db":
            return "pepperpy-core"
        if parts[0] in ["tests", "docs"]:
            if len(parts) > 1 and parts[1] in self.PACKAGE_MAPPING:
                return self.PACKAGE_MAPPING[parts[1]]["name"]
            return "pepperpy-core"

        # Default to core package
        return "pepperpy-core"

    def _get_unmigrated_files(self) -> set[Path]:
        """Get list of files that haven't been migrated"""
        all_files = self._scan_source_directory()
        return all_files - self.migrated_files

    async def _migrate_unmapped_files(self) -> None:
        """Migrate files that weren't caught by the main migration"""
        unmigrated = self._get_unmigrated_files()
        if not unmigrated:
            return

        print("\nMigrating remaining files:")
        for file_path in sorted(unmigrated):
            target_package = self._map_file_to_package(file_path)
            relative_path = file_path.relative_to(self.source_dir)

            # Determine target path
            if file_path.is_file():
                target_path = (
                    self.packages_dir
                    / target_package
                    / f"pepperpy_{target_package.split('-')[1]}"
                    / relative_path
                )
            else:
                target_path = (
                    self.packages_dir
                    / target_package
                    / f"pepperpy_{target_package.split('-')[1]}"
                    / relative_path.name
                )

            print(f"  - {relative_path} -> {target_package}")

            # Create parent directories
            target_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                if file_path.is_file():
                    shutil.copy2(file_path, target_path)
                else:
                    shutil.copytree(file_path, target_path, dirs_exist_ok=True)
                self.migrated_files.add(file_path)
            except Exception as e:
                print(f"    Error migrating {file_path}: {e}")
                self.unmigrated_files.add(file_path)

    def migrate(self) -> None:
        """Execute migration process"""
        print("\nStarting PepperPy Monorepo Migration")
        print("===================================")

        # Phase 1: Setup Package Structure
        print("\nPhase 1: Setting up package structure...")
        self._setup_package_structure()

        # Phase 2: Migrate Core Package
        print("\nPhase 2: Migrating core package...")
        asyncio.run(self._migrate_core_package())

        # Phase 3: Migrate Other Packages
        print("\nPhase 3: Migrating other packages...")
        asyncio.run(self._migrate_other_packages())

        # Phase 4: Migrate Remaining Files
        print("\nPhase 4: Migrating remaining files...")
        asyncio.run(self._migrate_unmapped_files())

        # Phase 5: Update Dependencies
        print("\nPhase 5: Updating dependencies...")
        self._update_dependencies()

        # Phase 6: Setup Development Environment
        print("\nPhase 6: Setting up development environment...")
        self._setup_development()

        # Report migration status
        self._report_migration_status()

        print("\nMigration completed!")

    def _report_migration_status(self) -> None:
        """Report migration status"""
        print("\nMigration Status Report")
        print("=====================")

        print(f"\nTotal files migrated: {len(self.migrated_files)}")
        if self.unmigrated_files:
            print(f"\nWarning: {len(self.unmigrated_files)} files could not be migrated:")
            for file in sorted(self.unmigrated_files):
                print(f"  - {file.relative_to(self.source_dir)}")

        # Check for any remaining files
        remaining = self._get_unmigrated_files()
        if remaining:
            print(f"\nWarning: {len(remaining)} files were not caught by migration:")
            for file in sorted(remaining):
                print(f"  - {file.relative_to(self.source_dir)}")

    def _setup_package_structure(self) -> None:
        """Setup initial package structure"""
        self.packages_dir.mkdir(exist_ok=True)

        for pkg_info in self.PACKAGE_MAPPING.values():
            pkg_name = pkg_info["name"]
            pkg_path = self.packages_dir / pkg_name
            pkg_path.mkdir(exist_ok=True)

            # Create package subdirectories
            module_path = pkg_path / f"pepperpy_{pkg_name.split('-')[1]}"
            module_path.mkdir(exist_ok=True)
            (pkg_path / "tests").mkdir(exist_ok=True)
            (pkg_path / "docs").mkdir(exist_ok=True)

            # Create package files
            self._create_package_files(pkg_path, pkg_info)

    def _create_package_files(self, pkg_path: Path, pkg_info: dict) -> None:
        """Create initial package files"""
        # Create pyproject.toml
        pyproject = {
            "tool": {
                "poetry": {
                    "name": pkg_info["name"],
                    "version": "0.1.0",
                    "description": pkg_info["description"],
                    "authors": ["Felipe Pimentel <fpimentel88@gmail.com>"],
                    "dependencies": {
                        "python": "^3.9",
                        **{dep: "*" for dep in pkg_info["dependencies"]},
                    },
                    "group": {
                        "dev": {
                            "dependencies": {
                                "pytest": "^8.0.0",
                                "pytest-asyncio": "^0.23.0",
                                "pytest-cov": "^4.1.0",
                            }
                        }
                    },
                }
            }
        }
        with open(pkg_path / "pyproject.toml", "w") as f:
            toml.dump(pyproject, f)

        # Create README.md
        readme_content = [
            f"# {pkg_info['name']}",
            "",
            f"{pkg_info['description']}",
            "",
            "## Installation",
            "",
            "```bash",
            f"poetry add {pkg_info['name']}",
            "```",
            "",
            "## Usage",
            "",
            "```python",
            f"from pepperpy_{pkg_info['name'].split('-')[1]} import *",
            "```",
            "",
        ]

        with open(pkg_path / "README.md", "w") as f:
            f.write("\n".join(readme_content))

        # Create __init__.py
        init_path = pkg_path / f"pepperpy_{pkg_info['name'].split('-')[1]}" / "__init__.py"
        with open(init_path, "w") as f:
            f.write(f'"""PepperPy {pkg_info["name"]} package"""\n\n__version__ = "0.1.0"\n')

    async def _migrate_core_package(self) -> None:
        """Migrate core package first"""
        core_info = self.PACKAGE_MAPPING["core"]
        core_path = self.packages_dir / core_info["name"]

        # Move core modules
        for module in core_info["modules"]:
            src = self.source_dir / module
            dst = core_path / f"pepperpy_core/{module}"
            if src.exists():
                shutil.copytree(src, dst, dirs_exist_ok=True)
                self.migrated_files.add(src)

    async def _migrate_other_packages(self) -> None:
        """Migrate remaining packages"""
        for pkg_name, pkg_info in self.PACKAGE_MAPPING.items():
            if pkg_name == "core":
                continue

            pkg_path = self.packages_dir / pkg_info["name"]

            # Move package modules
            for module in pkg_info["modules"]:
                src = self.source_dir / pkg_name / module
                dst = pkg_path / f"pepperpy_{pkg_name}/{module}"
                if src.exists():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                    self.migrated_files.add(src)

    def _update_dependencies(self) -> None:
        """Update package dependencies"""
        for pkg_path in self.packages_dir.iterdir():
            if not pkg_path.is_dir():
                continue

            pyproject_path = pkg_path / "pyproject.toml"
            if not pyproject_path.exists():
                continue

            with open(pyproject_path) as f:
                config = toml.load(f)

            # Update dependencies based on imports
            # This is a placeholder - actual implementation would analyze imports

            with open(pyproject_path, "w") as f:
                toml.dump(config, f)

    def _setup_development(self) -> None:
        """Setup development environment"""
        # Install dependencies
        subprocess.run(["poetry", "install"], check=True)

        # Setup pre-commit hooks
        pre_commit_config = """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.11
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
"""
        with open(self.root_dir / ".pre-commit-config.yaml", "w") as f:
            f.write(pre_commit_config)


def main() -> int:
    """Main entry point"""
    try:
        migrator = MonorepoMigrator()
        migrator.migrate()
        return 0
    except Exception as e:
        print(f"Error during migration: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
