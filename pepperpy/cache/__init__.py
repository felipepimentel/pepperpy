from typing import Any, Optional, Type, Dict, Union, Callable
from datetime import timedelta
import asyncio
from abc import ABC, abstractmethod
import json
from pathlib import Path
from contextlib import contextmanager

class CacheBackend(ABC):
    """Interface base para backends de cache."""
    
    @abstractmethod
    async def get(self, key: str, default: Any = None) -> Any:
        """Obtém valor do cache."""
        pass
    
    @abstractmethod
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[Union[int, timedelta]] = None
    ) -> None:
        """Define valor no cache."""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> None:
        """Remove valor do cache."""
        pass
    
    @abstractmethod
    async def clear(self) -> None:
        """Limpa todo o cache."""
        pass
    
    @abstractmethod
    async def has(self, key: str) -> bool:
        """Verifica se chave existe no cache."""
        pass

class Cache:
    """Interface unificada de cache com suporte a múltiplos backends."""
    
    def __init__(
        self,
        backend: str = "memory",
        config: Optional[Dict[str, Any]] = None,
        serializer: Optional[Type] = json,
        namespace: Optional[str] = None
    ):
        self._backend = self._get_backend(backend, config or {})
        self._serializer = serializer
        self._namespace = namespace
        self._locks: Dict[str, asyncio.Lock] = {}
    
    def _get_backend(self, name: str, config: Dict[str, Any]) -> CacheBackend:
        """Obtém instância do backend."""
        if name == "memory":
            from .backends.memory import MemoryCache
            return MemoryCache()
        elif name == "redis":
            from .backends.redis import RedisCache
            return RedisCache(**config)
        elif name == "file":
            from .backends.file import FileCache
            return FileCache(Path(config.get("path", ".cache")))
        else:
            raise ValueError(f"Backend '{name}' não suportado")
    
    def _get_key(self, key: str) -> str:
        """Gera chave com namespace."""
        return f"{self._namespace}:{key}" if self._namespace else key
    
    async def get(
        self,
        key: str,
        default: Any = None,
        raw: bool = False
    ) -> Any:
        """Obtém valor do cache."""
        key = self._get_key(key)
        value = await self._backend.get(key, default)
        
        if value is not None and not raw and self._serializer:
            try:
                value = self._serializer.loads(value)
            except Exception:
                return default
                
        return value
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[Union[int, timedelta]] = None,
        raw: bool = False
    ) -> None:
        """Define valor no cache."""
        key = self._get_key(key)
        
        if not raw and self._serializer:
            value = self._serializer.dumps(value)
            
        await self._backend.set(key, value, ttl)
    
    async def delete(self, key: str) -> None:
        """Remove valor do cache."""
        await self._backend.delete(self._get_key(key))
    
    async def clear(self, namespace: Optional[str] = None) -> None:
        """Limpa cache do namespace especificado ou todo o cache."""
        if namespace:
            # Limpa apenas namespace específico
            async for key in self._backend.iter_keys(f"{namespace}:*"):
                await self.delete(key)
        else:
            await self._backend.clear()
    
    @contextmanager
    async def lock(self, key: str, timeout: float = 5.0):
        """Lock para operações atômicas."""
        lock = self._locks.setdefault(key, asyncio.Lock())
        try:
            async with asyncio.timeout(timeout):
                async with lock:
                    yield
        except asyncio.TimeoutError:
            raise TimeoutError(f"Timeout ao aguardar lock para '{key}'")
    
    async def remember(
        self,
        key: str,
        func: Callable,
        ttl: Optional[Union[int, timedelta]] = None,
        **kwargs
    ) -> Any:
        """Obtém valor do cache ou executa função para obtê-lo."""
        value = await self.get(key)
        if value is None:
            async with self.lock(key):
                # Double check após obter lock
                value = await self.get(key)
                if value is None:
                    value = await func(**kwargs)
                    await self.set(key, value, ttl)
        return value