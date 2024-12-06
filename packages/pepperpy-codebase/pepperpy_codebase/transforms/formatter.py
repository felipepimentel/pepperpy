"""Code formatter implementation."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from ..config import CodebaseConfig
from .types import FormatOptions, TransformResult

ConfigT = TypeVar("ConfigT", bound=CodebaseConfig)


class BaseFormatter(Generic[ConfigT], ABC):
    """Base formatter implementation."""

    def __init__(self, config: ConfigT) -> None:
        """Initialize formatter.

        Args:
            config: Formatter configuration
        """
        self.config = config
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if formatter is initialized."""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize formatter."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup formatter resources."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    def _ensure_initialized(self) -> None:
        """Ensure formatter is initialized."""
        if not self._initialized:
            raise RuntimeError("Formatter not initialized")

    @abstractmethod
    async def _setup(self) -> None:
        """Setup formatter resources."""
        pass

    @abstractmethod
    async def _teardown(self) -> None:
        """Teardown formatter resources."""
        pass

    @abstractmethod
    async def format_code(
        self, code: str, options: FormatOptions | None = None
    ) -> TransformResult:
        """Format code.

        Args:
            code: Code to format
            options: Format options

        Returns:
            Format result

        Raises:
            RuntimeError: If formatter not initialized
        """
        pass

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        """Get formatter statistics.

        Returns:
            Formatter statistics

        Raises:
            RuntimeError: If formatter not initialized
        """
        pass
