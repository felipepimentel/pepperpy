"""Dialog component for console UI"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from rich.style import Style
from rich.text import Text

from .base import Component, ComponentConfig


@dataclass
class DialogButton:
    """Dialog button configuration"""

    label: str
    callback: Callable[[], None]
    enabled: bool = True


class Dialog(Component):
    """Dialog component"""

    def __init__(self) -> None:
        config = ComponentConfig(
            style={
                "title": Style(color="cyan", bold=True),
                "content": Style(color="white"),
                "button": Style(color="blue"),
                "button_selected": Style(color="blue", bold=True),
                "button_disabled": Style(color="grey50"),
                "border": Style(color="cyan"),
            },
        )
        super().__init__(config)
        self.title = ""
        self.content = ""
        self._buttons: list[DialogButton] = []
        self._selected_button = 0

    async def initialize(self) -> None:
        """Initialize dialog"""
        self._selected_button = 0

    async def cleanup(self) -> None:
        """Cleanup dialog"""
        self._buttons.clear()
        self._selected_button = 0

    async def handle_input(self, key: Any) -> bool:
        """Handle input event"""
        from pepperpy.console.ui.keyboard import DOWN, ENTER, UP

        if key == UP or key == DOWN:
            if self._buttons:
                self._selected_button = (self._selected_button + (1 if key == DOWN else -1)) % len(
                    self._buttons,
                )
            return True

        if key == ENTER:
            if self._buttons and self._buttons[self._selected_button].enabled:
                self._buttons[self._selected_button].callback()
            return True

        return False

    def add_button(self, label: str, callback: Callable[[], None], enabled: bool = True) -> None:
        """Add button to dialog"""
        self._buttons.append(DialogButton(label=label, callback=callback, enabled=enabled))

    def render(self) -> Text:
        """Render dialog"""
        text = Text()

        # Render title
        if self.title:
            text.append("┌─ ", style=self.config.style.get("border"))
            text.append(self.title, style=self.config.style.get("title"))
            text.append(" ", style=self.config.style.get("border"))
            text.append("─" * (40 - len(self.title)), style=self.config.style.get("border"))
            text.append("┐\n", style=self.config.style.get("border"))
        else:
            text.append("┌" + "─" * 42 + "┐\n", style=self.config.style.get("border"))

        # Render content
        if self.content:
            text.append("│ ", style=self.config.style.get("border"))
            text.append(self.content, style=self.config.style.get("content"))
            text.append(" " * (40 - len(self.content)), style=self.config.style.get("border"))
            text.append(" │\n", style=self.config.style.get("border"))

        # Render buttons
        if self._buttons:
            text.append("│ ", style=self.config.style.get("border"))
            for i, button in enumerate(self._buttons):
                if i > 0:
                    text.append(" | ")

                if not button.enabled:
                    style = self.config.style.get("button_disabled")
                elif i == self._selected_button:
                    style = self.config.style.get("button_selected")
                else:
                    style = self.config.style.get("button")

                text.append(button.label, style=style)

            text.append(" " * (40 - sum(len(b.label) + 3 for b in self._buttons) + 3))
            text.append(" │\n", style=self.config.style.get("border"))

        # Render bottom border
        text.append("└" + "─" * 42 + "┘", style=self.config.style.get("border"))

        return text
