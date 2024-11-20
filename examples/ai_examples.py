"""AI examples demonstrating core capabilities"""

import asyncio

from pepperpy.ai import AIClient
from pepperpy.console import Console

console = Console()


class Conversation:
    """Conversation handler"""

    def __init__(self, client: AIClient) -> None:
        self._client = client
        self._history: list[str] = []

    async def send_message(self, message: str) -> str:
        """Send message and get response"""
        try:
            response = await self._client.complete(message)
            self._history.append(message)
            self._history.append(response.content)
            return response.content
        except Exception as e:
            raise RuntimeError(f"Failed to send message: {e}")

    async def clear_history(self) -> None:
        """Clear conversation history"""
        self._history.clear()


async def demonstrate_conversation() -> None:
    """Demonstrate conversation capabilities"""
    try:
        await console.info("🤖 Initializing AI Client...")

        # Create AI client with default configuration
        client = AIClient()
        await client.initialize()

        try:
            # Create conversation
            conversation = Conversation(client)

            # First interaction
            await console.info("Starting conversation...")
            response = await conversation.send_message(
                "Hello! Can you help me understand how to use async/await in Python?"
            )
            await console.info("AI Response:", content=response)

            # Clear history and start new topic
            await conversation.clear_history()
            response = await conversation.send_message(
                "Now, can you explain the benefits of type hints in Python?"
            )
            await console.info("AI Response:", content=response)

            # Follow-up question
            response = await conversation.send_message(
                "How do type hints work with async functions?"
            )
            await console.info("AI Response:", content=response)

        finally:
            await client.cleanup()

    except Exception as e:
        await console.error("Conversation failed", str(e))


async def demonstrate_streaming() -> None:
    """Demonstrate streaming capabilities"""
    try:
        await console.info("🤖 Initializing Streaming...")

        client = AIClient()
        await client.initialize()

        try:
            prompt = "Explain the concept of coroutines in Python"
            await console.info("Starting stream...")

            async for chunk in client.stream(prompt):
                print(chunk, end="", flush=True)
            print()  # New line after streaming

        finally:
            await client.cleanup()

    except Exception as e:
        await console.error("Streaming failed", str(e))


if __name__ == "__main__":
    try:
        asyncio.run(demonstrate_conversation())
        asyncio.run(demonstrate_streaming())
    except KeyboardInterrupt:
        print("\n\n⚠️ Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
