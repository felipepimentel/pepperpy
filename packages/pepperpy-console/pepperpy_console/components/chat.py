"""Chat component implementation."""

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from ..base.component import BaseComponent


@dataclass
class Message:
    """Chat message."""

    content: str
    sender: str
    timestamp: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatConfig:
    """Chat configuration."""

    max_messages: int = 100
    show_timestamp: bool = True
    show_sender: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


class ChatView(BaseComponent):
    """Chat view component."""

    def __init__(self, config: ChatConfig | None = None) -> None:
        """Initialize chat view.

        Args:
            config: Chat configuration
        """
        super().__init__()
        self.config = config or ChatConfig()
        self._messages: list[Message] = []

    async def initialize(self) -> None:
        """Initialize chat view."""
        await super().initialize()

    async def render(self) -> Any:
        """Render chat view.

        Returns:
            Rendered chat content
        """
        await super().render()
        # TODO: Implement chat rendering
        return None

    async def cleanup(self) -> None:
        """Cleanup chat view."""
        await super().cleanup()
        self._messages.clear()

    def add_message(self, content: str, sender: str) -> None:
        """Add message to chat.

        Args:
            content: Message content
            sender: Message sender
        """
        self._ensure_initialized()
        message = Message(
            content=content,
            sender=sender,
            timestamp=0.0,  # TODO: Add real timestamp
        )
        self._messages.append(message)
        if len(self._messages) > self.config.max_messages:
            self._messages.pop(0)

    def get_messages(self) -> Sequence[Message]:
        """Get chat messages.

        Returns:
            List of messages
        """
        self._ensure_initialized()
        return self._messages
