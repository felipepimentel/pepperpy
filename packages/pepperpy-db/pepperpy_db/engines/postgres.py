"""PostgreSQL database engine"""

import time
from typing import Any, AsyncContextManager, Protocol, Sequence

import asyncpg
from asyncpg.pool import Pool as AsyncpgPool

from ..config import DatabaseConfig
from ..exceptions import DatabaseError
from ..types import QueryResult
from .base import BaseEngine


class Connection(Protocol):
    """Database connection protocol"""

    async def fetch(self, query: str, *args: Any) -> Sequence[Any]:
        """Execute query and fetch results"""
        ...

    async def execute(self, query: str, *args: Any) -> str:
        """Execute query"""
        ...

    async def close(self) -> None:
        """Close connection"""
        ...


class Pool(Protocol):
    """Database pool protocol"""

    async def close(self) -> None:
        """Close pool connection"""
        ...

    def acquire(self, *, timeout: float | None = None) -> AsyncContextManager[Connection]:
        """Acquire connection from pool"""
        ...


class PostgresEngine(BaseEngine):
    """PostgreSQL database engine"""

    def __init__(self, config: DatabaseConfig) -> None:
        super().__init__(config)
        self._pool: AsyncpgPool | None = None

    async def _initialize(self) -> None:
        """Initialize database connection"""
        await super()._initialize()
        try:
            self._pool = await asyncpg.create_pool(
                host=self.config.host,
                port=self.config.port,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database,
                min_size=self.config.min_size,
                max_size=self.config.max_size,
                **self.config.params,
            )
        except Exception as e:
            raise DatabaseError(f"Failed to connect to PostgreSQL: {e}", cause=e)

    async def execute(self, query: str, params: dict[str, Any] | None = None) -> QueryResult:
        """Execute database query"""
        self._ensure_initialized()
        if not self._pool:
            raise DatabaseError("Database pool not initialized")

        try:
            start_time = time.time()
            async with self._pool.acquire() as conn:
                result = await conn.fetch(query, *(params or {}).values())
                rows = [dict(row) for row in result]

            return QueryResult(
                rows=rows,
                affected_rows=len(rows),
                execution_time=time.time() - start_time,
            )
        except Exception as e:
            raise DatabaseError(f"Query execution failed: {e}", cause=e)

    async def execute_many(
        self, query: str, params_list: Sequence[dict[str, Any]]
    ) -> list[QueryResult]:
        """Execute multiple PostgreSQL queries"""
        self._ensure_initialized()
        if not self._pool:
            raise DatabaseError("Database pool not initialized")

        try:
            results = []
            async with self._pool.acquire() as conn:
                for params in params_list:
                    start_time = time.time()
                    result = await conn.fetch(query, *params.values())
                    rows = [dict(row) for row in result]

                    results.append(
                        QueryResult(
                            rows=rows,
                            affected_rows=len(rows),
                            execution_time=time.time() - start_time,
                        )
                    )
            return results
        except Exception as e:
            raise DatabaseError(f"PostgreSQL batch query failed: {e}", cause=e)
