"""Middleware system for request/response pipeline."""
from typing import Any, Callable, List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import asyncio
from ..core.config import Config

@dataclass
class Context:
    """Request/response context."""
    request: Any
    response: Any = None
    metadata: dict = None
    error: Exception = None

class MiddlewareInterface(ABC):
    """Base interface for middleware components."""
    
    @abstractmethod
    async def process(self, context: Context, next_middleware: Callable) -> Context:
        """Process the request/response pipeline."""
        pass

class MiddlewareChain:
    """Chain of middleware components."""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._middleware: List[MiddlewareInterface] = []
    
    def use(self, middleware: MiddlewareInterface) -> 'MiddlewareChain':
        """Add middleware to chain."""
        self._middleware.append(middleware)
        return self
    
    async def execute(self, context: Context) -> Context:
        """Execute middleware chain."""
        async def _execute_middleware(index: int) -> Context:
            if index >= len(self._middleware):
                return context
            
            current = self._middleware[index]
            return await current.process(
                context,
                lambda ctx: _execute_middleware(index + 1)
            )
        
        return await _execute_middleware(0)

# Middlewares comuns
class LoggingMiddleware(MiddlewareInterface):
    """Log requests and responses."""
    
    async def process(self, context: Context, next_middleware: Callable) -> Context:
        # Log request
        print(f"Request: {context.request}")
        
        try:
            context = await next_middleware(context)
            # Log response
            print(f"Response: {context.response}")
        except Exception as e:
            # Log error
            print(f"Error: {e}")
            raise
        
        return context

class CacheMiddleware(MiddlewareInterface):
    """Cache responses."""
    
    def __init__(self, ttl: int = 3600):
        self.cache = {}
        self.ttl = ttl
    
    async def process(self, context: Context, next_middleware: Callable) -> Context:
        cache_key = str(context.request)
        
        if cache_key in self.cache:
            context.response = self.cache[cache_key]
            return context
        
        context = await next_middleware(context)
        self.cache[cache_key] = context.response
        return context 