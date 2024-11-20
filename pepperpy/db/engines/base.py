"""Base database engine"""

from abc import abstractmethod
from typing import Any

from pepperpy.core.module import BaseModule

from ..config import DatabaseConfig
from ..types import QueryResult


class BaseEngine(BaseModule[DatabaseConfig]):
    """Base database engine"""

    def __init__(self, config: DatabaseConfig) -> None:
        """Initialize database engine.

        Args:
            config: Database configuration
        """
        super().__init__(config)

    @abstractmethod
    async def execute(self, query: str, params: dict[str, Any] | None = None) -> QueryResult:
        """Execute database query"""
        raise NotImplementedError

    async def _initialize(self) -> None:
        """Initialize database connection"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup database resources"""
        pass
