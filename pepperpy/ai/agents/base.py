"""Base agent implementation"""

from typing import Any

from pepperpy.core.module import BaseModule

from ..types import AIResponse
from .types import AgentConfig


class BaseAgent(BaseModule[AgentConfig]):
    """Base agent implementation"""

    def __init__(self, client: Any, config: AgentConfig) -> None:
        super().__init__(config)
        self._client = client

    async def execute(self, prompt: str) -> AIResponse:
        """Execute agent task"""
        if not self._initialized:
            await self.initialize()

        response = await self._client.complete(prompt)
        return response
