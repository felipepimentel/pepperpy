"""LLM client implementation"""

from typing import Any, AsyncGenerator

from pepperpy.core.module import BaseModule

from .config import LLMConfig
from .exceptions import LLMError
from .types import LLMResponse


class LLMClient(BaseModule[LLMConfig]):
    """LLM client implementation"""

    def __init__(self, config: LLMConfig) -> None:
        super().__init__(config)
        self._provider = None

    async def _initialize(self) -> None:
        """Initialize LLM client"""
        try:
            # Initialize provider based on config
            self._provider = self._create_provider()
            await self._provider.initialize()
        except Exception as e:
            raise LLMError(f"Failed to initialize LLM client: {e}", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        if self._provider:
            await self._provider.cleanup()
        self._provider = None

    async def complete(self, prompt: str, **kwargs: Any) -> LLMResponse:
        """Complete text using LLM"""
        if not self._initialized:
            await self.initialize()

        try:
            if not self._provider:
                raise LLMError("Provider not initialized")
            return await self._provider.complete(prompt, **kwargs)
        except Exception as e:
            raise LLMError(f"Completion failed: {e}", cause=e)

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[str, None]:
        """Stream text generation"""
        if not self._initialized:
            await self.initialize()

        try:
            if not self._provider:
                raise LLMError("Provider not initialized")
            async for token in self._provider.stream(prompt, **kwargs):
                yield token
        except Exception as e:
            raise LLMError(f"Streaming failed: {e}", cause=e)

    def _create_provider(self) -> Any:
        """Create LLM provider based on config"""
        # Implement provider creation logic here
        raise NotImplementedError
