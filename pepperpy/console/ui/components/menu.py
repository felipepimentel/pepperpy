"""Menu component implementation"""

from dataclasses import dataclass
from typing import Callable, List, Optional

from ..styles import Style
from .base import Component, ComponentConfig


@dataclass
class MenuItem:
    """Menu item definition"""

    label: str
    value: str
    enabled: bool = True
    on_select: Optional[Callable[[], None]] = None


class Menu(Component):
    """Menu component"""

    def __init__(
        self,
        config: ComponentConfig,
        items: List[MenuItem],
        on_select: Optional[Callable[[MenuItem], None]] = None,
    ):
        super().__init__(config)
        self.items = items
        self.on_select = on_select
        self._selected_index = 0

    @property
    def selected_item(self) -> Optional[MenuItem]:
        """Get currently selected item"""
        if not self.items:
            return None
        return self.items[self._selected_index]

    async def _setup(self) -> None:
        """Initialize menu"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup menu"""
        pass

    async def render(self) -> None:
        """Render menu component"""
        if not self.config.visible:
            return

        style = self.config.style or Style()

        for i, item in enumerate(self.items):
            # Move cursor
            print(f"\033[{self.config.y + i};{self.config.x}H", end="")

            # Apply styles
            if i == self._selected_index:
                print(f"{style.apply()}> ", end="")
            else:
                print("  ", end="")

            # Render item
            if item.enabled:
                print(f"{item.label}{style.reset()}")
            else:
                print(f"{style.disabled.apply()}{item.label}{style.reset()}")
