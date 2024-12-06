"""Layout component implementation."""

from dataclasses import dataclass, field
from typing import Any, Literal

from ..base.component import BaseComponent


@dataclass
class LayoutConfig:
    """Layout configuration."""

    direction: Literal["horizontal", "vertical"] = "vertical"
    spacing: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)


class Layout(BaseComponent):
    """Layout component."""

    def __init__(self, config: LayoutConfig | None = None) -> None:
        """Initialize layout."""
        super().__init__()
        self.config = config or LayoutConfig()
        self._children: list[BaseComponent] = []

    async def initialize(self) -> None:
        """Initialize layout."""
        await super().initialize()
        for child in self._children:
            await child.initialize()

    async def render(self) -> Any:
        """Render layout."""
        await super().render()
        return [await child.render() for child in self._children]

    async def cleanup(self) -> None:
        """Cleanup layout."""
        for child in self._children:
            await child.cleanup()
        await super().cleanup()

    async def split(self, *components: BaseComponent) -> None:
        """Split layout into components.

        Args:
            *components: Components to split layout into
        """
        self._children = list(components)
        if self._initialized:
            for child in self._children:
                await child.initialize()
