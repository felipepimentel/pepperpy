"""Chat interface example."""

import asyncio

from pepperpy_console import ChatConfig, ChatView


async def main() -> None:
    """Run chat interface example."""
    chat = ChatView(
        config=ChatConfig(
            max_messages=50,
            show_timestamp=True,
        )
    )

    await chat.initialize()

    # Add some messages
    chat.add_message("Hello!", "User")
    chat.add_message("Hi there!", "Bot")
    chat.add_message("How are you?", "User")
    chat.add_message("I'm doing great, thanks for asking!", "Bot")

    # Render chat
    await chat.render()

    await chat.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
