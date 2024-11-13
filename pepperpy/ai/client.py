"""AI client implementation"""

import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator, Dict, List, Optional, Sequence, cast

from dotenv import load_dotenv

from .chat.types import ChatRole  # Importar o tipo ChatRole
from .exceptions import AIError
from .llm import LLMClient, LLMResponse, Message, OpenRouterConfig

# Carregar variáveis de ambiente automaticamente
load_dotenv()


@dataclass
class AIConfig:
    """Configuration for AI client"""

    api_key: str
    model: str
    site_url: str = "https://github.com/felipepimentel/pepperpy"
    site_name: str = "PepperPy"

    @classmethod
    def from_env(cls) -> "AIConfig":
        """Create configuration from environment variables"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise AIError("OPENROUTER_API_KEY environment variable is required")

        return cls(
            api_key=api_key,
            model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4"),
            site_url=os.getenv("SITE_URL", cls.site_url),
            site_name=os.getenv("SITE_NAME", cls.site_name),
        )

    def to_llm_config(self) -> OpenRouterConfig:
        """Convert to LLM configuration"""
        return OpenRouterConfig(
            api_key=self.api_key,
            model=self.model,
            site_url=self.site_url,
            site_name=self.site_name,
        )


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


class AIClient:
    """High-level AI client interface"""

    def __init__(self, config: Optional[AIConfig] = None):
        """Initialize AI client with optional config. If not provided, will use environment variables."""
        self.config = config or AIConfig.from_env()
        self._client = LLMClient(self.config.to_llm_config())

    @classmethod
    def from_env(cls) -> "AIClient":
        """Create client from environment variables"""
        config = AIConfig.from_env()
        return cls(config)

    async def initialize(self) -> None:
        """Initialize client"""
        await self._client.initialize()

    async def cleanup(self) -> None:
        """Cleanup resources"""
        await self._client.cleanup()

    async def ask(self, question: str, system_prompt: Optional[str] = None) -> str:
        """Simple question-answer interface

        Args:
            question: The question to ask
            system_prompt: Optional system prompt to guide the response

        Returns:
            str: The AI's response
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": question})

        response = await self.complete(messages)
        return response.content

    async def complete(self, messages: Sequence[Dict[str, str]]) -> AIResponse:
        """Complete chat messages

        Args:
            messages: List of messages in the format {"role": str, "content": str}

        Returns:
            AIResponse: The completion response

        Raises:
            AIError: If completion fails
        """
        try:
            # Validar e converter o role para ChatRole
            llm_messages = []
            for msg in messages:
                role = msg["role"]
                if role not in ("system", "user", "assistant"):
                    raise AIError(f"Invalid role: {role}")
                llm_messages.append(
                    Message(
                        role=cast(ChatRole, role),  # Garantir que o tipo está correto
                        content=msg["content"],
                    )
                )

            response = await self._client.complete(llm_messages)
            return AIResponse.from_llm_response(response)
        except Exception as e:
            raise AIError(f"Completion failed: {str(e)}", cause=e)

    async def stream(self, messages: Sequence[Dict[str, str]]) -> AsyncIterator[AIResponse]:
        """Stream chat completions

        Args:
            messages: List of messages in the format {"role": str, "content": str}

        Yields:
            AIResponse: The streamed response chunks

        Raises:
            AIError: If streaming fails
        """
        try:
            # Validar e converter o role para ChatRole
            llm_messages = []
            for msg in messages:
                role = msg["role"]
                if role not in ("system", "user", "assistant"):
                    raise AIError(f"Invalid role: {role}")
                llm_messages.append(
                    Message(
                        role=cast(ChatRole, role),  # Garantir que o tipo está correto
                        content=msg["content"],
                    )
                )

            async for response in self._client.stream(llm_messages):
                yield AIResponse.from_llm_response(response)
        except Exception as e:
            raise AIError(f"Streaming failed: {str(e)}", cause=e)

    @classmethod
    @asynccontextmanager
    async def create(cls) -> AsyncIterator["AIClient"]:
        """Create and initialize client from environment"""
        client = cls.from_env()
        await client.initialize()
        try:
            yield client
        finally:
            await client.cleanup()


# Convenience functions
async def ask(question: str, system_prompt: Optional[str] = None) -> str:
    """Quick way to ask a single question"""
    async with AIClient.create() as client:
        return await client.ask(question, system_prompt)


async def complete(messages: List[Dict[str, str]]) -> AIResponse:
    """Quick way to complete a conversation"""
    async with AIClient.create() as client:
        return await client.complete(messages)


async def stream(messages: List[Dict[str, str]]) -> AsyncIterator[AIResponse]:
    """Quick way to stream a conversation"""
    async with AIClient.create() as client:
        async for response in client.stream(messages):
            yield response
