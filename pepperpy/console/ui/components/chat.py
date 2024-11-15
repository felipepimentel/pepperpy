"""Chat view component"""

from dataclasses import dataclass, field
from typing import Any, Literal

from rich.text import Text

from .base import Component

MessageType = Literal["system", "assistant", "user"]

@dataclass
class Message:
    """Chat message"""
    content: str
    type_: MessageType
    metadata: dict[str, Any] = field(default_factory=dict)

class ChatView(Component):
    """Chat view component"""
    
    def __init__(self):
        super().__init__()
        self._messages: list[Message] = []
        self._styles = {
            "system": "yellow bold",
            "assistant": "green",
            "user": "blue",
        }
        
    def add_message(self, content: str, type_: MessageType) -> None:
        """Add message to chat"""
        self._messages.append(Message(content, type_))
        
    def clear_messages(self) -> None:
        """Clear all messages"""
        self._messages.clear()
        
    def set_style(self, type_: MessageType, style: str) -> None:
        """Set style for message type"""
        self._styles[type_] = style
        
    async def render(self) -> Any:
        """Render chat view"""
        await super().render()
        
        text = Text()
        for msg in self._messages:
            style = self._styles.get(msg.type_, "default")
            text.append(f"{msg.content}\n", style=style)
            
        return text