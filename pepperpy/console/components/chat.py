"""Rich chat interface component"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text


@dataclass
class Message:
    """Chat message container"""

    text: str
    sender: str
    timestamp: datetime = datetime.now()
    style: Optional[str] = None


class Chat:
    """Interactive chat interface"""

    def __init__(self, console: Console):
        self._console = console
        self._messages: List[Message] = []
        self._styles = {
            "user": Style(color="blue"),
            "bot": Style(color="green"),
            "system": Style(color="yellow"),
        }

    def add_message(self, text: str, sender: str, style: Optional[str] = None) -> None:
        """Add message to chat"""
        msg = Message(text, sender, style=style or sender)
        self._messages.append(msg)
        self._render_message(msg)

    def clear(self) -> None:
        """Clear chat history"""
        self._messages.clear()
        self._console.clear()

    def _render_message(self, msg: Message) -> None:
        """Render single message"""
        style = self._styles.get(msg.style, Style())

        header = Text(f"{msg.sender} - {msg.timestamp:%H:%M:%S}", style=style)
        content = Text(msg.text)

        panel = Panel.fit(content, title=header, border_style=style)
        self._console.print(panel)
