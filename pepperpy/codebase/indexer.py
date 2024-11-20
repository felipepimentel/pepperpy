"""Code indexing implementation"""

import ast
from pathlib import Path
from typing import AsyncGenerator

from pepperpy.core.module import BaseModule

from .config import CodebaseConfig
from .parser import ASTParser, ImportParser
from .types import CodeEntity, EntityType, IndexEntry, Location


class CodeIndexer(BaseModule):
    """Indexes Python code for analysis"""

    def __init__(self, config: CodebaseConfig) -> None:
        self.config = config
        self._ast_parser = ASTParser()
        self._import_parser = ImportParser()
        self._index: dict[str, IndexEntry] = {}
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize indexer"""
        if self._initialized:
            return
        await self._ast_parser.initialize()
        await self._import_parser.initialize()
        self._initialized = True

    async def index_project(self, path: Path) -> list[IndexEntry]:
        """Index entire project"""
        if not self._initialized:
            await self.initialize()

        # Reset index
        self._index.clear()

        # Index all Python files
        async for entry in self._index_path(path):
            self._index[entry.entity.name] = entry

        # Process dependencies
        if self.config.track_dependencies:
            await self._process_dependencies()

        return list(self._index.values())

    async def _index_path(self, path: Path) -> AsyncGenerator[IndexEntry, None]:
        """Index files in path"""
        if path.is_file() and path.suffix == ".py":
            if await self._should_index_file(path):
                async for entry in self._index_file(path):
                    yield entry
        elif path.is_dir():
            for item in path.iterdir():
                if not self._should_ignore(item):
                    async for entry in self._index_path(item):
                        yield entry

    async def _index_file(self, path: Path) -> AsyncGenerator[IndexEntry, None]:
        """Index single Python file"""
        try:
            # Parse file
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                tree = ast.parse(content)

            # Get imports
            imports = await self._import_parser.parse_imports(tree)

            # Process each node
            for node in ast.walk(tree):
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    entity = await self._create_entity(node, path)
                    complexity = (
                        await self._ast_parser.get_complexity(node)
                        if self.config.analyze_complexity
                        else None
                    )
                    yield IndexEntry(entity=entity, dependencies=imports, complexity=complexity)

        except Exception as e:
            # Log error but continue indexing
            print(f"Error indexing {path}: {e}")

    async def _create_entity(self, node: ast.AST, path: Path) -> CodeEntity:
        """Create code entity from AST node"""
        if not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            raise ValueError("Invalid node type")

        entity_type = EntityType.CLASS if isinstance(node, ast.ClassDef) else EntityType.FUNCTION

        # Get location
        location = Location(
            file=path,
            start_line=getattr(node, "lineno", 0),
            end_line=getattr(node, "end_lineno", getattr(node, "lineno", 0)),
            start_col=getattr(node, "col_offset", 0),
            end_col=getattr(node, "end_col_offset", getattr(node, "col_offset", 0)),
        )

        # Get docstring if enabled
        docstring = None
        if self.config.parse_docstrings:
            if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)

        return CodeEntity(
            name=node.name,
            type=entity_type,
            location=location,
            docstring=docstring,
            signature=self._get_signature(node),
        )

    def _get_signature(self, node: ast.AST) -> str:
        """Get node signature"""
        if isinstance(node, ast.ClassDef):
            bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
            return f"class {node.name}({', '.join(bases)})"
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = [a.arg for a in node.args.args]
            is_async = isinstance(node, ast.AsyncFunctionDef)
            return f"{'async ' if is_async else ''}def {node.name}({', '.join(args)})"
        return ""

    async def _process_dependencies(self) -> None:
        """Process and link dependencies between entities"""
        for entry in self._index.values():
            for dep in entry.dependencies:
                if dep in self._index:
                    # Add bidirectional dependency
                    if dep not in entry.dependencies:
                        entry.dependencies.append(dep)
                    if entry.entity.name not in self._index[dep].dependents:
                        self._index[dep].dependents.append(entry.entity.name)

    async def _should_index_file(self, path: Path) -> bool:
        """Check if file should be indexed"""
        try:
            size = path.stat().st_size
            return size <= self.config.max_file_size
        except Exception:
            return False

    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored"""
        return any(path.match(pattern) for pattern in self.config.ignore_patterns)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        await self._ast_parser.cleanup()
        await self._import_parser.cleanup()
        self._index.clear()
        self._initialized = False
