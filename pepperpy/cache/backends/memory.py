from typing import Any, Optional, Dict, Union, AsyncIterator
from datetime import datetime, timedelta
import time
import asyncio

class MemoryCache:
    """Backend de cache em memória."""
    
    def __init__(self):
        self._data: Dict[str, tuple[Any, Optional[float]]] = {}
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Obtém valor do cache."""
        if not await self.has(key):
            return default
            
        value, expires_at = self._data[key]
        return value
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[Union[int, timedelta]] = None
    ) -> None:
        """Define valor no cache."""
        if ttl is None:
            expires_at = None
        else:
            if isinstance(ttl, timedelta):
                ttl = ttl.total_seconds()
            expires_at = time.time() + ttl
            
        self._data[key] = (value, expires_at)
    
    async def delete(self, key: str) -> None:
        """Remove valor do cache."""
        self._data.pop(key, None)
    
    async def clear(self) -> None:
        """Limpa todo o cache."""
        self._data.clear()
    
    async def has(self, key: str) -> bool:
        """Verifica se chave existe e não expirou."""
        if key not in self._data:
            return False
            
        _, expires_at = self._data[key]
        if expires_at is not None and time.time() > expires_at:
            await self.delete(key)
            return False
            
        return True
    
    async def iter_keys(self, pattern: str = "*") -> AsyncIterator[str]:
        """Itera sobre chaves que correspondem ao padrão."""
        from fnmatch import fnmatch
        for key in self._data.keys():
            if fnmatch(key, pattern):
                yield key
    
    async def _cleanup_loop(self):
        """Loop de limpeza de itens expirados."""
        while True:
            try:
                now = time.time()
                expired = [
                    key for key, (_, expires_at) in self._data.items()
                    if expires_at is not None and expires_at <= now
                ]
                for key in expired:
                    await self.delete(key)
                    
                await asyncio.sleep(60)  # Executa a cada minuto
                
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(60)  # Continua mesmo com erros
    
    def __del__(self):
        """Cancela task de limpeza."""
        self._cleanup_task.cancel() 