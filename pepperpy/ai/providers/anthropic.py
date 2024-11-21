"""Anthropic AI provider implementation"""

import asyncio
from typing import Any, AsyncGenerator

import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config.provider import ProviderConfig
from ..exceptions import AIError
from ..types import AIMessage, AIResponse, MessageRole
from .base import AIProvider


class AnthropicProvider(AIProvider):
    """Anthropic provider implementation"""

    def __init__(self, config: ProviderConfig) -> None:
        super().__init__(config)
        self._client: anthropic.AsyncAnthropic | None = None
        self._semaphore = asyncio.Semaphore(10)  # Rate limiting

    async def _initialize(self) -> None:
        """Initialize provider"""
        try:
            self._client = anthropic.AsyncAnthropic(api_key=self.config.api_key)
        except Exception as e:
            raise AIError(f"Failed to initialize Anthropic provider: {e}", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup provider resources"""
        self._client = None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    async def complete(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Complete text"""
        self._ensure_initialized()
        if not self._client:
            raise AIError("Client not initialized")

        try:
            async with self._semaphore:
                messages = [AIMessage(role=MessageRole.USER, content=prompt)]
                
                response = await self._client.messages.create(
                    model=self.config.model,
                    max_tokens=self.config.max_tokens,
                    messages=[{"role": m.role, "content": m.content} for m in messages],
                    temperature=self.config.temperature,
                    **self.config.provider_options,
                )

                messages.append(
                    AIMessage(
                        role=MessageRole.ASSISTANT,
                        content=response.content[0].text,
                    )
                )

                return AIResponse(
                    content=response.content[0].text,
                    messages=messages,
                    usage=response.usage,
                    metadata={
                        "provider": "anthropic",
                        "model": response.model,
                        "response_id": response.id,
                    },
                )

        except Exception as e:
            raise AIError(f"Anthropic completion failed: {e}", cause=e)

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[AIResponse, None]:
        """Stream text generation"""
        self._ensure_initialized()
        if not self._client:
            raise AIError("Client not initialized")

        try:
            async with self._semaphore:
                messages = [AIMessage(role=MessageRole.USER, content=prompt)]
                
                stream = await self._client.messages.create(
                    model=self.config.model,
                    max_tokens=self.config.max_tokens,
                    messages=[{"role": m.role, "content": m.content} for m in messages],
                    temperature=self.config.temperature,
                    stream=True,
                    **self.config.provider_options,
                )

                current_content = ""
                async for chunk in stream:
                    if chunk.content:
                        current_content += chunk.content[0].text
                        messages.append(
                            AIMessage(
                                role=MessageRole.ASSISTANT,
                                content=current_content,
                            )
                        )
                        yield AIResponse(
                            content=current_content,
                            messages=messages,
                            metadata={
                                "provider": "anthropic",
                                "model": chunk.model,
                                "streaming": True,
                            },
                        )

        except Exception as e:
            raise AIError(f"Anthropic streaming failed: {e}", cause=e)

    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding"""
        self._ensure_initialized()
        if not self._client:
            raise AIError("Client not initialized")

        try:
            async with self._semaphore:
                response = await self._client.embeddings.create(
                    model="claude-2.1",  # Anthropic's embedding model
                    input=text,
                    **self.config.provider_options,
                )
                return response.embeddings[0]

        except Exception as e:
            raise AIError(f"Anthropic embedding failed: {e}", cause=e) 