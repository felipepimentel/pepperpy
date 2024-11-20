"""Reviewer agent implementation"""

from ..types import AIResponse
from .base import BaseAgent
from .interfaces import ReviewerAgent as ReviewerAgentProtocol


class ReviewerAgent(BaseAgent, ReviewerAgentProtocol):
    """Code reviewer agent implementation"""

    async def _initialize(self) -> None:
        """Initialize agent"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        pass

    async def review(self, code: str) -> AIResponse:
        """Review code"""
        prompt = (
            f"As a code reviewer with the role of {self.config.role}, "
            f"please review the following code:\n\n{code}"
        )
        return await self._client.complete(prompt)

    async def suggest(self, code: str) -> AIResponse:
        """Suggest improvements"""
        prompt = (
            f"As a code reviewer with the role of {self.config.role}, "
            f"please suggest improvements for the following code:\n\n{code}"
        )
        return await self._client.complete(prompt)
