"""Base database engine implementation"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..config import DatabaseConfig
from ..types import QueryResult


class BaseEngine(ABC):
    """Base class for database engines"""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._pool = None

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize database engine"""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup database resources"""
        pass

    @abstractmethod
    async def execute(self, query: str, params: Optional[Dict[str, Any]] = None) -> QueryResult:
        """Execute database query"""
        pass

    @abstractmethod
    async def execute_many(
        self, query: str, params_list: List[Dict[str, Any]]
    ) -> List[QueryResult]:
        """Execute multiple queries"""
        pass

    @abstractmethod
    async def transaction(self) -> Any:
        """Get transaction context manager"""
        pass
