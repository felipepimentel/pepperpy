from typing import AsyncGenerator

import pytest

from pepperpy.core.exceptions import DatabaseError
from pepperpy.core.types import DatabaseConfig
from pepperpy.database import DatabaseModule


@pytest.fixture
async def database_module() -> AsyncGenerator[DatabaseModule, None]:
    """Fixture providing configured database module"""
    config = DatabaseConfig(
        backend="postgresql",
        connection_url="postgresql://localhost/test",
        pool_size=5,
        debug=True,
    )

    module = DatabaseModule(config=config)
    await module.setup()

    try:
        yield module
    finally:
        await module.cleanup()


@pytest.mark.asyncio
async def test_database_operations(database_module: DatabaseModule):
    """Test core database operations"""
    # Transaction management
    async with database_module.transaction() as session:
        # Query execution
        result = await session.execute("SELECT 1")
        assert result.success
        assert result.data == [(1,)]

        # Error handling
        with pytest.raises(DatabaseError):
            await session.execute("INVALID SQL")
