"""AI module for PepperPy"""

from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator, Dict, List, Literal, Optional, Sequence, TypedDict, cast

from .exceptions import AIError
from .llm import LLMClient, LLMResponse, OpenRouterConfig
from .llm.types import Message


class ChatMessage(TypedDict):
    """Chat message format for API input"""

    role: Literal["system", "user", "assistant"]
    content: str


@dataclass
class AIResponse:
    """AI response data"""

    content: str
    model: str
    usage: Dict[str, int]
    metadata: Optional[Dict[str, str]] = None

    @classmethod
    def from_llm_response(cls, response: LLMResponse) -> "AIResponse":
        """Convert LLM response to AI response"""
        return cls(
            content=response.content,
            model=response.model,
            usage=response.usage or {},
            metadata=response.metadata,
        )


@dataclass
class AIConfig:
    """Configuration for AI client"""

    api_key: str
    model: str
    site_url: str
    site_name: str

    def to_llm_config(self) -> OpenRouterConfig:
        """Convert to LLM configuration"""
        return OpenRouterConfig(
            api_key=self.api_key, model=self.model, site_url=self.site_url, site_name=self.site_name
        )


class AIClient:
    """High-level AI client interface"""

    def __init__(self, config: AIConfig):
        self.config = config
        self._client = LLMClient(config.to_llm_config())

    async def initialize(self) -> None:
        """Initialize client"""
        await self._client.initialize()

    async def cleanup(self) -> None:
        """Cleanup resources"""
        await self._client.cleanup()

    async def complete(self, messages: List[Dict[str, str]]) -> AIResponse:
        """Complete chat messages"""
        try:
            formatted_messages: Sequence[Message] = [
                Message(
                    role=cast(Literal["system", "user", "assistant"], msg["role"]),
                    content=msg["content"],
                )
                for msg in messages
            ]

            response = await self._client.complete(formatted_messages)
            return AIResponse.from_llm_response(response)

        except Exception as e:
            raise AIError(f"Completion failed: {str(e)}", cause=e)

    async def stream(self, messages: List[Dict[str, str]]) -> AsyncIterator[AIResponse]:
        """Stream chat completions"""
        try:
            formatted_messages: Sequence[Message] = [
                Message(
                    role=cast(Literal["system", "user", "assistant"], msg["role"]),
                    content=msg["content"],
                )
                for msg in messages
            ]

            async for response in self._client.stream(formatted_messages):
                yield AIResponse.from_llm_response(response)

        except Exception as e:
            raise AIError(f"Streaming failed: {str(e)}", cause=e)

    @classmethod
    @asynccontextmanager
    async def from_config(cls, config: AIConfig) -> AsyncIterator["AIClient"]:
        """Create and initialize client from config"""
        client = cls(config)
        await client.initialize()
        try:
            yield client
        finally:
            await client.cleanup()


__all__ = ["AIClient", "AIConfig", "AIResponse", "AIError", "Message", "ChatMessage"]
