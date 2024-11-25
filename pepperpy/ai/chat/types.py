"""Chat types module"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class ChatRole(str, Enum):
    """Chat role enumeration"""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    FUNCTION = "function"


@dataclass
class ChatMessage:
    """Chat message data class"""

    role: ChatRole
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate message content"""
        if not self.content:
            raise ValueError("Content cannot be empty")

    def __str__(self) -> str:
        """Get string representation"""
        return (
            f"ChatMessage(role={self.role.value}, content={self.content}, "
            f"metadata={self.metadata})"
        )


@dataclass
class ChatHistory:
    """Chat history data class"""

    messages: List[ChatMessage] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, message: ChatMessage) -> None:
        """Add message to history"""
        self.messages.append(message)

    def clear(self) -> None:
        """Clear message history"""
        self.messages.clear()

    def __str__(self) -> str:
        """Get string representation"""
        messages_str = ", ".join(str(msg) for msg in self.messages)
        return f"ChatHistory(messages=[{messages_str}], metadata={self.metadata})"


@dataclass
class ChatMetadata:
    """Chat metadata data class"""

    session_id: str
    user_id: str
    context: Dict[str, Any] = field(default_factory=dict)
    settings: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate metadata fields"""
        if not self.session_id:
            raise ValueError("Session ID cannot be empty")
        if not self.user_id:
            raise ValueError("User ID cannot be empty")

    def __str__(self) -> str:
        """Get string representation"""
        return (
            f"ChatMetadata(session_id={self.session_id}, user_id={self.user_id}, "
            f"context={self.context}, settings={self.settings})"
        )
