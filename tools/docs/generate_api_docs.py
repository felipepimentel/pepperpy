"""Generate API documentation for all packages."""

from pathlib import Path

PACKAGES = [
    "pepperpy-core",
    "pepperpy-console",
    "pepperpy-db",
    "pepperpy-codebase",
    "pepperpy-files",
    "pepperpy-ai",
]

DOCS_TEMPLATE = """
# {package} API Reference

::: {module}
    handler: python
    options:
      show_root_heading: true
      show_source: true
"""


def generate_api_docs():
    """Generate API documentation for all packages."""
    docs_dir = Path("docs/packages")
    docs_dir.mkdir(parents=True, exist_ok=True)

    for package in PACKAGES:
        # Converte pepperpy-core para core, etc
        pkg_name = package.split("-")[1]
        pkg_dir = docs_dir / pkg_name
        pkg_dir.mkdir(exist_ok=True)

        # Cria arquivo index.md
        with open(pkg_dir / "index.md", "w") as f:
            f.write(f"# {package}\n\nOverview of the {package} package.\n")

        # Cria arquivo api.md
        module_name = package.replace("-", "_")
        with open(pkg_dir / "api.md", "w") as f:
            f.write(DOCS_TEMPLATE.format(package=package, module=module_name))


if __name__ == "__main__":
    generate_api_docs()
