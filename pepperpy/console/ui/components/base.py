"""Base component implementation"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Tuple

from ..styles import Style


@dataclass
class ComponentConfig:
    """Base configuration for components"""

    x: int = 0
    y: int = 0
    width: Optional[int] = None
    height: Optional[int] = None
    style: Optional[Style] = None
    enabled: bool = True
    visible: bool = True


class Component(ABC):
    """Base class for UI components"""

    def __init__(self, config: ComponentConfig):
        self.config = config
        self._initialized = False

    @property
    def position(self) -> Tuple[int, int]:
        """Get component position"""
        return (self.config.x, self.config.y)

    @property
    def size(self) -> Tuple[Optional[int], Optional[int]]:
        """Get component size"""
        return (self.config.width, self.config.height)

    async def initialize(self) -> None:
        """Initialize component"""
        if self._initialized:
            return
        await self._setup()
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup component resources"""
        if not self._initialized:
            return
        await self._cleanup()
        self._initialized = False

    @abstractmethod
    async def _setup(self) -> None:
        """Component-specific initialization"""
        pass

    @abstractmethod
    async def _cleanup(self) -> None:
        """Component-specific cleanup"""
        pass

    @abstractmethod
    async def render(self) -> None:
        """Render component"""
        pass
