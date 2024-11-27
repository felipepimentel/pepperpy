"""Review agent implementation"""

from typing import Any

from bko.ai.types import AIResponse
from bko.core.exceptions import PepperPyError

from .base import BaseAgent


class ReviewAgent(BaseAgent):
    """Agent responsible for code review"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute code review task"""
        return await self.review(task, **kwargs)

    async def review(self, code: str, **kwargs: Any) -> AIResponse:
        """Review code for quality and best practices.

        Args:
            code: Code to review
            **kwargs: Additional arguments for review

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
            "- Documentation\n"
            "- Test coverage"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Code review failed: {e}", cause=e)

    async def _initialize(self) -> None:
        """Initialize agent"""
        if not self._client.is_initialized:
            await self._client.initialize()

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        pass
