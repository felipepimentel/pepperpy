"""Researcher agent implementation"""

from dataclasses import dataclass

from ..exceptions import AIError
from ..types import AIResponse
from .base import BaseAgent


@dataclass
class ResearcherAgent(BaseAgent):
    """Research agent implementation"""

    async def research(self, task: str) -> AIResponse:
        """Research a topic"""
        try:
            prompt = (
                f"Research the following topic:\n\n"
                f"{task}\n\n"
                "Include:\n"
                "1. Overview\n"
                "2. Key concepts\n"
                "3. Best practices\n"
                "4. Common challenges\n"
                "5. Recommendations"
            )
            return await self._get_completion(prompt)
        except Exception as e:
            raise AIError(f"Research failed: {e}", cause=e)

    async def analyze(self, content: str) -> AIResponse:
        """Analyze research content"""
        try:
            prompt = f"Analyze the following research:\n\n{content}"
            return await self._get_completion(prompt)
        except Exception as e:
            raise AIError(f"Analysis failed: {e}", cause=e)

    async def summarize(self, content: str) -> AIResponse:
        """Summarize research content"""
        try:
            prompt = f"Summarize the following research:\n\n{content}"
            return await self._get_completion(prompt)
        except Exception as e:
            raise AIError(f"Summarization failed: {e}", cause=e)
