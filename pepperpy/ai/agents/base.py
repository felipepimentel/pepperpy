"""Base agent implementation"""

from typing import TYPE_CHECKING, Any

from pepperpy.ai.config.agent import AgentConfig
from pepperpy.core.module import BaseModule

from ..types import AIResponse

if TYPE_CHECKING:
    from ..client import AIClient


class BaseAgent(BaseModule[AgentConfig]):
    """Base agent implementation"""

    def __init__(self, config: AgentConfig, client: "AIClient") -> None:
        """Initialize agent"""
        super().__init__(config)
        self._client = client

    async def _initialize(self) -> None:
        """Initialize agent"""
        if not self._client.is_initialized:
            await self._client.initialize()

    async def _cleanup(self) -> None:
        """Cleanup agent resources"""
        pass

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute agent task"""
        self._ensure_initialized()
        raise NotImplementedError
