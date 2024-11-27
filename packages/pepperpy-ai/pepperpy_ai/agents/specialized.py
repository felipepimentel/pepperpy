"""Specialized agent implementations"""

from typing import Any

from bko.ai.types import AIResponse
from bko.core.exceptions import PepperPyError

from .base import BaseAgent


class CodeReviewAgent(BaseAgent):
    """Agent responsible for code review"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute code review task"""
        return await self.review_code(task, **kwargs)

    async def review_code(self, code: str, **kwargs: Any) -> AIResponse:
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
            "- Suggested improvements"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Code review failed: {e}", cause=e)


class DocumentationAgent(BaseAgent):
    """Agent responsible for code documentation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute documentation task"""
        return await self.generate_docs(task, **kwargs)

    async def generate_docs(self, code: str, **kwargs: Any) -> AIResponse:
        """Generate documentation for code.

        Args:
            code: Code to document
            **kwargs: Additional arguments for documentation

        Returns:
            AIResponse: Documentation

        Raises:
            PepperPyError: If documentation fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()
        prompt = (
            f"As a documentation specialist with the role of {self.config.role}, "
            f"please document this code:\n\n{code}\n\n"
            "Include:\n"
            "- Overview\n"
            "- Usage examples\n"
            "- API documentation\n"
            "- Implementation details"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Documentation generation failed: {e}", cause=e)


class AutomatedTestingAgent(BaseAgent):
    """Agent responsible for test creation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute testing task"""
        return await self.create_tests(task, **kwargs)

    async def create_tests(self, code: str, **kwargs: Any) -> AIResponse:
        """Create test cases for code.

        Args:
            code: Code to test
            **kwargs: Additional arguments for test creation

        Returns:
            AIResponse: Test cases

        Raises:
            PepperPyError: If test creation fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()
        prompt = (
            f"As a testing specialist with the role of {self.config.role}, "
            f"please create tests for this code:\n\n{code}\n\n"
            "Include:\n"
            "- Unit tests\n"
            "- Integration tests\n"
            "- Edge cases\n"
            "- Test scenarios"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Test creation failed: {e}", cause=e)


class OptimizationAgent(BaseAgent):
    """Agent responsible for code optimization"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute optimization task"""
        return await self.optimize_code(task, **kwargs)

    async def optimize_code(self, code: str, **kwargs: Any) -> AIResponse:
        """Optimize code for performance.

        Args:
            code: Code to optimize
            **kwargs: Additional arguments for optimization

        Returns:
            AIResponse: Optimized code

        Raises:
            PepperPyError: If optimization fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()
        prompt = (
            f"As an optimization specialist with the role of {self.config.role}, "
            f"please optimize this code:\n\n{code}\n\n"
            "Focus on:\n"
            "- Performance improvements\n"
            "- Resource usage\n"
            "- Algorithmic efficiency\n"
            "- Memory optimization"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Code optimization failed: {e}", cause=e)


class SecurityAgent(BaseAgent):
    """Agent responsible for security audits"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute security audit task"""
        return await self.audit_code(task, **kwargs)

    async def audit_code(self, code: str, **kwargs: Any) -> AIResponse:
        """Audit code for security issues.

        Args:
            code: Code to audit
            **kwargs: Additional arguments for security audit

        Returns:
            AIResponse: Security audit results

        Raises:
            PepperPyError: If security audit fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()
        prompt = (
            f"As a security specialist with the role of {self.config.role}, "
            f"please audit this code:\n\n{code}\n\n"
            "Focus on:\n"
            "- Security vulnerabilities\n"
            "- Best practices\n"
            "- Risk assessment\n"
            "- Security recommendations"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Security audit failed: {e}", cause=e)
