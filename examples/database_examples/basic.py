import asyncio

from pepperpy.core.types import ModuleConfig
from pepperpy.database import DatabaseModule


async def main() -> None:
    # Configure database
    config = ModuleConfig(
        name="database",
        settings={
            "backend": "postgresql",
            "connection": {
                "url": "postgresql://user:pass@localhost/db",
                "options": {"echo": True},
            },
            "pool": {"size": 5, "max_overflow": 10},
            "auto_migrate": True,
        },
    )

    # Create and initialize module
    db = DatabaseModule(config)
    await db.setup()

    try:
        # Use the module
        async with db.session() as session:
            result = await session.execute("SELECT * FROM users")
            users = result.fetchall()
            print(f"Found {len(users)} users")
    finally:
        await db.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
