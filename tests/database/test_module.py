import pytest

from pepperpy.core.types import ModuleConfig
from pepperpy.database import DatabaseModule


@pytest.fixture
async def db_module():
    config = ModuleConfig(
        name="database",
        settings={
            "backend": "postgresql",
            "connection": {"url": "postgresql://localhost/test"},
        },
    )
    module = DatabaseModule(config)
    await module.setup()
    yield module
    await module.cleanup()


async def test_database_initialization(db_module):
    assert db_module.status == "active"
    assert db_module._engine is not None


async def test_database_query(db_module):
    result = await db_module.execute("SELECT 1")
    assert result.success
    assert result.data == [(1,)]


async def test_database_transaction(db_module):
    async with db_module.transaction.begin() as session:
        result = await session.execute("SELECT 1")
        assert result.scalar_one() == 1
