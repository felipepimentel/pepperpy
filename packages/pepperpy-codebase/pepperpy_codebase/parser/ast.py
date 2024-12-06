"""AST parser implementation."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from ..config import CodebaseConfig
from .types import ClassInfo, FunctionInfo, ImportInfo, ModuleInfo

ConfigT = TypeVar("ConfigT", bound=CodebaseConfig)


class BaseParser(Generic[ConfigT], ABC):
    """Base parser implementation."""

    def __init__(self, config: ConfigT) -> None:
        """Initialize parser.

        Args:
            config: Parser configuration
        """
        self.config = config
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if parser is initialized."""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize parser."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup parser resources."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    def _ensure_initialized(self) -> None:
        """Ensure parser is initialized."""
        if not self._initialized:
            raise RuntimeError("Parser not initialized")

    @abstractmethod
    async def _setup(self) -> None:
        """Setup parser resources."""
        pass

    @abstractmethod
    async def _teardown(self) -> None:
        """Teardown parser resources."""
        pass

    @abstractmethod
    async def parse_module(self, code: str) -> ModuleInfo:
        """Parse module.

        Args:
            code: Module source code

        Returns:
            Module information

        Raises:
            RuntimeError: If parser not initialized
        """
        pass

    @abstractmethod
    async def parse_imports(self, code: str) -> Sequence[ImportInfo]:
        """Parse imports.

        Args:
            code: Module source code

        Returns:
            Import information

        Raises:
            RuntimeError: If parser not initialized
        """
        pass

    @abstractmethod
    async def parse_functions(self, code: str) -> Sequence[FunctionInfo]:
        """Parse functions.

        Args:
            code: Module source code

        Returns:
            Function information

        Raises:
            RuntimeError: If parser not initialized
        """
        pass

    @abstractmethod
    async def parse_classes(self, code: str) -> Sequence[ClassInfo]:
        """Parse classes.

        Args:
            code: Module source code

        Returns:
            Class information

        Raises:
            RuntimeError: If parser not initialized
        """
        pass

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        """Get parser statistics.

        Returns:
            Parser statistics

        Raises:
            RuntimeError: If parser not initialized
        """
        pass
