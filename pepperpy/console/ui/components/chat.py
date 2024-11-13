"""Chat component for console UI"""

from typing import Any

from rich.style import Style
from rich.text import Text

from .base import Component, ComponentConfig


class ChatView(Component):
    """Chat view component"""

    def __init__(self) -> None:
        config = ComponentConfig(
            style={
                "system": Style(color="yellow"),
                "assistant": Style(color="green"),
                "user": Style(color="blue"),
                "timestamp": Style(color="grey50"),
            }
        )
        super().__init__(config)
        self._messages = []

    async def initialize(self) -> None:
        """Initialize chat view"""
        pass

    async def cleanup(self) -> None:
        """Cleanup chat view"""
        self._messages.clear()

    async def handle_input(self, key: Any) -> bool:
        """Handle input event"""
        return False

    def add_message(self, content: str, role: str) -> None:
        """Add message to chat"""
        self._messages.append({"content": content, "role": role})

    def render(self) -> Text:
        """Render chat view"""
        text = Text()

        for i, msg in enumerate(self._messages):
            if i > 0:
                text.append("\n")

            # Add role prefix
            role_style = self.config.style.get(msg["role"], Style())
            text.append(f"[{msg['role']}] ", style=role_style)

            # Add message content
            text.append(msg["content"])

        return text
