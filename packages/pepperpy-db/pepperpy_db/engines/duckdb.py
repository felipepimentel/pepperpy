"""DuckDB engine implementation"""

import time
from typing import Any, Protocol, Sequence

import duckdb

from ..config import DatabaseConfig
from ..exceptions import DatabaseError
from ..types import QueryResult
from .base import BaseEngine


class DuckDBConnection(Protocol):
    """DuckDB connection protocol"""

    def execute(self, query: str, parameters: dict[str, Any] | None = None) -> Any: ...

    def fetchall(self) -> list[Any]: ...

    def close(self) -> None: ...


class DuckDBEngine(BaseEngine):
    """DuckDB database engine"""

    def __init__(self, config: DatabaseConfig) -> None:
        super().__init__(config)
        self._conn: DuckDBConnection | None = None

    async def execute(self, query: str, params: dict[str, Any] | None = None) -> QueryResult:
        """Execute DuckDB query"""
        self._ensure_initialized()
        if not self._conn:
            raise DatabaseError("Database connection not initialized")

        try:
            start_time = time.time()
            result = self._conn.execute(query, parameters=params or {}).fetchall()

            rows = [{str(k): v for k, v in row.items()} for row in result]

            return QueryResult(
                rows=rows,
                affected_rows=len(result),
                execution_time=time.time() - start_time,
            )
        except Exception as e:
            raise DatabaseError(f"DuckDB query failed: {e!s}", cause=e)

    async def _initialize(self) -> None:
        """Initialize DuckDB database"""
        await super()._initialize()
        try:
            self._conn = duckdb.connect(
                database=self.config.database,
                read_only=False,
                **self.config.params,
            )
        except Exception as e:
            raise DatabaseError(f"Failed to initialize DuckDB: {e!s}", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup DuckDB resources"""
        if self._conn:
            self._conn.close()
        await super()._cleanup()

    async def execute_many(
        self, query: str, params_list: Sequence[dict[str, Any]]
    ) -> list[QueryResult]:
        """Execute multiple DuckDB queries"""
        self._ensure_initialized()
        if not self._conn:
            raise DatabaseError("Database connection not initialized")

        try:
            results = []
            for params in params_list:
                start_time = time.time()
                result = self._conn.execute(query, parameters=params).fetchall()

                rows = [{str(k): v for k, v in row.items()} for row in result]

                results.append(
                    QueryResult(
                        rows=rows,
                        affected_rows=len(result),
                        execution_time=time.time() - start_time,
                    )
                )
            return results
        except Exception as e:
            raise DatabaseError(f"DuckDB batch query failed: {e!s}", cause=e)

    async def transaction(self) -> Any:
        """Get DuckDB transaction context manager"""
        self._ensure_initialized()
        return self._conn
