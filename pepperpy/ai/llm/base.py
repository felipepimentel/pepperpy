from typing import Dict, List, Optional, Any, Generic, TypeVar, Callable, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from contextlib import contextmanager
import asyncio
from datetime import datetime

from .types import Message, Conversation, ModelInfo
from .metrics import TokenUsage, CostEstimate as Cost, Budget
from .cache import BaseCache, MemoryCache, CacheEntry, generate_cache_key
from .rate_limit import RateLimit, RateLimiter
from .retry import RetryConfig, retry_async
from ..core.config import Config

T = TypeVar('T')

class LLMException(Exception):
    """Base exception for LLM-related errors."""
    pass

class BudgetExceededError(LLMException):
    """Raised when budget limits are exceeded."""
    pass

class APIError(LLMException):
    """Raised when API calls fail."""
    pass

@dataclass
class LLMResponse(Generic[T]):
    """Standardized LLM response."""
    content: T
    usage: TokenUsage
    cost: Optional[Cost] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = None

    @property
    def total_tokens(self) -> int:
        """Total tokens used in this response."""
        return self.usage.total_tokens

    @property
    def total_cost(self) -> float:
        """Total cost of this response."""
        return self.cost.total_cost if self.cost else 0.0

@dataclass
class LLMConfig:
    """Configuration for LLM client."""
    api_key: str
    cache: Optional[BaseCache] = None
    rate_limit: Optional[RateLimit] = None
    retry_config: Optional[RetryConfig] = None
    budget: Optional[Budget] = None

@dataclass
class TokenUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass
class Cost:
    prompt_cost: float
    completion_cost: float
    total_cost: float

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

    @property
    @abstractmethod
    def available_models(self) -> Dict[str, ModelInfo]:
        """Available models for this LLM provider."""
        pass

    @contextmanager
    def new_conversation(self) -> Conversation:
        """Create a new conversation context."""
        previous = self.conversation
        self.conversation = Conversation()
        try:
            yield self.conversation
        finally:
            self.conversation = previous

    def __call__(self, prompt: str, **kwargs) -> str:
        """Allow direct calling for simple completions."""
        return self.complete(prompt, **kwargs).content

    @abstractmethod
    async def acomplete(self, prompt: str, **kwargs) -> LLMResponse[str]:
        """Async version of complete."""
        pass

    @abstractmethod
    async def achat(
        self, 
        messages: List[Message], 
        **kwargs
    ) -> LLMResponse[str]:
        """Async version of chat."""
        pass

    def complete(self, prompt: str, **kwargs) -> LLMResponse[str]:
        """Synchronous completion method."""
        return asyncio.run(self.acomplete(prompt, **kwargs))

    def chat(
        self, 
        messages: List[Message], 
        **kwargs
    ) -> LLMResponse[str]:
        """Synchronous chat method."""
        return asyncio.run(self.achat(messages, **kwargs))

    def stream(
        self, 
        prompt: str, 
        callback: Optional[callable] = None, 
        **kwargs
    ) -> LLMResponse[str]:
        """Stream responses with optional callback."""
        raise NotImplementedError(
            f"Streaming not implemented for {self.__class__.__name__}"
        )

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        # Implementação básica (4 caracteres = ~1 token)
        return len(text) // 4
    
    def estimate_cost(self, text: str, model: Optional[str] = None) -> Cost:
        """Estimate cost for text processing."""
        tokens = self.estimate_tokens(text)
        rates = self.get_model_rates(model)
        
        prompt_cost = tokens * rates['prompt']
        completion_cost = tokens * 1.5 * rates['completion']  # Estimativa de resposta
        
        return Cost(
            prompt_cost=prompt_cost,
            completion_cost=completion_cost,
            total_cost=prompt_cost + completion_cost
        )
    
    def get_model_rates(self, model: Optional[str] = None) -> Dict[str, float]:
        """Get token rates for model."""
        # Taxas padrão (pode ser sobrescrito por implementações específicas)
        return {
            'prompt': 0.0001,  # $0.0001 por token
            'completion': 0.0002  # $0.0002 por token
        }
