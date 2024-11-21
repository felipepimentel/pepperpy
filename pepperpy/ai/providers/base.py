"""Base AI provider implementation"""

from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator

from ..config import AIConfig
from ..types import AIResponse


class AIProvider(ABC):
    """Base class for AI providers"""

    def __init__(self, config: AIConfig) -> None:
        """Initialize provider with configuration"""
        self.config = config

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider"""
        ...

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        ...

    @abstractmethod
    async def complete(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Complete text"""
        ...

    @abstractmethod
    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[AIResponse, None]:
        """Stream text generation"""
        ...

    @abstractmethod
    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding"""
        ... 