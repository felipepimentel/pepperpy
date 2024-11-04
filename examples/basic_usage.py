from pepperpy.cache import CacheModule
from pepperpy.core import PepperApp
from pepperpy.database import DatabaseModule


async def main() -> None:
    # Create application
    app = PepperApp()

    # Register modules with config
    app.register_module(CacheModule, {"backend": "memory", "ttl": 3600})

    app.register_module(DatabaseModule, {"url": "postgresql://localhost/db"})

    # Start application
    await app.start()

    # Use modules
    cache = app.get_module("cache")
    await cache.set("key", "value")

    # Cleanup
    await app.stop()
