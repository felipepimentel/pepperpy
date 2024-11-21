"""OpenAI provider implementation"""

import os
from typing import Any, AsyncGenerator, TypedDict, cast

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from ..config.provider import ProviderConfig
from ..exceptions import AIError
from ..types import AIMessage, AIResponse, MessageRole
from .base import AIProvider


class ChatMessage(TypedDict):
    """Chat message format"""

    role: str
    content: str


class OpenAIProvider(AIProvider):
    """OpenAI provider implementation"""

    def __init__(self, config: ProviderConfig) -> None:
        """Initialize provider"""
        super().__init__(config)
        self._client: AsyncOpenAI | None = None

    async def _initialize(self) -> None:
        """Initialize provider"""
        try:
            api_key = self.config.api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise AIError("OpenAI API key not configured")
            self._client = AsyncOpenAI(api_key=api_key)
        except Exception as e:
            raise AIError(f"Failed to initialize OpenAI provider: {e}", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup provider resources"""
        self._client = None

    def _convert_messages(self, messages: list[AIMessage]) -> list[ChatCompletionMessageParam]:
        """Convert messages to OpenAI format"""
        converted: list[ChatMessage] = [
            {
                "role": m.role.value,
                "content": m.content,
            }
            for m in messages
        ]
        return cast(list[ChatCompletionMessageParam], converted)

    async def complete(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Complete text"""
        self._ensure_initialized()
        if not self._client:
            raise AIError("OpenAI client not initialized")

        try:
            messages = [AIMessage(role=MessageRole.USER, content=prompt)]

            response = await self._client.chat.completions.create(
                model=self.config.model,
                messages=self._convert_messages(messages),
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                **self.config.provider_options,
            )

            messages.append(
                AIMessage(
                    role=MessageRole.ASSISTANT,
                    content=response.choices[0].message.content or "",
                )
            )

            return AIResponse(
                content=response.choices[0].message.content or "",
                messages=messages,
                metadata={
                    "provider": "openai",
                    "model": self.config.model,
                    "response_id": response.id,
                },
            )

        except Exception as e:
            raise AIError(f"OpenAI completion failed: {e}", cause=e)

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[AIResponse, None]:
        """Stream text generation"""
        self._ensure_initialized()
        if not self._client:
            raise AIError("OpenAI client not initialized")

        try:
            messages = [AIMessage(role=MessageRole.USER, content=prompt)]

            stream = await self._client.chat.completions.create(
                model=self.config.model,
                messages=self._convert_messages(messages),
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                stream=True,
                **self.config.provider_options,
            )

            current_content = ""
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    current_content += chunk.choices[0].delta.content
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
                            "provider": "openai",
                            "model": self.config.model,
                            "streaming": True,
                        },
                    )

        except Exception as e:
            raise AIError(f"OpenAI streaming failed: {e}", cause=e)

    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding"""
        self._ensure_initialized()
        if not self._client:
            raise AIError("OpenAI client not initialized")

        try:
            response = await self._client.embeddings.create(
                model="text-embedding-ada-002",
                input=text,
                **self.config.provider_options,
            )
            return response.data[0].embedding

        except Exception as e:
            raise AIError(f"OpenAI embedding failed: {e}", cause=e)
