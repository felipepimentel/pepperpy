"""AI client implementation"""

from typing import Any, AsyncGenerator

from pepperpy.core.module import InitializableModule

from .config.provider import ProviderConfig
from .providers.factory import AIProviderFactory
from .types import AIResponse


class AIClient(InitializableModule):
    """AI client implementation"""

    def __init__(self, config: ProviderConfig) -> None:
        """Initialize client"""
        super().__init__()
        self.config = config
        self._provider = AIProviderFactory.create_provider(config)

    async def _initialize(self) -> None:
        """Initialize client"""
        await self._provider.initialize()

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        await self._provider.cleanup()

    async def complete(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Complete prompt using the provider"""
        self._ensure_initialized()
        return await self._provider.complete(prompt, **kwargs)

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[AIResponse, None]:
        """Stream completion using the provider"""
        self._ensure_initialized()
        generator = await self._provider.stream(prompt, **kwargs)
        async for chunk in generator:
            yield chunk

    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding"""
        self._ensure_initialized()
        return await self._provider.get_embedding(text)
