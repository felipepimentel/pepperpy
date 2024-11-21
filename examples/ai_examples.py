"""AI examples demonstrating core capabilities"""

import asyncio

from pepperpy.ai import AIClient
from pepperpy.ai.config import AIConfig
from pepperpy.ai.types import AIResponse
from pepperpy.console import Console

console = Console()


async def demonstrate_conversation() -> None:
    """Demonstrate conversation with AI"""
    try:
        await console.info("🤖 Initializing AI Client...")

        # Create AI configuration
        ai_config = AIConfig.get_default()

        # Create AI client
        client = AIClient(config=ai_config)
        await client.initialize()

        try:
            await console.info("Starting conversation...")

            # Ask about async/await
            response = await client.complete(
                "Hello! Can you help me understand how to use async/await in Python?"
            )
            await console.info("AI Response:", content=response.content)

            # Ask about type hints
            response = await client.complete(
                "Now, can you explain the benefits of type hints in Python?"
            )
            await console.info("AI Response:", content=response.content)

            # Ask about combining both
            response = await client.complete("How do type hints work with async functions?")
            await console.info("AI Response:", content=response.content)

        finally:
            await client.cleanup()

    except Exception as e:
        await console.error("Conversation failed", str(e))


async def demonstrate_streaming() -> None:
    """Demonstrate streaming responses"""
    try:
        await console.info("🤖 Initializing Streaming...")

        # Create AI client
        client = AIClient()
        await client.initialize()

        try:
            await console.info("Starting stream...")

            # Stream response about coroutines
            prompt = "Explain the concept of coroutines in Python"
            await console.print(prompt)
            await console.print("")

            async for chunk in client.stream(prompt):
                if isinstance(chunk, AIResponse):
                    print(chunk.content, end="", flush=True)
                else:
                    print(chunk, end="", flush=True)
            print()  # New line after streaming

        finally:
            await client.cleanup()

    except Exception as e:
        await console.error("Streaming failed", str(e))


async def main() -> None:
    """Run AI examples"""
    try:
        await demonstrate_conversation()
        await demonstrate_streaming()
    except KeyboardInterrupt:
        await console.info("\nExamples finished! 👋")


if __name__ == "__main__":
    asyncio.run(main())
