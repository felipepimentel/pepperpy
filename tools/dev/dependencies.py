"""Dependency management utilities"""
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import networkx as nx
import toml


class DependencyManager:
    """Manages project dependencies"""

    def __init__(self, packages_dir: Path) -> None:
        self.packages_dir = packages_dir
        self.graph: nx.DiGraph = nx.DiGraph()

    def build_dependency_graph(self) -> nx.DiGraph:
        """Build dependency graph from packages"""
        for package in self.packages_dir.glob("**/pyproject.toml"):
            config = toml.load(package)
            name = config["tool"]["poetry"]["name"]
            deps = self._get_dependencies(config)

            self.graph.add_node(name)
            for dep in deps:
                self.graph.add_edge(name, dep)

        return self.graph

    def check_circular_dependencies(self) -> set[tuple[str, ...]]:
        """Check for circular dependencies"""
        cycles: Iterator[list[str]] = nx.simple_cycles(self.graph)
        return {tuple(cycle) for cycle in cycles}

    def get_dependency_order(self) -> list[str]:
        """Get packages in dependency order"""
        return list(nx.topological_sort(self.graph))

    def _get_dependencies(self, config: dict[str, Any]) -> set[str]:
        """Extract package dependencies"""
        deps: set[str] = set()
        poetry_config = config.get("tool", {}).get("poetry", {})
        dependencies = poetry_config.get("dependencies", {})

        if isinstance(dependencies, dict):
            deps.update(
                name
                for name in dependencies.keys()
                if isinstance(name, str) and name.startswith("pepperpy-")
            )
        return deps
