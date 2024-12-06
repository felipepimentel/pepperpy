"""Menu component implementation."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from ..base.component import BaseComponent


@dataclass
class MenuConfig:
    """Menu configuration."""

    title: str = ""
    selected_style: str = "bold blue"
    metadata: dict[str, Any] = field(default_factory=dict)


class Menu(BaseComponent):
    """Menu component."""

    def __init__(self, config: MenuConfig | None = None) -> None:
        """Initialize menu."""
        super().__init__()
        self.config = config or MenuConfig()
        self._items: list[tuple[str, Callable[[], None]]] = []

    async def initialize(self) -> None:
        """Initialize menu."""
        await super().initialize()

    async def render(self) -> Any:
        """Render menu."""
        await super().render()
        return None

    async def cleanup(self) -> None:
        """Cleanup menu."""
        await super().cleanup()
