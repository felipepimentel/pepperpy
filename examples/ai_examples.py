"""AI examples demonstrating core capabilities"""

import asyncio

from dotenv import load_dotenv  # Importing dotenv

from pepperpy.ai import AIClient, AIConfig
from pepperpy.ai.types import AIResponse
from pepperpy.console import Console

load_dotenv()  # Loading environment variables

console = Console()


async def demonstrate_conversation() -> None:
    """Demonstrate conversation with AI"""
    try:
        console.info("🤖 Initializing AI Client...")

        # Create AI configuration
        ai_config = AIConfig.model_validate({})

        # Create AI client with the obtained configuration
        client = AIClient(config=ai_config)
        await client.initialize()

        try:
            console.info("Starting conversation...")

            # Ask about async/await
            response = await client.complete(
                "Hello! Can you help me understand how to use async/await in Python?"
            )
            console.info("AI Response:")
            console.print(response.content)

            # Ask about type hints
            response = await client.complete(
                "Now, can you explain the benefits of type hints in Python?"
            )
            console.info("AI Response:")
            console.print(response.content)

            # Ask about combining both
            response = await client.complete("How do type hints work with async functions?")
            console.info("AI Response:")
            console.print(response.content)

        finally:
            await client.cleanup()

    except Exception as e:
        console.error("Conversation failed", str(e))


async def demonstrate_streaming() -> None:
    """Demonstrate streaming responses"""
    try:
        console.info("🤖 Initializing Streaming...")

        # Create AI configuration
        ai_config = AIConfig.model_validate({})

        # Create AI client with the obtained configuration
        client = AIClient(config=ai_config)
        await client.initialize()

        try:
            console.info("Starting stream...")

            # Stream response about coroutines
            prompt = "Explain the concept of coroutines in Python"
            console.print(prompt)
            console.print("")

            # Corrigido: usando async for ao invés de await
            async for chunk in client.stream(prompt):
                if isinstance(chunk, AIResponse):
                    print(chunk.content, end="", flush=True)
                else:
                    print(chunk, end="", flush=True)
            print()  # New line after streaming

        finally:
            await client.cleanup()

    except Exception as e:
        console.error("Streaming failed", str(e))


async def main() -> None:
    """Run AI examples"""
    try:
        await demonstrate_conversation()
        await demonstrate_streaming()
    except KeyboardInterrupt:
        console.info("\nExamples finished! 👋")


if __name__ == "__main__":
    asyncio.run(main())
