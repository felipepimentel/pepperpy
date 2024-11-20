"""Code indexing implementation"""

from pathlib import Path
from typing import AsyncGenerator

from pepperpy.core.module import BaseModule

from .config import CodebaseConfig
from .types import IndexEntry


class CodeIndexer(BaseModule[CodebaseConfig]):
    """Code indexer implementation"""

    def __init__(self, config: CodebaseConfig) -> None:
        super().__init__(config)
        self._index: dict[str, IndexEntry] = {}

    async def index_project(self, path: Path) -> list[IndexEntry]:
        """Index project at path"""
        if not self._initialized:
            await self.initialize()

        self._index.clear()
        async for entry in self._scan_path(path):
            self._index[entry.id] = entry
        return list(self._index.values())

    async def _scan_path(self, path: Path) -> AsyncGenerator[IndexEntry, None]:
        """Scan path for code files"""
        if path.is_file() and path.suffix == ".py":
            yield await self._index_file(path)
        elif path.is_dir():
            for item in path.iterdir():
                if not self._should_ignore(item):
                    async for entry in self._scan_path(item):
                        yield entry

    async def _index_file(self, path: Path) -> IndexEntry:
        """Index single file"""
        # Implementation here
        raise NotImplementedError

    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored"""
        return any(path.match(pattern) for pattern in self.config.ignore_patterns)

    async def _initialize(self) -> None:
        """Initialize indexer"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        self._index.clear()
