"""Anthropic provider implementation"""

import os
from typing import Any, AsyncGenerator

from anthropic import Anthropic

from ..config import AIConfig
from ..exceptions import AIError
from ..types import AIResponse
from .base import AIProvider


class AnthropicProvider(AIProvider):
    """Anthropic provider implementation"""

    def __init__(self, config: AIConfig) -> None:
        """Initialize provider"""
        super().__init__(config)
        self._client: Anthropic | None = None

    async def initialize(self) -> None:
        """Initialize provider"""
        try:
            api_key = self.config.api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise AIError("Anthropic API key not configured")
            self._client = Anthropic(api_key=api_key)
        except Exception as e:
            raise AIError(f"Failed to initialize Anthropic provider: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        self._client = None

    async def complete(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Complete text"""
        try:
            if not self._client:
                raise AIError("Anthropic client not initialized")

            message = await self._client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[{"role": "user", "content": prompt}],
                **kwargs,
            )

            return AIResponse(content=message.content[0].text)

        except Exception as e:
            raise AIError(f"Anthropic completion failed: {e}", cause=e)

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[AIResponse, None]:
        """Stream text generation"""
        try:
            if not self._client:
                raise AIError("Anthropic client not initialized")

            stream = await self._client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                **kwargs,
            )

            async for chunk in stream:
                if chunk.type == "content_block_delta":
                    yield AIResponse(content=chunk.delta.text)

        except Exception as e:
            raise AIError(f"Anthropic streaming failed: {e}", cause=e)

    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding"""
        try:
            if not self._client:
                raise AIError("Anthropic client not initialized")

            response = await self._client.embeddings.create(
                model="claude-3-sonnet",
                input=text,
            )
            return response.embeddings[0]

        except Exception as e:
            raise AIError(f"Anthropic embedding failed: {e}", cause=e) 