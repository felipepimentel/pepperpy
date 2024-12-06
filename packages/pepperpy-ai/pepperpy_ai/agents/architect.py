"""Architect agent implementation"""

from typing import Any

from ..ai_types import AIMessage, AIResponse
from .base import BaseAgent
from .types import AgentConfig, AgentRole


class ArchitectAgent(BaseAgent):
    """Agent responsible for system architecture design"""

    def __init__(self, config: AgentConfig) -> None:
        """Initialize agent."""
        super().__init__(config)

    async def _setup(self) -> None:
        """Setup agent resources."""
        pass

    async def _teardown(self) -> None:
        """Teardown agent resources."""
        pass

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute architecture task."""
        self._ensure_initialized()
        return AIResponse(
            content=f"Architecture design for: {task}",
            messages=[AIMessage(role=AgentRole.ARCHITECT, content=task)],
        )

    def _ensure_initialized(self) -> None:
        """Ensure agent is initialized."""
        if not self.is_initialized:
            raise RuntimeError("Agent not initialized")
