"""Researcher agent implementation"""

from typing import Any

from pepperpy.ai.types import AIResponse
from pepperpy.core.exceptions import PepperPyError

from .base import BaseAgent


class ResearcherAgent(BaseAgent):
    """Agent responsible for conducting research and gathering information"""

    async def research(self, topic: str, **kwargs: Any) -> AIResponse:
        """Research a given topic.

        Args:
            topic: Topic to research
            **kwargs: Additional arguments for research customization

        Returns:
            AIResponse: Research results

        Raises:
            PepperPyError: If research fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()

        prompt = (
            f"As a technical researcher with the role of {self.config.role}, "
            f"please research:\n\n{topic}\n\n"
            "Include:\n"
            "- Key findings\n"
            "- Best practices\n"
            "- Current trends\n"
            "- Practical examples\n"
            "- References"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Research failed: {e}", cause=e)

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute a research task.

        Args:
            task: Research task description
            **kwargs: Additional arguments for task execution

        Returns:
            AIResponse: Research results

        Raises:
            PepperPyError: If execution fails
            RuntimeError: If agent is not initialized
        """
        return await self.research(task, **kwargs)
