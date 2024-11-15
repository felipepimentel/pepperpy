"""Base components for console UI"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from rich.text import Text


@dataclass
class ComponentConfig:
    """Component configuration"""

    style: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    visible: bool = True
    enabled: bool = True

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.metadata.get(key, default)


class Component(ABC):
    """Base component class"""

    def __init__(self, config: ComponentConfig) -> None:
        self.config = config

    @abstractmethod
    def render(self) -> Text:
        """
        Render component

        Returns:
            Text: Rendered component

        """

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize component"""

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup component"""

    @abstractmethod
    async def handle_input(self, key: Any) -> bool:
        """
        Handle input event

        Args:
            key: Input key

        Returns:
            bool: True if input was handled

        """
        return False
