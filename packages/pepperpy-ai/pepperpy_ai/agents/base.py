"""Base agent implementation"""

from abc import ABC, abstractmethod
from typing import Any

from bko.ai.config.agent import AgentConfig
from bko.ai.providers.base import AIProvider
from bko.ai.types import AIResponse


class BaseAgent(ABC):
    """Base agent class"""

    def __init__(self, config: AgentConfig, client: AIProvider) -> None:
        """Initialize agent.

        Args:
            config: Agent configuration
            client: AI client
        """
        self.config = config
        self._client = client
        self._initialized = False

    @property
    def name(self) -> str:
        """Get agent name"""
        return self.config.name

    @property
    def role(self) -> str:
        """Get agent role"""
        return self.config.role

    @property
    def metadata(self) -> dict[str, Any]:
        """Get agent metadata"""
        return self.config.metadata

    @property
    def is_initialized(self) -> bool:
        """Check if agent is initialized"""
        return self._initialized

    def _ensure_initialized(self) -> None:
        """Ensure agent is initialized"""
        if not self._initialized:
            raise RuntimeError("Agent is not initialized")

    async def initialize(self) -> None:
        """Initialize agent"""
        if not self._initialized:
            await self._initialize()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup agent resources"""
        if self._initialized:
            await self._cleanup()
            self._initialized = False

    @abstractmethod
    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute task.

        Args:
            task: Task to execute
            **kwargs: Additional arguments for task execution

        Returns:
            AIResponse: Task execution results

        Raises:
            PepperPyError: If execution fails
            RuntimeError: If agent is not initialized
        """
        ...

    async def _initialize(self) -> None:
        """Initialize agent resources"""
        if not self._client.is_initialized:
            await self._client.initialize()

    async def _cleanup(self) -> None:
        """Cleanup agent resources"""
        await self._client.cleanup()
