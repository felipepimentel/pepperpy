"""Architect agent implementation"""

from typing import Any

from pepperpy.ai.types import AIResponse
from pepperpy.core.exceptions import PepperPyError

from .base import BaseAgent


class ArchitectAgent(BaseAgent):
    """Agent responsible for system architecture design"""

    async def design_architecture(self, requirements: str, **kwargs: Any) -> AIResponse:
        """Design system architecture based on requirements.

        Args:
            requirements: System requirements
            **kwargs: Additional arguments for architecture design

        Returns:
            AIResponse: Architecture design

        Raises:
            PepperPyError: If design fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()

        prompt = (
            f"As a system architect with the role of {self.config.role}, "
            f"please design an architecture for:\n\n{requirements}\n\n"
            "Include:\n"
            "- System components\n"
            "- Component interactions\n"
            "- Data flow\n"
            "- Technology stack\n"
            "- Scalability considerations"
        )

        if "constraints" in kwargs:
            prompt += f"\n\nConstraints:\n{kwargs['constraints']}"
        elif kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Architecture design failed: {e}", cause=e)

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute an architecture design task.

        Args:
            task: Design task description
            **kwargs: Additional arguments for task execution

        Returns:
            AIResponse: Architecture design

        Raises:
            PepperPyError: If execution fails
            RuntimeError: If agent is not initialized
        """
        return await self.design_architecture(task, **kwargs)
