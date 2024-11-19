"""AI function implementations"""

from typing import Any, AsyncGenerator

from .client import AIClient
from .exceptions import AIError
from .types import AIResponse


class AIFunction:
    """Base AI function implementation"""

    def __init__(self, client: AIClient) -> None:
        self.client = client

    async def execute(self, *args: Any, **kwargs: Any) -> AIResponse:
        """Execute function"""
        raise NotImplementedError


class TextCompletion(AIFunction):
    """Text completion function"""

    async def execute(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Execute text completion"""
        try:
            return await self.client.complete(prompt)
        except Exception as e:
            raise AIError(f"Text completion failed: {e}", cause=e)


class TextGeneration(AIFunction):
    """Text generation function with streaming support"""

    async def execute(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Execute text generation"""
        try:
            return await self.client.complete(prompt)
        except Exception as e:
            raise AIError(f"Text generation failed: {e}", cause=e)

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[str, None]:
        """Stream text generation results"""
        try:
            async for chunk in self.client.stream(prompt):
                yield chunk
        except Exception as e:
            raise AIError(f"Text generation stream failed: {e}", cause=e)


class TextEmbedding(AIFunction):
    """Text embedding function"""

    async def execute(self, text: str, **kwargs: Any) -> list[float]:
        """Get text embedding"""
        try:
            return await self.client.get_embedding(text)
        except Exception as e:
            raise AIError(f"Text embedding failed: {e}", cause=e)


class VectorSearch(AIFunction):
    """Vector similarity search function"""

    async def execute(
        self, 
        collection: str,
        text: str,
        limit: int = 10,
        threshold: float = 0.8,
        **kwargs: Any
    ) -> list[dict[str, Any]]:
        """Search for similar vectors"""
        try:
            return await self.client.find_similar(
                collection=collection,
                text=text,
                limit=limit,
                threshold=threshold
            )
        except Exception as e:
            raise AIError(f"Vector search failed: {e}", cause=e)
