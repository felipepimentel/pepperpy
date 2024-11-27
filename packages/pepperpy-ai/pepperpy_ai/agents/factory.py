"""Agent factory module"""

from typing import Any, Dict, Type, TypeVar

from bko.ai.agents.base import BaseAgent
from bko.ai.agents.config import AgentConfig

T = TypeVar("T", bound=BaseAgent)


class AgentFactory:
    """Factory for creating agents"""

    _registry: Dict[str, Type[BaseAgent]] = {}

    @classmethod
    def register(cls, name: str, agent_class: Type[T]) -> None:
        """Register agent class"""
        cls._registry[name] = agent_class

    @classmethod
    def create_agent(cls, name: str, config: AgentConfig, **kwargs: Any) -> BaseAgent:
        """Create agent instance"""
        if name not in cls._registry:
            raise ValueError(f"Unknown agent type: {name}")
        return cls._registry[name](config, **kwargs)
