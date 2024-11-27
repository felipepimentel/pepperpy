"""Development agent implementation"""

from typing import Any

from bko.ai.types import AIResponse
from bko.core.exceptions import PepperPyError

from .base import BaseAgent


class DevelopmentAgent(BaseAgent):
    """Agent responsible for code implementation and development"""

    async def implement(self, task: str, **kwargs: Any) -> AIResponse:
        """Implement development task.

        Args:
            task: Development task description
            **kwargs: Additional arguments for implementation

        Returns:
            AIResponse: Implementation results

        Raises:
            PepperPyError: If implementation fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()
        prompt = (
            f"As a development agent with the role of {self.config.role}, "
            f"please implement:\n\n{task}\n\n"
            "Include:\n"
            "- Code implementation\n"
            "- Tests\n"
            "- Documentation\n"
            "- Error handling"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Implementation failed: {e}", cause=e)

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute a development task.

        Args:
            task: Development task description
            **kwargs: Additional arguments for task execution

        Returns:
            AIResponse: Implementation results

        Raises:
            PepperPyError: If execution fails
            RuntimeError: If agent is not initialized
        """
        return await self.implement(task, **kwargs)
