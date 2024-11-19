"""Base agent implementation"""

from dataclasses import dataclass, field
from typing import Any

from pepperpy.core.module import BaseModule, ModuleMetadata

from ..client import AIClient
from ..exceptions import AIError
from ..types import AIConfig, AIResponse


def create_default_client() -> AIClient:
    """Create default AI client"""
    config = AIConfig(
        model="default",
        temperature=0.7,
        max_tokens=1000,
    )
    return AIClient(config=config)


@dataclass
class BaseAgent(BaseModule):
    """Base agent implementation"""

    metadata: ModuleMetadata = field(init=False)
    client: AIClient = field(default_factory=create_default_client)

    def __post_init__(self) -> None:
        """Post initialization"""
        self.metadata = ModuleMetadata(
            name=self.__class__.__name__,
            version="1.0.0",
            description="AI agent implementation",
        )

    async def execute(self, task: str) -> AIResponse:
        """Execute agent task"""
        try:
            return await self._get_completion(task)
        except Exception as e:
            raise AIError(f"Task execution failed: {e}", cause=e)

    async def _get_completion(self, prompt: str) -> AIResponse:
        """Get completion from AI"""
        try:
            if not self.client:
                raise AIError("AI client not initialized")
            return await self.client.complete(prompt)
        except Exception as e:
            raise AIError(f"Failed to get completion: {e}", cause=e)

    async def _build_messages(self, prompt: str) -> list[dict[str, Any]]:
        """Build messages for completion"""
        return [{"role": "user", "content": prompt}]
