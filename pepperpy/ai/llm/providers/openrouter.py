"""OpenRouter LLM provider"""

import json
from typing import AsyncIterator, List, Optional

import httpx

from pepperpy.ai.llm.exceptions import ProviderError
from pepperpy.ai.llm.types import LLMConfig, LLMResponse, Message

from .base import BaseLLMProvider


class OpenRouterConfig(LLMConfig):
    """OpenRouter provider configuration"""

    def __init__(
        self,
        api_key: str,
        model: str = "anthropic/claude-3-sonnet",
        base_url: str = "https://openrouter.ai/api/v1",
        site_url: Optional[str] = None,
        site_name: Optional[str] = None,
    ) -> None:
        if not api_key:
            raise ValueError("OpenRouter API key is required")

        super().__init__(provider="openrouter", api_key=api_key, model=model)
        self.base_url = base_url
        self.site_url = site_url
        self.site_name = site_name


class OpenRouterProvider(BaseLLMProvider):
    """OpenRouter LLM provider implementation"""

    def __init__(self, config: Optional[OpenRouterConfig] = None) -> None:
        if not config:
            raise ValueError("OpenRouter configuration is required")

        self.config = config
        self._client: Optional[httpx.AsyncClient] = None

    async def initialize(self) -> None:
        """Initialize provider"""
        self._client = httpx.AsyncClient(
            base_url=self.config.base_url,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "HTTP-Referer": self.config.site_url
                or "https://github.com/felipepimentel/pepperpy",
                "X-Title": self.config.site_name or "PepperPy",
            },
            timeout=30.0,
        )

    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def complete(self, messages: List[Message]) -> LLMResponse:
        """Complete chat messages"""
        if not self._client:
            raise ProviderError("Provider not initialized")

        if not messages:
            raise ValueError("At least one message is required")

        try:
            response = await self._client.post(
                "/chat/completions",
                json={
                    "model": self.config.model,
                    "messages": messages,
                },
            )
            response.raise_for_status()
            data = response.json()

            if not data.get("choices"):
                raise ProviderError("Invalid response from OpenRouter API")

            return LLMResponse(
                content=data["choices"][0]["message"]["content"],
                model=data["model"],
                usage=data.get("usage", {}),
                metadata=data,
            )
        except httpx.HTTPError as e:
            raise ProviderError(f"HTTP error: {str(e)}", cause=e)
        except Exception as e:
            raise ProviderError(f"Failed to complete chat: {str(e)}", cause=e)

    async def stream(self, messages: List[Message]) -> AsyncIterator[LLMResponse]:
        """Stream chat completion"""
        if not self._client:
            raise ProviderError("Provider not initialized")

        if not messages:
            raise ValueError("At least one message is required")

        try:
            async with self._client.stream(
                "POST",
                "/chat/completions",
                json={
                    "model": self.config.model,
                    "messages": messages,
                    "stream": True,
                },
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            if data["choices"][0]["delta"].get("content"):
                                yield LLMResponse(
                                    content=data["choices"][0]["delta"]["content"],
                                    model=data["model"],
                                    usage={},
                                    metadata=data,
                                )
                        except json.JSONDecodeError as e:
                            raise ProviderError(f"Invalid JSON response: {str(e)}", cause=e)
        except httpx.HTTPError as e:
            raise ProviderError(f"HTTP error: {str(e)}", cause=e)
        except Exception as e:
            raise ProviderError(f"Failed to stream chat: {str(e)}", cause=e)
