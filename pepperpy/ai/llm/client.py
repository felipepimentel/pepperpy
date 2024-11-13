"""LLM client implementation"""

from typing import AsyncIterator, List, Optional

from pepperpy.core.module import BaseModule, ModuleMetadata

from .exceptions import LLMError
from .factory import ProviderConfig, ProviderFactory
from .types import LLMResponse, Message


class LLMClient(BaseModule):
    """Client for language model operations"""

    def __init__(self, config: Optional[ProviderConfig] = None) -> None:
        """Initialize LLM client

        Args:
            config: Provider configuration
        """
        super().__init__()
        self._config: Optional[ProviderConfig] = None
        self._provider = None

        # Configurar o módulo
        self.metadata = ModuleMetadata(
            name="llm",
            version="1.0.0",
            description="Language model operations",
            dependencies=[],
            config=config.to_dict() if config else {},
        )

        # Configurar o provider após metadata para evitar problemas de tipagem
        if config:
            self._config = config

    @property
    def config(self) -> Optional[ProviderConfig]:
        """Get provider configuration"""
        return self._config

    async def _setup(self) -> None:
        """Initialize LLM provider"""
        try:
            if not self._config:
                raise LLMError("Configuration is required")

            # Usar o provider type do config para criar o provider
            provider_type = self._config.provider
            self._provider = ProviderFactory.get_provider(provider_type, self._config)
            await self._provider.initialize()
        except Exception as e:
            raise LLMError("Failed to initialize LLM provider", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup LLM resources"""
        if self._provider:
            await self._provider.cleanup()

    async def complete(self, messages: List[Message]) -> LLMResponse:
        """Generate completion from messages

        Args:
            messages: List of messages to process

        Returns:
            LLMResponse: Generated response

        Raises:
            LLMError: If provider is not initialized or completion fails
        """
        if not self._provider:
            raise LLMError("LLM provider not initialized")
        return await self._provider.complete(messages)

    async def stream(self, messages: List[Message]) -> AsyncIterator[LLMResponse]:
        """Stream responses from messages

        Args:
            messages: List of messages to process

        Yields:
            LLMResponse: Generated response chunks

        Raises:
            LLMError: If provider is not initialized or streaming fails
        """
        if not self._provider:
            raise LLMError("LLM provider not initialized")

        stream = await self._provider.stream(messages)
        async for response in stream:
            yield response


# Global client instance
client = LLMClient()
