"""Base implementation for LLM clients."""
from typing import Dict, List, Optional, Any, Generic, TypeVar
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from contextlib import contextmanager
import asyncio

from .types import Message, Conversation, ModelInfo
from .metrics import TokenUsage, CostEstimate, Budget
from .cache import BaseCache, MemoryCache, CacheEntry, generate_cache_key
from .rate_limit import RateLimit, RateLimiter
from .retry import RetryConfig, retry_async
from ..core.config import Config

T = TypeVar('T')

@dataclass
class LLMConfig:
    """Configuration for LLM client."""
    api_key: str
    cache: Optional[BaseCache] = None
    rate_limit: Optional[RateLimit] = None
    retry_config: Optional[RetryConfig] = None
    budget: Optional[Budget] = None

class BaseLLM(ABC):
    """Base class for LLM implementations."""

    def __init__(
        self, 
        config: Optional[Config] = None,
        llm_config: Optional[LLMConfig] = None,
        conversation: Optional[Conversation] = None
    ):
        self.config = config or Config()
        self.conversation = conversation or Conversation()
        self._initialize(llm_config)

    def _initialize(self, llm_config: Optional[LLMConfig] = None) -> None:
        """Initialize LLM-specific configurations."""
        if llm_config:
            self.api_key = llm_config.api_key
            self.cache = llm_config.cache or MemoryCache()
            self.rate_limiter = (
                RateLimiter(llm_config.rate_limit)
                if llm_config.rate_limit
                else None
            )
            self.retry_config = llm_config.retry_config or RetryConfig()
            self.budget = llm_config.budget
        else:
            self.api_key = self.config.get("LLM_API_KEY")
            self.cache = MemoryCache()
            self.rate_limiter = None
            self.retry_config = RetryConfig()
            self.budget = None

        if not self.api_key:
            raise LLMException("API key not configured")

    async def _handle_request(
        self,
        cache_key: str,
        request_func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Handle a request with caching, rate limiting, and retries."""
        # Check cache
        if cached := self.cache.get(cache_key):
            if not cached.is_expired():
                return cached.content
        
        # Apply rate limiting if configured
        if self.rate_limiter:
            await self.rate_limiter.acquire()
        
        # Make request with retries
        @retry_async(config=self.retry_config)
        async def _make_request():
            return await request_func(*args, **kwargs)
        
        result = await _make_request()
        
        # Cache result
        self.cache.set(
            cache_key,
            CacheEntry(
                content=result.content,
                metadata=result.metadata,
                created_at=datetime.now()
            )
        )
        
        return result

    # ... resto do código permanece igual ... 