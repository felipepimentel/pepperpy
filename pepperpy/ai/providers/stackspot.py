"""Stackspot AI provider implementation"""

from typing import Any, AsyncGenerator

import aiohttp

from ..config.provider import ProviderConfig
from ..exceptions import AIError
from ..types import AIMessage, AIResponse, MessageRole
from .base import AIProvider


class StackspotProvider(AIProvider):
    """Stackspot provider implementation"""

    def __init__(self, config: ProviderConfig) -> None:
        super().__init__(config)
        self._session: aiohttp.ClientSession | None = None
        self._base_url = "https://api.stackspot.com/v1"

    async def _initialize(self) -> None:
        """Initialize provider"""
        try:
            self._session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json",
                }
            )
        except Exception as e:
            raise AIError(f"Failed to initialize Stackspot provider: {e}", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup provider resources"""
        if self._session:
            await self._session.close()
        self._session = None

    async def complete(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Complete text"""
        self._ensure_initialized()
        if not self._session:
            raise AIError("Session not initialized")

        try:
            messages = [AIMessage(role=MessageRole.USER, content=prompt)]

            async with self._session.post(
                f"{self._base_url}/completions",
                json={
                    "model": self.config.model,
                    "messages": [{"role": m.role.value, "content": m.content} for m in messages],
                    "temperature": self.config.temperature,
                    "max_tokens": self.config.max_tokens,
                    **self.config.provider_options,
                },
                timeout=aiohttp.ClientTimeout(total=self.config.timeout),
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise AIError(f"Stackspot API error: {error_text}")

                data = await response.json()
                assistant_message = data["choices"][0]["message"]
                messages.append(
                    AIMessage(
                        role=MessageRole.ASSISTANT,
                        content=assistant_message["content"],
                    )
                )

                return AIResponse(
                    content=assistant_message["content"],
                    messages=messages,
                    metadata={
                        "provider": "stackspot",
                        "model": self.config.model,
                        "response_id": data.get("id"),
                    },
                )

        except Exception as e:
            raise AIError(f"Stackspot completion failed: {e}", cause=e)

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[AIResponse, None]:
        """Stream text generation"""
        self._ensure_initialized()
        if not self._session:
            raise AIError("Session not initialized")

        try:
            messages = [AIMessage(role=MessageRole.USER, content=prompt)]

            async with self._session.post(
                f"{self._base_url}/completions/stream",
                json={
                    "model": self.config.model,
                    "messages": [{"role": m.role.value, "content": m.content} for m in messages],
                    "temperature": self.config.temperature,
                    "max_tokens": self.config.max_tokens,
                    **self.config.provider_options,
                },
                timeout=aiohttp.ClientTimeout(total=self.config.timeout),
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise AIError(f"Stackspot API error: {error_text}")

                current_content = ""
                async for line in response.content:
                    if line:
                        chunk = line.decode().strip()
                        if chunk:
                            current_content += chunk
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
                                    "provider": "stackspot",
                                    "model": self.config.model,
                                    "streaming": True,
                                },
                            )

        except Exception as e:
            raise AIError(f"Stackspot streaming failed: {e}", cause=e)

    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding"""
        self._ensure_initialized()
        if not self._session:
            raise AIError("Session not initialized")

        try:
            async with self._session.post(
                f"{self._base_url}/embeddings",
                json={
                    "input": text,
                    "model": "stackspot-embedding-v1",
                    **self.config.provider_options,
                },
                timeout=aiohttp.ClientTimeout(total=self.config.timeout),
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise AIError(f"Stackspot API error: {error_text}")

                data = await response.json()
                return data["data"][0]["embedding"]

        except Exception as e:
            raise AIError(f"Stackspot embedding failed: {e}", cause=e)
