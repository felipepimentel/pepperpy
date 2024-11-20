"""SQLite database engine"""

import sqlite3
from typing import Any

from ..config import DatabaseConfig
from ..exceptions import DatabaseError
from ..types import QueryResult
from .base import BaseEngine


class SQLiteEngine(BaseEngine):
    """SQLite database engine implementation"""

    def __init__(self, config: DatabaseConfig) -> None:
        super().__init__(config)
        self._conn: sqlite3.Connection | None = None
        self._cursor: sqlite3.Cursor | None = None

    async def _initialize(self) -> None:
        """Initialize database connection"""
        try:
            self._conn = sqlite3.connect(
                database=self.config.database,
                timeout=self.config.timeout
            )
            self._cursor = self._conn.cursor()
        except Exception as e:
            raise DatabaseError(f"Failed to connect to SQLite: {e}", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup database resources"""
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()

    async def execute(self, query: str, params: dict[str, Any] | None = None) -> QueryResult:
        """Execute database query"""
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
