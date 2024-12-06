"""Base handler module."""

from abc import ABC, abstractmethod
from pathlib import Path

from ..base import FileHandlerConfig
from ..exceptions import FileError
from ..types import FileContent


class BaseHandler(ABC):
    """Base class for file handlers."""

    def __init__(self, config: FileHandlerConfig | None = None) -> None:
        """Initialize handler.

        Args:
            config: Handler configuration
        """
        self.config = config or FileHandlerConfig()

    @abstractmethod
    async def read(self, path: Path) -> FileContent:
        """Read file content.

        Args:
            path: File path

        Returns:
            File content

        Raises:
            FileError: If file cannot be read
        """
        raise NotImplementedError

    @abstractmethod
    async def write(self, content: FileContent, path: Path | None = None) -> None:
        """Write file content.

        Args:
            content: File content
            path: Optional path to write to (defaults to content.path)

        Raises:
            FileError: If file cannot be written
        """
        raise NotImplementedError

    async def _read_file(self, path: Path) -> str:
        """Read text file content.

        Args:
            path: File path

        Returns:
            File content as string

        Raises:
            FileError: If file cannot be read
        """
        try:
            if not path.exists():
                raise FileError("File does not exist")

            if not path.is_file():
                raise FileError("Path is not a file")

            if path.stat().st_size > self.config.max_file_size:
                raise FileError("File is too large")

            return path.read_text(encoding=self.config.encoding)

        except Exception as e:
            raise FileError(f"Failed to read file: {e}") from e

    async def _write_file(self, path: Path, content: str | bytes) -> None:
        """Write file content.

        Args:
            path: File path
            content: Content to write (string or bytes)

        Raises:
            FileError: If file cannot be written
        """
        try:
            if not path.parent.exists():
                path.parent.mkdir(parents=True)

            if isinstance(content, str):
                path.write_text(content, encoding=self.config.encoding)
            else:
                path.write_bytes(content)

        except Exception as e:
            raise FileError(f"Failed to write file: {e}") from e
