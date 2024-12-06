"""Reviewer agent implementation."""

from typing import Any

from ..ai_types import AIMessage, AIResponse
from .base import BaseAgent
from .types import AgentConfig, AgentRole


class ReviewerAgent(BaseAgent):
    """Reviewer agent implementation."""

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

    async def review_pr(self, pr_description: str) -> AIResponse:
        """Review pull request.

        Args:
            pr_description: Pull request description

        Returns:
            Review response
        """
        self._ensure_initialized()
        return AIResponse(
            content=f"PR review: {pr_description}",
            messages=[AIMessage(role=AgentRole.REVIEWER, content=pr_description)],
        )

    async def review_design(self, design_doc: str) -> AIResponse:
        """Review design document.

        Args:
            design_doc: Design document to review

        Returns:
            Review response
        """
        self._ensure_initialized()
        return AIResponse(
            content=f"Design review: {design_doc}",
            messages=[AIMessage(role=AgentRole.REVIEWER, content=design_doc)],
        )
