"""Client for database operations"""

from typing import Any

from pepperpy.core.module import InitializableModule
from pepperpy.core.validation import ValidatorFactory

from .config import DatabaseConfig
from .exceptions import DatabaseError
from .types import QueryResult


class DatabaseClient(InitializableModule):
    """Database client implementation"""

    def __init__(self, config: DatabaseConfig):
        super().__init__()
        self.config = config
        self._config_validator = ValidatorFactory.create_schema_validator(DatabaseConfig)
        self._connection = None

    async def _initialize(self) -> None:
        """Initialize database connection"""
        result = await self._config_validator.validate(self.config.model_dump())
        if not result.is_valid:
            raise DatabaseError(f"Invalid database configuration: {', '.join(result.errors)}")
        await self.connect()

    async def _cleanup(self) -> None:
        """Cleanup database resources"""
        await self.disconnect()

    async def connect(self) -> None:
        """Establish database connection"""
        raise NotImplementedError

    async def disconnect(self) -> None:
        """Close database connection"""
        raise NotImplementedError

    async def execute_query(self, query: str, params: dict[str, Any] | None = None) -> QueryResult:
        """Execute a database query"""
        self._ensure_initialized()
        raise NotImplementedError
