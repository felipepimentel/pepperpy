"""Chat view component for console UI"""

from typing import Literal

from rich.panel import Panel as RichPanel
from rich.text import Text

from pepperpy.console.ui.base import Component


class ChatView(Component):
    """Chat view component for displaying messages"""

    def __init__(self):
        super().__init__()
        self.messages: list[tuple[str, str]] = []

    def add_message(
        self, 
        content: str, 
        role: Literal["system", "assistant", "user"]
    ) -> None:
        """Add a message to the chat view.
        
        Args:
            content: Message content
            role: Role of the message sender (system/assistant/user)
        """
        self.messages.append((content, role))

    def render(self) -> RichPanel:
        """Render chat messages in a panel"""
        # Create formatted text for all messages
        text = Text()
        
        for i, (content, role) in enumerate(self.messages):
            # Add role prefix with appropriate color
            prefix = {
                "system": Text("🔧 System: ", style="bold blue"),
                "assistant": Text("🤖 Assistant: ", style="bold green"),
                "user": Text("👤 User: ", style="bold yellow")
            }.get(role, Text(f"{role}: ", style="bold"))
            
            # Add message content
            text.append(prefix)
            text.append(content)
            
            # Add newline between messages
            if i < len(self.messages) - 1:
                text.append("\n\n")

        # Return panel containing messages
        return RichPanel(
            text,
            title="Chat",
            border_style="blue"
        )