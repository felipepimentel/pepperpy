"""List component for console UI"""

from dataclasses import dataclass, field
from typing import Any, Dict, Generic, List, Optional, TypeVar

from rich.style import Style
from rich.text import Text

from pepperpy.console.ui.components.base import Component, ComponentConfig
from pepperpy.console.ui.styles import styles

T = TypeVar("T")


@dataclass
class ListItem(Generic[T]):
    """List item configuration"""

    value: T
    label: str
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class ListView(Component, Generic[T]):
    """List view component"""

    def __init__(self) -> None:
        config = ComponentConfig(
            style={
                "default": Style(color="white"),
                "selected": Style(color="cyan", bold=True),
                "disabled": Style(color="grey50"),
            },
            metadata={
                "show_bullets": True,
                "bullet_char": "•",
            },
        )
        super().__init__(config=config)
        self._items: List[ListItem[T]] = []
        self._selected_index = 0

    async def initialize(self) -> None:
        """Initialize list view"""
        self._selected_index = 0

    async def cleanup(self) -> None:
        """Cleanup list view"""
        self._items.clear()
        self._selected_index = 0

    async def handle_input(self, key: Any) -> bool:
        """Handle input event"""
        from pepperpy.console.ui.keyboard import DOWN, ENTER, UP

        if key == UP:
            self.select_previous()
            return True
        elif key == DOWN:
            self.select_next()
            return True
        elif key == ENTER:
            if self.selected_item and self.selected_item.enabled:
                return True
        return False

    def add_item(self, value: T, label: str, enabled: bool = True) -> None:
        """Add item to list

        Args:
            value: Item value
            label: Item label
            enabled: Whether item is enabled
        """
        item = ListItem(value=value, label=label, enabled=enabled)
        self._items.append(item)

    def clear(self) -> None:
        """Clear all items"""
        self._items.clear()
        self._selected_index = 0

    @property
    def selected_item(self) -> Optional[ListItem[T]]:
        """Get selected item"""
        if not self._items:
            return None
        return self._items[self._selected_index]

    def select_next(self) -> None:
        """Select next item"""
        if not self._items:
            return
        self._selected_index = (self._selected_index + 1) % len(self._items)

    def select_previous(self) -> None:
        """Select previous item"""
        if not self._items:
            return
        self._selected_index = (self._selected_index - 1) % len(self._items)

    def render(self) -> Text:
        """Render list view"""
        text = Text()

        for i, item in enumerate(self._items):
            if i > 0:
                text.append("\n")

            # Adicionar bullet se configurado
            if self.config.metadata.get("show_bullets", True):
                bullet = self.config.metadata.get("bullet_char", "•")
                text.append(f"{bullet} ", style=styles.apply("default"))

            # Determinar estilo do item
            if not item.enabled:
                style = styles.apply("muted")
            elif i == self._selected_index:
                style = styles.apply("primary")
            else:
                style = styles.apply("default")

            # Adicionar label do item
            text.append(item.label, style=style)

        return text
