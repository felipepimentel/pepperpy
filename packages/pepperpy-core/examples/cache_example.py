"""Example demonstrating cache functionality"""

import asyncio
from datetime import timedelta

from pepperpy_core.cache import CacheConfig, CacheEntry, CacheManager
from pepperpy_core.utils.datetime import utc_now


async def demonstrate_memory_cache() -> None:
    """Demonstrate in-memory cache usage"""
    # Create cache manager
    config = CacheConfig(default_ttl=60, max_size=100, cleanup_interval=5)  # 1 minute  # 5 seconds
    cache = CacheManager(config)

    try:
        # Initialize cache
        await cache.initialize()

        # Store values
        print("Storing values in cache...")
        await cache.set("key1", "value1")
        await cache.set("key2", "value2", ttl=10)  # Expires in 10 seconds

        # Create expired entry
        expired_entry = CacheEntry(
            key="key3", value="value3", expires_at=utc_now() - timedelta(seconds=1)
        )
        await cache.set("key3", expired_entry)

        # Retrieve values
        print("\nRetrieving values...")
        value1 = await cache.get("key1")
        value2 = await cache.get("key2")
        value3 = await cache.get("key3")  # Should be None (expired)

        print(f"Value 1: {value1}")
        print(f"Value 2: {value2}")
        print(f"Value 3: {value3}")

        # Wait for cleanup
        print("\nWaiting for cleanup...")
        await asyncio.sleep(5)
        await cache._cleanup()

        # Check values again
        print("\nChecking values after cleanup...")
        value1 = await cache.get("key1")
        value2 = await cache.get("key2")
        value3 = await cache.get("key3")

        print(f"Value 1: {value1}")
        print(f"Value 2: {value2}")
        print(f"Value 3: {value3}")

    finally:
        await cache.cleanup()


if __name__ == "__main__":
    asyncio.run(demonstrate_memory_cache())
