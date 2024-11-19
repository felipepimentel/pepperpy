"""Agent interfaces"""

from typing import Protocol

from ..types import AIResponse


class BaseAgent(Protocol):
    """Base agent protocol"""

    async def execute(self, task: str) -> AIResponse:
        """Execute agent task"""
        ...


class ArchitectAgent(Protocol):
    """Architect agent interface"""

    async def execute(self, task: str) -> AIResponse:
        """Execute agent task"""
        ...

    async def design(self, task: str) -> AIResponse:
        """Design implementation"""
        ...


class DeveloperAgent(Protocol):
    """Developer agent interface"""

    async def execute(self, task: str) -> AIResponse:
        """Execute agent task"""
        ...

    async def implement(self, task: str) -> AIResponse:
        """Implementation"""
        ...


class ReviewerAgent(Protocol):
    """Code reviewer agent interface"""

    async def execute(self, task: str) -> AIResponse:
        """Execute agent task"""
        ...

    async def review(self, task: str) -> AIResponse:
        """Review implementation"""
        ...


class QAAgent(Protocol):
    """QA agent interface"""

    async def execute(self, task: str) -> AIResponse:
        """Execute agent task"""
        ...

    async def test(self, task: str) -> AIResponse:
        """Test implementation"""
        ...

    async def review(self, task: str) -> AIResponse:
        """Review implementation"""
        ...


class ResearcherAgent(Protocol):
    """Researcher agent interface"""

    async def execute(self, task: str) -> AIResponse:
        """Execute agent task"""
        ...

    async def research(self, task: str) -> AIResponse:
        """Research implementation"""
        ...


class AnalystAgent(Protocol):
    """Analyst agent interface"""

    async def execute(self, task: str) -> AIResponse:
        """Execute agent task"""
        ...

    async def analyze(self, task: str) -> AIResponse:
        """Analysis implementation"""
        ...


class ProjectManagerAgent(Protocol):
    """Project manager agent interface"""

    async def execute(self, task: str) -> AIResponse:
        """Execute agent task"""
        ...

    async def plan(self, task: str) -> AIResponse:
        """Planning implementation"""
        ...
