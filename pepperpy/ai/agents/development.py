"""Development agent implementation"""

from typing import Any

from ..types import AIResponse
from .base import BaseAgent


class DevelopmentAgent(BaseAgent):
    """Development agent implementation"""

    async def _initialize(self) -> None:
        """Initialize agent"""
        if not self._client.is_initialized:
            await self._client.initialize()

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        pass

    async def implement(self, task: str, **kwargs: Any) -> AIResponse:
        """Implement development task"""
        prompt = (
            f"As a development agent with the role of {self.config.role}, "
            f"please implement:\n\n{task}\n\n"
            "Include:\n"
            "- Code implementation\n"
            "- Tests\n"
            "- Documentation\n"
            "- Error handling"
        )
        return await self._client.complete(prompt)
