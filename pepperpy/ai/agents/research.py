"""Research agent implementation"""

from ..types import AIResponse
from .base import BaseAgent
from .interfaces import ResearchAgent as ResearchAgentProtocol


class ResearchAgent(BaseAgent, ResearchAgentProtocol):
    """Research agent implementation"""

    async def research(self, task: str) -> AIResponse:
        """Research implementation"""
        if not self._initialized:
            await self.initialize()

        prompt = (
            f"As a research agent with the role of {self.config.role}, "
            f"please research the following topic:\n\n{task}\n\n"
            "Provide a comprehensive analysis with key findings, "
            "implications, and recommendations."
        )
        return await self.execute(prompt)
