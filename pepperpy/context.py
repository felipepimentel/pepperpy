"""Context managers for resource management."""
from typing import Optional, Any, TypeVar
from contextlib import asynccontextmanager
import asyncio

T = TypeVar('T')

class ResourceManager:
    """Manage async resources with context managers."""
    
    def __init__(self):
        self._resources = {}
        self._locks = {}
        
    @asynccontextmanager
    async def acquire(self, key: str, factory: callable, **kwargs):
        """Acquire a resource with automatic cleanup."""
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
            
        async with self._locks[key]:
            if key not in self._resources:
                self._resources[key] = await factory(**kwargs)
            
            try:
                yield self._resources[key]
            finally:
                if hasattr(self._resources[key], 'close'):
                    await self._resources[key].close()
                del self._resources[key]
                
    async def cleanup(self):
        """Clean up all resources."""
        for key, resource in self._resources.items():
            if hasattr(resource, 'close'):
                await resource.close()
        self._resources.clear() 