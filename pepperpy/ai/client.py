"""AI client implementation"""

from typing import Any, AsyncGenerator, Optional

from pepperpy.core.module import BaseModule

from .config import AIConfig
from .exceptions import AIError
from .providers.factory import AIProviderFactory
from .types import AIResponse


class AIClient(BaseModule[AIConfig]):
    """AI client implementation"""

    def __init__(self, config: Optional[AIConfig] = None) -> None:
        """Initialize client"""
        super().__init__(config or AIConfig.get_default())
        self._provider = None

    async def _initialize(self) -> None:
        """Initialize client"""
        try:
            self._provider = AIProviderFactory.create_provider(self.config)
            await self._provider.initialize()
        except Exception as e:
            raise AIError(f"Failed to initialize AI client: {e}", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        if self._provider:
            await self._provider.cleanup()
        self._provider = None

    async def complete(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Complete text using AI"""
        if not self._initialized:
            await self.initialize()

        try:
            if not self._provider:
                raise AIError("Provider not initialized")
            return await self._provider.complete(prompt, **kwargs)
        except Exception as e:
            raise AIError(f"Completion failed: {e}", cause=e)

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[AIResponse, None]:
        """Stream text generation"""
        if not self._initialized:
            await self.initialize()

        try:
            if not self._provider:
                raise AIError("Provider not initialized")
            async for response in self._provider.stream(prompt, **kwargs):
                yield response
        except Exception as e:
            raise AIError(f"Streaming failed: {e}", cause=e)

    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding"""
        if not self._initialized:
            await self.initialize()

        try:
            if not self._provider:
                raise AIError("Provider not initialized")
            return await self._provider.get_embedding(text)
        except Exception as e:
            raise AIError(f"Embedding failed: {e}", cause=e)

    async def find_similar(
        self,
        collection: str,
        text: str,
        limit: int = 10,
        threshold: float = 0.8,
    ) -> list[dict[str, Any]]:
        """Find similar texts"""
        if not self._initialized:
            await self.initialize()

        try:
            if not self._provider:
                raise AIError("Provider not initialized")

            if not self.config.vector_enabled:
                return []

            # Get embedding for query text and search in vector store
            # TODO: Implement vector search using configured vector store
            _ = await self.get_embedding(text)
            return []

        except Exception as e:
            raise AIError(f"Similarity search failed: {e}", cause=e)
