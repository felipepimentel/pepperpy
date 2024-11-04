from contextlib import asynccontextmanager
from typing import Any, Dict, Optional, Type

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pepperpy.core import BaseModule

from .exceptions import DatabaseError
from .migrations import MigrationManager
from .models import BaseModel
from .query import QueryBuilder


class DatabaseModule(BaseModule):
    """Database management module with multiple backend support"""

    __module_name__ = "database"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[sessionmaker] = None
        self._base = declarative_base()
        self._migration_manager = MigrationManager(self)
        self._query_builder = QueryBuilder()

    async def setup(self) -> None:
        """Initialize database connection"""
        url = self.config.settings.get("url")
        if not url:
            raise DatabaseError("Database URL not configured")

        # Create engine with optimized settings
        self._engine = create_async_engine(
            url,
            echo=self.config.settings.get("echo", False),
            pool_size=self.config.settings.get("pool_size", 5),
            max_overflow=self.config.settings.get("max_overflow", 10),
            pool_timeout=self.config.settings.get("pool_timeout", 30),
            pool_recycle=self.config.settings.get("pool_recycle", 1800),
            pool_pre_ping=True,
        )

        # Create session factory
        self._session_factory = sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )

        # Run migrations if enabled
        if self.config.settings.get("auto_migrate", True):
            await self._migration_manager.run_migrations()

        await super().setup()

    async def cleanup(self) -> None:
        """Cleanup database resources"""
        if self._engine:
            await self._engine.dispose()
        await super().cleanup()

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        """Get database session with automatic cleanup"""
        if not self._session_factory:
            raise DatabaseError("Database not initialized")

        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def execute(self, query: str, params: Optional[Dict] = None) -> Any:
        """Execute raw SQL query"""
        async with self.session() as session:
            result = await session.execute(query, params or {})
            return result

    def register_model(self, model: Type[BaseModel]) -> None:
        """Register model with database"""
        if not issubclass(model, BaseModel):
            raise TypeError("Model must inherit from BaseModel")
        model.__table__.create(self._engine)
