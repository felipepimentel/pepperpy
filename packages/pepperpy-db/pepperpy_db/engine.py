"""Database engine module."""

import time
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, cast

from pepperpy_core.exceptions import PepperpyError
from sqlalchemy import text
from sqlalchemy.engine import CursorResult, Engine
from sqlalchemy.orm import Session


class DatabaseError(PepperpyError):
    """Database specific error."""

    pass


@dataclass
class QueryResult:
    """Query result data."""

    rows: Sequence[dict[str, Any]]
    affected_rows: int
    execution_time: float
    metadata: dict[str, Any] = field(default_factory=dict)


class DatabaseEngine:
    """Database engine implementation."""

    def __init__(self, engine: Engine) -> None:
        """Initialize database engine."""
        self._engine = engine
        self._session: Session | None = None

    async def connect(self) -> None:
        """Connect to database."""
        if not self._session:
            self._session = Session(self._engine)

    async def disconnect(self) -> None:
        """Disconnect from database."""
        if self._session:
            self._session.close()
            self._session = None

    async def execute(
        self, query: str, params: dict[str, Any] | None = None
    ) -> QueryResult:
        """Execute query."""
        try:
            if not self._session:
                raise DatabaseError("Not connected to database")

            start_time = time.perf_counter()
            # Convert SQL string to executable
            stmt = text(query)
            # Use bind parameters instead of direct dict
            result = self._session.execute(stmt, params or {})
            # Cast result to CursorResult to access rowcount
            cursor_result = cast(CursorResult[Any], result)
            execution_time = time.perf_counter() - start_time

            rows = [dict(row._mapping) for row in result.fetchall()]

            return QueryResult(
                rows=rows,
                affected_rows=cursor_result.rowcount,
                execution_time=execution_time,
            )

        except Exception as e:
            raise DatabaseError(f"Query execution failed: {str(e)}")

    async def execute_many(
        self, query: str, params_list: Sequence[dict[str, Any]]
    ) -> QueryResult:
        """Execute multiple queries."""
        try:
            if not self._session:
                raise DatabaseError("Not connected to database")

            start_time = time.perf_counter()
            # Convert SQL string to executable
            stmt = text(query)
            # Execute with sequence of parameters
            result = self._session.execute(stmt, [dict(p) for p in params_list])
            # Cast result to CursorResult to access rowcount
            cursor_result = cast(CursorResult[Any], result)
            execution_time = time.perf_counter() - start_time

            return QueryResult(
                rows=[],  # executemany doesn't return rows
                affected_rows=cursor_result.rowcount,
                execution_time=execution_time,
            )

        except Exception as e:
            raise DatabaseError(f"Batch query execution failed: {str(e)}")

    async def get_stats(self) -> dict[str, Any]:
        """Get database engine statistics."""
        return {
            "connected": self._session is not None,
            "engine_url": str(self._engine.url),
            # Access pool size safely
            "pool_size": getattr(self._engine.pool, "_size", None),
        }
