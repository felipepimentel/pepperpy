"""Development agent implementation"""

from dataclasses import dataclass

from ..exceptions import AIError
from ..types import AIResponse
from .base import BaseAgent


@dataclass
class DevelopmentAgent(BaseAgent):
    """Development agent implementation"""

    async def implement(self, task: str) -> AIResponse:
        """Implement solution"""
        try:
            prompt = (
                f"As a developer, implement:\n\n"
                f"{task}\n\n"
                "Include:\n"
                "1. Implementation details\n"
                "2. Code structure\n"
                "3. Error handling\n"
                "4. Performance considerations\n"
                "5. Testing approach"
            )
            return await self._get_completion(prompt)
        except Exception as e:
            raise AIError(f"Implementation failed: {e}", cause=e)
