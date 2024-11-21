"""Base AI provider implementation"""

from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator

from pepperpy.core.module import InitializableModule

from ..config.provider import ProviderConfig
from ..types import AIResponse


class AIProvider(InitializableModule, ABC):
    """Base class for AI providers"""

    def __init__(self, config: ProviderConfig) -> None:
        super().__init__()
        self.config = config

    @abstractmethod
    async def complete(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Complete a prompt and return the response"""
        pass

    @abstractmethod
    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[AIResponse, None]:
        """Stream completion of a prompt"""
        pass

    @abstractmethod
    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding"""
        pass 