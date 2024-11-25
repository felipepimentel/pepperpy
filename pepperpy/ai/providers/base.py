"""Base provider module"""

from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict

from pepperpy.ai.providers.config import ProviderConfig
from pepperpy.ai.providers.types import AIResponse


class AIProvider(ABC):
    """Base class for AI providers"""

    def __init__(self, config: ProviderConfig) -> None:
        """Initialize provider"""
        self._config = config
        self._initialized = False

    @property
    def config(self) -> ProviderConfig:
        """Get provider configuration"""
        return self._config

    @property
    def is_initialized(self) -> bool:
        """Check if provider is initialized"""
        return self._initialized

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider"""
        raise NotImplementedError

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup provider"""
        raise NotImplementedError

    @abstractmethod
    async def complete(self, prompt: str, **kwargs: Dict[str, Any]) -> AIResponse:
        """Complete prompt"""
        raise NotImplementedError

    @abstractmethod
    async def stream(
        self, prompt: str, **kwargs: Dict[str, Any]
    ) -> AsyncGenerator[AIResponse, None]:
        """Stream responses"""
        raise NotImplementedError


BaseProvider = AIProvider  # Alias para compatibilidade
