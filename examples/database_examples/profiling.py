import asyncio

from pepperpy.core.types import ModuleConfig
from pepperpy.database import DatabaseModule


async def main() -> None:
    config = ModuleConfig(
        name="database",
        settings={
            "backend": "postgresql",
            "connection": {"url": "postgresql://user:pass@localhost/db"},
            "slow_query_threshold": 0.5,  # 500ms
        },
    )

    db = DatabaseModule(config)
    await db.setup()

    try:
        # Execute some queries
        for i in range(10):
            await db.execute("SELECT pg_sleep(0.1 * :i)", {"i": i})

        # Get profiling information
        profile = await db.get_profile()
        print("\nDatabase Profile:")
        print(f"Total Queries: {profile['total_queries']}")
        print(f"Average Duration: {profile['average_duration']:.3f}s")
        print(f"Slow Queries: {profile['slow_queries']}")
        print(f"Cache Hit Ratio: {profile['cache_hit_ratio']:.2%}")
        print(f"Connection Utilization: {profile['connection_utilization']:.2%}")

    finally:
        await db.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
