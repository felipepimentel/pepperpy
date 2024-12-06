"""Review agent implementation."""

from typing import Any

from ..ai_types import AIMessage, AIResponse
from .base import BaseAgent
from .types import AgentConfig, AgentRole


class ReviewAgent(BaseAgent):
    """Review agent implementation."""

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
        """Execute review task."""
        self._ensure_initialized()
        return AIResponse(
            content=f"Review task: {task}",
            messages=[AIMessage(role=AgentRole.REVIEWER, content=task)],
        )

    def _ensure_initialized(self) -> None:
        """Ensure agent is initialized."""
        if not self.is_initialized:
            raise RuntimeError("Agent not initialized")

    async def review_code(self, code: str) -> AIResponse:
        """Review code.

        Args:
            code: Code to review

        Returns:
            Review response
        """
        self._ensure_initialized()
        return AIResponse(
            content=f"Code review: {code}",
            messages=[AIMessage(role=AgentRole.REVIEWER, content=code)],
        )

    async def review_documentation(self, docs: str) -> AIResponse:
        """Review documentation.

        Args:
            docs: Documentation to review

        Returns:
            Review response
        """
        self._ensure_initialized()
        return AIResponse(
            content=f"Documentation review: {docs}",
            messages=[AIMessage(role=AgentRole.REVIEWER, content=docs)],
        )
