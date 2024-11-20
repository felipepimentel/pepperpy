"""Agent interfaces"""

from typing import Protocol

from ..types import AIResponse


class BaseAgentProtocol(Protocol):
    """Base agent protocol"""

    async def initialize(self) -> None:
        """Initialize agent"""
        ...

    async def cleanup(self) -> None:
        """Cleanup agent resources"""
        ...


class AnalystAgent(BaseAgentProtocol):
    """Analyst agent interface"""

    async def analyze(self, task: str) -> AIResponse:
        """Analyze task"""
        ...


class ResearchAgent(BaseAgentProtocol):
    """Research agent interface"""

    async def research(self, task: str) -> AIResponse:
        """Research implementation"""
        ...


class ReviewerAgent(BaseAgentProtocol):
    """Reviewer agent interface"""

    async def review(self, code: str) -> AIResponse:
        """Review code"""
        ...

    async def suggest(self, code: str) -> AIResponse:
        """Suggest improvements"""
        ...


class ProjectManagerAgent(BaseAgentProtocol):
    """Project manager agent interface"""

    async def plan(self, task: str) -> AIResponse:
        """Plan project tasks"""
        ...


class QAAgent(BaseAgentProtocol):
    """QA agent interface"""

    async def plan_tests(self, task: str) -> AIResponse:
        """Plan test strategy"""
        ...
