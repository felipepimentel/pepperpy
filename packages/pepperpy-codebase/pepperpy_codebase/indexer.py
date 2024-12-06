"""Codebase indexer implementation."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from .config import IndexConfig
from .types import FileContent

ConfigT = TypeVar("ConfigT", bound=IndexConfig)


@dataclass
class IndexEntry:
    """Index entry."""

    file: FileContent
    tokens: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseIndexer(Generic[ConfigT], ABC):
    """Base indexer implementation."""

    def __init__(self, config: ConfigT) -> None:
        """Initialize indexer.

        Args:
            config: Indexer configuration
        """
        self.config = config
        self._initialized = False
        self._index: dict[str, IndexEntry] = {}

    @property
    def is_initialized(self) -> bool:
        """Check if indexer is initialized."""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize indexer."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup indexer resources."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    def _ensure_initialized(self) -> None:
        """Ensure indexer is initialized."""
        if not self._initialized:
            raise RuntimeError("Indexer not initialized")

    @abstractmethod
    async def _setup(self) -> None:
        """Setup indexer resources."""
        pass

    @abstractmethod
    async def _teardown(self) -> None:
        """Teardown indexer resources."""
        pass

    @abstractmethod
    async def index_file(self, file: FileContent) -> None:
        """Index file.

        Args:
            file: File to index

        Raises:
            RuntimeError: If indexer not initialized
        """
        pass

    @abstractmethod
    async def remove_file(self, path: str) -> None:
        """Remove file from index.

        Args:
            path: File path

        Raises:
            RuntimeError: If indexer not initialized
        """
        pass

    @abstractmethod
    async def search(self, query: str, **kwargs: Any) -> Sequence[IndexEntry]:
        """Search index.

        Args:
            query: Search query
            **kwargs: Additional arguments

        Returns:
            Matching index entries

        Raises:
            RuntimeError: If indexer not initialized
        """
        pass

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        """Get indexer statistics.

        Returns:
            Indexer statistics

        Raises:
            RuntimeError: If indexer not initialized
        """
        pass
