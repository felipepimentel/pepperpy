"""OpenRouter LLM provider"""

import json
from typing import AsyncIterator, List, Optional, cast

import httpx

from pepperpy.ai.llm.config import OpenRouterConfig
from pepperpy.ai.llm.exceptions import ProviderError
from pepperpy.ai.llm.types import LLMResponse, Message

from .base import BaseLLMProvider


class OpenRouterProvider(BaseLLMProvider[OpenRouterConfig]):
    """OpenRouter LLM provider implementation"""

    def __init__(self, config: Optional[OpenRouterConfig] = None) -> None:
        """Initialize provider with configuration"""
        super().__init__(config)
        self._client: Optional[httpx.AsyncClient] = None

    async def initialize(self) -> None:
        """Initialize provider"""
        try:
            config = cast(OpenRouterConfig, self.config)
            self._client = httpx.AsyncClient(
                base_url=config.base_url,
                headers={
                    "Authorization": f"Bearer {config.api_key}",
                    "HTTP-Referer": config.site_url or "https://github.com/felipepimentel/pepperpy",
                    "X-Title": config.site_name or "PepperPy",
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )

            # Validate connection and available models
            response = await self._client.get("/models")
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            await self.cleanup()
            if e.response.status_code == 401:
                raise ProviderError("Invalid API key or authentication failed", cause=e)
            if e.response.status_code == 404:
                raise ProviderError("Model not found or unavailable", cause=e)
            raise ProviderError(f"Failed to initialize OpenRouter provider: {str(e)}", cause=e)
        except Exception as e:
            await self.cleanup()
            raise ProviderError(f"Unexpected error during initialization: {str(e)}", cause=e)

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
                metadata={
                    "finish_reason": data["choices"][0].get("finish_reason"),
                    "model": data.get("model"),
                    "route": data.get("route"),
                },
            )
        except httpx.HTTPError as e:
            raise ProviderError(f"HTTP error: {str(e)}", cause=e)
        except Exception as e:
            raise ProviderError(f"Failed to complete chat: {str(e)}", cause=e)

    def stream(self, messages: List[Message]) -> AsyncIterator[LLMResponse]:
        """Stream chat completion"""
        if not self._client:
            raise ProviderError("Provider not initialized")

        if not messages:
            raise ValueError("At least one message is required")

        client = self._client

        async def stream_generator() -> AsyncIterator[LLMResponse]:
            try:
                response = await client.post(
                    "/chat/completions",
                    json={
                        "model": self.config.model,
                        "messages": messages,
                        "stream": True,
                    },
                    headers={"Accept": "text/event-stream"},
                )
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

        return stream_generator()
