"""QA agent implementation."""

from typing import Any

from ..ai_types import AIMessage, AIResponse
from .base import BaseAgent
from .types import AgentConfig, AgentRole


class QAAgent(BaseAgent):
    """QA agent implementation."""

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
        """Execute QA task."""
        self._ensure_initialized()
        return AIResponse(
            content=f"QA task: {task}",
            messages=[AIMessage(role=AgentRole.REVIEWER, content=task)],
        )

    def _ensure_initialized(self) -> None:
        """Ensure agent is initialized."""
        if not self.is_initialized:
            raise RuntimeError("Agent not initialized")
