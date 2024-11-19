"""AI client implementation"""

from typing import AsyncIterator

from pepperpy.core.module import BaseModule

from .exceptions import ClientError
from .types import AIConfig, AIResponse


class AIClient(BaseModule):
    """Base AI client"""

    def __init__(self, config: AIConfig) -> None:
        """Initialize client"""
        super().__init__()
        self.config = config

    async def complete(self, prompt: str) -> AIResponse:
        """Complete prompt"""
        try:
            return await self.generate(prompt)
        except Exception as e:
            raise ClientError(f"Completion failed: {e}", cause=e)

    async def generate(self, prompt: str) -> AIResponse:
        """Generate response for prompt"""
        try:
            # Implementar geração real
            return AIResponse(content=f"Echo: {prompt}")
        except Exception as e:
            raise ClientError(f"Generation failed: {e}", cause=e)

    async def stream(self, prompt: str) -> AsyncIterator[AIResponse]:
        """Stream responses for prompt"""
        try:
            # Implementar streaming real
            yield AIResponse(content=f"Echo: {prompt}")
        except Exception as e:
            raise ClientError(f"Streaming failed: {e}", cause=e)
