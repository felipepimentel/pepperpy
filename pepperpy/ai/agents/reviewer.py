"""Reviewer agent implementation"""

from typing import Any

from pepperpy.ai.types import AIResponse
from pepperpy.core.exceptions import PepperPyError

from .base import BaseAgent


class ReviewerAgent(BaseAgent):
    """Agent responsible for code review and quality assessment"""

    async def review(self, code: str, **kwargs: Any) -> AIResponse:
        """Review code and provide feedback.

        Args:
            code: Code to review
            **kwargs: Additional arguments for review customization

        Returns:
            AIResponse: Review results

        Raises:
            PepperPyError: If review fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()

        prompt = (
            f"As a code reviewer with the role of {self.config.role}, "
            f"please review this code:\n\n{code}\n\n"
            "Focus on:\n"
            "- Code quality\n"
            "- Best practices\n"
            "- Potential issues\n"
            "- Security concerns\n"
            "- Performance implications"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Code review failed: {e}", cause=e)

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute a code review task.

        Args:
            task: Code to review
            **kwargs: Additional arguments for task execution

        Returns:
            AIResponse: Review results

        Raises:
            PepperPyError: If execution fails
            RuntimeError: If agent is not initialized
        """
        return await self.review(task, **kwargs)
