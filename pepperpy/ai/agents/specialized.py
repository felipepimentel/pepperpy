"""Specialized agent implementations"""

from dataclasses import dataclass

from ..exceptions import AIError
from ..types import AIResponse
from .base import BaseAgent


@dataclass
class CodeReviewAgent(BaseAgent):
    """Code review agent implementation"""

    async def review(self, code: str) -> AIResponse:
        """Review code"""
        try:
            prompt = f"Review the following code:\n\n{code}"
            return await self._get_completion(prompt)
        except Exception as e:
            raise AIError(f"Code review failed: {e}", cause=e)


@dataclass
class DocumentationAgent(BaseAgent):
    """Documentation agent implementation"""

    async def document(self, code: str) -> AIResponse:
        """Document code"""
        try:
            prompt = f"Document the following code:\n\n{code}"
            return await self._get_completion(prompt)
        except Exception as e:
            raise AIError(f"Documentation failed: {e}", cause=e)


@dataclass
class TestingAgent(BaseAgent):
    """Testing agent implementation"""

    async def test(self, code: str) -> AIResponse:
        """Generate tests"""
        try:
            prompt = f"Generate tests for:\n\n{code}"
            return await self._get_completion(prompt)
        except Exception as e:
            raise AIError(f"Test generation failed: {e}", cause=e)


@dataclass
class OptimizationAgent(BaseAgent):
    """Optimization agent implementation"""

    async def optimize(self, code: str) -> AIResponse:
        """Optimize code"""
        try:
            prompt = f"Optimize the following code:\n\n{code}"
            return await self._get_completion(prompt)
        except Exception as e:
            raise AIError(f"Optimization failed: {e}", cause=e)


@dataclass
class SecurityAgent(BaseAgent):
    """Security agent implementation"""

    async def audit(self, code: str) -> AIResponse:
        """Audit code security"""
        try:
            prompt = f"Audit security of:\n\n{code}"
            return await self._get_completion(prompt)
        except Exception as e:
            raise AIError(f"Security audit failed: {e}", cause=e)
