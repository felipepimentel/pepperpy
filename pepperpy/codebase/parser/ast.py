"""AST parsing implementation"""

import ast
from typing import Any

from pepperpy.core.module import BaseModule


class ASTParser(BaseModule):
    """Python AST parser"""

    def __init__(self) -> None:
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize parser"""
        self._initialized = True

    async def parse_file(self, content: str) -> ast.AST:
        """Parse Python file content"""
        return ast.parse(content)

    async def get_complexity(self, node: ast.AST) -> int:
        """Get cyclomatic complexity"""
        visitor = ComplexityVisitor()
        visitor.visit(node)
        return visitor.complexity

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self._initialized = False


class ComplexityVisitor(ast.NodeVisitor):
    """AST visitor for calculating complexity"""

    def __init__(self) -> None:
        self.complexity = 1

    def visit_if(self, node: ast.If) -> Any:
        """Visit If node"""
        self.complexity += 1
        self.generic_visit(node)

    def visit_while(self, node: ast.While) -> Any:
        """Visit While node"""
        self.complexity += 1
        self.generic_visit(node)

    def visit_for(self, node: ast.For) -> Any:
        """Visit For node"""
        self.complexity += 1
        self.generic_visit(node)

    def visit_except_handler(self, node: ast.ExceptHandler) -> Any:
        """Visit ExceptHandler node"""
        self.complexity += 1
        self.generic_visit(node)

    def visit_bool_op(self, node: ast.BoolOp) -> Any:
        """Visit BoolOp node"""
        self.complexity += len(node.values) - 1
        self.generic_visit(node) 