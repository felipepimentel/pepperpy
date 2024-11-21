"""SQLite database engine"""

import sqlite3
from typing import Any, Protocol, Sequence, cast

from ..config import DatabaseConfig
from ..exceptions import DatabaseError
from ..types import QueryResult
from .base import BaseEngine


class SQLiteCursor(Protocol):
    """SQLite cursor protocol"""

    @property
    def description(self) -> list[tuple[str, ...]]: ...
    @property
    def rowcount(self) -> int: ...
    def execute(self, sql: str, parameters: dict[str, Any] | None = None) -> Any: ...
    def fetchall(self) -> list[tuple[Any, ...]]: ...
    def close(self) -> None: ...


class SQLiteConnection(Protocol):
    """SQLite connection protocol"""

    def cursor(self) -> SQLiteCursor: ...
    def commit(self) -> None: ...
    def close(self) -> None: ...


class SQLiteEngine(BaseEngine):
    """SQLite database engine implementation"""

    def __init__(self, config: DatabaseConfig) -> None:
        super().__init__(config)
        self._conn: SQLiteConnection | None = None
        self._cursor: SQLiteCursor | None = None

    async def _initialize(self) -> None:
        """Initialize database connection"""
        await super()._initialize()
        try:
            conn = sqlite3.connect(
                database=self.config.database,
                timeout=self.config.timeout
            )
            self._conn = cast(SQLiteConnection, conn)
            self._cursor = cast(SQLiteCursor, self._conn.cursor())
        except Exception as e:
            raise DatabaseError(f"Failed to connect to SQLite: {e}", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup database resources"""
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()
        await super()._cleanup()

    async def execute(self, query: str, params: dict[str, Any] | None = None) -> QueryResult:
        """Execute database query"""
        self._ensure_initialized()
        try:
            if not self._cursor or not self._conn:
                raise DatabaseError("Database not initialized")

            self._cursor.execute(query, params or {})
            rows = [dict(zip([col[0] for col in self._cursor.description], row))
                   for row in self._cursor.fetchall()]

            self._conn.commit()
            
            return QueryResult(
                rows=rows,
                affected_rows=self._cursor.rowcount,
                execution_time=0.0  # SQLite doesn't provide execution time
            )
        except Exception as e:
            raise DatabaseError(f"Query execution failed: {e}", cause=e)

    async def execute_many(
        self, query: str, params_list: Sequence[dict[str, Any]]
    ) -> list[QueryResult]:
        """Execute multiple SQLite queries"""
        self._ensure_initialized()
        try:
            if not self._cursor or not self._conn:
                raise DatabaseError("Database not initialized")

            results = []
            for params in params_list:
                self._cursor.execute(query, params)
                rows = [dict(zip([col[0] for col in self._cursor.description], row))
                       for row in self._cursor.fetchall()]

                results.append(
                    QueryResult(
                        rows=rows,
                        affected_rows=self._cursor.rowcount,
                        execution_time=0.0
                    )
                )

            self._conn.commit()
            return results
        except Exception as e:
            raise DatabaseError(f"SQLite batch query failed: {e}", cause=e)
