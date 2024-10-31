"""Database module with flexible and modular database management."""
from typing import Any, Dict, List, Optional, Union, Type
from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass
from contextlib import asynccontextmanager
from loguru import logger

@dataclass
class DatabaseConfig:
    """Database configuration."""
    url: str
    pool_size: int = 5
    max_overflow: int = 10
    timeout: float = 30.0
    echo: bool = False
    ssl: bool = False
    retry_attempts: int = 3
    retry_delay: float = 1.0

class DatabaseError(Exception):
    """Base exception for database errors."""
    pass

class ConnectionError(DatabaseError):
    """Database connection error."""
    pass

class QueryError(DatabaseError):
    """Database query error."""
    pass

class Database(ABC):
    """Abstract base class for database implementations."""
    
    @abstractmethod
    async def connect(self) -> None:
        """Establish database connection."""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Close database connection."""
        pass
    
    @abstractmethod
    async def execute(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> Any:
        """Execute a database query."""
        pass
    
    @abstractmethod
    async def fetch_one(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> Optional[Dict[str, Any]]:
        """Fetch a single row."""
        pass
    
    @abstractmethod
    async def fetch_all(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> List[Dict[str, Any]]:
        """Fetch all rows."""
        pass
    
    @abstractmethod
    async def transaction(self) -> Any:
        """Start a transaction."""
        pass

class DatabaseManager:
    """Central manager for database operations."""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._db: Optional[Database] = None
        self._pool: Dict[str, Database] = {}
        self._lock = asyncio.Lock()
    
    async def get_connection(self, name: str = "default") -> Database:
        """Get a database connection from the pool."""
        async with self._lock:
            if name not in self._pool:
                db = self._create_database()
                await db.connect()
                self._pool[name] = db
            return self._pool[name]
    
    def _create_database(self) -> Database:
        """Create a database instance based on URL scheme."""
        scheme = self.config.url.split("://")[0].lower()
        
        if scheme in ["postgresql", "postgres"]:
            from .postgresql import PostgreSQLDatabase
            return PostgreSQLDatabase(self.config)
        elif scheme == "mysql":
            from .mysql import MySQLDatabase
            return MySQLDatabase(self.config)
        elif scheme == "sqlite":
            from .sqlite import SQLiteDatabase
            return SQLiteDatabase(self.config)
        else:
            raise ValueError(f"Unsupported database scheme: {scheme}")
    
    @asynccontextmanager
    async def transaction(self, name: str = "default"):
        """Context manager for database transactions."""
        db = await self.get_connection(name)
        async with db.transaction() as transaction:
            try:
                yield transaction
            except Exception as e:
                logger.error(f"Transaction error: {str(e)}")
                raise
    
    async def execute_query(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None,
        connection_name: str = "default"
    ) -> Any:
        """Execute a database query."""
        db = await self.get_connection(connection_name)
        try:
            return await db.execute(query, params)
        except Exception as e:
            logger.error(f"Query execution error: {str(e)}")
            raise QueryError(str(e))
    
    async def fetch_one(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None,
        connection_name: str = "default"
    ) -> Optional[Dict[str, Any]]:
        """Fetch a single row."""
        db = await self.get_connection(connection_name)
        try:
            return await db.fetch_one(query, params)
        except Exception as e:
            logger.error(f"Fetch error: {str(e)}")
            raise QueryError(str(e))
    
    async def fetch_all(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None,
        connection_name: str = "default"
    ) -> List[Dict[str, Any]]:
        """Fetch all rows."""
        db = await self.get_connection(connection_name)
        try:
            return await db.fetch_all(query, params)
        except Exception as e:
            logger.error(f"Fetch error: {str(e)}")
            raise QueryError(str(e))
    
    async def close_all(self):
        """Close all database connections."""
        async with self._lock:
            for db in self._pool.values():
                await db.disconnect()
            self._pool.clear()

# Convenience functions
async def create_database(url: str, **kwargs) -> DatabaseManager:
    """Create a database manager instance."""
    config = DatabaseConfig(url=url, **kwargs)
    return DatabaseManager(config)

@asynccontextmanager
async def database_connection(url: str, **kwargs):
    """Context manager for database connections."""
    manager = await create_database(url, **kwargs)
    try:
        yield manager
    finally:
        await manager.close_all() 