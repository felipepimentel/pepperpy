"""Base AI provider implementation"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, List

from ..types import LLMResponse, Message


class BaseLLMProvider(ABC):
    """Base class for LLM providers"""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the provider"""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        pass

    @abstractmethod
    async def generate(self, messages: List[Message]) -> LLMResponse:
        """Generate a response from the LLM"""
        pass

    @abstractmethod
    async def stream(self, messages: List[Message]) -> AsyncIterator[LLMResponse]:
        """Stream responses from the LLM"""
        pass
