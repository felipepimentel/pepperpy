"""Chat history component implementation"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from ..styles import Style, Theme
from .base import Component, ComponentConfig
from .richtext import RichText


@dataclass
class ChatMessage:
    """Chat message representation"""

    content: str
    sender: str
    timestamp: datetime = None
    metadata: dict = None
    is_user: bool = False


class ChatHistory(Component):
    """Component for displaying chat history"""

    def __init__(
        self,
        config: ComponentConfig,
        messages: List[ChatMessage] = None,
        show_timestamps: bool = True,
        show_sender: bool = True,
        theme: Optional[Theme] = None,
    ):
        super().__init__(config)
        self.messages = messages or []
        self.show_timestamps = show_timestamps
        self.show_sender = show_sender
        self.theme = theme or Theme(
            primary=Style(fg_color=(70, 130, 180)),  # User messages
            secondary=Style(fg_color=(60, 179, 113)),  # AI messages
            info=Style(fg_color=(169, 169, 169)),  # Timestamps
        )
        self._scroll_offset = 0
        self._visible_lines = 0

    async def add_message(self, message: ChatMessage) -> None:
        """Add new message to history"""
        if not message.timestamp:
            message.timestamp = datetime.now()
        self.messages.append(message)

        # Auto-scroll to bottom
        self._scroll_offset = max(0, len(self.messages) - self._visible_lines)
        await self.render()

    async def clear(self) -> None:
        """Clear chat history"""
        self.messages.clear()
        self._scroll_offset = 0
        await self.render()

    async def scroll_up(self) -> None:
        """Scroll chat history up"""
        if self._scroll_offset > 0:
            self._scroll_offset -= 1
            await self.render()

    async def scroll_down(self) -> None:
        """Scroll chat history down"""
        if self._scroll_offset < len(self.messages) - self._visible_lines:
            self._scroll_offset += 1
            await self.render()

    async def _setup(self) -> None:
        """Initialize chat history"""
        self._visible_lines = self.config.height or 10

    async def _cleanup(self) -> None:
        """Cleanup chat history"""
        pass

    async def render(self) -> None:
        """Render chat history"""
        if not self.config.visible:
            return

        # Calculate visible range
        start_idx = self._scroll_offset
        end_idx = min(start_idx + self._visible_lines, len(self.messages))

        # Clear display area
        for i in range(self._visible_lines):
            print(f"\033[{self.config.y + i};{self.config.x}H\033[K")

        current_y = self.config.y
        for idx in range(start_idx, end_idx):
            message = self.messages[idx]

            # Render message header
            if self.show_sender or self.show_timestamps:
                header_parts = []

                if self.show_sender:
                    style = self.theme.primary if message.is_user else self.theme.secondary
                    header_parts.append(f"{style.apply()}{message.sender}{style.reset()}")

                if self.show_timestamps and message.timestamp:
                    time_str = message.timestamp.strftime("%H:%M:%S")
                    header_parts.append(
                        f"{self.theme.info.apply()}{time_str}{self.theme.info.reset()}"
                    )

                print(f"\033[{current_y};{self.config.x}H{' | '.join(header_parts)}")
                current_y += 1

            # Render message content
            content_style = self.theme.primary if message.is_user else self.theme.secondary
            rich_text = RichText(
                config=ComponentConfig(
                    x=self.config.x + 2,
                    y=current_y,
                    width=self.config.width - 4 if self.config.width else None,
                    style=content_style,
                ),
                text=message.content,
                parse_markdown=True,
                word_wrap=True,
            )
            await rich_text.render()

            # Update position for next message
            current_y += rich_text._wrapped_lines.__len__() + 1

        # Render scrollbar if needed
        if len(self.messages) > self._visible_lines:
            scrollbar_height = self._visible_lines
            thumb_size = max(1, int(scrollbar_height * self._visible_lines / len(self.messages)))
            thumb_pos = int(scrollbar_height * self._scroll_offset / len(self.messages))

            for i in range(scrollbar_height):
                x = self.config.x + (self.config.width or 80) - 1
                print(f"\033[{self.config.y + i};{x}H", end="")

                if i >= thumb_pos and i < thumb_pos + thumb_size:
                    print("█", end="")
                else:
                    print("░", end="")
