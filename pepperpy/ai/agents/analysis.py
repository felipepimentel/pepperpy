"""Analysis agent implementations"""

from typing import TYPE_CHECKING

from pepperpy.ai.config.agent import AgentConfig
from pepperpy.ai.types import AIResponse

from .base import BaseAgent
from .interfaces import AnalystAgent

if TYPE_CHECKING:
    from pepperpy.ai.client import AIClient


class AnalysisAgent(BaseAgent, AnalystAgent):
    """Analysis agent implementation"""

    def __init__(self, config: AgentConfig, client: "AIClient") -> None:
        super().__init__(config, client)

    async def analyze(self, task: str) -> AIResponse:
        """Analyze task"""
        return await self.execute(task)

    async def evaluate(self, task: str) -> AIResponse:
        """Evaluate analysis results"""
        return await self.execute(f"Evaluate: {task}")


class DataAnalystAgent(BaseAgent, AnalystAgent):
    """Data analysis agent implementation"""

    async def analyze(self, task: str) -> AIResponse:
        """Analyze data"""
        return await self.execute(task)

    async def evaluate(self, task: str) -> AIResponse:
        """Evaluate analysis results"""
        return await self.execute(f"Evaluate: {task}")


class IntegrationAgent(BaseAgent):
    """Integration agent implementation"""

    async def integrate(self, task: str) -> AIResponse:
        """Integrate systems"""
        return await self.execute(task)
