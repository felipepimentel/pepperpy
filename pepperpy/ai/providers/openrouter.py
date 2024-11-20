"""OpenRouter provider implementation"""

from typing import Any, AsyncGenerator

import httpx

from ..llm.config import LLMConfig, LLMProvider
from .exceptions import ProviderError
from .types import ProviderResponse


class OpenRouterProvider:
    """OpenRouter provider implementation"""

    def __init__(self, config: LLMConfig) -> None:
        """Initialize provider"""
        if config.provider != LLMProvider.OPENROUTER:
            raise ProviderError("Invalid provider configuration")
        self.config = config
        self._client: httpx.AsyncClient | None = None

    async def initialize(self) -> None:
        """Initialize provider"""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "HTTP-Referer": self.config.metadata.get("site_url", "https://github.com/pimentel/pepperpy"),
            "X-Title": self.config.metadata.get("site_name", "PepperPy"),
        }
        self._client = httpx.AsyncClient(
            base_url=self.config.api_base or "https://openrouter.ai/api/v1",
            headers=headers,
            timeout=self.config.timeout,
        )

    async def cleanup(self) -> None:
        """Cleanup resources"""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def complete(self, prompt: str, **kwargs: Any) -> ProviderResponse:
        """Complete text using OpenRouter"""
        if not self._client:
            raise ProviderError("Provider not initialized")

        try:
            data = {
                "model": self.config.model,
                "messages": [{"role": "user", "content": prompt}],
                **kwargs,
            }
            response = await self._client.post("/chat/completions", json=data)
            response.raise_for_status()
            result = response.json()

            return ProviderResponse(
                content=result["choices"][0]["message"]["content"],
                model=self.config.model,
            )
        except Exception as e:
            raise ProviderError(f"OpenRouter completion failed: {e}", cause=e)

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[str, None]:
        """Stream text generation"""
        if not self._client:
            raise ProviderError("Provider not initialized")

        try:
            data = {
                "model": self.config.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True,
                **kwargs,
            }
            async with self._client.stream(
                "POST", "/chat/completions", json=data
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        chunk = line[6:].strip()
                        if chunk == "[DONE]":
                            break
                        yield chunk
        except Exception as e:
            raise ProviderError(f"OpenRouter streaming failed: {e}", cause=e)
