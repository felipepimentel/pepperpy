"""List component implementation"""

from dataclasses import dataclass
from typing import Callable, List, Optional

from ..styles import Style
from .base import Component, ComponentConfig


@dataclass
class ListItem:
    """List item definition"""

    text: str
    value: any = None
    enabled: bool = True
    metadata: dict = None


class ListView(Component):
    """Scrollable list component"""

    def __init__(
        self,
        config: ComponentConfig,
        items: List[ListItem],
        on_select: Optional[Callable[[ListItem], None]] = None,
        show_scrollbar: bool = True,
        selected_style: Optional[Style] = None,
    ):
        super().__init__(config)
        self.items = items
        self.on_select = on_select
        self.show_scrollbar = show_scrollbar
        self.selected_style = selected_style or Style(bold=True)
        self._selected_index = 0
        self._scroll_offset = 0
        self._visible_items = config.height or 10

    @property
    def selected_item(self) -> Optional[ListItem]:
        """Get currently selected item"""
        if not self.items:
            return None
        return self.items[self._selected_index]

    async def _setup(self) -> None:
        """Initialize list view"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup list view"""
        pass

    async def render(self) -> None:
        """Render list view"""
        if not self.config.visible or not self.items:
            return

        style = self.config.style or Style()

        # Calculate visible range
        start = self._scroll_offset
        end = min(start + self._visible_items, len(self.items))

        # Render visible items
        for i in range(start, end):
            y = self.config.y + (i - start)
            item = self.items[i]

            # Move cursor
            print(f"\033[{y};{self.config.x}H", end="")

            # Apply styles
            if i == self._selected_index:
                print(f"{self.selected_style.apply()}", end="")
            elif not item.enabled:
                print(f"{style.disabled.apply()}", end="")
            else:
                print(f"{style.apply()}", end="")

            # Render item
            width = self.config.width or 40
            text = item.text
            if len(text) > width - 4:
                text = text[: width - 7] + "..."
            print(f"  {text:<{width-2}}", end="")

            print(f"{style.reset()}")

        # Render scrollbar
        if self.show_scrollbar and len(self.items) > self._visible_items:
            scrollbar_height = self._visible_items
            thumb_size = max(1, int(scrollbar_height * self._visible_items / len(self.items)))
            thumb_pos = int(scrollbar_height * self._scroll_offset / len(self.items))

            for i in range(scrollbar_height):
                y = self.config.y + i
                x = self.config.x + (self.config.width or 40) + 1
                print(f"\033[{y};{x}H│", end="")

                if i >= thumb_pos and i < thumb_pos + thumb_size:
                    print("█", end="")
                else:
                    print("░", end="")
