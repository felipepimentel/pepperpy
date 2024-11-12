"""Base component implementation"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

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

    @abstractmethod
    async def render(self) -> None:
        """Render component"""
        pass
