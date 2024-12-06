"""Development utilities for PepperPy."""

import subprocess
from pathlib import Path

import click
import toml
from rich.console import Console
from rich.prompt import Confirm

console = Console()


def run_command(cmd: str, cwd: Path | None = None) -> None:
    """Run shell command."""
    console.print(f"[blue]Running:[/] {cmd}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)


def create_package_structure(package_dir: Path, package_name: str) -> None:
    """Create standard package structure."""
    src_dir = package_dir / "src" / package_name.replace("-", "_")
    src_dir.mkdir(parents=True, exist_ok=True)

    # Create standard directories
    dirs = [
        src_dir / "core",
        src_dir / "utils",
        package_dir / "tests",
        package_dir / "docs",
        package_dir / "examples" / "basic",
        package_dir / "examples" / "advanced",
    ]
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

    # Create initial files
    (src_dir / "__init__.py").write_text('"""Main package module."""\n\n__version__ = "0.1.0"\n')
    (package_dir / "README.md").write_text(f"# {package_name}\n\nAdd package description here.\n")
    (package_dir / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [0.1.0] - Unreleased\n\n- Initial release\n"
    )


@click.group()
def cli() -> None:
    """PepperPy development utilities."""
    pass


@cli.command()
def setup() -> None:
    """Setup development environment."""
    run_command("poetry install")
    run_command("poetry run pre-commit install")
    run_command("poetry run pre-commit install --hook-type commit-msg")

    # Setup git hooks
    hooks_dir = Path(".git/hooks")
    if hooks_dir.exists() and Confirm.ask("Setup additional git hooks?"):
        run_command("cp tools/git-hooks/* .git/hooks/")
        run_command("chmod +x .git/hooks/*")


@cli.command()
def update() -> None:
    """Update dependencies."""
    run_command("poetry update")
    run_command("poetry run pre-commit autoupdate")

    # Check for outdated dependencies
    console.print("\n[yellow]Checking for outdated dependencies...[/]")
    run_command("poetry show --outdated")

    # Update lock files
    if Confirm.ask("Update lock files?"):
        run_command("poetry lock --no-update")
        run_command("pdm lock --no-update")


@cli.command()
@click.argument("package")
@click.option("--type", type=click.Choice(["lib", "app", "plugin"]), default="lib")
def create(package: str, type: str) -> None:
    """Create new package with specified type."""
    package_dir = Path("packages") / package
    if package_dir.exists():
        if not Confirm.ask(f"Package {package} already exists. Overwrite?"):
            return

    create_package_structure(package_dir, package)

    # Create pyproject.toml with type-specific configuration
    pyproject = {
        "tool": {
            "poetry": {
                "name": package,
                "version": "0.1.0",
                "description": f"{package} package",
                "authors": ["Felipe Pimentel <fpimentel88@gmail.com>"],
                "readme": "README.md",
                "packages": [{"include": f"src/{package.replace('-', '_')}"}],
                "dependencies": {
                    "python": ">=3.9,<4.0",
                    "pepperpy-core": {"path": "../pepperpy-core", "develop": True},
                },
            }
        }
    }

    # Add type-specific dependencies
    if type == "app":
        pyproject["tool"]["poetry"]["dependencies"].update({"click": "^8.0.0", "rich": "^13.7.0"})
    elif type == "plugin":
        pyproject["tool"]["poetry"]["dependencies"].update({"pluggy": "^1.3.0"})

    with open(package_dir / "pyproject.toml", "w") as f:
        toml.dump(pyproject, f)

    console.print(f"[green]Package {package} created as {type}![/]")

    # Initialize git
    if Confirm.ask("Initialize git?"):
        run_command("git init", cwd=package_dir)
        run_command("git add .", cwd=package_dir)
        run_command('git commit -m "Initial commit"', cwd=package_dir)


@cli.command()
def clean() -> None:
    """Clean development artifacts."""
    patterns = [
        "**/__pycache__",
        "**/.pytest_cache",
        "**/.coverage",
        "**/.mypy_cache",
        "**/.ruff_cache",
        "**/dist",
        "**/build",
        "**/*.egg-info",
        "**/.DS_Store",
    ]

    for pattern in patterns:
        for path in Path().glob(pattern):
            if path.is_dir():
                run_command(f"rm -rf {path}")
            else:
                path.unlink()

    console.print("[green]Development artifacts cleaned![/]")


@cli.command()
@click.argument("package")
def test(package: str) -> None:
    """Run tests for a specific package."""
    package_dir = Path("packages") / package
    if not package_dir.exists():
        console.print(f"[red]Package {package} not found![/]")
        return

    run_command("poetry run pytest", cwd=package_dir)


if __name__ == "__main__":
    cli()
