"""Management agent implementations"""

from typing import Any

from bko.ai.types import AIResponse
from bko.core.exceptions import PepperPyError

from .base import BaseAgent


class ProjectManagerAgent(BaseAgent):
    """Project manager agent implementation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute project management task"""
        return await self.coordinate(task, **kwargs)

    async def coordinate(self, tasks: list[str] | str, **kwargs: Any) -> AIResponse:
        """Coordinate project activities.

        Args:
            tasks: Tasks to coordinate
            **kwargs: Additional arguments for coordination

        Returns:
            AIResponse: Coordination plan

        Raises:
            PepperPyError: If coordination fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()

        if isinstance(tasks, list):
            tasks_str = "\n".join(f"- {task}" for task in tasks)
        else:
            tasks_str = tasks

        prompt = (
            f"As a project manager with the role of {self.config.role}, "
            f"please coordinate these tasks:\n\n{tasks_str}\n\n"
            "Provide:\n"
            "- Task dependencies\n"
            "- Resource assignments\n"
            "- Timeline coordination\n"
            "- Communication plan"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Project coordination failed: {e}", cause=e)


class QualityEngineerAgent(BaseAgent):
    """Quality engineer agent implementation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute quality engineering task"""
        return await self.assess_quality(task, **kwargs)

    async def assess_quality(self, project: str, **kwargs: Any) -> AIResponse:
        """Assess project quality.

        Args:
            project: Project to assess
            **kwargs: Additional arguments for quality assessment

        Returns:
            AIResponse: Quality assessment

        Raises:
            PepperPyError: If assessment fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()
        prompt = (
            f"As a quality engineer with the role of {self.config.role}, "
            f"please assess the quality of:\n\n{project}\n\n"
            "Include:\n"
            "- Quality metrics\n"
            "- Compliance assessment\n"
            "- Areas for improvement\n"
            "- Recommendations"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Quality assessment failed: {e}", cause=e)


class DevOpsAgent(BaseAgent):
    """DevOps agent implementation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute DevOps task"""
        return await self.plan_deployment(task, **kwargs)

    async def plan_deployment(self, project: str, **kwargs: Any) -> AIResponse:
        """Plan project deployment.

        Args:
            project: Project to deploy
            **kwargs: Additional arguments for deployment planning

        Returns:
            AIResponse: Deployment plan

        Raises:
            PepperPyError: If planning fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()
        prompt = (
            f"As a DevOps engineer with the role of {self.config.role}, "
            f"please create a deployment plan for:\n\n{project}\n\n"
            "Include:\n"
            "- Infrastructure requirements\n"
            "- Deployment steps\n"
            "- Monitoring setup\n"
            "- Rollback procedures"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Deployment planning failed: {e}", cause=e)


class ComplianceAgent(BaseAgent):
    """Compliance agent implementation"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute compliance check task"""
        return await self.check(task, **kwargs)

    async def check(self, task: str, **kwargs: Any) -> AIResponse:
        """Check compliance requirements.

        Args:
            task: Task to check
            **kwargs: Additional arguments for compliance check

        Returns:
            AIResponse: Compliance check results

        Raises:
            PepperPyError: If compliance check fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()

        prompt = (
            f"As a compliance officer with the role of {self.config.role}, "
            f"please check compliance for:\n\n{task}\n\n"
            "Include:\n"
            "- Regulatory requirements\n"
            "- Policy compliance\n"
            "- Risk assessment\n"
            "- Recommendations\n"
            "- Documentation needs"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Compliance check failed: {e}", cause=e)

    # Alias for backward compatibility
    check_compliance = check
