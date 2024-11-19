"""Architect agent implementation"""

from dataclasses import dataclass

from ..exceptions import AIError
from ..types import AIResponse
from .base import BaseAgent


@dataclass
class ArchitectAgent(BaseAgent):
    """Architecture design agent"""

    async def design(self, task: str) -> AIResponse:
        """Design system architecture"""
        try:
            prompt = (
                f"As a system architect, design:\n\n"
                f"{task}\n\n"
                "Include:\n"
                "1. System overview\n"
                "2. Component design\n"
                "3. Integration patterns\n"
                "4. Scalability considerations\n"
                "5. Security measures"
            )
            return await self._get_completion(prompt)
        except Exception as e:
            raise AIError(f"Architecture design failed: {e}", cause=e) 