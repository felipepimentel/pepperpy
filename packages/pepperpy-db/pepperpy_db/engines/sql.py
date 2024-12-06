"""SQL database engine implementation."""

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from ..base import BaseEngine, BaseEngineConfig, DatabaseError


@dataclass
class SQLEngineConfig(BaseEngineConfig):
    """SQL engine configuration."""

    url: str = ""
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: float = 30.0
    pool_recycle: int = -1
    echo: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


class SQLEngine(BaseEngine[SQLEngineConfig]):
    """SQL database engine implementation."""

    def __init__(self, config: SQLEngineConfig) -> None:
        """Initialize SQL engine."""
        super().__init__(config)
        self._engine: Engine | None = None
        self._session: Session | None = None

    async def execute(
        self, query: str, params: dict[str, Any] | None = None
    ) -> Sequence[dict[str, Any]]:
        """Execute query."""
        self._ensure_initialized()
        if not self._session:
            raise DatabaseError("Not connected to database")

        try:
            # Convert SQL string to executable
            stmt = text(query)
            # Use bind parameters instead of direct dict
            result = self._session.execute(stmt, params or {})
            return [dict(row._mapping) for row in result.fetchall()]
        except Exception as e:
            raise DatabaseError(f"Query execution failed: {str(e)}")

    async def get_stats(self) -> dict[str, Any]:
        """Get SQL engine statistics.

        Returns:
            Engine statistics
        """
        return {
            "connected": self._session is not None,
            "url": self.config.url,
            "pool_size": self.config.pool_size,
            "max_overflow": self.config.max_overflow,
            "pool_timeout": self.config.pool_timeout,
            "pool_recycle": self.config.pool_recycle,
            "echo": self.config.echo,
        }
