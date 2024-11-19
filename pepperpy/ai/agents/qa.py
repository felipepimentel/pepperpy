"""QA agent implementation"""

from dataclasses import dataclass

from ..exceptions import AIError
from ..types import AIResponse
from .base import BaseAgent


@dataclass
class QAAgent(BaseAgent):
    """Quality assurance agent"""

    async def test(self, task: str) -> AIResponse:
        """Execute testing"""
        try:
            prompt = (
                f"As a QA engineer, test:\n\n"
                f"{task}\n\n"
                "Include:\n"
                "1. Test cases\n"
                "2. Test execution\n"
                "3. Results analysis\n"
                "4. Bug reports\n"
                "5. Recommendations"
            )
            return await self._get_completion(prompt)
        except Exception as e:
            raise AIError(f"Testing failed: {e}", cause=e)

    async def review(self, task: str) -> AIResponse:
        """Review implementation"""
        try:
            prompt = (
                f"As a QA engineer, review:\n\n"
                f"{task}\n\n"
                "Include:\n"
                "1. Quality assessment\n"
                "2. Test coverage\n"
                "3. Performance analysis\n"
                "4. Security review\n"
                "5. Improvement suggestions"
            )
            return await self._get_completion(prompt)
        except Exception as e:
            raise AIError(f"Review failed: {e}", cause=e) 