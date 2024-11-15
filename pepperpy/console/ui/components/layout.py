"""Layout management for console UI"""

from collections.abc import Sequence
from typing import Any

from rich.layout import Layout as RichLayout
from rich.style import Style
from rich.text import Text

from .base import Component, ComponentConfig


class Layout(Component):
    """Layout manager for UI components"""

    def __init__(self):
        config = ComponentConfig(
            style={
                "border": Style(dim=True),
            },
        )
        super().__init__(config)
        self._layout = RichLayout()
        self._components: list[Component] = []

    async def initialize(self) -> None:
        """Initialize layout"""
        for component in self._components:
            await component.initialize()

    async def cleanup(self) -> None:
        """Cleanup layout"""
        for component in self._components:
            await component.cleanup()

    async def handle_input(self, key: Any) -> bool:
        """Handle input event"""
        for component in self._components:
            if await component.handle_input(key):
                return True
        return False

    def add(self, component: Component) -> None:
        """
        Add component to layout

        Args:
            component: Component to add

        """
        if component not in self._components:
            self._components.append(component)

    def remove(self, component: Component) -> None:
        """
        Remove component from layout

        Args:
            component: Component to remove

        """
        if component in self._components:
            self._components.remove(component)

    def split(
        self,
        *components: str | Component,
        direction: str = "vertical",
        ratios: Sequence[int] | None = None,
    ) -> None:
        """
        Split layout into multiple components

        Args:
            *components: Components to add to the layout
            direction: Split direction ("vertical" or "horizontal")
            ratios: Optional list of ratios for component sizes

        """
        self._components.extend(c for c in components if isinstance(c, Component))

        # Convert components to renderable objects
        renderables = []
        for component in components:
            if isinstance(component, Component):
                renderables.append(component.render())
            else:
                renderables.append(str(component))

        # Create sublayouts
        sublayouts = []
        for i, renderable in enumerate(renderables):
            sublayout = RichLayout(renderable)
            if ratios and i < len(ratios):
                sublayout.ratio = ratios[i]
            sublayouts.append(sublayout)

        # Split the layout
        if direction == "vertical":
            self._layout.split_column(*sublayouts)
        else:
            self._layout.split_row(*sublayouts)

    def render(self) -> Text:
        """Render layout"""
        # Ensure all components are rendered
        for component in self._components:
            if isinstance(component, Component):
                component.render()

        return Text.from_markup(str(self._layout))
