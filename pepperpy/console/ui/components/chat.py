"""Chat component for console UI"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from rich.style import Style
from rich.text import Text

from pepperpy.console.ui.components.base import Component, ComponentConfig
from pepperpy.console.ui.styles import styles


@dataclass
class ChatMessage:
    """Chat message data"""

    content: str
    sender: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ChatView(Component):
    """Chat view component"""

    def __init__(self) -> None:
        config = ComponentConfig(
            style={
                "timestamp": Style(color="gray50", dim=True),
                "sender": Style(color="cyan", bold=True),
                "content": Style(color="white"),
                "system": Style(color="yellow"),
                "user": Style(color="green"),
                "assistant": Style(color="blue"),
            }
        )
        super().__init__(config=config)
        self._messages: List[ChatMessage] = []
        self._max_width = 80

    def add_message(
        self, content: str, sender: str, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add message to chat

        Args:
            content: Message content
            sender: Message sender
            metadata: Optional message metadata
        """
        message = ChatMessage(
            content=content,
            sender=sender,
            metadata=metadata or {},
        )
        self._messages.append(message)

    def clear(self) -> None:
        """Clear all messages"""
        self._messages.clear()

    def render(self) -> Text:
        """Render chat view"""
        text = Text()

        for i, message in enumerate(self._messages):
            if i > 0:
                text.append("\n\n")

            # Render timestamp
            timestamp = message.timestamp.strftime("%H:%M:%S")
            text.append(f"[{timestamp}] ", style=styles.apply("muted"))

            # Render sender
            sender_style = (
                "system"
                if message.sender == "system"
                else "user" if message.sender == "user" else "assistant"
            )
            text.append(f"{message.sender}: ", style=styles.apply(sender_style))

            # Render content
            # Quebrar o texto em linhas para respeitar a largura máxima
            words = message.content.split()
            current_line = []
            current_width = 0

            for word in words:
                word_width = len(word)
                if current_width + word_width + 1 > self._max_width:
                    # Adicionar a linha atual
                    if current_line:
                        text.append(" ".join(current_line) + "\n", style=styles.apply("default"))
                    current_line = [word]
                    current_width = word_width
                else:
                    current_line.append(word)
                    current_width += word_width + 1

            # Adicionar a última linha
            if current_line:
                text.append(" ".join(current_line), style=styles.apply("default"))

        return text

    def set_max_width(self, width: int) -> None:
        """Set maximum content width

        Args:
            width: Maximum width in characters
        """
        self._max_width = max(40, width)  # Mínimo de 40 caracteres
