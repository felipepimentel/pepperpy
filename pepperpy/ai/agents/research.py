"""Research agent implementation"""

from typing import Any

from ..client import AIClient
from ..types import AIResponse
from .base import BaseAgent
from .interfaces import ResearchAgent as ResearchAgentProtocol
from .types import AgentConfig


class ResearchAgent(BaseAgent, ResearchAgentProtocol):
    """Research agent implementation"""

    def __init__(self, client: AIClient, config: AgentConfig, **kwargs: Any) -> None:
        """Initialize research agent.
        
        Args:
            client: AI client instance
            config: Agent configuration
            **kwargs: Additional arguments
        """
        super().__init__(client=client, config=config, **kwargs)

    async def research(self, task: str) -> AIResponse:
        """Research implementation.
        
        Args:
            task: Research task
            
        Returns:
            AIResponse: Research results
        """
        if not self._initialized:
            await self.initialize()

        prompt = (
            f"As a research agent with the role of {self.config.role}, "
            f"please research the following task:\n\n{task}"
        )
        return await self.client.complete(prompt)

    async def analyze(self, task: str) -> AIResponse:
        """Analyze research results.
        
        Args:
            task: Analysis task
            
        Returns:
            AIResponse: Analysis results
        """
        if not self._initialized:
            await self.initialize()

        prompt = (
            f"As a research agent with the role of {self.config.role}, "
            f"please analyze the following research task:\n\n{task}"
        )
        return await self.client.complete(prompt) 