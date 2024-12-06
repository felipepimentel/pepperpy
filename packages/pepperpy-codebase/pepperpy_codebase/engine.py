"""Codebase engine implementation."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from .config import CodebaseConfig
from .indexer import BaseIndexer, IndexConfig, IndexEntry
from .types import CodebaseChange, CodebaseSnapshot, FileContent

ConfigT = TypeVar("ConfigT", bound=CodebaseConfig)


class BaseEngine(Generic[ConfigT], ABC):
    """Base codebase engine implementation."""

    def __init__(self, config: ConfigT) -> None:
        """Initialize engine.

        Args:
            config: Engine configuration
        """
        self.config = config
        self._initialized = False
        self._indexer: BaseIndexer[IndexConfig] | None = None

    @property
    def is_initialized(self) -> bool:
        """Check if engine is initialized."""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize engine."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup engine resources."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    def _ensure_initialized(self) -> None:
        """Ensure engine is initialized."""
        if not self._initialized:
            raise RuntimeError("Engine not initialized")

    @abstractmethod
    async def _setup(self) -> None:
        """Setup engine resources."""
        pass

    @abstractmethod
    async def _teardown(self) -> None:
        """Teardown engine resources."""
        pass

    @abstractmethod
    async def scan(self, path: str) -> CodebaseSnapshot:
        """Scan codebase.

        Args:
            path: Path to scan

        Returns:
            Codebase snapshot

        Raises:
            RuntimeError: If engine not initialized
        """
        pass

    @abstractmethod
    async def analyze(self, file: FileContent) -> dict[str, Any]:
        """Analyze file.

        Args:
            file: File to analyze

        Returns:
            Analysis results

        Raises:
            RuntimeError: If engine not initialized
        """
        pass

    @abstractmethod
    async def search(self, query: str, **kwargs: Any) -> Sequence[IndexEntry]:
        """Search codebase.

        Args:
            query: Search query
            **kwargs: Additional arguments

        Returns:
            Search results

        Raises:
            RuntimeError: If engine not initialized
        """
        pass

    @abstractmethod
    async def get_changes(self, since: str) -> CodebaseChange:
        """Get codebase changes.

        Args:
            since: Version or timestamp

        Returns:
            Codebase changes

        Raises:
            RuntimeError: If engine not initialized
        """
        pass

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        """Get engine statistics.

        Returns:
            Engine statistics

        Raises:
            RuntimeError: If engine not initialized
        """
        pass
