"""Base team implementation"""

from typing import Any, Sequence

from bko.ai.config.agent import AgentConfig
from bko.core.module import BaseModule

from ..client import AIClient
from ..types import AIResponse
from .config import TeamConfig


class BaseTeam(BaseModule[TeamConfig]):
    """Base team implementation"""

    def __init__(
        self, config: TeamConfig, agent_configs: Sequence[AgentConfig], ai_client: AIClient
    ) -> None:
        """Initialize team"""
        super().__init__(config)
        self.agent_configs = agent_configs
        self._ai_client = ai_client

    async def execute_task(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute team task"""
        self._ensure_initialized()
        raise NotImplementedError
