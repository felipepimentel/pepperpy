"""Base agent implementation"""

from typing import Any

from pepperpy.core.module import BaseModule

from ..client import AIClient
from ..types import AIResponse
from .types import AgentConfig


class BaseAgent(BaseModule[AgentConfig]):
    """Base agent implementation"""

    def __init__(self, client: AIClient, config: AgentConfig, **kwargs: Any) -> None:
        """Initialize agent.
        
        Args:
            client: AI client instance
            config: Agent configuration
            **kwargs: Additional arguments
        """
        super().__init__(config)
        self.client = client
        self._kwargs = kwargs

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute agent task.
        
        Args:
            task: Task to execute
            **kwargs: Additional arguments
        
        Returns:
            AIResponse: Task execution result
        """
        if not self._initialized:
            await self.initialize()
        return await self._get_completion(task, **kwargs)

    async def _get_completion(self, prompt: str, **kwargs: Any) -> AIResponse:
        """Get completion from AI client.
        
        Args:
            prompt: Prompt to complete
            **kwargs: Additional arguments
            
        Returns:
            AIResponse: Completion result
        """
        return await self.client.complete(prompt)

    async def _initialize(self) -> None:
        """Initialize agent"""
        if self.client:
            await self.client.initialize()

    async def _cleanup(self) -> None:
        """Cleanup agent resources"""
        pass
