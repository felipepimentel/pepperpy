"""PostgreSQL database implementation."""
from typing import Any, Dict, List, Optional, Union
import asyncpg
from contextlib import asynccontextmanager
from ..database import Database, DatabaseConfig, ConnectionError, QueryError

class PostgreSQLDatabase(Database):
    """PostgreSQL database implementation."""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._pool: Optional[asyncpg.Pool] = None
    
    async def connect(self) -> None:
        """Establish connection pool."""
        try:
            self._pool = await asyncpg.create_pool(
                self.config.url,
                min_size=1,
                max_size=self.config.pool_size,
                max_inactive_connection_lifetime=self.config.timeout,
                command_timeout=self.config.timeout,
                ssl=self.config.ssl
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL: {str(e)}")
    
    async def disconnect(self) -> None:
        """Close all connections."""
        if self._pool:
            await self._pool.close()
    
    async def execute(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> Any:
        """Execute a query."""
        if not self._pool:
            raise ConnectionError("Not connected to database")
            
        try:
            async with self._pool.acquire() as conn:
                return await conn.execute(query, *(params or ()))
        except Exception as e:
            raise QueryError(f"Query execution failed: {str(e)}")
    
    async def fetch_one(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> Optional[Dict[str, Any]]:
        """Fetch a single row."""
        if not self._pool:
            raise ConnectionError("Not connected to database")
            
        try:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(query, *(params or ()))
                return dict(row) if row else None
        except Exception as e:
            raise QueryError(f"Fetch failed: {str(e)}")
    
    async def fetch_all(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> List[Dict[str, Any]]:
        """Fetch all rows."""
        if not self._pool:
            raise ConnectionError("Not connected to database")
            
        try:
            async with self._pool.acquire() as conn:
                rows = await conn.fetch(query, *(params or ()))
                return [dict(row) for row in rows]
        except Exception as e:
            raise QueryError(f"Fetch failed: {str(e)}")
    
    @asynccontextmanager
    async def transaction(self):
        """Start a transaction."""
        if not self._pool:
            raise ConnectionError("Not connected to database")
            
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                yield conn 