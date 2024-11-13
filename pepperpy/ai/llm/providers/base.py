"""Base LLM provider implementation"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, Generic, List, Optional, TypeVar

from ..config import BaseConfig
from ..types import LLMResponse, Message

T = TypeVar("T", bound=BaseConfig)


class BaseLLMProvider(Generic[T], ABC):
    """Base class for LLM providers"""

    def __init__(self, config: Optional[T] = None) -> None:
        """Initialize provider with configuration"""
        self._config: Optional[T] = config

    @property
    def config(self) -> T:
        """Get provider configuration"""
        if not self._config:
            raise ValueError("Provider configuration is required")
        return self._config

    @config.setter
    def config(self, value: Optional[T]) -> None:
        """Set provider configuration"""
        self._config = value

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider"""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        pass

    @abstractmethod
    async def complete(self, messages: List[Message]) -> LLMResponse:
        """Generate completion from messages"""
        pass

    @abstractmethod
    def stream(self, messages: List[Message]) -> AsyncIterator[LLMResponse]:
        """Stream responses from messages"""
        raise NotImplementedError("Stream method must be implemented by provider")
