"""Provider types module"""

from enum import Enum
from typing import Any, AsyncGenerator, Dict, Protocol, runtime_checkable

from bko.ai.types import AIResponse


class ProviderType(str, Enum):
    """Provider types"""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OPENROUTER = "openrouter"
    STACKSPOT = "stackspot"


@runtime_checkable
class LLMProvider(Protocol):
    """Protocol for LLM providers"""

    @property
    def is_initialized(self) -> bool:
        """Check if provider is initialized"""
        ...

    async def initialize(self) -> None:
        """Initialize provider"""
        ...

    async def cleanup(self) -> None:
        """Cleanup provider"""
        ...

    async def complete(self, prompt: str, **kwargs: Dict[str, Any]) -> AIResponse:
        """Complete prompt"""
        ...

    async def stream(
        self, prompt: str, **kwargs: Dict[str, Any]
    ) -> AsyncGenerator[AIResponse, None]:
        """Stream responses"""
        ...
