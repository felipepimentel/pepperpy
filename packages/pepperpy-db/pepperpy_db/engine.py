"""Database engine implementation"""

from typing import Any, AsyncGenerator, Dict, Optional

import asyncpg
from asyncpg import Connection, Pool

from ..module import BaseModule
from .config import DatabaseConfig
from .types import DatabaseError, QueryResult


class DatabaseEngine(BaseModule[DatabaseConfig]):
    """Database engine implementation"""

    def __init__(self, config: DatabaseConfig) -> None:
        super().__init__(config)
        self._pool: Optional[Pool] = None

    async def _initialize(self) -> None:
        """Initialize database engine"""
        try:
            self._pool = await asyncpg.create_pool(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password,
                min_size=1,
                max_size=self.config.pool_size,
                command_timeout=self.config.timeout,
                ssl=self.config.ssl_enabled,
                **self.config.options,
            )
        except Exception as e:
            raise DatabaseError("Failed to initialize database engine", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup database engine"""
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def execute(self, query: str, params: Optional[Dict[str, Any]] = None) -> QueryResult:
        """Execute database query"""
        self._ensure_initialized()
        if not self._pool:
            raise DatabaseError("Database pool not initialized")

        try:
            async with self._pool.acquire() as conn:
                result = await conn.fetch(query, *(params or {}).values())
                return QueryResult(rows=[dict(row) for row in result], count=len(result))
        except Exception as e:
            raise DatabaseError(f"Query execution failed: {e}", cause=e)

    async def stream(
        self, query: str, params: Optional[Dict[str, Any]] = None, batch_size: int = 1000
    ) -> AsyncGenerator[QueryResult, None]:
        """Stream query results"""
        self._ensure_initialized()
        if not self._pool:
            raise DatabaseError("Database pool not initialized")

        try:
            async with self._pool.acquire() as conn:
                async for batch in self._stream_results(conn, query, params, batch_size):
                    yield batch
        except Exception as e:
            raise DatabaseError(f"Query streaming failed: {e}", cause=e)

    async def _stream_results(
        self, conn: Connection, query: str, params: Optional[Dict[str, Any]], batch_size: int
    ) -> AsyncGenerator[QueryResult, None]:
        """Stream results in batches"""
        try:
            async with conn.transaction():
                cursor = await conn.cursor(query, *(params or {}).values())
                while True:
                    rows = await cursor.fetch(batch_size)
                    if not rows:
                        break
                    yield QueryResult(rows=[dict(row) for row in rows], count=len(rows))
        except Exception as e:
            raise DatabaseError(f"Result streaming failed: {e}", cause=e)
