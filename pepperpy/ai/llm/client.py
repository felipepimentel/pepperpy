"""LLM client implementation"""

from typing import AsyncIterator, List, Optional

from pepperpy.core.module import BaseModule, ModuleMetadata

from .config import LLMConfig
from .exceptions import LLMError
from .providers import get_provider
from .types import LLMResponse, Message


class LLMClient(BaseModule):
    """Client for language model operations"""

    _provider = None
    _config: Optional[LLMConfig] = None

    def __init__(self, config: Optional[LLMConfig] = None):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="llm",
            version="1.0.0",
            description="Language model operations",
            dependencies=[],
            config=config.dict() if config else {},
        )
        self._provider = None
        self._config = config

    async def _setup(self) -> None:
        """Initialize LLM provider"""
        try:
            self._provider = get_provider(self._config)
            await self._provider.initialize()
        except Exception as e:
            raise LLMError("Failed to initialize LLM provider", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup LLM resources"""
        if self._provider:
            await self._provider.cleanup()

    async def generate(self, messages: List[Message]) -> LLMResponse:
        """Generate response from messages"""
        if not self._provider:
            raise LLMError("LLM provider not initialized")
        return await self._provider.generate(messages)

    async def stream(self, messages: List[Message]) -> AsyncIterator[LLMResponse]:
        """Stream responses from messages"""
        if not self._provider:
            raise LLMError("LLM provider not initialized")
        async for response in await self._provider.stream(messages):
            yield response
