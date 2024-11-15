"""List view component"""

from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from rich.text import Text

from .base import Component

T = TypeVar("T")

@dataclass
class ListItem(Generic[T]):
    """List item configuration"""
    value: T
    label: str
    enabled: bool = True
    style: str = "default"

class ListView(Component, Generic[T]):
    """List view component for displaying items"""
    
    def __init__(self):
        super().__init__()
        self._items: list[ListItem[T]] = []
        self._selected_index: int = -1
        
    def add_item(self, value: T, label: str, enabled: bool = True,
                style: str = "default") -> None:
        """Add item to list"""
        self._items.append(ListItem(value, label, enabled, style))
        
    def remove_item(self, value: T) -> None:
        """Remove item from list"""
        self._items = [item for item in self._items if item.value != value]
        if self._selected_index >= len(self._items):
            self._selected_index = len(self._items) - 1
            
    def select_item(self, index: int) -> None:
        """Select item by index"""
        if 0 <= index < len(self._items):
            self._selected_index = index
            
    @property
    def selected_item(self) -> ListItem[T] | None:
        """Get selected item"""
        if 0 <= self._selected_index < len(self._items):
            return self._items[self._selected_index]
        return None
        
    async def render(self) -> Any:
        """Render list view"""
        await super().render()
        
        text = Text()
        for i, item in enumerate(self._items):
            # Add selection indicator
            prefix = ">" if i == self._selected_index else " "
            text.append(f"{prefix} ", style="bold")
            
            # Add item with style
            style = item.style
            if not item.enabled:
                style = "dim " + style
            text.append(f"{item.label}\n", style=style)
            
        return text 