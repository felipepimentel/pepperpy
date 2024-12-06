"""Code refactoring implementation."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from ..config import CodebaseConfig
from .types import RefactorOptions, TransformResult

ConfigT = TypeVar("ConfigT", bound=CodebaseConfig)


class BaseRefactorer(Generic[ConfigT], ABC):
    """Base refactorer implementation."""

    def __init__(self, config: ConfigT) -> None:
        """Initialize refactorer.

        Args:
            config: Refactorer configuration
        """
        self.config = config
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if refactorer is initialized."""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize refactorer."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup refactorer resources."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    def _ensure_initialized(self) -> None:
        """Ensure refactorer is initialized."""
        if not self._initialized:
            raise RuntimeError("Refactorer not initialized")

    @abstractmethod
    async def _setup(self) -> None:
        """Setup refactorer resources."""
        pass

    @abstractmethod
    async def _teardown(self) -> None:
        """Teardown refactorer resources."""
        pass

    @abstractmethod
    async def refactor_code(
        self, code: str, options: RefactorOptions | None = None
    ) -> TransformResult:
        """Refactor code.

        Args:
            code: Code to refactor
            options: Refactor options

        Returns:
            Refactor result

        Raises:
            RuntimeError: If refactorer not initialized
        """
        pass

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        """Get refactorer statistics.

        Returns:
            Refactorer statistics

        Raises:
            RuntimeError: If refactorer not initialized
        """
        pass
