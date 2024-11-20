"""Agent interfaces and protocols"""

from typing import Any, Protocol

from ..types import AIResponse


class BaseAgent(Protocol):
    """Base agent protocol"""

    async def initialize(self) -> None:
        """Initialize agent"""
        ...

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute task"""
        ...

    async def cleanup(self) -> None:
        """Cleanup resources"""
        ...


class ArchitectAgent(BaseAgent, Protocol):
    """Architect agent protocol"""

    async def design(self, task: str) -> AIResponse:
        """Design architecture"""
        ...


class DeveloperAgent(BaseAgent, Protocol):
    """Developer agent protocol"""

    async def implement(self, task: str) -> AIResponse:
        """Implement solution"""
        ...


class ReviewerAgent(BaseAgent, Protocol):
    """Reviewer agent protocol"""

    async def review(self, task: str) -> AIResponse:
        """Review code"""
        ...


class QAAgent(BaseAgent, Protocol):
    """QA agent protocol"""

    async def test(self, task: str) -> AIResponse:
        """Test implementation"""
        ...

    async def review(self, task: str) -> AIResponse:
        """Review test results"""
        ...

    async def validate(self, task: str) -> AIResponse:
        """Validate implementation"""
        ...


class ResearchAgent(BaseAgent, Protocol):
    """Research agent interface"""

    async def research(self, task: str) -> AIResponse:
        """Research implementation"""
        ...

    async def analyze(self, task: str) -> AIResponse:
        """Analyze research results"""
        ...


class AnalystAgent(BaseAgent, Protocol):
    """Analyst agent interface"""

    async def analyze(self, task: str) -> AIResponse:
        """Analysis implementation"""
        ...

    async def evaluate(self, task: str) -> AIResponse:
        """Evaluate analysis results"""
        ...


class ProjectManagerAgent(BaseAgent, Protocol):
    """Project manager agent interface"""

    async def plan(self, task: str) -> AIResponse:
        """Planning implementation"""
        ...

    async def coordinate(self, task: str) -> AIResponse:
        """Coordinate team activities"""
        ...
