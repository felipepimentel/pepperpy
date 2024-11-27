"""Anthropic provider implementation"""

from typing import Any, AsyncGenerator, cast

from anthropic import AI_PROMPT, HUMAN_PROMPT, AsyncAnthropic

from ...core.exceptions import PepperPyError
from ..types import AIResponse
from .base import BaseProvider
from .config import ProviderConfig


class AnthropicProvider(BaseProvider):
    """Anthropic provider implementation"""

    def __init__(self, config: ProviderConfig) -> None:
        """Initialize provider.

        Args:
            config: Provider configuration
        """
        super().__init__(config)
        self._client: AsyncAnthropic | None = None

    def _ensure_initialized(self) -> None:
        """Ensure provider is initialized"""
        if not self._initialized:
            raise RuntimeError("Provider is not initialized")

    async def _initialize(self) -> None:
        """Initialize provider resources"""
        try:
            self._client = AsyncAnthropic(api_key=self.config.api_key)
        except Exception as e:
            raise PepperPyError(f"Failed to initialize Anthropic client: {e}", cause=e)

    async def complete(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Complete prompt.

        Args:
            prompt: Prompt to complete
            **kwargs: Additional arguments for completion

        Returns:
            AIResponse: Completion response

        Raises:
            PepperPyError: If completion fails
            RuntimeError: If provider is not initialized
        """
        self._ensure_initialized()
        try:
            client = cast(AsyncAnthropic, self._client)
            completion = await client.completions.create(
                model=self.config.model,
                prompt=f"{HUMAN_PROMPT} {prompt}{AI_PROMPT}",
                max_tokens_to_sample=kwargs.get("max_tokens", 1000),
                temperature=kwargs.get("temperature", 0.7),
                top_p=kwargs.get("top_p", 1.0),
                top_k=kwargs.get("top_k", -1),
            )
            return AIResponse(
                content=completion.completion,
                metadata={"model": self.config.model, "provider": "anthropic", **kwargs},
            )
        except Exception as e:
            raise PepperPyError(f"Failed to complete prompt: {e}", cause=e)

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[AIResponse, None]:
        """Stream completions.

        Args:
            prompt: Prompt to complete
            **kwargs: Additional arguments for completion

        Yields:
            AIResponse: Completion response chunks

        Raises:
            PepperPyError: If streaming fails
            RuntimeError: If provider is not initialized
        """
        self._ensure_initialized()
        try:
            client = cast(AsyncAnthropic, self._client)
            stream = await client.completions.create(
                model=self.config.model,
                prompt=f"{HUMAN_PROMPT} {prompt}{AI_PROMPT}",
                max_tokens_to_sample=kwargs.get("max_tokens", 1000),
                temperature=kwargs.get("temperature", 0.7),
                top_p=kwargs.get("top_p", 1.0),
                top_k=kwargs.get("top_k", -1),
                stream=True,
            )
            async for completion in stream:
                yield AIResponse(
                    content=completion.completion,
                    metadata={"model": self.config.model, "provider": "anthropic", **kwargs},
                )
        except Exception as e:
            raise PepperPyError(f"Failed to stream completions: {e}", cause=e)

    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding.

        Args:
            text: Text to embed

        Returns:
            list[float]: Text embedding

        Raises:
            PepperPyError: If embedding fails
            RuntimeError: If provider is not initialized
        """
        self._ensure_initialized()
        try:
            # Note: Anthropic doesn't currently support embeddings
            # This is a placeholder for when they do
            raise NotImplementedError("Embeddings not supported by Anthropic")
        except Exception as e:
            raise PepperPyError(f"Failed to get embedding: {e}", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup provider resources"""
        if self._client:
            # No cleanup needed for Anthropic client
            self._client = None
