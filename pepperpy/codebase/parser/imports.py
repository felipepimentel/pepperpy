"""Import parsing implementation"""

import ast
from typing import Any

from pepperpy.core.module import BaseModule


class ImportParser(BaseModule):
    """Python import parser"""

    def __init__(self) -> None:
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize parser"""
        self._initialized = True

    async def parse_imports(self, tree: ast.AST) -> list[str]:
        """Parse imports from AST"""
        visitor = ImportVisitor()
        visitor.visit(tree)
        return visitor.imports

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self._initialized = False


class ImportVisitor(ast.NodeVisitor):
    """AST visitor for collecting imports"""

    def __init__(self) -> None:
        self.imports: list[str] = []

    def visit_import(self, node: ast.Import) -> Any:
        """Visit Import node"""
        for name in node.names:
            self.imports.append(name.name)

    def visit_import_from(self, node: ast.ImportFrom) -> Any:
        """Visit ImportFrom node"""
        if node.module:
            for name in node.names:
                if name.name == "*":
                    self.imports.append(node.module)
                else:
                    self.imports.append(f"{node.module}.{name.name}")
