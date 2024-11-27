"""Dependency management for PepperPy monorepo"""

import json
from pathlib import Path
from typing import Dict, List, Set


def get_package_deps(package_dir: Path) -> Set[str]:
    """Get package dependencies"""
    pyproject = package_dir / "pyproject.toml"
    if not pyproject.exists():
        return set()

    with open(pyproject) as f:
        content = f.read()

    # Parse TOML and extract dependencies
    deps = set()
    for line in content.split("\n"):
        if line.startswith("pepperpy-"):
            dep = line.split("=")[0].strip()
            deps.add(dep)

    return deps


def build_dep_graph() -> Dict[str, List[str]]:
    """Build dependency graph"""
    packages_dir = Path("packages")
    graph: Dict[str, List[str]] = {}

    for package in packages_dir.iterdir():
        if package.is_dir():
            deps = get_package_deps(package)
            graph[package.name] = sorted(deps)

    return graph


def validate_deps() -> bool:
    """Validate dependencies"""
    graph = build_dep_graph()
    valid = True

    # Check for circular dependencies
    visited: Set[str] = set()
    path: List[str] = []

    def check_circular(pkg: str) -> bool:
        if pkg in path:
            print(f"Circular dependency detected: {' -> '.join(path + [pkg])}")
            return False

        if pkg in visited:
            return True

        visited.add(pkg)
        path.append(pkg)

        for dep in graph.get(pkg, []):
            if not check_circular(dep):
                return False

        path.pop()
        return True

    # Check each package
    for pkg in graph:
        if not check_circular(pkg):
            valid = False

    return valid


def main() -> None:
    """Main function"""
    print("Analyzing dependencies...")
    graph = build_dep_graph()

    print("\nDependency Graph:")
    print(json.dumps(graph, indent=2))

    if validate_deps():
        print("\nAll dependencies are valid!")
    else:
        print("\nDependency validation failed!")
        exit(1)


if __name__ == "__main__":
    main()
