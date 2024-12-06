"""PostgreSQL engine implementation."""

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

import asyncpg

from ..base import BaseEngine, BaseEngineConfig, DatabaseError


@dataclass
class PostgresConfig(BaseEngineConfig):
    """PostgreSQL configuration."""

    host: str = "localhost"
    port: int = 5432
    database: str = ""
    user: str = ""
    password: str = ""
    min_size: int = 1
    max_size: int = 10
    metadata: dict[str, Any] = field(default_factory=dict)


class PostgresExecutor(BaseEngine[PostgresConfig]):
    """PostgreSQL engine implementation."""

    def __init__(self, config: PostgresConfig) -> None:
        """Initialize PostgreSQL engine.

        Args:
            config: PostgreSQL configuration
        """
        super().__init__(config)
        self._pool: asyncpg.Pool | None = None

    async def _setup(self) -> None:
        """Setup PostgreSQL engine."""
        try:
            self._pool = await asyncpg.create_pool(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password,
                min_size=self.config.min_size,
                max_size=self.config.max_size,
            )
        except Exception as e:
            raise DatabaseError(f"Failed to connect to PostgreSQL: {str(e)}")

    async def _teardown(self) -> None:
        """Teardown PostgreSQL engine."""
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def execute(
        self, query: str, params: dict[str, Any] | None = None
    ) -> Sequence[dict[str, Any]]:
        """Execute PostgreSQL query.

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            Query results

        Raises:
            DatabaseError: If query execution fails
        """
        self._ensure_initialized()
        if not self._pool:
            raise DatabaseError("Not connected to database")

        try:
            async with self._pool.acquire() as conn:
                result = await conn.fetch(query, *(params or {}).values())
                return [dict(row) for row in result]
        except Exception as e:
            raise DatabaseError(f"Query execution failed: {str(e)}")

    async def get_stats(self) -> dict[str, Any]:
        """Get PostgreSQL engine statistics.

        Returns:
            Engine statistics
        """
        return {
            "connected": self._pool is not None,
            "host": self.config.host,
            "port": self.config.port,
            "database": self.config.database,
            "min_size": self.config.min_size,
            "max_size": self.config.max_size,
        }
