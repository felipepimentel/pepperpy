"""QA agent implementation"""

from typing import Any

from bko.ai.types import AIResponse
from bko.core.exceptions import PepperPyError

from .base import BaseAgent


class QAAgent(BaseAgent):
    """Agent responsible for quality assurance and testing"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute QA task"""
        return await self.test_code(task, **kwargs)

    async def test_code(self, code: str, **kwargs: Any) -> AIResponse:
        """Test code with structured prompt"""
        self._ensure_initialized()
        prompt = (
            f"As a QA engineer with the role of {self.config.role}, "
            f"please test this code:\n\n{code}\n\n"
            "Include:\n"
            "- Test cases\n"
            "- Edge cases\n"
            "- Error scenarios\n"
            "- Test coverage"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Testing failed: {e}", cause=e)

    async def plan_tests(self, task: str, **kwargs: Any) -> AIResponse:
        """Plan test strategy for a task"""
        self._ensure_initialized()
        prompt = (
            f"As a QA engineer with the role of {self.config.role}, "
            f"please create a test plan for:\n\n{task}\n\n"
            "Include:\n"
            "- Test strategy\n"
            "- Test scenarios\n"
            "- Test priorities\n"
            "- Test coverage goals\n"
            "- Testing tools and frameworks"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Test planning failed: {e}", cause=e)
