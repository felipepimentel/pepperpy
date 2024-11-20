"""AI client implementation"""

from typing import Any, AsyncGenerator, Optional, Protocol

from pepperpy.core.module import BaseModule

from .config import AIConfig
from .exceptions import AIError
from .types import AIResponse


class AIProvider(Protocol):
    """AI provider protocol"""

    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        ...

    async def complete(self, prompt: str, **kwargs: Any) -> str:
        """Complete text"""
        ...

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[str, None]:
        """Stream text generation"""
        ...

    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding"""
        ...


class AIClient(BaseModule[AIConfig]):
    """AI client implementation"""

    def __init__(self, config: Optional[AIConfig] = None) -> None:
        """Initialize client"""
        super().__init__(config or AIConfig.get_default())
        self._provider: Optional[AIProvider] = None

    async def _initialize(self) -> None:
        """Initialize client"""
        if self.config.vector_enabled and not self._provider:
            # Initialize vector operations if enabled
            pass

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        if self._provider:
            await self._provider.cleanup()

    async def complete(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Complete text using AI"""
        if not self._initialized:
            await self.initialize()

        try:
            content = await self._provider.complete(prompt, **kwargs) if self._provider else prompt
            return AIResponse(content=content)
        except Exception as e:
            raise AIError(f"Completion failed: {e}", cause=e)

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[str, None]:
        """Stream text generation"""
        if not self._initialized:
            await self.initialize()

        try:
            if self._provider:
                async for chunk in self._provider.stream(prompt, **kwargs):
                    yield chunk
            else:
                yield prompt
        except Exception as e:
            raise AIError(f"Streaming failed: {e}", cause=e)

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
            vectors = await self._provider.get_embedding(text)
            # TODO: Implement similarity search using vectors
            return [{"score": 0.0, "text": "", "vectors": vectors}]
        except Exception as e:
            raise AIError(f"Similarity search failed: {e}", cause=e)

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
