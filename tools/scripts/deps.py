"""Dependency management script for PepperPy packages."""

import json
from pathlib import Path

import click
import toml
from packaging.version import Version


def get_package_version(package_dir: Path) -> str | None:
    """Get package version from pyproject.toml."""
    pyproject_path = package_dir / "pyproject.toml"
    if not pyproject_path.exists():
        return None

    data = toml.load(pyproject_path)
    return data["tool"]["poetry"]["version"]


def get_package_dependencies(package_dir: Path) -> dict[str, str]:
    """Get package dependencies from pyproject.toml."""
    pyproject_path = package_dir / "pyproject.toml"
    if not pyproject_path.exists():
        return {}

    data = toml.load(pyproject_path)
    return data["tool"]["poetry"]["dependencies"]


def update_package_dependency(package_dir: Path, dep_name: str, version: str) -> None:
    """Update package dependency version."""
    pyproject_path = package_dir / "pyproject.toml"
    if not pyproject_path.exists():
        return

    data = toml.load(pyproject_path)
    data["tool"]["poetry"]["dependencies"][dep_name] = f"^{version}"

    with open(pyproject_path, "w") as f:
        toml.dump(data, f)


def get_dependency_graph() -> dict[str, list[str]]:
    """Build dependency graph of packages."""
    graph = {}
    packages_dir = Path("packages")

    for package in packages_dir.iterdir():
        if not package.is_dir():
            continue

        package_name = package.name
        deps = get_package_dependencies(package)

        # Filter only internal dependencies
        internal_deps = [dep for dep in deps if Path(packages_dir / dep).exists()]

        graph[package_name] = internal_deps

    return graph


@click.group()
def cli() -> None:
    """Dependency management CLI."""
    pass


@cli.command()
def graph() -> None:
    """Show dependency graph."""
    deps = get_dependency_graph()
    click.echo(json.dumps(deps, indent=2))


@cli.command()
@click.argument("package")
def check(package: str) -> None:
    """Check package dependencies."""
    packages_dir = Path("packages")
    package_dir = packages_dir / package

    if not package_dir.exists():
        click.echo(f"Package {package} not found", err=True)
        return

    deps = get_package_dependencies(package_dir)
    version = get_package_version(package_dir)

    click.echo(f"Package: {package} v{version}")
    click.echo("\nDependencies:")
    for dep, ver in deps.items():
        if Path(packages_dir / dep).exists():
            dep_version = get_package_version(packages_dir / dep)
            click.echo(f"  {dep}: {ver} (available: {dep_version})")
        else:
            click.echo(f"  {dep}: {ver}")


@cli.command()
@click.argument("package")
@click.argument("version")
def bump(package: str, version: str) -> None:
    """Bump package version and update dependents."""
    packages_dir = Path("packages")
    package_dir = packages_dir / package

    if not package_dir.exists():
        click.echo(f"Package {package} not found", err=True)
        return

    # Validate version
    try:
        Version(version)
    except ValueError as e:
        click.echo(f"Invalid version: {e}", err=True)
        return

    # Update package version
    data = toml.load(package_dir / "pyproject.toml")
    data["tool"]["poetry"]["version"] = version
    with open(package_dir / "pyproject.toml", "w") as f:
        toml.dump(data, f)

    # Update dependents
    graph = get_dependency_graph()
    for dep_package, deps in graph.items():
        if package in deps:
            update_package_dependency(packages_dir / dep_package, package, version)
            click.echo(f"Updated {dep_package} dependency on {package}")


if __name__ == "__main__":
    cli()
