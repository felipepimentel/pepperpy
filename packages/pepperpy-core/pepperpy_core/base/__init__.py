"""Base classes for PepperPy Core"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# Define TypeVar for proper generic typing
T_Config = TypeVar("T_Config")


class Component(ABC, Generic[T_Config]):
    """Base component class"""

    def __init__(self, config: T_Config | None = None) -> None:
        self.config = config

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize component"""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup component resources"""
        pass
