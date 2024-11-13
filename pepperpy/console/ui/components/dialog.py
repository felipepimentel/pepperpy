"""Dialog component for console UI"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from rich.style import Style
from rich.text import Text

from pepperpy.console.ui.components.base import Component, ComponentConfig
from pepperpy.console.ui.keyboard import ENTER, ESCAPE, Key
from pepperpy.console.ui.styles import styles


@dataclass
class DialogButton:
    """Dialog button configuration"""

    label: str
    callback: Optional[Callable[[], None]] = None
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class Dialog(Component):
    """Dialog component"""

    def __init__(self) -> None:
        config = ComponentConfig(
            style={
                "title": Style(color="cyan", bold=True),
                "content": Style(color="white"),
                "button": Style(color="blue"),
                "button_focused": Style(color="cyan", bold=True),
                "button_disabled": Style(color="gray50", dim=True),
            }
        )
        super().__init__(config=config)
        self.title = ""
        self.content = ""
        self.buttons: List[DialogButton] = []
        self.focused_button = 0
        self.visible = True

    def add_button(self, label: str, callback: Optional[Callable[[], None]] = None) -> None:
        """Add button to dialog"""
        self.buttons.append(DialogButton(label=label, callback=callback))

    async def handle_input(self, key: Key) -> bool:
        """Handle input event"""
        if not self.visible or not self.buttons:
            return False

        if key == ENTER:
            button = self.buttons[self.focused_button]
            if button.enabled and button.callback:
                button.callback()
            return True

        if key == ESCAPE:
            self.visible = False
            return True

        return False

    def render(self) -> Text:
        """Render dialog"""
        if not self.visible:
            return Text()

        text = Text()

        # Render title
        if self.title:
            text.append(self.title + "\n", style=styles.apply("primary"))

        # Render content
        if self.content:
            text.append(self.content + "\n\n", style=styles.apply("default"))

        # Render buttons
        for i, button in enumerate(self.buttons):
            if i > 0:
                text.append(" ")

            style = (
                styles.apply("focused")
                if i == self.focused_button and button.enabled
                else styles.apply("muted" if not button.enabled else "default")
            )
            text.append(f"[ {button.label} ]", style=style)

        return text

    def show(self, title: str, content: str) -> None:
        """Show dialog with title and content"""
        self.title = title
        self.content = content
        self.visible = True
        self.focused_button = 0

    def hide(self) -> None:
        """Hide dialog"""
        self.visible = False
