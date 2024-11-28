"""Example of a chat interface using pepperpy-console"""

import asyncio

from pepperpy_console.base import Console
from pepperpy_console.components import (
    Button,
    ChatView,
    Input,
    Layout,
    Panel,
)
from pepperpy_console.components.button import ButtonConfig


class ExampleInput(Input):
    """Example input implementation"""

    async def initialize(self) -> None:
        """Initialize input"""
        await super().initialize()

    async def cleanup(self) -> None:
        """Cleanup input"""
        await super().cleanup()


async def main() -> None:
    """Run chat interface example"""
    # Initialize components
    console = Console()
    chat_view = ChatView()
    input_field = ExampleInput()

    # Create callback for sending messages
    def send_callback() -> None:
        """Wrapper for send_message"""
        asyncio.create_task(send_message())

    send_button = Button(
        ButtonConfig(
            label="Send",
            callback=send_callback,
            enabled=True,
        )
    )

    # Create layout
    layout = Layout()
    await layout.split(
        Panel(chat_view),
        Panel(input_field),
        Panel(send_button),
        direction="vertical",
        ratios=[0.7, 0.2, 0.1],
    )

    async def send_message() -> None:
        """Send message"""
        user_message = input_field.value
        if not user_message:
            return

        # Add user message to chat
        chat_view.add_message(user_message, "user")
        input_field.value = ""

        # Simulate response
        await asyncio.sleep(0.5)
        response = f"You said: {user_message}"
        chat_view.add_message(response, "system")
        await layout.render()

    # Main loop
    try:
        console.info("Chat interface started. Press Ctrl+C to exit.")
        while True:
            await layout.render()
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        console.info("Shutting down chat interface...")
    finally:
        await layout.cleanup()
        console.info("Chat interface closed.")


if __name__ == "__main__":
    asyncio.run(main())
