"""Layout management for console UI"""

from typing import List

from rich.text import Text

from .components.base import Component


class Layout:
    """Layout manager for UI components"""

    def __init__(self):
        self._components: List[Component] = []

    async def initialize(self) -> None:
        """Initialize layout"""
        pass

    async def cleanup(self) -> None:
        """Cleanup layout"""
        pass

    def add(self, component: Component) -> None:
        """Add component to layout"""
        self._components.append(component)

    def remove(self, component: Component) -> None:
        """Remove component from layout"""
        if component in self._components:
            self._components.remove(component)

    def render(self) -> Text:
        """Render all components"""
        text = Text()
        for component in self._components:
            text.append(component.render())
            text.append("\n")
        return text
