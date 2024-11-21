"""OpenRouter AI provider implementation"""

import asyncio
from typing import Any, AsyncGenerator

import aiohttp
from aiohttp import ClientTimeout
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config.provider import ProviderConfig
from ..exceptions import AIError
from ..types import AIMessage, AIResponse, MessageRole
from .base import AIProvider


class OpenRouterProvider(AIProvider):
    """OpenRouter provider implementation"""

    def __init__(self, config: ProviderConfig) -> None:
        super().__init__(config)
        self._session: aiohttp.ClientSession | None = None
        self._base_url = "https://openrouter.ai/api/v1"
        self._semaphore = asyncio.Semaphore(10)  # Rate limiting
        self.api_key = config.api_key  # Use the API key from the configuration

    async def _initialize(self) -> None:
        """Initialize provider"""
        self._session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "https://github.com/felipepimentel/pepperpy",
                "X-Title": "PepperPy Framework",
            }
        )

    async def _cleanup(self) -> None:
        """Cleanup provider resources"""
        if self._session:
            await self._session.close()
            self._session = None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    async def complete(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Complete prompt using OpenRouter"""
        self._ensure_initialized()
        if not self._session:
            raise AIError("Session not initialized")

        payload = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "messages": [{"role": "user", "content": prompt}],
            **self.config.provider_options,
            **kwargs,
        }

        async with self._semaphore:
            async with self._session.post(
                f"{self._base_url}/chat/completions",
                json=payload,
                timeout=ClientTimeout(total=self.config.timeout),
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise AIError(f"OpenRouter API error: {error_text}")

                data = await response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                ai_message = AIMessage(role=MessageRole.ASSISTANT, content=content)
                return AIResponse(content=ai_message.content, messages=[ai_message])

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[AIResponse, None]:
        """Stream completion using OpenRouter"""
        self._ensure_initialized()
        if not self._session:
            raise AIError("Session not initialized")

        session = self._session

        payload = {
            "prompt": prompt,
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "stream": True,
            # Include other parameters if needed
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/your-repo/pepperpy",
            "X-Title": "PepperPy Framework",
        }

        async with self._semaphore:
            async with session.post(
                f"{self._base_url}/completions",
                json=payload,
                headers=headers,
                timeout=ClientTimeout(total=self.config.timeout),
            ) as response:
                response.raise_for_status()
                async for line in response.content:
                    if line:
                        data = line.decode("utf-8")
                        # Process the line to extract the content
                        # This depends on the API's streaming format
                        ai_message = AIMessage(role=MessageRole.ASSISTANT, content=data)
                        yield AIResponse(content=ai_message.content, messages=[ai_message])

    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding"""
        self._ensure_initialized()
        if not self._session:
            raise AIError("Session not initialized")

        try:
            async with self._semaphore:
                async with self._session.post(
                    f"{self._base_url}/embeddings",
                    json={
                        "model": "text-embedding-ada-002",  # OpenRouter supports OpenAI models
                        "input": text,
                        **self.config.provider_options,
                    },
                    timeout=ClientTimeout(total=self.config.timeout),
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise AIError(f"OpenRouter API error: {error_text}")

                    data = await response.json()
                    return data["data"][0]["embedding"]

        except asyncio.TimeoutError as e:
            raise AIError(f"OpenRouter embedding timed out after {self.config.timeout}s", cause=e)
        except Exception as e:
            raise AIError(f"OpenRouter embedding failed: {e}", cause=e)
