"""AI function implementations"""

from typing import Any, AsyncGenerator

from .client import AIClient
from .exceptions import AIError
from .types import AIResponse


class TextGeneration:
    """Text generation functions"""

    def __init__(self, client: AIClient) -> None:
        """Initialize text generation"""
        self.client = client

    async def complete(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Generate text completion"""
        try:
            return await self.client.complete(prompt, **kwargs)
        except Exception as e:
            raise AIError(f"Text generation failed: {e}", cause=e)

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[AIResponse, None]:
        """Stream text generation"""
        try:
            async for chunk in self.client.stream(prompt, **kwargs):
                yield chunk
        except Exception as e:
            raise AIError(f"Text generation stream failed: {e}", cause=e)


class TextEmbedding:
    """Text embedding functions"""

    def __init__(self, client: AIClient) -> None:
        """Initialize text embedding"""
        self.client = client

    async def embed(self, text: str) -> list[float]:
        """Get text embedding"""
        try:
            return await self.client.get_embedding(text)
        except Exception as e:
            raise AIError(f"Text embedding failed: {e}", cause=e)