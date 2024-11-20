"""Team agent implementation"""

from pepperpy.core.module import BaseModule

from ..client import AIClient
from .base import BaseAgent
from .types import AgentConfig


class AgentTeam(BaseModule[AgentConfig]):
    """Team of agents working together"""

    def __init__(self, config: AgentConfig, ai_client: AIClient) -> None:
        super().__init__(config)
        self._client = ai_client
        self._agents: dict[str, BaseAgent] = {}

    async def _initialize(self) -> None:
        """Initialize team"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        for agent in self._agents.values():
            await agent.cleanup()
