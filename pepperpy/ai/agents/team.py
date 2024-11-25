"""Team agent implementations"""

from typing import Any, List, Optional

from pepperpy.ai.types import AIResponse
from pepperpy.core.exceptions import PepperPyError

from .base import BaseAgent


class TeamAgent(BaseAgent):
    """Base class for team agents"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute team task.
        
        Args:
            task: Task to execute
            **kwargs: Additional arguments for task execution
            
        Returns:
            AIResponse: Task execution results
            
        Raises:
            PepperPyError: If task execution fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()
        prompt = (
            f"As a team member with role {self.config.role}, "
            f"please execute this task:\n\n{task}\n\n"
            "Include:\n"
            "- Task breakdown\n"
            "- Dependencies\n"
            "- Timeline\n"
            "- Expected results"
        )

        if kwargs:
            prompt += f"\n\nContext:\n{kwargs}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Team task failed: {e}", cause=e)


class TeamCoordinator(BaseAgent):
    """Agent responsible for team coordination"""

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute coordination task"""
        if isinstance(task, list):
            return await self.coordinate_team(task, **kwargs)
        return await self.coordinate_team([task], **kwargs)

    async def coordinate_team(
        self,
        tasks: List[str],
        team_size: Optional[int] = None,
        deadline: Optional[str] = None,
        priority: Optional[str] = None,
        **kwargs: Any
    ) -> AIResponse:
        """Coordinate team tasks.
        
        Args:
            tasks: List of tasks to coordinate
            team_size: Optional team size
            deadline: Optional deadline
            priority: Optional priority level
            **kwargs: Additional arguments for coordination
            
        Returns:
            AIResponse: Coordination results
            
        Raises:
            PepperPyError: If coordination fails
            RuntimeError: If agent is not initialized
        """
        self._ensure_initialized()
        
        tasks_str = "\n".join(f"- {task}" for task in tasks)
        prompt = (
            f"As a team coordinator with role {self.config.role}, "
            f"please coordinate these tasks:\n\n{tasks_str}\n\n"
            "Include:\n"
            "- Task assignments\n"
            "- Dependencies\n"
            "- Timeline\n"
            "- Communication plan"
        )

        context = {}
        if team_size is not None:
            context["team_size"] = team_size
        if deadline is not None:
            context["deadline"] = deadline
        if priority is not None:
            context["priority"] = priority
        context.update(kwargs)

        if context:
            prompt += f"\n\nContext:\n{context}"

        try:
            return await self._client.complete(prompt)
        except Exception as e:
            raise PepperPyError(f"Team coordination failed: {e}", cause=e)
