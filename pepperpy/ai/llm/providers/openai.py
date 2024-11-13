"""OpenAI LLM provider implementation"""

from typing import AsyncIterator, List, Optional, cast

from openai import AsyncOpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionMessage,
    ChatCompletionMessageParam,
)

from ..config import LLMConfig
from ..exceptions import ProviderError
from ..types import LLMResponse, Message
from .base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider"""

    _client: Optional[AsyncOpenAI]

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._client = None

    def _convert_messages(self, messages: List[Message]) -> List[ChatCompletionMessageParam]:
        """Convert internal messages to OpenAI format"""
        return [
            cast(
                ChatCompletionMessageParam,
                {
                    "role": msg.role,
                    "content": msg.content,
                },
            )
            for msg in messages
        ]

    async def initialize(self) -> None:
        """Initialize OpenAI client"""
        try:
            self._client = AsyncOpenAI(
                api_key=self.config.api_key,
                base_url=self.config.api_base if self.config.api_base else None,
            )
        except Exception as e:
            raise ProviderError("Failed to initialize OpenAI client", cause=e)

    async def cleanup(self) -> None:
        """Cleanup OpenAI resources"""
        if self._client:
            await self._client.close()
        self._client = None

    async def generate(self, messages: List[Message]) -> LLMResponse:
        """Generate response using OpenAI"""
        if not self._client:
            raise ProviderError("OpenAI client not initialized")

        try:
            response: ChatCompletion = await self._client.chat.completions.create(
                model=self.config.model,
                messages=self._convert_messages(messages),
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p,
                frequency_penalty=self.config.frequency_penalty,
                presence_penalty=self.config.presence_penalty,
            )

            message = cast(ChatCompletionMessage, response.choices[0].message)
            usage_info = {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            }

            if response.usage:
                usage_info.update(
                    {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens,
                    }
                )

            return LLMResponse(
                content=message.content or "",
                model=response.model,
                usage=usage_info,
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                    "system_fingerprint": response.system_fingerprint,
                },
            )
        except Exception as e:
            raise ProviderError("Failed to generate response", cause=e)

    async def stream(self, messages: List[Message]) -> AsyncIterator[LLMResponse]:
        """Stream responses using OpenAI"""
        if not self._client:
            raise ProviderError("OpenAI client not initialized")

        try:
            stream = await self._client.chat.completions.create(
                model=self.config.model,
                messages=self._convert_messages(messages),
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p,
                frequency_penalty=self.config.frequency_penalty,
                presence_penalty=self.config.presence_penalty,
                stream=True,
            )

            async for chunk in stream:
                chunk = cast(ChatCompletionChunk, chunk)
                if chunk.choices[0].delta.content:
                    yield LLMResponse(
                        content=chunk.choices[0].delta.content,
                        model=chunk.model,
                        usage={},  # Usage não disponível em chunks
                        metadata={
                            "finish_reason": chunk.choices[0].finish_reason,
                            "system_fingerprint": chunk.system_fingerprint,
                        },
                    )
        except Exception as e:
            raise ProviderError("Failed to stream responses", cause=e)
