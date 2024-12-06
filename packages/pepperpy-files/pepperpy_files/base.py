"""Base file handler implementation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .types import FileContent


@dataclass
class FileHandlerConfig:
    """File handler configuration."""

    allowed_extensions: set[str] = field(default_factory=set)
    base_path: Path = field(default_factory=lambda: Path("."))
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    encoding: str = "utf-8"
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseHandler(ABC):
    """Base file handler implementation."""

    def __init__(self, config: FileHandlerConfig | None = None) -> None:
        """Initialize handler.

        Args:
            config: Handler configuration
        """
        self.config = config or FileHandlerConfig()
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize handler."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup handler."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    @abstractmethod
    async def _setup(self) -> None:
        """Setup handler."""
        pass

    @abstractmethod
    async def _teardown(self) -> None:
        """Teardown handler."""
        pass

    @abstractmethod
    async def read(self, path: str | Path) -> FileContent:
        """Read file content.

        Args:
            path: File path

        Returns:
            File content
        """
        pass

    @abstractmethod
    async def write(self, content: Any, output: str | Path) -> None:
        """Write file content.

        Args:
            content: Content to write
            output: Output path
        """
        pass

    def _convert_extensions(self, extensions: list[str]) -> set[str]:
        """Convert list of extensions to set.

        Args:
            extensions: List of file extensions

        Returns:
            Set of file extensions
        """
        return set(extensions)
