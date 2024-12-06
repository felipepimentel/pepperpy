"""Button component"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from rich.text import Text

from .base import Component


@dataclass
class ButtonConfig:
    """Button configuration"""

    label: str
    callback: Callable[[], None]
    enabled: bool = True


class Button(Component):
    """Button component"""

    def __init__(self, config: ButtonConfig) -> None:
        """Initialize button."""
        super().__init__()
        self.config = config

    async def initialize(self) -> None:
        """Initialize button"""
        await super().initialize()

    async def render(self) -> Any:
        """Render button"""
        await super().render()

        return Text(self.config.label)

    async def click(self) -> None:
        """Handle button click"""
        if self.config.enabled:
            self.config.callback()

    async def cleanup(self) -> None:
        """Cleanup button resources"""
        await super().cleanup()
