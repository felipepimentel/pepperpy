"""Cache manager implementation"""

from datetime import datetime, timedelta
from typing import Any, Optional

from ..base.module import BaseModule
from ..utils.datetime import utc_now
from .base import CacheConfig, CacheEntry


class CacheManager(BaseModule[CacheConfig]):
    """Cache manager implementation"""

    def __init__(self, config: Optional[CacheConfig] = None) -> None:
        super().__init__(config or CacheConfig())
        self._cache: dict[str, CacheEntry] = {}
        self._last_cleanup: Optional[datetime] = None

    async def _initialize(self) -> None:
        """Initialize cache manager"""
        self._last_cleanup = utc_now()
        self._cache.clear()

    async def _cleanup(self) -> None:
        """Cleanup expired entries"""
        now = utc_now()
        expired_keys = [
            key for key, entry in self._cache.items() if entry.expires_at and entry.expires_at < now
        ]
        for key in expired_keys:
            del self._cache[key]
        self._last_cleanup = now

    async def get(self, key: str) -> Optional[Any]:
        """Get cache value"""
        self._ensure_initialized()
        entry = self._cache.get(key)
        if not entry:
            return None

        # Se a entrada estiver expirada, remova-a e retorne None
        if entry.expires_at and entry.expires_at < utc_now():
            del self._cache[key]
            return None

        return entry

    async def set(self, key: str, value: Any, ttl: Optional[int] = None, **metadata: Any) -> None:
        """Set cache value"""
        self._ensure_initialized()

        if isinstance(value, CacheEntry):
            self._cache[key] = value
            return

        # Calcular expiração
        expires_at = None
        if ttl is not None:
            expires_at = utc_now() + timedelta(seconds=ttl)
        elif self.config.default_ttl:
            expires_at = utc_now() + timedelta(seconds=self.config.default_ttl)

        # Criar entrada
        entry = CacheEntry(key=key, value=value, expires_at=expires_at, metadata=metadata)

        # Verificar limite de tamanho do cache
        if (
            self.config.max_size
            and len(self._cache) >= self.config.max_size
            and key not in self._cache
        ):
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k].created_at)
            del self._cache[oldest_key]

        self._cache[key] = entry

    async def delete(self, key: str) -> None:
        """Delete cache value"""
        self._ensure_initialized()
        self._cache.pop(key, None)

    async def clear(self) -> None:
        """Clear all cache entries"""
        self._ensure_initialized()
        self._cache.clear()
