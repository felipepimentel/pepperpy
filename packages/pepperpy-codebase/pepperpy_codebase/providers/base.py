"""Base provider implementation."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from ..config import CodebaseConfig
from ..types import FileContent

ConfigT = TypeVar("ConfigT", bound=CodebaseConfig)


@dataclass
class SearchResult:
    """Search result."""

    file: FileContent
    matches: Sequence[str]
    line_numbers: Sequence[int]
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseProvider(Generic[ConfigT], ABC):
    """Base provider implementation."""

    def __init__(self, config: ConfigT) -> None:
        """Initialize provider.

        Args:
            config: Provider configuration
        """
        self.config = config
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if provider is initialized."""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize provider."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup provider resources."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    def _ensure_initialized(self) -> None:
        """Ensure provider is initialized."""
        if not self._initialized:
            raise RuntimeError("Provider not initialized")

    @abstractmethod
    async def _setup(self) -> None:
        """Setup provider resources."""
        pass

    @abstractmethod
    async def _teardown(self) -> None:
        """Teardown provider resources."""
        pass

    @abstractmethod
    async def get_file(self, path: str) -> FileContent | None:
        """Get file content.

        Args:
            path: File path

        Returns:
            File content if found, None otherwise

        Raises:
            RuntimeError: If provider not initialized
        """
        pass

    @abstractmethod
    async def search(self, query: str, **kwargs: Any) -> Sequence[SearchResult]:
        """Search files.

        Args:
            query: Search query
            **kwargs: Additional arguments

        Returns:
            Search results

        Raises:
            RuntimeError: If provider not initialized
        """
        pass

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        """Get provider statistics.

        Returns:
            Provider statistics

        Raises:
            RuntimeError: If provider not initialized
        """
        pass
