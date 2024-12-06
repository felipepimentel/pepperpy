"""Documentation generation script for PepperPy."""

from pathlib import Path
from typing import Any, TypedDict

try:
    import mkdocs_gen_files
    import yaml
except ImportError:
    raise ImportError(
        "Documentation dependencies not found. Install them with: poetry install --with docs"
    )


class NavItem(TypedDict, total=False):
    """Navigation item type."""
    title: str
    path: str
    children: list['NavItem']


def generate_api_docs() -> None:
    """Generate API documentation for all packages."""
    packages_dir = Path("packages")
    docs_dir = Path("docs/api")

    # Ensure docs directory exists
    docs_dir.mkdir(parents=True, exist_ok=True)

    for package in packages_dir.iterdir():
        if not package.is_dir():
            continue

        package_name = package.name
        module_name = package_name.replace("-", "_")

        # Generate package documentation
        with mkdocs_gen_files.open(f"api/{package_name}.md", "w") as f:
            f.write(f"# {package_name}\n\n")
            f.write("::: " + module_name + "\n")
            f.write("    options:\n")
            f.write("        show_root_heading: true\n")
            f.write("        show_source: true\n")


def generate_nav() -> None:
    """Generate navigation structure."""
    nav: list[dict[str, Any]] = []

    # Add static pages
    nav.extend([
        {"Home": "index.md"},
        {
            "Getting Started": [
                {"Installation": "getting-started/installation.md"},
                {"Quick Start": "getting-started/quickstart.md"},
            ]
        },
        {
            "Development": [
                {"Contributing": "development/contributing.md"},
                {"Architecture": "development/architecture.md"},
                {"Release Process": "development/release-process.md"},
            ]
        },
    ])

    # Add API reference
    api_nav: dict[str, list[dict[str, str]]] = {"API Reference": []}
    packages_dir = Path("packages")

    for package in sorted(packages_dir.iterdir()):
        if not package.is_dir():
            continue

        package_name = package.name
        api_nav["API Reference"].append({package_name: f"api/{package_name}.md"})

    nav.append(api_nav)
    nav.append({"Changelog": "changelog.md"})

    # Write nav to file
    with mkdocs_gen_files.open("nav.yml", "w") as f:
        yaml.dump(nav, f, allow_unicode=True)


if __name__ == "__main__":
    generate_api_docs()
    generate_nav()
