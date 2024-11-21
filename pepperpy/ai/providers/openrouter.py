"""OpenRouter provider implementation"""

import os
from typing import Any, AsyncGenerator

from openai import AsyncOpenAI

from ..config import AIConfig
from ..exceptions import AIError
from ..types import AIResponse
from .base import AIProvider


class OpenRouterProvider(AIProvider):
    """OpenRouter provider implementation"""

    def __init__(self, config: AIConfig) -> None:
        """Initialize provider"""
        super().__init__(config)
        self._client: AsyncOpenAI | None = None

    async def initialize(self) -> None:
        """Initialize provider"""
        try:
            api_key = self.config.api_key or os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise AIError("OpenRouter API key not configured")
            
            self._client = AsyncOpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost:3000"),
                    "X-Title": os.getenv("OPENROUTER_APP_NAME", "PepperPy"),
                }
            )
        except Exception as e:
            raise AIError(f"Failed to initialize OpenRouter provider: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        self._client = None

    async def complete(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Complete text"""
        try:
            if not self._client:
                raise AIError("OpenRouter client not initialized")

            response = await self._client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                **kwargs,
            )
            return AIResponse(content=response.choices[0].message.content)
        except Exception as e:
            raise AIError(f"OpenRouter completion failed: {e}", cause=e)

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[AIResponse, None]:
        """Stream text generation"""
        try:
            if not self._client:
                raise AIError("OpenRouter client not initialized")

            stream = await self._client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                stream=True,
                **kwargs,
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield AIResponse(content=chunk.choices[0].delta.content)

        except Exception as e:
            raise AIError(f"OpenRouter streaming failed: {e}", cause=e)

    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding"""
        try:
            if not self._client:
                raise AIError("OpenRouter client not initialized")

            response = await self._client.embeddings.create(
                model="openai/text-embedding-3-small",
                input=text,
            )
            return response.data[0].embedding

        except Exception as e:
            raise AIError(f"OpenRouter embedding failed: {e}", cause=e)
