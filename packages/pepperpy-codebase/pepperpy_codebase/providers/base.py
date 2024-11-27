"""Base codebase provider implementation"""

from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Protocol, Sequence

from bko.core.module import BaseModule

from ..config import CodebaseConfig
from ..types import CodeFile, CodeSearchResult


class FileReader(Protocol):
    """File reader protocol"""

    async def read_text(self, path: str) -> str:
        """Read text file"""
        ...

    async def exists(self, path: str) -> bool:
        """Check if file exists"""
        ...


class BaseProvider(BaseModule[CodebaseConfig], ABC):
    """Base codebase provider implementation"""

    def __init__(self, config: CodebaseConfig) -> None:
        super().__init__(config)
        self._file_reader: FileReader | None = None

    @abstractmethod
    async def search(self, query: str, **kwargs: Any) -> AsyncGenerator[CodeSearchResult, None]:
        """Search codebase"""
        pass

    @abstractmethod
    async def get_file(self, path: str) -> CodeFile:
        """Get file content"""
        pass

    @abstractmethod
    async def get_files(self, pattern: str) -> Sequence[CodeFile]:
        """Get files matching pattern"""
        pass
