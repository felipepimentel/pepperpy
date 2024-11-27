"""Base database engine implementation"""

from abc import abstractmethod
from typing import Any, Protocol

from bko.core.module import InitializableModule

from ..config import DatabaseConfig
from ..types import QueryResult


class Pool(Protocol):
    """Database pool protocol"""

    async def close(self) -> None:
        """Close pool connection"""
        ...


class BaseEngine(InitializableModule):
    """Base class for database engines"""

    def __init__(self, config: DatabaseConfig) -> None:
        super().__init__()
        self.config = config
        self._pool: Pool | None = None

    @abstractmethod
    async def execute(self, query: str, params: dict[str, Any] | None = None) -> QueryResult:
        """Execute database query"""
        pass

    async def _initialize(self) -> None:
        """Initialize database engine"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup database engine"""
        if self._pool:
            await self._pool.close()
            self._pool = None
