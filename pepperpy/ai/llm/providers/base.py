"""Base LLM provider implementation"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, List

from ..config import LLMConfig
from ..types import LLMResponse, Message


class BaseLLMProvider(ABC):
    """Base class for LLM providers"""

    def __init__(self, config: LLMConfig):
        self.config = config
        self._client = None

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider"""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        pass

    @abstractmethod
    async def generate(self, messages: List[Message]) -> LLMResponse:
        """Generate response from messages"""
        pass

    @abstractmethod
    async def stream(self, messages: List[Message]) -> AsyncIterator[LLMResponse]:
        """Stream responses from messages"""
        pass
