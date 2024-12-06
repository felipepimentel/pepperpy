"""Version management for PepperPy packages."""

import re
from pathlib import Path

import click
from packaging.version import Version


def update_version(file_path: Path, new_version: str) -> None:
    """Update version in file."""
    content = file_path.read_text()

    # Update version patterns
    patterns = [
        (r'version = "[^"]+"', f'version = "{new_version}"'),
        (r'__version__ = "[^"]+"', f'__version__ = "{new_version}"'),
        (r"version = '[^']+'", f"version = '{new_version}'"),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    file_path.write_text(content)


def get_current_version(file_path: Path) -> str | None:
    """Get current version from file."""
    content = file_path.read_text()

    patterns = [
        r'version = "([^"]+)"',
        r'__version__ = "([^"]+)"',
        r"version = '([^']+)'",
    ]

    for pattern in patterns:
        if match := re.search(pattern, content):
            return match.group(1)
    return None


@click.group()
def cli() -> None:
    """Version management CLI."""
    pass


@cli.command()
@click.argument("new_version")
def bump(new_version: str) -> None:
    """Bump version in all packages."""
    packages_dir = Path("packages")

    # Validate version format
    try:
        Version(new_version)
    except ValueError as e:
        click.echo(f"Invalid version format: {e}", err=True)
        return

    # Update versions in all packages
    for package_dir in packages_dir.iterdir():
        if not package_dir.is_dir():
            continue

        pyproject = package_dir / "pyproject.toml"
        init_file = package_dir / package_dir.name.replace("-", "_") / "__init__.py"

        if pyproject.exists():
            update_version(pyproject, new_version)
            click.echo(f"Updated version in {pyproject}")

        if init_file.exists():
            update_version(init_file, new_version)
            click.echo(f"Updated version in {init_file}")


@cli.command()
def show() -> None:
    """Show current versions of all packages."""
    packages_dir = Path("packages")

    for package_dir in packages_dir.iterdir():
        if not package_dir.is_dir():
            continue

        pyproject = package_dir / "pyproject.toml"
        if not pyproject.exists():
            continue

        version = get_current_version(pyproject)
        click.echo(f"{package_dir.name}: {version}")


if __name__ == "__main__":
    cli()
