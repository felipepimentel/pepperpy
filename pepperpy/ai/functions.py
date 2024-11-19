"""AI function implementations"""

from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Sequence

from pepperpy.core.module import BaseModule, ModuleMetadata

from .client import AIClient
from .exceptions import AIError
from .types import AIConfig, AIResponse


def create_default_client() -> AIClient:
    """Create default AI client"""
    config = AIConfig(model="default")
    return AIClient(config=config)


@dataclass
class AIFunction(BaseModule):
    """Base AI function implementation"""

    metadata: ModuleMetadata = field(init=False)
    client: AIClient = field(default_factory=create_default_client)

    def __post_init__(self) -> None:
        """Post initialization"""
        self.metadata = ModuleMetadata(
            name=self.__class__.__name__,
            version="1.0.0",
            description="AI function implementation",
        )

    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute function"""
        raise NotImplementedError


@dataclass
class TextCompletion(AIFunction):
    """Text completion function"""

    async def execute(self, prompt: str | Sequence[str]) -> AIResponse:
        """Execute completion"""
        try:
            # Convert sequence to single string if needed
            prompt_str = "\n".join(str(p) for p in prompt) if isinstance(prompt, (list, tuple)) else str(prompt)
            return await self.client.complete(prompt_str)
        except Exception as e:
            raise AIError(f"Completion failed: {e}", cause=e)


@dataclass
class TextGeneration(AIFunction):
    """Text generation function"""

    async def execute(self, prompt: str | Sequence[str]) -> AsyncIterator[AIResponse]:
        """Execute generation"""
        try:
            # Convert sequence to single string if needed
            prompt_str = "\n".join(str(p) for p in prompt) if isinstance(prompt, (list, tuple)) else str(prompt)
            async for response in self.client.stream(prompt_str):
                yield response
        except Exception as e:
            raise AIError(f"Generation failed: {e}", cause=e)
